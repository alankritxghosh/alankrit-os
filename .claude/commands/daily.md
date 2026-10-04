---
description: Run today's brand routine end to end (find targets, shortlist, draft, voice-check, log decisions)
---

Run Alankrit's daily routine. Do the work yourself; do not ask him to explain the project or the steps.

1. Read `CLAUDE.md` and `BRAND_AGENT_POLICY.md` if you have not this session.
2. `export BRAND_DATA_DIR="$PWD/state"` (when this repo is a Claude Code web checkout, or `state/` exists) then run `python3 -m brand_agents.doctor` and follow its **Next** list.
3. Follow the routine in `CLAUDE.md` section "The daily routine": get candidates, shortlist the best ones with one-line reasons, draft replies yourself under the voice rules, run `python3 -m brand_agents.daily replies`, and show him each reply with its link.
4. When he says use, edit or skip for a post, record it with `python3 -m brand_agents.decisions log`.
5. Never post, reply, like, follow or message anyone. He posts by hand.

Extra instructions from him for this run: $ARGUMENTS
