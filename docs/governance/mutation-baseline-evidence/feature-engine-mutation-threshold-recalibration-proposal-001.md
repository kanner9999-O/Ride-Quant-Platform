# Feature Engine Condition-1 Threshold — Recalibration Proposal 001

**STATUS: CANDIDATE — NOT EFFECTIVE / AWAITING REVIEW A**

This document is a **proposal only**. It does not activate, apply, or
change the currently-effective threshold. The existing
`feature-engine-mutation-threshold-proposal-001.md` (blob
`f4a3ca0c37aeb4684409a7344141103e64051e04`, status `APPROVED — EFFECTIVE`)
remains byte-unchanged and remains the sole controlling Condition-1
threshold: `87.001959503592%`, two-part gate (aggregate raw score **and**
§4.1's per-identity resolution condition). No Product Owner decision is
requested by this transaction.

## 0. Authority resolved directly (fresh-read, not restated from memory)

| Artifact | Path | Blob | Fresh-verified |
|---|---|---|---|
| Currently-effective threshold proposal | `docs/governance/mutation-baseline-evidence/feature-engine-mutation-threshold-proposal-001.md` | `f4a3ca0c37aeb4684409a7344141103e64051e04` | Yes — read in full this transaction |
| Testing Convention (current Approved) | `docs/engineering/testing.md` | `de17690733b2b3c75345e867a8c442a39911e5da` | Yes — `version: "0.17"`, `status: Approved` |
| Chapter 13 (Quality Gates) | `docs/constitution/13-quality-gates.md` | `acf4ab75eda1ea0613250ce3159669ea727e28ec` | Yes — `version: "1.8"`, `status: Locked` |
| ADR-044 | `docs/adr/ADR-044.md` | `82f07b523ff30b08d17b39a9beaf2d6d1c369179` | Yes — `version: "0.5"`, `status: Approved` |
| ADR-045 | `docs/adr/ADR-045.md` | `ac13ece16ff644d0d88ddf982d83bfb0e8d5ad16` | Yes — `version: "0.3"`, `status: Approved` |
| Evidence-005 (formal) | `docs/governance/mutation-baseline-evidence/feature-engine-mutation-step9-formal-evidence-005.json` | `f7a6ab715155ad166808e0e9d9a7474196d9b69d` | Yes |
| Post-E005 survivor assessment | `docs/governance/mutation-baseline-evidence/feature-engine-condition1-post-e005-survivor-assessment-001.json` | `5d7d626cfd1b500a3751c90613bd041cec50a792` | Yes — matches expected exactly |

**Post-E005 assessment identity, fresh-verified against §2 of this task's
own citation (exact match, no drift):**

```text
survivors:            406
GENUINE_TEST_GAP:      40
LOW_MATERIALITY_MESSAGE_TEXT: 344
PROVABLY_EQUIVALENT:   16
STRUCTURALLY_UNREACHABLE: 4
UNCLEAR:                2
```

Chapter 13 v1.8 §13.14 (Locked) explicitly defers the exact
test-effectiveness threshold number and tooling to Engineering Foundation
(Testing Convention) — the numeric threshold itself is, and remains,
Testing-Convention-owned/delegated territory, not Chapter-13-owned. This
proposal does not touch Chapter 13, ADR-044, or ADR-045.

## 1. Calibration-drift finding — independently re-derived

**Current Condition-1 facts (fresh-verified against Evidence-005, not
copied):**

```text
population (total)            = 2629
required threshold             = 87.001959503592%
required numerator             = ceil(0.87001959503592 × 2629) = 2288
                                  (independently recomputed: 2629 ×
                                  0.87001959503592 = 2287.281515349434,
                                  ceil = 2288 — exact match)
formal conservative numerator  = 2214  (killed 2209 + confirmed_timeout 5)
best-case current unstable bound = 2223  (2214 + 9 unstable_timeout_triage)
conservative gap                = 2288 − 2214 = 74
best-case gap                   = 2288 − 2223 = 65
```

**Credible test-remediation ceiling, two variants:**

*If the 2 UNCLEAR survivors resolve GENUINE (not performed — hypothetical
upper bound before §3's fresh resolution below):*

```text
40 GENUINE_TEST_GAP + 2 UNCLEAR + 9 UNSTABLE = 51
2214 + 51 = 2265
2265 < 2288  →  shortfall = 23
```

**Robustness check (independently recomputed):** even crediting every
single non-message-text survivor — including the 16 `PROVABLY_EQUIVALENT`
and 4 `STRUCTURALLY_UNREACHABLE` mutants, which Testing Convention v0.17
item 8's raw-denominator-by-default rule explicitly forbids crediting
without an individually-pinned, separately-governed equivalent-mutant
adjustment — as if all were killed:

```text
40 genuine + 2 unclear + 16 equivalent + 4 unreachable + 9 unstable = 71
2214 + 71 = 2285
2285 < 2288  →  shortfall = 3
```

**Independently verified: both arithmetic chains reconcile exactly** against
this task's own cited figures (`74`/`65` gaps, `51`/`71` combined credits,
`2265`/`2285` resulting numerators, `23`/`3` shortfalls). No discrepancy
found.

**Conclusion, derived (not assumed):** even under the maximally generous,
evidence-defying hypothetical where literally every currently-classified
non-message-text survivor is credited — including mutants this repository's
own governed rules (Testing Convention item 8) explicitly forbid crediting
without a separate governed reclassification — the fixed
`87.001959503592%` threshold is **still unreachable by 3 mutants** without
also killing some portion of the 344 `LOW_MATERIALITY_MESSAGE_TEXT`
population. This is the precise, quantitative proof of calibration drift:
the original threshold's own stated intent (§2 below) explicitly excludes
requiring message-text closure, yet the current fixed number can no longer
be satisfied without it.

## 2. Original Candidate-3 intent — quoted, not paraphrased loosely

From `feature-engine-mutation-threshold-proposal-001.md` §3, Candidate 3
(the approved figure):

> "`(1162 killed + 170 material-gap survivors) / 1531 × 100 =
> 87.001959503592...%`... This number is directly, traceably derived from
> Step 4's own evidence: it is exactly the *aggregate* score Feature Engine
> would reach if every one of the 170 individually-identified,
> individually-cited material actionable-test-gap mutants... were closed by
> new or strengthened tests, while explicitly **NOT** requiring closure of
> the 174 low-priority message-text-only/currently-unexercised gaps and
> **NOT** crediting any of the 25 candidate-equivalents (which remain,
> correctly, uncredited survivors per Testing Convention v0.16 item 8's
> raw-denominator-by-default rule)."

And, rejecting the theoretical-ceiling candidate that WOULD have required
message-text closure:

> "Candidate 4... **Rejected as a gating bar.** This requires closing all
> 174 low-priority message-text-only/currently-unexercised gaps in addition
> to the 170 material ones. Forcing closure of message-text-only gaps
> specifically risks the anti-gaming failure mode Testing Convention v0.16
> item 9 already warns against in spirit... it would incentivize writing
> brittle, exact-message-text assertions whose only purpose is to kill a
> mutant, not to validate genuine behavior."

**Stated intent, accurately restated:**

1. close all then-identified material actionable test gaps (the 170);
2. explicitly do **NOT** require closure of the low-priority message-text
   population (the 174, now analogous to today's 344
   `LOW_MATERIALITY_MESSAGE_TEXT`);
3. do **NOT** credit candidate-equivalents;
4. avoid incentivizing brittle exact-message assertions written merely to
   move the score.

**Semantic mismatch, derived (not assumed):** §1's robustness check proves
that satisfying the CURRENT fixed `87.001959503592%` number today would
require closing at least 3 `LOW_MATERIALITY_MESSAGE_TEXT` (or otherwise
non-creditable) mutants even in the best possible combination of every
other category — directly contradicting intent point (2) above. The
threshold was correctly calibrated to the **1531-mutant, 170-material-gap**
population at Step 4/5; the population has since grown to **2629 mutants**
with a **different, independently re-derived materiality composition** (40
material, not 170 — see §3), and the fixed percentage carried forward
unchanged no longer encodes the same closure obligation it was built to
represent.

**Disposition:**

```text
CALIBRATION_DRIFT_CONFIRMED
```

## 3. Fresh resolution of the 2 UNCLEAR survivors (folded in, no separate WP)

```text
feature_engine.ownership.xǁAuthoritativeSubjectOwnerǁacquire_and_activate__mutmut_21
feature_engine.ownership.xǁAuthoritativeSubjectOwnerǁacquire_and_activate__mutmut_23
```

Both mutate one field of the intermediate `OwnerHandle` constructed at
`self._handle = OwnerHandle(self._feature_subject_id, generation,
SubjectOwnershipState.CATCHING_UP)` inside `acquire_and_activate`
(`ownership.py:538`) — mutmut_21 nulls `self._feature_subject_id`;
mutmut_23 nulls `SubjectOwnershipState.CATCHING_UP`.

**Fresh trace of every path following that assignment (full source read,
this transaction):**

- **Success path:** `self._catch_up(catch_up_frontier)` returns without
  raising, and the very next statement unconditionally executes
  `self._handle = OwnerHandle(self._feature_subject_id, generation,
  SubjectOwnershipState.ACTIVE)` (`ownership.py:544`) — a **freshly
  reconstructed** handle using the real, unmutated
  `self._feature_subject_id` and the real `SubjectOwnershipState.ACTIVE`,
  completely overwriting the CATCHING_UP handle before the method returns.
- **Failure path:** any exception from `_catch_up` is caught by
  `except Exception: self._mark_terminal(); raise`. `_mark_terminal()`
  (`ownership.py`, read in full) unconditionally executes `self._handle =
  OwnerHandle(self._feature_subject_id, generation,
  SubjectOwnershipState.REVOKED)` — again a freshly reconstructed handle
  using the real, unmutated `self._feature_subject_id`, overwriting
  whatever CATCHING_UP handle (mutated or not) was set beforehand.
- **In between:** `_catch_up`'s own body (`ownership.py:567-613`, read in
  full) contains **zero** references to `self._handle`, `self.handle`, or
  `self.state` — confirmed by direct grep of the function body. It only
  reads `self._feature_subject_id`, `self._history_provider`,
  `self._merge_policy`, and `self._engine` (a distinct object with no
  reference to the owner's `self._handle` — `self._engine.prepare_
  upstream_event(...)` operates entirely on the wrapped engine, not the
  owner). Python's single-threaded, synchronous execution within one method
  call means no external observer can read `self._handle` between line 538
  and either line 544 or `_mark_terminal`'s own reassignment.

**Questions, answered directly:**

- *Is the intermediate `CATCHING_UP` `OwnerHandle` observably meaningful?*
  **No.** It is write-only — no code path, in this method or any method it
  calls, ever reads it before it is unconditionally overwritten.
- *Is `self._handle` deterministically overwritten before any external or
  failure-path observation?* **Yes, on every path**, with no exception —
  this is not merely likely, it is exhaustively confirmed by reading both
  the success continuation and the exception handler, plus confirming
  `_catch_up`'s own body never reads the field in between.
- *Can a legitimate production-semantic test distinguish either mutation?*
  **No.** Any test — unit-level or integration-level, black-box or
  white-box — that calls `acquire_and_activate` and then inspects
  `owner.handle`/`owner.state`/`owner.feature_subject_id` will observe only
  the post-overwrite value (`ACTIVE` or `REVOKED`, both with the real,
  unmutated `feature_subject_id`), regardless of whether the intermediate
  CATCHING_UP handle was corrupted. This is a structural property of the
  method's own control flow, not a gap in test authorship.
- *Classification:* **`PROVABLY_EQUIVALENT`** for both `mutmut_21` and
  `mutmut_23` — the same class of proof as the already-confirmed
  `ownership.__init__`'s `self._usable = True → False/None` dead-write
  (post-E005 assessment, `F_UNCLEAR` note on that earlier finding is now
  superseded by this fully-traced confirmation for these two specific
  mutants).

**Settled classification (this transaction, supersedes the post-E005
assessment's `UNCLEAR` label for exactly these two IDs — the assessment
artifact itself is NOT edited, per §15's immutability requirement; this is
a forward-looking analytical resolution recorded here only):**

```text
GENUINE_TEST_GAP:              40  (unchanged)
LOW_MATERIALITY_MESSAGE_TEXT: 344  (unchanged)
PROVABLY_EQUIVALENT:           18  (16 + 2, settled)
STRUCTURALLY_UNREACHABLE:       4  (unchanged)
UNCLEAR:                        0  (settled)
```

**Robustness re-confirmed:** because both resolve to `PROVABLY_EQUIVALENT`
— a category §1's robustness check already (correctly) included in the
71-credit hypothetical — the §1 shortfall-of-3 finding is **unchanged and
robust to this resolution**, exactly as required. The settled, non-
hypothetical genuine-test-gap population remains exactly **40**, not up to
42 — this *strengthens*, not weakens, the calibration-drift finding: the
population of mutants whose closure the original intent actually
contemplates crediting is now known precisely, not merely bounded.

## 4. Current population/materiality analysis (Model A's own basis)

```text
total                          2629
killed                         2209
confirmed_timeout                 5   (→ 2214 combined, formula-numerator basis)
unstable_timeout_triage           9   (not yet credited — pending individual
                                       re-confirmation per Testing Convention
                                       item 8's timeout-specific rule)
survived (406), decomposed:
  GENUINE_TEST_GAP                40  (the direct analog of the original
                                       170-mutant "material actionable-
                                       test-gap" population)
  LOW_MATERIALITY_MESSAGE_TEXT   344  (the direct analog of the original
                                       174 "low-priority-but-real" +
                                       message-text population — NOT to be
                                       required for closure, per original
                                       intent)
  PROVABLY_EQUIVALENT             18  (analog of the original 25 candidate-
                                       equivalents — remains in the raw
                                       denominator, uncredited, per Testing
                                       Convention item 8, unless and until a
                                       separate governed per-identity
                                       adjustment is recorded)
  STRUCTURALLY_UNREACHABLE         4  (dead-field/defensive-fallback
                                       mutants — same treatment as
                                       PROVABLY_EQUIVALENT for scoring
                                       purposes: real, but not creditable
                                       without a separate governed
                                       adjustment)
```

## 5. Model A — numeric re-baseline, same raw metric

**Formula unchanged:** `mutation_score = (killed + confirmed_timeout) /
(total − skipped) × 100` (Testing Convention v0.17 item 7, unchanged, this
proposal does not modify it). `skipped = 0` in Evidence-005 (all ten
statuses reconciled to `total`).

**Same conceptual principle as Candidate 3:** close the current materially-
actionable behavioral gap population (today's `GENUINE_TEST_GAP` survivors
— the direct analog of the original 170) without requiring closure of the
low-materiality/message-text population (today's `LOW_MATERIALITY_MESSAGE_
TEXT`, analog of the original 174) or crediting equivalents/unreachables
(today's `PROVABLY_EQUIVALENT`/`STRUCTURALLY_UNREACHABLE`, analog of the
original 25 candidate-equivalents).

**Conservative candidate (recommended final method — does not depend on any
pending measurement):**

```text
(2214 + 40) / 2629 × 100 = 2254 / 2629 × 100
= 85.736021300874857360213008748573602130087485736021...%
display, same 12-decimal-place convention as the original: 85.736021300875%
```

**Best-case variant (pending unstable-triage resolution — NOT recommended
as the final method, since it depends on 9 not-yet-individually-confirmed
mutants; provided only for transparency):**

```text
(2214 + 40 + 9) / 2629 × 100 = 2263 / 2629 × 100
= 86.078356789653860783567896538607835678965386078357...%
display: 86.078356789654%
```

**Explicit distinctions (per this task's own requirement):**

| Population | Count | Credited in Model A candidate? |
|---|---|---|
| Current already-positive numerator (killed + confirmed_timeout) | 2214 | Yes — base |
| Current materially-actionable survivors (`GENUINE_TEST_GAP`) | 40 | Yes — the closure target, exactly mirroring the original 170 |
| Unresolved/unclear population | 0 (settled this transaction, §3) | N/A |
| Unstable triage (pending) | 9 | No, in the recommended conservative candidate; yes, only in the disclosed best-case variant |
| Message-text-only population | 344 | **No** — never required, matching original intent |
| Equivalent/unreachable population | 18 + 4 = 22 | **No** — remains uncredited per Testing Convention item 8, matching original intent |

**Why the conservative candidate, not the best-case variant, is
recommended as the final auditable method:** the conservative candidate is
computable and verifiable TODAY from already-confirmed categories only
(`killed`, `confirmed_timeout`, and this transaction's own settled
`GENUINE_TEST_GAP` classification); it never depends on an outstanding
measurement (the 9 `unstable_timeout_triage` mutants' eventual disposition
is explicitly unresolved and, per Testing Convention item 8, must not be
credited before individual re-confirmation). This mirrors Candidate 3's own
preference for "explicit traceability to a named, closeable gap set" over
inspection-based ranges.

**Not chosen merely because it passes today:** current raw score is
`84.21453023963484%–84.55686572841384%`. Both Model A candidate figures
(`85.736021300875%` and `86.078356789654%`) are **above** the current
actual score — Feature Engine would still `FAIL` Condition 1 under either
recalibrated figure today. This is the same non-negotiable discipline the
original proposal applied when rejecting Candidate 1 (~76%, "round the
current baseline up to itself").

## 6. Model B — denominator/exclusion semantics change

**Evaluated, not recommended.** Explicitly changing denominator/exclusion
semantics — e.g., removing `LOW_MATERIALITY_MESSAGE_TEXT` mutants from the
denominator entirely, or introducing a `# pragma: no mutate`-style
mechanism scoped to message-text constructs — would directly rewrite
Testing Convention v0.17 items 7–9's controlling definitions: item 7's raw-
denominator formula, item 8's explicit "equivalent mutants REMAIN IN THE
RAW DENOMINATOR by default — no ad-hoc denominator edits are permitted"
rule, and item 9's exclusion-justification requirement ("never a free way
to inflate the score").

**Governance complexity:** this is not a Feature-Engine-only change — the
metric formula and denominator semantics are defined once, centrally, in
Testing Convention v0.17 and apply (or would apply, as other Tier-0/Tier-1
modules adopt mutation testing) across the whole repository. Changing them
here would either (a) improperly special-case Feature Engine outside the
shared contract, creating an inconsistent precedent, or (b) require its own
Testing Convention amendment cycle — a materially heavier, cross-cutting
process than a single-module numeric recalibration.

**Anti-gaming risk: high.** A mechanism that identifies "message-text-only"
mutants and removes them from scrutiny is structurally the exact loophole
Testing Convention already warns against — it would require establishing a
new, ongoing, auditable classification authority (who decides what counts
as message-text, how is a disputed classification appealed, how is drift
in that classification prevented over time) with no existing governed
precedent to reuse. This is fundamentally different from, and heavier than,
Model A's reuse of an already-approved formula against an updated
comparison figure.

**Would this constitute a metric-methodology change triggering broader
Step-4/5 recalibration and/or ADR scope?** Yes, on both counts. It directly
falls under the original proposal's own §4.3 trigger 3 ("Baseline
methodology change... invalidates this proposal's empirical grounding and
requires a fresh Step 4/5 pass") for ANY module using the same metric, and
plausibly crosses the Chapter 0 §4b Governance/Approval-process trigger
(inventing a new, ongoing classification-and-exclusion mechanism, not
merely applying an existing one) in a way Model A's simple recalibration
does not.

**Not implemented or recommended by this transaction.**

## 7. Model C — materiality-aware gate replaces raw percentage as primary gate

**Evaluated, not activated.** Under this model, the raw percentage becomes
diagnostic-only, and the primary Condition-1 gate is keyed on: (a) current
material behavioral gap resolution (an evolved, always-freshly-scoped
version of the existing 170-identity §4.1 obligation, generalized to
whatever the current `GENUINE_TEST_GAP` population is at each formal
evidence boundary), (b) mutation-surface completeness (§4.2, already
partly in place), unchanged.

**Advantages:**

- **Semantic fidelity: highest of the three models.** Directly targets the
  material behavioral gap population by construction; immune to population-
  composition drift entirely, since it never depends on a fixed percentage
  computed against a growing/shifting denominator.
- Already partially precedented: §4.1's exact per-identity mechanism
  already exists as a companion condition to the percentage gate; this
  model would only promote it to primary status and demote the percentage.

**Costs:**

- **Classification burden: highest of the three models.** Every future
  formal evidence transaction would need to reproduce a full survivor
  classification exercise (of the kind performed in the post-E005
  assessment and this proposal's own §3) rather than a single number
  comparison — itself a materially larger, more judgment-dependent
  evidence-production task each time.
- **Reproducibility/auditability risk.** A percentage is trivially
  recomputed by anyone from raw counts. A classification-based gate is
  reproducible only if the classification methodology itself is tightly
  governed with worked examples and an independent-review requirement for
  disputed calls — as demonstrated by this very transaction needing a
  dedicated, evidence-heavy trace (§3) to settle just 2 borderline mutants
  out of 406.
- **A distinct, new gaming risk: classification drift.** Model A's raw
  score cannot be gamed except by writing real tests (or the already-
  prohibited denominator manipulation Model B risks). A primarily
  classification-based gate creates a NEW surface: criteria could loosen
  over successive transactions to shrink the "material" count without ever
  closing a real gap — a subtler failure mode than message-text gaming, and
  one this repository's existing governance has no dedicated safeguard
  against today.
- **Longitudinal comparability: weaker.** A percentage is comparable across
  time trivially. "N `GENUINE_TEST_GAP` survivors, 0 remaining" is only
  comparable if the classification methodology is independently re-verified
  as stable at each boundary.
- **Governance complexity: highest of the three models** — establishing a
  rigorous, governed classification methodology as PRIMARY gating authority
  (not merely a companion condition, as §4.1 is today) is a heavier
  undertaking than either Model A or leaving §4.1 as a companion condition.

**Not activated by this transaction.**

## 8. Recommendation

**Recommended: Model A**, conservative candidate `85.736021300875%` (full
precision `85.736021300874857360213008748573602130087485736021...%`,
required numerator `2254` at `total = 2629`), as a **candidate for a future
governed Step 1–9-equivalent recalibration** — not activated here.

**Against the seven criteria:**

1. **Preserves anti-gaming** — the raw metric, formula, and denominator
   semantics are entirely unchanged; only the comparison figure moves,
   using the same derivation method the original threshold itself used.
2. **Reflects real behavior/testing quality** — the candidate figure is
   directly, traceably derived from the current, freshly-classified
   materially-actionable population (40 `GENUINE_TEST_GAP`), exactly as
   Candidate 3 was derived from the original 170.
3. **Does not force brittle message-text tests** — the 344 `LOW_
   MATERIALITY_MESSAGE_TEXT` and 22 equivalent/unreachable survivors remain
   uncredited and unrequired, preserving the original intent exactly.
4. **Remains reproducible/auditable** — a pure arithmetic recomputation
   from already-confirmed categories (`killed`, `confirmed_timeout`, and
   the settled `GENUINE_TEST_GAP` count); any reviewer can independently
   recompute it in seconds.
5. **Minimizes new governance machinery** — reuses the exact existing
   formula (Testing Convention item 7, unchanged), the exact existing §4.1
   per-identity companion-condition pattern, and the exact existing Step
   1–9 sequence; introduces no new exclusion mechanism, no new
   classification-as-primary-gate structure.
6. **Keeps longitudinal evidence interpretable** — still the same raw
   percentage metric, comparable across time exactly as before; only the
   calibration point is refreshed, the same conceptual move the original
   proposal itself made from `feature-engine-mutation-baseline-001.json`'s
   raw `75.898105813194%` to Candidate 3's `87.001959503592%`.
7. **Preserves Condition-2 and Condition-3 safety rails** — Model A touches
   only the Condition-1 numeric comparison; it does not read, reference, or
   alter §4.1's 170-identity mechanism's applicability to Condition 2, nor
   Condition 3's mutation-surface completeness requirement.

Models B and C are recorded for completeness and future reference but are
**not** recommended: Model B carries materially higher anti-gaming risk and
crosses into cross-cutting metric-methodology territory this single-module
proposal should not decide unilaterally; Model C, while offering higher
semantic fidelity, introduces a new classification-drift gaming surface and
a materially heavier, less-reproducible governance burden than Model A's
simple, auditable re-baseline.

**This transaction does not optimize for getting Feature Engine approved
sooner** — both Model A candidate figures remain above the current actual
raw score, so Feature Engine continues to `FAIL` Condition 1 under either
figure exactly as it does under the current effective `87.001959503592%`.

## 9. Proposed recalibration trigger (candidate policy only — not activated)

The existing `feature-engine-mutation-threshold-proposal-001.md` §4.3 lists
three proposed (not effective) recalibration triggers: tool/version change,
165-cohort resolution, and baseline methodology change. **This trigger set
is incomplete** — none of the three, on their own terms, covers what
actually occurred here: the mutation population grew (1531 → 2629) and its
materiality composition shifted (170 material-gap survivors → 40) through
ordinary, legitimate engineering (ADR-043's ownership/fencing
implementation and associated test suites), not a tool/version change, not
165-cohort resolution, and not a formula/contract change (§4.3 trigger 3's
own text). A fourth trigger category is proposed:

> **4. Materiality / mutation-population composition drift (proposed
> candidate, not activated).** If a fresh, governed survivor-classification
> exercise — of the kind performed in
> `feature-engine-condition1-post-e005-survivor-assessment-001.json` and
> this recalibration proposal's own §1/§3 — demonstrates that the
> currently-effective fixed percentage threshold can no longer be reached
> through closure of the population's own `GENUINE_TEST_GAP`-classified
> survivors (plus any `UNSTABLE_TIMEOUT_TRIAGE` mutants that individually
> resolve positive) without ALSO requiring closure of some portion of the
> `LOW_MATERIALITY_MESSAGE_TEXT` and/or `PROVABLY_EQUIVALENT`/
> `STRUCTURALLY_UNREACHABLE` population, this constitutes calibration
> drift. It triggers a mandatory re-baseline through a governed Step 1–9-
> equivalent recalibration proposal (mirroring this transaction's own
> methodology) before the existing fixed threshold may continue to be
> treated as authoritative for a formal Step-9-equivalent PASS
> determination.

**Design notes, addressing why this is not self-activating:**

- **Evidence-gated, not score-gated.** The trigger requires an actual,
  freshly-produced, bounded survivor-classification artifact as its
  evidentiary basis (exactly this transaction's §1 robustness check) — it
  can never fire merely from an aggregate raw-score number moving up or
  down, which would risk becoming a disguised, unreviewed threshold-
  lowering mechanism.
- **No new process invented.** The trigger's own resulting action —"a
  governed Step 1–9-equivalent recalibration proposal" — is the SAME
  mechanism §4.3's existing three triggers already use; only the
  triggering CONDITION is new, not the response machinery.
- **Not activated by this transaction.** No formal determination is made
  here that the trigger is currently "firing" in a binding sense — §1's
  finding is offered as the evidentiary basis a future governed decision
  could rely on, not as a self-executing declaration.

## 10. Non-goals

This transaction does **not**:

- change the currently-effective `87.001959503592%` threshold or its
  two-part gate (§4.1/§4.2 of the existing proposal remain fully
  controlling);
- exclude, skip, or pragma-mark any of the 344 `LOW_MATERIALITY_MESSAGE_
  TEXT` mutants, or any `PROVABLY_EQUIVALENT`/`STRUCTURALLY_UNREACHABLE`
  mutant, from the raw denominator;
- credit any survivor's status without a fresh, individual, formal
  re-measurement;
- implement any Wave 5 (or any) test;
- resolve `contracts.x__seal_verified_authority__mutmut_33`
  (`TOOL_IDENTITY_DRIFT`);
- touch Condition 2 (`169/170`) or Condition 3 (`SATISFIED — REVIEW A
  VALIDATED`) in any way;
- request or fabricate a Product Owner decision;
- author or modify any ADR;
- edit Testing Convention, Chapter 13, ADR-044, or ADR-045;
- edit the currently-effective threshold proposal, Evidence-005, its
  correction, or the post-E005 survivor assessment artifact (all remain
  byte-unchanged).

## 11. Activation requirements (future, not performed here)

A future transaction may activate a recalibrated Condition-1 threshold only
after ALL of:

1. Step 7 — bounded Review A (ChatGPT) of this candidate proposal,
   independently re-verifying §1's arithmetic, §3's equivalence trace, and
   the Model A/B/C comparison;
2. Independent Review B, per Chapter 11 §11.5's minimum-two-reviewer
   requirement (unless the reviewed proposal is itself eligible for
   Delegated Technical Resolution under ADR-045 — a determination reserved
   for that future transaction, not decided here);
3. a fresh Chapter 0 §4b ADR Scope Rule re-run against the reviewed
   boundary's actual final content (not inherited from §12 below);
4. an explicit Product Owner decision naming the exact candidate figure,
   boundary, and review dispositions being approved — never inferred or
   assumed from this candidate document alone;
5. only then, a Step-9-equivalent atomic activation transaction updating
   the controlling threshold artifact (this document's own eventual
   promotion, or a superseding activation record) — mirroring exactly how
   `feature-engine-mutation-threshold-proposal-001.md` itself was approved
   and would need to be superseded, not silently edited in place.

## 12. Rollback / reversal semantics

If a future recalibration is activated and later found defective (e.g., a
Review A finding after activation, or a subsequent materiality-composition
shift), reversal follows the same symmetric mechanism this proposal itself
relies on: a fresh, governed re-proposal transaction (Step 1–9-equivalent)
citing the specific defect, with its own fresh ADR Scope Rule and Risk
Classification — never a silent in-place edit of an already-activated
threshold artifact. The currently-effective `87.001959503592%` threshold
proposal document itself remains the permanent historical record of the
prior calibration; any future activation would supersede it explicitly
(mirroring how ADR supersession is recorded elsewhere in this repository),
never overwrite it.

## 13. ADR Scope Rule — fresh classification against the actual proposed model (Model A)

**Not inherited from the original proposal's `ADR_OPTIONAL`** — re-run
fresh, specifically against Model A (the actual recommended content of this
transaction), per this task's own explicit instruction.

| §4b trigger | Applies to Model A? | Reasoning |
|---|---|---|
| Platform Invariant change | No | No I-1–I-13 invariant touched. |
| Event Schema change | No | No event/fact schema, contract, or field touched. |
| Module Taxonomy/dependency-graph change | No | No `module-registry.yaml`/dependency-edge edit. |
| Governance/Approval-process change | No | Model A reuses the exact existing formula (Testing Convention item 7, unchanged), the exact existing Step 1–9 sequence, and the exact existing §4.1 per-identity companion-condition pattern. The new §9 trigger candidate reuses the SAME resulting mechanism (§4.3's own "governed re-proposal transaction") as the three existing triggers — no new role, lifecycle stage, or approval-gate structure is invented. |
| Decision affecting >1 module | No | Strictly Feature-Engine-only, Tier-1 scope — matches the original proposal's own scope exactly. |
| Hard-to-reverse decision | No | A `CANDIDATE — NOT EFFECTIVE` document with no lifecycle approval; §12's symmetric re-proposal mechanism preserves full reversibility, identical in kind to the original proposal's own reversibility. |
| Locked-ADR modification/supersession | No | No ADR touched. |
| **Alternative: significant but reversible single-module internal change** | **Yes** | A genuinely significant (will eventually gate a real PASS/FAIL dimension) but single-module, contract-preserving, already-delegated-authority (Chapter 13 §13.14 defers exact threshold detail to Testing-Convention-owned territory), fully-reversible candidate — the same textual fit as the original proposal's own §6.2 finding. |

**Explicit distinction, per this task's guidance:** Model A is a pure
numeric Feature-Engine-only recalibration using the same metric and the
same existing Step 1–9 mechanism — it does not touch denominator/exclusion
semantics (that would be Model B, evaluated in §6 and explicitly NOT
recommended) and does not introduce a new approval workflow (that would be
a heavier classification-as-primary-gate structure, Model C, evaluated in
§7 and explicitly NOT activated).

```text
ADR_SCOPE_DISPOSITION: ADR_OPTIONAL
```

**No ADR is authored by this transaction.** Per this task's explicit
instruction, this disposition (not `ADR_REQUIRED`) means the next governed
action is Step 7 review of this candidate proposal, not ADR authoring.

## 14. Risk Classification — candidate, fresh, not self-finalized

This is a candidate policy/quality-gate recalibration proposal, not mere
evidence/bookkeeping recording — `R0` is not assumed. It is also not `R2`:
it carries no Platform Invariant, Event Schema, cross-module, or Locked-ADR
effect, and remains fully reversible via the same symmetric mechanism used
to produce it.

```text
Risk candidate: R1
```

**Rationale:** a significant, single-module (Feature-Engine-only, Tier-1),
fully-reversible policy candidate that will eventually — if and when
separately activated through its own governed decision — gate a real
Quality Gate PASS/FAIL dimension. This is a genuine, substantive proposal
requiring independent review, not a mechanical recording action (ruling out
R0); it has no cross-module, Platform-Invariant, or hard-to-reverse
character (ruling out R2). **This Risk Classification is not self-finalized
Review A** — it is a candidate classification for the separate ChatGPT
Review A this transaction explicitly does not perform.

## 15. State preserved, explicitly verified unchanged

```text
Condition 1 (raw mutation score):  FAIL — criteria (unchanged; the
                                    currently-effective 87.001959503592%
                                    threshold remains controlling; this
                                    proposal changes nothing about it).
Condition 2 (identity resolution): 169/170 (unchanged; remaining item
                                    contracts.x__seal_verified_authority
                                    __mutmut_33, TOOL_IDENTITY_DRIFT — not
                                    touched, not folded into Condition 1).
Condition 3 (formal evidence):     SATISFIED — REVIEW A VALIDATED
                                    (unchanged, not reopened).
P3-FEATURE-QG-EVID-03:              OPEN (unchanged).
Feature Engine approval:           NOT APPROVED.
LIVE:                               NOT_AUTHORIZED.
```

**Explicitly confirmed byte-unchanged (git diff --stat empty):**
`feature-engine-mutation-threshold-proposal-001.md`,
`feature-engine-mutation-step9-formal-evidence-005.json`,
`feature-engine-mutation-step9-formal-evidence-005-correction-001.json`,
`feature-engine-condition1-post-e005-survivor-assessment-001.json`,
`docs/engineering/testing.md`, `docs/constitution/13-quality-gates.md` (and
all other Constitution chapters), `docs/adr/ADR-044.md`,
`docs/adr/ADR-045.md`, and all `python/feature-engine/src`,
`python/feature-engine/tests`, `python/feature-engine/tooling` files.
