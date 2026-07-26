"""
Paper-trading tracker — no brokerage, no real money, nothing here ever
touches an order endpoint. It simulates acting on SignalForge's own alerts
so the signal's actual predictive value can be measured before any real
capital is ever involved. See CLAUDE.md's execution boundary — this module
only ever reads market prices, never submits anything.

Trigger for opening a paper position: exactly the same bar as a real
Telegram alert (confidence >= min_confidence_for_alert AND crossref_hit),
plus a non-"Hold" buy_sell_signal. This deliberately answers "if I acted on
every alert I actually received, how would I have done" — not some looser,
more optimistic hypothetical.

Tracks percent return only, never dollar P&L — no position-sizing scheme is
assumed or invented here; that's a real decision for a human, not something
to fabricate a fake number for. Direction (Buy=long, Sell=short) determines
return sign: a "Sell" position gains when the price falls.

Uses yfinance (free) for real entry and mark-to-market prices — a lookup
failure means no entry is recorded, never a guessed price.
"""

import logging
from datetime import date, datetime
from typing import Dict, List, Optional

import yfinance as yf

from signalforge.config import settings
from signalforge.schema import ClassifiedEvent

logger = logging.getLogger(__name__)


def _get_price(ticker: str) -> Optional[float]:
    try:
        hist = yf.Ticker(ticker).history(period="5d")
        if hist.empty:
            return None
        return round(float(hist["Close"].iloc[-1]), 4)
    except Exception as e:
        logger.warning("Price lookup failed for %s: %s", ticker, e)
        return None


def _qualifies(ce: ClassifiedEvent) -> bool:
    meets_confidence = ce.confidence >= settings.min_confidence_for_alert
    meets_crossref = ce.crossref_hit or not settings.require_crossref_for_alert
    return meets_confidence and meets_crossref and ce.buy_sell_signal in ("Buy", "Sell")


def _trade_id(ce: ClassifiedEvent) -> str:
    return f"{ce.event.ticker}-{ce.event.public_disclosure_date}-{ce.event_type}-{ce.event.source}"


def open_new_positions(classified: List[ClassifiedEvent], existing_trade_ids: set) -> List[dict]:
    """Returns new 'entry' observation rows for qualifying events not already tracked."""
    rows = []
    today = date.today().isoformat()
    for ce in classified:
        if not _qualifies(ce):
            continue
        trade_id = _trade_id(ce)
        if trade_id in existing_trade_ids:
            continue

        price = _get_price(ce.event.ticker)
        if price is None:
            logger.info("Skipping paper entry for %s — no price available", ce.event.ticker)
            continue

        rows.append({
            "trade_id": trade_id,
            "observation_type": "entry",
            "direction": ce.buy_sell_signal,
            "ticker": ce.event.ticker,
            "company": ce.event.company,
            "event_type": ce.event_type,
            "confidence": ce.confidence,
            "entry_date": today,
            "entry_price": price,
            "observation_date": today,
            "observation_price": price,
            "return_pct": 0.0,
            "days_held": 0,
            "source": ce.event.source,
            "summary": ce.summary,
        })
    return rows


def _compute_return_pct(direction: str, entry_price: float, current_price: float) -> float:
    raw = (current_price - entry_price) / entry_price * 100
    return round(raw if direction == "Buy" else -raw, 3)


def update_open_positions(open_trades: Dict[str, dict]) -> List[dict]:
    """
    open_trades: trade_id -> {ticker, direction, entry_date, entry_price,
    company, event_type, confidence, source, summary, last_observed_date}
    (from sheets_log.load_paper_trades_summary()).

    Returns new 'checkpoint' observation rows for positions that are still
    within the tracking window and haven't been observed yet today.
    """
    today = date.today()
    rows = []
    for trade_id, info in open_trades.items():
        entry_date = datetime.fromisoformat(info["entry_date"]).date()
        days_held = (today - entry_date).days

        if days_held > settings.paper_trading_tracking_days:
            continue
        if info["last_observed_date"] == today.isoformat():
            continue

        price = _get_price(info["ticker"])
        if price is None:
            continue

        rows.append({
            "trade_id": trade_id,
            "observation_type": "checkpoint",
            "direction": info["direction"],
            "ticker": info["ticker"],
            "company": info["company"],
            "event_type": info["event_type"],
            "confidence": info["confidence"],
            "entry_date": info["entry_date"],
            "entry_price": info["entry_price"],
            "observation_date": today.isoformat(),
            "observation_price": price,
            "return_pct": _compute_return_pct(info["direction"], info["entry_price"], price),
            "days_held": days_held,
            "source": info["source"],
            "summary": info["summary"],
        })
    return rows
