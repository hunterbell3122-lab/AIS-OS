# Weekly Optimization

## Why this isn't run yet

The "Run weekly optimization using this performance data" command needs a real week of TikTok analytics — views, hold rate, watch time, clicks, purchases, etc. As of 2026-07-25 (Day 0), no account exists and nothing has published (see `today_2026-07-25.md`). There is no data to analyze, and fabricating numbers would violate the system's own Analytics Agent rule: *"If the conclusion is not tied to data, mark it as an assumption and request more data."* This file is the template, ready to run for real the first time a week of posts exists.

## How to run this for real

1. Export TikTok analytics for the trailing 7 days (Creator Tools → Analytics → Content, per-video).
2. Paste the export (views, hold rate, watch time, completion, likes, comments, shares, saves, clicks, purchases, commission, refunds, negative comments — one row per video) below in place of `[PASTE PERFORMANCE DATA]`.
3. Come back and ask to "run weekly optimization" — Claude will fill in the sections below against the real numbers.

```text
[PASTE PERFORMANCE DATA]
```

## Decision rules this will apply once data exists

- High views + low clicks → hook works, offer/CTA is weak.
- Low views + high retention → packaging (thumbnail/caption/hashtags) is weak, not the video.
- High clicks + low purchases → product page, price, reviews, shipping, or trust is weak.
- High comments + low sales → curiosity exists, buyer confidence doesn't.
- Refunds or repeated negative comments → pause the product immediately.

## Output template (filled in once data exists)

```text
1. What to scale:
2. What to kill:
3. What to revise:
4. Next product category:
5. Next hooks to test:
6. Next posting cadence:
7. Tool changes:
8. Next 7-day content calendar:
9. Strategic warning:
```
