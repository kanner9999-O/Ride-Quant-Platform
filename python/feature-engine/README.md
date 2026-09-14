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

## ADR-043 — Per-subject authoritative ownership implementation design (DESIGN ONLY)

**Status:** design record only, per Approved [`ADR-043`](../../docs/adr/ADR-043.md) (`v0.2`, `Approved`, immutable) — `ADR-043` is the sole architecture authority for everything in this section; this README only maps that already-decided authority onto concrete Feature Engine implementation structure. **No ownership runtime exists in this repository yet** — nothing in this section is implemented. `P3-FEATURE-QG-EVID07-A-MAJ-05` remains **OPEN**. `P3-FEATURE-QG-EVID-07` remains **OPEN / `FAIL — evidence`**. This design changes no production code, no test, no dependency, and no Event Schema.

**No prior README wording required correction here** — this module's README was previously *silent* on per-subject concurrency/ownership (it never claimed the question was "entirely undecided"), so there is nothing false to retract. The one true statement that remains true and unchanged: no real event log, broker, RPC/HTTP, or deployment/process topology exists for this module (see "What this module owns"/top-of-file, unchanged) — that external-adapter gap is exactly what part **C** below documents honestly, not something this design pretends to close.

### Chosen shape

A single new **module-internal per-`feature_subject_id` ownership/coordinator boundary wraps the existing analytical engines** — `RegimePassthroughFeatureEngine`, `SwingDistanceFeatureEngine`, and (structurally, though currently moot) `CandleWindowFeatureEngine` — rather than duplicating ownership/fencing logic independently inside each. The three engines' own deterministic analytical logic (lineage validation, total-order selection, `FeatureLineageError`/`InvalidSwingEligibilityInputError` rejection of illegal transitions) is **kept exactly as-is**; the coordinator adds ownership/fencing/catch-up/arbitration **around** it, and is the only thing authorized to call an engine's `on_*` methods on the authoritative (live-append) path. This is the smallest shape that satisfies `ADR-043` semantics 1–7 without inventing a second architecture layer: the engines already assume "one instance per Feature subject" (their own docstrings); the coordinator is what turns that assumption into an enforced, fenced, catch-up-proven guarantee.

### A — Subject ownership boundary

Key: `feature_subject_id` (the existing deterministic opaque subject-id `identity.py` already derives — unchanged). Ownership authority moves **out of** each engine instance and into a new `SubjectOwnershipRegistry` (in-process, module-internal — see the honest limitation below): it enforces, for each `feature_subject_id`, **at most one `ACTIVE` owner handle at any instant**; different subjects have fully independent handles and may be owned/processed concurrently with no shared state. Each engine's own `_lineage` dict remains its internal cache — it is **no longer implicitly sufficient ownership authority**; it is trustworthy only while the wrapping owner handle that constructed/drives that engine instance is `ACTIVE` at its current generation (below).

### B — Fencing / ownership generation

Each successful acquisition mints a strictly-increasing, per-subject `ownership_generation` (an integer epoch). An owner handle is the tuple `(feature_subject_id, ownership_generation, state)`. Revocation is a single, deterministic state transition (`ACTIVE → REVOKED`) that the registry performs **before** a new acquisition for the same subject may begin catch-up — never a window with two `ACTIVE` handles for one subject. **Critical:** ownership validity (`state == ACTIVE` and `ownership_generation` still current for the subject) is re-checked by the coordinator as the **last step immediately before** invoking an engine's `on_*` method and again immediately before treating the engine's returned events as ready for authoritative emission/sequence allocation — not merely once at owner construction. A call arriving against a handle whose generation has since gone stale fails closed (rejected), even if the caller still believes it holds ownership.

### C — Authoritative catch-up (honest limitation)

