# ALANKRIT GLOBAL CONTEXT

Compiled 2026-10-04 from 4 complete extraction(s): alankrit-os, campus-fund, icarus, personal-brand. Incomplete/unmerged: none. Staleness: icarus evidence ends 2026-09-13.

**Read this first.** Two sources are authoritative and never merged: (1) `compiler/current_state.md`, Alankrit's own latest statement; (2) each project's handoff below. If they differ, the newer dated statement from Alankrit wins, and the older one stays as history.

## Current state (Alankrit's own latest statement)

Last updated: 2026-10-04

- **Brand goal (EXPLICIT):** 10k followers on X, 10k on LinkedIn, 1k on Substack. At the time: 31 on X, 840 on LinkedIn, 0 on Substack.
- **Work (EXPLICIT):** he works in the Founders Office at a VC called Campus Fund. Start date and terms not given.
- **Icarus (EXPLICIT):** the product thesis is still being revised. He is "working different possibilities that can become Icarus". Which one, if any, is chosen: UNKNOWN.
- **Supersedes:** the 2026-09-13 goals of 1k X / 2k LinkedIn and the unknown outcome of the job search recorded in the Icarus extraction.

## Brand agent policy (decided 2026-10-04)
Full text: `BRAND_AGENT_POLICY.md`. Alankrit's choices:
- **Agents draft and queue only; he posts everything himself.**
- **Claude writes the first draft; he edits it on his command.** This supersedes the 2026-09-16 Personal Brand rule that he writes first drafts.
- **Scout 5 organically built personal-brand accounts per platform (5 on X, 5 on LinkedIn)** and study their commenting patterns (read-only, sourced); swaps need his approval.
- **Goal: 10k X / 10k LinkedIn / 1k Substack by 2027-10-04, back-loaded pace** (his choices). Monthly checkpoints and input gates are in the policy; he confirmed the checkpoint table on 2026-10-04; the input gates are still a proposal. First checkpoint 2026-10-31: X 140, LinkedIn 1,050, Substack first post. This replaces the 1,000-X-by-2026-10-31 target.
- **Privacy:** nothing about Campus Fund without asking; own failures only if funny and occasional; Icarus as evidence in stories only, no relaunch series; age, city and B.Com may be used as already public.

---

# Project: Alankrit OS (`alankrit-os`)

## HANDOFF TO ALANKRIT OS — Alankrit OS (the context pipeline itself)

> Project-level context, extracted 2026-10-03. It must not be treated as a complete global model of Alankrit until it is reconciled with other project extractions.
> **Circularity warning:** this project is one day old and is the system that builds Alankrit's context. Almost all of its files were written by an AI assistant. Claims about Alankrit's traits that come from the workspace are restated Icarus evidence (`DERIVED_FROM_ICARUS`). Count them once.

### What it is
Alankrit OS is a personal context layer for AI agents. Each project is extracted by an agent running a universal protocol, read-only, into `context-extraction/<slug>/`. A compiler in `/Users/alankritghosh/Alankrit OS ` then merges the extractions into a global context (`python compiler/run.py`): registers, belief evolution, contradictions, JSONL memory, a knowledge graph, a validation report, and a first-read handoff. The stated eventual consumer is "an autonomous multi-agent personal-brand system", which is not evidenced anywhere yet.

### Why it exists
So that "another AI system, which has never seen this project before" understands what he built, why, how he decides and what he believes, and so that this context will "persist into my future AI systems" (v1 protocol). INFERRED: the same idea as Icarus (preserve the *why* behind decisions for agents), applied to himself.

### What Alankrit did (all 2026-10-03, IST)
18:48 issued v1 protocol in the Icarus repo → Icarus extracted flat → 19:08 created the Alankrit OS folder → 19:19 issued the global-compiler spec → an assistant built and ran the compiler (19:22–19:37), which found the corpus held only one project → 21:41 issued v2 protocol (per-project folders, archive rules, author labels, source ranking, lessons separate from failures) → 21:42 chose to extract Alankrit OS itself and to move Icarus into `icarus/` (done, sha256-verified, original archived).

