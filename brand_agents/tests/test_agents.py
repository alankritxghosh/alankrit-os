from pathlib import Path
import tempfile
import unittest

from brand_agents.common import check_voice, require_all_pass
from brand_agents.draft_agent import build_variants
from brand_agents.issue_to_command import convert
from brand_agents.mobile_runner import run
from brand_agents.providers.x_playwright.find_posts import score_text, search_url
from brand_agents.reply_scout import draft_reply
from brand_agents.providers.x_playwright.save_cookies import build_state
from brand_agents.reply_scout import load_targets
from brand_agents.weekly_report import next_milestone


class AgentTests(unittest.TestCase):
    def test_voice_rejects_em_dash(self):
        checks = check_voice("This fails \u2014 obviously", "x")
        self.assertFalse(require_all_pass(checks))

    def test_x_length_limit(self):
        checks = check_voice("a" * 281, "x")
        self.assertFalse(require_all_pass(checks))

    def test_draft_uses_supplied_fact(self):
        variants = build_variants(
            "I build because it is fun. I learn on the way.",
            "x",
            [{"claim": "The claim is sourced.", "source": "test"}],
        )
        self.assertTrue(any("The claim is sourced." in variant for variant in variants))

    def test_reply_targets_require_opened(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "targets.json"
            path.write_text('[{"url":"https://x.com/a/status/1","post_text":"hi","opened":false}]', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_targets(path)

    def test_next_milestone(self):
        row = next_milestone("2026-10-04")
        self.assertEqual(row[0], "2026-10-31")

    def test_mobile_runner_draft(self):
        report = run({
            "command": "draft",
            "platform": "x",
            "raw_idea": "I build because it is fun.",
            "facts": [],
        })
        self.assertIn("Draft Agent Output", report)
        self.assertIn("Voice Check", report)

    def test_issue_form_to_draft_command(self):
        body = """### Command
Draft from raw idea

### Platform
x

### Raw idea
I build because it is fun.

### Facts JSON
```json
[]
```
"""
        command = convert(body)
        self.assertEqual(command["command"], "draft")
        self.assertEqual(command["platform"], "x")
        self.assertEqual(command["facts"], [])

    def test_x_scoring_prefers_agent_builder_posts(self):
        score, reasons = score_text("How are builders using Claude Code agents in real product workflows?")
        self.assertGreaterEqual(score, 8)
        self.assertIn("agent", reasons)

    def test_x_scoring_blocks_geopolitics(self):
        score, _ = score_text("AI agents and geopolitics in the election")
        self.assertLess(score, 0)

    def test_x_scoring_blocks_crypto(self):
        score, _ = score_text("AI agents need economic rails on Solana with token markets")
        self.assertLess(score, 0)

    def test_x_search_url(self):
        url = search_url('"AI agents" builders')
        self.assertTrue(url.startswith("https://x.com/search?q="))
        self.assertIn("f=live", url)

    def test_x_cookie_state(self):
        state = build_state("token", "csrf")
        names = {cookie["name"] for cookie in state["cookies"]}
        self.assertIn("auth_token", names)
        self.assertIn("ct0", names)

    def test_reply_mentions_claude_code(self):
        reply = draft_reply({"post_text": "Claude Code changed how I build products"})
        self.assertIn("Claude Code", reply)


if __name__ == "__main__":
    unittest.main()
