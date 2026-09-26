---
id: context-upstream-state-dependency-derivation-001
title: "Context Upstream Event-Contract State-Dependency Authority — Derivation"
kind: analysis
version: "0.1"
status: Draft
owner: Product Owner
generated_at: "2026-09-26"
---

# CONTEXT-UPSTREAM-STATE-DEPENDENCY-DERIVATION-001

**Analysis / derivation artifact only.** Does not modify or version any Event Contract; does not
publish any Event Contract; does not publish `context-market-input / v1.0`; does not modify any
Domain Contract, Constitution chapter, or ADR; does not implement runtime.

## 0. Boundary and fresh-verification record

Starting HEAD `e1b4cf30aa7c70f9d7c60b1119de26baf1b09054` — confirmed exact, `main == origin/main`,
working tree clean before this transaction.

Pinned source blobs, fresh-verified exact before analysis:

| File | Blob |
|---|---|
| `docs/domain/candle.md` | `17c3f9412924de577558dd9bad41c769b45eba22` |
| `docs/domain/structure.md` | `78964dfb6852bbac3fa1e034d64b4fc8031c3fef` |
| `docs/domain/regime.md` | `edd1584377f1db84269e7b1dfdd4926d0ce01c70` |
| `docs/domain/feature.md` | `fcdb052484a00400a575dbf6baba3a7f99ae42de` |
| `docs/constitution/08-event-model.md` | `4a27db556e6ee8f9b7ac085194a10c63677b035f` |
| `docs/adr/ADR-038.md` | `ef931de871786ccd27119528b680d4d85e06c9f2` |
| `docs/adr/ADR-039.md` | `717904b8fd75104a681805c0c94ab7c9b19e878f` |
| `docs/architecture/input-contracts/context-market-input.yaml` | `ce74ddf6291abb2b1ed21938ca88050550fb2a0b` |

Also fresh-read in full: Chapter 6 §6.7 (`docs/constitution/06-identity-model.md`), Chapter 10
(`docs/constitution/10-compatibility-capability-contract.md`, particularly §10.3/§10.3.1/§10.4),
`docs/adr/ADR-040.md`, `docs/architecture/stream-registry.yaml` (confirmed `registry_version: v1.0`,
`status: Approved`, all four Context-relevant streams `status: active`, `genesis_position: 0`), and
both Published Feature Event Contracts (`docs/architecture/event-contracts/feature-computed/v1.0.yaml`,
`docs/architecture/event-contracts/feature-fact-invalidated/v1.0.yaml`).

**Explicit boundary limitation, stated up front:** `docs/domain/swing.md` is **not** among this WP's
pinned fresh-read sources. Any classification question whose answer depends on Swing's own
payload-vs-envelope schema (e.g. whether a specific field on `SwingConfirmed`/`SwingInvalidated` is
payload or envelope/subject-scope) is **not mechanically derivable within this WP's boundary** and is
marked `UNRESOLVED` below with that reason stated explicitly — never guessed. This is itself a
governed finding of this WP (see §5.C).

## 1. Authority framework applied

Chapter 8 §8.2.3 (fresh-read, controlling): `mode: declared-state-dependencies` requires
`dependency_authority: per_effect_event_contract` — *"mỗi effect event dùng chính `event_contract_ref`
đã pin của nó để phân loại `causation_refs` nào là state dependency; chỉ những cause đó bắt buộc
trong scope... Classification KHÔNG được nằm trong code processor."* §8.3.4 supplies the intrinsic
test applied throughout this derivation:

```
causation_ref IN-SCOPE (STATE_DEPENDENCY) → phải cursor-visible VÀ apply trước effect
causation_ref EXTERNAL (EXTERNAL_NON_STATE_CAUSE) → chỉ cần immutable committed/existence proof;
                                                     KHÔNG áp rule cursor visibility; cấm đọc payload
```

**The intrinsic question actually asked, per causation-ref category, per event type:** does
authoritative application of *this effect event* need to **read** the causal predecessor's own
domain **payload/value** (a business quantity used to compute or validate this effect's own
payload), or does it only need **proof the predecessor exists** (and, separately, envelope-level
tuple-consistency — which Chapter 8 §8.2.3 already requires uniformly for *every* `causation_refs`
element, regardless of STATE_DEPENDENCY/EXTERNAL_NON_STATE_CAUSE classification, and is therefore
never itself evidence for classifying one way or the other)?

**Two shortcuts explicitly rejected throughout, per the task's own discipline:**
- "cause is one of Context's four included streams → therefore STATE_DEPENDENCY" — **not used**.
- "cause is outside Context's four streams → therefore EXTERNAL_NON_STATE" — **not used**.

Classification below is derived solely from what each event's own Domain Contract says its
authoritative application actually reads.

## 2. Event set analyzed

Exactly the 10 event types context.md §16 authorizes as Context upstream input:

| Family | Event types | Producer stream |
|---|---|---|
| Candle | `CANDLE_CLOSED`, `CANDLE_CORRECTED` | `market-data-ingestion-candle` |
| Structure | `BREAK_OF_STRUCTURE_DETECTED`, `CHANGE_OF_CHARACTER_DETECTED`, `STRUCTURE_FACT_INVALIDATED`, `STRUCTURE_RECOMPUTED` | `structure-engine-structure` |
| Regime | `REGIME_CLASSIFIED`, `REGIME_FACT_INVALIDATED` | `raw-regime-engine-regime` |
| Feature | `FEATURE_COMPUTED`, `FEATURE_FACT_INVALIDATED` | `feature-engine-feature` |

