# 13 — Knowledge Graph: Icarus

Machine-readable edges: `memory/relationships.jsonl` (basis: EXPLICIT / INFERRED). IDs refer to files 02–10.

```text
ICARUS (2026-06-27 → 09-13 active; stalled after)
 ├── ORIGIN: personal assistant "like JARVIS" ──derived_from──> JARVIS v0 CLI ──superseded_by──> Icarus  [E01, D01]
 ├── GOALS
 │    ├── company brain (D36) ──requires──> ICP, pricing, trust/legal [O01–O03, OPEN]
 │    ├── full-scale business / Antler (D47) ──blocked_by──> O01, O02
 │    ├── 50 users (D31) ──measured_by──> repos connected [O08]
 │    └── visibility for Icarus + himself (09-08) ──superseded_by──> personal brand first (D46, 09-13)
 ├── USERS: teams → low-attention readers → B2B AI startups → creative/gen-AI → agents → novices → serious vibe coders (BT03)
 ├── COMPONENTS
 │    ingest (AST, D12) → hybrid retrieval (D08) → writer (D09) ↔ trust interlock (D07) → gate (D13)
 │    faces: Mac app (Sparkle, D38) · extension · site (D29) · MCP (D18) · terminal (D32)
 │    hosting: Render → Azure (D10, enterprise-tech motive B39) ──superseded_by──> Oracle plan (D33, not run)
 ├── BELIEFS
 │    ├── B01 no bluff ──contradicted_by (tension)──> B38 abstention on knowable things is a bug  [C12]
 │    ├── B26 no public failures ──caused──> D22 ; ──contradicted──> B25 evidence-is-marketing [C07]
 │    ├── B21 distribution bottleneck ──led_to──> D45 job search, B49 learn sales
 │    └── B42 human writing ──led_to──> voice rules ; ──supported_by──> F45 rejected drafts
 ├── DECISIONS (50): key reversals D04→D09/D11, D21 (on→off in a day), D25→D31, D10→D33
 ├── EXPERIMENTS: A–D, C2 (4/4→1/4, F25), matched pair, quality delta (F27), history pilot (paused, O21)
 ├── FAILURES
 │    ├── silent-failure class: F05, F14, F19, F21 ──recurred_as──> F39 (27 scheduled runs, 09-11→10-03)
 │    ├── fabrication class: F01–F03, F30, F40 (résumé), F43 (agent research)
 │    └── distribution class: F31, F33–F35, F48 ──led_to──> D23, D31, D44, D45
 ├── PEOPLE
 │    ├── Alankrit (founder, 20) ── directs ──> Claude Code (builder/auditor), Codex (reviewer/builder), GPT models
 │    ├── co-founder candidates: Manroze (D39, via YC), Harshitha (D40 → barter D28)
 │    ├── early testers / feedback: Morphic AI team (relative), engineer friend, "aryan"
 │    ├── warm replies: Richie (Cap) (O11, O39), Prem, Idov, Deepak, Rohit Yadav, Akash
 │    └── demo for: Artem (uptimepage, C06)
 ├── TECHNOLOGIES: Python stdlib, fastembed, tree-sitter, Gemini, SwiftUI, Sparkle, MV3, Next.js, three.js, MCP,
 │                 Azure ACA, GitLab CI, Vercel, PostHog (counts-only), Obsidian, Claude Code, Codex, DaVinci Resolve, Raylight
 ├── OUTCOMES: Mac app 0.1.13 · PH 1 upvote · Show HN 1 point · ~104 emails / 2–3 replies · ~14–17 X followers · 0 revenue
 ├── OPEN LOOPS: O31 revised thesis · O32 broken scheduled jobs · O27 founder vs job · O01/O02 ICP/pricing · O05 no-train terms
 └── DATES: 06-27 reset · 07-15 private-repo outburst + business-first priority · 07-27 company brain · 08-04 agents
            · 08-17 content rules · 08-25 "biggest risk of my life" · 09-01 PH · 09-04 50 users · 09-10 job · 09-13 thesis revision
```

## Cross-project edges

```text
ICARUS ──derived_from──> JARVIS v0 (EXPLICIT)
ICARUS extraction (this) ──consumed_by──> Alankrit OS global compiler (EXPLICIT; ../alankrit-os/)
Icarus "never bluff" ──echoed_in──> Alankrit OS rule "NEVER present an inference as a fact" (INFERRED, two-project)
Icarus origin (personal assistant like JARVIS) ──related_to──> Alankrit OS, a personal context layer for his agents (INFERRED)
Icarus goal "visibility for … ourselves" (09-08) / personal brand (09-13) ──related_to──> Alankrit OS consumer:
     "autonomous multi-agent personal-brand system" (INFERRED)
```
