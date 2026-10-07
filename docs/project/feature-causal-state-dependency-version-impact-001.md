---
id: feature-causal-state-dependency-version-impact-001
title: "Feature Output Event Contracts — ADR-048 causal_state_dependency_declaration Version-Impact and Compatibility Classification"
kind: analysis
version: "0.1"
status: Draft
owner: Product Owner
generated_at: "2026-10-07"
---

# FEATURE-CAUSAL-STATE-DEPENDENCY-VERSION-IMPACT-001

**Analysis/derivation artifact, produced under
`docs/project/workstreams/m3/feature-future-dependency-workstream.md`
(packet blob `a400521aa42ea5e4645696872b7192580c7052f4`, confirmed exact this transaction).** Does
not modify or version any Published Event Contract in place; does not modify `feature.md`,
`ADR-038`, `ADR-039`, or `ADR-048`; does not author an ADR; does not touch any Structure/Regime
workstream file; does not publish anything (Draft candidates produced by this transaction remain
`status: Draft`, not `Published`).

## 0. Boundary and fresh-verification record

Starting HEAD `e8166e402f1cbf3f95e23908f28562d255b7d43f` — confirmed `main == origin/main`,
working tree clean of any in-progress change before this transaction (only pre-existing, unrelated
untracked `.DS_Store`/`CLAUDE.md` files present, not touched by this transaction).

Workstream packet (`docs/project/workstreams/m3/feature-future-dependency-workstream.md`) blob
confirmed exact: `a400521aa42ea5e4645696872b7192580c7052f4`. The one commit since the packet's own
`planning_head` (`197100785fb786278816b5b694dc9d380d9c1b8b`) through `e8166e402f1cbf3f95e23908f28562d255b7d43f`
(`M3 control plane bounded correction (M3-CP-A-MAJ-01/02)`) touched only
`docs/project/m3-execution-control-plane.yaml` — confirmed by direct diff inspection — and does not
alter this packet, its authority closure set, or any file this packet governs. No drift.

Published Feature Event Contract blobs, confirmed exact before this transaction (fresh-read in
full):

```text
docs/architecture/event-contracts/feature-computed/v1.0.yaml           9e1da0ac1e72403a780ff16e0d06ed68354da623
docs/architecture/event-contracts/feature-fact-invalidated/v1.0.yaml   7015fa4c09b0fa6993c1324858719ebca76d260d
```

Every authority in the packet's closure set was fresh-read in full this transaction:
`docs/domain/feature.md` v0.6 (Draft) §1–§5; both Published Feature Event Contract v1.0 artifacts
above; `docs/adr/ADR-048.md` (Approved v0.3); `docs/adr/ADR-038.md` (Approved v0.1); `docs/adr/ADR-039.md`
(Approved v0.1); `docs/constitution/10-compatibility-capability-contract.md` (Locked v2.7) §10.3,
§10.4, §10.7; `docs/project/context-upstream-state-dependency-derivation-001.md` v0.5 §2.1/§2.2 (and,
for this Feature-specific analysis, §2.9/§2.10 — the two causation-ref categories for
`FEATURE_COMPUTED`/`FEATURE_FACT_INVALIDATED`); `docs/domain/context-map.yaml` v0.19 (confirmed path
is `docs/domain/context-map.yaml`, not `docs/architecture/context-map.yaml` as the packet's own path
text names it — a stale path reference in the packet, not a drift/conflict in its substance; the
artifact itself, fresh-read, is unchanged in content from what the packet's authority closure set
describes).

## 1. Objective recap

Determine, as one coherent bounded analysis, whether `feature-computed`/`feature-fact-invalidated`
(both `status: Published`, `v1.0`) require a new version to carry Approved `ADR-048`'s
`causal_state_dependency_declaration` field, and if so, what Chapter 10 §10.4 Compatibility Result
classification that delta would receive.

## 2. Semantic Closure matrix — resolved

