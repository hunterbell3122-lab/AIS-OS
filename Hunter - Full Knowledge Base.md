---
tags: [hunter, knowledge-base, master-index]
created: 2026-07-29
---

# Hunter — Full Knowledge Base

This is a consolidated export of everything on record from conversations with Claude, organized for Obsidian. Every section below corresponds to a discrete topic, project, or person. Internal links use `[[Obsidian wikilink]]` syntax — create matching notes/aliases if you want this to become a true linked vault, or leave as headers within this single file.

---

## 1. Profile

- **Name:** Hunter
- **Role:** Account Manager at Rapids & Affiliates, a foodservice equipment and supplies dealer operating across Iowa, Minnesota, and Missouri
- **Transition in progress:** Moving into a Business Development Lead role at the same company
- **Book of business:** Manages $4M+ annually
- **Domain expertise:** Foodservice equipment, including familiarity with brands like Alto-Shaam
- **Confirmed outbound sales skills:** Cold calling, cold email, LinkedIn prospecting, account visits, trade show networking
- **Skill set:** Prompt engineering, AI automation, systems thinking, sales
- **North star / long-term goal:** Exit corporate employment by building scalable, automated income streams
- **Self-described identity:** "The person who automates the job so you can leave it"

---

## 2. People

### 2.1 Partner (Wife)
- Enjoys traveling
- Traveled with Hunter to Shortsville, NY for the IRONMAN 70.3 Musselman race
- Has a close friend (and her husband) living in Pittsburgh, PA
- Interested in wineries, lakefront areas, coffee shops, shopping, casual sightseeing

### 2.2 Son — Dax
- Goes by "Dax"

---

## 3. Topics

### 3.1 Fitness
- Active in triathlon training
- Has weight loss goals
- No running limitations
- Registered or considering: Pigman Triathlon (Palo, IA) and Des Moines Triathlon at Gray's Lake
- Prepared for IRONMAN 70.3 Musselman — July 12, 2026, Shortsville, NY

### 3.2 Personal Interests
- Sports, hiking, the outdoors, dogs
- Pets: Ollie and Roo

### 3.3 Recent / Miscellaneous Work Activity
- Received a 30-day Claude Code mastery roadmap tied to business systems: Rapids & Affiliates email parsing, [[Guide Studio]] product enrichment, KPI automation
- Studied **Loop Engineering** — designing self-reinforcing automated systems; self-identified gap in closing feedback loops
- Job applications submitted to **Elastic** and **Canonical** (enterprise software sales roles); Claude produced targeted cover letters and screening responses; both awaiting response
  - Canonical prohibits AI-generated content in applications — flagged for extra care
- Resume repositioned around a "hunter" sales identity, anchored on the $4M+ book of business
- Explored autonomous wealth generation concepts; Claude redirected toward executing existing projects instead of new ideation
- **Recurring pattern flagged by Claude:** concept accumulation displacing actual monetization — repeated redirection toward closing revenue on existing builds rather than starting new ones
- Evaluated recession-resilient business concepts:
  - Answer Engine Optimization (AEO) agency — assessed by Claude as strongest, but with platform dependency risk
  - Eco-friendly ad-supported packaging
  - Repair video content library
  - IoT retail experience kits
- Analyzed a GitHub repo of 35 AI agent marketing skill files ("marketingskills" by Corey Haines) — top priorities identified: product-marketing-context, ai-seo, cold-email, revops, programmatic-seo
- Prior ventures: an activewear concept (H22), and a fitness-management background reframed as a sales leadership story
- **Tool stack hierarchy (established across sessions):**
  - **S-tier:** N8N, Claude
  - **Critical tier:** GitHub, VSCode, Notion
  - **Secondary:** GPT-4o, Perplexity, ElevenLabs
  - **Tertiary:** Gemini, Figma, NotebookLM

---

## 4. Active Projects / Ventures

### 4.1 AI Business Mastery (90-Day Curriculum)
- Structured 90-day AI business mastery curriculum with daily tracked progress
- Built into a Notion database via MCP integration, under the **Master Command Center**
  - Database ID: `6d822b74-540a-41cb-ac94-e6947ae4d9b2`
