# Feature Engine Mutation-Effectiveness Threshold — Step-5 Proposal

**STATUS: PROPOSAL / NOT EFFECTIVE / PENDING REVIEW AND PRODUCT OWNER DECISION**

This document is a Step-5 threshold proposal under Testing Convention v0.16's
governed 9-step sequence (mechanism approval → install/pin → baseline
measurement → analyze → **separate threshold proposal (this document)** →
fresh ADR Scope Rule → review → Product Owner decision → threshold-bearing
formal evidence). It does not activate, approve, or apply any threshold. Until
Steps 6–9 complete, `TEST_EFFECTIVENESS_THRESHOLD` remains
`UNRESOLVED — BASELINE/CALIBRATION REQUIRED` and the current
75.898105813194% raw baseline is not evaluated as PASS or FAIL against
anything in this document.

**Step 6 update:** a fresh Chapter 0 §4b ADR Scope Rule classification of
this proposal has been performed (§6 below) — `ADR_OPTIONAL`, no ADR
authored. Next governed step: Step 7 (Review A + Independent Review B of
this proposal).

## 0. Authority resolved directly (not restated from memory)

- Testing Convention v0.16 (`docs/engineering/testing.md`), the governed
  9-step sequence, item 7 (Ride-owned raw metric formula
  `(killed + confirmed_timeout) / (total − skipped) × 100`), item 8 (raw
  denominator is always controlling; a claimed-equivalent mutant may be
  reported as a candidate but must not change the raw score absent a
  separately governed adjustment), §5b/§5c (mutation-surface completeness
  contract; an ordinary passing unit test does NOT qualify as equivalent
  test-effectiveness evidence for behavior outside mutmut's mutation
  surface), and the explicit non-inference rule (a Tier-1 baseline must not
  be used to infer or calibrate a Tier-0 threshold; no cross-module/cross-tier
  generalization without its own evidence).
- `feature-engine-mutation-baseline-001.json` (blob
  `978ebf92f89e5bd93ba112c1b8e4622835ea71ba`): total 1531, killed 1162,
  survived 369, all other eight statuses 0, raw score `75.898105813194%`,
  sorted-mapping SHA-256 `d69f0c1902d1c275bdb1db464eacbda35d6b2727fd4c5f5889c5c780add5e244`.
