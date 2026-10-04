# Draft-only agent suite

These tools turn Alankrit OS into supervised brand operations. They never post, schedule, like, follow, connect, DM, email or send anything.

## 1. Draft Agent

Input: Alankrit's raw idea as text, plus optional sourced facts.

```bash
python3 -m brand_agents.draft_agent \
  --idea brand_agents/examples/raw_idea.txt \
  --facts brand_agents/examples/facts.json \
  --platform x
```

Output: a local markdown file in `brand/agent_outputs/drafts/` with:

- one or two draft variants
- ALANKRIT-only voice examples used
- sources for every supplied fact
- voice-check results

## 2. Reply Target Scout

Input: targets exported by a logged-in browser operator. Every item must be opened and marked `opened: true`.

```bash
python3 -m brand_agents.reply_scout \
  --targets brand_agents/examples/reply_targets.json
```

Output: local draft replies with clickable URLs and checks. The scout does not browse by itself in this environment.

Every post gets `NEEDS HUMAN ANGLE`. The scout writes no replies of its own: keyword-matched templates cannot tell what a post means, and they produced replies that contradicted the author. It finds and scores targets, then formats and voice-checks the replies you write. Put your reply for each target worth answering in an angles file, a JSON object mapping the post URL to your text, then rerun:

```bash
python3 -m brand_agents.reply_scout \
  --targets /tmp/x-targets.json \
  --angles ~/my-angles.json
```

```json
{
  "https://x.com/someone/status/123": "Your reply here.\nOne thought per line."
}
```

- Query strings and trailing slashes on URLs are ignored. Blank values are skipped.
- Your text is used as written and is never truncated. It goes through the same voice checks as any draft, so a `FAIL` line means rewrite it (over 280 characters, a long dash, a "not X, it is Y" reframe and so on).
- A URL that matches no target prints a warning on stderr.
- Nothing is posted. You copy the reply and post it yourself.

## 3. Weekly Report

Input: manually checked follower counts.

```bash
python3 -m brand_agents.weekly_report \
  --counts brand_agents/examples/counts.json
```

Output: a weekly report against the approved milestone table.

## Rules

- A delivered draft is final until Alankrit says `revise` or gives a direct revision instruction.
- Facts must be supplied with sources or omitted.
- Campus Fund stays private unless Alankrit approves a specific item.
- Icarus thesis remains `UNKNOWN`.

## Prompt contracts

The `prompts/` folder contains the same rules as reusable contracts for Claude/Codex agents:

- `prompts/draft_agent.md`
- `prompts/reply_target_scout.md`
- `prompts/weekly_report.md`

## Phone runtime

See `MOBILE_OPERATIONS.md` for the GitHub Mobile workflow. The same local runner is available as:

```bash
python3 -m brand_agents.mobile_runner --command-file brand_agents/examples/mobile_draft.json
```

## Daily routine

One command per step. Files live in `~/.alankrit-os/daily/<date>/`, outside the repo, because they hold your own reply text.

```bash
python3 -m brand_agents.daily scout                  # about 3 minutes: finds 25 candidates, writes review.md + angles.json
python3 -m brand_agents.daily triage --keep 1,4,7    # keep only the numbers you want from review.md
# write your reply for each kept URL in angles.json
python3 -m brand_agents.daily replies                # voice-checks angles.json, writes replies.md
```

- `replies.md` has a **Ready** section with copy-ready text and a **Fix before posting** section listing each failed check. `replies` exits 1 when anything needs fixing.
- `scout` refuses to overwrite an existing day. `--force` refreshes the candidates and keeps every reply you already wrote. `--date` uses another folder.
- Nothing is posted, liked, followed or sent. You copy the text and post it by hand.

## Telegram bot

The same routine from your phone. It runs on the Mac (the X login lives there), so the Mac has to be awake while it runs. It is owner-only and draft-only: it never posts, likes, follows or messages anyone on X, and it ignores every Telegram account except the one you paired.

