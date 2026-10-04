from datetime import date
from pathlib import Path
import tempfile
import unittest

from brand_agents.common import check_voice, require_all_pass
from brand_agents.draft_agent import build_variants
from brand_agents.issue_to_command import convert
from brand_agents.mobile_runner import run
from brand_agents.providers.x_playwright.find_posts import DEFAULT_DAYS, DEFAULT_QUERIES, DEFAULT_SCROLLS, DEFAULT_TAB, KEYWORD_CAP, load_seen, order_reasons, save_seen, score_text, search_url, with_since
from brand_agents.reply_scout import apply_angles, draft_reply, load_angles, render_report
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

    def test_x_scoring_blocks_agentic_finance_cluster(self):
        posts = [
            "Ho3in @Lucky_Man1990 \u00b7 @ama_protocol Exploring what is building around agentic finance. Confidential execution verifiable compute, and interoperable AI agents could make complex financial workflows much easier to use.",
            "Emin @Eminweb3 \u00b7 B.AI Is Building The Economic Infrastructure That Could Turn AI Agents Into Digital Participants. AI progress is often measured through intelligence. More capable Agents.",
            "Agentic Finance Graph @AgenticGraph \u00b7 Oct We are opening a free week for teams building with agents: platforms, wallets, x402 sellers. Bring your agents' wallets. DMs open",
        ]
        for text in posts:
            score, reasons = score_text(text)
            self.assertLess(score, 0, text)
            self.assertEqual(reasons, ["blocked topic"])

    def test_default_queries_exclude_finance_cluster(self):
        for query in DEFAULT_QUERIES:
            for term in ["-wallet", "-x402", '-"agentic finance"', "-crypto", "-filter:replies"]:
                self.assertIn(term, query)

    def test_why_lists_penalties_first(self):
        reasons = ["a", "b", "c", "d", "e", "f", "no question or first-person angle"]
        self.assertEqual(order_reasons(reasons)[0], "no question or first-person angle")
        self.assertIn("no question or first-person angle", order_reasons(reasons)[:6])

    def test_x_scoring_keeps_good_batch_3_posts(self):
        keep = [
            "MAIRU @lambdascript \u00b7 I\u2019ve been hitting the limits of Claude Code, so I\u2019m trying Ollama Cloud\u2019s Max plan. I\u2019m building an observability app right now, so this will be a real-world test of coding quality, agent reliability, speed, and cost.",
            "Conor Murphy @cnrmurphy \u00b7 8h Very impressed by the new Opus model. I canceled my CC sub before. I\u2019ve never been happy with the whole vibe coding thing, but so far I\u2019ve built a few things.",
        ]
        for text in keep:
            score, _ = score_text(text)
            self.assertGreaterEqual(score, 6, text)

    def test_x_scoring_rejects_tutorial_funnels(self):
        score, reasons = score_text(
            "Davidd Tech @DaviddDotTech \u00b7 Claude built me a trading bot in hours and I never wrote a line of code. "
            "Here's how you can do the same: Step : Get set up Download Claude desktop and open Claude Code."
        )
        self.assertLess(score, 0)
        score, reasons = score_text("Dev @dev \u00b7 I built an agent workflow with Claude Code. Step : install it, set up free account, done.")
        self.assertEqual(reasons, ["promo or hype post"])

    def test_x_scoring_blocks_trading_bots(self):
        score, reasons = score_text("I built a trading bot with Claude Code agents and a workflow")
        self.assertLess(score, 0)
        self.assertEqual(reasons, ["blocked topic"])

    def test_x_scoring_rejects_article_repost_without_opinion(self):
        score, reasons = score_text(
            "456X @OptionKing666 \u00b7 Oct Article OpenAI\u2019s Dots Lead Explains the Future of ChatGPT and Proactive Agents "
            "Host: Okay, Alex, I want to go deep on Dots. There are so many new products in the agent space."
        )
        self.assertLess(score, 0)

    def test_x_scoring_keeps_article_post_with_personal_angle(self):
        score, _ = score_text(
            "Raditya @perdhevi \u00b7 My Obsidian vault holds most of my thinking. So I built a local MCP server for it. "
            "Here's the walkthrough Article I built an MCP server for my Obsidian vault, with Claude Code agent search."
        )
        self.assertGreaterEqual(score, 6)

    def test_x_scoring_keeps_agent_opinion_post(self):
        score, _ = score_text(
            "Reuben Roy @ReubenRoy10 \u00b7 One of the advantages of building with agents is that you can relate much more with the user. "
            "Because you yourself have little understanding on how your app works, you make several of the mistakes your users will make "
            "once product gets released. So agents let you find them early."
        )
        self.assertGreaterEqual(score, 6)

    def test_discovery_is_wider(self):
        self.assertGreaterEqual(len(DEFAULT_QUERIES), 9)
        self.assertEqual(DEFAULT_SCROLLS, 8)
        self.assertTrue(any("MCP server" in query for query in DEFAULT_QUERIES))

    def test_x_scoring_rejects_follow_me_and_networking_bait(self):
        posts = [
            "Rashad @AI_Acq \u00b7 3h Build an AI team for your agents. Follow me for practical AI workflows for revenue.",
            "Rohan @RohanBhanotAI \u00b7 Oct Hey @X, help me find the builders. I'm Rohan, founder. I want to meet more people building with agents.",
        ]
        for text in posts:
            score, _ = score_text(text)
            self.assertLess(score, 0, text)

    def test_x_scoring_rejects_news_and_third_party_summaries(self):
        posts = [
            "Guth Labs @GuthLabs \u00b7 Oct Bolt.new acquires Dokai, bringing its enterprise agent team into its AI organization. The startup built agents.",
            "Light @LightSciencXXII \u00b7 5h Abhi Aiyer, CTO at Mastra, discusses building AI applications with TypeScript during an Open Source Friday episode. Agents, workflows, memory.",
        ]
        for text in posts:
            score, reasons = score_text(text)
            self.assertLess(score, 0, text)
            self.assertEqual(reasons, ["news or third-party summary"])

    def test_x_scoring_rejects_corporate_launch_but_keeps_personal_launch(self):
        corporate = "Swami @SwamiSivasubram \u00b7 Oct The team just launched Kiro workflows, which addresses time spent supervising agents building complex work."
        score, reasons = score_text(corporate)
        self.assertLess(score, 0)
        self.assertEqual(reasons, ["corporate announcement"])
        personal = "Eddie @eaftandilian \u00b7 I just launched SafeRE, a Java regex library. I learned a lot about building with agents and wrote about the workflow."
        score, _ = score_text(personal)
        self.assertGreaterEqual(score, 6)

    def test_x_scoring_keeps_context_compaction_post(self):
        score, _ = score_text(
            "Niall @nialldarwinlabs \u00b7 1h I keep noticing the same problem with AI coding agents: once context gets compacted, "
            "they can forget what was rejected, redo old work, or say something is done when it isn't. So I'm building Agent Guardian, "
            "a persistent reliability layer. Claude Code workflow."
        )
        self.assertGreaterEqual(score, 6)

    def test_load_angles_and_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "angles.json"
            path.write_text(
                '{"https://x.com/a/status/1?s=20": "My take on a.", "https://x.com/b/status/2/": "   ", "https://x.com/z/status/9": "Orphan."}',
                encoding="utf-8",
            )
            angles = load_angles(path)
        self.assertEqual(set(angles), {"https://x.com/a/status/1", "https://x.com/z/status/9"})
        targets = [
            {"url": "https://x.com/a/status/1", "post_text": "post a"},
            {"url": "https://x.com/b/status/2", "post_text": "post b"},
        ]
        result, unmatched = apply_angles(targets, angles)
        self.assertEqual(result[0]["angle"], "My take on a.")
        self.assertNotIn("angle", result[1])
        self.assertEqual(unmatched, ["https://x.com/z/status/9"])
        self.assertNotIn("angle", targets[0])

    def test_load_angles_rejects_bad_shapes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "angles.json"
            path.write_text("[]", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_angles(path)
            path.write_text('{"https://x.com/a/status/1": 5}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_angles(path)

    def test_human_angle_is_voice_checked_and_not_truncated(self):
        long_angle = "A thought. " * 40
        target = {"url": "https://x.com/a/status/1", "post_text": "post", "angle": long_angle, "opened": True}
        self.assertEqual(draft_reply(target), long_angle.strip())
        report = render_report([target])
        self.assertIn("FAIL", report)

    def test_human_angle_with_reframe_fails_voice_check(self):
        target = {"url": "https://x.com/a/status/1", "post_text": "post", "angle": "It's not the model, it's the context."}
        self.assertIn("FAIL", render_report([target]))

    def test_keyword_stuffing_is_capped(self):
        stuffed = "claude code ai agents agent build building built builder workflow workflows gtm startup product vibe coding cursor codex"
        _, reasons = score_text(stuffed)
        score, _ = score_text(stuffed)
        self.assertGreater(len(reasons), KEYWORD_CAP // 2)
        self.assertLessEqual(score, KEYWORD_CAP + 2 + 3 + 2 + 2)

    def test_x_scoring_rejects_automated_accounts(self):
        score, reasons = score_text("Polsia @newonpolsia \u00b7 Automated by @polsia I built infrastructure for AI agents and workflows.")
        self.assertLess(score, 0)
        self.assertEqual(reasons, ["automated account"])

    def test_x_scoring_rejects_profanity_and_rants(self):
        for text in [
            "AI @Davidwuuu92 \u00b7 Fuck Anthropic, Fuck claude code. I am building a mods for @claudeai. Why I got banned for no reason.",
            "Dev @dev \u00b7 This agent workflow is bullshit and I built it myself with Claude Code.",
        ]:
            score, reasons = score_text(text)
            self.assertLess(score, 0, text)
            self.assertEqual(reasons, ["profanity or rant"])

    def test_x_scoring_rejects_listicles_but_not_personal_github_posts(self):
        score, reasons = score_text(
            "Tung Air @tungair87 \u00b7 Connect apps, prototype AI agents, or turn scripts into automations. The source describes these GitHub projects "
            "as open-source options for building automations, agents and workflows. Pick a starting point based on your stack."
        )
        self.assertLess(score, 0)
        self.assertEqual(reasons, ["listicle or aggregator"])
        score, _ = score_text("Dev @dev \u00b7 I built two GitHub projects with Claude Code agents and learned a lot about the workflow. What would you change?")
        self.assertGreaterEqual(score, 6)

    def test_x_scoring_rejects_hashtag_farming(self):
        score, reasons = score_text(
            "Siva @sivasankar___s \u00b7 AI has changed development speed. It hasn't cancelled debugging. Are you vibe coding or still trying to understand the code? #AICoding #VibeCoding"
        )
        self.assertLess(score, 0)
        self.assertEqual(reasons, ["hashtag farming"])

    def test_single_hashtag_is_allowed(self):
        score, _ = score_text("Dev @dev \u00b7 I built an agent workflow with Claude Code and learned a lot. What do you use? #buildinpublic")
        self.assertGreaterEqual(score, 6)

    def test_link_in_post_is_penalized(self):
        base = "Dev @dev \u00b7 I built an agent workflow with Claude Code and learned a lot about it"
        plain, _ = score_text(base)
        linked, reasons = score_text(base + " https://example.com/post")
        self.assertEqual(plain - linked, 4)
        self.assertIn("link in post", reasons)

    def test_emoji_heavy_post_without_question_is_penalized(self):
        base = "Dev @dev \u00b7 I built an agent workflow with Claude Code and learned a lot about it"
        plain, _ = score_text(base)
        emoji, reasons = score_text(base + " \U0001F680\U0001F9E0")
        self.assertEqual(plain - emoji, 3)
        self.assertIn("emoji-heavy without question", reasons)

    def test_single_emoji_is_not_penalized(self):
        base = "Dev @dev \u00b7 I built an agent workflow with Claude Code and learned a lot about it"
        plain, _ = score_text(base)
        one, _ = score_text(base + " \U0001F680")
        self.assertEqual(plain, one)

    def test_emoji_with_question_is_not_penalized(self):
        text = "Siim @Humunuk \u00b7 Been busy \U0001F41D this weekend, excited to explore Claude Code mods. Have you built anything cool yet? \U0001F604 Biggest issue I have is editing files from the agent workflow"
        score, reasons = score_text(text)
        self.assertNotIn("emoji-heavy without question", reasons)
        self.assertGreaterEqual(score, 6)

    def test_penalties_are_listed_first_in_why(self):
        _, reasons = score_text("Dev @dev \u00b7 I built an agent workflow with Claude Code and learned a lot https://example.com \U0001F680\U0001F9E0")
        ordered = order_reasons(reasons)
        self.assertEqual(set(ordered[:2]), {"link in post", "emoji-heavy without question"})

    def test_x_scoring_rejects_testimonial_requests(self):
        score, reasons = score_text(
            "Synwave Academy @SynwaveAcademy \u00b7 16h Today, a room full of strangers became builders. If Vibe Coding Live changed something for you "
            "we'd love to hear it. Reply, quote, or post about what you learned. Tell your story."
        )
        self.assertLess(score, 0)
        self.assertEqual(reasons, ["testimonial or engagement request"])

    def test_x_scoring_rejects_job_and_internship_content(self):
        posts = [
            "Leo @double_burger_2 \u00b7 Zero internship experience, one simple AI project, and finally landed a ByteDance AI product internship. Agent practice sessions, resume submission.",
            "Dev @dev \u00b7 I landed a job offer building AI agents with Claude Code workflows",
            "Dev @dev \u00b7 My top interview questions for AI agent builders and product workflows",
            "Dev @dev \u00b7 How I tailored my resume for AI agent product roles and workflows",
        ]
        for text in posts:
            score, reasons = score_text(text)
            self.assertLess(score, 0, text)
            self.assertEqual(reasons, ["job or career content"], text)

    def test_job_rule_does_not_hit_ordinary_words(self):
        for text in [
            "Dev @dev \u00b7 I built an agent workflow with Claude Code and learned that interviews with users beat guessing. What do you do?",
            "Dev @dev \u00b7 I built an agent that summarizes my notes and the workflow keeps improving. What would you change?",
        ]:
            score, _ = score_text(text)
            self.assertGreaterEqual(score, 6, text)

    def test_job_rule_keeps_claude_code_resume_feature(self):
        for text in [
            "Dev @dev \u00b7 I built an agent workflow and now use claude --resume to continue Claude Code sessions. What do you use?",
            "Dev @dev \u00b7 I built my Claude Code workflow so I can resume the session after a crash. What would you change?",
        ]:
            score, reasons = score_text(text)
            self.assertGreaterEqual(score, 6, text)
            self.assertNotIn("job or career content", reasons)

    def test_solicitation_rule_keeps_genuine_questions(self):
        score, _ = score_text("Dev @dev \u00b7 I built an agent workflow with Claude Code and learned a lot. What did you learn building yours?")
        self.assertGreaterEqual(score, 6)

    def test_queries_require_english(self):
        for query in DEFAULT_QUERIES:
            self.assertIn("lang:en", query)

    def test_search_url_supports_top_and_live(self):
        self.assertIn("f=top", search_url("claude code", "top"))
        self.assertIn("f=live", search_url("claude code", "live"))
        self.assertIn("f=live", search_url("claude code"))
        with self.assertRaises(ValueError):
            search_url("claude code", "media")

    def test_default_tab_is_top_with_recency_window(self):
        self.assertEqual(DEFAULT_TAB, "top")
        self.assertEqual(DEFAULT_DAYS, 7)

    def test_with_since_adds_recent_window(self):
        self.assertEqual(with_since("q", 7, date(2026, 10, 4)), "q since:2026-09-27")
        self.assertEqual(with_since("q", None), "q")
        self.assertEqual(with_since("q", 0), "q")

    def test_discovery_covers_problem_and_memory_topics(self):
        joined = " ".join(DEFAULT_QUERIES)
        for term in ["Claude Code mods", "agent memory", "context window", "compaction", "biggest issue"]:
            self.assertIn(term, joined)
        self.assertGreaterEqual(len(DEFAULT_QUERIES), 15)
        self.assertEqual(len(DEFAULT_QUERIES), len(set(DEFAULT_QUERIES)))

    def test_x_scoring_rejects_paid_partnership_posts(self):
        score, reasons = score_text(
            "PARSA @Parsats_eth \u00b7 14h A big part of my day goes to switching between tools. Hedwig AI brings them into one workspace, "
            "with AI agents that have the full picture. Paid partnership"
        )
        self.assertLess(score, 0)
        self.assertEqual(reasons, ["promo or hype post"])

    def test_x_scoring_rejects_growth_hack_funnels(self):
        score, reasons = score_text(
            "Umer @UmerShips \u00b7 Sep I went from to users for my B2B SaaS in days. No ads. No content agency. No editor. "
            "Just one Reel format, posted twice a day. The crazy part? The system is stupidly simple \U0001F447 Article How I Turned UGC Reactions Into Users "
            "for the AI sales tool I'm building. The product was built."
        )
        self.assertLess(score, 0)
        self.assertEqual(reasons, ["growth-hack funnel"])

    def test_funnel_rule_keeps_ordinary_down_arrow_and_crazy_part(self):
        for text in [
            "Raditya @perdhevi \u00b7 My Obsidian vault holds my thinking, so I built a local MCP server with Claude Code agent search. Here's the walkthrough \U0001F447",
            "Dev @dev \u00b7 I built an agent workflow with Claude Code. The crazy part is how often the agent fixed its own bugs. What do you use?",
        ]:
            score, reasons = score_text(text)
            self.assertGreaterEqual(score, 6, text)
            self.assertNotIn("growth-hack funnel", reasons)


if __name__ == "__main__":
    unittest.main()
