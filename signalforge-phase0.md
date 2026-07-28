# Project SignalForge — Phase 0: Strategic Research & Go/No-Go

## 0. A Boundary I Need to State Before Anything Else

Alpaca now ships an official MCP (Model Context Protocol) server that lets an LLM place live trades directly through natural language, in the same chat session. Your spec correctly identifies this as a bad idea (Non-Negotiable Principle 1: "Claude is not the final risk-control layer"). I'm going further than your spec on this one point: **I will not submit, approve, or trigger execution of a real-money order myself, in any chat or agent session, under any approval structure** — not even Phase 5 "specifically authorized strategy" automation. This isn't a technical limitation, it's a hard rule I operate under regardless of your authorization. Practically, this changes nothing about the architecture you designed: your Execution Engine is already specified as deterministic code, not an LLM call. I'll help you design, write, and test that code. The code fires the order. I don't, even by proxy through an MCP trade-execution tool. Keep the Alpaca MCP server pointed at paper trading only, or don't connect it to a Claude session at all for live keys.

---

## 0.5 MCP Permission Segmentation — Where I Diverge From the Addendum

Your addendum is good hardening and I'm adopting almost all of it as written: separate paper/live credentials, no live keys in a Claude conversation, no Claude-initiated withdrawals or permission changes, deterministic pre-trade risk checks before *and* immediately before submission, structural matching of approved-vs-submitted order fields, an independent kill switch, full reconciliation, and immutable audit logging. Build all of that regardless of what follows.

One place I need to be more restrictive than the addendum as written: the "Execution Session" concept still describes a session where Claude itself, after approval-matching succeeds, calls the Alpaca trading tool to submit a live order. I won't do that — not with least-privilege segmentation, not with cryptographic order-matching, not with every other safeguard in place. My rule is simpler and non-negotiable: **I do not invoke a tool that submits a live order, full stop, regardless of the approval architecture around it.** The distinction that matters to me isn't how tightly gated the "Execution Session" is — it's whether the actor pulling the trigger is an LLM inference or deterministic code. It has to be deterministic code.

Practically, this means: I'll help you write the execution engine as a standalone script or service (Python against Alpaca's REST API directly, not through an MCP tool call in a live chat session) that reads an approved-order record and submits it. That script is what fires. If you want a Telegram approval button to trigger execution, the button's webhook calls that script, not a Claude session. Research-only MCP access (market data, account read, watchlists) in a Claude session is fine under the segmentation you described; live order-management tools available to a Claude session are not, even gated.



The spec is unusually disciplined for a retail project of this kind — the phase-gating, kill switches, provenance requirements, and separation of LLM-as-analyst from deterministic-code-as-executor are the same architecture pattern used by firms that don't blow up accounts. That's the good news. The bad news: as scoped, this is a 6-12 month build for a small engineering team, not a side project. You are one person with a full-time Account Manager role transitioning into Business Development Lead. Read Section 3 before you commit calendar time to this.

**Go / No-Go recommendation: Go, but only if you cut Phase 0-1 scope by roughly 70% from what's written.** The full 24-module, 15-agent architecture is correct in direction and wrong in sequencing for a solo builder. Build the smallest version that proves the actual bottleneck — data quality and signal fusion, not agent count — before adding agents 4 through 15.

---

## 2. Primary Advantages

- Delayed-disclosure sources (13F, STOCK Act) are legally clean and won't get you in trouble the way scraping Discord servers or evading rate limits would.
- The bull/bear/arbitrator agent pattern is a legitimate way to use an LLM's actual strength (argument construction and critique) instead of asking it to "predict the stock," which it's bad at.
- The phase-gated brokerage rollout (intelligence-only → paper → shadow → approval-required live → limited automation) means you cannot accidentally fund a live account and lose real money before the system has any track record. That protection is worth preserving even as you cut scope elsewhere.

## 3. Primary Flaws and Risks

- **Scope-to-time mismatch.** 24 architecture modules and 15 agents is a team-of-5 build. Solo, sequenced correctly, expect Phase 0-1 alone to take 6-10 weeks of part-time effort, not the "let's start building" pace your other projects run at.
- **Signal edge is unproven, not assumed.** Congressional and 13F data is public and widely followed by exactly the tools in Section 5. Any edge that existed is partially arbitraged away by Quiver's own 25,000+ subscribers trading on the same alerts. Your entity-resolution and cross-referencing layer is the only place genuine edge could exist — everything else is commodity data everyone else has too.
- **Cost creep.** Real-time consolidated market data, options flow, and multiple paid filing APIs (Section 8) can run $150-400/month before you've placed a single trade. Budget this like a subscription, not a one-time cost.
- **Backtesting a delayed-disclosure strategy is unusually hard to do without look-ahead bias**, because the temptation to backtest off the transaction date instead of the public-disclosure date is constant and silently invalidates every result. Your spec already flags this (Non-Negotiable Principle 6) — it's the single easiest way this project produces a false-positive strategy that loses money live. Treat it as the top technical risk, not a checkbox.

