"""Global Alankrit Context compiler (v2).

    python compiler/run.py [--source DIR]

Reads every complete v2 extraction under the source corpus (read-only) and writes the global
documents and memory into the workspace root. Legacy v1 modules live in compiler/legacy_v1/.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source")
    a = ap.parse_args()
    if a.source:
        os.environ["ALANKRIT_SOURCE_DIR"] = a.source
    from collections import Counter

    import build_graph, build_memory, detect_conflicts, normalize, parse_sources, reconcile, scan_sources, synthesize, validate
    from common import WORKSPACE, sha256, source_dir, write_json

    src = source_dir()
    before = {str(p.relative_to(src)): sha256(p) for p in src.rglob("*") if p.is_file()}
    scan = scan_sources.scan(src)
    write_json("source_manifest.json", scan)
    model = normalize.normalize(parse_sources.load_all(scan))
    model = reconcile.reconcile(model)
    model = detect_conflicts.detect(model)
    model = build_memory.build(model)
    model = build_graph.build(model)
    model = synthesize.synthesize(model, scan)
    model = validate.validate(model, before)
    res = Counter(c["result"] for c in model["validation"])
    st = model["stats"]
    print(f"source:      {src}")
    print(f"output:      {WORKSPACE}")
    print(f"complete:    {st['projects_complete']}")
    print(f"incomplete:  {list(st['projects_incomplete'])}")
    print(f"rows:        {st['rows_total']} (independent {st['rows_independent']}, derived {st['rows_derived_from_icarus']})")
    print(f"memory:      {model['memory_counts']}")
    print(f"edges:       {len(model['edges'])} (cross-project {model['graph']['cross']})")
    print(f"validation:  {dict(res)}")
    for c in model["validation"]:
        if c["result"] != "PASS":
            print(f"  [{c['result']}] {c['area']}: {c['check']}: {str(c['detail'])[:200]}")
    return 1 if res.get("FAIL") else 0


if __name__ == "__main__":
    sys.exit(main())
