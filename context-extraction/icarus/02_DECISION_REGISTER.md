# 02 — Decision Register: Icarus

`Decider:` ALANKRIT (his instruction, verified in a transcript where possible) · ALANKRIT (per vault) (recorded by agents as his call; no transcript checked) · ASSISTANT (agent-made, adopted without recorded objection) · SHARED (agent proposal he explicitly chose).
IDs D01–D35 keep their v1 numbers; D36+ are new in v2. Each entry lists context, problem, alternatives, choice, rationale, evidence, tradeoffs and risks, result, reversal, status, confidence and sources.

**D01 · 2026-06-27 · Reset JARVIS v0 to docs-only and rename it Icarus.**
Decider: ALANKRIT (per vault/memory). Context: v0 was a local read-only "why" CLI; the idea began as a JARVIS-style personal assistant (`S:2f81409a@09-08T15:08`). Alternatives: build on v0 (rejected: "do not resurrect"). Rationale: new direction (cloud brain, GitHub source, voice face); deeper reason UNKNOWN. Result: Phase 1 from zero the next day. Reversed: no. Status: ACTIVE. Confidence: HIGH. Sources: git:2bdbac3, git:8ed0869; mem:icarus-reset-and-foundation-docs.

**D02 · 2026-06-28 · Brain before face; eval harness before brain.**
Decider: SHARED (strategy doc). Alternatives: voice-first demo. Rationale: Unblocked shows a typed brain sells; voice is differentiation, not revenue. Tradeoffs: no demoable face for days. Result: gate + red baseline on day one; faces from 06-30. Status: ACTIVE. Confidence: HIGH. Sources: repo:docs/STRATEGY.md §3; git:8afbfbb.

**D03 · 2026-06-28 · Freeze the eval corpus at simonw/llm @ 94769b8.**
Decider: ASSISTANT. Rationale: reproducible board. Status: ACTIVE. Confidence: HIGH. Sources: mem:phase-1-corpus-and-labelling.

**D04 · 2026-06-29 · Free hosted models, public repos only.**
Decider: SHARED. Context: no API budget, 8GB Mac. Alternatives: paid writer. Risks: free tiers may train on code. Result: superseded within two weeks. Reversed: yes, by D07, D09, D11. Status: REVERSED. Confidence: HIGH. Sources: mem:public-repo-mvp-direction.

**D05 · 2026-06-30 · Unified cloud with per-tenant isolation.**
Decider: SHARED. Alternatives: single-tenant per customer; pooled multi-tenant. Chosen: one operated cloud, isolated stores; single-tenant as enterprise upsell. Status: ACTIVE. Confidence: HIGH. Sources: repo:docs/decisions/2026-06-30-unified-cloud-per-tenant-isolation.md.

**D06 · 2026-06-30 · Positioning: organizational memory; explanation is the wedge.**
Decider: SHARED (after an external evaluation scored the PoC 7.5–8/10). Rationale: pull is low-frequency; capture and push are the moat. Result: push never built; capture partly built through Agent Mode. Status: ACTIVE. Confidence: HIGH. Sources: repo:docs/decisions/2026-06-30-organizational-memory-positioning.md.

**D07 · 2026-07-05 · Deterministic trust interlock (evals/trust.py).**
Decider: ASSISTANT. Rationale: refuse any provider not declaring private_safe; never infer it from a key string. Risks: the flag on the launch provider is not backed by verified contract terms (O05). Status: ACTIVE, challenged. Confidence: HIGH. Sources: git:59fdb1d; vault:Unknowns §2026-09-05.

**D08 · 2026-07-08 · Local embeddings (model2vec, then fastembed the same day).**
Decider: ASSISTANT. Rationale: "kill the billing/quota dependency". Status: ACTIVE. Confidence: HIGH. Sources: git:98261a4; vault:Stack History.

**D09 · 2026-07-13 · One model, no tier split (gemini-paid serves everything).**
Decider: SHARED. Rationale: one private-safe writer for every repo; the interlock stays so safety is provable, not coincidental. Status: ACTIVE. Confidence: HIGH. Sources: vault:Decision History §One model; mem:one-model-no-tier-split.

