"""Open X for manual login and save Playwright storage state.

This is intentionally manual. The script does not bypass login, CAPTCHA, 2FA or
platform checks. It opens a browser, waits for Alankrit to log in, then saves
cookies outside git by default.
"""
from __future__ import annotations

import argparse
from pathlib import Path

DEFAULT_STATE = Path.home() / ".alankrit-os" / "x-storage-state.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    args = parser.parse_args()

    args.state.parent.mkdir(parents=True, exist_ok=True)
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://x.com/login", wait_until="domcontentloaded")
        print("Log in to X in the opened browser.")
        print("When the home feed is visible, return here and press Enter.")
        input()
        context.storage_state(path=str(args.state))
        browser.close()
    print(args.state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
