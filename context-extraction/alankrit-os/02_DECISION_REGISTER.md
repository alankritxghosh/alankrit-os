# 02 — Decision Register: Alankrit OS

`Decider` says who made the call: ALANKRIT (his request or selection), or ASSISTANT (made by Claude while executing; not reviewed by him unless noted).
"Alternatives" are listed only where the evidence records them. Otherwise `—`.

**D01 · ≤18:48 · Build a persistent personal context layer ("Alankrit OS") for future AI systems.**
Decider: ALANKRIT. Context: work spread across many projects and AI sessions. Problem: a new AI "which has never seen this project before" lacks his reasoning (S-v1). Alternatives: —. Chosen: extract context per project and hand it off to "Alankrit OS". Rationale (EXPLICIT, S-v1): "What context from this project should persist into my future AI systems." Tradeoffs: heavy agent time per project. Result: pipeline exists. Reversed: no. Status: ACTIVE. Confidence: HIGH. Sources: S-v1 intro, §20.

**D02 · 18:48 · Use one universal, project-agnostic protocol, run by an agent inside each project, with read-only access.**
Decider: ALANKRIT. Alternatives: —. Rationale (INFERRED, MEDIUM): repeatable across ~40 home folders (H). Risks accepted: extraction quality depends on what the agent reads (the Icarus run read 0 session transcripts). Result: Icarus extraction. Status: ACTIVE (protocol revised to v2, D10). Sources: S-v1 "Do not modify project files"; X-icarus manifest.

**D03 · 18:48 · Epistemic labelling is mandatory: FACT / EXPLICIT_BELIEF / INFERRED_BELIEF / DECISION / HYPOTHESIS / UNKNOWN, plus HIGH/MEDIUM/LOW reliability.**
Decider: ALANKRIT. Rationale (EXPLICIT, S-v1 §4): "NEVER present an inference as a fact." Status: ACTIVE; extended in S-comp (status vocabulary) and S-v2 (author labels). Sources: S-v1 §4, §17.

**D04 · 19:19 · Two-stage architecture: per-project extractions feed a separate compiler workspace that treats the corpus as read-only.**
Decider: ALANKRIT. Rationale (EXPLICIT, S-comp): "The path above is the SOURCE CORPUS"; outputs go to the workspace. Tradeoff: two places to keep in sync. Status: ACTIVE, with the role refined by D10 (C01). Sources: S-comp preamble, Phase 22.

**D05 · 19:19 · The eventual consumer is an autonomous multi-agent personal-brand system.**
Decider: ALANKRIT. Status: STATED INTENT; the system itself is not evidenced (O02). Confidence: HIGH that it was stated, LOW on its state. Source: S-comp preamble.

**D06 · 19:19 · Optimization order: fidelity > completeness > provenance > elegance > brevity. Never invent, never silently resolve contradictions, never overwrite history with the latest statement.**
Decider: ALANKRIT. Status: ACTIVE; carried into S-v2's CRITICAL RULES. Source: S-comp Final Quality Test.

**D07 · 19:19 · Require machine-readable memory (JSONL), a knowledge graph, a reproducible local compiler (`python compiler/run.py`), and a validation report.**
Decider: ALANKRIT. Rationale (INFERRED, MEDIUM): agents need queryable memory and a reproducible build. Result: built (E07). Status: ACTIVE. Source: S-comp Phases 18, 19, 22, 23.

**D08 · ~19:20–19:37 · Compiler design: deterministic line-anchored parsers + a hand-curated overlay (`compiler/curated.py`) + authored narrative docs whose `[project:ID]` refs and quotes are checked by a validator.**
Decider: ASSISTANT. Alternatives considered (by the assistant): fully model-generated prose (rejected: unverifiable); fully deterministic (rejected: belief statuses and transitions need judgment). Tradeoffs: the overlay is manual and Icarus-specific, so it won't scale to many projects without per-project overlays. Result: 18 PASS / 2 WARN. Reviewed by Alankrit: **no record**. Status: ACTIVE. Sources: W `compiler/*.py`, `16_VALIDATION_REPORT.md`.

**D09 · ~19:25 · Do not claim cross-project patterns; label every "recurring" pattern as cross-domain within one project.**
Decider: ASSISTANT. Rationale: the corpus held one project. Status: ACTIVE until recompile. Source: W `03_GLOBAL_DECISION_REGISTER.md` § Recurring decision patterns.

**D10 · 21:41 · Protocol v2: per-project slug folders; archive before material overwrite; author labels; a 7-level source-priority ranking; new file set (adds belief evolution, Alankrit context and failures.jsonl; drops the glossary).**
Decider: ALANKRIT. Rationale (INFERRED, MEDIUM-HIGH): it fixes what the v0 compile exposed (see BT01–BT04). The slug examples in S-v2 (signal, tempo, pantheon, solar-forecasting, job-application-context) match the projects the compiler named as missing. Status: ACTIVE. Source: S-v2.

**D11 · 21:42 · Extract Alankrit OS itself.**
Decider: ALANKRIT (selection). Alternatives (offered by the assistant): extract a different project folder; re-home Icarus only. Chosen despite the stated warning that the result "would be mostly circular". Rationale: not stated. `HYPOTHESIS`: he wants every node, including the pipeline itself, captured as a project. Status: executed (this folder). Source: S-ans.

**D12 · 21:42 · Move the flat Icarus extraction into `icarus/`, archiving the original.**
Decider: ALANKRIT (picked the recommended option). Status: done (D13). Source: S-ans.

**D13 · ~21:46 · Execute the move as copy → sha256 verify → delete, with an ARCHIVE_NOTE explaining that the archive is for layout, not staleness.**
Decider: ASSISTANT. Note: the first attempt failed silently and was caught (F07). Status: done. Source: archive folder.

**D14 · ~21:50 · Tag every workspace-derived claim about Alankrit as `DERIVED_FROM_ICARUS`, and keep his authorship of protocol text `UNKNOWN`.**
Decider: ASSISTANT, under S-v2 Step 9 and Rule 8. Rationale: avoid double-counting in a global compile, and avoid attributing possibly AI-drafted prompts to him. Status: ACTIVE. Source: this folder's `memory/`.

## Not decided (deferred, by evidence)

Which project comes next; whether to re-extract Icarus under v2; how the brand system consumes memory; refresh cadence; whether any compiled output gets human sign-off. See 09.
