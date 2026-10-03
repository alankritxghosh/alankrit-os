# 13 — Knowledge Graph: Alankrit OS

Machine-readable edges: `memory/relationships.jsonl`. Basis per edge: EXPLICIT (stated in a source) / INFERRED.

```text
ALANKRIT OS (project, 2026-10-03, active, not git)
 ├── GOAL: persistent context for future AI systems ............ [D01, EXPLICIT]
 │     └── CONSUMER: multi-agent personal-brand system ......... [D05, EXPLICIT intent; existence UNKNOWN → O02]
 ├── COMPONENTS
 │     ├── extraction protocol v1 (18:48) ──superseded_by──> v2 (21:41)  [D02 → D10]
 │     ├── per-project extractions: icarus/ (v1 schema), alankrit-os/ (v2 schema) [C09]
 │     ├── archive/2026-10-03T2145_flat-root-icarus-extraction  [D12, D13]
 │     └── global compiler (Alankrit OS workspace) ── built_by ── ASSISTANT [D08]
 │            ├── curated overlay (Icarus-only) ── related_to ── O14
 │            └── validator ── contradicted ── validated ≠ verified [C10]
 ├── BELIEFS (directives)
 │     ├── B01 no invention ─────────── echoes ── Icarus B01 "cannot bluff"
 │     ├── B04 contradictions open ──── echoes ── Icarus R16
 │     ├── B06 provenance ───────────── echoes ── Icarus cite-or-abstain gate
 │     ├── B08 authorship labels ────── derived_from ── BT02 (INFERRED)
 │     └── B11 brand system (EXPLORATORY) ── contradicted ── Icarus B26 via C07
 ├── EVOLUTION
 │     ├── BT01 flat → per-slug ──── caused_by (INFERRED) ── F01
 │     ├── BT02 voice → author labels ─ caused_by (INFERRED) ── compiler provenance classes
 │     └── BT03 lessons separated, BT04 evolution file, BT05 statuses, BT06 source ranking
 ├── FAILURES
 │     ├── F01 single-project corpus ──led_to──> D10, D12
 │     ├── F03 silent parse drop ──── echoes ── Icarus F06 (silent 1/4 read)
 │     ├── F07 vacuous hash check ─── echoes ── Icarus F07 (vacuous tests), B17
 │     ├── F08 stale "ONE project" docs ─ echoes ── Icarus doc drift (C3, C4)
 │     └── F09 circular evidence ──led_to──> D14 (DERIVED_FROM_ICARUS)
 ├── PEOPLE
 │     ├── Alankrit Ghosh: requester; decided D01–D07, D10–D12
 │     └── Claude (ASSISTANT): built compiler, D08, D09, D13, D14
 ├── TECHNOLOGIES: Python 3.14 stdlib, Claude Code (desktop), JSONL, Markdown, sha256, zsh
 ├── DATES: 18:48 v1 · 18:50–56 Icarus extraction · 19:08 folder · 19:19 compiler spec · 19:22–37 build · 21:41 v2 · 21:42 choices · ~21:46 move
 ├── OUTCOMES: global layer v0 (18 PASS / 2 WARN) · Icarus re-homed · this extraction
 └── OPEN LOOPS: O01 next projects · O02 brand system · O03 v2 parsing · O04 protocol authorship ·
                 O05 Icarus v2 · O06 recompile · O07 memory contract · O08 freshness · O09 disclosure policy ·
                 O10 git · O11 human review · O12 name/scope · O13 glossary · O14 overlay scale
```

## Cross-project relationships (EXPLICIT unless noted)

```text
ICARUS extraction ──derived_from──> session ee20c209 (v1 protocol)
ALANKRIT OS compiler ──derived_from──> ICARUS extraction (read-only)
ALANKRIT OS ──related_to (INFERRED)──> Icarus goal "maximum visibility around both Icarus and Alankrit personally" (2026-09-08)
ALANKRIT OS ──parallels (INFERRED)──> ICARUS thesis: preserve the "why" behind decisions, for agents
```
