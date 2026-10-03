# 04 — Belief Evolution: Icarus

Both sides of every change are kept. Causes are labelled `EXPLICIT` when he stated them, otherwise `INFERRED`. Dates are 2026.

## BT01 — Model provider and privacy posture
```text
EARLIER POSITION     Free hosted models, public repos only (06-29): no API budget, 8GB Mac.
        ↓
OBSERVATION          Free tiers may train on code; private code is what companies would pay for.
        ↓
RECONSIDERATION      Trust interlock + private-repo machinery (07-05).
        ↓
NEW POSITION         One paid, private-safe writer for everything (07-13); interlock kept so safety is provable.
        ↓
CURRENT STATUS       CURRENT; contractual no-train terms unverified (O05). Cause: EXPLICIT (docs).
```
Evidence: D04, D07, D09.

## BT02 — Are private repos the product?
```text
EARLIER POSITION     Shelved (06-29); built (07-05); removed from the tester alpha (07-14).
        ↓
OBSERVATION          He discovered on 07-15 that Icarus could not do private repos.
        ↓
RECONSIDERATION      "WHY THE FUCK WOULD ANYONE USE ICARUS FOR PUBLIC FUCKING REPOS, IS THIS A NEW STUDY BUDDY" (S:172973ad@07-15T18:11).
        ↓
NEW POSITION         Private repos restored (07-16); later served over MCP too (08-07, D18).
        ↓
CURRENT STATUS       CURRENT. Cause: EXPLICIT.
```

## BT03 — Who the user is
```text
EARLIER POSITION     v0: founders/CTOs at 5-20-engineer companies.
        ↓
OBSERVATION / STEPS  07-27 "people with very low attention span who DO NOT WANT TO READ"; PR reviewer + new joiner + whole team.
                     07-28 "B2B SaaS AI companies … YC companies with 2 to 3 years of existence".
                     08-04 React-heavy, gen-AI creative-media startups.
                     08-03 "Humans for now but we will have to cater to ai agents quite quickly".
                     08-29 novice builders (Agent Mode).
        ↓
RECONSIDERATION      09-05 "Every real dev we try to sell to will already have an internal tool like this."
        ↓
NEW POSITION         "vibe coders … serious guys like me building out products without any technical knowledge", plus SF early adopters (D41).
        ↓
CURRENT STATUS       EVOLVING / UNRESOLVED: no written ICP; product thesis under revision (09-13). Causes: EXPLICIT.
```

## BT04 — What Icarus is meant to be
```text
EARLIER POSITION     A personal assistant "something like JARVIS from Ironman" (origin, stated 09-08) → a local "why" CLI (v0).
        ↓
OBSERVATION          The PR-reviewer wedge looked like "another basic developer tool".
        ↓
RECONSIDERATION      "Fuck it, we do the organisation bit … I want to build a brain an intelligence system a tech company would be foolish not to have in use" (07-27).
        ↓
NEW POSITION         Company brain (private) / Repo brain (public); then a memory layer for coding agents (Agent Mode as launch hero, 08-30).
        ↓
CURRENT STATUS       UNDER REVISION: "I am revising my thesis for Icarus … as a product" (09-13). New thesis UNKNOWN.
```

## BT05 — What the bottleneck is
```text
EARLIER POSITION     Engineering first; brain before face (06-28).
        ↓
OBSERVATION          Alpha working; "i am someone who has never launched a product so I don't know the path after engineering" (07-15).
        ↓
RECONSIDERATION      "the priority for the next session is just business decisions" (07-15).
        ↓
INTERMEDIATE         Engineering kept dominating (309 commits Jul, 206 Aug); ICP and pricing never written.
        ↓
NEW POSITION         "Icarus is clearly having sales and distribution as the biggest bottle neck, so learning how to sell and close,
                     building a strong network is what I need right now" (09-10).
        ↓
CURRENT STATUS       CURRENT as belief. Action: a job search to learn sales and fund cloud costs. Cause: EXPLICIT.
```

