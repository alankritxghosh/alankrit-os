"""Write global memory/*.jsonl: all complete extractions merged, nothing rewritten."""
from __future__ import annotations

from common import write_jsonl

OUT_KINDS = ["facts", "decisions", "beliefs", "episodes", "lessons", "failures",
             "open_loops", "contradictions", "voice_examples"]


def build(model: dict) -> dict:
    counts = {}
    for k in OUT_KINDS:
        # rows an extraction marks `confidential` stay in that extraction and never reach global memory
        rows = [{kk: v for kk, v in r.items() if not kk.startswith("_")} | {"extraction": r["_extraction"]}
                for r in model["merged"].get(k, []) if not r.get("confidential")]
        write_jsonl(f"memory/{k}.jsonl", rows)
        counts[k] = len(rows)
    projects = []
    for p in model["projects"]:
        m = p["manifest"]
        projects.append({
            "id": f"project:{p['slug']}", "type": "project", "content": p["name"],
            "status": "EXTRACTED" if p["complete"] else "INCOMPLETE_NOT_MERGED",
            "confidence": "HIGH", "date": {"latest_evidence": m.get("latest_evidence_date"), "extracted": m.get("extraction_date")},
            "project": p["slug"], "source": f"{p['root']}/extraction_manifest.json",
            "problems": p["problems"], "counts": {k: len(v) for k, v in p["rows"].items()},
            "coverage_gaps": m.get("coverage_gaps", []), "uncertainties": m.get("uncertainties", []),
        })
    write_jsonl("memory/projects.jsonl", projects)
    counts["projects"] = len(projects)
    model["memory_counts"] = counts
    return model
