#!/usr/bin/env bash
# Mac only. Scout X, then sync the day's candidates to the private repo so a Claude Code
# session on the web can pick them up. Draft-only: this never posts anything anywhere.
#
#   scripts/morning.sh              scout, commit state/, push
#   NO_PUSH=1 scripts/morning.sh    scout only
#   scripts/morning.sh --force      extra args go to `daily scout`
set -euo pipefail
cd "$(dirname "$0")/.."
export BRAND_DATA_DIR="$PWD/state"
# shellcheck disable=SC1091
source .venv/bin/activate 2>/dev/null || true

git pull --rebase --autostash origin main || echo "warning: could not pull, continuing with local state"
python3 -m brand_agents.daily scout "$@"

if [[ "${NO_PUSH:-}" == "1" ]]; then
  echo "NO_PUSH=1, not syncing state"
  exit 0
fi
git add state
if git diff --cached --quiet; then
  echo "nothing new to sync"
else
  git commit -q -m "state: morning scout $(date +%F)"
  git push origin main
  echo "synced state/ to the private repo"
fi
