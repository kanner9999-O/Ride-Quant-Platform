---
id: feature-causal-state-dependency-version-impact-001
title: "Feature Output Event Contracts — ADR-048 causal_state_dependency_declaration Version-Impact and Compatibility Classification"
kind: analysis
version: "0.2"
status: Draft
owner: Product Owner
generated_at: "2026-10-07"
---

# FEATURE-CAUSAL-STATE-DEPENDENCY-VERSION-IMPACT-001

**Analysis/derivation artifact, produced under
`docs/project/workstreams/m3/feature-future-dependency-workstream.md`
(packet blob `a400521aa42ea5e4645696872b7192580c7052f4`, originally confirmed exact; re-verified
this transaction).** Does not modify or version any Published Event Contract in place; does not
modify `feature.md`, `ADR-038`, `ADR-039`, or `ADR-048`; does not author an ADR; does not touch any
Structure/Regime workstream file; does not publish anything (the Draft `v1.1` candidates this
artifact's own prior version produced remain `status: Draft`, not `Published`, and are not edited
by this correction).

> **v0.2 — bounded correction (this transaction), per explicit architecture disposition: a new ADR
> is NOT required for this classification; this is a bounded application of already-Approved
> authority (`ADR-038`, `ADR-039`, `ADR-048`, Chapter 10 §10.3/§10.7) to one concrete delta.** A
> separate, parallel Draft ADR candidate was authored, corrected twice, and then explicitly
> abandoned on a different branch during this same workstream's review cycle — this correction does
> not reference, inherit, or depend on that candidate in any way; every conclusion below is
> re-derived directly from Approved/Locked authority. Two defects in v0.1 are corrected:
>
> 1. **§3.3/§3.4 described `ADR-038`'s `backward_only` commitment as "not engaged" by this delta.**
>    Read against `ADR-038`'s own Decision text — *"The Feature Output Event Contracts
>    (`feature-computed`, `feature-fact-invalidated`) commit to backward compatibility only"*,
>    committing the whole artifact, not only its payload — that framing was imprecise enough to
>    read as narrowing `ADR-038`'s own commitment by implication. **Corrected:** `ADR-038`'s
>    commitment is restated as applying in full to the entire artifact, `causal_state_dependency_declaration`
>    included; what v0.1 actually established (and v0.2 restates precisely) is which Chapter 10
>    mechanism correctly TESTS a delta against that still-fully-applicable commitment — §10.3's
>    general contract-surface/current-consumer test, read with §10.7's downstream-impact-assessment
>    requirement, rather than §10.3.1's own data-presence-calibrated schema-element rules, which do
>    not mechanically fit a field that is never serialized into any event instance.
> 2. **§3.3's second bullet stated `causal_state_dependency_declaration`'s `declared-state-dependencies`
>    consumption mode is "a consumption mode no currently-registered consumer of Feature's events
>    uses."** This is factually stale. Fresh-read this transaction:
>    `docs/architecture/input-contracts/context-market-input.yaml` (Draft v0.3) already declares
>    `causal_closure_policy: {mode: declared-state-dependencies, dependency_authority:
>    per_effect_event_contract}` over `included_streams` that explicitly include
>    `feature-engine-feature`. `context-aggregator`'s own Draft Input Contract already structurally
>    depends on this exact field for this exact stream. **Corrected** throughout §3.3/§3.4 below —
>    this field's addition is confirmed *enabling* a consumer's own already-declared dependency, not
>    merely harmless to an unrelated one.
>
> §3.3 is also extended with an explicit §10.7 downstream-impact-assessment that additionally checks
> tooling/validator consumers of the Event-Contract-artifact document itself (not only event-instance
> data readers) by direct code inspection — not by assuming tolerant-reader behavior anywhere. The
> bottom-line conclusion (non-breaking, `v1.0 → v1.1`) is unchanged by this correction; only its
> grounding and its consumer-topology fact are corrected. A new §8 records this transaction's own
> `ADR_NOT_REQUIRED` Scope and `ADR-045` Risk classification.

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

