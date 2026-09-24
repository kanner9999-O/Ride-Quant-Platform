# Feature Engine Condition-1 Threshold — Recalibration Proposal 003

**STATUS: CANDIDATE — NOT EFFECTIVE / AWAITING REVIEW A**

This document proposes a **third** Condition-1 threshold correction, built
on `FE-EVID03-COND1-WAVE6-CLASSIFICATION-DTR-001`'s Review-A-validated
six-identity semantic reclassification of the active 24-identity Condition-
1B population. It does **not** change the currently-effective threshold. It
does **not** request a Product Owner decision. It is authored candidate
content only, pending its own Review A.

## 0. Authority resolved directly (fresh-read, not restated from memory)

| Artifact | Path | Blob | Fresh-verified |
|---|---|---|---|
| Currently-effective threshold (sole current authority, unchanged by this candidate) | `docs/governance/mutation-baseline-evidence/feature-engine-mutation-threshold-recalibration-proposal-002.md` | `ea0b7a79b733622388597c59346c4615bb2726db` | Yes |
| Currently-effective Condition-1B companion artifact (unchanged by this candidate) | `docs/governance/mutation-baseline-evidence/feature-engine-condition1-current-material-gap-set-002.json` | `2e6030c5581df51323937de0bd5f646f3e98b5d9` | Yes — 24 identities, sorted-set sha256 `6c8181f7665a63494632ef89514ea7efdf9948c544c9a9a8094e87c17c3d2543` |
| Wave-6 test remediation evidence | `docs/governance/mutation-baseline-evidence/feature-engine-condition1-wave6-test-remediation-001.json` | `3dc2566222581f6e5e1f69c52b7e54fe13861348` | Yes — `7/13 KILLED_BY_WAVE6`, `6/13 CLASSIFICATION_CONTRADICTION_DISCOVERED` |
| Wave-6 classification DTR (`FE-EVID03-COND1-WAVE6-CLASSIFICATION-DTR-001`) | `docs/governance/mutation-baseline-evidence/feature-engine-condition1-wave6-classification-dtr-001.json` | `10404ae948cf7aefbeb5d9b416bb0ca12038538a` | Yes — 6 identities RECLASSIFIED (3 `PROVABLY_EQUIVALENT`, 3 `STRUCTURALLY_UNREACHABLE`); remaining genuine-material sha256 `e4d21a0f1765f860d48d8a607c5d4e25b5b43c88f76db631cdd8528d83f73872` |
| Prior material-set DTR (`FE-EVID03-COND1-MATERIAL-SET-DTR-001`) | `docs/governance/mutation-baseline-evidence/feature-engine-condition1-material-gap-dtr-001.json` | `fe43ffe2ac460fc42551617d9bb7781e52a07f26` | Yes — final partition at its own boundary `GENUINE_TEST_GAP=24 / NON_MATERIAL=18 / UNCLEAR=0` |
| Testing Convention (current Approved) | `docs/engineering/testing.md` | `de17690733b2b3c75345e867a8c442a39911e5da` | Yes — `version: "0.17"`, `status: Approved` |
| Chapter 13 (Quality Gates) | `docs/constitution/13-quality-gates.md` | `acf4ab75eda1ea0613250ce3159669ea727e28ec` | Yes — `version: "1.8"`, `status: Locked` |
| ADR-044 | `docs/adr/ADR-044.md` | `82f07b523ff30b08d17b39a9beaf2d6d1c369179` | Yes — `version: "0.5"`, `status: Approved` |
| ADR-045 | `docs/adr/ADR-045.md` | `ac13ece16ff644d0d88ddf982d83bfb0e8d5ad16` | Yes — `version: "0.3"`, `status: Approved` |
| Evidence-005 (formal) | `docs/governance/mutation-baseline-evidence/feature-engine-mutation-step9-formal-evidence-005.json` | `f7a6ab715155ad166808e0e9d9a7474196d9b69d` | Yes |

**New candidate companion artifact created by this transaction (inert
pinned-identity data, not itself a governing decision):**
`docs/governance/mutation-baseline-evidence/feature-engine-condition1-current-material-gap-set-003.json`
— exact 18 IDs (the active 24-ID set-002 minus the 6 DTR-reclassified
identities), `count = 18`, `duplicates = 0`, sorted-set sha256
`e4d21a0f1765f860d48d8a607c5d4e25b5b43c88f76db631cdd8528d83f73872`
(independently recomputed and confirmed to match the DTR's own recorded
value).

## 1. Why a third correction candidate is required

