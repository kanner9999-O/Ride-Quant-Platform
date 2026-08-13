# Ride — Phase 2 Prototype — Batch 01

Lifecycle entry + Research foundation. See [`batch-manifest.md`](batch-manifest.md) for the full
evidence record and [`traceability.md`](traceability.md) for the element-level mapping back to
[`docs/product/ux-blueprint.md`](../../../docs/product/ux-blueprint.md).

## What this is

A static, non-authoritative UX prototype — HTML + CSS + vanilla JavaScript, mock/static data
only. No build step, no framework, no backend, no real credentials, no real financial data. Open
`index.html` directly in a browser.

## What's included

- **WS-001** — the always-visible workspace shell (global context bar + six-stage nav bar).
- **SCR-001** — Market Analysis Workspace (Research entry point).
- **VIEW-001** — Strategy Instance Selector (commit gate).
- **VIEW-002** — Research Verification Result (commit gate, tri-state outcome).

Navigating to Replay / Backtest / Paper / Review / Improve shows a labelled "deferred" placeholder
— those stages are not authored in this batch (see `batch-manifest.md` §8).

## Prototype QA panel

The dark drawer pinned to the bottom of the page is **prototype tooling, not part of the
authoritative UX** — it exists only so every `STATE-XXX` in this batch's scope (loading, invalid,
missing evidence, missing Strategy Instance, PASSED/FAILED/INDETERMINATE) can be inspected
directly, since a static prototype has no real event log to compute these outcomes from.

## What this is not

Not a production frontend, not connected to any backend/exchange, not authorized for LIVE, not a
claim that Phase 2 (or even this batch's full UC/surface coverage) is complete. See
`batch-manifest.md` §16 for lifecycle/review state — this batch is a **candidate**, not yet
reviewed or approved.
