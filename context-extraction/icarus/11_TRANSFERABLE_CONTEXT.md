# 11 — Transferable Context: Icarus

Rule: project choices are not personality traits. **LIKELY PERSONAL PREFERENCE** requires either repetition across many sessions and surfaces (code, content, outreach, career), or confirmation in the second extracted project (Alankrit OS, `../alankrit-os/`).

## LIKELY PERSONAL PREFERENCE
- No em-dashes in anything in his voice; human, imperfect punctuation; no cliché outreach; under 280 chars on X. (≥10 statements, all surfaces)
- He writes his own reflective posts; agent drafts must be tightened, not substituted. (08-14 → 09-07)
- Plain-language explanations before decisions; checklists; links inline. (≥15 instances)
- Delegates execution to AI agents at high autonomy; keeps taste, decisions and public posting. (whole record; also Alankrit OS)
- Durable context in files: handoffs, the vault, "read this and give me a checklist" session starts. (whole record; also Alankrit OS)
- Wants unattended automation (scheduled agents, bypass permissions). (Icarus + Alankrit OS)
- High visual and taste bar, calibrated on best-in-class references (Apple, Raycast, Obsidian, Perseus, Wispr Flow).
- Demands provenance from agents once trust breaks ("tell me where you got what from").
- Never invent, never present inference as fact (Icarus product rule + Alankrit OS protocol rule: two-project evidence).

## STRATEGIC PRINCIPLE (his statements; tested in one project)
- Honesty as a product property: cite or say unknown; but abstaining on knowable things is a bug (B01 + B38).
- Spend after proof of demand (B46). Co-founders are paid in equity pre-revenue (B44).
- The binding constraint gets the effort (B21, B49).
- Specific beats generic; human beats polished (B24, B42).
- Never show public failures; be honest with investors and co-founders (B26, B27).

## TECHNICAL KNOWLEDGE (reusable regardless of who holds it)
- Deterministic honesty gate: cite-or-abstain prompt + code checks (citations resolve to retrieved refs; rationale guard; entity-presence guard).
- Trust interlock: providers declare private_safe; never infer it from a key string.
- Three-valued state for any check that can fail; unknown never renders as 0 or false.
- fastembed bge-small + BM25 + RRF; AST chunking to fit a 512-token embedder; measure chunk lengths.
- Closed-unmerged PRs as a signal git can't show; mergedBy for authority; filter bots.
- Claude Code: a project `.mcp.json` server shadows a same-name user-scope server under headless `claude -p`; hooks can't own the keyboard.
- macOS: ad-hoc signing re-prompts the Keychain; only notarization clears the Sequoia "malware" prompt; SwiftPM Bundle.module traps in packaged apps.
- Azure ACA Consumption ties memory to 2× vCPU; Oracle halved Always Free Ampere to 2 OCPU / 12 GB on 2026-06-15 and terminates over-limit instances.
- GitHub OAuth callback must match exactly; a pair mismatch is invisible to code review.
- **Scheduled Claude agents fail silently when OAuth expires; add a failure alarm** (F39).

## PRODUCT KNOWLEDGE
- The honest "I don't know" sells only with real hits; users read over-abstention as stupidity (BT11).
- Low-attention users want 2–3 line, context-rich summaries (B37).
- Capture must be one-tap; confirmation behind a separate GUI doesn't happen (F24).
- Install friction kills trials; collapse install to one site link and the fewest steps (D48, B36).
- Talking to a codebase was loved; the agent-memory mode went unused without demand pull (09-02).

## BUSINESS KNOWLEDGE (mostly small-n)
- Volume is not a diagnosis; contact people with authority; role addresses bounce.
- Launch platforms (PH, Show HN) fail without an audience and account standing.
- Warm DMs beat cold email (2/10 same-hour vs ~0).
- Replies into large threads beat own posts 10–100x at a small follower count.
- SDR hiring: job-post knockout filters (years of experience) gate before the résumé is read (agent research, 09-10; UNVERIFIED by him).

## PROJECT-SPECIFIC (do not generalize)
Python-stdlib brain; gemini-paid single writer; GitLab manual deploy gate; frozen simonw/llm board; GitHub-only source; Azure → Oracle; Mac app as credential broker; X/Reddit/LinkedIn as the September channels; "Repo Brain / Company Brain" naming; the Icarus myth aesthetic; 50-user goal.

## UNCERTAIN / INSUFFICIENT EVIDENCE
- Enterprise-tech fascination (B39, one statement).
- Competition as validation (B50, one post draft).
- Whether profanity and anger in chat carry over to human collaborators (only agent-directed evidence).
- Whether the personal-brand pivot (09-13) is about Icarus or about himself (C28).
