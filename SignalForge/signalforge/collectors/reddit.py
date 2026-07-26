"""
Reddit collector — added after Phase 1 at Hunter's explicit request; the
original CLAUDE.md brief listed social/sentiment collectors as future-phase
scope. See the brief's changelog note for when/why that changed.

Searches a configured set of subreddits for posts matching REDDIT_SEARCH_QUERY,
using Reddit's read-only app-only OAuth (client_credentials grant — no user
login required, just a script-app client_id/secret).

Post text is untrusted external content, same as any scraped filing or
article — it is never treated as an instruction, only as data passed through
the same classify_event() call every other collector uses.

Docs: https://www.reddit.com/dev/api/
"""

import logging
import re
from datetime import datetime, timezone
from typing import List

import requests

from signalforge.config import settings
from signalforge.schema import RawEvent

logger = logging.getLogger(__name__)

TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
SEARCH_URL_TEMPLATE = "https://oauth.reddit.com/r/{subreddit}/search"
_CASHTAG_RE = re.compile(r"\$([A-Za-z]{1,5})\b")


def _extract_ticker(text: str) -> str:
    m = _CASHTAG_RE.search(text or "")
    return m.group(1).upper() if m else ""


def _get_access_token() -> str:
    resp = requests.post(
        TOKEN_URL,
        data={"grant_type": "client_credentials"},
        auth=(settings.reddit_client_id, settings.reddit_client_secret),
        headers={"User-Agent": settings.reddit_user_agent},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def collect_all() -> List[RawEvent]:
    if not settings.reddit_client_id or not settings.reddit_client_secret:
        logger.info("REDDIT_CLIENT_ID/SECRET not set — skipping Reddit collection (expected in early testing)")
        return []

    try:
        token = _get_access_token()
    except requests.RequestException as e:
        logger.warning("Reddit auth failed: %s", e)
        return []

    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": settings.reddit_user_agent,
    }

    events = []
    for subreddit in settings.reddit_subreddits:
        try:
            resp = requests.get(
                SEARCH_URL_TEMPLATE.format(subreddit=subreddit),
                headers=headers,
                params={
                    "q": settings.reddit_search_query,
                    "restrict_sr": 1,
                    "sort": "new",
                    "limit": 10,
                },
                timeout=15,
            )
            resp.raise_for_status()
            children = resp.json().get("data", {}).get("children", [])
        except requests.RequestException as e:
            logger.warning("Reddit search failed for r/%s: %s", subreddit, e)
            continue

        for child in children:
            post = child.get("data", {})
            text = f"{post.get('title', '')} {post.get('selftext', '')}"
            ticker = _extract_ticker(text)
            permalink = post.get("permalink", "")
            created_utc = post.get("created_utc")
            disclosure_date = (
                RawEvent.now_utc_iso()[:10]
                if not created_utc
                else datetime.fromtimestamp(created_utc, tz=timezone.utc).strftime("%Y-%m-%d")
            )
            events.append(
                RawEvent(
                    ticker=ticker,
                    company="",
                    source="reddit",
                    source_subtype="reddit_post",
                    transaction_date=None,
                    public_disclosure_date=disclosure_date,
                    retrieval_timestamp=RawEvent.now_utc_iso(),
                    source_url=f"https://www.reddit.com{permalink}" if permalink else "",
                    raw_payload={"title": post.get("title", ""), "subreddit": subreddit},
                )
            )
    logger.info("Reddit collector pulled %d raw events", len(events))
    return events
