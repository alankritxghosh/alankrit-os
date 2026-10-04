"""Turn browser-verified reply targets into local draft replies."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .common import add_common_args, check_voice, output_path, render_checks, write_markdown


def load_targets(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("targets must be a JSON array")
    for item in data:
        if item.get("opened") is not True:
            raise ValueError(f"target was not marked opened: {item.get('url')}")
        if not item.get("url") or not str(item["url"]).startswith(("https://x.com/", "https://www.linkedin.com/")):
            raise ValueError(f"unsupported or missing url: {item.get('url')}")
        if not item.get("post_text"):
            raise ValueError(f"missing post_text for {item.get('url')}")
    return data


def normalize_url(url: str) -> str:
    return str(url).split("?")[0].rstrip("/")


def load_angles(path: Path) -> dict[str, str]:
    """Load {post url: your own reply text}. Blank values are ignored."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("angles must be a JSON object mapping post URL to reply text")
    angles: dict[str, str] = {}
    for url, text in data.items():
        if not isinstance(text, str):
            raise ValueError(f"angle for {url} must be a string")
        if text.strip():
            angles[normalize_url(url)] = text.strip()
    return angles


def apply_angles(targets: list[dict], angles: dict[str, str]) -> tuple[list[dict], list[str]]:
    """Attach angles to matching targets. Returns (targets, angle URLs that matched nothing)."""
    wanted = dict(angles)
    result = []
    for target in targets:
        angle = wanted.pop(normalize_url(target["url"]), None)
        result.append({**target, "angle": angle} if angle else target)
    return result, sorted(wanted)


def draft_reply(target: dict) -> str | None:
    """Return the reply Alankrit supplied as an angle, or None.

    There are no built-in templates. Keyword-matched replies cannot tell what a
    post means and misfired on real targets, so every reply is written by hand.
    """
    angle = (target.get("angle") or "").strip()
    return angle or None


def render_report(targets: list[dict]) -> str:
    blocks = [
        "# Reply Target Scout Output",
        "",
        "Draft-only. Every target below was marked as opened by the browser operator. Nothing was posted, liked, followed or sent.",
        "",
    ]
    for idx, target in enumerate(targets, start=1):
        platform = "linkedin" if "linkedin.com" in target["url"] else "x"
        reply = draft_reply(target)
        if reply is None:
            blocks.extend([
                f"## Target {idx}",
                "",
                f"- URL: {target['url']}",
                f"- Author: {target.get('author', 'UNKNOWN')}",
                f"- Checked: {target.get('checked_at', 'UNKNOWN')}",
                f"- Score: {target.get('score', 'UNKNOWN')}",
                f"- Why this target: {target.get('why', 'UNKNOWN')}",
                "",
                "Post excerpt:",
                "",
                str(target["post_text"]).strip(),
                "",
                "Draft reply:",
                "",
                "NEEDS HUMAN ANGLE. The scout writes no replies of its own. Add your reply for this URL to the angles file and rerun, or skip it.",
                "",
            ])
            continue
        checks = check_voice(reply, platform)
        score = target.get("score", "UNKNOWN")
        blocks.extend([
            f"## Target {idx}",
            "",
            f"- URL: {target['url']}",
            f"- Author: {target.get('author', 'UNKNOWN')}",
            f"- Checked: {target.get('checked_at', 'UNKNOWN')}",
            f"- Score: {score}",
            f"- Why this target: {target.get('why', 'UNKNOWN')}",
            "",
            "Post excerpt:",
            "",
            str(target["post_text"]).strip(),
            "",
            "Draft reply:",
            "",
            reply,
            "",
            "Voice check:",
            "",
            render_checks(checks),
            "",
        ])
    return "\n".join(blocks)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", type=Path, required=True, help="JSON array of browser-verified targets")
    parser.add_argument("--angles", type=Path, default=None, help="JSON object mapping post URL to your own reply text")
    add_common_args(parser)
    args = parser.parse_args()

    targets = load_targets(args.targets)
    if args.angles:
        targets, unmatched = apply_angles(targets, load_angles(args.angles))
        for url in unmatched:
            print(f"warning: angle matches no target: {url}", file=sys.stderr)
    out = args.out or output_path("reply-targets")
    write_markdown(out, render_report(targets))
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