### Major decisions
His: build the layer (D01); one universal read-only protocol (D02); mandatory epistemic labels (D03); two-stage, read-only architecture (D04); brand-system consumer (D05); fidelity > completeness > provenance > elegance > brevity (D06); JSONL + graph + reproducible compiler + validation (D07); v2 (D10); extract this project (D11); re-home Icarus (D12).
Assistant's (no review by him recorded): compiler = deterministic parsers + curated overlay + ref-validated narrative (D08); no cross-project claims from one project (D09); tag derived claims (D14).

### Beliefs (as directives he submitted; drafting author UNKNOWN)
Never present inference as fact or invent (B01). Context over facts (B02). Preserve history; recency is not truth (B03). Surface contradictions (B04). Failures are core context (B05). Trace every claim (B06). Project choices are not traits (B07). Assistant text is not his voice (B08). Unknowns are explicit states (B15).
**First two-project evidence in the whole corpus:** B01, B04, B06 and B15 match Icarus beliefs (cannot bluff; open contradictions; citations; three-valued unknowns). EXPLORATORY: an agent system can run his brand from this context (B11).

### How his thinking evolved (within three hours)
Flat output → per-slug folders (BT01). Voice examples with no authorship → mandatory ALANKRIT/ASSISTANT/UNKNOWN labels (BT02). Failures with lessons inside → lessons separated and labelled (BT03). Evolution as part of contradictions → its own document (BT04). Binary contradiction status → five statuses (BT05). "Prefer primary evidence" → ranked sources, his own words first (BT06). Causes are inferred from timing and wording; he did not state them.

### How he worked
Three long protocols (517 / 635 / 804 lines), three messages and two selections across ~3 hours; agents ran autonomously; durable files as memory; same-day scheduled headless agents for Icarus. This matches the Icarus record of delegating build work and keeping decisions.

### What failed / was learned
F01: the "global" layer could not be cross-project (one flat extraction) → v2 namespacing. The assistant's own failures in building it repeat Icarus failure classes: silent parse drops (F03), ID collisions (F04), a hash check that passed on two empty values (F07), prose counts gone stale (F08). Lesson: design against these classes up front (L04–L06). Validated is not verified: the compiler passes checks on judgments nobody has reviewed (C10, L09).

### How he communicated
**Not evidenced.** No prose in this project is established as his. The protocols are pasted; S-comp and S-v2 contain 23 and 21 em-dashes against his "No em-dashes. Ever." rule. Do not model his voice from them. Use `icarus/06_VOICE_PROFILE.md`.

### What it reveals about him (INFERRED unless marked)
He is building infrastructure so that agents can represent him. EXPLICIT goal; HIGH. He cares most that agents do not misrepresent him: inference as fact, AI text as his words, latest statement as truth, project choices as personality. These prohibitions repeat across all three versions; HIGH. He works by spec and delegation at high autonomy; MEDIUM-HIGH, two-project.

### Unresolved
Which projects next (O01). Does the brand system exist (O02). Compiler must read v2 files and two projects (O03, O06). Who drafted the protocols (O04). Re-extract Icarus under v2 (O05). Memory contract for the consumer (O07). Freshness cadence (O08). **Disclosure policy: the pipeline keeps full failure registers, but his public rule forbids showcasing his own failures (C07, O09).** No git (O10). No human review of compiled judgments (O11).

### What future agents should remember
1. Treat this extraction as metadata about the pipeline, not as new evidence about his personality.
2. Before publishing anything for him, respect the public no-own-failures rule even though memory contains failures (C07).
3. Keep authorship labels on everything you store about him; never promote assistant text to his voice.
4. Tag derived claims; never count the same evidence twice across extractions.
5. Every "current" fact has an as-of date; Icarus evidence stops at 2026-09-10.

---

# Project: Campus Fund (`campus-fund`)

## HANDOFF TO ALANKRIT OS — Campus Fund (lean)

> Very thin evidence: one internal meeting note (2026-09-25) and his 2026-10-04 statement.

- He works in the Founders Office at Campus Fund, a VC focused on student and young founders.
- The only recorded task: a brief to craft a one-line tagline for the organisation, with Apple and Figma as branding references.
- The meeting note is internal. Do not quote it, post about it or reuse its details publicly without asking him.
- Unknown: start date, terms, scope, whether any public statement about the job is allowed, and whether the role connects to the revised Icarus thesis.
- Context: it follows his September job search and sits beside his personal-brand push; his brand rules say no job framing in content.

---

# Project: Icarus (formerly JARVIS Engineering Intelligence) (`icarus`)

