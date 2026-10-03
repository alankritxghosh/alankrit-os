# 11 — Transferable Context: Alankrit OS

"Two-project" means the item is also evidenced independently in the Icarus extraction. Nothing seen in one project is promoted to a personal preference.

## PROJECT-SPECIFIC
- Folder `/Users/alankritghosh/Alankrit OS ` (trailing space), not a git repo; compiler at `compiler/run.py`; overlay `compiler/curated.py` (Icarus-only).
- Output layout `context-extraction/<slug>/`; archive at `context-extraction/archive/<timestamp>_<reason>/`.
- Session IDs: ee20c209 (v1 run, JARVIS folder), 9d6810ae (compiler + v2 run, Alankrit OS folder).
- `DERIVED_FROM_ICARUS` tagging convention (D14).

## TECHNICAL KNOWLEDGE
- Parse yield must be checked against declared counts; wrapped markdown bold titles break line-based regexes (F03).
- Namespace record IDs by project **and file** (F04).
- In zsh, an unquoted `$VAR` list is not word-split. A loop over it runs once with the whole string (F07).
- Hash verification must reject empty or missing inputs; equal empty hashes are not a match (F07).
- Quote verification must pair quote marks sequentially per line; apostrophes are not delimiters (F06).
- Generate counts in docs from data; never hand-write them (F08).
- Claude Code session transcripts live at `~/.claude/projects/<path-slug>/<session>.jsonl`; user turns carry UTC timestamps (IST = +5:30).

## PRODUCT KNOWLEDGE
- A context layer for agents needs both a dense first-read handoff and full registers with provenance (D07, C08).
- Explicit status vocabularies (CURRENT…UNCERTAIN; ALANKRIT/ASSISTANT/UNKNOWN) make uncertainty machine-usable (R03).
- Meta-projects create circular evidence; tag derived claims (F09).

## BUSINESS KNOWLEDGE
- None evidenced in this project.

## STRATEGIC PRINCIPLE (stated by him as directives; two-project where noted)
- Never present inference as fact; never invent (B01). **Two-project.**
- Surface contradictions; never reconcile them silently (B04). **Two-project.**
- Every important claim traceable (B06). **Two-project.**
- Preserve history; recency is not truth; changed minds are context (B03).
- Failures may be worth more than successes as context (B05, L01).
- Project choices are not personality traits; frequency is not importance (B07).

## LIKELY PERSONAL PREFERENCE (two-project evidence)
- Delegates whole jobs to AI agents through long written specs; keeps decisions for himself (06; Icarus 05).
- Durable files over chat as memory (B10; Icarus B20).
- Unknowns as explicit states (B15; Icarus B03).
- Uses Claude Code as the primary agent; runs scheduled headless agents (06).

## UNCERTAIN / INSUFFICIENT EVIDENCE
- Whether he drafts his own protocols (C02, C03, O04).
- Whether the personal-brand system will publish autonomously (H1).
- Fast option selection as a general trait (R07, n=2).
- Treating the pipeline as its own subject (R08, n=1).
- Evening work rhythm (one day).
