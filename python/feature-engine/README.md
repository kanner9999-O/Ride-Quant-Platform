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

## ADR-043 — Per-subject authoritative ownership implementation (IMPLEMENTATION CANDIDATE — pending Review A implementation review / formal EVID-07 evidence)

**Status:** implementation candidate, per Approved [`ADR-043`](../../docs/adr/ADR-043.md) (`v0.2`, `Approved`, immutable) — `ADR-043` remains the sole architecture authority for everything in this section; this README maps that already-decided authority onto concrete Feature Engine implementation structure, now backed by real, tested source code. **The module runtime/coordinator semantics, authority/commit/history Protocol boundaries, and fail-closed behavior described below are implemented** in `src/feature_engine/ownership.py` (new), extensions to `contracts.py`/`authority_resolver.py`/`errors.py`, and a behavior-preserving `regime_passthrough.py`/`swing_distance.py` prepare/commit/historical-reconcile refactor — verified by deterministic tests (`tests/test_ownership.py`, plus extensions to `test_contracts.py`/`test_authority_resolver.py`/`test_historical_authority_resolver.py`) using in-memory test doubles, never claimed production-authoritative. **No production-durable event log, distributed fencing store, broker, RPC, or deployment topology exists or is implemented** — `SubjectOwnershipAuthority`/`FencedFeatureCommitter`/`AuthoritativeLineageHistoryProvider` remain Protocol-only boundaries with no production adapter, exactly as designed (§B/§C). `P3-FEATURE-QG-EVID07-A-MAJ-05` remains **OPEN**. `P3-FEATURE-QG-EVID-07` remains **OPEN / `FAIL — evidence`** — no Hypothesis/property-based evidence has been produced. The Feature Engine module remains **NOT APPROVED**; LIVE remains **NOT_AUTHORIZED**. This transaction changes no Input Contract artifact, no Chapter 8 semantic, and no Event Schema; it adds no runtime dependency (`pyproject.toml` remains zero runtime dependencies).

**Bounded correction 001 (preserved as history).** Review A found the first revision `REVISION_REQUIRED` (0 Blocker / 2 Major / 0 Minor): `ADR043-IMPLDESIGN-A-MAJ-01` (in-process registry alone insufficient across crash/failover) and `ADR043-IMPLDESIGN-A-MAJ-02` (arrival-order monotonicity checking insufficient to prove ordering). Correction 001 introduced `SubjectOwnershipAuthority` and a first certified-frontier mechanism.

**Bounded correction 002 (this revision).** A further bounded Review A re-review found correction 001 itself `REVISION_REQUIRED` (0 Blocker / 3 Major / 0 Minor):

```text
ADR043-IMPLDESIGN-A-MAJ-01 (residual) — commit-time fencing still had a
  validate-then-commit TOCTOU gap: a successful SubjectOwnershipAuthority
  validation immediately before commit does not, by itself, prevent a
  revocation landing in the gap between that validation and the actual
  write.
ADR043-IMPLDESIGN-A-MAJ-02 (residual) — the §D example incorrectly implied
  a certified frontier including B's position necessarily also reflects a
  causally/sequence-unrelated A's position -- P_run is run-local (the
  bounded apply set of one Input Contract's own certified cut), not a
  cross-stream global order (Chapter 8 §8.3.3).
ADR043-IMPLDESIGN-A-MAJ-03 (new) — catch-up (§C) claimed replaying only
  upstream input through a FRESH engine instance is sufficient. It is not:
  a fresh instance allocates NEW refs via SequenceAllocator.next_ref(),
  which are not necessarily the CANONICAL refs actually committed
  historically (_WindowLineage.head_fact.ref, pending_invalidation_ref,
  supersedes_fact_ref chains) that future transitions must reference.
```

Correction 002 corrected below (§B/§"Atomicity and emission" for MAJ-01, §D for MAJ-02, §C for MAJ-03) — none self-closed:

```text
ADR043-IMPLDESIGN-A-MAJ-01: CLOSED — REVIEW A VALIDATED
ADR043-IMPLDESIGN-A-MAJ-02: CLOSED — REVIEW A VALIDATED
ADR043-IMPLDESIGN-A-MAJ-03: CLOSED — REVIEW A VALIDATED
```

**Bounded correction 003 (this revision).** A further bounded Review A re-review of correction 002 found one residual Major:

```text
ADR043-IMPLDESIGN-A-MAJ-04 (new) — the design correctly requires
  AuthoritativeSubjectOwner to construct P_run from the applicable Input
  Contract's authoritative merge_policy.algorithm/merge_policy.
  concurrent_tie_break, but the implementation authority path does not
  actually expose those fields: VerifiedInputContractAuthority
  (contracts.py) carries only feature_computation_profile/
  input_contract_ref/stream_registry_version/included_streams/
  input_contract_content_id/stream_registry_content_id, and
  authority_resolver.py's field extraction resolves only that same
  subset. Direct artifact inspection confirms both
  docs/architecture/input-contracts/feature-swing-distance-input.yaml
  and feature-regime-input.yaml (and their ADR-041 v1.0 historical
  snapshots) already declare a merge_policy: {algorithm, concurrent_tie_
  break} block the resolver simply does not read yet. Without this,
  implementation could only obtain merge_policy by hard-coding today's
  values inside ownership.py (a prohibited duplicate/ungoverned
  authority) or inventing a second, ungoverned source.
```

Corrected below (new §D2) — not self-closed:

```text
ADR043-IMPLDESIGN-A-MAJ-01: CLOSED — REVIEW A VALIDATED
ADR043-IMPLDESIGN-A-MAJ-02: CLOSED — REVIEW A VALIDATED
ADR043-IMPLDESIGN-A-MAJ-03: CLOSED — REVIEW A VALIDATED
ADR043-IMPLDESIGN-A-MAJ-04: CLOSED — REVIEW A VALIDATED
```