## HANDOFF TO ALANKRIT OS — Icarus (v2)

> Project-level context, extracted 2026-10-03 under protocol v2. It must not be treated as a complete global model of Alankrit until reconciled with other project extractions.
> Evidence: 1,552 human-typed messages (07-13 → 09-13), repo (585 commits on main, to 09-10), Obsidian vault, agent memory. Human evidence ends **2026-09-13**.
> Authorship matters here: much of what reads like "his voice" in the vault and posts was written by agents. See 07.

### What Icarus is
A GitHub-backed engineering memory. It answers *why* code is the way it is, with citations, or says "no one wrote this down". Surfaces: macOS app (hotkey, voice, glass overlay, decision graph), Chrome extension, a myth-themed 3D site, an MCP server for coding agents ("Agent Mode"), and terminal commands. Built almost entirely by AI agents under his direction, 06-27 → 09-10. Tagline: "Git remembers what changed. Icarus remembers why."

### Why it exists
In his words: "I see problems, in my workflows, get annoyed and then simply just try to build it … Icarus was originally supposed to be my personal assistant something like JARVIS from Ironman" (09-08). It pivoted into a company's engineering brain: "I don't want to build another cursor, claude code, codex or vscode … I want to build a brain an intelligence system a tech company would be foolish not to have in use" (07-27).

### What he was trying to do (in order)
Ship an honest engine (June–July) → make private repos work ("WHY THE FUCK WOULD ANYONE USE ICARUS FOR PUBLIC FUCKING REPOS", 07-15) → company brain (07-27) → serve coding agents (08) → turn it into "a full scale business, an actual startup" with a GTM co-founder and Antler funding (08-11 → 08-25) → launch on Product Hunt (09-01) → 50 users (09-04) → survive costs and learn sales through a job (09-10) → revise the product thesis and build a personal brand (09-13).

### Major decisions
Brain before face; one paid private-safe writer; private repos are the product (his outburst); AST chunking for "all languages … perfectly"; MCP open to private repos; human-confirmed decision capture, later moved into Claude Code; no Apple Dev ID until "proof of life and demand"; analytics capture on (08-13), then counts-only after a Codex privacy finding (08-14); no public failures (08-17); Agent Mode as the launch hero (08-30); 50 users (09-04); Oracle migration (09-10, not run); job search (09-10); thesis revision (09-13). Full register: 02 (50 entries).

### Beliefs
- Never bluff, but abstaining on things the repo contains is an embarrassing bug (C12 is the live tension).
- Distribution, not engineering, is the bottleneck; now he wants to learn sales himself.
- Human, specific, imperfect writing beats AI-polished writing; never use em-dashes; never show his own failures publicly; be honest with investors and co-founders.
- Spend only after proof of demand. Pre-revenue co-founders are paid in equity.
- Agents must show their sources; he no longer trusts their unverified context.

### How his thinking changed
Users: teams → low-attention readers → AI startups → agents → "serious guys like me" (because "every real dev … will already have an internal tool"). Product: assistant → CLI → company brain → agent memory → under revision. Bottleneck: engineering → business (stated 07-15, not acted on) → sales (09-10). Content: product posts → specific numbers → his own story posts → personal brand first. Infrastructure: enterprise tech for the learning → whatever is affordable. Full chains: 04 (20 transitions).

### How he worked
As router and judge over AI agents: Claude Code builds, Codex reviews, GPT models are tried. He pastes reviews between them, picks from proposed options in a few words ("do 1 and 2"), and asks for plain-language explanations ("I am not too apt with tech"). Rituals: read the handoff or vault → checklist → work → handoff. Sessions run late (5–6 am). Heavy on automation (scheduled scouts and syncs), which broke silently from 09-11.

### What he learned
"THERE IS NO POINT IN RUNNING ICARUS ON ALL THE REPOS, BURNING CREDITS AND TOKENS TO NOT HEAR BACK." Keep outreach simple. Real devs have internal tools. Sales is the bottleneck. His own words beat drafts. From the vault: fail-safe systems hide bugs; groundedness ≠ truth; a measurement's blind spot reads as a result.

