import json
import tempfile
import unittest
from pathlib import Path

from brand_agents import daily


def cand(n: int, text: str = "I built an agent workflow with Claude Code") -> dict:
    return {"url": f"https://x.com/user{n}/status/{n}", "author": f"user{n}", "post_text": text, "score": 10 + n, "opened": True}


class DailyTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name) / "2026-10-04"

    def tearDown(self):
        self._tmp.cleanup()

    def seed(self, count: int = 4):
        return daily.scout(self.dir, lambda: [cand(i) for i in range(1, count + 1)])

    def angles(self) -> dict:
        return json.loads((self.dir / "angles.json").read_text(encoding="utf-8"))

    def write_angles(self, data: dict):
        (self.dir / "angles.json").write_text(json.dumps(data), encoding="utf-8")

    def test_scout_writes_candidates_review_and_blank_angles(self):
        self.seed(3)
        self.assertEqual(len(json.loads((self.dir / "candidates.json").read_text())), 3)
        review = (self.dir / "review.md").read_text()
        self.assertIn("## 1. @user1 (score 11)", review)
        self.assertIn("https://x.com/user3/status/3", review)
        self.assertEqual(set(self.angles().values()), {""})
        self.assertEqual(len(self.angles()), 3)

    def test_scout_refuses_to_overwrite_without_force(self):
        self.seed()
        with self.assertRaises(FileExistsError):
            daily.scout(self.dir, lambda: [cand(9)])
        self.assertEqual(len(json.loads((self.dir / "candidates.json").read_text())), 4)

    def test_force_refresh_keeps_replies_already_written(self):
        self.seed()
        self.write_angles({**self.angles(), "https://x.com/user2/status/2": "My own take on this."})
        daily.scout(self.dir, lambda: [cand(2), cand(7)], force=True)
        angles = self.angles()
        self.assertEqual(angles["https://x.com/user2/status/2"], "My own take on this.")
        self.assertIn("https://x.com/user7/status/7", angles)
        self.assertEqual(angles["https://x.com/user7/status/7"], "")

    def test_merge_angles_normalizes_urls_and_never_blanks_text(self):
        merged = daily.merge_angles([cand(1)], {"https://x.com/user1/status/1/?s=20": "Kept."})
        self.assertEqual(merged, {"https://x.com/user1/status/1": "Kept."})

    def test_parse_keep(self):
        self.assertEqual(daily.parse_keep("1, 3,3,2", 4), [1, 3, 2])
        for bad in ["0", "5", "a", ",,", ""]:
            with self.assertRaises(ValueError, msg=bad):
                daily.parse_keep(bad, 4)

    def test_triage_shortlists_and_keeps_written_replies(self):
        self.seed(4)
        self.write_angles({**self.angles(), "https://x.com/user4/status/4": "Already wrote this one."})
        picked = daily.triage(self.dir, [1, 3])
        self.assertEqual([p["author"] for p in picked], ["user1", "user3"])
        self.assertEqual(json.loads((self.dir / "picks.json").read_text()), [p["url"] for p in picked])
        review = (self.dir / "review.md").read_text()
        self.assertIn("@user3", review)
        self.assertNotIn("@user2", review)
        angles = self.angles()
        self.assertEqual(set(angles), {"https://x.com/user1/status/1", "https://x.com/user3/status/3", "https://x.com/user4/status/4"})
        self.assertEqual(angles["https://x.com/user4/status/4"], "Already wrote this one.")

    def test_triage_requires_candidates(self):
        with self.assertRaises(FileNotFoundError):
            daily.triage(self.dir, [1])

    def test_replies_splits_ready_and_failing(self):
        self.seed(3)
        self.write_angles({
            "https://x.com/user1/status/1": "Compaction is where agents lose decisions.\nA record of what was rejected helps.",
            "https://x.com/user2/status/2": "This is fine — mostly.",
            "https://x.com/user3/status/3": "",
        })
        text, ready, failing = daily.build_replies(self.dir)
        self.assertEqual(ready, ["https://x.com/user1/status/1"])
        self.assertEqual(failing, ["https://x.com/user2/status/2"])
        self.assertIn("## Ready (1)", text)
        self.assertIn("## Fix before posting (1)", text)
        self.assertIn("FAIL: no em dash or en dash", text)
        self.assertIn("Compaction is where agents lose decisions.", text)
        self.assertNotIn("user3", text)

    def test_replies_flags_reframes_and_long_text(self):
        self.seed(2)
        self.write_angles({
            "https://x.com/user1/status/1": "It's not the model, it's the context.",
            "https://x.com/user2/status/2": "A thought. " * 40,
        })
        _, ready, failing = daily.build_replies(self.dir)
        self.assertEqual(ready, [])
        self.assertEqual(len(failing), 2)

    def test_replies_reports_urls_outside_todays_candidates(self):
        self.seed(1)
        self.write_angles({"https://x.com/stranger/status/99": "A reply for nothing."})
        text, ready, failing = daily.build_replies(self.dir)
        self.assertEqual((ready, failing), ([], []))
        self.assertIn("Not in today's candidates", text)

    def test_replies_with_nothing_written_says_so(self):
        self.seed(2)
        text, ready, _ = daily.build_replies(self.dir)
        self.assertEqual(ready, [])
        self.assertIn("None yet", text)

    def test_replies_requires_scout_first(self):
        with self.assertRaises(FileNotFoundError):
            daily.build_replies(self.dir)

    def test_cli_exit_codes_and_files(self):
        root = self.dir.parent
        self.seed(2)
        self.write_angles({"https://x.com/user1/status/1": "One clear thought."})
        self.assertEqual(daily.main(["--root", str(root), "--date", self.dir.name, "replies"]), 0)
        self.assertTrue((self.dir / "replies.md").exists())
        self.write_angles({"https://x.com/user1/status/1": "Bad — dash."})
        self.assertEqual(daily.main(["--root", str(root), "--date", self.dir.name, "replies"]), 1)
        self.assertEqual(daily.main(["--root", str(root), "--date", "1999-01-01", "replies"]), 2)
        self.assertEqual(daily.main(["--root", str(root), "--date", self.dir.name, "triage", "--keep", "9"]), 2)
        self.assertEqual(daily.main(["--root", str(root), "--date", self.dir.name, "triage", "--keep", "2"]), 0)

    def test_nothing_in_the_daily_module_can_post(self):
        source = Path(daily.__file__).read_text(encoding="utf-8").lower()
        for forbidden in ["click(", ".fill(", "like_button", "retweet", "send_message", "sendmessage"]:
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
