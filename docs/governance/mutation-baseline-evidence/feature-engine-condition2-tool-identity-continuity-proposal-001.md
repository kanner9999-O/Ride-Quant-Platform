# Feature Engine Condition-2 Tool-Identity-Continuity Mechanism — Proposal 001

**STATUS: CANDIDATE — NOT EFFECTIVE / AWAITING REVIEW A**

This document is not yet reviewed, not yet approved, and confers no
Condition-2 credit to any identity. It proposes one additional,
narrowly-scoped resolution mechanism for the Feature Engine Condition-2
material-gap identity-resolution contract (§4.1 of
`feature-engine-mutation-threshold-proposal-001.md`) — it does not edit
that document, does not reinterpret its existing branches, and does not
apply to any other module or gate.

## 0. Authority resolved directly (fresh-read, not restated from memory)

- **Controlling Condition-2 mechanism, as it stands today:**
  `feature-engine-mutation-threshold-proposal-001.md` §4.1 — every one of
  the 170 pinned historical material-gap identities must be resolved via
  exactly one of: **(a)** the exact historical mutant ID itself now
  `killed`/`confirmed_timeout` in fresh formal evidence, or **(b)** a
  separate, governed decision — exact mutant identity + specific semantic
  justification + a reviewed/recorded decision — establishing that a
  legitimate refactor altered or removed the exact code path such that
  the original material-gap classification no longer applies. This
  document does not edit, weaken, or reinterpret either branch.