**Implementation (this revision).** Bounded Review A of the final implementation design was CLEAN (0 Blocker / 0 Major / 0 Minor across all four findings). Risk Classification `R1`; no Product Owner re-approval required; this transaction implements the reviewed design — it is not architecture authoring, ADR authoring, Product Owner approval, or EVID-07 evidence closure.

```text
ADR043-IMPLDESIGN-A-MAJ-01: CLOSED — REVIEW A VALIDATED
ADR043-IMPLDESIGN-A-MAJ-02: CLOSED — REVIEW A VALIDATED
ADR043-IMPLDESIGN-A-MAJ-03: CLOSED — REVIEW A VALIDATED
ADR043-IMPLDESIGN-A-MAJ-04: CLOSED — REVIEW A VALIDATED
```

Implemented, source-level:

- `contracts.py` — `InputMergePolicy`; `VerifiedInputContractAuthority.merge_policy`, sealed only through the existing `_seal_verified_authority`/`_construct_verified_authority` factory; `PreparedFeatureComputed`/`PreparedFeatureFactInvalidated`/`PreparedTransition` — the shared prepare/live-commit/historical-reconcile machinery both engines use.
- `authority_resolver.py` — both the current-path and historical (exact pinned ADR-041 snapshot, no fallback) resolvers parse and fail-closed-validate `merge_policy` (`UnsupportedMergePolicyError` on missing/malformed/unsupported).
- `errors.py` — `UnsupportedMergePolicyError`, `StaleOwnershipGenerationError`, `DualOwnershipError`, `OwnershipAuthorityUnavailableError`, `UnprovenCatchUpError`, `CanonicalHistoryMismatchError`, `NonMonotonicApplicationOrderError`, `IncompleteCertifiedFrontierError`.
- `ownership.py` (new) — `SubjectOwnershipState`, `OwnerHandle`, `SubjectOwnershipAuthority`/`FencedFeatureCommitter`/`AuthoritativeLineageHistoryProvider` Protocols (no production implementation), `SubjectOwnershipRegistry`, `UpstreamEnvelope`/`UpstreamHistoryResult`/`CanonicalOutputHistoryResult`, `p_run_sort` (deterministic `P_stream ∪ P_causation` topological sort, resolved `merge_policy.concurrent_tie_break` tie-break, run-local, fails closed on a cycle via `NonMonotonicApplicationOrderError`), `AuthoritativeSubjectOwner` (acquire/catch-up/activate, `process_certified_frontier`, fenced commit, §9 fail-closed-and-fence-on-uncertain-outcome recovery model).
- `regime_passthrough.py`/`swing_distance.py` — existing `_emit_*` logic split into `prepare_*` (candidate only, no ref/no `_lineage` mutation), the existing `on_*` methods now prepare-then-immediately-live-commit (byte-identical behavior/output, all pre-existing tests pass unchanged), and `prepare_upstream_event` (the one dispatch seam `AuthoritativeSubjectOwner` uses). Analytical rules (eligibility, total order, lineage/no-fork, evidence normalization, cursor validation, correction semantics) are unchanged.

New/extended tests: `tests/test_ownership.py` (fencing, atomic batch commit/rollback, `p_run_sort` ordering including "does not wait for a hypothetical future event," catch-up reconstruction — including non-selected Swing state and zero-new-refs-allocated — canonical mismatch/incomplete-history fail-closed, positive-empty-proof activation, absent-provider fail-closed, crash/local-cache-recovery fencing), plus merge-policy coverage added to `test_contracts.py`/`test_authority_resolver.py`/`test_historical_authority_resolver.py`. All pre-existing tests remain green (339 passed; `ruff check`/`mypy --strict` clean on all changed files — 2 pre-existing, unrelated `authority_resolver.py` line-length findings predate this transaction).

**No prior README wording required correction beyond the above** — this module's README was previously *silent* on per-subject concurrency/ownership before the first design revision, so there was nothing false to retract there. The one true statement that remains true and unchanged: no real event log, broker, RPC/HTTP, or deployment/process topology exists for this module (see "What this module owns"/top-of-file, unchanged) — that external-adapter gap is exactly what §**B**/§**C** below document honestly, not something this design pretends to close.

### Chosen shape

A single new **module-internal per-`feature_subject_id` ownership/coordinator boundary wraps the existing analytical engines** — `RegimePassthroughFeatureEngine`, `SwingDistanceFeatureEngine`, and (structurally, though currently moot) `CandleWindowFeatureEngine` — rather than duplicating ownership/fencing logic independently inside each. The three engines' own deterministic analytical logic (lineage validation, total-order selection, `FeatureLineageError`/`InvalidSwingEligibilityInputError` rejection of illegal transitions) is **kept exactly as-is** — no analytical RULE changes; only an internal method-shape refactor is required (§"Atomicity and emission" below) exposing three seams: prepare a candidate transition, commit it live under a fenced authoritative commit, or reconcile it against canonical historical output during catch-up (§C). The coordinator adds ownership/fencing/catch-up/arbitration **around** the engines' unchanged logic, and is the only thing authorized to drive an engine's `on_*` methods on the authoritative (live-append) path. This remains the smallest shape that satisfies `ADR-043` semantics 1–7 without inventing a second architecture layer.

### A — Subject ownership boundary

Key: `feature_subject_id` (the existing deterministic opaque subject-id `identity.py` already derives — unchanged). Ownership authority moves **out of** each engine instance. Two distinct components are named:

