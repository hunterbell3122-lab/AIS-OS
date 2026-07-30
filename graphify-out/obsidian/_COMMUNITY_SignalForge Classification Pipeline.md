---
type: community
members: 28
---

# SignalForge Classification Pipeline

**Members:** 28 nodes

## Members
- [[.buy_sell_signal()]] - code - SignalForge/signalforge/schema.py
- [[.to_sheet_row()]] - code - SignalForge/signalforge/schema.py
- [[Classification one Claude API call per normalized event, using the exact prompt]] - rationale - SignalForge/signalforge/classify.py
- [[ClassifiedEvent]] - code - SignalForge/signalforge/schema.py
- [[Common normalized-event schema. Every collector must emit RawEvent objects; ever]] - rationale - SignalForge/signalforge/schema.py
- [[Cross-reference check deterministic code, not an LLM call.  Flags a classified]] - rationale - SignalForge/signalforge/crossref.py
- [[Cross-reference is the actual signal-quality lever in this project, so it gets a]] - rationale - SignalForge/signalforge/tests/test_crossref.py
- [[Telegram alerting — notification only, Phase 1. No approval buttons, no callback]] - rationale - SignalForge/signalforge/telegram_alert.py
- [[Two events in the same run, on the same ticker, different categories,     should]] - rationale - SignalForge/signalforge/tests/test_crossref.py
- [[_build_prompt()]] - code - SignalForge/signalforge/classify.py
- [[_format_message()]] - code - SignalForge/signalforge/telegram_alert.py
- [[_make_classified()]] - code - SignalForge/signalforge/tests/test_crossref.py
- [[apply_crossref()]] - code - SignalForge/signalforge/crossref.py
- [[classify.py]] - code - SignalForge/signalforge/classify.py
- [[classify_all()]] - code - SignalForge/signalforge/classify.py
- [[classify_event()]] - code - SignalForge/signalforge/classify.py
- [[crossref.py]] - code - SignalForge/signalforge/crossref.py
- [[history previously logged classified events (typically loaded from the     Goog]] - rationale - SignalForge/signalforge/crossref.py
- [[schema.py]] - code - SignalForge/signalforge/schema.py
- [[send_alert()]] - code - SignalForge/signalforge/telegram_alert.py
- [[send_alerts_above_threshold()]] - code - SignalForge/signalforge/telegram_alert.py
- [[telegram_alert.py]] - code - SignalForge/signalforge/telegram_alert.py
- [[test_crossref.py]] - code - SignalForge/signalforge/tests/test_crossref.py
- [[test_crossref_hit_within_window()]] - code - SignalForge/signalforge/tests/test_crossref.py
- [[test_crossref_no_hit_different_ticker()]] - code - SignalForge/signalforge/tests/test_crossref.py
- [[test_crossref_no_hit_outside_window()]] - code - SignalForge/signalforge/tests/test_crossref.py
- [[test_crossref_no_hit_same_category()]] - code - SignalForge/signalforge/tests/test_crossref.py
- [[test_crossref_within_same_batch()]] - code - SignalForge/signalforge/tests/test_crossref.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SignalForge_Classification_Pipeline
SORT file.name ASC
```

## Connections to other communities
- 18 edges to [[_COMMUNITY_SignalForge Data Collectors]]
- 15 edges to [[_COMMUNITY_SignalForge Main Orchestrator]]
- 5 edges to [[_COMMUNITY_SignalForge Paper Trading]]
- 1 edge to [[_COMMUNITY_SignalForge EDGAR Collector]]
- 1 edge to [[_COMMUNITY_SignalForge Reddit Collector]]

## Top bridge nodes
- [[schema.py]] - degree 17, connects to 5 communities
- [[ClassifiedEvent]] - degree 21, connects to 2 communities
- [[telegram_alert.py]] - degree 11, connects to 2 communities
- [[classify.py]] - degree 9, connects to 2 communities
- [[crossref.py]] - degree 7, connects to 2 communities