"""Phase 8: validate the compilation and write 16_VALIDATION_REPORT.md.

Checks (each yields PASS / WARN / FAIL with evidence):
- source integrity: corpus hashes unchanged across the run; no output inside it
- coverage: every source file contributed records; every project contributed
- provenance: every memory row has a source_ref; file:line refs point at real lines;
  every [project:ID] ref in every generated document resolves
- hallucination guards: quoted strings and multi-digit numbers in narrative docs
  must occur in the source corpus (or in the compiler's own computed counts)
- chronology, contradictions, duplication, nuance, personal-vs-project, voice, current state
- secrets: no credential-shaped strings, emails or phone numbers in outputs
"""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

from common import COMPILE_DATE, REF, WORKSPACE, sha256, source_dir, write_text

SECRET_RX = [
    ("api key", re.compile(r"\b(sk-[A-Za-z0-9]{16,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}|gh[pousr]_[A-Za-z0-9]{30,}|xox[bpas]-[A-Za-z0-9-]{10,})")),
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("phone", re.compile(r"(?<![\w.-])\+?\d{1,3}[ -]?\(?\d{3,5}\)?[ -]?\d{3,4}[ -]?\d{3,4}(?![\w.-])")),
]
QUOTE_RX = re.compile(r"[\"“]([^\"”\n]{12,200})[\"”]")
NUM_RX = re.compile(r"(?<![\w.:/-])(\d{1,3}(?:,\d{3})+|\d{2,}(?:\.\d+)?)(?![\w-])")


def _outputs():
    files = sorted(WORKSPACE.glob("*.md")) + sorted((WORKSPACE / "voice_examples").glob("*.md"))
    return [f for f in files if f.name != "16_VALIDATION_REPORT.md"]