No other event family (CandleObserved, CandleDataGapObserved, Swing events, current-view records,
Context output events, Strategy/Decision/Risk/Execution) is in scope.

## 3. Derivation matrix

For each event, the 12 requested items are folded into: canonical identity + Domain Contract
source + Event Contract artifact status (items 1–6); then, per causation-ref category, the
classification table (items 7–8); then a per-event summary (items 9–12).

### 3.1 `CANDLE_CLOSED`

- Canonical contract concept ID: `candle-closed`. `event_type: CANDLE_CLOSED`. Producer stream:
  `market-data-ingestion-candle`. Source: `candle.md` §4.
- Event Contract artifact status: **absent** (no Event Contract exists for any Candle event type).
  Potential path under ADR-039: `docs/architecture/event-contracts/candle-closed/v1.0.yaml`.
- `candle.md` §4: *"causation_refs: [] (root event — không sửa một fact nào trước)."*
- **`causation_refs: []` — normatively root.** No causal predecessor exists to classify.

**Classification: `VACUOUS`** (no causation-ref category exists — do not invent one).
Mechanically derivable: **YES** (trivial — root-event cardinality is Chapter 8 §8.2.1's own
already-Locked rule, applied not reinterpreted). Already satisfies `per_effect_event_contract`:
**N/A** (nothing to classify) — but the Event Contract artifact itself still does not exist.
Blocking gap: **artifact missing**. Next action: author first Candle Event Contract(s) under
ADR-039 (§4.D below).

### 3.2 `CANDLE_CORRECTED`

- Canonical contract concept ID: `candle-corrected`. Producer stream: `market-data-ingestion-candle`.
  Source: `candle.md` §5/§10/§11.
- Event Contract artifact status: **absent**. Potential path:
  `docs/architecture/event-contracts/candle-corrected/v1.0.yaml`.
- `candle.md` §5: *"causation_refs KHÔNG rỗng"* — exactly one category: a reference to the
  `CandleClosed`/`CandleCorrected` fact being corrected ("`causation_refs` PHẢI trỏ chính xác event
  đang được sửa").

| Category | Referenced family | Why carried | Payload/state needed by this effect's own application? | Proposed classification | Authority |
|---|---|---|---|---|---|
| corrected-fact ref | `candle-closed`/`candle-corrected` (same family, same stream) | Identifies which prior fact this correction replaces (§11 precedence algorithm, Bước 4) | The new OHLCV values are supplied **directly** in this event's own payload (venue-provided correction), never derived from the old fact's OHLC. The only reads against the referenced fact are `effective_time` and `recorded_time` — both **envelope** fields (candle.md §2), used for envelope-consistency binding ("effective_time KHÔNG đổi", "recorded_time PHẢI mới hơn"), not domain payload | `UNRESOLVED` | Chapter 8 §8.2.3's STATE_DEPENDENCY/EXTERNAL_NON_STATE_CAUSE dichotomy is framed around **cross-stream** value inputs (its own worked example: `ARBITRAGE_DECISION_CREATED` depending on two quote streams + risk state). A same-family, same-stream **lineage-supersession** reference — "which prior record does this one replace" — is a third causal-reference shape existing authority does not explicitly address. Envelope-consistency reads (tuple consistency, §8.2.3) are required uniformly regardless of classification and are therefore not themselves evidence either way. More than one legitimate reading exists → STOP triggered, not guessed |

**Event summary:** mechanically derivable: **NO** (1 of 1 category UNRESOLVED). Already satisfies
`per_effect_event_contract`: **NO**. Blocking gap: artifact missing **and** classification
semantic unresolved. Next action: see §6 ADR classification — this is the primary candidate for
architecture-level clarification, since the identical ambiguity recurs verbatim in
`CANDLE_CORRECTED`'s counterparts across Structure/Regime/Feature (§3.5, §3.7, §3.9 below).

### 3.3 `BREAK_OF_STRUCTURE_DETECTED` and 3.4 `CHANGE_OF_CHARACTER_DETECTED`

Structurally identical causation shape (`structure.md` §3/§4/§6/§6a/§7) — analyzed together.

- Canonical contract concept IDs: `break-of-structure-detected`, `change-of-character-detected`.
  Producer stream: `structure-engine-structure`.
- Event Contract artifact status: **absent** for both. Potential paths:
  `docs/architecture/event-contracts/break-of-structure-detected/v1.0.yaml`,
  `.../change-of-character-detected/v1.0.yaml`.
- `structure.md` §3/§4: *"causation_refs PHẢI chứa: `broken_swing_ref.swing_confirmed_event_ref`;
  VÀ `breaking_candle_refs` cung cấp bằng chứng break."*

| Category | Referenced family | Why carried | Payload/state needed? | Proposed classification | Authority |
|---|---|---|---|---|---|
| `swing_confirmed_event_ref` (via `broken_swing_ref`) | `swing-confirmed` | Identifies the Eligible Swing level being broken (§6a) | §6's break criterion table literally compares `candle.high/low/close` against **`broken_swing.pivot_price`** — a value read from the referenced `SwingConfirmed` fact's own payload, directly gating whether this effect event may even be emitted | `STATE_DEPENDENCY` | `structure.md` §6 (pinned, self-contained — this dependency is asserted by Structure's own Domain Contract, independent of Swing's internal schema, so no `swing.md` read is required to establish it) |
| `breaking_candle_refs` | `candle-closed`/`candle-corrected` | Provides the authoritative Candle(s) confirming the break | Same break criterion table reads `candle.high`/`candle.low`/`candle.close` directly from the referenced Candle fact's own payload | `STATE_DEPENDENCY` | `structure.md` §6, `candle.md` §3/§4 payload |

**Event summary (both event types):** mechanically derivable: **YES**, both categories, high
confidence. Already satisfies `per_effect_event_contract`: **NO** — no Event Contract artifact
exists. Blocking gap: artifact missing only (classification itself is clear). Next action:
first-publication Structure Event Contract authoring under ADR-039 (§4.D).

### 3.5 `STRUCTURE_FACT_INVALIDATED`

- Canonical contract concept ID: `structure-fact-invalidated`. Producer stream:
  `structure-engine-structure`. Source: `structure.md` §5/§10.
- Event Contract artifact status: **absent**. Potential path:
  `docs/architecture/event-contracts/structure-fact-invalidated/v1.0.yaml`.
- `structure.md` §5: *"causation_refs PHẢI trỏ: event BOS/CHoCH đang bị invalidate (bắt buộc, đúng
  một); VÀ nguyên nhân — SwingInvalidated (a), CandleCorrected (b), hoặc StructureFactInvalidated
  của fact mà nó phụ thuộc trong cascade (c)."*

