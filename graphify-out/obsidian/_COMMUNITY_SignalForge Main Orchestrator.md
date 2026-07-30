---
type: community
members: 41
---

# SignalForge Main Orchestrator

**Members:** 41 nodes

## Members
- [[Google Sheets logging.  Requires a Google Cloud service account with access to t]] - rationale - SignalForge/signalforge/sheets_log.py
- [[IPO calendar data is already fully structured — no confidencecrossref     score]] - rationale - SignalForge/signalforge/telegram_alert.py
- [[Load recent rows back into ClassifiedEvent objects for cross-referencing.     On]] - rationale - SignalForge/signalforge/sheets_log.py
- [[Macro releases have no confidencecrossref score to gate on — every new     (ded]] - rationale - SignalForge/signalforge/telegram_alert.py
- [[Mark-to-market existing open paper positions — independent of this     run's new]] - rationale - SignalForge/signalforge/main.py
- [[Opens new paper positions for events that just cleared the same bar as     a rea]] - rationale - SignalForge/signalforge/main.py
- [[Returns a set of (deal_id, stage) keys already logged. A deal moving     from 'f]] - rationale - SignalForge/signalforge/sheets_log.py
- [[Returns a set of (source_subtype, headline, public_disclosure_date) keys     alr]] - rationale - SignalForge/signalforge/sheets_log.py
- [[Returns trade_id - {ticker, direction, entry_date, entry_price,     company, ev]] - rationale - SignalForge/signalforge/sheets_log.py
- [[Separate from the ticker-centric pipeline on purpose — see     collectorsipo_ca]] - rationale - SignalForge/signalforge/main.py
- [[Separate from the ticker-centric pipeline on purpose — see     collectorsmacro_]] - rationale - SignalForge/signalforge/main.py
- [[SignalForge Phase 1 orchestrator.  Run manually with `python -m signalforge.main]] - rationale - SignalForge/signalforge/main.py
- [[_dedup_key()]] - code - SignalForge/signalforge/main.py
- [[_get_service()]] - code - SignalForge/signalforge/sheets_log.py
- [[_ipo_key()]] - code - SignalForge/signalforge/main.py
- [[_macro_key()]] - code - SignalForge/signalforge/main.py
- [[_run_ipo_calendar()]] - code - SignalForge/signalforge/main.py
- [[_run_macro()]] - code - SignalForge/signalforge/main.py
- [[_run_paper_trading_entries()]] - code - SignalForge/signalforge/main.py
- [[_run_paper_trading_updates()]] - code - SignalForge/signalforge/main.py
- [[annotations ticker - {recommendation str, target_price str}.      Rewrit]] - rationale - SignalForge/signalforge/sheets_log.py
- [[append_events()]] - code - SignalForge/signalforge/sheets_log.py
- [[append_ipo_events()]] - code - SignalForge/signalforge/sheets_log.py
- [[append_macro_events()]] - code - SignalForge/signalforge/sheets_log.py
- [[append_paper_trade_observations()]] - code - SignalForge/signalforge/sheets_log.py
- [[collectors__init__.py]] - code - SignalForge/signalforge/collectors/__init__.py
- [[ensure_header()]] - code - SignalForge/signalforge/sheets_log.py
- [[ensure_ipo_header()]] - code - SignalForge/signalforge/sheets_log.py
- [[ensure_macro_header()]] - code - SignalForge/signalforge/sheets_log.py
- [[ensure_paper_trades_header()]] - code - SignalForge/signalforge/sheets_log.py
- [[load_ipo_history()]] - code - SignalForge/signalforge/sheets_log.py
- [[load_macro_history()]] - code - SignalForge/signalforge/sheets_log.py
- [[load_paper_trades_summary()]] - code - SignalForge/signalforge/sheets_log.py
- [[load_recent_history()]] - code - SignalForge/signalforge/sheets_log.py
- [[main.py]] - code - SignalForge/signalforge/main.py
- [[run_once()]] - code - SignalForge/signalforge/main.py
- [[send_ipo_alert()]] - code - SignalForge/signalforge/telegram_alert.py
- [[send_macro_alert()]] - code - SignalForge/signalforge/telegram_alert.py
- [[sheets_log.py]] - code - SignalForge/signalforge/sheets_log.py
- [[signalforge__init__.py]] - code - SignalForge/signalforge/__init__.py
- [[update_ipo_recommendations()]] - code - SignalForge/signalforge/sheets_log.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SignalForge_Main_Orchestrator
SORT file.name ASC
```

## Connections to other communities
- 21 edges to [[_COMMUNITY_SignalForge Data Collectors]]
- 15 edges to [[_COMMUNITY_SignalForge Classification Pipeline]]
- 3 edges to [[_COMMUNITY_SignalForge Paper Trading]]
- 2 edges to [[_COMMUNITY_SignalForge EDGAR Collector]]
- 2 edges to [[_COMMUNITY_SignalForge Reddit Collector]]

## Top bridge nodes
- [[main.py]] - degree 31, connects to 5 communities
- [[run_once()]] - degree 18, connects to 4 communities
- [[sheets_log.py]] - degree 20, connects to 2 communities
- [[load_recent_history()]] - degree 6, connects to 2 communities
- [[send_macro_alert()]] - degree 5, connects to 2 communities