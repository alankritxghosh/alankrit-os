"""Where brand_agents keeps its files.

Two locations, kept apart on purpose:

* SECRET_DIR (~/.alankrit-os): X login cookies and the Telegram token. Never inside the repo.
* data_dir(): working data (daily folders, the decision log, seen URLs). Defaults to
  SECRET_DIR on the Mac. Set BRAND_DATA_DIR=<repo>/state to keep it in the private repo, so a
  Claude Code session on the web (which cannot see the Mac) reads and writes the same data.
"""
from __future__ import annotations

import os
from pathlib import Path

SECRET_DIR = Path.home() / ".alankrit-os"
REPO_ROOT = Path(__file__).resolve().parent.parent


def data_dir() -> Path:
    override = os.environ.get("BRAND_DATA_DIR", "").strip()
    return Path(override).expanduser() if override else SECRET_DIR
