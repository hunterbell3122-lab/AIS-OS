# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

AdvnturHub targets overlapping audiences, primary age range 21–45, but the design must stay accessible and useful to older travelers and families:

- Urban professionals looking for short escapes
- Couples searching for unique dates and weekend getaways
- Families looking for age-appropriate activities
- Solo travelers seeking safe, manageable adventures
- Outdoor beginners who need clear instructions
- Experienced hikers, paddlers, cyclists, and explorers
- Tourists looking for activities near their destination
- Local residents who believe they've already seen everything nearby
- Budget-conscious travelers
- Dog owners looking for pet-friendly activities

## Product Purpose

AdvnturHub helps people discover worthwhile adventures, day trips, hidden destinations, outdoor activities, and short getaways within practical driving distance of where they live or travel. It answers: what should I do this weekend, where can I go within one or two hours, what hidden places are worth visiting, and how can I plan the entire experience without researching across ten separate websites.

Success is a visitor thinking "this is exactly what I was looking for" — and being able to execute the plan without leaving the site.

## Positioning

AdvnturHub does not merely list places — it turns a destination into an executable adventure plan. Every adventure entry is meant to answer why it's worth visiting, who it's best for, duration, difficulty, cost, distance, parking, permits/reservations, best time to go, family/dog/accessibility fit, safety risks, nearby food/lodging/rentals, and a weather/access backup plan.

Competes conceptually with AllTrails, Roadtrippers, Tripadvisor, Lonely Planet, Atlas Obscura, and Airbnb Experiences — not by imitation, but by combining discovery with full trip-logistics planning in one place.

Brand language is built around terms people already search (things to do near me, day trips, weekend getaways, hidden gems, scenic drives) rather than the internal concept term "micro-adventures," which may appear as supporting language only, never as the primary public-facing category or a traffic/comprehension dependency.

## Operating Context

Live at advnturhub.com. Current reality is **WordPress**, not the Next.js/Supabase/Stripe stack described in `advnturhub-master-build-prompt.md` — that document is aspirational/superseded planning, not implemented architecture.

- Hosting: Hostinger (hpanel/hcdn) — confirmed via response headers and plugin namespaces, despite an earlier assumption of HostGator.
- Plugin stack: WooCommerce, GiveWP (donations), Elementor, Fluent Forms, Jetpack.
- MCP connection: WordPress MCP Adapter plugin live at `https://advnturhub.com/wp-json/mcp/mcp-adapter-default-server`, registered locally as the `advnturhub` MCP server. Auth is a standard WordPress Application Password (Basic Auth) — not WordPress.com's OAuth2.1 flow, which does not apply to this self-hosted site.
- As of 2026-07-26, site is placeholder-stage: nav/structure and the plugin stack are installed, but core content ("What We Do," impact stories) is still Lorem ipsum. There is no real adventure/destination content, testimonials, or case studies yet — do not fabricate any.
- Not one of the three written Q3 2026 priorities (Guide Studio revenue, the Guide-Studio-vs-Kitchen-Design-Tool single-bet decision, one owned distribution asset). Work here is a deliberate scope call each time it resurfaces, not an assumed default.

## Capabilities and Constraints

Confirmed monetization (all three, not yet built out): affiliate links (gear, lodging, tours — requires FTC disclosure), WooCommerce-powered digital-product shop, GiveWP donations.

Legal/compliance requirements carried over from the build prompt as durable constraints once any of the above goes live: FTC affiliate disclosure on every page with affiliate links plus a standing disclosure policy page; privacy policy covering data/cookies/analytics/third-party processors; terms of service; a safety liability disclaimer component on every adventure/guide page (attorney review required before production launch); GDPR/CCPA consent baseline; confirmed sales-tax handling on digital goods.

Undecided: whether a Next.js migration ever happens — recorded as an open question, not a plan in progress.

## Brand Commitments

Name: **AdvnturHub**.

Personality: adventurous, smart, trustworthy, modern, practical, inspiring, premium but approachable, useful rather than promotional, visually immersive, easy to navigate, grounded in real planning details.

Explicitly avoid: generic travel clichés, excessive exclamation points, empty inspirational language, artificial urgency, overly rugged/exclusionary branding, cheap affiliate-site aesthetics, overly childish outdoor imagery, corporate jargon, confusing terminology.

## Evidence on Hand

None yet. Core content is Lorem ipsum placeholder as of 2026-07-26 — no real adventure write-ups, impact stories, testimonials, case studies, or press exist. Future work must not invent any of these; state the absence rather than filling it with plausible-sounding placeholder copy.

## Product Principles

1. Executable plans over listings — every adventure page answers the full logistics set (cost, difficulty, parking, permits, backup plan), not just what/where.
2. Mainstream search language wins — build around what people already type ("day trips," "things to do near me"); "micro-adventure" stays supporting-only.
3. Multi-audience by design — a single adventure page must serve outdoor beginners and experienced explorers without alienating either.
4. Trust before promotion — practical, grounded tone; disclosures are non-negotiable, not decorative; avoid hype and affiliate-site cheapness.
5. Reality over roadmap — the live WordPress site is the source of truth; the Next.js master-plan document is aspirational, not implemented.

## Accessibility & Inclusion

Must remain accessible and usable to older travelers and families despite the 21–45 primary target. The build prompt treats "accessible" as a first-class Explore filter facet alongside dog-friendly and family-friendly — treat this as a product requirement, not a nice-to-have.
