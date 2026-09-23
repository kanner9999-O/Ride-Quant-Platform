# Feature Engine Condition-1 Threshold — Recalibration Proposal 001

**STATUS: CANDIDATE — NOT EFFECTIVE / AWAITING REVIEW A RE-REVIEW**

This document is a **proposal only**. It does not activate, apply, or
change the currently-effective threshold. The existing
`feature-engine-mutation-threshold-proposal-001.md` (blob
`f4a3ca0c37aeb4684409a7344141103e64051e04`, status `APPROVED — EFFECTIVE`)
remains byte-unchanged and remains the sole controlling Condition-1
threshold: `87.001959503592%`, two-part gate (aggregate raw score **and**
§4.1's per-identity resolution condition). No Product Owner decision is
requested by this transaction.

**Bounded correction (this transaction), remediating Review A findings on
the prior candidate (reviewed boundary `bc7e0c9df45ff8e02451078ca7b74a54bac43ee5`):**
Review A returned `REVISION_REQUIRED — 0 Blocker / 2 Major / 2 Minor`, Risk
`R1`, ADR Scope `ADR_OPTIONAL`. Per current ADR-045/Chapter 11 governance,
R1 requires no independent cross-check by default — this correction is
remediated on Review A's own finding, not self-closed.

- `MAJOR-01`: **REMEDIATED — PENDING REVIEW A RE-REVIEW.** Model A lacked a
  current-material-identity companion condition, recreating the exact
  aggregate-only loophole the original threshold proposal's own
  `P3-PY-MUT-THRESH-A-MAJ-01` correction already closed once. §5 below now
  defines an explicit two-part gate: Condition 1A (aggregate raw score) AND
  Condition 1B (all 42 pinned current-material identities individually
  resolved), reusing the existing §4.1 per-identity pattern.
- `MAJOR-02`: **REMEDIATED — PENDING REVIEW A RE-REVIEW.** §3 below
  corrects the classification of `ownership.acquire_and_activate
  __mutmut_21`/`_23` from `PROVABLY_EQUIVALENT` to `GENUINE_TEST_GAP` — the
  prior equivalence conclusion relied on a false single-thread-only
  observability assumption; `owner.handle`/`owner.state` are public
  properties with no lock/actor-isolation contract preventing a concurrent
  reader from observing the intermediate `CATCHING_UP` handle.
- `MINOR-01`: **REMEDIATED — PENDING REVIEW A RE-REVIEW.** §11 below
  corrects the review/decision authority to current ADR-045/Chapter 11
  semantics (Review A only at R1, no Independent Review B) and explicitly
  states DTR's ineligibility for the threshold-selection decision itself
  (ADR-045 D10).
- `MINOR-02`: **REMEDIATED — PENDING REVIEW A RE-REVIEW.** §12 below
  replaces the prior ambiguous activation language with one exact future
  SSOT (single source of truth) authority transition.

This document's content is corrected directly (not preserved-verbatim-and-
annotated), consistent with how the currently-effective threshold
proposal's own analogous bounded correction was recorded — it is
analysis/proposal output, not a historical transaction log; the correction
narrative itself is recorded in `docs/MANIFEST.md`/`docs/CHANGELOG.md`.
**Not self-closed** — remediated pending a subsequent bounded Review A
re-review, not performed by this transaction.

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
| Current-material gap set (this correction, new) | `docs/governance/mutation-baseline-evidence/feature-engine-condition1-current-material-gap-set-001.json` | `6360c8c1ad6e7c21129fa3b75415486d5447bf52` | Created this transaction |

**Post-E005 assessment identity, fresh-verified (exact match, no drift).
The assessment artifact itself remains byte-immutable — it is NOT edited by
this correction; the figures below are its own original, unedited
classification:**

```text
survivors:            406
GENUINE_TEST_GAP:      40
LOW_MATERIALITY_MESSAGE_TEXT: 344
PROVABLY_EQUIVALENT:   16
STRUCTURALLY_UNREACHABLE: 4
UNCLEAR:                2
```

**Settled classification after this correction's `MAJOR-02` remediation
(§3 below; analytical resolution recorded in this proposal only, the
assessment artifact is not edited):**

