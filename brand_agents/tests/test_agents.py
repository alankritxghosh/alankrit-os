from pathlib import Path
import tempfile
import unittest

from brand_agents.common import check_voice, require_all_pass
from brand_agents.draft_agent import build_variants
from brand_agents.issue_to_command import convert
from brand_agents.mobile_runner import run
from brand_agents.providers.x_playwright.find_posts import load_seen, save_seen, score_text, search_url
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

    def test_x_scoring_rejects_employment_announcement(self):
        score, reasons = score_text("A bike mechanic now works at Anthropic after building AI agents")
        self.assertLess(score, 0)
        self.assertIn("employment announcement", reasons)

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

    def test_generic_claude_code_post_needs_human_angle(self):
        self.assertIsNone(draft_reply({"post_text": "Claude Code changed how I build products"}))

    def test_supplied_angle_is_used(self):
        reply = draft_reply({"post_text": "anything", "angle": "My own take."})
        self.assertEqual(reply, "My own take.")

    def test_reply_handles_multi_agent_tooling(self):
        reply = draft_reply({
            "post_text": "Switching between Claude Code, Codex, and Grok means juggling terminal windows. Parallel agent sessions and PR management in one Mac app."
        })
        self.assertIn("handoff", reply)

    def test_x_scoring_rejects_promo_posts(self):
        promos = [
            "Aryaman @AryamanJazzy \u00b7 Oct Who is building AI agents in GTM? Comment \u2018Usage\u2019 and I\u2019ll share how it happened.",
            "Abdulsalam @turnless_HQ \u00b7 SOMEONE JUST BUILT A CHEAT CODE FOR CLAUDE CODE with ready-made agents and skills",
            "1Claw AI @1clawAI \u00b7 Oct Building with agents or wallets? Our Telegram is where builders swap notes.",
        ]
        for text in promos:
            score, reasons = score_text(text)
            self.assertLess(score, 0, text)
            self.assertIn("promo or hype post", reasons)

    def test_x_scoring_ignores_author_bio(self):
        score, _ = score_text("Sonwa | n8n | Build AI Agents & Workflows @Sonwa127 \u00b7 Nobody patriotic pass Nigerians in diaspora.")
        self.assertLess(score, 6)

    def test_x_scoring_drops_brand_mention_without_angle(self):
        score, _ = score_text(
            "my self only @mamagith \u00b7 We\u2019re entering a phase where AI agents can become specialized operators "
            "with their own skills, workflows and execution logic. The infrastructure behind that shift matters. @ama_protocol"
        )
        self.assertLess(score, 6)

    def test_x_scoring_keeps_real_builder_posts(self):
        keep = [
            "Pawel @agilelabspl \u00b7 After a month of building in public with Chat GPT Codex I will give a try to Claude Code for another month. What is your experience advice, which is better to use?",
            "Kenny Hanson @kennyhanson \u00b7 8h Back before vibe coding got big, I built startups in weekends using Webflow, Airtable, and Zapier. TechLayoffs: aggregated excel layoff lists from twitter and built a search UX around it.",
        ]
        for text in keep:
            score, _ = score_text(text)
            self.assertGreaterEqual(score, 6, text)

    def test_voice_rejects_not_x_it_is_y_reframes(self):
        reframes = [
            "The interesting bit with Claude Code is not speed, it is how quickly bad taste becomes visible.",
            "The real pain is not picking one agent, it is managing the handoff.",
            "This isn't about speed. It's about taste.",
            "It's not the model, it's the context.",
        ]
        for text in reframes:
            self.assertFalse(require_all_pass(check_voice(text, "x")), text)

    def test_voice_allows_plain_statements(self):
        self.assertTrue(require_all_pass(check_voice("Picking one agent is the easy part. The handoff is the work.", "x")))

    def test_reply_templates_pass_voice_check(self):
        posts = [
            "Switching between Claude Code, Codex, and Grok means juggling terminal windows. Parallel agent sessions and PR management in one Mac app.",
            "Parallel agent sessions and PR management in one place",
            "After a month with Codex I will try Claude Code. Which is better to use?",
            "Microsoft put ThinkingBox on Hugging Face. It grades AI agents on the database records they leave behind.",
            "Back before vibe coding got big, I built startups in weekends.",
        ]
        for post in posts:
            reply = draft_reply({"post_text": post})
            self.assertIsNotNone(reply, post)
            self.assertTrue(require_all_pass(check_voice(reply, "x")), reply)

    def test_reply_engages_with_tool_comparison_question(self):
        reply = draft_reply({"post_text": "After a month with Codex I will try Claude Code. What is your experience, which is better to use?"})
        self.assertIn("Switching", reply)

    def test_reply_engages_with_agent_grading_post(self):
        reply = draft_reply({"post_text": "ThinkingBox grades AI agents on the database records they leave behind, not the chat transcript."})
        self.assertIn("state an agent leaves behind", reply)

    def test_off_topic_and_promo_style_posts_get_no_template(self):
        for post in [
            "GTM with AI agents is the future of sales",
            "Building AI agents and workflows. Kiro deserves a seat at the table.",
        ]:
            self.assertIsNone(draft_reply({"post_text": post}), post)

    def test_x_scoring_rejects_milestone_and_engagement_bait(self):
        posts = [
            "Founder Arc @FounderArcx \u00b7 Oct Just hit followers on LinkedIn. Started FounderArc to document building AI agents. Keep building.",
            "Elias @eandualem \u00b7 14h Two days ago I had followers. Today I'm close to . Thank you to everyone who said hi. I build open-source tools for coding agents. If you're building too, what are you working on? Let's #connect",
        ]
        for text in posts:
            score, reasons = score_text(text)
            self.assertLess(score, 0, text)
            self.assertIn("milestone or engagement bait", reasons)

    def test_x_scoring_rejects_polls(self):
        score, reasons = score_text("Pavel @PavelFlit \u00b7 Oct Building with agents got cheaper. Which bill hit you first? Acquisition % Support load % votes \u00b7 Final results")
        self.assertLess(score, 0)
        self.assertIn("poll", reasons)

    def test_x_scoring_keeps_real_mcp_build_post(self):
        score, _ = score_text(
            "Raditya @perdhevi \u00b7 My Obsidian vault holds most of my thinking, and my AI assistants couldn't see any of it. "
            "So I built a local MCP server for it. Ollama for embeddings, LanceDB for vectors, nothing leaves my machine. Claude Code agent search."
        )
        self.assertGreaterEqual(score, 6)

    def test_seen_file_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nested" / "seen.json"
            self.assertEqual(load_seen(path), set())
            save_seen(path, {"https://x.com/a/status/1", "https://x.com/b/status/2"})
            self.assertEqual(load_seen(path), {"https://x.com/a/status/1", "https://x.com/b/status/2"})

    def test_seen_file_tolerates_garbage(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "seen.json"
            path.write_text("not json", encoding="utf-8")
            self.assertEqual(load_seen(path), set())
            path.write_text('{"a": 1}', encoding="utf-8")
            self.assertEqual(load_seen(path), set())

    def test_vibe_coding_reply_needs_shipping_context(self):
        self.assertIsNone(draft_reply({"post_text": "i built this tool by vibe coding and i'm learning what features to add by using it"}))
        self.assertIsNotNone(draft_reply({"post_text": "Back before vibe coding got big, I built startups in weekends."}))


if __name__ == "__main__":
    unittest.main()
