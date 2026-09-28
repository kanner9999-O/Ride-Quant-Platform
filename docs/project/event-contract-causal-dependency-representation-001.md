---
id: event-contract-causal-dependency-representation-001
title: "Event Contract Causal State-Dependency Declaration — Canonical Representation Derivation"
kind: analysis
version: "0.1"
status: Draft
owner: Product Owner
generated_at: "2026-09-28"
---

# EVENT-CONTRACT-CAUSAL-DEPENDENCY-REPRESENTATION-001

**Analysis / architecture-derivation artifact only.** Does not modify any Event Contract, does not
author an ADR, does not modify Chapter 8 or any Constitution file, does not continue
Structure/Regime Event Contract authoring.

**Boundary, fresh-verified before this transaction:** HEAD `064fcf59471865d3493b32ee78680ebd83b8c9a2`.
`docs/architecture/event-contracts/candle-closed/v1.0.yaml` matched pinned blob
`3f8d5f9a448c5796880d7a7b7a09d9c95c74c72f` exactly; `docs/architecture/event-contracts/candle-corrected/v1.0.yaml`
matched pinned blob `3649e516e4c69d948d8b3a4e4281bae019a7c0b7` exactly — neither touched by this
transaction. Fresh-read in full this transaction: `docs/adr/ADR-040.md` (Approved), Chapter 8
§8.1.1/§8.2.3/§8.3.4, `docs/adr/ADR-039.md` (Approved, re-confirmed), `docs/adr/ADR-047.md` (Approved,
re-confirmed unchanged), Chapter 0 §4b, `docs/adr/ADR-045.md` (R0/R1/R2 definitions), and the full
`docs/project/context-upstream-state-dependency-derivation-001.md` v0.4 §2.1–§2.10 (all 10 reviewed
event types), plus the exact `payload:` blocks of `structure.md` §3/§4/§5/§5a, `regime.md` §3/§4, and
`feature.md` §3/§4 to confirm exact payload field names used as test vectors below (read-only, not
modified).

## A. Authority basis

- **Chapter 8 §8.1.1** — every Referenced Authoritative Artifact (Event Contract version-artifacts
  included) must be versioned, immutable-once-referenced, non-reused-identifier, persistently
  resolvable within the committed horizon (explicit retention/archive policy required past it), and
  content-identity-verifiable.
- **Chapter 8 §8.2.3** — `causal_closure_policy.mode: declared-state-dependencies` requires
  `dependency_authority: per_effect_event_contract`: *"mỗi effect event dùng chính `event_contract_ref`
  đã pin của nó để phân loại `causation_refs` nào là state dependency... Classification KHÔNG được
  nằm trong code processor."* External non-state causes require only *"append-time committed/existence
  proof"* — *"run chỉ verify identity/existence, KHÔNG đọc payload"* — and are excluded from the
  merged apply set/frontier. Chapter 8 fixes the **semantic requirement** and the **prohibition on
  processor-code classification**. It does **not** fix a field name, field location, schema, selector
  grammar, or fail-closed algorithm.
- **Chapter 8 §8.2.3 canonical `event_record_ref`** — `{stream_id, sequence, event_id}`. Carries no
  cause-role label of any kind.
- **Chapter 8 §8.3.4** — `merge_constraints` is a distinct concept (causal **ordering**
  prerequisite — `prerequisite_policy: causation_must_resolve_before_apply`), owned by the Event
  Contract only as a *constraint*, with final merge **policy** owned by Input Contract. Chapter 8
  nowhere equates this with state-dependency **scope/visibility** classification (§8.2.3's own
  separate concept).
- **Approved `ADR-039`** — fixes the Event Contract version-artifact's canonical self-contained shape:
  `contract_id`, `contract_version`, `status`/review metadata, `event_type`, `event_class`,
  `allowed_streams`, `merge_constraints`, `payload_shape`, `payload_semantics_and_invariants`,
  `compatibility_commitment`, `provenance`. **No causal-dependency-classification field is named
  anywhere in ADR-039.**
- **Approved `ADR-040`** (fresh-read in full this transaction) — Class G retention/archive semantics
  for Event Contract version-artifacts: canonical path remains resolvable at current `HEAD` throughout
  the committed retention horizon; git history is content-identity/audit evidence only, never a
  fallback resolver; concrete past-horizon archival **mechanism** remains deferred. Consequences
  (verbatim, cited not re-derived): *"`ADR-039`'s own Consequences item (0) — establishing that an
  authoritative retention/archive policy exists before any Event Contract version-artifact becomes a
  usable `event_contract_ref` target — is now satisfied at the architecture-semantics level for Class G
  by this ADR (Event Contract version-artifacts are Class G)."* This is Finding 1's controlling text —
  see §B below.
