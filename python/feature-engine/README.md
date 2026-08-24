# feature-engine

Authoritative Feature Engine: `FeatureComputed` / `FeatureFactInvalidated`
facts fanning in **selectively** (Definition-pinned, ADR-014) from Structure
Engine's Swing layer and Raw Regime Engine's classifications, plus a bounded
Candle-window path (`docs/domain/feature.md`). `module_id: feature-engine`
per `docs/architecture/module-registry.yaml`. Implementation language
(Python) resolved in this build transaction as the unambiguous application
of [ADR-008](../../docs/adr/ADR-008.md)'s "Feature Engineering → Python"
layer-level pin to this module's own `implements_capabilities:
[feature-engineering]` registry entry (`docs/engineering/monorepo.md` §4) —
`ADR_NOT_REQUIRED`, no new ADR created.

This is the **analytical core only** — no broker, no RPC/HTTP, no
Go↔Python transport, no deployment/process topology, no real event log, no
venue connectivity, and **no concrete production Candle-derived formula**
(see "The formula boundary" below). Those are all separate, future governed
decisions.

## What this module owns

- `FeatureComputed` / `FeatureFactInvalidated` facts for exactly three
  founding feature types (`feature.md`'s closed enum): `volatility_metric`,
  `directional_persistence_metric`, `distance_to_last_confirmed_swing`.
- The non-authoritative `FeatureCurrentView` projection (`feature.md` §11).

## What this module never does

- Own Candle/Swing/Structure/Regime/Context/Strategy/Decision/Risk/Execution
  state, or emit trade signals, strategy recommendations, order intents, risk
  decisions, or execution commands.
- Consume `CandleObserved`, `CandleCurrentView`, `SwingCandidateDetected`,
  `SwingCurrentView`, `BreakOfStructureDetected`, `ChangeOfCharacterDetected`,
  `StructureFactInvalidated`, `StructureRecomputed`, `StructureCurrentView`,
  `RegimeCurrentView`, or any Context/Strategy/Decision/Risk/Execution
  state — `feature.md` §14's input contract is exactly
  `CandleClosed`/`CandleCorrected`, `SwingConfirmed`/`SwingInvalidated`,
  `RegimeClassified`/`RegimeFactInvalidated`, nothing else.
  `depends_on: [market-data-ingestion, structure-engine, raw-regime-engine]`
  in `module-registry.yaml` is a module-level dependency-graph fact, not
  authorization to consume every event those modules emit.
  This package has no import of, and no dependency on, `structure_engine` or
  `raw_regime_engine` (`test_no_prohibited_module_imports` enforces this
  directly on the committed source tree); it defines its own
  consumer-side `swing_input.py`/`regime_input.py` views of those contracts.
- Invent a canonical ATR/stdev/realized-volatility/variance/momentum/slope/
  RSI/directional-count/return-aggregation Candle formula — `feature.md`
  deliberately does not pin one. Only clearly-labeled `test-*` formulas exist
  in this repository.
- Assign its own Quality Tier or claim a formal Chapter 13 Quality Gate
  result — both are separate governed prerequisites; `feature-engine`'s
  Quality Tier remains **UNRESOLVED** after this transaction.

## The formula boundary

`feature.md` intentionally does not select a concrete Candle-derived metric
formula for `upstream_source=candle`. `CandleWindowFeatureEngine` is generic
over an injected `FeatureFormula` (a `formula_id` + `compute(evidence) ->
Decimal`) and fails closed (`UnsupportedFeatureFormulaError`) at
**construction time** if the supplied formula's own `formula_id` does not
match the `FeatureDefinition`'s pinned `formula_id` — there is no global
formula registry to fall back on, and no arbitrary callable/plugin execution
path exists to bypass this. The Regime-source path
(`RegimePassthroughFeatureEngine`) and the Swing-distance path
(`SwingDistanceFeatureEngine`) are independently and fully implementable
without any Candle formula, and are fully implemented in this build; only
the Candle-window path's concrete formula selection is authority-limited,
and is recorded honestly as a bounded known implementation limitation, not a
fabricated formula decision.

## Per-feature-type / per-path implementation status

| Feature type | Path | Status |
|---|---|---|
| `volatility_metric` | `regime` (`RegimePassthroughFeatureEngine`) | FULLY_IMPLEMENTED |
| `volatility_metric` | `candle` (`CandleWindowFeatureEngine`) | FULLY_IMPLEMENTED (generic engine; fails closed for any `formula_id` without an injected, authorized `FeatureFormula`) |
| `directional_persistence_metric` | `regime` | FULLY_IMPLEMENTED |
| `directional_persistence_metric` | `candle` | FULLY_IMPLEMENTED (same formula-boundary note as above) |
| `distance_to_last_confirmed_swing` | swing + candle | FULLY_IMPLEMENTED |

## Package layout

```
src/feature_engine/
  identity.py            deterministic opaque subject-id derivation (module-local).
                          Duplicated, not imported, from structure-engine's/
                          raw-regime-engine's own identity.py.
  envelope.py             Chapter 8 §8.2 event-record identity shapes (EventRecordRef/StreamRef/ProducerRef)
  publish.py              in-process, per-stream contiguous sequence allocation (ADR-009)
  candle.py               authoritative Candle input (CandleScope/OHLCV/CandleFact), plus a
                           bounded OHLCV.field(name) accessor for Definition-pinned
                           reference_price_field
  swing_input.py          Feature's own consumer-side view of Structure's Swing contract
                           (SwingConfirmedFact/SwingInvalidatedFact) — not an import of
                           structure_engine
  regime_input.py         Feature's own consumer-side view of Raw Regime's contract
                           (RegimeClassifiedFact/RegimeFactInvalidatedFact) — not an import
                           of raw_regime_engine
  contracts.py            FeatureScope/DecimalPrecisionPolicy/FeatureDefinition (exhaustive
                           __post_init__ validation)/FeatureComputed/FeatureFactInvalidated/
                           RecordedTimeSource/normalize_input_facts (§8a generic evidence
                           normalization)/the four exact canonical policy identifier strings
  regime_passthrough.py   RegimePassthroughFeatureEngine — volatility_metric/
                           directional_persistence_metric over RegimeClassified, verbatim
                           pass-through of computed_metric with no reclassification
  candle_window.py        FeatureFormula protocol + CandleWindowFeatureEngine — rolling
                           fixed-cardinality Candle window, deterministic evidence order,
                           fail-closed formula boundary
  swing_distance.py        SwingDistanceFeatureEngine — feature.md §9a's 5-step eligible-
                           Swing filter pipeline + 8-criterion total order, Decimal-only
                           signed/absolute distance arithmetic, independent per-stream
                           recorded-time monotonicity (Candle vs Swing)
  current_view.py         FeatureCurrentView — feature.md §11's 7-criterion total order;
                           no row before first computation; PENDING_CORRECTION never falls
                           back to an older valid window
  errors.py               explicit technical failure modes (Error Handling Convention §7)