- Days 1–28: fully populated
- Days 29–90: still pending population
- Core AI automation stack: N8N, Claude API, GitHub, VSCode, Notion, GPT-4o, ElevenLabs, Gemini, Figma, Perplexity
- Preferred stack ranking: N8N (S-tier), Claude API (S-tier), GitHub/VSCode/Notion (Tier 1), Make.com as an alternative

### 4.2 Account Manager (AM) Automation
- Building an N8N + Salesforce-integrated follow-up sequencer to automate repetitive layers of the Account Manager role
- Goal: reclaim time for corporate exit ventures
- Relevant B2B context: Rapids Wholesale (rapidswholesale.com), used for sales work and automation testing
- Built a production-ready follow-up sequencer workflow (N8N + Salesforce)
- Key custom Salesforce fields required: `Last_Quote_Sent_Date__c`, `Last_Contact_Date__c` on the Opportunity object
- Claude flagged Apollo.io and Clay as weak fits for foodservice buyers; also flagged fine-tuning as the wrong approach at Hunter's data volume — recommended Retrieval-Augmented Generation (RAG) instead

### 4.3 Guide Studio
> **Flagged as Hunter's highest-priority near-term revenue action.**
- Fully functional, single-file HTML application for automated Etsy how-to guide production
- Three-step pipeline: niche finder → guide builder → Etsy listing generator, powered by the Claude API
- Features: niche research, guide generation, SEO-optimized listing output
- **Status:** Fully built but unlaunched — launching it is the current primary focus
- **Key unresolved challenge:** Hunter accumulates strong business concepts without closing revenue on any of them; Guide Studio is the flagged focal point for breaking that pattern

### 4.4 Heirloom Books (AI-Generated Heirloom Family History Books)
- Premium print-on-demand service combining genealogy data, AI narrative writing, and professional design
- Framed as a potential online, hands-off revenue vehicle
- Full phased execution blueprint received:
  1. Validation
  2. MVP build using Claude API + Canva
  3. Print-on-demand fulfillment via Blurb or Lulu
  4. Facebook/Instagram ad-driven sales

### 4.5 Commercial Kitchen Design Tool
*(aliases: kitchen design app, commercial kitchen designer, kitchen layout tool)*
- Web app that designs commercial kitchen layouts; residential use case deprioritized (back burner)
- Output: 2D layout, with an optional paid upgrade to 3D
- **Menu-driven:** what the operator plans to cook determines equipment needs and optimal layout
- Accounts for food storage, walk-in cooler/freezer space requirements, and planned delivery logistics
- Regional building/health code compliance pulled live from the web in a self-updating "loop" to stay current
- Equipment specs/dimensions pulled directly from manufacturer websites (URL/programmatic), offered as recommendations users can override
- Uses an LLM to guide users through layout arrangement by workflow and code — deliberately chosen over an algorithmic constraint-solver
- **Target customers:** restaurant groups (B2B) and direct-to-consumer at list price
- Manufacturers considered as a third stakeholder group (visibility, leads, integration)
- Fits Hunter's broader goal of building scalable ventures to exit corporate employment
- **Go-to-market decision:** independent-operator beachhead first; Iowa/Minnesota/Missouri as pilot jurisdictions; per-project fee monetization to start; kept firewalled from the Rapids & Affiliates day job
- Architect/GC compliance-checking tool (for architects who occasionally take restaurant projects and lack code expertise) scoped as a parallel v2 track
- Directed to build and execute the plan accordingly

### 4.6 Legal Intake AI
*(aliases: Legal Receptionist AI, AI legal receptionist, legal intake agent, after-hours intake)*
- Original brief: **"Legal Receptionist AI, Enterprise Edition"** — a full AI virtual receptionist for law firms, benchmarked against Smith.ai, Ruby Receptionists, Answering Legal, Back Office Betties, and LawDroid
- Original scope: call answering, screening, routing, scheduling, payment collection, bilingual English/Spanish support, 20 practice areas, analytics, and a continuous self-improvement loop
- **Narrowed wedge chosen instead:** after-hours intake for personal injury firms in a single metro; mandatory AI disclosure; no payment handling; one integration
- Four deliverables requested:
  1. Intake script with compliant disclosure language
  2. Clio integration spec
  3. Pricing model anchored against Smith.ai
  4. First ten-call test scorecard

