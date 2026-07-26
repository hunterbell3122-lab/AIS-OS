# SignalForge — Phase 1 (Intelligence-Only)

Tracks legally disclosed Congress trades and SEC filings (8-K executive/M&A events,
Form 4 insider transactions, Schedule 13D activist stakes), classifies them, checks
for cross-referencing signals, logs to Google Sheets, and sends Telegram alerts
above a confidence threshold.

**There is no brokerage connectivity in this codebase.** That's deliberate — see
`CLAUDE.md` and `docs/signalforge-phase0.md` for the full reasoning and the
non-negotiable execution boundary this project operates under.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Fill in .env — at minimum ANTHROPIC_API_KEY is required to run at all.
# QUIVER_API_KEY, Google Sheets, and Telegram are all optional — the pipeline
# degrades gracefully (prints to stdout, skips alerts) if they're unset.
```

To use Google Sheets logging: create a Google Cloud service account, download
its JSON key, share your target Sheet with the service account's email address
(found in the JSON file), and set `GOOGLE_SERVICE_ACCOUNT_JSON` and
`GOOGLE_SHEET_ID` in `.env`.

To use Telegram alerts: create a bot via @BotFather, get the token, and get your
chat ID (message the bot once, then check
`https://api.telegram.org/bot<TOKEN>/getUpdates`).

## Running

```bash
python -m signalforge.main
```

Wire this to cron or a scheduled task for the polling cadence set in
`config.py` (EDGAR every 20 min, Quiver daily, by default).

## Testing

```bash
python -m pytest signalforge/tests/ -v
```

The cross-reference logic (`crossref.py`) is the actual signal-quality lever in
this project and has real unit tests. The collectors, classifier, Sheets, and
Telegram modules are thin API plumbing — better verified against live sandboxed
credentials than mocked, so they don't have unit tests here. Test them by running
`main.py` with real (or free-tier) credentials and checking the output.

## Known Limitations / Next Steps

- **EDGAR 8-K item filtering is not yet implemented.** Full-text search returns
  all 8-Ks, not filtered to Items 1.01/2.01/5.02 specifically — that requires
  fetching and parsing the actual filing document. Until that's added, expect
  higher noise from the EDGAR 8-K collector than from Form 4 or Quiver.
- `transaction_date` is often `None` for EDGAR-sourced events (full-text search
  doesn't expose it) — only `public_disclosure_date` is guaranteed populated.
  Fine for Phase 1 alerting; will need fixing before any future backtesting work.
- `config.py` validates `ANTHROPIC_API_KEY` eagerly at import time. This means
  even `crossref.py`'s standalone unit tests need a dummy value in the
  environment to import cleanly (see `tests/test_crossref.py` — run with
  `ANTHROPIC_API_KEY=test python -m pytest ...` if you haven't set up `.env` yet).
- Phase 1 scope stops here on purpose. Do not add brokerage code, entity
  resolution, the 15-agent structure, or backtesting to this repo without
  reading `docs/signalforge-phase0.md` first — those are later, deliberately
  separate phases.