### What failed
~104 cold emails → 2–3 replies; Show HN 1 point; Product Hunt 1 upvote ("0 views"); ~14–17 X followers after weeks of volume; Agent Mode unused at launch; multiple rejected launch videos; résumé overclaims surviving his removal order (agent error); 27 scheduled jobs failing silently (09-11 → 10-03). Engineering failures (fabrication, silent truncation, OAuth) were mostly caught and fixed. Full list: 08 (50 entries).

### How he communicated
Two registers. **Chat with agents:** lowercase, run-on, typos, "lets / Well / Alright / I suppose", profane in capitals when frustrated ("WHAT THE ACTUAL FUCK IS WRONG WITH YOU"), blunt social analogies. **Public:** his own posts are plain first-person stories with a chain of thought ("This is how I write things, simple but actually follow through with a chain of thought and a story"); approved agent drafts are terse contrast lines. Rules: no em-dashes, under 280 chars on X, no clichés, no polish, no public failures.

### What this project reveals about him
A 20-year-old who calls Icarus "the biggest risk of my life", describes himself as non-technical, and still built a deep, honest system by directing agents relentlessly. He has a high bar for taste and honesty and low tolerance for looking foolish or repeating himself. Business fundamentals (ICP, pricing) went unwritten while engineering absorbed the time. By September he had diagnosed distribution, money and his own sales skills as the constraints.

### Unresolved
1. What the revised product thesis (09-13) is. 2. Founder path vs job, after 09-13. 3. ICP and pricing. 4. Whether Agent Mode beats a good CLAUDE.md. 5. No-train contract for the production Gemini key. 6. All scheduled jobs failing since 09-11 (does he know?). 7. YC, Antler, co-founder candidates and barter: outcomes unknown. 8. Résumé overclaims still in the saved file. 9. Warm leads (Richie, aryan) left cold.

### What future agents should remember
- Start replies with "Alankrit," inside the Icarus project (his stated rule there; mem:always-address-as-alankrit). Never use em-dashes in his voice. Keep messages short and human. Put links inline.
- Explain effects in plain language before asking him to decide; offer 2–3 options.
- Show sources for every fact about people or numbers; read artifacts back, not your own report of them.
- Do not draft his reflective posts from scratch; tighten his words.
- Do not take irreversible or unrequested actions mid-task (he punished the unasked re-ingestion).
- Every "current" fact here is as of 2026-09-13 at best.

### Never assume
That posted lines are his own writing. That the résumé overclaims are his. That he reads code. That Icarus is still active, or still the priority, after 2026-09-13. That anger in chat with agents says anything about how he treats people. That an exploratory belief (novice users, vibe coders, harness > model) is settled.

---

# Project: Personal Brand (`personal-brand`)

## HANDOFF TO ALANKRIT OS — Personal Brand (lean)

> Project-level context. Not a complete model of Alankrit. Evidence: 7 distinct typed messages (2026-09-16) + an agent-written Obsidian vault (35 files, to 09-22).

### What it is
The vault and plan for growing "Alankrit Ghosh, curious builder, grower, inventor" on X, LinkedIn and later Substack. Built 2026-09-16 as the main project while Icarus is paused.

### Why
His words: "the current thesis loses to the growth of frontier models and that cannot become a business", and "this brand … portfolio of organic growth" as proof of GTM skill. Motive: building is fun, "fuck around and find out".

### Decisions that matter
Brand is the person, not a product (D01). He writes first drafts, agents edit (D10). Failures only occasionally and only if funny (D04). Swear on X only (D05). No job framing (D07). Lane reopened 09-18 toward explore-everything (D12, not locked). X primary from 09-20 (D14). Geopolitics never public (D18).

### What happened
Planning week, then silence: no posts, comments or replies recorded; last edit 09-22. On 2026-10-04 he reports X 31, LinkedIn 840, Substack 0, goals 10k / 10k / 1k.

### For future agents
- Never write his first draft of a post; edit, cut and check against Voice Rules.
- No em-dashes, hashtags or banned phrases; humour punches at himself; nothing about geopolitics or jobs.
- Verify any link or fact before adding it to a list.
- This vault says never post on his behalf; Alankrit OS may want the opposite. Ask before posting anything (C01, O06).

### Unresolved
Lane (O01); has any post shipped (O02); the dated goal (O03); the new Icarus thesis (O04); who wrote the playbook (O05); agent posting policy (O06).

---

## Brand Agent Policy

