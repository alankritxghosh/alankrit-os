import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from unittest import mock

from brand_agents import daily, decisions, doctor, paths


def post(n, text="I built an agent workflow with Claude Code and learned a lot. What would you change?", **extra):
    return {"url": f"https://x.com/user{n}/status/{n}", "post_text": text, "opened": True, **extra}


class PathsTests(unittest.TestCase):
    def test_data_dir_defaults_to_the_secret_dir_and_follows_the_override(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("BRAND_DATA_DIR", None)
            self.assertEqual(paths.data_dir(), paths.SECRET_DIR)
        with mock.patch.dict(os.environ, {"BRAND_DATA_DIR": "/tmp/somewhere"}):
            self.assertEqual(paths.data_dir(), Path("/tmp/somewhere"))

    def test_login_cookies_never_follow_the_data_dir(self):
        from brand_agents.providers.x_playwright import find_posts
        with mock.patch.dict(os.environ, {"BRAND_DATA_DIR": "/tmp/in-the-repo"}):
            self.assertEqual(find_posts.DEFAULT_STATE.parent, paths.SECRET_DIR)
            self.assertEqual(find_posts.DEFAULT_STATE.name, "x-storage-state.json")

    def test_secret_dir_is_outside_the_repo(self):
        self.assertNotIn(paths.REPO_ROOT, paths.SECRET_DIR.resolve().parents)


class IngestTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_good_posts_become_scored_candidates_sorted_best_first(self):
        kept, dropped = daily.prepare_ingest([
            post(1, "I built an agent workflow with Claude Code. What would you change?"),
            post(2, "I built a Claude Code agent workflow product startup with codex and cursor builders. What do you think of the workflow?"),
        ])
        self.assertEqual(dropped, [])
        self.assertEqual(len(kept), 2)
        self.assertGreaterEqual(kept[0]["score"], kept[1]["score"])
        item = kept[0]
        self.assertTrue(item["opened"])
        self.assertEqual(item["url"], f"https://x.com/{item['author']}/status/{item['url'].rsplit('/', 1)[1]}")
        self.assertIn("ingested", item["why"])

    def test_posts_not_marked_opened_are_refused(self):
        kept, dropped = daily.prepare_ingest([{**post(1), "opened": False}, {"url": "https://x.com/u/status/2", "post_text": "text"}])
        self.assertEqual(kept, [])
        self.assertEqual(len(dropped), 2)
        self.assertIn("opened: true", dropped[0]["why"])

    def test_bad_urls_and_empty_text_are_dropped_with_a_reason(self):
        kept, dropped = daily.prepare_ingest([
            {"url": "https://example.com/status/1", "post_text": "x", "opened": True},
            {"url": "https://x.com/someone", "post_text": "x", "opened": True},
            post(3, "   "),
        ])
        self.assertEqual(kept, [])
        self.assertEqual([d["why"] for d in dropped], ["not an x.com status URL", "not an x.com status URL", "no post_text"])

    def test_the_scouts_filters_apply_to_ingested_posts(self):
        kept, dropped = daily.prepare_ingest([
            post(1, "Comment 'agents' and I'll send you the free guide to building AI agents workflow"),
            post(2, "Bolt.new acquires Dokai, bringing its enterprise agent team into its AI organization. Built agents."),
            post(3),
        ])
        self.assertEqual([k["author"] for k in kept], ["user3"])
        self.assertEqual(len(dropped), 2)
        self.assertTrue(all(d["why"].startswith("filtered") for d in dropped))

    def test_seen_and_duplicate_urls_are_skipped_and_urls_normalised(self):
        seen = {"https://x.com/user1/status/1"}
        kept, dropped = daily.prepare_ingest([
            post(1),
            {**post(2), "url": "https://twitter-ish.example"},
            {**post(5), "url": "https://www.x.com/user5/status/5?s=20"},
            post(5),
        ], seen)
        self.assertEqual([k["url"] for k in kept], ["https://x.com/user5/status/5"])
        self.assertEqual([d["why"] for d in dropped].count("already surfaced"), 2)

    def test_load_ingest_validates_the_shape(self):
        path = self.tmp / "in.json"
        path.write_text('{"not": "a list"}')
        with self.assertRaises(ValueError):
            daily.load_ingest(str(path))
        path.write_text('[1, 2]')
        with self.assertRaises(ValueError):
            daily.load_ingest(str(path))
        path.write_text(json.dumps([post(1)]))
        self.assertEqual(len(daily.load_ingest(str(path))), 1)

    def test_cli_ingest_builds_the_day_and_records_seen_urls(self):
        source = self.tmp / "posts.json"
        source.write_text(json.dumps([post(1), post(2, "Join my cohort, book a call"), {**post(3), "opened": False}]))
        seen = self.tmp / "seen.json"
        out = io.StringIO()
        with redirect_stdout(out):
            code = daily.main(["--root", str(self.tmp), "--date", "2026-10-04", "ingest", "--file", str(source), "--seen-file", str(seen)])
        self.assertEqual(code, 0)
        self.assertIn("1 candidates, 2 dropped", out.getvalue())
        day = self.tmp / "2026-10-04"
        self.assertEqual(len(json.loads((day / "candidates.json").read_text())), 1)
        self.assertEqual(json.loads(seen.read_text()), ["https://x.com/user1/status/1"])
        self.assertIn("https://x.com/user1/status/1", json.loads((day / "angles.json").read_text()))
        # the rest of the routine works on ingested data
        self.assertEqual(daily.main(["--root", str(self.tmp), "--date", "2026-10-04", "triage", "--keep", "1"]), 0)

    def test_cli_ingest_refuses_to_overwrite_without_force(self):
        source = self.tmp / "posts.json"
        source.write_text(json.dumps([post(1)]))
        args = ["--root", str(self.tmp), "--date", "2026-10-04", "ingest", "--file", str(source), "--no-dedupe"]
        with redirect_stdout(io.StringIO()):
            self.assertEqual(daily.main(args), 0)
            with redirect_stderr(io.StringIO()):
                self.assertEqual(daily.main(args), 2)
            self.assertEqual(daily.main(args + ["--force"]), 0)


class DecisionLogCliTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.log = Path(self._tmp.name) / "decisions.jsonl"

    def tearDown(self):
        self._tmp.cleanup()

    def run_cli(self, *args):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return decisions.main(["--log", str(self.log), "log", *args])

    def test_use_draft_is_logged_as_approved_agent_text(self):
        self.assertEqual(self.run_cli("--action", "use_draft", "--url", "https://x.com/a/status/1", "--author", "a", "--draft", "Claude wrote this."), 0)
        (event,) = decisions.read_events(self.log)
        self.assertEqual(event["final"], "Claude wrote this.")
        self.assertEqual(event["final_source"], "draft_as_is")
        self.assertEqual(event["source"], "claude_code_session")

    def test_edit_is_logged_as_the_owners_own_words_with_similarity(self):
        self.run_cli("--action", "edit_saved", "--url", "https://x.com/a/status/1", "--draft", "Claude wrote this.", "--final", "Alankrit rewrote this.")
        (event,) = decisions.read_events(self.log)
        self.assertEqual(event["final_source"], "typed_by_alankrit")
        self.assertGreater(event["similarity"], 0)
        self.assertLess(event["similarity"], 1)

    def test_skip_needs_only_a_url(self):
        self.assertEqual(self.run_cli("--action", "skip", "--url", "https://x.com/a/status/1"), 0)
        self.assertEqual(decisions.read_events(self.log)[0]["action"], "skip")

    def test_missing_required_text_is_refused_and_nothing_is_written(self):
        self.assertEqual(self.run_cli("--action", "use_draft", "--url", "https://x.com/a/status/1"), 2)
        self.assertEqual(self.run_cli("--action", "edit_saved", "--url", "https://x.com/a/status/1"), 2)
        self.assertEqual(decisions.read_events(self.log), [])

    def test_unknown_actions_are_rejected_by_the_parser(self):
        with self.assertRaises(SystemExit):
            self.run_cli("--action", "posted", "--url", "https://x.com/a/status/1")


class DoctorTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.secret = self.root / "secret"
        self.data = self.root / "data"
        self.repo = self.root / "repo"
        self.repo.mkdir()
        (self.repo / "BRAND_AGENT_POLICY.md").write_text("policy")
        self.day = self.data / "daily" / "2026-10-04"

    def tearDown(self):
        self._tmp.cleanup()

    def diagnose(self):
        return doctor.diagnose("2026-10-04", repo=self.repo, secret_dir=self.secret, data=self.data, git=False)

    def test_remote_mode_without_an_x_login(self):
        report = self.diagnose()
        self.assertEqual(report["mode"], "remote")
        self.assertFalse(report["can_scout"])
        self.assertIn("daily ingest", " ".join(report["next"]))

    def test_scout_mode_with_login_and_playwright(self):
        self.secret.mkdir()
        (self.secret / "x-storage-state.json").write_text("{}")
        with mock.patch("importlib.util.find_spec", return_value=object()):
            report = self.diagnose()
        self.assertEqual(report["mode"], "scout")
        self.assertIn("daily scout", " ".join(report["next"]))

    def test_login_without_playwright_cannot_scout(self):
        self.secret.mkdir()
        (self.secret / "x-storage-state.json").write_text("{}")
        with mock.patch("importlib.util.find_spec", return_value=None):
            self.assertEqual(self.diagnose()["mode"], "remote")

    def test_next_step_follows_the_state_of_the_day(self):
        self.day.mkdir(parents=True)
        (self.day / "candidates.json").write_text(json.dumps([{"url": "u1"}, {"url": "u2"}]))
        self.assertIn("not triaged", self.diagnose()["next"][0])
        (self.day / "picks.json").write_text(json.dumps(["u1"]))
        self.assertIn("1 shortlisted", self.diagnose()["next"][0])
        (self.day / "angles.json").write_text(json.dumps({"u1": "One clear thought."}))
        report = self.diagnose()
        self.assertEqual((report["today"]["replies_ready"], report["today"]["replies_failing"]), (1, 0))
        self.assertIn("1 replies ready", report["next"][-1])

    def test_failing_replies_are_called_out(self):
        self.day.mkdir(parents=True)
        (self.day / "candidates.json").write_text(json.dumps([{"url": "u1"}]))
        (self.day / "picks.json").write_text(json.dumps(["u1"]))
        (self.day / "angles.json").write_text(json.dumps({"u1": "Bad — dash."}))
        report = self.diagnose()
        self.assertEqual(report["today"]["replies_failing"], 1)
        self.assertIn("fail the voice check", " ".join(report["next"]))

    def test_missing_policy_stops_everything(self):
        (self.repo / "BRAND_AGENT_POLICY.md").unlink()
        report = self.diagnose()
        self.assertEqual(len(report["next"]), 1)
        self.assertIn("missing", report["next"][0])

    def test_data_dir_inside_the_repo_is_detected(self):
        report = doctor.diagnose("2026-10-04", repo=self.repo, secret_dir=self.secret, data=self.repo / "state", git=False)
        self.assertTrue(report["data_dir_in_repo"])
        self.assertFalse(self.diagnose()["data_dir_in_repo"])

    def test_report_text_and_json_render(self):
        text = doctor.format_report(self.diagnose())
        self.assertIn("Mode: REMOTE", text)
        self.assertIn("Next:", text)
        out = io.StringIO()
        with redirect_stdout(out), mock.patch("brand_agents.doctor.diagnose", return_value=self.diagnose()):
            self.assertEqual(doctor.main(["--json"]), 0)
        self.assertEqual(json.loads(out.getvalue())["mode"], "remote")

    def test_doctor_is_read_only(self):
        source = Path(doctor.__file__).read_text(encoding="utf-8")
        for forbidden in ["write_text", ".unlink(", "playwright.sync_api", "git\", \"commit", "git\", \"push", "os.remove"]:
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
