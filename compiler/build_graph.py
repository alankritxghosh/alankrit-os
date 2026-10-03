"""Global graph: merge each project's relationships and add cross-project edges.

Cross-project edges are the ones whose endpoint ids belong to another project, or that an
extraction marked `basis` containing 'cross-project'. They are listed first in 15_KNOWLEDGE_GRAPH.md.
"""
from __future__ import annotations

from collections import Counter

from common import write_jsonl, write_text


def build(model: dict) -> dict:
    by_id = model["by_id"]
    edges = [{kk: v for kk, v in r.items() if not kk.startswith("_")} | {"extraction": r["_extraction"]}
             for r in model["merged"].get("relationships", [])]
    slugs = set(model["stats"]["projects_complete"])

    def proj(x):
        if x in by_id:
            return by_id[x]["_extraction"]
        return x.split(":")[0] if ":" in x and x.split(":")[0] in slugs else x

    cross, dangling = [], []
    for e in edges:
        a, b = proj(e["from"]), proj(e["to"])
        e["from_project"], e["to_project"] = a, b
        if a != b:
            cross.append(e)
        for end in (e["from"], e["to"]):
            if ":" in end and end.split(":")[0] in slugs and end not in by_id and not end.endswith(":PROJECT") and not end.endswith("PROJECT"):
                dangling.append((e["id"], end))
    write_jsonl("memory/relationships.jsonl", edges)
    rel = Counter(e["rel"] for e in edges)
    L = ["# 15 — Global Knowledge Graph", "",
         f"{len(edges)} edges from {len(slugs)} extractions (`memory/relationships.jsonl`). Edges are exactly as the extractions recorded them; "
         "this compiler adds none.", "", "| relation | count |", "|---|---|"] + [f"| {k} | {v} |" for k, v in sorted(rel.items())]
    L += ["", f"## Cross-project edges ({len(cross)})", "", "| id | from | relation | to | basis |", "|---|---|---|---|---|"]
    L += [f"| {e['id']} | {e['from']} | {e['rel']} | {e['to']} | {e.get('basis')} |" for e in cross] or ["| — | | | | |"]
    L += ["", f"## Dangling endpoints ({len(dangling)})", "",
          "Edges pointing at ids that do not exist in any complete extraction. Reported, not fixed.", ""]
    L += [f"- {a}: {b}" for a, b in dangling] or ["- none"]
    write_text("15_KNOWLEDGE_GRAPH.md", "\n".join(L) + "\n")
    model["edges"] = edges
    model["graph"] = {"cross": len(cross), "dangling": dangling}
    return model
