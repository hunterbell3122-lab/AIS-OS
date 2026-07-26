"""
Google Sheets logging.

Requires a Google Cloud service account with access to the target sheet
(share the sheet with the service account's email). Set
GOOGLE_SERVICE_ACCOUNT_JSON to the path of the downloaded key file, and
GOOGLE_SHEET_ID to the sheet's ID from its URL.

This module has no relationship to any brokerage credential. The automated
pipeline (main.py) only ever appends — it never rewrites past rows. The one
exception is update_ipo_recommendations(), which exists specifically for
recording actual human/researched investment opinions (recommendation,
target price) onto existing IPO rows — that data can only ever come from
real research done in a session, never fabricated by the collector, so it's
a deliberate manual annotation step, not something main.py calls on its own.
"""

import logging
from datetime import date, timedelta
from typing import List

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from signalforge.config import settings
from signalforge.schema import ClassifiedEvent, RawEvent, SHEET_HEADER

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Macro events skip classify_event() entirely (see collectors/macro_calendar.py),
# so they get their own simpler header — no ticker, no event_type/confidence.
MACRO_SHEET_HEADER = ["public_disclosure_date", "source_subtype", "headline", "source_url", "retrieval_timestamp"]

# IPO calendar events also skip classify_event() (see collectors/ipo_calendar.py)
# — this data is already fully structured, no LLM interpretation needed.
# listing_date/recommendation/target_price are populated two different ways:
# listing_date is derived deterministically (stage + date), safe to automate;
# recommendation/target_price are manual research annotations only — see
# update_ipo_recommendations() — and default to "Not yet reviewed"/blank.
IPO_SHEET_HEADER = [
    "public_disclosure_date", "stage", "ticker", "company", "exchange",
    "price", "shares_offered", "dollar_value", "deal_id", "source_url",
    "listing_date", "recommendation", "target_price",
]

# Paper-trading tracker (see paper_trading.py) — append-only log of
# observations, one "entry" row per opened position plus one "checkpoint"
# row per day it's still tracked. No dollar P&L column on purpose — see
# paper_trading.py's module docstring for why.
PAPER_TRADES_SHEET_HEADER = [
    "trade_id", "observation_type", "direction", "ticker", "company",
    "event_type", "confidence", "entry_date", "entry_price",
    "observation_date", "observation_price", "return_pct", "days_held",
    "source", "summary",
]


def _get_service():
    creds = Credentials.from_service_account_file(
        settings.google_service_account_json, scopes=SCOPES
    )
    return build("sheets", "v4", credentials=creds)


def ensure_header(tab: str = None):
    tab = tab or settings.google_sheet_tab
    service = _get_service()
    range_ = f"'{tab}'!A1"
    service.spreadsheets().values().update(
        spreadsheetId=settings.google_sheet_id,
        range=range_,
        valueInputOption="RAW",
        body={"values": [SHEET_HEADER]},
    ).execute()


def append_events(events: List[ClassifiedEvent], tab: str = None):
    if not events:
        return
    tab = tab or settings.google_sheet_tab
    service = _get_service()
    rows = [e.to_sheet_row() for e in events]
    service.spreadsheets().values().append(
        spreadsheetId=settings.google_sheet_id,
        range=f"'{tab}'!A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": rows},
    ).execute()
    logger.info("Logged %d events to Google Sheets tab '%s'", len(rows), tab)


def load_recent_history(tab: str = None, lookback_days: int = None) -> List[ClassifiedEvent]:
    """
    Load recent rows back into ClassifiedEvent objects for cross-referencing.
    Only the fields crossref.py actually needs (ticker, event_type,
    public_disclosure_date) are populated — this is not a full round-trip
    deserialization.
    """
    tab = tab or settings.google_sheet_tab
    lookback_days = lookback_days or settings.crossref_lookback_days
    cutoff = date.today() - timedelta(days=lookback_days)

    service = _get_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=settings.google_sheet_id,
        range=f"'{tab}'!A2:N",
    ).execute()
    rows = result.get("values", [])

    history = []
    for row in rows:
        if len(row) < 5:
            continue
        disclosure_date_str = row[0]
        try:
            if date.fromisoformat(disclosure_date_str[:10]) < cutoff:
                continue
        except ValueError:
            continue

        dummy_event = RawEvent(
            ticker=row[2],
            company=row[3] if len(row) > 3 else "",
            source=row[10] if len(row) > 10 else "",
            source_subtype=row[11] if len(row) > 11 else "",
            transaction_date=row[1] if len(row) > 1 else None,
            public_disclosure_date=disclosure_date_str,
            retrieval_timestamp=row[13] if len(row) > 13 else "",
            source_url=row[12] if len(row) > 12 else "",
            raw_payload={},
        )
        history.append(
            ClassifiedEvent(
                event=dummy_event,
                event_type=row[4],
                directional_read=row[5] if len(row) > 5 else "",
                confidence=int(row[6]) if len(row) > 6 and row[6].isdigit() else 0,
                summary=row[9] if len(row) > 9 else "",
            )
        )
    logger.info("Loaded %d historical events for cross-referencing", len(history))
    return history


