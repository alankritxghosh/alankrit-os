# Handoff to the local session (Mac, Claude Code with the Chrome extension)

Written 2026-10-05 by the cloud session on branch `claude/eager-dirac-yf3vag`. Read `CLAUDE.md` and `BRAND_AGENT_POLICY.md` first. The policy wins over this file.

Setup, every session:

```bash
cd "/Users/campusfund15/Personal/Alankrit OS"
git fetch origin && git checkout claude/eager-dirac-yf3vag && git pull
export BRAND_DATA_DIR="$PWD/state"
python3 -m brand_agents.doctor      # should say SCOUT if the X login and Playwright exist
```

The Chrome extension must be connected. The cloud session had no browser, and linkedin.com, substack.com, nber.org and hbs.edu were blocked there. Everything you can read in a logged-in browser was out of reach for it.

## Hard rules that apply to every task below

- Draft only. Never post, comment, reply, like, repost, follow, connect, DM, email, schedule or publish. Alankrit posts by hand. Read-only browsing is fine.
- Open and read every post you use. Never guess a URL or its text.
- Voice, for every draft: no em or en dashes, no hashtags, no emoji, no links or @mentions in replies, no "it is not X, it is Y" reframes, no outreach cliches, X under 280 characters, LinkedIn connection notes under 180. Titles stay simple (his standing rule).
- Private, never in a draft unless he says so for that item: Campus Fund, the Icarus thesis, personal facts beyond age, Bangalore and B.Com. He has approved, for his own Substack pieces, mention of his art, design, poetry and photos.
- First drafts are Claude's. Edits happen only when he says "revise" or gives a direct instruction. If he says a draft is wrong in kind ("AI generic"), stop tuning and ask for his raw words.
- Report honestly: say what failed or is unverified. No "perfect" claims without numbers.
- Commit and push `state/` and the outputs below to this private repo when he says the session is done. Code changes only when he asks. End commits with the attribution line the harness gives you.

## What the cloud session already did (all pushed)

- Read the repo, ran `doctor` (REMOTE mode, empty state), confirmed no decisions logged yet.
- Substack research and the second Substack piece. Files in `state/substack/`:
  - `2026-10-05-research-brief.md`, `2026-10-05-generalist-with-agents-skeleton.md`, `2026-10-05-piece2-plan-and-spinoffs.md` (research and planning, earlier versions).
  - `2026-10-05-piece2-draft-v2-humanised.md` (working draft) and `2026-10-05-piece2-clean-text.md` (the text as posted, with the URL).
  - `2026-10-05-piece2-spinoff-posts.md` (6 X drafts and 2 LinkedIn drafts).
- The piece is live: https://alankritghosh.substack.com/p/why-does-a-generalist-with-agents . Title: "Why does a generalist with agents sometimes beat a specialist without them?" He posted it himself on 2026-10-05, with a Louis Pasteur epigraph ("Chance favors only the prepared mind", 1854). The wording of the quote is NOT verified.
- His earlier piece, "Jack of all trades or just restless?" (2026-10-01), was read from text he pasted. Not fetched.
- Study figures in the piece were checked on 2026-10-05: BCG (758 consultants, 12.2%, 25.1%, over 40%, 19 percentage points) from the paper PDF; P&G (776 professionals, comparable to teams) from the NBER paper; IG Group (78 people, 12/26/40, 3.96/3.92/3.42) from HBS's write-up only. The IG Group working paper ("The GenAI Wall Effect", HBS WP 26-011) was not opened. Source fetching worked through the Parallel Search `web_fetch` tool when normal fetch was blocked; it hit a free-tier rate limit.

## Task 1: the X post for the Substack article

Goal: one X post he can publish today for the article above.

- Open his X profile and find his earlier post(s) about his Substack. Read them, then match the pattern and avoid repeating the same opening. Note what got engagement, with the date counts were read.
- The cloud session's candidate (draft, not verified against his profile):

  ```
  new on substack: why does a generalist with agents sometimes beat a specialist without them?

  in the IG Group study marketers nearly matched the analysts with AI, developers ended up about 13% behind
  the distance from the task decides how much AI helped
  ```

  255 characters. Plan: Substack link in his first reply, not in the post. His call.
- Alternatives are in `state/substack/2026-10-05-piece2-spinoff-posts.md` (X-1 to X-6). Present one primary and at most one variant. Run the voice checks and show the result.
- Done when: he has a single post with a link to the reply and a one-line reason.

## Task 2: 10 X accounts, and their posts to comment on

Interpretation to confirm with him in one question before starting: he wants 10 accounts whose recent posts he can reply to (post-level targets), not only the policy's role-model study.