The currently-effective threshold (proposal-002, `APPROVED — EFFECTIVE`)
was calibrated as:

```text
M = 24  (the full active Condition-1B population at that boundary)
base confirmed numerator = 2214  (killed 2209 + confirmed_timeout 5)
population = 2629

candidate numerator = 2214 + 24 = 2238
threshold = 2238 / 2629 × 100 = 85.127424876379%
```

Wave 6 subsequently implemented targeted tests against the 13 of those 24
identities not yet remediated, killing 7 (`FE-EVID03-COND1-WAVE6-001`) and
honestly discovering that the remaining 6 are `PROVABLY_EQUIVALENT` or
`STRUCTURALLY_UNREACHABLE`, not genuine behavioral gaps — verified by
direct source-level reachability proof, not assumption. A distinct-
principal ChatGPT Review A then issued a governed Delegated Technical
Resolution (`FE-EVID03-COND1-WAVE6-CLASSIFICATION-DTR-001`, `CLEAN —
0/0/0`) confirming all 6 reclassifications.

The active 24-identity population and its `85.127424876379%` figure are
therefore now proven, by the active proposal's own calibration principle,
to be **conservative/over-strict** relative to what they actually measure —
6 of the 24 identities the active threshold was calibrated against do not
represent genuine behavioral gaps. This candidate recalibrates the numeric
figure to the exact same calibration principle, applied to the Review-A-
validated 18-identity population.

This is a **correction of measurement precision**, not a weakening of the
underlying policy — the same closure obligation the active proposal
encodes, now pointed at the identities that actually represent it.

## 2. The calibration principle is preserved exactly

Unchanged from the active proposal:

```text
The numeric threshold represents the raw mutation score reached when all
CURRENT genuine material behavioral gaps at the calibration boundary are
closed, without requiring low-materiality / non-behavioral mutant kills.

Every exact current material identity used to derive the numeric
threshold must itself be individually resolved (the companion gate).
```

This candidate does **not** introduce a percentage-only gate, does
**not** allow unrelated kills to substitute for material-gap closure, and
does **not** change the raw formula, the denominator semantics, or the
resolution mechanism.

## 3. Candidate 18-ID companion artifact