## BT06 — Which channel works
```text
EARLIER POSITION     Cold email at volume: "over 100 emails scheduled for this week alone … 400 emails for the month of August" (08-03).
        ↓
OBSERVATION          ~23 sends, 0 replies; repo-proof personalized pages also ~0.
        ↓
RECONSIDERATION      "We are dropping that approach … keep it simple not bombard them with information" (08-11);
                     "THERE IS NO POINT IN RUNNING ICARUS ON ALL THE REPOS, BURNING CREDITS" (08-17).
        ↓
STEPS                Three channels, X/Reddit/HN (08-25) → Show HN 1 point → Product Hunt (09-01) "we have gotten 0 views"
                     → warm X DMs (2/10 replied) → "current goal is to get 50 users" via replies and LinkedIn (09-04).
        ↓
NEW POSITION         09-13: content "more on brand with me than Icarus"; follower goals 1k X / 2k LinkedIn.
        ↓
CURRENT STATUS       EVOLVING. No channel shown to produce connected repos (O08).
```

## BT07 — Showing failure in public
```text
EARLIER POSITION     Candid about failure with peers: to a co-founder candidate, "I have sent 26 cold emails and gotten exactly one reply.
                     The product works. My distribution does not." (08-11, sent by him).
        ↓
OBSERVATION          His vulnerable posts performed best (vault:X Content).
        ↓
RECONSIDERATION      "being human is fine, but show casing our failures or lack of effectiveness never, remember that everywhere" (08-17).
        ↓
NEW POSITION         No public zeros or defeats; feelings and struggle allowed (his 09-04 post "The hardest part of building Icarus hasn't
                     been engineering. It's spending an entire day working and still feeling like you accomplished nothing.").
                     Honest numbers for investors and co-founders.
        ↓
CURRENT STATUS       CURRENT; reaffirmed under the 09-13 content change. Cause: EXPLICIT (decision); motive UNKNOWN.
```

## BT08 — Do tool descriptions change agent behaviour?
```text
EARLIER POSITION     0/11 → "4/4" after the rewrite (08-11); he posted "0 calls in 11 tasks, then 4 of 4." (08-22).
        ↓
OBSERVATION          The 4/4 came from one shared session.
        ↓
NEW POSITION         "1 of 4, independent sessions" (08-25); he chose to let existing X replies stand (08-26).
        ↓
CURRENT STATUS       CURRENT (corrected); the stale 4/4 remains in a strategy note and old replies (C08).
```

## BT09 — Is Icarus measurably better for agents?
```text
EARLIER POSITION     "25% better" posted unmeasured.
        ↓
OBSERVATION          6/6 in both arms; the value appears only when the tool is called.
        ↓
NEW POSITION         Comparative claims need the comparison to exist; the real signal is tool invocation.
        ↓
CURRENT STATUS       CURRENT. He wanted "numbers as results, how better does opus 5 get with Icarus" (08-21).
```

## BT10 — Analytics vs privacy
```text
EARLIER POSITION     Content capture on by default: "we DONT FUCKING HAVE CUSTOMERS" (08-13).
        ↓
OBSERVATION          Codex P1: "Private questions, answers, and evidence are exported to PostHog by default" (08-14, pasted review).
        ↓
NEW POSITION         "counts-only default for finding 1" (08-14); browser analytics removed from the site (08-18).
        ↓
CURRENT STATUS       CURRENT. Side effect: site conversion unmeasured (O09). Cause: EXPLICIT (review finding accepted).
```

## BT11 — When is "I don't know" honest?
```text
EARLIER POSITION     Honest unknown expected and welcomed: "I suppose this was supposed to be an honest unknown everything else worked well." (07-14).
        ↓
OBSERVATION          Abstentions on things the repo clearly contains: PR 6952 ("This is embarrassing bug", 07-28); the languages question
                     (08-06); line explanations.
        ↓
RECONSIDERATION      "there cannot be a no one wrote this down for that, it just does not make sense" (08-06);
                     "INDEX A BLOODY REPO COMPLETELY" (08-10).
        ↓
NEW POSITION         Total coverage; "only what genuinely does not exist gets I don't know" (mem:total-repo-coverage-principle).
        ↓
CURRENT STATUS       CURRENT; the honesty gate stays. Tension with recall limits is open (O13, C12).
```

## BT12 — Dependencies and stack
```text
EARLIER POSITION     Stdlib by default.
        ↓
OBSERVATION          The embedder silently read 1/4 of each chunk; the site read as "too plain … no soul".
        ↓
NEW POSITION         tree-sitter on measured evidence ("I want all languages to be done perfectly"); full React/three.js site.
        ↓
CURRENT STATUS       EVOLVING: strict for the brain, relaxed for presentation.
```

