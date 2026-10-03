# 05 — Reasoning Patterns: Alankrit OS

Evidence is thin: three submitted protocols, two selections, timestamps. Every pattern is `INFERRED`. Confidence is capped at MEDIUM unless the Icarus record independently shows the same behavior ("echo"). No psychological claims.

| ID | pattern | evidence in this project | echo in Icarus extraction | conf |
|---|---|---|---|---|
| R01 | **Starts from the end consumer and works back to the data layer.** Agents that will act for him → a handoff they read first → memory/graph → per-project extraction. | S-comp preamble names the consumer, then Phase 21 defines what it reads first; S-v1 §20 | Icarus R1: vivid scene (JARVIS) → narrowest provable brick | MEDIUM-HIGH |
| R02 | **Puts the quality gate inside the request.** Each protocol ends with a self-test the agent must pass ("If the answer is no, continue investigating."; "If not, continue synthesis."; v2 Step 21 checklist). | S-v1 QUALITY TEST; S-comp FINAL QUALITY TEST; S-v2 Step 21 | Icarus R2: defines the failure before the feature | MEDIUM-HIGH |
| R03 | **Encodes epistemics as explicit vocabularies** (fact/belief/inference labels; seven belief statuses; five contradiction statuses; three author labels) rather than trusting judgment. | D03, BT05, BT02 | Icarus: three-valued state; deterministic gate over model judgment (B03, B04) | HIGH |
| R04 | **Separates layers with one-way flow and read-only sources** (project → extraction → compiler → consumer). | D02, D04 | Icarus brain/face split; repo = truth, vault = thinking | MEDIUM-HIGH |
| R05 | **Revises the spec quickly after seeing output.** v1 → v2 in 2h53m, with the compile and its findings in between. | E03–E09 | Icarus R5: reverses quickly, records the reversal | MEDIUM |
| R06 | **Breadth before depth across projects.** Designs a universal protocol and a global compiler before a second project is extracted. | timeline: global compile built with one project in the corpus | Icarus R12: broadens scope where feedback is weak (distribution) | MEDIUM (counter: v1 was run on one project first) |
| R07 | **Chooses fast among presented options.** Two answers within ~40 seconds of the question; took the recommended default on Q2 and overrode the circularity framing on Q1. | S-ans timestamps (question → answer at 16:12:00Z) | Icarus: "Decides fast, records the reason" | LOW-MEDIUM (n=2) |
| R08 | **Treats the pipeline itself as an object of the pipeline** (extract Alankrit OS with the protocol it built). | D11 | — | LOW (n=1, reason unstated) |

## How he handled uncertainty / failure here

- Uncertainty is pushed into labels and statuses (R03), not resolved by asking. No clarifying question from him appears in the record.
- No failure attributable to his own decisions appears yet. The project's failures are the assistant's (08).

## What persuades him (this project)

Unknown. He gave no feedback on the compiler's output in this record. v2's contents are the only signal (BT01–BT02), and the link is inferred.