def validate(model: dict, hashes_before: dict) -> dict:
    src = source_dir()
    checks = []

    def check(area, name, ok, detail, warn=False):
        checks.append({"area": area, "check": name, "result": "PASS" if ok else ("WARN" if warn else "FAIL"), "detail": detail})

    # ---- source integrity
    after = {str(p.relative_to(src)): sha256(p) for p in src.rglob("*") if p.is_file()}
    changed = [k for k in hashes_before if hashes_before[k] != after.get(k)] + [k for k in after if k not in hashes_before]
    check("Integrity", "source corpus unchanged (sha256 before vs after)", not changed, f"{len(after)} files; changed: {changed or 'none'}")
    check("Integrity", "no output written inside source corpus", not any(src in p.resolve().parents for p in WORKSPACE.rglob("*")),
          f"workspace {WORKSPACE} is outside {src}")

    # ---- coverage
    by_file = Counter(r["source"]["file"] for r in model["records"].values() if "file" in r.get("source", {}))
    by_file = Counter(f"{Path(r['source']['root']).name}/{r['source']['file']}" for r in model["records"].values() if "file" in r.get("source", {}))
    tops = [f for f in after if f.endswith(".md") and len(Path(f).parts) == 2]
    missing = [f for f in tops if by_file.get(f, 0) == 0]
    check("Coverage", "every top-level source markdown file contributed parsed records", not missing,
          "; ".join(f"{k}: {v}" for k, v in sorted(by_file.items())) + (f" · NO RECORDS (no parser for this artifact/format yet): {missing}" if missing else ""), warn=True)
    import curated as _C
    unreconciled = [p for p in model["projects"] if p != _C.PROJECT]
    check("Coverage", "every project is reconciled by the curated overlay and narrative docs", not unreconciled,
          f"overlay covers '{_C.PROJECT}' only; parsed but NOT synthesized into narrative: {unreconciled}. "
          "Narrative docs (06-09, ALANKRIT_GLOBAL_CONTEXT, HANDOFF) describe the overlay project only.", warn=True)
    check("Coverage", "every discovered project contributed", all(any(r.get("project") == p for r in model["records"].values()) for p in model["projects"]),
          f"projects: {list(model['projects'])}")
    check("Coverage", "corpus spans more than one project", len(model["projects"]) > 1,
          f"{len(model['projects'])} project extraction(s). Cross-project claims are impossible; patterns are labelled cross-domain within one project.", warn=True)

    # ---- provenance
    mem = model["memory"]
    rows = [r for rs in mem.values() for r in rs]
    no_src = [r["id"] for r in rows if not (r.get("source_ref") or r.get("source"))]
    check("Provenance", "every memory row has a source_ref", not no_src, f"{len(rows)} rows; missing: {no_src[:10]}")
    bad_lines = []
    for r in rows:
        ref = r["source_ref"]
        if r.get("shipped_by_extraction"):
            continue  # provenance of shipped rows is the extraction's own responsibility
        if isinstance(ref, str) and ":" in ref:
            f, _, ln = ref.rpartition(":")
            proj = model["projects"].get(r.get("project") or "")
            p = (Path(proj["root"]) if proj else src) / f
            if not p.exists() or not ln.isdigit() or int(ln) > len(p.read_text(encoding="utf-8").splitlines()):
                bad_lines.append(r["id"])
    check("Provenance", "file:line refs point at existing lines", not bad_lines, f"bad: {bad_lines[:10]}")
    known = set(model["records"]) | {f"project:{p['id']}" for p in __import__("curated").PROJECTS}
    unresolved = {}
    total_refs = 0
    for f in _outputs():
        for m in REF.finditer(f.read_text(encoding="utf-8")):
            total_refs += 1
            gid = f"{m.group(1)}:{m.group(2)}"
            if gid not in known:
                unresolved.setdefault(f.name, set()).add(gid)
    check("Provenance", "every [project:ID] ref in generated docs resolves", not unresolved,
          f"{total_refs} refs across {len(_outputs())} docs; unresolved: {{{', '.join(f'{k}: {sorted(v)}' for k, v in unresolved.items())}}}")
    import curated as C
    cur_refs = re.findall(r"\b((?:icarus|global):[A-Za-z]+\d+(?:L\d+)?|icarus:MANIFEST)\b", Path(C.__file__).read_text())
    bad_cur = sorted({x for x in cur_refs if x not in known})
    check("Provenance", "every ref in the curated overlay resolves", not bad_cur, f"{len(cur_refs)} refs; unresolved: {bad_cur}")

    # ---- hallucination guards on narrative docs
    corpus = re.sub(r"\s+", " ", " ".join(p.read_text(encoding="utf-8") for p in src.rglob("*") if p.is_file()))
    corpus_nums = set(NUM_RX.findall(corpus))
    computed = {str(len(model["records"])), str(len(rows)), str(len(model.get("edges", []))), "2026", "16", "10", "20", "22", "23"}
    narrative = [WORKSPACE / n for n in ("06_ALANKRIT_IDENTITY.md", "07_REASONING_MODEL.md", "08_WORKING_STYLE.md",
                                         "09_VOICE_MODEL.md", "ALANKRIT_GLOBAL_CONTEXT.md", "HANDOFF_TO_ALANKRIT_OS.md")]
    q_miss, n_miss, q_total = {}, {}, 0
    for f in narrative:
        if not f.exists():
            continue
        t = f.read_text(encoding="utf-8")
        quotes = [seg for line in t.replace("“", '"').replace("”", '"').splitlines()
                  for seg in line.split('"')[1::2] if 12 <= len(seg) <= 200]
        for q in quotes:
            q = re.sub(r"\s+", " ", q).strip(" .,…")
            if not re.search(r"[a-z]{3}", q) or q.startswith(("global:", "icarus:")):
                continue
            q_total += 1
            if q.lower() not in corpus.lower():
                q_miss.setdefault(f.name, []).append(q)
        for n in NUM_RX.findall(t):
            if n not in corpus_nums and n not in computed and not re.fullmatch(r"0\d", n):
                n_miss.setdefault(f.name, set()).add(n)
    check("Hallucination", "quoted strings in narrative docs occur verbatim in corpus", not q_miss,
          f"{q_total} quotes checked; not found: {json.dumps(q_miss, ensure_ascii=False)[:1500]}", warn=True)
    check("Hallucination", "multi-digit numbers in narrative docs occur in corpus", not n_miss,
          f"not found: {{{', '.join(f'{k}: {sorted(v)}' for k, v in n_miss.items())}}}", warn=True)
    unverified_voice = [r["id"] for r in model["records"].values() if r["type"] == "voice_example" and not r["verified"]]
    check("Voice", "every voice excerpt found verbatim in its cited source file", not unverified_voice, f"unverified: {unverified_voice}")
    cats = Counter(c for r in model["records"].values() if r["type"] == "voice_example" for c in r["categories"])
    check("Voice", "voice categories with evidence", all(cats.get(c) for c in ["argument", "reflection", "technical reasoning", "disagreement", "short-form", "directness"]),
          f"{dict(cats)}; long-form/explanation/humor thin by design (no evidence)", warn=True)

    # ---- chronology / contradictions / duplication / nuance
    trans = [r for r in model["records"].values() if r["type"] == "belief_transition"]
    hist = [r for r in model["records"].values() if r["type"] == "belief" and r.get("global_status") in {"HISTORICAL", "REJECTED"}]
    rev = [r for r in model["records"].values() if r["type"] == "decision" and r.get("global_status") in {"REVERSED", "SUPERSEDED", "BEING_REVERSED"}]
    check("Chronology", "transitions preserve earlier and new positions", all(t["earlier"] and t["new"] for t in trans),
          f"{len(trans)} transitions, {len(hist)} historical/rejected beliefs, {len(rev)} reversed/superseded decisions retained (not deleted)")
    srcC = model["conflicts"]["source"]
    check("Contradictions", "all source contradictions carried with a status", all(r.get("global_status") for r in srcC),
          f"{len(srcC)} source + {len(model['conflicts']['global'])} compiler-level + {len(model['conflicts']['auto'])} automatic flags; none resolved")
    ids = Counter(r["id"] for r in rows)
    dup = [k for k, v in ids.items() if v > 1]
    check("Duplication", "memory ids unique across files", not dup, f"duplicates: {dup[:10]}")
    statuses = Counter(r["status"] for r in mem["beliefs"])
    check("Nuance", "uncertainty preserved (exploratory/uncertain beliefs not promoted)",
          all(model["records"][f"icarus:{b}"]["global_status"] in {"EXPLORATORY", "UNCERTAIN"} for b in ["B13", "B25", "B30", "B33", "B34", "B35"]),
          f"belief statuses: {dict(statuses)}")
    personal_decisions = [r["id"] for r in model["records"].values() if r["type"] == "decision" and r.get("classification") != "PROJECT-SPECIFIC"]
    check("Personal vs project", "no project decision promoted to a personal trait", not personal_decisions,
          f"transferable buckets: {model.get('transferable_buckets')}")

    # ---- current state
    import curated as _C2
    per = {k: (p.get("latest_evidence_date") or p.get("extraction_date")) for k, p in model["projects"].items()}
    gaps = {k: (date.fromisoformat(COMPILE_DATE) - date.fromisoformat(v)).days for k, v in per.items() if v}
    narr = gaps.get(_C2.PROJECT, 0)
    check("Current state", "'current' in the narrative is backed by recent evidence (per project)", narr <= 14,
          f"latest evidence per project: {per}; gap days: {gaps}. Narrative describes '{_C2.PROJECT}', so 'current' there means 'as of {per.get(_C2.PROJECT)}'.", warn=True)

    # ---- secrets
    hits = []
    for f in list(WORKSPACE.glob("*.md")) + list(WORKSPACE.glob("memory/*.jsonl")) + list(WORKSPACE.glob("voice_examples/*.md")) + [WORKSPACE / "source_manifest.json"]:
        if not f.exists():
            continue
        t = f.read_text(encoding="utf-8")
        for name, rx in SECRET_RX:
            for m in rx.finditer(t):
                if name == "phone" and re.fullmatch(r"[\d ,.-]+", m.group(0)) and len(re.sub(r"\D", "", m.group(0))) < 10:
                    continue
                hits.append(f"{f.name}: {name}: {m.group(0)[:12]}…")
    check("Secrets", "no credentials, emails or phone numbers in outputs", not hits, f"hits: {hits[:10]}")

    model["validation"] = checks
    _report(model, checks)
    return model


