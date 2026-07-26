"""
Twitter/X collector — added after Phase 1 at Hunter's explicit request; the
original CLAUDE.md brief listed social/sentiment collectors as future-phase
scope. See the brief's changelog note for when/why that changed.

Pulls recent public posts matching TWITTER_SEARCH_QUERY via the X API v2
recent-search endpoint. Requires TWITTER_BEARER_TOKEN (app-only auth).

Post text is untrusted external content, same as any scraped filing or
article — it is never treated as an instruction, only as data passed through
the same classify_event() call every other collector uses.

Docs: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent
"""

import logging
import re
from typing import List

import requests

from signalforge.config import settings
from signalforge.schema import RawEvent

logger = logging.getLogger(__name__)

SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"
_CASHTAG_RE = re.compile(r"\$([A-Za-z]{1,5})\b")


def _extract_ticker(text: str) -> str:
    m = _CASHTAG_RE.search(text or "")
    return m.group(1).upper() if m else ""


def collect_all() -> List[RawEvent]:
    if not settings.twitter_bearer_token:
        logger.info("TWITTER_BEARER_TOKEN not set — skipping Twitter collection (expected in early testing)")
        return []

    headers = {"Authorization": f"Bearer {settings.twitter_bearer_token}"}
    params = {
        "query": settings.twitter_search_query,
        "max_results": 25,
        "tweet.fields": "created_at,author_id",
    }
    try:
        resp = requests.get(SEARCH_URL, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        tweets = resp.json().get("data", [])
    except requests.RequestException as e:
        logger.warning("Twitter search request failed: %s", e)
        return []

    events = []
    for tweet in tweets:
        text = tweet.get("text", "")
        ticker = _extract_ticker(text)
        tweet_id = tweet.get("id", "")
        events.append(
            RawEvent(
                ticker=ticker,
                company="",
                source="twitter",
                source_subtype="tweet",
                transaction_date=None,
                public_disclosure_date=(tweet.get("created_at") or RawEvent.now_utc_iso())[:10],
                retrieval_timestamp=RawEvent.now_utc_iso(),
                source_url=f"https://x.com/i/web/status/{tweet_id}" if tweet_id else "",
                raw_payload={"text": text, "author_id": tweet.get("author_id", "")},
            )
        )
    logger.info("Twitter collector pulled %d raw events", len(events))
    return events
