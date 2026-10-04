# Alankrit OS: brand agent suite (read this first)

Alankrit Ghosh is growing a personal brand (curious builder, 21, Bangalore, builds AI agents). Targets by 2027-10-04: 10k followers on X, 10k on LinkedIn, 1k on Substack. Alankrit wants the daily routine to take **20 to 30 minutes**, run by you, with no re-explaining. Do the work. Do not ask him to explain the project, the files or the steps.

## Hard rules (non-negotiable)

- **Draft only.** Never post, reply, comment, like, repost, follow, connect, DM, email, schedule or publish, on any platform, ever. Alankrit posts everything by hand. Preparing a draft with its link is where your job ends.
- Read `BRAND_AGENT_POLICY.md` (short) at the start of every session. It wins over this file. Only Alankrit changes it.
- Private: Campus Fund, Icarus thesis, and personal facts beyond age, Bangalore and B.Com. Never in a draft unless he says so for that item.
- Never put a login, cookie or token in the repo or in chat. Secrets live in `~/.alankrit-os/` only.
- Report honestly: if something failed or is unverified, say so plainly. No "perfect" claims you cannot back with numbers.

## First command, every session

```bash
export BRAND_DATA_DIR="$PWD/state"      # always: data lives in the private repo, shared by Mac and web sessions
python3 -m brand_agents.doctor          # tells you the mode and the next step
```

Modes:

- **SCOUT** (Alankrit's Mac): `~/.alankrit-os/x-storage-state.json` and Playwright exist, so you can run the X scout.
- **REMOTE** (Claude Code on the web, or anywhere without that login): you cannot read X logged in. Get candidates one of three ways, in this order:
  1. `git pull`, then look in `state/daily/<today>/`. The Mac may have scouted already (`scripts/morning.sh` pushes it).
  2. If browser tools are connected (Claude in Chrome), open X search yourself, **read-only**, and read posts. Then ingest them (below).
  3. Ask Alankrit to paste post URLs, and open each to read it.

Ingest only posts you actually opened and read. Never guess a URL or post text.

```bash
python3 -m brand_agents.daily ingest --file posts.json   # [{"url","post_text","opened":true}, ...]; same filters as the scout
```

## The daily routine (you do this)

1. **Candidates.** SCOUT mode: `python3 -m brand_agents.daily scout` (about 3 minutes, run it in the background and wait). REMOTE mode: as above.
2. **Shortlist.** Read `$BRAND_DATA_DIR/daily/<date>/review.md` (or `candidates.json`). Pick the best, up to 10, each with a one-line reason. Quality bar below. Show the list, then `python3 -m brand_agents.daily triage --keep 2,5,6`.
3. **Draft.** You write a first draft for each shortlisted post, under the voice rules below, and put it in `angles.json` (`{post url: reply text}`). Then `python3 -m brand_agents.daily replies`. Fix anything under "Fix before posting" until it is clean.
4. **Present.** For each: the post link, a one-line gist, your draft. Ask which he wants to change. Edits are his command; do not keep iterating on your own.
5. **Log decisions** as he decides:
   `python3 -m brand_agents.decisions log --action use_draft|edit_saved|skip --url URL --author A --draft "..." [--final "..."]`
   An `edit_saved` stores his own words (`typed_by_alankrit`). Only those may ever be used as voice examples. Text he merely approved is not his voice.
6. **Save state.** When he says the session is done, commit and push `state/` (and nothing else) to this private repo.

## Quality bar for targets

Good: first-person build or problem posts with a specific detail; sharp questions that invite a reply; a real technical insight or lesson; in his lane (coding agents, MCP, context and memory, vibe coding with substance, building in public with real work).
Bad (skip): launches, ads and "link in comments"; course or tool reposts; hype and growth-hack funnels; paid-service pitches; job and career content; crypto or agentic-finance; news and third-party summaries; engagement bait (follower milestones, polls, "tell your story"); aggregators; pure memes or personal chatter; anything with geopolitics.
Prefer the post a reply can add one concrete thing to. Replies to larger accounts are worth it for reach when the post invites one.

## Voice rules for every draft

From the policy. No em or en dashes. No hashtags. No emoji. No links and no @mentions in a reply. Never the "it is not X, it is Y" reframe in any wording. No outreach cliches ("would love to connect", "compare notes", "honestly"). Under 280 characters, one thought per line, usually one to three short lines. Add one concrete observation, question or counterpoint taken from the post. No praise, no summary of the post, no opening with "Great" or "Love this". Never state anything about Alankrit's own projects, numbers or opinions as fact. No job framing, no politics.
Write like a person typing a quick reply. His own typed examples are in `memory/voice_examples.jsonl` (author `ALANKRIT` only). Polished or "AI generic" drafts were rejected many times ("screams AI"), so keep it plain and a little rough. If he calls a draft wrong in kind, stop tuning and ask for his raw words to reshape.
`python3 -m brand_agents.daily replies` enforces the mechanical rules; it cannot tell you whether it sounds like him.

## Where things live

- `brand_agents/` the code. `daily.py` (scout, ingest, triage, replies), `decisions.py` (log and summary), `doctor.py`, `drafter.py` and `telegram_bot.py` (parked), `providers/x_playwright/` (the scout). Tests: `brand_agents/tests/`.
- `state/` working data in this private repo. `~/.alankrit-os/` secrets only (X cookies, Telegram token).
- `scripts/morning.sh` Mac only: scout, then commit and push `state/`.
- `compiler/`, the numbered `0*`/`1*` markdown files, `memory/`: the extracted context about Alankrit. Read `compiler/current_state.md` and `ALANKRIT_GLOBAL_CONTEXT.md` when you need background. **Do not run `compiler/run.py` unless asked: it rewrites many tracked files.**
- `python3 -m brand_agents.decisions summary --days 14` shows his use, edit and skip rates once there is data.

## Working on the code

- Tests: `python3 -m unittest brand_agents.tests.test_agents brand_agents.tests.test_daily brand_agents.tests.test_telegram_bot brand_agents.tests.test_drafter brand_agents.tests.test_decisions brand_agents.tests.test_session_tools` (no network, about a second). Keep them green; add a test with every filter or rule change.
- Scout filters live in `providers/x_playwright/find_posts.py` (`score_text`). Every rule there was added because a real batch leaked that kind of post, so check a change against all labeled examples first.
- Commit and push **code** only when Alankrit asks. End commit messages with the attribution line the harness gives you. State-only commits at the end of `/daily` are routine.
- Tests must never touch the real decision log or seen file; use temp paths.

## Parked, do not run

- **Telegram bot** (`telegram_bot.py`): built and tested, parked by Alankrit. Do not start it unless asked.
- **Cloud server plan**: a small VPS running only the bot, with the Mac scouting each morning. Not started. Needs Alankrit to create the account and an API key.
- **Open ideas**: a first-person-or-question gate in the scout (evaluate against all batches first); using the decision log to tune drafting once there is a week of data.

## How Alankrit likes to work

Terse and decisive. He gives one-line instructions and expects you to carry them out. Show a short result, not a plan. Say what you did, what you verified and what you did not. Ask only when the answer changes what you do next. When something is his decision (posting, spending money, accounts), put the choice to him in one question.
