"""
SignalForge Phase 1 orchestrator.

Run manually with `python -m signalforge.main`, or wire to cron / a scheduled
task for the polling cadence in config.py.

Pipeline: collect -> normalize -> classify -> cross-reference -> log -> alert.

There is no brokerage connectivity anywhere in this file or anything it imports.
If you're looking for execution code, it doesn't exist yet on purpose — see
CLAUDE.md and docs/signalforge-phase0.md for why, and for what a later,
deliberately separate execution phase would require.
"""

import logging
import sys

from signalforge.collectors import edgar, quiver, twitter, reddit, press_wire, macro_calendar, ipo_calendar
from signalforge.normalize import normalize
from signalforge.classify import classify_all
from signalforge.crossref import apply_crossref
from signalforge import sheets_log
from signalforge.telegram_alert import send_alerts_above_threshold, send_macro_alert, send_ipo_alert
from signalforge.config import settings
from signalforge import paper_trading

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("signalforge.main")

# Maps event source -> destination sheet tab. EDGAR/Quiver/press wires share
# the "Events" tab. Twitter/Reddit collectors exist in the codebase but are
# dormant (no credentials configured) and their "X"/"Reddit" tabs were removed
# from the sheet — deliberately left out of this map so crossref history
# loading doesn't try to read tabs that no longer exist. Re-add them here (and
# recreate the tabs) if those collectors ever get turned back on.
_SOURCE_TO_TAB = {
    "edgar": settings.google_sheet_tab,
    "quiver": settings.google_sheet_tab,
    "press_wire": settings.google_sheet_tab,
}


def _dedup_key(ce):
    return (ce.event.ticker, ce.event_type, ce.event.source_subtype, ce.event.public_disclosure_date)


def _macro_key(e):
    return (e.source_subtype, e.raw_payload.get("title", ""), e.public_disclosure_date)


def _run_macro():
    """Separate from the ticker-centric pipeline on purpose — see
    collectors/macro_calendar.py's docstring. Runs independently of the main
    pipeline's early returns so a quiet EDGAR day doesn't suppress macro alerts."""
    macro_events = macro_calendar.collect_all()
    if not macro_events:
        return

    if not (settings.google_sheet_id and settings.google_service_account_json):
        logger.info("Google Sheets not configured — printing macro results instead:")
        for e in macro_events:
            print(e.public_disclosure_date, e.source_subtype, e.raw_payload.get("title", ""))
        return

    try:
        seen = sheets_log.load_macro_history()
        history_load_ok = True
    except Exception as e:
        logger.warning("Could not load macro history for dedup: %s", e)
        seen = set()
        history_load_ok = False

    # Cold start (tab genuinely empty, not a failed load) — back-fill the sheet
    # so history exists for next time, but don't fire a wall of alerts for a
    # backlog that was never "new." Same guard applies if a fresh feed URL is
    # added later.
    is_cold_start = history_load_ok and not seen

    new_events = [e for e in macro_events if _macro_key(e) not in seen]
    skipped = len(macro_events) - len(new_events)
    if skipped:
        logger.info("Skipped %d macro event(s) already logged (persistent dedup)", skipped)
    if not new_events:
        return

    try:
        sheets_log.ensure_macro_header()
        sheets_log.append_macro_events(new_events)
    except Exception as e:
        logger.error("Failed to log macro events to Sheets: %s", e)

    if is_cold_start:
        logger.info("Macro: %d event(s) logged on cold start — skipping alerts for backlog", len(new_events))
        return

    sent = sum(1 for e in new_events if send_macro_alert(e))
    logger.info("Macro: %d new event(s) logged, %d alert(s) sent", len(new_events), sent)


def _ipo_key(e):
    return (e.raw_payload.get("dealID", ""), e.source_subtype)


def _run_ipo_calendar():
    """Separate from the ticker-centric pipeline on purpose — see
    collectors/ipo_calendar.py's docstring."""
    ipo_events = ipo_calendar.collect_all()
    if not ipo_events:
        return

    if not (settings.google_sheet_id and settings.google_service_account_json):
        logger.info("Google Sheets not configured — printing IPO results instead:")
        for e in ipo_events:
            print(e.public_disclosure_date, e.source_subtype, e.ticker, e.company)
        return

    try:
        seen = sheets_log.load_ipo_history()
        history_load_ok = True
    except Exception as e:
        logger.warning("Could not load IPO history for dedup: %s", e)
        seen = set()
        history_load_ok = False

    is_cold_start = history_load_ok and not seen

    new_events = [e for e in ipo_events if _ipo_key(e) not in seen]
    skipped = len(ipo_events) - len(new_events)
    if skipped:
        logger.info("Skipped %d IPO event(s) already logged (persistent dedup)", skipped)
    if not new_events:
        return

    try:
        sheets_log.ensure_ipo_header()
        sheets_log.append_ipo_events(new_events)
    except Exception as e:
        logger.error("Failed to log IPO events to Sheets: %s", e)

    if is_cold_start:
        logger.info("IPO: %d event(s) logged on cold start — skipping alerts for backlog", len(new_events))
        return

    sent = sum(1 for e in new_events if send_ipo_alert(e))
    logger.info("IPO: %d new event(s) logged, %d alert(s) sent", len(new_events), sent)


