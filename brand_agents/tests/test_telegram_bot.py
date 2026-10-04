import json
import os
import re
import stat
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

from brand_agents import daily, decisions, drafter, telegram_bot as tb

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
        self.draft_calls = []
        self.draft_result = None
        self.bot = tb.Bot(self.api, OWNER, root=self.root, scouter=self.fake_scouter, today=lambda: "2026-10-04", run_async=False, drafter=self.fake_drafter, decisions_path=self.root / "decisions.jsonl")

    def tearDown(self):
        self._tmp.cleanup()

    def fake_drafter(self, item, avoid=None):
        self.draft_calls.append((item["author"], avoid))
        if self.draft_result is not None:
            return self.draft_result
        suffix = " (again)" if avoid else ""
        return drafter.DraftResult(f"Draft for {item['author']}{suffix}.", "ok", "", 1)

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
        for update in [msg("/start", STRANGER), msg("/scout", STRANGER), press(f"e:{self.tag(1)}", STRANGER), msg("hello", STRANGER)]:
            self.bot.handle_update(update)
        self.assertEqual(self.api.calls, [])

    def test_owner_in_a_group_chat_is_ignored(self):
        update = msg("/start")
        update["message"]["chat"]["id"] = -999
        self.bot.handle_update(update)
        self.assertEqual(self.api.calls, [])

    def test_every_message_goes_only_to_the_owner(self):
        self.seed()
        for update in [msg("/start"), msg("/more"), press(f"e:{self.tag(1)}"), msg("One clear thought."), msg("/ready"), msg("/status")]:
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
        rows = cards[0]["reply_markup"]["inline_keyboard"]
        self.assertEqual([[b["text"] for b in row] for row in rows], [["Use draft", "Edit"], ["Redraft", "Skip"]])
        self.assertTrue(rows[0][0]["callback_data"].startswith("u:"))
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
        self.bot.handle_update(press(f"e:{self.tag(3)}"))
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
        self.bot.handle_update(press(f"e:{self.tag(1)}"))
        self.assertNotIn("Switched", self.api.texts()[-1])
        self.bot.handle_update(press(f"e:{self.tag(2)}"))
        last = self.api.texts()[-1]
        self.assertIn("Switched. I dropped @user1", last)
        self.assertIn("tap Edit on it again", last)
        self.assertIn("Send your reply to @user2", last)
        self.assertEqual(self.bot.state()["pending"], "https://x.com/user2/status/2")

    def test_tapping_the_same_post_twice_is_not_a_switch(self):
        self.seed()
        self.bot.handle_update(press(f"e:{self.tag(1)}"))
        self.bot.handle_update(press(f"e:{self.tag(1)}"))
        self.assertNotIn("Switched", self.api.texts()[-1])

    def test_saved_reply_names_the_post_it_belongs_to(self):
        self.seed()
        self.bot.handle_update(press(f"e:{self.tag(1)}"))
        self.bot.handle_update(press(f"e:{self.tag(3)}"))
        self.bot.handle_update(msg("One clear thought."))
        last = self.api.texts()[-1]
        self.assertIn("Ready for @user3.", last)
        self.assertIn("https://x.com/user3/status/3", last)
        self.assertEqual(self.bot.angles().get("https://x.com/user1/status/1", ""), "")

    def test_reply_text_is_html_escaped(self):
        self.seed()
        self.bot.handle_update(press(f"e:{self.tag(1)}"))
        self.bot.handle_update(msg("Use <b>hooks</b> & skills."))
        self.assertIn("&lt;b&gt;hooks&lt;/b&gt; &amp; skills.", self.api.sent()[-1]["text"])

    def test_failing_reply_lists_problems_and_stays_pending(self):
        self.seed()
        self.bot.handle_update(press(f"e:{self.tag(2)}"))
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
        self.assertIn("Tap Edit", self.api.texts()[-1])
        self.assertEqual(set(self.bot.angles().values()), {""})

    def test_cancel_clears_pending(self):
        self.seed()
        self.bot.handle_update(press(f"e:{self.tag(1)}"))
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
        self.bot.handle_update(press(f"e:{self.tag(1)}"))
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

    # ----- drafts -----
    def test_every_card_carries_a_draft_to_copy(self):
        self.seed(3)
        self.bot.handle_update(msg("/more"))
        cards = [p for p in self.api.sent() if p.get("reply_markup")]
        self.assertEqual(len(cards), 3)
        self.assertEqual(cards[0]["parse_mode"], "HTML")
        self.assertIn("Draft:\n<code>Draft for user1.</code>", cards[0]["text"])
        self.assertEqual([a for a, _ in self.draft_calls], ["user1", "user2", "user3"])
        self.assertEqual(self.bot.state()["drafts"]["https://x.com/user2/status/2"], "Draft for user2.")

    def test_a_draft_is_never_ready_until_the_owner_acts(self):
        self.seed(3)
        self.bot.handle_update(msg("/more"))
        self.assertEqual(set(self.bot.angles().values()), {""})
        self.api.calls.clear()
        self.bot.handle_update(msg("/ready"))
        self.assertIn("No ready replies", self.api.texts()[-1])

    def test_use_draft_saves_it_and_returns_copyable_text(self):
        self.seed(3)
        self.bot.handle_update(msg("/more"))
        self.api.calls.clear()
        self.bot.handle_update(press(f"u:{self.tag(2)}"))
        last = self.api.sent()[-1]
        self.assertIn("Ready for @user2.", last["text"])
        self.assertIn("<code>Draft for user2.</code>", last["text"])
        self.assertEqual(last["parse_mode"], "HTML")
        self.assertEqual(self.bot.angles()["https://x.com/user2/status/2"], "Draft for user2.")
        self.assertEqual(self.bot.angles().get("https://x.com/user1/status/1", ""), "")

    def test_use_draft_without_a_draft_says_so(self):
        self.seed(2)
        self.bot.handle_update(press(f"u:{self.tag(1)}"))
        self.assertIn("no draft", self.api.texts()[-1])
        self.assertEqual(self.bot.angles().get("https://x.com/user1/status/1", ""), "")

    def test_use_draft_rechecks_the_voice_rules(self):
        self.seed(2)
        self.bot.handle_update(msg("/more"))
        state = self.bot.state()
        state["drafts"]["https://x.com/user1/status/1"] = "Bad \u2014 draft."
        self.bot.save_state(state)
        self.bot.handle_update(press(f"u:{self.tag(1)}"))
        self.assertIn("no longer passes", self.api.texts()[-1])
        self.assertEqual(self.bot.angles().get("https://x.com/user1/status/1", ""), "")

    def test_edit_shows_the_draft_and_the_owners_version_replaces_it(self):
        self.seed(2)
        self.bot.handle_update(msg("/more"))
        self.bot.handle_update(press(f"e:{self.tag(1)}"))
        asked = self.api.sent()[-1]
        self.assertIn("Send your reply to @user1", asked["text"])
        self.assertIn("Draft for reference:\n<code>Draft for user1.</code>", asked["text"])
        self.bot.handle_update(msg("My own wording is better here."))
        self.assertEqual(self.bot.angles()["https://x.com/user1/status/1"], "My own wording is better here.")
        self.assertIn("Ready for @user1.", self.api.texts()[-1])

    def test_old_write_reply_buttons_still_work_as_edit(self):
        self.seed(2)
        self.bot.handle_update(press(f"w:{self.tag(1)}"))
        self.assertEqual(self.bot.state()["pending"], "https://x.com/user1/status/1")

    def test_redraft_asks_for_a_different_angle_and_sends_a_new_card(self):
        self.seed(2)
        self.bot.handle_update(msg("/more"))
        self.draft_calls.clear()
        self.api.calls.clear()
        self.bot.handle_update(press(f"r:{self.tag(1)}"))
        self.assertEqual(self.draft_calls, [("user1", "Draft for user1.")])
        card = self.api.sent()[-1]
        self.assertIn("<code>Draft for user1 (again).</code>", card["text"])
        self.assertTrue(card.get("reply_markup"))
        self.assertEqual(self.bot.state()["drafts"]["https://x.com/user1/status/1"], "Draft for user1 (again).")
        self.assertEqual(self.bot.angles().get("https://x.com/user1/status/1", ""), "")

    def test_failed_and_skipped_drafts_show_why_and_offer_edit(self):
        self.seed(1)
        for result, expected in [
            (drafter.DraftResult(None, "failed", "could not run Claude (not logged in)", 1), "not logged in"),
            (drafter.DraftResult(None, "skip", "no honest specific reply without facts about you", 1), "no honest specific reply"),
        ]:
            self.api.calls.clear()
            self.draft_result = result
            daily.write_json(self.bot.directory / "bot_state.json", {})
            self.bot.handle_update(msg("/more"))
            card = [p for p in self.api.sent() if p.get("reply_markup")][0]
            self.assertIn(expected, card["text"])
            self.assertIn("Tap Edit to write your own", card["text"])
            labels = [b["text"] for row in card["reply_markup"]["inline_keyboard"] for b in row]
            self.assertNotIn("Use draft", labels)
            self.assertIn("Edit", labels)

    def test_a_crashing_drafter_does_not_take_the_bot_down(self):
        self.seed(2)
        def boom(item, avoid=None):
            raise ValueError("secret detail")
        self.bot.drafter = boom
        self.bot.handle_update(msg("/more"))
        cards = [p for p in self.api.sent() if p.get("reply_markup")]
        self.assertEqual(len(cards), 2)
        self.assertIn("drafting error (ValueError)", cards[0]["text"])
        self.assertNotIn("secret detail", cards[0]["text"])

    def test_drafts_and_post_text_are_html_escaped_in_cards(self):
        daily.scout(self.bot.directory, lambda: [{**cand(1), "post_text": "Use <script>alert(1)</script> & more"}])
        self.draft_result = drafter.DraftResult("Try <b>this</b> & that.", "ok", "", 1)
        self.bot.handle_update(msg("/more"))
        card = [p for p in self.api.sent() if p.get("reply_markup")][0]["text"]
        self.assertNotIn("<script>", card)
        self.assertIn("&lt;script&gt;", card)
        self.assertIn("<code>Try &lt;b&gt;this&lt;/b&gt; &amp; that.</code>", card)

    def test_a_second_page_request_while_drafting_is_refused(self):
        self.seed(3)
        self.bot._paging = True
        self.bot.handle_update(msg("/more"))
        self.assertIn("Still drafting", self.api.texts()[-1])
        self.assertEqual(self.draft_calls, [])

    def test_paging_flag_is_released_even_if_sending_fails(self):
        self.seed(2)
        real = self.api.call
        def broken(method, params=None, http_timeout=35):
            if method == "sendMessage" and params.get("reply_markup"):
                raise tb.TelegramError("sendMessage failed: HTTP 400")
            return real(method, params, http_timeout)
        self.api.call = broken
        with self.assertRaises(tb.TelegramError):
            self.bot.send_page()
        self.assertFalse(self.bot._paging)

    def test_default_drafter_hands_the_post_to_the_drafting_module(self):
        item = cand(4)
        with mock.patch("brand_agents.drafter.draft_reply", return_value=drafter.DraftResult("x", "ok", "", 1)) as call:
            result = tb.default_drafter(item, "old draft")
        call.assert_called_once_with(item["post_text"], "user4", avoid="old draft")
        self.assertEqual(result.text, "x")

    # ----- decision log -----
    def events(self, action=None):
        events = decisions.read_events(self.root / "decisions.jsonl")
        return [e for e in events if action is None or e["action"] == action]

    def test_shown_cards_are_logged_with_their_draft_and_context(self):
        self.seed(2)
        self.bot.handle_update(msg("/more"))
        shown = self.events("shown")
        self.assertEqual([e["author"] for e in shown], ["user1", "user2"])
        first = shown[0]
        self.assertEqual(first["draft"], "Draft for user1.")
        self.assertEqual(first["draft_status"], "ok")
        self.assertEqual(first["score"], 19)
        self.assertIn("agent workflow number 1", first["post_text"])
        self.assertEqual(first["day"], "2026-10-04")
        self.assertEqual(first["url"], "https://x.com/user1/status/1")

    def test_use_draft_is_logged_as_agent_text_the_owner_approved(self):
        self.seed(2)
        self.bot.handle_update(msg("/more"))
        self.bot.handle_update(press(f"u:{self.tag(2)}"))
        (event,) = self.events("use_draft")
        self.assertEqual(event["author"], "user2")
        self.assertEqual(event["draft"], "Draft for user2.")
        self.assertEqual(event["final"], "Draft for user2.")
        self.assertEqual(event["final_source"], "draft_as_is")

    def test_skip_is_logged_with_whether_a_draft_existed(self):
        self.seed(2)
        self.bot.handle_update(msg("/more"))
        self.bot.handle_update(press(f"s:{self.tag(1)}"))
        (event,) = self.events("skip")
        self.assertEqual(event["author"], "user1")
        self.assertTrue(event["has_draft"])
        self.assertEqual(event["draft"], "Draft for user1.")

    def test_skip_without_a_draft_is_logged_as_such(self):
        self.seed(1)
        self.bot.handle_update(press(f"s:{self.tag(1)}"))
        (event,) = self.events("skip")
        self.assertFalse(event["has_draft"])
        self.assertIsNone(event["draft"])

    def test_an_edit_logs_the_draft_and_the_owners_own_words_separately(self):
        self.seed(1)
        self.bot.handle_update(msg("/more"))
        self.bot.handle_update(press(f"e:{self.tag(1)}"))
        self.bot.handle_update(msg("Draft for user1, but in my words."))
        self.assertEqual(len(self.events("edit_started")), 1)
        (event,) = self.events("edit_saved")
        self.assertEqual(event["draft"], "Draft for user1.")
        self.assertEqual(event["final"], "Draft for user1, but in my words.")
        self.assertEqual(event["final_source"], "typed_by_alankrit")
        self.assertGreater(event["similarity"], 0.6)
        self.assertLess(event["similarity"], 1.0)

    def test_an_edit_with_no_draft_has_no_similarity(self):
        self.seed(1)
        self.bot.handle_update(press(f"e:{self.tag(1)}"))
        self.bot.handle_update(msg("Entirely my own reply."))
        (event,) = self.events("edit_saved")
        self.assertIsNone(event["draft"])
        self.assertIsNone(event["similarity"])
        self.assertEqual(event["final_source"], "typed_by_alankrit")

    def test_a_rejected_edit_is_logged_with_the_failed_checks(self):
        self.seed(1)
        self.bot.handle_update(press(f"e:{self.tag(1)}"))
        self.bot.handle_update(msg("Bad \u2014 dash."))
        (event,) = self.events("edit_rejected")
        self.assertIn("no em dash or en dash", event["failed_checks"])
        self.assertEqual(self.events("edit_saved"), [])

    def test_redraft_is_logged_with_the_draft_it_replaced(self):
        self.seed(1)
        self.bot.handle_update(msg("/more"))
        self.bot.handle_update(press(f"r:{self.tag(1)}"))
        (event,) = self.events("redraft")
        self.assertEqual(event["previous_draft"], "Draft for user1.")
        self.assertEqual(event["draft"], "Draft for user1 (again).")

    def test_every_event_has_a_timestamp_and_schema(self):
        self.seed(1)
        self.bot.handle_update(msg("/more"))
        for event in self.events():
            self.assertEqual(event["schema"], decisions.SCHEMA)
            self.assertRegex(event["ts"], r"^\d{4}-\d{2}-\d{2}T")

    def test_a_broken_log_never_breaks_the_bot(self):
        self.seed(1)
        self.bot.decisions_path = Path("/proc/not-writable/decisions.jsonl")
        self.bot.handle_update(msg("/more"))
        self.bot.handle_update(press(f"u:{self.tag(1)}"))
        self.assertEqual(self.bot.angles()["https://x.com/user1/status/1"], "Draft for user1.")

    def test_the_log_never_contains_the_bot_token(self):
        self.seed(1)
        self.bot.handle_update(msg("/more"))
        raw = (self.root / "decisions.jsonl").read_text()
        self.assertNotIn("SECRET", raw)
        self.assertNotIn("api.telegram.org", raw)

    def test_tests_never_touch_the_real_log(self):
        self.assertNotEqual(self.bot.decisions_path, decisions.DEFAULT_LOG)

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
