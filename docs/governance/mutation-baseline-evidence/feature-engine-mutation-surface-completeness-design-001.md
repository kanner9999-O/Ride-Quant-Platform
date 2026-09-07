# Feature Engine — Mutation-Surface Completeness (Condition 3) Design Candidate 001

```yaml
status: CANDIDATE / NOT EFFECTIVE / PENDING REVIEW
artifact_id: feature-engine-mutation-surface-completeness-design-001
created_for: >
  Designing (not implementing) one governed mechanism to resolve EVID-03's
  Condition 3 (mutation-surface completeness) for the 5 high-materiality
  methods mutmut 3.7.0 structurally excludes from Feature Engine's mutation
  surface.
transaction_kind: DESIGN ONLY
production_changed: false
tests_changed: false
tooling_changed: false
fault_injection_performed: false
formal_step9_qg_evaluation_performed: false
evid_03_closed: false
repository_head_at_authoring: 5e8b1a884d67031c68596378c33e49d82c18532c
```

This document is a **design candidate**. It proposes a mechanism and, for
each of the 5 named high-materiality methods, a concrete fault-class plan —
it does **not** execute any fault injection, does not add or modify any
test, and does not close `P3-FEATURE-QG-EVID-03` or any part of it. Nothing
below is effective until a separately recorded review/approval decision
accepts this design (or an amended version of it), and a **separate,
later** implementation transaction actually authors and runs the harness
against pinned source.

## 0. Authority resolved

- **Testing Convention v0.16, `docs/engineering/testing.md` §5a-i/§5b/§5c/§5d**
  (Approved) — §5b requires an EXACT inventory of every un-mutated
  behavior-bearing unit with its specific exclusion reason and whether
  qualifying evidence exists; §5c defines EXACTLY two qualifying-evidence
  paths for behavior outside mutmut's surface — (i) a separately-accepted
  supplemental mutation-testing mechanism reaching that code, or (ii)
  governed, deterministic, reproducible fault-injection evidence (a
  documented, specific defect deliberately introduced, proven detected by
  the existing suite, with the defect/detecting-test/result all
  individually pinned) — and explicitly states an ordinary passing unit
  test is NOT sufficient by itself; §5d records the decorated-class skip as
  a genuine, material, currently-open mutmut 3.7.0 limitation with three
  closure paths ((a) tool fix, (b) §5c evidence per gap, (c) carry forward
  as residual) and explicitly defers the choice among them to "a future
  governed transaction (candidate installation or a dedicated
  gap-remediation transaction)" — this document is exactly that dedicated
  transaction, for path (b).
- **Approved Feature Engine mutation threshold proposal §4.2** — restates
  §5b's rule as an explicit Condition 3 for `P3-FEATURE-QG-EVID-03`: for
  each of the 5 high-materiality methods, EITHER (a) an accepted
  supplemental mutation-testing mechanism, (b) governed deterministic
  fault-injection evidence, or (c) an explicit, separately-recorded
  Product Owner risk-acceptance naming that residual — meeting the raw
  score threshold never silently satisfies this.
- **`feature-engine-chapter13-remediation-plan-001.md`** — classifies this
  exact work as `EVID-03(b): blind-spot path decision` -> `blind-spot
  evidence authored`, one of four mutually-independent tracks, with no
  cross-dependency on `EVID-04`/`EVID-05`/`EVID-06`/`EVID-07`/`EVID-08`.
- **`feature-engine-mutation-baseline-001-analysis.md` §2** — original
  12-method inventory and per-method materiality rationale (re-derived
  independently from current source below, not trusted verbatim).
- **`feature-engine-mutation-full-checkpoint-002.json`** — current
  Condition 1 evidence (killed 1342/1531, raw score 87.65512736773351%,
  numerically above the 87.001959503592% threshold, NOT a formal PASS) and
  Condition 2 evidence (170/170 material identities governedly resolved,
  10 of them still raw-`survived`) — cited for state continuity only; this
  design touches neither.
- **Current exact Feature Engine source** — `src/feature_engine/
  authority_resolver.py`, `candle.py`, `contracts.py` — read directly and
  in full for this design (§2 below); independently re-verified empirically
  (§1.1) that all 5 methods generate ZERO mutmut mutants at the current
  pinned boundary, not merely re-asserted from a prior transaction.

## 1. Fresh Chapter 0 §4b ADR Scope Rule check (this design, not inherited)

Evaluated independently for THIS specific decision (whether introducing a
Feature-only supplemental deterministic fault-injection evidence mechanism
requires an ADR) — not assumed from the threshold proposal's own
`ADR_OPTIONAL` (a different, larger-scoped decision) nor from the mutant-
reclassification candidate's `ADR_NOT_REQUIRED` (a narrower, no-new-
mechanism decision).