def ensure_macro_header(tab: str = None):
    tab = tab or settings.google_sheet_tab_macro
    service = _get_service()
    service.spreadsheets().values().update(
        spreadsheetId=settings.google_sheet_id,
        range=f"'{tab}'!A1",
        valueInputOption="RAW",
        body={"values": [MACRO_SHEET_HEADER]},
    ).execute()


def append_macro_events(events: List[RawEvent], tab: str = None):
    if not events:
        return
    tab = tab or settings.google_sheet_tab_macro
    service = _get_service()
    rows = [
        [e.public_disclosure_date, e.source_subtype, e.raw_payload.get("title", ""), e.source_url, e.retrieval_timestamp]
        for e in events
    ]
    service.spreadsheets().values().append(
        spreadsheetId=settings.google_sheet_id,
        range=f"'{tab}'!A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": rows},
    ).execute()
    logger.info("Logged %d macro events to Google Sheets tab '%s'", len(rows), tab)


def load_macro_history(tab: str = None) -> set:
    """Returns a set of (source_subtype, headline, public_disclosure_date) keys
    already logged, for dedup — macro events have no ticker/classification to
    key on, so the headline itself is the identity.

    Unlike load_recent_history() (crossref, intentionally time-windowed),
    this has no cutoff: RSS feeds return their N most-recent items regardless
    of age, and BLS/Fed publish infrequently enough that a 30-day window would
    let an old-but-still-in-the-feed item fall outside it and get re-alerted
    every run. Dedup here means "ever logged," not "logged recently."
    """
    tab = tab or settings.google_sheet_tab_macro

    service = _get_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=settings.google_sheet_id,
        range=f"'{tab}'!A2:C",
    ).execute()
    rows = result.get("values", [])

    keys = set()
    for row in rows:
        if len(row) < 3:
            continue
        keys.add((row[1], row[2], row[0]))
    logger.info("Loaded %d historical macro keys from tab '%s'", len(keys), tab)
    return keys


def ensure_ipo_header(tab: str = None):
    tab = tab or settings.google_sheet_tab_ipo
    service = _get_service()
    service.spreadsheets().values().update(
        spreadsheetId=settings.google_sheet_id,
        range=f"'{tab}'!A1",
        valueInputOption="RAW",
        body={"values": [IPO_SHEET_HEADER]},
    ).execute()


def append_ipo_events(events: List[RawEvent], tab: str = None):
    if not events:
        return
    tab = tab or settings.google_sheet_tab_ipo
    service = _get_service()
    rows = []
    for e in events:
        p = e.raw_payload
        # listing_date is only meaningful once a deal has an actual/expected
        # trading date (priced/upcoming); filed/withdrawn have no listing yet.
        listing_date = e.public_disclosure_date if e.source_subtype in ("priced", "upcoming") else ""
        rows.append([
            e.public_disclosure_date,
            e.source_subtype,
            e.ticker,
            e.company,
            p.get("proposedExchange", ""),
            p.get("proposedSharePrice", ""),
            p.get("sharesOffered", ""),
            p.get("dollarValueOfSharesOffered", ""),
            p.get("dealID", ""),
            e.source_url,
            listing_date,
            "Not yet reviewed",
            "",
        ])
    service.spreadsheets().values().append(
        spreadsheetId=settings.google_sheet_id,
        range=f"'{tab}'!A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": rows},
    ).execute()
    logger.info("Logged %d IPO events to Google Sheets tab '%s'", len(rows), tab)