- Two inputs already exist: `brand/scouting/2026-10-04-role-model-report.md` and `...-pass-2.md` (10 proposed role models, 5 X and 5 LinkedIn, pending his approval, large-account heavy, with swaps proposed at the bottom). Use them as a starting pool, not as the answer.
- Target quality is in `CLAUDE.md`: first-person build or problem posts with a specific detail, sharp questions, real technical insight, in his lane (coding agents, MCP, context and memory, vibe coding with substance, building in public). Skip launches, ads, hype, growth funnels, job content, crypto, news summaries, engagement bait, politics. Prefer posts a reply can add one concrete thing to. Larger accounts are worth it when the post invites a reply.
- Mac workflow: `python3 -m brand_agents.daily scout` (about 3 minutes, run in the background). Then `triage`, then write replies into `angles.json` and run `python3 -m brand_agents.daily replies` until "Fix before posting" is clean. If the scout cannot run, read X search in the browser and use `daily ingest`.
- Output per account: handle, profile URL (opened), follower count with the date read, 1 or 2 post URLs read, a one-line gist, and a draft reply under 280 characters. Do not state anything about his projects, numbers or opinions as fact in a reply.
- Log his decisions with `python3 -m brand_agents.decisions log ...` as he decides. Only text he types himself counts as voice examples.

## Task 3: 10 LinkedIn accounts to comment on

- Same rules as Task 2, in the browser, read-only. His gate is at least 10 LinkedIn comments a week. The role-model report's LinkedIn five are GTM and personal-brand coaches from an unreliable source, so prefer builders and AI-agent practitioners in his lane.
- Comments are plain and add one concrete thing. No praise opener, no summary of the post, no links or @mentions, no cliches. Under about 600 characters unless he says otherwise. Do not connect or follow.
- Output per account: name, profile URL (opened), follower count with date, the post URL read, a one-line gist, a draft comment.
- He is at about 840 LinkedIn followers (2026-10-04 count). Report counts only with their date.

## Task 4: all context on Alankrit into the Obsidian vault under Alankrit OS

- I could not see an Obsidian vault in this repo. The policy mentions a separate "Personal Brand vault". Ask him once where the vault lives (a folder inside the repo or one on the Mac). Do not create a second vault if one exists.
- Sources to pull from: `ALANKRIT_GLOBAL_CONTEXT.md`, `compiler/current_state.md`, `memory/*.jsonl` (beliefs, decisions, episodes, facts, failures, lessons, open loops, projects, relationships, voice examples), the numbered `0*`/`1*` files, `context-extraction/`, `BRAND_AGENT_POLICY.md`, the Substack pieces and `state/substack/*`.
- Build an evolving knowledge graph: one note per person, project (Icarus, Alankrit OS, the brand), decision, belief, lesson, open loop and published piece, linked with `[[wikilinks]]`, plus index notes (projects, timeline, open loops, voice, studies cited).
- Rules: keep the vault private. Mark each fact EXPLICIT or inferred and carry its source and date. Keep Campus Fund and the Icarus thesis in notes flagged `private`, and never copy them into drafts. No logins, cookies or tokens. Do not run `compiler/run.py` unless he asks, because it rewrites many tracked files.
- New facts from 2026-10-05 to add: the second Substack piece is live; Icarus went from idea to Product Hunt launch in 60 days; moving Icarus retrieval from keyword search to semantic retrieval took one weekend with a 30-hour timeout bug fixed by him and his agents; he describes himself as a curious builder with a finance degree who loves art, design, poetry and photos; and his rule that titles stay simple.
- Done when: the vault opens, the index links resolve, and every note shows its source.

## Task 5: October content calendar (.xlsx, saved under Alankrit OS)

- Use the `xlsx` skill. Save it in the repo root or a `calendar/` folder, for example `calendar/october-2026-content-calendar.xlsx`, and report the path.
- Cover X, LinkedIn and Substack for 2026-10-05 to 2026-10-31 (the month so far is already partly done).
- His input gates from policy: X replies 20 to 25 a day in October, X posts at least 5 a week, LinkedIn at least 2 posts and 10 comments a week, Substack first post by 2026-10-31 and then 1 to 2 a month. The first Substack post is already out (2026-10-01), and the second on 2026-10-05, so October's Substack target is met. Plan one more only if he wants it.
- Checkpoint to keep in view: by 2026-10-31, 140 on X, 1,050 on LinkedIn, about 10 on Substack (policy table). Counts were 31 / 840 / 0 on 2026-10-04.
- Sheets: a month grid (date, platform, format, topic, source or draft file, status), a weekly gates tracker, a reply and comment quota sheet, and a notes sheet listing assumptions. Posts come from `state/substack/*` and his raw ideas. Mark each cell Draft or Planned, never Posted, since he posts by hand.
- Include the spin-off posts from the second article (6 X, 2 LinkedIn) so they have dates. Space them out and avoid posting all six X drafts back to back.
- Done when: the file opens, formulas compute, and the dates cover every day to 2026-10-31.

## Open items for Alankrit (ask once, early)

1. Confirm the Pasteur quote wording, or check it yourself first.
2. Where the Obsidian vault lives.
3. Whether Task 2 means post-level targets for 10 accounts, as assumed above.
4. Whether to approve or swap the 10 proposed role-model accounts.
5. Whether to plan a third Substack piece in October, and add the URL for the second piece if it differs.

## Known issues to flag, not fix

- `BRAND_AGENT_POLICY.md` says "Version 3" at the top while its history lists changes to v5. He alone changes that file; mention it and move on.
- `state/` holds no logged decisions yet. The scout, triage and drafting loop has never run end to end on real data in this repo.
- Nothing in this handoff has been posted. Every post, comment and reply is a draft for him.
