# Decisions Log

Append-only record of meaningful decisions and why they were made. `/level-up` Phase 2 (Method interview) writes scoped automation specs here. You can also append manually whenever you decide something worth remembering.

**Format per entry:**

```
## YYYY-MM-DD — Short title

**Decision:** what was decided.

**Why:** the reasoning, constraints, and what would change your mind.

**Alternatives considered:** what else was on the table.

**Owner:** who's accountable.
```

Keep it terse. Future-you will thank present-you for capturing the *why*, not just the *what*.

---

## 2026-07-27 — ComplianceShield added as a 6th venture

**Decision:** Add ComplianceShield (Florida construction/skilled-trades compliance audit service + former FailSafe360 SaaS platform, merged) as a tracked venture, scaffolded at `ComplianceShield/` in this repo following the `TikTokShop/`/`SignalForge/` subfolder pattern. Full build sequencing lives in `ComplianceShield/PLAYBOOK.md`. Phase 0 (repo scaffolding) is done; Phase 1 (audit checklist engine) is blocked on `/shared/knowledge-base-export.md`, which doesn't exist yet.

**Why:** Hunter supplied a complete 10-phase build playbook and confirmed, when asked, that this is being added as a new venture rather than folded into an existing one or held for later.

**Alternatives considered:** Standalone repo outside the AIOS folder (rejected — no stated need for separate git history, and the existing multi-venture pattern already lives here). Holding the file without scaffolding (rejected — Hunter chose to proceed now).

**Tension to flag:** `context/priorities.md` explicitly diagnoses "five ventures across four markets means none get enough energy to compound" as a Q3 problem, and Priority 2 is forcing a single-bet decision between Guide Studio and the Kitchen Design Tool by 2026-08-01. This adds a sixth venture during that same window. Not reversing the decision, just noting it so it doesn't get lost — worth revisiting at the Aug 1 single-bet checkpoint.

**Owner:** Hunter

---

## 2026-07-26 — Guide Studio Etsy listing pipeline (Make.com)

**Decision:** Build an automated listing pipeline for Guide Studio's Etsy shop, run on Make.com:

- **Trigger:** daily scheduled run, pulls the next unlisted product from the Notion queue.
- **Data sources:** Notion (product content/backlog), Claude (drafts listing copy).
- **Transformations:** Notion product content → Claude-drafted title/description/SEO tags → Canva-generated thumbnail (Nano Banana 2) → assembled draft listing.
- **Decision point:** single email gate, Approve/Reject buttons only (no inline editing in v1).
- **Destination:** on Approve, Make.com posts the listing live to Etsy via its Etsy module. On Reject, nothing posts; item stays in the Notion queue for manual revision.
- **Autonomy level:** L2 (Drafted) — AI runs the full pipeline through draft; nothing goes live without a human click.
- **KPI:** bucket = more customers (distribution channel activation); metric = 1 listing published per day.

**Why:** Guide Studio is built but has zero live Etsy presence (account just created, no listings yet) — Priority 1 names this exact gap. Make.com was already connected and unused, making it the highest-leverage pick this week. EAD: Eliminate didn't apply — no prior manual listing process existed to eliminate, this is a build from zero, straight to Automate. One-per-day cadence chosen deliberately (both KPI and trigger) since steady catalog growth reads better to Etsy's discovery algorithm than a bulk dump on day one.

**Alternatives considered:** L1 (AI suggests, human executes every step) — rejected, not enough leverage. L4 (fully autonomous posting) — rejected for now, no track record yet on this shop; revisit after several clean approvals. Editable draft instead of approve/reject-only — deferred to a later iteration for shipping speed.

**Owner:** Hunter

---
