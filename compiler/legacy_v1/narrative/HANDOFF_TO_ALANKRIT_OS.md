# HANDOFF TO ALANKRIT OS

> Read this first. Executive context layer, compiled 2026-10-03 by `python compiler/run.py`.
> **Evidence stops at 2026-09-10 and comes from ONE project (Icarus).** Full detail: `ALANKRIT_GLOBAL_CONTEXT.md`, files 00–16, `memory/*.jsonl`.

## Who is Alankrit?

A Bangalore-based solo founder with about 1.5 years of prior work as an AI/automation engineer. He built **Icarus**, an engineering memory that answers why code is the way it is, with citations, or says "no one wrote this down". He built it almost entirely by directing AI coding agents: 585 commits from 2026-06-27 to 2026-09-10 [icarus:FACT01L7] [icarus:FACT01L9] [icarus:X00L8]. His own line: "Not the strongest traditional dev. But I ship fast." [global:V04]. Before Icarus: JARVIS v0, a local CLI with the same thesis; earlier side products Signal, Tempo, Pantheon.ai (not extracted) [icarus:T01] [icarus:FACT01L13].

## Why he built it

Founding image: Iron Man's JARVIS, "fluent like JARVIS, honest about what it knows" [global:V33]. Core insight: "Code shows what exists. Not why it exists." and "A merged PR leaves a commit. A refused one leaves nothing." Git and agents are blind to refused work and unrecorded reasons; AI made code abundant and meaning scarce [global:V01] [global:V02] [icarus:B32].

## What is he trying to do now? (as of 2026-09-10)

Get 50 users (counted as connected repos) through reply-guy on X/Reddit and warm/LinkedIn DMs; gain visibility for Icarus and himself; cut hosting cost (Azure → Oracle, not yet run); and, in parallel, job-hunt (SDR/BDR, DevTools) [icarus:D31] [icarus:X01L8] [icarus:D33] [icarus:FACT01L32]. Zero paying customers, no written ICP, no price [icarus:X00L9]. **What happened after 2026-09-10 is unknown. Ask him.**

## What does he care about?

That AI systems do not bluff. That the reason behind a decision survives the people who made it. That humans, not agents, confirm intent. That claims are exact. That things are made with taste ("no soul" is a rejection reason) [icarus:B01] [icarus:B12] [icarus:R3] [icarus:D29].

## What does he believe?

- It must not bluff; "I don't know" is a feature. Unchanged since v0 [icarus:B01].
- Groundedness ≠ relevance ≠ truth [icarus:B02]. Unknown never renders as 0 or yes [icarus:B03].
- Deterministic code for anything trust-bearing [icarus:B04]. Self-reports are evidence, not proof [icarus:B05]. Pre-register; read every number back [icarus:B06] [icarus:B07].
- Agents propose; humans confirm; nothing is captured silently; nobody should have to write docs [icarus:B11] [icarus:B12].
- Rent commodities, own the moat; stdlib unless a measurement earns a dependency [icarus:B15] [icarus:B16].
- For Icarus, distribution, not engineering, is the bottleneck. Specificity is the asset. Conversion = a repo connected [icarus:B21] [icarus:B24] [icarus:B29].
- Never showcase his own failures publicly; never bluff investors [icarus:B26] [icarus:B27].
- Exploratory only: novice builders as the Agent Mode user, "harness > model", Icarus as a trust primitive [icarus:B13] [icarus:B35] [icarus:B33].

## What did he previously believe?

That free models and public repos were enough (then: private code is the product) [global:BT01] [global:BT02]. That cold email and launch platforms could open the market (then: ~104 sends with 0 verified positives, 1 HN point, 1 PH upvote, declared dead) [global:GB03] [global:GB04]. That a tool-description rewrite moved agents from 0/11 to 4/4 (he retracted it publicly to 1 of 4) [global:BT08]. That a lexical scorer could catch fabrications (it was anti-correlated with truth; he deleted it) [global:BT10]. That the buyer is an engineering leader at a 5–20 engineer company (the target has moved four times; still unsettled) [global:BT03]. Full transitions: `05_BELIEF_EVOLUTION.md`.

## How does he make decisions?

