"""Merge loaded extractions into one global model.

Rules:
- ids are already namespaced "<slug>:<ID>"; a duplicate id across projects is a compile error
  (reported, first occurrence kept);
- rows flagged `derived_from_icarus` are kept but excluded from any frequency/echo counting,
  so the same evidence is never counted twice;
- nothing is rewritten: statuses, dates and authorship labels come from the extraction.
"""
from __future__ import annotations

from collections import Counter

from common import DERIVED_PROJECTS


def normalize(projects: list[dict]) -> dict:
    complete = [p for p in projects if p["complete"]]
    merged = {}
    dups = []
    by_id = {}
    for p in complete:
        for kind, rows in p["rows"].items():
            for r in rows:
                if r["id"] in by_id:
                    dups.append(r["id"])
                    continue
                by_id[r["id"]] = r
                merged.setdefault(kind, []).append(r)
    for r in by_id.values():
        if r["_extraction"] in DERIVED_PROJECTS:
            r["derived_from_icarus"] = True
    independent = [r for rs in merged.values() for r in rs if not r.get("derived_from_icarus")]
    stats = {
        "projects_complete": [p["slug"] for p in complete],
        "projects_incomplete": {p["slug"]: p["problems"] for p in projects if not p["complete"]},
        "rows_total": len(by_id),
        "rows_independent": len(independent),
        "rows_derived_from_icarus": len(by_id) - len(independent),
        "duplicates": dups,
        "by_project": dict(Counter(r["_extraction"] for r in by_id.values())),
    }
    return {"projects": projects, "merged": merged, "by_id": by_id, "stats": stats}