def load_ipo_history(tab: str = None) -> set:
    """Returns a set of (deal_id, stage) keys already logged. A deal moving
    from 'filed' to 'upcoming' to 'priced' is 3 genuinely distinct,
    alert-worthy events for the same deal_id, not duplicates of each other —
    same reasoning as load_macro_history(), no time cutoff."""
    tab = tab or settings.google_sheet_tab_ipo

    service = _get_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=settings.google_sheet_id,
        range=f"'{tab}'!A2:I",
    ).execute()
    rows = result.get("values", [])

    keys = set()
    for row in rows:
        if len(row) < 9:
            continue
        keys.add((row[8], row[1]))  # (deal_id, stage)
    logger.info("Loaded %d historical IPO keys from tab '%s'", len(keys), tab)
    return keys


def update_ipo_recommendations(annotations: dict, tab: str = None):
    """
    annotations: ticker -> {"recommendation": str, "target_price": str}.

    Rewrites the recommendation/target_price columns (and backfills
    listing_date if it was blank) for existing rows matching by ticker.
    This is the one function in this module that modifies already-logged
    rows — see the module docstring for why that's fine specifically here:
    the values only ever come from real research done in a session, never
    fabricated automatically.
    """
    tab = tab or settings.google_sheet_tab_ipo
    service = _get_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=settings.google_sheet_id,
        range=f"'{tab}'!A2:M",
    ).execute()
    rows = result.get("values", [])

    updated = []
    matched = 0
    for row in rows:
        row = row + [""] * (13 - len(row))
        ticker, stage, disclosure_date = row[2], row[1], row[0]

        if not row[10] and stage in ("priced", "upcoming"):
            row[10] = disclosure_date

        ann = annotations.get(ticker)
        if ann:
            row[11] = ann.get("recommendation", row[11])
            row[12] = ann.get("target_price", row[12])
            matched += 1
        updated.append(row)

    if updated:
        service.spreadsheets().values().update(
            spreadsheetId=settings.google_sheet_id,
            range=f"'{tab}'!A2:M{1 + len(updated)}",
            valueInputOption="RAW",
            body={"values": updated},
        ).execute()
    logger.info("Updated %d/%d IPO row(s) with recommendations in tab '%s'", matched, len(updated), tab)


def ensure_paper_trades_header(tab: str = None):
    tab = tab or settings.google_sheet_tab_paper_trades
    service = _get_service()
    service.spreadsheets().values().update(
        spreadsheetId=settings.google_sheet_id,
        range=f"'{tab}'!A1",
        valueInputOption="RAW",
        body={"values": [PAPER_TRADES_SHEET_HEADER]},
    ).execute()


def append_paper_trade_observations(rows: List[dict], tab: str = None):
    if not rows:
        return
    tab = tab or settings.google_sheet_tab_paper_trades
    service = _get_service()
    sheet_rows = [[r[col] for col in PAPER_TRADES_SHEET_HEADER] for r in rows]
    service.spreadsheets().values().append(
        spreadsheetId=settings.google_sheet_id,
        range=f"'{tab}'!A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": sheet_rows},
    ).execute()
    logger.info("Logged %d paper-trade observation(s) to Google Sheets tab '%s'", len(sheet_rows), tab)


def load_paper_trades_summary(tab: str = None) -> dict:
    """Returns trade_id -> {ticker, direction, entry_date, entry_price,
    company, event_type, confidence, source, summary, last_observed_date},
    built from every observation row (entry + checkpoints) logged so far —
    the 'entry' row supplies the fixed facts, and the max observation_date
    across all rows for that trade_id is its last_observed_date."""
    tab = tab or settings.google_sheet_tab_paper_trades

    service = _get_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=settings.google_sheet_id,
        range=f"'{tab}'!A2:O",
    ).execute()
    rows = result.get("values", [])

    trades: dict = {}
    for row in rows:
        if len(row) < 15:
            continue
        cols = dict(zip(PAPER_TRADES_SHEET_HEADER, row))
        trade_id = cols["trade_id"]

        if trade_id not in trades:
            trades[trade_id] = {
                "ticker": cols["ticker"],
                "direction": cols["direction"],
                "company": cols["company"],
                "event_type": cols["event_type"],
                "confidence": cols["confidence"],
                "entry_date": cols["entry_date"],
                "entry_price": float(cols["entry_price"]),
                "source": cols["source"],
                "summary": cols["summary"],
                "last_observed_date": cols["observation_date"],
            }
        else:
            if cols["observation_date"] > trades[trade_id]["last_observed_date"]:
                trades[trade_id]["last_observed_date"] = cols["observation_date"]

    logger.info("Loaded %d paper trade(s) from tab '%s'", len(trades), tab)
    return trades
