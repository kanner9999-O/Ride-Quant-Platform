---
id: feature-engine-chapter13-remediation-plan-001
title: "Feature Engine Chapter 13 Remediation Plan #001 — the six blocking EVID findings"
plan_version: "1.0"
plan_status: PLANNING ONLY — NOT AN IMPLEMENTATION TRANSACTION
performed_at: "2026-09-04"
evaluated_boundary: "2d6ab4040a9f48f59d8dd92b875b32dff159adee"
---

# Feature Engine Chapter 13 Remediation Plan #001

**STATUS: PLANNING ONLY. No test/code/tooling implemented. No mutation testing or
Quality Gate rerun. No threshold semantics changed. No finding closed. Feature
Engine not approved. Phase 3 gate not opened. LIVE not authorized.**

This plan addresses the six currently blocking Feature Engine Chapter 13
findings: `P3-FEATURE-QG-EVID-03` through `P3-FEATURE-QG-EVID-08`. It resolves
each dimension's authority directly from the repository (Chapter 2 invariant
text, Chapter 13, Testing Convention v0.16, the original formal QG evidence
and its later corrections, the Step-4 mutation analysis, the Step-9 evidence
and its correction, and current Feature Engine source/tests) rather than
restating prior transactions' prose uncritically — two factual corrections
made during this planning pass are noted explicitly in §1.

## 0. Preserved lifecycle state (unchanged by this plan)

```text
TEST_EFFECTIVENESS_THRESHOLD: EFFECTIVE (87.001959503592% raw AND 170/170
  material-gap identity resolution, Tier-1/FEATURE-ENGINE-ONLY) — unchanged.
P3-FEATURE-QG-EVID-03 through -08: OPEN / blocking — unchanged, none closed
  by this plan.
Overall Feature Engine Chapter 13 Quality Gate: FAIL — evidence — unchanged.
P3-PY-MUT-THRESH-A-MIN-02: OPEN — MINOR / NON-BLOCKING — unchanged.
Feature Engine approval: NOT APPROVED. Phase 3 Approval Gate: NOT OPENED.
LIVE: NOT_AUTHORIZED.
```

## 1. Six-row blocker matrix

| Finding | Dimension | Classification | Exact gap | Dependency | Closure condition |
|---|---|---|---|---|---|
| `EVID-03` (raw score / 170 IDs) | Test-effectiveness — mutation score & material-gap identities | **ACTIONABLE_NOW** | 0/170 pinned material-gap mutants killed; raw score 75.898105813194% < 87.001959503592% | None — ordinary test-writing against already-identified, already-cited mutant IDs | A fresh Step-9-style formal measurement shows raw score ≥87.001959503592% **and** all 170 pinned identities individually killed/confirmed_timeout or governedly reclassified (proposal §4.1) |
| `EVID-03` (12-method blind spot) | Test-effectiveness — mutation-surface completeness | **NEEDS_GOVERNED_DESIGN_OR_MECHANISM** | 5 high-materiality methods structurally outside mutmut 3.7.0's mutation surface; no qualifying supplemental mechanism/fault-injection/risk-acceptance evidence exists | A governed decision on which of three paths to pursue (Testing Convention v0.16 §5c) | One of: (a) an accepted supplemental mutation-testing mechanism reaching decorated classes now exists; (b) governed deterministic fault-injection evidence is authored and pinned per method; (c) Product Owner explicitly records risk-acceptance naming the 5 residuals |
| `EVID-04` | I-2 Decision Parity / Tier-1 Parity Test | **BLOCKED_BY_EXTERNAL_DEPENDENCY** | I-2's own Verification (golden event-log test, canonical semantic-decision hash comparison across all 4 execution modes at the **Decision** layer) cannot be performed — no Decision Engine/Strategy Plugin Host exists anywhere in the repository (confirmed: `python/`, `go/` contain only feature-engine, raw-regime-engine, structure-engine, market-data-ingestion, market-reference-service) | Decision Engine + a parity harness (Chapter 14 §14.2 sequence) | Decision Engine exists and a parity harness reproduces the same canonical Decision hash across Replay/Backtest/Paper/Live for a real scenario touching Feature Engine's own output |
| `EVID-05` | I-5 Decision-Time Observable Dependency | **NEEDS_GOVERNED_DESIGN_OR_MECHANISM** (split — see §2) | (a) no self-contained-replay test proves `on_candle`/`on_swing_confirmed`/etc. never re-touch the filesystem after construction-time authority resolution; (b) `ComputationCursor` carries `input_contract_ref`/`stream_registry_version` (identity/version strings) but no content-identity **checksum** referenced from the event, so I-5's "checksum của mọi artifact phải khớp" clause is structurally unverifiable today | (a) none — test-only, exercises already-existing cached-authority design; (b) a schema/design decision — plausibly an Event-Schema-adjacent change requiring a **fresh Chapter 0 §4b run** | (a) a self-contained replay test passes with network/filesystem cut after materialization; (b) either `ComputationCursor` (or an equivalent persisted-evidence mechanism) carries a verifiable content-identity checksum, checked against the resolved authority at replay time |
| `EVID-06` | I-6 Fail-Safe by Scope | **NEEDS_GOVERNED_DESIGN_OR_MECHANISM** (interpretation sub-step now **RESOLVED**, §9 — fault-injection tests/formal evidence still not authored) | I-6's actual Verification is fault injection per scope + blast-radius confirmation + a risk-not-increased assertion "theo risk metric/policy authoritative" — Feature Engine (a pure Compute Engine, no risk/exposure semantics of its own) has no resolved interpretation of how "risk-not-increased" applies to it at all | ~~A design/interpretation decision (likely affecting every Compute-Engine-class module identically — structure-engine, raw-regime-engine, feature-engine — so plausibly `ADR_REQUIRED` under Chapter 0 §4b's ">1 module" trigger)~~ **CORRECTED (§9, this transaction):** the interpretation is fully derivable, Feature-Engine-only, from already-Locked authority (I-6 itself + I-9's own Scope boundary line + already-approved ADR-043 + already-Locked feature.md subject identity) — **`ADR_NOT_REQUIRED`**, not `ADR_REQUIRED`; the old ">1 module" assumption was never verified against source and does not hold once actually derived. Genuine fault-injection tests (not merely exception-raising unit tests) still need authoring — see §9's evidence-matrix design. | The interpretation decision is recorded (§9, this transaction), then genuine fault-injection tests (not merely exception-raising unit tests) are authored per applicable scope with blast-radius and risk-not-increased assertions — **not performed by this transaction** |
| `EVID-07` | I-13 State Transition Integrity / property-based evidence | **NEEDS_GOVERNED_DESIGN_OR_MECHANISM** | No Python property-based testing framework is approved or installed anywhere in the repository (confirmed: zero "hypothesis" references in `testing.md` or any `pyproject.toml`) — I-13's Verification explicitly requires "Property-based test trên transition graph authoritative" | A full governed mechanism-selection sequence, mirroring Testing Convention v0.16's own already-completed mutmut precedent (candidate authoring → Review A/B → Product Owner decision → install/pin → measurement) | A property-based framework is Approved, installed, pinned, and produces transition-graph/illegal-transition/concurrent-transition/replay-reconstruction evidence for Feature Engine's own state-machine entities (e.g. `_WindowLineage`'s VALID/PENDING_CORRECTION lifecycle, `FeatureCurrentView`'s row lifecycle) |
| `EVID-08` | I-1 Explainability / Decision-Pipeline trace completeness | **BLOCKED_BY_EXTERNAL_DEPENDENCY** | I-1's Verification requires 100% trace-completeness across "Toàn bộ Decision Pipeline (Structure/Regime/Feature → Strategy → Decision → Risk Gateway → Execution)" — Strategy/Decision/Risk Gateway/Execution Engine are all unbuilt | Full Decision/Risk/Execution evidence path (superset of EVID-04's own dependency) | The complete pipeline exists and produces production Decision/Risk Action evidence; Feature-local causation evidence (`causation_refs`, `input_fact_refs`, `computation_cursor`) already exists and is preserved as supporting-only evidence, never sufficient alone |

