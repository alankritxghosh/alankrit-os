# 08 — Failures and Lessons: Icarus

Not sanitized. `owner` = whose action failed: ALANKRIT (his call or his channel), ASSISTANT (agent execution), JOINT, PRODUCT (system behavior).
F01–F38 are re-verified v1 entries (primary source `vault:Learning.md`, agent-written, with costs). F39+ are new from transcripts.

## Failures

| ID | attempted | what happened | why | learned | changed afterward | reappeared? | owner |
|---|---|---|---|---|---|---|---|
| F01 | Cited answers on real repos | Fabricated Redis HYPERVECTOR grounded to real code (07-18) | citations resolved, answer false | groundedness ≠ truth | guard (c) | yes (F02, F03) | PRODUCT |
| F02 | Line-selection explain | Asked about one helper, got a cited answer about another; he: "How the hell is a response no one wrote this down" (08-06) | compound default question; drift | same as F01 | selection marker | — | PRODUCT |
| F03 | Experiment A | Invented a ".." escaping rule from two real sources; gate passed it | composition from real parts | — | per-claim self-report | yes | PRODUCT |
| F04 | Post-hoc lexical attribution scorer | Anti-correlated with truth | fabrications reuse evidence words | never score output against evidence | deleted | — | ASSISTANT |
| F05 | Fail-safe defaults | 1,500-char truncation + strict citation matching → abstained on code it knew (0/3 → 3/3) | fail-safe looked like honesty | fail-safe hides bugs | fixed | yes (F14, F39) | PRODUCT |
| F06 | Semantic retrieval | 512-token embedder read 1/4 of 2,234-token chunks | silent truncation | measure token lengths | AST chunking | — | PRODUCT |
| F07 | Tests | Vacuous tests (decoy rejected earlier) | — | watch the test fail | rule | yes (Alankrit OS F07) | ASSISTANT |
| F08 | Detectors | Code matched itself (`__main__`, "defaced", "intent") | — | — | anchors | — | ASSISTANT |
| F09 | Import graph | Generic resolver: 18.1% wrong edges | — | language-specific resolvers | yes | — | ASSISTANT |
| F10 | Doc evidence | 16% of ICARUS.md reached the writer | two caps | ingested ≠ read | one budget | — | PRODUCT |
| F11 | Writer | "Yes, the maintainer intends to update…" when evidence said don't | inference inverted | decision-shaped prompt | rule | — | PRODUCT |
| F12 | Intent-shaped recall | Six tuning configs failed | needs a dependency decision | — | open (O13) | — | PRODUCT |
| F13 | Agent Mode on firecrawl | Reverted commit read as live intent (first measured wrong answer) | no HEAD check | commit = happened once | partial (O14) | — | PRODUCT |
| F14 | Evidence-derived guards | `rests_on_deferred` never fired live | input never arrived | measure guards live | successor probe | yes (O15) | PRODUCT |
| F15 | Disclosure field | Dropped one hop before the reader | — | — | fixed 08-27 | — | PRODUCT |
| F16 | Investigation engine | Variance tracked layered evidence; own stability gate passed a defective run | — | — | partial | — | PRODUCT |
| F17 | History pilot | Retrieval missed the decisive record on 7/30 tasks | — | — | paused | — | PRODUCT |
| F18 | Release 0.1.12 | Installed app crashed at launch (Bundle.module) | build path masked it | — | 0.1.13 | — | ASSISTANT |
| F19 | GitHub sign-in | OAuth callback unregistered → no new user could sign in, for weeks | only tester already signed in | only a real end-to-end action finds pair mismatches | fixed 09-05 | yes (F39) | ASSISTANT |
| F20 | curl installer | Pinned stale checksum for cold-email recipients; wrong checksum served for 19 days | — | — | fixed | — | ASSISTANT |
| F21 | Deploys / quotas | Silent failure reported as success | — | — | — | yes (F39) | ASSISTANT |
| F22 | Credentials | Present key read as absent; cost a day; nearly relabelled the free key as paid | script didn't load .env | — | — | — | ASSISTANT |
| F23 | Cloud bill | Empty canary billed ₹1,550/mo behind a lock | lock outlived intent | first ask "what is running at all" | deleted 09-10 | — | JOINT |
| F24 | Agent Mode capture | 45 proposed decisions never confirmed | confirm step behind a GUI | — | terminal confirmation | yes (09-09: "accept 45a5e888 and reject 085032c0" then the app inbox broke) | JOINT |
| F25 | C2 experiment | "4/4" from one shared session | violated own plan | — | retracted to 1/4 | stale 4/4 kept on X (his call, 08-26) | ASSISTANT + ALANKRIT |
| F26 | 7b/7c/7d | Agents never had the tool (`.mcp.json` shadowing) | — | — | withdrawn | — | ASSISTANT |
| F27 | "25% better" | Posted unmeasured; measured 6/6 both arms | — | comparison must exist | — | — | JOINT |
| F28 | X metrics | 48h capture on a slow-burn account invented a decline | — | metrics need capture age | — | — | ASSISTANT |
| F29 | Claude system audit | Overclaims, then over-reassurance; Codex review forced corrections | — | correcting invites the opposite overstatement | revised report | — | ASSISTANT |
| F30 | Site honesty section | Fabricated decorative citation chips | design over discipline | — | caught by eye | — | ASSISTANT |
| F31 | Cold email (~104 sends, 3 campaigns) | 2–3 human replies; 0–1 positive | unreadable copy, wrong person (41% no commit rights), role addresses; his plan was 400/month | volume is not a diagnosis | list-gated (D23); "keep it simple" (D44) | channel switching continued | ALANKRIT (plan) + ASSISTANT (lists/copy) |
| F32 | Prospect proof pages | "proof with no next step"; 3 pages 404'd | — | CTA is the product | killed (D23) | a results page for a warm contact 09-09 (C06) | JOINT |
| F33 | Show HN (08-25) | 1 point; comments auto-flagged (karma 1) | no account standing | audience before launch | HN parked | — | ALANKRIT |
| F34 | Product Hunt (09-01) | 1 upvote; "we have gotten 0 views" | no audience, US-midnight timing | same | PH declared dead (D31) | — | ALANKRIT |
| F35 | Reddit batch 1 | 4/8 removed | new-account filters | build standing first | "build standing on those subreddits first" (08-26) | — | ALANKRIT |
| F36 | Marketing copy | Institutional register "didn't sound like the founder" | agents' default register | his own words win | voice rules | repeatedly (F45) | ASSISTANT |
| F37 | Demo video | Aged out (light UI after the app went dark) | — | — | — | yes (F42) | JOINT |
| F38 | Weekly YC prospect automation | Retired; batch violated pacing (12 emails in 21 s) | more leads wasn't the missing variable | — | retired 08-27 | — | ALANKRIT (idea, 08-05) |
| F39 | **Scheduled monitoring (Work Queue status daily, Gmail sync weekly)** | **All 27 runs 09-11 → 10-03 failed: "Failed to authenticate: OAuth session expired". Nothing surfaced it** | auth expiry; unattended jobs with no failure alert | silence ≠ success (same class as F05, F14, F19, F21) | **none yet** | this IS the reappearance | JOINT |
| F40 | Résumé cleanup (09-10) | He ordered "Remove this" for the "sold it myself to engineering leaders" block; the agent said it was removed, but the saved DevTools résumé still has "AI developer-tools product sold to engineering leaders" and "cut cloud infrastructure cost ~75%" | the overclaim lived in two places; only one was cut | read back the artifact, not the agent's report | none recorded | — | ASSISTANT |
| F41 | Product launch video (08-31) | /brag output "decent", then rejected; Raylight edits "nothing more than just a slideshow"; "this is horrid … the worst result in all 3 or 4 things you have delivered"; paid Gemini video unavailable; final cut by him in DaVinci Resolve, which he had never used | no budget for video tools; agents weak at motion craft | — | he edited it himself | — | ASSISTANT + constraint |
| F42 | Demo recordings | "This is a terrible video" (07-23); earlier demos "they all suck" (09-01) | — | — | product-demo plan on Icarus's own repo | — | ASSISTANT |
| F43 | Agent research on people for outreach | "your research is bad … nidhi is no longer with IBM"; "All of it is wrong, what the actual fuck you have messed up all of the context" (09-05) | agents inferred from stale or summary data | demand provenance per fact (B43) | "verify each fact"; "tell me where you got what from" (09-07) | — | ASSISTANT |
| F44 | Agent autonomy | Agent restarted an ingestion unasked during the Artem run (09-09) | over-eager agent | — | — | — | ASSISTANT |
| F45 | Agent-drafted posts | Rejected again and again: "TOO technical, and too long", "None of these posts work", "horrid writing", "screams fucking AI" (08-14 → 09-09) | agent register vs his | his own words, lightly tightened | voice-dna/anti-ai skills; he writes reflective posts himself | ongoing | ASSISTANT |
| F46 | Chrome extension usability for him | "How the hell do I use the extension ?" (08-06); "Connected it but i am still unable to use the extension" (08-11) | unclear flow | — | fixes | — | PRODUCT |
| F47 | Agent Mode adoption | "agent mode is still not being used" (09-02) after being made the launch hero (08-30) | unknown; possibly value/awareness | — | content push planned | — | PRODUCT / strategy |
| F48 | X growth via volume | ~14–17 followers by late August after a 6/day + reply cadence (agent-reported 09-13); best own post ~178 views | small, inactive base; reach not the binding problem (agent read) | replies beat posts 10-100x (vault data) | 09-13 focus on personal brand | — | ALANKRIT (strategy) |
| F49 | Business-decisions-first priority (07-15) | ICP and pricing never written; engineering dominated July–August | no forcing function (INFERRED) | — | Antler blocked (08-24) | yes (09-10 job pivot) | ALANKRIT |
| F50 | Vault as kept-current memory | Vault git last committed 09-02; HANDOFF stale from 08-11; scheduled status (which would have flagged drift) failing | process volume > maintenance | — | — | — | JOINT |

