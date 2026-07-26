"""
Quiver Quantitative collector.

Pulls recent congressional trade disclosures. Requires QUIVER_API_KEY
(free tier available — start there per the Phase 1 default in CLAUDE.md
before paying for a higher tier).

Docs: https://api.quiverquant.com/docs/
"""

import logging
from typing import List

import requests

from signalforge.config import settings
from signalforge.schema import RawEvent

logger = logging.getLogger(__name__)


def collect_congress_trades() -> List[RawEvent]:
    if not settings.quiver_api_key:
        logger.info("QUIVER_API_KEY not set — skipping Quiver collection (expected in early testing)")
        return []

    headers = {"Authorization": f"Bearer {settings.quiver_api_key}"}
    try:
        resp = requests.get(
            f"{settings.quiver_base_url}/live/congresstrading",
            headers=headers,
            timeout=15,
        )
        resp.raise_for_status()
        raw_trades = resp.json()
    except requests.RequestException as e:
        logger.warning("Quiver request failed: %s", e)
        return []

    events = []
    for trade in raw_trades:
        events.append(
            RawEvent(
                ticker=trade.get("Ticker", ""),
                company=trade.get("Company", ""),
                source="quiver",
                source_subtype="congress_trade",
                transaction_date=trade.get("TransactionDate"),
                public_disclosure_date=trade.get("ReportDate", trade.get("TransactionDate", "")),
                retrieval_timestamp=RawEvent.now_utc_iso(),
                source_url="https://www.quiverquant.com/congresstrading/",
                raw_payload=trade,
            )
        )
    logger.info("Quiver collector pulled %d congress trade events", len(events))
    return events
