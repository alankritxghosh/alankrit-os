"""Find X reply targets with a logged-in Playwright browser.

Read-only by design:
- opens search pages
- scrolls lightly
- extracts visible post text and URLs
- does not click like, reply, repost, follow, DM or post
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import quote

from typing import Any

DEFAULT_STATE = Path.home() / ".alankrit-os" / "x-storage-state.json"

DEFAULT_QUERIES = [
    '"Claude Code" ("built" OR "building") -crypto -web3 -solana -filter:replies',
    '"AI agents" ("workflow" OR "workflows") -crypto -web3 -solana -filter:replies',
    '"building with agents" -crypto -web3 -solana -filter:replies',
    '"vibe coding" ("built" OR "learned") -crypto -web3 -solana -filter:replies',
    '"GTM" "AI agents" -crypto -web3 -solana -filter:replies',
]

BLOCKED_TERMS = [
    "geopolitics",
    "election",
    "war",
    "left wing",
    "right wing",
    "dm me",
    "join my cohort",
    "book a call",
    "growth hack",
    "crypto",
    "web3",
    "solana",
    "token",
    "on-chain",
    "onchain",
    "defi",
    "airdrop",
    "nft",
    "permissionless",
    "gpu hours",
    "compute markets",
    "$",
]

HIGH_SIGNAL_TERMS = [
    "claude code",
    "ai agents",
    "agent",
    "build",
    "building",
    "built",
    "builder",
    "workflow",
    "workflows",
    "gtm",
    "startup",
    "product",
    "vibe coding",
    "cursor",
    "codex",
]


PROMO_PATTERNS = [
    r"\bcomment\s*['\u2018\u2019\"\u201c\u201d]",
    r"\bt\.me\b",
    r"\btelegram\b",
    r"\bwaitlist\b",
    r"\bgiveaway\b",
    r"\bfree guide\b",
    r"\bfollow for\b",
    r"\bbookmark this\b",
    r"\bcheat code\b",
    r"\blink in (?:bio|comments)\b",
    r"\bjoin (?:our|the) (?:community|discord|channel|group)\b",
]

FIRST_PERSON_RE = re.compile(r"\b(?:i|i'm|i\u2019m|i've|i\u2019ve|my|me)\b")

HEADER_RE = re.compile(r"^.*?@\w+\s*\u00b7\s*(?:\d+[smhd]\b|[A-Z][a-z]{2}\b)?\s*")


@dataclass
class Candidate:
    url: str
    author: str
    post_text: str
    why: str
    checked_at: str
    score: int

    def to_target(self) -> dict:
        return {
            "url": self.url,
            "opened": True,
            "checked_at": self.checked_at,
            "author": self.author,
            "post_text": self.post_text,
            "why": self.why,
            "score": self.score,
        }


def normalize_text(text: str) -> str:
    text = re.sub(r"\b(Show more|Translate post|Image|GIF|ALT)\b", " ", text)
    text = re.sub(r"\b\d+[KkMm]?\b", " ", text)
    return " ".join(text.split())


def post_url_from_article(article) -> str | None:
    links = article.locator("a[href*='/status/']")
    count = links.count()
    for idx in range(count):
        href = links.nth(idx).get_attribute("href")
        if not href:
            continue
        match = re.search(r"^/([^/]+)/status/(\d+)", href)
        if match:
            return f"https://x.com{match.group(0)}"
        if href.startswith("https://x.com/") and "/status/" in href:
            return href.split("?")[0]
    return None


def author_from_url(url: str) -> str:
    match = re.match(r"https://x.com/([^/]+)/status/", url)
    return match.group(1) if match else "UNKNOWN"


def strip_header(text: str) -> str:
    """Drop the 'Display Name @handle \u00b7 time' prefix so bios do not score as post content."""
    match = HEADER_RE.match(text)
    return text[match.end():] if match else text


def promo_reasons(text: str) -> list[str]:
    lowered = text.lower()
    hits = [pattern for pattern in PROMO_PATTERNS if re.search(pattern, lowered)]
    shouting = [word for word in re.findall(r"[A-Za-z]{4,}", text) if word.isupper()]
    if len(shouting) >= 3:
        hits.append("all-caps hype")
    return hits


def score_text(text: str) -> tuple[int, list[str]]:
    text = strip_header(text)
    lowered = text.lower()
    reasons: list[str] = []
    score = 0
    if promo_reasons(text):
        return -90, ["promo or hype post"]
    if any(term in lowered for term in BLOCKED_TERMS):
        return -100, ["blocked topic"]
    if any(term in lowered for term in ["works at", "joined ", "joining ", "hired", "we're hiring", "we are hiring"]):
        return -80, ["employment announcement"]
    if any(term in lowered for term in ["breaking:", "today's news", "live on x", "subscribe to premium"]):
        return -80, ["news/ui noise"]
    has_agent_signal = any(term in lowered for term in ["agent", "agents", "claude code", "cursor", "codex", "vibe coding"])
    has_builder_signal = any(term in lowered for term in ["build", "building", "built", "workflow", "workflows", "product", "gtm", "ship", "shipping"])
    if not (has_agent_signal and has_builder_signal):
        score -= 6
        reasons.append("missing agent+builder pair")
    for term in HIGH_SIGNAL_TERMS:
        if term in lowered:
            score += 2
            reasons.append(term)
    if "?" in text:
        score += 2
        reasons.append("question")
    word_count = len(text.split())
    if 20 <= word_count <= 180:
        score += 2
        reasons.append("commentable length")
    if word_count > 220:
        score -= 4
        reasons.append("too long")
    if any(term in lowered for term in ["i built", "i'm building", "i am building", "we built", "we are building"]):
        score += 3
        reasons.append("builder first-person")
    if any(term in lowered for term in ["learned", "mistake", "problem", "workflow", "how i"]):
        score += 2
        reasons.append("has comment hook")
    personal = "?" in text or bool(FIRST_PERSON_RE.search(lowered))
    if not personal:
        score -= 4
        reasons.append("no question or first-person angle")
    if re.search(r"@\w+", text) and not personal:
        score -= 4
        reasons.append("brand mention without personal angle")
    return score, reasons


def extract_candidates(page: Any, checked_at: str) -> list[Candidate]:
    candidates: list[Candidate] = []
    articles = page.locator("article")
    for idx in range(articles.count()):
        article = articles.nth(idx)
        url = post_url_from_article(article)
        if not url:
            continue
        text = normalize_text(article.inner_text(timeout=2000))
        if not text:
            continue
        score, reasons = score_text(text)
        if score < 6:
            continue
        candidates.append(Candidate(
            url=url,
            author=author_from_url(url),
            post_text=text[:1200],
            why=f"X search candidate; score {score}; signals: {', '.join(reasons[:6])}",
            checked_at=checked_at,
            score=score,
        ))
    return candidates


def search_url(query: str) -> str:
    return f"https://x.com/search?q={quote(query)}&src=typed_query&f=live"


def find_posts(state: Path, queries: list[str], limit: int, headless: bool, scrolls: int, channel: str | None = None) -> list[dict]:
    seen: set[str] = set()
    results: list[Candidate] = []
    checked_at = date.today().isoformat()

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, channel=channel)
        context = browser.new_context(storage_state=str(state))
        page = context.new_page()
        for query in queries:
            page.goto(search_url(query), wait_until="domcontentloaded")
            page.wait_for_timeout(2500)
            for _ in range(scrolls):
                for candidate in extract_candidates(page, checked_at):
                    if candidate.url not in seen:
                        seen.add(candidate.url)
                        results.append(candidate)
                page.mouse.wheel(0, 900)
                page.wait_for_timeout(1200)
        browser.close()
    results.sort(key=lambda item: item.score, reverse=True)
    return [item.to_target() for item in results[:limit]]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--query", action="append", help="X search query. Can be repeated.")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--scrolls", type=int, default=4)
    parser.add_argument("--headed", action="store_true", help="show browser window")
    parser.add_argument("--channel", default=None, help="browser channel, for example chrome")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    if not args.state.exists():
        raise SystemExit(f"missing storage state. Run login first: {args.state}")
    queries = args.query or DEFAULT_QUERIES
    targets = find_posts(args.state, queries, args.limit, headless=not args.headed, scrolls=args.scrolls, channel=args.channel)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(targets, indent=2) + "\n", encoding="utf-8")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