Version 3, 2026-10-04. Source: Alankrit's own answers in chat on 2026-10-04, plus the voice and boundary rules he set earlier (each cited). Only he changes this file. Any change gets a new dated version and the old one stays below as history.

### 1. What agents may do

**Draft and queue only.** Agents scout, draft, edit and prepare. Alankrit posts everything himself.

Agents never: post, reply, comment, like, repost, follow, connect, DM, email, submit, schedule or publish on his X, LinkedIn or Substack, and never on his behalf anywhere else. Preparing a draft with its link is the end of an agent's job.

Replies and comments are drafted with the direct clickable URL of the post (his standing rule: `mem:always-link-reply-targets`).

### 2. How drafting works (changed 2026-10-04)

- **Claude writes the first draft.** Alankrit edits it, and further revisions happen **on his command**: an agent does not keep iterating, posting or "improving" a draft on its own after delivering it.
- This **supersedes** the 2026-09-16 rule in the Personal Brand vault (`CLAUDE.md`, Decisions) that "Alankrit writes first drafts; Claude never generates the first draft". That vault still contains the old rule; it needs updating by him or on his instruction.
- Why this needs care: agent first drafts were rejected many times for sounding like AI ("screams fucking AI", 2026-09-09) and his own raw posts did better. So every first draft must:
  1. be built from examples he typed himself (the ALANKRIT voice examples, not agent text he approved);
  2. pass the voice checks in section 4 and show the result, naming any violation;
  3. contain no fact, number or name that is not traced to a source;
  4. be short, one idea, with at most two variants.
- If he says a draft is wrong in kind ("too polished", "AI generic"), the agent stops tuning and asks for his raw words to reshape, because he has repeatedly said that his own wording works best.

### 3. Scouting role-model accounts (new 2026-10-04)

Agents maintain a short list of **organically built personal-brand accounts** that generate strong engagement and visibility on their own, and study how they comment.

- **Selection:** grew mainly through their own content and replies, not paid promotion or bots; engagement is proportionate to followers (he has already flagged one account whose likes did not match its size); fits his curious-builder lane, including regular creators with a day job; never geopolitics-led accounts.
- **Per account, record:** handle and profile URL (opened and confirmed, never guessed), follower count with the date checked, what they post, and **their commenting pattern**: where they comment, how long, structure, opening line, tone, timing, whether they add a data point or a counterpoint, how often the author replies back.
- **Output:** a dated report with sources for every fact; patterns described, texts not copied. At most short quotes with attribution. The aim is to learn patterns, not clone voices.
- **Read-only:** scouts never interact with these accounts.
- **Size (his decision, 2026-10-04): 5 accounts per platform, so 5 on X and 5 on LinkedIn (10 in all).** Substack is not scouted until he has a first post live. Refresh monthly; swaps need his approval.

### 4. Voice rules every draft must pass

From his typed instructions and the extractions: no em-dashes (nor en-dash or spaced hyphen substitutes); no hashtags; no emoji unless he uses them; no cliché outreach ("compare notes", "would love to connect"); not the "it is X not Y" reframe; human and imperfect punctuation is fine, spelling errors are not; one thought per line; a specific number, name or moment instead of vague claims; humour punches at himself; swearing on X only, never on LinkedIn; X posts and replies under 280 characters; LinkedIn connection notes under 180 characters; Substack titles are "Why" questions; no job-hunting framing; **never geopolitics**.

### 5. What is private

| Area | Rule |
|---|---|
| Campus Fund | Nothing about its work, notes, people or investors in any draft unless he says so for that item. |
| His own failures | Occasional and funny only; never the identity; no zeros, defeat numbers or "we fail all the time". (Replaces the Icarus-era "never show failures" for personal posts; product failure numbers still stay out.) |
| Icarus | Evidence inside stories only. No relaunch series, no new product storyline, while the thesis is under review. |
| Personal facts | Age (21), Bangalore and the B.Com background may be used because he already states them. Everything else personal needs his approval. |
| Other people | No private messages or names without confirming; humour never targets the other person. |
| Secrets | Never any keys, tokens, contact details or financial data. |

### 6. Evidence rules

Every factual claim and number in a draft is traced to a source and read back before it goes to him. Links and handles are opened and confirmed. Counts carry the date they were checked. If a fact cannot be verified, the draft says it is unverified or leaves it out.

### 7. Goals and milestones

