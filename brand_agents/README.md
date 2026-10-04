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

## X discovery provider

For the one-day automation path, use X only:

```bash
python3 -m brand_agents.providers.x_playwright.login
python3 -m brand_agents.providers.x_playwright.find_posts --limit 10 --out /tmp/x-targets.json
python3 -m brand_agents.reply_scout --targets /tmp/x-targets.json
```

`find_posts` remembers every URL it has surfaced in `~/.alankrit-os/x-seen-urls.json`, so repeat runs only show new posts. Pass `--no-dedupe` to ignore that file, or `--seen-file` to use another. A run searches 9 queries at 8 scrolls each and takes about 2 minutes.

LinkedIn scouting is intentionally out of scope for this first pass.
