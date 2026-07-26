"""
Macro calendar collector — free, official RSS feeds (BLS, Federal Reserve).

Deliberately does NOT flow through normalize()/classify_event(): those assume
a single affected ticker and one of the 5 company-event categories (CLAUDE.md
says not to add categories until Phase 1 has run long enough to judge the
existing five). A CPI print or FOMC statement affects the whole market, not
one ticker, and doesn't fit "insider_conviction" or "leadership_transition" —
forcing it through that pipeline would mean either a fake ticker or a
misclassified category, both worse than a separate simple path. See main.py's
_run_macro() for how these get deduped and alerted instead.

Entry text is untrusted external content, same as any collector — never
treated as an instruction, only ever passed through as plain data.
"""

import logging
import time
from typing import List

import feedparser
import requests

from signalforge.config import settings
from signalforge.schema import RawEvent

logger = logging.getLogger(__name__)


def _collect_feed(feed_name: str, url: str) -> List[RawEvent]:
    try:
        resp = requests.get(
            url, timeout=15, headers={"User-Agent": settings.press_wire_user_agent}
        )
        resp.raise_for_status()
        parsed = feedparser.parse(resp.content)
    except requests.RequestException as e:
        logger.warning("Macro feed fetch failed for %s (%s): %s", feed_name, url, e)
        return []

    events = []
    for entry in parsed.entries:
        title = entry.get("title", "")
        disclosure_date = RawEvent.now_utc_iso()[:10]
        if getattr(entry, "published_parsed", None):
            disclosure_date = time.strftime("%Y-%m-%d", entry.published_parsed)

        events.append(
            RawEvent(
                ticker="MACRO",
                company="",
                source="macro",
                source_subtype=feed_name,
                transaction_date=None,
                public_disclosure_date=disclosure_date,
                retrieval_timestamp=RawEvent.now_utc_iso(),
                source_url=entry.get("link", ""),
                raw_payload={"title": title, "summary": entry.get("summary", "")},
            )
        )
    logger.info("Macro feed '%s' collector pulled %d raw events", feed_name, len(events))
    return events


def collect_all() -> List[RawEvent]:
    if not settings.macro_feeds:
        logger.info("No macro feeds configured — skipping macro collection")
        return []

    events = []
    for feed_name, url in settings.macro_feeds:
        events.extend(_collect_feed(feed_name, url))
    return events
