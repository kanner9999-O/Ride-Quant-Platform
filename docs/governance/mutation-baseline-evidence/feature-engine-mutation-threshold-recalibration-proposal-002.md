# Feature Engine Condition-1 Threshold — Recalibration Proposal 002

**STATUS: APPROVED — EFFECTIVE**

**Product Owner APPROVAL — atomic activation (2026-09-24T10:08+07:00),
vai trò: `Feature Engine Condition-1 Threshold Recalibration Proposal 002
Product Owner Decision Recorder`.** Product Owner decision (verbatim):

> "APPROVE Feature Engine Condition-1 Threshold Recalibration Proposal 002
> at reviewed boundary f99f75973049e71b7e3f1876ba0683a7d8434d48. Replace
> the current Condition-1 gate with: Condition 1A: raw
> mutation-effectiveness >= 85.127424876379% (2238/2629 at the reviewed
> calibration boundary); AND Condition 1B: all 24 exact identities in
> feature-engine-condition1-current-material-gap-set-002.json must be
> individually resolved under the existing governed per-identity
> mechanism. Preserve Condition 2 and Condition 3 as independent
> requirements. Accept Review A CLEAN — 0 Blocker / 0 Major / 0 Minor,
> Risk R1, ADR_OPTIONAL. No independent cross-check required."

Decision date: `2026-09-24T10:08+07:00`.

**Reviewed semantic boundary:** `f99f75973049e71b7e3f1876ba0683a7d8434d48`
(the commit at which this candidate document reached its reviewed
content — the actual, immutable proposal content this approval covers).
**Reviewed subject blob:** `4ca7354600ccd81331b3fb8a46f25327bdf53371`
(this file, at that boundary — the byte-identical `CANDIDATE — NOT
EFFECTIVE / AWAITING REVIEW A` content Review A evaluated). **Reviewed
24-ID artifact blob:** `d4558f37c8c9084bf8f404309c342126733eeebc` (the
exact set Review A evaluated). This activation adds an approval banner to
this document and an `activation` lifecycle block to the 24-ID artifact —
both changes are lifecycle-record metadata only, never a change to the
reviewed substantive calibration semantics (§1–§18 below remain
byte-identical to what Review A evaluated). The **resulting,
activated/lifecycle-record 24-ID artifact blob** is
`2e6030c5581df51323937de0bd5f646f3e98b5d9`. Reviewed and resulting blobs
are recorded explicitly and distinctly, never conflated: the reviewed
blob identifies exactly what Review A evaluated; the resulting blob
identifies the byte-identity of the artifact as it stands after this
activation's lifecycle-metadata addition.

**Review evidence at this approval (already completed, recorded — not
recorder self-closure):**

```text
Review A -- ChatGPT / AI Technical Architect, reviewed boundary
f99f75973049e71b7e3f1876ba0683a7d8434d48, reviewed proposal blob
4ca7354600ccd81331b3fb8a46f25327bdf53371, reviewed 24-ID artifact blob
d4558f37c8c9084bf8f404309c342126733eeebc:
  CLEAN -- 0 Blocker / 0 Major / 0 Minor.
Risk: R1. ADR Scope: ADR_OPTIONAL.
R1 default: NO CROSS-CHECK. Product Owner explicitly selected: no
  independent cross-check required. No Independent Review B performed or
  fabricated.
```

**State after this approval:**

