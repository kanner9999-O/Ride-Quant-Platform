---
id: event-contract-causal-dependency-representation-001
title: "Event Contract Causal State-Dependency Declaration — Canonical Representation Derivation"
kind: analysis
version: "0.2"
status: Draft
owner: Product Owner
generated_at: "2026-09-28"
---

# EVENT-CONTRACT-CAUSAL-DEPENDENCY-REPRESENTATION-001

**Analysis / architecture-derivation artifact only.** Does not modify any Event Contract, does not
author an ADR, does not modify Chapter 8 or any Constitution file, does not continue
Structure/Regime Event Contract authoring.

**Boundary, fresh-verified before this transaction:** HEAD `28e32a4f5b6451c6114c01c462b290aef29762d8`.
`docs/architecture/event-contracts/candle-closed/v1.0.yaml` matched pinned blob
`3f8d5f9a448c5796880d7a7b7a09d9c95c74c72f` exactly; `candle-corrected/v1.0.yaml` matched pinned blob
`3649e516e4c69d948d8b3a4e4281bae019a7c0b7` exactly; `docs/adr/ADR-039.md`/`docs/adr/ADR-040.md`/
`docs/adr/ADR-047.md` and `docs/project/context-upstream-state-dependency-derivation-001.md` all
re-confirmed byte-identical to their previously-pinned identities — none touched by this transaction.

