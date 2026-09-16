# Feature Engine — Mutation-Surface Completeness (Condition 3) Design — Amendment 001 (Current-Boundary Target-Population Extension)

```yaml
status: >
  APPROVED — DESIGN AMENDMENT EFFECTIVE for the full current population (9
  methods / 14 faults). FI-INPUTMERGE-POSTINIT-01's ORIGINAL fault spec
  (guard_inversion, new_string "if self.algorithm:") is SUPERSEDED,
  EFFECTIVE 2026-09-16, by Bounded Correction 002's CORRECTED spec
  (fail_closed_bypass, new_string "if self.algorithm is None:"),
  APPROVED — EFFECTIVE per approval_recording_002 below. The ORIGINAL
  spec and its own Product Owner approval (approval_recording_001) remain
  preserved verbatim as historical authority of record for the earlier
  approval/execution boundary — not rewritten, not deleted. No fault has
  yet been executed against the corrected spec by this recording
  transaction.
artifact_id: feature-engine-mutation-surface-completeness-design-001-amendment-001
amends: feature-engine-mutation-surface-completeness-design-001
created_for: >
  Extending the already-approved Condition-3 fault-injection DESIGN (mechanism
  unchanged) from its historical five-method target population to four
  newly-material current-boundary methods identified by the EVID-03
  current-boundary applicability analysis (P3-FEATURE-EVID03-REBASE-A-MAJ-01,
  CLOSED — BOUNDED REVIEW A RE-REVIEW).
transaction_kind: DESIGN ONLY — NOW APPROVED; IMPLEMENTATION NOT YET PERFORMED
production_changed: false
tests_changed: false
tooling_changed: false
fault_injection_performed: false
formal_step9_qg_evaluation_performed: false
evid_03_closed: false
condition_3_closed: false
repository_head_at_authoring: b5014955c77964a9a5ceb0f22a1b79a297be595b
bounded_correction_001:
  applied_at_repository_head: dd2a923f0283e9b2cbb73d3085c699c61e3d834f
  reviewer_finding_addressed: P3-FEATURE-EVID03-COND3-AMEND-A-MIN-01
  finding_status: "CLOSED — BOUNDED REVIEW A RE-REVIEW"
approval_recording_001:
  recorded_at_repository_head: db37fa3eec53f7150c58659d4bd82bf1c251d07d
  review_a:
    reviewer: "ChatGPT — AI Technical Architect / Review A"
    reviewed_boundary: db37fa3eec53f7150c58659d4bd82bf1c251d07d
    performed_by: "external to this recording transaction — this transaction only transcribes the completed review's own outcome"
    closures:
      - id: P3-FEATURE-EVID03-COND3-AMEND-A-MIN-01
        status: "CLOSED — BOUNDED REVIEW A RE-REVIEW"
    counts: { blocker: 0, major: 0, minor: 0 }
    disposition: "CLEAN — READY_FOR_RISK_CLASSIFICATION"
  risk_classification: "R1"
  review_b: "NOT REQUIRED"
  adr_disposition: "ADR_OPTIONAL — ADR NOT AUTHORED"
  product_owner_decision:
    verbatim: "APPROVE Feature Engine EVID-03 Condition-3 Current-Boundary Fault-Spec Amendment 001 at boundary db37fa3eec53f7150c58659d4bd82bf1c251d07d."
    authority: "Product Owner — sole approval authority"
  approved_scope: "The 4 new current-boundary target methods (contracts.PreparedTransition.reconcile, contracts.PreparedFeatureComputed.finalize, contracts.InputMergePolicy.__post_init__, ownership.AuthoritativeSubjectOwner.state) and their 4 exact fault specifications (FI-PREPTRANS-RECONCILE-01, FI-PFC-FINALIZE-01, FI-INPUTMERGE-POSTINIT-01, FI-OWNER-STATE-01). The historical 5-method/10-fault design (feature-engine-mutation-surface-completeness-design-001.md) remains unchanged, not reapproved, not reopened."
execution_finding_001:
  finding_id: P3-FEATURE-EVID03-COND3-EXEC-A-MAJ-01
  observed_boundary: cda4d0ebaf0f1d9e71bb4be0205380059db7a68b
  observed_result: "13/14 DETECTED; FI-INPUTMERGE-POSTINIT-01 = TEST_INFRA_ERROR (evidence_exit_code=4)"
  cause: "The approved fault's 'valid non-empty algorithm now wrongly raises' direction makes tests/conftest.py's own real, valid InputMergePolicy construction (module-import time, before any test collection) raise -- pytest never collects a single test."
  disposition: "Executor STOP was correct. No formal evidence-003 committed. Design fault-spec correction required before this one fault can be re-executed."
  executor_stop: "CONFIRMED CORRECT — REVIEW A P3-FEATURE-EVID03-COND3-EXEC-A-MAJ-01, REVISION_REQUIRED, 0 Blocker / 1 Major / 0 Minor, R1"
bounded_correction_002_candidate:
  status: "CANDIDATE — PENDING REVIEW A"
  candidate_repository_head: cda4d0ebaf0f1d9e71bb4be0205380059db7a68b
  addresses_finding: P3-FEATURE-EVID03-COND3-EXEC-A-MAJ-01
  scope: "FI-INPUTMERGE-POSTINIT-01 fault specification ONLY — target method, fault ID, and target population (9 methods / this fault's own membership) unchanged; harness/mechanism unchanged; no other fault spec touched"
  supersedes_pending_approval: "The ORIGINAL FI-INPUTMERGE-POSTINIT-01 spec recorded under approval_recording_001 above (old_string: \"if not self.algorithm:\", new_string: \"if self.algorithm:\") -- that original spec and its Product Owner approval remain PRESERVED, VERBATIM, as historical authority; this correction does not rewrite or retroactively reinterpret that approval as having covered the corrected spec"
  requires_before_use_as_evidence: "Review A, Risk Classification, and a fresh Product Owner decision -- self-approval prohibited"
approval_recording_002:
  recorded_at_repository_head: 89471f41b2518b7c96860b13a550670a4ed50066
  review_a:
    reviewer: "ChatGPT — AI Technical Architect / Review A"
    reviewed_boundary: 89471f41b2518b7c96860b13a550670a4ed50066
    performed_by: "external to this recording transaction — this transaction only transcribes the completed review's own outcome"
    result: "CLEAN — 0 Blocker / 0 Major / 0 Minor"
  risk_classification: "R1"
  review_b: "NOT REQUIRED"
  adr_disposition: "ADR_NOT_REQUIRED"
  product_owner_decision:
    verbatim: "APPROVE Feature Engine EVID-03 Condition-3 Amendment 001 Bounded Correction 002 for FI-INPUTMERGE-POSTINIT-01 at boundary 89471f41b2518b7c96860b13a550670a4ed50066, with corrected new_string \"if self.algorithm is None:\" and fault_class \"fail_closed_bypass\"."
    authority: "Product Owner — sole approval authority"
  effective_spec:
    fault_id: FI-INPUTMERGE-POSTINIT-01
    method: contracts.InputMergePolicy.__post_init__
    source_file: src/feature_engine/contracts.py
    fault_class: fail_closed_bypass
    old_string: "if not self.algorithm:"
    new_string: "if self.algorithm is None:"
  finding_state: { id: P3-FEATURE-EVID03-COND3-EXEC-A-MAJ-01, status: "CLOSED — DESIGN CORRECTION APPROVED" }
  bounded_correction_002_state: "APPROVED — EFFECTIVE"
  current_approved_condition_3_population: "9 methods / 14 faults"
  not_yet_performed: "No fault executed against the corrected spec by this recording transaction. Implementation (tooling/fault_injection/faults.py) and a fresh 14-fault execution against a new executable boundary are separate, subsequent transaction steps."
```