---

## 4. Recommended Brokerage

**Alpaca**, for paper and eventual live trading. It's also the only major broker with an official MCP server, which matters for your approval-dashboard integration in Phase 4.

### 5. Brokerage Comparison

| Criterion | Alpaca | Interactive Brokers |
|---|---|---|
| API-first design | Yes — REST/WebSocket built for this use case | Yes, but built for a broader professional platform; steeper integration |
| Paper trading | Free, $100K simulated, unlimited | Free, high-fidelity, but account setup is heavier |
| Commission-free equities | Yes | Low-cost but not zero on all tiers |
| Fractional shares | Yes | Limited |
| Claude/MCP integration | Official first-party MCP server (paper by default, live requires explicit key swap) | No first-party MCP server as of this writing |
| Rate limits | ~200 calls/min free tier, 1,000/min funded | ~50 order messages/sec, 100 concurrent data lines |
| Asset breadth | US equities, ETFs, options, crypto | Much broader — global equities, futures, forex, bonds |
| Restrict money movement via API | Supported (narrow-scope keys, no withdrawal endpoint use) | Supported |
| Best for | Solo/small-team programmatic builds | Professional/institutional breadth, multi-asset |

For a pilot restricted to long-only US equities and ETFs with no margin, no options, no leverage (your own default restrictions), Alpaca's narrower feature set is a non-issue and its API is meaningfully faster to build against. Revisit Interactive Brokers only if you outgrow US-listed equities.

---

## 6. Recommended Architecture (Phase 0-1 Cut)

Build these first. Everything else in your 24-module list is a later phase, not a Phase 1 requirement:

1. **Filing collectors** — SEC EDGAR full-text search (free) + Quiver Quantitative API (Congress + insider, paid tier)
2. **Event normalizer** — turns raw filings into a common schema (ticker, event type, transaction/filing date, public timestamp, source)
3. **Classification + scoring** — one LLM call per event, using the taxonomy in Section 11, plus the cross-reference check
4. **Google Sheets logging** — your audit trail and where you eyeball results before trusting anything
5. **Telegram alerting** — notification only, no approval buttons yet

Skip for now: entity-resolution knowledge graph, social-attention service, 15-agent structure, backtesting engine. Add these once Phase 1 has run for a few weeks and you know which data sources are actually producing signal versus noise — building the knowledge graph before you have evidence it's needed is the classic way this kind of project stalls at 20% complete.

---

## 7. System Workflow (Phase 1)

```
Scheduled poll (EDGAR every 20 min, Quiver daily)
  → Parse filing → Normalize event
  → LLM classification (event type, direction, confidence)
  → Cross-reference check (same ticker in another category, trailing 30 days)
  → Log to Google Sheet
  → If confidence + cross-reference above threshold → Telegram alert
```

Phase 2 adds: paper-trade proposal generation and Alpaca paper-account simulation. Phase 3+ adds: approval buttons, live execution, agent expansion — only after Phase 1 has real output to evaluate.

---

## 8. Source Matrix (Condensed)

| Tier | Source | Cost | Latency | Notes |
|---|---|---|---|---|
| Regulatory | SEC EDGAR full-text search | Free | Real-time | Raw source of truth for everything |
| Congress | Quiver Quantitative API | $10-75/mo by tier | Up to 45-day disclosure lag | Cleanest programmatic Congress feed |
| Congress (free alt) | Tracefour | Free | Same lag, source is the disclosure itself | No API, browse/scrape their public pages |
| 13F institutional | WhaleWisdom | Free tier + paid | Quarterly, up to 45-day lag | Best for quarter-over-quarter change tracking |
| Named investors | Dataroma | Free | Quarterly | ~80 tracked "superinvestor" portfolios pre-aggregated |
| Insider (Form 4) | SEC EDGAR / Quiver | Free / paid | 2 business days | Fastest of the disclosure-based sources |
| 8-K events (exec changes, M&A) | SEC EDGAR / sec-api.io / Financial Modeling Prep | Free / paid | 4 business days | Your fastest structured signal |
| Market data | Alpaca (bundled with brokerage) | Free at pilot scale | Real-time (IEX feed) to near-real-time | Upgrade to consolidated (SIP) feed only if execution quality demands it |
| Social/attention | Quiver sentiment feeds, Unusual Whales | Paid | Real-time | Confirmation signal only, per your own Non-Negotiable Principle 3 |

