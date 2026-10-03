"""Phase 3: apply the curated overlay to the normalized model.

Adds global statuses to source records and creates compiler-level records
(global:*) for historical beliefs, belief transitions, decision patterns,
global contradictions, global open loops, recurring lessons, interests and
voice examples. Source records are annotated, never rewritten.
"""
from __future__ import annotations

import re

import curated as C


def _add(model, rec):
    model["records"][rec["id"]] = rec
    model["by_kind"].setdefault(rec["type"], []).append(rec)


def reconcile(model: dict) -> dict:
    P = C.PROJECT
    R = model["records"]

    # beliefs
    for lid, ov in C.BELIEFS.items():
        rec = R[f"{P}:{lid}"]
        rec.update(global_status=ov["status"], first_observed=ov["first"], last_observed=ov["last"],
                   associated_decisions=[f"{P}:{d}" for d in ov["decisions"]],
                   contradicting_evidence=ov["contradicting"], classification=ov["cls"],
                   observed_in_projects=ov["projects"], compiler_note=ov["note"])

    # decisions
    for lid, (status, outcome, reversal) in C.DECISIONS.items():
        rec = R[f"{P}:{lid}"]
        rec.update(global_status=status, outcome=outcome, later_reversal=reversal,
                   classification="PROJECT-SPECIFIC")

    # failures
    for lid, changed in C.FAILURE_CHANGED.items():
        R[f"{P}:{lid}"]["changed_later_behavior"] = changed
    for rl in C.RECURRING_LESSONS:
        for f in rl["failures"]:
            R[f"{P}:{f}"].setdefault("recurring_lessons", []).append(f"global:{rl['id']}")

    # contradictions
    for lid, status in C.CONTRADICTION_STATUS.items():
        R[f"{P}:{lid}"]["global_status"] = status

    # compiler-level records
    for gid, stmt, status, first, last, refs, note in C.HISTORICAL_BELIEFS:
        _add(model, dict(id=f"global:{gid}", type="belief", statement=stmt, global_status=status,
                         first_observed=first, last_observed=last, refs=refs, compiler_note=note,
                         kind="RECONSTRUCTED", confidence="MEDIUM", project=P, classification="PROJECT-SPECIFIC",
                         source={"derived_from": refs}))
    for t in C.TRANSITIONS:
        _add(model, dict(t, id=f"global:{t['id']}", type="belief_transition", project=P,
                         confidence="HIGH" if "UNRESOLVED" not in t["status"] else "MEDIUM",
                         source={"derived_from": t["refs"]}))
    for d in C.DECISION_PATTERNS:
        _add(model, dict(d, id=f"global:{d['id']}", type="decision_pattern", project=P,
                         source={"derived_from": d["evidence"]}))
    for g in C.GLOBAL_CONTRADICTIONS:
        _add(model, dict(g, id=f"global:{g['id']}", type="contradiction", project=P,
                         source={"derived_from": g["refs"]}))
    for o in C.GLOBAL_OPEN_LOOPS:
        _add(model, dict(o, id=f"global:{o['id']}", type="open_loop", project="global",
                         source={"derived_from": o["refs"]}))
    for rl in C.RECURRING_LESSONS:
        _add(model, dict(rl, id=f"global:{rl['id']}", type="recurring_lesson", project=P,
                         source={"derived_from": rl["refs"] + [f"{P}:{f}" for f in rl["failures"]]}))
    for p in C.PROJECTS:
        _add(model, dict(p, id=f"global:P-{p['id']}".replace("global:P-", "project:"), type="project",
                         source={"derived_from": p["refs"]}))

    # interests: frequency computed from source records
    texts = [(r, " ".join(str(r.get(k, "")) for k in ("text", "title", "statement", "event", "question",
                                                       "pattern", "meaning", "understanding")).lower())
             for r in list(R.values()) if r["id"].startswith(f"{P}:")]
    for iid, name, kws, kind, trend, note in C.INTERESTS:
        hits = [r for r, t in texts if any(k in t for k in kws)]
        dates = sorted(d for d in (r.get("date") for r in hits) if d and re.match(r"\d{4}-\d\d", d))
        _add(model, dict(id=f"global:{iid}", type="interest", name=name, keywords=kws, nature=kind,
                         trend=trend, compiler_note=note, frequency=len(hits),
                         by_type={t: sum(1 for r in hits if r["type"] == t) for t in sorted({r["type"] for r in hits})},
                         first_dated=dates[0] if dates else None, last_dated=dates[-1] if dates else None,
                         sample_refs=[r["id"] for r in hits[:8]], project=P,
                         source={"derived_from": [r["id"] for r in hits[:8]]}))

    # voice examples: locate the exact excerpt in the source file
    root = model["projects"][P]["root"]
    from pathlib import Path
    for vid, cats, prov, fname, excerpt, why in C.VOICE_EXAMPLES:
        lines = (Path(root) / fname).read_text(encoding="utf-8").splitlines()
        line = next((i for i, l in enumerate(lines, 1) if excerpt in l), None)
        if line is None:  # excerpt may wrap across two lines in the source
            joined = [l + " " + (lines[i + 1] if i + 1 < len(lines) else "") for i, l in enumerate(lines)]
            line = next((i for i, l in enumerate(joined, 1) if excerpt in re.sub(r"\s+", " ", l)), None)
        _add(model, dict(id=f"global:{vid}", type="voice_example", categories=cats, provenance=prov,
                         excerpt=excerpt, why=why, project=P, verified=line is not None,
                         source={"root": root, "file": fname, "line": line}))
    return model