- `feature-engine-mutation-baseline-001-analysis.md` (blob
  `8915c66f2e65c1785cbbe2d88a100fcde0ccb156`, post-correction): 369/369
  survivors resolved with 0 unresolved; 170 material actionable-test-gap
  mutants (83 `constructed_object_field_not_independently_asserted` + 87
  `actionable_test_gap_candidate`); 174 low-priority-but-real gaps (173
  `low_materiality_message_text` + 1 `low_materiality_but_real_observable_gap`);
  25 candidate-equivalents (22 `candidate_equivalent` + 3
  `very_likely_equivalent_codec_case_insensitive`), none removed from the
  denominator; 30 functions with ≥3 survivors cover 345/369 (93.5%) of the
  total; 12 hand-written methods entirely outside mutmut 3.7.0's mutation
  surface, 5 assessed high-materiality, no qualifying §5c evidence closes
  this gap; the 165-member `BadTestExecutionCommandsException` cohort's
  mechanism and scope boundary (≤184 candidates, confined to
  `authority_resolver.py`/three named `contracts.py` helper functions) are
  established but exact membership is not, and `STEP-4 THRESHOLD READINESS`
  is recorded `READY` (after Review A's bounded correction) — the state this
  proposal builds on.
- Current `docs/MANIFEST.md` (`manifest_version` verified at this
  transaction's own start, recorded in §7 below) and current
  `docs/governance/execution-rules.md`/`docs/governance/phases/phase-3-rules.md`
  (P3-TXN-001's fold rule; ADR Scope Rule = Constitution Chapter 0 §4b,
  never inherited across transactions).

## 1. What this proposal is, and is not

This is a **proposal**, not an activation. It does not, by itself, change
`TEST_EFFECTIVENESS_THRESHOLD`'s current `UNRESOLVED` state, does not cause
any Chapter 13 PASS/FAIL determination, and does not evaluate whether Feature
Engine currently passes or fails the number proposed below — that evaluation
is explicitly out of scope for Step 5 and is reserved for Step 9's
threshold-bearing formal evidence transaction, after Steps 6–8 complete.

## 2. Empirical basis (restated, not re-derived)

| Quantity | Value |
|---|---|
| Total mutants | 1531 |
| Killed | 1162 |
| Survived | 369 |
| Raw score (controlling, NON-GATING today) | 75.898105813194% |
| Material actionable-test-gap survivors | 170 (83 + 87) |
| Low-priority-but-real survivors | 174 (173 + 1) |
| Candidate-equivalent survivors (in denominator) | 25 (22 + 3) |
| Functions with ≥3 survivors | 30, covering 345/369 (93.5%) |
| Mutation-surface blind spot | 12 methods, 5 high-materiality, 0 in mutation surface |
| Kill-validity caveat | ≤184-candidate crash-cohort bound, 165 actual, exact membership unresolved |

## 3. Candidate thresholds evaluated

Four candidates were computed and weighed. None was selected merely to make
the current baseline pass — candidate 1 is explicitly rejected for exactly
that reason, and the recommended candidate (3) is **above** the current
score, meaning Feature Engine would currently fail it.

### Candidate 1 — ~76% (round the current baseline up to itself)

**Rejected.** This is precisely the "choose a number so today's score
passes" pattern this task explicitly forbids. It carries no independent
empirical justification, encodes today's *actual* gap population (170
material gaps) as acceptable residual risk, and provides no improvement
incentive. Testing Convention v0.16 v0.9's own history already rejected an
analogous move once (the original, non-repository-specific `80%` figure was
removed for being asserted "alongside this document's other genuinely-
resolved numeric contracts... in a way that risked being read as similarly
settled" before any baseline existed) — accepting the current score outright
would repeat the same defect in the opposite direction.

### Candidate 2 — 80% (generic industry-practice figure, the same number v0.8 originally proposed and v0.9 removed)

**Considered, not recommended as the primary figure.** Reaching 80% requires
closing ≈63 additional mutants (`0.80 × 1531 − 1162 ≈ 62.8`) — achievable
without closing all 170 material gaps, and would leave significant identified
material risk (over 100 mutants) formally acceptable. More importantly, 80%
is not itself derived from this repository's own survivor distribution — it
is the same non-repository-specific figure Testing Convention v0.9 already
rejected once, before any baseline existed, for exactly that reason.
Re-adopting it now, with real data available that supports a more precise,
directly-traceable number, would be a weaker proposal than Candidate 3 below.
Recorded as a plausible **minimum floor** if Candidate 3 is judged too
aggressive for an initial threshold, but not the recommendation.

### Candidate 3 — 87.0% (close every currently-identified material actionable-test-gap survivor; RECOMMENDED)

`(1162 killed + 170 material-gap survivors) / 1531 × 100 = 86.9954...%`
(reported to three decimals: **86.995%**, stated as **87.0%**).

This number is directly, traceably derived from Step 4's own evidence: it is
exactly the score Feature Engine would reach if every one of the 170
individually-identified, individually-cited material actionable-test-gap
mutants (§1.4 of the analysis) were closed by new or strengthened tests,
while explicitly NOT requiring closure of the 174 low-priority
message-text-only/currently-unexercised gaps and NOT crediting any of the 25
candidate-equivalents (which remain, correctly, uncredited survivors per
Testing Convention v0.16 item 8's raw-denominator-by-default rule).

This is more achievable than the raw gap count suggests: the analysis's own
duplication finding (30 functions with ≥3 survivors cover 345/369, 93.5%)
means the 170 material gaps are concentrated in a small number of underlying
root causes, not 170 independent test-writing efforts — e.g. the 7
`_recompute` mutants sharing one untested branch close together with a single
new test scenario, and the `constructed_object_field_not_independently_asserted`
pattern (83 mutants) is dominated by a handful of constructor-heavy functions
(`resolve_computation_cursor` 35, `_seal_verified_authority` 24, engine
`__init__` methods) where one disciplined "assert every field" test per
function closes many mutants at once.

### Candidate 4 — 98.4% (theoretical ceiling: close every gap except confirmed/candidate equivalents)

`(1531 − 25 equivalents) / 1531 × 100 = 98.367...%`

**Rejected as a gating bar.** This requires closing all 174 low-priority
message-text-only/currently-unexercised gaps in addition to the 170 material
ones. Forcing closure of message-text-only gaps specifically risks the
anti-gaming failure mode Testing Convention v0.16 item 9 already warns
against in spirit (no exclusion/manipulation merely to move a score) in
reverse form — it would incentivize writing brittle, exact-message-text
assertions whose only purpose is to kill a mutant, not to validate genuine
behavior, since by definition these mutants change no other observable
output. Recorded as the empirical ceiling for context, not proposed as a
gate.

### Candidate 5 — a range instead of a point (e.g. 85–90%)

**Rejected as the primary form.** Chapter 13's eventual formal
threshold-bearing evidence transaction (Step 9) needs a definite,
auditable PASS/FAIL boundary, not a range. Candidate 3's precise,
directly-computed figure (87.0%) already falls inside this range and is
preferred for its explicit traceability to a named, closeable gap set rather
than an interval chosen by inspection.

## 4. Recommended proposal

> **Propose (NOT active): Feature Engine (Tier-1, FEATURE-ENGINE-ONLY scope)
> raw mutation-effectiveness threshold = 87.0%**, computed as
> `(killed + confirmed_timeout) / (total − skipped) × 100` per Testing
> Convention v0.16 item 7's already-approved Ride-owned formula, unchanged.

**Exact scope:** `python/feature-engine/src/feature_engine/**`, evaluated
against the mutation surface and ten-status contract already defined in
Testing Convention v0.16 (items 5a–5d, 6, 8, 8a). This proposal is
**Tier-1-only** and **Feature-Engine-only**. It must NOT be read as, applied
to, or cited as precedent for a Tier-0 threshold (Risk Gateway, Execution
Engine, Position Ledger) or any other module/tier — per v0.16's own explicit
non-inference rule, any such broader threshold requires its own independent
baseline measurement and its own Step 1–9 sequence on that subject.

**If the current Feature Engine score (75.898105813194%) remains below
87.0% at the time this threshold becomes effective (post Step 9):** Feature
Engine's test-effectiveness dimension would evaluate `FAIL` under Chapter 13,
exactly as `P3-FEATURE-QG-EVID-03` already does today for the unrelated
reason of the threshold being unresolved. This proposal does not soften,
does not pre-emptively waive, and does not create any grace period for that
outcome — closing the material gap population (or securing a governed
threshold revision through this same proposal process) are the only two
paths to a future PASS, and neither is decided by this document.

### 4.1 Companion eligibility condition (explicitly proposed only, not effective)

**Proposed:** meeting the 87.0% raw score alone does not, by itself,
constitute complete Tier-1 test-effectiveness evidence for Feature Engine.
This restates — does not create — Testing Convention v0.16 §5b's existing
fail-closed rule: a formal evidence transaction must record the 12-method
mutation-surface blind spot (5 high-materiality) as a named, open residual
unless, for each high-materiality method, EITHER (a) a separately-accepted
supplemental mutation-testing mechanism reaching that code exists, or (b)
governed deterministic fault-injection evidence per §5c exists, or (c) the
Product Owner has separately and explicitly recorded a risk-acceptance
decision naming that specific residual. Meeting the numeric threshold must
never be read as silently satisfying this pre-existing, separate
requirement.

### 4.2 Proposed recalibration triggers (explicitly proposed only, not effective)

**Proposed**, none currently triggered, none self-executing — each would
require its own separate governed re-proposal transaction, not an automatic
adjustment:

1. **Tool/version change.** If mutmut is upgraded past `3.7.0` and the
   decorated-class mutation-surface limitation (Testing Convention v0.16
   §5a-i) is fixed, extending the mutation surface to the 12 currently-
   excluded methods materially changes both the denominator and the
   achievable score — this threshold must be re-baselined against a fresh
   measurement, never silently carried forward across a mutation-surface
   change.
2. **165-cohort resolution.** If a future diagnostic (Step-4 analysis §3.6's
   deferred, bounded 184-candidate follow-up) resolves the exact
   `BadTestExecutionCommandsException` cohort membership and finds the
   `authority_resolver.py`/`contracts.py`-authority-helper subset's kill rate
   is disproportionately inflated by the crash-detection channel rather than
   genuine assertion coverage, this threshold's empirical basis should be
   reviewed against a recomputed, detection-channel-adjusted picture.
3. **Baseline methodology change.** Any change to the Ride-owned metric
   formula, the ten-status contract, or the mutation-surface completeness
   contract (Testing Convention v0.16 items 6–8a, 5b–5d) invalidates this
   proposal's empirical grounding and requires a fresh Step 4/5 pass.

These conditions are recorded as proposed governance intent only. None is
active; none may be silently treated as effective by any future transaction
without its own governed decision.

## 5. Treatment of Testing Convention v0.16's controlling constraints

- **Candidate-equivalents (25) remain in the raw denominator**, uncredited,
  exactly as item 8 requires. No adjustment is made or proposed here; a
  governed equivalent-mutant adjustment (individually-pinned mutant identity
  + justification + separate reviewed decision, per item 8) remains a
  distinct, separately-governable action this proposal does not perform.
- **The raw score (75.898105813194%) is unchanged and unadjusted.** This
  proposal does not retroactively adjust it for the 165-cohort caveat, the
  12-method blind spot, or any other reason — it remains the single
  controlling, already-recorded number.
- **No Tier-0 inference.** This proposal makes no claim about, and must not
  be cited for, any Tier-0 subject's threshold.

## 6. `ADR_SCOPE_DISPOSITION` — Step 6 fresh classification

Testing Convention v0.16's own ADR-scope disposition note is explicit: the
mechanism-selection candidate's `ADR_NOT_REQUIRED` disposition does **not**
extend to a future numeric-threshold proposal, which must independently
re-run Constitution Chapter 0 §4b's ADR Scope Rule at its own boundary. This
section performs that fresh classification, as its own separate,
subsequent governed transaction (Step 6), not inherited from Step 5.

### 6.1 Trigger-by-trigger analysis (Chapter 0 §4b)

| §4b trigger | Applies to this proposal? | Reasoning |
|---|---|---|
| Platform Invariant change | **No** | The proposal touches no I-1–I-13 invariant (`docs/constitution/02-platform-invariants.md`) — it is a test-effectiveness measurement parameter, not a domain/architecture invariant. |
| Event Schema change | **No** | No event/fact schema, contract, or field is added, removed, or reinterpreted. |
| Module Taxonomy/dependency-graph change | **No** | No edit to `module-registry.yaml` or any module dependency edge; Feature Engine's own module boundary is unchanged. |
| Governance/Approval-process change | **No — this is the trigger requiring the most care, resolved from Chapter 13's own text, not precedent.** Chapter 13 §13.14 (Locked) explicitly, already defers "concrete tooling, CI operator, coverage/mutation **ngưỡng số vượt tier floor**" (numeric coverage/mutation thresholds beyond the tier floor) to Engineering Foundation/Testing Convention. This is pre-existing, Locked delegation of the *authority to set a specific numeric threshold* — not a decision this proposal is inventing. Filling that already-delegated slot with a specific, evidence-grounded number for one module is exercising already-granted authority, not creating new governance/approval-process machinery. (ADR-030's own ADR-scope-check reasoning, itself grounded in Chapter 3 §3.2/Chapter 13 §13.14 text rather than being cited as bare precedent, draws the same "existing Locked authority already pre-resolved → author directly, no ADR" distinction for Testing Convention content generally.) Testing Convention v0.16's own caution that a threshold proposal "closer to a governance/quality-policy decision" needs its own §4b re-run is specifically flagged for a **cross-module or repository-wide** threshold — this proposal is explicitly neither; it is Tier-1/FEATURE-ENGINE-ONLY. |
| Decision affecting >1 module | **No** | Proposal §3/§4 explicitly, repeatedly scopes this to Feature Engine only and explicitly disclaims any Tier-0 or cross-module/cross-tier generalization, consistent with Testing Convention v0.16's own non-inference rule. |
| Hard-to-reverse decision | **No** | The threshold is not a one-way architectural commitment: Testing Convention v0.16's own 9-step sequence (and this proposal's own §4.2 recalibration triggers) establish that a threshold is revisable via a symmetric, evidence-grounded re-proposal — the same governed mechanism that would set it can reset it. This contrasts with genuinely hard-to-reverse decisions (Event Schema, cross-module contracts) that cascade into other artifacts' own compatibility guarantees. |
| Locked-ADR modification/supersession | **No** | No existing ADR addresses Feature Engine's (or any module's) mutation-effectiveness threshold; nothing is modified or superseded. |
| **Alternative: significant but reversible single-module internal change** | **Yes** | The proposal is significant — once effective, it would be the actual number that determines a real Chapter 13 test-effectiveness PASS/FAIL outcome for Feature Engine, a genuine governance consequence, not cosmetic. It is confined to one module, changes no contract, and (per the row above) exercises already-delegated authority rather than creating new process. This is precisely §4b's own "ADR Optional" example: *"Thay đổi nội bộ một module không đổi contract nhưng ảnh hưởng đáng kể"* (an internal change to one module that does not change a contract but has significant impact). |

