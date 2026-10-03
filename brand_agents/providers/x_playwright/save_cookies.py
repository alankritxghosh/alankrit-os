"""Create Playwright X storage state from locally copied X cookies.

Use this only on Alankrit's machine. Do not paste cookies into chat, commit them,
or store them anywhere except the local storage-state file.
"""
from __future__ import annotations

import argparse
import getpass
import json
from pathlib import Path

from .login import DEFAULT_STATE


def build_state(auth_token: str, ct0: str | None) -> dict:
    cookies = [
        {
            "name": "auth_token",
            "value": auth_token,
            "domain": ".x.com",
            "path": "/",
            "expires": -1,
            "httpOnly": True,
            "secure": True,
            "sameSite": "Lax",
        },
        {
            "name": "auth_token",
            "value": auth_token,
            "domain": ".twitter.com",
            "path": "/",
            "expires": -1,
            "httpOnly": True,
            "secure": True,
            "sameSite": "Lax",
        },
    ]
    if ct0:
        for domain in [".x.com", ".twitter.com"]:
            cookies.append({
                "name": "ct0",
                "value": ct0,
                "domain": domain,
                "path": "/",
                "expires": -1,
                "httpOnly": False,
                "secure": True,
                "sameSite": "Lax",
            })
    return {"cookies": cookies, "origins": []}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--auth-token", help="X auth_token cookie. Prefer the prompt instead of shell history.")
    parser.add_argument("--ct0", help="X ct0 cookie. Optional but recommended.")
    args = parser.parse_args()

    auth_token = args.auth_token or getpass.getpass("Paste X auth_token cookie (input hidden): ").strip()
    ct0 = args.ct0
    if ct0 is None:
        ct0 = getpass.getpass("Paste X ct0 cookie if available, else press Enter (input hidden): ").strip() or None
    if not auth_token:
        raise SystemExit("auth_token is required")

    args.state.parent.mkdir(parents=True, exist_ok=True)
    args.state.write_text(json.dumps(build_state(auth_token, ct0), indent=2) + "\n", encoding="utf-8")
    args.state.chmod(0o600)
    print(args.state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

