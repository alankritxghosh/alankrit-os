"""Append-only log of what Alankrit decides about each target and draft.

Every shown card, Use draft, Skip, Edit and Redraft is one JSON line in
~/.alankrit-os/decisions.jsonl. It lives outside the repo (mode 600) because it
holds post text and Alankrit's own replies. Nothing here posts or sends anything.

Two fields are kept deliberately apart so the log can feed drafting later without
breaking the voice policy (first drafts come from text Alankrit typed himself, not
from agent text he approved):

    draft         what Claude wrote
    final_source  "draft_as_is" (Alankrit approved agent text) or
                  "typed_by_alankrit" (Alankrit's own words)

    python -m brand_agents.decisions summary [--days 14]
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import sys
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

DEFAULT_LOG = Path.home() / ".alankrit-os" / "decisions.jsonl"
SCHEMA = 1
ACTIONS = ("shown", "use_draft", "skip", "edit_started", "edit_saved", "edit_rejected", "redraft")


def similarity(draft: str | None, final: str | None) -> float | None:
    """0 to 1: how much of the draft survived the edit. None when there is no draft."""
    if not draft or not final:
        return None
    return round(difflib.SequenceMatcher(None, draft, final).ratio(), 3)


def log_event(event: dict, path: Path = DEFAULT_LOG) -> bool:
    """Append one event. Logging must never break the bot, so failures return False."""
    record = {"schema": SCHEMA, "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), **event}
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        with os.fdopen(fd, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        os.chmod(path, 0o600)
        return True
    except (OSError, TypeError, ValueError):
        return False


def read_events(path: Path = DEFAULT_LOG) -> list[dict]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    events = []
    for line in lines:
        try:
            record = json.loads(line)
        except ValueError:
            continue
        if isinstance(record, dict) and record.get("action"):
            events.append(record)
    return events


def summarize(events: list[dict]) -> dict:
    counts = Counter(e["action"] for e in events)
    used, edited, skipped = counts["use_draft"], counts["edit_saved"], counts["skip"]
    decided = used + edited + skipped

    def rate(n: int) -> float | None:
        return round(n / decided, 3) if decided else None

    shown = [e for e in events if e["action"] == "shown"]
    drafted = sum(1 for e in shown if e.get("draft"))
    sims = [e["similarity"] for e in events if e["action"] == "edit_saved" and isinstance(e.get("similarity"), (int, float))]
    skipped_authors = Counter(e.get("author", "UNKNOWN") for e in events if e["action"] == "skip")
    return {
        "events": len(events),
        "counts": dict(counts),
        "decided": decided,
        "use_rate": rate(used),
        "edit_rate": rate(edited),
        "skip_rate": rate(skipped),
        "drafts_shown": drafted,
        "drafts_missing": len(shown) - drafted,
        "avg_similarity_of_edits": round(sum(sims) / len(sims), 3) if sims else None,
        "redrafts": counts["redraft"],
        "most_skipped_authors": skipped_authors.most_common(5),
    }


def since(events: list[dict], days: int | None, today: date | None = None) -> list[dict]:
    if not days:
        return events
    cutoff = (today or date.today()) - timedelta(days=days)
    return [e for e in events if str(e.get("day") or e.get("ts", ""))[:10] >= cutoff.isoformat()]


def format_summary(summary: dict) -> str:
    def pct(value):
        return "n/a" if value is None else f"{value * 100:.0f}%"

    lines = [
        f"Decisions logged: {summary['events']} events, {summary['decided']} decided",
        f"  used as is   {summary['counts'].get('use_draft', 0):>4}  ({pct(summary['use_rate'])})",
        f"  edited       {summary['counts'].get('edit_saved', 0):>4}  ({pct(summary['edit_rate'])})",
        f"  skipped      {summary['counts'].get('skip', 0):>4}  ({pct(summary['skip_rate'])})",
        f"  redrafts     {summary['redrafts']:>4}",
        f"Drafts shown: {summary['drafts_shown']}, cards with no draft: {summary['drafts_missing']}",
        f"Edits kept {pct(summary['avg_similarity_of_edits'])} of the draft on average",
    ]
    if summary["most_skipped_authors"]:
        lines.append("Most skipped: " + ", ".join(f"@{a} ({n})" for a, n in summary["most_skipped_authors"]))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    sub = parser.add_subparsers(dest="step", required=True)
    p = sub.add_parser("summary")
    p.add_argument("--days", type=int, default=None, help="only the last N days")
    args = parser.parse_args(argv)
    events = read_events(args.log)
    if not events:
        print(f"No decisions logged yet in {args.log}", file=sys.stderr)
        return 1
    print(format_summary(summarize(since(events, args.days))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
