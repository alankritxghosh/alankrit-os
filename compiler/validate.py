"""Validate the compilation and write 16_VALIDATION_REPORT.md."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from common import COMPILE_DATE, DERIVED_PROJECTS, WORKSPACE, sha256, source_dir, write_text

SECRET = [("api key", re.compile(r"(sk-[A-Za-z0-9]{16,}|phc_[A-Za-z0-9]{10,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}|gh[pousr]_[A-Za-z0-9]{30,}|xox[bpas]-[A-Za-z0-9-]{10,})")),
          ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
          ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
          ("phone", re.compile(r"(?<![\w.-])\+\d{1,3}[ -]?\d{5}[ -]?\d{5}(?![\w.-])"))]
COUNT_KEYS = {"decisions": "decisions", "failures": "failures", "lessons": "lessons", "open_loops": "open_loops",
              "contradictions": "contradictions", "voice_examples": "voice_examples"}


def validate(model: dict, hashes_before: dict) -> dict:
    src = source_dir()
    checks = []

    def chk(area, name, ok, detail, warn=False):
        checks.append({"area": area, "check": name, "result": "PASS" if ok else ("WARN" if warn else "FAIL"), "detail": detail})

    after = {str(p.relative_to(src)): sha256(p) for p in src.rglob("*") if p.is_file()}
    changed = [k for k in hashes_before if hashes_before[k] != after.get(k)]
    chk("Integrity", "source corpus unchanged during the run", not changed, f"{len(hashes_before)} files hashed; changed: {changed or 'none'}")
    chk("Integrity", "no output written inside the source corpus", not any(src in p.resolve().parents for p in WORKSPACE.rglob("*") if p.is_file()), "workspace is separate")

    st = model["stats"]
    chk("Coverage", "every extraction with a manifest is complete", not st["projects_incomplete"], f"incomplete: {st['projects_incomplete'] or 'none'}")
    chk("Coverage", "more than one independent project", len([x for x in st["projects_complete"] if x not in DERIVED_PROJECTS]) >= 2,
        f"{len(st['projects_complete'])} extractions, of which alankrit-os is derived from Icarus; independent projects: "
        f"{len([s for s in st['projects_complete'] if s not in DERIVED_PROJECTS])}. Cross-project patterns need at least 2 independent ones.", warn=True)
    bad = [b for p in model["projects"] for b in p["bad_lines"]]
    chk("Provenance", "every memory line is valid JSON", not bad, f"bad lines: {bad[:5] or 'none'}")
    chk("Provenance", "ids unique across projects", not st["duplicates"], f"duplicates: {st['duplicates'][:5] or 'none'}")
    nosrc = [i for i, r in model["by_id"].items() if not (r.get("source") or r.get("source_file"))]
    chk("Provenance", "every row has a source", not nosrc, f"missing: {nosrc[:5] or 'none'}")
    nolabel = [i for i, r in model["by_id"].items() if not r.get("status") or not r.get("confidence")]
    chk("Nuance", "every row has a status and a confidence", not nolabel, f"missing: {nolabel[:5] or 'none'}")
    ids = set(model["by_id"]) | {f"project:{s}" for s in st["projects_complete"]}
    dang = model["graph"]["dangling"]
    chk("Provenance", "relationship endpoints resolve", not dang, f"dangling: {dang[:5] or 'none'}", warn=True)
    mism = []
    for p in model["projects"]:
        if not p["complete"]:
            continue
        for mk, rk in COUNT_KEYS.items():
            declared = p["manifest"].get(mk)
            if isinstance(declared, int) and declared != len(p["rows"][rk]):
                mism.append(f"{p['slug']}.{mk}: manifest {declared} vs memory {len(p['rows'][rk])}")
    chk("Provenance", "manifest counts match memory files", not mism, f"{mism or 'all match'}", warn=True)
    voice = [r for r in model["merged"].get("voice_examples", [])]
    unverified = [r["id"] for r in voice if r.get("verified_verbatim") is False]
    chk("Voice", "every voice example verified verbatim by its extraction", not unverified, f"unverified: {unverified or 'none'}")
    mislabel = [r["id"] for r in voice if str(r.get("author", "")).upper().startswith("ALANKRIT") and "ASSISTANT" in str(r.get("author", "")).upper()
                and "selected" not in str(r.get("author", "")).lower() and "selection" not in str(r.get("author", "")).lower()]
    chk("Voice", "no example labelled as both his and the assistant's", not mislabel, f"{mislabel or 'none'}")
    chk("Personal vs project", "derived rows excluded from independent counts", st["rows_derived_from_icarus"] > 0 and st["rows_independent"] > 0,
        f"independent {st['rows_independent']}, derived {st['rows_derived_from_icarus']}")
    stale = model["conflicts"]["stale"]
    chk("Current state", "per-project evidence is recent", not stale, f"{stale or 'all within 14 days'}", warn=True)
    cs = re.search(r"Last updated: (\d{4}-\d\d-\d\d)", model["current_state"])
    chk("Current state", "authored current_state.md present and dated", bool(cs), f"last updated {cs.group(1) if cs else 'MISSING'}")
    hits = []
    for f in list(WORKSPACE.glob("*.md")) + list(WORKSPACE.glob("memory/*.jsonl")) + list(WORKSPACE.glob("voice_examples/*.md")) + [WORKSPACE / "source_manifest.json"]:
        if f.exists():
            t = f.read_text(encoding="utf-8")
            for name, rx in SECRET:
                for m in rx.finditer(t):
                    hits.append(f"{f.name}: {name}: {m.group(0)[:10]}…")
    chk("Secrets", "no credentials, emails or phone numbers in outputs", not hits, f"{hits[:8] or 'none'}")
    model["validation"] = checks
    res = Counter(c["result"] for c in checks)
    L = ["# 16 — Validation Report", "", f"Generated by `compiler/validate.py` on {COMPILE_DATE}. **{res.get('PASS', 0)} PASS · {res.get('WARN', 0)} WARN · {res.get('FAIL', 0)} FAIL**.", "",
         "| area | check | result | detail |", "|---|---|---|---|"]
    L += [f"| {c['area']} | {c['check']} | **{c['result']}** | {str(c['detail']).replace('|', '/')[:500]} |" for c in checks]
    L += ["", "## What this does and does not show", "",
          "- PASS means the records are intact, traceable by id and free of secrets. It does not mean the judgments inside them are true or reviewed.",
          "- The compiler adds no analysis of its own now: statuses, transitions and contradictions are the extractions'. Review them there.",
          "- Narrative synthesis (identity, reasoning and voice models) is not regenerated here. The global documents assemble each project's own handoff plus "
          "Alankrit's dated statement in `compiler/current_state.md`."]
    write_text("16_VALIDATION_REPORT.md", "\n".join(L) + "\n")
    return model
