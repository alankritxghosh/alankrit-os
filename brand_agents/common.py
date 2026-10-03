"""Shared helpers for draft-only brand agents.

These tools never post, schedule, send, like, follow, connect, DM or email.
They only write local markdown outputs for Alankrit to review.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "brand" / "agent_outputs"
VOICE_MEMORY = ROOT / "memory" / "voice_examples.jsonl"
FACT_MEMORY = ROOT / "memory" / "facts.jsonl"
POLICY = ROOT / "BRAND_AGENT_POLICY.md"

FORBIDDEN_DASHES = {"\u2014": "em dash", "\u2013": "en dash"}
NO_GO_PHRASES = [
    "compare notes",
    "would love to connect",
    "would love to chat",
    "honestly",
]
PLATFORM_LIMITS = {
    "x": 280,
    "linkedin_note": 180,
}


@dataclass
class Check:
    name: str
    passed: bool
    detail: str


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def write_markdown(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return path


def today_slug() -> str:
    return date.today().isoformat()


def load_alankrit_voice_examples(limit: int = 12) -> list[dict]:
    rows = [
        row
        for row in read_jsonl(VOICE_MEMORY)
        if row.get("author") == "ALANKRIT" and row.get("verified_verbatim") is True
    ]
    rows.sort(key=lambda row: (str(row.get("date", "")), row.get("id", "")), reverse=True)
    return rows[:limit]


def load_fact_sources() -> list[dict]:
    return read_jsonl(FACT_MEMORY)


def load_fact_inputs(path: Path | None) -> list[dict]:
    if path is None:
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("facts input must be a JSON array")
    for item in data:
        if not item.get("claim") or not item.get("source"):
            raise ValueError("each fact needs claim and source")
    return data


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9']+", text)


def one_thought_per_line(text: str) -> bool:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return bool(lines) and all(len(words(line)) <= 32 for line in lines)


def has_it_is_x_not_y(text: str) -> bool:
    normalized = " ".join(text.lower().split())
    return bool(re.search(r"\bit(?:'s| is) not\b.+\bit(?:'s| is)\b", normalized))


def check_voice(text: str, platform: str = "x") -> list[Check]:
    checks: list[Check] = []
    checks.append(Check("no em dash or en dash", not any(ch in text for ch in FORBIDDEN_DASHES), "No long dash characters."))
    checks.append(Check("no hashtags", "#" not in text, "No hashtags."))
    checks.append(Check("no emoji", not re.search(r"[\U00010000-\U0010ffff]", text), "No emoji."))
    lowered = text.lower()
    banned = [phrase for phrase in NO_GO_PHRASES if phrase in lowered]
    checks.append(Check("no banned outreach phrases", not banned, ", ".join(banned) if banned else "No banned phrases."))
    checks.append(Check("no it is X not Y reframe", not has_it_is_x_not_y(text), "Avoids the banned contrast template."))
    checks.append(Check("one thought per line", one_thought_per_line(text), "Every non-empty line is compact."))
    checks.append(Check("never geopolitics", "geopolitic" not in lowered, "No geopolitics."))
    checks.append(Check("no job framing", "job" not in lowered and "hiring" not in lowered, "No job-hunting framing."))
    if platform == "x":
        checks.append(Check("x under 280 characters", len(text) <= 280, f"{len(text)} characters."))
    if platform == "linkedin_note":
        checks.append(Check("linkedin note under 180 characters", len(text) <= 180, f"{len(text)} characters."))
    if platform.startswith("linkedin"):
        checks.append(Check("no linkedin swearing", not re.search(r"\b(fuck|fucking|shit)\b", lowered), "No swearing on LinkedIn."))
    return checks


def render_checks(checks: Iterable[Check]) -> str:
    lines = []
    for check in checks:
        mark = "PASS" if check.passed else "FAIL"
        lines.append(f"- {mark}: {check.name} ({check.detail})")
    return "\n".join(lines)


def require_all_pass(checks: Iterable[Check]) -> bool:
    return all(check.passed for check in checks)


def output_path(kind: str, stem: str | None = None) -> Path:
    name = stem or f"{today_slug()}-{kind}"
    return OUTPUT_DIR / kind / f"{name}.md"


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--out", type=Path, help="optional markdown output path")