## 2. Two evidence-fidelity corrections made during this planning pass

Freshly re-verifying each finding's factual premise against current repository
state (not restated uncritically) surfaced two corrections, neither of which
changes any finding's `FAIL — evidence` disposition:

1. **`EVID-06`'s "zero test coverage" premise is now stale.** Direct
   inspection of `tests/test_current_view.py`, `tests/test_regime_passthrough.py`,
   and `tests/test_swing_distance.py` shows all 4 `ForeignScopeError` raise
   sites now DO have ordinary example-based coverage
   (`test_foreign_scope_event_rejected`, `test_foreign_scope_regime_fact_rejected`,
   `test_foreign_scope_candle_rejected`, `test_foreign_scope_swing_confirmed_rejected`
   — added, per their own code comments, as branch-coverage remediation for
   `P3-FEATURE-QG-COV-01`, explicitly self-documented as "factual overlap
   only, not a claim of EVID-06 closure"). This does not close EVID-06 — per
   the already-recorded I-6 clarification, ordinary exception-raising tests
   are supporting evidence only; the actual fault-injection/blast-radius/
   risk-not-increased Verification remains entirely unaddressed — but the
   blocker-matrix row above states the CURRENT gap precisely (interpretation
   + fault-injection design) rather than repeating the outdated "zero
   coverage" framing.
2. **`EVID-05`'s dependency is confirmed real by direct code reading, not
   assumed.** `ComputationCursor` (current_view.py/contracts.py-adjacent
   structures) was independently checked: it carries `input_contract_ref`
   (an `{contract_id, contract_version}` identity pair) and
   `stream_registry_version` (a version string) — genuinely no
   content-identity checksum field. `VerifiedInputContractAuthority` DOES
   compute `input_contract_content_id`/`stream_registry_content_id`
   checksums at resolution time, but they are not threaded into the
   persisted, replay-relevant cursor. This confirms the finding's own
   "Required follow-up" text and justifies classifying part (b) as a
   genuine schema-adjacent design gap, not merely a missing test.

## 3. Dependency graph / critical path

```text
EVID-03(a) raw score/170 IDs  ──────────────────────────────▶ [independent, ACTIONABLE_NOW]
EVID-03(b) blind-spot path decision ──▶ blind-spot evidence authored ──▶ [independent]
EVID-05(a) self-contained replay test ────────────────────────▶ [independent, ACTIONABLE_NOW]
EVID-05(b) checksum/schema design ──▶ fresh SS4b run ──▶ implementation ──▶ replay-checksum test ──▶ [independent]
EVID-06 risk-model-applicability interpretation (RESOLVED §9, ADR_NOT_REQUIRED) ──▶ fault-injection test design (§9, this transaction) ──▶ tests ──▶ [independent]
EVID-07 property-based mechanism candidate ──▶ Review A/B ──▶ PO decision ──▶ install/pin ──▶ tests ──▶ [independent]

EVID-04 Decision Parity  ◀── BLOCKED ── Decision Engine + Strategy Plugin Host must exist (Chapter 14 SS14.2) ── external, outside Feature Engine's own remediation scope
EVID-08 I-1 trace completeness ◀── BLOCKED ── Decision Engine + Risk Gateway + Execution Engine must ALL exist (superset of EVID-04's dependency) ── external, longest pole
```

**Critical path:** `EVID-08` has the longest, strictly-superset external
dependency (Decision Engine **and** Risk Gateway **and** Execution Engine);
`EVID-04` depends on a subset of that same chain (Decision Engine alone,
plus a parity harness). Neither can be shortened by any action internal to
Feature Engine. The four remaining findings (`EVID-03`, `EVID-05`, `EVID-06`,
`EVID-07`) are **mutually independent** of each other and of `EVID-04`/`EVID-08`
— none blocks or is blocked by any other.

## 4. Ordered remediation sequence

1. **Immediately, in parallel:** `EVID-03(a)` (material-gap test additions)
   and `EVID-05(a)` (self-contained replay test) — both `ACTIONABLE_NOW`,
   zero design prerequisites, zero cross-dependency.
2. **In parallel with step 1, as separate governed transactions:** initiate
   the design/decision work for `EVID-03(b)` (blind-spot path selection),
   `EVID-05(b)` (checksum/schema design — must rerun Chapter 0 §4b fresh
   before any implementation), `EVID-06` (risk-model-applicability
   interpretation — **RESOLVED §9, this transaction: `ADR_NOT_REQUIRED`,
   not the previously-assumed likely `ADR_REQUIRED`** — proceed directly
   to fault-injection test design/authoring, no ADR/Review-B/PO-decision
   step in between), and `EVID-07` (property-based mechanism candidate
   authoring, mirroring the mutmut precedent's own Step 1 candidate stage
   — since resolved: `P3-FEATURE-QG-EVID-07` is now `CLOSED — PASS`).
   These four are independent efforts that can proceed on separate tracks
   without contention.
3. **Once each design/decision from step 2 resolves:** author the
   corresponding tests/implementation for that specific finding, then a
   dedicated formal evidence transaction for that dimension (mirroring the
   Step-9 pattern already established for EVID-03).
4. **`EVID-04`/`EVID-08`:** do not start. Track as externally blocked (see
   §5's stop/unblock conditions). Revisit when Phase 3's Decision Engine
   (and, for EVID-08, Risk Gateway/Execution Engine) build reaches a point
   where a parity harness / trace-completeness evidence transaction becomes
   feasible — this is a Phase-3-sequencing question, not a Feature-Engine
   remediation task.

## 5. Parallelizable work

`EVID-03(a)`, `EVID-03(b)`-design, `EVID-05(a)`, `EVID-05(b)`-design,
`EVID-06`-interpretation, and `EVID-07`-candidate can all be worked
**simultaneously** by separate governed transactions — none reads or writes
state the others depend on. The only sequencing constraint within each
finding is design-before-implementation-before-formal-evidence (steps 2→3
above); there is no cross-finding sequencing constraint among these six.

## 6. Explicit stop/unblock conditions for externally-blocked items

```text
EVID-04 — STOP condition (do not attempt now): no Decision Engine or
  Strategy Plugin Host exists in this repository.
  UNBLOCK condition: Decision Engine reaches a state where it can process a
  real event log end-to-end AND a parity test harness exists comparing
  canonical Decision hashes across Replay/Backtest/Paper/Live.
EVID-08 — STOP condition (do not attempt now): Strategy/Decision/Risk
  Gateway/Execution Engine are all unbuilt.
  UNBLOCK condition: the full Decision/Risk/Execution evidence path exists
  AND produces real production Decision/Risk Action traces that a
  Chapter-2 I-1 100%-trace-completeness verification can be run against.
  This is a STRICT SUPERSET of EVID-04's own unblock condition -- EVID-08
  cannot unblock before EVID-04 does.
```

Neither condition is evaluated as met or attempted-toward by this plan.

## 7. Explicitly NOT recommended

Per this task's own instruction, and consistent with Testing Convention
v0.16's own anti-gaming discipline: this plan does **not** recommend
weakening the approved 87.001959503592% / 170-identity threshold merely
because Feature Engine currently fails it, does not recommend substituting
same-process determinism for `EVID-04`'s genuine cross-execution-mode parity
requirement, and does not recommend closing `EVID-06` via a
`ForeignScopeError` unit test alone (per §2's correction, such tests already
exist and are already, correctly, recorded as insufficient).

## 8. Single best next governed transaction

**Recommended: a bounded, test-only remediation transaction for `EVID-03(a)`**
— closing as many of the 170 pinned material-gap mutant identities as
possible, prioritized by the Step-4 analysis's own duplication data: **22 of
the 30 functions containing material-gap mutants each contain ≥2, together
covering 162 of the 170 (95%)** — independently re-verified during this
planning pass. The top concentrations: `SwingDistanceFeatureEngine._recompute`
(18), `._invalidate_and_replace` (16), `RegimePassthroughFeatureEngine.
_emit_replacement` (15), `._emit_invalidation` (13), `FeatureCurrentView.current`
(12), `SwingDistanceFeatureEngine._emit_replacement_only` (12). A disciplined
test-writing pass targeting these ~20-30 functions (not 170 independent
efforts) is expected to close the large majority of the 170, followed by a
fresh Step-9-style formal measurement to confirm.

This is the recommended next transaction because it is the only blocker that
is (a) fully `ACTIONABLE_NOW` with zero design/mechanism/ADR prerequisite,
(b) already has an exact, repository-pinned target list (the 170 mutant IDs
in `feature-engine-mutation-baseline-001-analysis.md` §1.6), and (c) directly
moves the one dimension with an already-approved, already-EFFECTIVE numeric
gate — no other blocker has a comparably concrete, immediately-startable
scope.

## 9. `EVID-06` applicability / fail-safe design interpretation (this transaction)

**Vai trò: `Feature Engine EVID-06 Applicability / Fail-Safe Design Executor`.** Resolves ONLY the semantic/applicability question needed to make `EVID-06` testable — does NOT write fault-injection tests, does NOT close `EVID-06`, does NOT author an ADR, does NOT modify production code/Constitution/Domain Contract/Risk semantics. Fresh authority read this transaction (superseding this plan's own earlier, unverified ">1 module → likely `ADR_REQUIRED`" guess at the §1 row/§4 step-2 text above, now struck through and corrected in place): `docs/constitution/02-platform-invariants.md` I-6 (§112-126) and I-9 (§158-172, specifically its Scope line); `docs/constitution/13-quality-gates.md` §13.2/§13.4-13.6 (Tier 1, I-6 evidence row, Chaos/fault-injection category trigger); `docs/constitution/07-module-taxonomy.md` §I-6 cross-reference (line 79); `docs/domain/feature.md` (subject/scope identity, existing fail-closed discipline already present at §4/replay-preparation); `docs/architecture/module-registry.yaml` (`feature-engine` entry, `quality_tier: Tier 1`, `depends_on`); `python/feature-engine/README.md`; `python/feature-engine/src/feature_engine/{errors.py, ownership.py, regime_passthrough.py, swing_distance.py, current_view.py, authority_resolver.py}` (full read); `python/feature-engine/tests/{test_ownership.py, test_regime_passthrough.py, test_swing_distance.py, test_current_view.py}` (representative fault-path tests); `docs/adr/ADR-043.md` (no I-6/fail-safe language present — checked, not assumed); grep across every ADR/architecture doc for "I-6"/fail-safe/degraded-mode/risk-boundary authority (no Feature-Engine-specific or Compute-Engine-class-wide fail-safe ADR exists anywhere in the repository).

### 9.1 Key Question 1 — is existing authority sufficient?

**Yes.** No new authority is created or required by this interpretation; `no new authority → no ADR` applies. The interpretation is a direct, single-module reading of ALREADY-Locked text:

- I-6 itself (Chapter 2, Locked) is self-scoping: `Scope: Mọi Compute Engine, Projection, Runtime Service` — Feature Engine (`module_type: compute_engine`, `module-registry.yaml`) is directly, unambiguously in scope. No new invariant text is needed to establish applicability.
- I-9's own Scope line (Chapter 2, Locked) already draws the exact boundary this finding needs: *"ranh giới (boundary) giữa Feature Engine (analytical float được phép) và Execution/Ledger (bắt buộc lossless decimal từ đầu đến cuối)"* — i.e. Constitution itself already states, in already-Locked text, that Feature Engine's outputs are analytical (pre-financial), not financial/risk values. This single line resolves most of Key Question 3 without inventing anything.
- `feature.md` (Domain Contract) already declares Context snapshot / trade signal / action recommendation / entry-exit setup **out of scope by domain definition** (§"Out of scope theo ranh giới domain") — adding any risk semantics to Feature Engine would violate its own already-Locked Domain Contract boundary, not merely be unnecessary.
- `feature.md` already defines `feature_subject_id` as the domain's own smallest independent identity/isolation unit, explicitly: *"Hai Feature subject trên cùng instrument nhưng khác `venue_id` hoặc `timeframe` là hai subject **độc lập hoàn toàn**."* This is existing Domain Contract authority, not invented for this transaction.
- ADR-043 (Approved, v0.2) already establishes the per-subject ownership/fencing/catch-up architecture; its implementation (Review A CLEAN, README) already fails closed at ~30 identified fault points, all BEFORE any authoritative append (confirmed by direct source read — see §9.4).
- `module-registry.yaml` already confirms Feature Engine has **no** `depends_on` edge toward Risk Gateway/Execution Engine/Decision Authority Service — it is strictly upstream of any risk-bearing module, consuming only `market-data-ingestion`/`structure-engine`/`raw-regime-engine`.
- The remediation plan's own `EVID-04`/`EVID-08` findings (unchanged by this transaction) already confirm, as an independently-established repository fact, that **no Decision Engine, Risk Gateway, or Execution Engine exists anywhere in this repository yet** — so there is structurally no "authoritative risk metric/policy" reachable from Feature Engine to consult, today, by construction.

None of the above required a new decision, a new cross-module contract, or an edit to any Locked document — every fact was already present. The old plan's ">1 module, likely `ADR_REQUIRED`" framing (§1/§4, corrected above) was an unverified assumption made before any of this was actually read; it does not survive contact with the source. No genuine architecture/authority gap exists — two or more materially different valid behaviors are NOT possible under current authority; the interpretation below is the unique reading current authority implies.

### 9.2 Key Question 2 — safe-state interpretation for Feature Engine

The task's own candidate formulation is verified against source, not accepted blindly, and matches ALREADY-implemented behavior almost exactly:

```text
When correctness cannot be proven for one Feature scope:
  fail closed for NEW authoritative Feature transitions in that scope
    (never emit a FeatureComputed/FeatureFactInvalidated built on
    unverified/unprovable state)
  do not fabricate/fallback/guess
    (no error class below ever substitutes a default/guessed value;
    every one raises instead)
  do not advance authoritative Feature state/frontier
    (StaleOwnershipGenerationError: "no sequence consumed, no event
    appended, no local _lineage mutated"; UnprovenCatchUpError: a
    CATCHING_UP -> ACTIVE transition fails closed instead of advancing;
    CanonicalHistoryMismatchError: catch-up fails closed rather than
    preferring either candidate)
  preserve already-committed history
    (every fail-closed check below runs BEFORE mutation/append -- never
    a rollback of already-persisted facts; confirmed by source read,
    not assumed)
  keep unrelated subjects/scopes operational
    (verified structurally, §9.3 -- separate engine/owner/committer
    instances per feature_subject_id, separate per-window dict entries
    within a subject; no shared mutable state links independent scopes
    except where explicitly identified, §9.3)
```

`FeatureCurrentView` is explicitly `"non-authoritative projection... never used as authoritative input anywhere"` (its own module docstring) — I-6's binding obligation for Feature Engine attaches to the **authoritative emission path** (`on_regime_classified`/`on_swing_confirmed`/`on_candle`/`process_certified_frontier` and the ADR-043 ownership/commit layer), consistent with `module-registry.yaml`'s own `owns_authoritative_state: true` classification, and with Chapter 7 §I-6's own text that non-critical projections are explicitly permitted more latitude to degrade — the view utility is not the primary surface this interpretation targets.

### 9.3 Smallest legitimate fault scope(s) and escalation

Verified directly against source (not asserted); four tiers, in ascending order — **not** the task's example "instrument" tier, which does not exist as a distinct boundary in this architecture (explained below):

```text
1. WINDOW  (within one feature_subject_id)
   Evidence: FeatureCurrentView._windows and both engines' _lineage are
   both keyed by (window_start, window_end) WITHIN one subject/scope --
   an illegal-transition raise (FeatureLineageError,
   EligibleSwingComputationDefectError) for window W1 touches ONLY the
   W1 dict entry; W2 (same subject) and every other subject are
   structurally untouched by that call.
   Faults: FeatureLineageError, EligibleSwingComputationDefectError,
   most per-fact admissibility checks (EvidenceCardinalityError,
   DefinitionVersionMismatchError, RegimeDimensionMismatchError,
   ProhibitedInputError, InvalidSwingEligibilityInputError).

2. SUBJECT  (feature_subject_id -- one engine + one owner instance,
   ALL windows of that subject)
   Evidence: both engines' own docstring, "One instance per Feature
   subject" (regime_passthrough.py, swing_distance.py); ADR-043's
   AuthoritativeSubjectOwner/SubjectOwnershipAuthority/
   FencedFeatureCommitter are keyed per feature_subject_id, not per
   window -- a fenced/terminal owner blocks ALL windows for that
   subject until a fresh engine + fresh owner + fresh generation +
   catch-up (ADR043-IMPL-A-MAJ-05). Escalates from window scope
   whenever the fault's root cause is subject-level shared state
   (ownership generation, engine construction-time cached authority,
   allocator), not one window's lineage entry.
   Faults: StaleOwnershipGenerationError, OwnershipAuthorityUnavailableError,
   DualOwnershipError, EngineNotPristineForCatchUpError,
   UnprovenCatchUpError, CanonicalHistoryMismatchError,
   NonMonotonicApplicationOrderError, ProviderFrontierMismatchError,
   IncompleteCertifiedFrontierError, ConflictingUpstreamEnvelopeError,
   RecordedTimeSourceViolationError, NonMonotonicRecordedTimeError,
   ForeignScopeError (rejected before any state read/write at all --
   the narrowest possible instance of this tier).

3. SHARED UPSTREAM AUTHORITY / DEFINITION  (every subject depending on
   the SAME Input Contract, Output Contract, or FeatureDefinition/
   formula resolution)
   Evidence: InputContractAuthorityProvider/
   OutputEventContractAuthorityProvider are Protocol boundaries a
   caller may legitimately share across many engine instances of the
   same feature_computation_profile; authority is resolved ONCE at
   construction and cached (`self._resolved_input_contract`) -- so a
   newly-broken artifact fails EVERY NEW construction/resolution
   attempt under that profile, but does NOT retroactively affect
   already-constructed subjects with already-cached authority (no
   rollback of running state). Escalates from subject scope only when
   the root cause is the SHARED authority artifact/definition itself,
   not one subject's own instance state.
   Faults: UnresolvedComputationCursorAuthorityError,
   InputContractIdentityMismatchError, RegistryContractMismatchError,
   StreamPositionsUniverseMismatchError,
   CursorRelationalInvariantViolationError, UnsupportedMergePolicyError,
   UnresolvedOutputContractAuthorityError,
   OutputEventContractUnresolvableError,
   OutputEventContractIdentityMismatchError,
   OutputEventContractNotPublishedError, OutputStreamEligibilityError,
   UnsupportedFeatureFormulaError (construction-time, unconditional --
   every subject of that feature_type/definition fails identically),
   UnsupportedDistanceRepresentationError.

4. WHOLE FEATURE ENGINE  (shared, stateless logic defect --
   e.g. a genuine bug in p_run_sort itself, not bad input)
   This is the architecture's actual ceiling, not "toàl platform":
   module-registry.yaml's own depends_on direction confirms Feature
   Engine is strictly DOWNSTREAM of market-data-ingestion/
   structure-engine/raw-regime-engine (consumes them, never the
   reverse) -- a Feature Engine-internal defect cannot structurally
   cascade UPSTREAM to those modules, and Feature Engine's own outputs
   reach only a non-authoritative projection (context-aggregator) and,
   eventually, an as-yet-unbuilt Decision layer -- consistent with I-6's
   own Prohibited-behavior clause against over-broad platform-wide
   stoppage for a non-execution-critical-boundary failure. For a truly
   shared PURE function (p_run_sort has no mutable shared state across
   calls), correctness is already the correct evidence question --
   NOT cross-subject isolation, which is structurally guaranteed for
   free by statelessness (no shared mutable state exists for one
   subject's fault to leak through) and is already covered by EVID-07's
   own property-based evidence, now CLOSED — PASS. No NEW fault-
   injection isolation test is meaningful here; escalation to this
   tier is a correctness question, not a blast-radius question.

NOT a distinct tier: "instrument". feature_subject_id already fully
  captures {instrument_id, venue_id, timeframe, feature_type,
  feature_definition_version} identity, and feature.md's own text
  explicitly declares subjects sharing an instrument but differing in
  ANY other field "hoàn toàn độc lập" -- forcing an "instrument-wide"
  fault boundary distinct from subject/shared-authority scope would
  invent a tier current architecture does not provide, the same
  discipline this task's own instruction applies in the opposite
  direction (do not force per-subject isolation the architecture
  cannot provide).
```

### 9.4 Key Question 3 — "risk-not-increased" clause

**Interpretation A**, chosen because it is the only one existing authority supports (verified, not preselected):

```text
Feature Engine itself only proves: no new uncertain authoritative
  Feature output is emitted for the affected scope.
It does NOT itself assert financial risk, because it has none to
  assert -- I-9's own Scope line already draws this boundary in
  already-Locked Constitution text (§9.1), and feature.md's own
  out-of-scope declaration forbids inventing one.
Actual "risk-not-increased" verification (I-6's own "theo risk model
  authoritative" clause) belongs downstream to Risk Gateway/Decision
  Pipeline -- and is NOT locally measurable today, for the exact same
  reason EVID-04/EVID-08 are BLOCKED_BY_EXTERNAL_DEPENDENCY: no
  Decision Engine, Risk Gateway, or Execution Engine exists anywhere
  in this repository to hold or expose an authoritative risk model
  Feature Engine (or a test of it) could consult.
```

Interpretation B (a stronger Compute-Engine-local surrogate already defined by existing architecture) does not hold — no such surrogate risk metric exists anywhere in this repository's architecture docs, ADRs, or Feature Engine's own source; inventing one now would itself be new risk semantics, explicitly prohibited by this task. Interpretation C (current authority genuinely insufficient, cross-module interpretation must be governed first) does not hold either — §9.1 already shows existing authority is sufficient for the LOCAL half of the question; only the DOWNSTREAM half is blocked, and it is blocked by missing IMPLEMENTATION (no Risk Gateway exists), not by missing AUTHORITY (I-6/I-9 already say what would be required if a risk model existed).

**Explicit split, per instruction — the first is never claimed to be proof of the second:**

```text
LOCALLY TESTABLE NOW (Feature Engine's own EVID-06 evidence):
  - blast-radius correctness: a fault in one scope (window/subject/
    shared-authority, §9.3) fails that scope closed and leaves
    unrelated scopes fully operational (§9.5 evidence matrix).
  - "no new uncertain authoritative Feature output is emitted": every
    identified fault class raises BEFORE any FeatureComputed/
    FeatureFactInvalidated append and BEFORE any FencedFeatureCommitter
    commit -- already true of the implementation (§9.2), to be proven
    by fault-injection tests, not merely exception-raising unit tests
    (the current gap, per §2's own correction above).
  - already-committed history is never modified/rolled back by a
    fail-safe action (structural: no fault path below ever mutates a
    prior fact).

EXTERNALLY BLOCKED (platform-level financial risk assertion,
  NOT locally provable, tracked as a NEW EVID-06 sub-dependency
  alongside EVID-04/EVID-08 -- NOT closed, NOT attempted by fault-
  injection tests written against Feature Engine alone):
  - "does this fail-safe action not increase risk per an authoritative
    risk model/policy" -- requires a Risk Gateway/Decision Pipeline
    that does not exist in this repository (same blocker class as
    EVID-04/EVID-08). Feature Engine emitting nothing new for an
    affected scope is a NECESSARY precondition for downstream risk not
    increasing, but is NOT a platform-level risk-not-increased proof
    by itself -- the two must never be conflated in the eventual
    EVID-06 evidence record.
```

### 9.5 Key Question 4 — fault catalog (grouped by scope, §9.3's tiers; source-grounded, no invented types)

```text
WINDOW scope:
  FeatureLineageError (fork/skip/double-invalidation/premature-
    replacement -- current_view.py + both engines' _lineage)
  EligibleSwingComputationDefectError (swing_distance.py)
  EvidenceCardinalityError, DefinitionVersionMismatchError,
    RegimeDimensionMismatchError, ProhibitedInputError,
    InvalidSwingEligibilityInputError (per-fact admissibility gates)

SUBJECT scope:
  ownership/fencing (ADR-043): StaleOwnershipGenerationError,
    OwnershipAuthorityUnavailableError, DualOwnershipError,
    EngineNotPristineForCatchUpError
  history/catch-up: UnprovenCatchUpError, CanonicalHistoryMismatchError,
    ProviderFrontierMismatchError, IncompleteCertifiedFrontierError
  P_run/apply-set (per-subject certified frontier):
    NonMonotonicApplicationOrderError, ConflictingUpstreamEnvelopeError
  recorded-time: RecordedTimeSourceViolationError,
    NonMonotonicRecordedTimeError
  scope admissibility: ForeignScopeError (narrowest instance --
    stateless rejection)

SHARED UPSTREAM AUTHORITY / DEFINITION scope:
  input-contract: UnresolvedComputationCursorAuthorityError,
    InputContractIdentityMismatchError, RegistryContractMismatchError,
    StreamPositionsUniverseMismatchError,
    CursorRelationalInvariantViolationError, UnsupportedMergePolicyError
  output-contract: UnresolvedOutputContractAuthorityError,
    OutputEventContractUnresolvableError,
    OutputEventContractIdentityMismatchError,
    OutputEventContractNotPublishedError, OutputStreamEligibilityError
  formula/representation: UnsupportedFeatureFormulaError (construction-
    time, unconditional), UnsupportedDistanceRepresentationError

WHOLE FEATURE ENGINE scope (correctness, not isolation -- §9.3 tier 4):
  a genuine defect in shared, stateless p_run_sort logic itself --
  already the evidence question EVID-07 (CLOSED — PASS) answers, not a
  new fault-injection target.
```

Every entry above is a class that already exists in `errors.py` and is already raised at an identified, source-confirmed site. No fault type not present in source is included.

### 9.6 Key Question 5 — future fault-injection evidence matrix (design only, NOT implemented)

Sized deliberately between "one row per exception type" (too narrow -- mechanical, does not prove isolation, just re-proves what `test_ownership.py`/`test_regime_passthrough.py`/`test_swing_distance.py` already prove today) and "one blanket module-down test" (too broad -- would not distinguish which scope tier actually bounds the blast radius). One representative fault per scope tier, covering all four tiers from §9.3:

```text
[1] WINDOW -- FeatureLineageError (fork attempt on window W1)
  injected boundary: second RegimeClassified fact targeting an
    already-superseded head for W1, subject A.
  affected scope: window W1 of subject A only.
  expected fail-safe: FeatureLineageError raised; W1's lineage head
    unchanged (still the legitimate winner).
  unaffected control: window W2 of the SAME subject A (independent
    dict entry) continues accepting legal transitions; subject B
    (different feature_subject_id) continues fully independently.
  must-not-advance: no new FeatureComputed/FeatureFactInvalidated for
    W1; engine._lineage[W1] byte-identical before/after the attempt.
  recovery: none needed -- W1 remains valid at its pre-attempt head;
    a correctly-targeted future replacement is still accepted normally.
  proves: per-window isolation WITHIN one subject, not just
    cross-subject isolation.

[2] SUBJECT -- StaleOwnershipGenerationError (fenced predecessor
    attempts commit after handoff)
  injected boundary: owner_0 (subject A, generation N) attempts
    FencedFeatureCommitter.commit(...) after owner_1 (generation N+1)
    has already acquired subject A.
  affected scope: subject A, generation N (owner_0) only.
  expected fail-safe: StaleOwnershipGenerationError raised; zero
    effect (already the exact assertion test_committer_rejects_
    stale_generation_with_zero_effect makes for ONE subject -- this
    matrix entry additionally requires a second, independent subject
    B constructed alongside).
  unaffected control: subject B (different feature_subject_id, SAME
    shared authority/provider/committer instances) continues normal
    acquire/process/commit throughout, unaffected by A's fencing.
  must-not-advance: committer_0.log for subject A unchanged; allocator
    sequence count for subject A unchanged; subject A's lineage
    unchanged by the rejected attempt.
  recovery: a fresh owner_1 (already holding generation N+1) continues
    normally -- no separate recovery action needed for A beyond the
    handoff that already occurred.
  proves: subject-level fencing does not leak into a second,
    independent subject sharing the same authority infrastructure.

[3] SUBJECT -- OwnershipAuthorityUnavailableError (owner goes
    permanently terminal after a prior uncertain commit outcome)
  injected boundary: a StaleOwnershipGenerationError (as in [2]) is
    allowed to mark owner_0 REVOKED/terminal for subject A.
  affected scope: subject A's owner_0 instance -- permanently, all
    windows of subject A blocked until a FRESH engine + fresh owner +
    fresh generation + catch-up (ADR043-IMPL-A-MAJ-05).
  expected fail-safe: every subsequent call on owner_0 raises
    OwnershipAuthorityUnavailableError, including re-acquire attempts.
  unaffected control: subject B, constructed independently, is
    entirely unaware of subject A's terminal owner.
  must-not-advance: subject A emits nothing further via owner_0; no
    partial/uncertain commit is ever treated as successful.
  recovery expectation: a genuinely FRESH engine_1 + fresh owner_1 +
    fresh generation for subject A, performing canonical catch-up
    (AuthoritativeLineageHistoryProvider), reconstructs subject A's
    lineage exactly and may resume authoritative work -- already
    proven for ONE subject by test_fresh_owner_and_fresh_engine_
    recover_canonical_state_after_prior_owner_goes_terminal; this
    matrix entry requires proving recovery of A happens without
    touching subject B's own independent, concurrently-running state.
  proves: permanent subject-level failure does not cascade, and
    recovery is subject-scoped, not module-wide.

[4] SUBJECT -- UnprovenCatchUpError / CanonicalHistoryMismatchError
    (history provider cannot positively prove catch-up)
  injected boundary: AuthoritativeLineageHistoryProvider returns an
    incomplete/ambiguous result (neither a genuine event list nor
    positive proof of emptiness) for subject A's catch-up.
  affected scope: subject A's CATCHING_UP -> ACTIVE transition only.
  expected fail-safe: subject A's owner never reaches ACTIVE; no
    authoritative work is performed for A.
  unaffected control: subject B, catching up against its own
    correctly-resolving provider call (even if the SAME provider
    instance, a different subject_id argument), reaches ACTIVE and
    operates normally.
  must-not-advance: zero FeatureComputed/FeatureFactInvalidated
    emitted for A; fresh_allocator sequence count for A stays at zero.
  recovery: a corrected/complete provider response allows a fresh
    catch-up attempt to succeed normally.
  proves: an ambiguous PROOF failure for one subject does not block or
    corrupt a different subject's own, independently-resolving proof.

[5] SHARED UPSTREAM AUTHORITY -- UnresolvedComputationCursorAuthorityError
    / RegistryContractMismatchError (Input Contract for feature_type=X
    becomes unresolvable/mismatched)
  injected boundary: the InputContractAuthorityProvider shared by
    every feature_type=X subject starts returning an invalid/
    unresolvable authority (simulating a broken/missing artifact).
  affected scope: EVERY NEW engine construction or frontier-processing
    call for feature_type=X attempted AFTER the break.
  expected fail-safe: construction/processing raises the appropriate
    error; no engine for feature_type=X is usable while the condition
    holds.
  unaffected control (two distinct controls, both required): (a) an
    engine for feature_type=X constructed and already caching valid
    authority BEFORE the break continues serving its already-resolved
    work normally (cached, never re-resolved per-call); (b) a subject
    of feature_type=Y (a DIFFERENT Input Contract instance) is fully
    unaffected regardless of construction order.
  must-not-advance: no new authoritative output for feature_type=X
    from any NEWLY-affected construction attempt.
  recovery: once the Input Contract artifact resolves correctly again,
    a fresh engine construction for feature_type=X succeeds normally;
    already-running engines were never affected and need no recovery.
  proves: shared-authority-scope faults are bounded by "which artifact
    is actually broken," not "which subject," and do not retroactively
    corrupt already-cached, already-running state.

[6] SHARED DEFINITION -- UnsupportedFeatureFormulaError (construction-
    time, unconditional, CandleWindowFeatureEngine)
  injected boundary: attempt to construct an engine for a
    feature_type/definition requiring an unresolved formula.
  affected scope: every subject of that exact feature_type +
    feature_definition_version.
  expected fail-safe: construction itself raises; no instance of that
    definition is ever usable.
  unaffected control: subjects of OTHER feature_types (Regime
    pass-through, Swing distance -- definitions with a resolved
    formula) construct and operate normally, unaffected.
  must-not-advance: zero output ever for the unresolved definition
    (this is a permanent, not transient, fail-closed state until a
    governed formula-resolution decision is made -- out of scope here).
  recovery: not applicable until a separate, future governed decision
    resolves the formula -- correctly reported as "no recovery
    expectation" rather than inventing one.
  proves: definition-wide fault scope is bounded by the shared
    definition, not by instrument/venue/timeframe.

If a fault legitimately affects module-global authority (WHOLE FEATURE
  ENGINE tier, §9.3/§9.5), module-global failure IS correct and no
  per-subject isolation test should be forced onto it -- per
  instruction, and per §9.3's own statelessness argument for
  p_run_sort, already covered by EVID-07 (CLOSED — PASS), not
  re-tested here.
```

### 9.7 ADR Scope Rule (Chapter 0 §4b) — run fresh, not preselected

```text
Platform Invariant addition/edit:            NO -- I-6/I-9 text unchanged;
                                               this reads/applies it.
Event Schema change:                          NO.
Module Taxonomy / dependency-graph change:    NO -- module-registry.yaml
                                               untouched.
Governance/Approval-process change:           NO.
Decision affecting >1 module:                 NO -- explicitly scoped
                                               FEATURE-ENGINE-ONLY (same
                                               scoping discipline already
                                               established for the
                                               Hypothesis/Testing
                                               Convention v0.17 decision
                                               in this exact chain).
                                               Whether structure-engine/
                                               raw-regime-engine reach an
                                               identical conclusion is a
                                               SEPARATE question for
                                               their OWN future findings
                                               to independently derive --
                                               this transaction does not
                                               bind them, canonicalize a
                                               cross-module doctrine, or
                                               edit any shared authority
                                               document.
Hard to reverse:                              NO -- pure documentation/
                                               evidence-design; a future
                                               bounded correction can
                                               amend it, same discipline
                                               already used throughout
                                               this file's own §2.
Edit/supersede a Locked ADR:                  NO -- no ADR touched.
Materially significant module-internal
  decision (Optional criterion):              NO -- no contract change,
                                               no behavior change, no new
                                               test-execution mechanism/
                                               dependency/tool introduced
                                               (unlike the Hypothesis
                                               decision, which DID change
                                               test-execution behavior).
                                               This decision only reads
                                               already-Locked text and
                                               documents evidence design
                                               for FUTURE tests not yet
                                               written -- the same
                                               "evidence design feeding a
                                               future candidate" shape as
                                               this file's own §1-§8 and
                                               EVID-07 QG candidate's own
                                               §2 surface-identification
                                               work, neither of which was
                                               separately ADR-scored.

Result: ADR_NOT_REQUIRED.
```

Per instruction: the design only describes evidence for already-authoritative semantics (I-6, I-9, ADR-043, feature.md — all already Locked/Approved) — no ADR is authored by this transaction, none is required.

### 9.8 Not performed by this transaction (explicit)

```text
No fault-injection test authored. No production source file touched
  (verified `git diff --quiet -- python/feature-engine/src
  python/feature-engine/tests`, this transaction). No Constitution/
  Domain Contract/Risk-semantics edit. No ADR authored. No Review A,
  Review B, Risk Classification, or Product Owner decision performed.
  `P3-FEATURE-QG-EVID-06` disposition unchanged: still OPEN,
  `NEEDS_GOVERNED_DESIGN_OR_MECHANISM` — only its interpretation
  sub-step is now resolved (§9.1-§9.6); fault-injection authoring and
  formal evidence remain a SEPARATE future governed transaction. Overall
  Feature Engine Chapter 13 Quality Gate: unchanged, FAIL — evidence
  (EVID-04/EVID-06/EVID-08 remain OPEN/blocking). Feature Engine module
  approval: NOT APPROVED (unaffected). LIVE: NOT_AUTHORIZED (unaffected).
```

**Next governed step (not performed by this transaction):** Review A of this §9 interpretation/design; if CLEAN, a separate fault-injection implementation/evidence transaction authors the §9.6 matrix (and any additional rows Review A requests) against real Feature Engine source, then a formal Chapter 13 §13.9-style evidence transaction records measurement and, only if it genuinely passes — including the LOCAL half of §9.4's split, never claiming the externally-blocked platform-level half — closes `P3-FEATURE-QG-EVID-06`.