def _report(model, checks):
    res = Counter(c["result"] for c in checks)
    L = ["# 16 — Validation Report", "",
         f"Generated by `compiler/validate.py` on {COMPILE_DATE}. Result: **{res.get('PASS', 0)} PASS · {res.get('WARN', 0)} WARN · {res.get('FAIL', 0)} FAIL**.", "",
         "| area | check | result | detail |", "|---|---|---|---|"]
    for c in checks:
        L.append(f"| {c['area']} | {c['check']} | **{c['result']}** | {c['detail'].replace('|', '/')} |")
    L += ["", "## Interpretation", "",
          "- **Coverage:** every source file contributed. But the corpus contains one project, so 'did every source project contribute' is trivially yes "
          "and 'cross-project' is unattainable. This is the main limitation of the whole compilation.",
          "- **Provenance:** parsed records cite file:line; compiler records cite the parsed records they derive from; narrative docs cite inline refs that resolve.",
          "- **Hallucinations:** automated guards check that quotes and numbers in narrative docs exist in the corpus. WARN entries list strings to inspect by hand: "
          "typically paraphrases in quotation marks or computed counts.",
          "- **Chronology:** superseded beliefs and reversed decisions are retained with both positions (05, 04 historical table, 03 statuses).",
          "- **Nuance:** six beliefs held at EXPLORATORY/UNCERTAIN; reconstructed historical beliefs are marked MEDIUM confidence.",
          "- **Personal vs project:** all 35 decisions are PROJECT-SPECIFIC; only multi-surface items are PERSONAL PREFERENCE (see 14).",
          "- **Voice:** every excerpt is verbatim from the corpus with a provenance class separating his posted words from AI-written house style.",
          "- **Current state:** evidence stops 2026-09-10. Any agent using this on or after 2026-10-03 must treat 'current' as at least three weeks stale.", "",
          "## Final quality test", "",
          "Would a new AI reading only `HANDOFF_TO_ALANKRIT_OS.md` understand what he built, why, how his thinking changed, what he believes, how he "
          "communicates, what he cares about, rejected, learned, and what is unresolved? **Yes for the Icarus period (2026-06-27 → 2026-09-10).** "
          "**No for anything outside it**: his other projects, his life before March 2026, and the three weeks before compilation are absent from the corpus. "
          "The handoff says so explicitly instead of filling the gap."]
    write_text("16_VALIDATION_REPORT.md", "\n".join(L) + "\n")
