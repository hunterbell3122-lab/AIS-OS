---
type: community
members: 5
---

# SignalForge Reddit Collector

**Members:** 5 nodes

## Members
- [[Reddit collector — added after Phase 1 at Hunter's explicit request; the origina]] - rationale - SignalForge/signalforge/collectors/reddit.py
- [[_extract_ticker()]] - code - SignalForge/signalforge/collectors/reddit.py
- [[_get_access_token()]] - code - SignalForge/signalforge/collectors/reddit.py
- [[collect_all()_4]] - code - SignalForge/signalforge/collectors/reddit.py
- [[reddit.py]] - code - SignalForge/signalforge/collectors/reddit.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SignalForge_Reddit_Collector
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_SignalForge Data Collectors]]
- 2 edges to [[_COMMUNITY_SignalForge Main Orchestrator]]
- 1 edge to [[_COMMUNITY_SignalForge Classification Pipeline]]

## Top bridge nodes
- [[reddit.py]] - degree 8, connects to 3 communities
- [[collect_all()_4]] - degree 6, connects to 2 communities