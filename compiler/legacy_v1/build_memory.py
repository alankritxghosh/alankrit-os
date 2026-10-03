"""Phase 5: machine-readable memory (memory/*.jsonl).

Uniform envelope for every row:
  id, type, content, status, confidence, date{first,last,raw}, project, source_ref, extra
`source_ref` is "file:line" for parsed records or a list of record ids for
compiler-derived ones. Nothing is written that the validator's secret scan rejects.
"""
from __future__ import annotations

import curated as C
import json

from common import write_jsonl


def _src(r):
    s = r.get("source", {})
    if "derived_from" in s:
        return s["derived_from"]
    return f"{s.get('file')}:{s.get('line')}"


def _row(r, content, status=None, conf=None, first=None, last=None, raw=None, **extra):
    return {
        "id": r["id"], "type": r["type"], "content": content,
        "status": status or r.get("global_status") or r.get("status") or "RECORDED",
        "confidence": conf or r.get("confidence") or "UNSTATED",
        "date": {"first": first or r.get("first_observed") or r.get("date"),
                 "last": last or r.get("last_observed") or r.get("date"),
                 "raw": raw or r.get("date_raw")},
        "project": r.get("project"), "source_ref": _src(r), "extra": extra,
    }


# v2 extractions ship their own memory/; map their file names onto the global files
SHIPPED_MAP = {"facts": "facts", "decisions": "decisions", "beliefs": "beliefs", "episodes": "episodes",
               "lessons": "lessons", "failures": "lessons", "open_loops": "open_loops",
               "contradictions": "contradictions", "voice_examples": "voice_examples"}


def _shipped(model):
    from pathlib import Path
    out = {}
    for slug_, p in model["projects"].items():
        mem = Path(p["root"]) / "memory"
        if not mem.is_dir():
            continue
        for f in sorted(mem.glob("*.jsonl")):
            target = SHIPPED_MAP.get(f.stem)
            if not target:
                continue  # relationships are merged by build_graph
            for line in f.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    row = json.loads(line)
                    row.setdefault("source_ref", f"{slug_}/{row.get('source_file')}:{row.get('source_line')}")
                    row["shipped_by_extraction"] = slug_
                    out.setdefault(target, []).append(row)
    return out