```text
Feature Engine Condition-1 Threshold Recalibration Proposal 002: APPROVED
  -- Product Owner, EFFECTIVE. This is now the SOLE current Feature
  Engine Condition-1 threshold authority.
Condition 1A: raw mutation-effectiveness >= 85.127424876379% (exact-count
  basis 2238/2629 at the reviewed calibration boundary) -- necessary but
  not sufficient.
Condition 1B: all 24 exact identities in the activated
  feature-engine-condition1-current-material-gap-set-002.json (blob
  2e6030c5581df51323937de0bd5f646f3e98b5d9) individually resolved --
  necessary. Killing unrelated (message-text) mutants never substitutes.
  No blanket reclassification. No score-offset mechanism.
Condition 2 and Condition 3 preserved as independent requirements,
  UNCHANGED and NOT merged with Condition 1B.
Proposal-001 (feature-engine-mutation-threshold-recalibration-
  proposal-001.md, 85.812095853937%, blob
  12040044578d57d15e699a327a5a8ae39c1e9ea3) and its companion set-001
  (feature-engine-condition1-current-material-gap-set-001.json, 42 IDs,
  blob 49c30b439eb84db95c55dc4a86de22e2b491dbb5): now historical /
  superseded threshold authority. Both files remain byte-unchanged --
  their own internal historical APPROVED -- EFFECTIVE banners describe
  their own historical lifecycle and are NOT retroactively edited; current
  authority must be read from THIS document and from MANIFEST's canonical
  current-threshold pointer, never inferred from either superseded
  document's own banner.
Current Condition 1 status: FAIL -- criteria (Condition 1A: FAIL --
  criteria, current raw score 84.21453023963484%-84.55686572841384% <
  85.127424876379%; Condition 1B: FAIL -- criteria / formal closure
  incomplete, the 24 pinned identities are not all individually resolved
  -- 11 carry Wave-5 targeted-kill implementation evidence with formal
  credit NOT yet claimed, 13 remain unremediated). This activation changes
  the governing threshold only -- no fresh mutation measurement was
  performed by this transaction.
Condition 2: 169/170, unchanged, independent.
Condition 3: SATISFIED -- REVIEW A VALIDATED, unchanged.
P3-FEATURE-QG-EVID-03: OPEN. Feature Engine: NOT APPROVED. Phase-3 module
  approval: NOT GRANTED. LIVE: NOT_AUTHORIZED.
```

**Approval này KHÔNG:** perform a fresh 2629-mutant (or any) formal
mutation measurement; resolve any of the 24 Condition-1B identities;
resolve `contracts.x__seal_verified_authority__mutmut_33`
(`TOOL_IDENTITY_DRIFT`); implement any Wave-6 test; mutate
`feature-engine-mutation-threshold-recalibration-proposal-001.md`
(remains byte-unchanged at `12040044578d57d15e699a327a5a8ae39c1e9ea3`) or
`feature-engine-condition1-current-material-gap-set-001.json` (remains
byte-unchanged at `49c30b439eb84db95c55dc4a86de22e2b491dbb5`); mutate the
root-cause audit or the material-set DTR artifact (both remain
byte-unchanged); touch Evidence-005, its correction, Testing Convention,
Chapter 13, ADR-044, or ADR-045; touch any source/test/tooling; fabricate
Independent Review B evidence; use Delegated Technical Resolution for the
threshold-selection decision (ADR-045 `D10(a)` reserves it to Product
Owner); mark Condition 1 PASS; approve Feature Engine; or authorize LIVE.

**Below this banner (§0–§18) is this candidate's own authored content,
byte-identical to what Review A evaluated (reviewed blob
`4ca7354600ccd81331b3fb8a46f25327bdf53371`) — preserved unedited as the
correct, immutable record of what was proposed and reviewed. Statements
below describing this document as "CANDIDATE," "not requesting a Product
Owner decision," "not activated," or similar are accurate as of this
document's own authoring/review boundary and are superseded, effective
this activation, by the banner above — never retroactively edited.**

---

## 0. Authority resolved directly (fresh-read, not restated from memory)

| Artifact | Path | Blob | Fresh-verified |
|---|---|---|---|
| Currently-effective threshold (sole current authority, unchanged by this candidate) | `docs/governance/mutation-baseline-evidence/feature-engine-mutation-threshold-recalibration-proposal-001.md` | `12040044578d57d15e699a327a5a8ae39c1e9ea3` | Yes |
| Currently-effective Condition-1B companion artifact (unchanged by this candidate) | `docs/governance/mutation-baseline-evidence/feature-engine-condition1-current-material-gap-set-001.json` | `49c30b439eb84db95c55dc4a86de22e2b491dbb5` | Yes — 42 identities, sorted-set sha256 `932698b4b312c1a8f70c261426555a5c6f3566579ed0a27102d4a0f0214adedc` |
| Root-cause material-gap audit | `docs/governance/mutation-baseline-evidence/feature-engine-condition1-material-gap-root-cause-audit-001.json` | `aaece3895c3c66e05aba3a421f7b045db94e8bbb` | Yes |
| Delegated Technical Resolution (`FE-EVID03-COND1-MATERIAL-SET-DTR-001`) | `docs/governance/mutation-baseline-evidence/feature-engine-condition1-material-gap-dtr-001.json` | `fe43ffe2ac460fc42551617d9bb7781e52a07f26` | Yes — final partition `GENUINE_TEST_GAP=24 / NON_MATERIAL=18 / UNCLEAR=0`, remaining-material sha256 `6c8181f7665a63494632ef89514ea7efdf9948c544c9a9a8094e87c17c3d2543` |
| Wave-5 test remediation evidence | `docs/governance/mutation-baseline-evidence/feature-engine-condition1-wave5-test-remediation-001.json` | `6fd2f3a9aebe7df8035c0b64dac46de3fa707a26` | Yes |
| Testing Convention (current Approved) | `docs/engineering/testing.md` | `de17690733b2b3c75345e867a8c442a39911e5da` | Yes — `version: "0.17"`, `status: Approved` |
| Chapter 13 (Quality Gates) | `docs/constitution/13-quality-gates.md` | `acf4ab75eda1ea0613250ce3159669ea727e28ec` | Yes — `version: "1.8"`, `status: Locked` |
| ADR-044 | `docs/adr/ADR-044.md` | `82f07b523ff30b08d17b39a9beaf2d6d1c369179` | Yes — `version: "0.5"`, `status: Approved` |
| ADR-045 | `docs/adr/ADR-045.md` | `ac13ece16ff644d0d88ddf982d83bfb0e8d5ad16` | Yes — `version: "0.3"`, `status: Approved` |
| Evidence-005 (formal) | `docs/governance/mutation-baseline-evidence/feature-engine-mutation-step9-formal-evidence-005.json` | `f7a6ab715155ad166808e0e9d9a7474196d9b69d` | Yes |

