"""Phase 4: surface conflicts. Never resolves them; only lists and flags.

Sources of conflict:
1. contradictions recorded by the extraction (type=contradiction, project ids);
2. compiler-level contradictions from the overlay (global:GC*);
3. automatic checks over the model:
   - beliefs carrying contradicting evidence;
   - decisions whose status is REVERSED / SUPERSEDED / BEING_REVERSED;
   - beliefs marked CURRENT whose last observation predates the latest evidence by > 30 days.
"""
from __future__ import annotations

from datetime import date


def _d(s):
    try:
        return date.fromisoformat(s[:10])
    except (TypeError, ValueError):
        return None


def detect(model: dict) -> dict:
    recs = model["records"].values()
    latest = max((_d(p.get("latest_evidence_date")) for p in model["projects"].values() if p.get("latest_evidence_date")), default=None)
    auto = []
    for r in recs:
        if r["type"] == "belief" and r.get("contradicting_evidence"):
            auto.append({"id": r["id"], "check": "belief_has_counter_evidence",
                         "detail": "; ".join(r["contradicting_evidence"])})
        if r["type"] == "decision" and r.get("global_status") in {"REVERSED", "SUPERSEDED", "BEING_REVERSED"}:
            auto.append({"id": r["id"], "check": "decision_reversed_or_superseded",
                         "detail": f"{r['global_status']} by {r.get('later_reversal')}"})
        if r["type"] == "belief" and r.get("global_status") in {"CURRENT", "PERSISTENT"} and latest:
            last = _d(r.get("last_observed", ""))
            if last and (latest - last).days > 30:
                auto.append({"id": r["id"], "check": "current_belief_not_recently_observed",
                             "detail": f"last observed {last}, latest evidence {latest} ({(latest - last).days} days)"})
    model["conflicts"] = {
        "source": [r for r in recs if r["type"] == "contradiction" and not r["id"].startswith("global:")
                   and r.get("global_status")],  # unreconciled projects are reported via their own memory/
        "global": [r for r in recs if r["type"] == "contradiction" and r["id"].startswith("global:")],
        "auto": auto,
    }
    return model
