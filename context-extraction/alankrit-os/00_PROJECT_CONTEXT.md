# 00 — Project Context: Alankrit OS

Extraction date: 2026-10-03 (about 21:45–22:30 IST). Protocol: UNIVERSAL ALANKRIT CONTEXT EXTRACTION PROTOCOL (v2).
Labels: `FACT` · `DECISION` · `EXPLICIT` · `INFERRED` · `HYPOTHESIS` · `UNKNOWN`. Confidence HIGH / MEDIUM / LOW.
Author labels for any text: `ALANKRIT` · `ASSISTANT` · `UNKNOWN`.

> **Read this caveat first.** This project is one day old and mostly self-referential. Almost every artifact in the
> project folder was written by the assistant (Claude, in session 9d6810ae) from (a) prompts Alankrit submitted and
> (b) the Icarus extraction. Claims about Alankrit's traits found in the workspace are **derived from Icarus**, not
> independent evidence. They are tagged `DERIVED_FROM_ICARUS` in `memory/` so a global compiler does not count them twice.
> The independent evidence this project adds is narrow. It shows what Alankrit asked for, when, how the request evolved,
> and two choices he made.

## Source key (used throughout)

| key | what | author | location |
|---|---|---|---|
| S-v1 | v1 "UNIVERSAL PROJECT CONTEXT EXTRACTION PROTOCOL" (517 lines), first person ("What I, Alankrit…") | UNKNOWN (submitted by Alankrit) | `~/.claude/projects/-Users-alankritghosh-JARVIS--jarvis-engineering/ee20c209-88f5-4964-b927-a3f7ffe23259.jsonl`, user message 2026-10-03T13:18:18Z (18:48 IST) |
| S-comp | "Global Context Compiler" prompt (635 lines), third person | UNKNOWN (submitted by Alankrit) | `~/.claude/projects/-Users-alankritghosh-Alankrit-OS-/9d6810ae-6f0b-4db3-8ef5-72d274392edd.jsonl`, user message 2026-10-03T13:49:59Z (19:19 IST) |
| S-v2 | v2 "UNIVERSAL ALANKRIT CONTEXT EXTRACTION PROTOCOL" (804 lines), third person | UNKNOWN (submitted by Alankrit) | same session, user message 2026-10-03T16:11:23Z (21:41 IST) |
| S-ans | Answers to two multiple-choice questions | ALANKRIT (selection); option text by ASSISTANT | same session, 2026-10-03T16:12:00Z (21:42 IST) |
| W | Compiler workspace `/Users/alankritghosh/Alankrit OS /` (compiler/, 17 docs, memory/, voice_examples/) | ASSISTANT | file mtimes 19:22–19:37 IST |
| X-icarus | Icarus extraction `context-extraction/icarus/` (formerly flat at the root) | ASSISTANT (session ee20c209) about Alankrit | written 18:50–18:56 IST |
| H | Listing of `/Users/alankritghosh/` top-level folders (names only; contents not opened) | — | observed 2026-10-03 |

Excluded after inspection: sessions `a1a7ec67` and `c608e01f` (JARVIS folder, 2026-10-03). These are scheduled, headless Icarus jobs (Gmail outreach sync, Work Queue status). They are not this project, though they are cited once as working-style evidence.

## Project identity

- **Name:** Alankrit OS. `FACT` HIGH. The folder `/Users/alankritghosh/Alankrit OS ` has a trailing space in its name. It was created 2026-10-03 19:08 IST.
- **Slug:** `alankrit-os`.
- **Aliases / earlier names:** none recorded. The name first appears as the filename `HANDOFF_TO_ALANKRIT_OS.md`, required by S-v1 §20 at 18:48 IST. So "Alankrit OS" existed as a named target before its folder did. `FACT` HIGH.
- **Status:** ACTIVE, day 1. Not a git repository. `FACT` HIGH.
- **Relationship to other projects:** it consumes the Icarus extraction (X-icarus). Its stated eventual consumer is "an autonomous multi-agent personal-brand system" (S-comp). Whether that system exists, and in which folder, is `UNKNOWN`. H shows folders named `Personal Brand`, `alankrit.dev`, `thought-engine`, `composio-linkedin-agent`, but none was opened.

