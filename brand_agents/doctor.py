"""One command that tells a fresh Claude Code session where it is and what to do next.

    python3 -m brand_agents.doctor          # readable
    python3 -m brand_agents.doctor --json   # for scripts

Read-only. It inspects files and git status; it never posts, browses or changes anything.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

from .common import check_voice, require_all_pass
from .paths import REPO_ROOT, SECRET_DIR, data_dir


def read_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def git_state(repo: Path) -> dict:
    def run(*args: str) -> str | None:
        try:
            done = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, timeout=15)
        except (OSError, subprocess.TimeoutExpired):
            return None
        return done.stdout.strip() if done.returncode == 0 else None

    branch = run("rev-parse", "--abbrev-ref", "HEAD")
    if branch is None:
        return {"available": False}
    status = run("status", "--porcelain") or ""
    return {
        "available": True,
        "branch": branch,
        "uncommitted": len([line for line in status.splitlines() if line.strip() and not line.startswith("?? .venv")]),
    }


def day_state(directory: Path) -> dict:
    candidates = read_json(directory / "candidates.json", [])
    picks = read_json(directory / "picks.json", None)
    angles = read_json(directory / "angles.json", {})
    angles = angles if isinstance(angles, dict) else {}
    written = {url: text for url, text in angles.items() if isinstance(text, str) and text.strip()}
    ready = sum(1 for text in written.values() if require_all_pass(check_voice(text, "x")))
    return {
        "exists": (directory / "candidates.json").exists(),
        "candidates": len(candidates) if isinstance(candidates, list) else 0,
        "shortlisted": len(picks) if isinstance(picks, list) else None,
        "replies_written": len(written),
        "replies_ready": ready,
        "replies_failing": len(written) - ready,
    }


def diagnose(today: str | None = None, repo: Path = REPO_ROOT, secret_dir: Path | None = None, data: Path | None = None, git: bool = True) -> dict:
    secret = secret_dir if secret_dir is not None else SECRET_DIR
    data_path = data if data is not None else data_dir()
    day = today or date.today().isoformat()
    x_state = secret / "x-storage-state.json"
    has_playwright = importlib.util.find_spec("playwright") is not None
    can_scout = x_state.exists() and has_playwright
    directory = data_path / "daily" / day
    today_state = day_state(directory)
    seen = read_json(data_path / "x-seen-urls.json", [])
    report = {
        "date": day,
        "mode": "scout" if can_scout else "remote",
        "can_scout": can_scout,
        "x_login_present": x_state.exists(),
        "playwright_installed": has_playwright,
        "policy_present": (repo / "BRAND_AGENT_POLICY.md").exists(),
        "data_dir": str(data_path),
        "data_dir_in_repo": repo.resolve() in data_path.resolve().parents or data_path.resolve() == repo.resolve(),
        "seen_urls": len(seen) if isinstance(seen, list) else 0,
        "today": today_state,
        "git": git_state(repo) if git else {"available": False},
        "python": sys.version.split()[0],
    }
    report["next"] = next_steps(report)
    return report


def next_steps(report: dict) -> list[str]:
    steps: list[str] = []
    if not report["policy_present"]:
        steps.append("BRAND_AGENT_POLICY.md is missing. Stop and tell Alankrit before doing anything.")
        return steps
    today = report["today"]
    if not today["exists"]:
        if report["can_scout"]:
            steps.append("No candidates today. Run `python3 -m brand_agents.daily scout` (about 3 minutes, run it in the background).")
        else:
            steps.append("No candidates today and no X login here. Get posts another way: pull the repo for a morning scout from the Mac, "
                         "read posts in the browser tools if connected, or ask Alankrit to paste URLs. Then `daily ingest`.")
    elif today["shortlisted"] is None:
        steps.append(f"{today['candidates']} candidates, not triaged. Read review.md, pick the best, run `daily triage --keep ...`.")
    elif today["replies_written"] == 0:
        steps.append(f"{today['shortlisted']} shortlisted. Draft a reply for each, put them in angles.json, then run `daily replies`.")
    else:
        if today["replies_failing"]:
            steps.append(f"{today['replies_failing']} written replies fail the voice check. Fix them, then run `daily replies`.")
        steps.append(f"{today['replies_ready']} replies ready. Show them to Alankrit to post by hand, then log what he did with `decisions log`.")
    if report["data_dir_in_repo"] and report["git"].get("available") and report["git"]["uncommitted"]:
        steps.append("State changes are uncommitted. Commit and push `state/` when Alankrit says the session is done.")
    return steps


def format_report(report: dict) -> str:
    today = report["today"]
    lines = [
        f"Alankrit OS doctor, {report['date']}",
        f"Mode: {report['mode'].upper()}  ({'X login and Playwright found, can scout' if report['can_scout'] else 'cannot scout here'})",
        f"Data dir: {report['data_dir']}" + ("  (inside the repo)" if report["data_dir_in_repo"] else ""),
        f"Today: {today['candidates']} candidates" + (f", {today['shortlisted']} shortlisted" if today["shortlisted"] is not None else "")
        + f", {today['replies_written']} replies written ({today['replies_ready']} ready, {today['replies_failing']} failing)"
        if today["exists"] else "Today: nothing yet",
        f"Seen URLs: {report['seen_urls']}",
    ]
    if report["git"].get("available"):
        lines.append(f"Git: {report['git']['branch']}, {report['git']['uncommitted']} uncommitted file(s)")
    lines.append("")
    lines.append("Next:")
    lines.extend(f"  - {step}" for step in report["next"])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    report = diagnose()
    print(json.dumps(report, indent=2) if args.json else format_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
