# X Playwright Provider

One-day scope: X only. LinkedIn scouting is deliberately out of scope for now.

This provider uses a logged-in Playwright browser to find possible X reply targets, then writes JSON compatible with `brand_agents.reply_scout`.

It is read-only:

- no posting
- no replying
- no liking
- no reposting
- no following
- no DMs

## Setup

Install Playwright in the runtime:

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
```

Log in once:

```bash
python3 -m brand_agents.providers.x_playwright.login
```

The session is saved to:

```text
~/.alankrit-os/x-storage-state.json
```

Do not commit that file.

## Find X targets

```bash
python3 -m brand_agents.providers.x_playwright.find_posts \
  --limit 10 \
  --out /tmp/x-targets.json
```

Then draft replies:

```bash
python3 -m brand_agents.reply_scout \
  --targets /tmp/x-targets.json
```

## Phone/Telgram path later

The Telegram command should call this provider first, then pass its output into `reply_scout`.

Example command:

```text
/find_replies x 10
```

Equivalent mobile runner JSON:

```json
{
  "command": "find_x_replies",
  "limit": 10
}
```

This command needs a runtime with Playwright installed and `~/.alankrit-os/x-storage-state.json` already created by the manual login step.
