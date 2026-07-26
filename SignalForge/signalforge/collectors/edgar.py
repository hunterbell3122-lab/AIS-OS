"""
SEC EDGAR collector.

Pulls recent 8-K filings (Items 1.01, 2.01, 5.02), Form 4 insider transactions,
and Schedule 13D activist filings via EDGAR's free full-text search API.

EDGAR requires a descriptive User-Agent identifying the requester (SEC policy,
not a technicality — requests without one get rate-limited or blocked). Set
EDGAR_USER_AGENT in .env to "YourProject you@email.com".

Docs: https://www.sec.gov/edgar/sec-api-documentation
"""

import logging
from datetime import datetime, timezone
from typing import List

import requests

from signalforge.config import settings
from signalforge.schema import RawEvent

logger = logging.getLogger(__name__)

FORM_TYPES = {
    "8-K": "leadership_or_transaction",
    "4": "insider_transaction",
    "SC 13D": "activist_stake",
}


def _search_edgar(form_type: str, days_back: int = 1) -> List[dict]:
    """Query EDGAR full-text search for a given form type, most recent filings."""
    params = {
        "q": '"' + form_type + '"',
        "dateRange": "custom",
        "forms": form_type,
        "startdt": _n_days_ago(days_back),
        "enddt": _today(),
    }
    headers = {"User-Agent": settings.edgar_user_agent}
    try:
        resp = requests.get(
            "https://efts.sec.gov/LATEST/search-index",
            params=params,
            headers=headers,
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json().get("hits", {}).get("hits", [])
    except requests.RequestException as e:
        logger.warning("EDGAR request failed for form %s: %s", form_type, e)
        return []


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _n_days_ago(n: int) -> str:
    from datetime import timedelta
    return (datetime.now(timezone.utc) - timedelta(days=n)).strftime("%Y-%m-%d")


def _hit_to_event(hit: dict, form_type: str) -> RawEvent:
    src = hit.get("_source", {})
    ticker = (src.get("tickers") or [""])[0]
    company = src.get("display_names", [""])[0] if src.get("display_names") else ""
    filing_date = src.get("file_date", _today())
    accession = src.get("adsh", "")
    cik = (src.get("ciks") or [""])[0]
    url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}"

    return RawEvent(
        ticker=ticker,
        company=company,
        source="edgar",
        source_subtype=form_type,
        transaction_date=None,  # EDGAR full-text search doesn't expose this directly;
                                 # the classifier / a follow-up doc fetch fills it in later
        public_disclosure_date=filing_date,
        retrieval_timestamp=RawEvent.now_utc_iso(),
        source_url=url,
        raw_payload={"accession_number": accession, "raw_hit": src},
    )


def collect_8k_events() -> List[RawEvent]:
    """
    Collect recent 8-K filings. Note: full-text search returns the form type,
    not the specific Item number (1.01/2.01/5.02) — filtering to those specific
    items requires fetching and parsing the actual filing document. This function
    returns all recent 8-Ks; wire in item-level filtering before this goes into
    production classification if false-positive volume is too high.
    """
    hits = _search_edgar("8-K", days_back=1)
    return [_hit_to_event(h, "8-K") for h in hits]


def collect_form4_events() -> List[RawEvent]:
    hits = _search_edgar("4", days_back=1)
    return [_hit_to_event(h, "Form 4") for h in hits]


def collect_13d_events() -> List[RawEvent]:
    hits = _search_edgar("SC 13D", days_back=1)
    return [_hit_to_event(h, "Schedule 13D") for h in hits]


def collect_all() -> List[RawEvent]:
    events: List[RawEvent] = []
    events.extend(collect_8k_events())
    events.extend(collect_form4_events())
    events.extend(collect_13d_events())
    logger.info("EDGAR collector pulled %d raw events", len(events))
    return events