A new owner must reconstruct the subject's authoritative lineage from authoritative Feature event history before it may reach `ACTIVE` — process-local/empty memory is never sufficient. This is expressed as a bounded `AuthoritativeLineageHistoryProvider` protocol/interface boundary (mirroring the exact discipline already governing this codebase's `input_contract_authority_provider`/`output_event_contract_authority_provider` — required, verified, fail-closed-if-wrong-type constructor dependencies, `authority_resolver.py`/`output_contract_resolver.py`, unchanged) that the coordinator calls during `CATCHING_UP`. **Stated honestly, per instruction:** `publish.py`'s `SequenceAllocator` is explicitly **not**, and is not proposed to become, this provider — its own docstring already states it is "NOT a real event log or broker." No real, durable, cross-process Feature event log exists anywhere in this repository today (confirmed: `SequenceAllocator` is in-process/non-persistent; no broker/RPC/deployment topology exists per the top of this README). Therefore: **no production-authoritative implementation of this provider exists or is proposed by this design** — that is genuinely separate, future infrastructure work. The provider boundary's job is to answer, with proof, "what is the current authoritative lineage for this subject" — including truthfully for a genuinely brand-new subject with no prior history — and a `CATCHING_UP → ACTIVE` transition **fails closed** (stays `CATCHING_UP`, never advances) whenever no such provider is configured or the configured provider cannot prove successful reconstruction. This design does not fake persistence and does not treat "no provider configured" as equivalent to "subject has no history."

### D — Deterministic arbitration

The existing one-event-at-a-time API (`on_candle`/`on_regime_classified`/`on_swing_confirmed`/etc., already caller-driven "in cursor order" per this README) does not, by itself, prove a caller actually presented events in Chapter 8 §8.3.4's own `P_run` order. Rather than hide that gap, the coordinator adds one minimal, provable check: before applying an incoming fact, it validates that fact's **own already-carried Chapter 8 envelope fields** (`stream_ref.{stream_id, sequence}`, `causation_refs` — `envelope.py`, unchanged) are monotonically consistent with `P_stream ∪ P_causation` relative to what it has already applied for this subject; for facts unordered by either hard constraint, the subject's applicable Feature Input Contract's own `merge_policy.concurrent_tie_break` (unchanged, un-redefined, same authority already cited by `ADR-043`) resolves the remaining order. A fact that would violate this monotonic relationship is **rejected, fail-closed** — never silently applied in arrival order. This is not a new platform-global total order (it reuses only already-existing, already-authoritative per-event fields and the subject's own already-existing Input Contract) and not an arbitrary caller-supplied order value accepted on trust (the check is against the event's own Chapter-8-shaped identity, not a bare integer the caller asserts). Catch-up (**C**) replays authoritative history in this same `P_run` order, so a new owner necessarily arrives at the identical lineage state an uninterrupted original owner would have. The competing-successor case itself (two candidates both targeting the same lineage head) is still caught by the engines' own existing, unmodified `FeatureLineageError`/`InvalidSwingEligibilityInputError` — the coordinator's job is to guarantee that check is reached only once, by exactly the one currently-fenced owner, in `P_run` order.

### E — Existing engine integration

- `RegimePassthroughFeatureEngine` / `SwingDistanceFeatureEngine`: unchanged internally; wrapped, not modified. Their `_lineage` remains internal cache, now understood as valid only under an `ACTIVE`, current-generation owner (documentation reframing, not a code change).
- `CandleWindowFeatureEngine`: structurally covered by the same wrapper (any of the three engine types is wrappable identically), but moot in practice — construction always fails closed today (`UnsupportedFeatureFormulaError`, unrelated, untouched, not reopened).
- `FeatureCurrentView`: explicitly **outside** the ownership boundary. It is already non-authoritative, fed by an external caller, never wired automatically into any engine (unchanged) — no ownership concept applies to a read-side projection regardless of how many consumers read it.
- `SequenceAllocator`/`publish.py`: unchanged. Sequence allocation for a subject can only occur while that subject's owner is `ACTIVE` (the ownership check gates access to the engine calls that lead to `next_ref`), but the allocator itself is not modified — it remains the existing, honestly-labeled, non-persistent, module-local stand-in.

**Proposed new source files (identified only, not implemented by this transaction):**

```
src/feature_engine/ownership.py   SubjectOwnershipState (INACTIVE/CATCHING_UP/
                                   ACTIVE/REVOKED), OwnerHandle (subject_id,
                                   generation, state), SubjectOwnershipRegistry
                                   (in-process, per-subject single-ACTIVE-owner
                                   enforcement, acquire/revoke), AuthoritativeSubjectOwner
                                   (coordinator: wraps one analytical engine instance
                                   for one subject; gatekeeps on_* calls; performs the
                                   §D monotonicity check; re-validates ownership
                                   immediately before emission per §B)
src/feature_engine/errors.py      (extended, not replaced) new named fail-closed
                                   exceptions: e.g. StaleOwnershipGenerationError,
                                   DualOwnershipError, UnprovenCatchUpError,
                                   NonMonotonicApplicationOrderError,
                                   AuthoritativeHistoryProviderUnavailableError
```

