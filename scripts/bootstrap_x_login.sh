#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v git >/dev/null 2>&1; then
  echo "git is not installed. Install Xcode Command Line Tools first: xcode-select --install" >&2
  exit 1
fi

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Updating repo..."
  git pull --ff-only origin main || true
fi

PYTHON_BIN=""
for candidate in /usr/bin/python3 python3.12 python3.11 python3; do
  if command -v "$candidate" >/dev/null 2>&1; then
    if "$candidate" - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if sys.version_info >= (3, 10) else 1)
PY
    then
      PYTHON_BIN="$candidate"
      break
    fi
  fi
done

if [ -z "$PYTHON_BIN" ]; then
  echo "No working Python 3.10+ found. Install Xcode Command Line Tools: xcode-select --install" >&2
  exit 1
fi

echo "Using Python: $($PYTHON_BIN --version) at $(command -v "$PYTHON_BIN" || echo "$PYTHON_BIN")"

if [ ! -d .venv ]; then
  "$PYTHON_BIN" -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install playwright
python -m playwright install chromium

BROWSER_CHANNEL=()
if [[ "$(uname -s)" == "Darwin" ]] && [[ -d "/Applications/Google Chrome.app" ]]; then
  BROWSER_CHANNEL=(--channel chrome)
  echo "Using installed Google Chrome for login instead of Chrome for Testing."
fi

cat <<'MSG'

Opening X login now.
Log in in the browser window.
When your X home feed is visible, return to this terminal and press Enter.

MSG

python -m brand_agents.providers.x_playwright.login "${BROWSER_CHANNEL[@]}"

cat <<'MSG'

Saved X session state.
Testing X target discovery with 3 targets...

MSG

python -m brand_agents.providers.x_playwright.find_posts --limit 3 --headed "${BROWSER_CHANNEL[@]}" --out /tmp/x-targets.json || {
  echo "Login saved, but discovery test failed. You can retry later with:" >&2
  echo "python -m brand_agents.providers.x_playwright.find_posts --limit 10 --out /tmp/x-targets.json" >&2
  exit 0
}
python -m brand_agents.reply_scout --targets /tmp/x-targets.json --out /tmp/x-replies.md

echo "Done. Draft replies written to /tmp/x-replies.md"
