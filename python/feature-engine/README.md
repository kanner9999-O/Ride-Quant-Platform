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

**Bounded correction (this revision).** Review A found the prior revision `REVISION_REQUIRED` (0 Blocker / 2 Major / 0 Minor): `ADR043-IMPLDESIGN-A-MAJ-01` — an in-process `SubjectOwnershipRegistry` alone cannot establish `ADR-043` exclusivity across crash/failover/restart/deployment replacement; `ADR043-IMPLDESIGN-A-MAJ-02` — one-event-at-a-time monotonicity rejection detects some violations but does not itself prove deterministic application order (Live arrival order could still select a winner before an earlier, tie-breaking event becomes visible). Both corrected below (§B/§"Atomicity and emission" for MAJ-01, §D for MAJ-02) — neither self-closed:

```text
ADR043-IMPLDESIGN-A-MAJ-01: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW
ADR043-IMPLDESIGN-A-MAJ-02: REMEDIATED — PENDING BOUNDED REVIEW A RE-REVIEW
```

**No prior README wording required correction beyond the above** — this module's README was previously *silent* on per-subject concurrency/ownership before the first design revision, so there was nothing false to retract there. The one true statement that remains true and unchanged: no real event log, broker, RPC/HTTP, or deployment/process topology exists for this module (see "What this module owns"/top-of-file, unchanged) — that external-adapter gap is exactly what §**B**/§**C** below document honestly, not something this design pretends to close.

### Chosen shape

A single new **module-internal per-`feature_subject_id` ownership/coordinator boundary wraps the existing analytical engines** — `RegimePassthroughFeatureEngine`, `SwingDistanceFeatureEngine`, and (structurally, though currently moot) `CandleWindowFeatureEngine` — rather than duplicating ownership/fencing logic independently inside each. The three engines' own deterministic analytical logic (lineage validation, total-order selection, `FeatureLineageError`/`InvalidSwingEligibilityInputError` rejection of illegal transitions) is **kept exactly as-is** — no analytical RULE changes; only an internal method-shape refactor is required (§"Atomicity and emission" below) to give the coordinator a genuine prepare/commit seam. The coordinator adds ownership/fencing/catch-up/arbitration **around** the engines' unchanged logic, and is the only thing authorized to drive an engine's `on_*` methods on the authoritative (live-append) path. This remains the smallest shape that satisfies `ADR-043` semantics 1–7 without inventing a second architecture layer.

### A — Subject ownership boundary