**This transaction's own fresh boundary:** starting `main == origin/main == d8308785705369916909b5070d8e3306acb452cb`,
executed on a clean continuation branch cut directly from this commit (no Draft-ADR-candidate
history from any other branch pulled in). Re-confirmed, fresh, at this boundary, by direct blob
comparison against values this artifact already pinned: `feature-computed/v1.0.yaml`
(`9e1da0ac1e72403a780ff16e0d06ed68354da623`), `feature-fact-invalidated/v1.0.yaml`
(`7015fa4c09b0fa6993c1324858719ebca76d260d`), `feature-computed/v1.1.yaml`
(`34023c8958ad13df86c17d66634d219bf2c777b7`), `feature-fact-invalidated/v1.1.yaml`
(`2fbd9cd528582324a70dce1458c6ee8b54465622`) — all four byte-identical, no drift since this
artifact's own v0.1. `docs/adr/ADR-039.md` (blob `717904b8fd75104a681805c0c94ab7c9b19e878f`) and
`docs/adr/ADR-048.md` (blob `560d5191d08a80ae4fa3dd1b8bab93fc9f36c11f`) likewise byte-identical to
values independently pinned earlier in this same workstream. `docs/adr/ADR-038.md`'s own exact
Decision sentence re-read verbatim this transaction (quoted in full in the v0.2 banner above) — no
amendment, `status: Approved` unchanged. `docs/architecture/input-contracts/context-market-input.yaml`
(Draft v0.3) fresh-read in full this transaction — the specific correction to §3.3/§3.4 below is
grounded directly in its own current `causal_closure_policy`/`included_streams` content, re-verified
line-by-line, not inherited from any prior session's summary. `python/feature-engine/src/feature_engine/output_contract_resolver.py`
and `python/feature-engine/src/feature_engine/authority_resolver.py` — the two actual,
currently-existing pieces of tooling in this repository that read an Event Contract/Input Contract
artifact's own file content (as opposed to event-instance data) — fresh-inspected this transaction
(§3.3 below).

## 1. Objective recap

Determine, as one coherent bounded analysis, whether `feature-computed`/`feature-fact-invalidated`
(both `status: Published`, `v1.0`) require a new version to carry Approved `ADR-048`'s
`causal_state_dependency_declaration` field, and if so, what Chapter 10 §10.4 Compatibility Result
classification that delta would receive.

## 2. Semantic Closure matrix — resolved