- **`docs/project/context-upstream-state-dependency-derivation-001.md` v0.4** (Review A validated,
  `CLEAN — 0/0/1`) — the accepted classification result for all 21 causation-ref categories across the
  10 Context-upstream event types: `20 EXTERNAL_NON_STATE_CAUSE / 1 VACUOUS / 0 STATE_DEPENDENCY / 0
  UNRESOLVED`. Used here strictly as **test-vector data** — not re-derived, not re-classified.
- **Candle candidates** (`candle-closed/v1.0.yaml`, `candle-corrected/v1.0.yaml`), read-only — the
  locally-invented `payload_semantics_and_invariants.causation_ref_state_dependency_classification`
  nesting is the artifact under scrutiny in §D Option A, not modified here.

## B. Finding 1 — retention authority correction (`CANDLE-EC-A-MAJ-01`)

The Candle candidates' own header comments (authored prior to this transaction) state that even once
Published, they must not be treated as usable `event_contract_ref` targets *"until the
separately-governed platform retention/archive policy's concrete past-horizon archival mechanism is
established."* Fresh-read Approved `ADR-040` in full shows this framing is **stale**: `ADR-040`
already exists, is `Approved`, and its own Consequences section explicitly states the `ADR-039`
prerequisite is *"now satisfied at the architecture-semantics level for Class G"* — Event Contract
version-artifacts are named as Class G members directly in `ADR-040`'s own Decision text.

**Corrected state:**

```text
ADR-040 retention semantics:      APPROVED / SATISFIED at architecture-semantics level for Class G
Concrete past-horizon archival:   DEFERRED (ADR-040 does not invent the mechanism)
Current blocker to an otherwise-governed
Published Event Contract becoming
an event_contract_ref target:     NO — retention/archive policy absence is NOT the blocker
```

