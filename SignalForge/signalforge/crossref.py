"""
Cross-reference check: deterministic code, not an LLM call.

Flags a classified event if the same ticker has appeared under a DIFFERENT
event category within the trailing lookback window. This is the actual
signal-quality lever per the design brief — a single congressional trade is
weak signal; the same ticker also showing an insider cluster buy is not.
"""

import logging
from datetime import date, timedelta
from typing import List, Dict

from signalforge.config import settings
from signalforge.schema import ClassifiedEvent

logger = logging.getLogger(__name__)


def apply_crossref(
    new_events: List[ClassifiedEvent],
    history: List[ClassifiedEvent],
) -> List[ClassifiedEvent]:
    """
    history: previously logged classified events (typically loaded from the
    Google Sheet at the start of a run — see sheets_log.load_recent_history).
    Mutates and returns new_events with crossref_hit / crossref_categories set.
    """
    cutoff = date.today() - timedelta(days=settings.crossref_lookback_days)

    # ticker -> set of categories seen in the lookback window
    ticker_categories: Dict[str, set] = {}
    for h in history:
        try:
            disclosure_date = date.fromisoformat(h.event.public_disclosure_date[:10])
        except (ValueError, TypeError):
            continue
        if disclosure_date < cutoff:
            continue
        ticker_categories.setdefault(h.event.ticker, set()).add(h.event_type)

    for ce in new_events:
        prior_categories = ticker_categories.get(ce.event.ticker, set())
        other_categories = prior_categories - {ce.event_type}
        if other_categories:
            ce.crossref_hit = True
            ce.crossref_categories = sorted(other_categories)
        # Add this event to the working set so later events in the same batch
        # can cross-reference against it too
        ticker_categories.setdefault(ce.event.ticker, set()).add(ce.event_type)

    hits = sum(1 for ce in new_events if ce.crossref_hit)
    logger.info("Cross-reference flagged %d/%d events", hits, len(new_events))
    return new_events
