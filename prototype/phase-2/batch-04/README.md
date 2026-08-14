# Ride — Phase 2 Prototype — Batch 04

PAPER initiation + execution evidence/detail. See [`batch-manifest.md`](batch-manifest.md) for the
full evidence record and [`traceability.md`](traceability.md) for the element-level mapping back
to [`docs/product/ux-blueprint.md`](../../../docs/product/ux-blueprint.md),
[`docs/product/use-case-workflow.md`](../../../docs/product/use-case-workflow.md), and the
Domain Contracts under [`docs/domain/`](../../../docs/domain/).

## What this is

A static, non-authoritative UX prototype — HTML + CSS + vanilla JavaScript, mock/static data
only. No build step, no framework, no backend, no real credentials, no real financial data, no
signing/custody, no production execution/simulation engine. Open `index.html` directly in a
browser. This is a separate, self-contained page from [Batch 01](../batch-01/),
[Batch 02](../batch-02/), and [Batch 03](../batch-03/) — it does not share live JavaScript state
with any of them. "Paper-pinned Strategy Instance" is represented as Batch-04-local simulated
state via the QA panel plus a bounded local fixture standing in for VIEW-001, not by
re-implementing VIEW-001 as a new surface.

## What's included

- **NAV-004** — Paper navigation, always available independent of initiation eligibility, with
  four distinct blocked causes (STATE-003 invalid Account/Instrument/Venue, STATE-028 Strategy
  Instance not selected, STATE-029 selected but not pinned, STATE-011 pinned but no eligible
  PAPER-context Decision) — never collapsed into one generic message.
- **SCR-006 — Paper Execution Initiation**: shows the existing, distinct PAPER-context Decision
  (outcome, Strategy Instance/Definition Version origin, recorded input snapshot) *before*
  initiation, visually separated from the downstream chain the initiation itself produces. Two
  genuinely distinct illustrative PAPER Decision fixtures are selectable (LONG and SHORT — each
  its own identity, evidence, and evaluation text; never one mutated into the other), so both
  directions are materially inspectable, not just the outcome LABEL. The user supplies intent
  only — no quantity/order-type/sizing/fee/slippage input exists anywhere. Initiating actually
  drives prototype-local state; RiskEvaluation REJECTED/NON_EVALUABLE truncate the chain exactly
  at RiskEvaluation, before any Execution Intent/Order/ExecutionResultComputation/
  PaperExecutionObservation is created.
- **SCR-007 — Paper Order/Execution Detail**: inspects the *same* lineage SCR-006 produced (no
  disconnected fixtures) across four panels — ExecutionResult (EXECUTED/NOT_EXECUTED, with the
  distinct ExecutionResultComputation and PaperExecutionObservation identities that authorize it
  exposed as supporting evidence), Fill evidence (economics + four-axis simulation evidence, both
  sourced from that same PaperExecutionObservation), Position (FLAT/LONG/SHORT/NON_EVALUABLE, all
  four materially reachable — direction is read from the Fill's own `direction` field, which is
  bound to whichever Decision scenario actually produced it — explicit, never guessed or
  collapsed to FLAT), and a standing PAPER safety confirmation (no real exchange order, no real
  network route in this prototype).

The nav bar's "Research"/"Replay"/"Backtest" items are real links to `../batch-01/index.html`,
`../batch-02/index.html`, and `../batch-03/index.html`. Review/Improve show a labelled "deferred"
placeholder — those stages (and SCR-008 for the Review handoff) are not authored in this batch.

## PAPER Decision separation (critical)

The PAPER-context Decision shown here is a distinct, already-existing authoritative fixture —
nothing in this batch clones, carries forward, promotes, or reuses the Batch 03 Backtest Decision
(or any Research Decision) as this PAPER Decision, and nothing defines the mechanism that created
it (that remains an explicitly deferred domain/workflow dependency, per
`use-case-workflow.md` UC-011). Research/Replay/Backtest evidence, if viewed, informs the user's
judgment only — it is never authoritative input to this chain.

## Prototype QA panel

The dark drawer pinned to the bottom of the page is **prototype tooling, not part of the
authoritative UX** — it lets you simulate every precondition/Risk/execution/Position scenario
family described in `batch-manifest.md`, since a static prototype has no real event log or
Risk/execution engine to derive these from. The Position tab's `NON_EVALUABLE` option is
explicitly a QA-only demonstration: this prototype's single-initiation flow can only naturally
produce zero or one Fill, so a genuine multiple-conflicting-Fill-lineage scenario (which
`position.md` defines `NON_EVALUABLE` for) cannot arise from real interaction here. To stay
internally coherent with the Fill/ExecutionResult tabs, the override only renders `NON_EVALUABLE`
when the current execution actually produced a Fill (EXECUTED) — it then pairs that real current
Fill with one explicitly-labelled illustrative *prior* Fill for the same Account/Instrument
(clearly distinguished, never an unexplained second current Fill). If the current execution has
no Fill (NOT_EXECUTED, or Risk-truncated), the override does not apply and the actual Position
state is shown instead, with a note explaining why — the demo never fabricates evidence or
contradicts what the other tabs show.

### Initiation-context mutation invalidates the current execution

QA controls fall into two kinds, and they behave differently on purpose:

- **Initiation-context controls** — Account/Instrument/Venue validity, Paper Strategy Instance
  selection/pin, PAPER Decision availability, and *which* PAPER Decision scenario (LONG/SHORT) is
  current. Changing any of these represents a different bounded Paper interaction, so any
  already-created execution is invalidated (`state.execution` is cleared) — SCR-007 returns to
  its empty state until a new initiation happens under the (possibly new) context. This is
  prototype-local demo-state hygiene only, not a production session/context invalidation model,
  and it is what prevents SCR-007 from ever showing historical execution evidence labelled
  "continuous from SCR-006" while the current context bar says otherwise.
- **Next-initiation-outcome controls** — Risk APPROVED/REJECTED/NON_EVALUABLE and ExecutionResult
  EXECUTED/NOT_EXECUTED. These only set the scenario that the *next* click of "Initiate PAPER
  execution" will produce; they never retroactively change an execution that already exists.
  Switching the Position inspection demo mode likewise never mutates the recorded execution
  lineage — it only changes how the existing Fill evidence (if any) is presented.

## What this is not

Not a production frontend, not connected to any backend/exchange, not authorized for LIVE, not an
implementation of a Risk/execution/simulation engine, not a claim that a real network audit was
performed, and not a claim that Phase 2's full UC/surface coverage is complete or that this
batch's own contribution is independently verified. See `batch-manifest.md` for the exact
candidate-vs-verified progress distinction — this batch is a **candidate**, not yet reviewed or
approved.