**D10 · 2026-07-12 · Host on Azure Container Apps.**
Decider: ALANKRIT, partly by preference: "there is this thing of mine to work and learn complex tech or enterprise grade tech, hence I picked docker image, I picked Azure and now seem a little keen on going with Kubernetes" (`S:fb942d6d@2026-07-29T16:20`). Alternatives: Render free (0.1 CPU killed ingest); HF Spaces (planned, never run). Result: worked; ~₹5,600–6,200/mo became unaffordable. Reversed: being reversed by D33. Status: BEING_REVERSED. Confidence: HIGH. Sources: vault:Stack History; transcript above.

**D11 · 2026-07-15/16 · Private repos are the product: re-enable them.**
Decider: ALANKRIT. Trigger: "DO THE PRIVATE REPOS, WHAT THE ACTUAL FUCK IS WRONG WITH YOU, I NEED THE PRIVATE REPOS WORKING, WHY THE FUCK WOULD ANYONE USE ICARUS FOR PUBLIC FUCKING REPOS" (`S:172973ad@2026-07-15T18:11`), after alpha-1 removed them. Alternatives: public-only alpha. Result: alpha-5 on 07-16; one shared corpus per private repo from 07-28. Status: ACTIVE. Confidence: HIGH. Sources: transcript; tags alpha-1, alpha-5.

**D12 · 2026-07-17/18 · AST-aware chunking (stdlib ast + tree-sitter).**
Decider: ALANKRIT ("yes, prove the AST-chunking win with a red→green eval"; "yes, add tree-sitter and scope the migration, I want all languages to be done perfectly", `S:f6d9d234@07-16T23:58`, `07-17T00:13`). Evidence: semantic recall@5 69.2% → 92.3%. Status: ACTIVE. Confidence: HIGH. Sources: vault:Stack History.

**D13 · 2026-07-18 · Gate guard (c): entity presence.**
Decider: SHARED. Trigger: live P0, a fabricated Redis HYPERVECTOR answer grounded to real code; he confirmed "HYPERVECTOR now abstains" (`S:7905c0b6@07-18T10:28`). Status: ACTIVE. Confidence: HIGH. Sources: mem:entity-presence-gate-fix.

**D14 · 2026-07-29 · Onboarding tour steps chosen by measurement.**
Decider: ALANKRIT ("Run the abstention-rate measurement across ten real repos first"; "build the thin onboarding over the five proven steps", `S:fb942d6d@07-29T10:08`, `11:55`). Status: ACTIVE. Confidence: HIGH.

**D15 · 2026-07-30 · Returning-user state: exactly four facts, never joined to questions.**
Decider: ASSISTANT. Status: ACTIVE. Sources: repo:docs/decisions/2026-07-30-returning-user-state.md.

**D16 · 2026-08-03 · Short-lived, repo-scoped agent sessions; never the GitHub credential.**
Decider: ASSISTANT. Status: ACTIVE. Sources: repo:docs/decisions/2026-08-03-short-lived-agent-sessions.md.

**D17 · 2026-08-07 · Engineering memory records: one proposal, one branch, one PR, never auto-merge.**
Decider: SHARED ("go with option 2", `S:c3848080@08-07T19:32`). Result: seven confirmed proposals exist as unmerged icarus/decision-* branches (08-31 → 09-01). Status: ACTIVE. Confidence: HIGH. Sources: repo:docs/decisions/2026-08-07-engineering-memory-records.md; git branches.

**D18 · 2026-08-07 · The MCP serves private repos.**
Decider: ALANKRIT ("why not make pvt repos accessible via mcp?" … "It is okay let it be generic, make icarus mcp private in terms of capability as well, let any model use it", `S:c3848080@08-07T18:04`, `18:09`). Tradeoff, accepted openly: the exposure moves to whoever configures the client. Status: ACTIVE. Confidence: HIGH. Sources: transcript; repo:docs/decisions/2026-08-07-mcp-private-repository-access.md.

**D19 · 2026-08-11 · Rewrite MCP tool descriptions to trigger on observable events.**
Decider: ASSISTANT. Result: "4/4" later corrected to "1 of 4" (D26). Status: ACTIVE (claim revised). Sources: git:064879a.

**D20 · 2026-08-11 · Take the repo OAuth scope off first sign-in.**
Decider: SHARED ("fix the oauth scope", `S:345ea254@08-11T14:03`, after "These are too many steps we will lose people", `13:55`). Status: ACTIVE. Confidence: HIGH.