**New candidate companion artifact created by this transaction (inert
pinned-identity data, not itself a governing decision):**
`docs/governance/mutation-baseline-evidence/feature-engine-condition1-current-material-gap-set-002.json`
— exact 24 IDs sourced from the DTR's `remaining_material_24_sorted`,
`count = 24`, `duplicates = 0`, sorted-set sha256
`6c8181f7665a63494632ef89514ea7efdf9948c544c9a9a8094e87c17c3d2543`
(independently recomputed and confirmed to match the DTR's own recorded
value).

## 1. Why a second correction candidate is required

The currently-effective threshold (proposal-001, `APPROVED — EFFECTIVE`)
was calibrated as:

```text
M = 42  (settled GENUINE_TEST_GAP population at that boundary)
base confirmed numerator = 2214  (killed 2209 + confirmed_timeout 5)
population = 2629

candidate numerator = 2214 + 42 = 2256
threshold = 2256 / 2629 × 100 = 85.812095853937%
```

Subsequent to that activation, a consolidated, first-principles root-
cause audit (`feature-engine-condition1-material-gap-root-cause-audit-001.json`)
freshly re-extracted and independently re-classified all 42 pinned
identities from first principles — never inheriting prior category
labels — and a distinct-principal ChatGPT Review A then issued a governed
Delegated Technical Resolution (`FE-EVID03-COND1-MATERIAL-SET-DTR-001`,
`CLEAN — 0/0/1`) adjudicating the audit's findings:

```text
GENUINE MATERIAL = 24
NON-MATERIAL     = 18
UNCLEAR           =  0
TOTAL            = 42
```

The active 42-identity population and its derived `85.812095853937%`
figure are therefore now **proven, by the active proposal's own
calibration principle, to be conservative/over-strict** relative to what
they actually measure: 18 of the 42 identities the active threshold was
calibrated against do not represent genuine behavioral gaps (9
message-text-only, 6 structurally unreachable, 1 implementation-detail-
only, 2 confirmed non-material transient in-flight state). This candidate
recalibrates the numeric figure to the exact same calibration principle,
applied to the Review-A-validated 24-identity population.

This is a **correction of measurement precision**, not a weakening of
the underlying policy — the same closure obligation the active proposal
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
**not** allow unrelated kills to substitute for material-gap closure,
and does **not** change the raw formula, the denominator semantics, or
the resolution mechanism.

## 3. Candidate 24-ID companion artifact

