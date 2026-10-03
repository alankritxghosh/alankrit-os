# 06 — Working Style: Alankrit OS

`PROJECT-SPECIFIC BEHAVIOR` = seen only here. `LIKELY PERSONAL PREFERENCE` = seen here **and** independently in the Icarus record (two projects). Nothing seen once is generalized.

| area | observation | classification | conf | evidence |
|---|---|---|---|---|
| Delegation | Hands an entire multi-phase job to an agent in one pasted protocol; the agent plans, builds, validates and reports | LIKELY PERSONAL PREFERENCE | HIGH | S-v1, S-comp, S-v2; Icarus: "Delegates nearly all code to agents; keeps decisions, taste and public voice" |
| Interaction density | 3 messages + 2 selections over ~3h 25m (18:48 → 21:42 IST); no mid-run steering recorded | PROJECT-SPECIFIC (one day) | HIGH as fact | session timestamps |
| Tools | Claude Code (desktop app, Code tab); separate sessions per folder (JARVIS repo, Alankrit OS); Obsidian vault attached as an extra working directory | LIKELY PERSONAL PREFERENCE (Claude Code); PROJECT-SPECIFIC (layout) | HIGH | session paths; environment |
| Automation | Scheduled headless agents run status and sync jobs for Icarus on the same day | LIKELY PERSONAL PREFERENCE (also in Icarus: weekly YC prospect automation, CI) | MEDIUM | sessions c608e01f, a1a7ec67 |
| Documentation | Everything durable is a file: numbered md docs, manifests, JSONL, handoffs | LIKELY PERSONAL PREFERENCE | HIGH | outputs; Icarus B20 |
| Planning | Specifies outputs exhaustively up front (file trees, JSON schemas, field lists) | LIKELY PERSONAL PREFERENCE | MEDIUM-HIGH | protocols; Icarus brick plans |
| Version control | Alankrit OS is not a git repo (Icarus: 585 commits) | PROJECT-SPECIFIC (day 1) | HIGH as fact | `git status` fails |
| Research | None observed in this project | — | — | — |
| Experimentation / debugging | No direct involvement; validation delegated to the compiler's own checks | PROJECT-SPECIFIC | MEDIUM | W `validate.py` |
| Desired autonomy | High: no approvals requested, none given except two multiple-choice answers | LIKELY PERSONAL PREFERENCE | MEDIUM | S-ans; Icarus long autonomous sessions |
| Preferred detail level | Very high detail in specs; wants outputs both dense (handoff) and exhaustive (registers) | PROJECT-SPECIFIC | MEDIUM | S-comp "This should be dense." and fidelity order |
| Session timing | Evening, IST (18:48–21:42) | PROJECT-SPECIFIC (one day; Icarus also notes evening/overnight sessions) | LOW | timestamps |
| Frustrations | None expressed in this project | — | — | — |
| Bottlenecks | Evidence base (one extracted project); no review step; no git; stale upstream evidence (Icarus to 2026-09-10) | PROJECT-SPECIFIC | HIGH | 09 |

## Implication for agents working on Alankrit OS

Expect long autonomous runs from a single spec, with no mid-course check-ins. Put the outputs where the spec says. Surface anything ambiguous with one compact multiple-choice question, which he answered within a minute here. Leave unreviewed outputs marked unreviewed.
