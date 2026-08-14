# Ride — Phase 2 Prototype — Batch 06

Improve — new Strategy Definition Version creation, Strategy Instance registration/binding,
version comparison, and old-version evidence access. See [`batch-manifest.md`](batch-manifest.md)
for the full evidence record and [`traceability.md`](traceability.md) for the element-level
mapping back to [`docs/product/ux-blueprint.md`](../../../docs/product/ux-blueprint.md),
[`docs/product/use-case-workflow.md`](../../../docs/product/use-case-workflow.md), and
[`docs/domain/strategy.md`](../../../docs/domain/strategy.md).

## What this is

A static, non-authoritative UX prototype — HTML + CSS + vanilla JavaScript, mock/static/
counter-generated data only. No build step, no framework, no backend, no real persistent
storage, no network calls, no credentials, no Strategy management engine. Open `index.html`
directly in a browser. This is a separate, self-contained page from
[Batch 01](../batch-01/)–[Batch 05](../batch-05/) — it does not share live JavaScript state with
any of them. This is the **final planned Phase-2 Product Prototype milestone** — with Batch 06,
the candidate set reaches the full 17-surface/21-UC scope, though none of that is claimed as
independently verified (see "What this is not" below).

## What's included

- **NAV-006** — Improve navigation, always available from the global nav bar at every stage.
  Required context is action-specific per destination, never a navigation blocker.
- **SCR-010 — Strategy Definition Version Creation**: shows the existing Strategy Definition
  identity and its current version's full content (all seven `strategy.md` §1 fields), then a
  real, editable creation control (`thesis`/`supported_scope`) that materially produces a
  brand-new, distinct `strategy_definition_version_id` — the old version is re-displayed
  unchanged afterward, proving it was never mutated in place.
- **VIEW-006 — Strategy Instance Creation/Binding**: after SCR-010 creates a new version, VIEW-006
  registers a *separate* new Strategy Instance bound to exactly that version — never a
  select/pin action, never a reuse of an existing Instance identity. The handoff to VIEW-001 uses
  the exact required wording ("Instance is now available to select/pin through VIEW-001") and
  never claims the Instance is already pinned.
- **SCR-011 — Strategy Version Comparison**: pick a Strategy Instance and a mode independently for
  each side of a comparison — same mode on both sides gives Backtest-vs-Backtest or
  PAPER-vs-PAPER; different modes give a cross-mode side-by-side view. The two evidence families
  are never merged, normalized, or scored together, and a Strategy Instance with no outcome in
  the selected mode renders empty for that side only.
- **VIEW-005 — Old-Version Evidence Access**: for a Strategy Instance that is RETIRED (illustrating
  a version that is "no longer active"), the bound version's identity is always shown first,
  independent of whether its evidence resolves; Backtest and PAPER evidence families resolve
  independently, and a QA toggle demonstrates both STATE-025 (complete) and STATE-026 (PAPER
  Fill/Position unavailable, Backtest remains fully visible).

The nav bar's "Research"/"Replay"/"Backtest"/"Paper"/"Review" items are real links to
`../batch-01/index.html` through `../batch-05/index.html`.

## Strategy Definition Version vocabulary (critical — read before assuming more exists)

Every field on a Strategy Definition Version fixture here is exactly one of `strategy.md` §1's
seven `StrategyDefinitionVersionRegistered` payload fields (`strategy_definition_version_id`,
`strategy_definition_id`, `thesis`, `supported_scope`, `required_input_contracts`,
`decision_rule_ref`, `explanation_contract_ref`, `downstream_output_capability`). No DSL,
compiler, rule language, validation taxonomy, version graph, or approval workflow exists anywhere
in this batch — those are explicitly out of scope for `strategy.md` itself.

## "No longer active" — what that means here

`strategy.md` does not give Strategy Definition Version an "active" field — versions are never
invalidated merely for being superseded (see `strategy.md` §1). This prototype represents
"no longer active" as a product-level description of a `RETIRED` **Strategy Instance** (a genuine
`strategy.md` §5 lifecycle value) that happens to be bound to the older version — the version
itself remains independently resolvable and is never marked invalid.

## Comparison and old-version evidence — two families, never one

Both SCR-011 and VIEW-005 keep the Backtest evidence family (non-PAPER simulated authority) and
the PAPER evidence family (authoritative where current domain authority defines that class)
structurally separate — rendered by two entirely different functions, never merged into a single
object, never scored, ranked, or normalized against each other. Backtest material is never
labelled authoritative `ExecutionResult`/`Fill`/`Position`.

## Prototype-local mutation semantics

SCR-010's "Create Strategy Definition Version" and VIEW-006's "Register Strategy Instance" both
mutate *prototype-local UI state only* — each click appends a brand-new record (via a counter) to
a bounded prototype-local array; the pre-existing fixtures (`VERSION_FIXTURES`/
`INSTANCE_FIXTURES`) are never edited in place. This is not a claim of real, production
authoritative persistence — refreshing the page discards everything created this way.

## Prototype QA panel

The dark drawer pinned to the bottom of the page is **prototype tooling, not part of the
authoritative UX** — it lets you toggle VIEW-005's STATE-025/STATE-026 evidence-completeness
scenario and SCR-011's required-context-missing (STATE-002) scenario, and reset all
prototype-local creation/registration state back to its initial baseline.

## What this is not

Not a production frontend, not connected to any backend, not authorized for LIVE, not an
implementation of a Strategy management service/engine, not a claim that a real network audit was
performed. Reaching a candidate 17/17 surfaces and 21/21 UC with this batch does **not** establish
Phase-2 substantive completion — see `batch-manifest.md` for the exact progress accounting: this
is an **authoring transaction only**, Review A and Independent Review B have not yet been
performed on this batch, so its own +4 surface / +3 UC contribution is a **candidate**, not yet
independently verified (unlike Batch 01-05, each of which has already completed both review
rounds). Phase-2 completion additionally requires Quality Gate/Gate 3 evidence entirely separate
from per-batch review — none of that is claimed, run, or authorized here.
