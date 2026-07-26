"""
IPO calendar collector — free, public API that backs Nasdaq's own IPO
calendar page (api.nasdaq.com/api/ipo/calendar), covering both NASDAQ- and
NYSE-bound IPOs (Nasdaq's calendar aggregates across exchanges, not just its
own listings). No API key.

Deliberately does NOT flow through classify_event(), same reasoning as
collectors/macro_calendar.py: an IPO filing/pricing/withdrawal doesn't fit any
of the 5 company-event categories, and unlike a filing or press release this
data is already fully structured (ticker, price, shares, dollar value) —
there's no free text for an LLM to usefully interpret. main.py's
_run_ipo_calendar() handles dedup/logging/alerting directly.

Each deal has a stable Nasdaq-issued dealID, used as the dedup identity
(paired with lifecycle stage, since "filed" -> "upcoming" -> "priced" are
each a genuinely new, alert-worthy status change for the same deal, not a
duplicate of each other).
"""

import logging
from datetime import date, timedelta
from typing import List

import requests

from signalforge.config import settings
from signalforge.schema import RawEvent

logger = logging.getLogger(__name__)

_API_URL = "https://api.nasdaq.com/api/ipo/calendar"
_CALENDAR_PAGE_URL = "https://www.nasdaq.com/market-activity/ipos"

_STAGE_DATE_FIELD = {
    "priced": "pricedDate",
    "upcoming": "expectedPriceDate",
    "filed": "filedDate",
    "withdrawn": "withdrawDate",
}


def _parse_date(mdy: str) -> str:
    if not mdy:
        return RawEvent.now_utc_iso()[:10]
    try:
        month, day, year = mdy.split("/")
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
    except ValueError:
        return RawEvent.now_utc_iso()[:10]


def _rows_for_stage(payload: dict, stage: str) -> List[dict]:
    section = payload.get(stage)
    if stage == "upcoming":
        section = (section or {}).get("upcomingTable")
    return (section or {}).get("rows") or []


# Nasdaq's API silently hangs/times out on requests that don't look like a
# real browser (a plain descriptive User-Agent, fine for EDGAR/press wires,
# isn't enough here) — confirmed by testing: bare UA times out consistently,
# a full browser-like header set succeeds every time.
_BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://www.nasdaq.com/market-activity/ipos",
    "Origin": "https://www.nasdaq.com",
    "Accept-Language": "en-US,en;q=0.9",
}


def _fetch_month(year_month: str) -> dict:
    resp = requests.get(
        _API_URL,
        params={"date": year_month},
        headers=_BROWSER_HEADERS,
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json().get("data", {})


def collect_all() -> List[RawEvent]:
    if not settings.ipo_calendar_enabled:
        logger.info("IPO calendar disabled in config — skipping")
        return []

    today = date.today()
    next_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1)
    months = [today.strftime("%Y-%m"), next_month.strftime("%Y-%m")]

    events = []
    seen_deal_stage = set()
    for ym in months:
        try:
            payload = _fetch_month(ym)
        except requests.RequestException as e:
            logger.warning("IPO calendar fetch failed for %s: %s", ym, e)
            continue

        for stage, date_field in _STAGE_DATE_FIELD.items():
            for row in _rows_for_stage(payload, stage):
                deal_id = row.get("dealID", "")
                key = (deal_id, stage)
                if deal_id and key in seen_deal_stage:
                    continue
                seen_deal_stage.add(key)

                ticker = (row.get("proposedTickerSymbol") or "").upper()
                events.append(
                    RawEvent(
                        ticker=ticker,
                        company=row.get("companyName", ""),
                        source="ipo_calendar",
                        source_subtype=stage,
                        transaction_date=None,
                        public_disclosure_date=_parse_date(row.get(date_field, "")),
                        retrieval_timestamp=RawEvent.now_utc_iso(),
                        source_url=_CALENDAR_PAGE_URL,
                        raw_payload={**row, "dealID": deal_id},
                    )
                )
    logger.info("IPO calendar collector pulled %d raw events across %s", len(events), months)
    return events