### 6.2 Classification

```text
ADR_SCOPE_DISPOSITION: ADR_OPTIONAL
```

No ADR-Required trigger is met. `ADR_NOT_REQUIRED` would understate the
decision's real significance (it is not cosmetic/typo/refactor-only — it
will eventually gate a real Quality Gate PASS/FAIL dimension) and this task's
own instruction requires classifying this as a new semantic decision rather
than defaulting to the mechanism candidate's prior disposition. `ADR_OPTIONAL`
is the textually-supported fit: single-module, contract-preserving,
already-delegated authority, but genuinely significant.

**No ADR is authored by this transaction.** Per this task's own instruction,
an `ADR_OPTIONAL` (or `ADR_NOT_REQUIRED`) classification means the next
governed action is Step 7 (Review A + Independent Review B of the threshold
proposal itself), not ADR authoring. A future reviewer or Product Owner
remains free to judge, at Step 7 or Step 8, that an ADR would nonetheless be
worthwhile — that discretionary option is preserved, not exercised, by this
classification.

## 7. Review A disposition folded in (externally-supplied; no prior record existed)

Per this task's instruction and the P3-TXN-001 default-fold rule, the
following externally-supplied bounded Review A re-review disposition, for the
Step-4 correction at boundary `b591e56d2dbf637322345f0acf3f58e04f13adf8`, is
recorded here (no standalone review-evidence transaction created):

- `P3-PY-MUT-CAL-A-MAJ-01`: **CLOSED — REVIEW A**
- `P3-PY-MUT-CAL-A-MIN-01`: **CLOSED — REVIEW A**
- New Blocker/Major/Minor: 0/0/0 — `FINAL BOUNDED REVIEW A RE-REVIEW: CLEAN`
- `STEP-4 THRESHOLD READINESS: READY` (confirmed, unchanged by this Step-5
  transaction, which only *consumes* that readiness state)

No prior record of these two closure dispositions existed in
`docs/MANIFEST.md` or `docs/CHANGELOG.md` before this transaction — this is
their first recording.

## 8. Lifecycle states preserved (unchanged by this proposal)

- `TEST_EFFECTIVENESS_THRESHOLD`: **UNRESOLVED — BASELINE/CALIBRATION
  REQUIRED** (this proposal does not resolve it; only Step 9 could, after
  Steps 6–8)
- `P3-FEATURE-QG-EVID-03`: **FAIL — evidence**
- Feature Engine Chapter 13 Quality Gate: **FAIL**
- Feature Engine approval status: **NOT APPROVED**
- Phase 3 gate: **NOT OPENED**
- LIVE authorization: **NOT_AUTHORIZED**
