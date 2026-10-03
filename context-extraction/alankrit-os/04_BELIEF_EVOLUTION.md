# 04 — Belief Evolution: Alankrit OS

The changes here happened within about three hours on 2026-10-03, across three protocol versions (S-v1 18:48 → S-comp 19:19 → S-v2 21:41 IST).
They are changes in **what he required**. Whether each reflects a changed belief or a refined spec is marked per item. Causes are `INFERRED` unless stated; he never explained a change.

## BT01 — How project context should be laid out

```text
EARLIER POSITION     One flat output directory per run: "Produce the following files in a new directory:" followed by a flat context-extraction/ tree (S-v1 §19)
        ↓
OBSERVATION          The compiler found the corpus held exactly one flat project; "cross-project" claims were impossible.
                     It recommended "extract the other projects into subfolders of the source, each with its own
                     extraction_manifest.json" (assistant report, 19:37)
        ↓
RECONSIDERATION      (not recorded)
        ↓
NEW POSITION         context-extraction/<PROJECT_SLUG>/; inspect before overwriting; archive/ when material changes (S-v2)
        ↓
CURRENT STATUS       CURRENT. Icarus re-homed (D12–D13). Spec refinement, not a belief change. Cause: INFERRED, MEDIUM-HIGH.
```

## BT02 — Whose words count as his voice

```text
EARLIER POSITION     "Extract actual representative examples where useful" with no authorship rule (S-v1 §7)
        ↓
OBSERVATION          The compiler split voice evidence into POSTED / HIS_FEEDBACK / DOC_PHRASE / AI_HOUSE_STYLE.
                     It noted that commit messages were "written by AI agents under his direction; NOT his direct voice"
        ↓
RECONSIDERATION      (not recorded)
        ↓
NEW POSITION         Every example labelled ALANKRIT / ASSISTANT / UNKNOWN; "Never attribute text to Alankrit unless the
                     source establishes that he wrote it." (S-v2 Step 9; Rule 8)
        ↓
CURRENT STATUS       CURRENT. Looks like a real belief change: authorship moved from implicit to required. INFERRED, MEDIUM.
```

## BT03 — Failures vs lessons

```text
EARLIER POSITION     Failures and lessons in one section, with "what was learned" a field of each failure (S-v1 §9)
        ↓
OBSERVATION          S-comp asked to "Explicitly identify recurring lessons. These may be more valuable than successful outcomes."
                     The compiler produced recurring-lesson clusters across failures
        ↓
NEW POSITION         "Separate lessons from failures"; label EXPLICIT vs INFERRED; failures.jsonl separate from lessons.jsonl (S-v2 Steps 10–11, 17)
        ↓
CURRENT STATUS       CURRENT. The weight on lessons grew across all three versions.
```

## BT04 — Belief change as its own artifact

```text
EARLIER POSITION     Evolution handled inside "CONTRADICTIONS AND EVOLUTION" (S-v1 §11) and the strategic-evolution phases (§14)
        ↓
NEW POSITION         A dedicated document (S-comp Phase 7 → S-v2 Step 5, 04_BELIEF_EVOLUTION.md) with a fixed
                     EARLIER → OBSERVATION → RECONSIDERATION → NEW → STATUS chain; "Do not erase the earlier position."
        ↓
CURRENT STATUS       CURRENT. Evolution moved from a side-effect of contradiction-hunting to a primary output.
```

## BT05 — How contradictions are classified

```text
EARLIER POSITION     Binary: "intentional evolution or unresolved inconsistency" (S-v1 §11)
        ↓
NEW POSITION         UNRESOLVED / EXPLAINED BY TIME / DOCUMENTATION ERROR / EVIDENCE CONFLICT / UNKNOWN (S-v2 Step 13)
        ↓
CURRENT STATUS       CURRENT. A finer vocabulary for uncertainty; consistent with B15.
```

## BT06 — How sources are ranked

```text
EARLIER POSITION     "Prefer primary evidence over interpretation." (S-v1 constraint 7)
        ↓
NEW POSITION         Explicit 7-level priority; "Direct statements by Alankrit" first, "Inference" last (S-v2 SOURCE PRIORITY)
        ↓
CURRENT STATUS       CURRENT. Puts his own words above the code and docs that agents wrote for him.
```

## BT07 — The extraction folder's role

```text
EARLIER POSITION     context-extraction/ is the SOURCE CORPUS: "Treat the source corpus as READ-ONLY." (S-comp)
        ↓
NEW POSITION         context-extraction/<slug>/ is the write target for extractions (S-v2 ABSOLUTE OUTPUT LOCATION)
        ↓
CURRENT STATUS       Role-based, not a reversal: the compiler reads it, extractors write it. EXPLAINED BY TIME (C01).
```

## BT08 — Glossary

```text
EARLIER POSITION     Glossary required, incl. "old name → new name → reason" (S-v1 §8; Icarus has 12_GLOSSARY.md)
        ↓
NEW POSITION         No glossary in the v2 output contract
        ↓
CURRENT STATUS       UNKNOWN whether deliberate. Creates schema drift between projects (C09).
```

## BT09 — Voice and person of the request (observation, not a belief)

S-v1 is in the first person ("What I, Alankrit, was trying to accomplish") with 0 em-dashes. S-comp and S-v2 are in the third person ("for Alankrit Ghosh") with 23 and 21 em-dashes. This changes the evidence about who drafted them, not what he believes. Recorded in C02 and C03.