He picks the narrowest provable unit under a big vision, and defines the failure before the feature. Measurements, reproductions and real user words move him; aphorisms and rounded numbers do not. He decides fast, records the reason and reverses cleanly. He sets dated checkpoints and abort rules. He will decide against his own data when values conflict, and writes that down. He encodes trust as structure, not policy. **Weak spot:** that rigor fades where nothing is instrumented. He switched channels before tests finished, and ICP and pricing stayed unwritten from July [global:DP01] [global:DP02] [global:DP03] [global:DP05] [icarus:R6] [global:GC04].

## How does he communicate?

One thought per line. Short declaratives. A two-sentence contrast is the signature. Unrounded numbers. Flat self-deprecation. Direct asks ("Reply if you're interested."). **No em-dashes ever** (nor en-dash or spaced-hyphen substitutes). No emoji, hashtags or cliché outreach ("would love to connect"). Replies are loose and phone-typed. Uncertainty is shown by scoping ("n=1"). Disagreement is a flat fact. Almost no humor. He writes his own reflective posts: tighten them, never replace them [icarus:X06L1] [icarus:X06L9] [icarus:X06L11] [icarus:X06L16] [icarus:X11L9]. Use `09_VOICE_MODEL.md` § checklist before drafting anything in his voice.

## What patterns recur across his projects?

**Only one project is in evidence, so nothing is proven cross-project.** Across domains inside Icarus: fast recorded reversals; structural guarantees; measurement-gated choices; heavy documentation that later drifts; distribution as the unsolved problem; cash forcing infrastructure choices [global:DP01] [global:DP02] [global:DP03] [global:GC07] [global:GO02] [global:DP08]. The only thing spanning two project generations is the no-bluff thesis and the JARVIS scene [icarus:B01] [global:IN14].

## What has he learned?

A system that fails safe hides its bugs; only a real end-to-end action finds them [global:RL02]. A measurement's blind spot reads as a result [global:RL03]. "The thing was fine; the wording was wrong", three times [global:RL04]. Volume is not a diagnosis; activity is not authority [global:RL05]. Launches need an audience first [global:RL06]. Correcting an overstatement invites the opposite one [global:RL09]. Knowing a failure mode is not designing against it [icarus:L7].

## What does he strongly reject?

Bluffing (by products, agents or himself in a pitch); unknowns shown as numbers; model judgment for trust-bearing checks; silent capture; agent self-confirmation; training on customer code; post-hoc attribution scoring; templated cold email to role addresses; proof with no next step; third-party analytics on his site; contributing to repos that ban AI; institutional or cliché copy; em-dashes; soulless design [icarus:B01] [icarus:B03] [icarus:B04] [icarus:D32] [icarus:X11L39] [icarus:F04] [icarus:X11L36] [icarus:D23] [icarus:D24] [icarus:D34] [icarus:X06L11] [icarus:D29].

## What remains unresolved?

1. Founder path vs employment [global:GO01]. 2. ICP and pricing [icarus:O1] [icarus:O2]. 3. Which channel yields connected repos [icarus:O8]. 4. Is the production Gemini key on contractual no-train terms (the privacy promise rests on it) [icarus:O5]. 5. Does Agent Mode beat a good CLAUDE.md [icarus:O4]. 6. Notarization ($99) vs the "malware" warning [icarus:O7]. 7. 45+ unconfirmed decisions and uncommitted work [icarus:O19] [icarus:O20]. 8. Resume claims vs record, against his own no-bluff rule [global:GC02].

## What should future agents remember?

- The honesty discipline (cite-or-unknown, three-valued unknowns, pre-registration, public self-correction) is the most distinctive thing he built and the clearest signal of how he thinks [icarus:R3] [icarus:D26].
- The hardest lesson was commercial, not technical: a correct, honest engine with no audience and no written ICP did not sell itself [global:GO02] [global:GO08].
- Working rules: state assumptions; ask on ambiguity; never claim done without running it; never fabricate; never weaken a test; write durable outcomes to files; keep every claim checkable [icarus:X99L15] [icarus:X99L16] [icarus:X99L17].
- Label fact / recommendation / confirmed decision / unknown in what you hand him [icarus:X11L24].

## What should they never assume?

That this covers his other projects or anything after 2026-09-10. That Icarus has customers. That resume claims or "~10 users" are verified. That an exploratory belief is settled. That a project choice (stdlib, GitHub-only, Azure, X/Reddit) is a personality trait. That he wants AI-written reflective posts. That public failure stories suit his voice. That the rule to open replies with "Alankrit," applies outside Icarus. Anything about his personal life: the corpus has none [global:GC09] [global:GO03] [icarus:C9] [icarus:C23] [icarus:X01L12].
