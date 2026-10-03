# 01 — Project Timeline: Alankrit OS

All events are on 2026-10-03; times are IST (UTC+5:30), taken from session timestamps (UTC) and file mtimes. Source keys are in 00.

| # | time (IST) | event | what changed | why | evidence | consequence | status |
|---|---|---|---|---|---|---|---|
| E01 | before 18:48 | The name "Alankrit OS" exists as a target system | A named destination for persistent context | `UNKNOWN`; never explained | S-v1 §20 requires `HANDOFF_TO_ALANKRIT_OS.md` | Every extraction ends in a handoff addressed to it | CURRENT |
| E02 | 10:09 and 18:30 (adjacent, not this project) | Scheduled headless Icarus agents run: Work Queue status; Gmail outreach sync into Obsidian | — | Icarus operations | sessions c608e01f, a1a7ec67 | Shows he already runs unattended agents | excluded from scope |
| E03 | 18:48 | v1 extraction protocol submitted in the Icarus repo session | Start of the extraction pipeline | Make project context persist "into my future AI systems" (S-v1) | S-v1 | Icarus extraction | HISTORICAL (superseded by v2) |
| E04 | 18:50–18:56 | Icarus extraction written, flat at the `context-extraction/` root (16 files) | First corpus | — | X-icarus mtimes | The only corpus the compiler had | MOVED to `icarus/` at E10 |
| E05 | 19:08 | Folder `/Users/alankritghosh/Alankrit OS ` created | Separate compiler workspace | S-comp: "current working directory is the OUTPUT / COMPILER WORKSPACE" | dir mtime | Read-only separation of corpus and compiler | CURRENT |
| E06 | 19:19 | Global Context Compiler prompt submitted (session 9d6810ae) | Second stage defined; consumer named as a "multi-agent personal-brand system" | Build one coherent global layer from many project extractions | S-comp | Compiler built | CURRENT spec |
| E07 | 19:22–19:37 | Assistant builds and runs the compiler: 11 Python modules, curated overlay, 6 narrative docs, 17 generated docs, 11 JSONL files, 557 graph edges; validation 18 PASS / 2 WARN | Global layer v0 | — | W mtimes; `16_VALIDATION_REPORT.md` | Found that the corpus held only one project | CURRENT, stale on project count (C05) |
| E08 | 19:37 | Assistant reports: "cross-project" impossible; recommends extracting other projects into subfolders, each with its own manifest | Diagnosis | Single flat corpus | session transcript (assistant turn) | Likely input to v2 (INFERRED) | — |
| E09 | 21:41 | v2 protocol submitted | Per-slug output folders; `archive/` before overwrite; ALANKRIT/ASSISTANT/UNKNOWN labels; source priority ranking; 04_BELIEF_EVOLUTION and 12_ALANKRIT_CONTEXT as separate files; failures split from lessons; glossary dropped | `INFERRED` MEDIUM-HIGH: answers the compiler's findings (see BT01–BT02) | S-v2 | This extraction | CURRENT spec |
| E10 | 21:42 | Alankrit selects "Alankrit OS itself" as the project, and "Yes, move into icarus/" | Scope chosen, despite the circularity warning | Not stated | S-ans | This file set; Icarus re-homed | — |
| E11 | ~21:45 | First move attempt fails silently (zsh does not word-split); hash check passes on empty values; delete step fails harmlessly | — | Assistant error | session transcript | Caught on reading the output; nothing was lost | FIXED (F07) |
| E12 | ~21:46 | Icarus moved byte-for-byte (sha256 verified) into `icarus/`; original kept in `archive/2026-10-03T2145_flat-root-icarus-extraction/` | Layout now v2-compliant; content still v1 schema | v2 layout + S-ans | `find` listing; ARCHIVE_NOTE.md | Compiler must read per-slug folders | CURRENT |
| E13 | ~21:50–22:30 | This extraction written to `context-extraction/alankrit-os/` | Second project in the corpus | S-v2 | this folder | Global compile needs a rerun (O06) | CURRENT |

## Phases

1. **Extraction-only** (18:48–19:08). One protocol, one project, flat output.
2. **Global compile v0** (19:08–19:37). Two-stage architecture; the gap between "global" and a single-project corpus became visible.
3. **Protocol v2 and re-homing** (21:41–). Namespaced, archived, authorship-aware. The pipeline starts extracting itself.

Gap: 19:37–21:41 has no recorded activity in this project.