| Category | Referenced family | Why carried | Payload/state needed? | Proposed classification | Authority |
|---|---|---|---|---|---|
| `invalidated_fact_ref` (the BOS/CHoCH being invalidated) | `break-of-structure-detected`/`change-of-character-detected` | Identifies the specific historical fact being negated | **All three** `invalidation_cause` legitimacy invariants (§5) require reading this referenced fact's own payload: cause `swing_invalidated` needs its `broken_swing_ref`; cause `breaking_candle_corrected` needs its `breaking_candle_refs`; cause `chained_invalidation` needs its `prior_orientation`. This is a genuine payload read on the invalidated fact itself, not merely identity/existence | `STATE_DEPENDENCY` | `structure.md` §5 invariants (all three, explicit) |
| cause (a) `SwingInvalidated` | `swing-invalidated` | Proves the broken Swing level itself was invalidated | Validation requires matching `swing_id`/`swing_revision` — **whether these fields live in `SwingInvalidated`'s payload or in its `subject_ref`/scope is a `swing.md` fact this WP cannot verify** (swing.md not pinned) | `UNRESOLVED` | Requires `swing.md` — out of this WP's boundary (§0) |
| cause (b) `CandleCorrected` | `candle-corrected` | Proves the breaking Candle was itself corrected | §5 invariant: *"invalidation_cause = breaking_candle_corrected CHỈ hợp lệ khi... payload đã sửa không còn thỏa break criterion (§9)"* — this **explicitly** requires reading `CandleCorrected`'s own new OHLC payload and re-evaluating the break formula | `STATE_DEPENDENCY` | `structure.md` §5 invariant (explicit, conditional re-validation) |
| cause (c) `chained_invalidation` (prior `StructureFactInvalidated` in same cascade) | `structure-fact-invalidated` | Proves this fact's cascade-ordering precondition (§10 step 7: no descendant invalidation causation to an uncommitted invalidation) | The referenced `StructureFactInvalidated`'s own payload is `{invalidated_fact_ref, invalidation_cause, invalidation_reason}` only — no orientation data. The chaining *semantic* check reads `prior_orientation` from `invalidated_fact_ref` (already counted above), not from this reference. This reference itself proves only that the prior cascade step has already **committed** | `EXTERNAL_NON_STATE_CAUSE` | `structure.md` §10 step 7 (existence/commit-order proof only, intrinsic test applied directly — not a stream-membership shortcut) |

**Event summary:** mechanically derivable: **3 of 4** categories (`invalidated_fact_ref`,
`breaking_candle_corrected`, `chained_invalidation`); **1 of 4 UNRESOLVED** (`swing_invalidated`,
requires `swing.md`). Already satisfies `per_effect_event_contract`: **NO** (artifact absent, and
one category unresolved). Blocking gap: artifact missing + one classification category pending a
Swing-inclusive re-derivation. Next action: (i) first-publication Structure Event Contract
authoring for the 3 resolved categories; (ii) a follow-on Swing-inclusive derivation WP for the
`swing_invalidated` category only.

### 3.6 `STRUCTURE_RECOMPUTED`

- Canonical contract concept ID: `structure-recomputed`. Producer stream: `structure-engine-structure`.
  Source: `structure.md` §5a.
- Event Contract artifact status: **absent**. Potential path:
  `docs/architecture/event-contracts/structure-recomputed/v1.0.yaml`.