### 4.7 Market Signal Tracker ("Project SignalForge")
*(aliases: autopilot idea, political trade tracker, congress trading bot, Project SignalForge, SignalForge)*
- Modeled on the "Autopilot" app concept
- Tracks disclosed trades from Congress (STOCK Act disclosures), hedge funds/institutions (13F filings), named investors (e.g., Buffett, Burry, Ackman), and traction on Reddit/Twitter
- Also tracks corporate executive/M&A events that could move a stock
- **Execution model:** alerts + one-click approval to execute matching trades — explicitly NOT fully automated execution
- Confirmed as a **standalone project**, kept separate from [[Day-Trading Scraper]] (different time horizon, sources, risk profile)
- Based in Iowa; starts in paper trading, eventually funds a dedicated live brokerage account kept separate from retirement/core investment accounts
- **Brokerage integration:** Alpaca as default/first-choice; cash-only and long-only initially — no margin, options, short selling, futures, forex, or leverage
- **Phase-gated rollout:**
  1. Intelligence-only
  2. Paper trading
  3. Shadow live mode
  4. Approval-required live pilot
  5. Limited single-strategy automation — only after explicit written approval
- **Strict MCP permission segmentation** for the Alpaca integration:
  - Research sessions get market-data/account-read/watchlist tools only
  - Live order-management tools kept fully separate
  - Paper and live credentials fully separate; no live keys ever entered in a Claude conversation
  - Independent kill switch
  - Full reconciliation and immutable audit logging of every request/approval/order/fill
- **Absolute rule:** no LLM or Claude session may ever directly submit, modify, cancel, or exercise a live order, regardless of approval or segmentation. Live order-management credentials must be technically unavailable to any Claude session — isolated in a standalone deterministic execution engine outside Claude and outside the research MCP server
- **Fail-closed requirement:** if the approval service, database, risk engine, market data, reconciliation, audit log, or execution engine becomes unavailable, no order may submit. Claude/manual natural-language instruction must never be used as a fallback execution path
- Full working Phase 1 codebase requested and delivered as `signalforge-project.zip`

### 4.8 Day-Trading Idea Scraper
*(aliases: trade idea scraper, day trading bot)*
- AI-powered web scraper pulling day-trading ideas from financial/news sites (RSS feeds)
- Pipeline: RSS feeds → Claude extraction → Markdown log → Discord notification
- AI summarizes and ranks ideas, logs to a running document, sends notifications
- **Decision:** build the lean MVP version rather than the full original spec
- Kept as a separate, standalone project from [[Market Signal Tracker]] (different time horizon, sources, and risk profile)

### 4.9 PCM Helmet Cooling Insert
*(aliases: helmet cooling insert, PCM helmet, triathlon helmet insert)*
- Concept: a phase change material (PCM)-based cooling insert — paraffin-wax or salt-hydrate PCM tuned to melt around 15–18°C — built into a triathlon aero helmet
- **Goal:** partner with a triathlon helmet brand and sell it as an upgraded model of helmet

### 4.10 Tripopotamous
- A travel and planning site
- Actively continuing as part of Hunter's corporate exit portfolio

### 4.11 RegTech Platform & Universal Health Tracker App (Evaluation)
- Both evaluated as primary corporate exit vehicle candidates
- Considered alongside [[Guide Studio]] and [[Tripopotamous]]
- Status: under active consideration (no further build activity logged)

---

## 5. Cross-Cutting Themes

- **Corporate exit strategy** is the unifying thread across nearly every project: [[Guide Studio]], [[Heirloom Books]], [[Commercial Kitchen Design Tool]], [[Legal Intake AI]], [[Market Signal Tracker]], [[Day-Trading Idea Scraper]], [[PCM Helmet Cooling Insert]], [[Tripopotamous]], and the [[RegTech Platform & Universal Health Tracker App]] evaluation are all candidate ventures toward that same goal.
- **Recurring diagnosed pattern:** concept accumulation without monetization. Claude has repeatedly flagged this and redirected focus toward finishing and launching existing builds — most notably [[Guide Studio]] — rather than generating new ideas.
- **Automation stack** (N8N, Claude/Claude API, GitHub, VSCode, Notion) is reused across the [[AI Business Mastery]] curriculum, [[AM Automation]] project, and multiple ventures.
- **Risk discipline** is a consistent design principle in financially-exposed projects — most visible in [[Market Signal Tracker]]'s fail-closed, no-LLM-execution architecture.

---

*End of export. This file reflects everything on record as of July 29, 2026.*
