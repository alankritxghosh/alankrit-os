# Substack research brief, 2026-10-05 (DRAFT, not published)

Status: sources below were seen only as web search excerpts. I did not open any page (egress to linkedin.com and substack.com is blocked here, other pages were not fetched). Every claim is UNVERIFIED until Alankrit or a session with browser access opens the source and confirms it. Nothing here states anything about his own projects, numbers or opinions.

## Candidate topic

Title (policy: Substack titles are "Why" questions):
**Why do coding agents forget what they were doing?**

Why this fits his lane: coding agents, context and memory. It needs his own raw material before it is publishable: a real moment where an agent lost the plot in his work. I have none on record, so the piece below is a skeleton that needs his story in section 1.

## Spine of the piece

1. His moment (HIS WORDS NEEDED): a specific session where an agent forgot a decision or repeated a mistake.
2. Context rot. Chroma's report tested 18 frontier models and says every one gets worse as input length grows, even on simple tasks. Source: https://www.trychroma.com/research/context-rot (excerpt only, verify).
3. Compaction loses the "why". One paper describes compaction summarising away the connective tissue of long arcs, so the plan survives and the reasoning does not. Source: https://arxiv.org/pdf/2609.05510 (excerpt only, verify).
4. Memory that only appends rots. Same line of work says append-only memory collects duplicates, stale advice and contradictions, and that writes should be add, update, merge, supersede or reject. Sources: https://arxiv.org/pdf/2609.05510, https://arxiv.org/html/2609.32091v1 (excerpts only, verify).
5. What he does about it (HIS WORDS NEEDED). He already runs a file-based context setup (CLAUDE.md, memory/ jsonl files). Any claim about how well it works needs his numbers or his say-so.
6. Close: one question for readers.

Other leads seen in search, not read: Snowflake ArcticMem blog, Cloudflare Agent Memory announcement, Oracle "agent memory amnesia" post, Mem0 guide.

## Spin-off posts (drafts, voice checked by hand only)

Each is a seed for Alankrit to reshape with his raw words. X under 280 characters.

X-1:
every model in that Chroma test got worse as the input got longer
all 18 of them
so the long session you keep nursing is the worst place to ask for something hard

X-2:
compaction keeps the plan and drops the why
that is the part I would want back after a long agent run

X-3:
append-only memory for an agent sounds fine until week three
duplicates, stale advice, two notes that disagree
who cleans that up?

LinkedIn-1 (needs his story before use):
Append-only memory piles up stale advice and contradictions, according to one paper on agent memory.
Should an agent be allowed to delete its own notes?
(First draft had a "not X, Y" reframe and claims about him. Both removed.)

## Before any of this goes out

- Open and confirm every cited source and number.
- Add his real moment and his real setup, in his words.
- Run `python3 -m brand_agents.daily replies`-style checks on final text (no dashes, hashtags, emoji, links in replies).
