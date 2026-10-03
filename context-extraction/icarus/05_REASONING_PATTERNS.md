# 05 — Reasoning Patterns: Icarus

Observable patterns only; no psychological diagnosis.
Columns: **observed** (what the evidence shows) and **inference** (the reading). "Origin" says whose habit it is:
- **HIS:** shown in his own typed messages.
- **JOINT:** he directs or enforces it, but agent-written docs carry the method.
- **AGENT-LED:** the method appears mainly in agent work he approved.

## Patterns re-verified from v1 (R1–R18)

| ID | pattern | observed | inference | origin | conf |
|---|---|---|---|---|---|
| R1 | Vivid end-state scene, then the narrowest provable brick | JARVIS scene since v0; Phase 1 = one repo, cited or unknown; "Wisprflow … cylindrical button" overlay brief (`S:7905c0b6@07-18T15:18`) | Vision sets direction; proof sets scope | JOINT | HIGH |
| R2 | Define the failure before the feature | gate + red baseline before UI; "prove the AST-chunking win with a red→green eval" (`S:f6d9d234@07-16T23:58`) | Correctness gate is a precondition | JOINT | HIGH |
| R3 | Precise about what a guarantee covers | gate wording; "proof read to ensure we are not lying anywhere or overstating anywhere" (`S:7440e957@08-25T12:00`) | Exactness of claims matters more than strength | JOINT | HIGH |
| R4 | A surprising good result is a bug until re-run | C2 4/4 → 1/4; 7b–7d zeros withdrawn | — | AGENT-LED, accepted by him | HIGH |
| R5 | Reverse fast, record the reversal | private repos in a day; analytics in a day; site stack in a day | Sunk cost carries little weight | HIS | HIGH |
| R6 | Persuaded by measurements, reproductions, a failing case, real user words | "I want numbers as results" (`S:e8bb2d56@08-21T12:37`); Morphic feedback acted on the same night (`S:f6d9d234@07-16`); "why are we going with these strategies show me evidence" (`S:2193ef7b@09-09T18:10`) | — | HIS | HIGH |
| R7 | Rejects generic or aphoristic content and unverifiable claims | "generalised crap"; "not fucking AI generic" | — | HIS | HIGH |
| R8 | Names the binding constraint and moves effort to it | "sales and distribution as the biggest bottle neck" (09-10); "I cannot afford the azure bill" | Constraint-first reallocation | HIS | HIGH |
| R9 | Structural guarantees over policy | signature-level guarantees; trust interlock | — | AGENT-LED | HIGH |
| R10 | "What fact would prove the property?" | mergedBy for authority; bot-filtered counts | — | AGENT-LED | MEDIUM-HIGH |
| R11 | Decides against his own data when values conflict | no public failures despite vulnerable posts performing best (D22) | Values over engagement metrics | HIS | HIGH |
| R12 | Scope narrows in engineering, broadens in distribution | channel sequence email → X → HN → PH → Reddit → LinkedIn in ~5 weeks | Rigor follows instrumentation | HIS | MEDIUM-HIGH |
| R13 | Every failure becomes a named rule with its cost | PROTOCOL; Learning entries open with "Cost:"; "I don't want the failures of the last session and attempts to repeat again" (`S:345ea254@08-11T07:46`) | — | JOINT | HIGH |
| R14 | Dated checkpoints and abort rules | "15th of september will be that day" (`S:b4e90b56@09-02T12:35`); Oracle Task 0 | — | JOINT | HIGH |
| R15 | Measurement probes before UI | "Run the abstention-rate measurement across ten real repos first" (`S:fb942d6d@07-29T10:08`) | — | HIS | HIGH |
| R16 | Unknowns kept as explicit states | Unknowns note; three-valued state | — | AGENT-LED | HIGH |
| R17 | Leverage = deterministic signals nobody else has | refused-PR signal ("build the rejected PR signal", `S:42d3afaa@08-10T13:20`) | — | JOINT | MEDIUM-HIGH |
| R18 | Speed vs rigor depends on context | rigor on honesty claims; speed on UI and launch ("WE HAVE TO FINISH ALL OF THIS TONIGHT", 08-28) | Deadlines can override protocol | HIS | HIGH |