No change proposed to `regime_passthrough.py`, `swing_distance.py`, `candle_window.py`, `current_view.py`, `publish.py`, `contracts.py`, `authority_resolver.py`, `output_contract_resolver.py`, `replay_preparation.py`, `identity.py`, or `envelope.py`.

### F — Failure semantics (fail closed, no speculative authoritative output)

- Unknown owner (no registry entry / never acquired) → rejected.
- Stale fencing generation → rejected.
- Dual-owner ambiguity for one subject (should be structurally prevented by the registry's own acquire logic; if ever detected, e.g. via an internal invariant check) → that subject scope fails closed, never a runtime-selected "winner."
- Failed/incomplete catch-up → stays `CATCHING_UP`, never reaches `ACTIVE`; no emission possible.
- Inability to derive deterministic precedence (§D's monotonicity check fails and no Input-Contract tie-break resolves it) → the fact is rejected, not guessed.
- Handoff interrupted between revoke and activation (e.g. process crash mid-handoff) → the subject is left with **no** `ACTIVE` owner; fails closed for all further attempts until a fresh acquisition completes catch-up from scratch. Blast radius is scoped to the one affected `feature_subject_id` — consistent with [I-6](../../docs/constitution/02-platform-invariants.md) Fail-Safe by Scope, never a platform-wide halt.

### G — Replay / non-authoritative modes

Replay/backtest/shadow/simulation execution **never** calls into `SubjectOwnershipRegistry`/`AuthoritativeSubjectOwner` — it constructs and drives the analytical engines directly, exactly as `EVID-05(a)`'s already-validated self-contained-replay tests (`tests/test_replay_isolation.py`) already do today, unaffected and unrevisited by this design. Owner identity/generation is pure execution-control metadata; it is never serialized into `FeatureComputed`/`FeatureFactInvalidated` and never added to Feature Event Schema (`ADR-043` semantic 6, unchanged). Because catch-up strictly replays `P_run` order (§C/§D) and owner identity never enters event content, replaying identical authoritative history through the same, unmodified analytical engines reproduces the identical result regardless of which owner/generation originally produced it — an unchanged property of the existing pure, deterministic engines, not something this design has to add.

### H — Handoff lifecycle

Smallest sufficient state machine, one instance per `(feature_subject_id, ownership_generation)`:

```
INACTIVE → CATCHING_UP → ACTIVE → REVOKED
```

- `INACTIVE → CATCHING_UP`: on an acquire request, only when the registry holds no `ACTIVE`/`CATCHING_UP` handle for that subject.
- `CATCHING_UP → ACTIVE`: only after the `AuthoritativeLineageHistoryProvider` (§C) proves successful reconstruction; otherwise stays `CATCHING_UP` (fail closed, §F).
- `ACTIVE → REVOKED`: an explicit, single-step revoke, always performed before a new acquisition for the same subject may begin its own `CATCHING_UP`.
- `REVOKED` is terminal for that generation; any call against a revoked handle fails closed. No separate "draining" state is introduced — this codebase's engine calls are synchronous and single-threaded (no in-flight concurrent work exists to drain), and `ADR-043` does not itself require one; adding it would be over-design beyond what the ADR asks for.

### ADR Scope conflict check (explicit, per instruction)

This design introduces no new module, no dependency-graph edge, no Event Schema change, no Chapter 8 change, and no cross-module authority change — all confirmed directly against the proposed shape above. `AuthoritativeLineageHistoryProvider` is **not** a new authoritative source: it is a bounded read-side reconstruction boundary onto the *already*-authoritative Feature event stream `ADR-043`/Chapter 8 already grant `feature-engine` sole writer authority over — it creates no competing source of truth, and (per §C) no production implementation of it exists or is proposed here. No STOP condition is triggered.

## Current state (as of this build)

- Feature Engine: implemented (engine semantics only) — no production
  `FeatureDefinition`/`FeatureFormula` instance exists or is claimed; those
  remain externally unresolved configuration.
- Per-subject authoritative ownership (`ADR-043`, Approved): **design only**
  (see section above) — no ownership runtime exists yet. `P3-FEATURE-QG-
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