`docs/governance/mutation-baseline-evidence/feature-engine-condition1-current-material-gap-set-003.json`
(status `CANDIDATE — NOT EFFECTIVE`) pins the exact 18 identities: the
active 24-ID set-002's own membership minus the 6 identities the Wave-6
classification DTR reclassified non-material. Fresh-verified: `count =
18`, `duplicates = 0`, sorted-set `sha256 =
e4d21a0f1765f860d48d8a607c5d4e25b5b43c88f76db631cdd8528d83f73872` (matches
the DTR's own recorded value exactly). The 6 identities present in the
active set-002 but absent here are **not transferred** — see §14 below for
their preserved disposition.

## 4. Current engineering status of the 18 candidate identities

Carried forward from the Wave-6 classification DTR accounting:

```text
18 / 18: targeted engineering kill implementation evidence exists for
         EVERY identity (11 from Wave-5, 7 from Wave-6, real test
         execution scoped to each exact mutant ID).
         FORMAL CREDIT NOT YET CLAIMED for any of the 18 by this or any
         prior transaction — a future, separately-governed formal
         mutation-measurement transaction determines actual Condition-1B
         credit.
```

This is materially stronger engineering-evidence stability than either
prior calibration population: every identity retained in this candidate
has now been individually inspected, backed by a real behavioral
obligation, and empirically killed by a targeted behavioral test — not
merely pattern/cluster-classified. This candidate does **not** claim,
grant, or imply formal Condition-1B credit for any of the 18 identities.
Engineering-evidence existence and formal gate credit remain explicitly
distinct.

## 5. Corrected Model A — numeric re-baseline, same raw metric, same calibration boundary

**Same calibration boundary as the active proposal — not any post-Wave-6
observed aggregate score:**

```text
Evidence-005 population:            2629
base confirmed numerator:           2214  (killed 2209 + confirmed_timeout 5)
Review-A-validated current material: 18  (per Wave-6 classification DTR
                                          FE-EVID03-COND1-WAVE6-
                                          CLASSIFICATION-DTR-001)

candidate numerator: 2214 + 18 = 2232

candidate threshold = 2232 / 2629 × 100
= 84.899201217192848992012171928489920121719284899201...%  (repeating
  decimal, independently recomputed to 50-digit precision)
display, matching the prior proposals' 12-decimal-place convention:
84.899201217193%
```

Exact-count basis: `required numerator = 2232` at `total = 2629`. This is
the normative derivation for this candidate — not a formula to be
mechanically re-applied should the population change again.

**Not derived from a post-Wave-6 observed aggregate score, and not chosen
merely to pass:** see §6 below.

## 6. Proposed Condition-1 gate

```text
Condition 1A: raw mutation-effectiveness >= 84.899201217193%
              exact calibration basis: 2232 / 2629

AND

Condition 1B: all 18 exact IDs in
              feature-engine-condition1-current-material-gap-set-003.json
              individually resolved via exactly one of:
                (a) Killed / confirmed_timeout in a fresh, formal
                    mutation measurement; OR
                (b) Individually reclassified — a SEPARATE, governed
                    decision, exact mutant identity + specific semantic
                    justification + a separate reviewed/recorded
                    decision (never a blanket, unreviewed claim).
              No blanket classification. No score-offset substitution.
              Killing unrelated (e.g. message-text) mutants must NEVER
              satisfy Condition 1B.
```

Both conditions are required — no substitution, no blanket reclassification,
no score-offset mechanism. This is a direct, structurally identical reuse
of the active proposal's own Condition 1A/1B mechanism, applied to the
Review-A-validated 18-identity population instead of the 24-identity one —
not an invented new mechanism (see §20's fresh ADR Scope re-run).

**Formula unchanged:** `mutation_score = (killed + confirmed_timeout) /
(total − skipped) × 100` (Testing Convention v0.17 item 7). `skipped = 0`
in Evidence-005, unchanged by this candidate.

## 7. Preserve independent Condition 2

Condition 2 remains entirely separate and untouched by this candidate:

```text
Condition 2: 169/170.
Remaining unresolved: contracts.x__seal_verified_authority__mutmut_33.
Current classification: TOOL_IDENTITY_DRIFT — NO EXISTING GOVERNED
  RESOLUTION MECHANISM.
```

Not resolved, not touched, not merged into the 18-ID current-material gate
by this candidate.

## 8. Preserve Condition 3

Condition 3 remains `SATISFIED — REVIEW A VALIDATED`, unchanged, not
reopened by this candidate.

## 9. Current active state — unchanged by this authoring transaction

This candidate is **not** activated by this transaction. The controlling
gate remains, unchanged:

```text
Condition 1A: 85.127424876379%
Condition 1B: 24-ID feature-engine-condition1-current-material-gap-set-002.json
```

Current formal state remains, unchanged:

```text
Condition 1:                FAIL — criteria
Condition 2:                169/170
Condition 3:                SATISFIED — REVIEW A VALIDATED
P3-FEATURE-QG-EVID-03:      OPEN
Feature Engine:              NOT APPROVED
LIVE:                        NOT_AUTHORIZED
```

Within the active 24-ID gate, the Wave-6 classification DTR has already
resolved 6/24 identities via delegated technical reclassification; the
remaining 18/24 carry engineering-kill evidence with formal credit NOT
claimed. This candidate does not change that active accounting.

## 10. Why 84.899201217193% is not a pass-fitting number

This candidate figure is derived exclusively from `2214 + 18` — the same
already-confirmed base numerator the active proposal itself uses, plus
the exact, distinct-principal-reviewed count of genuinely material
identities established by the Wave-6 classification DTR — **never** from
any post-Wave-6 observed aggregate formal score. No full post-Wave-6
formal 2629-mutant measurement has been performed by this or any prior
transaction; the actual formal outcome remains genuinely unknown until
that future measurement transaction runs. This candidate therefore cannot
have been selected merely to clear an observed formal result — no such
result exists yet to clear.

If a future formal measurement is performed, this candidate's Condition
1A/1B may `PASS` or `FAIL` on its own merits, entirely independent of how
this candidate figure was derived.

## 11. Supersession / future SSOT transition (defined, not executed)

**Before any future activation (current state, unchanged by this
transaction):**

```text
feature-engine-mutation-threshold-recalibration-proposal-002.md
  = APPROVED -- EFFECTIVE
  = sole current Feature Engine Condition-1 threshold authority

feature-engine-condition1-current-material-gap-set-002.json
  = current Condition-1B current-material identity authority
```

**If, and only if, a future, separate activation transaction approves this
candidate (proposal-003):**

```text
feature-engine-mutation-threshold-recalibration-proposal-003.md
  = APPROVED -- EFFECTIVE
  = sole current Feature Engine Condition-1 threshold authority

feature-engine-condition1-current-material-gap-set-003.json
  = sole current Condition-1B current-material identity authority

feature-engine-mutation-threshold-recalibration-proposal-002.md
  = historical / superseded threshold authority
  = file remains byte-unchanged

feature-engine-condition1-current-material-gap-set-002.json
  = historical calibration evidence
  = file remains byte-unchanged
```

That future activation transaction's own `docs/MANIFEST.md` update would
atomically switch the canonical current-threshold pointer, exactly
mirroring how proposal-002's own activation superseded proposal-001.
**This transaction does not perform that switch.** Both proposal-002 and
set-002 remain, right now, the sole current, fully controlling authority.

## 12. Rollback / reversal semantics

Unchanged in kind from the prior proposals: if a future activation of this
candidate is later found defective, reversal follows the same symmetric
mechanism — a fresh, governed re-proposal transaction citing the specific
defect, with its own fresh ADR Scope Rule and Risk Classification, never a
silent in-place edit of an already-activated threshold artifact.

## 13. Extraction-method root cause and stronger classification discipline

This candidate's own population is the direct product of discovering and
correcting a methodology defect during Wave-6 implementation: this
session's custom, offline zero-test CST diff-extraction script (used
throughout the root-cause audit and prior transactions) can silently drift
out of index-alignment with mutmut's own real internal mutation ordering
for functions with unusually dense/nested mutation candidate counts —
concretely observed in `swing_distance.py`'s `_select_eligible_swing`
(containing a lambda) and `_prepare_reevaluate_all_windows` (containing
multiple adjacent `continue`-shaped branches). Two of the six Wave-6
classification-contradiction identities were affected by this exact bug;
the other four were correctly described but had not previously received
sufficiently rigorous reachability analysis.

**Recommended (not activated) procedural tightening, offered as
rationale, not as a new governance rule:** for any identity whose exact
mutation semantics matter to a governed materiality decision, mutmut's own
real generated mutant body (from its materialized `mutants/<path>`
workspace) should be treated as the canonical mutation-body evidence,
independently re-verified against any custom extraction tooling's output,
rather than trusting the custom tooling's output alone — exactly the
discipline this transaction itself applied to reach the 18-identity
population above. This is proposal/rationale content only; it does not
create a new global governance rule in this transaction.

## 14. Treatment of the reclassified identities from both DTRs

Both DTR resolutions are preserved as valid, governed audit history and
are **not** erased, invalidated, or reopened by this candidate:

- `FE-EVID03-COND1-MATERIAL-SET-DTR-001` (18 identities reclassified
  non-material from the original 42-identity population, at its own
  boundary);
- `FE-EVID03-COND1-WAVE6-CLASSIFICATION-DTR-001` (6 further identities
  reclassified non-material from the active 24-identity population, at
  this boundary).

The 6 identities present in the active 24-ID set-002 but absent from this
candidate's 18-ID set-003 are absent for exactly one reason: they are no
longer members of the final, Review-A-validated current-material
population, per the Wave-6 classification DTR's governed reclassification.
Across the original 42-identity history: `18` (prior DTR) `+ 6` (this DTR)
`= 24` non-material, `18` genuine material, `42` total — this candidate
does not restate, re-derive, or re-litigate either prior disposition.

## 15. Non-goals

This transaction does **not**:

- change the currently-effective `85.127424876379%` threshold or its
  Condition 1A/1B gate (proposal-002 remains fully controlling);
- mutate `feature-engine-mutation-threshold-recalibration-proposal-002.md`
  (remains byte-unchanged at `ea0b7a79b733622388597c59346c4615bb2726db`)
  or `feature-engine-condition1-current-material-gap-set-002.json`
  (remains byte-unchanged at `2e6030c5581df51323937de0bd5f646f3e98b5d9`);
- mutate the Wave-6 evidence artifact, the Wave-6 classification DTR, the
  prior root-cause audit, or the prior material-set DTR (all remain
  byte-unchanged);
- perform a fresh 2629-mutant (or any) formal mutation measurement;
- resolve any of the 18 Condition-1B candidate identities, or any of the
  24 DTR-resolved (18 + 6) ones;
- implement any further test;
- resolve `contracts.x__seal_verified_authority__mutmut_33`
  (`TOOL_IDENTITY_DRIFT`);
- touch Condition 2 (`169/170`) or Condition 3 (`SATISFIED — REVIEW A
  VALIDATED`) in any way;
- request, perform, or fabricate Review A, an Independent Review B, or a
  Product Owner decision;
- author or modify any ADR;
- edit Testing Convention, Chapter 13, ADR-044, or ADR-045;
- activate this candidate.

## 16. Review and decision path

**Fresh-run, not inherited from proposal-002's own prior ADR Scope Rule
outcome** — re-examined specifically against this candidate's actual
content (the 18-identity companion artifact and the recalibrated Model A
figure).

| §4b trigger | Applies to this candidate? | Reasoning |
|---|---|---|
| Platform Invariant change | No | No I-1–I-13 invariant touched. |
| Event Schema change | No | No event/fact schema, contract, or field touched. |
| Module Taxonomy/dependency-graph change | No | No `module-registry.yaml`/dependency-edge edit. |
| Governance/Approval-process change | No | Condition 1B's resolution semantics are verbatim the same, already-established `(a) killed/confirmed_timeout OR (b) individually reclassified` mechanism proposal-001/-002 both already use — applied to a smaller, more precisely audited identity set. The new pinned 18-ID artifact is inert data, not a new review role, lifecycle stage, or approval-gate structure. |
| Decision affecting >1 module | No | Strictly Feature-Engine-only, Tier-1 scope — unchanged from proposal-002. |
| Hard-to-reverse decision | No | §12's symmetric re-proposal mechanism preserves full reversibility, identical in kind to proposal-002's own. |
| Locked-ADR modification/supersession | No | No ADR touched. |
| **Alternative: significant but reversible single-module internal change** | **Yes** | A genuinely significant (will eventually gate a real PASS/FAIL dimension), single-module, contract-preserving, already-delegated-authority (Chapter 13 §13.14 defers exact threshold detail to Testing-Convention-owned territory), fully-reversible candidate — same textual fit as proposal-002's own §16 finding. |

```text
ADR_SCOPE_DISPOSITION: ADR_OPTIONAL
```

**Risk Classification:** a substantive policy/quality-gate recalibration,
not mere evidence/bookkeeping recording (ruling out `R0`); no Platform
Invariant, Event Schema, cross-module, or Locked-ADR effect, fully
reversible via §12 (ruling out `R2`):

```text
Risk: R1 (candidate disposition — pending independent confirmation by
  this candidate's own Review A, exactly as proposal-002's R1 was
  independently confirmed rather than self-finalized by its author).
```

**Current review path under ADR-045/Chapter 11 v2.4, fresh-read, not
restated from memory:**

```text
Review A mandatory.
R1 default: NO independent cross-check, unless Review A or the Product
  Owner escalates this specific case to R2.
```

**Numeric threshold selection remains explicitly Product-Owner-reserved**
(ADR-045 `D10(a)`). Therefore:

```text
DTR is NOT ELIGIBLE for proposal-003's own activation decision.
```

**Proposed path (not performed by this transaction):** after this
candidate receives a `CLEAN` (or remediated-to-`CLEAN`) Review A, route
exactly one narrow Product Owner decision naming the exact candidate
figure (`84.899201217193%`), the exact companion artifact (set-003, 18
IDs), the review disposition, and the boundary being approved. **This
decision is not requested by this transaction.**

## 17. Formal measurement remains blocked

No further test implementation is proposed against the 18-ID candidate
population by this transaction — all 18 already carry targeted engineering
kill evidence (§4). The primary next governed step after this transaction
is Review A of this candidate (proposal-003/set-003), followed by a
Product Owner threshold decision. A full formal Condition-1 measurement
remains deferred until that decision resolves which population/threshold
it should be measured against.

## 18. Candidate lineage — no history rewritten

```text
Original threshold:            87.001959503592%
                                historical / superseded by proposal-001.

Recalibration proposal-001:    85.812095853937% + 42 IDs (set-001)
                                historical / superseded by proposal-002.

Root-cause audit + DTR:        24 genuine / 18 non-material / 0 unclear
                                (FE-EVID03-COND1-MATERIAL-SET-DTR-001,
                                CLEAN -- 0/0/1).

Recalibration proposal-002:    85.127424876379% + 24 IDs (set-002)
                                CURRENT APPROVED -- EFFECTIVE.

Wave-6 test remediation:       7/13 killed, 6/13 classification-
                                contradiction finding
                                (FE-EVID03-COND1-WAVE6-001).

Wave-6 classification DTR:     6 further identities reclassified non-
                                material (FE-EVID03-COND1-WAVE6-
                                CLASSIFICATION-DTR-001, CLEAN -- 0/0/0).

Recalibration proposal-003:    84.899201217193% + 18 IDs (set-003)
                                THIS DOCUMENT -- CANDIDATE -- NOT
                                EFFECTIVE / AWAITING REVIEW A.
```

No prior document is rewritten, reinterpreted, or retroactively edited by
this candidate.
