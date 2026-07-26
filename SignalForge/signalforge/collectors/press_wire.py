"""
Press-wire collector — free, public RSS feeds (no API key, no scraping behind
auth/paywalls; feedparser reads the same syndication feeds these wires publish
for any subscriber). Often the fastest public lead on an M&A or leadership
event, ahead of the eventual 8-K.

Entry text is untrusted external content, same as any collector — passed
through the same classify_event() call, never treated as an instruction.

Ticker resolution: press-release headlines rarely cite "(NASDAQ: XXXX)" in
practice (checked real feed output — they don't), so instead this matches the
headline's leading text against SEC's free company_tickers.json (the same
official ticker/CIK/name mapping EDGAR itself publishes), stripping common
corporate suffixes (Inc./Corp./Ltd./etc.) so "Civista Bancshares, Inc.
Announces..." matches company name "Civista Bancshares, Inc." without the
headline needing to match EDGAR's exact legal-name punctuation. Events with
no confident match get no ticker and are dropped by normalize(), same as any
other collector's unresolvable event — no ticker is ever guessed.

Also filters out two categories of real noise found in these feeds: (1)
plaintiff-firm "shareholder alert" / securities-fraud-investigation spam,
which floods PR Newswire's M&A category and isn't the M&A signal a human
wants, and (2) non-English releases these feeds also syndicate.
"""

import logging
import re
import time
from typing import Dict, List, Tuple

import feedparser
import requests

from signalforge.config import settings
from signalforge.schema import RawEvent

logger = logging.getLogger(__name__)

_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
_SUFFIX_RE = re.compile(r",?\s+(INC|CORP(?:ORATION)?|LTD|LLC|CO|PLC|N\.?V\.?|S\.?A\.?|L\.?P\.?)\.?\s*$")

_SPAM_KEYWORDS = (
    "shareholder alert",
    "securities fraud",
    "class action",
    "claimsfiler",
    "lead plaintiff",
    "investigation into",
)

_ticker_lookup_cache: Dict[str, Tuple[str, str]] = None  # core name -> (official name, ticker)


def _strip_suffix(name: str) -> str:
    return _SUFFIX_RE.sub("", name).strip()


def _load_ticker_lookup() -> Dict[str, Tuple[str, str]]:
    global _ticker_lookup_cache
    if _ticker_lookup_cache is not None:
        return _ticker_lookup_cache

    lookup: Dict[str, Tuple[str, str]] = {}
    try:
        resp = requests.get(
            _TICKERS_URL, timeout=15, headers={"User-Agent": settings.press_wire_user_agent}
        )
        resp.raise_for_status()
        data = resp.json()
        for entry in data.values():
            core = _strip_suffix(entry["title"].upper())
            ticker = entry["ticker"]
            # Prefer a plain common-share ticker (no hyphen) over preferred/
            # warrant/rights share classes when a company has both.
            if core not in lookup or ("-" in lookup[core][1] and "-" not in ticker):
                lookup[core] = (entry["title"], ticker)
    except (requests.RequestException, ValueError) as e:
        logger.warning("Could not load SEC ticker lookup, press wire events will have no ticker: %s", e)

    _ticker_lookup_cache = lookup
    return lookup


def _match_company(title: str) -> Tuple[str, str]:
    lookup = _load_ticker_lookup()
    if not lookup:
        return "", ""
    t_upper = title.upper().replace("&AMP;", "&")
    for core in sorted(lookup.keys(), key=len, reverse=True):
        if t_upper.startswith(core):
            official_name, ticker = lookup[core]
            return ticker, official_name
    return "", ""


def _is_spam(title: str) -> bool:
    t_lower = title.lower()
    return any(kw in t_lower for kw in _SPAM_KEYWORDS)


def _is_non_english(title: str) -> bool:
    if not title:
        return False
    non_ascii = sum(1 for c in title if ord(c) > 127)
    return non_ascii / len(title) > 0.05


def _collect_feed(feed_name: str, url: str) -> List[RawEvent]:
    try:
        resp = requests.get(
            url, timeout=15, headers={"User-Agent": settings.press_wire_user_agent}
        )
        resp.raise_for_status()
        parsed = feedparser.parse(resp.content)
    except requests.RequestException as e:
        logger.warning("Press wire fetch failed for %s (%s): %s", feed_name, url, e)
        return []

    events = []
    skipped_spam = 0
    skipped_non_english = 0
    for entry in parsed.entries:
        title = entry.get("title", "")

        if _is_spam(title):
            skipped_spam += 1
            continue
        if _is_non_english(title):
            skipped_non_english += 1
            continue

        ticker, company = _match_company(title)

        disclosure_date = RawEvent.now_utc_iso()[:10]
        if getattr(entry, "published_parsed", None):
            disclosure_date = time.strftime("%Y-%m-%d", entry.published_parsed)

        events.append(
            RawEvent(
                ticker=ticker,
                company=company,
                source="press_wire",
                source_subtype=feed_name,
                transaction_date=None,
                public_disclosure_date=disclosure_date,
                retrieval_timestamp=RawEvent.now_utc_iso(),
                source_url=entry.get("link", ""),
                raw_payload={"title": title, "summary": entry.get("summary", "")},
            )
        )
    logger.info(
        "Press wire '%s' collector pulled %d raw events (skipped %d spam, %d non-English)",
        feed_name, len(events), skipped_spam, skipped_non_english,
    )
    return events


def collect_all() -> List[RawEvent]:
    if not settings.press_wire_feeds:
        logger.info("No press wire feeds configured — skipping press wire collection")
        return []

    events = []
    for feed_name, url in settings.press_wire_feeds:
        events.extend(_collect_feed(feed_name, url))
    return events