Estimated Phase 1 monthly cost: **$25-90/month** (Quiver mid-tier + Google Workspace already in use + free EDGAR/Alpaca). This rises to $150-400/month once you add options flow, consolidated market data, and a second filing API in later phases.

---

## 9. Initial Agent Architecture (Phase 1 Cut)

Start with 3 roles, not 15:

1. **Classifier** — reads a normalized event, assigns taxonomy category and confidence
2. **Cross-Referencer** — deterministic code (not an LLM call) checking your event log for corroborating signals on the same ticker
3. **Summarizer** — writes the one-line alert text

Bull/Bear/Red-Team agents are valuable but belong in Phase 2+, once you're generating trade proposals, not just logging events. Running 3 extra LLM calls per event before you've validated the base classification is producing anything useful is wasted spend.

---

## 10. Initial Signal Taxonomy (Phase 1 Cut)

From your list, these five cover the highest-value, fastest-arriving signals:

- **A. Insider conviction** (Form 4 open-market buys, especially clusters of 3+ insiders)
- **D. Activist involvement** (new Schedule 13D)
- **E. Potential acquisition or change of control** (8-K Item 1.01/2.01)
- **G. Leadership transition** (8-K Item 5.02)
- **B. Institutional accumulation** (13F quarter-over-quarter adds)

Add the remaining 15 categories from your original taxonomy once you have Phase 1 data to know which ones are actually firing with useful frequency.

---

## 11. Initial Scoring Framework

Simple weighted score to start, not the full multi-factor model in your spec:

```
score = source_quality_weight
      + (2 if corroborated by a second tracked category within 30 days else 0)
      + (2 if open-market purchase vs. option exercise/gift/automatic sale else -1)
      + (1 per additional corroborating insider, capped at +3)
      - (1 if market cap or liquidity below your minimum threshold)
```

Route anything scoring above your chosen threshold to a Telegram alert. Refine into per-category models (your Section on Signal-Fusion) once you have real score distributions to calibrate against — building five separate scoring models before you have data to tune any of them produces five equally-uncalibrated models.

---

## 12. Risk-Policy Proposal (Conservative Defaults)

| Parameter | Proposed Default |
|---|---|
| Pilot capital | You decide — start small enough that a total loss doesn't matter to you emotionally or financially |
| Max position % | 5% of pilot capital per position |
| Max daily loss | 2% of pilot capital |
| Max portfolio drawdown | 15%, kill switch triggers |
| Max open positions | 10 |
| Max sector exposure | 25% |
| Minimum share price | $5 (avoids penny-stock manipulation risk) |
| Minimum avg daily dollar volume | $5M (liquidity floor) |
| Trading hours | Regular hours only, no extended hours |
| Allowed securities | Long-only US-listed common stock and ETFs |

These match your own stated defaults — I'm not changing your direction, just confirming it's the right starting point.

---

## 13. Recommended Validation Gates

Match your Phase 2-4 structure as written: minimum 60 calendar days and 100 eligible candidates in paper trading before shadow mode; shadow mode until proposed-vs-actual fills are consistently close; weekly review during approval-required live pilot before any single strategy is considered for Phase 5 automation. Do not compress these — the whole point of the gate structure is that it's slower than your instinct will want it to be.

---

## 14. Security Threat Summary

Highest-priority items from your threat list, given a solo-builder context: (1) API key exposure — never in chat, repo, or logs, use an OS keychain or `.env` excluded from git from day one; (2) prompt injection via filing/article content — treat all fetched filing and social text as data, never as instructions, which is already how I operate by default; (3) narrow-scope API keys with no withdrawal permission, enforced at the Alpaca account level, not just in your code; (4) duplicate-order prevention via unique client order IDs, which Alpaca's API supports natively.

---

## 15. Development Phases (Realistic Timeline)

