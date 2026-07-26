"""
Google Sheets logging.

Requires a Google Cloud service account with access to the target sheet
(share the sheet with the service account's email). Set
GOOGLE_SERVICE_ACCOUNT_JSON to the path of the downloaded key file, and
GOOGLE_SHEET_ID to the sheet's ID from its URL.

This module is read-and-append only. It never modifies existing rows and
has no relationship to any brokerage credential.
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


def _get_service():
    creds = Credentials.from_service_account_file(
        settings.google_service_account_json, scopes=SCOPES
    )
    return build("sheets", "v4", credentials=creds)


def ensure_header():
    service = _get_service()
    range_ = f"{settings.google_sheet_tab}!A1"
    service.spreadsheets().values().update(
        spreadsheetId=settings.google_sheet_id,
        range=range_,
        valueInputOption="RAW",
        body={"values": [SHEET_HEADER]},
    ).execute()


def append_events(events: List[ClassifiedEvent]):
    if not events:
        return
    service = _get_service()
    rows = [e.to_sheet_row() for e in events]
    service.spreadsheets().values().append(
        spreadsheetId=settings.google_sheet_id,
        range=f"{settings.google_sheet_tab}!A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": rows},
    ).execute()
    logger.info("Logged %d events to Google Sheets", len(rows))


def load_recent_history(lookback_days: int = None) -> List[ClassifiedEvent]:
    """
    Load recent rows back into ClassifiedEvent objects for cross-referencing.
    Only the fields crossref.py actually needs (ticker, event_type,
    public_disclosure_date) are populated — this is not a full round-trip
    deserialization.
    """
    lookback_days = lookback_days or settings.crossref_lookback_days
    cutoff = date.today() - timedelta(days=lookback_days)

    service = _get_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=settings.google_sheet_id,
        range=f"{settings.google_sheet_tab}!A2:N",
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
