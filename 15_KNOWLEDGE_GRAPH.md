# 15 — Global Knowledge Graph

109 edges from 4 extractions (`memory/relationships.jsonl`). Edges are exactly as the extractions recorded them; this compiler adds none.

| relation | count |
|---|---|
| caused | 5 |
| consumed_by | 1 |
| contradicted | 10 |
| derived_from | 10 |
| echoed_in | 1 |
| echoes | 9 |
| influenced | 1 |
| led_to | 23 |
| related_to | 32 |
| reversed | 1 |
| superseded | 1 |
| superseded_by | 5 |
| supported | 9 |
| supported_by | 1 |

## Cross-project edges (29)

| id | from | relation | to | basis |
|---|---|---|---|---|
| alankrit-os:REL032 | alankrit-os:B01 | echoes | icarus:B01 | INFERRED (cross-project) |
| alankrit-os:REL033 | alankrit-os:B04 | echoes | icarus:R16 | INFERRED (cross-project) |
| alankrit-os:REL034 | alankrit-os:B06 | echoes | icarus:B01 | INFERRED (cross-project) |
| alankrit-os:REL035 | alankrit-os:B15 | echoes | icarus:B03 | INFERRED (cross-project) |
| alankrit-os:REL036 | alankrit-os:B10 | echoes | icarus:B20 | INFERRED (cross-project) |
| alankrit-os:REL037 | alankrit-os:F03 | echoes | icarus:F06 | INFERRED (cross-project) |
| alankrit-os:REL038 | alankrit-os:F07 | echoes | icarus:F07 | INFERRED (cross-project) |
| alankrit-os:REL039 | alankrit-os:F07 | echoes | icarus:B17 | INFERRED (cross-project) |
| alankrit-os:REL040 | alankrit-os:F08 | echoes | icarus:C03 | INFERRED (cross-project) |
| alankrit-os:REL041 | alankrit-os:C07 | contradicted | icarus:B26 | INFERRED (cross-project) |
| alankrit-os:REL042 | alankrit-os:B11 | related_to | icarus:E47 | INFERRED (cross-project) |
| alankrit-os:REL043 | alankrit-os:PROJECT | derived_from | project:icarus | INFERRED (cross-project) |
| campus-fund:REL001 | campus-fund:C01 | contradicted | personal-brand:D07 | INFERRED |
| campus-fund:REL002 | campus-fund:FA02 | related_to | icarus:D45 | INFERRED |
| icarus:REL049 | icarus:B01 | echoed_in | alankrit-os:B01 | INFERRED (cross-project) |
| icarus:REL050 | icarus:D42 | related_to | alankrit-os:D01 | INFERRED (cross-project) |
| icarus:REL051 | icarus:D46 | related_to | alankrit-os:D05 | INFERRED (cross-project) |
| icarus:REL052 | icarus:F39 | related_to | alankrit-os:F07 | INFERRED (cross-project) |
| icarus:REL053 | icarus:E01 | derived_from | jarvis-v0 | INFERRED (cross-project) |
| icarus:REL054 | icarus:PROJECT | consumed_by | alankrit-os | INFERRED (cross-project) |
| personal-brand:REL001 | personal-brand:D08 | related_to | icarus:O31 | INFERRED |
| personal-brand:REL002 | personal-brand:B04 | contradicted | icarus:B33 | INFERRED |
| personal-brand:REL003 | personal-brand:B05 | superseded | icarus:B26 | INFERRED |
| personal-brand:REL004 | personal-brand:D07 | related_to | icarus:D45 | INFERRED |
| personal-brand:REL005 | personal-brand:D15 | related_to | icarus:D46 | INFERRED |
| personal-brand:REL006 | personal-brand:O06 | related_to | alankrit-os:D05 | INFERRED |
| personal-brand:REL007 | personal-brand:C01 | related_to | alankrit-os:D05 | INFERRED |
| personal-brand:REL008 | personal-brand:D10 | supported_by | icarus:B42 | INFERRED |
| personal-brand:REL009 | personal-brand:F08 | related_to | icarus:F48 | INFERRED |

## Dangling endpoints (0)

Edges pointing at ids that do not exist in any complete extraction. Reported, not fixed.

- none