| §4b criterion | Applies here? |
|---|---|
| Adds/changes a Platform Invariant | No — does not touch Chapter 8/13 or any Locked invariant. The evidence CLASS ("governed deterministic fault-injection evidence") is already defined by Testing Convention v0.16 §5c (Approved); this design does not redefine it. |
| Changes an Event Schema | No. |
| Changes Module Taxonomy/dependency graph | No. |
| Changes Governance/Approval process | **Borderline — resolved below.** §5c already defines WHAT qualifies as evidence; this design proposes a NEW, concrete, reusable EXECUTION MECHANISM (a harness pattern, a fault-ID naming convention, a machine-readable per-fault evidence schema) to actually PRODUCE that evidence for Feature Engine. It is a genuinely new artifact/process, not present anywhere in the repository today. |
| Affects >1 module | Scoped explicitly to `feature-engine` only in this design; but the mechanism is generic enough (temporary source patch + governed suite run + restore) that it could be reused for structure-engine/raw-regime-engine's own dataclass-hosted methods in the future — a real, if not immediate, cross-module reusability concern. |
| Hard to reverse | No — supplemental, additive evidence; produces no permanent code change; a future mutmut version fix (§5d path (a)) could make the whole mechanism moot without reversing anything. |
| Modifies/supersedes a Locked ADR | No. |

