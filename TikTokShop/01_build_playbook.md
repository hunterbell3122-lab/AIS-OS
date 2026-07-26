# One-Day Build: TikTok Shop Operating System

Output of the "Build the complete minimum viable TikTok Shop Operating System today" command, run 2026-07-25. Loops applied: Requirement Completion, Platform Reality, Product Selection, Compliance Gate, Production Readiness, Automation Debugging.

## 1. Requirement Completion — assumptions made

| Item | Status | Assumption (if missing) |
|---|---|---|
| Business model | Assumed | TikTok Shop **Affiliate Creator** (promote existing sellers' products for commission), not Seller. Lowest setup cost, fastest to test. |
| Account status | Assumed | Zero followers, new/existing personal TikTok account, US-based, 18+. |
| TikTok Shop eligibility | Verified (web, July 2026) | See Section 2 — not yet eligible for Shop features. |
| Product category | Assumed | Home organization / kitchen tools / desk accessories — low-risk, high visual-demo categories. |
| Tool stack | Assumed | Minimum-viable stack, Section 4 — Claude, Sheets, CapCut, phone camera, free voiceover. |
| Daily content volume | Assumed | 3–5 videos/day target; realistically 1–2/day while building the workflow solo. Flagged as open question. |
| Compliance rules | Included | Section 2 + Section 6. |
| Publishing workflow | Defined | Manual drafts in TikTok app until 1,000-follower threshold and workflow are proven — Section 7. |
| Metrics | Defined | Section 9. |
| Human approval gates | Defined | Every video requires manual compliance + final-look approval before posting. No auto-publish. |

**Open question:** realistic daily volume given this is a solo, part-time operation alongside Guide Studio/Kitchen Design Tool work. Flagged in Section 12.

## 2. Platform Reality (verified July 2026)

**TikTok Shop Affiliate Creator eligibility (US):**
- 1,000 followers minimum to apply.
- 18+, US-based, identity verification required.
- Account in good standing (no Community Guidelines strikes), no revoked e-commerce permissions.
- Under 5,000 followers → 30-day **Creator Pilot Program** with posting caps, not full affiliate access. 5,000 followers is the graduation line out of the pilot, not the entry bar.
- Alternative: register as a **Seller** (own storefront) — works at zero followers via a linked Marketing Account, but requires business/product setup and inventory or dropship sourcing. Heavier lift, not the MVP path.

**Consequence for this build:** You cannot post shoppable video #1 today. The first phase of content must be non-shoppable, follower-building content in the target niche. Once past 1,000 followers, apply for Affiliate Creator status and start attaching product links.

**AI disclosure rules:**
- Required when AI generates or meaningfully alters a *realistic depiction of a person, place, or event* that a viewer could mistake for real (e.g., AI avatars, synthetic voices standing in for a real presenter).
- **Exempt:** AI-assisted captions, hashtags, on-screen text, and script writing. So Claude writing scripts/captions needs no disclosure — an AI avatar presenting them does.
- Deepfakes of real people are banned outright, disclosed or not.
- TikTok auto-detects via C2PA Content Credentials + watermarking; mislabeling risks a 4-tier penalty up to permanent ban.

**Practical read:** faceless with real product B-roll + voiceover needs no AI disclosure (CapCut/TikTok TTS voiceover isn't a synthetic clone of a real identifiable person).

**Personal constraint (operator decision, not a platform rule): the creator's face never appears on camera, permanently — not a Day-1-only default.** No AI avatar substitutes for it either; the operator confirmed pure faceless (product B-roll, hands/close-ups, voiceover) as the only production format for this channel. This removes the AI-avatar disclosure workflow entirely — there's nothing to disclose because nothing synthetic is standing in for a person.

**Required manual checks before every post:** product still in stock/linked correctly, claims match what's actually demonstrable on camera, no face (including partial/reflection/shadow that reads as identifiable) visible in any frame.

## 3. Business Model Recommendation

**Path: Affiliate Creator, pure faceless (no avatar, no on-camera presenter), home/kitchen/desk organization niche.**

Why: lowest capital risk (no inventory), fastest content velocity (no filming or avatar setup), category has strong visual-demo potential and low compliance risk (no health/beauty/financial claims to manage), and TikTok Shop actively promotes these categories to new accounts. Pure faceless was an explicit operator decision (2026-07-25) — the AI-avatar path was considered and rejected, not just deferred.

**Positioning:** "the useful drawer" — a small, faceless account that shows one genuinely useful home/desk/kitchen fix per video. Useful-first, salesy-second — per the spec's Brand & Trust rule, this is what keeps a faceless account from reading as spam.

## 4. Account Setup Checklist

- [ ] Create or repurpose one TikTok account (dedicated to this niche, not mixed with personal).
- [ ] Switch to Business or Creator account type (unlocks analytics).
- [ ] Write bio: one line on what the account posts + who it's for. No shop-link claims yet (not eligible).
- [ ] Turn on TikTok analytics.
- [ ] Do **not** apply for Shop/Affiliate yet — wait for 1,000 followers (Section 2).
- [ ] Set up identity-verification documents in advance so the affiliate application is fast once eligible.

## 5. Tool Stack — mandatory vs. optional

| Function | Mandatory (Day 1) | Optional upgrade |
|---|---|---|
| Strategy/scripting | Claude | Claude Project with this repo's files as knowledge |
| Trend/product research | TikTok Creative Center, TikTok search | Google Trends, Amazon Best Sellers |
| Production board | Google Sheets (`product_board.csv` in this repo) | Airtable / Notion |
| Asset storage | Google Drive folder | Dropbox |
| Editing | CapCut (free) | Adobe Premiere Pro |
| Voiceover | CapCut built-in voice / TikTok voice | ElevenLabs |
| Avatar video | **Not used — pure faceless is a locked decision, not a phase** | N/A |
| Automation | Manual + Sheets | Make/Zapier/n8n once volume justifies it |
| Publishing | Manual TikTok draft upload | Approved scheduler once available |
| Analytics | TikTok native analytics + Sheets | Looker Studio |

Total mandatory spend: **$0/month.** Nothing here requires a paid tool to start.

## 6. Compliance Checklist (run before every post)

- [ ] No fake testimonial or fake "I used this" claim unless the product was actually used on camera.
- [ ] No before/after unless real and demonstrable.
- [ ] No health, beauty, medical, financial, or performance claims.
- [ ] No fake scarcity/pricing/shipping claims.
- [ ] No copied footage, no unlicensed music.
- [ ] No AI avatar, no on-camera presenter — pure faceless is a hard rule for this channel, not just a compliance minimum.
- [ ] No face (including partial, reflection, or shadow that reads as identifiable) visible in any frame.
- [ ] Caption and hashtags relevant, not spammy.
- [ ] Product link (once eligible) correct and live.
- [ ] Video understandable with sound off (captions burned in).
- [ ] Verdict recorded: Approved / Revise / Blocked — nothing posts without "Approved."

## 7. Product Scoring Rubric (120-point, 12 categories × 10)

Impulse-buy strength · Visual demo strength · Problem urgency · Price attractiveness · Commission/margin · Seller reliability · Review quality · Shipping reliability · Low compliance risk · Content angle depth · Trend strength · Audience breadth.

**Decision rule:** ≥85 → Test. 70–84 → Watch. <70 → Reject (or document a specific strategic exception).

Full scored candidates: [product_board.csv](product_board.csv).

## 8. Competitor Deconstruction Template

```text
Pattern name:
Product category:
First frame:
Hook type:
Video structure:
Proof used:
Buyer trigger:
Ethical original version:
Risks to avoid:
```

**Note on sourcing:** the patterns below are general, widely-observed short-form-commerce archetypes, not extracted from any specific creator's video (no TikTok Creative Center account access from this session). Before scaling, replace these with 5 patterns pulled directly from TikTok Creative Center for your actual niche — that's a Day-2 action, not a Day-1 blocker.

| Pattern | Structure | Ethical use |
|---|---|---|
| "Wait, it does WHAT" reveal | Show the annoying problem (2s) → reveal product mid-action → payoff shot | Show your own product footage doing the same job |
| Mistake correction | "You're doing X wrong" → show common mistake → show the fix (the product) | Only if the "mistake" is genuinely common, not invented |
| Silent demo + captions | No voiceover, just captions + product in motion, trending audio | Requires strong first-frame, works well sound-off |
| Object POV | Camera as if you're the buyer discovering the product on your counter/desk | Easy to shoot solo, no face needed |
| Comparison split-screen | Old messy way vs. new way with product, side by side | Must be a fair, real comparison |

## 9. Hook Library Starter (15 hooks, product-agnostic patterns to fill in)

1. "This is why your [space] always looks messy."
2. "Nobody told me this existed until [timeframe]."
3. "POV: you finally fix the thing that's bugged you for years."
4. "I didn't believe this would fit until I tried it."
5. "This is the $[X] fix for a problem you've had since [event]."
6. "Stop doing [common workaround]. Do this instead."
7. "The most oddly satisfying [category] fix I've found."
8. "If you have a [specific space], you need to see this."
9. "This took my [space] from chaos to this in 30 seconds."
10. "Three things in my [room] that finally make sense."
11. "This is what I wish I had before [common frustrating moment]."
12. "The $[X] thing that solved a problem I didn't know had a name."
13. "Watch this before you buy another [generic alternative]."
14. "This is the most requested fix in my comments."
15. "I almost didn't post this because it's so simple."

Rule: reject any hook that could apply to *any* product — every hook must name the specific problem or space.

## 10. Script Template

```text
Product:
Angle:
Target buyer:
First frame:
First spoken line:
Voiceover:
On-screen text:
Shot list:
Caption:
Hashtags:
Call to action:
Proof needed:
Compliance notes:
AI disclosure notes:
```

## 11. Production Workflow

**Pure faceless — the only production format for this channel (locked 2026-07-25):**
1. Shoot product in real use, 9:16, natural light, phone camera. Hands/close-ups only — no face in frame, ever.
2. Voiceover via CapCut TTS, or a recorded voice track that never appears on camera.
3. Burn in captions (auto-caption + manual cleanup).
4. B-roll: 3–5 short clips of the product solving the problem.
5. Export 1080x1920, cover frame = clearest problem/solution shot, no face.

No AI avatar workflow — considered and rejected, not deferred. If this ever changes, it needs a fresh decision, not a default reversion.

**CapCut editing timeline:**
- 0:00–0:03 hook (visual + text, no wasted setup)
- 0:04–0:08 problem shown
- 0:09–0:20 product solving it
- 0:21–0:25 payoff / result shot
- 0:26–0:30 CTA + caption reinforcement
- Captions on every line, thumbnail = clearest mid-action frame.

## 12. Automation Recipes (Day-1, manual-first)

| Workflow | Trigger | Action | Tool | Approval gate |
|---|---|---|---|---|
| New product intake | New row added to board | Score against rubric, assign tier | Sheets + manual | Human scores it |
| Script draft | Product marked "Test" | Generate script via Claude command (Section in `today_2026-07-25.md`) | Claude | Human runs Compliance Checklist |
| Compliance check | Script marked "Ready" | Run Section 6 checklist | Manual | Human signs off before "Approved" |
| Post prep | Video edited | Add to posting calendar, write caption/hashtags | Sheets | Human confirms before draft upload |
| Metrics logging | 48h after post | Enter views/clicks/saves into board | Manual, from TikTok analytics | N/A — no auto-publish involved |

Nothing here auto-posts. That's intentional — the spec's rule is "automate repetition, not responsibility."

## 13. Posting Calendar (template)

| Date | Time | Product | Angle | Status |
|---|---|---|---|---|
| Fill in from `today_2026-07-25.md` and each day after | | | | Draft / Scheduled / Published |

## 14. Metrics Dashboard Schema

Views · 2-second hold rate · 6-second hold rate · avg watch time · completion rate · likes · comments · shares · saves · product clicks · click-through rate · add-to-cart · purchases · commission · refunds · negative comments.

## 15. 30-Day Execution Plan

- **Days 1–7:** Post non-shoppable, useful content daily (or every other day, realistically). Build the habit and the workflow. No product links possible yet.
- **Days 8–14:** Review Week 1 with `weekly_optimization.md`. Double down on the hook/format that held attention. Keep posting.
- **Days 15–21:** If nearing 1,000 followers, prep the Affiliate Creator application (ID verification docs ready per Section 4).
- **Days 22–30:** Apply for Affiliate Creator once eligible. Attach product links to the best-performing existing angles. First shoppable posts.
- **Ongoing:** Weekly optimization every 7 days; monthly strategy reset at day 30.

## 16. Open Issues

1. Realistic daily content volume for a solo, part-time operator — 3–5/day per spec is aggressive; recommend starting at 1/day and raising once the workflow is fast.
2. No account exists yet — Section 4 checklist is unstarted.
3. Competitor patterns in Section 8 are generic, not pulled from live TikTok Creative Center data — refresh once you have account access.
4. Whether this venture gets formally added to `context/about-business.md` given the Aug 1 single-bet commitment (see README strategic flag).

## 17. Exact Next Actions

1. Create/convert the TikTok account (Section 4).
2. Pick the actual first product from `product_board.csv` top 3.
3. Shoot one faceless video today using `today_2026-07-25.md` script #1.
4. Post it as a draft, review against Section 6 checklist, then publish.
5. Log it as a row on the posting calendar and metrics board.
