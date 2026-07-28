# Connections

Registry of every system your AIOS can reach. Filled by `/onboard` from Q4-Q7 answers; expanded over time as you wire new tools. `/audit` checks this file for domain coverage and freshness.

| # | Domain | Tool | Mechanism | Auth | Last checked |
|---|---|---|---|---|---|
| 1 | Revenue / Financials | None yet (pre-revenue) | not yet connected | — | — |
| 2 | Customer interactions | None yet (no customers) | not yet connected | — | — |
| 3 | Calendar | Google Calendar | not yet connected (Google Drive is connected; Calendar is not the same connector) | — | — |
| 4 | Communication | Gmail (primary); phone, text, Facebook Messenger, Snapchat | mcp | connected (Gmail live; phone/text/Messenger/Snapchat remain informal, unconnected) | 2026-07-26 |
| 5 | Project / task tracking | None dedicated yet — Notion is connected (row 7) but not yet adopted for this | not yet connected | — | — |
| 6 | Meeting intelligence | Otter (transcription, as needed) | not yet connected | — | — |
| 7 | Knowledge / files | Notion | mcp | connected | 2026-07-26 |
| 8 | AdvnturHub (travel platform, self-hosted WP on Hostinger) | WordPress MCP Adapter plugin, `advnturhub` MCP server | mcp | pending — needs WP Application Password | 2026-07-26 |
| 9 | Automation / workflow | Make.com | mcp | connected, not yet wired to a workflow | 2026-07-26 |
| 10 | Design / creative assets | Canva, Figma | mcp | connected | 2026-07-26 |
| 11 | File storage | Google Drive | mcp | connected | 2026-07-26 |
| 12 | Work suite (secondary, unclear active use) | Microsoft 365 | mcp | connected | 2026-07-26 |

**Mechanism options:** `mcp` (MCP server), `script` (Python/Bash hitting an API, in `scripts/`), `export` (CSV/JSON dump pipeline), `key+ref` (`.env` key + `references/{tool}-api.md` guide), `not yet connected`.

When you wire a new tool, also save `references/{tool}-api.md` capturing endpoints, auth flow, and common queries — researched-once-saved-forever.
