# 12 — Glossary

| Term | Meaning | Status | Related |
|---|---|---|---|
| **JARVIS Engineering Intelligence → Icarus** | Original name (local CLI, v0) → product name from 2026-06-27. Reason for "Icarus": `UNKNOWN` (no record found) | renamed | `jarvis-v0` tag |
| Brain / Face | Cloud pipeline (retrieval, writer, gate) / clients (Mac app, extension, web, MCP) | current | — |
| Honesty gate | `evals/gate.py`; deterministic; guards (a) groundedness, (b) rationale, (c) entity-presence | current | cite-or-abstain |
| Cite-or-abstain / cite-or-unknown | Writer must cite retrieved evidence or answer "unknown" | current | — |
| "No one wrote this down" | The user-facing honest unknown | current | abstention |
| Trust interlock | `evals/trust.py`; refuses non-`private_safe` providers | current | gemini-paid |
| gemini-paid | The single production writer (billing-enabled Gemini) | current | one model |
| Eval board / frozen corpus | Labelled questions over `simonw/llm @ 94769b8` | current | Phase 1 |
| Brick | A scoped unit of build work (Brick A–G, 0, Q, S, D...) | current | plans |
| Red → green | Prove gap with a failing eval before fixing | current | WORKFLOWS |
| alpha-1…6 | Tester release tags Jul 14 – Aug 10 | historical | — |
| Launch canary | Final-user limited production cohort + isolated infra (infra deleted 09-10) | partly abandoned | `docs/LAUNCH_CANARY.md` |
| Agent Mode | Icarus for coding agents via MCP; later the capture/confirmation loop for novice builders | current | MCP |
| `get_change_context` / `explain_code_context` / `get_task_context` | MCP read tools (ask / explain lines / structured task context) | current | `/ask`, `/explain`, `/context` |
| `record_decision_candidate` / `record_no_decision` | MCP capture tools called once per turn | current | decision ledger |
| Authority ladder | agent recommendation → human-confirmed PR proposal → merged + indexed truth | current | 2026-08-29 decision |
| Memory Gap | An honest unknown turned into a reviewable PR proposal | current | engineering memory loop |
| `rejected_attempts` / `unlanded_prs` | Closed-unmerged PRs / anything not shown landed | current | `evals/attempts.py` |
| `rests_on_unlanded` (was `rests_on_rejected`) | Per-claim flag: nothing cited shows the change landed | renamed 2026-08-14 | — |
| `rests_on_deferred` | Claim rests on a deferral later merged work may have overtaken | current | temporal check |
| Successor check / probe | Drop a closed PR a merged PR says it replaces; probe n+1..n+3 | current | pr:23→pr:24 |
| Per-claim self-report | Writer labels sentences quoted/composed/unsupported (advisory) | current | attribution (deleted) |
| Investigation engine | Bounded loop over retrieve/inspect/trace/compare/verify | current | `/investigate` |
| Repo map / structure / freshness / visits | Writer-free "speaks first" features | current | Era 8 |
| PROTOCOL.md | One rule per experiment failure that actually happened | current | experiments |
| C2 | Tool-description experiment; 4/4 retracted to 1/4 | corrected | — |
| Matched pair | world-model-mcp (live) vs coding-agent-memory-benchmark (null) | done | — |
| History-failure pilot | Preregistered paired with/without-Icarus trial, n=23 | paused | — |
| ICARUS.md | Repo's own non-derivable context file, `last-verified-against` stamp, no privilege | current | — |
| Vault | `~/Documents/Obsidian Vault/Icarus/`, the thinking layer | current | Work Queue |
| Work Queue | Vault note: what must be done, gates, DoD | current | HANDOFF (stale) |
| Ponytail | Leanness discipline/skill; "ponytail audit" trimmed dead fields | current | — |
| Honest Brutalism | Design language for the app | current | `docs/DESIGN_VISION.md` |
| Read the Repo | Sept content franchise: one recognizable repo, one "why", cited answer + honest unknown | current | carousels |
| Reply-guy | Distribution by genuine replies on X/Reddit/HN | current | 50-user push |
| Barter (Harshitha) | Build her meta-ads tool ↔ she markets Icarus | unknown outcome | — |
| try-icarus.vercel.app | Canonical site URL (earlier `icarus-website-kappa`) | current | — |
| Organisation brain | Team-shared index beyond one repo | parked | multi-repo |
