"""
Common normalized-event schema. Every collector must emit RawEvent objects;
everything downstream (classify, crossref, log, alert) consumes this shape only.
"""

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional, Any, Dict


@dataclass
class RawEvent:
    ticker: str
    company: str
    source: str                    # "edgar" | "quiver"
    source_subtype: str            # e.g. "8-K Item 5.02", "congress_trade", "form_4"
    transaction_date: Optional[str]      # when the underlying trade/event occurred (ISO date), if known
    public_disclosure_date: str          # when it became legally public (ISO date) — required
    retrieval_timestamp: str             # when our collector pulled it (ISO datetime, UTC)
    source_url: str
    raw_payload: Dict[str, Any]

    @staticmethod
    def now_utc_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# Deterministic label only — derived from the classifier's existing directional_read,
# not a new LLM call or a trade-proposal schema (sizing/entry/stop-loss/order type are
# explicitly out of Phase 1 scope; this is just a plainer restatement of the same signal).
_DIRECTIONAL_TO_BUY_SELL = {
    "bullish": "Buy",
    "bearish": "Sell",
    "neutral": "Hold",
    "ambiguous": "Hold",
}


@dataclass
class ClassifiedEvent:
    event: RawEvent
    event_type: str        # one of config.event_categories
    directional_read: str  # bullish | bearish | neutral | ambiguous
    confidence: int        # 1-10
    summary: str
    crossref_hit: bool = False
    crossref_categories: Optional[list] = None

    @property
    def buy_sell_signal(self) -> str:
        return _DIRECTIONAL_TO_BUY_SELL.get(self.directional_read, "Hold")

    def to_sheet_row(self) -> list:
        return [
            self.event.public_disclosure_date,
            self.event.transaction_date or "",
            self.event.ticker,
            self.event.company,
            self.event_type,
            self.directional_read,
            str(self.confidence),
            "yes" if self.crossref_hit else "no",
            ",".join(self.crossref_categories or []),
            self.summary,
            self.event.source,
            self.event.source_subtype,
            self.event.source_url,
            self.event.retrieval_timestamp,
            self.buy_sell_signal,
        ]


SHEET_HEADER = [
    "public_disclosure_date",
    "transaction_date",
    "ticker",
    "company",
    "event_type",
    "directional_read",
    "confidence",
    "crossref_hit",
    "crossref_categories",
    "summary",
    "source",
    "source_subtype",
    "source_url",
    "retrieval_timestamp",
    "buy_sell_signal",
]
