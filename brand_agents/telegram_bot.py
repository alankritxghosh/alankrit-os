"""Telegram front end for the daily routine. Draft-only, owner-only, runs on Alankrit's Mac.

The bot finds targets and voice-checks replies you write. It never posts, replies,
likes, follows, DMs or emails on X or anywhere else. It only messages the one
Telegram chat that was paired as the owner, and ignores everyone else.

    python -m brand_agents.telegram_bot check        # verify the token (prints the bot name only)
    python -m brand_agents.telegram_bot set-token    # store or rotate the token (hidden prompt)
    python -m brand_agents.telegram_bot pair         # send /start to the bot, then confirm your id
    python -m brand_agents.telegram_bot pair --save-id 123456789
    python -m brand_agents.telegram_bot run          # keep this running on the Mac
"""
from __future__ import annotations

import argparse
import getpass
import hashlib
import html
import json
import os
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path
from typing import Callable

from .common import check_voice, require_all_pass
from .daily import DEFAULT_ROOT, day_dir, excerpt, read_json, write_json
from .reply_scout import normalize_url

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = Path.home() / ".alankrit-os" / "telegram.json"
MESSAGE_LIMIT = 3800
PAGE_SIZE = 5
POST_EXCERPT_CHARS = 420

HELP = (
    "Alankrit OS (draft-only: I never post, like, follow or message anyone on X)\n\n"
    "/scout  find today's targets (about 3 minutes)\n"
    "/more  show the next 5 targets\n"
    "/ready  your replies that passed the voice check\n"
    "/status  counts for today\n"
    "/cancel  stop writing a reply\n\n"
    "Tap Write reply under a post, then send your reply as one message. "
    "I check it and send it back ready to copy. You post it yourself."
)


class TelegramError(RuntimeError):
    """Raised for any Telegram failure. Messages never include the bot token."""


def load_config(path: Path = CONFIG_PATH) -> dict:
    config = read_json(path, {})
    config = config if isinstance(config, dict) else {}
    env_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if env_token:
        config["token"] = env_token
    return config


