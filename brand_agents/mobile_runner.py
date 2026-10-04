"""Run draft-only brand agents from a JSON command.

This is designed for GitHub Actions, so Alankrit can run the system from a phone.
It writes local markdown only. It never posts, schedules, sends, likes, follows,
connects, DMs or emails.
"""
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from .common import OUTPUT_DIR, today_slug, write_markdown
from .draft_agent import render_report as render_draft_report
from .draft_agent import build_variants
from .reply_scout import load_targets, render_report as render_reply_report
from .weekly_report import load_counts, render_report as render_weekly_report


VALID_COMMANDS = {"draft", "reply_scout", "weekly_report", "find_x_replies"}


def load_command(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("command must be a JSON object")
    command = data.get("command")
    if command not in VALID_COMMANDS:
        raise ValueError(f"command must be one of: {', '.join(sorted(VALID_COMMANDS))}")
    return data


def run_draft(command: dict) -> str:
    raw_idea = str(command.get("raw_idea", "")).strip()
    if not raw_idea:
        raise ValueError("draft command needs raw_idea")
    platform = command.get("platform", "x")
    if platform not in {"x", "linkedin", "substack"}:
        raise ValueError("platform must be x, linkedin or substack")
    facts = command.get("facts", [])
    if not isinstance(facts, list):
        raise ValueError("facts must be an array")
    for fact in facts:
        if not fact.get("claim") or not fact.get("source"):
            raise ValueError("each fact needs claim and source")
    variants = build_variants(raw_idea, platform, facts)
    return render_draft_report(raw_idea, platform, facts, variants)


def run_reply_scout(command: dict) -> str:
    targets = command.get("targets", [])
    if not isinstance(targets, list):
        raise ValueError("targets must be an array")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "targets.json"
        path.write_text(json.dumps(targets), encoding="utf-8")
        loaded = load_targets(path)
    return render_reply_report(loaded)


def run_weekly_report(command: dict) -> str:
    counts = command.get("counts")
    if not isinstance(counts, dict):
        raise ValueError("weekly_report command needs counts object")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "counts.json"
        path.write_text(json.dumps(counts), encoding="utf-8")
        loaded = load_counts(path)
    return render_weekly_report(loaded)


def run_find_x_replies(command: dict) -> str:
    from .providers.x_playwright.find_posts import DEFAULT_STATE, find_posts
    from .reply_scout import render_report as render_reply_report

    limit = int(command.get("limit", 10))
    queries = command.get("queries") or None
    state = Path(command.get("state", str(DEFAULT_STATE)))
    if not state.exists():
        raise ValueError(f"missing X login state at {state}. Run the X Playwright login first.")
    targets = find_posts(state=state, queries=queries, limit=limit, headless=True, scrolls=int(command.get("scrolls", 8)))
    return render_reply_report(targets)


def run(command: dict) -> str:
    kind = command["command"]
    if kind == "draft":
        return run_draft(command)
    if kind == "reply_scout":
        return run_reply_scout(command)
    if kind == "weekly_report":
        return run_weekly_report(command)
    if kind == "find_x_replies":
        return run_find_x_replies(command)
    raise AssertionError(kind)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--command-file", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    command = load_command(args.command_file)
    report = run(command)
    out = args.out or OUTPUT_DIR / "mobile" / f"{today_slug()}-{command['command']}.md"
    write_markdown(out, report)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
