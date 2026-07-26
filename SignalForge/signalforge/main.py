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

from signalforge.collectors import edgar, quiver
from signalforge.normalize import normalize
from signalforge.classify import classify_all
from signalforge.crossref import apply_crossref
from signalforge import sheets_log
from signalforge.telegram_alert import send_alerts_above_threshold
from signalforge.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("signalforge.main")


def run_once():
    assert settings.BROKERAGE_EXECUTION_ENABLED is False, (
        "BROKERAGE_EXECUTION_ENABLED must be False in Phase 1. "
        "If you're seeing this, someone changed config.py outside of a "
        "deliberate, reviewed execution-phase rollout. Stop."
    )

    logger.info("=== SignalForge run starting ===")

    raw_events = []
    raw_events.extend(edgar.collect_all())
    raw_events.extend(quiver.collect_congress_trades())

    events = normalize(raw_events)
    if not events:
        logger.info("No new events after normalization — done.")
        return

    classified = classify_all(events)
    if not classified:
        logger.info("No events survived classification — done.")
        return

    history = []
    if settings.google_sheet_id and settings.google_service_account_json:
        try:
            history = sheets_log.load_recent_history()
        except Exception as e:
            logger.warning("Could not load history for cross-referencing: %s", e)

    classified = apply_crossref(classified, history)

    if settings.google_sheet_id and settings.google_service_account_json:
        try:
            sheets_log.append_events(classified)
        except Exception as e:
            logger.error("Failed to log events to Sheets: %s", e)
    else:
        logger.info("Google Sheets not configured — printing results instead:")
        for ce in classified:
            print(ce.to_sheet_row())

    send_alerts_above_threshold(classified)

    logger.info("=== SignalForge run complete: %d events processed ===", len(classified))


if __name__ == "__main__":
    try:
        run_once()
    except Exception:
        logger.exception("SignalForge run failed")
        sys.exit(1)
