# 07 — Voice Profile: Icarus

## Authorship first (this changes the v1 profile)

The v1 profile was built from posted X content, and much of that was **agent-drafted text he selected**, not his own writing.
In the transcripts, a block beginning `<!-- attach -->` followed by `>` lines is text he quoted from the assistant's output. Examples:

| text | author | his act | ref |
|---|---|---|---|
| "Watched a coding agent about to write a patch two people had already had rejected. … A merged PR leaves a commit. A refused one leaves nothing. Icarus tells it first. Live today." | ASSISTANT draft | selected and posted ("Posted this") after rejecting other drafts | `S:c1cd1bc4@08-14T21:45` |
| "I build a thing a coding agent can call … 0 calls in 11 tasks, then 4 of 4." | ASSISTANT draft | "went with this instead" | `S:3146f729@08-22T17:52` |
| Product Hunt launch post ("After 2 months of building, Icarus is finally live on Product Hunt. …") | ASSISTANT draft built to his spec | edited and posted | `S:331ba684@09-01T07:03` |
| "The hardest part of building Icarus hasn't been engineering. / It's spending an entire day working and still feeling like you accomplished nothing." | **ALANKRIT** | "I posted it as it is, none of your posts got used" | `S:98f3787d@09-04T08:33`, `08:37` |
| "I tried out GPT-6 Astra, asked it to build me a city with a dark art deco aesthetic, something with a more 1940 Manhattan look, and it wrote the whole thing in python … Crazy how far AI has gotten." | **ALANKRIT** | his rewrite of a rejected draft ("horrid writing") | `S:e0e8aab2@09-07T15:24` |
| "I spoke to an engineer friend of mine today, about icarus and I got to know that the company she is working for is also building a product just like Icarus, initially it seemed quite intimidating …" | **ALANKRIT** (raw; he asked for a sub-280-char cut) | "Here is the post in my words" | `S:6bc55771@08-25T19:43` |
| Message to co-founder candidate ("I built it alone … The product works. My distribution does not. … Worth a call?") | sent by ALANKRIT; drafting UNKNOWN | he sent it | `S:8e8c6d02@08-11T20:15` |

**His description of his own writing (ALANKRIT, `S:e0e8aab2@09-07T15:24`):** "This is how I write things, simple but actually follow through with a chain of thought and a story". Elsewhere: "it must be humanised with a chain of thought visible in the writing" (`S:2bd25f86@09-10T08:06`).

**Short imperative commands may be accepted prompt suggestions.** Messages like "ship it — deploy the brain and bump the dmg" and "go — stage 1, red→green" carry em-dashes his composed writing never uses. The choice is his; the wording may be the agent's. Do not model his voice from terse commands.

## Register 1: private chat with agents (ALANKRIT; 1,317 unique typed messages)

Measured on de-duplicated typed messages, excluding pasted or attached agent text:
- **Length:** median 47 characters. Bursts of short commands, punctuated by occasional long run-on paragraphs when he thinks aloud.
- **Case and punctuation:** 58% start lowercase; sentences joined with commas; question marks often dropped; "???" when exasperated. Typos common: "atleast", "upto", "hobbiests", "neede", "nwo", "runit", "do itt". Composed text has no em-dashes (the 12 that appear are pasted agent text or suggestion chips).
- **Vocabulary markers:** "lets" (107), "Well" (59), "Alright" (31), "Okay" (19), "I suppose" (13), "reckon", "do the needful", "Buddy", "my god", "for fuck sakes". British/Indian-English idiom.
- **Profanity:** genuinely present and frequent under frustration: "fuck" ×36, "hell" ×10, "shit" ×6, "crap", "bloody". Eight mostly-capitals messages, nearly all angry ("WHAT THE ACTUAL FUCK IS WRONG WITH YOU", 07-15; "WHY THE FUCK DID YOU RESTART INGESTION WHO THE FUCK ASKED YOU TO DO IT? ARE YOU FUCKING STUPID?", 09-09). Insults go at the agent ("are you slow?", "your context is fuck all"), and once an ableist slur about a third party (09-05, not reproduced here).
- **Analogies, blunt and social:** "IS THIS A NEW STUDY BUDDY" (07-15); "I am not talking to a girl I am trying hook up with, this is business" (09-10); "Introduce him to Icarus like he is an unaware idiot" (09-04); "try framing it as speaking with a child you are trying to sell" (09-05); "explain … like I am non technical founder, with 0 understanding about tech, and I am extremely stupid" (07-27).
- **Uncertainty:** "I suppose", "I guess", "I don't know", "I think", plus direct questions to the agent. He doesn't hedge with adjectives.
- **Disagreement:** immediate and flat ("No", "Nope", "this is horrid", "they all suck", "Absolutely not have you not learnt anything"). Often followed in the same message by the exact fix he wants.
- **Self-disclosure in chat:** "I am just a tad intimidated by the mere fact that two months ago there was nothing here" (08-25); "I want to sleep how much time will it take?" (08-04); "I havent slept the whole night" (08-09).
- **Argument structure:** a goal stated plainly ("I want…", ~frequent), then constraints, then an open question ("how do you propose we do this").
- **Ambition:** stated directly in chat ("I want to build a brain an intelligence system a tech company would be foolish not to have in use"); rarely in public.

