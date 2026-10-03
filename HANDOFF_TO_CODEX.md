# Handoff prompt for Codex: continue and finish Alankrit OS

You are taking over a project from Claude, whose session is ending. Work carefully, change as little as needed, and ask Alankrit before any decision that is his to make. Today's date when this was written: 2026-10-04 (IST).

## 1. What Alankrit OS is

A personal context layer for Alankrit Ghosh (21, Bangalore). Two stages:
1. **Per-project extractions**, one folder per project under `/Users/alankritghosh/JARVIS /jarvis_engineering/context-extraction/<slug>/` (note the trailing space in `JARVIS `). Each holds markdown docs, `extraction_manifest.json`, `HANDOFF_TO_ALANKRIT_OS.md` and `memory/*.jsonl`.
2. **A global compiler** in `/Users/alankritghosh/Alankrit OS ` (trailing space) that merges complete extractions into global documents and memory.

The goal: let autonomous agents help run Alankrit's personal brand (X, LinkedIn, Substack) using his real history, beliefs, voice and rules, without misrepresenting him.

## 2. Read these first, in this order

1. `/Users/alankritghosh/Alankrit OS /HANDOFF_TO_ALANKRIT_OS.md` (global handoff)
2. `/Users/alankritghosh/Alankrit OS /BRAND_AGENT_POLICY.md` (version 3, binding rules for any agent)
3. `/Users/alankritghosh/Alankrit OS /compiler/current_state.md` (Alankrit's own latest statements; overrides older extracted facts)
4. `/Users/alankritghosh/Alankrit OS /brand/scouting/2026-10-04-role-model-report-pass-2.md` (and the first-pass report next to it)
5. `.../context-extraction/icarus/HANDOFF_TO_ALANKRIT_OS.md`, `.../personal-brand/...`, `.../campus-fund/...`, `.../alankrit-os/...` (project handoffs)
6. `/Users/alankritghosh/Alankrit OS /16_VALIDATION_REPORT.md`

## 3. State at handoff

- **Compiler (v2) works.** `cd "/Users/alankritghosh/Alankrit OS " && python3 compiler/run.py` reads every complete extraction, writes `00_`…`16_` docs, `ALANKRIT_GLOBAL_CONTEXT.md`, `HANDOFF_TO_ALANKRIT_OS.md`, `memory/*.jsonl`, `voice_examples/`, `source_manifest.json`. Expected result: 15 PASS, 1 WARN (Icarus evidence is stale). It adds no judgments; it copies each extraction's records. Legacy v1 code is in `compiler/legacy_v1/`; old outputs are in `archive/2026-10-04_v1-compile/`.
- **Four complete extractions:** `icarus` (rebuilt under protocol v2 from 1,552 typed messages; evidence to 2026-09-13), `alankrit-os` (derived from Icarus; never count it as independent: `DERIVED_PROJECTS` in `compiler/common.py`), `personal-brand` (lean v2), `campus-fund` (lean v2, thin and confidential).
- **Alankrit's decisions on 2026-10-04:** brand goal 10k X / 10k LinkedIn / 1k Substack by 2027-10-04, back-loaded pace, monthly checkpoints (in the policy, confirmed by him); agents **draft and queue only, he posts everything himself**; **Claude writes first drafts, he edits on his command** (this supersedes the old rule in his Personal Brand vault); scout **5 role-model accounts per platform** (X and LinkedIn), read-only; Campus Fund is private; own failures only if occasional and funny; Icarus as story evidence only; age, Bangalore and B.Com may be used publicly. Baseline: X 31, LinkedIn 840, Substack 0. He works in the Founders Office at Campus Fund. The Icarus product thesis is still being revised; the new thesis is unknown.
- **Scouting passes 1 and 2 are done** (Chrome extension, read-only). Recommendation: keep Marc Lou, Tony Dinh, Dillon Mulroy (X) and Amy Watts, Lara Acosta (LinkedIn); replace the other five with smaller builders who grew recently. Not yet approved by him.

## 4. Work to finish, in priority order

1. **Scouting pass 3.** Find replacement candidates for the 5 swap slots (aim 1K–20K followers, grew in the last 12 months, builder or explorer lane, not geopolitics-led, not growth-service sellers). Verify handles and URLs by opening them; record follower counts with the date; check growth evidence; sample replies and comments on other people's posts; compute engagement vs followers. Write `brand/scouting/<date>-role-model-report-pass-3.md`. **Do not finalize the list: Alankrit approves or swaps.**
2. **Fix silent failures.** Every scheduled Claude job for the Icarus project (daily Work Queue status, weekly Gmail outreach sync) has failed with "OAuth session expired" since 2026-09-11. Re-authentication needs Alankrit; tell him. Then add a visible failure alert so silence never reads as success (policy section 8).
3. **Build the agents the policy allows, all draft-only:** (a) a drafting agent that writes first drafts from his raw idea, using only his own typed words as voice examples, runs the voice checklist and shows its result, with sources for every fact; (b) a reply-target scout that returns post links with draft replies, 20–25 a day in October, every link opened and verified; (c) a weekly report of follower counts vs the milestone table, with check dates. Nothing posts, likes, follows, connects or messages. Hand every output to Alankrit.
4. **Housekeeping:** update stale lines in `context-extraction/alankrit-os/HANDOFF_TO_ALANKRIT_OS.md` (it still says the compiler must read v2 files and that Icarus evidence stops 2026-09-10); keep `compiler/current_state.md` current whenever he states something newer; rerun the compiler after any change.
5. **Ask Alankrit, do not decide for him:** review the input gates in policy section 7 (replies/day, posts/week, Substack date); what "on my command" means in practice; whether to update the old first-draft rule in his Personal Brand vault (`/Users/alankritghosh/Personal Brand /CLAUDE.md`); whether to `git init` the workspace; the revised Icarus thesis; start date and terms of the Campus Fund role; who wrote `alankrit-brand-playbook.md`.

## 5. Out of scope on purpose

Alankrit chose **not** to extract eight session projects: Job Application Context, Marketing Intelligence, Design Portfolio, Solar Forecasting, thought-engine, Video Editor Workflow, Icarus V2, X Post CLI. Do not extract them unless he asks. Leftover partial folders may exist in `context-extraction/` (thought-engine has 3 files and no manifest). The compiler lists them as unassigned and never merges them. Do not delete them; ask him.

## 6. Non-negotiable rules

- **Never post, send, reply, like, follow, connect, DM or email on his behalf.** Preparing a draft is the end of your job.
- **Source projects and `context-extraction/` are read-only for the compiler.** Never modify a source project. Archive before overwriting an extraction (`context-extraction/archive/<timestamp>_<reason>/`).
- **Never invent.** Every fact traces to a source. Quote verbatim or not at all. Label EXPLICIT vs INFERRED. Hypotheses are not beliefs. A project choice is not a personality trait.
- **Authorship matters.** Text is Alankrit's only if he typed it. Quoted/attached assistant text, pasted specs and repo docs written by agents are not his voice. Lines containing em-dashes in short commands are likely accepted suggestions.
- **Voice rules for anything in his name:** no em-dashes (nor en-dash or spaced-hyphen substitutes), no hashtags, no "it is X not Y", no cliché outreach, swearing on X only, X posts under 280 characters, LinkedIn connection notes under 180, humour punches at himself, no job-hunting framing, **never geopolitics**, no Campus Fund content without his say-so.
- **Secrets and privacy:** never store API keys or tokens (two PostHog tokens appear in old transcripts), emails, phone numbers, salary figures or other people's contact details. Campus Fund notes are confidential.
- **Do not delete files without asking**; moving to an archive folder is fine.
- **Do not overclaim.** Report what was and was not done. A validation PASS means records are intact and traceable, not that judgments are true.

## 7. Practical notes learned the hard way

- Two folder names end with a space: `/Users/alankritghosh/Alankrit OS ` and `/Users/alankritghosh/JARVIS ` (and `Personal Brand `). Always quote paths.
- In zsh an unquoted `$VAR` holding a list is not word-split; a hash check that compares two empty strings "passes". Verify that inputs are non-empty.
- Browser scouting: X virtualizes the page, so only 5–7 posts exist in the DOM at once; use JavaScript with `await` and `window.scrollBy` loops and read `article` elements. To find a person's replies to others: search `from:handle -to:handle filter:replies` (Latest tab). LinkedIn activity pages show about 5 items; `/recent-activity/comments/` and `/recent-activity/all/` work when logged in. `get_page_text` returns only the first post.
- Long parallel agent runs hit usage limits; prefer small batches and do small projects inline.
- Session transcripts live in `~/.claude/projects/<path-slug>/*.jsonl`; human turns have `type: user` with string content; times are UTC (IST is +5:30).

## 8. Definition of done

1. Pass-3 report written; the final 5 + 5 role-model list approved by Alankrit.
2. Scheduled-job failures fixed (needs his re-auth) with a visible failure alert.
3. Draft-only agents built and tested on real examples, each output showing its voice-check result and sources; he has tried them.
4. Stale lines fixed; `python3 compiler/run.py` passes with no FAIL; global docs match `current_state.md`.
5. A short report to Alankrit: what exists, what was verified, what remains and what you need from him.

Start by reading section 2, running the compiler once to confirm the baseline, then asking Alankrit the questions in 4.5 that block your work.