**D21 · 2026-08-13 → 08-14 · Analytics: content capture on by default → counts-only by default.**
Decider: ALANKRIT, both times. First he insisted on on-by-default capture of codebases and questions: "Buddy keep the toggle on by default we DONT FUCKING HAVE CUSTOMERS, CAN YOU UNDERSTAND THAT" (`S:44a14cb9@2026-08-13T08:11`). Then, after a pasted Codex review flagged "[P1] Private questions, answers, and evidence are exported to PostHog by default" (`S:c1cd1bc4@08-14T17:54`, ASSISTANT), he chose "counts-only default for finding 1" (`18:20`). The vault rationale, "Absence is not consent", is agent-written. Status: ACTIVE (counts-only). Reversed: yes, within a day. Confidence: HIGH.

**D22 · 2026-08-17 · No public disclosure of his own failures.**
Decider: ALANKRIT: "One thing being human is fine, but show casing our failures or lack of effectiveness never, remember that everywhere" (`S:f0610142@2026-08-17T04:56`). Made knowing his vulnerable posts performed best (vault:X Content). Scope: public. Investors and co-founders get the honest numbers (his 08-11 message to Manroze disclosed "26 cold emails … exactly one reply"). Status: ACTIVE. Confidence: HIGH.

**D23 · 2026-08-17 · Kill the prospect proof pages; the CTA is the download; outreach is list-gated.**
Decider: ALANKRIT: "sending over an indexed query search along with results means nothing to the receivers … I need to direct them to the download site" and "THERE IS NO POINT IN RUNNING ICARUS ON ALL THE REPOS, BURNING CREDITS AND TOKENS TO NOT HEAR BACK" (`S:f0610142@08-17T07:37`, `07:47`). Status: ACTIVE (a results page was later made for a warm contact; C06). Confidence: HIGH.

**D24 · 2026-08-17/18 · No third-party analytics script on the website.**
Decider: ALANKRIT ("remove the posthog snippet and redeploy", `S:f0610142@08-18T12:14`). Consequence: site conversion is unobservable (O09). Status: ACTIVE. Confidence: HIGH.

**D25 · 2026-08-25 · Three distribution channels: Reddit, X, Hacker News.**
Decider: ALANKRIT ("Three platforms I need us to double down on … Reddit, X and Hacker News", `S:7440e957@08-25T12:05`). Superseded in practice by D31 (PH and LinkedIn added; HN/PH declared dead). Status: SUPERSEDED. Confidence: HIGH.

**D26 · 2026-08-25/26 · Retire C2's "4/4"; quote "1 of 4, independent sessions".**
Decider: SHARED ("yes, find every surface quoting 4/4" … "let the X replies exist it is fine", `S:d0f42e64@08-26T13:27`, `13:30`). Note: he chose to leave X replies that quoted 4/4 standing (C08). Status: ACTIVE. Confidence: HIGH.

**D27 · 2026-08-24/25 · Successor check; a temporal flag that annotates, never resolves.**
Decider: ASSISTANT ("build the temporal check", `S:776c7f56@08-24T18:58`). Status: ACTIVE. Sources: vault:Decision History.

**D28 · 2026-08-25/26 · Barter with Harshitha: he builds her meta-ads product, she markets Icarus.**
Decider: ALANKRIT ("I am going to build her, her product while she markets Icarus for me a barter system exchange", `S:6bc55771@08-25T21:49`). Context: she was first a **co-founder candidate** (D40). Terms (vault): "delivered" means repos connected; he approves every claim; 30-day review. Outcome: UNKNOWN. Status: UNKNOWN. Confidence: HIGH (that it was decided).

**D29 · 2026-08-26 · Website rebuilt in Next/React/Tailwind/Motion/three.js.**
Decider: ALANKRIT ("the website for icarus must also be 3d"; "I don't like the current site, i suppose the tailwind, motion, react stack"; "make sure that we do not just come across as a dark site with no soul", `S:6bc55771@08-25T22:38`; `S:d0f42e64@08-26T15:31`, `16:00`). Status: ACTIVE. Confidence: HIGH.

**D30 · 2026-08-29/30 · Agent Mode = continuity and judgment scaffold for novice builders; Agent Mode as the launch hero.**
Decider: ALANKRIT (per vault: a "24-hour build mandate") and in transcript: "I am looking to make agent mode the main hero for Icarus … I myself am not familiar with agent mode, and while you were gone, I used codex to add onto and rebuild our agent mode" (`S:331ba684@08-30T22:39`, `22:42`). Evidence after launch: "agent mode is still not being used" (`S:1e17c9e2@09-02T19:39`). Status: ACTIVE; value unmeasured (O04). Confidence: HIGH.