tests/
  conftest.py              candle/swing/regime/definition/formula/time-source fixtures
                           (TEST-ONLY implementations, clearly labeled)
  test_definition.py       feature subject identity, FeatureDefinition validation
  test_regime_passthrough.py  regime pass-through (both dimensions), dedup, correction
                           lineage, causal ordering
  test_candle_window.py    candle-path cardinality/order/formula-mismatch/warm-up/correction
  test_swing_distance.py   eligible-Swing effective cutoff, recorded/effective-time
                           independence, revision selection, total-order tie-break, distance
                           arithmetic, deterministic replay
  test_current_view.py     FeatureCurrentView no-row/valid/pending-never-falls-back/resolves
  test_evidence.py         normalize_input_facts order-independence/dedup/cardinality/
                           reference-conflict fail-closed (Candle/Swing/Regime)
  test_boundaries.py       static import-boundary + prohibited-vocabulary + prohibited-input
                           checks against the committed source tree
```

**Why this package duplicates `identity.py`/`envelope.py`/`publish.py`/
`candle.py` instead of importing structure-engine's or raw-regime-engine's:**
each Python module is independently built/deployed (Chapter 3 §3.1), and
being a permitted `depends_on` in `module-registry.yaml` is an event-contract
relationship, not a license to import the producing module's Python package.
Duplicating these small, self-contained building blocks mirrors the existing,
already-governed precedent established by raw-regime-engine's own README.

Each engine (`RegimePassthroughFeatureEngine`, `CandleWindowFeatureEngine`,
`SwingDistanceFeatureEngine`) is pure, deterministic, in-process, and holds no
network dependency — a caller drives it by calling `on_regime_classified`/
`on_candle`/`on_swing_confirmed` etc. in cursor order.

## Recorded-time causality (injected, never fabricated)

`FeatureComputed`/`FeatureFactInvalidated`'s own `recorded_time` is **never**
copied from an upstream fact's `recorded_time` — an original fact's must be
later than its evidence's; an invalidation's must be later than both the
fact it targets and the causing upstream event; a replacement's must be
later than its own invalidation. Every engine asks an injected
`RecordedTimeSource` (`next_after(strict_floor) -> datetime`) and
independently validates `result > strict_floor`, raising
`RecordedTimeSourceViolationError` otherwise. `SwingDistanceFeatureEngine`
tracks this floor **independently per upstream stream**
(`_last_candle_recorded_time` vs `_last_swing_recorded_time`) rather than one
shared counter, because Candle and Swing are independent upstream streams
(Chapter 8 §8.3.3 — no invented global cross-stream order): a Swing
confirmation can legitimately be recorded much later than its own pivot, with
no required interleaving relationship to Candle recorded_time.

## Eligible-Swing selection (`feature.md` §9a)

`SwingDistanceFeatureEngine` implements the exact ordered pipeline: (1)
scope/identity match, (2) recorded-time visibility, (3) effective-time cutoff
— **strict `<`**, `reference_cutoff = reference Candle
effective_time.window_end`, condition `SwingConfirmed.pivot_effective_time.
window_start < reference_cutoff` (half-open; a Swing exactly at `window_end`
is **ineligible**), (4) latest valid revision, (5) not invalidated — all five
filter steps run before the 8-criterion total order, which never resurrects
an effective-time-ineligible Swing even via its own tie-break criteria.
Signed distance is `reference_price - pivot_price` (the standard
mathematical signed difference) — one bounded, non-fabricated arithmetic
convention, not an invented directional/price-action interpretation.

## First-Python-build toolchain reused

Per the governing task's own instruction, this module reuses
structure-engine's/raw-regime-engine's already-verified toolchain baseline,
with its **own independent reproducible environment evidence**:

**Python >= 3.13.** Interpreter used to build and verify this module: Python
3.13.6 (CPython, arm64, macOS).

| Concern | Tool | Pinned version |
|---|---|---|
| Formatter | `ruff format` | `0.16.4` |
| Lint / static analysis | `ruff check` | `0.16.4` |
| Type checking | `mypy --strict` | `2.3.1` |
| Test framework | `pytest` | `9.1.1` |

No numerical/data-science stack is used — **zero runtime dependencies**;
`decimal.Decimal` (stdlib) provides lossless arbitrary-precision arithmetic
for every authoritative numerical value — never binary float.

### Reproducible build/dev environment

- **Build backend:** `[build-system].requires` pins `setuptools==84.0.0` exactly.
- **Full transitive dev/build dependency state:**
  [`requirements-dev.lock.txt`](./requirements-dev.lock.txt) — generated via
  `pip freeze --exclude-editable` from a fresh venv built specifically for
  this module.
- **Zero production runtime dependencies** — `[project].dependencies` is empty.

## Build / test locally

```bash
cd python/feature-engine
python3.13 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip==25.2
pip install -e ".[dev]"

