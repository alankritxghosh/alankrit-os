# 00 — Project Context: Icarus

Extraction: 2026-10-03 (~22:30 IST), UNIVERSAL ALANKRIT CONTEXT EXTRACTION PROTOCOL **v2**. Supersedes the v1 extraction
(archived at `../archive/2026-10-03T2230_icarus-v1-schema/`).
Labels: `FACT` · `DECISION` · `EXPLICIT` · `INFERRED` · `HYPOTHESIS` · `UNKNOWN`. Confidence HIGH / MEDIUM / LOW.
Authorship: `ALANKRIT` (established as typed by him) · `ASSISTANT` (Claude, Codex or other model) · `UNKNOWN` (pasted, drafted elsewhere, or not attributable).

## Source key

| key | meaning |
|---|---|
| `S:<sid8>@<UTC time>` | A human-typed message in a Claude Code session transcript, `~/.claude/projects/-Users-alankritghosh-JARVIS--jarvis-engineering/<sid>.jsonl`. Typed messages are `ALANKRIT` unless they contain pasted agent output, which is marked separately. IST = UTC+5:30. |
| `vault:<note> §<heading>` | `~/Documents/Obsidian Vault/Icarus/`. Written by agents under his direction; entries tagged "(Alankrit)" record his calls. Author: ASSISTANT; decisions: his. |
| `repo:<path>` / `git:<hash>` | `/Users/alankritghosh/JARVIS /jarvis_engineering` (private GitHub `alankritxghosh/Icarus`, deploys via GitLab). Code and docs written by agents. |
| `mem:<file>` | Claude auto-memory for the repo: agent-written records of his feedback. |
| `v1:<file>` | Archived v1 extraction. Cited only where the claim was not re-verified in this run. |

**Evidence weight in this run (v2 source priority).** v1 relied on agent-written vault and repo docs. v2 adds **1,552 human-typed
messages across 106 sessions (2026-07-13 → 2026-09-13)**, the highest-priority evidence. Several v1 conclusions changed
as a result (listed at the end of this file).

## Project identity

- **Name:** Icarus. **Slug:** `icarus`. **Former name:** JARVIS Engineering Intelligence (v0, local CLI), archived as tag `jarvis-v0` / `git:2bdbac3` on 2026-06-27. `FACT` HIGH.
- **Origin, in his words** (ALANKRIT, `S:2f81409a@2026-09-08T15:08`): "I have the curiosity of building things, I see problems, in my workflows, get annoyed and then simply just try to build it, somewhere along the way I start pivoting in places, Icarus was originally supposed to be my personal assistant something like JARVIS from Ironman". So the JARVIS name was literal: a personal assistant that pivoted into an engineering brain. `EXPLICIT` HIGH.
- **Why "Icarus":** `UNKNOWN`. His site brief used the myth on purpose ("I want Icarus the myth character flying high as the hero", "his rise, all the way upto his fall", `S:696dfe35@2026-08-09T20:53`, `21:10`), but the reason for choosing the name is not recorded.
- **Dates:** repo 2026-06-27 → last commit 2026-09-10 (`git:25e583f`); last human session about Icarus 2026-09-13; the résumé dates his founder role from Mar 2026 (assistant-drafted, UNVERIFIED).
- **Status:** ACTIVE but stalled as of 2026-09-13. After that: no commits, no vault edits, no typed sessions, and 27 scheduled agent runs that failed on authentication (see Current state). `FACT` HIGH.

## Purpose, problem, user

- **Product (FACT HIGH):** a "privacy-first conversational engineering brain a company can buy". It ingests a GitHub repo (code, PRs, issues, commits) and answers *why / what / how* with citations, or says "no one wrote this down". Tagline: "Git remembers what changed. Icarus remembers why." (`repo:CLAUDE.md`, `repo:docs/VISION.md`).
- **The problem as he frames it (EXPLICIT):** decisions and rejected attempts are invisible to git and to coding agents. "A merged PR leaves a commit. A refused one leaves nothing." (his posted line, `S:c1cd1bc4@2026-08-14T21:45`).
- **His ambition for it (ALANKRIT, `S:6d69c3f2@2026-07-27T22:06`):** "I don't want to build another cursor, claude code, codex or vscode, nor do I want another basic developer tool, I want to build a brain an intelligence system a tech company would be foolish not to have in use".
- **Target user: never settled.** Moved from 5–20-engineer companies (v0) → teams / design partners (July) → low-attention readers (07-27) → B2B SaaS AI startups 1–5 years old (07-28) → React-heavy / gen-AI creative startups (08-04) → coding agents (08-03+) → novice "vibe coders … serious guys like me" in SF (09-05). See `04_BELIEF_EVOLUTION.md` BT03.

## System / architecture (FACT HIGH; from repo and vault)

```
GitHub (code + PRs + issues + commits)
 -> ingest (AST-aware via stdlib ast + tree-sitter; leak-safe token)
 -> per-tenant corpus (shared corpus per private repo; public cache shared)
 -> hybrid retrieval (BM25 + local fastembed bge-small, RRF, query normalization)
 -> cite-or-abstain prompt -> one rented writer (gemini-paid) behind a trust interlock
 -> deterministic honesty gate: (a) groundedness (b) rationale (c) entity-presence
 -> cited answer | "no one wrote this down"
faces: macOS app (hotkey, voice, glass overlay, decision graph) · Chrome MV3 extension · Next.js/three.js site
       · MCP server for coding agents ("Agent Mode") · terminal commands (Icarus --login/--connect/--decide)
hosting: Azure Container Apps (migration to Oracle authorized 09-10, not run) · CI: GitLab manual gate · releases: Sparkle
```

