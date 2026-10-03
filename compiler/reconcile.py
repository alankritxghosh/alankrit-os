"""Attach authored inputs that postdate the extractions (compiler/current_state.md).

The extractions are snapshots. When Alankrit states something newer in chat, it goes in
current_state.md with its date; it is shown next to, never merged into, the extracted records.
"""
from __future__ import annotations

from common import COMPILER_DIR


def reconcile(model: dict) -> dict:
    f = COMPILER_DIR / "current_state.md"
    model["current_state"] = f.read_text(encoding="utf-8") if f.exists() else ""
    return model