**D31 · 2026-09-04 · Goal: 50 users through replies and DMs; PH, HN and cold email declared dead.**
Decider: ALANKRIT ("Look our current goal is to get 50 users for Icarus that is it", `S:98f3787d@09-04T09:35`). Status: ACTIVE as of 09-13, then the thesis came under revision (D46). Confidence: HIGH.

**D32 · 2026-09-05 · Agent Mode confirmation lives inside Claude Code (terminal), not in the app.**
Decider: ALANKRIT: "the goal is to make the claude code session so good, that the user does not even need to enter Icarus MacApp … all the recommendations are accepted here … without having to accept/ confirm anything inside Icarus" (`S:17a798b1@2026-09-05T12:14`). The agent's design kept a human confirming act, as `/icarus` commands. Status: BUILT, UNCOMMITTED. Confidence: HIGH.

**D33 · 2026-09-10 · Leave Azure for Oracle Always Free; abort rule to a ~₹500/mo paid floor.**
Decider: ALANKRIT ("We might have to migrate to Oracle cloud, from azure I cannot afford the azure bill yet"; "okay, this could work as a plan", `S:468c2054@09-10T07:13`, `08:03`). The agent found and deleted an empty canary (₹1,550/mo). Status: AUTHORIZED, NOT RUN. Confidence: HIGH.

**D34 · 2026-08-21 · Never contribute to repos that forbid AI contributions; add an attribution footer.**
Decider: SHARED ("post it with the attribution footer", `S:e8bb2d56@08-21T17:56`). Status: ACTIVE.

**D35 · 2026-08-23 · Every Substack headline answers a "Why".**
Decider: ALANKRIT ("Start all our articles with a why, the heading should always be answering a question", `S:3146f729@08-23T17:25`). Status: ACTIVE.

**D36 · 2026-07-27 · Build an organisation / company brain, not "another basic developer tool".**
Decider: ALANKRIT: "Fuck it, we do the organisation bit, we currently are unknown nothing matters, I don't want to build another cursor, claude code, codex or vscode … I want to build a brain an intelligence system a tech company would be foolish not to have in use" (`S:6d69c3f2@07-27T22:06`). Alternatives (from the agent): PR-reviewer extension wedge; eng-manager digest. Result: org-brain plan; multi-repo deferred to last (07-30). Status: PARKED (vision kept). Confidence: HIGH.

**D37 · 2026-07-28 · "Repo Brain" for public repos, "Company Brain" for private repos.**
Decider: ALANKRIT (`S:e76a10e1@07-28T12:47`). Status: ACTIVE in UI copy, partially; "company brain" text later removed to declutter (`S:1e17c9e2@09-02T20:18`). Confidence: MEDIUM.

**D38 · 2026-07-29 · No Apple Developer ID until there is proof of demand.**
Decider: ALANKRIT: "for sometime I will not be going with the dev id path of apple because I need proof of life and demand for me to go through with it" (`S:fb942d6d@07-29T16:19`); earlier "there is no dev ID till we get some form of funding" (`S:6d69c3f2@07-25T19:45`). Chosen instead: Sparkle in-app updates, a curl installer and Homebrew. Risk accepted: Gatekeeper friction. Result: a "malware detected" warning on launch day (09-01). Status: ACTIVE (O07). Confidence: HIGH.

**D39 · 2026-08-11 · Recruit a GTM co-founder for equity, not salary (Manroze, via YC).**
Decider: ALANKRIT: "This won't be like hiring this will practically be GTM cofounder for me, I am pre revenue so I cannot pay her, this is going to be about ownership" (`S:8e8c6d02@08-11T20:10`). His opening message (sent by him; drafting UNKNOWN) disclosed "26 cold emails and gotten exactly one reply. The product works. My distribution does not." Outcome: UNKNOWN. Confidence: HIGH (decision), outcome UNKNOWN.

**D40 · 2026-08-25 · Assess Harshitha as a GTM/marketing/sales co-founder.**
Decider: ALANKRIT ("Harshitha is a supposed to come in and partner with me for GTM, Marketing and Building out a Sales pipeline … how much of the company should I be willing to give her", `S:7440e957@08-25T09:39`). It became a barter (D28) the same day. Status: UNKNOWN. Confidence: HIGH.