## BT13 — Hosting: enterprise tech vs cost
```text
EARLIER POSITION     Free hosting (Render) → Azure + Docker, partly for the learning: "I picked docker image, I picked Azure and now seem a little
                     keen on going with Kubernetes" (07-29).
        ↓
OBSERVATION          August bill ₹5,629; a quarter of it was an empty canary.
        ↓
NEW POSITION         "I cannot afford the azure bill yet" → Oracle Always Free; abort to a ~₹500 paid floor (09-10).
        ↓
CURRENT STATUS       AUTHORIZED, NOT RUN. Cause: EXPLICIT (cost).
```

## BT14 — Going solo vs a co-founder
```text
EARLIER POSITION     Solo builder with AI agents.
        ↓
OBSERVATION          "The product works. My distribution does not." (08-11).
        ↓
STEPS                GTM co-founder search for equity: Manroze (08-11), Harshitha (08-25) "how much of the company should I be willing to give her";
                     the Harshitha talks became a barter (08-25/26).
        ↓
NEW POSITION         09-10: learn to sell himself, through a sales job.
        ↓
CURRENT STATUS       UNCERTAIN: no co-founder outcome recorded.
```

## BT15 — Funding
```text
EARLIER POSITION     "get some revenue before moving towards some funding" (07-15); YC application submitted (~07-25).
        ↓
RECONSIDERATION      "we will be seeking funding from them [Antler] … turn this from a simple product into a full scale business" (08-24).
        ↓
OBSERVATION          Blocked: ICP and pricing never written.
        ↓
NEW POSITION         Employment to fund the cloud (09-10).
        ↓
CURRENT STATUS       UNCERTAIN; YC and Antler outcomes UNKNOWN.
```

## BT16 — Agent Mode's role
```text
EARLIER POSITION     "Humans for now" (08-03).
        ↓
STEPS                MCP (08-04) → experiments → "productise the MCP tool" (08-11) → "make agent mode the main hero" (08-30), rebuilt by Codex.
        ↓
OBSERVATION          "the main usecase of talking to your codebase is brilliant it is loved, agent mode is still not being used" (09-02).
        ↓
NEW POSITION         Agent Mode lives inside Claude Code; the user "does not even need to enter Icarus MacApp" (09-05).
        ↓
CURRENT STATUS       EVOLVING; efficacy vs a good CLAUDE.md unmeasured (O04).
```

## BT17 — Content strategy
```text
EARLIER POSITION     Product posts (agent drafts) at 6/day (08-16).
        ↓
OBSERVATION          Drafts read as "generalised crap" and "AI generic"; his own raw posts did better.
        ↓
STEPS                "specific over personal" (08-17) → his own posts ("This is how I write things, simple but actually follow through
                     with a chain of thought and a story", 09-07).
        ↓
NEW POSITION         "more on brand with me than Icarus" (09-13).
        ↓
CURRENT STATUS       CURRENT (as of 09-13).
```

## BT18 — Detecting fabrication
```text
EARLIER POSITION     Score output against evidence lexically (evals/attribution.py).
        ↓
OBSERVATION          It was anti-correlated with truth.
        ↓
NEW POSITION         Compare things to each other, never score against evidence; deterministic guards.
        ↓
CURRENT STATUS       CURRENT.
```

## BT19 — Data retention claim
```text
EARLIER POSITION     Docs and the vault say data is "discarded after each request".
        ↓
OBSERVATION          The 09-05 audit found corpora and decisions durable until deletion.
        ↓
NEW POSITION         He ordered "fix the retention copy on the website", "now fix the internal docs too" (09-05).
        ↓
CURRENT STATUS       Website fixed; repo docs fixed but uncommitted; vault notes still say "discarded" (C01).
```

## BT20 — How agents should be trusted (meta)
```text
EARLIER POSITION     High delegation: "Run it yourself, I have given you full permission" (07-17); "do it all for me" (08-28).
        ↓
OBSERVATION          Wrong facts in agent research; agents restarting work unasked; repeated em-dash violations.
        ↓
NEW POSITION         "I don't trust your context grabbing ability anymore … tell me where you got what from" (09-07);
                     "Stop adding emdashes … I don't want to waste credits reminding you the same thing over and over again" (09-03).
        ↓
CURRENT STATUS       CURRENT: delegation stays high, but with demanded provenance.
```
