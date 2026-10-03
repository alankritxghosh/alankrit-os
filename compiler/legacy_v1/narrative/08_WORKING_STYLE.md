# 08 — Working Style Model

> Authored narrative, copied by `python compiler/run.py`. Refs resolve via `compiler/validate.py`.
> **STABLE** = evidenced on several surfaces (code, content, outreach, agent instructions) or stated by him as a rule.
> **PROJECT** = observed only as an Icarus-specific practice. Stability across projects is untestable here.

| area | observed behavior | stable or project | conf | refs |
|---|---|---|---|---|
| **Tools** | Claude Code is the engineering team (builder, auditor); Codex as independent reviewer and parallel builder; custom agents (adversarial architect reviewer, test writer). Content skills installed (voice-dna, anti-ai-writing, viral-hooks, ponytail, playbooks). Obsidian vault = thinking layer; git = truth. | STABLE (agents-as-team); PROJECT (specific tools) | H | [icarus:X05L1] [icarus:X05L2] [icarus:X05L3] |
| **Coding** | Delegates nearly all code. Directs: stdlib-first, lazy imports, fail-safe defaults, three-valued state, language-specific resolvers, tests watched failing, leanness audits. | STABLE as standards he gives agents; PROJECT as stack | H | [icarus:X11L2] [icarus:B16] [icarus:B17] |
| **Automation** | Automates deploy (GitLab CI with a manual gate), releases, outreach batches (weekly YC prospect automation, later retired), experiments run headless. Never auto-deploys the brain; never auto-merges memory. | PROJECT; the human gate is STABLE | H | [icarus:X05L9] [icarus:F38] [icarus:D17] |
| **Research** | Reverse-engineers comparables and playbooks; marks confidence per claim. | STABLE (seen in engineering, distribution, job search) | H | [icarus:R6] [icarus:X11L11] |
| **Planning** | Brick-by-brick plans in `docs/plans/` with red→green TDD tasks; dated checkpoints; abort rules; Work Queue with gates and definitions of done. | PROJECT form, STABLE habit | H | [icarus:X05L7] [icarus:R14] |
| **Execution** | Long, intense sessions, sometimes overnight; several deploys a day at peak (4 on 2026-07-18). 585 commits in about 10 weeks. | PROJECT (single period) | M | [icarus:X00L8] |
| **Delegation** | Agents write code, draft outreach and technical replies; he keeps decisions, taste and public voice, writes his own reflective posts, approves every external claim. Explicit "do not do X unless…" gates in agent instructions. | STABLE | H | [icarus:X11L9] [icarus:X11L5] |
| **Documentation** | Extremely heavy, on purpose: decision records with reasons, Learning entries with costs, indexes verified by CI, `last-verified-against` stamps, a 7,269-line HANDOFF. Summary docs drift (HANDOFF stale from 08-11; STRATEGY outdated). | STABLE habit; drift is RECURRING | H | [icarus:X05L6] [icarus:B20] [global:GC07] |
| **Iteration** | Ships, tries, reverses within days when output disappoints by measurement or taste. | STABLE | H | [icarus:X11L6] [global:DP01] |
| **Preferred detail level** | Thinks in product scenes and trust boundaries; drops into detail exactly where trust is at stake (gate wording, credential paths). | INFERRED, M-H | M-H | [icarus:R3] |
| **Autonomy given to agents** | High for implementation; zero for confirming intent, merging memory, or making public claims. Agents propose; he confirms. | STABLE | H | [global:DP09] [icarus:B12] |
| **Workflow structure** | Session discipline: read vault Work Queue → plan → work → write back in the same pass, routed by actionability, one home per item. | PROJECT form, STABLE intent ("files are memory") | H | [icarus:X05L5] [icarus:B20] |
| **Bottlenecks** | Distribution; cash; account trust on HN/Reddit; unsigned binary ("malware" warning); unconfirmed decisions; agent quota. | PROJECT (2026) | H | [icarus:O7] [icarus:O19] [icarus:O21] |
| **Recurring frustrations** | Copy that doesn't sound like him; having to repeat the same rule (em-dashes); soulless design; channels returning zero; things breaking silently. | STABLE (multi-surface) | H | [icarus:X01L18] [icarus:X01L19] [icarus:X01L20] [icarus:X01L21] [icarus:X01L22] |
| **Collaboration model** | Multiple AI agents set against each other (Claude builds and audits, Codex reviews); claims kept checkable by the other agent; durable files over chat. | STABLE | H | [icarus:X99L17] [icarus:X99L16] |

## Repeatedly optimized vs repeatedly neglected

- **Optimized (H):** honesty precision, install friction (6 steps → 3), measurement correctness, copy register, visual soul of surfaces.
- **Neglected (M-H):** pricing and ICP (flagged since 2026-07-16), site conversion measurement (dark by choice), keeping summary docs current, confirming queued decisions (45 pending), finishing single-variable channel tests before switching [icarus:O1] [icarus:O2] [icarus:O9] [icarus:O19] [global:GC04].

## Process-to-product ratio (INFERENCE, M-H)

Low tolerance for runtime dependencies; high tolerance for process (35 experiment files, ~580KB vault, 119KB Work Queue). The extractor reads the process overhead as a self-imposed cost. Evidence: drift in the summary docs it was meant to keep current [global:GC07].

## How to work with him (agent-facing, STABLE items only)

1. State assumptions; ask on ambiguity; never claim done without running it; never fabricate names, paths, results or citations; never weaken a test [icarus:X99L15].
2. Write durable outcomes to files in the same session; read the source, not the summary [icarus:X99L16].
3. Keep every claim checkable by another agent; show the evidence for every number [icarus:B07].
4. Separate fact / recommendation / confirmed decision / unknown in what you hand him [icarus:X11L24].
5. Do not draft his reflective posts from scratch; tighten his words [icarus:X11L9].
