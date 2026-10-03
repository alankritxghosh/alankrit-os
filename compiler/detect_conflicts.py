"""Surface conflicts. Never resolves them.

1. contradictions the extractions recorded (kept with their own statuses);
2. cross-project contradictions: relationships whose `rel` is contradicted/reversed and whose
   endpoints belong to different projects;
3. automatic flags: beliefs with counterevidence, decisions marked reversed/superseded,
   and 'current' facts older than 30 days at compile time.
"""
from __future__ import annotations

from datetime import date

from common import COMPILE_DATE


def detect(model: dict) -> dict:
    m = model["merged"]
    by_id = model["by_id"]
    cross = []
    for r in m.get("relationships", []):
        if r.get("rel") in {"contradicted", "reversed"}:
            a, b = by_id.get(r.get("from")), by_id.get(r.get("to"))
            if a and b and a["_extraction"] != b["_extraction"]:
                cross.append(r)
    auto = []
    for b in m.get("beliefs", []):
        ce = (b.get("counterevidence") or "").strip()
        if b.get("type") == "belief" and ce and ce not in {"—", "-", "none", "none recorded"}:
            auto.append({"id": b["id"], "check": "belief_has_counterevidence", "detail": ce})
    for d in m.get("decisions", []):
        st = str(d.get("status", "")).upper()
        if any(w in st for w in ("REVERSED", "SUPERSEDED", "BEING_REVERSED")):
            auto.append({"id": d["id"], "check": "decision_reversed_or_superseded", "detail": d.get("status")})
    stale = []
    today = date.fromisoformat(COMPILE_DATE)
    for p in model["projects"]:
        if not p["complete"]:
            continue
        ev = p["manifest"].get("latest_evidence_date")
        if ev:
            gap = (today - date.fromisoformat(ev)).days
            if gap > 14:
                stale.append({"project": p["slug"], "latest_evidence": ev, "gap_days": gap})
    model["conflicts"] = {"recorded": m.get("contradictions", []), "cross_project": cross, "auto": auto, "stale": stale}
    return model