**Disposition: `ADR_OPTIONAL`.** Reasoning: this is directly analogous to
the precedent already set for the mutmut/compatibility-shim mechanism
itself (`docs/MANIFEST.md`'s own recorded disposition for that candidate:
`ADR_OPTIONAL — ADR NOT AUTHORED`) — introducing a genuinely new test-
effectiveness TOOL/MECHANISM for Feature Engine is a real methodological
decision worth documenting for future consistency and cross-module
reusability ("ảnh hưởng đáng kể" — ADR Optional's own criterion), but does
not touch a Platform Invariant, Event Schema, Module Taxonomy, or cross-
module contract, and is fully reversible. **Per this task's own
instruction, no ADR is authored in this transaction regardless of
disposition** — `ADR_OPTIONAL` means discretionary, not blocking; a future
implementation transaction may author one if judged worthwhile, or proceed
directly to implementation under this design's own review/approval.

## 1.1 Empirical re-confirmation — why mutmut 3.7.0 excludes each method (not trusted from any prior summary)

All 5 classes are `@dataclass(frozen=True, slots=True)`-decorated; mutmut
3.7.0's decorated-class limitation (Testing Convention v0.16 §5a-i, `P3-
PY-MUT-A-MAJ-02`) skips ALL hand-written methods on such classes wholesale
— confirmed FRESH in this transaction, not re-asserted from
`feature-engine-mutation-baseline-001-analysis.md` §2: a `python -m
tooling run` mutant-GENERATION pass (no tests executed to completion; the
generated `mutants/src/feature_engine/*.py` tree was inspected directly,
then the entire disposable venv/mutants/ workspace was destroyed, leaving
zero footprint) shows **zero** `_mutmut_N` variants for any of the 5
target methods — each appears in the generated tree exactly once, as its
own unmutated original body, while ordinary (non-dataclass-hosted) methods
in the SAME files (e.g. `authority_resolver.resolve_input_contract_
authority_from_repository`, which has dozens of `_mutmut_N` variants) are
mutated normally. This is a structural, tool-version-specific exclusion,
not a materiality judgment — confirmed empirically, not inferred.

## 2. Selected mechanism: governed deterministic fault injection (Testing Convention v0.16 §5c path (ii))

**Why fault injection, not path (i) or (iii):** no separately-accepted
supplemental mutation-testing mechanism reaching decorated classes exists
today (re-confirmed: no such tool is installed, pinned, or referenced
anywhere in `pyproject.toml`/`requirements-dev.lock.txt`/`docs/engineering/
testing.md`) — path (i) is unavailable, not merely unexamined. Product
Owner risk-acceptance (path (iii)) is available in principle but is
explicitly NOT proposed here per this task's own instruction not to use it
"merely for convenience" — these 5 methods carry genuine, non-trivial
branching logic (comparison guards, 4-way dispatch, numeric rounding,
~25-guard validation chain) that a hand-authored, reviewable fault-
injection harness CAN meaningfully exercise; risk-acceptance would be
appropriate only if no such mechanism were feasible, which is not the case
here.

### 2.1 Mechanism shape (design only — no script exists yet)

A NEW, Feature-Engine-scoped supplemental harness (proposed future location:
`python/feature-engine/tooling/fault_injection/`, out of scope to create in
this transaction) that, for each individually-pinned fault record:

1. **Pins the exact boundary.** Records `repository_head`, the exact
   target file's blob hash, and the exact target method's fully-qualified
   name before touching anything.
2. **Applies one exact, surgical source patch.** Each fault is specified as
   an exact `(file, old_string, new_string)` triple (mirroring this
   repository's own `Edit` tool semantics) — a single, minimal, AST-
   meaningful token/operator/branch change, never a fuzzy or regex-based
   substitution. **Fail-closed:** if `old_string` is not found VERBATIM
   (and uniquely) in the current file, the harness aborts with a non-zero
   exit and records the fault as `INJECTION_FAILED — SOURCE DRIFT`, never
   silently skipping or approximating.
3. **Proves activation.** Immediately after patching, the harness re-reads
   the patched file and asserts the exact `new_string` is present at the
   expected location (byte-for-byte) — proof the intended, and ONLY the
   intended, fault is live, before any test runs.
4. **Runs the governed ordinary test suite unmodified** (`pytest tests/
   -q`, the SAME command and SAME test tree used for every other
   Feature Engine evidence transaction in this program — never a bespoke
   fault-specific test invocation that could be gamed) against the
   patched working tree.
5. **Records the verdict.** `DETECTED` if the suite reports any failure;
   `SURVIVED` if the suite reports 226/226 (or whatever the then-current
   ordinary count is) passing despite the live fault — an explicit,
   named residual, exactly mirroring what a real `survived` mutmut status
   would mean, but never merged into mutmut's own ten-status counts.
6. **Restores unconditionally.** Whether `DETECTED`, `SURVIVED`, or
   `INJECTION_FAILED`, the harness restores the exact original file
   content (e.g. `git checkout -- <file>`, or a captured pre-patch byte
   copy) and verifies `git diff --quiet -- <file>` confirms zero residual
   modification BEFORE proceeding to the next fault or exiting — this is
   the "leave no modified working-tree source after each run" requirement,
   enforced by an explicit post-condition check, not merely by intent.
7. **Emits one machine-readable record per fault** (proposed JSON shape):
   ```json
   {
     "fault_id": "FI-OHLCV-FIELD-01",
     "method": "candle.OHLCV.field",
     "source_file": "src/feature_engine/candle.py",
     "source_blob_before": "<git blob hash>",
     "fault_class": "branch_swap",
     "old_string": "...",
     "new_string": "...",
     "activation_confirmed": true,
     "test_command": "pytest tests/ -q",
     "detecting_tests": ["tests/test_candle.py::test_field_high_returns_high"],
     "result": "DETECTED",
     "restored_confirmed": true,
     "repository_head_at_run": "<sha>"
   }
   ```

### 2.2 How each mechanism requirement is met

| Requirement | How this design satisfies it |
|---|---|
| Leaves production source unchanged during evidence execution | Step 6's unconditional restore + `git diff --quiet` post-check, per fault, not per batch. |
| Deterministic/reproducible from an exact pinned boundary | Every fault record pins `repository_head`, source blob, exact `old_string`/`new_string` — re-running the SAME record against the SAME boundary reproduces the SAME patch byte-for-byte. |
| Identifies each injected fault uniquely | `fault_id` naming convention `FI-{METHOD-SLUG}-{NN}`, pinned in the evidence record. |
| Proves the fault was actually activated | Step 3's post-patch read-back-and-assert, recorded as `activation_confirmed`. |
| Proves the governed ordinary suite distinguishes it | Step 4's UNMODIFIED `pytest tests/ -q` run against the SAME governed test tree used everywhere else — never a fault-specific bespoke check. |
| Fails closed if injection cannot be applied exactly | Step 2's exact-match-or-abort rule. |
| Leaves no modified working-tree source after each run | Step 6's explicit post-condition, checked per fault. |
| Produces machine-readable per-method/per-fault evidence | §2.1 item 7's JSON record shape, one per fault, aggregable per method. |
| Avoids changing the raw 1531-mutant denominator or Condition-1 score | The harness never invokes `mutmut`/`python -m tooling run`, never touches `mutants/`/`.mutmut-cache`, and its own results are written to a SEPARATE, distinctly-named evidence artifact, never merged into any `sorted_mutant_id_to_result_mapping` or `ten_status_counts`. |
| Remains supplemental Condition-3 evidence only | Explicitly framed throughout as satisfying Testing Convention v0.16 §5c path (ii) for Condition 3 alone — never cited as, or convertible into, Condition-1 raw-score evidence. |

## 3. Per-method fault-class plans

Each entry: why mutmut excludes it (§1.1, common to all 5, restated
briefly per-method for self-containedness), the authoritative behavior/
invariant protected, the proposed fault(s), injection boundary, expected
observable distinguishing behavior, exact current test surface (existing
vs. new), the deterministic reproduction contract, pass/fail criteria,
evidence to record, and assumptions/invalidation triggers.

---

### 3.1 `authority_resolver.StaticInputContractAuthorityProvider.resolve`

- **Why excluded:** `StaticInputContractAuthorityProvider` is
  `@dataclass(frozen=True, slots=True)`-decorated (`authority_resolver.py`,
  class definition immediately preceding `resolve`); empirically confirmed
  zero `_mutmut_N` variants (§1.1).
- **Authoritative behavior/invariant protected:** current source (`resolve`,
  lines 251-258):
  ```python
  def resolve(self, profile: FeatureComputationProfile) -> VerifiedInputContractAuthority:
      if self.authority.feature_computation_profile != profile:
          raise InputContractIdentityMismatchError(...)
      return self.authority
  ```
  A static provider must NEVER return authority for a mismatched profile —
  "a static provider can never be substituted for the wrong engine's
  authority" (the class's own docstring).
- **Fault class — `FI-STATIC-PROVIDER-01`, inverted guard:** `!=` -> `==`.
  Under the fault, the guard fires (raises) exactly when the profile
  MATCHES (rejecting the correct case) and silently falls through to
  `return self.authority` when the profile MISMATCHES — the exact
  "silently accept mismatched-profile authority" defect class this method
  exists to prevent.
- **Injection boundary:** single comparison-operator token in the `if`
  condition; no other line touched.
- **Expected observable distinguishing behavior:** constructing an engine
  with a `StaticInputContractAuthorityProvider` wrapping the WRONG
  profile's authority must raise `InputContractIdentityMismatchError`
  under the original code; under the fault, no exception is raised and the
  wrong authority is silently returned/bound.
- **Existing test surface (no new test required):**
  `tests/test_swing_distance.py` (~line 1901) and `tests/test_regime_
  passthrough.py` (~line 731) each already construct a
  `StaticInputContractAuthorityProvider(REGIME_INPUT_CONTRACT)` /
  `StaticInputContractAuthorityProvider(SWING_DISTANCE_INPUT_CONTRACT)`
  passed to the WRONG engine type and assert `pytest.raises
  (InputContractIdentityMismatchError)` — under `FI-STATIC-PROVIDER-01`
  this assertion would fail to raise, so the existing suite already
  detects this fault; no new test is proposed.
- **Deterministic reproduction contract:** `old_string=
  "if self.authority.feature_computation_profile != profile:"`,
  `new_string="if self.authority.feature_computation_profile == profile:"`
  in `src/feature_engine/authority_resolver.py`, applied at the current
  pinned source blob.
- **Pass/fail criteria:** `DETECTED` iff at least one of the two named
  existing tests fails under the fault; `SURVIVED` otherwise.
- **Evidence to record:** the JSON record per §2.1 item 7, `detecting_
  tests` listing both named tests if both fail.
- **Assumptions/invalidation triggers:** assumes the two named tests are
  not removed/weakened in a future transaction without a corresponding
  fault-injection re-run; a future change to either engine's constructor
  validation order that short-circuits BEFORE reaching `.resolve()` would
  invalidate this specific detection path and require re-verification.

---

### 3.2 `candle.OHLCV.field`

- **Why excluded:** `OHLCV` is `@dataclass(frozen=True, slots=True)`-
  decorated (`candle.py`); empirically confirmed zero mutants (§1.1).
- **Authoritative behavior/invariant protected:** current source (lines
  54-66): a strict 4-way name-to-field dispatch (`open`/`high`/`low`/
  `close`) with a fail-closed `raise ValueError` for any other name — "read
  one of the four price fields by name ... bounded to the OHLC fields
  only, never an arbitrary attribute lookup."
- **Fault classes:**
  - `FI-OHLCV-FIELD-01` (branch swap): `if name == "high": return
    self.high` -> `return self.low` — wrong field routing, silent data
    corruption feeding directly into `reference_price_field` lookups.
  - `FI-OHLCV-FIELD-02` (fail-closed bypass): `raise ValueError(f"unsupported
    reference_price_field: {name!r}")` -> `return self.close` — silently
    defaulting instead of rejecting an unsupported field name.
- **Injection boundary:** one `return` statement's target attribute
  (FI-01); the final `raise` statement's entire body (FI-02).
- **Expected observable distinguishing behavior:** `.field("high")` must
  return the `high` value specifically (distinct from `open`/`low`/
  `close`); `.field(<anything not in the 4 names>)` must raise
  `ValueError`, never silently return a value.
- **Existing test surface (no new test required):** `tests/test_candle.py`
  already asserts, on a fixture with 5 mutually DISTINCT OHLCV values
  (open=100, high=110, low=90, close=105, volume=1): `test_field_open_
  returns_open`, `test_field_high_returns_high`, `test_field_low_returns_
  low`, `test_field_close_returns_close` (each field's own dedicated exact-
  value assertion) and `test_field_unsupported_name_rejected` (`pytest.
  raises(ValueError, match=...)` for `.field("volume")`). Because every
  field value is distinct, `FI-OHLCV-FIELD-01`'s swap is caught by
  `test_field_high_returns_high`'s own exact-value assertion; `FI-OHLCV-
  FIELD-02`'s bypass is caught by `test_field_unsupported_name_rejected`'s
  `pytest.raises`. No new test proposed.
- **Deterministic reproduction contract:** exact `old_string`/`new_string`
  pairs against `src/feature_engine/candle.py`'s current pinned blob, one
  per fault ID, applied and restored independently (never both faults
  live simultaneously).
- **Pass/fail criteria:** `DETECTED` iff the corresponding named test
  fails; `SURVIVED` otherwise.
- **Evidence to record:** per §2.1 item 7, one record per fault ID.
- **Assumptions/invalidation triggers:** assumes the 5 OHLCV fixture
  values remain mutually distinct in `test_candle.py` (a future edit
  collapsing e.g. `high == low` would silently weaken `FI-OHLCV-FIELD-01`'s
  detection without changing any assertion's pass/fail outcome trivially —
  this is exactly the kind of fixture-fragility this bounded evidence
  transaction is meant to catch, and should be explicitly re-checked at
  execution time, not merely assumed from this design).

---

### 3.3 `contracts.DecimalPrecisionPolicy.apply`

- **Why excluded:** `DecimalPrecisionPolicy` is `@dataclass(frozen=True,
  slots=True)`-decorated (`contracts.py`); empirically confirmed zero
  mutants (§1.1).
- **Authoritative behavior/invariant protected:** current source (lines
  660-662):
  ```python
  def apply(self, value: Decimal) -> Decimal:
      quantum = Decimal(1).scaleb(-self.digits)
      return value.quantize(quantum, rounding=self.rounding)
  ```
  The actual numeric rounding computation applied to every emitted Feature
  value — "core numeric business logic" (baseline analysis's own framing,
  independently re-confirmed by direct reading here).
- **Fault classes:**
  - `FI-DECIMAL-APPLY-01` (sign flip): `Decimal(1).scaleb(-self.digits)` ->
    `Decimal(1).scaleb(self.digits)` — computes a wildly wrong quantum
    (e.g. `digits=2` -> quantum `100` instead of `0.01`), corrupting every
    rounded value's magnitude, not merely its last digit.
  - `FI-DECIMAL-APPLY-02` (dropped rounding kwarg): `value.quantize(quantum,
    rounding=self.rounding)` -> `value.quantize(quantum)` — silently falls
    back to Python's `Decimal` context default rounding (`ROUND_HALF_EVEN`)
    regardless of the policy's own configured `rounding`, observable only
    at an exact half-way rounding boundary.
- **Injection boundary:** one unary-minus token (FI-01); the entire
  `rounding=self.rounding` keyword argument (FI-02).
- **Expected observable distinguishing behavior:** for FI-01, any non-
  trivial fixed-point value computed anywhere in the suite (e.g. a
  `distance_to_last_confirmed_swing` result asserted as `Decimal("5.00")`)
  would instead come out rounded to the nearest 10^digits multiple (e.g.
  `"0"` or `"100"` for `digits=2`) — a gross, suite-wide magnitude error.
  For FI-02, only a value landing exactly on a rounding half-boundary under
  a NON-default rounding mode would diverge from the policy's own
  configured behavior.
- **Existing test surface:**
  - `FI-DECIMAL-APPLY-01`: caught INCIDENTALLY by the entire existing
    numeric-assertion surface across `test_swing_distance.py`/`test_
    regime_passthrough.py` (every `Decimal("N.NN")`-style value assertion
    uses `make_decimal_policy(digits=2)`'s quantum; a magnitude-scale error
    would fail essentially all of them) — existing coverage is sufficient
    for detection, though a single DEDICATED, isolated unit test of
    `.apply()` itself (proposed new test, e.g. `test_apply_uses_negative_
    digits_exponent`) would give a cleaner, more attributable
    `detecting_tests` record than "226 unrelated tests failed."
  - `FI-DECIMAL-APPLY-02`: **no existing test surface** — every current
    fixture value in the suite is a "clean" decimal (e.g. `.00`), never
    landing on an exact rounding half-boundary; `DecimalPrecisionPolicy`
    itself is only ever constructed via `conftest.make_decimal_policy()`
    with a fixed `digits`/`rounding="ROUND_HALF_UP"`, never directly unit-
    tested for its OWN rounding-mode-sensitive behavior. **New test
    proposed:** `DecimalPrecisionPolicy(digits=2,
    rounding="ROUND_HALF_UP").apply(Decimal("1.005")) == Decimal("1.01")`
    (a value exactly on the 2-digit half-boundary; `ROUND_HALF_UP` rounds
    up to `1.01`, while Python's context default `ROUND_HALF_EVEN` would
    round to `1.00`, since 0 is the even digit) — this new test is
    REQUIRED before `FI-DECIMAL-APPLY-02` can be claimed `DETECTED`.
- **Deterministic reproduction contract:** exact `old_string`/`new_string`
  pairs against `src/feature_engine/contracts.py`'s current pinned blob.
- **Pass/fail criteria:** `DETECTED` iff the (existing or, for FI-02, the
  proposed new) test fails; `SURVIVED` otherwise. `FI-DECIMAL-APPLY-02`
  cannot be run against this design's own claim of `DETECTED` until the
  proposed new test is actually authored in a later implementation
  transaction — this design records it as `PLANNED, TEST REQUIRED`, not a
  pre-judged outcome.
- **Evidence to record:** per §2.1 item 7; FI-01's record should name
  the DEDICATED new test as `detecting_tests[0]` once authored, with the
  broad incidental-detection set as corroborating context, not the primary
  claim.
- **Assumptions/invalidation triggers:** a future change to any fixture's
  `digits` value that removes all "clean multiple-of-10^-digits" values
  would strengthen (not weaken) FI-01's incidental detection; a future
  change to the Decimal context's own default rounding mode (extremely
  unlikely, Python-version-level) would invalidate FI-02's specific
  boundary value and require recomputation.

---

### 3.4 `contracts.DecimalPrecisionPolicy.__post_init__`

- **Why excluded:** same class as §3.3; empirically confirmed zero mutants
  (§1.1).
- **Authoritative behavior/invariant protected:** current source (lines
  654-658):
  ```python
  def __post_init__(self) -> None:
      if self.digits < 0:
          raise InvalidFeatureDefinitionError(f"digits must be >= 0, got {self.digits!r}")
      if self.rounding not in _VALID_ROUNDINGS:
          raise InvalidFeatureDefinitionError(f"unsupported rounding mode: {self.rounding!r}")
  ```
  Construction-time boundary/membership validation for the policy `apply`
  itself depends on (§3.3).
- **Fault classes:**
  - `FI-DECIMAL-POSTINIT-01` (boundary flip): `self.digits < 0` ->
    `self.digits <= 0` — wrongly rejects the valid boundary value
    `digits=0`.
  - `FI-DECIMAL-POSTINIT-02` (inverted membership): `self.rounding not in
    _VALID_ROUNDINGS` -> `self.rounding in _VALID_ROUNDINGS` — inverts
    accept/reject entirely: valid rounding modes are rejected, invalid ones
    are silently accepted.
- **Injection boundary:** one comparison operator (FI-01); one membership-
  test negation (FI-02).
- **Expected observable distinguishing behavior:** FI-01 —
  `DecimalPrecisionPolicy(digits=0, rounding="ROUND_HALF_UP")` must
  construct successfully under the original code, must raise under the
  fault. FI-02 — a policy with a VALID rounding mode (e.g.
  `"ROUND_HALF_UP"`) must construct successfully; a policy with an INVALID
  rounding mode (e.g. `"NOT_A_REAL_MODE"`) must raise
  `InvalidFeatureDefinitionError` — both directions invert under the
  fault.
- **Existing test surface:** **no existing test surface** —
  `DecimalPrecisionPolicy` is only ever constructed via `conftest.
  make_decimal_policy(digits=2)` (always non-zero digits, always the same
  valid rounding string); no test anywhere directly constructs it with
  `digits=0` or with an invalid `rounding`. **New tests proposed:**
  `test_decimal_precision_policy_digits_zero_is_valid_boundary`
  (constructs `DecimalPrecisionPolicy(digits=0, rounding="ROUND_HALF_UP")`,
  asserts no exception) and `test_decimal_precision_policy_invalid_
  rounding_mode_rejected` (constructs with `rounding="NOT_A_REAL_MODE"`,
  asserts `InvalidFeatureDefinitionError`) — both REQUIRED before either
  fault can be claimed `DETECTED`.
- **Deterministic reproduction contract:** exact `old_string`/`new_string`
  pairs against `src/feature_engine/contracts.py`'s current pinned blob.
- **Pass/fail criteria:** `DETECTED` iff the corresponding new test fails
  under the fault; `SURVIVED` otherwise. Recorded `PLANNED, TESTS
  REQUIRED` in this design, not a pre-judged outcome.
- **Evidence to record:** per §2.1 item 7, once the two new tests exist.
- **Assumptions/invalidation triggers:** assumes `_VALID_ROUNDINGS` (the
  module-level frozenset of accepted `decimal` rounding-mode strings)
  remains non-empty and contains at least one mode distinguishable from
  `"NOT_A_REAL_MODE"`; trivially true today and structurally unlikely to
  change without an intentional, reviewed edit.

---

### 3.5 `contracts.FeatureDefinition.__post_init__`

- **Why excluded:** `FeatureDefinition` is `@dataclass(frozen=True,
  slots=True)`-decorated (`contracts.py`); empirically confirmed zero
  mutants (§1.1).
- **Authoritative behavior/invariant protected:** current source (lines
  703-813) — directly counted (not estimated): **25 independent
  `raise InvalidFeatureDefinitionError(...)` fail-closed guard statements**
  spanning non-empty-string checks, 6 exact-policy-string equality guards,
  and feature-type-specific (metric vs. distance) cross-field mutual-
  exclusivity/required-presence/allowed-value checks — "feature-engine's
  single largest, most safety-critical validation guard chain" (Testing
  Convention v0.16 §5d's own framing, independently re-confirmed by direct
  count here). Representative (not exhaustive) fault coverage is proposed,
  spanning 3 distinct guard SHAPES present in this method, per this task's
  own "meaningful semantic corruption, not exhaustive mechanical coverage"
  guidance:
- **Fault classes:**
  - `FI-FEATUREDEF-01` (policy-equality guard inversion): `self.
    correction_policy != CORRECTION_POLICY` -> `==` — inverts the guard so
    it fires exactly when the CORRECT canonical value is supplied
    (rejecting every valid Definition) and is silent when an incorrect
    value is supplied (accepting an invalid `correction_policy`).
  - `FI-FEATUREDEF-02` (cross-field OR->AND inversion, broken invariant):
    `any(field is not None for field in distance_only_fields) or
    self.normalization_policy is not None` -> `and` — a metric-type
    Definition setting exactly ONE distance-only field (e.g.
    `swing_direction`) alone, with `normalization_policy` left `None`, is
    silently ACCEPTED instead of rejected (the OR requires only one side;
    the AND wrongly requires both).
  - `FI-FEATUREDEF-03` (boundary flip): `self.window_candle_count is None
    or self.window_candle_count < 1` -> `<= 1` — wrongly rejects the valid
    boundary value `window_candle_count=1`.
- **Injection boundary:** one comparison-operator token (FI-01); one
  boolean-operator token (FI-02); one comparison-operator token (FI-03) —
  each independently applied/restored.
- **Expected observable distinguishing behavior:** FI-01 — ANY successful
  construction of ANY valid `FeatureDefinition` anywhere in the suite
  (e.g. via `make_candle_definition()`/`make_distance_definition()`) must
  raise under the fault, since every valid Definition necessarily supplies
  the CORRECT `correction_policy` value. FI-02 — a metric-type Definition
  with exactly one distance-only field set must still raise under the
  original code; under the fault it does not. FI-03 —
  `make_candle_definition(window_candle_count=1)` must construct
  successfully under the original code; under the fault it raises.
- **Existing test surface:**
  - `FI-FEATUREDEF-01`: **existing, very broad** — `tests/test_
    definition.py::test_valid_definitions_accepted` (and, transitively,
    essentially every OTHER test file's own engine-construction fixtures,
    e.g. `_engine()` helpers in `test_swing_distance.py`/`test_regime_
    passthrough.py`) constructs a valid `FeatureDefinition` and asserts no
    exception; ANY of these already fails under the fault. No new test
    needed, though `test_valid_definitions_accepted` alone is sufficient
    to name as the primary `detecting_tests` entry for a clean, minimal
    evidence record.
  - `FI-FEATUREDEF-02`: **existing** — `tests/test_definition.py::
    test_contradictory_type_specific_fields_rejected_distance_field_on_
    metric` constructs exactly this scenario (a `volatility_metric`
    Definition with `swing_direction="HIGH"` set alone, `normalization_
    policy` left at its default `None`) and asserts `pytest.raises
    (InvalidFeatureDefinitionError)` — under the fault this assertion
    fails to raise. No new test needed.
  - `FI-FEATUREDEF-03`: **no existing test surface** — every current
    fixture uses `window_candle_count`'s conftest default (`3`); the
    boundary value `1` is never directly constructed anywhere. **New test
    proposed:** `test_window_candle_count_of_one_is_valid_boundary`
    (`make_candle_definition(window_candle_count=1)`, asserts no
    exception) — REQUIRED before FI-03 can be claimed `DETECTED`.
- **Deterministic reproduction contract:** exact `old_string`/`new_string`
  pairs against `src/feature_engine/contracts.py`'s current pinned blob,
  one per fault ID, applied/restored independently.
- **Pass/fail criteria:** `DETECTED` iff the named (existing, for FI-01/
  FI-02) or new (for FI-03, once authored) test fails under the fault;
  `SURVIVED` otherwise.
- **Evidence to record:** per §2.1 item 7, one record per fault ID.
- **Assumptions/invalidation triggers:** FI-01's broad detection depends
  on at least one construction-fixture test continuing to exist and run
  as part of the governed suite (trivially true — the entire suite would
  otherwise be non-functional); FI-02/FI-03 depend on the two named tests'
  exact scenario shape (single-field-set / boundary-value) not being
  altered in a way that changes what they exercise without renaming.

---

## 4. Condition-3 completion criterion (this design's own proposed gate)

Condition 3 is satisfied **only when ALL FIVE** high-materiality methods
each have at least one fault class with a recorded `DETECTED` result under
this mechanism (once implemented and reviewed) — **no partial aggregate
counts, no averaging, no "4 of 5 is close enough."** A single `SURVIVED`
result on any one method's only attempted fault is itself a genuine,
actionable test-effectiveness gap requiring either a strengthened test (and
re-run) or, failing that, a separate, explicit Product Owner risk-
acceptance naming that specific residual — never silently averaged away by
the other 4 methods' clean results. This mirrors Testing Convention v0.16
§5b's own "each omission must be individually, exactly identified" rule,
applied at the method level for this specific gate.

**Current status against this criterion (design time, no execution yet):**

| Method | Fault(s) planned | Existing test surface | Status |
|---|---|---|---|
| `StaticInputContractAuthorityProvider.resolve` | FI-STATIC-PROVIDER-01 | Existing (2 tests) | Ready to run, no new test needed |
| `OHLCV.field` | FI-OHLCV-FIELD-01/02 | Existing (5 tests) | Ready to run, no new test needed |
| `DecimalPrecisionPolicy.apply` | FI-DECIMAL-APPLY-01/02 | 01: existing (incidental); 02: new test required | FI-01 ready; FI-02 blocked on new test |
| `DecimalPrecisionPolicy.__post_init__` | FI-DECIMAL-POSTINIT-01/02 | New tests required (both) | Blocked on 2 new tests |
| `FeatureDefinition.__post_init__` | FI-FEATUREDEF-01/02/03 | 01/02: existing; 03: new test required | FI-01/02 ready; FI-03 blocked on new test |

**None of the 5 methods currently has an EXECUTED, recorded `DETECTED`
result** — this design only establishes readiness/blockers; a later,
separate implementation transaction must (a) author the identified new
tests, (b) build the harness, (c) execute all fault records, (d) pin the
resulting evidence artifact, before Condition 3 can be marked resolved.

## 5. The 7 lower-materiality excluded methods — current authority requirement (not promoted, not demoted)

Testing Convention v0.16 §5b's fail-closed rule applies to EVERY un-mutated
behavior-bearing unit, not only the 5 named high-materiality ones — the
threshold proposal §4.2 and the remediation plan's own `EVID-03` framing
single out the 5 for THIS gate's own completion criterion (§4 above)
because they are the ones independently assessed as high-materiality with
non-trivial branching; the remaining 7 (`FilesystemInputContractAuthority
Resolver.resolve`, `CandleScope.subject_id`, `EvaluationFrontier.plain_
stream_positions`, `VerifiedInputContractAuthority.__init__`, `FeatureScope.
feature_subject_id`, `SequenceAllocator.next_ref`, `SequenceAllocator.
producer_ref`) remain, under CURRENT authority, **individually-named, OPEN
residuals under the SAME §5b/§5c framework** — they are not exempted, not
silently satisfied by this design's own 5-method scope, and not required to
be resolved by this design's own completion criterion either. Closing them
(if ever pursued) would require the SAME §5c-qualifying evidence (a
supplemental mechanism, fault injection, or Product Owner risk-acceptance)
applied individually to each, exactly as `feature-engine-mutation-
baseline-001-analysis.md` §2 already states — this design neither expands
nor narrows that existing requirement for the 7.

## 6. Checkpoint-002 evidence-fidelity note (recorded, not corrected)

`feature-engine-mutation-full-checkpoint-002.json`'s own `ten_status_
counts` object lists `confirmed_timeout: 0` as a sibling key alongside the
governed ten raw mutmut statuses. Per Testing Convention v0.16 item 8a,
`confirmed_timeout` is NOT one of the ten raw mutmut statuses (the ten are:
`killed`, `survived`, `no_tests`, `not_checked`, `skipped`, `suspicious`,
`timeout`, `caught_by_type_check`, `segfault`, `check_was_interrupted_by_
user`) — it is a SEPARATE, supplemental bookkeeping field this program's
own evidence artifacts have historically nested inside the same JSON object
for convenience, which is non-blocking (its value is correctly `0` and does
not affect `reconciliation`'s own ten-category sum) but is, strictly, a
schema-presentation imprecision. **Per this task's own explicit instruction,
Checkpoint 002 is NOT modified to correct this** — this note is recorded
here as a forward-looking requirement only: any FUTURE formal Step-9/QG
evidence transaction must present the governed ten raw statuses as their
own exact, closed set, with `confirmed_timeout` pinned as a visibly
separate, clearly-labeled supplemental field, never commingled as if an
11th raw status.

## 7. Preserved (unchanged by this design)

```text
Condition 1:                    evidence-ready (Checkpoint 002, raw score
                                87.65512736773351%) -- NOT a formal PASS,
                                unaffected by this design.
Condition 2:                    SATISFIED (170/170) -- unaffected.
Condition 3:                    UNRESOLVED -- remains unresolved until this
                                (or an amended) mechanism is reviewed,
                                approved, AND EXECUTED against all 5
                                methods with a qualifying result each.
P3-FEATURE-QG-EVID-03:         OPEN / blocking (unchanged, not evaluated).
P3-FEATURE-QG-EVID-04..-08:    OPEN / blocking (unchanged, untouched).
Overall Feature Chapter 13 QG: FAIL — evidence (unchanged).
No formal Step-9/QG evaluation performed. No fault injection performed. No
  production/test/tooling file modified. No ADR authored.
Feature module approval:       NOT APPROVED.
Phase 3 Approval Gate:         NOT opened.
LIVE:                           NOT_AUTHORIZED, unreferenced.
```

## 8. Next governed action

**Review A of this design candidate** — an independent reviewer assesses
the selected mechanism, the ADR-scope disposition, and each of the 5
per-method fault-class plans (including the identified new-test
requirements), and either accepts, rejects, or amends this design. Only
after review/approval may a SEPARATE, later implementation transaction
author the proposed new tests, build the harness, execute the fault
records, and pin the resulting evidence artifact toward Condition 3's
resolution. This document performs none of that itself.