## Register 2: public writing (his own and the drafts he approved)

- **His own (ALANKRIT):** plain first-person story with a chain of thought, a single reflection at the end, light punctuation, no em-dashes ("Crazy how far AI has gotten."). More personal and less clipped than the drafts he approves.
- **Approved drafts (ASSISTANT, chosen by him):** one thought per line; two-sentence contrast ("A merged PR leaves a commit. A refused one leaves nothing."); unrounded numbers; flat CTA. This register was shaped by his edits and rules but written by agents.

## Rules he set (ALANKRIT, repeated)

- **No em-dashes**, stated ≥10 times: "No, I dont want emdashes, type it out like a human is typing, have typos" (08-11); "Stop adding emdashes to anything that is written in my voice … I don't want to waste credits reminding you the same thing over and over again" (09-03).
- **Imperfect, human punctuation:** "there can be typos, not spelling errors … you cannot use the IT IS X NOT Y framing" (09-07); "missed commas … typed on the phone via a regular chain of thought" (09-07).
- **Length limits:** under 280 characters on X (no Premium); under 200 (later 180) for LinkedIn notes.
- **No cliché outreach:** "DO NOT EVER USE THIS COMPARE NOTES CTA OR SOMETHING AS CLICHE AS THAT THIS IS NOT A LINKEDIN OUTREACH 101 CLASS, BE AUTHENTIC." (09-04).
- **Not "cheesy"; business register for connection notes:** open with "I saw X on your profile" / "I came across your profile"; one line on why a post works; "I am Alankrit and I am building Icarus"; end "you seem like a good conversation to have, so let's connect" (09-10).
- **Never showcase failures publicly** (08-17). **Substack titles start with "Why"** (08-23). **Lead with a specific number, not a vague personal frame** (08-17).

## Natural vs unnatural

| natural (his) | unnatural (rejected by him) |
|---|---|
| plain story + chain of thought, one reflection | polished, "too AI generated", "screams fucking AI" |
| short, lowercase-tolerant, small typos | "pitch perfect punctuations" |
| direct ask, business-like | "cheesy" warmth ("been thinking about X for a few days") |
| specific numbers and names | "generalised crap", "AI generic" |
| no em-dashes | em-dashes; "it is X not Y" reframes |

## Voice signatures

1. Starts with what happened ("I tried out…", "I spoke to…", "Watched…"). 2. Story before product. 3. One closing reflection or verdict. 4. No em-dash. 5. In chat: "Alright / Well / lets / I suppose". 6. Anger in capitals with profanity, then a precise instruction.

## Caveats

The public sample is small (account ~54 lifetime posts as of 08-17; ~14–17 followers in late August). The private register is large (1,317 messages) but is instruction-giving to agents, not writing for an audience. Only a handful of examples are both his own words and public. See `voice_examples/`.
