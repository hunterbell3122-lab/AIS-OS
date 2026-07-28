# ComplianceShield

Combined entity: **ComplianceShield** (audit service) + former **FailSafe360** (SaaS platform), merged into one brand. Full build sequencing lives in [PLAYBOOK.md](PLAYBOOK.md) — read that before touching any phase.

Pre-revenue, zero clients. Florida-specific, construction/skilled-trades-only until the first paid client (see Playbook Section 7).

## Repo layout

- **`/service`** — the audit tooling track (Phases 1-3). Checklist engine, remediation report generator, and the Zoom-call-ready delivery wrapper. This is the revenue-critical path — a single operator runs a live compliance audit on a call and hands the client a finished report before it ends. Ships independently of `/platform`.
- **`/platform`** — the SaaS track (Phases 4-7). FastAPI backend + Postgres data model, a RAG compliance Q&A assistant, a Next.js frontend (ported from the existing `failsafe360-prototype.html`), and multi-tenant auth/billing. Depends on `/service`'s Phase 1 knowledge base but is otherwise a separate build track.
- **`/shared`** — knowledge base source content and common types/schemas both tracks read from. **`/shared/knowledge-base-export.md` must exist before Phase 1 can start** — see Playbook Section 0.5. Nothing in `/service` or `/platform` should encode regulatory checklist content that didn't come from this file.

## Why two tracks in one repo

The service track reaches revenue fastest and generates the real workflow data the SaaS platform should be built around, so it's front-loaded. The SaaS track's frontend doesn't start until `/platform`'s backend data model exists (Phase 4). See the dependency graph in Playbook Section 1.

## Status

Phase 0 (this scaffold) — done. See `BUILD_LOG.md` for phase-by-phase history (Notion MCP isn't connected in this environment yet, so that file is the source of truth until it is — see Playbook Section 5).

**Deviation from Playbook Section 3, Phase 0:** this folder is a subfolder of the existing `AI OS - (VSC)` git repo (the pattern already used by the `TikTokShop/` and `SignalForge/` ventures), not a standalone repo with its own `main`/`dev` branches. A nested `.git` here would create submodule-style conflicts with the parent repo. If ComplianceShield later needs its own branch workflow, that's a `git checkout -b` in the parent repo, not a nested init.