**Approval recording (this revision, mechanical only):** ChatGPT bounded Review A re-review of the amendment 001 correction closed `P3-FEATURE-EVID03-COND3-AMEND-A-MIN-01` — `CLEAN — 0 Blocker / 0 Major / 0 Minor`, Risk Classification `R1`, Review B `NOT REQUIRED`, `ADR_OPTIONAL` (ADR not authored, unchanged from the candidate's own §6 classification). The Product Owner then recorded an explicit APPROVE decision at this exact boundary. This transaction performed none of those steps itself — it only mechanically transcribes their already-completed outcomes. **This amendment's DESIGN is now `APPROVED — DESIGN AMENDMENT EFFECTIVE`.** Approval covers the DESIGN/fault-specification content only — it does **not** itself execute any fault, does not add or modify any test, and does not close Condition 3 or `P3-FEATURE-QG-EVID-03`. A separate, later implementation transaction (tracked in this same executor task, Part B/C below) still builds the tooling extension and runs the now-approved population before any Condition-3 evidence exists at the current boundary.

**Bounded Correction 002 — approval recording (mechanical only, `approval_recording_002` above):** ChatGPT Review A of the correction candidate returned `CLEAN — 0 Blocker / 0 Major / 0 Minor`, Risk Classification `R1`, Review B `NOT REQUIRED`, `ADR_NOT_REQUIRED` (ADR not authored). The Product Owner then recorded an explicit APPROVE decision at this exact boundary (verbatim above). This transaction performs none of those steps itself — it only mechanically transcribes their already-completed outcomes. **`P3-FEATURE-EVID03-COND3-EXEC-A-MAJ-01` is now `CLOSED — DESIGN CORRECTION APPROVED`. Bounded Correction 002 is now `APPROVED — EFFECTIVE`.** The current authoritative `FI-INPUTMERGE-POSTINIT-01` specification is the corrected one (`fault_class: fail_closed_bypass`, `new_string: "if self.algorithm is None:"`) — the current approved Condition-3 population is **9 methods / 14 faults**. This approval covers the corrected fault SPECIFICATION only — it does **not** itself execute any fault; no fault has been run against the corrected spec by this recording transaction. A separate, later implementation transaction (tracked in this same executor task, Part B/C below) updates `tooling/fault_injection/faults.py` and runs the full 14-fault population against a fresh executable boundary before any Condition-3 evidence exists.

**Bounded correction 001:** ChatGPT bounded Review A returned
`REVISION_REQUIRED — 0 Blocker / 0 Major / 1 Minor` (R1):
`P3-FEATURE-EVID03-COND3-AMEND-A-MIN-01` — `FI-OWNER-STATE-01` was
incorrectly classified `GAP`; the fault itself was valid, but a fresh
re-read of `tests/test_ownership.py` shows two existing tests already
exercise the exact handle-less branch this fault corrupts, requiring no
new test. §3.4 and the §3 test-readiness summary below are corrected
in place (candidate not yet approved — corrected directly, not via a
separate Amendment-002/correction artifact, per this task's own
instruction). `FI-PREPTRANS-RECONCILE-01`/`FI-PFC-FINALIZE-01`/
`FI-INPUTMERGE-POSTINIT-01` are unaffected, not reopened. No target
method, fault ID, `old_string`/`new_string`, materiality classification,
the candidate total (9 methods), the historical five-target design, the
harness semantics, `ADR_SCOPE_DISPOSITION` (`ADR_OPTIONAL`), or any
historical evidence is altered by this correction. **Finding state:**
`CLOSED — BOUNDED REVIEW A RE-REVIEW` (see approval recording below —
this candidate is now `APPROVED — DESIGN AMENDMENT EFFECTIVE`).

This document does **not** modify, rewrite, or supersede
`feature-engine-mutation-surface-completeness-design-001.md` — that document,
its 5-method target population, its 10 approved fault specs, its Review
A/Review B/Product Owner approval record, and `evidence-002.json`'s executed
results all remain byte-unchanged and fully valid for their own pinned
boundary (`5e8b1a884d67031c68596378c33e49d82c18532c`/
`35a4e5f281b38718602c2a0b4ef8ae08c7a76807`). This is a **separate, additive**
candidate: four NEW target methods and four NEW fault specifications only.
It is authored, not approved — **no fault is executed, no test is added, no
production file is touched, and Condition 3 is not marked resolved by this
document.**

## Execution finding `P3-FEATURE-EVID03-COND3-EXEC-A-MAJ-01` and bounded correction 002 (candidate)

**Execution finding, ChatGPT Review A — `REVISION_REQUIRED — 0 Blocker / 1 Major / 0 Minor` (R1):** the approved 14-fault population was executed against implementation boundary `cda4d0ebaf0f1d9e71bb4be0205380059db7a68b` (a separate tooling-implementation commit, not this document). Result: **13/14 DETECTED**, 0 SURVIVED, 0 CONTROL_FAILED, 0 INJECTION_FAILED, **1 TEST_INFRA_ERROR** — `FI-INPUTMERGE-POSTINIT-01` (`evidence_exit_code=4`). **Root cause, confirmed by direct, reproducible manual verification (disposable isolated checkout, not the formal harness, canonical checkout untouched):** the approved fault's second direction — a genuinely valid, non-empty `algorithm` now wrongly raising `UnsupportedMergePolicyError` — makes `tests/conftest.py`'s own real, module-level `InputMergePolicy` construction (via `resolve_input_contract_authority_from_repository` → `_extract_merge_policy`, executed at test-COLLECTION time, before any test runs) raise on import. pytest never collects a single test and exits with a conftest-load `ImportError` (code 4) — correctly, per the approved harness's own unmodified contract (`classify_verdict`: any exit code outside `{0, 1}` is `TEST_INFRA_ERROR`, never coerced into `DETECTED`/`SURVIVED`), classified `TEST_INFRA_ERROR`, never `DETECTED`. **The Executor's STOP after this run was correct — no formal `evidence-003.json` was committed; the raw run remains non-qualifying diagnostic evidence, not committed to this repository.** No other fault, and no target method's own DETECTED status among the other 8 methods, is affected or reopened by this finding.

**Why this is a bounded DESIGN correction, not a contextual `old_string`/`new_string` adjustment:** the originally-approved fault deliberately inverted the guard in BOTH directions (empty accepted; valid rejected) — a genuine two-directional `guard_inversion`. The corrected fault below changes the defect's own shape (a one-directional, narrowly-targeted acceptance-of-invalid-input, not a symmetric inversion) and its honest `fault_class` label changes accordingly. Per this repository's own established precedent (contextual re-pointing of an `old_string`/`new_string` at drifted line numbers does not require new governance; a change to what the fault MEANS does), this is treated as a bounded semantic correction requiring its own Review A / Risk Classification / Product Owner decision before use — exactly the same discipline `bounded_correction_001` above already applied to `FI-OWNER-STATE-01`'s readiness classification.

**Corrected `FI-INPUTMERGE-POSTINIT-01` fault specification (CANDIDATE — not yet approved):**

```text
fault_id:              FI-INPUTMERGE-POSTINIT-01 (unchanged)
qualified_method:      contracts.InputMergePolicy.__post_init__ (unchanged)
source_file:            src/feature_engine/contracts.py (unchanged)
fault_class:            fail_closed_bypass (CORRECTED from guard_inversion --
                        see rationale below; matches the existing taxonomy
                        term already used for the structurally identical
                        FI-OHLCV-FIELD-02 shape: one specific invalid input
                        silently escapes an otherwise-intact fail-closed
                        guard, rather than the guard's direction inverting
                        symmetrically for both valid and invalid inputs)
old_string:              "if not self.algorithm:" (unchanged from the
                        original approved spec -- still unique, verified
                        fresh: occurs exactly once in contracts.py)
new_string (CORRECTED): "if self.algorithm is None:"
  (was: "if self.algorithm:")
semantic_defect (corrected): narrows the guard's trigger condition from
  "falsy" (empty string OR None) to "literally None only". Traced exactly,
  fresh, against current source:
  - algorithm="" (the intended defect target): "" is None -> False -> guard
    does NOT fire -> EMPTY algorithm SILENTLY ACCEPTED (exactly, and only,
    the intended material defect).
  - algorithm=<any genuine non-empty string> (the ordinary/valid case,
    including every real construction in tests/conftest.py via
    authority_resolver.py's own _extract_merge_policy, which itself
    already guards `if algorithm is None ... : return None` BEFORE ever
    constructing InputMergePolicy -- so algorithm reaching __post_init__
    from that path is always a genuine, non-None, non-empty string):
    <string> is None -> False -> guard does NOT fire -> construction
    succeeds, IDENTICAL to unfaulted behavior. This is the fix: the
    "valid non-empty algorithm wrongly rejected" direction is eliminated
    entirely -- conftest.py's own module-level construction can never
    observe this fault, so test collection can never be broken by it.
  - algorithm=None (type-illegal for the `algorithm: str` field; not a
    realistic runtime input given mypy --strict and the resolver's own
    None-guard above; included only for completeness): both original and
    corrected code raise identically -- no behavior change for this
    unreachable case.
activation_uniqueness:  old_string verified fresh: exactly one occurrence
                        in contracts.py. new_string ("if self.algorithm is
                        None:") verified fresh: zero occurrences anywhere
                        in contracts.py before patch, so exactly one after
                        a single-token replacement.
predicted_detecting_test: tests/test_contracts.py::
                        test_input_merge_policy_rejects_empty_algorithm
                        (pytest.raises(UnsupportedMergePolicyError) around
                        InputMergePolicy(algorithm="", ...) -- would no
                        longer raise under the corrected fault, so this
                        test FAILS -- DETECTED).
required_positive_control: tests/test_contracts.py::
                        test_input_merge_policy_accepts_well_formed_value
                        MUST continue to pass unaffected under the
                        corrected fault (traced above: a valid algorithm
                        never triggers the narrowed guard) -- this is the
                        exact regression the corrected spec is designed to
                        eliminate, verified by direct source tracing, not
                        assumed.
conftest_collision_eliminated: yes -- traced exactly above via
                        authority_resolver.py's own _extract_merge_policy
                        None-guard; no live/formal re-execution performed
                        by this correction transaction (PROHIBITED --
                        deferred to a later, separately-approved
                        implementation/rerun transaction).
```

**Fresh Chapter 0 §4b ADR Scope Rule (this one-fault correction, not inherited from Amendment 001's own `ADR_OPTIONAL`):**

| §4b criterion | Applies here? |
|---|---|
| Platform Invariant / Event Schema / Module Taxonomy change | No. |
| Governance/Approval-process change | No — reuses the identical, already-established evidentiary-design pattern (a named fault targeting a named method's fail-closed guard, per design-001 §3's own template); corrects ONE fault's own semantic defect, invents no new mechanism, process, role, or review stage. |
| Affects >1 module | No — `feature-engine` only, one method, one fault ID. |
| Hard to reverse | No — a documentation-only candidate correction; trivially revisable/re-correctable again if wrong. |
| Locked-ADR modification | No. |

**Disposition: `ADR_NOT_REQUIRED`.** This is narrower than Amendment 001's own `ADR_OPTIONAL` (which introduced 4 wholly new target methods/faults) and narrower still than design-001's own `ADR_OPTIONAL` (which introduced the entire mechanism) — this correction touches exactly one already-approved fault ID's own `new_string`/`fault_class`, using the identical, unmodified template and mechanism. No ADR authored.

**Approval requirement (not self-approved by this transaction):** Review A REQUIRED. Risk Classification REQUIRED. Product Owner decision REQUIRED before this corrected spec may be implemented in `tooling/fault_injection/faults.py` or used to produce Condition-3 evidence. Review B NOT REQUIRED by default (matches the risk/review pattern already applied to `bounded_correction_001` and to Amendment 001 itself). This candidate is **not** implemented in tooling by this transaction, and the previously-approved (now superseded-pending-approval) original spec's own historical Product Owner approval record (`approval_recording_001`) is preserved byte-verbatim above, not rewritten.

**Current executable state at the time this correction was authored (superseded by approval, see `approval_recording_002` above):** implementation Commit B (`cda4d0ebaf0f1d9e71bb4be0205380059db7a68b`, `tooling/fault_injection/faults.py`, etc.) truthfully implemented the then-approved ORIGINAL `FI-INPUTMERGE-POSTINIT-01` spec and is preserved as the historical stopped-execution boundary. Bounded Correction 002 has now been reviewed and approved (`approval_recording_002` above) — the corrected spec is `APPROVED — EFFECTIVE`, not yet implemented in `tooling/fault_injection/faults.py`, not yet executed. A separate, later implementation transaction updates exactly `FI-INPUTMERGE-POSTINIT-01` in `faults.py` and re-runs all 14 faults against a fresh executable boundary.

**Next governed step:** implement the approved corrected `FI-INPUTMERGE-POSTINIT-01` spec in `tooling/fault_injection/faults.py` and execute the full 14-fault population against a fresh executable boundary, producing formal current-boundary Condition-3 evidence — pending its own subsequent Review A.

## 0. Authority resolved fresh this transaction

- `feature-engine-mutation-surface-completeness-design-001.md` §2/§2.1/§2.1a
  (Approved mechanism — isolated checkout, clean-control contract, five-way
  fail-closed verdict enum, evidence-record schema) — reused **unchanged**,
  not redesigned.
- `feature-engine-mutation-surface-completeness-design-001.md` §3.1–3.5, §5
  (the 5 approved targets + their 10 fault specs; the "7 lower-materiality
  residuals, not promoted" rule) — the template this amendment follows.
- The EVID-03 current-boundary applicability analysis and its bounded
  correction (`P3-FEATURE-EVID03-REBASE-A-MAJ-01`/`-MIN-01`, both **CLOSED —
  BOUNDED REVIEW A RE-REVIEW**, Review A CLEAN 0/0/0, Risk R1) — the source
  of the 4 candidate methods below; NOT reopened by this document.
- Current exact Feature Engine source — `src/feature_engine/contracts.py`
  (blob `0d2e39bffb705a2b1f903cd1a54b5f099ae6a686`), `src/feature_engine/
  ownership.py` (blob `1c02cb21cf73442fb08ec3d2b3d0d912edf09baa`), at
  repository HEAD `b5014955c77964a9a5ceb0f22a1b79a297be595b` — read directly
  and in full for §2/§3 below, not trusted from any prior summary.

## 1. Step 1 — Re-verification of the original five targets (compatibility check, no redesign)

All five re-read directly at current HEAD, `src/feature_engine/{authority_resolver,candle,contracts}.py`:

| Method | Still exists? | Semantic intent unchanged? | Historical fault spec's exact activation string still matches current source? | Historical fault class still meaningful? |
|---|---|---|---|---|
| `authority_resolver.StaticInputContractAuthorityProvider.resolve` | Yes (line 557, class; line 567, method) | Yes — identical docstring/body | Yes — `if self.authority.feature_computation_profile != profile:` present verbatim | Yes |
| `candle.OHLCV.field` | Yes (line 45/54) | Yes | Yes — 4-way `if name == "..."` dispatch + trailing `raise ValueError(f"unsupported reference_price_field: {name!r}")` present verbatim | Yes |
| `contracts.DecimalPrecisionPolicy.apply` | Yes (line 828/842) | Yes | Yes — `Decimal(1).scaleb(-self.digits)` / `rounding=self.rounding` present verbatim | Yes |
| `contracts.DecimalPrecisionPolicy.__post_init__` | Yes (line 828/836) | Yes | Yes — `self.digits < 0` / `self.rounding not in _VALID_ROUNDINGS` present verbatim | Yes |
| `contracts.FeatureDefinition.__post_init__` | Yes (line 848) | Yes | Yes — re-counted fresh via `sed -n '848,1003p' contracts.py \| grep -c "raise InvalidFeatureDefinitionError"` = **27** (matches design-001's own corrected count exactly); `correction_policy != CORRECTION_POLICY`, the `distance_only_fields ... or self.normalization_policy is not None` OR-chain, and `window_candle_count is None or self.window_candle_count < 1` (FI-01/02/03's exact activation targets) all present verbatim | Yes |

**No compatibility issue found.** Line numbers have drifted (unrelated additions elsewhere in `contracts.py`/`authority_resolver.py`), but every historical fault spec's exact `old_string` activation target is present, unique, and semantically unchanged. All five historical fault specs remain reusable **as-is**, without amendment. This amendment does not touch §3.1–3.5 of design-001.

## 2. Step 2 — Re-verification of the four new candidates

### 2.1 `contracts.PreparedTransition.reconcile`

- **Behavior-bearing:** Yes — two distinct fail-closed guards: a batch-length-mismatch check and a per-element content-mismatch check, both raising `CanonicalHistoryMismatchError` (ADR-043 §C catch-up invariant).
- **Materiality: HIGH** — same class of invariant as the 5 already-approved guards (construction/consistency validation protecting a Chapter-8/ADR-043 correctness property), not a cosmetic or message-only unit.
- **Covered by one of the 5 approved targets?** No.
- **Existing approved fault spec directly applies?** No — none of the 10 existing `old_string`/`new_string` pairs exist in this method; a new spec is required.
- **New fault spec needed:** Yes (below).
- **Masking finding (direct source verification, `ownership.py` lines 594–606):** `AuthoritativeSubjectOwner._catch_up` — the SOLE production caller of `PreparedTransition.reconcile` — performs its OWN pre-check immediately before calling `reconcile`: `if len(batch) != batch_size: raise CanonicalHistoryMismatchError(...)`. This means `batch` handed to `reconcile()` is *always* exactly the expected length by construction — `reconcile`'s own internal length-mismatch guard is **masked/unreachable** via the only real call path, exactly the same masking pattern design-001's own `P3-PY-MUT-COND3-A-MAJ-03` finding identified for `StaticInputContractAuthorityProvider.resolve`. The **content-mismatch** guard (`_prepared_matches_canonical`) is NOT similarly pre-checked by the caller and IS reachable/exercised.

### 2.2 `contracts.PreparedFeatureComputed.finalize`

- **Behavior-bearing:** Yes — one real conditional: `if self.preceding_batch_invalidation_causation: if invalidation_ref is None: raise ValueError(...); causation_refs = (*causation_refs, invalidation_ref)`.
- **Materiality: MODERATE-HIGH** — a silent corruption of `causation_refs` (an ADR-043 lineage/causation-correctness field feeding directly into every emitted `FeatureComputed`) is a genuine, non-cosmetic defect class.
- **Covered by one of the 5?** No.
- **Existing spec applies?** No — new spec required.
- **New fault spec needed:** Yes (below).

### 2.3 `contracts.InputMergePolicy.__post_init__`

- **Behavior-bearing:** Yes — two guards: `if not self.algorithm: raise UnsupportedMergePolicyError(...)`; `if not self.concurrent_tie_break: raise UnsupportedMergePolicyError(...)`.
- **Materiality: MODERATE** — directly analogous in shape/size to the already-approved `DecimalPrecisionPolicy.__post_init__` (also exactly 2 simple non-empty-value guards, already judged high-materiality by design-001) — a `merge_policy` accepted with an empty algorithm/tie-break tuple is a genuine ADR043-IMPLDESIGN-A-MAJ-04 P_run tie-break-authority integrity defect, not cosmetic.
- **Covered by one of the 5?** No.
- **Existing spec applies?** No — new spec required.
- **New fault spec needed:** Yes (below).

### 2.4 `ownership.AuthoritativeSubjectOwner.state` (property)

- **Behavior-bearing:** Yes — `return self._handle.state if self._handle is not None else SubjectOwnershipState.INACTIVE`, a real None-guarded branch over a 4-member enum (`INACTIVE`/`CATCHING_UP`/`ACTIVE`/`REVOKED`).
- **Materiality: MODERATE** — a materially wrong lifecycle-state report (e.g. an owner with no handle silently reporting `ACTIVE`) is a genuine observable defect in the same ownership-lifecycle domain EVID-06's own fault-injection evidence already treats as safety-relevant; not textual/cosmetic.
- **Covered by one of the 5?** No.
- **Existing spec applies?** No — new spec required.
- **New fault spec needed:** Yes (below).

**No other omitted method is promoted by this amendment.** `PreparedFeatureFactInvalidated.finalize` (re-confirmed: pure straight-line dataclass construction, zero conditional branches), `VerifiedOutputEventContractAuthority.__init__` (re-confirmed: unconditional `raise TypeError`, structurally identical to `VerifiedInputContractAuthority.__init__`, which design-001 §5 itself already places in the 7 lower-materiality "not promoted" bucket), `SubjectOwnershipRegistry.get`/`.set` (pure dict-wrapper, no guard), and the Protocol `...` stubs / trivial passthrough `@property` accessors all remain correctly recorded in the full mutation-surface omission inventory but are **not** promoted to evidence targets — fresh inspection found no material error in the prior bounded analysis for any of these.

## 3. Proposed fault specifications (design-001 §2.1b template, unamended)

Fault-ID vocabulary extended coherently: `FI-{METHOD-SLUG}-{NN}`, four new slugs (`PREPTRANS-RECONCILE`, `PFC-FINALIZE`, `INPUTMERGE-POSTINIT`, `OWNER-STATE`), none colliding with the existing ten (`STATIC-PROVIDER`, `OHLCV-FIELD`, `DECIMAL-APPLY`, `DECIMAL-POSTINIT`, `FEATUREDEF`).

**Minimality note:** one fault per new target (not two), following the task's own "do not force two faults per method merely because the historical five happened to have ten total faults" instruction — each method here has exactly one clearly dominant, cleanly-attributable material defect class; a second candidate fault existed for two of the four methods (`reconcile`'s length-guard; `finalize`'s guard-inversion direction) but was excluded from this minimal amendment as lower-value/less-cleanly-attributable than the chosen one (documented per-method above/below), not overlooked.

---

### 3.1 `FI-PREPTRANS-RECONCILE-01` — content-mismatch guard inversion

```text
fault_id:            FI-PREPTRANS-RECONCILE-01
qualified_method:    contracts.PreparedTransition.reconcile
source_file:          src/feature_engine/contracts.py
fault_class:          guard_inversion (content-mismatch bypass)
semantic_defect:      Inverts the per-element canonical-content match check so
                       a genuinely MISMATCHED recomputed candidate is silently
                       ACCEPTED (never raises CanonicalHistoryMismatchError),
                       while a genuinely MATCHING candidate now wrongly
                       raises -- both directions of ADR-043 §C's fail-closed
                       catch-up reconciliation invariant break simultaneously.
old_string:            "if not _prepared_matches_canonical(prepared, canonical):"
new_string:            "if _prepared_matches_canonical(prepared, canonical):"
activation_uniqueness: exact string occurs exactly once in contracts.py
                       (verified: grep -c returns 1)
detecting_test(s):     tests/test_ownership.py::test_catch_up_mismatch_fails_closed
                       (tampers a canonical value's own `value` field via
                       dataclasses.replace before registering it as the
                       canonical record, then asserts
                       pytest.raises(CanonicalHistoryMismatchError) from
                       owner.acquire_and_activate -- this reaches `reconcile`
                       with a LENGTH-matching but CONTENT-mismatched batch,
                       exercising exactly the guard this fault targets)
readiness:             READY -- existing test already exercises this exact
                       guard with a content-tampered canonical value.
why_detection_matters: A silently-accepted content mismatch during historical
                       catch-up would hydrate `_lineage` from an UNVERIFIED
                       recomputed candidate rather than genuinely-canonical
                       history -- exactly the "catch-up fails closed rather
                       than preferring either source" invariant the method's
                       own docstring names as its purpose.
```

**Documented, not promoted:** `reconcile`'s OWN internal length-mismatch guard (`len(canonical_tuple) != len(self.prepared_events)`) is currently masked/unreachable via the only production call path (`AuthoritativeSubjectOwner._catch_up`'s own pre-check intercepts any length mismatch first, §2.1 above) — a genuine finding, but not promoted to a required fault in this minimal amendment; a future transaction wanting full guard-shape parity would need a NEW direct test that calls `prepared.reconcile(...)` directly, bypassing `_catch_up`, mirroring the `FI-STATIC-PROVIDER-01` direct-call pattern.

---

### 3.2 `FI-PFC-FINALIZE-01` — dropped same-batch causation-ref append

```text
fault_id:            FI-PFC-FINALIZE-01
qualified_method:    contracts.PreparedFeatureComputed.finalize
source_file:          src/feature_engine/contracts.py
fault_class:          silent_corruption (dropped tuple element)
semantic_defect:      When preceding_batch_invalidation_causation is True,
                       the final causation_refs silently OMITS the preceding
                       same-batch invalidation's own ref -- no exception, no
                       observable difference except the returned
                       FeatureComputed's own causation_refs field content.
old_string:            "causation_refs = (*causation_refs, invalidation_ref)"
new_string:            "causation_refs = (*causation_refs,)"
activation_uniqueness: exact string occurs exactly once in contracts.py
                       (verified: grep -c returns 1)
detecting_test(s):     tests/test_swing_distance.py::
                       test_causation_refs_for_reattempt_and_preempt_replacements_are_asserted
                       (asserts set(final.causation_refs) - set(final.
                       input_fact_refs) == {preempt_invalidation.ref}) and
                       the adjacent same-batch replacement assertion at
                       tests/test_swing_distance.py line 974
                       (assert replacement.causation_refs ==
                       (*replacement.input_fact_refs, invalidation.ref))
readiness:             READY -- existing tests directly, exactly assert the
                       invalidation ref's presence in the finalized
                       causation_refs tuple.
why_detection_matters: causation_refs is the ADR-043 lineage-audit field
                       proving WHY a Feature value changed; a silently
                       dropped invalidation ref breaks lineage
                       reconstructability for that specific replacement
                       event with no other observable symptom.
```

**Documented, not promoted:** the sibling `if invalidation_ref is None: raise ValueError(...)` guard-inversion direction (breaking the normal path by raising when a valid `invalidation_ref` IS supplied) was considered and excluded from this minimal amendment — it would produce only broad, non-uniquely-attributable breakage across nearly every same-batch invalidate-then-replace test, materially less clean than `FI-PFC-FINALIZE-01`'s own directly-targeted assertions.

---

### 3.3 `FI-INPUTMERGE-POSTINIT-01` — empty-algorithm guard bypass

```text
fault_id:            FI-INPUTMERGE-POSTINIT-01
qualified_method:    contracts.InputMergePolicy.__post_init__
source_file:          src/feature_engine/contracts.py
fault_class:          guard_inversion
semantic_defect:      Inverts the non-empty-algorithm check so an EMPTY
                       algorithm string is silently ACCEPTED (never raises
                       UnsupportedMergePolicyError), while a genuinely
                       non-empty algorithm now wrongly raises -- a
                       structurally invalid InputMergePolicy (no tie-break
                       authority algorithm named at all) becomes constructible.
old_string:            "if not self.algorithm:"
new_string:            "if self.algorithm:"
activation_uniqueness: exact string occurs exactly once in contracts.py
                       (verified: grep -c returns 1)
detecting_test(s):     tests/test_contracts.py::
                       test_input_merge_policy_rejects_empty_algorithm
                       (pytest.raises(UnsupportedMergePolicyError) around
                       InputMergePolicy(algorithm="", ...)) and
                       tests/test_contracts.py::
                       test_input_merge_policy_accepts_well_formed_value
                       (asserts a non-empty algorithm constructs successfully
                       -- would wrongly raise under this fault's other
                       direction)
readiness:             READY -- both existing tests, found by fresh
                       inspection (tests/test_contracts.py lines 97-110),
                       directly and cleanly exercise this exact guard in
                       both directions.
why_detection_matters: merge_policy.algorithm is the P_run tie-break
                       authority (Chapter 8 §8.3.4, ADR043-IMPLDESIGN-A-MAJ-04)
                       -- an empty value silently accepted here means a
                       structurally unusable policy reaches downstream
                       ordering logic with no construction-time signal.
```

**Documented, not promoted:** the sibling `concurrent_tie_break`-emptiness guard was considered (also directly tested,
`test_input_merge_policy_rejects_empty_concurrent_tie_break`) and excluded from this minimal amendment as the second instance
of the SAME guard *shape* (non-empty-value check) already represented by `FI-INPUTMERGE-POSTINIT-01` — not a distinct defect
class, unlike `DecimalPrecisionPolicy.__post_init__`'s own two guards, which the approved design already treats as one
representative pair; a future amendment may add it if reviewers want full guard-shape parity.

---

### 3.4 `FI-OWNER-STATE-01` — no-handle lifecycle-state misreport (readiness corrected: READY, `P3-FEATURE-EVID03-COND3-AMEND-A-MIN-01`)

```text
fault_id:            FI-OWNER-STATE-01
qualified_method:    ownership.AuthoritativeSubjectOwner.state
source_file:          src/feature_engine/ownership.py
fault_class:          silent_corruption (wrong enum constant)
semantic_defect:      An owner instance with NO handle (never activated, or
                       otherwise handle-less) silently reports its own
                       lifecycle state as ACTIVE instead of INACTIVE -- a
                       materially incorrect exclusivity/lifecycle observation,
                       not a textual change.
old_string:            "return self._handle.state if self._handle is not None else SubjectOwnershipState.INACTIVE"
new_string:            "return self._handle.state if self._handle is not None else SubjectOwnershipState.ACTIVE"
activation_uniqueness: exact full-line string occurs exactly once in
                       ownership.py (verified: grep -c returns 1; the
                       structurally similar line at ownership.py:729 uses a
                       distinct "current_state = " prefix, not matched)
detecting_test(s):     tests/test_ownership.py::
                       test_acquire_and_activate_rejects_a_non_pristine_engine
                       (line 571-574: owner is freshly constructed, line
                       571's pytest.raises(EngineNotPristineForCatchUpError)
                       fires from the pristine-engine guard BEFORE any handle
                       is ever assigned -- line 574's own comment confirms
                       "no generation was ever minted" -- then line 573
                       asserts owner.state is not SubjectOwnershipState.
                       ACTIVE) and tests/test_ownership.py::
                       test_acquire_and_activate_fails_closed_on_invalid_frontier_even_with_proven_empty_history
                       (line 697-706: owner is freshly constructed, line
                       703's pytest.raises(RegistryContractMismatchError)
                       fires from the frontier-validation guard BEFORE any
                       handle is assigned -- line 707 confirms
                       owner._committed_frontier is None -- then line 706
                       asserts state_after_failure is not
                       SubjectOwnershipState.ACTIVE). Corroborating,
                       non-primary: the same "state is not ACTIVE"
                       assertion pattern also recurs at lines 921
                       (test_absent_provider_history_cannot_activate) and
                       1008 (test_catch_up_mismatch_fails_closed).
readiness:             READY (corrected -- Review A finding
                       P3-FEATURE-EVID03-COND3-AMEND-A-MIN-01) -- fresh
                       re-read of tests/test_ownership.py confirms owner has
                       genuinely NO handle/generation at both cited
                       assertion points (verified directly: the rejecting
                       guard in each case fires strictly before any handle
                       assignment, not merely before successful activation),
                       so both already exercise exactly the `self._handle is
                       None` branch this fault corrupts. Under this fault
                       (INACTIVE -> ACTIVE in that branch), owner.state
                       would return ACTIVE at both assertion points,
                       directly failing `assert owner.state is not
                       SubjectOwnershipState.ACTIVE` / `assert
                       state_after_failure is not SubjectOwnershipState.
                       ACTIVE`. No new test is required.
minimum_test_required: NONE.
why_detection_matters: `.state` is the public lifecycle-observation surface
                       other code/tests read to decide whether ownership
                       exclusivity may be assumed; silently reporting ACTIVE
                       for a handle-less owner is the exact class of defect
                       an ownership-exclusivity fail-safe mechanism must
                       never exhibit (same domain as EVID-06's own I-6
                       fault-injection evidence).
```

## 4. Candidate target population after this amendment

```text
Historical approved target population:  5 methods (design-001, unchanged,
                                         re-verified compatible, §1 above)
New candidate target population:        4 methods (§2-3 above)
Candidate total after amendment:        9 material methods

This 9 is a CURRENT-BOUNDARY CANDIDATE population only. It does not rewrite,
supersede, or reinterpret feature-engine-mutation-surface-completeness-
evidence-002.json, which remains valid, unmodified evidence for its own
pinned historical boundary and its own 5-method/10-fault scope.
```

**Test-readiness summary (corrected — `P3-FEATURE-EVID03-COND3-AMEND-A-MIN-01`):** `FI-PREPTRANS-RECONCILE-01` READY, `FI-PFC-FINALIZE-01` READY, `FI-INPUTMERGE-POSTINIT-01` READY, `FI-OWNER-STATE-01` READY. **4 of 4 new faults** are executable against the EXISTING governed suite with **no new test required** — none of the 4 is claimed READY merely because an adjacent happy-path test exists elsewhere; `FI-OWNER-STATE-01` specifically is READY because two existing tests genuinely exercise the handle-less (`self._handle is None`) branch this fault corrupts, not merely a related-but-distinct scenario (§3.4 above).

## 5. Harness/mechanism reuse — precise scope

```text
The existing harness/pattern (design-001 §2/§2.1/§2.1a) is reusable WITHOUT
semantic redesign for target-specific faults that satisfy its existing
activation, single-isolation, integrity, control-run, and evidence
preconditions. All 4 fault specs above satisfy those preconditions (single
comparison/token-level source edit, unique exact old_string, verifiable
post-patch hash, single-hunk/single-file diff scope, detectable via the SAME
`pytest tests/ -q` control/evidence pair) -- no harness change is proposed or
required.

This is NOT a claim that the harness supports literally any future target --
a future fault that cannot satisfy these same preconditions (e.g. a defect
requiring a multi-file coordinated patch, or one whose activation cannot be
proven by a single-hunk diff) would require its own mechanism assessment,
not an assumed extension of this amendment.
```

## 6. Fresh Chapter 0 §4b ADR Scope Rule (this amendment, not inherited)

Evaluated independently for extending fault-spec content to 4 new targets under an already-approved, unmodified mechanism — not inherited from design-001's own `ADR_OPTIONAL` (a decision about *creating* a new mechanism) nor from the EVID-03 applicability analysis's own `ADR_NOT_REQUIRED`/`ADR_OPTIONAL` conclusions (different, narrower/broader decisions).

| §4b criterion | Applies here? |
|---|---|
| Adds/changes a Platform Invariant | No. |
| Changes an Event Schema | No. |
| Changes Module Taxonomy/dependency graph | No. |
| Changes Governance/Approval process | No — the evidence CLASS (§5c) and the execution MECHANISM (design-001 §2) are both already approved and unchanged; this amendment only proposes WHAT additional fault-spec content would qualify, using the identical existing template design-001 §3.1-3.5 already demonstrated 5 times. |
| Affects >1 module | No — `feature-engine` only. |
| Hard to reverse | No — purely additive candidate evidentiary design content; approving or rejecting it reverses trivially, no code/tooling changed. |
| Modifies/supersedes a Locked ADR | No. |

**Disposition: `ADR_OPTIONAL`.** Reasoning: genuinely new, not-cosmetic evidentiary-design content (4 new fault specifications that will, once approved and executed, materially affect what qualifies as complete Condition-3 evidence) — "ảnh hưởng đáng kể" within one module, not merely typo/formatting/refactor — but touches no invariant/schema/taxonomy/cross-module/Locked-ADR trigger and remains fully reversible. Per this task's own instruction, **no ADR is authored** — `ADR_OPTIONAL` is discretionary, and no concrete reason to exercise that discretion is present here (default fewer artifacts).

## 7. Current state (unaffected by this candidate)

```text
Condition 1:                    unaffected by this document.
Condition 2:                    unaffected by this document (separate,
                                 130-identity §4.1(b) resolution track).
Condition 3:                    UNRESOLVED. The historical 13/14-DETECTED/
                                 1-TEST_INFRA_ERROR run against implementation
                                 boundary cda4d0ebaf0f1d9e71bb4be0205380059db7a68b
                                 remains non-qualifying diagnostic output
                                 only (no evidence-003.json exists, none
                                 was ever committed). Bounded Correction 002
                                 (corrected FI-INPUTMERGE-POSTINIT-01 spec:
                                 fail_closed_bypass, "if self.algorithm is
                                 None:") is now APPROVED — EFFECTIVE
                                 (approval_recording_002) but NOT YET
                                 implemented in tooling/faults.py, NOT YET
                                 executed. The full 14-fault population
                                 must be re-run against a fresh executable
                                 boundary before any Condition-3 evidence
                                 exists.
design-001 (historical):        PRESERVED, unchanged, 5-target/10-fault
                                 approval fully intact.
evidence-002.json (historical): PRESERVED, unchanged, valid for its own
                                 pinned boundary.
P3-FEATURE-QG-EVID-03:          OPEN / blocking, unaffected.
Overall Feature Chapter 13 QG:  FAIL — evidence, unaffected.
Feature module approval:        NOT APPROVED.
Phase 3 Approval Gate:          NOT opened.
LIVE:                           NOT_AUTHORIZED.
```

## 8. Not performed by this transaction

No `src/**` change. No test change. No tooling change. No dependency change. No fault injection executed or re-executed. No mutation run. No Condition-2 work. No survivor remediation. No threshold change. No Condition-3 closure. No EVID-03 closure. No Feature Engine approval. No LIVE authorization. This recording transcribes an externally-completed Review A / Risk Classification / Product Owner decision for Bounded Correction 002; it does not itself perform or fabricate any of those steps, and does not itself execute the corrected fault.

**Next governed step:** implement the approved corrected `FI-INPUTMERGE-POSTINIT-01` spec in `tooling/fault_injection/faults.py` and execute the full 14-fault population against a fresh executable boundary.