- `structure.md` §5a: *"causation_refs PHẢI trỏ đủ MỌI StructureFactInvalidated thuộc cùng
  cascade."*

| Category | Referenced family | Why carried | Payload/state needed? | Proposed classification | Authority |
|---|---|---|---|---|---|
| full `StructureFactInvalidated` set of the cascade | `structure-fact-invalidated` | Proves the cascade is complete before recomputation | `resulting_orientation` is computed by **refolding** Swing/Candle facts pinned via `payload.input_cursor_ref` — a completely separate mechanism from `causation_refs`. The referenced `StructureFactInvalidated` events' own payload (`invalidated_fact_ref`/`invalidation_cause`/`invalidation_reason`) is never read to compute `resulting_orientation`; only their **existence as a complete set** (§5a invariant: none of the affected facts may be missing from causation) is required | `EXTERNAL_NON_STATE_CAUSE` | `structure.md` §5a (explicit: recomputation input is `input_cursor_ref`, not the causation set's own payload) |

**Event summary:** mechanically derivable: **YES** (1 of 1). Already satisfies
`per_effect_event_contract`: **NO** (artifact absent). Blocking gap: artifact missing only. Next
action: first-publication Structure Event Contract authoring.

### 3.7 `REGIME_CLASSIFIED`

- Canonical contract concept ID: `regime-classified`. Producer stream: `raw-regime-engine-regime`.
  Source: `regime.md` §3/§8/§8a/§10.
- Event Contract artifact status: **absent**. Potential path:
  `docs/architecture/event-contracts/regime-classified/v1.0.yaml`.
- `regime.md` §3: *"causation_refs KHÔNG BAO GIỜ rỗng: (a) original — toàn bộ candle_evidence_refs;
  (b) replacement — candle_evidence_refs đã cập nhật VÀ chính RegimeFactInvalidated đang được
  supersede."*

| Category | Referenced family | Why carried | Payload/state needed? | Proposed classification | Authority |
|---|---|---|---|---|---|
| `candle_evidence_refs` | `candle-closed`/`candle-corrected` | The Candle window this classification is computed over | `payload.computed_metric` is directly computed by `metric_formula_id` (§6) operating on these Candles' own OHLCV payload; `class` is derived from `computed_metric` against `class_thresholds`. Genuine, formula-level payload dependency | `STATE_DEPENDENCY` | `regime.md` §6 (metric formula reads Candle evidence), §3 invariants |
| `RegimeFactInvalidated` ref (replacement case only) | `regime-fact-invalidated` | Proves the fact this replacement supersedes has actually been invalidated (lineage precondition, §3/§10 rule 2/4/7) | `class`/`computed_metric` of the replacement are recomputed **solely** from `candle_evidence_refs` — the referenced `RegimeFactInvalidated`'s own payload (`invalidated_fact_ref`/`invalidation_reason`) is never read; only its existence/visibility is required | `EXTERNAL_NON_STATE_CAUSE` | `regime.md` §3 invariants (recomputation uses only evidence refs) |

**Event summary:** mechanically derivable: **YES** (2 of 2). Already satisfies
`per_effect_event_contract`: **NO** (artifact absent). Blocking gap: artifact missing only. Next
action: first-publication Regime Event Contract authoring.

### 3.8 `REGIME_FACT_INVALIDATED`

- Canonical contract concept ID: `regime-fact-invalidated`. Producer stream:
  `raw-regime-engine-regime`. Source: `regime.md` §4/§10.
- Event Contract artifact status: **absent**. Potential path:
  `docs/architecture/event-contracts/regime-fact-invalidated/v1.0.yaml`.
- `regime.md` §4: *"causation_refs PHẢI trỏ: invalidated_fact_ref (bắt buộc, đúng một); VÀ
  CandleCorrected là nguyên nhân trực tiếp."* — the **single** cause family (unlike Structure,
  Regime does not consume Swing, so there is no `swing_invalidated`/`chained_invalidation` branch —
  `regime.md` §4 description states this explicitly, symmetric with `ADR-003`).

