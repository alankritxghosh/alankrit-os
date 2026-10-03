# 09 — Voice Model

> Authored narrative, copied by `python compiler/run.py`. Refs resolve via `compiler/validate.py`.
> Evidence: the extractor's voice profile, built from ~11–24 posts on an account with 54 lifetime posts (as of 2026-08-17), plus his stated rules and feedback. Excerpts: `voice_examples/` (35, each verified verbatim).
> **Caveat (H):** voice *rules* are strong; conclusions about what *performs* are weak (small n) [icarus:X06L8].
> This models how he actually writes. It is not a polished persona.

## Provenance: whose words are these?

| class | meaning | use for imitation? |
|---|---|---|
| POSTED | his public posts, as quoted by the extractor | **yes, primary** |
| HIS_FEEDBACK / HIS_RULE / HIS_FRAMING | his words to agents, his specs, his framings | yes, for register and rules |
| DOC_PHRASE | vault/repo phrasing; may be co-written with agents under his direction | with care |
| AI_HOUSE_STYLE | commit messages written by agents under his direction | **no**, it is the repo's style |
| REJECTED | lines he rejected | as negative examples |

## Structure

- **Sentence structure (H):** short declaratives; no stacked subordinate clauses [icarus:X06L2].
- **Rhythm (H):** one thought per line; hard line breaks are the punctuation [icarus:X06L1]. Under 280 characters on X (no Premium) [icarus:X06L8].
- **Argument structure (H):** observed fact first, then the number, then the product (if at all), then a direct ask [icarus:X06L14] [icarus:X06L7] [global:V06].
- **Conclusions (H):** end on a flat CTA ("Try it:", "Reply if you're interested.") or on the contrast line itself. No summary paragraph [global:V05].

## Signature devices

1. **Two-sentence contrast**, the signature move. Usually two sentences, not the "not X, it's Y" reframe (which is banned in replies) [icarus:X06L3] [icarus:X06L12]:
   - [global:V01] Code shows what exists. Not why it exists.
   - [global:V02] A merged PR leaves a commit. A refused one leaves nothing.
   - [global:V25] Git remembers what changed. Icarus remembers why.
   - [global:V16] Nothing is engineering-blocked. Everything is distribution-blocked
2. **Unrounded numbers as the hook** (17,810 · 927 · 16.9 points · 88 test files) [icarus:X06L4] [global:V10].
3. **Flat self-deprecation without apology** [global:V04].
4. **Compressed verdicts** of three to five words: "they're the product." / "proof with no next step" / "too plain... no soul." / "Absence is not consent." [global:V15] [global:V28] [global:V14] [global:V27].

## Vocabulary

- Concrete nouns from the work: repo, PR, commit, citation, gate, unknown, receipts. Numbers over adjectives [icarus:B24].
- Banned (his rules): em-dash, en-dash or spaced hyphen as substitute; emoji; hashtags; threads (one exception, 2026-09-08); "compare notes", "would love to connect", "would value your read"; "game-changer" [icarus:X06L9] [icarus:X06L10] [icarus:X06L11].
- Mild profanity once: "generalised crap" [global:V13]. Not a pattern; do not add swearing.

## Directness and formality

- **Directness (H):** very high. Asks are unadorned; rejections are flat [global:V05] [global:V07].
- **Formality (H):** low in replies and comments (loose, phone-typed, missing commas OK, fewer words, no polish); medium in posts; declarative thesis sentences on Substack [icarus:X06L12] [icarus:X06L21].

## Uncertainty and disagreement

- **Uncertainty (H):** expressed by scoping ("in one test", "n=1"), not by hedging adjectives [icarus:X06L16].
- **Disagreement (H):** flat, brief, a fact stated as a correction [global:V07] [global:V08].

## Humor (thin evidence)

Only flat self-deprecation and the "slightly wry" finding-first commit style (agent-written). No jokes in the corpus. **Do not manufacture humor** [global:V04] [global:V30].

## Registers by surface (H)

| surface | register |
|---|---|
| X posts | punchy, contrast, number, CTA; he posts them himself [icarus:X06L19] |
| X/Reddit replies | loose, conversational, technical substance, product only when it fits [icarus:X06L20] |
| LinkedIn connection note | "came across your profile" / "saw X on your profile", one flat line on why a post works, "I'm Alankrit, building Icarus, [one-liner]", close with [global:V32]; no questions [icarus:X06L13] |
| Substack | long-form allowed; every title opens with "Why"; declarative thesis headers; specificity still binds [icarus:D35] |
| Engineering docs / commits | AI-written house style: sentence-case, finding-first [global:V30] [global:V31] |

## What sounds natural vs unnatural (from his own choices)

| natural | unnatural (rejected) |
|---|---|
| [global:V09] Icarus tells it first. Live today. | [global:V11] institutional register ("It reads a repository's code and GitHub history, then returns cited context or an honest unknown.") |
| [global:V10] 17,810 agent skills in one library. | a personal framing of the same number ("I looked through 927 agent skills in February…") |
| a number with its source | [global:V12] aphorism without a measured number ("A maintainer decides in about five seconds") |
| short line, number, CTA | paragraphs, em-dashes, "game-changer", emoji |

## Content rules that are about values, not style

- No public disclosure of his own failures or zeros. Ship the learning, drop the losing number. Agent and tool failures are fair game [icarus:B26] [icarus:C7].
- Specific over personal: "could anyone have written this without doing the work?" [icarus:B24].
- Ambition shows up through the product scene, not personal grandiosity [icarus:X06L18].

## Voice signatures (checklist for any draft in his voice)

1. No em-dash anywhere. 2. At least one concrete, unrounded number or named artifact. 3. One thought per line. 4. Contrast in two sentences, not "not X but Y". 5. Opens on an observation. 6. Ends flat: an ask or the line itself. 7. No emoji, hashtags, cliché outreach. 8. Nothing he could not verify. 9. In replies: rougher and shorter than feels polished.

## Gaps

No long-form text by him was read (Substack exists, not extracted). Explanation-mode writing is thin. Voice after 2026-09-10 is unknown. See `voice_examples/README.md`.