## Purpose and problem

- `EXPLICIT` (S-v1 intro, items 1–10): let "another AI system, which has never seen this project before" understand what he built, why, how he decides, believes, works and communicates, and "What context from this project should persist into my future AI systems."
- `EXPLICIT` (S-comp): construct "a single coherent Global Alankrit Context Layer". It is "not a project summary exercise", and the consumer is an autonomous multi-agent personal-brand system.
- `INFERRED` MEDIUM. The problem being solved is context loss across AI tools and projects. Agents that act for him (especially on his public brand) need his reasoning, beliefs and voice, with provenance.

## Target user

AI agents (EXPLICIT: "future autonomous agents should read first", S-comp Phase 21), and through them Alankrit himself. No human audience other than Alankrit is named.

## System (as built, 2026-10-03)

```
[per project]  agent runs extraction protocol (S-v1 → S-v2) inside the project, read-only
                 → context-extraction/<slug>/   (md + manifest + memory/*.jsonl under v2)
[global]       Alankrit OS workspace: python compiler/run.py
                 scan → parse (line-anchored) → normalize → reconcile (curated overlay) →
                 detect_conflicts → build_memory → build_graph → synthesize → validate
                 → ALANKRIT_GLOBAL_CONTEXT.md, HANDOFF_TO_ALANKRIT_OS.md, 00–16 docs, memory/, voice_examples/
[consumer]     autonomous multi-agent personal-brand system (not yet evidenced)
```

Design choices inside the compiler were made by the ASSISTANT (decision D08). There is no record that Alankrit reviewed them.

## Current state (as of this extraction)

- Two project extractions exist: `icarus/` (v1 schema) and `alankrit-os/` (v2 schema, this one). `FACT`.
- The global compile was run once, at 19:37 IST, over a single project. Its narrative docs say "ONE project" and became stale when this folder was created (C05). `FACT`.
- Icarus evidence ends 2026-09-10. Nothing between 2026-09-10 and 2026-10-03 is captured anywhere. `FACT`.
- No human review of any compiled output is recorded. `FACT`.

## Historical states (all 2026-10-03, IST)

1. 18:48 v1 protocol issued in the Icarus repo → flat extraction at the `context-extraction/` root.
2. 19:08–19:37 Alankrit OS folder created; global compiler built and run over one project.
3. 21:41 v2 protocol issued: per-slug folders, archive rules, author labels, a richer schema.
4. 21:42 Alankrit chose to extract Alankrit OS itself and to move Icarus into `icarus/`.
5. ~21:45 Icarus moved (sha256-verified), with the original kept in `archive/`.

## Important constraints

- Source projects and the extraction corpus are read-only, except that v2 extractions write into `context-extraction/<slug>/` (C01).
- No secrets or credentials in any context artifact (S-v1 constraint 11; S-comp Phase 19; S-v2 Rule 12).
- The evidence base is a single project plus this meta-project (see 09 and 10).

## High-level lessons (detail in 08)

- A global layer needs several independent, namespaced extractions. One flat extraction made "cross-project" claims impossible (F01).
- Silent failures appeared in the compiler itself: dropped beliefs, ID collisions, and a hash check that passed on two empty values (F03, F04, F07). These are the same failure classes the Icarus record names.
- Authorship has to be labelled before voice can be modelled (BT02).

## Major unresolved questions (detail in 09)

Which projects to extract next (O01). Where the personal-brand system is and how it consumes `memory/` (O02, O07). Who drafted the protocols (O04). Whether Icarus should be re-extracted under v2 (O05). How to keep context fresh (O08). How the personal-brand system should treat failures that his public rule keeps private (C07).