One-time setup:

```bash
python3 -m brand_agents.telegram_bot set-token     # hidden prompt; stores the BotFather token in ~/.alankrit-os/telegram.json (mode 600)
# send /start to your bot from your own Telegram account
python3 -m brand_agents.telegram_bot pair          # prints who messaged first
python3 -m brand_agents.telegram_bot pair --save-id <id>   # only after you confirm that id is you
python3 -m brand_agents.telegram_bot check         # confirms the bot is reachable
```

Daily use:

```bash
python3 -m brand_agents.telegram_bot run           # keep this running
```

| Command | What it does |
|---|---|
| `/scout` | finds today's targets (about 3 minutes); `/scout force` searches again |
| `/more` | drafts and shows the next 5 targets. Each card has the post, its link and a draft reply, with **Use draft**, **Edit**, **Redraft** and **Skip** buttons |
| Use draft | saves the draft as ready and sends it back as tap-to-copy text |
| Edit | shows the draft for reference; your next message replaces it and is voice-checked (the bot lists what failed) |
| Redraft | asks for a different angle and sends a new card |
| `/ready` | your replies that passed the voice check |
| `/status` / `/cancel` | counts for today / stop writing a reply |

- Drafts are written by headless Claude Code on this Mac (`claude -p`, so run `claude auth login` once). It has every tool, MCP server and skill turned off, treats the post as untrusted data, and uses only your own typed voice examples. A draft that fails the voice check, contains a link, an @mention or a number that is not in the post is retried up to 3 times and then dropped, never shown. If it cannot write a specific reply without inventing facts about you it answers SKIP and the card offers Edit. Set `BRAND_DRAFT_MODEL` to change the model (default `sonnet`).
- A draft is never saved as ready until you tap Use draft or send your own text.
- One reply is pending at a time. Tapping Edit on another post says which one it dropped, and a saved reply says which post it belongs to.
- If you ran `triage` for the day, the bot shows only that shortlist.
- Replies are saved to the same `angles.json` the `daily replies` command reads.
- The token never goes in the repo. `TELEGRAM_BOT_TOKEN` in the environment overrides the file. To rotate it, revoke it in BotFather, then run `set-token` again.

## Decision log

Every card shown and every tap (Use draft, Edit, Redraft, Skip) is appended to `~/.alankrit-os/decisions.jsonl`, outside the repo and mode 600, because it holds post text and your own replies. Each line records the post, its author, score and signals, Claude's draft, and what you did. Logging never blocks the bot: if the file cannot be written the bot carries on.

```bash
python3 -m brand_agents.decisions summary --days 14   # use / edit / skip rates, how much of each draft survived your edits, most-skipped authors
```

Two fields stay apart on purpose, so the log can feed drafting later without breaking the voice policy (first drafts come from text you typed, not agent text you approved):

| Field | Meaning |
|---|---|
| `draft` | what Claude wrote |
| `final_source` | `draft_as_is` (you approved agent text) or `typed_by_alankrit` (your own words) |

An `edit_saved` event also stores `similarity`, from 0 to 1, for how much of the draft survived. Only `typed_by_alankrit` text should ever be used as a voice example.

## X discovery provider

For the one-day automation path, use X only:

```bash
python3 -m brand_agents.providers.x_playwright.login
python3 -m brand_agents.providers.x_playwright.find_posts --limit 10 --out /tmp/x-targets.json
python3 -m brand_agents.reply_scout --targets /tmp/x-targets.json
```

`find_posts` remembers every URL it has surfaced in `~/.alankrit-os/x-seen-urls.json`, so repeat runs only show new posts. Pass `--no-dedupe` to ignore that file, or `--seen-file` to use another. A run searches 9 queries at 8 scrolls each and takes about 2 minutes.

LinkedIn scouting is intentionally out of scope for this first pass.
