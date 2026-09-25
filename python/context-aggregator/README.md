# context-aggregator

Context deterministic aggregation core (`docs/domain/context.md`).
`module_id: context-aggregator` per `docs/architecture/module-registry.yaml`
— **Type-2 Projection**, `owns_authoritative_state: false`. Implementation
language (Python) resolved in this build transaction as the unambiguous
application of [ADR-008](../../docs/adr/ADR-008.md)'s layer-level pin
(Python for core analytical/decision-support logic that owns no external
side effect/venue I/O/risk-control/execution boundary) to this module's
`implements_capabilities: [context-aggregation]` registry entry
(`docs/engineering/monorepo.md` §4) — `ADR_NOT_REQUIRED`, no new ADR
created.

This is the **deterministic Context aggregation core only** — no runtime/
event-log integration, no stream-frontier capture, no Input Contract
authority resolution, no output Event Contract publication, no Strategy/
Decision integration, no Quality-Gate closure. See "What this slice does
not implement" below for the exact list of deliberately open gaps.

## What this module owns (this slice)

- `aggregate_context_candidate` (`aggregation.py`) — the public entrypoint.
  Given, per role, an already cursor-visible candidate-fact set, it selects
  the Eligible Upstream Fact for each of the seven required roles
  (context.md §8's exact two-phase pipeline), enforces exact seven-role
  cardinality with a fail-closed `None` result on any gap (§9), and
  assembles an **eligible cursor-bounded Context aggregation candidate**
  (`ContextAggregationCandidate`, `values.py`) by copying upstream values
  verbatim (§17) — never recomputing Structure/Regime/Feature semantics.
- `ContextSubjectScope`/`context_subject_id` (`scope.py`) — the five-field
  qualifying scope and its deterministic opaque subject identity (§1).
- `ContextDefinition` (`definition.py`) — the bounded definition-version-pin
  representation this core needs (§6); explicitly not a registry.
- Module-local consumer-side evidence views (`evidence.py`) for exactly the
  seven upstream fact roles (§7): Candle cutoff/cadence source, Structure,
  the two Regime dimensions, the three founding Feature types.
- The exact two-phase Eligible Upstream Fact selection pipeline
  (`selection.py`): Phase 1 per-candidate eligibility filtering (identity/
  scope match, required definition-version match, effective-time cutoff,
  role-specific validity-at-cursor), Phase 2 role-specific current
  selection (Structure: max `recorded_time`; Regime/Feature: lineage head),
  and the shared seven-criterion total-order tie-break — plus §10's
  canonical input-fact normalization.

## Terminology — "eligible cursor-bounded candidate", never "authoritative"

`ContextAggregationCandidate` is **not** a published `MarketContextSnapshot`
event. Per `feature-context-architecture.md` §5.2/§13's terminology
correction, this core's own result is called an **eligible cursor-bounded
Context aggregation candidate** — the record-integrity properties
(immutable, cursor-bounded, lineage-preserving, eligible per §8) this core
can and does guarantee. It never claims to be the authoritative Chapter 8
§8.2 event envelope (a genuine `event_id`/`event_contract_ref`/`stream_ref`/
`producer_ref`/`sequence`/`causation_refs`), because `context-aggregator`
owns no such publishing authority yet
(`owns_authoritative_state: false`). This is the same non-blocking open
gap `feature-context-architecture.md` §13 documents between context.md's
own envelope framing and module-registry.yaml's Projection classification
— **preserved here unresolved, not decided by this slice.**

## Explicit visibility/frontier boundary (Boundary D)

`aggregate_context_candidate`'s public entrypoint accepts, per role, an
input set whose facts are explicitly supplied as **already cursor-visible**
by the caller — this core does **not** calculate or self-certify runtime
stream visibility (context.md §8 Phase 1 step 2, §14(a)). Cursor-visibility
qualification is an external prerequisite established by a future
orchestration/frontier layer, not by this module — re-deriving it here
would require inventing stream-position/frontier semantics this module does
not own (`feature-context-architecture.md` §13, still open), and would
reduce Chapter 8 cursor visibility to a scalar `recorded_time` test, which
context.md §14 explicitly treats as only one of two independent required
conditions.

Every other locally-resolvable Context-owned predicate **is** enforced by
this core: identity/scope match, required definition-version match,
effective-time/cutoff eligibility (inclusive, no look-ahead), role-specific
validity via the supplied invalidation/lineage evidence, exact role
cardinality, deterministic role-specific winner selection, and deterministic
canonical normalization.

## What this slice does not implement

- **No Input Contract** — Context has no Context-scoped Input Contract yet.
- **No Event Contract** — Context's own output Event Contracts for
  `market-context-snapshot`/`market-context-fact-invalidated` are not
  governed/published; no upstream Event Contract is authored here either.
- **No runtime `stream_ref`/`producer_ref`/publishing** — this core never
  fabricates a `producer_ref`, `stream_ref`, authoritative `sequence`, or
  `causation_refs`. Binding a candidate to a real Chapter 8 §8.2 envelope is
  a later, separate, governed publishing slice.
- **No stream-registry frontier capture** — `stream-registry.yaml`'s own
  gap for Context's `producer_ref`/`stream_ref` resolution
  (`feature-context-architecture.md` §13) is unchanged by this slice.
- **No concrete `context_definition_version` registry/storage mechanism**
  — the caller supplies an already-resolved `ContextDefinition` value.
- **No Quality Tier / Quality-Gate PASS** — `context-aggregator`'s
  `quality_tier` remains unresolved after this transaction; no formal
  Chapter 13 Quality Gate result is claimed here.
- **No Strategy/Decision/Risk/Execution work** — `context_values` never
  contains signal strength, setup quality, bias, buy/sell/hold, entry/stop/
  target, position size, strategy id, or account state (context.md §17;
  enforced structurally by `test_context_values_has_no_strategy_decision_
  risk_execution_fields` in `tests/test_aggregation.py`).

## Independence from other Python modules

Independent from `structure-engine`/`raw-regime-engine`/`feature-engine`'s
own Python packages — this package never imports any of them
(`identity.py`'s module docstring; enforced directly by
`tests/test_boundaries.py::test_no_imports_of_producer_implementation_
packages` on the committed source tree). `module-registry.yaml`'s
`depends_on: [market-data-ingestion, structure-engine, raw-regime-engine,
feature-engine]` is a permitted event/contract relationship
(`feature-context-architecture.md` §2), never a license to import another
module's implementation package — this package defines its own
consumer-side `evidence.py` views of those contracts instead.

## Determinism guarantees this core enforces (and tests)

- No wall-clock domain decision anywhere in the deterministic core
  (`test_no_wall_clock_domain_decision`).
- No runtime network/filesystem dependency in the deterministic core
  (`test_no_runtime_network_or_filesystem_dependency`).
- Numerical Context values (`volatility_metric`,
  `directional_persistence_metric`, `distance_to_last_confirmed_swing`) are
  preserved exactly as `Decimal` — never round-tripped through `float`
  (`test_decimal_value_preserved_without_float_round_trip`,
  `test_no_float_round_trip_of_decimal_values`).
- Raw `sequence` is never compared across two different streams as a global
  order (`test_cross_stream_sequence_never_used_as_global_order`).
- The same seven evidence facts, delivered in any incoming order, normalize
  to the identical computation identity (`test_incoming_order_independence`).
