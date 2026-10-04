import json
import os
import stat
import tempfile
import unittest
from datetime import date
from pathlib import Path

from brand_agents import decisions


class DecisionsTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "nested" / "decisions.jsonl"

    def tearDown(self):
        self._tmp.cleanup()

    def test_log_event_appends_lines_with_timestamp_and_schema(self):
        self.assertTrue(decisions.log_event({"action": "skip", "author": "a"}, self.path))
        self.assertTrue(decisions.log_event({"action": "use_draft", "author": "b"}, self.path))
        lines = self.path.read_text().splitlines()
        self.assertEqual(len(lines), 2)
        first = json.loads(lines[0])
        self.assertEqual(first["schema"], decisions.SCHEMA)
        self.assertEqual(first["action"], "skip")
        self.assertRegex(first["ts"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")

    def test_log_file_is_private(self):
        decisions.log_event({"action": "skip"}, self.path)
        self.assertEqual(stat.S_IMODE(os.stat(self.path).st_mode), 0o600)

    def test_unicode_is_kept_readable(self):
        decisions.log_event({"action": "skip", "post_text": "日本語 café"}, self.path)
        self.assertIn("日本語 café", self.path.read_text(encoding="utf-8"))

    def test_log_event_never_raises(self):
        self.assertFalse(decisions.log_event({"action": "skip"}, Path("/proc/nope/decisions.jsonl")))
        self.assertFalse(decisions.log_event({"action": "skip", "bad": object()}, self.path))

    def test_read_events_skips_corrupt_lines_and_missing_files(self):
        self.assertEqual(decisions.read_events(self.path), [])
        self.path.parent.mkdir(parents=True)
        self.path.write_text('{"action": "skip"}\nnot json\n[1,2]\n{"no_action": 1}\n{"action": "use_draft"}\n')
        self.assertEqual([e["action"] for e in decisions.read_events(self.path)], ["skip", "use_draft"])

    def test_similarity(self):
        self.assertEqual(decisions.similarity("same text", "same text"), 1.0)
        self.assertLess(decisions.similarity("abcdefghij", "zyxwvutsrq"), 0.1)
        self.assertIsNone(decisions.similarity(None, "x"))
        self.assertIsNone(decisions.similarity("x", ""))

    def test_summarize_counts_and_rates(self):
        events = (
            [{"action": "shown", "draft": "d"}] * 3 + [{"action": "shown", "draft": None}]
            + [{"action": "use_draft"}] * 2
            + [{"action": "edit_saved", "similarity": 0.5}, {"action": "edit_saved", "similarity": 0.7}]
            + [{"action": "skip", "author": "spammy"}] * 4
            + [{"action": "redraft"}]
        )
        s = decisions.summarize(events)
        self.assertEqual(s["decided"], 8)
        self.assertEqual((s["use_rate"], s["edit_rate"], s["skip_rate"]), (0.25, 0.25, 0.5))
        self.assertEqual((s["drafts_shown"], s["drafts_missing"], s["redrafts"]), (3, 1, 1))
        self.assertEqual(s["avg_similarity_of_edits"], 0.6)
        self.assertEqual(s["most_skipped_authors"], [("spammy", 4)])

    def test_summarize_with_nothing_decided_does_not_divide_by_zero(self):
        s = decisions.summarize([{"action": "shown", "draft": "x"}])
        self.assertIsNone(s["use_rate"])
        self.assertIsNone(s["avg_similarity_of_edits"])
        self.assertIn("n/a", decisions.format_summary(s))

    def test_since_filters_by_day(self):
        events = [{"action": "skip", "day": "2026-09-01"}, {"action": "skip", "day": "2026-10-03"}, {"action": "skip", "ts": "2026-10-04T10:00:00+00:00"}]
        recent = decisions.since(events, 7, today=date(2026, 10, 4))
        self.assertEqual(len(recent), 2)
        self.assertEqual(len(decisions.since(events, None)), 3)

    def test_cli_summary_and_empty_log(self):
        self.assertEqual(decisions.main(["--log", str(self.path), "summary"]), 1)
        decisions.log_event({"action": "use_draft", "day": "2026-10-04"}, self.path)
        self.assertEqual(decisions.main(["--log", str(self.path), "summary"]), 0)
        self.assertEqual(decisions.main(["--log", str(self.path), "summary", "--days", "7"]), 0)

    def test_the_default_log_is_outside_the_repo(self):
        repo = Path(decisions.__file__).resolve().parent.parent
        self.assertNotIn(repo, decisions.DEFAULT_LOG.resolve().parents)


if __name__ == "__main__":
    unittest.main()