## New patterns from the transcripts (R19–R28)

| ID | pattern | observed | inference | origin | conf |
|---|---|---|---|---|---|
| R19 | **Asks for a plain-language explanation before deciding** | ≥15 instances: "in simple words" (07-17, 07-29, 08-25), "I am not too apt with tech so I would appreciate a simpler why" (07-13), "teach me … like I am non technical founder, with 0 understanding" (07-27), "I am unable to understand what is it that we solved now … simplify this for me" (07-29) | He evaluates by user-visible effect, not implementation | HIS | HIGH |
| R20 | **Decides by picking from agent-proposed options in very few words** | "do 1 and 2", "A it is", "option A", "go with option 2", "B", "start with 3A, then 2A" | The agent drafts the alternatives; he selects. Alternatives in the record are often the agent's | HIS | HIGH |
| R21 | **Reasons from the user's experience** | "what will Icarus look like to a basic user?" (07-29); "what is it that they do?" after the site (08-26); "Give me a run through of how a lead will go ahead and install" (08-11) | UX is his main test of progress | HIS | HIGH |
| R22 | **Benchmarks against leaders and references** | "a company like AWS or Microsoft were trying to solve, how would they index" (07-16); "How do things like claude code, cursor and codex do it" (08-10); Wispr Flow, Perseus, Raycast, Obsidian ("copy obsidian shamelessly", 09-02), Apple launch videos | Borrows proven patterns; taste is calibrated on best-in-class | HIS | HIGH |
| R23 | **Tests the product himself and reports bugs as experiences** | "this is quite embarrassing" (07-14); "DO I HAVE TO ASK ALL PERMUTATIONS" (08-06); "How the hell do I use the extension ?" (08-06) | The founder as first user is his QA | HIS | HIGH |
| R24 | **Time-boxes hard** | "user friendly product in a matter of 3 days" (07-29); "before 7pm ist that gives us 4 hours" (08-28); "it need not take 10 to 12 hours … 2 hours max" (08-10) | Momentum over completeness under pressure | HIS | HIGH |
| R25 | **Counts agent credits as a real cost** | "since we are short on credits" (07-23); "BURNING CREDITS AND TOKENS" (08-17); "we will run out of usage credits not even halfway" (08-28) | Agent compute is a binding resource | HIS | HIGH |
| R26 | **Ambition jumps to maximal scope** | "I want all languages to be done perfectly" (07-17); "index atleast a vast majority of codebases on earth" (08-10); "full scale business, an actual startup" (08-24); "agent mode to pass all the benchmark tests" (08-24) | Ambition outruns the evidence; agents translate it into bricks | HIS | HIGH |
| R27 | **Diagnoses his own position against the market** | "Every real dev we try to sell to will already have an internal tool like this" (09-05); "we currently are unknown nothing matters" (07-27) | Market reasoning arrives in short, decisive statements, usually without data | HIS | MEDIUM-HIGH |
| R28 | **Uses parallel agents and models, and relays between them** | pastes Codex reviews into Claude; "Create a PR … for codex to review" (08-08); "gpt 5.6 sol High to review it" (09-03); identical prompts sent to 2–3 sessions at the same minute (07-29, 08-08) | Adversarial or redundant multi-agent checking; why identical prompts went to parallel sessions is UNKNOWN | HIS | HIGH (behavior) / UNKNOWN (intent) |

## Under uncertainty / after failure

- **Uncertainty:** delegates the research ("Research and tell me …"), then asks for evidence ("show me evidence"). In public, scopes claims ("in one test").
- **Failure:** first frustration, often profane and in capitals. Then a concrete instruction within minutes, e.g. "Okay the private repos work for now" (07-15) after the outburst. Lessons then get written into the vault by agents.
- **Revisiting assumptions:** fast on product and UX; slow on business fundamentals (ICP and pricing open since 07-16).
