---
type: community
members: 10
---

# SignalForge Paper Trading

**Members:** 10 nodes

## Members
- [[Paper-trading tracker — no brokerage, no real money, nothing here ever touches a]] - rationale - SignalForge/signalforge/paper_trading.py
- [[Returns new 'entry' observation rows for qualifying events not already tracked.]] - rationale - SignalForge/signalforge/paper_trading.py
- [[_compute_return_pct()]] - code - SignalForge/signalforge/paper_trading.py
- [[_get_price()]] - code - SignalForge/signalforge/paper_trading.py
- [[_qualifies()]] - code - SignalForge/signalforge/paper_trading.py
- [[_trade_id()]] - code - SignalForge/signalforge/paper_trading.py
- [[open_new_positions()]] - code - SignalForge/signalforge/paper_trading.py
- [[open_trades trade_id - {ticker, direction, entry_date, entry_price,     compan]] - rationale - SignalForge/signalforge/paper_trading.py
- [[paper_trading.py]] - code - SignalForge/signalforge/paper_trading.py
- [[update_open_positions()]] - code - SignalForge/signalforge/paper_trading.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SignalForge_Paper_Trading
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_SignalForge Classification Pipeline]]
- 3 edges to [[_COMMUNITY_SignalForge Main Orchestrator]]
- 1 edge to [[_COMMUNITY_SignalForge Data Collectors]]

## Top bridge nodes
- [[paper_trading.py]] - degree 11, connects to 3 communities
- [[open_new_positions()]] - degree 7, connects to 2 communities
- [[update_open_positions()]] - degree 5, connects to 1 community
- [[_qualifies()]] - degree 3, connects to 1 community
- [[_trade_id()]] - degree 3, connects to 1 community