| Category | Referenced family | Why carried | Payload/state needed? | Proposed classification | Authority |
|---|---|---|---|---|---|
| `invalidated_fact_ref` | `regime-classified` | Identifies the fact being invalidated; envelope binding requires inheriting `subject_ref`/`effective_time` from it | Regime's invalidation policy is **unconditional**: §10 explicitly requires invalidation whenever a `CandleCorrected` affects `candle_evidence_refs`, "kể cả khi cả computed_metric lẫn class cuối cùng đều giữ nguyên" — there is **no** conditional re-validation against this fact's own `class`/`computed_metric` payload (contrast Structure §3.5 above, where `invalidation_cause` legitimacy explicitly reads the invalidated fact's payload). The only reads are `subject_ref`/`effective_time` — both **envelope** fields (regime.md §2), used for binding, not domain payload | `EXTERNAL_NON_STATE_CAUSE` | `regime.md` §4/§10 (unconditional invalidation policy; envelope inheritance ≠ payload dependency, same envelope/payload split `candle.md`/`structure.md`/`feature.md` all use) |
| `CandleCorrected` (direct cause) | `candle-corrected` | Proves the triggering correction | Same unconditional policy — the invalidation decision needs only the **identity** of which Candle was corrected (does it appear in some `RegimeClassified`'s `candle_evidence_refs`?), never the corrected value itself, since invalidation fires regardless of whether the value actually changed | `EXTERNAL_NON_STATE_CAUSE` | `regime.md` §10 (unconditional trigger, explicit) |

**Event summary:** mechanically derivable: **YES** (2 of 2) — and notably **both** categories
classify **differently** from their nearest Structure analogue (`invalidated_fact_ref` and
`breaking_candle_corrected`/`CandleCorrected`), precisely because Regime's own Domain Contract
defines an unconditional invalidation policy where Structure's defines a conditional one. This is
the concrete illustration of the task's own warning not to assume analogous corrections share a
class. Already satisfies `per_effect_event_contract`: **NO** (artifact absent). Blocking gap:
artifact missing only. Next action: first-publication Regime Event Contract authoring.

### 3.9 `FEATURE_COMPUTED`

- Canonical contract concept ID: `feature-computed`. Producer stream: `feature-engine-feature`.
  Source: `feature.md` §3/§6/§7; Event Contract: `docs/architecture/event-contracts/feature-computed/v1.0.yaml`
  (**Published**, `status: Published`, `allowed_streams: [feature-engine-feature]`).
- `feature.md` §3: *"causation_refs KHÔNG BAO GIỜ rỗng: (a) original — toàn bộ input_fact_refs; (b)
  replacement — input_fact_refs đã cập nhật VÀ chính FeatureFactInvalidated đang được supersede."*
  (Identical to the reviewed Event Contract's own text — confirmed byte-consistent this
  transaction.)

| Category | Referenced family | Why carried | Payload/state needed? | Proposed classification | Authority |
|---|---|---|---|---|---|
| `input_fact_refs` | `candle-closed`/`candle-corrected`, `regime-classified`, and/or `swing-confirmed` (feature_type-dependent, §6/§7) | The evidence set `value` is computed over | §7.1/§7.2 (`volatility_metric`/`directional_persistence_metric`) compute `value` from Candle-evidence formulas — same shape as Regime's `computed_metric`. §7.3 (`distance_to_last_confirmed_swing`) computes `value` from a Swing pivot price and a reference Candle. For the Candle/Regime-sourced categories, this is a direct, self-contained formula-level payload dependency (`feature.md` §6/§7.1/§7.2, no `swing.md` needed). For the Swing-sourced category (only relevant when `feature_type = distance_to_last_confirmed_swing`), the dependency is real in principle but this WP cannot independently confirm which of `SwingConfirmed`'s fields carry the pivot price without `swing.md` | `STATE_DEPENDENCY` for the Candle-evidence and Regime-evidence-sourced sub-categories (mechanically derivable from `feature.md` alone); `swing.md`-dependent for the Swing-evidence sub-category (payload dependency direction is clear — the specific field is not, without `swing.md`) | `feature.md` §6/§7.1/§7.2 (self-contained); §7.3 (directionally clear, field-level detail deferred) |
| `FeatureFactInvalidated` ref (replacement case only) | `feature-fact-invalidated` | Proves the fact this replacement supersedes has been invalidated | `value` of the replacement is recomputed solely from `input_fact_refs` — the referenced `FeatureFactInvalidated`'s own payload is never read, only its existence/visibility | `EXTERNAL_NON_STATE_CAUSE` | `feature.md` §3 invariants (same pattern as Regime §3.7) |

**Event summary:** mechanically derivable: **substantially YES** for both categories at the
principle level (Candle/Regime evidence: fully derivable; Swing evidence: dependency direction
clear, exact field pending `swing.md`; supersede ref: fully derivable). Already satisfies
`per_effect_event_contract`: **NOT YET** — the Published artifact exists but was never evaluated
against, or amended to carry, this classification (this is exactly `CONTEXT-IC-A-MAJ-02`'s
finding). Blocking gap: **versioning/compatibility prerequisite** (§4.A), not a missing artifact.
Next action: see §4.A/§6.

### 3.10 `FEATURE_FACT_INVALIDATED`

- Canonical contract concept ID: `feature-fact-invalidated`. Producer stream:
  `feature-engine-feature`. Source: `feature.md` §4/§9a; Event Contract:
  `docs/architecture/event-contracts/feature-fact-invalidated/v1.0.yaml` (**Published**).
- `feature.md` §4: *"causation_refs PHẢI trỏ: invalidated_fact_ref (bắt buộc, đúng một); VÀ event
  authoritative là nguyên nhân trực tiếp (CandleCorrected/RegimeFactInvalidated/SwingInvalidated/
  winning SwingConfirmed tùy invalidation_cause)."*

| Category | Referenced family | Why carried | Payload/state needed? | Proposed classification | Authority |
|---|---|---|---|---|---|
| `invalidated_fact_ref` | `feature-computed` | Identifies fact being invalidated; envelope binding inherits `subject_ref`/`effective_time` | `feature.md` §3's own invariant explicitly adopts Regime's unconditional policy verbatim: *"KHÔNG có shortcut khi value không đổi... đúng nguyên tắc `regime.md` §10."* No conditional payload re-validation against this fact exists (unlike Structure) | `EXTERNAL_NON_STATE_CAUSE` | `feature.md` §3 invariant citing `regime.md` §10 directly |
| cause (a) `CandleCorrected` | `candle-corrected` | Triggers invalidation when a Candle in `input_fact_refs` is corrected | Same unconditional-trigger reasoning as Regime's analogous cause — identity of the corrected Candle is what matters, not its new value | `EXTERNAL_NON_STATE_CAUSE` | `feature.md` §4 description + §3 unconditional-policy invariant |
| cause (b) `RegimeFactInvalidated` | `regime-fact-invalidated` | Triggers invalidation when a Regime fact in `input_fact_refs` is invalidated | Same unconditional-trigger reasoning | `EXTERNAL_NON_STATE_CAUSE` | `feature.md` §4 description + §3 unconditional-policy invariant |
| cause (c) `SwingInvalidated` | `swing-invalidated` | Triggers invalidation when the Swing used is invalidated (`distance_to_last_confirmed_swing` only) | Whether the identity fields checked (`swing_id`/`swing_revision`) are payload or subject-scope on `SwingInvalidated` is a `swing.md` fact this WP cannot verify | `UNRESOLVED` | Requires `swing.md` — out of boundary |
| cause (d) `eligible_swing_selection_superseded` | `swing-confirmed` (winning candidate) | A newer `SwingConfirmed` won §9a's total order at `R_later` while the fact's original Swing remains valid | §9a's filter pipeline/total order (visibility, `pivot_effective_time`, `recorded_time`, stream identity, `sequence`, `swing_revision`, `swing_id`, `event_id`) reads mostly cursor/envelope-shaped fields of the winning `SwingConfirmed` — but whether `pivot_effective_time` and the identity-scope fields are `SwingConfirmed`'s own envelope/subject-scope or its payload is a `swing.md` fact this WP cannot verify | `UNRESOLVED` | Requires `swing.md` — out of boundary |

**Event summary:** mechanically derivable: **3 of 5** categories (`invalidated_fact_ref`,
`CandleCorrected`, `RegimeFactInvalidated`); **2 of 5 UNRESOLVED** (`SwingInvalidated`,
`eligible_swing_selection_superseded` — both pending `swing.md`). Already satisfies
`per_effect_event_contract`: **NOT YET** (same versioning/compatibility prerequisite as §3.9, plus
the two Swing-dependent categories remain unresolved regardless). Blocking gap: versioning
prerequisite (§4.A) **and** two classification categories pending a Swing-inclusive re-derivation.
Next action: see §4.A/§6, plus follow-on Swing-inclusive derivation.

## 4. Four buckets

### A. MECHANICALLY DERIVABLE

17 of 21 analyzed causation-ref categories, spanning 7 of 10 event types in full
(`CANDLE_CLOSED` vacuously; `BREAK_OF_STRUCTURE_DETECTED`; `CHANGE_OF_CHARACTER_DETECTED`;
`STRUCTURE_RECOMPUTED`; `REGIME_CLASSIFIED`; `REGIME_FACT_INVALIDATED`; `FEATURE_COMPUTED`'s
non-Swing-evidence categories) plus 3 of 4 `STRUCTURE_FACT_INVALIDATED` categories and 3 of 5
`FEATURE_FACT_INVALIDATED` categories, follow directly from each event's own already-authored
Domain Contract text — no new semantic choice, no consumer-specific reasoning, no invented
authority.

### B. EVENT CONTRACT ARTIFACT MISSING

Classification is clear (bucket A), but no Published Event Contract artifact exists at all, for:
`CANDLE_CLOSED`, `CANDLE_CORRECTED` (candle family — none exist at all); `BREAK_OF_STRUCTURE_DETECTED`,
`CHANGE_OF_CHARACTER_DETECTED`, `STRUCTURE_FACT_INVALIDATED`, `STRUCTURE_RECOMPUTED` (structure
family — none exist); `REGIME_CLASSIFIED`, `REGIME_FACT_INVALIDATED` (regime family — none exist).
**8 of 10 event types have zero Event Contract artifact today.**

### C. CLASSIFICATION SEMANTIC UNRESOLVED

Two distinct sources of unresolved classification, deliberately not conflated:

1. **Architecture-framework gap** (`CANDLE_CORRECTED`'s single causation category): Chapter 8
   §8.2.3's STATE_DEPENDENCY/EXTERNAL_NON_STATE_CAUSE dichotomy does not explicitly address a
   same-family, same-stream lineage-supersession reference. This is not a `swing.md` gap — it
   recurs identically in spirit across every family's own correction/invalidation event (compare
   §3.5's `invalidated_fact_ref`, which this WP *was* able to resolve via Structure's own explicit
   payload-reading invariants — `CANDLE_CORRECTED` has no equivalent invariant to resolve it the
   same way, since the new OHLCV values are supplied directly rather than derived from the old
   fact).
2. **Out-of-boundary dependency** (`swing.md` not pinned): `STRUCTURE_FACT_INVALIDATED`'s
   `swing_invalidated` cause; `FEATURE_FACT_INVALIDATED`'s `SwingInvalidated` and
   `eligible_swing_selection_superseded` causes; the Swing-evidence sub-category of
   `FEATURE_COMPUTED`'s `input_fact_refs` (field-level detail only — the dependency's existence
   and direction are already established).

### D. VERSIONING / COMPATIBILITY PREREQUISITE

**Feature (`feature-computed`/`feature-fact-invalidated` v1.0, immutable, Published, `status:
Published`):** adding the derived classification to these two events requires a **new** version
artifact — the existing `v1.0` files are immutable per `ADR-039` and are **not** edited by this or
any future WP; a `v1.1` (non-breaking, additive) or new-major (`v2.0`) artifact would need to be
authored, reviewed, and Product-Owner-decided as a **separate**, governed transaction.

Classifying that future change against `ADR-038`'s `compatibility_commitment: backward_only`:
Chapter 10 §10.3.1's own minimum classification principle states *"thêm element optional có
semantic/default an toàn cho reader chưa biết nó → **có thể** non-breaking"* — the state-dependency
classification would be exactly such an addition (a new optional metadata field per
`causation_refs` element, or an equivalent schema addition; not a change to any existing field's
meaning, type, or cardinality). This is a genuine candidate for "schema/authority metadata addition
only," structurally. **However**, Chapter 10 explicitly refuses to let this abstract principle
alone certify compatibility: *"Quy tắc theo từng format cụ thể (JSON Schema, Avro, Protobuf...)
thuộc Domain Contract/Phase 1"* (§10.3.1) — the concrete reader/format rule (does the actual
validator tolerate an unrecognized additional field, i.e. "unknown-field tolerance") is not
established anywhere in this repository today. `ADR-038` itself states this precisely: *"it does
not assert or require any particular unknown-field-tolerance behavior of any consumer's reader."*
No schema validator implementation, JSON-Schema/Avro/Protobuf binding, or reader conformance rule
exists in the repository for these Event Contracts at this boundary.

