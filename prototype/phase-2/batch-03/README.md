# Ride — Phase 2 Prototype — Batch 03

Backtest setup + run detail + run comparison. See [`batch-manifest.md`](batch-manifest.md) for the
full evidence record and [`traceability.md`](traceability.md) for the element-level mapping back
to [`docs/product/ux-blueprint.md`](../../../docs/product/ux-blueprint.md),
[`docs/product/use-case-workflow.md`](../../../docs/product/use-case-workflow.md), and
[`docs/domain/decision.md`](../../../docs/domain/decision.md)/[`risk.md`](../../../docs/domain/risk.md).

## What this is

A static, non-authoritative UX prototype — HTML + CSS + vanilla JavaScript, mock/static data
only. No build step, no framework, no backend, no real credentials, no real financial data, no
simulation engine, no Decision/Risk engine. Open `index.html` directly in a browser. This is a
separate, self-contained page from [Batch 01](../batch-01/) and [Batch 02](../batch-02/) — it does
not share live JavaScript state with either; "Strategy Instance already pinned" is represented as
Batch-03-local simulated incoming context via the QA panel, not by re-implementing VIEW-001.

## What's included

- **NAV-003** — Backtest navigation, including its precondition gate (Strategy Instance must be
  pinned to START a new run) and read-only-inspection behavior (existing runs remain viewable even
  without a pinned Strategy Instance).
- **SCR-003** — Backtest Run Setup: choose a bounded historical interval, start a run under a
  stable illustrative run identity bound to the Strategy Instance / Strategy Definition Version /
  configuration in use. A missing-evidence interval blocks the run from starting (STATE-005).
- **SCR-004** — Backtest Run Detail: three separated panels — (1) Decision/RiskEvaluation trace,
  with every Decision split into outcome (A), upstream explainability (B), and downstream lineage
  (C, when present — RiskEvaluation always here, never in B); (2) simulated economic evidence and
  exposure/position progression, non-PAPER; (3) a threshold-neutral strategy-level evaluable
  result.
- **SCR-005** — Backtest Run Comparison: select two runs, see their evaluable results side by
  side, each retaining its own identity/interval/version context — never aggregated into one
  score.

The nav bar's "Research" and "Replay" items are real links to `../batch-01/index.html` and
`../batch-02/index.html`. Paper / Review / Improve show a labelled "deferred" placeholder — those
stages (and SCR-011 for the run-comparison → Improve handoff) are not authored in this batch.

## Backtest / Paper authority separation

Nothing in this batch creates, reuses, or promotes a PAPER Order/ExecutionResult/Fill/Position.
"Simulated exposure change" and "simulated position" are illustrative, non-PAPER labels only — no
`BacktestFill`/`BacktestPosition`/`BacktestExecutionResult` entity is defined or invented. There is
no action anywhere resembling "execute this Backtest Decision in Paper" or "promote this run to
Paper."

## Prototype QA panel

The dark drawer pinned to the bottom of the page is **prototype tooling, not part of the
authoritative UX** — it lets you simulate the Strategy Instance pin state, inspect STATE-001/
STATE-002/STATE-010, and reset all demo state, since a static prototype has no real event log or
Backtest engine to derive these from.

## What this is not

Not a production frontend, not connected to any backend/exchange, not authorized for LIVE, not an
implementation of a simulation/Decision/Risk engine, and not a claim that Phase 2's full 17-surface/
21-UC coverage is complete. See `batch-manifest.md` §17 for the exact progress accounting — Review
A and Independent Review B are complete for this batch's own SCR-003/SCR-004/SCR-005 contribution
(verdict `READY_FOR_NEXT_PHASE2_BATCH`), but this batch's lifecycle remains a **candidate**, not
yet approved — that verdict is not itself a lifecycle promotion.