Key: `feature_subject_id` (the existing deterministic opaque subject-id `identity.py` already derives — unchanged). Ownership authority moves **out of** each engine instance. Two distinct components are now named (§B corrects the prior revision's conflation of them):

- `SubjectOwnershipRegistry` — process-local coordinator/cache/state-machine view (§H's `INACTIVE`/`CATCHING_UP`/`ACTIVE`/`REVOKED`), unchanged from the prior revision as a *local* concept.
- `SubjectOwnershipAuthority` — the external, durable, exclusivity-proving boundary (§B, new this revision).

Different subjects have fully independent ownership state and may be owned/processed concurrently with no shared state between them. Each engine's own `_lineage` dict remains its internal cache — it is **no longer implicitly sufficient ownership authority**; it is trustworthy only while the wrapping owner is `ACTIVE` at a generation the `SubjectOwnershipAuthority` (not merely the local registry) currently recognizes as current (§B).

### B — Fencing / authoritative fencing boundary (`ADR043-IMPLDESIGN-A-MAJ-01` corrected)

**Correction, stated directly:** the prior revision described `SubjectOwnershipRegistry` — process-local, in-memory — as if it alone were sufficient fencing authority. It is not: it does not survive process crash/restart, and two independently-running processes each running their own local registry could both believe they hold generation N for the same subject. This revision introduces a distinct, named boundary:

**`SubjectOwnershipAuthority`** (interface/semantics only — exact name/implementation-technology intentionally unselected here; no database/broker/orchestration product is chosen by this design). Per `feature_subject_id`, it must provide:

- **atomic acquisition** of a strictly-increasing `ownership_generation` — the Authority, not the local process, mints the generation, and two concurrent acquisition attempts for the same subject can never both succeed for the same or an overlapping generation;
- **validation** that `(feature_subject_id, ownership_generation)` is still the unique current authoritative generation, callable at any time by whichever process currently believes it holds ownership;
- **revocation/fencing** of the old generation as a precondition — the old generation is provably no longer current *before* a successor generation may be minted for the same subject;
- **fail-closed behavior** whenever exclusivity cannot be proven (Authority unreachable, ambiguous, or absent) — never a default-to-local-registry fallback;
- **survival across process crash/restart/deployment replacement** — this is precisely the property an in-process registry structurally cannot provide, which is why it cannot be the sole source of exclusivity;
- **no wall-clock election, no dual-active generations** — the same invariant `ADR-043` semantic 3 already requires, now pinned to an external authority rather than local memory.

**`SubjectOwnershipRegistry`** is retained, explicitly demoted: a process-local coordinator/cache reflecting what the coordinator *believes* the `SubjectOwnershipAuthority` most recently granted, plus the local `INACTIVE`/`CATCHING_UP`/`ACTIVE`/`REVOKED` state machine (§H, unchanged) driving *when* the coordinator asks the Authority to acquire/validate/revoke. It is never treated as authoritative by itself.

**Test/local adapter:** a bounded in-memory implementation of `SubjectOwnershipAuthority` may be designed for deterministic unit/integration testing or single-process, non-production use. It **must be explicitly labeled `NOT sufficient for production-authoritative cross-process ownership`** — the same honesty discipline this README already applies to `SequenceAllocator`. Running in an "authoritative production mode" without a genuine, durable `SubjectOwnershipAuthority` configured **fails closed** — the coordinator never silently falls back to local-registry-only fencing.

**Last-safe-point validation (corrected — was construction-time-only in the prior revision):** ownership validity is validated against the `SubjectOwnershipAuthority` (not merely local registry state) at two points: (1) **before beginning** an authoritative transition attempt for a subject, and (2) again, as the true last safe point, **immediately before commit** (§"Atomicity and emission" below) — i.e. immediately before the real sequence is allocated and the engine's `_lineage`/applied-frontier state is durably updated. A generation that was current at point (1) but has been fenced by the time point (2) is checked aborts the attempt with zero effect (§"Atomicity and emission").

### C — Authoritative catch-up (corrected — upstream replay, not output-only reconstruction)

**Correction, stated directly:** the prior revision implied Feature's own `FeatureComputed`/`FeatureFactInvalidated` output history alone would be sufficient to reconstruct an engine's full internal state. Direct source analysis shows this is **not proven** and, for at least two concrete fields, is false:

- `RegimePassthroughFeatureEngine._lineage[key].last_evidence_fact` holds the **full content** of the upstream `RegimeClassifiedFact` (used by `EvidenceReferenceConflictError`'s duplicate-delivery-with-conflicting-content check) — Feature's own output `input_fact_refs` carries the upstream fact's *ref*, not necessarily a byte-for-byte copy of its full content.
- `SwingDistanceFeatureEngine`'s per-`swing_id` confirmation/invalidation tracking (`_SwingConfirmationRecord`/`_SwingInvalidationRecord`) records **every** upstream Swing confirmation/invalidation the engine has seen, including ones that were **never selected** as the eligible Swing for any `FeatureComputed` — such a Swing leaves no trace in Feature's own output history at all, yet the engine needs it to correctly evaluate *future* candles under `feature.md` §9a's 5-step filter/8-criterion order.

**Corrected design:** catch-up is **not** a bespoke state-reconstruction algorithm inverting output facts. Instead, a new owner reconstructs state the same way this module's own `EVID-05(a)`-validated self-contained-replay discipline (`tests/test_replay_isolation.py`, unaffected, unrevisited) already proves the engines behave: construct a **fresh instance** of the relevant engine and **replay the certified, ordered upstream input history** (the same `CandleFact`/`SwingConfirmedFact`/`SwingInvalidatedFact`/`RegimeClassifiedFact`/`RegimeFactInvalidatedFact` sequence, under the subject's own Input Contract) through that engine's **existing, unmodified** `on_*` methods, in `P_run` order (§D), up to the certified catch-up frontier. This requires no new engine-internal reconstruction logic — it reuses the engines' own already-proven determinism.

This is expressed as a bounded `AuthoritativeLineageHistoryProvider` protocol/interface boundary (mirroring the exact discipline already governing this codebase's `input_contract_authority_provider`/`output_event_contract_authority_provider` — required, verified, fail-closed-if-wrong-type constructor dependencies, `authority_resolver.py`/`output_contract_resolver.py`, unchanged) with **two** roles, unified under one interface family rather than two separate abstractions: (1) one-time catch-up — supply the certified, ordered upstream input history for a subject up to a frontier, for fresh-instance replay as above; (2) ongoing operation — supply the certified, not-yet-applied apply-set for a subject at a freshly-certified frontier (§D). **Stated honestly, per instruction:** `publish.py`'s `SequenceAllocator` is explicitly **not**, and is not proposed to become, this provider — its own docstring already states it is "NOT a real event log or broker." No real, durable, cross-process Feature event log exists anywhere in this repository today. **No production-authoritative implementation of this provider exists or is proposed by this design** — genuinely separate, future infrastructure work. A `CATCHING_UP → ACTIVE` transition **fails closed** (stays `CATCHING_UP`, never advances) whenever no such provider is configured or the configured provider cannot prove successful, complete replay — including truthfully for a genuinely brand-new subject with no prior history, which still requires the provider to affirmatively prove "no history exists" rather than being silently assumed from an absent/misconfigured provider.

### D — Deterministic arbitration over a certified complete frontier (`ADR043-IMPLDESIGN-A-MAJ-02` corrected)

**Correction, stated directly:** the prior revision's "reject a fact that violates monotonicity relative to what's already applied" check can *detect* some out-of-order deliveries, but cannot *prove* correct ordering — it is retained below only as a **defensive invariant check**, never the primary correctness mechanism. Processing "whichever event the caller happened to hand the Python method first" is never sufficient, even with that check present.

**Corrected primary mechanism — reuse only already-existing, already-approved machinery, no new ordering authority invented:**

- [`contracts.py`](./src/feature_engine/contracts.py)'s existing `EvaluationFrontier` — already documented as "caller-certified, PROOF-CARRYING" (`recorded_time`, `stream_registry_version`, `lifecycle_frontier`, `stream_positions`, each with proof) — the engine "NEVER constructs `stream_positions`/`lifecycle_frontier` itself." This is, unchanged, exactly the "certified complete input cut/frontier" this correction requires; it is not invented here.
- [`feature-context-architecture.md`](../../docs/architecture/engine/feature-context-architecture.md) §4.6 (v0.6, already Approved-authority-instantiating) already specifies, in full, the certification protocol that *produces* a valid `EvaluationFrontier`: the lifecycle bracket (`L_before`/`L_after` direct synchronous reads of the canonical Lifecycle Stream), the registry-contract equality gate, per-stream direct log reads (never transport/notification-derived), the causal-closure fixed point, and the deterministic discard-and-retry-from-step-1 behavior on a detected lifecycle race. This design invents none of it — the coordinator is simply a *consumer* of a frontier some external caller/orchestrator has already certified this way, exactly as the engines already are today.
- Chapter 8 §8.3.4's `P_stream ∪ P_causation` hard constraints and the subject's own Feature Input Contract `merge_policy.concurrent_tie_break` (unchanged, un-redefined) — already cited, unchanged from the prior revision.

**Corrected per-step algorithm, for each authoritative processing step on a subject:**

1. Obtain/receive an `EvaluationFrontier` already certified by the existing §4.6 protocol (the coordinator does not certify it itself — same non-authority the engines already have today).
2. Query the provider (§C) for the set of authoritative upstream/output events for this subject that are visible within that certified frontier and **not yet applied** (tracked via the coordinator's own `last_committed_frontier` marker — coordinator-owned bookkeeping, not a new authoritative Feature concept, never added to Event Schema).
3. Construct `P_run` over exactly that bounded apply set (§8.3.4, unchanged): per-stream sequence precedence and causation precedence as hard constraints; `merge_policy.concurrent_tie_break` only for events ordered by neither.
4. Deterministic-topologically sort the apply set under that `P_run`.
5. Apply in that derived order, driving the wrapped engine's own unmodified `on_*` methods (the defensive monotonicity check from the prior revision still runs here as a belt-and-suspenders invariant, now checking an already-`P_run`-sorted sequence rather than arrival order).
6. Advance `last_committed_frontier` for this subject **only after** the whole ordered batch is successfully committed (§"Atomicity and emission").

When the received frontier is incomplete for this subject's own Input Contract: defer/buffer according to that Input Contract's own already-authoritative `frontier_policy` (`mechanism`/`completeness_rule`/`late_arrival_behavior`/`buffer_limit_policy`/`incomplete_frontier_behavior`, Chapter 8 §8.3.4, unchanged, values not restated here per this README's own existing SSOT discipline) — or fail closed where that policy requires it. An event is never applied merely because it is the one the Python method received first.

**Required example (explicit, per instruction):**

```text
The applicable Input Contract's own P_run says A precedes B.
The coordinator's on_* method is called with B before A arrives.
B MUST NOT become authoritative merely because it arrived first.
The coordinator does not act on B in isolation: it (re-)certifies the
frontier, computes the current complete not-yet-applied apply set for
the subject, P_run-sorts it -- which places A before B whenever B is
genuinely visible at a valid certified frontier, because a frontier
that includes B's own stream position necessarily reflects A's
already-committed position too (A precedes B in the authoritative log
itself; Chapter 8 §8.3.4 already rejects an append that would violate
this at the authoritative log's own append boundary, upstream of
Feature Engine) -- and applies A, then B, in that derived order.
```

**No global order:** ordering stays local to the applicable Feature Input Contract's own apply set (`P_run`) for one subject's certified frontier — this design does not create, and does not need, a platform-wide total order (unchanged conclusion from the prior revision, now on a corrected mechanism). The competing-successor case (two candidates targeting the same lineage head) remains caught by the engines' own existing, unmodified `FeatureLineageError`/`InvalidSwingEligibilityInputError`, now reached in genuine `P_run` order rather than arrival order.

### E — Existing engine integration (updated — a bounded internal refactor is now required)

- `RegimePassthroughFeatureEngine` / `SwingDistanceFeatureEngine`: **analytical rules unchanged** (lineage validation, eligibility filtering, total-order selection, illegal-transition rejection all stay byte-identical in behavior). **A bounded internal method-shape refactor is required** — see "Atomicity and emission" below; this corrects the prior revision's unqualified "no change" claim, which direct source analysis (below) disproves for the atomicity requirement specifically.
- `CandleWindowFeatureEngine`: structurally covered by the same wrapper (any of the three engine types is wrappable identically), but moot in practice — construction always fails closed today (`UnsupportedFeatureFormulaError`, unrelated, untouched, not reopened).
- `FeatureCurrentView`: explicitly **outside** the ownership boundary, unchanged from the prior revision. Already non-authoritative, fed by an external caller, never wired automatically into any engine — no ownership concept applies to a read-side projection regardless of how many consumers read it.
- `SequenceAllocator`/`publish.py`: **not modified**, but its `next_ref(...)` call site moves — see "Atomicity and emission" below for exactly where.

### Atomicity and emission (new — resolves `ADR043-IMPLDESIGN-A-MAJ-01`'s atomicity concern)

**Direct source analysis, this transaction:** today, `SwingDistanceFeatureEngine._emit_original`/`_emit_replacement_only`/`_invalidate_and_replace` (and `RegimePassthroughFeatureEngine`'s equivalent `_emit_*` methods) call `self._allocator.next_ref(...)` **and** mutate `self._lineage[key] = ...` **together, in one synchronous method**, with no seam between them. If fencing were discovered stale only *after* such a call returns, a real sequence would already be consumed and `_lineage` already mutated under a stale generation — an illegitimate partial commit, and (per Chapter 8 §8.3.2) a **sequence gap** the moment that consumed-but-invalid ref is discarded. This is exactly the failure mode `ADR043-IMPLDESIGN-A-MAJ-01` identified; the prior revision's "no engine change needed" claim did not hold against it.

**Corrected boundary — a bounded prepare/commit split, design-level only, not implemented by this transaction:**

```text
1. validate current fenced generation           (§B, "before beginning")
2. derive the certified P_run-ordered apply set  (§D)
3. compute PROPOSED transition(s)                (engine logic UNCHANGED;
                                                   candidate FeatureComputed/
                                                   FeatureFactInvalidated value
                                                   + candidate lineage delta
                                                   computed WITHOUT calling
                                                   next_ref() and WITHOUT
                                                   mutating self._lineage yet)
4. revalidate fencing/current generation         (§B, the true last safe point,
                                                   against SubjectOwnershipAuthority)
5. allocate sequence + finalize event ref         (next_ref(...) now, only
                                                   if step 4 passed)
6. commit local owner state: apply the lineage
   delta to self._lineage, advance
   last_committed_frontier                       (only after step 5)
```

If step 4 fails: the attempt is discarded in full — **no** `next_ref()` call occurs, **no** `_lineage` mutation is applied, **no** frontier advance occurs. No sequence gap is created, because no sequence was ever allocated for the discarded attempt — Chapter 8's contiguous-sequence requirement is preserved by construction, not by cleanup. Steps 3–6 execute within one synchronous, single-threaded coordinator call (this codebase has no threading/asyncio anywhere — confirmed, unchanged), so within *this* process the sequence above is effectively atomic; the genuine cross-process atomicity requirement this exposes — durably and atomically persisting steps 5–6 together once a real distributed store backs `SequenceAllocator`'s eventual replacement — is production infrastructure this design does not select or implement, exactly as §C already discloses for catch-up.

**Required engine-internal refactor (documented, not implemented):** `regime_passthrough.py`'s and `swing_distance.py`'s `_emit_*` methods must be split into a candidate-computation phase (step 3, no `next_ref`/`_lineage` mutation) and a separate commit phase (steps 5–6) the coordinator drives only after step 4 passes. The engines' own analytical decisions (which transition is legal, what value to compute, which head is superseded) are computed identically either way — only the *point* at which a sequence ref is allocated and `_lineage` is mutated moves, from "inside one fused call" to "after the coordinator's last-safe-point fencing recheck."

**Proposed new/changed source files (identified only, not implemented by this transaction):**

```
src/feature_engine/ownership.py   SubjectOwnershipState (INACTIVE/CATCHING_UP/
                                   ACTIVE/REVOKED), OwnerHandle (subject_id,
                                   generation, state), SubjectOwnershipRegistry
                                   (process-local, NOT sufficient authority alone),
                                   SubjectOwnershipAuthority (Protocol -- external,
                                   durable, exclusivity-proving; no technology
                                   selected), AuthoritativeSubjectOwner (coordinator:
                                   drives the §D certified-frontier algorithm;
                                   drives the prepare/commit split above; re-validates
                                   fencing at both last-safe points per §B)
src/feature_engine/regime_passthrough.py,
src/feature_engine/swing_distance.py
                                   (bounded, behavior-preserving refactor) split
                                   existing _emit_* methods into candidate-compute
                                   (no next_ref/_lineage mutation) vs. commit
                                   (next_ref + _lineage mutation) phases, per
                                   "Atomicity and emission" above -- analytical
                                   rules unchanged
src/feature_engine/errors.py      (extended, not replaced) new named fail-closed
                                   exceptions: e.g. StaleOwnershipGenerationError,
                                   DualOwnershipError, OwnershipAuthorityUnavailableError,
                                   UnprovenCatchUpError, NonMonotonicApplicationOrderError,
                                   IncompleteCertifiedFrontierError
```

`application_order.py` is deliberately **not** introduced as a separate file — the §D algorithm is small enough to live inside `ownership.py`'s `AuthoritativeSubjectOwner`; splitting it out now would be aesthetic, not necessary, per instruction. No change proposed to `candle_window.py`, `current_view.py`, `publish.py`, `contracts.py`, `authority_resolver.py`, `output_contract_resolver.py`, `replay_preparation.py`, `identity.py`, or `envelope.py`.

### F — Failure semantics (fail closed, no speculative authoritative output)

- Unknown owner (no registry entry / never acquired) → rejected.
- Stale fencing generation, detected at either last-safe point (§B) → rejected; if detected at the post-computation safe point (step 4 above), the computed candidate is discarded with zero effect (no sequence consumed, no mutation, no frontier advance).
- Dual-owner ambiguity for one subject → structurally prevented by `SubjectOwnershipAuthority`'s own atomic-acquisition guarantee (§B); if ever detected regardless (e.g. an internal invariant check), that subject scope fails closed, never a runtime-selected "winner."
- `SubjectOwnershipAuthority` unreachable/unconfigured in an authoritative-production context → fails closed; never silently falls back to local-registry-only fencing (§B).
- Failed/incomplete catch-up, including an upstream-history provider that cannot prove complete replay (§C) → stays `CATCHING_UP`, never reaches `ACTIVE`; no emission possible.
- Certified frontier incomplete for this subject's Input Contract → defer/buffer per that contract's own `frontier_policy`, or fail closed where the policy requires (§D).
- Inability to derive deterministic precedence within a certified apply set (no `P_stream`/`P_causation` relation and no Input Contract tie-break resolves two events) → the batch is rejected, not guessed.
- Handoff interrupted between revoke and activation (e.g. process crash mid-handoff) → the subject is left with **no** `ACTIVE` owner; fails closed for all further attempts until a fresh acquisition completes catch-up from scratch. Blast radius is scoped to the one affected `feature_subject_id` — consistent with [I-6](../../docs/constitution/02-platform-invariants.md) Fail-Safe by Scope, never a platform-wide halt.

### G — Replay / non-authoritative modes

Replay/backtest/shadow/simulation execution **never** calls into `SubjectOwnershipRegistry`/`SubjectOwnershipAuthority`/`AuthoritativeSubjectOwner` — it constructs and drives the analytical engines directly, exactly as `EVID-05(a)`'s already-validated self-contained-replay tests (`tests/test_replay_isolation.py`) already do today, unaffected and unrevisited by this design. Owner identity/generation is pure execution-control metadata; it is never serialized into `FeatureComputed`/`FeatureFactInvalidated` and never added to Feature Event Schema (`ADR-043` semantic 6, unchanged). Because catch-up (§C) and ongoing processing (§D) both strictly apply events in `P_run` order derived from already-certified, already-authoritative structure, and owner identity never enters event content, replaying identical authoritative history through the same, unmodified analytical engines reproduces the identical result regardless of which owner/generation originally produced it — an unchanged property of the existing pure, deterministic engines.

### H — Handoff lifecycle

Smallest sufficient state machine, one instance per `(feature_subject_id, ownership_generation)` — unchanged from the prior revision; correction found no need for another state:

```
INACTIVE → CATCHING_UP → ACTIVE → REVOKED
```

- `INACTIVE → CATCHING_UP`: on an acquire request, only when `SubjectOwnershipAuthority` (§B) grants a new generation for that subject (no other `ACTIVE`/`CATCHING_UP` generation currently recognized).
- `CATCHING_UP → ACTIVE`: only after the corrected §C replay-based catch-up proves complete; otherwise stays `CATCHING_UP` (fail closed, §F).
- `ACTIVE → REVOKED`: an explicit, single-step revoke against `SubjectOwnershipAuthority`, always performed before a new acquisition for the same subject may begin its own `CATCHING_UP` (§B).
- `REVOKED` is terminal for that generation; any call against a revoked handle fails closed. No separate "draining" state — this codebase's engine calls are synchronous and single-threaded (no in-flight concurrent work exists to drain), and `ADR-043` does not itself require one.

### ADR Scope conflict check (explicit, per instruction)

This corrected design still introduces no new module, no dependency-graph edge, no Event Schema change, no Chapter 8 change, and no cross-module authority change — confirmed directly against the corrected shape above, including the engine-internal `_emit_*` refactor (a behavior-preserving method-shape change inside the already-registered `feature-engine` module, not a new module or contract). `AuthoritativeLineageHistoryProvider` and `SubjectOwnershipAuthority` are **not** new authoritative sources: the former is a bounded read-side/replay boundary onto the *already*-authoritative Feature event stream `feature-engine` already holds sole writer authority over (`stream-registry.yaml`, unchanged); the latter is a bounded exclusivity-proving boundary realizing `ADR-043`'s own already-decided per-subject-ownership semantic, not a competing domain-truth source. No production implementation of either exists or is proposed here (§B/§C). No STOP condition is triggered.

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
