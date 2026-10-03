# 10 — Contradictions: Alankrit OS

Statuses: UNRESOLVED · EXPLAINED BY TIME · DOCUMENTATION ERROR · EVIDENCE CONFLICT · UNKNOWN. None is silently reconciled.

| ID | position A | position B | date A | date B | evidence | possible explanation | status |
|---|---|---|---|---|---|---|---|
| C01 | The extraction folder is a READ-ONLY source corpus; the compiler "should never write into that source directory" | Extractions are written into `context-extraction/<slug>/` | 19:19 | 21:41 | S-comp; S-v2 | Different roles: the compiler only reads, extractors write | EXPLAINED BY TIME |
| C02 | His hard voice rule: no em-dashes, ever | The compiler prompt and v2 protocol he submitted contain 23 and 21 em-dashes; v1 contains 0 | rule recorded by 2026-08 (Icarus) | 19:19, 21:41 | `icarus/06_VOICE_PROFILE.md`; counts over the session texts | Prompts drafted with an AI; or the rule covers only text in his public voice | UNKNOWN |
| C03 | v1 written as him ("What I, Alankrit…", "Do not psychoanalyze me.") | Later versions written about him ("for Alankrit Ghosh", "he") | 18:48 | 19:19, 21:41 | S-v1; S-comp; S-v2 | Different drafter or template; intent unchanged | UNKNOWN |
| C04 | "Never attribute text to Alankrit unless the source establishes that he wrote it." | The protocols define his beliefs and priorities, yet their authorship is unestablished | 21:41 | — | S-v2 Step 9 | Treated as his *directives* (he submitted them), not his *words* | EVIDENCE CONFLICT (handled by labelling) |
| C05 | Global docs: corpus = "ONE project extraction" | `context-extraction/` now holds `icarus/` and `alankrit-os/` | 19:37 | ~21:50 | W `HANDOFF_TO_ALANKRIT_OS.md`; folder listing | Docs predate the second extraction | DOCUMENTATION ERROR (pending recompile) |
| C06 | v1 required a glossary with renames | v2 contract has no glossary | 18:48 | 21:41 | S-v1 §8; S-v2 contract | Possibly folded into other files | UNKNOWN |
| C07 | Pipeline: "Do not sanitize failures"; failures are core context fed to a personal-brand system | Icarus B26: never showcase his own failures or zeros publicly | 19:19 / 21:41 | 2026-08-17 | S-comp; S-v2 Step 10; `icarus/03_BELIEF_SYSTEM.md` B26 | Private memory vs public output; the boundary is not written down | UNRESOLVED (HIGH risk for a publishing agent) |
| C08 | Optimize fidelity over brevity | The handoff must be "substantially smaller than the full corpus" | 19:19 | 19:19 | S-comp | Layered outputs: dense handoff over full registers | EXPLAINED (not a real conflict) |
| C09 | Icarus extraction uses the v1 schema | Alankrit OS uses the v2 schema | 18:50 | 21:50 | folder contents | Protocol changed between runs | UNRESOLVED (schema drift; O05) |
| C10 | Compiler validation: 18 PASS | The judgments it validates (statuses, transitions, classifications) were made by the assistant and never reviewed by him | 19:37 | — | W `16_VALIDATION_REPORT.md`; `curated.py` | Validation checks traceability, not truth | UNRESOLVED |
| C11 | "Extract the current project… investigate deeply" (source code, git, docs) | The current project has no git, one day of history, and mostly assistant-made files | 21:41 | 21:42 | S-v2; D11 | He chose the project knowing this | EXPLAINED (scope accepted) |
