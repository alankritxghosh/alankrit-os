# 07 — Reasoning Model

> Authored narrative, copied by `python compiler/run.py`. Refs resolve via `compiler/validate.py`.
> 18 source reasoning patterns (R1–R18) come from one project. Below, **OBSERVED** = behavior recorded in the corpus;
> **INFERENCE** = the compiler's reading of why. "Recurring" means across domains inside Icarus (engineering, product,
> content, outreach, infrastructure), never across projects. The corpus has none to compare.

## Summary in one paragraph

He starts from a vivid end-state scene (JARVIS: hold a key, ask aloud, see receipts), then cuts to the smallest unit that can be *proven*. He defines how it fails before he builds it, and trusts measurements, reproductions and real user words over arguments. When a measurement contradicts him he reverses quickly and writes the reversal down. That rigor is strong where he can instrument (code, experiments, claims). It is weak where he cannot or chose not to (channels, ICP, pricing) [icarus:R1] [icarus:R2] [icarus:R5] [icarus:R6] [icarus:R12] [icarus:R18].

## Dimension by dimension

| dimension | OBSERVED | INFERENCE | conf | refs |
|---|---|---|---|---|
| **Decomposing problems** | Vision scene → narrowest provable brick ("cited answer or honest unknown about ONE repo"). Work is split into lettered bricks with red→green tasks. | Decomposes by *what can be verified*, not by feature list. | H | [icarus:R1] [icarus:X05L7] [icarus:D03] |
| **Evaluating alternatives** | Decision records list options and rejected paths (unified cloud vs pooled vs single-tenant; inline [Y/n] vs agent self-confirm vs terminal). | Rejects options that move trust from code to policy, even when cheaper. | H | [icarus:D05] [icarus:D32] [icarus:R9] |
| **Researching** | Reverse-engineers comparables (Unblocked, Glean, Greptile, Wispr; Cursor, Marc Lou for distribution); studies top PH launches and ATS. Marks confidence per claim. | Research is pattern-borrowing from winners, then adapted. More used for distribution than for pricing or ICP. | H / M | [icarus:X05L4] [icarus:D02] |
| **Testing assumptions** | Pre-registers predictions; logs amendments before outcomes; watches tests fail; reads transcripts instead of agent self-reports. | Treats his own optimism as the main contaminant. | H | [icarus:B05] [icarus:B06] [icarus:B17] |
| **Handling uncertainty** | Three-valued state; "no one wrote this down"; contradictions left "open" in Unknowns rather than picked; uncertainty expressed by scoping ("in one test", "n=1"). | Prefers a visible unknown to a confident guess, in code and in prose. | H | [icarus:R16] [icarus:B03] [icarus:X06L16] |
| **Responding to failure** | Every failure becomes a named rule with its cost (PROTOCOL: one rule per failure that actually happened; Learning entries open with "Cost:"). Surprising good results are treated as bugs until re-run. | Failure is converted to process. The process is not always followed (GC01, L7). | H | [icarus:R13] [icarus:R4] [global:GC01] |
| **Narrowing scope** | GitHub-only source, one frozen eval repo, one model, a "do not build yet" list, policy exclusions (no Slack/Notion, no training, no autonomous coding). | Narrowing is his default in engineering. | H | [icarus:R12] [icarus:D03] [icarus:D09] [icarus:A2] |
| **Broadening scope** | Distribution: email → X → LinkedIn → Substack → HN → PH → Reddit → LinkedIn in about 5 weeks; the three-channel rule broken within about 10 days. Engineering broadened too (org brain, investigation engine) while ICP stayed unwritten. | Broadens when the feedback signal is weak or absent. | M-H | [icarus:R12] [global:GC04] [icarus:C16] |
| **First principles** | "Code shows what exists. Not why it exists." Git is structurally blind to refused work, so a signal git lacks is the wedge. Asks "what fact would PROVE the property?" (`mergedBy` for authority). | Reasons from what a system can and cannot record. | H | [global:V01] [icarus:R10] |
| **Leverage** | Names the binding constraint and moves effort there ("Nothing is engineering-blocked. Everything is distribution-blocked"). Leverage = deterministic signals nobody else has, not better models. "Rent commodities, own the moat." | Seeks asymmetric, structural advantages over effort. | H / M-H | [icarus:R8] [icarus:R17] [icarus:B15] |
| **Tradeoffs** | Accepts tradeoffs openly when written (MCP private repos: exposure transferred to the client). Decides against his own data when values conflict, and records that he did (no public failures). Speed vs rigor by context. | Values are allowed to beat metrics, but only explicitly. | H | [icarus:D18] [icarus:R11] [icarus:R18] |
| **Abstract → system** | Turns principles into code-level guarantees: "cannot bluff" → deterministic gate; "absence is not consent" → counts-only analytics; human confirmation → signature that cannot accept a question. Measurement probes come before UI. | His abstractions are finished only when a function signature enforces them. | H | [icarus:R9] [icarus:R15] [icarus:D15] [icarus:D21] |
| **Revisiting decisions** | Reverses quickly (private repos in 2 days, site stack in 1 day, analytics in 1 day) and records reversals as features. Uses dated checkpoints and abort conditions. Some decisions are superseded in practice and never formally revised (three-channel rule). | Fast to revisit when a test or taste says so; slower to formally close what he has stopped doing. | H | [icarus:R5] [icarus:R14] [icarus:C5] [icarus:O23] |

## What persuades him / what he rejects

- **Persuaded by (H):** measurements, reproductions, a concrete failing case, real user words. Two human replies outweighed 102 silences [icarus:R6].
- **Rejects (H):** aphorisms, rounded numbers, premises inferred but not executed, claims resting on a summary instead of the source ("generalised crap") [icarus:R7] [global:V13].

## Precision about guarantees (distinctive)

He insists on the exact boundary of a claim: groundedness is provable in code, abstention only for the clear case; "narrows what's requested, never what's enforced"; "deployed and healthy, effect UNMEASURED" [icarus:R3] [global:V24]. **INFERENCE (H):** this is the most transferable trait of his reasoning, and the one a downstream agent most needs to imitate when writing for him.

## Where the model breaks (INFERENCE, M-H)

1. **Rigor follows instrumentation.** Where nothing was measured (site conversion was deliberately dark), choices about channels were made on near-zero signals and switched quickly [icarus:D24] [global:GC04].
2. **Engineering absorbs time that business questions need.** ICP and pricing have been open since 2026-07-16 [global:GO08] [global:GC03].
3. **Knowing ≠ designing against.** His own phrase. Groundedness was learned three times; silent failures recur [icarus:L7] [global:RL01] [global:RL02].

## Recurring reasoning patterns (count)

18 source patterns; 9 decision patterns derived from them (see `03_GLOBAL_DECISION_REGISTER.md` § Recurring decision patterns). None can be confirmed as cross-project.
