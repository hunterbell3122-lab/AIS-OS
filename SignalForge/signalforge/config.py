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

    # --- Twitter/X (social collector — added after Phase 1; see CLAUDE.md) ---
    twitter_bearer_token: str = field(default_factory=lambda: _optional("TWITTER_BEARER_TOKEN", ""))
    twitter_search_query: str = field(
        default_factory=lambda: _optional(
            "TWITTER_SEARCH_QUERY",
            '(insider OR "activist stake" OR "13D" OR acquisition OR accumulation) has:cashtags -is:retweet lang:en',
        )
    )
    google_sheet_tab_twitter: str = field(default_factory=lambda: _optional("GOOGLE_SHEET_TAB_TWITTER", "X"))

    # --- Reddit (social collector — added after Phase 1; see CLAUDE.md) ---
    reddit_client_id: str = field(default_factory=lambda: _optional("REDDIT_CLIENT_ID", ""))
    reddit_client_secret: str = field(default_factory=lambda: _optional("REDDIT_CLIENT_SECRET", ""))
    reddit_user_agent: str = field(
        default_factory=lambda: _optional("REDDIT_USER_AGENT", "SignalForge/0.1")
    )
    reddit_search_query: str = field(
        default_factory=lambda: _optional(
            "REDDIT_SEARCH_QUERY", "insider buying OR activist stake OR 13D OR acquisition rumor"
        )
    )
    reddit_subreddits: List[str] = field(
        default_factory=lambda: ["wallstreetbets", "stocks", "investing", "SecurityAnalysis"]
    )
    google_sheet_tab_reddit: str = field(default_factory=lambda: _optional("GOOGLE_SHEET_TAB_REDDIT", "Reddit"))

    # --- Press wires (free RSS, no API key — added post-Phase-1) ---
    press_wire_user_agent: str = field(
        default_factory=lambda: _optional("PRESS_WIRE_USER_AGENT", "SignalForge research@example.com")
    )
    press_wire_feeds: List[tuple] = field(
        default_factory=lambda: [
            ("PR Newswire - M&A", "https://www.prnewswire.com/rss/mergers-and-acquisitions-list.rss"),
            (
                "PR Newswire - Financial Services",
                "https://www.prnewswire.com/rss/financial-services-latest-news/financial-services-latest-news-list.rss",
            ),
        ]
    )

    # --- Macro calendar (free official RSS — added post-Phase-1) ---
    # Deliberately separate from event_categories/classify_event() — see
    # collectors/macro_calendar.py's module docstring for why.
    macro_feeds: List[tuple] = field(
        default_factory=lambda: [
            ("BLS - CPI", "https://www.bls.gov/feed/cpi.rss"),
            ("BLS - Employment Situation", "https://www.bls.gov/feed/empsit.rss"),
            ("Federal Reserve - Press Releases", "https://www.federalreserve.gov/feeds/press_all.xml"),
        ]
    )
    google_sheet_tab_macro: str = field(default_factory=lambda: _optional("GOOGLE_SHEET_TAB_MACRO", "Macro"))

    # --- IPO calendar (free Nasdaq public API — added post-Phase-1) ---
    ipo_calendar_enabled: bool = True
    google_sheet_tab_ipo: str = field(default_factory=lambda: _optional("GOOGLE_SHEET_TAB_IPO", "IPO"))

    # --- Paper trading tracker (no brokerage, no real money — see paper_trading.py) ---
    paper_trading_enabled: bool = True
    paper_trading_tracking_days: int = 30  # ~20 trading days, kept as calendar days for simplicity
    google_sheet_tab_paper_trades: str = field(
        default_factory=lambda: _optional("GOOGLE_SHEET_TAB_PAPER_TRADES", "Paper Trades")
    )

    # --- Polling cadence (minutes) ---
    edgar_poll_interval_minutes: int = 20
    quiver_poll_interval_minutes: int = 1440  # daily
    social_poll_interval_minutes: int = 60
    press_wire_poll_interval_minutes: int = 30
    macro_poll_interval_minutes: int = 60
    ipo_poll_interval_minutes: int = 240

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