def save_config(config: dict, path: Path = CONFIG_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(config, handle)
    os.chmod(path, 0o600)


class TelegramAPI:
    def __init__(self, token: str):
        self._token = token

    def call(self, method: str, params: dict | None = None, http_timeout: int = 35):
        url = f"https://api.telegram.org/bot{self._token}/{method}"
        request = urllib.request.Request(
            url, data=json.dumps(params or {}).encode("utf-8"), headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(request, timeout=http_timeout) as response:
                body = json.load(response)
        except urllib.error.HTTPError as exc:
            raise TelegramError(f"{method} failed: HTTP {exc.code}") from None
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            raise TelegramError(f"{method} failed: {type(exc).__name__}") from None
        if not body.get("ok"):
            raise TelegramError(f"{method} failed: {body.get('description', 'unknown error')}")
        return body["result"]


def url_tag(url: str) -> str:
    return hashlib.sha1(normalize_url(url).encode("utf-8")).hexdigest()[:6]


def clip(text: str, limit: int = MESSAGE_LIMIT) -> str:
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def subprocess_scouter(force: bool) -> tuple[bool, str]:
    command = [sys.executable, "-m", "brand_agents.daily", "scout"] + (["--force"] if force else [])
    try:
        done = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return False, "Scouting took longer than 15 minutes and was stopped."
    if done.returncode != 0:
        last = (done.stderr or done.stdout).strip().splitlines()
        return False, last[-1] if last else "Scouting failed."
    return True, "ok"


class Bot:
    def __init__(
        self,
        api,
        owner_id: int,
        root: Path = DEFAULT_ROOT,
        scouter: Callable[[bool], tuple[bool, str]] = subprocess_scouter,
        today: Callable[[], str] = lambda: date.today().isoformat(),
        run_async: bool = True,
    ):
        self.api = api
        self.owner_id = int(owner_id)
        self.root = root
        self.scouter = scouter
        self.today = today
        self.run_async = run_async
        self._lock = threading.Lock()
        self._scouting = False

    # ----- files -----
    @property
    def directory(self) -> Path:
        return day_dir(self.root, self.today())

    def candidates(self) -> list[dict]:
        return read_json(self.directory / "candidates.json", [])

    def visible(self) -> list[dict]:
        picks = read_json(self.directory / "picks.json", None)
        items = self.candidates()
        if picks:
            wanted = {normalize_url(url) for url in picks}
            items = [item for item in items if normalize_url(item["url"]) in wanted]
        return items

    def author_for(self, url: str) -> str:
        wanted = normalize_url(url)
        return next((c.get("author", "UNKNOWN") for c in self.candidates() if normalize_url(c["url"]) == wanted), "UNKNOWN")

    def state(self) -> dict:
        state = read_json(self.directory / "bot_state.json", {})
        state = state if isinstance(state, dict) else {}
        state.setdefault("pending", None)
        state.setdefault("shown", [])
        state.setdefault("skipped", [])
        return state

    def save_state(self, state: dict) -> None:
        write_json(self.directory / "bot_state.json", state)

    def angles(self) -> dict:
        data = read_json(self.directory / "angles.json", {})
        return data if isinstance(data, dict) else {}

    # ----- sending (only ever to the owner) -----
    def send(self, text: str, markup: dict | None = None, html_mode: bool = False) -> None:
        params: dict = {
            "chat_id": self.owner_id,
            "text": clip(text),
            "link_preview_options": {"is_disabled": True},
        }
        if markup:
            params["reply_markup"] = markup
        if html_mode:
            params["parse_mode"] = "HTML"
        self.api.call("sendMessage", params)

    def send_candidate(self, number: int, item: dict) -> None:
        text = f"{number}. @{item.get('author', 'UNKNOWN')} (score {item.get('score', '?')})\n{item['url']}\n\n{excerpt(item['post_text'], POST_EXCERPT_CHARS)}"
        tag = url_tag(item["url"])
        markup = {"inline_keyboard": [[
            {"text": "Write reply", "callback_data": f"w:{tag}"},
            {"text": "Skip", "callback_data": f"s:{tag}"},
        ]]}
        self.send(text, markup)

    def send_page(self) -> None:
        state = self.state()
        hidden = set(state["shown"]) | set(state["skipped"])
        items = self.visible()
        remaining = [item for item in items if normalize_url(item["url"]) not in hidden]
        if not items:
            self.send("No targets for today yet. Send /scout.")
            return
        if not remaining:
            self.send("That is every target for today. Send /ready to see your replies, or /scout force for a fresh search.")
            return
        for item in remaining[:PAGE_SIZE]:
            state["shown"].append(normalize_url(item["url"]))
            self.send_candidate(items.index(item) + 1, item)
        self.save_state(state)
        left = len(remaining) - PAGE_SIZE
        if left > 0:
            self.send(f"{left} more. Send /more.")

    # ----- updates -----
    def handle_update(self, update: dict) -> None:
        if "callback_query" in update:
            query = update["callback_query"]
            if query.get("from", {}).get("id") != self.owner_id:
                return
            self.handle_callback(query)
            return
        message = update.get("message")
        if not message:
            return
        if message.get("from", {}).get("id") != self.owner_id or message.get("chat", {}).get("id") != self.owner_id:
            return
        text = (message.get("text") or "").strip()
        if not text:
            return
        if text.startswith("/"):
            self.handle_command(text)
        else:
            self.handle_text(text)

    def handle_command(self, text: str) -> None:
        parts = text.split()
        command = parts[0].split("@")[0].lower()
        argument = parts[1].lower() if len(parts) > 1 else ""
        if command in ("/start", "/help"):
            self.send(HELP)
        elif command == "/scout":
            self.start_scout(force=argument == "force")
        elif command == "/more":
            self.send_page()
        elif command == "/ready":
            self.send_ready()
        elif command == "/status":
            self.send_status()
        elif command == "/cancel":
            state = self.state()
            state["pending"] = None
            self.save_state(state)
            self.send("Cancelled.")
        else:
            self.send(HELP)

    def handle_callback(self, query: dict) -> None:
        data = query.get("data", "")
        action, _, tag = data.partition(":")
        item = next((c for c in self.candidates() if url_tag(c["url"]) == tag), None)
        try:
            self.api.call("answerCallbackQuery", {"callback_query_id": query.get("id")})
        except TelegramError:
            pass
        if item is None or action not in ("w", "s"):
            self.send("That post is no longer in today's list. Send /more.")
            return
        url = normalize_url(item["url"])
        state = self.state()
        if action == "s":
            if url not in state["skipped"]:
                state["skipped"].append(url)
            self.save_state(state)
            self.remove_buttons(query)
            return
        previous = state.get("pending")
        state["pending"] = url
        self.save_state(state)
        note = ""
        if previous and previous != url:
            note = f"Switched. I dropped @{self.author_for(previous)}; tap Write reply on it again if you still want it.\n\n"
        self.send(f"{note}Send your reply to @{item.get('author', 'UNKNOWN')} as one message. /cancel to stop.\n{item['url']}")

    def remove_buttons(self, query: dict) -> None:
        message = query.get("message") or {}
        try:
            self.api.call("editMessageReplyMarkup", {
                "chat_id": self.owner_id,
                "message_id": message.get("message_id"),
                "reply_markup": {"inline_keyboard": []},
            })
        except TelegramError:
            pass

    def handle_text(self, text: str) -> None:
        state = self.state()
        pending = state.get("pending")
        if not pending:
            self.send("Tap Write reply under a post first, or send /help.")
            return
        checks = check_voice(text, "x")
        if not require_all_pass(checks):
            problems = "\n".join(f"- {c.name}: {c.detail}" for c in checks if not c.passed)
            self.send(f"Not ready. Fix and send it again, or /cancel.\n\n{problems}")
            return
        angles = self.angles()
        angles[pending] = text
        write_json(self.directory / "angles.json", angles)
        state["pending"] = None
        self.save_state(state)
        self.send(
            f"Ready for @{html.escape(self.author_for(pending))}. Copy it and post it yourself:\n\n"
            f"<code>{html.escape(text)}</code>\n\n{html.escape(pending)}",
            html_mode=True,
        )

    def send_ready(self) -> None:
        by_url = {normalize_url(c["url"]): c for c in self.candidates()}
        sent = 0
        for url, text in self.angles().items():
            if not isinstance(text, str) or not text.strip():
                continue
            if not require_all_pass(check_voice(text, "x")):
                continue
            author = by_url.get(normalize_url(url), {}).get("author", "UNKNOWN")
            self.send(f"@{html.escape(author)}\n\n<code>{html.escape(text)}</code>\n\n{html.escape(url)}", html_mode=True)
            sent += 1
        if not sent:
            self.send("No ready replies yet.")

    def send_status(self) -> None:
        state = self.state()
        written = [t for t in self.angles().values() if isinstance(t, str) and t.strip()]
        self.send(
            f"Targets today: {len(self.visible())}\nShown: {len(state['shown'])}\n"
            f"Skipped: {len(state['skipped'])}\nReplies written: {len(written)}"
        )

    # ----- scouting -----
    def start_scout(self, force: bool) -> None:
        existing = self.candidates()
        if existing and not force:
            state = self.state()
            self.send(
                f"Today's pool already has {len(existing)} posts ({len(state['shown'])} shown). "
                "Send /more for the rest, or /scout force to search again."
            )
            return
        with self._lock:
            if self._scouting:
                self.send("Already scouting. I will message you when it is done.")
                return
            self._scouting = True
        self.send("Scouting. About 3 minutes.")
        if self.run_async:
            threading.Thread(target=self._scout_job, args=(force,), daemon=True).start()
        else:
            self._scout_job(force)

    def _scout_job(self, force: bool) -> None:
        try:
            ok, detail = self.scouter(force and bool(self.candidates()))
            if not ok:
                self.send(f"Scouting failed: {detail}")
                return
            state = self.state()
            state["shown"], state["skipped"] = [], []
            self.save_state(state)
            self.send(f"Found {len(self.visible())} targets.")
            self.send_page()
        except TelegramError:
            pass
        finally:
            with self._lock:
                self._scouting = False


def run_forever(bot: Bot, should_stop: Callable[[], bool] = lambda: False) -> None:
    offset = None
    while not should_stop():
        params: dict = {"timeout": 30, "allowed_updates": ["message", "callback_query"]}
        if offset is not None:
            params["offset"] = offset
        try:
            updates = bot.api.call("getUpdates", params, http_timeout=40)
        except TelegramError as exc:
            print(f"warning: {exc}", file=sys.stderr)
            time.sleep(5)
            continue
        for update in updates:
            offset = update["update_id"] + 1
            try:
                bot.handle_update(update)
            except TelegramError as exc:
                print(f"warning: {exc}", file=sys.stderr)


def pair(api: TelegramAPI, save_id: int | None, wait_seconds: int = 120) -> int:
    if save_id is not None:
        config = load_config()
        config["owner_id"] = int(save_id)
        save_config(config)
        print(f"Saved owner id {save_id}. Only that chat can use the bot.")
        return 0
    print("Send /start to the bot from your own Telegram account now. Waiting...")
    deadline = time.time() + wait_seconds
    while time.time() < deadline:
        for update in api.call("getUpdates", {"timeout": 10}, http_timeout=20):
            sender = (update.get("message") or {}).get("from")
            if sender:
                name = " ".join(filter(None, [sender.get("first_name"), sender.get("last_name")]))
                print(f"First message came from: {name} (@{sender.get('username', 'no username')}), id {sender['id']}")
                print(f"If that is you, run: python -m brand_agents.telegram_bot pair --save-id {sender['id']}")
                return 0
    print("No message arrived. Try again.", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="step", required=True)
    sub.add_parser("check")
    sub.add_parser("set-token")
    p_pair = sub.add_parser("pair")
    p_pair.add_argument("--save-id", type=int, default=None)
    p_run = sub.add_parser("run")
    p_run.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args(argv)

    try:
        if args.step == "set-token":
            token = getpass.getpass("Bot token (hidden): ").strip()
            if not token:
                print("error: empty token", file=sys.stderr)
                return 2
            me = TelegramAPI(token).call("getMe")
            config = load_config()
            config["token"] = token
            save_config(config)
            print(f"Stored token for @{me.get('username')}.")
            return 0
        config = load_config()
        if not config.get("token"):
            print("error: no token. Run set-token first.", file=sys.stderr)
            return 2
        api = TelegramAPI(config["token"])
        if args.step == "check":
            me = api.call("getMe")
            print(f"Bot @{me.get('username')} is reachable. Owner paired: {'yes' if config.get('owner_id') else 'no'}")
            return 0
        if args.step == "pair":
            return pair(api, args.save_id)
        if not config.get("owner_id"):
            print("error: no owner paired. Run pair first.", file=sys.stderr)
            return 2
        bot = Bot(api, config["owner_id"], root=args.root)
        print("Bot running. Ctrl-C to stop.")
        try:
            run_forever(bot)
        except KeyboardInterrupt:
            print("Stopped.")
        return 0
    except TelegramError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
