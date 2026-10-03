"""Generate a weekly follower report against approved milestones."""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

from .common import add_common_args, output_path, write_markdown


MILESTONES = [
    ("2026-10-31", 140, 1050, "first post live, ~10"),
    ("2026-11-30", 420, 1450, "40"),
    ("2026-12-31", 850, 2000, "90"),
    ("2027-01-31", 1400, 2600, "150"),
    ("2027-02-28", 2050, 3300, "210"),
    ("2027-03-31", 2850, 4050, "290"),
    ("2027-04-30", 3750, 4900, "380"),
    ("2027-05-31", 4750, 5800, "480"),
    ("2027-06-30", 5850, 6700, "600"),
    ("2027-07-31", 7100, 7750, "720"),
    ("2027-08-31", 8400, 8800, "850"),
    ("2027-09-30", 9800, 9850, "980"),
    ("2027-10-04", 10000, 10000, "1000"),
]


def load_counts(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ["checked_at", "x", "linkedin", "substack"]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"missing count fields: {', '.join(missing)}")
    return data


def next_milestone(checked_at: str) -> tuple[str, int, int, str]:
    for row in MILESTONES:
        if row[0] >= checked_at:
            return row
    return MILESTONES[-1]


def delta(current: int, target: int) -> str:
    diff = current - target
    if diff >= 0:
        return f"+{diff}"
    return str(diff)


def render_report(counts: dict) -> str:
    date, x_target, li_target, sub_target = next_milestone(str(counts["checked_at"]))
    sub_current = counts["substack"]
    sub_line = str(sub_current)
    if isinstance(sub_current, int) and sub_target.isdigit():
        sub_line = f"{sub_current} ({delta(sub_current, int(sub_target))})"

    return "\n".join([
        "# Weekly Follower Report",
        "",
        "Draft-only report. Counts must be checked manually or through approved read-only tooling.",
        "",
        f"- Checked at: {counts['checked_at']}",
        f"- Next checkpoint: {date}",
        "",
        "| Platform | Current | Checkpoint | Delta |",
        "|---|---:|---:|---:|",
        f"| X | {counts['x']} | {x_target} | {delta(int(counts['x']), x_target)} |",
        f"| LinkedIn | {counts['linkedin']} | {li_target} | {delta(int(counts['linkedin']), li_target)} |",
        f"| Substack | {sub_line} | {sub_target} | see note |",
        "",
        "## Notes",
        "",
        "- If input gates or checkpoints are missed for two weeks running, stop and revisit the plan.",
        "- Do not explain shortfalls with guesses. Record what was done and what was not done.",
    ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--counts", type=Path, required=True, help="JSON object with checked_at, x, linkedin, substack")
    add_common_args(parser)
    args = parser.parse_args()

    counts = load_counts(args.counts)
    out = args.out or output_path("weekly-reports")
    write_markdown(out, render_report(counts))
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

