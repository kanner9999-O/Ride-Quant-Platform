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
formula for `upstream_source=candle`, and no current repository authority
pins an immutable executable identity + parameters for any `formula_id`.
`CandleWindowFeatureEngine` no longer accepts an injected, caller-supplied
formula at all (the prior `FeatureFormula` injection Protocol — authorized
only by a `formula_id` string equality check, not real authority — has been
removed): construction **always** fails closed
(`UnsupportedFeatureFormulaError`), regardless of `formula_id`
(P3-FEATURE-A-MAJ-03 remediation, Round 2). No formula registry, expression
language, plugin mechanism, or concrete indicator exists as a substitute —
Candle-path Feature computation is unavailable by design until a governed
decision pins genuine executable formula identity. The Regime-source path
(`RegimePassthroughFeatureEngine`) and the Swing-distance path
(`SwingDistanceFeatureEngine`) are independently and fully implementable
without any Candle formula, and remain fully implemented.

## Per-feature-type / per-path implementation status

| Feature type | Path | Status |
|---|---|---|
| `volatility_metric` | `regime` (`RegimePassthroughFeatureEngine`) | FULLY_IMPLEMENTED |
| `volatility_metric` | `candle` (`CandleWindowFeatureEngine`) | FAIL_CLOSED_PENDING_AUTHORITY — construction always fails closed (`UnsupportedFeatureFormulaError`); no executable formula identity is authorized (P3-FEATURE-A-MAJ-03, Round 2) |
| `directional_persistence_metric` | `regime` | FULLY_IMPLEMENTED |
| `directional_persistence_metric` | `candle` | FAIL_CLOSED_PENDING_AUTHORITY (same as above) |
| `distance_to_last_confirmed_swing` (`absolute`) | swing + candle | FULLY_IMPLEMENTED |
| `distance_to_last_confirmed_swing` (`signed`) | swing + candle | FAIL_CLOSED_PENDING_AUTHORITY — no authoritative sign-orientation convention exists in feature.md §6/§7.3; `SwingDistanceFeatureEngine` fails closed (`UnsupportedDistanceRepresentationError`) at construction rather than inventing one (P3-FEATURE-A-MAJ-01 remediation). |

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
                           __post_init__ validation, incl. upstream_contract_refs)/
                           FeatureComputed/FeatureFactInvalidated (both carry
                           event_contract_ref)/RecordedTimeSource/normalize_input_facts (§8a
                           generic evidence normalization)/the four exact canonical policy
                           identifier strings/the closed upstream+output contract-ID vocabulary
  regime_passthrough.py   RegimePassthroughFeatureEngine — volatility_metric/
                           directional_persistence_metric over RegimeClassified, verbatim
                           pass-through of computed_metric with no reclassification,
                           contract-ref-qualified inputs, ref-identity-only dedup
  candle_window.py        CandleWindowFeatureEngine — permanently fail-closed for
                           upstream_source=candle (P3-FEATURE-A-MAJ-03, Round 2): no
                           caller-supplied executable formula is accepted; construction
                           always raises UnsupportedFeatureFormulaError
  swing_distance.py        SwingDistanceFeatureEngine — feature.md §9a's 5-step eligible-
                           Swing filter pipeline + 8-criterion total order against an
                           explicit, caller-supplied computation cursor `R` threaded through
                           on_candle/on_swing_confirmed/on_swing_invalidated (never derived
                           from any input event's own recorded_time, P3-FEATURE-A-MAJ-06);
                           Decimal-only absolute-only distance arithmetic (signed fails
                           closed); independent per-stream recorded-time monotonicity
                           (Candle vs Swing); swing.md §1a revision-sequencing enforcement;
                           full-window re-evaluation (PENDING_CORRECTION AND already-VALID
                           windows settled on an alternate Swing) on every newly-visible
                           Swing revision (P3-FEATURE-A-MAJ-04); exact-contract-ref
                           (id+version) upstream authorization and full consumer-side-fact
                           equality ref-conflict checks for both Candle and Swing inputs
                           (P3-FEATURE-A-MAJ-02/-05)
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

**Explicit computation cursor `R` (P3-FEATURE-A-MAJ-02, Round 2).**
Recorded-time visibility (step 2) is checked against `R`, a **required
keyword argument** on `on_candle`/`on_swing_confirmed`/`on_swing_invalidated`
— never implicitly substituted with `R = candle.recorded_time` or
`R = triggering_event.recorded_time` internally. A live/real-time caller may
legitimately choose to pass an event's own `recorded_time` as `R`, but that
is the caller's explicit choice, never an engine default; a replay/backtest
caller can independently supply any `R` (e.g. evaluate a Candle recorded at
R10 as-of R100, after a Swing correction recorded at R20 has become visible).

**Full-window re-evaluation on newly-visible Swing revisions
(P3-FEATURE-A-MAJ-04, Round 2).** `on_swing_confirmed` re-evaluates every
window with a lineage entry, not only windows currently
`PENDING_CORRECTION` — a window that already settled `VALID` on a
lower-priority alternate Swing (because the preferred Swing was invalidated
and no replacement was visible yet) is invalidated and replaced again if a
corrected/higher-priority Swing revision now wins the deterministic total
order (the `A -> invalidate -> B(temporary) -> A(N+1)-wins` sequence).

Only `distance_representation="absolute"` is computable; `"signed"` fails
closed at construction (see "Signed-distance boundary" below).

## Signed-distance boundary

feature.md §6/§7.3 leaves `distance_representation="signed"`'s sign
orientation genuinely unpinned — no authoritative convention exists for
which direction is positive. `SwingDistanceFeatureEngine` does not invent
one: it fails closed (`UnsupportedDistanceRepresentationError`) at
construction time for `signed`, and only computes
`distance_representation="absolute"` (an unambiguous, orientation-
independent magnitude). A prior build of this module computed `signed` as
`reference_price - pivot_price` — that was an invented convention with no
authority pin and has been removed (P3-FEATURE-A-MAJ-01 remediation).

## Contract qualification (`feature.md` §6/§14, Chapter 8 §8.2.5)

Every authoritative event Feature consumes or emits carries an
`event_contract_ref` (`{contract_id, contract_version}`). `FeatureDefinition.
upstream_contract_refs` (feature.md §6, scoped to `volatility_metric`/
`directional_persistence_metric`) pins the exact upstream contract(s) a
given definition authorizes — `RegimePassthroughFeatureEngine` validates
every incoming fact's `event_contract_ref` against it, failing closed
(`UnauthorizedUpstreamContractError`) otherwise. `distance_to_last_
confirmed_swing` has no equivalent per-definition field in feature.md §6
(deliberately not invented here); `SwingDistanceFeatureEngine` instead takes
a **caller-injected, required** `authorized_candle_contract_refs`/
`authorized_swing_contract_refs` (exact `{contract_id, contract_version}`
sets, validated non-empty and contract-ID-bounded to feature.md §14's fixed
enumeration at construction) and exact-matches every incoming Candle/Swing
fact's full `event_contract_ref` against it — `contract_id` matching alone
is never sufficient authorization for an arbitrary `contract_version`
(P3-FEATURE-A-MAJ-02, Round 2).

`FeatureComputed`/`FeatureFactInvalidated` outputs from all three engines
carry `event_contract_ref` pinned to feature.md §3/§4's own contract IDs
(`feature-computed`/`feature-fact-invalidated`) with a `contract_version`
the caller now injects via a required `feature_event_contract_version`
constructor argument (`resolve_output_contract_refs` in `contracts.py`) — the
former fabricated `FEATURE_EVENT_CONTRACT_VERSION = "v0"` stand-in has been
removed; an empty/missing value fails closed
(`UnresolvedOutputContractAuthorityError`) instead of defaulting to an
invented value (P3-FEATURE-A-MAJ-02, Round 2).

**Scope boundary — not touched by this remediation.** The `_REGISTRY_VERSION
= "v0"` internal stand-in (`contracts.py`, `swing_distance.py`,
`current_view.py`) used purely as tie-break criterion #4
(`stream_ref.registry_version`) inside `input_fact_refs`
normalization/total-order sort keys is **unchanged**. It mirrors the
identical pattern already present in `structure-engine`/`raw-regime-engine`
(verified via direct source inspection), reflects the repo-wide absence of
`stream-registry.yaml` (Phase 1, explicitly not-yet-authored per
`feature.md`/`swing.md` §2's own text), and none of this package's consumer-
side fact types (`CandleFact`/`SwingConfirmedFact`/`RegimeClassifiedFact`)
model a real per-fact `registry_version` field to source it from. Since the
value is a single module-wide constant applied identically to every fact,
it never changes the *result* of any comparison it participates in (all
facts tie on it, deferring to criterion #5) — but eliminating it for real
would require inventing per-fact registry-version modeling repo-wide, a
cross-engine architecture decision outside this bounded correction's scope.
Flagged, not fixed: `GOVERNED_DECISION_REQUIRED` if this is to close.

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
(warm-up/missing-input/effective-window policy values), this module pins one
bounded, documented interpretation in code, not a governance decision. Where
`feature.md` pins no mechanism at all (the `signed` sign orientation), this
build fails closed rather than inventing one (see "Signed-distance boundary"
above).

## Remediation history

**Round 1** — a bounded remediation batch fixed six verified Review A Major
findings against the first build (`9452e8341516c25f2b4e576921c75751df1894d4`):
`P3-FEATURE-A-MAJ-01` (removed the invented `signed` sign-orientation
convention; fails closed instead), `P3-FEATURE-A-MAJ-02`
(`upstream_contract_refs` + `event_contract_ref` envelope field implemented
across all three engines and both output event types), `P3-FEATURE-A-MAJ-03`
(the Candle-formula injection boundary was assessed as already fail-closed
by construction — re-verified claim, not re-implemented), `P3-FEATURE-A-MAJ-
04` (Swing `swing_revision` N+1 requires this engine's own explicit
invalidation of revision N first; newly-visible replacement revisions
re-evaluate any `PENDING_CORRECTION` window), `P3-FEATURE-A-MAJ-05`
(Candle/Regime dedup is ref-identity-only, never value-equality),
`P3-FEATURE-A-MAJ-06` (Swing eligibility's recorded-time visibility check
takes an explicit cursor parameter derived from the triggering event). All
six recorded `REMEDIATED_PENDING_BOUNDED_REREVIEW`.

**Round 2** (this build, boundary `039358e5856168fe14557e194e50133d4fbf7cf8`)
— a bounded re-review found MAJ-02/-03/-04/-05/-06 still open against the
Round 1 remediation's actual code (MAJ-01 confirmed closed, untouched here):

- `P3-FEATURE-A-MAJ-02`: Round 1 left a fabricated `"v0"` stand-in for
  Feature's own outbound `event_contract_ref.contract_version`
  (`FEATURE_EVENT_CONTRACT_VERSION`), and `SwingDistanceFeatureEngine`
  validated only `contract_id`, accepting any `contract_version`. Both
  removed: output contract version is now a required, caller-injected,
  fail-closed-if-empty constructor argument
  (`resolve_output_contract_refs`), and `SwingDistanceFeatureEngine` now
  exact-matches full `{contract_id, contract_version}` against a
  caller-injected authorized set for both Candle and Swing inputs.
- `P3-FEATURE-A-MAJ-03`: Round 1's "already fail-closed" claim was
  re-verified as **incorrect** — a matching `formula_id` string was
  sufficient to authorize execution of an arbitrary caller-supplied
  callable. `CandleWindowFeatureEngine` no longer accepts any injected
  formula; construction always fails closed
  (`UnsupportedFeatureFormulaError`).
- `P3-FEATURE-A-MAJ-04`: Round 1's reattempt only covered windows currently
  `PENDING_CORRECTION`, silently leaving windows that had already settled
  `VALID` on a lower-priority alternate Swing permanently stale once the
  preferred Swing's corrected revision arrived. `on_swing_confirmed` now
  re-evaluates every window with a lineage entry and invalidates+replaces a
  settled window if the deterministic winner changes (regression:
  `test_settled_valid_window_preempted_by_higher_priority_corrected_revision`).
- `P3-FEATURE-A-MAJ-05`: Round 1's Swing-side dedup in
  `SwingDistanceFeatureEngine.on_swing_confirmed` never compared prior
  content for a redelivered ref at all, and the Candle-side check compared
  only `.ohlcv`, not the complete fact. Both now perform a full
  consumer-side-fact equality check before any dedup/routing/lineage logic.
- `P3-FEATURE-A-MAJ-06`: Round 1's "explicit cursor" was in fact always
  `candle.recorded_time`/`triggering_event.recorded_time` internally — no
  caller could supply an independent `R`. `on_candle`/`on_swing_confirmed`/
  `on_swing_invalidated` now take `cursor` as a required keyword argument,
  threaded through every internal eligibility/recomputation path.

All five recorded `REMEDIATED_PENDING_BOUNDED_REREVIEW` — none self-closed.
`P3-FEATURE-A-MAJ-01` remains `CLOSED`, untouched.

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
