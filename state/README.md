# state/

Working data for the daily brand routine, kept in this **private** repo so a Claude Code session
on the web (which cannot see the Mac) and the Mac read and write the same files.

Use it with `export BRAND_DATA_DIR="$PWD/state"` (the `/daily` command and `scripts/morning.sh` do this).

- `daily/<date>/` candidates, review sheet, your replies (`angles.json`), shortlist
- `decisions.jsonl` what Alankrit did with every draft (use, edit, skip)
- `x-seen-urls.json` posts already surfaced, so they never repeat

Never put logins, cookies or tokens here. Those stay in `~/.alankrit-os/`, outside the repo.