**D41 · 2026-09-05 · Target serious vibe coders and SF early adopters; professional devs already have internal tools.**
Decider: ALANKRIT: "lets try finding and getting vibe coders on boarded not basic hobbiests serious guys like me building out products without any technical knowledge learning as they go. Every real dev we try to sell to will already have an internal tool like this … lets try finding devs and customers in the SF region the best early adapters are from there" (`S:ee9454cf@09-05T17:30`). Status: ACTIVE hypothesis; no written ICP. Confidence: HIGH (as stated).

**D42 · 2026-08-16 · The Obsidian vault is mandatory session context; scheduled sync agents.**
Decider: ALANKRIT ("claude MUST REFER TO OBSIDIAN, AND WHEN NEEDED AT THE END OF A SESSION OR SO, UPDATE OBSIDIAN"; Gmail sync "every Saturday at 6:30 PM IST", `S:635f7365@08-16T22:43`, `22:36`). Result: vault + routing rules; daily Work Queue status job; all scheduled jobs failing since 09-11 (F39). Status: ACTIVE (automation broken). Confidence: HIGH.

**D43 · 2026-08-16 → 09-02 · Content cadence: 6 X posts/day; reply scout every 2h (9 am to midnight); daily quotas of 15 X / 15 Reddit / 5 HN replies.**
Decider: ALANKRIT (`S:635f7365@08-16T23:04`; `S:3146f729@08-23T21:58`; `S:b4e90b56@09-02T12:35`). Status: ACTIVE until 09-13; then the content focus moved to his personal brand (D46). Confidence: HIGH.

**D44 · 2026-08-11 · Short, direct outreach emails; drop the long "manual" style.**
Decider: ALANKRIT ("I want the emails to be direct and to the point … Simple no overcomplication"; "30 seconds max is what we get to impress a person"; "We are dropping that approach, it is not working", `S:345ea254@08-11T13:36`, `13:38`, `14:43`). Status: ACTIVE. Confidence: HIGH.

**D45 · 2026-09-10 · Job search for sales/SDR roles in parallel with Icarus.**
Decider: ALANKRIT: "I suppose I will need a job fast to be able to afford the costs of running Icarus on the cloud"; "I suppose I want to learn more of sales, and distribution than engineering right now, as Icarus is clearly having sales and distribution as the biggest bottle neck, so learning how to sell and close, building a strong network is what I need right now" (`S:468c2054@09-10T08:03`, `08:07`). Alternatives: solutions-engineer or developer-advocate roles (offered by the agent; set aside). Status: ACTIVE as of 09-10; outcome UNKNOWN. Confidence: HIGH.

**D46 · 2026-09-13 · Revise the Icarus product thesis; personal brand first in content.**
Decider: ALANKRIT ("Say the type of content I will be posting to be more on brand with me than Icarus, I am revising my thesis for Icarus." … "The thesis review is for Icarus as a product", `S:57c4e98f@09-13T08:41`, `08:45`). Content of the revision: UNKNOWN. Status: OPEN. Confidence: HIGH (that it was decided).

**D47 · 2026-08-24 · Pursue Antler funding; build the business plan.**
Decider: ALANKRIT ("we are going to have to prepare a pitch for Antler as well, we will be seeking funding from them"; "its about time we turn this from a simple product into a full scale business, an actual startup", `S:3146f729@08-24T13:56`, `14:01`). Status: BLOCKED on ICP and pricing (O24). Confidence: HIGH.

**D48 · 2026-08-11 · The website is the only install path, and friction must be minimal.**
Decider: ALANKRIT ("I want to reduce the friction behind installing Icarus as MUCH AS POSSIBLE. The emails we send out and dms we send out will not carry these steps they will only carry the website link", `S:345ea254@08-11T14:14`). Result: 6 install steps reduced to 3. Status: ACTIVE. Confidence: HIGH.

**D49 · 2026-08-31 · Launch on the Vercel default domain.**
Decider: ALANKRIT ("I don't have a domain yet, I cannot afford one, so I suppose Icarus launches with vercel site", `S:331ba684@08-31T18:02`). Status: ACTIVE. Confidence: HIGH.

**D50 · 2026-07-15 · Business decisions take priority after this engineering pass.**
Decider: ALANKRIT ("the priority for the next session is just business decisions, the rest can wait for after the feedback", `S:172973ad@07-15T19:57`). Result: engineering continued to dominate through August (C16). Status: STATED, NOT FOLLOWED. Confidence: HIGH.
