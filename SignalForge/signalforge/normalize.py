"""
Normalization: dedupe and clean raw events from all collectors before classification.
"""

import logging
from typing import List

from signalforge.schema import RawEvent

logger = logging.getLogger(__name__)


def _dedupe_key(event: RawEvent) -> tuple:
    return (
        event.ticker.upper().strip(),
        event.source,
        event.source_subtype,
        event.public_disclosure_date,
        event.raw_payload.get("accession_number", "") or event.raw_payload.get("TransactionDate", ""),
    )


def normalize(events: List[RawEvent]) -> List[RawEvent]:
    """Drop events with no ticker (unresolvable), dedupe, and strip whitespace."""
    seen = set()
    cleaned: List[RawEvent] = []

    for e in events:
        if not e.ticker or not e.ticker.strip():
            continue
        e.ticker = e.ticker.strip().upper()
        e.company = e.company.strip()

        key = _dedupe_key(e)
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(e)

    logger.info("Normalized %d raw events down to %d", len(events), len(cleaned))
    return cleaned