| semantic topic | authoritative source | resolved? | conclusion |
|---|---|---|---|
| Feature's own causation-ref classification (`STATE_DEPENDENCY` vs `EXTERNAL_NON_STATE_CAUSE`) | derivation v0.5 §2.9 (`FEATURE_COMPUTED`, 2 categories)/§2.10 (`FEATURE_FACT_INVALIDATED`, 5 categories, collapsing to 2 declared roles — §3.5 below) | resolved | reused as-is, not re-derived: all 7 category rows classify `EXTERNAL_NON_STATE_CAUSE`; 0 `STATE_DEPENDENCY`; 0 `UNRESOLVED` |
| Whether a Published v1.0 Event Contract may gain `causal_state_dependency_declaration` without a version bump | `ADR-039` self-containment model + Chapter 10 §10.3 (three independent version axes, Event Contract axis owns `event_class`/`allowed_streams`/`merge_constraints`/payload semantic as one bundle) | resolved | **No.** `ADR-039`'s immutability discipline (*"a version-artifact file transitions `Draft` → `Published`; from the `Published` boundary forward it is immutable byte-for-byte — no in-place edits"*) applies to the whole artifact, not only `payload_shape` — confirmed independently by `ADR-048`'s own §Non-retroactivity item 5 (*"An existing immutable Event Contract version requiring this capability must receive a NEW version-artifact"*). This is a confirmation of already-decided authority, not a new architecture question |
| Compatibility classification of that delta (additive field vs. breaking), and which Chapter 10 mechanism tests it | Chapter 10 §10.3/§10.7 (§10.3.1's own schema-element rule confirmed not to mechanically fit, §3.3 below) | resolved this transaction (§3.3 below) | **Non-breaking**, under `ADR-038`'s fully-applicable `backward_only` commitment tested via §10.3's general consumer-invalidation test + §10.7's downstream-impact assessment — contract-surface-evolving, minor bump (`v1.0` → `v1.1`) for both `feature-computed` and `feature-fact-invalidated`. Reasoning in §3.3; distinguished explicitly from `feature.md` v0.6's own `BREAKING` precedent for `computation_dependency_content_evidence`, which is a different kind of delta correctly tested under §10.3.1 (§3.2/§3.3) |
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

### 3.3 Classification mechanism, and why §10.3.1's schema-element rule is the wrong tool here

`ADR-038`'s `backward_only` commitment (Chapter 10 §10.3.1) applies, **in full**, to the entire
Feature Output Event Contract artifact — `ADR-038`'s own Decision text commits "The Feature Output
Event Contracts," not merely their `payload_shape`, to `backward_only` (quoted verbatim, §0 above).
This delta does not sit outside that commitment, is not exempt from it, and this analysis creates no
exception to it. The question this section actually resolves is narrower: **which Chapter 10
mechanism correctly tests this specific delta against that still-fully-applicable commitment.**

§10.3.1's own minimal-classification sub-rules (*"thêm element required không có fallback →
breaking"*, and the symmetric data-presence reasoning throughout the section) are written for, and
calibrated to, elements of **payload data** a consumer's reader actually parses out of event
instances — *"consumer CŨ vẫn đọc/validate đúng dữ liệu MỚI"*. `causal_state_dependency_declaration`
is never present in any event instance's own payload bytes (§3.1 above, confirmed by direct
inspection of both Draft `v1.1` candidates) — no reader of event DATA ever encounters it, favorably
or unfavorably. Mechanically applying §10.3.1's data-presence rules to it would answer a
reader-tolerance question for a field that raises no reader-tolerance question at all — a category
error, not a more faithful reading of `ADR-038`'s commitment.

**The correct mechanism is instead Chapter 10 §10.3's own general breaking-change test — *"thay đổi
làm consumer hợp lệ hiện tại không còn hợp lệ"* (a change that makes a currently-valid consumer
invalid) — read together with §10.7's downstream-impact-assessment requirement, both applied
entirely within, and in service of, `ADR-038`'s fully-applicable commitment:**

- **Published contract surface / output semantic (§10.7).** The delta strictly adds one new
  top-level field; it removes, narrows, or reinterprets no existing field, value, or meaning.
  `value`/`unit`/`effective_window`/`input_fact_refs`/`supersedes_fact_ref`/`computation_cursor`/
  `computation_dependency_content_evidence` (`FeatureComputed`) and the analogous
  `FeatureFactInvalidated` fields are byte-for-byte unchanged in shape, type, nullability, and
  meaning.