def _run_paper_trading_updates():
    """Mark-to-market existing open paper positions — independent of this
    run's new events, so it happens whether or not anything new fires today."""
    if not settings.paper_trading_enabled:
        return
    if not (settings.google_sheet_id and settings.google_service_account_json):
        return

    try:
        open_trades = sheets_log.load_paper_trades_summary()
    except Exception as e:
        logger.warning("Could not load paper trades for mark-to-market: %s", e)
        return

    checkpoint_rows = paper_trading.update_open_positions(open_trades)
    if not checkpoint_rows:
        return

    try:
        sheets_log.append_paper_trade_observations(checkpoint_rows)
        logger.info("Paper trading: %d checkpoint observation(s) recorded", len(checkpoint_rows))
    except Exception as e:
        logger.error("Failed to log paper trade checkpoints: %s", e)


def _run_paper_trading_entries(classified):
    """Opens new paper positions for events that just cleared the same bar as
    a real Telegram alert. Called with the already-deduped classified list,
    so re-running never double-enters the same signal."""
    if not settings.paper_trading_enabled:
        return
    if not (settings.google_sheet_id and settings.google_service_account_json):
        return

    try:
        existing_trade_ids = set(sheets_log.load_paper_trades_summary().keys())
    except Exception as e:
        logger.warning("Could not load existing paper trades: %s", e)
        existing_trade_ids = set()

    entry_rows = paper_trading.open_new_positions(classified, existing_trade_ids)
    if not entry_rows:
        return

    try:
        sheets_log.ensure_paper_trades_header()
        sheets_log.append_paper_trade_observations(entry_rows)
        logger.info("Paper trading: %d new position(s) opened", len(entry_rows))
    except Exception as e:
        logger.error("Failed to log new paper trade entries: %s", e)


def run_once():
    assert settings.BROKERAGE_EXECUTION_ENABLED is False, (
        "BROKERAGE_EXECUTION_ENABLED must be False in Phase 1. "
        "If you're seeing this, someone changed config.py outside of a "
        "deliberate, reviewed execution-phase rollout. Stop."
    )

    logger.info("=== SignalForge run starting ===")

    _run_macro()
    _run_ipo_calendar()
    _run_paper_trading_updates()

    raw_events = []
    raw_events.extend(edgar.collect_all())
    raw_events.extend(quiver.collect_congress_trades())
    raw_events.extend(twitter.collect_all())
    raw_events.extend(reddit.collect_all())
    raw_events.extend(press_wire.collect_all())

    events = normalize(raw_events)
    if not events:
        logger.info("No new events after normalization — done.")
        return

    classified = classify_all(events)
    if not classified:
        logger.info("No events survived classification — done.")
        return

    sheets_configured = bool(settings.google_sheet_id and settings.google_service_account_json)

    history = []
    if sheets_configured:
        for tab in set(_SOURCE_TO_TAB.values()):
            try:
                history.extend(sheets_log.load_recent_history(tab=tab))
            except Exception as e:
                logger.warning("Could not load history from tab '%s' for cross-referencing: %s", tab, e)

    if history:
        seen = {_dedup_key(h) for h in history}
        before = len(classified)
        classified = [ce for ce in classified if _dedup_key(ce) not in seen]
        skipped = before - len(classified)
        if skipped:
            logger.info("Skipped %d event(s) already logged in a previous run (persistent dedup)", skipped)
        if not classified:
            logger.info("All classified events were already logged previously — nothing new to log/alert.")
            return

    classified = apply_crossref(classified, history)

    if sheets_configured:
        by_tab: dict = {}
        for ce in classified:
            tab = _SOURCE_TO_TAB.get(ce.event.source, settings.google_sheet_tab)
            by_tab.setdefault(tab, []).append(ce)
        for tab, group in by_tab.items():
            try:
                sheets_log.ensure_header(tab=tab)
                sheets_log.append_events(group, tab=tab)
            except Exception as e:
                logger.error("Failed to log events to Sheets tab '%s': %s", tab, e)
    else:
        logger.info("Google Sheets not configured — printing results instead:")
        for ce in classified:
            print(ce.to_sheet_row())

    send_alerts_above_threshold(classified)
    _run_paper_trading_entries(classified)

    logger.info("=== SignalForge run complete: %d events processed ===", len(classified))


if __name__ == "__main__":
    try:
        run_once()
    except Exception:
        logger.exception("SignalForge run failed")
        sys.exit(1)
