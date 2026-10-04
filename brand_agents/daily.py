"""Daily brand routine: find targets, shortlist them, then voice-check the replies you wrote.

Draft-only. This never posts, replies, likes, follows, DMs, emails or schedules.
Everything lands in ~/.alankrit-os/daily/<date>/ (outside the repo, because it
holds your own reply text). You copy the final text and post it by hand.

    python -m brand_agents.daily scout            # discover, write review.md + angles.json
    python -m brand_agents.daily triage --keep 1,4,7
    # write your reply for each kept URL into angles.json
    python -m brand_agents.daily replies          # voice-check, write replies.md
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Callable

from .common import check_voice, require_all_pass, write_markdown
from .reply_scout import load_angles, normalize_url

DEFAULT_ROOT = Path.home() / ".alankrit-os" / "daily"
POOL_SIZE = 25
EXCERPT_CHARS = 600

Finder = Callable[[], list[dict]]


def day_dir(root: Path, day: str | None = None) -> Path:
    return root / (day or date.today().isoformat())


def read_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def excerpt(text: str, limit: int = EXCERPT_CHARS) -> str:
    flat = " ".join(str(text).split())
    return flat if len(flat) <= limit else flat[: limit - 1].rstrip() + "…"


def build_review(candidates: list[dict]) -> str:
    lines = [
        "# Daily review sheet",
        "",
        "Draft-only. Nothing here was posted, liked, followed or sent.",
        "Pick the posts worth answering, write your own reply for each URL in `angles.json`, then run `replies`.",
        "",
    ]
    for idx, item in enumerate(candidates, start=1):
        lines.extend([
            f"## {idx}. @{item.get('author', 'UNKNOWN')} (score {item.get('score', '?')})",
            "",
            item["url"],
            "",
            excerpt(item["post_text"]),
            "",
        ])
    if not candidates:
        lines.append("No candidates today.")
    return "\n".join(lines)


def merge_angles(candidates: list[dict], existing: dict) -> dict[str, str]:
    """Template of URL -> reply text. Never drops or blanks text already written."""
    merged: dict[str, str] = {}
    for key, value in existing.items():
        merged[normalize_url(key)] = value if isinstance(value, str) else ""
    for item in candidates:
        merged.setdefault(normalize_url(item["url"]), "")
    return merged


def scout(directory: Path, finder: Finder, force: bool = False) -> list[dict]:
    candidates_path = directory / "candidates.json"
    if candidates_path.exists() and not force:
        raise FileExistsError(
            f"{candidates_path} already exists. Use --force to refresh the candidates "
            "(replies you already wrote in angles.json are kept) or --date for another folder."
        )
    candidates = finder()
    write_json(candidates_path, candidates)
    write_json(directory / "angles.json", merge_angles(candidates, read_json(directory / "angles.json", {})))
    write_markdown(directory / "review.md", build_review(candidates))
    (directory / "picks.json").unlink(missing_ok=True)
    return candidates


def parse_keep(spec: str, total: int) -> list[int]:
    keep: list[int] = []
    for part in spec.replace(" ", "").split(","):
        if not part:
            continue
        if not part.isdigit() or not 1 <= int(part) <= total:
            raise ValueError(f"'{part}' is not a candidate number between 1 and {total}")
        if int(part) not in keep:
            keep.append(int(part))
    if not keep:
        raise ValueError("keep list is empty")
    return keep


def triage(directory: Path, keep: list[int]) -> list[dict]:
    """Shortlist candidates by their number in review.md. Keeps any replies already written."""
    candidates = read_json(directory / "candidates.json", None)
    if candidates is None:
        raise FileNotFoundError(f"no candidates in {directory}. Run scout first.")
    picked = [candidates[i - 1] for i in keep]
    write_json(directory / "picks.json", [item["url"] for item in picked])
    write_markdown(directory / "review.md", build_review(picked))
    angles = read_json(directory / "angles.json", {})
    keep_urls = {normalize_url(item["url"]) for item in picked}
    shortlisted = {url: text for url, text in merge_angles(picked, angles).items() if url in keep_urls or text.strip()}
    write_json(directory / "angles.json", shortlisted)
    return picked


def build_replies(directory: Path) -> tuple[str, list[str], list[str]]:
    """Return (replies.md text, urls ready to post, urls whose reply fails the voice check)."""
    candidates = read_json(directory / "candidates.json", None)
    if candidates is None:
        raise FileNotFoundError(f"no candidates in {directory}. Run scout first.")
    angles_path = directory / "angles.json"
    if not angles_path.exists():
        raise FileNotFoundError(f"{angles_path} is missing. Run scout first.")
    angles = load_angles(angles_path)
    by_url = {normalize_url(item["url"]): item for item in candidates}

    ready: list[str] = []
    failing: list[str] = []
    ready_blocks: list[str] = []
    failing_blocks: list[str] = []
    unknown: list[str] = []
    for url, text in angles.items():
        item = by_url.get(url)
        if item is None:
            unknown.append(url)
            continue
        checks = check_voice(text, "x")
        header = f"### @{item.get('author', 'UNKNOWN')}\n\nPost: {item['url']}"
        if require_all_pass(checks):
            ready.append(item["url"])
            ready_blocks.append(f"{header}\n\n```text\n{text}\n```")
        else:
            failing.append(item["url"])
            problems = "\n".join(f"- FAIL: {c.name} ({c.detail})" for c in checks if not c.passed)
            failing_blocks.append(f"{header}\n\nYour text:\n\n```text\n{text}\n```\n\n{problems}")

    parts = [
        "# Replies to post by hand",
        "",
        "Draft-only. Copy each reply and post it yourself. Nothing was posted, liked, followed or sent.",
        "",
        f"## Ready ({len(ready)})",
        "",
        "\n\n".join(ready_blocks) if ready_blocks else "None yet. Write replies in angles.json and run `replies` again.",
        "",
    ]
    if failing_blocks:
        parts += [f"## Fix before posting ({len(failing)})", "", "\n\n".join(failing_blocks), ""]
    if unknown:
        parts += ["## Not in today's candidates", "", "\n".join(f"- {u}" for u in unknown), ""]
    return "\n".join(parts), ready, failing


def default_finder(args: argparse.Namespace) -> Finder:
    def run() -> list[dict]:
        from .providers.x_playwright.find_posts import find_posts, load_seen, save_seen

        if not args.state.exists():
            raise SystemExit(f"missing X login state: {args.state}. Run the X cookie login first.")
        already = set() if args.no_dedupe else load_seen(args.seen_file)
        targets = find_posts(
            args.state, None, args.pool, headless=True, scrolls=args.scrolls, channel=args.channel,
            already_seen=already, tab=args.tab, days=args.days or None,
        )
        if not args.no_dedupe:
            save_seen(args.seen_file, already | {t["url"] for t in targets})
        return targets

    return run


def main(argv: list[str] | None = None) -> int:
    from .providers.x_playwright.find_posts import DEFAULT_DAYS, DEFAULT_SCROLLS, DEFAULT_SEEN, DEFAULT_STATE, DEFAULT_TAB

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="folder that holds one subfolder per day")
    parser.add_argument("--date", default=None, help="day folder name, default today (YYYY-MM-DD)")
    sub = parser.add_subparsers(dest="step", required=True)

    p_scout = sub.add_parser("scout", help="discover candidates and write the review sheet")
    p_scout.add_argument("--pool", type=int, default=POOL_SIZE)
    p_scout.add_argument("--channel", default="chrome")
    p_scout.add_argument("--state", type=Path, default=DEFAULT_STATE)
    p_scout.add_argument("--seen-file", type=Path, default=DEFAULT_SEEN)
    p_scout.add_argument("--no-dedupe", action="store_true")
    p_scout.add_argument("--tab", choices=["top", "live"], default=DEFAULT_TAB)
    p_scout.add_argument("--days", type=int, default=DEFAULT_DAYS)
    p_scout.add_argument("--scrolls", type=int, default=DEFAULT_SCROLLS)
    p_scout.add_argument("--force", action="store_true", help="refresh candidates; keeps replies already in angles.json")

    p_triage = sub.add_parser("triage", help="keep only the candidates you or Claude picked")
    p_triage.add_argument("--keep", required=True, help="comma-separated candidate numbers from review.md, e.g. 1,4,7")

    sub.add_parser("replies", help="voice-check angles.json and write replies.md")

    args = parser.parse_args(argv)
    directory = day_dir(args.root, args.date)

    try:
        if args.step == "scout":
            candidates = scout(directory, default_finder(args), force=args.force)
            print(f"{len(candidates)} candidates")
            print(f"review:  {directory / 'review.md'}")
            print(f"angles:  {directory / 'angles.json'}")
        elif args.step == "triage":
            total = len(read_json(directory / "candidates.json", []))
            picked = triage(directory, parse_keep(args.keep, total))
            print(f"kept {len(picked)} of {total}")
            print(f"review:  {directory / 'review.md'}")
        else:
            text, ready, failing = build_replies(directory)
            out = write_markdown(directory / "replies.md", text)
            print(f"{len(ready)} ready, {len(failing)} need fixing")
            print(f"replies: {out}")
            if failing:
                return 1
    except (FileExistsError, FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