```text
GENUINE_TEST_GAP:              42  (40 + 2, both formerly-UNCLEAR mutants
                                    reclassified)
LOW_MATERIALITY_MESSAGE_TEXT: 344  (unchanged)
PROVABLY_EQUIVALENT:           16  (unchanged — NOT 18; the 2 formerly-
                                    UNCLEAR mutants moved to GENUINE_TEST_GAP,
                                    not PROVABLY_EQUIVALENT)
STRUCTURALLY_UNREACHABLE:       4  (unchanged)
UNCLEAR:                        0  (settled)
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

**Credible test-remediation ceiling (settled, §3's `MAJOR-02` correction
resolves the 2 formerly-`UNCLEAR` survivors to `GENUINE_TEST_GAP`, not
hypothetically — this is now the definite figure, not an upper bound):**

```text
42 GENUINE_TEST_GAP (settled) + 9 UNSTABLE = 51
2214 + 51 = 2265
2265 < 2288  →  shortfall = 23
```

**Robustness check (independently recomputed, cardinality unchanged by the
`MAJOR-02` reclassification):** even crediting every single non-message-
text survivor — including the 16 `PROVABLY_EQUIVALENT` and 4
`STRUCTURALLY_UNREACHABLE` mutants, which Testing Convention v0.17 item 8's
raw-denominator-by-default rule explicitly forbids crediting without an
individually-pinned, separately-governed equivalent-mutant adjustment — as
if all were killed:

```text
42 genuine (settled) + 16 equivalent + 4 unreachable + 9 unstable = 71
2214 + 71 = 2285
2285 < 2288  →  shortfall = 3
```

**Independently verified: both arithmetic chains reconcile exactly** against
this task's own cited figures (`74`/`65` gaps, `51`/`71` combined credits,
`2265`/`2285` resulting numerators, `23`/`3` shortfalls) — the `MAJOR-02`
reclassification moves the 2 formerly-`UNCLEAR` mutants from the "unclear"
slot into the "genuine" slot within the SAME 71-mutant maximal
non-message-text population; the combined total, and therefore this
robustness finding, is **unchanged in cardinality and unchanged in
conclusion**. No discrepancy found.

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
with a **different, independently re-derived materiality composition** (42
material, settled per §3, not 170), and the fixed percentage carried
forward unchanged no longer encodes the same closure obligation it was
built to represent.

**Disposition:**

```text
CALIBRATION_DRIFT_CONFIRMED
```

## 3. Fresh resolution of the 2 UNCLEAR survivors (folded in, no separate WP) — corrected by Review A `MAJOR-02`

```text
feature_engine.ownership.xǁAuthoritativeSubjectOwnerǁacquire_and_activate__mutmut_21
feature_engine.ownership.xǁAuthoritativeSubjectOwnerǁacquire_and_activate__mutmut_23
```

**`MAJOR-02` (Review A, this correction): the prior candidate's
`PROVABLY_EQUIVALENT` conclusion is WRONG.** It relied on a false premise —
that Python's single-threaded, synchronous execution *within one method
call* is the only relevant observability boundary. That premise ignores
that `acquire_and_activate` is a method on a **shared, mutable object**
(`AuthoritativeSubjectOwner`), and `owner.handle`/`owner.state` are
**public properties** with no lock, no actor-isolation contract, and no
single-thread-only authority anywhere in `ownership.py` or ADR-043 itself.
ADR-043 explicitly treats thread/process scheduling and concurrent
acquisition attempts as real runtime concerns the module's own fencing
design exists to address — it does not assume or require single-threaded
access to an owner instance.

Both mutate one field of the intermediate `OwnerHandle` constructed at
`self._handle = OwnerHandle(self._feature_subject_id, generation,
SubjectOwnershipState.CATCHING_UP)` inside `acquire_and_activate`
(`ownership.py:538`) — mutmut_21 nulls `self._feature_subject_id`;
mutmut_23 nulls `SubjectOwnershipState.CATCHING_UP`. The method explicitly
transitions `INACTIVE → CATCHING_UP → ACTIVE`, and `self._catch_up(...)` —
called while the handle is at `CATCHING_UP` — is exactly the kind of
externally-triggerable, potentially slow/blocking operation (a history
provider read) a concurrent reader can legitimately observe mid-flight.

**A legitimate, non-gaming, production-semantic deterministic test is
constructible** (not implemented by this correction, per instruction):

```text
1. Run acquire_and_activate in worker thread A.
2. Use a blocking/synchronized test-double history-provider seam (a
   legitimate fake, per this module's own documented fake-based testing
   convention) to hold execution inside _catch_up after the CATCHING_UP
   handle has been assigned at ownership.py:538.
