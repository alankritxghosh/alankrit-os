# 10 — Contradictions: Icarus

Statuses: UNRESOLVED · EXPLAINED BY TIME · DOCUMENTATION ERROR · EVIDENCE CONFLICT · UNKNOWN. None is silently reconciled.
C01–C23 continue v1's numbering, re-checked against the transcripts. C24+ are new.

| ID | position A | position B | date A | date B | evidence | possible explanation | status |
|---|---|---|---|---|---|---|---|
| C01 | Vault/product docs: data "discarded after each request" | Audit: corpora and decisions durable until deletion; he ordered the website and repo docs fixed | ≤08-27 | 09-05 | vault:Icarus, Product Philosophy; `S:d58ec7d1@09-05T19:30`, `19:35` | vault never updated | DOCUMENTATION ERROR (vault) |
| C02 | Private storage per user | One shared corpus per private repo | 07-16 | 07-28 | memory; git:5d447c9 | intentional change, stale code comment | EXPLAINED BY TIME |
| C03 | HANDOFF.md is "the one doc kept current" | last updated 08-11; the vault replaced it | — | 08-11 | repo:CLAUDE.md | role moved to the vault | DOCUMENTATION ERROR |
| C04 | STRATEGY.md: line-window chunking | prod runs AST chunking | 06-28 | 07-18 | CLAUDE.md flag | doc lag | DOCUMENTATION ERROR |
| C05 | Three channels only (X, Reddit, HN) | PH + LinkedIn added; HN/PH declared dead | 08-25 | 09-01/04 | D25, D31 | strategy moved on, never formally revised | EXPLAINED BY TIME |
| C06 | "Proof pages are dead" | uptimepage results page made for Artem | 08-17 | 09-09 | D23; `S:2193ef7b@09-09T19:50` ("attach link/image to the results … deploy the page") | a requested deliverable for a warm contact, not a cold pitch | EXPLAINED (scope), not recorded as an exception |
| C07 | "Never showcase failures publicly" | "the evidence is the marketing"; negative-result post ideas; his 09-04 post about feeling he accomplished nothing | 08-17 | 08 / 09-04 | D22; vault:Ideas | feelings ≠ zeros; tool failures ≠ own failures | PARTLY EXPLAINED |
| C08 | 4/4 retired | 4/4 still in the Content Approach note and in X replies he chose to leave up ("let the X replies exist it is fine") | 08-25 | 09-02 / 08-26 | `S:d0f42e64@08-26T13:30` | deliberate: old public replies left standing | UNRESOLVED (strategy note); EXPLAINED (X replies, his call) |
| C09 | No-bluff rule binds him with investors and recruiters; he ordered "Remove this" for "sold it myself to engineering leaders" | Saved DevTools résumé still says "AI developer-tools product sold to engineering leaders" and "cut cloud infrastructure cost ~75%" (25% realized) | 09-10 08:17Z | 09-10 13:49 IST (file) | `S:468c2054@09-10T08:17`; `repo:outputs/resume/Alankrit_Ghosh_Resume_DevTools.md` lines 8, 16 | **v1 attributed this to him; the text is ASSISTANT-drafted**; the removal was incomplete and the agent reported it done | EVIDENCE CONFLICT (corrected from v1's "his overclaim") |
| C10 | Stdlib/minimal dependencies | Next/React/three.js site | — | 08-26 | D29 | scoped to presentation | EXPLAINED BY TIME |
| C11 | Vanilla three.js "vendored, zero external requests" | reversed the next day | 08-26 | 08-27 | vault:DH | — | EXPLAINED BY TIME |
| C12 | **Honesty: "It never bluffs"; abstain when no one wrote it down** | **He demands answers: "there cannot be a no one wrote this down for that, it just does not make sense"; PR 6952 abstention "embarrassing"** | 06-27 → | 07-28, 08-06 | B01, B38 | reconciled in principle ("only what genuinely does not exist gets I don't know"), but recall limits keep producing abstentions on knowable things | UNRESOLVED (product tension) |
| C13 | MCP private repos: fail-closed | deliberately allowed (his call) | ≤08-07 | 08-07 | D18 | — | EXPLAINED BY TIME |
| C14 | Privacy-first product ("never trains on your code", "Absence is not consent") | He demanded on-by-default capture of codebases and questions: "we DONT FUCKING HAVE CUSTOMERS" | always | 08-13 | `S:44a14cb9@08-13T08:01`, `08:11` | pre-customer pragmatism; reversed next day after the Codex P1 | EXPLAINED BY TIME (reversed 08-14) |
| C15 | Target user: buyers → maintainers → individual devs → novices → vibe coders | no written ICP | 06 → 09 | 09-05 | BT03 | still searching | UNRESOLVED |
| C16 | "the priority for the next session is just business decisions" | 309 commits in July, 206 in August; ICP and pricing unwritten | 07-15 | 07–08 | D50 | engineering is where progress was felt | UNRESOLVED |
| C17 | LaunchGeminiProvider.private_safe = True | docstring disclaims contractual attestation | — | 09-05 | audit | unverified terms | UNRESOLVED |
| C18 | "never hero the write-back loop, it never ran end-to-end" | a confirmed decision reached PR #17 on 08-31; 7 decision branches exist | 09-02 | 08-31 | audit E-7; git branches | stale belief | DOCUMENTATION ERROR |
| C19 | memory "public-repo-mvp-direction" (free models, public only) | one paid model, private repos | 06-29 | 07-13/16 | memory | superseded, not deleted | DOCUMENTATION ERROR |
| C20 | HN "one clean shot" | "worth another attempt"; then "dead" | 08-22/25 | 08-25 / 09-04 | vault:HN Launch | — | EXPLAINED BY TIME |
| C21 | Barter for marketing | only his own specific replies ever converted | 08-26 | — | D28 | risk noted at decision time | UNKNOWN (no outcome) |
| C22 | Total coverage ("INDEX A BLOODY REPO COMPLETELY") | caps and exclusions remain (commits, PR/issue limits, .json) | 07-28 / 08-10 | — | B14 | engineering limits | UNRESOLVED |
| C23 | "~10 users" | 50-user goal requires distinct-user counting that may be off (salt) | Work Queue | 09-04 | O10 | unverifiable | UNKNOWN |
| C24 | Self-description: non-technical ("I am not too apt with tech", "without any technical knowledge") | résumé: "Built … ~85,000 lines of Python and Swift" (ASSISTANT-written) | 07-13 / 09-05 | 09-10 | transcripts; résumé | built by directing agents; both true in different senses | EXPLAINED (framing) |
| C25 | Cost discipline ("I cannot afford the azure bill") | chose Azure/Docker and wanted Kubernetes partly "to work and learn complex tech or enterprise grade tech" | 09-10 | 07-29 | D10, B39 | learning motive vs survival constraint | EXPLAINED BY TIME |
| C26 | Revenue before funding (07-15) | Antler pitch pre-revenue (08-24) | 07-15 | 08-24 | B45, D47 | runway pressure | EXPLAINED BY TIME |
| C27 | Pull beats cold push (Content Approach) | LinkedIn connection-note and DM campaign; 40 cold targets in SF/NYC/London/Seattle | 09-02 | 09-04 / 09-10 | D31; `S:2bd25f86@09-10T07:12` | "warm-ish" first touches vs templated cold email | UNRESOLVED (definition) |
| C28 | Visibility for Icarus *and* himself (09-08); 50 Icarus users (09-04) | job search (09-07+); content "more on brand with me than Icarus" (09-13) | 09-04/08 | 09-10/13 | D31, D45, D46 | Icarus may be becoming a portfolio piece; not stated | UNKNOWN |
| C29 | Measurement discipline (pre-register, run cleanly) | "we only have tonight nothing else we HAVE TO FINISH ALL OF THIS TONIGHT" for the pre-registered pilot | 08 | 08-28 | `S:80a681e0@08-28T11:27` | deadline vs rigor | UNRESOLVED (pattern R18) |
| C30 | Silent failures are a named lesson (L09, L16) | 27 scheduled runs failed silently for 23 days | 07-13 → | 09-11 → 10-03 | F39 | knowing ≠ designing against (L15) | UNRESOLVED |
| C31 | Vault = current memory ("Make sure everything in obsidian is up to date, nothing stale", 08-26) | vault git last committed 09-02 | 08-26 | 09-02 → | `S:d0f42e64@08-26T21:41`; vault git log | — | DOCUMENTATION ERROR |
| C32 | Agent Mode is the launch "hero" | "agent mode is still not being used"; he is "not familiar with agent mode" himself | 08-30 | 08-30 / 09-02 | D30 | hero chosen before demand evidence | UNRESOLVED |
