"""Shared configuration and helpers for the Global Alankrit Context compiler.

The source corpus is READ-ONLY. Every write goes through `out_path()`, which
refuses any path inside the configured source directory.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

DEFAULT_SOURCE = "/Users/alankritghosh/JARVIS /jarvis_engineering/context-extraction"
WORKSPACE = Path(__file__).resolve().parent.parent
COMPILER_DIR = Path(__file__).resolve().parent
COMPILE_DATE = "2026-10-04"

# Canonical artifact names a project extraction is expected to contain.
EXPECTED_ARTIFACTS = [
    "00_PROJECT_CONTEXT.md",
    "01_ALANKRIT_CONTEXT.md",
    "02_DECISION_REGISTER.md",
    "03_BELIEF_SYSTEM.md",
    "04_REASONING_PATTERNS.md",
    "05_WORKING_STYLE.md",
    "06_VOICE_PROFILE.md",
    "07_PROJECT_TIMELINE.md",
    "08_FAILURES_AND_LESSONS.md",
    "09_OPEN_LOOPS.md",
    "10_CONTRADICTIONS.md",
    "11_TRANSFERABLE_CONTEXT.md",
    "12_GLOSSARY.md",
    "13_KNOWLEDGE_GRAPH.md",
    "HANDOFF_TO_ALANKRIT_OS.md",
    "extraction_manifest.json",
]
# v2 protocol (2026-10-03T16:11Z) renamed and added artifacts; either schema is valid
EXPECTED_ARTIFACTS_V2 = [
    "00_PROJECT_CONTEXT.md", "01_PROJECT_TIMELINE.md", "02_DECISION_REGISTER.md", "03_BELIEF_SYSTEM.md",
    "04_BELIEF_EVOLUTION.md", "05_REASONING_PATTERNS.md", "06_WORKING_STYLE.md", "07_VOICE_PROFILE.md",
    "08_FAILURES_AND_LESSONS.md", "09_OPEN_LOOPS.md", "10_CONTRADICTIONS.md", "11_TRANSFERABLE_CONTEXT.md",
    "12_ALANKRIT_CONTEXT.md", "13_KNOWLEDGE_GRAPH.md", "HANDOFF_TO_ALANKRIT_OS.md", "extraction_manifest.json",
]


BUNDLED_SOURCE = WORKSPACE / "context-extraction"


def source_dir() -> Path:
    """env var > the original corpus if it exists on this machine > the extractions bundled in this repo."""
    env = os.environ.get("ALANKRIT_SOURCE_DIR")
    if env:
        return Path(env).resolve()
    default = Path(DEFAULT_SOURCE)
    return default.resolve() if default.is_dir() else BUNDLED_SOURCE.resolve()


def out_path(rel: str) -> Path:
    """Resolve a workspace output path, refusing anything inside the source corpus."""
    p = (WORKSPACE / rel).resolve()
    src = source_dir()
    if p == src or src in p.parents:
        raise PermissionError(f"refusing to write inside source corpus: {p}")
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def write_text(rel: str, text: str) -> Path:
    p = out_path(rel)
    p.write_text(text, encoding="utf-8")
    return p


def write_json(rel: str, obj) -> Path:
    return write_text(rel, json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def write_jsonl(rel: str, rows) -> Path:
    return write_text(rel, "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


ISO_FULL = re.compile(r"(20\d\d)-(\d\d)-(\d\d)")
ISO_MONTH = re.compile(r"(20\d\d)-(\d\d)(?!-\d)")
SHORT = re.compile(r"(?<![\d-])(\d\d)-(\d\d)(?![\d])")


def norm_date(raw: str, default_year: str = "2026") -> str | None:
    """Return the first date in `raw` as YYYY-MM-DD (or YYYY-MM), else None.

    Short `MM-DD` forms are assumed to be in `default_year`: every dated event in
    the current corpus falls in 2026. The raw string is always kept alongside.
    """
    if not raw:
        return None
    m = ISO_FULL.search(raw)
    if m:
        return m.group(0)
    m = SHORT.search(raw)
    if m and 1 <= int(m.group(1)) <= 12 and 1 <= int(m.group(2)) <= 31:
        return f"{default_year}-{m.group(1)}-{m.group(2)}"
    m = ISO_MONTH.search(raw)
    if m:
        return m.group(0)
    return None


CONF = re.compile(r"\b(HIGH|MEDIUM-HIGH|MEDIUM|LOW)\b")


def find_conf(text: str, default: str = "UNSTATED") -> str:
    m = CONF.search(text or "")
    return m.group(1) if m else default


REF = re.compile(r"\[([a-z0-9-]+):([A-Za-z]+[0-9]+(?:L[0-9]+)?|MANIFEST)\]")
REF_BARE = re.compile(r"\b(icarus|global):([A-Za-z]+[0-9]+(?:L[0-9]+)?|MANIFEST)\b")


# Extractions whose claims about Alankrit restate another project's evidence. Their rows are kept
# but never counted as independent (see alankrit-os/HANDOFF: "Count them once").
DERIVED_PROJECTS = {"alankrit-os"}