## Current state (2026-09-13, with what is known to 2026-10-03)

- Engineering core shipped: Mac app 0.1.13, extension, site at `try-icarus.vercel.app`, MCP, terminal decision flow. `FACT`.
- Seven human-confirmed Agent Mode decision proposals exist as unmerged `icarus/decision-*` branches (08-31 → 09-01; `git` branch list). The "merged = truth" rung of the authority ladder has not been reached. `FACT` HIGH.
- Traction: zero paying customers, zero design partners, no written ICP or pricing. X ~14–17 followers (assistant read of vault, 2026-09-13); LinkedIn outreach just started. ~104 cold emails, 2–3 human replies. Show HN 1 point, Product Hunt 1 upvote. `FACT` MEDIUM-HIGH.
- Money: Azure ₹5,629 in August; empty canary (₹1,550/mo) deleted 09-10; Oracle migration authorized, not run. He wrote: "I suppose I will need a job fast to be able to afford the costs of running Icarus on the cloud" (`S:468c2054@2026-09-10T08:03`). `EXPLICIT` HIGH.
- Job search: two applications rejected (he names them as "them"; the assistant context identifies MongoDB and Atlassian; `S:468c2054@2026-09-10T08:11`); a DevTools résumé was produced 09-10. Outcome after that: `UNKNOWN`.
- **2026-09-13:** "I am revising my thesis for Icarus" … "The thesis review is for Icarus as a product"; content to be "more on brand with me than Icarus"; goal 1k X / 2k LinkedIn followers (`S:57c4e98f`). The revised thesis is not recorded anywhere. `UNKNOWN`.
- **2026-09-11 → 2026-10-03:** every scheduled job (daily Work Queue status, weekly Gmail outreach sync; 27 runs) failed with "Failed to authenticate: OAuth session expired". Nothing reported the failures. `FACT` HIGH.
- Uncommitted at snapshot: Oracle plan, terminal Agent Mode commands, retention-copy fixes, `outputs/resume/`, growth notes. The vault's own git last committed 2026-09-02. `FACT`.

## Historical states / major phases

| phase | period | thesis | ref |
|---|---|---|---|
| 0 JARVIS v0 | ≤ 06-27 | personal assistant → local "why" CLI, "cannot bluff" | `git:2bdbac3`; `S:2f81409a@09-08` |
| 1 Honest brain, headless | 06-28 → 06-29 | brain before face; red eval baseline day one | `git:8afbfbb` |
| 2 Faces + private service | 06-30 → 07-16 | voice/overlay Mac app; hosted; private repos are the product | tags alpha-1…5 |
| 3 Depth / speaks-first | 07-17 → 07-30 | total coverage; "company brain"; features chosen by measurement | 02 D14, D36 |
| 4 Agent-facing + measurement era | 08-03 → 08-29 | MCP; refused-attempt signal; pre-registered experiments | 02 D19–D27 |
| 5 Launch, distribution, survival | 08-29 → 09-10 | PH launch; 50 users; cost cuts; job search | 02 D31, D33, D45 |
| 6 Thesis revision / stall | 09-13 → (10-03) | product thesis under review; personal-brand-first content | `S:57c4e98f` |

## Relationship to Alankrit

Icarus is the main body of evidence about him: a 20-year-old solo founder (his statement, `S:7440e957@2026-08-25T09:47`) who describes himself as non-technical, builds through AI agents, and treats the project as "the biggest risk of my life". See `12_ALANKRIT_CONTEXT.md`.

## Important constraints

Cash (Azure unaffordable; no domain: "I cannot afford one", `S:331ba684@2026-08-31T18:02`; no Apple Developer ID). Agent credit and usage limits ("we are at 96% limit for the week", `S:80a681e0@2026-08-28T19:33`). One person across every function. 8GB Mac at the start (v1 / `mem:public-repo-mvp-direction`). New-account standing on HN and Reddit.

## High-level lessons (detail: 08)

Groundedness ≠ truth. Fail-safe and silent failures hide bugs, which happened again with the scheduled jobs from 09-11. Volume is not a diagnosis. The wording, not the product, was wrong. A correct, honest engine with no audience and no written ICP did not sell itself.

## Major unresolved questions (detail: 09)

What the revised thesis is (09-13). Founder path vs employment. ICP and pricing. Whether Agent Mode beats a good CLAUDE.md. Whether the production Gemini key is on no-train terms. Why every scheduled job has failed since 09-11.

## What changed from v1 (corrections made by this run)

1. **Résumé overclaim.** v1 attributed "sold to engineering leaders" to him, against his own no-bluff rule. In fact the text was assistant-drafted. He told the agent to "Remove this" on 09-10. A residual tagline survived in the saved DevTools résumé (`10_CONTRADICTIONS.md` C09).
2. **Analytics.** v1 presented "Absence is not consent" as his principle. In fact he demanded content capture on by default on 08-13 ("we DONT FUCKING HAVE CUSTOMERS"). He reversed it on 08-14 after a Codex review found a P1 leak (BT10).
3. **Private repos.** He triggered their re-enabling himself, in a furious message on 07-15 (D11).
4. **Harshitha.** She was a **co-founder candidate**, not only a barter marketer. There was also an earlier GTM co-founder search (Manroze, via YC) (D39, D40).
5. **Job search.** The reason is now explicit: cloud cost, and wanting to learn sales (D45).
6. **Richie reply.** He reported it himself on 08-07 (O11 partly resolved).
7. **Evidence window.** It extends to 09-13 (human) and 10-03 (failed jobs).
8. **Voice.** A second, private register (chat with agents) is now documented: run-on, lowercase, profane under frustration (`07_VOICE_PROFILE.md`).
