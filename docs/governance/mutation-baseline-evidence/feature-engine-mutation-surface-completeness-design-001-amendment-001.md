# Feature Engine — Mutation-Surface Completeness (Condition 3) Design — Amendment 001 (Current-Boundary Target-Population Extension)

```yaml
status: CANDIDATE — PENDING REVIEW A
artifact_id: feature-engine-mutation-surface-completeness-design-001-amendment-001
amends: feature-engine-mutation-surface-completeness-design-001
created_for: >
  Extending the already-approved Condition-3 fault-injection DESIGN (mechanism
  unchanged) from its historical five-method target population to four
  newly-material current-boundary methods identified by the EVID-03
  current-boundary applicability analysis (P3-FEATURE-EVID03-REBASE-A-MAJ-01,
  CLOSED — BOUNDED REVIEW A RE-REVIEW).
transaction_kind: DESIGN ONLY — AMENDMENT CANDIDATE, NOT APPROVED
production_changed: false
tests_changed: false
tooling_changed: false
fault_injection_performed: false
formal_step9_qg_evaluation_performed: false
evid_03_closed: false
condition_3_closed: false
repository_head_at_authoring: b5014955c77964a9a5ceb0f22a1b79a297be595b
```

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

### 3.4 `FI-OWNER-STATE-01` — no-handle lifecycle-state misreport

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
detecting_test(s):     GAP -- see below.
readiness:             GAP -- no existing test directly asserts `.state` on
                       a handle-less (never-activated / pre-acquisition)
                       AuthoritativeSubjectOwner instance; every existing
                       `owner.state` assertion in tests/test_ownership.py
                       (13 occurrences) is taken AFTER some acquisition/
                       revocation/failure sequence has already assigned a
                       real handle, never on a pristine, handle-less
                       instance.
minimum_test_required: A new, minimal direct test (NOT authored by this
                       amendment): construct a fresh AuthoritativeSubjectOwner
                       with no acquire_and_activate call yet performed, and
                       assert owner.state is SubjectOwnershipState.INACTIVE.
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

**Test-readiness summary:** `FI-PREPTRANS-RECONCILE-01` READY, `FI-PFC-FINALIZE-01` READY, `FI-INPUTMERGE-POSTINIT-01` READY, `FI-OWNER-STATE-01` GAP (1 new test required). 3 of 4 new faults are executable against the EXISTING governed suite with no new test; only `FI-OWNER-STATE-01` blocks on the one minimal test named above — none of the 4 is claimed READY merely because an adjacent happy-path test exists elsewhere.

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
Condition 3:                    UNRESOLVED. This candidate amendment is
                                 PENDING REVIEW A -- not approved, not
                                 effective, no fault executed.
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

No `src/**` change. No test change. No tooling change. No dependency change. No fault injection executed. No mutation run. No Condition-2 work. No survivor remediation. No threshold change. No EVID-03 closure. No Feature Engine approval. No LIVE authorization. **No self-approval** — this candidate is recorded `CANDIDATE — PENDING REVIEW A` and is not, and cannot be, closed by this executor.

**Next governed step:** ChatGPT Review A of this Condition-3 current-boundary fault-spec amendment candidate. After Review A: Risk Classification required; if this candidate remains a semantic amendment to the Product-Owner-approved Condition-3 design (the expected case), Product Owner approval is required before these 4 new fault specs may be used as formal Condition-3 evidence. No Review B automatically triggered by this candidate's own risk tier; an optional advisory cross-check may be added later only if the Product Owner chooses, per current ADR-042 governance.