**Alankrit's decisions (2026-10-04):** 10,000 followers on X, 10,000 on LinkedIn, 1,000 on Substack, by **2027-10-04** (12 months), on a **back-loaded** pace: slow start, faster later. Starting counts on 2026-10-04: **31 / 840 / 0**.

**How the numbers were made:** I fitted a curve to his two choices (start, end date, back-loaded shape). **He reviewed the checkpoint table on 2026-10-04 and confirmed it.** He can still edit any figure.

| Checkpoint | X | LinkedIn | Substack |
|---|---|---|---|
| 2026-10-31 | 140 | 1,050 | first post live, ~10 |
| 2026-11-30 | 420 | 1,450 | 40 |
| 2026-12-31 | 850 | 2,000 | 90 |
| 2027-01-31 | 1,400 | 2,600 | 150 |
| 2027-02-28 | 2,050 | 3,300 | 210 |
| 2027-03-31 | 2,850 | 4,050 | 290 |
| 2027-04-30 | 3,750 | 4,900 | 380 |
| 2027-05-31 | 4,750 | 5,800 | 480 |
| 2027-06-30 | 5,850 | 6,700 | 600 |
| 2027-07-31 | 7,100 | 7,750 | 720 |
| 2027-08-31 | 8,400 | 8,800 | 850 |
| 2027-09-30 | 9,800 | 9,850 | 980 |
| **2027-10-04** | **10,000** | **10,000** | **1,000** |

**What each stretch demands (new followers per day, average):** X about 4 in October, 9 in November, 14 in December, 19 in January, then rising to about 30 by April, 36 by June and 46 by September. LinkedIn about 8, 14, 18, 21 and then 25 to 36. Substack about 1 a day in the first quarter, rising to 3 a day.

**Honest read:** the early targets are small on purpose, so the first test is not growth but output. From 2026-09-16 to 2026-10-04 X grew by about 3 and no post is recorded. The back half is steep: sustaining ~45 new X followers a day late in the year assumes the account has compounding reach by then. A shortfall in the first quarter makes the later months unrealistic rather than merely late.

**Input gates (my proposal; he confirmed the milestones but has not yet commented on these gates):** these are what agents actually control. Outputs (followers) are not.

| Input | Gate |
|---|---|
| X replies | 20-25 a day during October (his own ramp, 2026-09-20), scaling only if each reply still adds a data point or counterpoint |
| X posts | at least 5 a week, each started from his raw idea |
| LinkedIn | at least 2 posts and 10 comments a week |
| Substack | first post by 2026-10-31, then 1-2 a month |
| Scouting | report on the 5 + 5 role-model accounts within the first two weeks, then monthly |

**Review rule (from his 2026-09-20 decision):** if the input gates or checkpoints are missed for two weeks running, stop and revisit the plan with him instead of working harder on the same plan. The first formal review is at the 2026-10-31 checkpoint.

**Replaced:** the 2026-09-20 target of 1,000 X followers by 2026-10-31 (now 140 by 2026-10-31) and the 2026-09-13 goals of 1k X / 2k LinkedIn.

### 8. Checks and reporting

- Agents report counts weekly against these milestones, with the date each count was taken.
- Any scheduled job that fails must raise a visible alert; silent failure is not acceptable (all scheduled jobs failed unnoticed from 2026-09-11).
- A report states what was and was not done. Unfinished work is listed as unfinished.

### 9. Open items for Alankrit

1. Milestones are confirmed. Review the input gates in section 7 and edit any you disagree with.
2. Update the Personal Brand vault's old first-draft rule (section 2).
3. Name any role-model accounts you already want on the list (5 per platform; the agents propose the rest, you approve).
4. Name what "on my command" means in practice (a word, a button, a reply) so agents know when they may revise.

### History

- v1, 2026-10-04: created from his answers in chat.
- v2, 2026-10-04: milestones fixed to his choices (12 months, back-loaded); checkpoint figures computed; input gates added as a proposal.
- v3, 2026-10-04: milestones confirmed by him; role-model scouting set to 5 accounts per platform (X and LinkedIn).

---

## Known limits of this compilation

- Only the projects listed above are included. Everything else about Alankrit is absent, not negative.
- `alankrit-os` is derived evidence (its claims restate Icarus); do not count it twice.
- Statuses and classifications come from the extractions; no human has reviewed them.
