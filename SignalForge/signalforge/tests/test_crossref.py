"""
Cross-reference is the actual signal-quality lever in this project, so it gets
a real test — everything else in Phase 1 is thin API plumbing that's better
verified against live (sandboxed) API responses than mocked here.

Run with: python -m pytest signalforge/tests/test_crossref.py -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from datetime import date, timedelta

from signalforge.schema import RawEvent, ClassifiedEvent
from signalforge.crossref import apply_crossref


def _make_classified(ticker, event_type, days_ago, confidence=5):
    disclosure_date = (date.today() - timedelta(days=days_ago)).isoformat()
    event = RawEvent(
        ticker=ticker,
        company=f"{ticker} Corp",
        source="test",
        source_subtype="test",
        transaction_date=disclosure_date,
        public_disclosure_date=disclosure_date,
        retrieval_timestamp=RawEvent.now_utc_iso(),
        source_url="https://example.com",
        raw_payload={},
    )
    return ClassifiedEvent(
        event=event,
        event_type=event_type,
        directional_read="bullish",
        confidence=confidence,
        summary="test event",
    )


def test_crossref_hit_within_window():
    history = [_make_classified("ACME", "institutional_accumulation", days_ago=10)]
    new = [_make_classified("ACME", "insider_conviction", days_ago=0)]

    result = apply_crossref(new, history)

    assert result[0].crossref_hit is True
    assert result[0].crossref_categories == ["institutional_accumulation"]


def test_crossref_no_hit_outside_window():
    history = [_make_classified("ACME", "institutional_accumulation", days_ago=45)]
    new = [_make_classified("ACME", "insider_conviction", days_ago=0)]

    result = apply_crossref(new, history)

    assert result[0].crossref_hit is False


def test_crossref_no_hit_same_category():
    history = [_make_classified("ACME", "insider_conviction", days_ago=5)]
    new = [_make_classified("ACME", "insider_conviction", days_ago=0)]

    result = apply_crossref(new, history)

    assert result[0].crossref_hit is False


def test_crossref_no_hit_different_ticker():
    history = [_make_classified("ACME", "institutional_accumulation", days_ago=5)]
    new = [_make_classified("OTHR", "insider_conviction", days_ago=0)]

    result = apply_crossref(new, history)

    assert result[0].crossref_hit is False


def test_crossref_within_same_batch():
    """Two events in the same run, on the same ticker, different categories,
    should cross-reference against each other even with no prior history."""
    new = [
        _make_classified("ACME", "institutional_accumulation", days_ago=0),
        _make_classified("ACME", "insider_conviction", days_ago=0),
    ]

    result = apply_crossref(new, history=[])

    assert result[1].crossref_hit is True


if __name__ == "__main__":
    test_crossref_hit_within_window()
    test_crossref_no_hit_outside_window()
    test_crossref_no_hit_same_category()
    test_crossref_no_hit_different_ticker()
    test_crossref_within_same_batch()
    print("All crossref tests passed.")