- `SubjectOwnershipRegistry` — process-local coordinator/cache/state-machine view (§H's `INACTIVE`/`CATCHING_UP`/`ACTIVE`/`REVOKED`) — never sufficient authority by itself (§B).
- `SubjectOwnershipAuthority` — the external, durable, exclusivity-proving boundary (§B).

Different subjects have fully independent ownership state and may be owned/processed concurrently with no shared state between them. Each engine's own `_lineage` dict remains its internal cache/reconstruction material — it is **never itself the commit authority** (§B/§"Atomicity and emission"); it is trustworthy only while the wrapping owner is `ACTIVE` at a generation the `SubjectOwnershipAuthority` currently recognizes as current.

### B — Authoritative fencing boundary (`ADR043-IMPLDESIGN-A-MAJ-01` corrected — residual TOCTOU closed)

**`SubjectOwnershipAuthority`** (interface/semantics only — exact name/implementation-technology intentionally unselected; no database/broker/orchestration product is chosen). Per `feature_subject_id`, it must provide atomic generation acquisition, validation that a generation is still current, revocation-before-successor, fail-closed behavior whenever exclusivity cannot be proven, survival across process crash/restart/deployment replacement, no wall-clock election, no dual-active generations — unchanged from correction 001.

**`SubjectOwnershipRegistry`** remains demoted: process-local coordinator/cache reflecting what the coordinator *believes* the Authority most recently granted, plus the local state machine (§H) driving *when* the coordinator asks the Authority to acquire/validate/revoke — never authoritative by itself.

**Test/local adapter:** a bounded in-memory implementation of `SubjectOwnershipAuthority` may exist for deterministic unit/integration testing or single-process, non-production use, **explicitly labeled `NOT sufficient for production-authoritative cross-process ownership`**. Authoritative-production mode without a genuine, durable `SubjectOwnershipAuthority` configured **fails closed**.

**Correction, stated directly (residual `ADR043-IMPLDESIGN-A-MAJ-01`):** the prior revision's "revalidate immediately before commit" was still a **separate check followed by a separate write** — a validate-then-commit TOCTOU gap. Counterexample: owner N's revalidation call returns "current"; before N's own subsequent write actually lands, another process revokes N and mints N+1; N's write still lands, now under a fenced-but-unenforced generation. A validation call that merely *precedes* the write, however closely, is not itself sufficient.

**Corrected boundary — `FencedFeatureCommitter` (naming implementation-local):** the authoritative commit is redefined as **one indivisible operation**, not a validate-step followed by a write-step:

```text
verify ownership generation is still current
  + allocate authoritative Feature stream sequence(s)
  + append/commit authoritative Feature event(s)
= ONE indivisible authoritative operation, enforced by the commit
  authority itself -- not by the caller performing "check" then "write"
  as two separate calls with a gap between them.
```

A stale generation is rejected **by the commit authority as part of this one operation**, not by a caller-side check that could itself be stale by the time the write actually happens. This is the same class of guarantee a conditional/compare-and-write primitive provides in a real durable store — this design does not select which one; it fixes the semantic contract the eventual implementation must satisfy.

**Fencing token is operational commit metadata only.** The `ownership_generation` used by `FencedFeatureCommitter`/`SubjectOwnershipAuthority` **MUST NOT** be added to `FeatureComputed`, `FeatureFactInvalidated`, Feature Event Schema, or any Feature domain semantic — unchanged principle from `ADR-043` semantic 6, restated here explicitly at the commit boundary where it would be easiest to accidentally leak in.

**Batch commit for multi-event transitions.** Direct source analysis confirms at least one existing transition already produces two events together: `SwingDistanceFeatureEngine._invalidate_and_replace` returns `[invalidation, replacement]` from one logical engine transition. The fenced commit operation above must therefore support an **atomic batch**: verify-generation + allocate-sequence(s) + append-event(s) for the **whole** batch as one indivisible operation — no partial authoritative transition (e.g. invalidation committed but replacement not), no consumed-but-uncommitted sequence gap, contiguous sequence preserved across the batch, and every event in the batch committed under the same still-current generation.

**Corrected local ordering:**

```text
1. derive certified ordered work                 (§D)
2. prepare candidate transition(s)                (engine logic UNCHANGED;
                                                    no authoritative refs
                                                    allocated yet, no
                                                    self._lineage mutation
                                                    yet)
3. fenced authoritative commit                    (FencedFeatureCommitter,
                                                    ONE indivisible op:
                                                    verify generation +
                                                    allocate sequence(s) +
                                                    append event(s), as a
                                                    batch when >1 event)
4. only after step 3 succeeds: update process-
   local engine lineage/cache; advance the local
   committed-frontier cache
```

If the process crashes after step 3 succeeds but before step 4 completes: the authoritative history is already correct (step 3 is the durable commit); restart/catch-up (§C) recovers local `_lineage`/cache state from that already-committed authoritative history — `_lineage` was always cache/reconstruction material, never the commit authority, so this crash window loses no authoritative data, only local cache that catch-up rebuilds.

### C — Authoritative catch-up (`ADR043-IMPLDESIGN-A-MAJ-03` corrected — canonical identity reconciliation, not fresh replay)

**Correction, stated directly:** the prior revision's "construct a fresh engine instance and replay upstream input through unmodified `on_*` methods" is **not sufficient**. A fresh instance's own `SequenceAllocator.next_ref()` calls mint **new** refs from wherever that instance's own counter starts — these are not necessarily the **canonical** refs that were actually, historically committed. Downstream state depends on exact canonical identity: `_WindowLineage.head_fact.ref`, `pending_invalidation_ref`/`pending_invalidation_recorded_time`, and every `supersedes_fact_ref`/`invalidated_fact_ref` chain a *future* live transition must reference correctly. A replay that silently invents its own new refs for historical facts would desynchronize the reconstructed lineage from the real, already-committed chain.

Catch-up therefore needs **both** authoritative history sources, not one:

1. **certified upstream input history** — to rebuild hidden analytical state, including non-selected Swing observations `_SwingConfirmationRecord`/`_SwingInvalidationRecord` track that leave no trace in Feature's own output (unchanged finding from correction 001, still valid);
2. **canonical authoritative Feature output history** (`FeatureComputed`/`FeatureFactInvalidated`, as actually committed) — to restore/validate the *exact* committed refs, `recorded_time` values, invalidation refs, and supersession chain.

**Corrected reconstruction model, per upstream input event replayed in `P_run` order (§D) up to the catch-up frontier:**

```text
certified upstream input event
        v
engine computes a PREPARED historical candidate transition
  (same deterministic logic as live "prepare", §"Atomicity and emission" --
  NO next_ref() call, NO self._lineage mutation yet)
        v
match/validate the candidate against the corresponding CANONICAL
committed FeatureComputed / FeatureFactInvalidated event supplied by
canonical Feature output history (same window, same computed value,
same superseded/invalidated target)
        v
if they match: commit the INTERNAL reconstructed _lineage entry using
  the CANONICAL historical event's own ref / recorded_time / causation
  content -- never a freshly allocated one
if they do NOT match: FAIL CLOSED (never silently prefer upstream-
  replay semantics over canonical output history, or vice versa)
        v
continue to the next certified input event
```

**During catch-up, explicitly:** the live `FencedFeatureCommitter` path (§B) is **never** called; no new authoritative Feature sequence/ref is ever allocated; no replacement/invalidation event is ever appended; no `recorded_time` is ever invented — every value used to populate reconstructed `_lineage` comes from the canonical historical record the provider supplies.

**Exact state that must be reconstructed before `CATCHING_UP → ACTIVE`:**

- the exact current canonical Feature lineage head per window (`_WindowLineage.head_fact`, with its real, historical `ref`);
- exact invalidated/pending-correction state (`pending_invalidation_ref`/`pending_invalidation_recorded_time` where applicable);
- the exact historical Feature refs needed for any future `supersedes_fact_ref`/`invalidated_fact_ref` a live transition will need to reference;
- hidden upstream analytical state the engine needs (non-selected Swing confirmations/invalidations; last-evidence full content for `RegimePassthroughFeatureEngine`'s conflict check) — from certified upstream input history, unchanged from correction 001's finding;
- `last_committed_frontier` (or equivalent checkpoint) — the certified boundary up to which reconstruction is proven complete, so live processing (§D) resumes exactly there, never reapplying already-committed input.

**A genuinely brand-new subject must be positively proven, not assumed.** The provider must affirmatively answer "no prior authoritative Feature history exists for this subject" **and** "no prior applicable upstream history exists at the starting frontier" — both as positive proof from a real, configured, reachable provider. Absence of a configured provider, or an unreachable one, is **never** treated as evidence of an empty subject; both fail closed identically (§F).

This is expressed as a bounded `AuthoritativeLineageHistoryProvider` protocol/interface boundary (mirroring the exact discipline already governing this codebase's `input_contract_authority_provider`/`output_event_contract_authority_provider` — required, verified, fail-closed-if-wrong-type constructor dependencies, `authority_resolver.py`/`output_contract_resolver.py`, unchanged), now explicitly supplying **both** certified upstream input history and canonical Feature output history for catch-up, plus (unchanged from correction 001) the certified not-yet-applied apply-set for ongoing operation (§D). **Stated honestly, per instruction:** `publish.py`'s `SequenceAllocator` is explicitly **not**, and is not proposed to become, this provider — its own docstring already states it is "NOT a real event log or broker." No real, durable, cross-process Feature event log exists anywhere in this repository today. **No production-authoritative implementation of this provider exists or is proposed by this design** — genuinely separate, future infrastructure work. A `CATCHING_UP → ACTIVE` transition **fails closed** whenever no such provider is configured, the provider is unreachable, or reconciliation (above) does not prove complete and matched.

**Corrected `EVID-05(a)` citation:** `tests/test_replay_isolation.py` (unaffected, unrevisited) proves that Replay **execution** is externally self-contained after authority materialization — it does **not** prove that exact historical Feature-ref/lineage identity can be reconstructed from a fresh instance. That is a different property; the prior revision's citation overstated what it shows, and this correction relies on it only for the narrower, correct claim.

### D — Deterministic arbitration over a certified complete frontier (`ADR043-IMPLDESIGN-A-MAJ-02` corrected — P_run is run-local, not a cross-stream global order)

**Correction, stated directly:** correction 001's own worked example incorrectly implied that a certified frontier including B's stream position necessarily also reflects a causally/sequence-*unrelated* A's committed position — treating the Input Contract's `concurrent_tie_break` as if it created an ordering *obligation* between independent streams. It does not: Chapter 8 §8.3.3 is explicit that the platform "does not claim a global total order between independent streams," and `P_run` (§8.3.4) is the **induced order over one Input Contract's own bounded apply set** for one certified cut — not a claim about append timing between events with no `P_stream`/`P_causation` relationship at all. That incorrect implication is retracted.

**Corrected primary mechanism — unchanged tools, corrected reasoning:** [`contracts.py`](./src/feature_engine/contracts.py)'s existing, caller-certified, proof-carrying `EvaluationFrontier`; [`feature-context-architecture.md`](../../docs/architecture/engine/feature-context-architecture.md) §4.6 (v0.6, already Approved)'s frontier-certification protocol (lifecycle bracket, registry-contract equality gate, causal-closure fixed point, deterministic discard-and-retry on a detected race) — the coordinator is a *consumer* of an already-certified frontier, same as the engines already are; Chapter 8 §8.3.4's `P_stream ∪ P_causation` hard constraints and the subject's own Input Contract `merge_policy.algorithm`/`merge_policy.concurrent_tie_break` for events ordered by neither. **Corrected this revision (§D2 below):** that `merge_policy` value is obtained exclusively from the coordinator's own resolved `VerifiedInputContractAuthority.merge_policy` — never a README constant, never a value `ownership.py` hard-codes, and never a fresh YAML read `ownership.py` performs itself.

**Corrected per-step algorithm** (steps 1–6 unchanged in shape from correction 001: obtain a certified `EvaluationFrontier`; query the provider (§C) for the not-yet-applied apply-set visible within it; construct `P_run` over that bounded set; topologically sort; apply in that order via the engine's unmodified `on_*` methods, with the defensive monotonicity check now running only as a belt-and-suspenders invariant over the already-`P_run`-sorted sequence; advance `last_committed_frontier` only after the batch commits per §B).

When the received frontier is incomplete for this subject's own Input Contract: defer/buffer according to that Input Contract's own already-authoritative `frontier_policy` (values not restated here per this README's own SSOT discipline) — or fail closed where that policy requires it.

**Two corrected, explicit cases (replacing the prior single, incorrectly-reasoned example):**

```text
Case 1 -- both A and B are already authoritative committed records,
  both visible within the SAME certified cut:
  Transport/notification delivers B's arrival to this process before A's.
  The certified direct-log frontier (§4.6) includes BOTH A and B.
  P_run (derived from Chapter 8 hard constraints + Input Contract
    tie-break) orders A before B.
  The coordinator applies A, then B -- transport/notification arrival
    order is irrelevant. This is exactly the delivery-lag hazard the
    frontier-certification mechanism exists to solve (§4.6's own stated
    purpose).

Case 2 -- B is committed and visible at this certified frontier; A does
  NOT yet exist at this frontier (not yet committed, or on an
  independent stream with no P_stream/P_causation relationship to B):
  A is not a vertex of THIS apply set's P_run at all.
  The coordinator MUST NOT wait for a hypothetical future A merely
    because some future apply set's tie-break key might sort an A
    before a B -- there is no such obligation for events that are not
    both members of the same certified apply set.
  B is processed now, under the CURRENT, valid P_run.
  A LATER A, once it is itself certified/committed, belongs to a LATER
    P_run/apply set, and its own resulting Feature transition is then
    governed by the current authoritative lineage/head at THAT time,
    feature.md's correction/no-fork semantics, and ADR-043's own
    serialization -- never by retroactively reinterpreting the earlier,
    already-valid P_run that already processed B.
```

**No global order:** ordering stays local to the applicable Feature Input Contract's own apply set (`P_run`) for one subject's certified frontier — unchanged conclusion, now on a corrected, run-local (not cross-stream) reasoning. The competing-successor case (two candidates targeting the same lineage head) remains caught by the engines' own existing, unmodified `FeatureLineageError`/`InvalidSwingEligibilityInputError`, reached in genuine `P_run` order rather than arrival order.

### D2 — Merge-policy authority (`ADR043-IMPLDESIGN-A-MAJ-04` corrected — extend the existing resolver boundary, invent nothing new)

**Correction, stated directly:** §D's `P_run` construction correctly names the subject's own Input Contract `merge_policy.algorithm`/`merge_policy.concurrent_tie_break` as (together with Chapter 8's hard constraints) the authority for tie-breaking. But direct source inspection confirms the implementation authority path does not yet carry that value anywhere a coordinator could legitimately obtain it:

- `VerifiedInputContractAuthority` (`contracts.py`) — the *only* type any engine/coordinator is structurally permitted to trust as bound Input Contract authority — carries exactly `feature_computation_profile`, `input_contract_ref`, `stream_registry_version`, `included_streams`, `input_contract_content_id`, `stream_registry_content_id`. No `merge_policy` field exists.
- `authority_resolver.py`'s `_extract_scalar`/`_extract_included_streams` line-scanner extracts exactly that same subset from the real YAML text. It does not read the `merge_policy:` block at all, even though direct inspection confirms both real current artifacts (`docs/architecture/input-contracts/feature-swing-distance-input.yaml:109-111`, `feature-regime-input.yaml:105-107`) — and their ADR-041 `v1.0` immutable historical snapshots under `docs/architecture/input-contract-versions/*/v1.0.yaml` — already declare:
  ```yaml
  merge_policy:
    algorithm: deterministic-causal-topological-order
    concurrent_tie_break: [stream_id, sequence]
  ```

Without a corrected resolver boundary, `AuthoritativeSubjectOwner` (`ownership.py`) could only obtain this value by hard-coding today's `deterministic-causal-topological-order`/`[stream_id, sequence]` directly inside `ownership.py` (a prohibited second, ungoverned copy of Input Contract authority — the exact duplicate-authority defect this repository's whole `VerifiedInputContractAuthority`/`InputContractAuthorityProvider` discipline exists to prevent) or by having `ownership.py` read the Input Contract YAML itself (an ungoverned second resolution path, bypassing `authority_resolver.py`'s cross-validation entirely). Neither is acceptable; both are ruled out below.

**Corrected design — extend the existing authority-resolution boundary, do not create a second one:**

```text
InputMergePolicy                    (contracts.py, new; naming implementation-
  algorithm: str                    local)
  concurrent_tie_break: tuple[str, ...]

VerifiedInputContractAuthority      (contracts.py, extended — same no-public-
  ...                                constructor / resolver-only-provenance
  merge_policy: InputMergePolicy    discipline as every other field on this
                                     type, unchanged: only _seal_verified_
                                     authority may populate it)
```

`InputMergePolicy` is sealed as part of the *same* `_seal_verified_authority`/`_construct_verified_authority` factory pair that already exclusively constructs `VerifiedInputContractAuthority` — no new construction path, no new trust boundary, no relaxation of the existing "no public constructor, resolver-provenance-only" rule that field already documents for every other field on this type.

**Current path — `resolve_input_contract_authority_from_repository`:** extended to additionally parse the current artifact's own `merge_policy:` block (a bounded block-scanner analogous to the existing `_extract_included_streams`, reading `algorithm:` and the `concurrent_tie_break:` flow-sequence directly beneath it — no PyYAML dependency introduced, consistent with this resolver's existing dependency-free discipline) and to validate it (fail-closed rules below) before sealing it onto the returned `VerifiedInputContractAuthority`. This is the *same* artifact bytes already hashed into `input_contract_content_id` — no second read, no second artifact, no second trust boundary.

**Historical path — `resolve_historical_input_contract_authority_from_repository`:** extended identically, but reading `merge_policy:` from the exact immutable ADR-041 version-snapshot the historical `input_contract_ref`/`contract_version` names (`docs/architecture/input-contract-versions/<contract_id>/<contract_version>.yaml`) — never from the current/mutable Input Contract file, never a "same as current" shortcut, never a nearest-version search. A fact whose `computation_cursor` pins an older contract version is reconciled/replayed (§C) using **that exact pinned version's own** `merge_policy`, even if today's current artifact's `merge_policy` has since changed — mirroring the exact discipline this resolver already applies to `included_streams`/`stream_registry_version` for historical facts.

**Fail-closed validation (both paths, same rule set):** authority resolution raises (a new, named error — e.g. `UnsupportedMergePolicyError`, extending `errors.py`) whenever the parsed `merge_policy` is:

- missing (no `merge_policy:` block found in the artifact at all);
- malformed (`algorithm`/`concurrent_tie_break` absent, empty, or not parseable as this resolver's own bounded block grammar expects);
- **unsupported by the current Feature implementation** — for this correction, the *only* algorithm/tie-break combination this design's coordinator logic actually implements is exactly `algorithm: deterministic-causal-topological-order` with `concurrent_tie_break: [stream_id, sequence]` (§D's own P_run algorithm is built around precisely this combination); any other resolved value, however well-formed, is rejected — **never silently normalized/coerced into the supported combination**, and never silently ignored in favor of a coordinator default.

This is the same "validate exactly what the implementation actually supports, fail closed on anything else" discipline `FeatureDefinition.__post_init__` (`contracts.py`) already applies to `correction_policy`/`input_normalization_policy`/etc. — extended here to `merge_policy`, not a new validation philosophy.

**Coordinator consumption — `ownership.py` never resolves, never hard-codes:** `AuthoritativeSubjectOwner` receives its `VerifiedInputContractAuthority` the same way every existing computation engine already does — injected via an `InputContractAuthorityProvider` at construction (or, more precisely, the *same already-resolved instance* the wrapped engine itself holds, so the coordinator and the engine it wraps are provably looking at one identical, single resolution — never two independent resolutions that could disagree). `ownership.py`'s own source performs **no filesystem/repository access of any kind** — that discipline, already true for every existing engine (`contracts.py`/`swing_distance.py`/`regime_passthrough.py` never import `authority_resolver.py`), is extended unchanged to the new coordinator. The corrected dependency direction:

```text
authority_resolver.py  (filesystem I/O; parses + validates merge_policy,
    |                    current AND historical paths)
    v
VerifiedInputContractAuthority.merge_policy
    |
    v
AuthoritativeSubjectOwner (ownership.py)  -- consumes resolved merge_policy
    |                                        to construct P_run (§D);
    v                                        NEVER invents/hard-codes it
analytical engine (regime_passthrough.py /
                    swing_distance.py)
```

This changes no Input Contract artifact, no Chapter 8 semantic, no Event Schema, and creates no new authoritative concept — it only carries a value the Input Contract artifact *already, today* authoritatively declares through the one resolution boundary (`authority_resolver.py`) that already carries every other field of that same artifact's authority.

### E — Existing engine integration (updated — three seams, not two)

- `RegimePassthroughFeatureEngine` / `SwingDistanceFeatureEngine`: **analytical rules unchanged**. A bounded internal method-shape refactor is required exposing three seams — see "Atomicity and emission" below: (1) prepare a candidate transition (no refs, no mutation); (2) commit it live via `FencedFeatureCommitter` (§B); (3) reconcile a prepared historical candidate against canonical output during catch-up (§C). This corrects the "no engine change needed" claim from the very first revision, further specified (not merely "prepare/commit," but the three-way split catch-up also requires) this correction.
- `CandleWindowFeatureEngine`: structurally covered by the same wrapper, but moot in practice — construction always fails closed today (`UnsupportedFeatureFormulaError`, unrelated, untouched, not reopened).
- `FeatureCurrentView`: explicitly **outside** the ownership boundary, unchanged. Already non-authoritative, fed by an external caller, never wired automatically into any engine — no ownership concept applies to a read-side projection.
- `SequenceAllocator`/`publish.py`: **not modified**, but its `next_ref(...)` call site moves inside `FencedFeatureCommitter`'s own indivisible commit operation (§B) — never called during prepare (§B/§C), never called during catch-up reconciliation (§C).

### Atomicity and emission (resolves `ADR043-IMPLDESIGN-A-MAJ-01`'s residual TOCTOU gap)

**Direct source analysis, unchanged finding:** `SwingDistanceFeatureEngine._emit_original`/`_emit_replacement_only`/`_invalidate_and_replace` (and `RegimePassthroughFeatureEngine`'s equivalent `_emit_*` methods) today call `self._allocator.next_ref(...)` **and** mutate `self._lineage[key] = ...` together, in one synchronous method, with no seam. The corrected boundary (§B) replaces the prior revision's separate "revalidate, then allocate+mutate" two-step with the single indivisible `FencedFeatureCommitter` operation (§B) — closing the TOCTOU window a separate validate call could not.

**Engine-internal refactor (implemented):** `regime_passthrough.py`'s and `swing_distance.py`'s `_emit_*` methods are split into: a **prepare** phase (candidate value + candidate lineage delta, no `next_ref`, no `_lineage` mutation) driven for both live processing (§D) and historical reconciliation (§C); a **live commit** phase, invoked only through `FencedFeatureCommitter`'s indivisible verify+allocate+append operation (§B), which then applies the resulting `_lineage` mutation; and a **historical commit** phase (§C), which applies a `_lineage` mutation using a canonical historical event's own identity, never calling `next_ref()` or `FencedFeatureCommitter` at all. The engines' own analytical decisions (which transition is legal, what value to compute, which head is superseded) are identical across all three seams — only *where the resulting identity comes from* (freshly allocated live vs. canonical historical) and *whether/how it durably commits* differ.

**New/changed source files (implemented this transaction):**

```
src/feature_engine/contracts.py   (extended, not replaced) new InputMergePolicy
                                   value type (algorithm, concurrent_tie_break);
                                   VerifiedInputContractAuthority gains a
                                   merge_policy: InputMergePolicy field, sealed
                                   only by the existing _seal_verified_authority/
                                   _construct_verified_authority factory pair --
                                   no new construction path
src/feature_engine/authority_resolver.py
                                   (extended, not replaced) both
                                   resolve_input_contract_authority_from_
                                   repository (current path) and
                                   resolve_historical_input_contract_authority_
                                   from_repository (historical/pinned-snapshot
                                   path) parse + fail-closed-validate the
                                   artifact's own merge_policy block and seal it
                                   onto the returned VerifiedInputContractAuthority
                                   -- no PyYAML dependency introduced, same
                                   dependency-free block-scanner discipline
                                   already used for included_streams
src/feature_engine/ownership.py   SubjectOwnershipState (INACTIVE/CATCHING_UP/
                                   ACTIVE/REVOKED), OwnerHandle, SubjectOwnershipRegistry
                                   (process-local, NOT sufficient authority alone),
                                   SubjectOwnershipAuthority (Protocol -- external,
                                   durable, exclusivity-proving; no technology
                                   selected), AuthoritativeLineageHistoryProvider
                                   (Protocol -- supplies certified upstream input
                                   history + canonical Feature output history for
                                   catch-up, and the certified apply-set for
                                   ongoing operation), FencedFeatureCommitter
                                   (Protocol -- the one indivisible verify+
                                   allocate+append authoritative commit boundary,
                                   batch-capable), AuthoritativeSubjectOwner
                                   (coordinator: drives the §D certified-frontier
                                   algorithm; drives prepare/live-commit/historical-
                                   reconcile per §"Atomicity and emission"; re-
                                   validates fencing before beginning AND via the
                                   indivisible commit operation, never a separate
                                   pre-commit check alone; consumes the wrapped
                                   engine's own already-resolved
                                   VerifiedInputContractAuthority.merge_policy to
                                   construct P_run (§D/§D2) -- never resolves
                                   authority itself, never hard-codes a policy
                                   value)
src/feature_engine/regime_passthrough.py,
src/feature_engine/swing_distance.py
                                   (bounded, behavior-preserving refactor) split
                                   existing _emit_* methods into the three seams
                                   above -- analytical rules unchanged
src/feature_engine/errors.py      (extended, not replaced) new named fail-closed
                                   exceptions: e.g. StaleOwnershipGenerationError,
                                   DualOwnershipError, OwnershipAuthorityUnavailableError,
                                   UnprovenCatchUpError, CanonicalHistoryMismatchError,
                                   NonMonotonicApplicationOrderError,
                                   IncompleteCertifiedFrontierError,
                                   UnsupportedMergePolicyError
```

`application_order.py` is deliberately **not** introduced as a separate file — the §D algorithm remains small enough to live inside `ownership.py`'s `AuthoritativeSubjectOwner`. No change proposed to `candle_window.py`, `current_view.py`, `publish.py`, `output_contract_resolver.py`, `replay_preparation.py`, `identity.py`, or `envelope.py`. `contracts.py`/`authority_resolver.py` changes (§D2) are the one addition to correction 002's "no change" list — both bounded, additive extensions of their own existing types/functions, not new modules.

### F — Failure semantics (fail closed, no speculative authoritative output)

- Unknown owner (no registry entry / never acquired) → rejected.
- Stale fencing generation → rejected **as part of** `FencedFeatureCommitter`'s own indivisible operation (§B) — there is no separate window between a passing check and the write where staleness could slip through; a discarded attempt consumes no sequence, mutates no `_lineage`, advances no frontier.
- Dual-owner ambiguity for one subject → structurally prevented by `SubjectOwnershipAuthority`'s own atomic-acquisition guarantee; if ever detected regardless, that subject scope fails closed, never a runtime-selected "winner."
- `SubjectOwnershipAuthority` (or `FencedFeatureCommitter`) unreachable/unconfigured in an authoritative-production context → fails closed; never silently falls back to local-registry-only fencing.
- Partial multi-event batch commit → structurally prevented by the batch-capable indivisible commit (§B) — a batch either fully commits or has no effect at all.
- Failed/incomplete catch-up, including a provider that cannot prove complete, matched reconciliation (§C) → stays `CATCHING_UP`, never reaches `ACTIVE`; no emission possible.
- A recomputed historical candidate that does not match canonical Feature output history during catch-up (§C) → fail closed; never silently prefer one source over the other.
- Certified frontier incomplete for this subject's Input Contract → defer/buffer per that contract's own `frontier_policy`, or fail closed where the policy requires (§D).
- Inability to derive deterministic precedence within a certified apply set → the batch is rejected, not guessed.
- Resolved Input Contract `merge_policy` (current or historical/pinned) missing, malformed, or not one of the combinations this Feature implementation actually supports (§D2) → authority resolution itself fails closed; never silently normalized into the supported combination, never a coordinator-local default.
- Handoff interrupted between revoke and activation (e.g. process crash mid-handoff) → the subject is left with **no** `ACTIVE` owner; fails closed until a fresh acquisition completes catch-up from scratch. Blast radius scoped to the one affected `feature_subject_id` — consistent with [I-6](../../docs/constitution/02-platform-invariants.md) Fail-Safe by Scope.

### G — Replay / non-authoritative modes

Replay/backtest/shadow/simulation execution **never** calls into `SubjectOwnershipRegistry`/`SubjectOwnershipAuthority`/`FencedFeatureCommitter`/`AuthoritativeSubjectOwner` — it constructs and drives the analytical engines directly, exactly as `EVID-05(a)`'s already-validated self-contained-replay tests (`tests/test_replay_isolation.py`) already do today, unaffected and unrevisited by this design. This mode never needs canonical-ref reconciliation (§C) — it is not resuming live authoritative emission, only reproducing/verifying already-recorded values. Owner identity/generation is pure execution-control metadata; it is never serialized into `FeatureComputed`/`FeatureFactInvalidated` and never added to Feature Event Schema (`ADR-043` semantic 6, unchanged).

### H — Handoff lifecycle

Smallest sufficient state machine, one instance per `(feature_subject_id, ownership_generation)` — unchanged shape from prior revisions; correction found no need for another state:

```
INACTIVE → CATCHING_UP → ACTIVE → REVOKED
```

- `INACTIVE → CATCHING_UP`: on an acquire request, only when `SubjectOwnershipAuthority` (§B) grants a new generation for that subject.
- `CATCHING_UP → ACTIVE`: only after the corrected §C canonical-history reconciliation proves complete and matched, including positive proof of emptiness for a genuinely new subject; otherwise stays `CATCHING_UP` (fail closed, §F).
- `ACTIVE → REVOKED`: an explicit, single-step revoke against `SubjectOwnershipAuthority`, always performed before a new acquisition for the same subject may begin its own `CATCHING_UP`.
- `REVOKED` is terminal for that generation; any call against a revoked handle fails closed. No separate "draining" state — this codebase's engine calls are synchronous and single-threaded, and `ADR-043` does not itself require one.

### ADR Scope conflict check (explicit, per instruction)

This corrected design still introduces no new module, no dependency-graph edge, no Event Schema change, no Chapter 8 change, and no cross-module authority change — confirmed directly against the corrected shape above, including the engine-internal `_emit_*` refactor (a behavior-preserving method-shape change inside the already-registered `feature-engine` module). `AuthoritativeLineageHistoryProvider`, `SubjectOwnershipAuthority`, and `FencedFeatureCommitter` are **not** new authoritative sources: the first is a bounded read-side/reconciliation boundary onto the *already*-authoritative Feature event stream `feature-engine` already holds sole writer authority over (`stream-registry.yaml`, unchanged); the second and third are bounded exclusivity/commit boundaries realizing `ADR-043`'s own already-decided per-subject-ownership semantic, not competing domain-truth sources. No production implementation of any of them exists or is proposed here (§B/§C).

**§D2 addition, confirmed:** extending `VerifiedInputContractAuthority`/`authority_resolver.py` to also carry `merge_policy` changes no Input Contract artifact (both real artifacts already declare this block today, unmodified), no Chapter 8 semantic, no Event Schema, and no cross-module authority boundary — it carries an already-authoritative field of an artifact this resolver already reads and hashes, through the one resolution boundary that already carries every other field of that same artifact's authority. It does not create a second Input Contract authority path, and `ownership.py` remains, unchanged, forbidden from performing its own repository/filesystem authority resolution. No STOP condition is triggered.

## Current state (as of this build)

- Feature Engine: implemented (engine semantics only) — no production
  `FeatureDefinition`/`FeatureFormula` instance exists or is claimed; those
  remain externally unresolved configuration.
- Per-subject authoritative ownership (`ADR-043`, Approved): **implementation
  candidate** (see section above) — `ownership.py`'s coordinator/Protocol
  boundaries and the engines' prepare/commit/historical-reconcile seam are
  implemented and covered by deterministic tests using in-memory test
  doubles; no production-durable authority/commit/history adapter exists.
  Pending independent Review A implementation review. `P3-FEATURE-QG-
  EVID07-A-MAJ-05` remains **OPEN**. `P3-FEATURE-QG-EVID-07` remains
  **OPEN / `FAIL — evidence`**.
- Feature Engine Quality Tier: **UNRESOLVED** — not assigned in this
  transaction (registry has no `quality_tier` field for `feature-engine`).
- Structure Engine / Raw Regime Engine: unchanged by this transaction.
  Structure Engine's formal Chapter 13 Quality Gate (boundary
  `5b2b44f2263fc69af8c03578692796e63bafb5df`) remains **FAIL — evidence**;
  those findings are not remediated or reclassified here.
- No formal Chapter 13 Quality Gate claimed for Feature Engine.
- No module-level, Data-Layer-level, or Phase-3-level approval implied.
- LIVE: **NOT_AUTHORIZED**.