| semantic topic | authoritative source | resolved? | conclusion |
|---|---|---|---|
| Feature's own causation-ref classification (`STATE_DEPENDENCY` vs `EXTERNAL_NON_STATE_CAUSE`) | derivation v0.5 §2.9 (`FEATURE_COMPUTED`, 2 categories)/§2.10 (`FEATURE_FACT_INVALIDATED`, 5 categories, collapsing to 2 declared roles — §3.4 below) | resolved | reused as-is, not re-derived: all 7 category rows classify `EXTERNAL_NON_STATE_CAUSE`; 0 `STATE_DEPENDENCY`; 0 `UNRESOLVED` |
| Whether a Published v1.0 Event Contract may gain `causal_state_dependency_declaration` without a version bump | `ADR-039` self-containment model + Chapter 10 §10.3 (three independent version axes, Event Contract axis owns `event_class`/`allowed_streams`/`merge_constraints`/payload semantic as one bundle) | resolved | **No.** `ADR-039`'s immutability discipline (*"a version-artifact file transitions `Draft` → `Published`; from the `Published` boundary forward it is immutable byte-for-byte — no in-place edits"*) applies to the whole artifact, not only `payload_shape` — confirmed independently by `ADR-048`'s own §Non-retroactivity item 5 (*"An existing immutable Event Contract version requiring this capability must receive a NEW version-artifact"*). This is a confirmation of already-decided authority, not a new architecture question |
| Compatibility Result classification of that delta (additive field vs. breaking) | Chapter 10 §10.3/§10.3.1/§10.4 | resolved this transaction (§3.3 below) | **Non-breaking** — contract-surface-evolving, minor bump (`v1.0` → `v1.1`) for both `feature-computed` and `feature-fact-invalidated`. Reasoning in §3.3; distinguished explicitly from `feature.md` v0.6's own `BREAKING` precedent for `computation_dependency_content_evidence`, which is a different kind of delta (§3.2) |
| Whether Feature consumes any Structure/Regime event type directly (would create a true cross-lane dependency this packet does not currently assume) | `docs/domain/context-map.yaml` v0.19 fresh-read, `feature.md` v0.6 §1 `events_consumed` | re-verified fresh this transaction | **No new/unexpected edge.** Feature consumes Candle (`candle-closed`/`candle-corrected`), Swing (`swing-confirmed`/`swing-invalidated`), and Regime (`regime-classified`/`regime-fact-invalidated`) — all three already registered, `feature-engineering` as sole consumer context, in `context-map.yaml`'s `relationships` block. **Feature does not consume any Structure event** (`break-of-structure-detected`/`change-of-character-detected`/`structure-fact-invalidated`/`structure-recomputed` — no relationship edge from `market-structure-analysis` to `feature-engineering` carries any of these four `contract_id`s; only `swing-confirmed`/`swing-invalidated`, a distinct contract family within the same `market-structure-analysis` context). This confirms, rather than contradicts, the control plane's "Feature is independent of Structure/Regime's own Event Contract content" assumption — no escalation triggered |

## 3. Analysis

### 3.1 `causal_state_dependency_declaration` is Event-Contract-artifact-level governed metadata, not a payload field

`ADR-048` §1 fixes this field as *"a new top-level field on the Event Contract version-artifact,
sibling to `event_class`/`allowed_streams`/`merge_constraints`/`payload_shape`/
`payload_semantics_and_invariants`/`compatibility_commitment`"* — and explicitly **prohibits**
placing it under `payload_semantics_and_invariants` or inside `payload_shape`. It is declarative
metadata read by a validator implementing Chapter 8 §8.2.3's `declared-state-dependencies` mode; it
never appears in, and never changes, any `FeatureComputed`/`FeatureFactInvalidated` event
**instance**'s own payload bytes. No field is added to, removed from, or retyped within
`payload_shape` by this delta.

This is the controlling distinction for §3.3 below, and it is categorically different from the one
prior delta this repository has already classified for these same two `contract_id`s —
`computation_dependency_content_evidence` (`ADR-037`), which **was** added directly to
`payload_shape` (`feature.md` v0.6 §3/§4; confirmed in both Published v1.0 artifacts'
`payload_shape` blocks) and was therefore correctly classified `BREAKING` under §10.3.1's own
*"thêm element required không có fallback → breaking"* rule — a rule stated in terms of what a
**reader must parse in the data** (*"consumer CŨ vẫn đọc/validate đúng dữ liệu MỚI"*, §10.3.1).
`causal_state_dependency_declaration` adds no such element to the data a consumer reads.

### 3.2 A version bump is still required, independent of breaking/non-breaking classification

`ADR-039`'s immutability discipline treats the entire version-artifact file as the atomic
Referenced Authoritative Artifact — not only its `payload_shape` portion. Any addition of any kind
to a `Published` snapshot, including a sibling top-level field that touches no payload byte, is
still forbidden in place and still requires a new `contract_version`. This is not reopened or
re-derived here — it is `ADR-039`/`ADR-048`'s own already-decided position, confirmed by direct
re-read (§0).

### 3.3 Breaking vs. non-breaking classification of this specific delta

