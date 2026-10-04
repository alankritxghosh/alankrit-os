"""Turn browser-verified reply targets into local draft replies."""
from __future__ import annotations

import argparse
import json
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


def draft_reply(target: dict) -> str | None:
    """Return a draft reply, or None when the post needs a human angle."""
    angle = (target.get("angle") or "").strip()
    if angle:
        return angle[:260].strip()
    post = " ".join(str(target["post_text"]).split())
    lowered = post.lower()
    if all(term in lowered for term in ["claude code", "codex"]) and any(term in lowered for term in ["switching", "terminal", "parallel", "sessions"]):
        return "The real pain is managing the handoff between agents without losing context. Picking one is the easy part."
    if "parallel agent sessions" in lowered or "pr management" in lowered:
        return "This feels useful because keeping parallel agent work comparable in one place is the messy part."
    if "claude code" in lowered and "codex" in lowered and "?" in post:
        return "Switching for a month tells you more than any comparison thread. Pick the one whose failures you can read fastest."
    if "agent" in lowered and any(term in lowered for term in ["grades", "benchmark", "eval"]) and any(term in lowered for term in ["database", "records", "backend"]):
        return "Grading on the state an agent leaves behind is the right test. A clean transcript can hide a lot of broken writes."
    if "vibe coding" in lowered and any(term in lowered for term in ["i built", "i've built", "i shipped"]) and any(term in lowered for term in ["startup", "shipped", "in production", "launched"]):
        return "Vibe coding still needs taste. Otherwise you just ship confusion faster."
    return None


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
                "NEEDS HUMAN ANGLE. No template fits this post and a generic reply would be noise. Add an `angle` to this target and rerun, or skip it.",
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
    add_common_args(parser)
    args = parser.parse_args()

    targets = load_targets(args.targets)
    out = args.out or output_path("reply-targets")
    write_markdown(out, render_report(targets))
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
