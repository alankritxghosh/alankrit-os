"""Global Alankrit Context compiler: one command, full regeneration.

Usage:
    python compiler/run.py                         # default source corpus
    ALANKRIT_SOURCE_DIR=/path python compiler/run.py
    python compiler/run.py --source /path

The source corpus is never written. All outputs go to the workspace root
(the parent of this compiler/ directory).
"""
from __future__ import annotations

import argparse
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", help="source corpus directory (read-only)")
    args = ap.parse_args()
    if args.source:
        os.environ["ALANKRIT_SOURCE_DIR"] = args.source

    from common import WORKSPACE, sha256, source_dir, write_json
    import build_graph, build_memory, detect_conflicts, normalize, parse_sources, reconcile, scan_sources, synthesize, validate

    src = source_dir()
    before = {str(p.relative_to(src)): sha256(p) for p in src.rglob("*") if p.is_file()}

    scan = scan_sources.scan(src)
    write_json("source_manifest.json", scan)
    parsed = {p["slug"]: parse_sources.parse_project(__import__("pathlib").Path(p["root"])) for p in scan["projects"]}
    model = normalize.normalize(parsed, scan)
    model = reconcile.reconcile(model)
    model = detect_conflicts.detect(model)
    model = build_memory.build(model)
    model = build_graph.build(model)
    model = synthesize.synthesize(model)
    model = validate.validate(model, before)

    m = model["memory"]
    t = Counter(r["type"] for r in model["records"].values())
    res = Counter(c["result"] for c in model["validation"])
    print(f"source:            {src}")
    print(f"output:            {WORKSPACE}")
    print(f"projects:          {len(scan['projects'])}  ({', '.join(p['slug'] for p in scan['projects'])})")
    print(f"source files:      {scan['file_count']}")
    print(f"facts (memory):    {len(m['facts'])}")
    print(f"decisions:         {t['decision']}  (+{t['decision_pattern']} recurring patterns)")
    print(f"beliefs:           {t['belief']}  (35 source + {t['belief'] - 35} reconstructed historical)")
    print(f"belief transitions:{t['belief_transition']}")
    print(f"reasoning patterns:{t['reasoning_pattern']}")
    print(f"lessons:           {t['failure']} failures, {t['lesson']} lesson statements, {t['recurring_lesson']} recurring lessons")
    print(f"open loops:        {t['open_loop']}")
    print(f"contradictions:    {t['contradiction']}  (+{len(model['conflicts']['auto'])} automatic flags)")
    print(f"voice examples:    {t['voice_example']}")
    print(f"graph edges:       {len(model['edges'])}")
    print(f"validation:        {dict(res)}")
    for c in model["validation"]:
        if c["result"] != "PASS":
            print(f"  [{c['result']}] {c['area']}: {c['check']}")
    return 1 if res.get("FAIL") else 0


if __name__ == "__main__":
    sys.exit(main())
