---
type: community
members: 13
---

# SignalForge EDGAR Collector

**Members:** 13 nodes

## Members
- [[Collect recent 8-K filings. Note full-text search returns the form type,     no]] - rationale - SignalForge/signalforge/collectors/edgar.py
- [[Query EDGAR full-text search for a given form type, most recent filings.]] - rationale - SignalForge/signalforge/collectors/edgar.py
- [[SEC EDGAR collector.  Pulls recent 8-K filings (Items 1.01, 2.01, 5.02), Form 4]] - rationale - SignalForge/signalforge/collectors/edgar.py
- [[_hit_to_event()]] - code - SignalForge/signalforge/collectors/edgar.py
- [[_n_days_ago()]] - code - SignalForge/signalforge/collectors/edgar.py
- [[_parse_display_name()]] - code - SignalForge/signalforge/collectors/edgar.py
- [[_search_edgar()]] - code - SignalForge/signalforge/collectors/edgar.py
- [[_today()]] - code - SignalForge/signalforge/collectors/edgar.py
- [[collect_13d_events()]] - code - SignalForge/signalforge/collectors/edgar.py
- [[collect_8k_events()]] - code - SignalForge/signalforge/collectors/edgar.py
- [[collect_all()]] - code - SignalForge/signalforge/collectors/edgar.py
- [[collect_form4_events()]] - code - SignalForge/signalforge/collectors/edgar.py
- [[edgar.py]] - code - SignalForge/signalforge/collectors/edgar.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SignalForge_EDGAR_Collector
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_SignalForge Data Collectors]]
- 2 edges to [[_COMMUNITY_SignalForge Main Orchestrator]]
- 1 edge to [[_COMMUNITY_SignalForge Classification Pipeline]]

## Top bridge nodes
- [[edgar.py]] - degree 14, connects to 3 communities
- [[collect_all()]] - degree 6, connects to 2 communities
- [[_hit_to_event()]] - degree 8, connects to 1 community
- [[collect_8k_events()]] - degree 6, connects to 1 community
- [[collect_form4_events()]] - degree 5, connects to 1 community