- **Capability set / dependency graph — event-instance-data consumers (§10.7).**
  `context-aggregator` (Feature's one confirmed registered consumer, `ADR-038`'s own finding,
  independently reconfirmed in `context-map.yaml`'s `relationships` block, §2 above) reads only the
  `payload_shape` fields listed above — never `causal_state_dependency_declaration`, which sits
  outside `payload_shape` entirely. No event-data-reading consumer's behavior changes in any way.
  This is not an assumption of tolerant-reader behavior: a reader cannot fail to tolerate bytes that
  are never present in the data it processes.
- **Capability set / dependency graph — the one validator this field has a defined role for
  (§10.7, corrected consumer-topology fact).** `docs/architecture/input-contracts/context-market-input.yaml`
  (Draft v0.3, fresh-read this transaction, §0 above) already declares
  `causal_closure_policy: {mode: declared-state-dependencies, dependency_authority:
  per_effect_event_contract}` over `included_streams` that explicitly include
  `feature-engine-feature`. **This corrects v0.1's own stale claim** that no currently-registered
  consumer uses this mode for Feature's stream — `context-aggregator`'s own Draft Input Contract
  already structurally commits to exactly this mode, for exactly this stream. Per Chapter 8
  §8.2.3's own text, that mode cannot be satisfied for `feature-engine-feature` until a Feature
  Event Contract version actually carries `causal_state_dependency_declaration`. This consumer is
  therefore not merely unaffected by the delta — it currently **cannot** satisfy its own
  already-declared dependency at all, and this field's addition is what first makes that
  satisfiable. Enabling, not breaking.
- **Dependency graph — tooling/validator consumers of the Event-Contract-artifact document itself
  (§10.7), checked by direct code inspection, not assumed tolerant.**
  `python/feature-engine/src/feature_engine/output_contract_resolver.py` is the one actual,
  currently-existing piece of tooling in this repository that reads a Feature output Event Contract
  version-artifact's own file content (feature-engine's own producer-side self-resolution of its
  `event_contract_ref` identity before emitting a fact). Its `_extract_scalar`/`_extract_allowed_streams`
  functions extract only `contract_id`/`contract_version`/`status` scalars and the
  `allowed_streams:` block, each via a targeted prefix-match line scan — confirmed, by reading the
  exact implementation, to enforce no closed or exhaustive top-level key set, and to terminate each
  scan on its own specific target, never on "any unrecognized key." Adding
  `causal_state_dependency_declaration` as a new top-level key neither alters, truncates, nor
  interferes with any of these four extraction targets. `authority_resolver.py` (the analogous
  Input-Contract-side resolver) uses the identical targeted-key-scan discipline. No code anywhere in
  this repository enforces a closed top-level key set against an Event Contract or Input Contract
  artifact that would reject an unrecognized additional field — confirmed by repository-wide search,
  not merely undiscovered.
- **Permission requirement / freshness-latency commitment (§10.7).** Neither is introduced,
  narrowed, or otherwise touched by this delta.

**Conclusion: non-breaking under Chapter 10 §10.3's general test, applied with §10.7's
downstream-impact assessment — `ADR-038`'s `backward_only` commitment is satisfied, not bypassed.**
No currently-valid consumer, of any category checked above, becomes invalid. Per `ADR-039`'s
major.minor grammar (*"a non-breaking, contract-surface-evolving change is published as a new
version-artifact whose minor component is incremented by exactly `1`, major unchanged"*), the
correct next identifier for both `contract_id`s is **`v1.1`** (not `v2.0`) — confirming, under this
corrected grounding, the same identifier the Draft candidates already use (§4/§6 below; the
candidates themselves are not edited by this correction, having been authored correctly the first
time on this specific point).

This conclusion is reached entirely from existing Approved/Locked authority (`ADR-038`, `ADR-039`,
`ADR-048`, Chapter 10 §10.3/§10.7, and `context-map.yaml`/`context-market-input.yaml`'s registered
edges) — it invents no new classification rule, no reader/format policy, and reopens no prior
decision. It does not retroactively reclassify `computation_dependency_content_evidence`'s own,
separately-grounded `BREAKING` conclusion (`feature.md` v0.6), which remains correct for that
different, payload-level delta, correctly tested under §10.3.1's own data-presence rule (the right
tool for a true `payload_shape` field).

### 3.4 Why no Chapter 10 §10.4 Compatibility Result is created here

This analysis reaches a classification conclusion (non-breaking) by direct application of §10.3/§10.7
to the facts above; it does not itself produce a Chapter 10 §10.4 Compatibility Result — that is a
heavier, separately-governed artifact requiring a registered, granted evaluator (Declaration → Grant
→ Enforcement → Verification) and full subject/input/policy-version/grant/evaluation-boundary
evidence (§10.4.1), none of which this transaction creates or invokes. Should a Compatibility Result
ever be sought for a specific consumer/subject pinning the new `v1.1` version, producing one remains
separate, later, governed work, exactly as `ADR-038`'s own Consequences already scope it — unaffected
either way by this correction.

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
- **`ADR-038`'s `backward_only` commitment:** unchanged, applies in full to the entire artifact; not
  narrowed, not exempted, not reopened by this analysis (v0.2 correction).
