"""Draft a local-only post from Alankrit's raw idea."""
from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

from .common import (
    add_common_args,
    check_voice,
    load_alankrit_voice_examples,
    load_fact_inputs,
    output_path,
    render_checks,
    require_all_pass,
    write_markdown,
)


MAX_X_CHARS = 280


def compact_lines(text: str, max_lines: int = 4) -> list[str]:
    parts = [part.strip(" .") for part in text.replace("\n", " ").split(".") if part.strip()]
    if len(parts) == 1:
        raw = parts[0]
        chunks = [chunk.strip() for chunk in raw.split(",") if chunk.strip()]
        parts = chunks if len(chunks) > 1 else [raw]
    return parts[:max_lines]


def build_variants(raw_idea: str, platform: str, facts: list[dict]) -> list[str]:
    lines = compact_lines(raw_idea)
    if not lines:
        raise ValueError("raw idea is empty")

    specific = facts[0]["claim"] if facts else None
    variant_a = "\n".join(lines[:3])
    if specific and specific.lower() not in variant_a.lower():
        variant_a = f"{variant_a}\n{specific}"

    opener = lines[0]
    rest = lines[1:3]
    if platform == "x":
        variant_b_lines = [opener]
        if specific:
            variant_b_lines.append(specific)
        variant_b_lines.extend(rest[:1])
    else:
        variant_b_lines = [opener] + rest
        if specific:
            variant_b_lines.append(specific)
    variant_b = "\n".join(variant_b_lines)
    variants = [variant_a.strip(), variant_b.strip()]
    if platform == "x":
        variants.append(short_x_variant(lines, specific))
    return dedupe([fit_platform(variant, platform) for variant in variants])


def short_x_variant(lines: list[str], specific: str | None) -> str:
    seed = lines[0]
    if len(seed) > 170:
        seed = seed[:167].rsplit(" ", 1)[0]
    if specific:
        fact = specific
        if len(fact) > 90:
            fact = fact[:87].rsplit(" ", 1)[0]
        return f"{seed}\n{fact}".strip()
    return seed.strip()


def fit_platform(text: str, platform: str) -> str:
    if platform != "x" or len(text) <= MAX_X_CHARS:
        return text
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    kept: list[str] = []
    for line in lines:
        candidate = "\n".join(kept + [line])
        if len(candidate) <= MAX_X_CHARS:
            kept.append(line)
    if kept:
        return "\n".join(kept)
    return text[:MAX_X_CHARS].rsplit(" ", 1)[0].strip()


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item and item not in seen:
            result.append(item)
            seen.add(item)
    return result[:2]


def render_report(raw_idea: str, platform: str, facts: list[dict], variants: list[str]) -> str:
    voice_examples = load_alankrit_voice_examples()
    blocks: list[str] = [
        "# Draft Agent Output",
        "",
        "Draft-only. Nothing was posted, scheduled or sent.",
        "",
        "## Raw Idea",
        "",
        raw_idea.strip(),
        "",
        "## Voice Examples Used",
        "",
    ]
    for row in voice_examples[:8]:
        blocks.append(f"- {row['id']}: \"{row['content']}\"")
        blocks.append(f"  Source: {row['source']}")
    if not voice_examples:
        blocks.append("- None found. This should block drafting.")

    blocks.extend(["", "## Sources For Facts", ""])
    if facts:
        for item in facts:
            blocks.append(f"- Claim: {item['claim']}")
            blocks.append(f"  Source: {item['source']}")
    else:
        blocks.append("- No external facts supplied. Draft must use only the raw idea.")

    for idx, draft in enumerate(variants, start=1):
        checks = check_voice(draft, platform)
        status = "PASS" if require_all_pass(checks) else "FAIL"
        blocks.extend([
            "",
            f"## Variant {idx}",
            "",
            draft,
            "",
            f"## Voice Check Variant {idx}: {status}",
            "",
            render_checks(checks),
        ])
    return "\n".join(blocks)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--idea", type=Path, required=True, help="text file with Alankrit's raw idea")
    parser.add_argument("--facts", type=Path, help="JSON array of {claim, source}")
    parser.add_argument("--platform", choices=["x", "linkedin", "substack"], default="x")
    add_common_args(parser)
    args = parser.parse_args()

    raw_idea = args.idea.read_text(encoding="utf-8").strip()
    facts = load_fact_inputs(args.facts)
    variants = build_variants(raw_idea, args.platform, facts)
    report = render_report(raw_idea, args.platform, facts, variants)
    out = args.out or output_path("drafts")
    write_markdown(out, report)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
