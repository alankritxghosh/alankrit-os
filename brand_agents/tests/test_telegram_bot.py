import json
import os
import re
import stat
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

from brand_agents import daily, telegram_bot as tb

OWNER = 111
STRANGER = 222
TOKEN = "123456:SECRET-TOKEN-VALUE"


def cand(n: int) -> dict:
    return {"url": f"https://x.com/user{n}/status/{n}", "author": f"user{n}", "post_text": f"I built agent workflow number {n} with Claude Code", "score": 20 - n, "opened": True}


class FakeAPI:
    def __init__(self):
        self.calls = []

    def call(self, method, params=None, http_timeout=35):
        self.calls.append((method, params or {}))
        return {}

    def sent(self):
        return [p for m, p in self.calls if m == "sendMessage"]

    def texts(self):
        return [p["text"] for p in self.sent()]


def msg(text, sender=OWNER):
    return {"update_id": 1, "message": {"message_id": 5, "text": text, "from": {"id": sender}, "chat": {"id": sender}}}


def press(data, sender=OWNER):
    return {"update_id": 2, "callback_query": {"id": "q1", "data": data, "from": {"id": sender}, "message": {"message_id": 9, "chat": {"id": sender}}}}


class BotTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.api = FakeAPI()
        self.scout_calls = []
        self.pool = 8
        self.bot = tb.Bot(self.api, OWNER, root=self.root, scouter=self.fake_scouter, today=lambda: "2026-10-04", run_async=False)

    def tearDown(self):
        self._tmp.cleanup()

    def fake_scouter(self, force):
        self.scout_calls.append(force)
        daily.scout(self.bot.directory, lambda: [cand(i) for i in range(1, self.pool + 1)], force=True)
        return True, "ok"

    def seed(self, count=8):
        daily.scout(self.bot.directory, lambda: [cand(i) for i in range(1, count + 1)])

    def tag(self, n):
        return tb.url_tag(cand(n)["url"])

    # ----- owner only -----
    def test_strangers_get_no_response_at_all(self):
        for update in [msg("/start", STRANGER), msg("/scout", STRANGER), press(f"w:{self.tag(1)}", STRANGER), msg("hello", STRANGER)]:
            self.bot.handle_update(update)
        self.assertEqual(self.api.calls, [])

    def test_owner_in_a_group_chat_is_ignored(self):
        update = msg("/start")
        update["message"]["chat"]["id"] = -999
        self.bot.handle_update(update)
        self.assertEqual(self.api.calls, [])

    def test_every_message_goes_only_to_the_owner(self):
        self.seed()
        for update in [msg("/start"), msg("/more"), press(f"w:{self.tag(1)}"), msg("One clear thought."), msg("/ready"), msg("/status")]:
            self.bot.handle_update(update)
        self.assertTrue(self.api.sent())
        self.assertEqual({p["chat_id"] for p in self.api.sent()}, {OWNER})

    # ----- flow -----
    def test_start_shows_help_and_states_draft_only(self):
        self.bot.handle_update(msg("/start"))
        self.assertIn("never post", self.api.texts()[0])

    def test_scout_then_five_per_page_with_buttons(self):
        self.bot.handle_update(msg("/scout"))
        self.assertEqual(self.scout_calls, [False])
        cards = [p for p in self.api.sent() if p.get("reply_markup")]
        self.assertEqual(len(cards), 5)
        buttons = cards[0]["reply_markup"]["inline_keyboard"][0]
        self.assertEqual([b["text"] for b in buttons], ["Write reply", "Skip"])
        self.assertTrue(buttons[0]["callback_data"].startswith("w:"))
        self.assertIn("3 more", " ".join(self.api.texts()))
        self.api.calls.clear()
        self.bot.handle_update(msg("/more"))
        self.assertEqual(len([p for p in self.api.sent() if p.get("reply_markup")]), 3)
        self.api.calls.clear()
        self.bot.handle_update(msg("/more"))
        self.assertIn("every target", self.api.texts()[0])

    def test_scout_does_not_repeat_when_pool_exists(self):
        self.seed()
        self.bot.handle_update(msg("/scout"))
        self.assertEqual(self.scout_calls, [])
        self.assertIn("/scout force", self.api.texts()[0])
        self.bot.handle_update(msg("/scout force"))
        self.assertEqual(self.scout_calls, [True])

    def test_scout_failure_is_reported(self):
        self.bot.scouter = lambda force: (False, "missing X login state")
        self.bot.handle_update(msg("/scout"))
        self.assertIn("Scouting failed: missing X login state", self.api.texts())

    def test_skip_hides_post_and_removes_buttons(self):
        self.seed(7)
        self.bot.handle_update(press(f"s:{self.tag(1)}"))
        self.assertIn("editMessageReplyMarkup", [m for m, _ in self.api.calls])
        self.api.calls.clear()
        self.bot.handle_update(msg("/more"))
        shown = " ".join(self.api.texts())
        self.assertNotIn("user1/status/1\n", shown)
        self.assertIn("user2/status/2", shown)

    def test_write_reply_flow_saves_and_returns_copyable_text(self):
        self.seed()
        self.bot.handle_update(press(f"w:{self.tag(3)}"))
        self.assertIn("Send your reply to @user3", self.api.texts()[-1])
        self.bot.handle_update(msg("Compaction is where agents lose decisions.\nA record of rejections helps."))
        last = self.api.sent()[-1]
        self.assertEqual(last["parse_mode"], "HTML")
        self.assertIn("<code>Compaction is where agents lose decisions.\nA record of rejections helps.</code>", last["text"])
        self.assertIn("https://x.com/user3/status/3", last["text"])
        angles = json.loads((self.bot.directory / "angles.json").read_text())
        self.assertEqual(angles["https://x.com/user3/status/3"], "Compaction is where agents lose decisions.\nA record of rejections helps.")
        self.assertIsNone(self.bot.state()["pending"])

    def test_tapping_a_second_post_says_what_it_replaced(self):
        self.seed()
        self.bot.handle_update(press(f"w:{self.tag(1)}"))
        self.assertNotIn("Switched", self.api.texts()[-1])
        self.bot.handle_update(press(f"w:{self.tag(2)}"))
        last = self.api.texts()[-1]
        self.assertIn("Switched. I dropped @user1", last)
        self.assertIn("Send your reply to @user2", last)
        self.assertEqual(self.bot.state()["pending"], "https://x.com/user2/status/2")

    def test_tapping_the_same_post_twice_is_not_a_switch(self):
        self.seed()
        self.bot.handle_update(press(f"w:{self.tag(1)}"))
        self.bot.handle_update(press(f"w:{self.tag(1)}"))
        self.assertNotIn("Switched", self.api.texts()[-1])

    def test_saved_reply_names_the_post_it_belongs_to(self):
        self.seed()
        self.bot.handle_update(press(f"w:{self.tag(1)}"))
        self.bot.handle_update(press(f"w:{self.tag(3)}"))
        self.bot.handle_update(msg("One clear thought."))
        last = self.api.texts()[-1]
        self.assertIn("Ready for @user3.", last)
        self.assertIn("https://x.com/user3/status/3", last)
        self.assertEqual(self.bot.angles().get("https://x.com/user1/status/1", ""), "")

    def test_reply_text_is_html_escaped(self):
        self.seed()
        self.bot.handle_update(press(f"w:{self.tag(1)}"))
        self.bot.handle_update(msg("Use <b>hooks</b> & skills."))
        self.assertIn("&lt;b&gt;hooks&lt;/b&gt; &amp; skills.", self.api.sent()[-1]["text"])

    def test_failing_reply_lists_problems_and_stays_pending(self):
        self.seed()
        self.bot.handle_update(press(f"w:{self.tag(2)}"))
        self.bot.handle_update(msg("It's not the model, it's the context."))
        self.assertIn("Not ready", self.api.texts()[-1])
        self.assertIn("reframe", self.api.texts()[-1])
        self.assertEqual(self.bot.state()["pending"], "https://x.com/user2/status/2")
        self.assertEqual(self.bot.angles().get("https://x.com/user2/status/2", ""), "")
        self.bot.handle_update(msg("Context is the model's working memory."))
        self.assertIn("Ready for @user2.", self.api.texts()[-1])

    def test_text_without_a_pending_post_is_not_saved(self):
        self.seed()
        self.bot.handle_update(msg("random thought"))
        self.assertIn("Tap Write reply", self.api.texts()[-1])
        self.assertEqual(set(self.bot.angles().values()), {""})

    def test_cancel_clears_pending(self):
        self.seed()
        self.bot.handle_update(press(f"w:{self.tag(1)}"))
        self.bot.handle_update(msg("/cancel"))
        self.assertIsNone(self.bot.state()["pending"])

    def test_stale_or_forged_buttons_are_refused(self):
        self.seed()
        for data in ["w:deadbe", "x:" + self.tag(1), "garbage"]:
            self.api.calls.clear()
            self.bot.handle_update(press(data))
            self.assertIn("no longer in today's list", self.api.texts()[-1])
        self.assertIsNone(self.bot.state()["pending"])

    def test_ready_lists_only_replies_that_pass(self):
        self.seed()
        self.bot.handle_update(press(f"w:{self.tag(1)}"))
        self.bot.handle_update(msg("One clear thought."))
        angles = self.bot.angles()
        angles["https://x.com/user2/status/2"] = "Bad — dash."
        daily.write_json(self.bot.directory / "angles.json", angles)
        self.api.calls.clear()
        self.bot.handle_update(msg("/ready"))
        self.assertEqual(len(self.api.sent()), 1)
        self.assertIn("One clear thought.", self.api.texts()[0])
        self.assertNotIn("dash", self.api.texts()[0])

    def test_ready_with_nothing_written(self):
        self.seed()
        self.bot.handle_update(msg("/ready"))
        self.assertIn("No ready replies", self.api.texts()[-1])

    def test_status_counts(self):
        self.seed()
        self.bot.handle_update(msg("/more"))
        self.api.calls.clear()
        self.bot.handle_update(msg("/status"))
        text = self.api.texts()[0]
        self.assertIn("Targets today: 8", text)
        self.assertIn("Shown: 5", text)

    def test_triage_picks_limit_what_the_bot_shows(self):
        self.seed()
        daily.triage(self.bot.directory, [2, 4])
        self.bot.handle_update(msg("/more"))
        shown = " ".join(self.api.texts())
        self.assertIn("user2/status/2", shown)
        self.assertIn("user4/status/4", shown)
        self.assertNotIn("user1/status/1", shown)

    def test_long_messages_are_clipped(self):
        self.bot.send("x" * 10000)
        self.assertLessEqual(len(self.api.texts()[0]), tb.MESSAGE_LIMIT)

    # ----- safety -----
    def test_bot_only_uses_allowed_telegram_methods(self):
        source = Path(tb.__file__).read_text(encoding="utf-8")
        used = set(re.findall(r'\.call\("(\w+)"', source))
        self.assertLessEqual(used, {"getUpdates", "sendMessage", "answerCallbackQuery", "editMessageReplyMarkup", "getMe"})

    def test_nothing_in_the_bot_can_post_to_x(self):
        source = Path(tb.__file__).read_text(encoding="utf-8").lower()
        for forbidden in ["x.com/compose", "tweet", "retweet", ".click(", "playwright", "like_button"]:
            self.assertNotIn(forbidden, source)

    def test_errors_never_contain_the_token(self):
        api = tb.TelegramAPI(TOKEN)
        for failure in [
            urllib.error.URLError(f"https://api.telegram.org/bot{TOKEN}/getMe unreachable"),
            urllib.error.HTTPError(f"https://api.telegram.org/bot{TOKEN}/getMe", 401, "Unauthorized", {}, None),
            TimeoutError(f"timeout on {TOKEN}"),
        ]:
            with mock.patch("urllib.request.urlopen", side_effect=failure):
                with self.assertRaises(tb.TelegramError) as ctx:
                    api.call("getMe")
            self.assertNotIn(TOKEN, str(ctx.exception))
            self.assertNotIn("SECRET", str(ctx.exception))
            self.assertIsNone(ctx.exception.__cause__)

    def test_telegram_rejection_is_an_error_without_token(self):
        class Resp:
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def read(self): return json.dumps({"ok": False, "description": "Unauthorized"}).encode()
        with mock.patch("urllib.request.urlopen", return_value=Resp()):
            with self.assertRaises(tb.TelegramError) as ctx:
                tb.TelegramAPI(TOKEN).call("getMe")
        self.assertIn("Unauthorized", str(ctx.exception))
        self.assertNotIn(TOKEN, str(ctx.exception))

    def test_config_file_is_private_and_env_overrides_token(self):
        path = self.root / "cfg" / "telegram.json"
        tb.save_config({"token": "from-file", "owner_id": 7}, path)
        self.assertEqual(stat.S_IMODE(os.stat(path).st_mode), 0o600)
        self.assertEqual(tb.load_config(path), {"token": "from-file", "owner_id": 7})
        with mock.patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "from-env"}):
            self.assertEqual(tb.load_config(path)["token"], "from-env")
            self.assertEqual(tb.load_config(path)["owner_id"], 7)

    def test_run_loop_advances_offset_and_survives_errors(self):
        class LoopAPI(FakeAPI):
            def __init__(self):
                super().__init__()
                self.polls = 0
            def call(self, method, params=None, http_timeout=35):
                if method == "getUpdates":
                    self.polls += 1
                    self.calls.append((method, dict(params or {})))
                    if self.polls == 1:
                        raise tb.TelegramError("getUpdates failed: URLError")
                    if self.polls == 2:
                        update = msg("/start")
                        update["update_id"] = 40
                        return [update]
                    return []
                return super().call(method, params, http_timeout)
        api = LoopAPI()
        bot = tb.Bot(api, OWNER, root=self.root, today=lambda: "2026-10-04", run_async=False)
        with mock.patch("time.sleep"):
            tb.run_forever(bot, should_stop=lambda: api.polls >= 3)
        polls = [p for m, p in api.calls if m == "getUpdates"]
        self.assertNotIn("offset", polls[0])
        self.assertEqual(polls[2]["offset"], 41)
        self.assertTrue(api.texts())


if __name__ == "__main__":
    unittest.main()