- **Compatibility classification:** non-breaking, contract-surface-evolving delta, tested under
  Chapter 10 §10.3's general consumer-invalidation test + §10.7's downstream-impact assessment
  (§10.3.1's own schema-element rule confirmed not to mechanically fit a non-payload artifact field)
  — minor bump, `v1.0` → `v1.1`, for both `feature-computed` and `feature-fact-invalidated`. **`v1.1`
  is confirmed the correct identifier** — no change to the existing Draft candidates' own
  `contract_version` is warranted.
- **Corrected consumer-topology fact (v0.2):** `context-aggregator`'s own Draft Input Contract
  (`context-market-input.yaml`) already declares `declared-state-dependencies` for
  `feature-engine-feature` — this field's addition is enabling an already-declared dependency, not
  merely harmless to an unrelated one.
- **Tooling/validator consumers of the artifact document checked, not assumed tolerant (v0.2):**
  `output_contract_resolver.py`/`authority_resolver.py` confirmed unaffected by direct code
  inspection.
- **No `ARCHITECTURE_ESCALATION`:** every question in the Semantic Closure matrix (§2) resolves from
  existing Approved/Locked authority; no genuinely unresolved architecture decision was found; no
  new/undisclosed cross-lane dependency was found; no new ADR is required (§8).
- Draft `v1.1` candidates for both `contract_id`s already exist (§4), carrying the `ADR-048`
  declaration, `status: Draft`, not self-certified as `Published`, not edited by this correction,
  not requested for Review A by this transaction — Review A is a separate, later, human/governed
  step.

## 8. ADR Scope and Risk Classification (this transaction)

**ADR Scope — `ADR_NOT_REQUIRED`.** This transaction applies already-Approved/Locked authority
(`ADR-038`'s `backward_only` commitment, `ADR-039`'s immutability/versioning model, `ADR-048`'s
`causal_state_dependency_declaration` grammar, Chapter 10 §10.3/§10.7) to one bounded,
individually-verifiable classification case. It creates no new Platform Invariant, Event Schema,
module-taxonomy/dependency edge, compatibility policy, or architecture rule — it corrects a stale
factual claim and selects, among already-locked Chapter 10 mechanisms, the one that actually fits a
non-payload artifact field, a determination the governing text itself (§10.3 vs. §10.3.1's own
respective scope) already supports without requiring a new decision. Per `G-ADR-004`: (1) existing
authority resolves this without a new decision — YES, confirmed above; (2) not a new architecture
decision, cheaply correctable if wrong — this is a classification conclusion for one already-Draft,
not-yet-Published pair of candidates, reversible by ordinary correction before publication; (3)
Chapter 0 §4b triggers — none fire: no Event Schema is changed (the Draft candidates are not edited
by this correction), no new module/dependency edge is created (the `context-aggregator`/
`feature-engine-feature` edge already existed in `context-map.yaml` before this transaction); (4)
not authored to "complete" a prior ADR's open item, because no ADR is authored at all.

**Risk Classification (`ADR-045`) — `R1`.** Bounded semantic correction: a factual-topology fix
(`context-aggregator` already uses `declared-state-dependencies`) plus a classification-mechanism
correction (§10.3/§10.7, not §10.3.1) applied to one concrete, already-identified delta — internal
to this analysis artifact, does not alter any external contract/authority (`ADR-038`/`ADR-039`/
`ADR-048` all unchanged), reversible with limited blast radius (only this Draft analysis artifact is
edited; neither Draft `v1.1` candidate's own content changes). Not `R2`: no Platform Invariant or
Event Schema is changed; no new authority/source-of-truth semantic is created (the opposite — an
existing semantic is correctly applied); this exact artifact has not been through a prior round of
semantic correction (`ADR-045`'s own "repeated semantic correction" criterion does not fire for a
first correction); no conflicting authority/evidence was found once the stale consumer-topology
claim was corrected. Per `ADR-045`, R1 defaults to `NO CROSS-CHECK` — Review A (separate, later,
human/governed step) is sufficient.
