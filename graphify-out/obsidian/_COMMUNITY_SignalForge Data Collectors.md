---
type: community
members: 40
---

# SignalForge Data Collectors

**Members:** 40 nodes

## Members
- [[.now_utc_iso()]] - code - SignalForge/signalforge/schema.py
- [[.to_dict()]] - code - SignalForge/signalforge/schema.py
- [[Any]] - code
- [[Drop events with no ticker (unresolvable), dedupe, and strip whitespace.]] - rationale - SignalForge/signalforge/normalize.py
- [[IPO calendar collector — free, public API that backs Nasdaq's own IPO calendar p]] - rationale - SignalForge/signalforge/collectors/ipo_calendar.py
- [[Macro calendar collector — free, official RSS feeds (BLS, Federal Reserve).  Del]] - rationale - SignalForge/signalforge/collectors/macro_calendar.py
- [[Normalization dedupe and clean raw events from all collectors before classifica]] - rationale - SignalForge/signalforge/normalize.py
- [[Press-wire collector — free, public RSS feeds (no API key, no scraping behind au]] - rationale - SignalForge/signalforge/collectors/press_wire.py
- [[Quiver Quantitative collector.  Pulls recent congressional trade disclosures. Re]] - rationale - SignalForge/signalforge/collectors/quiver.py
- [[RawEvent]] - code - SignalForge/signalforge/schema.py
- [[Settings]] - code - SignalForge/signalforge/config.py
- [[SignalForge configuration.  All values here are Phase 1 defaults from the design]] - rationale - SignalForge/signalforge/config.py
- [[TwitterX collector — added after Phase 1 at Hunter's explicit request; the orig]] - rationale - SignalForge/signalforge/collectors/twitter.py
- [[_collect_feed()]] - code - SignalForge/signalforge/collectors/macro_calendar.py
- [[_collect_feed()_1]] - code - SignalForge/signalforge/collectors/press_wire.py
- [[_dedupe_key()]] - code - SignalForge/signalforge/normalize.py
- [[_extract_ticker()_1]] - code - SignalForge/signalforge/collectors/twitter.py
- [[_fetch_month()]] - code - SignalForge/signalforge/collectors/ipo_calendar.py
- [[_is_non_english()]] - code - SignalForge/signalforge/collectors/press_wire.py
- [[_is_spam()]] - code - SignalForge/signalforge/collectors/press_wire.py
- [[_load_ticker_lookup()]] - code - SignalForge/signalforge/collectors/press_wire.py
- [[_match_company()]] - code - SignalForge/signalforge/collectors/press_wire.py
- [[_optional()]] - code - SignalForge/signalforge/config.py
- [[_parse_date()]] - code - SignalForge/signalforge/collectors/ipo_calendar.py
- [[_require()]] - code - SignalForge/signalforge/config.py
- [[_rows_for_stage()]] - code - SignalForge/signalforge/collectors/ipo_calendar.py
- [[_strip_suffix()]] - code - SignalForge/signalforge/collectors/press_wire.py
- [[collect_all()_1]] - code - SignalForge/signalforge/collectors/ipo_calendar.py
- [[collect_all()_2]] - code - SignalForge/signalforge/collectors/macro_calendar.py
- [[collect_all()_3]] - code - SignalForge/signalforge/collectors/press_wire.py
- [[collect_all()_5]] - code - SignalForge/signalforge/collectors/twitter.py
- [[collect_congress_trades()]] - code - SignalForge/signalforge/collectors/quiver.py
- [[config.py]] - code - SignalForge/signalforge/config.py
- [[ipo_calendar.py]] - code - SignalForge/signalforge/collectors/ipo_calendar.py
- [[macro_calendar.py]] - code - SignalForge/signalforge/collectors/macro_calendar.py
- [[normalize()]] - code - SignalForge/signalforge/normalize.py
- [[normalize.py]] - code - SignalForge/signalforge/normalize.py
- [[press_wire.py]] - code - SignalForge/signalforge/collectors/press_wire.py
- [[quiver.py]] - code - SignalForge/signalforge/collectors/quiver.py
- [[twitter.py]] - code - SignalForge/signalforge/collectors/twitter.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SignalForge_Data_Collectors
SORT file.name ASC
```

## Connections to other communities
- 21 edges to [[_COMMUNITY_SignalForge Main Orchestrator]]
- 18 edges to [[_COMMUNITY_SignalForge Classification Pipeline]]
- 8 edges to [[_COMMUNITY_SignalForge EDGAR Collector]]
- 4 edges to [[_COMMUNITY_SignalForge Reddit Collector]]
- 1 edge to [[_COMMUNITY_SignalForge Paper Trading]]

## Top bridge nodes
- [[config.py]] - degree 17, connects to 5 communities
- [[RawEvent]] - degree 39, connects to 4 communities
- [[.now_utc_iso()]] - degree 10, connects to 3 communities
- [[press_wire.py]] - degree 12, connects to 2 communities
- [[ipo_calendar.py]] - degree 9, connects to 2 communities