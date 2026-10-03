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


def draft_reply(target: dict) -> str:
    angle = (target.get("angle") or "").strip()
    if angle:
        return angle[:260].strip()
    post = " ".join(str(target["post_text"]).split())
    if "?" in post:
        return "This is worth asking because the answer changes what you build next."
    return "The useful bit here is the specific example, not the generic lesson."


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
        blocks.extend([
            f"## Target {idx}",
            "",
            f"- URL: {target['url']}",
            f"- Author: {target.get('author', 'UNKNOWN')}",
            f"- Checked: {target.get('checked_at', 'UNKNOWN')}",
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