`docs/governance/mutation-baseline-evidence/feature-engine-condition1-current-material-gap-set-002.json`
(status `CANDIDATE — NOT EFFECTIVE`) pins the exact 24 identities sourced
directly from the DTR's own `remaining_material_24_sorted` field —
verified identical, not re-derived independently, since the DTR is
itself the governed, distinct-principal-reviewed source of truth for
this population. Fresh-verified: `count = 24`, `duplicates = 0`,
sorted-set `sha256 =
6c8181f7665a63494632ef89514ea7efdf9948c544c9a9a8094e87c17c3d2543`
(matches the DTR's own recorded value exactly). The 18 identities present
in the active 42-ID set-001 but absent here are **not transferred** —
see §14 below for their preserved disposition.

## 4. Current engineering status of the 24 candidate identities

Carried forward from the DTR accounting, unchanged:

```text
11 / 24: Wave-5 targeted-kill implementation evidence exists (real test
         execution scoped to exactly these mutant IDs — see
         feature-engine-condition1-wave5-test-remediation-001.json).
         FORMAL CREDIT NOT YET CLAIMED for any of the 11 by this or any
         prior transaction — a future, separately-governed formal
         mutation-measurement transaction determines actual Condition-1B
         credit.

13 / 24: not yet remediated or tested. Confirmed GENUINE_TEST_GAP by the
         root-cause audit via fresh exact-diff extraction and
         reachability/control-flow analysis. Eligible for a future
         Wave-6 implementation Work Package.
```

This candidate does **not** claim, grant, or imply formal Condition-1B
credit for any of the 24 identities. Engineering-evidence existence and
formal gate credit remain explicitly distinct, exactly as the active
proposal and the Wave-5 evidence artifact already establish.

## 5. Corrected Model A — numeric re-baseline, same raw metric, same calibration boundary

**Same calibration boundary as the active proposal — not the post-Wave-5
killed count:**

```text
Evidence-005 population:            2629
base confirmed numerator:           2214  (killed 2209 + confirmed_timeout 5)
Review-A-validated current material: 24  (GENUINE_TEST_GAP, per DTR
                                          FE-EVID03-COND1-MATERIAL-SET-DTR-001)

candidate numerator: 2214 + 24 = 2238

candidate threshold = 2238 / 2629 × 100
= 85.12742487637885...%  (repeating decimal, independently recomputed
  to 50-digit precision: 85.127424876378851274248763788512742487637885...%)
display, matching the active proposal's 12-decimal-place convention:
85.127424876379%
```

Exact-count basis: `required numerator = 2238` at `total = 2629`. This is
the normative derivation for this candidate — not a formula to be
mechanically re-applied should the population change again; a future
population change would require its own fresh recalibration under §9's
carried-forward trigger, exactly as the active proposal itself states for
its own figure.

**Not derived from the post-Wave-5 killed count, and not chosen merely to
pass:** see §6 below.

## 6. Proposed Condition-1 gate

```text
Condition 1A: raw mutation-effectiveness >= 85.127424876379%
              exact reviewed calibration basis: 2238 / 2629

AND

Condition 1B: all 24 exact IDs in
              feature-engine-condition1-current-material-gap-set-002.json
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

Both conditions are required — no substitution, no blanket
reclassification, no score-offset mechanism. This is a direct,
structurally identical reuse of the active proposal's own Condition
1A/1B mechanism (itself a reuse of the original threshold's §4.1
per-identity pattern), applied to the Review-A-validated 24-identity
population instead of the 42-identity one — not an invented new
mechanism (see §16's fresh ADR Scope re-run).

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

Not resolved, not touched, not merged into the 24-ID current-material
gate by this candidate.

## 8. Preserve Condition 3

Condition 3 remains `SATISFIED — REVIEW A VALIDATED`, unchanged, not
reopened by this candidate.

## 9. Current active state — unchanged by this authoring transaction

This candidate is **not** activated by this transaction. The controlling
gate remains, unchanged:

```text
Condition 1A: 85.812095853937%
Condition 1B: 42-ID feature-engine-condition1-current-material-gap-set-001.json
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

## 10. Why 85.127424876379% is not a pass-fitting number

This candidate figure is derived exclusively from `2214 + 24` — the same
already-confirmed base numerator the active proposal itself uses, plus
the exact, distinct-principal-reviewed count of genuinely material
identities established by the DTR — **never** from the current
post-remediation raw score.

The current Evidence-005 raw score remains approximately
`84.21453023963484%–84.55686572841384%`, which is **below**
`85.127424876379%`. Therefore, even if this candidate were later
activated exactly as proposed:

```text
Condition 1A would still be FAIL on current formal evidence
  (84.21%-84.56% < 85.127424876379%).
```

Condition 1B would also remain incomplete: 13 of the 24 identities are
still unremediated, and the 11 with Wave-5 targeted-kill implementation
evidence carry no formal gate credit in this or any prior transaction.
This candidate cannot be read as selected to obtain a green gate — under
either the active or the candidate figure, Feature Engine continues to
`FAIL` Condition 1 on today's formal evidence.

## 11. Supersession / future SSOT transition (defined, not executed)

**Before any future activation (current state, unchanged by this
transaction):**

```text
feature-engine-mutation-threshold-recalibration-proposal-001.md
  = APPROVED -- EFFECTIVE
  = sole current Feature Engine Condition-1 threshold authority

feature-engine-condition1-current-material-gap-set-001.json
  = current Condition-1B current-material identity authority
```

**If, and only if, a future, separate activation transaction approves
this candidate (proposal-002):**

```text
feature-engine-mutation-threshold-recalibration-proposal-002.md
  = APPROVED -- EFFECTIVE
  = sole current Feature Engine Condition-1 threshold authority

feature-engine-condition1-current-material-gap-set-002.json
  = sole current Condition-1B current-material identity authority

feature-engine-mutation-threshold-recalibration-proposal-001.md
  = historical / superseded threshold authority
  = file remains byte-unchanged

feature-engine-condition1-current-material-gap-set-001.json
  = historical calibration evidence
  = file remains byte-unchanged
```

That future activation transaction's own `docs/MANIFEST.md` update would
atomically switch the canonical current-threshold pointer, exactly
mirroring how proposal-001's own activation superseded the original
`87.001959503592%` threshold. **This transaction does not perform that
switch.** Both proposal-001 and set-001 remain, right now, the sole
current, fully controlling authority.

## 12. Rollback / reversal semantics

Unchanged in kind from the active proposal: if a future activation of
this candidate is later found defective, reversal follows the same
symmetric mechanism — a fresh, governed re-proposal transaction citing
the specific defect, with its own fresh ADR Scope Rule and Risk
Classification, never a silent in-place edit of an already-activated
threshold artifact. Both proposal-001 and this candidate, once (if ever)
superseded, remain the permanent historical record of their own
calibration boundary.

## 13. Treatment of the 18 DTR-resolved non-material identities

The DTR resolution (`FE-EVID03-COND1-MATERIAL-SET-DTR-001`) is preserved
as valid, governed audit history and is **not** erased, invalidated, or
reopened by this candidate. The 18 identities present in the active
42-ID set-001 but absent from the candidate 24-ID set-002 are absent
for exactly one reason: they are no longer members of the final,
Review-A-validated current-material population, per the DTR's governed
reclassification. Their disposition (9 `LOW_MATERIALITY_MESSAGE_TEXT`, 6
`STRUCTURALLY_UNREACHABLE`, 1 `LOW_MATERIALITY_IMPLEMENTATION_DETAIL`, 2
`NON_MATERIAL_TRANSIENT_IN_FLIGHT_STATE`) remains recorded, in full,
in the DTR artifact and in `docs/MANIFEST.md`'s DTR section — this
candidate does not restate, re-derive, or re-litigate it.

## 14. Recalibration trigger — this incident as the concrete worked example

The active proposal's own §9 already proposes (not activates) a fourth
recalibration-trigger category: **materiality / mutation-population
composition drift**. This transaction's own history is offered as the
concrete worked example that trigger category was written to describe —
not as a new rule:

> A cluster-level survivor classification initially produced 42
> candidate current-material identities (the post-E005 assessment plus
> two Review-A-corrected reclassifications). A subsequent, independent,
> first-principles exact-diff + reachability/control-flow + documented-
> contract audit, adjudicated by a distinct-principal Review A via a
> governed Delegated Technical Resolution, proved only 24 of those 42
> genuinely material. The other 18 survived a pattern-level/cluster-level
> classification pass but did not survive a per-identity exact-diff and
> reachability trace.

**Recommended (not activated) procedural tightening for future
materiality-derived thresholds:** before a materiality-derived numeric
threshold becomes effective, every candidate material identity should
receive an exact-diff + reachability + documented-contract review, not
merely a cluster-pattern classification — mirroring the methodology this
audit and DTR actually applied, retroactively, to the already-activated
42-ID population. This is proposal/rationale content only; it does not
create a new global governance rule in this transaction.

## 15. Non-goals

This transaction does **not**:

- change the currently-effective `85.812095853937%` threshold or its
  Condition 1A/1B gate (proposal-001 remains fully controlling);
- mutate `feature-engine-mutation-threshold-recalibration-proposal-001.md`
  (remains byte-unchanged at `12040044578d57d15e699a327a5a8ae39c1e9ea3`)
  or `feature-engine-condition1-current-material-gap-set-001.json`
  (remains byte-unchanged at `49c30b439eb84db95c55dc4a86de22e2b491dbb5`);
- mutate the root-cause audit artifact or the DTR artifact (both remain
  byte-unchanged);
- perform a fresh 2629-mutant (or any) formal mutation measurement;
- resolve any of the 24 Condition-1B candidate identities, or the 18
  DTR-resolved ones;
- implement any Wave-6 test — Wave 6 remains explicitly PAUSED during
  this candidate's own authoring and review (§17);
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

**Fresh-run, not inherited from proposal-001's own prior ADR Scope Rule
outcome** — re-examined specifically against this candidate's actual
content (the 24-identity companion artifact and the recalibrated Model A
figure), since a materially different identity population and a
materially different numeric figure are, in principle, capable of
triggering a different classification even under the same category of
change.

| §4b trigger | Applies to this candidate? | Reasoning |
|---|---|---|
| Platform Invariant change | No | No I-1–I-13 invariant touched. |
| Event Schema change | No | No event/fact schema, contract, or field touched. |
| Module Taxonomy/dependency-graph change | No | No `module-registry.yaml`/dependency-edge edit. |
| Governance/Approval-process change | No | Condition 1B's resolution semantics are verbatim the same, already-established `(a) killed/confirmed_timeout OR (b) individually reclassified` mechanism proposal-001 and the original threshold both already use — applied to a smaller, more precisely audited identity set. The new pinned 24-ID artifact is inert data (a sorted ID list + hash + engineering-status notes), not a new review role, lifecycle stage, or approval-gate structure. |
| Decision affecting >1 module | No | Strictly Feature-Engine-only, Tier-1 scope — unchanged from proposal-001. |
| Hard-to-reverse decision | No | §12's symmetric re-proposal mechanism preserves full reversibility, identical in kind to proposal-001's own. |
| Locked-ADR modification/supersession | No | No ADR touched. |
| **Alternative: significant but reversible single-module internal change** | **Yes** | A genuinely significant (will eventually gate a real PASS/FAIL dimension), single-module, contract-preserving, already-delegated-authority (Chapter 13 §13.14 defers exact threshold detail to Testing-Convention-owned territory), fully-reversible candidate — same textual fit as proposal-001's own §14 finding. |

```text
ADR_SCOPE_DISPOSITION: ADR_OPTIONAL
```

**Risk Classification:** a substantive policy/quality-gate recalibration,
not mere evidence/bookkeeping recording (ruling out `R0`); no Platform
Invariant, Event Schema, cross-module, or Locked-ADR effect, fully
reversible via §12 (ruling out `R2`):

```text
Risk: R1 (candidate disposition — pending independent confirmation by
  this candidate's own Review A, exactly as proposal-001's R1 was
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
(ADR-045 `D10(a)` — a governing artifact, here proposal-001's own §8
precedent and Testing Convention v0.17's own named Step-8 "Product Owner
decision", explicitly reserves the threshold-selection decision class to
Product Owner). Therefore:

```text
DTR is NOT ELIGIBLE for proposal-002's own activation decision.
```

**Proposed path (not performed by this transaction):** after this
candidate receives a `CLEAN` (or remediated-to-`CLEAN`) Review A, route
exactly one narrow Product Owner decision naming the exact candidate
figure (`85.127424876379%`), the exact companion artifact (set-002, 24
IDs), the review disposition, and the boundary being approved — mirroring
proposal-001's own top-banner activation record exactly. **This decision
is not requested by this transaction.**

## 17. Wave 6 remains paused during authoring/review

This transaction does not implement any of the 13 remaining unremediated
genuine identities. Reason: stabilize the controlling quality-bar
candidate (this document) before spending the next implementation wave's
effort — implementing tests against identities pinned by a candidate
whose own companion artifact could still change under Review A would risk
wasted or misaligned work. After proposal-002 is reviewed and a Product
Owner decision is made (activated or not), Wave 6 may proceed against
exactly the 13 unremediated genuine identities named in §4 above (or
their equivalent in whatever population is controlling at that time).

## 18. Candidate lineage — no history rewritten

```text
Original threshold:            87.001959503592%
                                historical / superseded by proposal-001.

Recalibration proposal-001:    85.812095853937% + 42 IDs (set-001)
                                CURRENT APPROVED -- EFFECTIVE.

Root-cause audit + DTR:        24 genuine / 18 non-material / 0 unclear
                                (FE-EVID03-COND1-MATERIAL-SET-DTR-001,
                                CLEAN -- 0/0/1).

Recalibration proposal-002:    85.127424876379% + 24 IDs (set-002)
                                THIS DOCUMENT -- CANDIDATE -- NOT
                                EFFECTIVE / AWAITING REVIEW A.
```

No prior document is rewritten, reinterpreted, or retroactively edited by
this candidate.