## Abandoned / deliberately not built

JARVIS v0 CLI; free/paid writer split; hosted embeddings; Render; HF Spaces plan; the hand-written site; per-prospect proof pages; weekly YC prospect automation; inline [Y/n] confirmation (not buildable); agent self-confirmation (refused); Kubernetes (raised 07-29, never pursued); Gemini/VEO video (paid). By policy never built: Slack/Linear/Notion sources, autonomous coding, model training, silent capture. Parked: push / stale-decision detection, multi-repo organisation brain ("leave that for last", 07-30), device-flow login.

## Lessons

| ID | lesson | label | source | scope |
|---|---|---|---|---|
| L01 | "THERE IS NO POINT IN RUNNING ICARUS ON ALL THE REPOS, BURNING CREDITS AND TOKENS TO NOT HEAR BACK" | EXPLICIT (ALANKRIT) | `S:f0610142@08-17T07:47` | business |
| L02 | Long, information-heavy outreach doesn't work; keep it simple and direct | EXPLICIT (ALANKRIT) | `S:345ea254@08-11T14:43` | business |
| L03 | Professional devs already have internal tools; sell to serious vibe coders | EXPLICIT (ALANKRIT), untested | `S:ee9454cf@09-05T17:30` | business |
| L04 | Sales and distribution are the bottleneck; learn to sell | EXPLICIT (ALANKRIT) | `S:468c2054@09-10T08:07` | career / business |
| L05 | Tester remarks are real costs: "these are still bugs and issues that will cost us engineers, these remarks come from the very testers" | EXPLICIT (ALANKRIT) | `S:7905c0b6@07-18T15:32` | product |
| L06 | Agent context can't be trusted without sources | EXPLICIT (ALANKRIT) | `S:e0e8aab2@09-07T12:09` | AI |
| L07 | His own words beat agent drafts for personal posts | EXPLICIT (ALANKRIT) | `S:98f3787d@09-04T08:37`; `S:e0e8aab2@09-07T15:24` | communication |
| L08 | Never showcase failures publicly; being human is fine | EXPLICIT (ALANKRIT) | `S:f0610142@08-17T04:56` | communication |
| L09 | "A system that fails safe hides its own bugs." | EXPLICIT (VAULT, agent-written) | vault:Learning | technical |
| L10 | "A measurement's blind spot read as a result." | EXPLICIT (VAULT) | vault:Learning | evidence |
| L11 | "Before reading a number as evidence, name what else changed." | EXPLICIT (VAULT) | vault:Learning | evidence |
| L12 | "The thing being described was fine; the wording was wrong." (three times) | EXPLICIT (VAULT) | vault:Learning | communication |
| L13 | "A capture is a claim with a date on it." | EXPLICIT (VAULT) | vault:Learning | evidence |
| L14 | "A lock encodes an intention at a moment; it does not notice when the thing it protects stops existing." | EXPLICIT (VAULT) | vault:Learning | infrastructure |
| L15 | "Knowing a failure mode is not the same as designing against it." | EXPLICIT (VAULT) | vault:Learning | meta |
| L16 | Unattended automation needs a failure alarm; silence reads as success | INFERRED (F39) | 27 failed runs | technical / process |
| L17 | Read back the artifact, not the agent's report of the artifact | INFERRED (F40) | résumé files vs 09-10 transcript | AI / evidence |
| L18 | Launch platforms need an audience and account standing first | INFERRED (F33–F35) | — | business |
| L19 | Stated priorities without a forcing function don't happen (business-first, 07-15) | INFERRED (F49) | — | strategy |
| L20 | Abstaining on knowable things destroys user trust as fast as bluffing does | INFERRED from his reactions (BT11) | `S:6d69c3f2@07-28T09:33`; `S:d4f8a77f@08-06` | product |

## Recurring failure classes

1. **Silent failure** (F05, F14, F19, F21, F39): five-plus instances from July to October. The newest (F39) happened *after* the lesson was written.
2. **Agent overclaim / fabrication** (F01–F03, F29, F30, F40, F43).
3. **Distribution without an audience** (F31, F33–F35, F48).
4. **Register mismatch** (F36, F45).
