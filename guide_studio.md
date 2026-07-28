# Guide Studio — Etsy Digital Product Engine

> *Automated Etsy digital product engine — niche to listing in minutes*

**Current Version:** 1.5 · 2026-07-23  
**File:** `etsy_guide_studio.html` (single-file, self-contained)  
**Runtime:** Browser — no server, no build step, no dependencies beyond Google Fonts  
**API:** Anthropic Claude Sonnet 4.6 (`claude-sonnet-4-6`) via `api.anthropic.com/v1/messages`

---

## Table of Contents

1. [Purpose](#purpose)
2. [Architecture Overview](#architecture-overview)
3. [Pipeline — Three-Step Workflow](#pipeline--three-step-workflow)
4. [API Integration](#api-integration)
5. [State Management](#state-management)
6. [Component Reference](#component-reference)
7. [Export System](#export-system)
8. [Error Handling & Resilience](#error-handling--resilience)
9. [Design System](#design-system)
10. [Version History](#version-history)
11. [Known Constraints](#known-constraints)
12. [Compliance Notes](#compliance-notes)
13. [Operational Checklist Before Publishing](#operational-checklist-before-publishing)

---

## Purpose

Guide Studio is a single-file browser application that automates the creation of Etsy digital product listings — from niche identification through to a publish-ready listing — using the Anthropic Claude API as the generative engine.

It is purpose-built for the **cleaning business owner tools** vertical (and analogous functional how-to niches), designed to produce defensible, non-AI-generated-image products that comply with Etsy's 2026 Creativity Standards enforcement environment.

The three deliverables it produces per session:

| Deliverable | Format | Use |
|---|---|---|
| Niche analysis | Scored cards (JSON-backed) | Product investment decision |
| Guide content | Markdown / print-ready HTML | The actual digital product file |
| Etsy listing | Title, 13 tags, description, pricing | Copy-paste to Etsy seller dashboard |

---

## Architecture Overview

```
etsy_guide_studio.html
│
├── <style>          Design system (CSS custom properties, all components)
├── <body>           Three-panel UI — one panel per pipeline step
└── <script>
    ├── VERSION      Semver constant + changelog array
    ├── state {}     Single source of truth for session data
    ├── callClaude() Streaming API wrapper (SSE reader)
    ├── callClaudeJSON() Non-streaming API wrapper (returns parsed JSON)
    ├── repairTruncatedJSON() Token-limit JSON salvage utility
    ├── Step 1       findNiches() → renderNiches() → selectNiche()
    ├── Step 2       buildGuide() → buildSingleGuide() | buildBundle()
    ├── Step 3       generateListing() → renderListing()
    ├── Export       exportGuideMarkdown/HTML, exportBundleMarkdown/HTML
    └── Utilities    renderMarkdown(), escapeHtml(), copyOutput(), setLoading()
```

No frameworks. No build toolchain. Vanilla HTML/CSS/JS — intentionally portable and auditable.

---

## Pipeline — Three-Step Workflow

### Step 1 — Niche Finder

**Inputs**

| Field | Type | Description |
|---|---|---|
| Broad Category | Text | e.g. "home repair", "personal finance" |
| Target Buyer Identity | Text | e.g. "first-time homeowners", "solo freelancers" |
| Price Anchor | Select | $4–$9 / $12–$20 / $25–$50 |

**Process**

Calls `callClaudeJSON()` with a structured prompt demanding exactly four niche objects. The system prompt prohibits preamble and backticks; the user prompt enforces field-level character caps to prevent token bloat.

**Output Schema (JSON)**

```json
{
  "niches": [
    {
      "name": "4–7 words, max 45 chars",
      "category": "max 25 chars",
      "description": "one sentence, max 110 chars",
      "demandScore": "0–10",
      "competitionScore": "0–10 (10 = no competition)",
      "viabilityScore": "0–10",
      "searchKeywords": ["kw1", "kw2", "kw3"],
      "economicStake": "max 90 chars",
      "tags": ["hot", "low-comp"]
    }
  ]
}
```

**Scoring Note:** `competitionScore` is inverted — 10 means virtually no competition. Score bars render green for competition (higher = better), yellow for demand, orange for viability. Scores are clamped to 0–10 before rendering to handle model drift.

**Selection:** User clicks a niche card to set `state.selectedNiche`. A persistent banner at the top of the UI displays the active niche across all subsequent steps.

---

### Step 2 — Guide Builder

**Mode: Single Guide**

Generates one complete how-to guide via the streaming `callClaude()` wrapper. Content streams character-by-character into the output panel via an inline markdown renderer.

**Inputs**

| Field | Options |
|---|---|
| Guide Title | Optional — auto-generated if blank |
| Guide Format | Step-by-step · Beginner's system · Checklist hybrid · Troubleshooting · Quick-start blueprint |
| Depth | Concise (8–12 steps, ~1,500 words) · Standard (12–18 steps, ~2,500 words) · Comprehensive (18–25 steps, ~4,000 words) |
| Tone | Direct/practical · Warm/encouraging · Expert authority · No-fluff tactical |
| Special Instructions | Free text — materials lists, audience callouts, budget focus, etc. |

**Required guide structure (enforced in prompt)**

1. Compelling title
2. Brief intro (2–3 sentences, buyer-problem hook)
3. What You'll Need / Prerequisites (if applicable)
4. Numbered step-by-step body
5. Common Mistakes to Avoid (3–5 items)
6. Pro Tips (3–5 items)
7. Brief close / next steps

---

**Mode: Bundle System**

Executes a two-phase pipeline:

**Phase 1 — Bundle Planning** (non-streaming JSON call)

Requests a `bundleName` and an array of `{title, focus}` objects for N guides (5–10, user-selected). Guides must be sequenced foundational → advanced and non-overlapping.

**Phase 2 — Sequential Guide Generation** (streaming, one guide at a time)

Each guide is generated in order. The UI renders an accordion per guide with live status badges: `Queued → Writing → Done / Failed`. Completed guides collapse automatically. Failed guides display inline error text and do not block subsequent guides.

On completion, `state.guideContent` is set to a concatenated markdown string of all bundle guides — this is what the listing step uses for context.

---

### Step 3 — Etsy Listing

**Inputs**

| Field | Description |
|---|---|
| Bundle Strategy | Single only · Single + bundle upsell hook · Bundle series framing |
| Competitor Price | Optional reference price to undercut or match |

**Output Schema (JSON)**

```json
{
  "title": "Max 140 characters — high-value keywords front-loaded",
  "tags": ["tag1", "...", "tag13"],
  "description": "150–300 words — buyer problem → product → what's inside → instant download → AI disclosure",
  "recommendedPrice": "Specific price with rationale (accounts for Etsy fee stack)",
  "launchStrategy": "4–6 bullet points"
}
```

**Etsy Fee Stack Used in Pricing Calculation**

- Transaction fee: 6.5%
- Payment processing: 3% + $0.25
- Listing fee: $0.20

**Output is displayed in three tabs:** Title + Tags · Description · Pricing + Strategy

All three fields support one-click copy-to-clipboard.

---

## API Integration

### Streaming Endpoint — `callClaude()`

Used for: guide content generation (single and each bundle guide)

```
POST https://api.anthropic.com/v1/messages
Content-Type: application/json

{
  model: "claude-sonnet-4-6",
  max_tokens: 1000,
  stream: true,
  system: "...",
  messages: [{ role: "user", content: "..." }]
}
```

Reads Server-Sent Events (SSE) via `ReadableStream`. Fires `onChunk(text)` callback on each `content_block_delta` event. The callback updates the DOM in real-time.

### Non-Streaming Endpoint — `callClaudeJSON()`

Used for: niche research, bundle planning, listing generation

Same endpoint, `stream: false`. Returns parsed JSON. Includes pre-parse cleanup: strips markdown code fences, trims to first `{` and last `}`.

### Token Limit Handling

When `stop_reason === "max_tokens"`, the response is assumed truncated. `repairTruncatedJSON()` is invoked as a salvage pass:

1. Walks the raw string character-by-character tracking string/escape state
2. Identifies the last position where a complete nested value closed (`cut`)
3. Slices to `cut`, strips trailing commas, re-closes any unclosed `{` or `[` brackets
4. Marks the result with `__truncated: true` so callers can surface a user warning

---

## State Management

All session data lives in a single `state` object. No `localStorage`, no cookies, no persistence across page loads.

```javascript
const state = {
  category: '',          // Step 1 input
  buyer: '',             // Step 1 input
  price: '',             // Step 1 price anchor selection
  selectedNiche: null,   // Full niche object from Step 1
  guideContent: '',      // Full guide text (single) or concatenated bundle text
  mode: 'single',        // 'single' | 'bundle'
  bundleGuides: [],      // [{ title: string, content: string }]
  bundleName: '',        // Bundle system name from Phase 1 planning
  currentStep: 1,        // Active pipeline step
  stepsCompleted: Set    // Steps marked done in nav
}
```

**Step navigation** is not gated — users can jump to any step via the pipeline nav bar. This is intentional: it allows regeneration without losing niche context.

---

## Component Reference

### Pipeline Nav Bar

Three-segment horizontal bar. Segments cycle through three visual states:

| State | Trigger | Visual |
|---|---|---|
| Default | Not yet visited | Dark background, muted label |
| Active | Currently selected | Accent yellow background, black text |
| Done | Step index < current step | Dark surface, green step number badge |

### Niche Cards

Rendered by `renderNiches()` from the JSON response. Each card contains:
- Category label (accent orange)
- Niche name (display font, large)
- Description (italic serif)
- Three score bars (Demand / Low Competition / Viability)
- Tag badges (hot / low-comp)
- Economic stake statement
- Search keyword tags

Click to select; re-click another card deselects the previous. Selection state is CSS-class-driven (`niche-card.selected`).

### Bundle Accordion

One accordion per guide in the bundle. Rendered before generation begins so status is visible during the sequential build. State machine per accordion:

```
Queued → Writing (yellow badge, body open) → Done (green badge, body collapsed)
                                           → Failed (body open with error text)
```

### Inline Markdown Renderer — `renderMarkdown()`

A bespoke block-level renderer (no external library). Supports:

- `#`, `##`, `###` headings → `<h1>`, `<h2>`, `<h3>`
- Numbered lists (`1.` / `1)`) → `<ol><li>`
- Bullet lists (`-`, `*`, `+`) → `<ul><li>`
- Horizontal rules (`---`, `***`, `___`) → `<hr>`
- Blank lines → paragraph breaks
- `**bold**` → `<strong>`
- `*italic*` → `<em>` (word-boundary anchored to avoid false positives)

All user-supplied and model-supplied strings pass through `escapeHtml()` before rendering to prevent XSS.

---

## Export System

| Function | Output |
|---|---|
| `exportGuideMarkdown()` | `{niche-slug}.md` — raw guide content |
| `exportGuideHTML()` | `{niche-slug}-printable.html` — print-ready single-guide document |
| `exportBundleMarkdown()` | `{bundle-slug}-bundle.md` — all guides concatenated with `---` separators |
| `exportBundleHTML()` | `{bundle-slug}-bundle-printable.html` — multi-guide print document with cover page and page-break dividers |

Print-ready HTML documents include embedded CSS with `@page { margin: 2cm }` and `.pagebreak { page-break-after: always }` for clean PDF generation via browser print dialog.

Files are delivered via a programmatic `<a>` click with `URL.createObjectURL()` — no server upload required.

---

## Error Handling & Resilience

| Scenario | Handling |
|---|---|
| Empty API response / no niches returned | Error box displayed; user prompted to refine inputs |
| HTTP error from API | Error message surfaced with status code |
| `stop_reason: max_tokens` on JSON call | `repairTruncatedJSON()` salvage pass; truncation warning shown; partial results displayed |
| Individual bundle guide failure | Guide marked Failed; remaining guides continue; partial export enabled |
| All bundle guides failed | Error box shown; export buttons hidden |
| Clipboard API unavailable | Copy button flashes "Copy failed" (graceful degradation) |
| Malformed JSON that cannot be salvaged | Full error message logged to console; user-facing message prompts retry |

---

## Design System

### Color Tokens

| Token | Value | Role |
|---|---|---|
| `--bg` | `#0a0a0a` | Page background |
| `--surface` | `#111111` | Card / panel background |
| `--surface2` | `#1a1a1a` | Hover state / secondary surface |
| `--border` | `#2a2a2a` | All borders |
| `--accent` | `#e8ff47` | Primary accent — yellow-green |
| `--accent2` | `#ff6b35` | Secondary accent — orange |
| `--text` | `#f0f0f0` | Body text |
| `--muted` | `#666` | Labels, placeholder text |
| `--muted2` | `#444` | Inactive UI elements |
| `--success` | `#47ff9a` | Done states, low-competition bars |
| `--error` | `#ff4747` | Error states |

### Typography

| Token | Font | Usage |
|---|---|---|
| `--font-display` | Barlow Condensed | Headings, labels, UI chrome |
| `--font-body` | DM Mono | Body text, code, metadata |
| `--font-serif` | Fraunces | Descriptions, guide content output |

### Responsive Breakpoints

Single breakpoint at `max-width: 600px`. Two-column grids collapse to one column. Mode toggle buttons stack vertically.

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.5 | 2026-07-23 | Version tracking system with badge + tooltip changelog |
| 1.4 | — | Token-limit truncation handling + JSON salvage (`repairTruncatedJSON`) |
| 1.3 | — | Etsy AI disclosure compliance + 9 defect fixes |
| 1.2 | — | Bundle system + file export |
| 1.1 | — | Model string + tab highlight fixes |
| 1.0 | — | Initial build |

---

## Known Constraints

- **`max_tokens: 1000` on all API calls.** This is intentionally conservative. Comprehensive guides (18–25 steps, ~4,000 words target) will be truncated at this limit. Raise to `4096` or higher for production use if longer output is required — verify cost impact first.
- **No API key management UI.** The key is injected at the infrastructure level (Anthropic's claude.ai artifact runtime). For self-hosted deployment, you must add an `Authorization: x-api-key {KEY}` header to both `callClaude()` and `callClaudeJSON()`.
- **Session-only state.** Refreshing the page resets everything. No persistence is built in by design.
- **Sequential bundle generation.** Guides are generated one at a time, not in parallel. A 7-guide bundle at standard depth will take 3–6 minutes depending on API latency.
- **Keyword data is hypothesis-grade.** The niche scores and search keywords are model-generated estimates. They must be validated against eRank or Marmalead before committing to a listing. The app does not have access to live keyword volume data.

---

## Compliance Notes

Etsy's 2026 Creativity Standards enforcement requires the following for AI-assisted digital products:

**In the listing description (auto-included by Guide Studio):**
> "This guide was created by me with the assistance of AI writing tools, then reviewed and edited for accuracy."

**In Etsy seller dashboard — set manually, these cannot be automated:**

| Field | Required Value |
|---|---|
| Attribution | "Designed by a seller" |
| who_made | "I did" |
| when_made | "Made to order" |
| is_supply | "A finished product" |

Failure to set these fields on an AI-assisted product is an active suspension risk under current Etsy enforcement.

---

## Operational Checklist Before Publishing

- [ ] Guide content reviewed and edited by a human for accuracy
- [ ] Etsy listing description includes AI disclosure line
- [ ] Dashboard fields set: who_made, when_made, is_supply, attribution
- [ ] Title validated against eRank / Marmalead for actual search volume
- [ ] Tags validated — no tag exceeds 20 characters (Etsy limit)
- [ ] Price verified against Etsy fee stack — target ≥ $15 for viable margin
- [ ] Product file (the guide itself) tested for download and readability
- [ ] Mockup images created — not auto-generated by this tool
- [ ] Listing reviewed by human before going live (Tier 2 approval gate)
