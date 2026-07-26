"""
SignalForge configuration.

All values here are Phase 1 defaults from the design brief (docs/signalforge-phase0.md
and CLAUDE.md). Override via environment variables — never hardcode secrets here.
"""

import os
from dataclasses import dataclass, field
from typing import List

from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            f"Copy .env.example to .env and fill it in."
        )
    return val


def _optional(name: str, default: str = "") -> str:
    return os.getenv(name, default)


@dataclass(frozen=True)
class Settings:
    # --- Anthropic (classification) ---
    anthropic_api_key: str = field(default_factory=lambda: _require("ANTHROPIC_API_KEY"))
    classifier_model: str = field(default_factory=lambda: _optional("CLASSIFIER_MODEL", "claude-sonnet-4-6"))

    # --- Quiver Quantitative ---
    quiver_api_key: str = field(default_factory=lambda: _optional("QUIVER_API_KEY"))
    quiver_base_url: str = "https://api.quiverquant.com/beta"

    # --- SEC EDGAR ---
    edgar_base_url: str = "https://efts.sec.gov/LATEST/search-index"
    edgar_user_agent: str = field(
        default_factory=lambda: _optional(
            "EDGAR_USER_AGENT", "SignalForge research@example.com"
        )
    )

    # --- Google Sheets ---
    google_service_account_json: str = field(
        default_factory=lambda: _optional("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    )
    google_sheet_id: str = field(default_factory=lambda: _optional("GOOGLE_SHEET_ID", ""))
    google_sheet_tab: str = field(default_factory=lambda: _optional("GOOGLE_SHEET_TAB", "Events"))

    # --- Telegram ---
    telegram_bot_token: str = field(default_factory=lambda: _optional("TELEGRAM_BOT_TOKEN", ""))
    telegram_chat_id: str = field(default_factory=lambda: _optional("TELEGRAM_CHAT_ID", ""))

    # --- Polling cadence (minutes) ---
    edgar_poll_interval_minutes: int = 20
    quiver_poll_interval_minutes: int = 1440  # daily

    # --- Signal taxonomy: Phase 1 categories only (Phase 0 doc, Section 10) ---
    event_categories: List[str] = field(
        default_factory=lambda: [
            "insider_conviction",
            "activist_involvement",
            "potential_acquisition_or_control_change",
            "leadership_transition",
            "institutional_accumulation",
        ]
    )

    # 8-K items mapped to event categories we care about in Phase 1
    edgar_8k_items: List[str] = field(
        default_factory=lambda: ["1.01", "2.01", "5.02"]  # agreements/M&A, control change, leadership
    )

    # --- Alert threshold ---
    min_confidence_for_alert: int = 7
    require_crossref_for_alert: bool = True
    crossref_lookback_days: int = 30

    # --- Safety ---
    # This is intentionally the only "execution-adjacent" setting in the whole project,
    # and it does nothing but prevent accidental scope creep. Phase 1 has no brokerage
    # code at all. If this ever becomes True somewhere, that's a bug, not a feature.
    BROKERAGE_EXECUTION_ENABLED: bool = False


settings = Settings()
