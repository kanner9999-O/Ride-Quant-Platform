# Ride — Phase 2 Prototype — Batch 05

Review / causation / historical comparison / correction inspection. See
[`batch-manifest.md`](batch-manifest.md) for the full evidence record and
[`traceability.md`](traceability.md) for the element-level mapping back to
[`docs/product/ux-blueprint.md`](../../../docs/product/ux-blueprint.md),
[`docs/product/use-case-workflow.md`](../../../docs/product/use-case-workflow.md), and the
Domain Contracts under [`docs/domain/`](../../../docs/domain/).

## What this is

A static, non-authoritative UX prototype — HTML + CSS + vanilla JavaScript, mock/static data
only. No build step, no framework, no backend, no real credentials, no real financial data, no
signing/custody, no Replay/correction engine. Open `index.html` directly in a browser. This is a
separate, self-contained page from [Batch 01](../batch-01/), [Batch 02](../batch-02/),
[Batch 03](../batch-03/), and [Batch 04](../batch-04/) — it does not share live JavaScript state
with any of them.

## What's included

- **NAV-005** — Review navigation, always available from the global nav bar at every stage, with
  its own required-context routing: opening a specific SCR-008 trace needs a Fill/Position
  contribution to exist; opening a specific SCR-009 comparison needs a Replay Cursor already run
  at SCR-002. When missing, no evidence is fabricated to fill the gap.
- **SCR-008 — Decision → Position Lineage Trace**: select a Fill (two genuinely distinct
  already-recorded lineages, LONG and SHORT) to see the exact seven-link causation trace UC-016
  names — Fill → ExecutionResult → Order → Execution Intent → RiskEvaluation → Trade Intent →
  Decision — with no missing link, plus a separately-grouped Decision explainability panel
  (outcome, Strategy Instance/Definition Version, recorded input snapshot/evaluation evidence)
  resolved directly from the recorded fact, never re-derived.
- **SCR-009 — Historical State Comparison**: select an already-run Replay Cursor to see
  ReplayState(C) reconstructed now next to the state recorded at that same cursor — structurally
  the same object, demonstrating no-drift by construction rather than by coincidence — then a
  separate correction-check panel that reaches either "No conflict" or "Correction visible after
  historical cursor" (the historical panel above it is never altered either way).
- **VIEW-004 — Correction Inspection**: the one bounded correction fixture in this batch (a
  Decision that was originally recorded `NO_ACTION`, later invalidated, and replaced by a
  corrected `LONG` Decision) is always shown as **both** the original fact (still resolvable,
  append-only) and the invalidation + replacement fact, with an explicit `supersedes_fact_ref`
  link — never collapsed to only the "corrected" value.

The nav bar's "Research"/"Replay"/"Backtest"/"Paper" items are real links to
`../batch-01/index.html`, `../batch-02/index.html`, `../batch-03/index.html`, and
`../batch-04/index.html`. Improve shows a labelled "deferred" placeholder — that stage is not
authored in this batch.

## Read-only boundary (critical)

Every screen in this batch is read-only inspection only. There is no create, overwrite, correct,
invalidate, promote, "apply correction," "accept replacement," or "save reconstructed state"
action anywhere — verify directly: no function in `app.js` mutates a `MOCK_*`/`LINEAGE_FILLS`/
`REPLAY_CURSORS` fixture; only prototype-local UI selection state (which Fill/cursor/tab is
currently displayed) changes.

## Correction-lineage scope (important — read before assuming uniformity)

The domain layer does **not** use one uniform correction pattern across every fact type. This
batch's one interactive correction fixture uses Decision's own exact vocabulary
(`decision.md` §6 `DecisionFactInvalidated` — `invalidated_fact_ref`/`invalidation_reason` — and
`DecisionRecorded`'s own `supersedes_fact_ref`, pointing directly at the predecessor fact).
RiskEvaluation and Fill share this same direct pattern but are not separately fixtured here.
**ExecutionResult's correction lineage is materially more complex** — it requires a new
`ExecutionResultComputation` (`computation_purpose: CORRECTION`) carrying
`predecessor_execution_result_ref` and `correction_authorization_ref`, followed by a new
`ExecutionResultRecorded` — and is not modeled interactively in this batch.
`PaperExecutionObservation` and `Position` have **no correction lineage of their own**
(`execution-result.md` §11, `position.md` §1) — no Position correction fact is invented anywhere
here.

## Prototype QA panel

The dark drawer pinned to the bottom of the page is **prototype tooling, not part of the
authoritative UX** — it lets you simulate NAV-005's required-context-missing scenario for SCR-008
and SCR-009 (labelled `STATE-002` per NAV-005's own text — see `traceability.md` §3 for why this
is explicitly distinguished from `STATE-002`'s own narrower canonical catalogue row, which lists
only SCR-004/SCR-005/SCR-007/SCR-011). VIEW-004 has no empty/blocked state of its own per
`ux-blueprint.md`'s explicit text ("KHÔNG áp dụng — hiển thị luôn cả hai trạng thái"), so there is
no QA toggle for it — its one bounded correction fixture is always shown directly.

## What this is not

Not a production frontend, not connected to any backend/exchange, not authorized for LIVE, not an
implementation of a Replay/correction engine, not a claim that a real network audit was
performed, and not a claim that Phase 2's full 17-surface/21-UC coverage is complete. See
`batch-manifest.md` for the exact progress accounting — this is an **authoring transaction only**:
Review A and Independent Review B have not yet been performed on this batch, so its own +3
surface / +3 UC contribution is a **candidate**, not yet independently verified (unlike Batch
01-04, each of which has already completed both review rounds).
