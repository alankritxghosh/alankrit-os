"""Turn browser-verified reply targets into local draft replies."""
from __future__ import annotations

import argparse
import json
import re
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


def draft_reply(target: dict) -> str:
    angle = (target.get("angle") or "").strip()
    if angle:
        return angle[:260].strip()
    post = " ".join(str(target["post_text"]).split())
    lowered = post.lower()
    if all(term in lowered for term in ["claude code", "codex"]) and any(term in lowered for term in ["switching", "terminal", "parallel", "sessions"]):
        return "The real pain is not picking one agent, it is managing the handoff between them without losing context."
    if "parallel agent sessions" in lowered or "pr management" in lowered:
        return "This feels useful because the messy part is not running agents, it is keeping their work comparable in one place."
    if "claude code" in lowered:
        return "The interesting bit with Claude Code is not speed, it is how quickly bad taste becomes visible."
    if "agent" in lowered and "workflow" in lowered:
        return "This is where agents get useful for me too. Not replacing the workflow, but making the weak parts obvious."
    if "vibe coding" in lowered:
        return "The part people miss with vibe coding is that you still need taste. Otherwise you just ship confusion faster."
    if "gtm" in lowered:
        return "GTM with agents gets interesting when the agent is forced to show sources, not just produce more copy."
    if "?" in post:
        return "I think the real question is what result would make you stop and say this actually worked."
    keywords = extract_keywords(post)
    if keywords:
        return f"The useful bit here is {keywords[0]}. That is usually where the generic advice starts becoming real."
    return "This is useful because it points at the actual work, not just the clean lesson after it."


def extract_keywords(text: str) -> list[str]:
    candidates = []
    for phrase in ["Claude Code", "AI agents", "workflow", "GTM", "vibe coding", "building in public", "product"]:
        if phrase.lower() in text.lower():
            candidates.append(phrase)
    if candidates:
        return candidates
    words = re.findall(r"[A-Za-z][A-Za-z0-9+.-]{3,}", text)
    blocked = {"this", "that", "with", "from", "have", "works", "show", "more", "just", "they", "your"}
    return [word for word in words if word.lower() not in blocked][:2]


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