def build(model: dict) -> dict:
    import json as _json  # noqa: F401
    shipped = _shipped(model)
    shipped_projects = {r["shipped_by_extraction"] for rows in shipped.values() for r in rows}
    R = [r for r in model["records"].values() if r.get("project") not in shipped_projects]
    of = lambda *types: [r for r in R if r["type"] in types]
    out = {}

    facts = []
    for r in of("fact"):
        if len(r["text"]) > 60 and not r["text"].rstrip().endswith(":"):
            facts.append(_row(r, r["text"], status="FACT"))
    for r in of("definition"):
        facts.append(_row(r, f"{r['term']}: {r['meaning']}", status=r["status"].upper() or "RECORDED", conf="HIGH",
                          related=r.get("related")))
    for r in of("project_note", "identity_note", "working_style_note"):
        if "`FACT`" in r["text"]:
            continue  # already captured as a tagged fact record
        facts.append(_row(r, r["text"], status="OBSERVATION", heading=r.get("heading")))
    for r in of("transferable_insight"):
        facts.append(_row(r, r["text"], status="TRANSFERABLE_CANDIDATE", heading=r.get("heading")))
    out["facts"] = facts

    out["beliefs"] = [
        _row(r, r.get("statement"), domain=r.get("domain"), kind=r.get("kind"), classification=r.get("classification"),
             associated_decisions=r.get("associated_decisions"), contradicting_evidence=r.get("contradicting_evidence"),
             observed_in_projects=r.get("observed_in_projects"), note=r.get("compiler_note"),
             source_detail=r.get("text"), refs=r.get("refs"))
        for r in of("belief")
    ] + [
        _row(r, f"{r['topic']}: {r['earlier']} -> {r['new']}", status=r["status"], refs=r["refs"],
             observation=r["observation"], reconsideration=r["reconsideration"])
        for r in of("belief_transition")
    ]

    out["decisions"] = [
        _row(r, r["title"], conf=r.get("confidence"), outcome=r.get("outcome"), later_reversal=r.get("later_reversal"),
             fields=r.get("fields"), status_as_recorded=r.get("status_raw"))
        for r in of("decision")
    ] + [
        _row(r, r["pattern"], status=r["persistence"], conf="MEDIUM", evidence=r["evidence"], domains=r["domains"])
        for r in of("decision_pattern")
    ]

    out["episodes"] = [_row(r, r["event"], status="HISTORICAL", conf="HIGH", why=r.get("why"),
                            cited=r.get("source_ref")) for r in of("episode")] + [
        _row(r, f"{r['title']} {r['text']}", status="PHASE", conf="HIGH") for r in of("phase")]

    out["projects"] = [_row(r, r["purpose"], status=r["status"], conf=r["evidence_level"], raw=r["period"],
                            name=r["name"], goals=r["goals"], pivots=r["pivots"], technologies=r["technologies"],
                            unresolved=r["unresolved"], extracted=r["extracted"]) for r in of("project")]
    for i, (name, desc, ref) in enumerate(C.MENTIONED_PROJECTS, 1):
        out["projects"].append({"id": f"project:mentioned-{i:02d}", "type": "project", "content": f"{name}: {desc}",
                                "status": "MENTIONED_ONLY (not extracted)", "confidence": "LOW",
                                "date": {"first": None, "last": None, "raw": None}, "project": None,
                                "source_ref": [ref], "extra": {"name": name}})

    out["interests"] = [_row(r, r["name"], status=r["trend"], conf="MEDIUM", first=r["first_dated"], last=r["last_dated"],
                             nature=r["nature"], frequency=r["frequency"], by_type=r["by_type"], note=r["compiler_note"])
                        for r in of("interest")]

    out["lessons"] = [
        _row(r, f"{r['title']}. {r['text']}".strip(), status="FAILURE", category=r.get("category"),
             changed_later_behavior=r.get("changed_later_behavior"), recurring_lessons=r.get("recurring_lessons"))
        for r in of("failure")
    ] + [_row(r, r["text"], status="LESSON", conf="HIGH") for r in of("lesson")] + [
        _row(r, r["text"], status="ABANDONED_OR_NOT_BUILT", conf="HIGH") for r in of("abandoned")
    ] + [
        _row(r, r["lesson"], status="RECURRING", conf="HIGH" if len(r["failures"]) > 2 else "MEDIUM",
             failures=r["failures"], changed=r["changed"], reappeared=r["reappeared"])
        for r in of("recurring_lesson")
    ]

    out["contradictions"] = [
        _row(r, r.get("title") or f"{r['a']} || {r['b']}", detail=r.get("text"), kind=r.get("kind"),
             position_a=r.get("a"), position_b=r.get("b"), when_a=r.get("when_a"), when_b=r.get("when_b"),
             explanation=r.get("explanation"))
        for r in of("contradiction")
    ]

    out["open_loops"] = [
        _row(r, r.get("question") or r.get("q"), why=r.get("why"), understanding=r.get("understanding"),
             next_step=r.get("next_step"), importance=r.get("importance"),
             first=r.get("first"), last=r.get("last"))
        for r in of("open_loop")
    ]

    out["voice_examples"] = [
        _row(r, r["excerpt"], status=r["provenance"], conf="HIGH" if r["verified"] else "UNVERIFIED",
             categories=r["categories"], why=r["why"])
        for r in of("voice_example")
    ] + [_row(r, r["text"], status="VOICE_RULE_OR_TRAIT", heading=r.get("heading")) for r in of("voice_rule")]

    for name, rows in shipped.items():
        out.setdefault(name, []).extend(rows)
    for name, rows in out.items():
        write_jsonl(f"memory/{name}.jsonl", rows)
    model["memory"] = out
    return model
