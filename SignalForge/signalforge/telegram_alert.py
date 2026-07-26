"""
Telegram alerting — notification only, Phase 1. No approval buttons, no callback
handlers, no path back into anything that could execute a trade. That's a later
phase's design (see docs/signalforge-phase0.md, Section 6), built as a separate
module when execution work actually starts.
"""

import logging
from typing import List

import requests

from signalforge.config import settings
from signalforge.schema import ClassifiedEvent, RawEvent

logger = logging.getLogger(__name__)


def _format_message(ce: ClassifiedEvent) -> str:
    crossref_note = ""
    if ce.crossref_hit:
        crossref_note = f"\n🔗 Also seen in: {', '.join(ce.crossref_categories)}"
    return (
        f"📊 {ce.event.ticker} — {ce.event.company}\n"
        f"Type: {ce.event_type} | {ce.directional_read} | Confidence: {ce.confidence}/10"
        f"{crossref_note}\n"
        f"{ce.summary}\n"
        f"Source: {ce.event.source_subtype} ({ce.event.public_disclosure_date})\n"
        f"{ce.event.source_url}"
    )


def send_alert(ce: ClassifiedEvent) -> bool:
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        logger.info("Telegram not configured — skipping alert for %s", ce.event.ticker)
        return False

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    try:
        resp = requests.post(
            url,
            json={"chat_id": settings.telegram_chat_id, "text": _format_message(ce)},
            timeout=10,
        )
        resp.raise_for_status()
        return True
    except requests.RequestException as e:
        logger.warning("Telegram alert failed for %s: %s", ce.event.ticker, e)
        return False


def send_macro_alert(event: RawEvent) -> bool:
    """Macro releases have no confidence/crossref score to gate on — every new
    (deduped) one is scheduled, official, market-wide, so all of them alert."""
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        logger.info("Telegram not configured — skipping macro alert for %s", event.source_subtype)
        return False

    text = (
        f"\U0001F30D {event.source_subtype}\n"
        f"{event.raw_payload.get('title', '')}\n"
        f"Released: {event.public_disclosure_date}\n"
        f"{event.source_url}"
    )
    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    try:
        resp = requests.post(url, json={"chat_id": settings.telegram_chat_id, "text": text}, timeout=10)
        resp.raise_for_status()
        return True
    except requests.RequestException as e:
        logger.warning("Telegram macro alert failed for %s: %s", event.source_subtype, e)
        return False


_STAGE_EMOJI = {"filed": "\U0001F4DD", "upcoming": "⏳", "priced": "✅", "withdrawn": "❌"}


def send_ipo_alert(event: RawEvent) -> bool:
    """IPO calendar data is already fully structured — no confidence/crossref
    score to gate on, same as macro. Every new (deduped) stage transition
    alerts: filed/upcoming/priced/withdrawn are each real news on their own."""
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        logger.info("Telegram not configured — skipping IPO alert for %s", event.ticker or event.company)
        return False

    p = event.raw_payload
    emoji = _STAGE_EMOJI.get(event.source_subtype, "\U0001F4C8")
    ticker_part = f"{event.ticker} — " if event.ticker else ""
    text = (
        f"{emoji} IPO {event.source_subtype.upper()}: {ticker_part}{event.company}\n"
        f"Exchange: {p.get('proposedExchange', 'n/a')} | Price: {p.get('proposedSharePrice', 'n/a')} | "
        f"Shares: {p.get('sharesOffered', 'n/a')}\n"
        f"Offer amount: {p.get('dollarValueOfSharesOffered', 'n/a')}\n"
        f"Date: {event.public_disclosure_date}\n"
        f"{event.source_url}"
    )
    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    try:
        resp = requests.post(url, json={"chat_id": settings.telegram_chat_id, "text": text}, timeout=10)
        resp.raise_for_status()
        return True
    except requests.RequestException as e:
        logger.warning("Telegram IPO alert failed for %s: %s", event.ticker or event.company, e)
        return False


def send_alerts_above_threshold(events: List[ClassifiedEvent]) -> int:
    sent = 0
    for ce in events:
        meets_confidence = ce.confidence >= settings.min_confidence_for_alert
        meets_crossref = ce.crossref_hit or not settings.require_crossref_for_alert
        if meets_confidence and meets_crossref:
            if send_alert(ce):
                sent += 1
    logger.info("Sent %d/%d events as alerts", sent, len(events))
    return sent