**Fresh Review A of v0.1:** `REVISION_REQUIRED — 0 Blocker / 2 Major / 2 Minor`. Findings
`EC-CDR-A-MAJ-01` (order-dependent role matching — a `by_target` role's "so-far-unclaimed" evaluation
and cardinality-budget claiming made classification depend on role declaration order, and could hide
a ref that genuinely matches two roles), `EC-CDR-A-MAJ-02` (open/non-exhaustive declaration mode — the
`vacuous`/`closed` two-boolean shape allowed an unauthorized `closed: false` escape hatch with no
governed semantic for intentionally-unclassified causation_refs), `EC-CDR-A-MIN-01` (underspecified
selector grammar — `event_types`/`contract_ids` AND/OR ambiguity, static-vs-discriminated precedence
undefined, discriminant-miss behavior unlocked), `EC-CDR-A-MIN-02` (§H's aggregate category/role
counts were internally contradictory, conflating "reviewed causation category" with "representation
role" as if they were forced to be the same number) — all four addressed/remediated in this v0.2,
**not self-closed** (closure is a fresh Review A re-review determination).

**Preserved unchanged from v0.1** (no fresh authority contradicts any of these; only the
representation *mechanics* are corrected below): Chapter 8 requires machine-readable per-effect Event
Contract causal-dependency authority; processor/event-specific code must not own classification; the
Candle candidates' current freeform nested representation is insufficient (Option A, rejected); state-
dependency classification is distinct from `merge_constraints`; the canonical representation belongs
at top-level Event Contract scope (Option B); explicit per-cause rules are needed for multi-cause/
mixed cases (Option E); missing/ambiguous classification must fail closed; external-cause domain
payload must never be read merely to classify it; the target architecture decision remains
`ADR_REQUIRED`, Risk `R2`; `ADR-040` retention semantics remain `APPROVED`/`SATISFIED` at
architecture-semantics level for Class G, concrete past-horizon archival mechanism `DEFERRED`, not
the current blocker. **This correction transaction's own Risk is `R1`, ADR Scope
`ADR_NOT_REQUIRED`** — a bounded analysis-artifact correction, not itself the architecture decision.

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
- **Approved `ADR-040`** — Class G retention/archive semantics for Event Contract version-artifacts:
  canonical path remains resolvable at current `HEAD` throughout the committed retention horizon; git
  history is content-identity/audit evidence only, never a fallback resolver; concrete past-horizon
  archival **mechanism** remains deferred. Consequences (verbatim, cited not re-derived):
  *"`ADR-039`'s own Consequences item (0) — establishing that an authoritative retention/archive
  policy exists before any Event Contract version-artifact becomes a usable `event_contract_ref`
  target — is now satisfied at the architecture-semantics level for Class G by this ADR (Event
  Contract version-artifacts are Class G)."* This is §B's controlling text.
- **`docs/project/context-upstream-state-dependency-derivation-001.md` v0.4** (Review A validated,
  `CLEAN — 0/0/1`) — the accepted classification result for all 21 causation-ref categories across the
  10 Context-upstream event types: `20 EXTERNAL_NON_STATE_CAUSE / 1 VACUOUS / 0 STATE_DEPENDENCY / 0
  UNRESOLVED`. Used here strictly as **test-vector data** — not re-derived, not re-classified.
- **Candle candidates** (`candle-closed/v1.0.yaml`, `candle-corrected/v1.0.yaml`), read-only — the
  locally-invented `payload_semantics_and_invariants.causation_ref_state_dependency_classification`
  nesting is the artifact under scrutiny in §D Option A, not modified here.

## B. Finding 1 — retention authority correction (`CANDLE-EC-A-MAJ-01`, unchanged this correction)

The Candle candidates' own header comments state that even once Published, they must not be treated
as usable `event_contract_ref` targets *"until the separately-governed platform retention/archive
policy's concrete past-horizon archival mechanism is established."* Fresh-read Approved `ADR-040`
shows this framing is **stale**: `ADR-040`'s own Consequences explicitly state the `ADR-039`
prerequisite is *"now satisfied at the architecture-semantics level for Class G."*

**Corrected state (unchanged from v0.1):**

```text
ADR-040 retention semantics:      APPROVED / SATISFIED at architecture-semantics level for Class G
Concrete past-horizon archival:   DEFERRED (ADR-040 does not invent the mechanism)
Current blocker to an otherwise-governed
Published Event Contract becoming
an event_contract_ref target:     NO — retention/archive policy absence is NOT the blocker
```

This does **not** claim archival tooling exists, does **not** claim any Event Contract is now
Published or runtime-usable, and does **not** modify `ADR-040`/`ADR-039`. The Candle candidate files
themselves remain unedited (`CANDLE-EC-A-MAJ-01` remains recorded, not remediated).

The genuine remaining blocker to Event Contract publication/reference-usability is unrelated to
retention: the candidates are `Draft`, unreviewed, unpublished, and the machine-readable causal
state-dependency representation they must eventually use is not yet governed — the subject of this
correction.

## C. Runtime-consumer requirements

The consumer of this representation is any current or future **Input Contract** that declares
`causal_closure_policy: {mode: declared-state-dependencies, dependency_authority:
per_effect_event_contract}` (Chapter 8 §8.2.3) — today, no Input Contract has reached `Published`
using this mode (Context Input Contract v0.3 remains `Draft`/`NOT PUBLISHED`), but the mechanism must
be implementable **once**, generically, by a shared validator/library used across every current and
future producer module (`market-data-ingestion`, `structure-engine`, `raw-regime-engine`,
`feature-engine`, and any later module) and every current and future Input Contract instance — never
reimplemented per event type inside processor code. Concretely, the validator must be able to answer,
for one effect event and its pinned `event_contract_ref`:

1. Is this event root/vacuous (no causal-closure obligation)?
2. For each entry in `envelope.causation_refs`, is it `STATE_DEPENDENCY` (must be resolved within
   this Input Contract's apply set/cursor universe, participates in frontier completeness) or
   `EXTERNAL_NON_STATE_CAUSE` (existence/commit proof only, excluded from apply set/frontier, payload
   never read)?
3. Is every entry accounted for, deterministically, **independent of the order roles happen to be
   declared in the Event Contract** (`EC-CDR-A-MAJ-01` — a validator re-reading the same artifact must
   reach the same result no matter what order it iterates the `roles` list)?

## D. Option comparison

### Option A — current freeform/nested semantic block (as authored in the Candle candidates)

```yaml
payload_semantics_and_invariants:
  causation_ref_state_dependency_classification:
    classification: VACUOUS   # or: categories: {<ad hoc label>: {classification: ..., ...}}
```

**Assessment: NOT machine-canonical.** Three independent defects: (1) `payload_semantics_and_invariants`
is a narrative/prose field by `ADR-039`'s own illustrative shape and actual use — no authority defines
a strict machine schema for anything nested inside it; (2) ad hoc category labels (e.g.
`corrected_fact`) have no formal linkage to a specific `envelope.causation_refs` array entry; (3) no
cardinality grammar, no selector grammar, no fail-closed completeness rule. **Rejected** as the
canonical representation — useful human annotation only.

### Option B — new top-level Event Contract field

A dedicated canonical field, sibling to `event_class`/`allowed_streams`/`merge_constraints`/
`payload_shape`/`payload_semantics_and_invariants`/`compatibility_commitment` in `ADR-039`'s own
enumerated shape. **Assessment: correct placement** — self-contained, versioned with the artifact,
immutable at publication, trivially parseable by path without prose search. **Recommended** — see §E.

### Option C — structured subfield of `merge_constraints`

**Assessment: rejected — conflates two distinct Chapter-8 concepts.** `merge_constraints.
prerequisite_policy` (§8.3.4) governs **ordering**; state-dependency classification (§8.2.3) governs
**scope/visibility**. A root event like `candle-closed` already has a truthfully-empty
`merge_constraints: {}`; forcing classification content into that same field would corrupt the "no
prerequisite" signal or force two independently-versioned concepts to share one field's schema
evolution. **Rejected.**

### Option D — declare only state-dependency selectors, default everything else to external

**Assessment: rejected in its literal (silent-default) form — fails fail-closed.** A future producer
emitting a genuinely new, undeclared `causation_ref` role would be silently treated as
`EXTERNAL_NON_STATE_CAUSE` — fail-**open**, a correctness gap. Its minimalism instinct — 20 of 21
reviewed categories are `EXTERNAL_NON_STATE_CAUSE`, 0 are `STATE_DEPENDENCY` — is preserved without
the unsafe default: declaring an `EXTERNAL_NON_STATE_CAUSE` role costs the same one entry as a
`STATE_DEPENDENCY` role in the recommended representation (§E). **Rejected as specified; minimalism
absorbed into B/E without the unsafe default.**

### Option E — explicit per-cause rule table

```text
role/category | selector | cardinality | classification
```

**Assessment: necessary, not over-specified.** Proven necessary by real test-vector data (§H):
multiple reviewed event types carry more than one causation-ref category simultaneously, each
requiring its own selector/cardinality. **B (placement) + E (internal shape), combined, is
recommended.** No better option was identified.

## E. Proposed canonical representation (corrected, `EC-CDR-A-MAJ-02` / `EC-CDR-A-MIN-01`)

New top-level Event Contract field: **`causal_state_dependency_declaration`**, a **closed sum type**
over exactly two modes. `mode` is **required**, has **no default**, and no value other than the two
below is valid.

### E.1 `mode: vacuous`

```yaml
causal_state_dependency_declaration:
  mode: vacuous
```

**Semantics:** `envelope.causation_refs` MUST be canonically `[]` for every instance of this
`event_type`. The `roles` field is **PROHIBITED** under this mode — its mere presence is a malformed
declaration (§J-4). A non-empty `causation_refs` on an event whose Event Contract declares
`mode: vacuous` is an integrity violation (§J-3).

### E.2 `mode: exhaustive`

```yaml
causal_state_dependency_declaration:
  mode: exhaustive
  roles:
    - role_id: <string, unique within this artifact, human-legible label>
      selector:
        # A tagged union — the `kind` field selects the form; exactly one form, never both/neither.
        kind: payload_field
        path: <dot-path into payload_shape, e.g. "invalidated_fact_ref" or
          "broken_swing_ref.swing_confirmed_event_ref">
      # OR:
      selector:
        kind: by_target
        match:                          # static form
          event_types: [<UPPER_SNAKE event_type values>]      # at least one of match's two keys
          contract_ids: [<contract_id values>]                 # required; if BOTH present, AND
      # OR:
      selector:
        kind: by_target
        discriminant:                   # discriminated form — mutually exclusive with `match`
          payload_field: <dot-path into THIS EFFECT event's OWN payload — never the target's>
          cases:
            <discriminant value>:
              event_types: [<...>]        # same "at least one of the two, AND if both" rule per case
              contract_ids: [<...>]
      cardinality: {exactly: <int>}                    # or {min: <int>, max: <int or null>}
      classification: STATE_DEPENDENCY | EXTERNAL_NON_STATE_CAUSE   # VACUOUS is not a role value —
                                                                     # vacuity belongs to mode: vacuous
                                                                     # only (fixes EC-CDR-A-MAJ-02)
      apply_time_requirement: >
        Required for every role — free-text rationale citing exactly what authoritative application
        does and does not need from this cause, consistent with Chapter 8 §8.2.3's apply-time test.
      authority: >
        Citation to the already-reviewed state-dependency derivation category this role
        transcribes (never re-derived inline).
```

**Selector tagged-union rules (fixes `EC-CDR-A-MIN-01`):**

- A role's `selector` is **exactly one** of `kind: payload_field` or `kind: by_target` — structurally
  enforced by the `kind` tag, never both, never neither.
- `payload_field` — `path` resolves directly in the effect event's **own** payload, at the type
  already fixed by `payload_shape` (`event_record_ref` or an array of it).
- `by_target.match` (static form) — MUST provide **at least one** of `event_types`/`contract_ids`. If
  **both** are present, they are **conjunctive** (target must satisfy BOTH allow-sets). Target
  **domain payload** is never read — only the target's own envelope `event_type` and/or
  `event_contract_ref.contract_id`, obtained via the tuple-consistency existence check Chapter 8
  §8.2.3 already mandates for every causation_ref.
- `by_target.discriminant` (discriminated form) — **mutually exclusive** with `match` on the same
  role. `payload_field` under `discriminant` refers **only** to the EFFECT event's own payload, never
  the target's. Each entry in `cases` follows the identical `match`-style rule (at least one of
  `event_types`/`contract_ids`; AND if both present). There is **no implicit/default case** — a
  discriminant value with no matching `cases` entry fails closed (§J-15); a missing/unresolvable
  discriminant field on the effect's own payload fails closed (§J-14). A case is not required to
  specify both identifiers when one is already sufficient under current authority (e.g. `event_types`
  alone) — but when both are authored on the same case, the AND semantics above apply deterministically.
- Target domain payload is **never** read by any selector form, in any case — the sole permitted
  target inspection is the target's own envelope/identity, exactly the surface Chapter 8 §8.2.3's
  tuple-consistency rule already requires resolving for every causation_ref.

**Separation from `merge_constraints`:** this field and `merge_constraints` are independent,
co-existing top-level fields. A role's classification here never implies, and is never implied by,
`merge_constraints.prerequisite_policy`.

## F. Generic validation algorithm — order-independent, two-phase (corrected, `EC-CDR-A-MAJ-01`)

Given one effect event record and its pinned `event_contract_ref`:

### Phase 0 — mode dispatch

1. Resolve `event_contract_ref` to its Event Contract version-artifact (`ADR-039` direct-path
   resolution).
2. Read `causal_state_dependency_declaration`. Absent entirely → **fail closed** (§J-1). `mode`
   absent or not one of `{vacuous, exhaustive}` → **fail closed** (§J-2).
3. If `mode: vacuous`: `roles` present at all → **fail closed** (§J-4). Otherwise assert
   `envelope.causation_refs == []`; mismatch → **fail closed** (§J-3). Stop — no further processing.
4. If `mode: exhaustive`: `roles` absent, empty, or structurally malformed (a role missing
   `role_id`/`selector`/`cardinality`/`classification`) → **fail closed** (§J-5). Otherwise proceed to
   Phase 1.

### Phase 1 — independent match-set computation (order-independent)

For **every** declared role `r`, compute its complete match set `M(r)` **against the full, original,
unmutated `envelope.causation_refs` set** — never against a "remaining/unclaimed" subset, never
stopping early once a cardinality budget is nominally reached. Every role is evaluated exactly once,
independently of every other role and of its own position in the `roles` list:

- **`payload_field` role:** resolve `path` in the effect's **own** payload. The resolved value(s) —
  singular, or every element if the path is array-typed — form this role's candidate set. Each
  candidate MUST also literally occur in `envelope.causation_refs` (tuple-consistency cross-check);
  absent → **fail closed** (§J-11). `M(r)` = exactly the `envelope.causation_refs` entries that are
  tuple-equal to a resolved payload candidate. A path that resolves to nothing, for a role whose own
  `cardinality` permits zero (e.g. `{min: 0, max: 1}`), is a legitimate empty `M(r)` — see §J-10.
- **`by_target` role, static (`match`):** for **every** entry `c` in the complete
  `envelope.causation_refs` set (not a remaining subset), resolve `c`'s target's own envelope via the
  Chapter 8 §8.2.3 tuple-consistency existence check, and test it against `match`'s allow-set(s)
  (AND, if both `event_types` and `contract_ids` are declared). `M(r)` = every `c` that satisfies the
  test. A `c` that resolves but does not satisfy the conjunction is simply excluded from `M(r)` — not
  itself a failure (§J-16); it may still belong to another role, or remain unclaimed (§J-6, Phase 2).
- **`by_target` role, discriminated (`discriminant`):** read `discriminant.payload_field` once, in the
  effect's **own** payload. Missing/unresolvable → **fail closed** (§J-14). Look up the resolved value
  in `discriminant.cases`; absent → **fail closed** (§J-15). Otherwise apply the matched case's
  allow-set(s) (same AND rule) against **every** entry `c` in the complete `envelope.causation_refs`
  set, exactly as the static form does, to build `M(r)`.

No role's evaluation depends on, mutates, or is affected by any other role's evaluation or by
declaration order — `M(r1) ∪ M(r2) ∪ ...` and each individual `M(r)` are fully determined by the
Event Contract's own declared schema plus the effect event's own payload/envelope and each target's
own envelope, computed independently.

### Phase 2 — validation

1. For every role `r`: validate its declared `cardinality` against `|M(r)|`. Unsatisfied → **fail
   closed** (§J-8).
2. For every entry `c` in `envelope.causation_refs`, compute `matches(c) = { r : c ∈ M(r) }`.
3. Require `|matches(c)| = 1` for **every** `c`:
   - `|matches(c)| = 0` → **fail closed** (§J-6) — unclaimed, never defaulted.
   - `|matches(c)| > 1` → **fail closed** (§J-7) — ambiguous overlap, **even if one of the
     overlapping roles is optional** (e.g. `{min: 0, max: 1}`); an optional role's cardinality
     permitting zero does **not** make selector overlap with another role legal — the ref still has
     more than one match and validation still fails.
4. Once every `c` has exactly one match, its classification is that role's declared `classification`.
5. For every `c` classified `STATE_DEPENDENCY`: its target's payload/state MUST be within the
   consuming Input Contract's apply set/cursor universe (Chapter 8 §8.2.3 in-scope rule).
6. For every `c` classified `EXTERNAL_NON_STATE_CAUSE`: only existence/commit proof is required
   (already satisfied by Phase 1's own tuple-consistency check); excluded from the merged apply
   set/frontier; its domain payload is never read to reach or use this classification.

**Role declaration order has zero semantic effect anywhere in this algorithm** — Phase 1 evaluates
every role against the complete original set; Phase 2's `matches(c)` computation is a set-membership
test, not a sequential claim process.

No step above references a specific `event_type`, `contract_id`, or Domain Contract by name — every
decision is driven entirely by the pinned Event Contract's own declared schema, using only the
effect's own payload and each target's own envelope/identity.

## G. Candle mapping (corrected grammar; illustrative, not applied to the files in this WP)

```yaml
# candle-closed/v1.0
causal_state_dependency_declaration:
  mode: vacuous
```

```yaml
# candle-corrected/v1.0
causal_state_dependency_declaration:
  mode: exhaustive
  roles:
    - role_id: corrected_fact
      selector:
        kind: by_target
        match:
          event_types: [CANDLE_CLOSED, CANDLE_CORRECTED]
          contract_ids: [candle-closed, candle-corrected]
      cardinality: {exactly: 1}
      classification: EXTERNAL_NON_STATE_CAUSE
      apply_time_requirement: >
        Authoritative application does not require re-reading the corrected predecessor's domain
        payload/state; the effect carries the complete replacement OHLCV/state itself; the
        predecessor reference is required only for identity/existence/lineage/causal precedence.
      authority: >
        docs/project/context-upstream-state-dependency-derivation-001.md v0.4 §2.2.
```

`candle-closed` has no named payload field and no target to select against — `mode: vacuous` is the
entire declaration, matching `causation_refs: []` (root event) exactly. `candle-corrected` has no
payload-field duplicate of its causal reference (`candle.md` §5 places it envelope-only), so it is the
canonical worked example of the `by_target` static-`match` form. The `cardinality: {exactly: 1}` above
mechanically captures `CANDLE-EC-A-MIN-01`'s originally-requested cardinality-explicitness concern —
**the Candle candidate files themselves are not modified in this WP.**

## H. Traceability matrix — reviewed category → representation rule (corrected, `EC-CDR-A-MIN-02`)

**Correction rationale:** v0.1 attempted to force "19 `payload_field` + 4 `by_target`" and later "15 +
5" to both describe the same 21-category total, treating *reviewed causation category* and
*representation role* as if they were necessarily the same count. They are not: a single
**discriminated** role can encode several mutually-exclusive reviewed categories (exactly one
discriminant `case` fires per concrete event instance). The fix is a many-to-one **traceability
matrix** — every reviewed category maps to exactly one representation rule/branch — reported
separately from role/branch counts, never force-reconciled against them.

| Reviewed `event_type` | Reviewed cause category (`context-upstream-state-dependency-derivation-001.md` v0.4) | Accepted classification | Representation `role_id` | Selector kind | Discriminant case (if applicable) |
|---|---|---|---|---|---|
| `CANDLE_CLOSED` | *(root — no causation-ref category exists)* | `VACUOUS` | *(none — `mode: vacuous`)* | — | — |
| `CANDLE_CORRECTED` | corrected-fact ref (§2.2) | `EXTERNAL_NON_STATE_CAUSE` | `corrected_fact` | `by_target` (static `match`) | — |
| `BREAK_OF_STRUCTURE_DETECTED` | `broken_swing_ref.swing_confirmed_event_ref` (§2.3) | `EXTERNAL_NON_STATE_CAUSE` | `broken_swing_confirmed_event_ref` | `payload_field` | — |
| `BREAK_OF_STRUCTURE_DETECTED` | `breaking_candle_refs` (§2.3) | `EXTERNAL_NON_STATE_CAUSE` | `breaking_candle_refs` | `payload_field` | — |
| `CHANGE_OF_CHARACTER_DETECTED` | `broken_swing_ref.swing_confirmed_event_ref` (§2.3/§2.4, shared reasoning) | `EXTERNAL_NON_STATE_CAUSE` | `broken_swing_confirmed_event_ref` | `payload_field` | — |
| `CHANGE_OF_CHARACTER_DETECTED` | `breaking_candle_refs` (§2.3/§2.4, shared reasoning) | `EXTERNAL_NON_STATE_CAUSE` | `breaking_candle_refs` | `payload_field` | — |
| `STRUCTURE_FACT_INVALIDATED` | `invalidated_fact_ref` (§2.5) | `EXTERNAL_NON_STATE_CAUSE` | `invalidated_fact_ref` | `payload_field` | — |
| `STRUCTURE_FACT_INVALIDATED` | cause (a) `swing_invalidated` (§2.5) | `EXTERNAL_NON_STATE_CAUSE` | `invalidation_cause_ref` | `by_target` (discriminated) | `swing_invalidated` → `[SWING_INVALIDATED]` |
| `STRUCTURE_FACT_INVALIDATED` | cause (b) `breaking_candle_corrected` (§2.5) | `EXTERNAL_NON_STATE_CAUSE` | `invalidation_cause_ref` | `by_target` (discriminated) | `breaking_candle_corrected` → `[CANDLE_CORRECTED]` |
| `STRUCTURE_FACT_INVALIDATED` | cause (c) `chained_invalidation` (§2.5) | `EXTERNAL_NON_STATE_CAUSE` | `invalidation_cause_ref` | `by_target` (discriminated) | `chained_invalidation` → `[STRUCTURE_FACT_INVALIDATED]` |
| `STRUCTURE_RECOMPUTED` | full `StructureFactInvalidated` cascade set (§2.6) | `EXTERNAL_NON_STATE_CAUSE` | `cascade_invalidations` | `by_target` (static `match`) | — |
| `REGIME_CLASSIFIED` | `candle_evidence_refs` (§2.7) | `EXTERNAL_NON_STATE_CAUSE` | `candle_evidence_refs` | `payload_field` | — |
| `REGIME_CLASSIFIED` | `supersedes_fact_ref`, replacement case (§2.7) | `EXTERNAL_NON_STATE_CAUSE` | `supersedes_fact_ref` | `payload_field` | — |
| `REGIME_FACT_INVALIDATED` | `invalidated_fact_ref` (§2.8) | `EXTERNAL_NON_STATE_CAUSE` | `invalidated_fact_ref` | `payload_field` | — |
| `REGIME_FACT_INVALIDATED` | `CandleCorrected` direct cause (§2.8) | `EXTERNAL_NON_STATE_CAUSE` | `candle_corrected_cause` | `by_target` (static `match`) | — |
| `FEATURE_COMPUTED` | `input_fact_refs` (§2.9) | `EXTERNAL_NON_STATE_CAUSE` | `input_fact_refs` | `payload_field` | — |
| `FEATURE_COMPUTED` | `supersedes_fact_ref`, replacement case (§2.9) | `EXTERNAL_NON_STATE_CAUSE` | `supersedes_fact_ref` | `payload_field` | — |
| `FEATURE_FACT_INVALIDATED` | `invalidated_fact_ref` (§2.10) | `EXTERNAL_NON_STATE_CAUSE` | `invalidated_fact_ref` | `payload_field` | — |
| `FEATURE_FACT_INVALIDATED` | cause (a) `candle_corrected` (§2.10) | `EXTERNAL_NON_STATE_CAUSE` | `invalidation_cause_ref` | `by_target` (discriminated) | `candle_corrected` → `[CANDLE_CORRECTED]` |
| `FEATURE_FACT_INVALIDATED` | cause (b) `regime_fact_invalidated` (§2.10) | `EXTERNAL_NON_STATE_CAUSE` | `invalidation_cause_ref` | `by_target` (discriminated) | `regime_fact_invalidated` → `[REGIME_FACT_INVALIDATED]` |
| `FEATURE_FACT_INVALIDATED` | cause (c) `swing_invalidated` (§2.10) | `EXTERNAL_NON_STATE_CAUSE` | `invalidation_cause_ref` | `by_target` (discriminated) | `swing_invalidated` → `[SWING_INVALIDATED]` |
| `FEATURE_FACT_INVALIDATED` | cause (d) `eligible_swing_selection_superseded` (§2.10) | `EXTERNAL_NON_STATE_CAUSE` | `invalidation_cause_ref` | `by_target` (discriminated) | `eligible_swing_selection_superseded` → `[SWING_CONFIRMED]` |

**Result: every reviewed category maps to exactly one representation rule/branch, with zero
event-specific validator code** — `payload_field` roles are resolved purely from the effect's own
`payload_shape`; `by_target` roles (static and discriminated) are resolved purely from target
envelope identity and, where discriminated, the effect's own payload — no target domain payload is
ever read (fixes the residual §H concern this correction closes alongside `EC-CDR-A-MIN-02`). No
reviewed category required event-specific code to represent — the all-10-event proof did **not**
trigger the STOP condition for representability.

### H.1 Separately-reported counts — A / B / C, never mixed (fixes `EC-CDR-A-MIN-02`)

**A. Accepted derivation classification totals — copied unaltered from
`context-upstream-state-dependency-derivation-001.md` v0.4 §3, not re-derived, not recomputed here:**

```text
20 EXTERNAL_NON_STATE_CAUSE
1 VACUOUS
0 STATE_DEPENDENCY
0 UNRESOLVED
```

**B. Representation role-declaration count — counted independently from the representation side
(§H's matrix, `role_id` column, de-duplicated per Event Contract):**

```text
CANDLE_CLOSED:                 0 roles (mode: vacuous)
CANDLE_CORRECTED:               1 role
BREAK_OF_STRUCTURE_DETECTED:    2 roles
CHANGE_OF_CHARACTER_DETECTED:   2 roles
STRUCTURE_FACT_INVALIDATED:     2 roles
STRUCTURE_RECOMPUTED:           1 role
REGIME_CLASSIFIED:              2 roles
REGIME_FACT_INVALIDATED:        2 roles
FEATURE_COMPUTED:               2 roles
FEATURE_FACT_INVALIDATED:       2 roles
-----------------------------------------
Total role declarations across all 10 Event Contracts: 16
  (11 payload_field roles + 5 by_target roles)
```

**C. Selector-branch (discriminant `case`) count — counted independently, only where applicable:**

```text
STRUCTURE_FACT_INVALIDATED.invalidation_cause_ref:  3 cases
FEATURE_FACT_INVALIDATED.invalidation_cause_ref:    4 cases
-----------------------------------------------------------
Total discriminant cases across 2 discriminated roles: 7
```

**A, B, and C are three independently-true, non-comparable figures — deliberately not summed or
reconciled against each other.** A is v0.4's own classification-authority tally (unaltered). B is how
many role declarations the corrected representation actually needs (fewer than A's 21 categories,
because two discriminated roles each absorb several reviewed categories as `cases`, exactly what
"many-to-one" in the traceability matrix above means). C further decomposes two of B's 16 roles into
their own internal branches. **This is the corrected discipline itself** — v0.1's `EC-CDR-A-MIN-02`
defect was attempting to force A and B into one shared sum; this version reports each on its own
terms, with the matrix as the actual proof linking them.

## I. Mixed-case capability proof (corrected grammar; hypothetical schema test only — NOT proposed for Ride architecture)

Purely to test that the representation can express `STATE_DEPENDENCY` and `EXTERNAL_NON_STATE_CAUSE`
on the *same* event simultaneously (no currently-reviewed real event needs this — §H has zero
`STATE_DEPENDENCY` roles):

```yaml
# HYPOTHETICAL event_type: ACCOUNT_BALANCE_RECONCILED — schema-capability test only.
# Not added to Ride architecture; not a proposed Event Contract; no Domain Contract authored for it.
causal_state_dependency_declaration:
  mode: exhaustive
  roles:
    - role_id: source_position_ref
      selector:
        kind: payload_field
        path: source_position_ref
      cardinality: {exactly: 1}
      classification: STATE_DEPENDENCY
      apply_time_requirement: >
        HYPOTHETICAL: authoritative application must read source_position_ref's own
        payload.quantity/payload.side to compute the reconciled delta — existence alone is
        insufficient; this cause's stream MUST be in the consuming Input Contract's apply
        set/cursor universe.
      authority: >
        HYPOTHETICAL — no real Event Contract; schema-capability test only.
    - role_id: reconciliation_run_ref
      selector:
        kind: by_target
        match:
          event_types: [RECONCILIATION_RUN_COMPLETED]
      cardinality: {exactly: 1}
      classification: EXTERNAL_NON_STATE_CAUSE
      apply_time_requirement: >
        HYPOTHETICAL: only existence/audit-trail proof required — the reconciliation run's own
        payload content is never read to apply this effect.
      authority: >
        HYPOTHETICAL — no real Event Contract; schema-capability test only.
```

**Result: capability confirmed under the corrected grammar too.** Two independently-typed selectors
(`payload_field` for the state dependency, `by_target` static `match` for the external cause), each
with its own cardinality, evaluated per the order-independent two-phase algorithm of §F exactly as
any other role would be — no grammar change was needed to support the mixed case; `mode: exhaustive`
already accommodates an arbitrary mix of `STATE_DEPENDENCY`/`EXTERNAL_NON_STATE_CAUSE` roles per
Event Contract. This hypothetical is not added anywhere else in this repository.

## J. Fail-closed behavior (corrected/expanded, `EC-CDR-A-MAJ-01`/`EC-CDR-A-MIN-01`)

No branch below resolves an ambiguous or missing case permissively — there is no fail-open/default
branch anywhere in this table.

1. **`causal_state_dependency_declaration` entirely absent** from a Published Event Contract — a
   malformed/incomplete artifact; Review A must reject before `Published` (governance-time fail
   closed); if one were ever somehow Published, any validator implementing `dependency_authority:
   per_effect_event_contract` must refuse to treat it as authoritative — never silently assume zero
   state dependencies.
2. **Invalid `mode`** (absent, or a value other than `vacuous`/`exhaustive`) → integrity violation,
   reject.
3. **`mode: vacuous` declared but `envelope.causation_refs` non-empty** → integrity violation, reject.
4. **`mode: vacuous` declared with `roles` present at all** → malformed declaration, reject
   (authoring-time defect; Review A must reject before `Published`).
5. **`mode: exhaustive` with `roles` missing, empty, or structurally malformed** (a role missing
   `role_id`/`selector`/`cardinality`/`classification`) → malformed declaration, reject
   (authoring-time defect).
6. **Zero role matches for a `causation_refs` entry** (`|matches(c)| = 0`) → integrity violation,
   unclaimed, reject. Never defaulted to any classification.
7. **More than one role matches for a `causation_refs` entry** (`|matches(c)| > 1`) → integrity
   violation, ambiguous, reject — **including** when one of the overlapping roles is itself optional
   (e.g. `{min: 0, max: 1}`); optionality of one role never legalizes overlap with another.
8. **Role cardinality unsatisfied** (`|M(r)|` outside the role's declared `min`/`max`/`exactly`) →
   integrity violation, reject.
9. **Malformed `payload_field` path** (references a path absent from `payload_shape`) —
   authoring-time defect; Review A must reject before `Published`, not a runtime case.
10. **Runtime optional payload path/cardinality — NOT a failure when correctly declared:** a
    `payload_field` role whose target path is declared optional in `payload_shape` (e.g.
    `supersedes_fact_ref`, `required: false`) legitimately resolving to zero refs for a given event
    instance is expected, valid behavior when the role's own `cardinality` permits zero (e.g.
    `{min: 0, max: 1}`) — distinguished explicitly from item 8, which fires only when the *actual*
    count falls outside the *declared* bound.
11. **`payload_field`-derived ref absent from `envelope.causation_refs`** (tuple-consistency mismatch
    between the payload's own declared duplicate and the envelope set) → integrity violation, reject.
12. **`by_target` selector's resolved target fails Chapter 8 §8.2.3 tuple consistency** — the
    pre-existing, already-Locked fail-closed rule applies unchanged; this representation adds no
    weakening of it.
13. **Static `by_target.match` malformed** (neither `event_types` nor `contract_ids` present) —
    authoring-time defect; Review A must reject before `Published`.
14. **Discriminant field missing/unresolvable** (`discriminant.payload_field` absent or unresolvable
    on the effect's own payload) → integrity violation, reject.
15. **Discriminant value unknown/unhandled** (resolved value has no matching entry in `cases`) →
    integrity violation, reject — no implicit/default case.
16. **Target satisfies only part of a declared `event_types`/`contract_ids` conjunction** — this is
    **not itself a failure**: the target is simply excluded from that role's `M(r)` (§F Phase 1); it
    may still belong to another role, or (if it belongs to none) trigger item 6 above at Phase 2.
    Recorded here only to distinguish normal non-match from an integrity violation.

## K. ADR scope / Risk assessment

**Target canonical-representation decision — preserved unchanged, independently re-verified against
Chapter 0 §4b and ADR-045's own R2 criteria, not merely the task's stated hypothesis:**

- *"thay đổi Event Schema"* (Event Schema change) — fires: this establishes a new canonical field in
  the Event Contract schema convention every current and future producer module's contracts must
  eventually use to satisfy Chapter 8 §8.2.3.
- *">1 module"* — fires independently: affects every current producer (`market-data-ingestion`,
  `structure-engine`, `raw-regime-engine`, `feature-engine`) and every current/future Input Contract
  validator.
- *"khó đảo ngược"* (hard to reverse) — fires independently: once a version-artifact using this
  representation is `Published` it is immutable (Chapter 11 §11.3, `ADR-039`); changing the
  representation format afterward requires re-authoring every already-Published contract's
  classification under a new format via new versions.
- ADR-045 R2 criteria — *"Platform Invariant or Event Schema change"* yes; *"cross-module
  contract/dependency change with significant blast radius"* yes; *"migration difficult or expensive
  to reverse"* yes.

```text
Target canonical representation decision:
ADR_REQUIRED
Risk R2
```

**This correction transaction itself — distinguished explicitly, never conflated with the target
decision above:**

```text
Correction transaction (this WP):
Risk R1 — bounded analysis-artifact correction, single document, no external contract/behavior
change, reversible.
ADR_NOT_REQUIRED — corrects representation mechanics of an unpublished analysis artifact; does
not itself decide, publish, or bind any Event Contract, Domain Contract, or Constitution content.
```

**STOP-condition disposition (all explicitly re-checked under the corrected grammar, none
triggered):**

- *Existing Approved authority already defines the complete canonical representation* — not found
  (unchanged from v0.1's finding; Chapter 8 fixes the requirement only, `ADR-039` names no such
  field).
- *Representation mechanically derivable with no genuine choice* — not the case; field
  name/placement, the `mode` sum type, selector tagged-union shape, and the two-phase order-
  independent algorithm are all genuine authoring choices Chapter 8 declines to fix.
- *Selected representation would require external-cause payload reads* — does not; confirmed again
  under the corrected grammar (§E, §F Phase 1) — `by_target` (static and discriminated) reads only
  target envelope identity, never target domain payload.
- *Depends on event-specific processor code* — does not; §F's algorithm and §H's traceability matrix
  required zero event-specific validator branches under the corrected grammar either.

**Smallest proposed ADR scope (decision surface only — not authored here):**

1. Canonical field name/placement: `causal_state_dependency_declaration`, a new top-level sibling of
   `ADR-039`'s existing enumerated Event Contract fields.
2. The `mode: vacuous | exhaustive` closed sum type exactly as derived in §E — no `open`/`partial`
   third mode, no future-extension escape hatch without its own separate authority.
3. The `roles[].{role_id, selector, cardinality, classification, apply_time_requirement, authority}`
   grammar, the `STATE_DEPENDENCY | EXTERNAL_NON_STATE_CAUSE` role-classification enum (`VACUOUS`
   excluded, belongs to `mode: vacuous` only), and the `selector` tagged union (`payload_field` /
   `by_target` with static `match` or `discriminant` forms) exactly as derived in §E — confirmed
   necessary, not optional, by §H's traceability matrix (2 of 10 event types require the
   `discriminant` form).
4. The order-independent two-phase validation algorithm of §F as normative (not merely descriptive) —
   Phase 1 independent match-set computation, Phase 2 exactly-one-match validation.
5. The fail-closed rules of §J as normative, including the explicit non-legalization of selector
   overlap by role optionality (§J-7).
6. Explicit non-scope: does **not** re-decide any of the 21 already-reviewed classification results
   (`context-upstream-state-dependency-derivation-001.md` v0.4 remains the cited authority for *which*
   category gets *which* classification); does **not** amend `ADR-039`'s or `ADR-040`'s own decisions;
   does **not** publish any Event Contract; does **not** itself remediate the Candle candidates.
7. `depends_on` — **kept as a fresh-check item for the ADR's own authoring transaction, not
   pre-decided here.** The eventual ADR must determine whether it normatively depends on `ADR-039`
   (as an extension of `ADR-039`'s own enumerated Event Contract shape) or can stand independently
   under Chapter 8 directly — this correction does **not** arbitrarily supersede `ADR-039`, and makes
   no whole-file-supersession decision.

## L. Smallest follow-on sequence (not executed here)

1. Fresh ChatGPT Review A of this corrected representation derivation (v0.2).
2. If `CLEAN`: author the bounded representation ADR candidate (`Draft`) implementing exactly the
   decision surface in §K — no re-decision of any existing classification result; fresh-check the
   `ADR-039` `depends_on` question at that time.
3. Fresh Review A of that ADR candidate; Risk Classification (expected `R2`, non-final); Product
   Owner decision.
4. Once Approved: remediate the two Candle candidates — fold in `CANDLE-EC-A-MAJ-01` (retention
   correction, §B), migrate to the corrected canonical `causal_state_dependency_declaration`
   `mode: vacuous | exhaustive` field (`CANDLE-EC-A-MAJ-02`), and apply the explicit
   `cardinality: {exactly: 1}` for `candle-corrected` (`CANDLE-EC-A-MIN-01`) — then fresh Review A of
   the corrected pair.
5. Resume Structure (4) / Regime (2) Event Contract authoring using the validated representation
   pattern directly — no re-derivation of classification results, already reviewed in
   `context-upstream-state-dependency-derivation-001.md` v0.4.
6. Governed publication routing for the eight clean first-version contracts.
7. Feature Event Contract future-version/state-dependency-authority derivation, independent of steps
   4–6.
8. Context Input Contract v0.3 readiness re-review.
9. Only then consider `context-market-input/v1.0` publication.