ruff format --check .
ruff check .
mypy
pytest tests/ -v
```

## ADR Scope Rule

`ADR_NOT_REQUIRED` — this build implements one already-registered module
(`feature-engine`) under the already-existing boundary/dependency graph,
`feature.md` Domain Contract, ADR-014 fan-in semantics, ADR-008 language
principle, Event Model, and Feature/Context architecture. No new Platform
Invariant, Event Schema, module taxonomy, dependency-graph change,
cross-module contract, governance-process change, or hard-to-reverse choice
was introduced. Where `feature.md` explicitly defers a concrete mechanism
(warm-up/missing-input/effective-window policy values, the signed-distance
arithmetic convention), this module pins one bounded, documented
interpretation in code, not a governance decision.

## Current state (as of this build)

- Feature Engine: implemented (engine semantics only) — no production
  `FeatureDefinition`/`FeatureFormula` instance exists or is claimed; those
  remain externally unresolved configuration.
- Feature Engine Quality Tier: **UNRESOLVED** — not assigned in this
  transaction (registry has no `quality_tier` field for `feature-engine`).
- Structure Engine / Raw Regime Engine: unchanged by this transaction.
  Structure Engine's formal Chapter 13 Quality Gate (boundary
  `5b2b44f2263fc69af8c03578692796e63bafb5df`) remains **FAIL — evidence**;
  those findings are not remediated or reclassified here.
- No formal Chapter 13 Quality Gate claimed for Feature Engine.
- No module-level, Data-Layer-level, or Phase-3-level approval implied.
- LIVE: **NOT_AUTHORIZED**.
