---
name: AdvnturHub
description: Executable adventure plans, not just place listings
colors:
  gradient-gold: "#FBB040"
  gradient-mid: "#F5773B"
  gradient-red: "#F04937"
  emphasis-solid: "#F5843C"
  dusk-charcoal: "#15120F"
  charcoal-2: "#1D1915"
  charcoal-3: "#262019"
  ash: "#B0B0B3"
  paper-warm: "#F5F1EA"
  paper-dim: "#DCD6C8"
typography:
  display:
    fontFamily: "Space Grotesk, system-ui, sans-serif"
    fontWeight: 700
  body:
    fontFamily: "DM Sans, system-ui, sans-serif"
    fontWeight: 400
rounded:
  card: "14px"
  pill: "999px"
---

<!-- Built: advnturhub-homepage.html is the first implementation of this world. Tokens below reflect what survived the build, not a pre-build seed. -->

# Design System: AdvnturHub

## Overview

**Creative North Star: "Trailhead at Dusk"**

The confirmed brand mark (hexagon badge, twin-peak mountain glyph, warm gold-to-red-orange gradient, "FIND YOUR PATH" tagline) is the fixed visual authority — extracted directly from the live logo, not invented. Everything else builds outward from it. The world reads as a trailhead sign at the last good light before dark: warm gradient signal against a deep, near-black ground, practical and legible rather than glossy. This is deliberately not the warm-cream-editorial-serif look AI design defaults to for outdoor/family subjects — the brief calls for adventurous-but-trustworthy, and cream-paper softness undersells the "executable plan" promise.

Rejected explicitly: cream/parchment grounds, glassmorphism, generic gradient-blob hero art, neon-dark-tech monoculture, stock "adventure" clichés (lens-flared mountain photos, italic script logotypes).