| Phase | Scope | Est. build time (solo, part-time) |
|---|---|---|
| 0 | This document + your decisions on Section 21 | Done once you answer the questions below |
| 1 | Intelligence-only: collectors, classifier, Sheet log, Telegram alerts | 3-6 weeks |
| 2 | Paper trading via Alpaca, trade-proposal format | 2-4 weeks |
| 3 | Shadow mode | 1-2 weeks build + 2-4 weeks running |
| 4 | Approval-required live pilot, small capital | 2-3 weeks build + 60+ days running per your own gate |
| 5 | Single-strategy limited automation | Only after Phase 4 produces evidence — no fixed timeline |

## 16. Estimated Monthly Costs by Phase

Phase 1: $25-90. Phase 2-3: add nothing (paper trading is free). Phase 4: $150-400/month if you add options flow, consolidated data, or a second paid filing API; otherwise stays near Phase 1 cost.

---

## 17. Recommended Initial Watchlist Categories

Start with three, not twelve: (1) Congress members on committees relevant to sectors you understand from your foodservice/equipment background or otherwise track closely, (2) Dataroma's pre-aggregated superinvestor list rather than building your own from scratch, (3) corporate insiders at companies already on your radar. Expand to activist investors, journalists, and social accounts in Phase 2+, once the watchlist-scoring logic in your spec has been tested against a smaller set.

---

## 18. Twenty Additional Legal Data Signals Worth Evaluating

Executive stock option repricing, insider 10b5-1 plan adoption/cancellation timing, corporate jet flight-tracking (public ADS-B data, used as a due-diligence signal by some funds), state-level lobbying registration changes, university endowment 13F filings, SBIR/STTR federal grant awards, USPTO patent litigation filings (vs. patent grants, a different and faster-moving signal), FDA advisory committee meeting calendars, state pension fund 13F filings, corporate 8-K auditor-change filings specifically (a known distress signal), UCC lien filings (state-level, signals secured borrowing), H-1B visa petition data by employer (hiring-trend proxy), Federal Reserve beige book regional mentions, GSA schedule contract awards, court PACER docket filings for named companies, S-1/S-4 draft registration leaks via EDGAR "DRS" filings, credit default swap spread data where accessible, ISS/Glass Lewis proxy advisory recommendations ahead of shareholder votes, corporate share-buyback authorization announcements vs. actual repurchase execution (frequently diverge), and state attorney general investigation announcements.

---

## 19. Relationship to Day-Trading-Scraper

Confirmed separate, per your spec and my earlier read: different time horizon, different data sources, different risk profile. Share only the notification layer and logging pattern if convenient — keep data sources, classification logic, and execution paths fully isolated.

---

## 20. Ten Questions That Need Your Decision

1. Pilot capital amount — even a rough range changes position-sizing defaults.
2. Which brokerage account will this be — new dedicated account, or do you already have an Alpaca account from another project?
3. Do you want Phase 1 built now, or do you want to see Quiver's actual data quality (via their free tier) before subscribing to anything paid?
4. Google Sheets or a proper database (Supabase/Postgres) for logging — Sheets is faster to start, a database is better once volume grows. Which matters more to you right now, speed or scale?
5. Telegram or Discord for alerts — you already use Discord for day-trading-scraper; same channel type or deliberately separate?
6. How much of your own review time per week are you realistically willing to spend reading alerts and approving/rejecting proposals during Phase 4?
7. Sector or industry focus, or fully open universe? A focus (e.g., your foodservice/equipment domain expertise) would let you add a human-judgment layer no automated system has.
8. Are you building this yourself in Python, or do you want me to scaffold it for you to run?
9. Minimum viable alert threshold — how much noise are you willing to tolerate in exchange for not missing a real signal?
10. Timeline pressure — is this a background project with no deadline, or do you want Phase 1 live within a specific number of weeks?

---

## 21. First Component to Build, and Why

**Build the SEC EDGAR + Quiver polling script with the classification prompt (Section 6, items 1-3) first**, logging to a single Google Sheet with no alerting yet. Reasoning: this is the cheapest possible way to find out whether the classification and cross-reference logic actually produces signal worth acting on, before you spend a single hour on Telegram bots, entity graphs, or execution engines. If the Sheet fills up with noise you wouldn't act on, you've learned that for a few hours of work instead of a few months.

**Inputs required from you:** answers to Section 20, plus a Quiver Quantitative account (free tier is enough to start) and a Google account with Sheets API access already set up (you likely have this from day-trading-scraper).

**Phase 0 acceptance criteria:** you've reviewed this document, answered the ten questions, and given explicit go-ahead on the Phase 1 scope in Section 6 before any code gets written.