**Feature compatibility assessment: cannot yet be evaluated — this fact is recorded, not a fabricated
result.** No Compatibility Result (Chapter 10 §10.4) is asserted, invented, or assumed here.

**Candle/Structure/Regime first-contract compatibility-policy status (all three families):** none
of the three has ever had a `compatibility_commitment` declared (no Event Contract of any kind
exists yet for any of them). Per Chapter 10 §10.3.1: *"published contract nằm trong phạm vi
compatibility evaluation mà KHÔNG khai báo chiều compatibility bắt buộc là invalid declaration →
không được chứng nhận compatible → `eligible = false`."* A `compatibility_commitment` declaration
is therefore an **independent publication prerequisite** for each of Candle's, Structure's, and
Regime's first Event Contract artifacts — exactly as `ADR-038` supplied that declaration for
Feature's first two artifacts. **This choice (backward-only / forward / bidirectional / no
commitment) is explicitly not made by this WP** — per the task's own instruction, and because
Chapter 10 requires it be a governed, explicit declaration, evaluated per family, not inferred by
analogy to Feature's own choice.

Under `ADR-039`, the first `Published` version-artifact for a `contract_id` with no prior snapshot
is authored, reviewed, and Product-Owner-decided through the **same governance process as the
owning Domain Contract itself** (Draft → Review A/Independent Review B → Product Owner decision),
fixed at `contract_version: v1.0`. This applies identically to Candle's, Structure's, and Regime's
first artifacts (§4.B above) and is **not itself an open question** — only the
`compatibility_commitment` value each family declares is.