**Key Characteristics:**
- Warm gold→red-orange gradient as the one signature color move, used sparingly and at page scale (hero, primary CTAs, key accents) — never scattered as decoration.
- Deep charcoal ground, not black-black and not cream.
- Hexagon as the recurring geometric motif (badges, chips, card corners echo the logo's frame).
- Topographic contour-line texture as a background device, tying to trail maps and the mountain glyph.
- Geometric, modern type pairing — no serif-editorial default.

## Colors

Palette strategy: **Committed** — the gradient carries 30–60% of the surface at key moments (hero, CTAs); it does not appear as a thin accent line.

### Primary
- **Trailhead Gradient** (`linear-gradient(135deg, #FBB040 0%, #F5773B 50%, #F04937 100%)`) — sampled directly from the live logo's hexagon/mountain mark. Carries the hero background field, primary buttons, active states, and section dividers. Never used for body text (contrast risk).

### Neutral
- **Dusk Charcoal** (#15120F): primary page background — warm-tinted near-black, not pure #000, so the orange gradient reads warm rather than neon.
- **Ash** (#B0B0B3): sampled directly from the logo's own wordmark/tagline text color. Use for secondary/muted text and dividers on dark backgrounds — this is the logo's own neutral, so it's an inherited constant, not a new choice.
- **Paper Warm** (#F5F1EA): primary body/heading text on dark backgrounds — warm off-white, deliberately not stark white, to stay in the same warm family as the gradient. Confirmed against Dusk Charcoal at ~17:1 contrast.
- **Paper Dim** (#DCD6C8): secondary body copy (lede paragraphs, card hooks) — one step down from Paper Warm, still comfortably ≥4.5:1.

### Named Rules
**The One Gradient Rule.** The Trailhead Gradient appears as a full field (hero, button, divider), never as a text-fill or a thin one-pixel accent. The first build shipped with a gradient-clip headline emphasis and it was corrected during finishing — emphasis text uses solid **Emphasis Orange** (#F5843C) instead. If it needs to shrink below "a shape you'd notice," use Ash or Emphasis Orange instead.

## Typography

**Display Font:** Space Grotesk (with system-ui, sans-serif fallback)
**Body Font:** DM Sans (with system-ui, sans-serif fallback)

**Character:** Geometric and confident without going corporate-tech-mono; picked to match the wordmark's bold condensed energy while staying legible at body sizes — explicitly not a serif-display pairing, which would default this into the generic "warm outdoor/family" AI look the brief rejects.

### Hierarchy
- **Display** (Space Grotesk, 700, clamp(2.4rem, 5.4vw, 4rem)): hero headline only.
- **Headline** (Space Grotesk, 600, clamp(1.7rem, 3.4vw, 2.35rem)): section titles.
- **Title** (Space Grotesk, 600, 1.15–1.3rem): card and proof-panel titles.
- **Body** (DM Sans, 400, 1rem, 1.6 line-height, max 65–75ch): paragraph copy.
- **Label** (DM Sans, 500–700, 0.72–0.95rem): filter chips, meta chips, fact labels. Chips at this size read fine without forced uppercase/tracking — reserve uppercase+tracking for the smallest fact-label micro-copy (`.fact .k`, `.proof-label`) where it aids scannability.

## Layout

Single-column, mobile-first long scroll for the homepage. Generous vertical rhythm between sections (the "pace it like a studio" principle — dense sections earn a quiet one after). Container max-width ~1200px, comfortable side gutters. One primary responsive breakpoint collapses multi-column grids (adventure cards, footer columns) to single column on mobile.

## Elevation & Depth

Mostly flat with tonal layering (charcoal steps, not drop shadows) — depth comes from the gradient's own glow and contrast against Dusk Charcoal, not from generic box-shadows. A soft ambient glow (not a hard shadow) is acceptable directly under gradient-filled elements (buttons, featured card) to reinforce the "last light of dusk" idea.

### Named Rules
**The No Grey-Shadow Rule.** Depth comes from charcoal tonal steps or a warm ambient glow keyed to the gradient — never a neutral grey `box-shadow` sitting on top of the warm palette.

## Shapes

Hexagon is the signature recurring form — echoed at reduced scale in difficulty badges, filter chips, and card corner treatment (a clipped hexagonal corner cut on featured cards, subtle rounded corners elsewhere). Otherwise soft, moderate corner radii (not sharp rectangles, not pill-shaped everything) to stay approachable rather than either corporate or cutesy.

## Components

### Buttons
- **Shape:** fully pill (`border-radius: 999px`).
- **Primary:** Trailhead Gradient background, Dusk Charcoal text (dark-on-gradient tested at ≥5:1 across both gradient endpoints). Padding ~0.7rem/1.4rem.
- **Hover/Focus:** lifts 2px, gains a warm gradient-tinted glow (offset + blur, never a flat halo); focus ring is a solid Paper outline, never removed.
- **Ghost/Secondary:** transparent fill, 1px low-opacity Paper border; hover raises border opacity slightly. Used for secondary CTAs (never for two competing primaries side by side).

### Chips (filter chips, meta chips, example badge)
- **Style:** pill-shaped, Charcoal-2/Charcoal-3 background, Paper-Dim or Ash text.
- **Active/featured state (cost chip, active filter):** fills with the Trailhead Gradient, Dusk Charcoal text — same rule as buttons, gradient as a filled shape, never text.

### Cards (adventure cards)
- **Corner Style:** 14px radius, no hexagon clip on the card body itself (tried and rejected as impractical for legible content — the hexagon motif instead lives in the card's icon badge).
- **Background:** Charcoal-2 on Dusk Charcoal page background.
- **Depth:** flat at rest; hover adds a gradient-tinted ambient shadow (offset + blur) and a 4px lift.
- **Border:** 1px low-opacity Paper border at rest; warms toward the gradient's orange on hover.

### Hexagon icon badge
- **Signature component.** A small hexagon (clip-path polygon) filled with the Trailhead Gradient, holding a simple line-art SVG icon in Dusk Charcoal. This is the primary carrier of the logo's hexagon motif into the UI — used once per card, not repeated decoratively elsewhere.

### Navigation
- Sticky, blurred-charcoal bar. Text links at 0.86 opacity resting, full opacity on hover/focus. Primary CTA (gradient pill) anchors the right edge. Below 720px, text links hide behind the CTA remaining visible — no hamburger menu was built in this mockup (open decision, not resolved).

## Do's and Don'ts

### Do:
- **Do** treat the existing logo as fixed — do not redraw the mark, recolor it, or change the tagline.
- **Do** keep the gradient rare and page-scale; one hero field, one or two CTAs, not every icon.
- **Do** use the hexagon motif for at least one recurring UI element beyond the logo itself.
- **Do** label every placeholder adventure card as illustrative/example content.

### Don't:
- **Don't** default to a cream/parchment background or serif display type — confirmed anti-reference for this brief.
- **Don't** invent real testimonials, prices, customer counts, or benchmarks; label everything synthetic.
- **Don't** use stock lens-flare mountain photography or script-font logotypes anywhere on the page.
- **Don't** let the gradient touch body text directly (contrast/legibility risk).
