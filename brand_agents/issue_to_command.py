"""Convert a GitHub issue-form body into a mobile runner command JSON."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def sections(body: str) -> dict[str, str]:
    result: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    for line in body.splitlines():
        match = re.match(r"^###\s+(.+?)\s*$", line)
        if match:
            if current:
                result[current] = "\n".join(buf).strip()
            current = match.group(1).strip()
            buf = []
        elif current:
            buf.append(line)
    if current:
        result[current] = "\n".join(buf).strip()
    return result


def strip_fences(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 2 and lines[-1].strip() == "```":
            return "\n".join(lines[1:-1]).strip()
    return stripped


def parse_json_field(value: str, fallback):
    value = strip_fences(value)
    if not value or value == "_No response_":
        return fallback
    return json.loads(value)


def convert(body: str) -> dict:
    sec = sections(body)
    command = sec.get("Command", "").strip()
    if command == "Draft from raw idea":
        return {
            "command": "draft",
            "platform": sec.get("Platform", "x").strip().lower(),
            "raw_idea": sec.get("Raw idea", "").strip(),
            "facts": parse_json_field(sec.get("Facts JSON", ""), []),
        }
    if command == "Reply target scout":
        return {
            "command": "reply_scout",
            "targets": parse_json_field(sec.get("Targets JSON", ""), []),
        }
    if command == "Weekly follower report":
        return {
            "command": "weekly_report",
            "counts": parse_json_field(sec.get("Counts JSON", ""), {}),
        }
    raise ValueError(f"unknown Command section: {command!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--issue-body", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    command = convert(args.issue_body.read_text(encoding="utf-8"))
    args.out.write_text(json.dumps(command, indent=2) + "\n", encoding="utf-8")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

