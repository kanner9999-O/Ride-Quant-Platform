# Ride — Phase 2 Prototype — Batch 02

Replay reconstruction + optional parity verification. See
[`batch-manifest.md`](batch-manifest.md) for the full evidence record and
[`traceability.md`](traceability.md) for the element-level mapping back to
[`docs/product/ux-blueprint.md`](../../../docs/product/ux-blueprint.md) and
[`docs/domain/decision.md`](../../../docs/domain/decision.md) §9a.

## What this is

A static, non-authoritative UX prototype — HTML + CSS + vanilla JavaScript, mock/static data
only. No build step, no framework, no backend, no real credentials, no real financial data, no
replay/Decision/parity engine. Open `index.html` directly in a browser. This is a separate,
self-contained page from [Batch 01](../batch-01/) — it does not share live JavaScript state with
it; "arriving from Research" (a pinned Strategy Instance, a Research verification outcome) is
represented as Batch-02-local simulated incoming context via the QA panel, not by re-implementing
VIEW-001/VIEW-002.

## What's included

- **NAV-002** — Replay navigation, including its precondition gate (Strategy Instance must be
  pinned) and read-only-inspection behavior (blocked reason still shown if Research verification
  did not PASS).
- **SCR-002** — Replay Cursor & Historical Reconstruction: choose a canonical Replay Cursor,
  inspect the illustrative historical ReplayState(C) at that cursor — the authoritative
  recorded-fact lineage (Decision → Trade Intent → RiskEvaluation → Execution Intent → Order →
  ExecutionResult → Fill) and Position (a separately-labelled, derived, deterministic,
  non-authoritative projection reconstructed at the same cursor) are shown with their own,
  distinct authority-class labels — never under one universal "authoritative" badge.
- **VIEW-003** — Parity Recomputation Result: an optional, never-automatic action from SCR-002.
  Shows the recorded vs. recomputed Canonical Decision Semantic Representation, the nine pinned
  axes, and one of MATCH / MISMATCH / INDETERMINATE — always demo-selected, never actually
  computed.

The nav bar's "Research" item is a real link to `../batch-01/index.html`. Backtest / Paper /
Review / Improve show a labelled "deferred" placeholder — those stages (and SCR-009 for the
MISMATCH → Review handoff) are not authored in this batch.

## Prototype QA panel

The dark drawer pinned to the bottom of the page is **prototype tooling, not part of the
authoritative UX** — it lets you simulate the incoming context from Research (pinned/not pinned,
verification PASSED/not PASSED), inspect every included `STATE-XXX`, and switch the VIEW-003
outcome (MATCH/MISMATCH/INDETERMINATE) on demand, since a static prototype has no real event log
or parity engine to derive these from.

## What this is not

Not a production frontend, not connected to any backend/exchange, not authorized for LIVE, not an
implementation of replay or parity computation, and not a claim that Phase 2's full 17-surface/
21-UC coverage is complete. See `batch-manifest.md` §16 for the exact progress accounting — Review
A and Independent Review B completed for this batch's v1.3 contribution (verdict
`READY_FOR_NEXT_PHASE2_BATCH`), but v1.5 then authored a new bounded semantic correction to
SCR-002 (Phase-2 Full-Scope BCC finding `P2-BCC-MAJ-01`, prototype-side) that has **not** yet
gone through its own governed review — that verdict does not automatically extend to this new
delta. This batch's lifecycle remains a **candidate** either way, not yet approved — a review
verdict is not itself a lifecycle promotion.
