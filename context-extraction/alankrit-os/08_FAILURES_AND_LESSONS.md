# 08 — Failures and Lessons: Alankrit OS

Not sanitized. "Owner" says whose action failed. Most failures here are the ASSISTANT's, made while building for him. They are kept because they show which failure classes his pipeline is exposed to.

## Failures

| ID | attempted | what happened | why | learned | changed afterwards | reappeared later? | owner |
|---|---|---|---|---|---|---|---|
| F01 | A global, cross-project context layer from the extraction corpus | Corpus held one project, flat at the root; no cross-project claim could be supported; every "recurring" pattern had to be relabelled "cross-domain within one project" | v1 extracted only the project it ran in; other projects were "deliberately out of scope" (Icarus manifest) | A global layer needs several independent, namespaced extractions | v2 per-slug folders (BT01); Icarus re-homed | Partly: the second project is this meta-project, not an independent one | design (ALANKRIT spec) + scope |
| F02 | Use the Icarus extraction as primary evidence | Its own manifest: 0 session transcripts, ~40% of Learning.md, the top of a 7,269-line HANDOFF; evidence ends 2026-09-10 | Extraction time and scope | Extractions are second-hand; mark them so | Compiler flags secondary-hand evidence | Open (Icarus not re-extracted) | extraction run |
| F03 | Parse 35 beliefs and 18 reasoning patterns | First parse returned 18 beliefs and 16 patterns, with no error | Bold titles wrapping across lines didn't match the regex | **Compare parse yield to the manifest's declared counts**; a silent drop looks like clean output | Fixed; inventory now prints parsed vs declared | Same class as Icarus F06 ("silently read 1/4 of each code window") | ASSISTANT |
| F04 | Global IDs `<project>:<local_id>` | Bullet IDs (`X09`) and FACT IDs repeated across files and would have silently overwritten each other in the record index | IDs scoped to the line, not the file | Namespace IDs by file | Fixed (`X11L8`, `FACT01L32`) | — | ASSISTANT |
| F05 | Verify voice excerpts verbatim | 9 of 35 flagged unverified | Off-by-one in the wrapped-line fallback | — | Fixed | — | ASSISTANT |
| F06 | Check that quotes in narrative docs exist in the corpus | Apostrophes were paired as quotation marks (false warnings); one real paraphrase was found inside quote marks ("Business, not engineering") | Regex re-scan pairing | Paraphrase in quotation marks is a hallucination vector | Sequential pairing; quote corrected to the corpus wording | — | ASSISTANT |
| F07 | Move the Icarus extraction with hash verification | Every `cp` failed (zsh does not word-split `$FILES`); the hash check **passed** because both sides were empty; `rm` failed harmlessly | Unquoted list in zsh; verification compared two failures as equal | **A check that cannot fail is not a check**; verify non-empty | Redone in Python with per-file sha256 + non-empty size check | Same class as Icarus "Vacuous tests" (F07) and B17 "A test you haven't watched fail is a test you haven't written." | ASSISTANT |
| F08 | Global narrative docs describing the corpus | They hardcode "ONE project"; stale the moment `alankrit-os/` was created | Counts written as prose, not generated | Generate counts; never hand-write them | Pending recompile (O06) | Same class as Icarus doc drift (HANDOFF/STRATEGY) | ASSISTANT |
| F09 | Extract Alankrit OS itself | Most material is assistant-generated or derived from Icarus → circular evidence; risk of double-counting in the next global compile | Project is one day old and meta | Derived claims must be tagged and excluded from frequency counts | `DERIVED_FROM_ICARUS` tags in memory/ | Open until the compiler honors the tag (O06) | scope choice (ALANKRIT, warned) |
| F10 | Treat the compiled "current state" as current | Upstream evidence is 23 days old; no refresh mechanism exists | Extraction is a one-shot snapshot | Context needs an as-of date and a refresh cadence | "Current" is labelled "as of 2026-09-10" everywhere | Open (O08) | design |

## Rejected or abandoned ideas

- Fully model-generated global docs (rejected by the ASSISTANT: unverifiable; D08).
- Claiming cross-project persistence from a single project (rejected; D09).
- Leaving Icarus flat at the root (abandoned by D12).
- Glossary as a required artifact (dropped in v2; reason UNKNOWN; BT08).

## Lessons

| ID | lesson | label | scope | source |
|---|---|---|---|---|
| L01 | Failures and rejected ideas may be more valuable context than successes. | EXPLICIT (directive) | STRATEGIC PRINCIPLE | S-comp Phase 13; S-v2 Step 10 |
| L02 | Never let the latest statement overwrite the historical record. | EXPLICIT (directive) | STRATEGIC PRINCIPLE | S-comp; S-v2 Rule 6 |
| L03 | A global context layer needs multiple independent, namespaced extractions. | INFERRED (F01 → BT01) | PROJECT-SPECIFIC → reusable | F01 |
| L04 | Compare yields to declared counts; silent drops read as success. | INFERRED (assistant) | TECHNICAL KNOWLEDGE | F03 |
| L05 | A verification step that cannot fail is not verification. | INFERRED (assistant) | TECHNICAL KNOWLEDGE | F07 |
| L06 | Counts in prose go stale; generate them. | INFERRED | TECHNICAL KNOWLEDGE | F08 |
| L07 | Label authorship before modelling voice. | INFERRED (BT02) | STRATEGIC PRINCIPLE | BT02 |
| L08 | Meta-extractions must tag derived claims so evidence isn't counted twice. | INFERRED | TECHNICAL KNOWLEDGE | F09 |
| L09 | Validated is not verified: a compiler can pass every check on judgments nobody reviewed. | INFERRED | STRATEGIC PRINCIPLE | C10; echoes Icarus B02 "Groundedness ≠ relevance ≠ truth" |

## Cross-project signal (the most useful finding here)

The failure classes in the Icarus record appeared again in this pipeline within hours, in work done for him by an agent. They are silent drops, vacuous checks and drifting prose. Icarus's own line applies: "Knowing a failure mode is not the same as designing against it." Agents building Alankrit OS should design against these classes from the start.