3. From thread B, read owner.handle / owner.state while thread A is
   blocked inside _catch_up.
4. Assert the observed handle's feature_subject_id equals the real,
   expected subject id, and its state equals SubjectOwnershipState.
   CATCHING_UP.
```

Under `mutmut_21`, thread B would observe `feature_subject_id = None`.
Under `mutmut_23`, thread B would observe `state = None`. Both are
concretely, deterministically **observable behavioral changes** through
the object's own public interface — not an impossible or fabricated
internal state, and not implementation trivia: `owner.handle`/`owner.state`
are the documented, intended public surface for inspecting ownership
progress.

**Why the prior conclusion's "no external observer" claim was incorrect:**
it is true that *within the single call to `acquire_and_activate` itself*,
no code path re-reads `self._handle` before the final overwrite — that part
of the prior trace was accurate. What it missed is that "no code path
within this method reads it" is not the same claim as "no observer anywhere
in the running process can read it" — the intermediate assignment mutates
shared object state (`self._handle`) that is reachable, via the object's
own public `.handle`/`.state` properties, from any other thread holding a
reference to the same `owner` instance, at any point before the
overwriting statement executes. This is a materially different (and
correct) observability analysis than the single-call, single-threaded
trace the prior candidate relied on.

**Questions, answered directly (corrected):**

- *Is the intermediate `CATCHING_UP` `OwnerHandle` observably meaningful?*
  **Yes.** It is reachable via `owner.handle`/`owner.state` from any
  concurrent reader before the method's own later overwrite executes.
- *Is `self._handle` deterministically overwritten before any external or
  failure-path observation?* **Only from the perspective of the SAME
  calling thread's own subsequent statements** — not from the perspective
  of a genuinely concurrent reader on another thread, which is exactly what
  ADR-043's own fencing/concurrency design contemplates as a real scenario.
- *Can a legitimate production-semantic test distinguish either mutation?*
  **Yes** — via the deterministic concurrent-observation construction
  above, using only the object's own public interface and a legitimate
  test-double history-provider seam; no impossible state, no mutant-name
  assertion, no message-text snapshotting.
- *Classification:* **`GENUINE_TEST_GAP`** for both `mutmut_21` and
  `mutmut_23`.

**Settled classification (this transaction, supersedes both the post-E005
assessment's `UNCLEAR` label AND this proposal's own prior, Review-A-
corrected `PROVABLY_EQUIVALENT` conclusion, for exactly these two IDs — the
assessment artifact itself is NOT edited, per §16's immutability
requirement; this is a forward-looking analytical resolution recorded
here, and in the new pinned identity artifact §"Current-material gap set"
below, only):**

```text
GENUINE_TEST_GAP:              42  (40 + 2, settled)
LOW_MATERIALITY_MESSAGE_TEXT: 344  (unchanged)
PROVABLY_EQUIVALENT:           16  (unchanged)
STRUCTURALLY_UNREACHABLE:       4  (unchanged)
UNCLEAR:                        0  (settled)
```

**Robustness re-confirmed:** both mutants were already counted within §1's
71-mutant maximal non-message-text robustness hypothetical (under the
"unclear" label); moving them to "genuine" changes which label they sit
under, not the total population credited in that hypothetical — the §1
shortfall-of-3 finding is **unchanged and robust to this correction**. The
settled, non-hypothetical genuine-test-gap population is now precisely
**42** — this directly grounds §"Current-material gap set" and the
corrected Model A derivation in §5 below.

### Current-material gap set (new pinned identity artifact, this correction)

`docs/governance/mutation-baseline-evidence/feature-engine-condition1-current-material-gap-set-001.json`
(blob `6360c8c1ad6e7c21129fa3b75415486d5447bf52`) pins the exact 42-ID set
this settled classification defines — the 40 `GENUINE_TEST_GAP` identities
from the post-E005 assessment plus the 2 identities reclassified above.
Fresh-verified: `count = 42`, `duplicates = 0`, sorted-set
`sha256 = 932698b4b312c1a8f70c261426555a5c6f3566579ed0a27102d4a0f0214adedc`.
This artifact is the pinned identity source for Condition 1B (§5 below) —
it is a **new, current-boundary obligation, entirely separate from and not
a replacement for** Condition 2's independent, historical 170-identity
obligation (§4.1 of the currently-effective threshold proposal).

## 4. Current population/materiality analysis (Model A's own basis) — settled figures per §3's `MAJOR-02` correction

```text
total                          2629
killed                         2209
confirmed_timeout                 5   (→ 2214 combined, formula-numerator basis)
unstable_timeout_triage           9   (not yet credited — pending individual
                                       re-confirmation per Testing Convention
                                       item 8's timeout-specific rule)
survived (406), decomposed:
  GENUINE_TEST_GAP                42  (40 from the post-E005 assessment +
                                       2 reclassified by this correction's
                                       MAJOR-02 remediation — the direct
                                       analog of the original 170-mutant
                                       "material actionable-test-gap"
                                       population; pinned identity list:
                                       feature-engine-condition1-current-
                                       material-gap-set-001.json)
  LOW_MATERIALITY_MESSAGE_TEXT   344  (the direct analog of the original
                                       174 "low-priority-but-real" +
                                       message-text population — NOT to be
                                       required for closure, per original
                                       intent)
  PROVABLY_EQUIVALENT             16  (analog of the original 25 candidate-
                                       equivalents — remains in the raw
                                       denominator, uncredited, per Testing
                                       Convention item 8, unless and until a
                                       separate governed per-identity
                                       adjustment is recorded; NOT 18 — the
                                       2 formerly-UNCLEAR mutants settled
                                       to GENUINE_TEST_GAP, not this
                                       category, per §3's correction)
  STRUCTURALLY_UNREACHABLE         4  (dead-field/defensive-fallback
                                       mutants — same treatment as
                                       PROVABLY_EQUIVALENT for scoring
                                       purposes: real, but not creditable
                                       without a separate governed
                                       adjustment)
```

## 5. Model A — numeric re-baseline, same raw metric — corrected by Review A `MAJOR-01`

**`MAJOR-01` (Review A, this correction): the prior candidate's Model A
enforced only the aggregate percentage.** This recreates, at the
recalibrated boundary, the exact loophole the currently-effective
threshold proposal's own `P3-PY-MUT-THRESH-A-MAJ-01` correction already
closed once at the original boundary: an unrelated set of low-materiality/
message-text kills could numerically satisfy the aggregate percentage
while leaving every one of the 42 pinned current-material identities
exactly as they are today. Model A is now corrected to an explicit
**two-part gate**, mirroring §4.1 of the currently-effective threshold
proposal exactly:

```text
Condition 1A: raw mutation-effectiveness >= recalibrated numeric threshold
              (necessary but not sufficient)

AND

Condition 1B: every one of the 42 exact current-material-gap mutant
              identities pinned in
              feature-engine-condition1-current-material-gap-set-001.json
              (blob 6360c8c1ad6e7c21129fa3b75415486d5447bf52) is
              individually resolved via exactly one of:
                (a) Killed / confirmed_timeout in a fresh, formal mutation
                    measurement; OR
                (b) Individually reclassified — a SEPARATE, governed
                    decision, exact mutant identity + specific semantic
                    justification + a separate reviewed/recorded decision
                    (never a blanket, unreviewed claim).
              No blanket classification. No score-offset substitution.
              Killing unrelated (e.g. message-text) mutants must NEVER
              satisfy Condition 1B.
```

This is a direct, structurally identical reuse of the currently-effective
proposal's own §4.1 per-identity resolution mechanism, applied to the
current-boundary 42-identity set instead of the historical 170-identity
set — not an invented new mechanism (see §14's ADR Scope re-analysis).

**Formula unchanged:** `mutation_score = (killed + confirmed_timeout) /
(total − skipped) × 100` (Testing Convention v0.17 item 7, unchanged, this
proposal does not modify it). `skipped = 0` in Evidence-005 (all ten
statuses reconciled to `total`).

**Same conceptual principle as Candidate 3:** close the current materially-
actionable behavioral gap population (today's settled 42 `GENUINE_TEST_GAP`
survivors — the direct analog of the original 170) without requiring
closure of the low-materiality/message-text population (today's 344
`LOW_MATERIALITY_MESSAGE_TEXT`, analog of the original 174) or crediting
equivalents/unreachables (today's 16 `PROVABLY_EQUIVALENT`/4
`STRUCTURALLY_UNREACHABLE`, analog of the original 25 candidate-
equivalents).

**Corrected candidate numerator and threshold (Condition 1A), using exact
count semantics as the normative derivation — supersedes the prior
candidate's `85.736021300875%`:**

```text
current confirmed numerator:  2214  (killed 2209 + confirmed_timeout 5)
current genuine material gaps: 42  (settled, §3's MAJOR-02 correction)
candidate numerator:          2214 + 42 = 2256

candidate threshold = 2256 / 2629 × 100
= 85.812095853936858120958539368581209585393685812096...%
display, same 12-decimal-place convention as the original: 85.812095853937%
```

`85.736021300875%` (the prior candidate's recommended figure, derived from
40 rather than the settled 42) is **removed as the recommended figure** —
it is retained below only as superseded historical candidate-analysis
prose, per this correction's own instruction.

**Best-case variant (pending unstable-triage resolution — NOT recommended
as the final method, since it depends on 9 not-yet-individually-confirmed
mutants; provided only for transparency):**

```text
(2214 + 42 + 9) / 2629 × 100 = 2265 / 2629 × 100
= 86.154431342715861544313427158615443134271586154431...%
display: 86.154431342716%
```

**Explicit distinctions (per this task's own requirement):**

| Population | Count | Credited in Model A candidate (Condition 1A numerator)? | Individually required (Condition 1B)? |
|---|---|---|---|
| Current already-positive numerator (killed + confirmed_timeout) | 2214 | Yes — base | N/A |
| Current materially-actionable survivors (`GENUINE_TEST_GAP`, settled) | 42 | Yes — the closure target, exactly mirroring the original 170 | **Yes — each of the exact 42 pinned identities, individually** |
| Unresolved/unclear population | 0 (settled this transaction, §3) | N/A | N/A |
| Unstable triage (pending) | 9 | No, in the recommended candidate; yes, only in the disclosed best-case variant | No |
| Message-text-only population | 344 | **No** — never required, matching original intent | **No — may never substitute for Condition 1B** |
| Equivalent/unreachable population | 16 + 4 = 20 | **No** — remains uncredited per Testing Convention item 8, matching original intent | No |

**Why this candidate, not the best-case variant, is recommended as the
final auditable method:** it is computable and verifiable TODAY from
already-confirmed categories only (`killed`, `confirmed_timeout`, and this
correction's own settled 42-identity `GENUINE_TEST_GAP` classification); it
never depends on an outstanding measurement (the 9
`unstable_timeout_triage` mutants' eventual disposition is explicitly
unresolved and, per Testing Convention item 8, must not be credited before
individual re-confirmation). This mirrors Candidate 3's own preference for
"explicit traceability to a named, closeable gap set" over inspection-based
ranges.

**Not chosen merely because it passes today:** current raw score is
`84.21453023963484%–84.55686572841384%`. Both Model A candidate figures
(`85.812095853937%` and `86.154431342716%`) are **above** the current
actual score — Feature Engine would still `FAIL` Condition 1 under either
recalibrated figure today. This is the same non-negotiable discipline the
original proposal applied when rejecting Candidate 1 (~76%, "round the
current baseline up to itself").

**Normative derivation rule:** `required numerator = 2256` at `total =
2629` is the exact-count basis for this candidate — not a formula to be
mechanically re-applied if the population changes. If a future formal
mutation population changes (population growth, a mutmut version change,
or a fresh survivor-classification exercise), the normal governed
recalibration/drift rules (§9's proposed trigger, or the existing §4.3
triggers) apply; `2256`/`85.812095853937%` must never be silently
transplanted onto a different population.

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

## 8. Recommendation — corrected by Review A `MAJOR-01`/`MAJOR-02`

**Recommended: Model A**, corrected two-part gate — **Condition 1A**
(candidate numeric threshold `85.812095853937%`, full precision
`85.812095853936858120958539368581209585393685812096...%`, required
numerator `2256` at `total = 2629`) **AND Condition 1B** (all 42 exact
current-material-gap identities in
`feature-engine-condition1-current-material-gap-set-001.json` individually
resolved) — as a **candidate for a future governed Step 1–9-equivalent
recalibration** — not activated here.

**Against the seven criteria:**

1. **Preserves anti-gaming** — the raw metric, formula, and denominator
   semantics are entirely unchanged; the comparison figure moves, using the
   same derivation method the original threshold itself used, AND
   Condition 1B (corrected, `MAJOR-01`) now forecloses the aggregate-only
   loophole an unrelated set of low-materiality kills could otherwise
   exploit — exactly mirroring the currently-effective proposal's own
   §4.1 safeguard.
2. **Reflects real behavior/testing quality** — the candidate figure is
   directly, traceably derived from the current, settled materially-
   actionable population (42 `GENUINE_TEST_GAP`, corrected per `MAJOR-02`),
   exactly as Candidate 3 was derived from the original 170; Condition 1B
   further requires those SPECIFIC 42 identities, not merely an equal-sized
   unrelated set.
3. **Does not force brittle message-text tests** — the 344 `LOW_
   MATERIALITY_MESSAGE_TEXT` and 20 equivalent/unreachable survivors remain
   uncredited, unrequired, and explicitly ineligible to satisfy Condition
   1B, preserving the original intent exactly.
4. **Remains reproducible/auditable** — a pure arithmetic recomputation
   from already-confirmed categories (`killed`, `confirmed_timeout`, and
   the settled 42-identity `GENUINE_TEST_GAP` classification, pinned in a
   dedicated artifact with a verifiable sorted-set hash); any reviewer can
   independently recompute the numerator and re-verify the exact identity
   set in seconds.
5. **Minimizes new governance machinery** — reuses the exact existing
   formula (Testing Convention item 7, unchanged), the exact existing §4.1
   per-identity companion-condition pattern (now explicitly applied as
   Condition 1B, not merely referenced), and the exact existing Step 1–9
   sequence; introduces no new exclusion mechanism, no new classification-
   as-primary-gate structure.
6. **Keeps longitudinal evidence interpretable** — still the same raw
   percentage metric, comparable across time exactly as before; only the
   calibration point is refreshed, the same conceptual move the original
   proposal itself made from `feature-engine-mutation-baseline-001.json`'s
   raw `75.898105813194%` to Candidate 3's `87.001959503592%`.
7. **Preserves Condition-2 and Condition-3 safety rails** — Model A's
   Condition 1B is explicitly a NEW, current-boundary obligation, entirely
   separate from Condition 2's independent, historical 170-identity
   obligation (currently `169/170`) — they answer different questions
   (current-boundary material gaps vs. historically-pinned closure) and are
   never merged; Condition 3's mutation-surface completeness requirement is
   untouched.

Models B and C are recorded for completeness and future reference but are
**not** recommended: Model B carries materially higher anti-gaming risk and
crosses into cross-cutting metric-methodology territory this single-module
proposal should not decide unilaterally; Model C, while offering higher
semantic fidelity, introduces a new classification-drift gaming surface and
a materially heavier, less-reproducible governance burden than Model A's
simple, auditable re-baseline plus companion identity gate.

**This transaction does not optimize for getting Feature Engine approved
sooner** — both Model A candidate figures (`85.812095853937%` and the
disclosed best-case `86.154431342716%`) remain above the current actual raw
score, so Feature Engine continues to `FAIL` Condition 1 under either figure
exactly as it does under the current effective `87.001959503592%`.

## 9. Proposed recalibration trigger (candidate policy only — not activated)

The existing `feature-engine-mutation-threshold-proposal-001.md` §4.3 lists
three proposed (not effective) recalibration triggers: tool/version change,
165-cohort resolution, and baseline methodology change. **This trigger set
is incomplete** — none of the three, on their own terms, covers what
actually occurred here: the mutation population grew (1531 → 2629) and its
materiality composition shifted (170 material-gap survivors → 42, settled)
through ordinary, legitimate engineering (ADR-043's ownership/fencing
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
- implement any Wave 5 (or any) test — including the deterministic
  concurrent-observation test construction described in §3 for
  `acquire_and_activate__mutmut_21`/`_23`, which is described only, not
  implemented, per this correction's own explicit instruction;
- resolve `contracts.x__seal_verified_authority__mutmut_33`
  (`TOOL_IDENTITY_DRIFT`);
- touch Condition 2 (`169/170`) or Condition 3 (`SATISFIED — REVIEW A
  VALIDATED`) in any way, or merge Condition 1B into Condition 2 — they
  remain independent obligations answering different questions;
- request or fabricate a Product Owner decision;
- author or modify any ADR;
- edit Testing Convention, Chapter 13, ADR-044, or ADR-045;
- edit the currently-effective threshold proposal, Evidence-005, its
  correction, or the post-E005 survivor assessment artifact (all remain
  byte-unchanged);
- edit the new `feature-engine-condition1-current-material-gap-set-001.json`
  artifact after this transaction creates it — it is a pinned identity
  snapshot, not a living document.

## 11. Activation requirements (future, not performed here) — corrected by Review A `MINOR-01`

**`MINOR-01` (Review A, this correction): the prior candidate's review/
decision authority citations were stale.** The prior text cited "Chapter 11
§11.5's minimum-two-reviewer requirement" as controlling for this proposal.
That is no longer current governing authority for a Feature-Engine-only,
R1-classified quality-policy proposal — **current ADR-045/Chapter 11 v2.4
review semantics control**, fresh-verified this transaction directly from
`docs/adr/ADR-045.md`:

```text
R1 — Bounded semantic / normal implementation risk... Default: NO
  CROSS-CHECK -- Review A is sufficient unless Review A or the Product
  Owner escalates the specific case to R2 because actual uncertainty/risk
  is materially higher than the nominal category suggests.
```

(`ADR-045.md`, "Decision — R0/R1/R2 definitions", R1 entry, fresh-read this
transaction, blob `ac13ece16ff644d0d88ddf982d83bfb0e8d5ad16`, unchanged.)

**Corrected activation requirements** — a future transaction may activate a
recalibrated Condition-1 threshold only after ALL of:

1. Step 7 — bounded Review A (ChatGPT) of this candidate proposal (this
   correction's own reviewed subject), independently re-verifying §1's
   arithmetic, §3's corrected classification/observability trace, the
   corrected Model A two-part gate, and the Model A/B/C comparison;
2. **No Independent Review B is required at R1** under current ADR-045/
   Chapter 11 v2.4 governance — R1's default is Review A alone, no
   cross-check, unless Review A or the Product Owner itself escalates this
   specific case to R2 (not decided by this correction). The Testing
   Convention v0.17 9-step text's own "review → Product Owner decision"
   wording (item sequence, §0) still uses pre-ADR-045-era "Review A +
   Independent Review B" phrasing in places — this is recorded as a known,
   lower-tier **documentation-alignment residual** that does **not**
   override current, higher-precedence ADR-045/Chapter 11 governance
   authority (ADR > Testing Convention, per this repository's own
   authority-precedence ordering); it is not remediated by this correction
   (out of scope — no Testing Convention edit performed, per §10's
   non-goals);
3. a fresh Chapter 0 §4b ADR Scope Rule re-run against the reviewed
   boundary's actual final content (not inherited from §14 below);
4. **an explicit Product Owner decision on the numeric threshold
   specifically** — this reservation is controlling and is **not** waived
   or narrowed by R1's no-cross-check default. Testing Convention v0.17's
   own governed 9-step sequence explicitly names "Product Owner decision"
   as its own distinct step (Step 8), and the currently-effective
   threshold proposal's own §8 (Product Owner approval record) confirms
   this class of decision is a named, governing-artifact-reserved Product
   Owner action. Under ADR-045 `D10(a)` ("a governing artifact explicitly
   reserves this decision class to Product Owner"), this is exactly such a
   reservation:

   ```text
   DTR is NOT eligible for the threshold-selection decision.
   Reason: ADR-045 D10(a) -- a governing artifact (the currently-effective
     threshold proposal's own §8 Product-Owner-decision precedent, and
     Testing Convention v0.17's own named Step-8 "Product Owner decision")
     explicitly reserves the threshold-selection decision to Product
     Owner. D10 fails closed on EITHER of its two independent conditions
     alone -- (a) alone is sufficient here, regardless of D1-D9/D11/D12's
     outcome.
   ```

   DTR is explicitly **not offered as an alternative approval path** for
   the numeric threshold decision itself, even if a future Review A on
   this proposal returns CLEAN and even though R1 requires no cross-check —
   D10(a)'s governing-artifact reservation is independent of, and controls
   over, the R1 no-cross-check default. An explicit Product Owner decision
   naming the exact candidate figure, boundary, and review disposition
   being approved remains required — never inferred or assumed from this
   candidate document alone;
5. only then, a Step-9-equivalent atomic activation transaction performing
   the exact future SSOT authority transition defined in §12 below.

## 12. Exact future SSOT authority transition — corrected by Review A `MINOR-02`

**`MINOR-02` (Review A, this correction): the prior candidate left future
activation ambiguous** between "promote this document" and "a superseding
activation record." Replaced with one exact authority transition,
**defined only as future activation semantics — not performed now**:

**Before activation (current state, unchanged by this proposal or this
correction):**

```text
feature-engine-mutation-threshold-proposal-001.md
  = APPROVED -- EFFECTIVE
  = sole current Feature Engine Condition-1 threshold authority
```

**After a future activation of this recalibration proposal (not performed
here — requires the full §11 activation sequence, including the
Product-Owner-reserved threshold decision):**

```text
feature-engine-mutation-threshold-recalibration-proposal-001.md
  = APPROVED -- EFFECTIVE
  = sole current Feature Engine Condition-1 threshold authority

feature-engine-mutation-threshold-proposal-001.md
  = historical / superseded threshold authority
  = file remains byte-unchanged (never mutated merely to change its own
    lifecycle-state label -- its own internal STATUS banner is itself part
    of the permanent historical record and is not retroactively edited)
```

A future activation transaction's own `docs/MANIFEST.md` update must
atomically write a **canonical current-threshold pointer/state** — a single
unambiguous field naming which artifact is the sole current Condition-1
threshold authority at that boundary — so that no reader is ever required
to infer current authority from two documents' independent STATUS banners.
The superseded document is historical evidence, not a candidate for
lifecycle-state mutation; only the superseding document's own STATUS
banner and the MANIFEST pointer change.

## 13. Rollback / reversal semantics

If a future recalibration is activated and later found defective (e.g., a
Review A finding after activation, or a subsequent materiality-composition
shift), reversal follows the same symmetric mechanism this proposal itself
relies on: a fresh, governed re-proposal transaction (Step 1–9-equivalent)
citing the specific defect, with its own fresh ADR Scope Rule and Risk
Classification — never a silent in-place edit of an already-activated
threshold artifact. The currently-effective `87.001959503592%` threshold
proposal document itself remains the permanent historical record of the
prior calibration; any future activation would supersede it explicitly per
§12's exact transition above (mirroring how ADR supersession is recorded
elsewhere in this repository), never overwrite it.

## 14. ADR Scope Rule — fresh classification against the actual corrected proposed model (Model A, now with Condition 1A/1B)

**Not inherited from the original proposal's `ADR_OPTIONAL`, and not
mechanically carried forward from this document's own prior candidate's
`ADR_OPTIONAL`** — re-run fresh, specifically against Model A's now-
corrected content (the two-part Condition 1A/1B gate, and the new pinned
42-identity artifact), per this task's own explicit instruction not to
force the expected classification.

| §4b trigger | Applies to corrected Model A? | Reasoning |
|---|---|---|
| Platform Invariant change | No | No I-1–I-13 invariant touched. |
| Event Schema change | No | No event/fact schema, contract, or field touched. |
| Module Taxonomy/dependency-graph change | No | No `module-registry.yaml`/dependency-edge edit. |
| Governance/Approval-process change | **No — re-examined specifically for the `MAJOR-01` correction's added Condition 1B, not merely re-asserted.** Is a companion condition requiring 42 specific, pinned mutant identities to each be individually resolved — via a NEW dedicated identity artifact — a NEW governance mechanism, or an application of an EXISTING one? Condition 1B's own resolution semantics are VERBATIM the currently-effective proposal's own §4.1 pattern: "(a) killed/confirmed_timeout in a fresh formal measurement; OR (b) individually reclassified — a separate, governed decision... never a blanket, unreviewed claim." This is the same conclusion the currently-effective proposal's own §6.1 reached for its own analogous §4.1 addition — a direct, structurally identical reuse of an already-established pattern (also, independently, Testing Convention item 8's equivalent-mutant-adjustment mechanism), applied to a current-boundary identity set instead of a historical one. The pinned-identity artifact itself is inert data (a sorted ID list + hash), not a new review role, lifecycle stage, or approval-gate structure. The §9 trigger candidate similarly reuses the SAME resulting mechanism (§4.3's own "governed re-proposal transaction") as the three existing triggers. Conclusion unchanged: no new governance/approval-process machinery is created. |
| Decision affecting >1 module | No | Strictly Feature-Engine-only, Tier-1 scope — matches the original proposal's own scope exactly. |
| Hard-to-reverse decision | No | A `CANDIDATE — NOT EFFECTIVE` document with no lifecycle approval; §13's symmetric re-proposal mechanism preserves full reversibility, identical in kind to the original proposal's own reversibility. |
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

## 15. Risk Classification — candidate, fresh, not self-finalized

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

## 16. State preserved, explicitly verified unchanged

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
