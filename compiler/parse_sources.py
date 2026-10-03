"""Load v2 extractions.

A v2 extraction ships its own machine-readable memory (`memory/*.jsonl`), so the compiler reads
those records directly instead of re-parsing prose. A project is COMPLETE only if it has a
manifest, a HANDOFF file and at least one memory file. Anything else is reported as incomplete
and is not merged.
"""
from __future__ import annotations

import json
from pathlib import Path

KINDS = ["facts", "decisions", "beliefs", "episodes", "lessons", "failures",
         "open_loops", "contradictions", "voice_examples", "relationships"]


def load_project(p: dict) -> dict:
    root = Path(p["root"])
    problems = []
    if not (root / "HANDOFF_TO_ALANKRIT_OS.md").exists():
        problems.append("no HANDOFF_TO_ALANKRIT_OS.md")
    mem = root / "memory"
    if not mem.is_dir() or not any(mem.glob("*.jsonl")):
        problems.append("no memory/*.jsonl")
    if p.get("schema") != "v2":
        problems.append(f"schema {p.get('schema')} (only v2 is supported by this compiler)")
    rows = {k: [] for k in KINDS}
    bad_lines = []
    if not problems:
        for k in KINDS:
            f = mem / f"{k}.jsonl"
            if not f.exists():
                continue
            for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                if not line.strip():
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    bad_lines.append(f"{p['slug']}/memory/{k}.jsonl:{n}")
                    continue
                r["_kind"] = k
                r["_extraction"] = p["slug"]
                r.setdefault("project", p["slug"])
                rows[k].append(r)
    manifest = {}
    try:
        manifest = json.loads((root / "extraction_manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        problems.append("manifest unreadable")
    handoff = (root / "HANDOFF_TO_ALANKRIT_OS.md").read_text(encoding="utf-8") if not problems else ""
    return {"slug": p["slug"], "root": str(root), "name": manifest.get("project_name", p["slug"]),
            "complete": not problems, "problems": problems, "bad_lines": bad_lines,
            "rows": rows, "manifest": manifest, "handoff": handoff}


def load_all(scan: dict) -> list[dict]:
    return [load_project(p) for p in scan["projects"]]
