# 09 — Open Loops: Icarus

Status as of the latest evidence (human: 2026-09-13; automated: 2026-10-03). O01–O30 continue v1's numbering, updated. O31+ are new.

| ID | question | why it matters | current understanding | evidence | status | next known step |
|---|---|---|---|---|---|---|
| O01 | Who is the ICP? | gates pricing, outreach, investors | latest stated: serious vibe coders + SF early adopters (09-05); vault warns not to collapse audience/user/buyer | D41; vault:Unknowns §Product | OPEN since 07-16 | write a defended position |
| O02 | Pricing | no business without it | "Untouched" | vault:Unknowns | OPEN | provisional price |
| O03 | Trust/legal for a design partner's private repo | first enterprise question | not written | vault:Unknowns | OPEN | write it |
| O04 | Does Agent Mode beat a best-possible CLAUDE.md? | if not, collapse it into a file | unmeasured; "agent mode is still not being used" (09-02) | vault:Unknowns; `S:1e17c9e2@09-02T19:39` | OPEN | paired novice test |
| O05 | Is the production Gemini key on contractual no-train terms? | underwrites the privacy promise | private_safe flag set; terms unverified | 09-05 audit | OPEN, audit-flagged | check console |
| O06 | Oracle migration | survival cost | authorized; Task 0 capacity gate | D33 | NOT STARTED (to 10-03) | get a VM or take the paid floor |
| O07 | Apple notarization ($99/yr) | "malware" warning at download | deferred until "proof of life and demand" | D38; `S:331ba684@09-01T18:24` | OPEN | fund it |
| O08 | Does any channel produce connected repos? | north star | none shown | D31 | OPEN | count repos per channel |
| O09 | Site conversion measurement | every channel lands on an unmeasured page | browser analytics removed (his call) | D24 | OPEN | server-side counts or stay dark, decided deliberately |
| O10 | Is ICARUS_ANALYTICS_SALT set in prod? | distinct-user counts for the 50-user goal | he ordered "set the analytics salt on azure then deploy" (`S:c1cd1bc4@08-14T20:45`); the 09-05 audit still lists it as unknown | vault:Unknowns | OPEN (possibly done) | check env |
| O11 | Richie McIlroy reply provenance | the only positive outreach reply | **partly resolved:** he reported it on 08-07 ("also got a reply from richie the founder of cap"); the agent logged it as an X DM; an 08-25 inbox read found no such thread; channel still unverified | `S:c3848080@08-07T13:46` | PARTLY RESOLVED | check email for the thread |
| O12 | Harshitha barter / co-founder outcome | time and equity | barter agreed 08-25/26; co-founder assessment pending; no later record | D28, D40 | UNKNOWN | ask him |
| O13 | Intent-shaped recall | ceiling on Agent Mode | tuning ruled out; needs a reranker or stronger embedder | vault:Learning | OPEN | dependency decision |
| O14 | Cited commit not checked against HEAD | first wrong answer | mechanism known, unbuilt | vault:Unknowns | OPEN | build |
| O15 | Do the other evidence-derived guards receive input in prod? | silence ≠ nothing to flag | only one measured | vault:Unknowns | OPEN | live run per guard |
| O16 | /context variance, ~55s latency | quoting numbers | partly fixed | vault:Unknowns | OPEN | — |
| O17 | Prod vs local retrieval differ | local results aren't evidence | unseparated causes | vault:Unknowns | OPEN | compare with include_evidence |
| O18 | One repo vs multi-repo (org brain) | his "company brain" vision (D36) | "leave that for last" (07-30) | D36 | DEFERRED | his decision |
| O19 | Unconfirmed decision candidates | capture without memory | 45 found 09-05; more accrued 09-09/09-10 (four pending on 09-10); app inbox failed on 09-09 | `S:2193ef7b@09-09T20:21`; `S:468c2054@09-10T08:16` | OPEN | triage |
| O20 | Uncommitted work (terminal Agent Mode, retention copy, Oracle plan, resume, growth notes) | lost-work risk | uncommitted as of 10-03 | `git status` | OPEN | review + commit |
| O21 | History-failure pilot | the product-shaped efficacy number | n=23, paused on agent quota | experiments 08-29 | PAUSED | resume |
| O22 | 4/4 → 1/4: priming or interactivity? | interpreting call rates | open | vault:Unknowns | OPEN | four fresh sessions |
| O23 | Cold email: retired or parked? | 113–125 drafts unsent | declared dead 09-04 | D31 | EFFECTIVELY CLOSED, never formally | — |
| O24 | Antler pitch | funding path | blocked on O01/O02 | D47 | BLOCKED | ICP + pricing |
| O25 | q07 weak-verdict edge (1/60) | gate writer-trust gap | decision owed | mem:gate-gap-writer-verdict-trust | OPEN | decide |
| O26 | Push / stale-decision detection | named as the SaaS-frequency fix on 06-30 | never built | D06 | PARKED | — |
| O27 | Founder path vs employment | determines Icarus's future | job search for cost and to learn sales (09-10); thesis under revision (09-13) | D45, D46 | UNKNOWN after 09-13 | ask him |
| O28 | Tagline canonicalization | positioning clarity | two taglines coexist | vault:Ideas | OPEN | — |
| O29 | HN: lead source or channel? | — | karma blocks participation ("I am unable to comment on HN", 09-03) | `S:b4e90b56@09-03T15:05` | PAUSED | build karma |
| O30 | Reddit account name credibility | serious commenting from a crude username | flagged | v1 / memory | OPEN | new account? |
| O31 | **What is the revised product thesis (09-13)?** | the direction of Icarus | "I am revising my thesis for Icarus … as a product"; content not recorded | `S:57c4e98f@09-13T08:41`, `08:45` | OPEN, HIGH importance | ask him |
| O32 | **Why has every scheduled job failed since 09-11, and does he know?** | no status reports or outreach sync for 23 days | "OAuth session expired" on all 27 runs | 27 session files | OPEN, HIGH | re-authenticate; add failure alerts |
| O33 | YC application outcome | funding / validation | submitted ~07-25; YC form answers drafted again 08-14 | `S:6d69c3f2@07-25T19:20`; `S:c1cd1bc4@08-14T22:23` | UNKNOWN | ask him |
| O34 | Manroze (GTM co-founder via YC) outcome | co-founder | asked about role scope; he framed it as equity-only | D39 | UNKNOWN | — |
| O35 | Job search outcomes after 09-10 | founder path | 2 rejections (MongoDB, Atlassian per agent context); YC Work-at-a-Startup founding roles suggested | `S:468c2054@09-10T08:11`, `08:28` | UNKNOWN | — |
| O36 | Résumé overclaims still in the saved file | his no-bluff rule; job applications | tagline + "~75%" remain in `Alankrit_Ghosh_Resume_DevTools.md` | F40 | OPEN | fix the file |
| O37 | Follower goals (1k X / 2k LinkedIn) | the personal-brand strategy | set 09-13; base ~14–17 X followers | `S:57c4e98f@09-13T08:19` | OPEN | — |
| O38 | Whether the personal-brand pivot is a step away from Icarus | trajectory | content "more on brand with me than Icarus" (09-13) | D46 | UNKNOWN | — |
| O39 | Warm leads left cold (Richie at Cap; aryan) | highest-value pipeline | the agent flagged both as unworked on 09-10; drafts unsent | `S:468c2054@09-10T08:15` (ASSISTANT) | OPEN | send the revival messages |
| O40 | Who owns the Icarus myth / name story | brand coherence | name reason unrecorded; site uses the myth arc (rise to fall) | `S:696dfe35@08-09T21:10` | UNKNOWN | — |