## 5. STOP conditions — explicit disposition

No STOP condition was silently resolved by guessing. Explicit disposition per condition:

- **A. "Domain Contract causation semantics allow more than one legitimate interpretation":**
  triggered for `CANDLE_CORRECTED`'s lineage reference (§3.2) — recorded `UNRESOLVED`, not guessed.
- **B. "Deciding requires new consumer-specific semantics":** not triggered for any row — every
  classification above is derived from the producing event's own Domain Contract, not from any
  particular consumer's (including Context's) needs.
- **C. "Classification would contradict another consumer's existing governed use":** not
  triggered — no existing governed consumer classification exists to contradict (this is the
  first classification attempt for all 10 event types).
- **D. "Event Contract needs semantics not owned by its Domain Contract":** triggered for every
  `swing.md`-dependent category (§3.5, §3.9's Swing sub-category, §3.10) — recorded `UNRESOLVED`
  with the exact missing authority named, not guessed.
- **E. "Feature version evolution requires a compatibility choice/result not already governed":**
  triggered — recorded in §4.A as a versioning/compatibility prerequisite, no Compatibility Result
  fabricated.

## 6. ADR classification of unresolved semantic choices

| Unresolved item | Existing authority fully determines value? | Assessment |
|---|---|---|
| Same-family lineage-supersession causal-reference classification (`CANDLE_CORRECTED`, and structurally the same open question underlying why `structure.md`/`regime.md`/`feature.md` each had to work out their *own* invalidation-conditionality answer independently, §3.5/§3.8/§3.10) | **NO** | This is a **cross-cutting** gap in Chapter 8 §8.2.3's own classification framework, not a single Domain Contract's local ambiguity — it recurs, in some form, across every family with a self-referential correction/invalidation event (4 of 4 families). Affects more than one module's Event Contract authoring. Appears to trigger **`ADR_REQUIRED`** — a bounded ADR clarifying whether/how the STATE_DEPENDENCY/EXTERNAL_NON_STATE_CAUSE dichotomy extends to same-family lineage references (a third, currently unnamed shape), rather than a per-Domain-Contract local decision. Not created by this WP. |
| `swing.md`-dependent categories (§3.5, §3.9, §3.10) | **Cannot be assessed from this WP's own boundary** | This is not evidence of an architectural gap — it is evidence that this WP's own pinned reading set was deliberately bounded to exclude `swing.md`. The correct next step is a **follow-on derivation WP** that adds `swing.md` to its pinned reading, not an ADR. Likely **R2 routing** once resolved (same Risk classification as this WP and as the Context Input Contract itself), not `ADR_REQUIRED` — pending what `swing.md` actually says. |
| Candle/Structure/Regime `compatibility_commitment` value | **NO** | Chapter 10 §10.3.1 requires an explicit, governed declaration per family; existing authority supplies the *requirement* to declare, not the *value*. This is a normal, bounded **Product Owner decision** per family (the same shape `ADR-038` already recorded for Feature) — does not itself appear to require a new ADR, since `ADR-038`'s own precedent already establishes the mechanism; only the per-family value differs. |
| Feature `v1.0 → v1.1`/new-major versioning choice, and its Compatibility Result | **NO** | Requires a governed Compatibility Result evaluation (Chapter 10 §10.4) once concrete reader/format rules exist, and a Product Owner decision on the new version's own identity/scope. Not `ADR_REQUIRED` on its own evidence — this is ordinary Event-Contract-version governance under already-Approved `ADR-038`/`ADR-039`, not a new architecture choice. |

**No ADR is created by this WP.**

## 7. Proposed smallest ordered follow-on WP sequence (not executed here)

1. **Architecture-level ADR** (if the Product Owner chooses to pursue it): clarify Chapter 8
   §8.2.3's classification framework for same-family lineage-supersession causal references —
   resolves `CANDLE_CORRECTED` (§3.2) and supplies the general principle the other three families'
   own local invariants already answered ad hoc (§3.5/§3.8/§3.10 — each Domain Contract happened to
   settle its own version of this question independently; a platform-level principle would make
   that consistent and citable, rather than re-derived per family).
2. **Swing-inclusive re-derivation** (a narrowly-scoped follow-on to this WP, adding `swing.md` to
   its pinned reading): resolves the 3 remaining `UNRESOLVED` categories in §3.5/§3.10, and the
   Swing-evidence field-level detail in §3.9.
3. **Per-family `compatibility_commitment` decisions** (Product Owner, one per family): Candle,
   Structure, Regime — each a small, bounded decision, same shape as `ADR-038`.
4. **First Event Contract authoring, per family** (governed authoring, Draft → Review A/
   Independent Review B → Product Owner decision, per `ADR-039`): Candle (`candle-closed`,
   `candle-corrected`), Structure (`break-of-structure-detected`, `change-of-character-detected`,
   `structure-fact-invalidated`, `structure-recomputed`), Regime (`regime-classified`,
   `regime-fact-invalidated`) — each incorporating its own resolved state-dependency
   classification from steps 1–2 above.
5. **Feature Event Contract versioning** (`feature-computed`/`feature-fact-invalidated`
   `v1.0 → v1.1` or new major, per the outcome of step 1/2 and a governed Compatibility Result):
   adds the classification to Feature's two already-Published event types without editing the
   immutable `v1.0` artifacts.
6. **Fresh ChatGPT Review A of Context Input Contract `context-market-input / v1.0`'s
   `causal_closure_policy` readiness**, now backed by a fully-resolved per-effect classification
   across all 10 event types — the actual prerequisite for a `v1.0` publication decision.

## 8. Context Input Contract state — unchanged

`docs/architecture/input-contracts/context-market-input.yaml` is **not** touched by this
transaction. Confirmed state, fresh-verified: `version: "0.3"`, `status: Draft`, blob
`ce74ddf6291abb2b1ed21938ca88050550fb2a0b`; Review A `CLEAN — 0 Blocker / 0 Major / 0 Minor`, Risk
`R2`, ADR Scope `ADR_NOT_REQUIRED` for the candidate itself; Product Owner's already-made R2
advisory choice for this candidate is `PROCEED WITHOUT CROSS-CHECK` (no cross-check was executed;
none fabricated here); `NOT PUBLISHED`. The unresolved Event Contract/state-dependency prerequisite
derived in this WP remains the blocker to publication/runtime readiness — no PO approval of v0.3,
no publication authorization, and no residual-risk acceptance is recorded by this transaction.

## 9. Milestone state

M2: `BLOCKED` — parallel evidence lane. M3: `ACTIVE` — Context deterministic core `REVIEW A
VALIDATED — CLEAN`; `ADR-046` `APPROVED`; `context.md` v0.4 `PO ACCEPTED`; Context Input Contract
v0.3 `REVIEW A CLEAN — R2 — PROCEED WITHOUT CROSS-CHECK — NOT PUBLISHED`; current blocker: upstream
Event Contract / per-effect state-dependency authority derivation (this WP's own subject — now
analyzed, not yet remediated). M4: `QUEUED`. Phase-3 Approval Gate: `NOT REACHED`. LIVE:
`NOT_AUTHORIZED`.