This does **not** claim archival tooling exists, does **not** claim any Event Contract is now
Published or runtime-usable, and does **not** modify `ADR-040`/`ADR-039`. It corrects only the
*characterization* of the retention gap. The Candle candidate files themselves are **not** edited in
this WP (`CANDLE-EC-A-MAJ-01` remains recorded, not remediated, per the task's own instruction) —
current bookkeeping (`docs/MANIFEST.md`, `docs/project/milestone.md`,
`docs/project/milestone-dashboard.html`) that presented "retention/archive policy absent" as a current
runtime-wide blocker is corrected in this same transaction (see Files Changed / commit).

The genuine remaining blocker to Event Contract publication/reference-usability is unrelated to
retention: the candidates are `Draft`, unreviewed, unpublished, and — per Finding 2 below — the
machine-readable causal state-dependency representation they must eventually use is not yet governed.

## C. Runtime-consumer requirements

The consumer of this representation is any current or future **Input Contract** that declares
`causal_closure_policy: {mode: declared-state-dependencies, dependency_authority:
per_effect_event_contract}` (Chapter 8 §8.2.3) — today, no Input Contract has reached `Published`
using this mode (Context Input Contract v0.3 remains `Draft`/`NOT PUBLISHED`), but the mechanism must
be implementable **once**, generically, by a shared validator/library used across every current and
future producer module (`market-data-ingestion`, `structure-engine`, `raw-regime-engine`,
`feature-engine`, and any later module) and every current and future Input Contract instance — never
reimplemented per event type inside processor code (the exact prohibition Chapter 8 §8.2.3 states).
Concretely, the validator must be able to answer, for one effect event and its pinned
`event_contract_ref`:

1. Is this event root/vacuous (no causal-closure obligation)?
2. For each entry in `envelope.causation_refs`, is it `STATE_DEPENDENCY` (must be resolved within
   this Input Contract's apply set/cursor universe, participates in frontier completeness) or
   `EXTERNAL_NON_STATE_CAUSE` (existence/commit proof only, excluded from apply set/frontier, payload
   never read)?
3. Is every entry accounted for (no unclassified, no ambiguously double-classified entry)?

## D. Option comparison

### Option A — current freeform/nested semantic block (as authored in the Candle candidates)

```yaml
payload_semantics_and_invariants:
  causation_ref_state_dependency_classification:
    classification: VACUOUS   # or: categories: {<ad hoc label>: {classification: ..., ...}}
```

**Assessment: NOT machine-canonical.** Three independent defects:

1. `payload_semantics_and_invariants` is, by `ADR-039`'s own illustrative shape and by its actual use
   in `feature-computed/v1.0.yaml`, a narrative/prose field (descriptions, invariant sentences) — no
   authority defines a strict machine schema for *anything* nested inside it. Any validator reading it
   would need free-text/prose parsing, directly violating requirement 11 (no informal prose search).
2. The nesting uses ad hoc category labels (e.g. `corrected_fact`) with **no formal linkage** back to
   a specific entry of the actual `envelope.causation_refs` array. A generic validator has no rule
   telling it "the label `corrected_fact` corresponds to `causation_refs[0]`" — that correspondence
   only exists in the surrounding human prose.
3. No cardinality grammar, no selector grammar, no fail-closed completeness rule — nothing prevents an
   Event Contract from silently omitting a category, and nothing lets a validator detect that omission
   mechanically.

**Verdict: rejected as the canonical representation** — it is a useful human-readable annotation, but
cannot satisfy requirements 1/3/4/10/11 as currently shaped.

### Option B — new top-level Event Contract field

A dedicated canonical field, sibling to `event_class`/`allowed_streams`/`merge_constraints`/
`payload_shape`/`payload_semantics_and_invariants`/`compatibility_commitment` in `ADR-039`'s own
enumerated shape.

**Assessment: correct placement.** This is a policy declaration exactly like `merge_constraints` or
`compatibility_commitment` — self-contained, versioned with the artifact, immutable at publication
(fits `ADR-039`'s model, requirement 9), and trivially parseable by path without prose search
(requirement 10/11). **Recommended** — see §E. The remaining question is the field's *internal* shape,
addressed by Option E below.

### Option C — structured subfield of `merge_constraints`

**Assessment: rejected — conflates two distinct Chapter-8 concepts** (the task's own explicit warning,
independently confirmed). `merge_constraints.prerequisite_policy` (§8.3.4) governs **ordering** — must
this cause's event record apply before the effect, contributing to `P_causation`/`P_global`. State-
dependency classification (§8.2.3) governs **scope/visibility** — must this cause's *payload* be
inside the Input Contract's apply set/cursor universe. A root/`VACUOUS` event like `candle-closed`
already has `merge_constraints: {}` (no prerequisite, correctly empty); forcing classification content
into that same field would either (a) make a truthfully-empty `merge_constraints` non-empty for a
root event, corrupting the "no prerequisite" signal `candle-closed/v1.0.yaml` currently and correctly
sends, or (b) require two independently-versioned concepts to share one field's schema evolution,
violating the separation requirement 8 outright. **Rejected.**

### Option D — declare only state-dependency selectors, default everything else to external

**Assessment: rejected in its literal (silent-default) form — fails requirement 4 (fail-closed).**
Chapter 10 §10.3.1's own governing principle (*"Vắng mặt là mơ hồ; tuyên bố tường minh là một lựa
chọn có thể audit"*) and Chapter 8 §8.2.3's own fail-closed default for unresolved classification both
argue against a silent default. Under Option D as literally stated, a future producer that starts
emitting a genuinely new `causation_ref` role the Event Contract's author simply forgot to declare
would be silently treated as `EXTERNAL_NON_STATE_CAUSE` — a real classification the code
never actually made, defaulted into existence by omission. That is fail-**open**, not fail-closed: a
correctness gap (a processor might apply an effect without state it actually needed), not merely an
audit-trail gap. Its underlying *instinct* — minimize authoring burden, since 20 of 21 reviewed
categories are `EXTERNAL_NON_STATE_CAUSE` and 0 are `STATE_DEPENDENCY` — is preserved without the
unsafe default: declaring an `EXTERNAL_NON_STATE_CAUSE` role costs exactly the same one entry as
declaring a `STATE_DEPENDENCY` role in the recommended representation (§E), so there is no genuine
authoring-cost reason to accept an unsafe default. **Rejected as specified; its minimalism instinct is
absorbed into Option B/E without the unsafe default.**

### Option E — explicit per-cause rule table

```text
role/category | selector | cardinality | classification
```

**Assessment: necessary, not over-specified.** Proven necessary, not merely convenient, by the actual
test-vector data in §H below: multiple reviewed event types (`BREAK_OF_STRUCTURE_DETECTED`,
`STRUCTURE_FACT_INVALIDATED`, `REGIME_CLASSIFIED`, `REGIME_FACT_INVALIDATED`, `FEATURE_COMPUTED`,
`FEATURE_FACT_INVALIDATED`) carry **more than one** causation-ref category simultaneously, each
requiring its own selector/cardinality — a single scalar classification per event type cannot express
this, and would be outright incapable of representing the required mixed-case capability (§I). Option
E's granularity is the *internal shape* of Option B's field, not a competing alternative — the
recommendation is **B (placement) + E (internal shape), combined**.

**No better option was identified.** A–E are the complete assessed set; B+E is recommended.

## E. Proposed canonical representation

New top-level Event Contract field: **`causal_state_dependency_declaration`**.

```yaml
causal_state_dependency_declaration:
  vacuous: <bool, default false>
  # true ONLY for a root event whose envelope.causation_refs is canonically [] (Chapter 8 §8.2.1).
  # When true, `roles` MUST be empty and `closed` MUST be true (see below) — any non-empty
  # causation_refs on this event_type is then an integrity violation, fail-closed (§J).

  closed: <bool, REQUIRED, true in every case reviewed here>
  # true = every entry of envelope.causation_refs MUST match exactly one declared role below;
  # an unmatched or multiply-matched entry is an integrity violation, fail-closed (§J). No
  # currently-reviewed event type has any reason to declare `closed: false`; the grammar keeps
  # the field explicit rather than assuming it, per the same "explicit over implicit default"
  # principle Option D was rejected for violating.

  roles:
    - role_id: <string, unique within this artifact, human-legible label>
      selector:
        # Exactly ONE of the two forms below — never both on the same role.
        payload_field: <dot-path into payload_shape, e.g. "invalidated_fact_ref" or
          "broken_swing_ref.swing_confirmed_event_ref">
        # OR:
        by_target:
          event_types: [<UPPER_SNAKE event_type values the target MAY be>]
          contract_ids: [<contract_id values the target's own event_contract_ref.contract_id MAY be,
            optional, more precise than event_types when needed>]
          discriminated_by: <optional dot-path into THIS event's own payload — e.g.
            "invalidation_cause" — whose value selects a NARROWER event_types/contract_ids set,
            see event_types_by_discriminant below>
          event_types_by_discriminant:
            <discriminant value>: [<event_type values allowed for that discriminant value>]
      cardinality: {min: <int>, max: <int or null for unbounded>}
      # or the shorthand {exactly: <int>}
      classification: VACUOUS | EXTERNAL_NON_STATE_CAUSE | STATE_DEPENDENCY
      apply_time_requirement: >
        Required for EXTERNAL_NON_STATE_CAUSE and STATE_DEPENDENCY roles — free-text rationale
        citing exactly what authoritative application does and does not need from this cause,
        consistent with Chapter 8 §8.2.3's own apply-time test.
      authority: >
        Citation to the already-reviewed state-dependency derivation category this role
        transcribes (never re-derived inline).
```

**Selector semantics:**

- `payload_field` — the role's ref(s) are read directly from the effect event's **own** payload, at
  the declared path, using the type already fixed by `payload_shape` (`event_record_ref` or an array
  of it). No inspection of any other event is required to resolve which entries this role claims.
- `by_target` — the role claims any so-far-unclaimed `envelope.causation_refs` entry whose **target's
  own envelope** (`event_type`, optionally `event_contract_ref.contract_id`) matches the declared
  allow-set — resolved via the target's own identity/existence verification that Chapter 8 §8.2.3's
  tuple-consistency rule already mandates for every causation_ref, never via the target's domain
  payload (requirement 6; permitted explicitly by requirement 7). `discriminated_by` narrows the
  allow-set using a value already present in the **effect event's own** payload (never the target's) —
  fully generic and data-driven, not event-type-specific code (§F, §H).

**Separation from `merge_constraints` (requirement 8, Option C's rejection applied positively):** this
field and `merge_constraints` are independent, co-existing top-level fields. A role's classification
here never implies, and is never implied by, `merge_constraints.prerequisite_policy` — an Event
Contract may (and, per the existing precedent, does) declare
`prerequisite_policy: causation_must_resolve_before_apply` platform-uniformly for all non-empty
`causation_refs` while this field separately classifies each entry's scope/visibility.

## F. Generic validation algorithm (no event-type-specific code)

Given one effect event record and its pinned `event_contract_ref`:

1. Resolve `event_contract_ref` to its Event Contract version-artifact (already-mandated `ADR-039`
   direct-path resolution).
2. Read that artifact's `causal_state_dependency_declaration`.
3. If `vacuous: true`: assert `envelope.causation_refs == []`. Mismatch → **fail closed** (§J-4). Stop.
4. Otherwise, for each declared role, independently:
   a. `payload_field` selector — dereference the declared path in the effect's **own** payload
      (already required present by `payload_shape`); every `event_record_ref` found there (singular or
      every element if the path is array-typed) is claimed by this role.
   b. `by_target` selector — for every `envelope.causation_refs` entry not yet claimed by any role,
      resolve the target's own envelope via the tuple-consistency existence check Chapter 8 §8.2.3
      already requires; if `discriminated_by` is set, read that path in the **effect's own** payload
      to select the applicable `event_types_by_discriminant` entry; test the target's `event_type`
      (and/or `event_contract_ref.contract_id`) against the resulting allow-set; every match, up to
      this role's own cardinality budget, is claimed by this role.
   c. Validate the role's own `cardinality` against the number of refs it claimed. Unsatisfied →
      **fail closed** (§J-3).
5. Cross-check: every `payload_field`-derived ref MUST also literally appear in
   `envelope.causation_refs` (tuple-consistency between the payload's own declared duplicate and the
   envelope set — the exact discipline `structure.md`'s own `invalidated_fact_ref` description already
   states: *"trùng với causation_refs"*). Mismatch → **fail closed** (§J-6).
6. If `closed: true` (required in every case here): every entry of `envelope.causation_refs` MUST now
   be claimed by **exactly one** role. Any unclaimed or multiply-claimed entry → **fail closed**
   (§J-1/§J-2).
7. For every ref claimed `STATE_DEPENDENCY`: its target's payload/state MUST be within the consuming
   Input Contract's apply set/cursor universe (Chapter 8 §8.2.3 `mode: declared-state-dependencies`
   in-scope rule) — the Input Contract validator includes it in frontier/completeness accounting.
8. For every ref claimed `EXTERNAL_NON_STATE_CAUSE`: only existence/commit proof is required (already
   satisfied by step 4b's own tuple-consistency check); excluded from the merged apply set/frontier;
   its domain payload is never read to reach or use this classification.

No step above references a specific `event_type`, `contract_id`, or Domain Contract by name — every
decision is driven entirely by the pinned Event Contract's own declared schema (requirement 2), using
only the effect's own payload and each target's own envelope/identity (requirements 6/7).

## G. Candle mapping

```yaml
# candle-closed/v1.0 — illustrative, not applied to the file in this WP
causal_state_dependency_declaration:
  vacuous: true
  closed: true
  roles: []
```

```yaml
# candle-corrected/v1.0 — illustrative, not applied to the file in this WP
causal_state_dependency_declaration:
  vacuous: false
  closed: true
  roles:
    - role_id: corrected_fact
      selector:
        by_target:
          event_types: [CANDLE_CLOSED, CANDLE_CORRECTED]
      cardinality: {exactly: 1}
      classification: EXTERNAL_NON_STATE_CAUSE
      apply_time_requirement: >
        Authoritative application does not require re-reading the corrected predecessor's domain
        payload/state; the effect carries the complete replacement OHLCV/state itself; the
        predecessor reference is required only for identity/existence/lineage/causal precedence.
      authority: >
        docs/project/context-upstream-state-dependency-derivation-001.md v0.4 §2.2.
```

`candle-closed` has no named payload field and no target to select against — `vacuous: true` is the
entire declaration, matching `causation_refs: []` (root event) exactly. `candle-corrected` has no
payload-field duplicate of its causal reference (`candle.md` §5 places it envelope-only), so it is the
canonical worked example of the `by_target` selector form with fixed (non-discriminated) `event_types`.

## H. Mapping proof across all 10 reviewed Context-upstream event types

Not re-deriving any classification — citing the already-Review-A-validated result per category
(`context-upstream-state-dependency-derivation-001.md` v0.4 §2.1–§2.10) and confirming, per event,
that the declared payload field names (fresh-read from `structure.md`/`regime.md`/`feature.md`,
read-only) support a `payload_field` or `by_target` selector without any event-specific validator code.

| # | `event_type` | Role(s) | Selector | Cardinality | Classification |
|---|---|---|---|---|---|
| 1 | `CANDLE_CLOSED` | *(none)* | `vacuous: true` | exactly 0 | `VACUOUS` |
| 2 | `CANDLE_CORRECTED` | `corrected_fact` | `by_target`, `event_types: [CANDLE_CLOSED, CANDLE_CORRECTED]` | exactly 1 | `EXTERNAL_NON_STATE_CAUSE` |
| 3 | `BREAK_OF_STRUCTURE_DETECTED` | `broken_swing_confirmed_event_ref` | `payload_field: broken_swing_ref.swing_confirmed_event_ref` | exactly 1 | `EXTERNAL_NON_STATE_CAUSE` |
| 3 | `BREAK_OF_STRUCTURE_DETECTED` | `breaking_candle_refs` | `payload_field: breaking_candle_refs` (array) | min 1 | `EXTERNAL_NON_STATE_CAUSE` |
| 4 | `CHANGE_OF_CHARACTER_DETECTED` | *(same two roles as #3 — identical fields, `structure.md` §4)* | same | same | `EXTERNAL_NON_STATE_CAUSE` |
| 5 | `STRUCTURE_FACT_INVALIDATED` | `invalidated_fact_ref` | `payload_field: invalidated_fact_ref` | exactly 1 | `EXTERNAL_NON_STATE_CAUSE` |
| 5 | `STRUCTURE_FACT_INVALIDATED` | `invalidation_cause_ref` | `by_target`, `discriminated_by: invalidation_cause` → `{swing_invalidated: [SWING_INVALIDATED], breaking_candle_corrected: [CANDLE_CORRECTED], chained_invalidation: [STRUCTURE_FACT_INVALIDATED]}` | exactly 1 | `EXTERNAL_NON_STATE_CAUSE` |
| 6 | `STRUCTURE_RECOMPUTED` | `cascade_invalidations` | `by_target`, `event_types: [STRUCTURE_FACT_INVALIDATED]` | min 1 | `EXTERNAL_NON_STATE_CAUSE` |
| 7 | `REGIME_CLASSIFIED` | `candle_evidence_refs` | `payload_field: candle_evidence_refs` (array) | min 1 | `EXTERNAL_NON_STATE_CAUSE` |
| 7 | `REGIME_CLASSIFIED` | `supersedes_fact_ref` (replacement case) | `payload_field: supersedes_fact_ref` | 0 or 1 | `EXTERNAL_NON_STATE_CAUSE` |
| 8 | `REGIME_FACT_INVALIDATED` | `invalidated_fact_ref` | `payload_field: invalidated_fact_ref` | exactly 1 | `EXTERNAL_NON_STATE_CAUSE` |
| 8 | `REGIME_FACT_INVALIDATED` | `candle_corrected_cause` | `by_target`, `event_types: [CANDLE_CORRECTED]` | exactly 1 | `EXTERNAL_NON_STATE_CAUSE` |
| 9 | `FEATURE_COMPUTED` | `input_fact_refs` | `payload_field: input_fact_refs` (array) | min 1 | `EXTERNAL_NON_STATE_CAUSE` |
| 9 | `FEATURE_COMPUTED` | `supersedes_fact_ref` (replacement case) | `payload_field: supersedes_fact_ref` | 0 or 1 | `EXTERNAL_NON_STATE_CAUSE` |
| 10 | `FEATURE_FACT_INVALIDATED` | `invalidated_fact_ref` | `payload_field: invalidated_fact_ref` | exactly 1 | `EXTERNAL_NON_STATE_CAUSE` |
| 10 | `FEATURE_FACT_INVALIDATED` | `invalidation_cause_ref` | `by_target`, `discriminated_by: invalidation_cause` → `{candle_corrected: [CANDLE_CORRECTED], regime_fact_invalidated: [REGIME_FACT_INVALIDATED], swing_invalidated: [SWING_INVALIDATED], eligible_swing_selection_superseded: [SWING_CONFIRMED]}` | exactly 1 | `EXTERNAL_NON_STATE_CAUSE` |

**Result: all 21 reviewed categories across all 10 event types are mechanically representable** —
19 via `payload_field` (the payload field names above are fresh-read exact matches from
`structure.md`/`regime.md`/`feature.md`, not invented), and 4 via `by_target` (2 fixed, 2
`discriminated_by`). Totals reconcile exactly with the accepted derivation (`20
EXTERNAL_NON_STATE_CAUSE / 1 VACUOUS / 0 STATE_DEPENDENCY / 0 UNRESOLVED`) — every non-VACUOUS role
above is `EXTERNAL_NON_STATE_CAUSE`, matching the 20 total (2+2+2+4+1+2+2+2+5 across event types
2–10 = 20; `by_target` roles for events 2, 5 (second row), 6, 8 (second row), 10 (second row) = 5 of
the 20; `payload_field` roles = 15 of the 20; plus event 1's single `VACUOUS` declaration).

**The `discriminated_by` extension is not optional** — 2 of the 10 real event types
(`STRUCTURE_FACT_INVALIDATED`, `FEATURE_FACT_INVALIDATED`) require it; without it the representation
could not cover all 10 reviewed types without event-specific code, failing requirement 2. This is
carried into §K as an explicit decision-surface item.

## I. Mixed-case capability proof (hypothetical schema test only — NOT proposed for Ride architecture)

Purely to test that the representation can express `STATE_DEPENDENCY` and `EXTERNAL_NON_STATE_CAUSE`
on the *same* event simultaneously (no currently-reviewed real event needs this — §H has zero
`STATE_DEPENDENCY` roles):

```yaml
# HYPOTHETICAL event_type: ACCOUNT_BALANCE_RECONCILED — schema-capability test only.
# Not added to Ride architecture; not a proposed Event Contract; no Domain Contract authored for it.
causal_state_dependency_declaration:
  vacuous: false
  closed: true
  roles:
    - role_id: source_position_ref
      selector:
        payload_field: source_position_ref
      cardinality: {exactly: 1}
      classification: STATE_DEPENDENCY
      apply_time_requirement: >
        HYPOTHETICAL: authoritative application must read source_position_ref's own
        payload.quantity/payload.side to compute the reconciled delta — existence alone is
        insufficient; this cause's stream MUST be in the consuming Input Contract's apply
        set/cursor universe.
    - role_id: reconciliation_run_ref
      selector:
        by_target:
          event_types: [RECONCILIATION_RUN_COMPLETED]
      cardinality: {exactly: 1}
      classification: EXTERNAL_NON_STATE_CAUSE
      apply_time_requirement: >
        HYPOTHETICAL: only existence/audit-trail proof required — the reconciliation run's own
        payload content is never read to apply this effect.
```

**Result: capability confirmed.** The schema expresses both classifications on one event with two
independently-typed selectors (`payload_field` for the state dependency, `by_target` for the external
cause) and independent cardinalities, without any change to the grammar derived in §E. This hypothetical
is not added anywhere else in this repository.

## J. Fail-closed behavior

1. **Unclaimed `causation_refs` entry** (no role's selector matches it) → integrity violation, reject
   / fail-safe per I-6. Never defaulted to any classification.
2. **Multiply-claimed entry** (more than one role's selector matches the same entry) → integrity
   violation, ambiguous, reject.
3. **Role cardinality unsatisfied** (fewer or more refs claimed than the role's declared bound) →
   integrity violation, reject.
4. **`vacuous: true` declared but `envelope.causation_refs` non-empty** → integrity violation, reject.
5. **`payload_field` selector references a path absent from `payload_shape`** — an authoring-time
   defect in the Event Contract itself; Review A must reject the candidate before `Published`, this is
   not a runtime case.
6. **`payload_field`-derived ref absent from `envelope.causation_refs`** (tuple-consistency mismatch
   between the payload's own declared duplicate and the envelope set) → integrity violation, reject.
7. **`by_target` selector's resolved target fails Chapter 8 §8.2.3 tuple consistency** — the
   pre-existing, already-Locked fail-closed rule applies unchanged; this representation adds no
   weakening of it.
8. **`causal_state_dependency_declaration` entirely absent from a Published Event Contract** — a
   malformed/incomplete artifact; Review A must reject before `Published` (governance-time fail
   closed); if one were ever somehow Published, any validator implementing `dependency_authority:
   per_effect_event_contract` must refuse to treat it as authoritative for causal-closure purposes —
   never silently assume zero state dependencies.

No branch above resolves an ambiguous or missing case permissively.

## K. ADR scope / Risk assessment

**Chapter 0 §4b triggers, independently evaluated (not merely hypothesized):**

- *"thay đổi Event Schema"* (Event Schema change) — **fires.** This establishes a new canonical field
  in the Event Contract schema convention every current and future producer module's contracts must
  eventually use to satisfy Chapter 8 §8.2.3 for any Input Contract adopting
  `mode: declared-state-dependencies`.
- *">1 module"* — **fires independently.** Affects every current producer (`market-data-ingestion`,
  `structure-engine`, `raw-regime-engine`, `feature-engine`) and every current/future Input Contract
  validator — the same cross-cutting footprint `ADR-039`/`ADR-040` themselves were already found
  `ADR Required` for.
- *"khó đảo ngược"* (hard to reverse) — **fires independently.** Once a version-artifact using this
  representation is `Published` it is immutable (Chapter 11 §11.3, `ADR-039`); once real persisted
  events pin `event_contract_ref` to it, changing the representation format requires re-authoring
  every already-Published contract's classification under a new format via new versions — a costly
  migration once adopted at scale.

**ADR-045 R2 criteria, independently checked (not merely hypothesized):** *"Platform Invariant or
Event Schema change"* — yes. *"cross-module contract/dependency change with significant blast
radius"* — yes (every producer + every Input Contract validator). *"migration difficult or expensive
to reverse"* — yes (immutable-after-publication artifacts).

**Conclusion: `ADR_REQUIRED`, Risk `R2`** — independently verified against Chapter 0 §4b and ADR-045's
own criteria text, not merely the task's stated hypothesis.

**STOP-condition disposition (all explicitly checked, none triggered):**

- *Existing Approved authority already defines the complete canonical representation* — **not
  found.** Chapter 8 fixes the requirement only; `ADR-039` enumerates the Event Contract's canonical
  fields with no causal-dependency-classification field among them; no other Approved ADR defines one.
- *Representation mechanically derivable with no genuine choice* — **not the case.** Field
  name/placement (§D), selector grammar (`payload_field` vs `by_target`, `discriminated_by`),
  cardinality expression, and the `closed`/`vacuous` fail-closed flags are all genuine authoring
  choices Chapter 8 explicitly declines to fix (*"Classification KHÔNG được nằm trong code
  processor"* fixes a prohibition, not a schema).
- *Selected representation would require external-cause payload reads* — **does not.**
  `payload_field` reads the effect's own payload; `by_target` reads only the target's envelope
  (`event_type`/`contract_id`), never its domain payload (§E, §F step 4b).
  `discriminated_by` reads only the effect's own payload.
- *Depends on event-specific processor code* — **does not.** §F's algorithm is fully schema-driven;
  §H's 10-event mapping required zero event-specific validator branches, only declarative role tables.

**Smallest proposed ADR scope (decision surface only — not authored here):**

1. Canonical field name/placement: `causal_state_dependency_declaration`, a new top-level sibling of
   `ADR-039`'s existing enumerated Event Contract fields.
2. The `vacuous` / `closed` / `roles[].{role_id, selector, cardinality, classification,
   apply_time_requirement, authority}` grammar exactly as derived in §E.
3. The `selector` two-forms (`payload_field`, `by_target`) and the `discriminated_by` extension —
   confirmed necessary by §H, not optional.
4. The fail-closed rules of §J as normative (not merely descriptive).
5. Explicit non-scope: does **not** re-decide any of the 21 already-reviewed classification results
   (`context-upstream-state-dependency-derivation-001.md` v0.4 remains the cited authority for *which*
   category gets *which* classification); does **not** amend `ADR-039`'s or `ADR-040`'s own decisions;
   does **not** publish any Event Contract; does **not** itself remediate the Candle candidates.
6. `depends_on`: whether `ADR-039` is a true normative prerequisite (this field extends `ADR-039`'s
   own enumerated canonical shape) versus precedent-only is a fresh-check question for the ADR's own
   authoring transaction — not pre-decided here.

## L. Smallest follow-on sequence (not executed here)

1. Fresh ChatGPT Review A of this analysis artifact.
2. If `CLEAN`: author the bounded representation ADR candidate (`Draft`) implementing exactly the
   decision surface in §K — no re-decision of any existing classification result.
3. Fresh Review A of that ADR candidate; Risk Classification (expected `R2`, non-final); Product
   Owner decision.
4. Once Approved: remediate the two Candle candidates — fold in `CANDLE-EC-A-MAJ-01` (retention
   correction, §B), migrate to the new canonical `causal_state_dependency_declaration` field
   (`CANDLE-EC-A-MAJ-02`), and make the `exactly: 1` cardinality explicit for `candle-corrected`
   (`CANDLE-EC-A-MIN-01`) — then fresh Review A of the corrected pair.
5. Resume Structure (4) / Regime (2) Event Contract authoring using the validated representation
   pattern directly — no re-derivation of classification results, already reviewed in
   `context-upstream-state-dependency-derivation-001.md` v0.4.
6. Governed publication routing for the eight clean first-version contracts.
7. Feature Event Contract future-version/state-dependency-authority derivation, independent of steps
   4–6.
8. Context Input Contract v0.3 readiness re-review.
9. Only then consider `context-market-input/v1.0` publication.
