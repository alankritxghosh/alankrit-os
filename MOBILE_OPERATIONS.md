# Mobile Operations

Goal: Alankrit can run the draft-only brand system from a phone, with no laptop open.

Runtime: the private GitHub repo runs GitHub Actions. Outputs come back as an issue comment and as a workflow artifact. Nothing is posted, scheduled, sent, liked, followed, connected, DMed or emailed.

## Phone path A: issue form

1. Open the private `alankrit-os` repo in GitHub Mobile or mobile web.
2. Create a new issue.
3. Choose the `Brand command` template.
4. Pick one command:
   - `Draft from raw idea`
   - `Reply target scout`
   - `Weekly follower report`
5. Fill the relevant field.
6. Submit the issue.
7. GitHub Actions comments the draft-only output back on the issue.

For the one-day X-only automation, the cloud runtime can later use:

```json
{
  "command": "find_x_replies",
  "limit": 10
}
```

That requires Playwright and a saved X login state in the runtime. LinkedIn scouting is intentionally out of scope for this first pass.

## Phone path B: manual workflow

1. Open Actions in the private repo.
2. Run `Brand Agents Mobile`.
3. Paste one JSON command from `brand_agents/examples/mobile_*.json`.
4. Read the run summary or download the `brand-agent-output` artifact.

## Command JSON

Draft:

```json
{
  "command": "draft",
  "platform": "x",
  "raw_idea": "your raw idea here",
  "facts": [
    {
      "claim": "a sourced claim",
      "source": "where it came from"
    }
  ]
}
```

Reply scout:

```json
{
  "command": "reply_scout",
  "targets": [
    {
      "url": "https://x.com/...",
      "opened": true,
      "checked_at": "2026-10-04",
      "author": "handle",
      "post_text": "copied text",
      "why": "why this target fits",
      "angle": "optional draft angle"
    }
  ]
}
```

Weekly report:

```json
{
  "command": "weekly_report",
  "counts": {
    "checked_at": "2026-10-04",
    "x": 31,
    "linkedin": 840,
    "substack": 0
  }
}
```

## Boundaries

- The system is draft-only.
- Reply targets must still be opened in a logged-in browser before use.
- Campus Fund remains private unless Alankrit approves a specific item.
- A delivered draft is final until Alankrit says `revise` or gives a direct revision instruction.