- **Current Condition-2 state:** `169/170` — `BLOCKING`. The sole
  remaining unresolved identity is `contracts.x__seal_verified_authority
  __mutmut_33`, classified `TOOL_IDENTITY_DRIFT — NO EXISTING GOVERNED
  RESOLUTION MECHANISM` in
  `feature-engine-condition2-final-six-resolution-assessment-001.json`
  (that assessment's own conclusion, verified byte-unchanged, not
  reopened by this document: "No existing governed mechanism in this
  repository's Testing Convention / §4.1 stack covers 'same semantic
  mutation, different tool-assigned ID due to unrelated file-level
  AST-node-count drift.'").
- **Condition 1:** `PASS — REVIEW A VALIDATED` (unaffected by this
  document; not reopened).
- **Condition 3:** `SATISFIED — REVIEW A VALIDATED` (unaffected by this
  document; not reopened).
- **`P3-FEATURE-QG-EVID-03`:** `OPEN`.

## 1. What this proposal is, and is not

**Is:** a candidate for exactly one additional, disjoint Condition-2
resolution branch — **(c) `VERIFIED_TOOL_IDENTITY_CONTINUITY`** — for the
narrow case where a historical material-gap mutant's exact tool-assigned
identity was reassigned to a different ordinal by mutmut's own AST-node
counting, with the underlying Feature code path at that exact
construction site otherwise unchanged, unrefactored, and unremoved.

**Is not:** a re-interpretation of branch (a) or (b); a general
identity-continuity/renumbering table; a heuristic ("same function name
therefore same mutant") matcher; an ordinal-proximity inference rule; a
change to the raw mutation-score denominator/numerator formula; a grant
of Condition-2 credit to any identity, including
`contracts.x__seal_verified_authority__mutmut_33` — this document does
not resolve that row. It also does not authorize any broader
tool-version-compatibility claim beyond the current mutmut `3.7.0`
evidence pinned below.

## 2. Why branches (a) and (b) do not cover this case

Restated from the already-governed final-six assessment, not
reinterpreted:

- **(a) does not apply** — it requires the *exact historical ID itself*
  (`..._mutmut_33`) to now be `killed`/`confirmed_timeout`. Current
  `..._mutmut_33` is a different, unrelated mutation (§4 below) —
  confirmed `DISCONTINUOUS`.
- **(b) does not apply as written** — it requires "a reviewed refactor
  altered or removed the exact code path such that the original
  material-gap classification no longer applies." No refactor occurred;
  the exact code path is unchanged (§4 below). §4.1(b) explicitly
  forbids crediting on ID-drift alone, and this proposal does not ask it
  to.

This is a genuine gap in the existing evidentiary contract, not a
disagreement with either existing branch's own scope.

## 3. Fresh technical reconstruction (this transaction, not inherited)

Full method, boundary provenance, and per-finding verification detail:
`feature-engine-condition2-tool-identity-continuity-technical-evidence-001.json`
(new, additive). Summary of the five facts this proposal depends on, all
independently fresh-verified this transaction (not merely inherited from
`feature-engine-condition2-final-six-resolution-assessment-001.json`,
which is left byte-unchanged):

1. **`_seal_verified_authority`'s semantic code path was not refactored.**
   Confirmed via direct historical-vs-current diff of the full function
   body (historical boundary `8d6293aca773757bc3b62cc0d3b80cba9e243954`,
   reconstructed with the exact pinned mutmut `3.7.0` via a disposable
   isolated worktree; current boundary
   `e9873e17170ada23da98be9c7dd3820045d64cde`, `src` tree
   `1029a9fef083b0902d6d00a2e96cfde14213324c`, identical to Evidence-006's
   own executable boundary). One honest correction of a minor
   imprecision in the prior assessment is recorded in the technical
   evidence artifact (the historical delegating call had 6 kwargs, not
   "the identical 7-kwarg list ... as it did historically" — the 7th,
   `merge_policy`, is a purely additive ADR-043 parameter) — this does
   not change the substantive conclusion.
2. **Historical mutation site and current `mutmut_36` site are
   structurally and semantically the same.** Both are the exact same
   single-line transformation, `feature_computation_profile=
   feature_computation_profile,` → `feature_computation_profile=None,`,
   at the same logical position in the same delegating call.
3. **Current `mutmut_33` is a different, unrelated mutation.** It negates
   the new `isinstance(merge_policy, InputMergePolicy)` guard — a code
   branch that did not exist at the historical boundary at all. This
   directly demonstrates the ordinal collision, not merely asserts it.
4. **The historical-33 → current-36 mapping is unique.** An exhaustive
   scan of all 49 current `x__seal_verified_authority__mutmut_N`
   mutants (excluding `__mutmut_orig`) found exactly one exact match to
   the historical diff: `mutmut_36`.
5. **The drift is tool-generated ordinal renumbering, not a Feature
   behavior change.** The function grew from 44 to 49 total mutants
   between the two boundaries, fully explained by the additive
   `merge_policy` parameter/validation/docstring change identified in
   finding 1 — not by any change at the mutated site itself.

## 4. Current-boundary status evidence for the successor identity

Bounded, isolated verification only — **no full 2629-mutant rerun was
performed**, per instruction. Target:
`feature_engine.contracts.x__seal_verified_authority__mutmut_36`.

```text
Environment: python 3.13.6, mutmut 3.7.0, pytest 9.1.1, coverage 7.16.0,
             platformdirs 4.11.5, ruff 0.16.4, mypy 2.3.1 -- all match
             requirements-dev.lock.txt and Evidence-006's own recorded
             versions exactly.

Run 1: fresh workspace (mutants/ absent before run) ->
       python -m tooling run --max-children 1
       feature_engine.contracts.x__seal_verified_authority__mutmut_36
       -> killed

Run 2: fresh workspace (mutants/ + .mutmut-cache removed and
       regenerated before this run) -> same command -> killed

Agreement: killed + killed. No disagreement.
```

Per instruction, agreement between the two independent isolated runs
permits authoring a positive continuity candidate. Full command
transcripts and result-store confirmation are in the technical evidence
artifact (§3 above).

## 5. Proposed mechanism — branch (c): `VERIFIED_TOOL_IDENTITY_CONTINUITY`

**Proposed addition to Condition-2's existing per-identity resolution
contract** (companion to, not an edit of, §4.1 of
`feature-engine-mutation-threshold-proposal-001.md`):

> A historical material-gap identity may be mapped to a current
> tool-generated identity, and thereby resolved under a NEW, disjoint
> branch **(c) `VERIFIED_TOOL_IDENTITY_CONTINUITY`**, ONLY when ALL of
> the following are true:
>
> - **C1** — the historical mutant body is reproducibly reconstructed
>   from the exact pinned historical source boundary using the exact
>   pinned mutation tool identity (no reliance on ordinal coincidence or
>   memory);
> - **C2** — the current mutant body is reproducibly generated from
>   current source, using the same method;
> - **C3** — the historical and current mutations target the same
>   semantic construction site and perform the same mutation (verified
>   by direct diff comparison, never by function-name or ordinal
>   similarity alone);
> - **C4** — the mapping is unique 1:1 (verified by an exhaustive scan of
>   every current mutant of the relevant function); any ambiguity fails
>   closed — no candidate is authored, no credit is proposed;
> - **C5** — the underlying Feature code path has NOT been legitimately
>   refactored, removed, or semantically changed; if it has, that case
>   continues to use existing §4.1(b), never this mechanism;
> - **C6** — the historical and current exact IDs differ solely because
>   of mutation-tool-generated identity/ordinal drift (an affirmative,
>   evidenced causal account is required, not merely "the numbers
>   differ");
> - **C7** — any current reuse/collision of the historical ordinal is
>   explicitly demonstrated, by direct diff, to represent a different
>   mutation — never merely asserted;
> - **C8** — mutation-tool provenance is compatible and pinned; for this
>   initial mechanism, scope is bounded to the current, evidenced mutmut
>   `3.7.0` toolchain only, unless a future, independently governed
>   decision extends it;
> - **C9** — the current successor identity itself carries qualifying
>   fresh evidence (formal `killed`/`confirmed_timeout` status, or, as in
>   this initial case, agreeing bounded isolated-verification evidence
>   per §4 above);
> - **C10** — credit is granted **per historical identity only**, and
>   requires its own separate, reviewed/recorded governed decision — this
>   document, by itself, grants none;
> - **C11** — no unrelated mutant kill may ever substitute for the
>   historical identity's own resolution;
> - **C12** — this mechanism creates no adjustment whatsoever to the raw
>   mutation-score numerator/denominator; it is a Condition-2
>   per-identity-accounting mechanism only, structurally isolated from
>   Condition 1 exactly as branches (a)/(b) already are.
>
> Branch (c) does not reinterpret, widen, or narrow branches (a) or (b).
> A historical identity that fails any single criterion above remains
> unresolved under this mechanism and must continue to rely on (a) or
> (b), or remain an open, honestly-reported gap.

**Why this is not a bulk table, heuristic, or ordinal-only rule:** every
one of C1–C12 requires exact, reproducible, per-identity technical
evidence (§3–§4 demonstrate exactly this discipline for the one case this
document actually examines). No shortcut based on name similarity,
proximity, or count is permitted by the mechanism's own text.

## 6. Bounded application — this document does not resolve any row

`contracts.x__seal_verified_authority__mutmut_33`'s own C1–C12 evidence
is fully assembled in §3–§4 above and would, on the fresh technical
record, appear to satisfy all twelve criteria. **This document
nonetheless grants no credit** — per C10, crediting a specific historical
identity under branch (c) requires its own separate, reviewed/recorded
governed decision, distinct from the act of authoring the mechanism
itself. That decision is explicitly **not requested by this document**
(§9).

## 7. Preserve Condition 1 and Condition 3

Unaffected, not reopened, not touched by this document:

```text
Condition 1: PASS -- REVIEW A VALIDATED (evidence-006 +
             FE-EVID03-COND1-FORMAL-006-DTR-001). Unchanged.
Condition 3: SATISFIED -- REVIEW A VALIDATED. Unchanged.
```

## 8. Preserve Condition 2's current count

```text
Condition 2 before this document: 169/170 -- BLOCKING.
Condition 2 after this document:  169/170 -- UNCHANGED.
```

No credit is granted by authoring a candidate mechanism. Should this
mechanism later receive a `CLEAN` (or remediated-to-`CLEAN`) Review A and
a subsequent, separate, governed per-identity decision credit
`contracts.x__seal_verified_authority__mutmut_33`, the resulting state
would become `170/170` — that is a distinct, future, not-yet-requested
transaction.

## 9. Current active state — unchanged by this authoring transaction

```text
Condition 1:                  PASS -- REVIEW A VALIDATED
Condition 2:                  169/170 -- BLOCKING (unchanged)
  final unresolved row:       contracts.x__seal_verified_authority
                               __mutmut_33
  candidate continuity
  mechanism:                  AUTHORED -- NOT EFFECTIVE / AWAITING
                               REVIEW A
Condition 3:                  SATISFIED -- REVIEW A VALIDATED
P3-FEATURE-QG-EVID-03:        OPEN
Feature Engine approval:      NOT APPROVED
LIVE:                         NOT_AUTHORIZED
PO action required now:       NO
```

## 10. `ADR_SCOPE_DISPOSITION` — fresh-run Chapter 0 §4b, not inherited

**Not mechanically inherited from any prior document's own disposition.**
`feature-engine-condition2-final-six-resolution-assessment-001.json`'s
own `secondary_recommendation_deferred` field flagged a *prospective*
concern that pursuing this class of work might require *amending
Testing Convention v0.16/v0.17's §4.1 text itself* — which it reasoned
would likely be `ADR_REQUIRED` as a direct edit to an already-Locked
mechanism. This document deliberately takes the narrower path that
concern did not evaluate: a **companion candidate document** (exact same
pattern already used, without an ADR, for
`feature-engine-mutation-threshold-recalibration-proposal-002.md` and
`-003.md` relative to `-001.md`'s own §4.1) — it does not edit
`feature-engine-mutation-threshold-proposal-001.md` in place, does not
bump its version, and does not touch Testing Convention at all. The
trigger-by-trigger analysis below is re-derived fresh against this
document's actual content, not against the hypothetical in-place-edit
scenario that prior note flagged.

### 10.1 Trigger-by-trigger analysis (Chapter 0 §4b)

| §4b trigger | Applies to this candidate? | Reasoning |
|---|---|---|
| Platform Invariant change | No | No I-1–I-13 invariant (`docs/constitution/02-platform-invariants.md`) is touched. |
| Event Schema change | No | No event/fact schema, contract, or field is added, removed, or reinterpreted. |
| Module Taxonomy/dependency-graph change | No | No `module-registry.yaml`/dependency-edge edit. |
| Governance/Approval-process change | **No — examined directly, not merely re-asserted.** The question is whether adding a third, disjoint per-identity evidentiary branch (c) — under the same identity-pin + individually-recorded-justification + separate-governed-decision shape Testing Convention v0.16 item 8 and §4.1(b) already both use — creates a NEW review workflow, role, lifecycle stage, or approval-gate structure, or merely applies that SAME already-established evidentiary shape to a new substantive category (tool-renumbering continuity, as opposed to behavior-equivalence or legitimate refactor). Reviewed directly against item 8's own text (§8 of `docs/engineering/testing.md`): item 8 already requires, for ANY mutant-identity-level adjustment claim, "a deterministic, reproducible, exactly-pinned mutant identity... an individually-recorded semantic justification... and a governed adjustment mechanism (a reviewed, recorded decision)" — this is the identical procedural shape C1–C12 impose. No new reviewer role is created (Review A remains the reviewing principal); no new lifecycle stage is created (Draft/Candidate → Review A → Product Owner decision, unchanged); no new approval-gate structure is created (this document routes through the same Chapter-13-delegated, Testing-Convention-owned evidentiary framework §4.1(a)/(b) already occupy). The genuine novelty is in the SUBSTANCE of what may qualify as evidence (a new fact pattern, not previously addressed), not in the PROCESS by which it is reviewed and decided — the Constitution's own §4b table asks specifically about process/contract/invariant/schema change, not about the breadth of evidentiary categories a delegated, already-Testing-Convention-owned mechanism may recognize. |
| Decision affecting >1 module | No | Strictly Feature-Engine-only; explicitly bounded in scope (§1, §5's C8). |
| Hard-to-reverse decision | No | This document, and any future per-identity decision under it, can be revised or withdrawn by a future governed decision exactly as proposal-002/003 could revise proposal-001's own numeric figure — no structural lock-in is created. |
| Locked-ADR modification/supersession | No | No ADR is touched. Testing Convention is a living document (Constitution §5.1), not an ADR (§5.2) — this document is a new, separate companion candidate, not an in-place edit of any living document or ADR. |
| **Alternative: significant but reversible single-module internal change** | **Yes** | A genuinely significant (it will, if later activated and applied, resolve a real Quality-Gate blocking identity), single-module, contract-preserving (no Feature Engine behavior/contract is touched), already-delegated-authority (reuses item 8's shape), fully reversible candidate. Textually the same fit Constitution §4b's own "ADR Optional" row example describes. |

### 10.2 Classification

```text
ADR_SCOPE_DISPOSITION: ADR_OPTIONAL
```

**No ADR is authored by this document.** This classification is reached
by direct trigger-by-trigger analysis, not by mechanically inheriting
the task's own suggested expectation — the Governance/Approval-process
trigger in particular was examined on its own facts (§10.1), including
the genuine tension the prior assessment's own deferred note raised, and
resolved by distinguishing process (unchanged) from evidentiary
substance (novel, but not itself a process/contract/invariant/schema
change). A future reviewer or Product Owner remains free to judge, at
Review A or the eventual decision point, that an ADR would nonetheless
be worthwhile for a mechanism of this kind — that discretionary option
is preserved, not exercised, here.

### 10.3 Risk Classification

Per `P3-REVIEW-001` (`docs/governance/phases/phase-3-rules.md` §8):
routing is by TYPE of change, not by module size. This document
introduces a genuinely **new** evidentiary/authority mechanism — a third,
previously-nonexistent Condition-2 resolution branch — which is squarely
`P3-REVIEW-001`'s own "new architecture / authority / contract
semantics" category, not a "bounded semantic correction" (the latter
describes recalibrating an *existing* mechanism's numbers/population,
exactly what proposal-002/003 each did relative to proposal-001's own
already-established (a)/(b) branches — this document does the opposite:
it adds a new branch type).

```text
Risk: R2 -- Review A + mandatory Risk Classification. Review A may
      recommend an optional advisory cross-check; the Product Owner
      chooses whether to use one (never automatic Review A/B pairing).
```

## 11. Review and decision path

```text
Review A: mandatory.
R2: mandatory Risk Classification (this section). Optional advisory
    cross-check recommendable by Review A; Product Owner decides
    whether to use it.
```

**This mechanism's own eventual activation is explicitly
Product-Owner-reserved** (ADR-045 `D10(a)` — a quality/evidence-policy
decision of this kind is not a bounded, mechanical application of
already-settled criteria; it establishes new criteria). Therefore:

```text
DTR is NOT ELIGIBLE for this candidate's own activation decision, nor
for any future per-identity credit decision made under it (C10).
```

**Proposed path (not performed by this document):** after this candidate
receives a `CLEAN` (or remediated-to-`CLEAN`) Review A and any
Product-Owner-selected advisory cross-check, route exactly one narrow
Product Owner decision naming: the exact mechanism text (§5), the exact
Review A disposition, and whether to activate branch (c) as a general
mechanism. A SEPARATE subsequent decision (§6, §10.1) would then be
required to apply it to `contracts.x__seal_verified_authority__mutmut_33`
specifically. **Neither decision is requested by this document.**

## 12. Non-goals

This document does not: resolve
`contracts.x__seal_verified_authority__mutmut_33`; change Condition 2
from `169/170`; edit production source, tests, or mutation tooling; add
tests to force a favorable outcome; change Condition 1 or reopen
Condition 3; close `P3-FEATURE-QG-EVID-03`; approve Feature Engine;
authorize LIVE; author a broader Ride governance/process-improvement
ADR; weaken exact-identity accounting generally; or affect any module
outside Feature Engine.

## 13. Lineage — no history rewritten

```text
feature-engine-mutation-threshold-proposal-001.md §4.1 -- (a)/(b),
  APPROVED -- EFFECTIVE, unchanged, not edited by this document.
feature-engine-condition2-final-six-resolution-assessment-001.json --
  established TOOL_IDENTITY_DRIFT classification for
  contracts.x__seal_verified_authority__mutmut_33, byte-unchanged.
feature-engine-condition2-remaining-ambiguity-historical-reconstruction
  -001.json -- resolved 2 unrelated rows via existing (b); byte-
  unchanged; explicitly left contracts.x__seal_verified_authority
  __mutmut_33 out of scope.
feature-engine-condition2-tool-identity-continuity-technical-evidence
  -001.json -- fresh technical evidence, this transaction (new).
feature-engine-condition2-tool-identity-continuity-proposal-001.md --
  THIS document -- CANDIDATE -- NOT EFFECTIVE / AWAITING REVIEW A.
```