Applying Chapter 10 §10.3's own general breaking-change test — *"thay đổi làm consumer hợp lệ hiện
tại không còn hợp lệ"* (a change that makes a currently-valid consumer invalid) — against Feature's
one confirmed registered consumer (`context-aggregation`/`context-projection`, per `ADR-038`'s own
finding and independently reconfirmed in `context-map.yaml`'s `relationships` block, §2 above):

- `context-aggregator` reads `payload.value`/`unit`/`effective_window`/`input_fact_refs`/
  `supersedes_fact_ref`/`computation_cursor`/`computation_dependency_content_evidence`
  (`FeatureComputed`) and the analogous `FeatureFactInvalidated` payload fields — none of which
  change shape, type, nullability, or meaning under this delta.
- `causal_state_dependency_declaration` is read only by a validator implementing
  `dependency_authority: per_effect_event_contract` for an Input Contract that specifically
  declares `causal_closure_policy.mode: declared-state-dependencies` — a consumption mode no
  currently-registered consumer of Feature's events uses. Even a consumer that *does* read it in
  the future reads a field that is wholly new (nothing it previously depended on is withdrawn,
  narrowed, or reinterpreted).
- Per §10.3.1's own minimal classification principles: *"thêm element optional có semantic/default
  an toàn cho reader chưa biết nó → có thể non-breaking."* A reader unaware of
  `causal_state_dependency_declaration` is unaffected by its presence — it sits outside
  `payload_shape` entirely and is not a value any currently-valid consumer's reader must parse to
  continue correctly reading `value`/`unit`/`effective_window`/etc.

**Conclusion: non-breaking.** No currently-valid consumer becomes invalid; no existing commitment
`context-aggregator` relies on is withdrawn or reinterpreted. Per `ADR-039`'s major.minor grammar
(*"a non-breaking, contract-surface-evolving change is published as a new version-artifact whose
minor component is incremented by exactly `1`, major unchanged"*), the correct next identifier for
both `contract_id`s is **`v1.1`** (not `v2.0`).

This conclusion is reached entirely from existing Approved/Locked authority (`ADR-039`, `ADR-048`,
Chapter 10 §10.3/§10.3.1, `ADR-038`'s own consumer-topology finding, and `context-map.yaml`'s
registered edges) — it invents no new classification rule and reopens no prior decision. It does
not retroactively reclassify `computation_dependency_content_evidence`'s own, separately-grounded
`BREAKING` conclusion (`feature.md` v0.6), which remains correct for that different, payload-level
delta.

### 3.4 Existing `backward_only` commitment — scope of what it actually governs here

`ADR-038`'s `backward_only` commitment (Chapter 10 §10.3.1, *"consumer CŨ vẫn đọc/validate đúng dữ
liệu MỚI"*) governs the DATA these two Event Contracts carry — `payload_shape` content, as read by
an advancing consumer (§ "What this commitment protects" in `ADR-038`). Because this delta touches
no `payload_shape` content, the commitment is not engaged by it in any way that could fail: there is
no new required payload element for an old reader to stumble on. No fresh Chapter 10 §10.4
Compatibility Result is created or required by this delta's publication alone (consistent with the
packet's forbidden scope — this transaction creates no evaluator/grant/policy-registry mechanism);
should a Compatibility Result ever be sought for a specific consumer/subject pinning this new
version, that remains separate, later, governed work exactly as `ADR-038`'s own Consequences already
scope it.

### 3.5 Role declarations for the Draft `v1.1` candidates

Reusing derivation v0.5 §2.9/§2.10 (already Review-A-validated `EXTERNAL_NON_STATE_CAUSE`
classifications, not re-derived here) and `feature.md` v0.6 §3/§4's own envelope-binding invariants
for exactly which refs populate `causation_refs`:

**`feature-computed`** — `causation_refs` is the union of `input_fact_refs` (always present, never
empty) and, only for a correction replacement, the superseded `FeatureFactInvalidated` ref
(`feature.md` §3 invariant: *"(a) original computation — PHẢI chứa toàn bộ `input_fact_refs`; (b)
correction replacement — PHẢI chứa `input_fact_refs` đã cập nhật VÀ chính `FeatureFactInvalidated`
đang được supersede"*). Two roles, both `payload_field` selectors (`input_fact_refs`,
`supersedes_fact_ref`), both `EXTERNAL_NON_STATE_CAUSE` — no `payload_field` role is needed beyond
these two, and no overlap is possible between them (disjoint referenced event families).

**`feature-fact-invalidated`** — `causation_refs` is always exactly two entries: `invalidated_fact_ref`
and the one direct causing event selected by `invalidation_cause` (`feature.md` §4 invariant,
quoted in full in §3.3's sibling matrix). Two roles: a `payload_field` selector for
`invalidated_fact_ref` (`exactly: 1`), and a discriminated `by_target` selector keyed on
`invalidation_cause` with the four `cases` (`candle_corrected`/`regime_fact_invalidated`/
`swing_invalidated`/`eligible_swing_selection_superseded`) — the same discriminant shape `ADR-048`
itself illustrates for exactly this kind of enum-keyed direct-cause role (`ADR-048` §4's
`discriminant` example cites `swing_invalidated`/`swing-invalidated` verbatim). Both roles
`EXTERNAL_NON_STATE_CAUSE`.

Full role bodies are inlined in the Draft candidates themselves (§4).

## 4. Draft vNext artifacts produced by this transaction

```text
docs/architecture/event-contracts/feature-computed/v1.1.yaml          (new file, status: Draft)
docs/architecture/event-contracts/feature-fact-invalidated/v1.1.yaml  (new file, status: Draft)
```

Each is authored as the one complete, self-contained snapshot `ADR-039` requires — not a diff
against `v1.0` — carrying `v1.0`'s own `event_class`/`allowed_streams`/`merge_constraints`/
`payload_shape`/`payload_semantics_and_invariants`/`compatibility_commitment` forward byte-identical
in meaning, adding only `causal_state_dependency_declaration` (governed-authored directly against
`ADR-048`, per the same authoring discipline `v1.0` itself already used for `event_class`/
`allowed_streams`/`merge_constraints` — *"GOVERNED-AUTHORED against current higher authority... NOT
mechanically transcribed from `feature.md`"*), and updating `contract_version`/`status`/
`reviewers`/`approved_by`/`approved_at`/`last_review`/`provenance` accordingly. **Neither `feature.md`
nor `ADR-038` is touched to produce these candidates** — consistent with precedent already set by
`v1.0`'s own authoring of fields `feature.md` never declared.

## 5. Validation performed

- Fresh-read every authority in the packet's closure set in full (§0); confirmed no drift on the
  packet itself or on any authority it cites.
- Independently re-verified Feature's registered consumer/producer topology against
  `docs/domain/context-map.yaml` v0.19 (not merely inherited from `ADR-038`'s or the derivation's own
  prior citation) — confirms no undisclosed Structure dependency and no new consumer.
- Cross-checked the two new roles' selector/cardinality/classification shapes against `ADR-048`'s
  own closed grammar (§2–§6, §9 fail-closed list) for every applicable rule: closed selector key
  sets, cardinality forms, discriminant `cases` closure, canonical-locator uniqueness precondition
  (trivially satisfied — Feature's `causation_refs` entries are always distinct event types/streams
  in every category examined), exactly-one-match coverage of `causation_refs` for both event types.
- Confirmed, by direct blob-hash comparison before/after, that neither Published `v1.0` artifact was
  modified (§0, §6).
- Confirmed `feature.md`, `ADR-038`, `ADR-039`, and `ADR-048` are unmodified by this transaction (no
  `Edit`/`Write` call targeted any of them).
- Confirmed no file under any other workstream's scope (`structure`, `regime`, `m3-execution-control-plane.yaml`,
  any other workstream packet) was read for mutation purposes or written.

## 6. Non-retroactivity / forbidden-scope confirmation

- `docs/architecture/event-contracts/feature-computed/v1.0.yaml` — **unmodified**, blob
  `9e1da0ac1e72403a780ff16e0d06ed68354da623` (re-confirmed identical after this transaction).
- `docs/architecture/event-contracts/feature-fact-invalidated/v1.0.yaml` — **unmodified**, blob
  `7015fa4c09b0fa6993c1324858719ebca76d260d` (re-confirmed identical after this transaction).
- `docs/domain/feature.md` — unmodified.
- `docs/adr/ADR-038.md`, `docs/adr/ADR-039.md`, `docs/adr/ADR-048.md` — unmodified.
- No ADR authored by this transaction.
- No Structure/Regime/other-workstream file touched.
- No Published artifact anywhere created or altered by this transaction — only two new `status:
  Draft` files added under `feature-computed/`/`feature-fact-invalidated/`, plus this analysis
  artifact.

## 7. Conclusion

- **Version-impact:** a new version is warranted; neither Published `v1.0` artifact may be edited
  in place (confirmation of existing authority, not a new decision).
- **Compatibility classification:** non-breaking, contract-surface-evolving delta — minor bump,
  `v1.0` → `v1.1`, for both `feature-computed` and `feature-fact-invalidated`.
- **No `ARCHITECTURE_ESCALATION`:** every question in the Semantic Closure matrix (§2) resolves from
  existing Approved/Locked authority; no genuinely unresolved architecture decision was found; no
  new/undisclosed cross-lane dependency was found.
- Draft `v1.1` candidates for both `contract_id`s are produced (§4), carrying the `ADR-048`
  declaration, `status: Draft`, not self-certified as `Published`, not requested for Review A by this
  transaction (per the packet's own completion contract — Review A is a separate, later, human/
  governed step).
