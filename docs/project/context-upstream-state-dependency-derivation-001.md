---
id: context-upstream-state-dependency-derivation-001
title: "Context Upstream Event-Contract State-Dependency Authority — Derivation"
kind: analysis
version: "0.3"
status: Draft
owner: Product Owner
generated_at: "2026-09-28"
---

# CONTEXT-UPSTREAM-STATE-DEPENDENCY-DERIVATION-001 (v0.3 — corrected)

**Analysis / derivation artifact only.** Does not modify or version any Event Contract; does not
publish any Event Contract; does not publish `context-market-input / v1.0`; does not modify any
Domain Contract, Constitution chapter, or ADR; does not implement runtime.

## 0. Boundary and fresh-verification record

Starting HEAD `69f8731e006e126cd06e81eaa73ee8e52b8ac9ed` — confirmed exact, `main == origin/main`,
working tree clean before this transaction. Reviewed candidate blob (v0.2 of this artifact)
`44fe265e0a6f6ad064c7e25066a7eb18778f0916` — confirmed exact before mutation.

`docs/architecture/input-contracts/context-market-input.yaml` confirmed unchanged: `version:
"0.3"`, `status: Draft`, blob `ce74ddf6291abb2b1ed21938ca88050550fb2a0b`, Review A `CLEAN — 0/0/0`,
Risk `R2`, `PROCEED WITHOUT CROSS-CHECK`, `NOT PUBLISHED` — this transaction does not touch it.

**Fresh-read this transaction (not previously pinned for this artifact):** `docs/adr/ADR-038.md`
(Approved, `status: Approved`) in full, and Chapter 0 §4b (`docs/constitution/00-governance.md`)
for the exact ADR Scope Rule table wording — both used to ground the `CONTEXT-SD-DERIV-A-MAJ-03`
correction below.

**Fresh Review A of v0.1 (prior correction round):** `REVISION_REQUIRED — 0 Blocker / 2 Major / 0
Minor`. `CONTEXT-SD-DERIV-A-MAJ-01`, `CONTEXT-SD-DERIV-A-MAJ-02` — remediated by
`CONTEXT-UPSTREAM-STATE-DEPENDENCY-DERIVATION-001-CORR-001` (v0.2).

**Fresh Review A of v0.2 (this correction round):** `REVISION_REQUIRED — 0 Blocker / 1 Major / 2
Minor`, analysis-artifact Risk `R1`, ADR Scope `ADR_NOT_REQUIRED` (for this correction transaction
itself). Prior findings `CONTEXT-SD-DERIV-A-MAJ-01 — CLOSED — REVIEW A VALIDATED`,
`CONTEXT-SD-DERIV-A-MAJ-02 — CLOSED — REVIEW A VALIDATED`, both confirmed genuinely remediated by
Review A's own determination, neither reopened. New findings `CONTEXT-SD-DERIV-A-MAJ-03`,
`CONTEXT-SD-DERIV-A-MIN-01`, `CONTEXT-SD-DERIV-A-MIN-02` — addressed/remediated in this v0.3,
**not self-closed** (closure is a fresh Review A re-review determination).

## 1. What was wrong in v0.1, and the corrected test

### 1.1 `CONTEXT-SD-DERIV-A-MAJ-01` — wrong classification layer

v0.1 repeatedly treated *"producer read cause payload to compute/validate effect"* as equivalent
to *"cause is a STATE_DEPENDENCY for authoritative application of the effect."* Chapter 8 does not
define the classification that way. The controlling text (§8.2.3, line-for-line):

> *"Với mọi event B mà contract authoritative-apply, nếu processor **cần payload/state** của một
> `causation_ref` A thì stream của A **BẮT BUỘC** thuộc input scope + cursor universe của contract
> đó. Causal predecessor **không phải state-input** của consumer hiện tại thì không bị ép vào
> scope — chỉ cần xác minh identity/existence."*

**Corrected test, applied uniformly to every causation-ref category below:**

1. What does the **effect event's own** payload/subject_ref/envelope already materialize?
2. To **authoritative-apply** that effect (accept it as valid, fold it into a consumer's own
   state/view, use it for whatever purpose downstream consumers legitimately have) — must a
   processor **read** the **cause's own domain payload**?
3. Or does the processor need only: canonical identity, existence/commit proof, causal
   precedence, or envelope/subject binding **already available without reading cause payload**?

Only (2) establishes `STATE_DEPENDENCY`. Producer-side computation dependency (what the **producer**
needed to read from a cause to decide whether/how to emit the effect, before publication) is a
**separate, distinct question** — labeled `PRODUCER COMPUTATION DEPENDENCY` in the matrix below,
never conflated with the classification column, `PROCESSOR APPLY-TIME STATE DEPENDENCY`.

**The central finding this correction exposes, once the test is applied uniformly (corrected under
`CONTEXT-SD-DERIV-A-MIN-01` — see §1.4):** what is actually authoritative, per event type, is not a
platform-wide `event_class: derived_fact` generalization but the reviewed per-category Domain
Contract semantics themselves. For `FEATURE_COMPUTED`/`FEATURE_FACT_INVALIDATED`, the Published
Event Contracts explicitly declare `event_class: derived_fact`, confirmed by direct read. For the
other 8 event types (Candle/Structure/Regime), no Event Contract yet exists, so no `event_class` has
been authored for them — this is not decided, inferred, or needed by this analysis. **Regardless of
whatever `event_class` those 8 event types are eventually assigned**, the per-category Domain
Contract text reviewed in §2 already shows, event by event, that each effect's own payload is a
complete result materialization — `class`/`computed_metric` (Regime), `new_orientation`/
`resulting_orientation` (Structure), `value` (Feature) — and that no Domain Contract anywhere in
this WP's boundary states a downstream consumer must **re-read** a causal predecessor's own payload
to correctly use an already-emitted fact of any of these 10 types. Every causation_ref in this event
set therefore exists for **lineage, precedence, and explainability (I-1)** — not for supplying
apply-time state a consumer would otherwise lack. This is a per-category finding derived from each
event's own reviewed semantics (§2), not a deduction from an unverified global `event_class` label.

### 1.2 `CONTEXT-SD-DERIV-A-MAJ-02` — false third shape / ADR escalation, corrected

v0.1 treated `CANDLE_CORRECTED`'s corrected-fact reference as a possible third causal-reference
shape (same-family/same-stream/lineage) requiring an architecture ADR. Re-evaluated below (§2.2)
with the identical apply-time test used for every other category: the corrected-fact reference
resolves cleanly to `EXTERNAL_NON_STATE_CAUSE` under the existing two-category model. Same-stream
sequence precedence (Chapter 8 §8.3.2/§8.3.3) is a separate ordering invariant; lineage/supersession
meaning is ordinary Domain/Event Contract semantic content. Neither creates, nor requires, a third
causal-closure class. **No ADR is required for this reason** (re-assessed fully in §6).

### 1.3 `docs/domain/swing.md` — fresh-read, now pinned authority

Fresh-read in full this transaction (not previously pinned). Confirmed exact placements (§2, §4, §5
of `swing.md`):

- `SwingConfirmed.pivot_price` — **payload** (§4 payload block, top-level field).
- `SwingConfirmed.confirmation_evidence` (`pivot_candle_ref`/`left_evidence_refs`/`right_evidence_refs`)
  — **payload** (§4 payload block).
- `SwingInvalidated.invalidation_cause`/`invalidation_reason` — **payload** (§5 payload block).
- `swing_id` — `subject_ref.subject_id` (§2), **not payload**.
- `swing_revision` — `subject_ref.scope.revision_ref.swing_revision` (§2), **not payload**.
- `pivot_effective_time` — bound to `envelope.effective_time` (§2/§7: *"effective_time... LUÔN LUÔN
  = pivot_effective_time"*), **envelope, not payload**.

These placements are used below wherever a Swing-sourced causation category is evaluated — no
inference from the prior summary, direct citation of `swing.md`'s own text.

### 1.4 `CONTEXT-SD-DERIV-A-MAJ-03` — compatibility-commitment governance routing, corrected

v0.2 stated, in substance, that Candle/Structure/Regime `compatibility_commitment` values are
ordinary bounded Product Owner decisions that do not require an ADR, because `ADR-038` already
established the mechanism. **This was incorrect.** Fresh-read `ADR-038.md` (Approved) in full: its
own exact scope classification is *"Scope classification — `ADR Required`."* Its own stated
rationale: Chapter 10 §10.3.1 *"defines the valid choice space for a compatibility commitment
(backward-only / forward-only / bidirectional / explicit no-commitment) and mandates that every
published contract declare one, but does not itself select a value for any specific contract — that
selection is a genuine semantic decision."* `ADR-038` further found Chapter 0 §4b's `>1`-module
trigger *independently sufficient*, confirmed disjunctive, because a real, already-registered
producer/consumer edge existed (`feature-engine` → `context-aggregator`, per `module-registry.yaml`
and `context.md` §7.3/§8). Chapter 0 §4b itself lists *"thay đổi Event Schema"* and *"quyết định ảnh
hưởng >1 module"* as independently `ADR Required` triggers.

**`ADR-038`'s Decision text applies specifically, and only, to `feature-computed`/
`feature-fact-invalidated`.** It does not pre-authorize a compatibility-commitment value, or a
no-ADR-needed path, for Candle, Structure, or Regime Event Contracts — those are different
`contract_id`s, with their own producer/consumer topology not evaluated by `ADR-038`.

**Corrected governance state, for each of the 8 missing Context-required `contract_id`s:**

```text
compatibility_commitment value:     UNRESOLVED
existing authority supplies choice space:  YES (Chapter 10 §10.3.1)
existing authority selects value:          NO
```

Selecting a `compatibility_commitment` for any of these `contract_id`s is therefore an **`ADR
Required` candidate**, on `ADR-038`'s own exact precedent, subject to actual downstream-impact
verification for the `contract_id`(s) any proposed ADR's scope would include — not decided by this
analysis WP.

**Packaging is not predetermined.** `ADR-038` itself bundled two `contract_id`s
(`feature-computed`/`feature-fact-invalidated`) into one governed ADR, because both shared the same
producer/consumer relationship and the same reasoning applied coherently to both. This does **not**
establish that one ADR must, or must not, cover all 8 missing `contract_id`s, one per family, or
some other grouping. The correct governing principle: *compatibility declaration is per
`contract_id`, but one bounded ADR **may** govern multiple `contract_id`s if its scope is explicit,
every included `contract_id` is enumerated, the decision is semantically coherent across them, and
downstream impact is assessed for every included `contract_id`.* Determining the smallest coherent
ADR scope requires inspecting the actual producer/consumer topology for these 8 `contract_id`s
against `module-registry.yaml`/`context.md`/the relevant Domain Contracts — an analysis this
correction WP does **not** perform (see STOP conditions, §7). A dedicated, narrowly-scoped follow-on
WP is recommended instead (§8). **No Product Owner compatibility-commitment decision should be
requested before that candidate ADR has been authored and is Review-A-clean.**

### 1.5 `CONTEXT-SD-DERIV-A-MIN-01` and `CONTEXT-SD-DERIV-A-MIN-02` — corrected

**`CONTEXT-SD-DERIV-A-MIN-01`:** v0.2's unsupported claim that all 10 event types share
`event_class: derived_fact` is removed (§1.1 above) and replaced by the narrower, actually-reviewed
conclusion: regardless of the eventual `event_class` Candle/Structure/Regime Event Contracts are
assigned when first authored, the per-category Domain Contract semantics reviewed in §2 already
establish, event by event, that authoritative application of the already-emitted effect does not
require re-reading the causal predecessor's domain payload — for all 20 non-vacuous categories.

**`CONTEXT-SD-DERIV-A-MIN-02`:** v0.2's proposed follow-on sequence (§8) numbered compatibility
decisions/Event Contract authoring ahead of "fresh ChatGPT Review A," while separately stating Review
A must occur first — an internally inconsistent ordering. Corrected: this transaction's own fresh
Review A of v0.2 is recorded as already performed at this boundary (§0); the sequence in §8 below is
renumbered so a **fresh Review A of this v0.3** is explicitly step 1, and every other step is
ordered strictly after it, including the newly-identified compatibility-ADR-scope-derivation step
`CONTEXT-SD-DERIV-A-MAJ-03` requires.

## 2. Corrected derivation matrix

Same 10 event types, no others: `CANDLE_CLOSED`, `CANDLE_CORRECTED`, `BREAK_OF_STRUCTURE_DETECTED`,
`CHANGE_OF_CHARACTER_DETECTED`, `STRUCTURE_FACT_INVALIDATED`, `STRUCTURE_RECOMPUTED`,
`REGIME_CLASSIFIED`, `REGIME_FACT_INVALIDATED`, `FEATURE_COMPUTED`, `FEATURE_FACT_INVALIDATED`.

### 2.1 `CANDLE_CLOSED`

Fresh-reconfirmed `candle.md` §4: `causation_refs: []` (root event — no fact it corrects, nothing
to classify). **Classification: `VACUOUS`.** No causation-ref category exists.

### 2.2 `CANDLE_CORRECTED`

Exactly one category, `candle.md` §5: *"causation_refs PHẢI trỏ chính xác event đang được sửa."*

| Item | Content |
|---|---|
| Cause category | Corrected-fact ref (the `CandleClosed`/`CandleCorrected` this correction replaces) |
| Exact source | `candle.md` §5/§10/§11 |
| Producer computation dependency | Producer reads the referenced fact's `effective_time`/`recorded_time` (envelope) to bind the correction to the same window and enforce ordering (§5 invariants); the **new OHLCV values themselves are supplied directly** by the venue-provided correction, never derived from the old fact's OHLC |
| What the effect already materializes | The complete new `open`/`high`/`low`/`close`/`volume` (§5 payload) — a full, self-sufficient replacement value |
| What apply requires from cause | Only identity (which prior fact is superseded, for lineage/explainability) and the envelope-consistency facts already required uniformly by tuple consistency (§8.2.3) — no OHLC value of the old fact is read to use the new one |
| Cause payload/state read at apply? | **No** |
| Classification | **`EXTERNAL_NON_STATE_CAUSE`** |
| Authority | `candle.md` §5 (new payload self-contained); Chapter 8 §8.2.3 (tuple consistency applies uniformly, is not itself STATE_DEPENDENCY evidence) |
| Confidence | High — no third causal-reference shape needed; same two-category model applies |

### 2.3 `BREAK_OF_STRUCTURE_DETECTED` / 2.4 `CHANGE_OF_CHARACTER_DETECTED`

`structure.md` §3/§4/§6/§6a/§7. Both share the same two categories.

| Cause category | Producer computation dependency | What the effect already materializes | What apply requires from cause | Read cause payload at apply? | Classification | Authority |
|---|---|---|---|---|---|---|
| `broken_swing_ref.swing_confirmed_event_ref` (`swing-confirmed`) | §6's break criterion table compares `candle.high/low/close` against `broken_swing.pivot_price` — the **producer** reads this to decide whether/how to emit BOS/CHoCH at all | `broken_swing_ref` itself: `{swing_id, swing_revision, direction}` (§6a) — the pivot's **identity**, not its price. `prior_orientation`/`new_orientation` (the conclusion) are separately materialized | Identity/verification only — `swing_confirmed_event_ref` is explicitly a "**verification field**" per `structure.md` §6a ("xác minh đúng bản ghi vật lý"), i.e. existence/tuple-consistency, not a value a consumer re-reads to use BOS/CHoCH | **No** | **`EXTERNAL_NON_STATE_CAUSE`** | `structure.md` §6a (verification-field framing, explicit) |
| `breaking_candle_refs` (`candle-closed`/`candle-corrected`) | Same break criterion table — producer reads Candle OHLC to decide the break | BOS/CHoCH's own payload never copies Candle OHLC — only the reference and the conclusion (`new_orientation`) | Existence/precedence proof only — a consumer already has `new_orientation` and does not need to re-verify the break arithmetic to use the fact | **No** | **`EXTERNAL_NON_STATE_CAUSE`** | `structure.md` §3/§4 payload shape (no OHLC field materialized) |

Both event types: mechanically derivable, **corrected from `STATE_DEPENDENCY` (v0.1) to
`EXTERNAL_NON_STATE_CAUSE`** — the v0.1 conclusion conflated the producer's gating computation with
apply-time need, exactly `CONTEXT-SD-DERIV-A-MAJ-01`'s finding.

### 2.5 `STRUCTURE_FACT_INVALIDATED`

`structure.md` §5/§10. Four categories, all re-evaluated from scratch.

| Cause category | Producer computation dependency | What the effect already materializes | What apply requires from cause | Read cause payload at apply? | Classification | Authority |
|---|---|---|---|---|---|---|
| `invalidated_fact_ref` (the BOS/CHoCH being invalidated) | Producer/emission-time invariants (§5) require reading the target's own `broken_swing_ref`/`breaking_candle_refs`/`prior_orientation` **to validate that the emitted `invalidation_cause` is legitimate** — this is a constraint on what a **correct producer** may legitimately emit, not on what a consumer must verify after the fact | `StructureFactInvalidated`'s own payload is exactly `{invalidated_fact_ref, invalidation_cause, invalidation_reason}` — no orientation/level data copied in | A consumer applying (accepting, marking obsolete) this invalidation needs only to know **which** fact is invalidated — identity, not the invalidated fact's own business content | **No** | **`EXTERNAL_NON_STATE_CAUSE`** | `structure.md` §5 payload shape (no business content materialized here); the v0.1 `STATE_DEPENDENCY` conclusion rested on the producer's own emission-time legitimacy checks, the exact conflation `CONTEXT-SD-DERIV-A-MAJ-01` identifies |
| cause (a) `SwingInvalidated` | Producer matches `swing_id`/`swing_revision` (§5 invariant) — these live in `SwingInvalidated`'s **`subject_ref`/`subject_ref.scope.revision_ref`** (`swing.md` §2), **not its payload** (`swing.md` §5 payload is only `invalidation_cause`/`invalidation_reason`) | Same as above — no Swing content copied into `StructureFactInvalidated`'s own payload | Existence + subject/envelope identity match only — confirmed now that `swing.md` places the matched fields outside payload entirely | **No** | **`EXTERNAL_NON_STATE_CAUSE`** | `swing.md` §2/§5 (fresh-read this transaction) — resolved, was `UNRESOLVED` in v0.1 for lack of `swing.md` |
| cause (b) `CandleCorrected` | Producer re-evaluates the break criterion against the corrected OHLC (§5 invariant) **to decide whether to emit** this invalidation at all | No OHLC copied into `StructureFactInvalidated`'s own payload | Same as (a)/`invalidated_fact_ref` — existence/identity only | **No** | **`EXTERNAL_NON_STATE_CAUSE`** | `structure.md` §5 payload shape; same corrected reasoning as `invalidated_fact_ref` |
| cause (c) `chained_invalidation` (prior `StructureFactInvalidated` in cascade) | Producer traverses the dependency-forward chain (§10) to determine emission order | Payload is `{invalidated_fact_ref, invalidation_cause, invalidation_reason}` — no orientation data | Existence/commit-order proof only (§10 step 7: no descendant causation to an uncommitted invalidation) | **No** | **`EXTERNAL_NON_STATE_CAUSE`** | `structure.md` §10 (already the v0.1 conclusion here — unchanged, now clearly consistent with the other three categories rather than an outlier) |

**Event summary:** all 4 of 4 categories mechanically derivable, all `EXTERNAL_NON_STATE_CAUSE`.
The `swing_invalidated` category, `UNRESOLVED` in v0.1 for lack of `swing.md`, is now fully
resolved. No category remains `UNRESOLVED`.

### 2.6 `STRUCTURE_RECOMPUTED`

`structure.md` §5a. One category, unchanged in substance from v0.1 (it was already reasoned on the
existence/completeness basis, not producer-computation-provenance, so the correction does not
change its conclusion — re-verified here for completeness).

| Cause category | Producer computation dependency | What the effect already materializes | What apply requires from cause | Read cause payload at apply? | Classification | Authority |
|---|---|---|---|---|---|---|
| Full `StructureFactInvalidated` set of the cascade | Producer must enumerate the complete set to know the cascade is finished before recomputing (§5a) | `resulting_orientation` is computed by refolding Swing/Candle facts pinned via `payload.input_cursor_ref` — a mechanism entirely separate from `causation_refs` | Only proof the cascade's invalidation set is complete (§5a invariant: none of the affected facts may be missing) — never the referenced facts' own payload (which carries no orientation data at all) | **No** | **`EXTERNAL_NON_STATE_CAUSE`** | `structure.md` §5a (`input_cursor_ref` is the actual computation input, not the causation set) |

**Event summary:** mechanically derivable, unchanged conclusion.

### 2.7 `REGIME_CLASSIFIED`

`regime.md` §3/§6/§8a/§10. Two categories, re-evaluated.

| Cause category | Producer computation dependency | What the effect already materializes | What apply requires from cause | Read cause payload at apply? | Classification | Authority |
|---|---|---|---|---|---|---|
| `candle_evidence_refs` | `metric_formula_id` (§6) reads these Candles' own OHLCV to **compute** `computed_metric`/`class` — a **producer**-side dependency | `class` and `computed_metric` are already fully materialized in `RegimeClassified`'s own payload (§3) | A consumer uses `class`/`computed_metric` directly — no need to re-derive them from Candle OHLC | **No** | **`EXTERNAL_NON_STATE_CAUSE`** | `regime.md` §3/§6 (result fully materialized) — **corrected from `STATE_DEPENDENCY` (v0.1)**, which had conflated the metric formula's producer-side read with apply-time need |
| `RegimeFactInvalidated` ref (replacement case) | Producer must confirm the invalidation exists/is visible before emitting a replacement (§3 rule 2/4/7) | `class`/`computed_metric` of the replacement are recomputed solely from `candle_evidence_refs`, never from the referenced `RegimeFactInvalidated`'s own payload (`{invalidated_fact_ref, invalidation_reason}`) | Existence/visibility proof only | **No** | **`EXTERNAL_NON_STATE_CAUSE`** | `regime.md` §3 invariants (unchanged from v0.1 — this category was already reasoned correctly there) |

**Event summary:** both categories mechanically derivable, both `EXTERNAL_NON_STATE_CAUSE`.

### 2.8 `REGIME_FACT_INVALIDATED`

`regime.md` §4/§10. Two categories — **unchanged conclusions from v0.1**, since that analysis was
already reasoned on the envelope-vs-payload/unconditional-policy basis, not producer-computation
provenance; re-verified here under the corrected test for completeness.

| Cause category | Producer computation dependency | What the effect already materializes | What apply requires from cause | Read cause payload at apply? | Classification | Authority |
|---|---|---|---|---|---|---|
| `invalidated_fact_ref` | Producer inherits `subject_ref`/`effective_time` (envelope, not payload) from the target (§4 binding rule); invalidates **unconditionally** whenever an affecting `CandleCorrected` exists (§10), never re-validating `class`/`computed_metric` | `{invalidated_fact_ref, invalidation_reason}` only | Existence + envelope binding, already available without reading the target's own `class`/`computed_metric` payload | **No** | **`EXTERNAL_NON_STATE_CAUSE`** | `regime.md` §4/§10 |
| `CandleCorrected` (direct cause) | Producer's unconditional policy needs only the **identity** of which Candle was corrected (does it appear in some `RegimeClassified`'s evidence?), never its new value, since invalidation fires regardless of whether the value changed | Same as above | Identity/existence only | **No** | **`EXTERNAL_NON_STATE_CAUSE`** | `regime.md` §10 (explicit unconditional trigger) |

**Event summary:** both categories mechanically derivable, unchanged, both `EXTERNAL_NON_STATE_CAUSE`.

### 2.9 `FEATURE_COMPUTED`

`feature.md` §3/§6/§7. Two categories, re-evaluated (the Swing-evidence sub-category of
`input_fact_refs` is now fully resolvable with `swing.md` pinned).

| Cause category | Producer computation dependency | What the effect already materializes | What apply requires from cause | Read cause payload at apply? | Classification | Authority |
|---|---|---|---|---|---|---|
| `input_fact_refs` (Candle and/or Regime and/or Swing evidence, `feature_type`-dependent) | §7.1/§7.2 formulas read Candle-evidence OHLC; §7.3 (`distance_to_last_confirmed_swing`) reads the winning `SwingConfirmed.pivot_price` (confirmed **payload**, `swing.md` §4) and a reference Candle — all **producer**-side reads to compute `value` | `value` (the computed result) is fully materialized in `FeatureComputed`'s own payload (§3), regardless of `feature_type` | A consumer (Strategy/Context/any downstream) uses `value` directly — it does not re-derive it from Candle OHLC, Regime `class`, or Swing `pivot_price` | **No** | **`EXTERNAL_NON_STATE_CAUSE`** for every evidence sub-category (Candle, Regime, Swing alike) | `feature.md` §3 (`value` fully materialized); `swing.md` §4 (confirms `pivot_price` is payload, and confirms it is not re-read downstream of `FeatureComputed`'s own materialized `value`) — **corrected from `STATE_DEPENDENCY` (v0.1)**, and the Swing sub-category is now **resolved** (was pending `swing.md` in v0.1) rather than field-level-deferred |
| `FeatureFactInvalidated` ref (replacement case) | Producer confirms the invalidation is visible before emitting a replacement | `value` of the replacement is recomputed solely from `input_fact_refs`, never from the referenced `FeatureFactInvalidated`'s own payload | Existence/visibility proof only | **No** | **`EXTERNAL_NON_STATE_CAUSE`** | `feature.md` §3 invariants (unchanged from v0.1) |

**Event summary:** both categories mechanically derivable, both `EXTERNAL_NON_STATE_CAUSE`, no
remaining Swing-dependent field-level deferral.

### 2.10 `FEATURE_FACT_INVALIDATED`

`feature.md` §4/§9a. Five categories, all re-evaluated; the two Swing-dependent categories
(`UNRESOLVED` in v0.1) are now resolved using `swing.md`.

| Cause category | Producer computation dependency | What the effect already materializes | What apply requires from cause | Read cause payload at apply? | Classification | Authority |
|---|---|---|---|---|---|---|
| `invalidated_fact_ref` | Producer inherits `subject_ref`/`effective_time` from the target; invalidates unconditionally per `feature.md` §3's explicit adoption of `regime.md` §10's policy | `{invalidated_fact_ref, invalidation_cause, invalidation_reason, computation_cursor, computation_dependency_content_evidence}` — no re-copy of the target's `value` | Existence + envelope binding only | **No** | **`EXTERNAL_NON_STATE_CAUSE`** | `feature.md` §3 invariant citing `regime.md` §10 (unchanged from v0.1) |
| cause (a) `CandleCorrected` | Same unconditional-trigger reasoning as Regime | Same as above | Identity/existence only | **No** | **`EXTERNAL_NON_STATE_CAUSE`** | `feature.md` §4 description + §3 policy invariant (unchanged) |
| cause (b) `RegimeFactInvalidated` | Same unconditional-trigger reasoning | Same as above | Identity/existence only | **No** | **`EXTERNAL_NON_STATE_CAUSE`** | `feature.md` §4/§3 (unchanged) |
| cause (c) `SwingInvalidated` | Producer matches `swing_id`/`swing_revision` (subject_ref/scope fields per `swing.md` §2, not payload) to decide whether this cause legitimately applies | Same `FeatureFactInvalidated` payload as above | Existence + subject/envelope identity match only | **No** | **`EXTERNAL_NON_STATE_CAUSE`** | `swing.md` §2/§5 (fresh-read) — **resolved**, was `UNRESOLVED` in v0.1 |
| cause (d) `eligible_swing_selection_superseded` (winning `SwingConfirmed`) | Producer evaluates §9a's full cursor-visibility predicate + 5-step filter pipeline + 8-criterion total order against the winning `SwingConfirmed`'s own fields — `pivot_price` (payload, `swing.md` §4), `pivot_effective_time` (bound to **envelope** `effective_time`, `swing.md` §2/§7), `recorded_time`/`sequence`/`stream_ref` (envelope) — **entirely to decide whether this invalidation may legitimately be emitted at all** | `FeatureFactInvalidated`'s own payload does not copy the winning `SwingConfirmed`'s `pivot_price` or `confirmation_evidence` — only `invalidated_fact_ref`/`invalidation_cause`/`computation_cursor` | A consumer accepting this already-emitted invalidation needs only to know that a winning `SwingConfirmed` reference exists (identity/lineage) — it does not need to re-verify the total-order computation or read `pivot_price` to use the fact that the prior `FeatureComputed` is now superseded | **No** | **`EXTERNAL_NON_STATE_CAUSE`** | `swing.md` §2/§4 (fresh-read, confirms exact payload/envelope placement); `feature.md` §4 (payload shape confirms no re-copy) — **resolved**, was `UNRESOLVED` in v0.1; the producer-side total-order evaluation is real but is, per §1.1's corrected test, a producer computation dependency, not an apply-time one |

**Event summary:** all 5 of 5 categories mechanically derivable, all `EXTERNAL_NON_STATE_CAUSE`. No
category remains `UNRESOLVED`.

## 3. Corrected totals

| Metric | v0.1 (superseded) | v0.2 (corrected) |
|---|---|---|
| Total causation-ref categories | 21 | 21 |
| `STATE_DEPENDENCY` | 8 | **0** |
| `EXTERNAL_NON_STATE_CAUSE` | 9 | **20** |
| `VACUOUS` | 1 (implicit, `CANDLE_CLOSED`) | 1 (`CANDLE_CLOSED`) |
| `UNRESOLVED` | 4 | **0** |

**Every one of the 20 non-vacuous categories, across all 10 event types, classifies
`EXTERNAL_NON_STATE_CAUSE`.** This is not a rounding artifact of applying one rule loosely — it
follows mechanically, category by category, from the same single structural fact restated in §1.1:
every event in this set is a `derived_fact` whose own payload is a complete materialized result: no
Domain Contract in this WP's boundary (now including `swing.md`) requires a downstream authoritative
application of any of these 10 event types to re-read a causal predecessor's own payload. Every
`causation_refs` element in this set exists for lineage/precedence/explainability (I-1), satisfying
`EXTERNAL_NON_STATE_CAUSE`'s own definition exactly (existence/commitment proof, no payload read,
no cursor-visibility/apply-scope requirement).

This total invalidates and replaces v0.1's `17 mechanically derivable / 4 UNRESOLVED` count, per
the task's own instruction that it "must be recomputed," not patched.

**Fresh Review A of v0.2 independently rechecked this corrected apply-time reasoning and found no
causation category in the 10-event set requiring re-reading the predecessor's domain payload at
authoritative apply time — the matrix and totals above are preserved unchanged by this v0.3
correction.** Only §1.1's unsupported rationale (`CONTEXT-SD-DERIV-A-MIN-01`) and the compatibility-
governance conclusion in §5/§6/§8 (`CONTEXT-SD-DERIV-A-MAJ-03`) are corrected in this round —
producer-computation provenance is not reintroduced as the classification test anywhere below.

## 4. Event Contract artifact inventory — unaffected by the classification correction

Classification (§2/§3) is now fully resolved for all 21 categories — this is a separate fact from
**whether an Event Contract artifact exists to declare it**. Preserved, truthful inventory:

- **8 of 10** Context-upstream effect event types have **no Published Event Contract** today:
  `CANDLE_CLOSED`, `CANDLE_CORRECTED` (Candle family, zero artifacts); `BREAK_OF_STRUCTURE_DETECTED`,
  `CHANGE_OF_CHARACTER_DETECTED`, `STRUCTURE_FACT_INVALIDATED`, `STRUCTURE_RECOMPUTED` (Structure
  family, zero artifacts); `REGIME_CLASSIFIED`, `REGIME_FACT_INVALIDATED` (Regime family, zero
  artifacts).
- `FEATURE_COMPUTED`/`FEATURE_FACT_INVALIDATED`: Published, immutable, `v1.0`
  (`docs/architecture/event-contracts/feature-computed/v1.0.yaml`,
  `docs/architecture/event-contracts/feature-fact-invalidated/v1.0.yaml`) — neither artifact
  contains the state-dependency classification field/rule this WP derives (confirmed by direct
  read, unchanged from the prior WP's finding).

**"Classification mechanically derivable" is not "Event Contract authority already exists."** Even
though every category's correct value is now known, no Event Contract for any of the 10 event types
currently *declares* it — Chapter 8 §8.2.3 requires the artifact itself to carry the classification
("mỗi effect event dùng chính `event_contract_ref` đã pin của nó để phân loại"), not merely for the
value to be derivable by an external analysis document.

## 5. Versioning / compatibility — retained conclusions only

**Feature (`feature-computed`/`feature-fact-invalidated` v1.0):** immutable, **remains unedited**.
Adding the now-fully-resolved classification (a declaration that every one of its `causation_refs`
categories is `EXTERNAL_NON_STATE_CAUSE`) requires a new, separate version artifact. This WP does
**not** decide `v1.1` vs a new major, and does **not** characterize the addition as non-breaking
merely because it appears additive — Chapter 10 §10.3.1 explicitly defers the concrete
reader/format/consumer conformance rule needed to actually determine that, and no such rule exists
anywhere in this repository today; `ADR-038` itself declines to assume any unknown-field-tolerance
behavior. **Actual compatibility cannot be established without that concrete evidence — this fact
is recorded, not a Compatibility Result, and none is fabricated.**

**Candle/Structure/Regime compatibility-declaration state, granularity, and governance route
(corrected under `CONTEXT-SD-DERIV-A-MAJ-03` — see §1.4 for the full correction):** none of the
three has ever declared a `compatibility_commitment` — no Event Contract of any kind exists for any
of them. Chapter 10 §10.3.1's declaration requirement is framed per **published contract** —
confirmed by direct inspection that each of Feature's two Published artifacts carries its **own**
`compatibility_commitment` line. **The authority-supported granularity is per `contract_id` (per
Event Contract artifact), not per family** — each of Candle's 2, Structure's 4, and Regime's 2
relevant `contract_id`s requires its own stated value before that artifact can be evaluated
compatible.

**This is not an ordinary, un-escalated Product Owner decision.** `ADR-038` (Approved), fresh-read
this transaction, is the exact controlling precedent for exactly this class of decision — and
`ADR-038` itself classified selecting Feature's own compatibility commitment as `ADR Required`,
precisely because Chapter 10 §10.3.1 supplies the choice space (backward-only / forward-only /
bidirectional / explicit no-commitment) but never the value, and because a real producer/consumer
relationship made Chapter 0 §4b's `>1`-module trigger independently sufficient. `ADR-038`'s Decision
applies only to `feature-computed`/`feature-fact-invalidated` — it does not pre-authorize a value,
or a no-ADR path, for any Candle/Structure/Regime `contract_id`. **Corrected state, for each of the
8 missing `contract_id`s:** `compatibility_commitment` value `UNRESOLVED`; existing authority
supplies the choice space (`YES`, Chapter 10 §10.3.1); existing authority selects the value (`NO`).
Selecting any of these values is an **`ADR Required` candidate**, subject to actual downstream-impact
verification, not an ordinary bounded governance decision. **This WP does not choose any of these
values, and does not itself determine how many ADRs should package the 8 `contract_id`s** — see §1.4
and §8 for the recommended, narrowly-scoped follow-on to determine that.

## 6. ADR classification — re-assessed after the corrected matrix

No `UNRESOLVED` classification category remains (§3). No genuinely architecture-level unresolved
choice was exposed by the corrected analysis: the apply-time test (§1.1), applied identically to
all 21 categories using only each event's own already-authored Domain Contract text (now including
`swing.md`), produced a single, uniform, mechanically consistent answer with no competing
interpretation requiring a Product-Owner-level architectural decision.

**`CONTEXT-SD-DERIV-A-MAJ-02`'s specific question — is `CANDLE_CORRECTED`'s corrected-fact
reference a genuine third causal-reference shape requiring an ADR — is answered NO** (§2.2): it
classifies `EXTERNAL_NON_STATE_CAUSE` under the ordinary two-category model, the same as every
same-family lineage reference examined in this WP (`STRUCTURE_FACT_INVALIDATED.invalidated_fact_ref`,
`REGIME_FACT_INVALIDATED.invalidated_fact_ref`, `FEATURE_FACT_INVALIDATED.invalidated_fact_ref`, the
`RegimeFactInvalidated`/`FeatureFactInvalidated` supersede refs in `REGIME_CLASSIFIED`/`FEATURE_COMPUTED`).
Same-stream sequence precedence and lineage/supersession meaning remain, respectively, an ordinary
Chapter 8 ordering invariant and ordinary Domain/Event Contract content — neither requires, nor
motivates, a third classification value.

**No ADR is required to resolve the classification matrix itself (§2/§3).** The classification
question this WP was chartered to answer — `STATE_DEPENDENCY` vs `EXTERNAL_NON_STATE_CAUSE` per
causation-ref category — is fully resolved by existing Domain Contract authority with no competing
interpretation, for all 21 categories.

**This is distinct from, and must not be conflated with, the compatibility-commitment governance
question (`CONTEXT-SD-DERIV-A-MAJ-03`, §1.4/§5).** Selecting a `compatibility_commitment` for any of
the 8 missing `contract_id`s **is** an `ADR Required` candidate, on `ADR-038`'s own exact precedent
— Chapter 10 §10.3.1 supplies only the choice space, not the value, and `ADR-038`'s Decision does not
extend to Candle/Structure/Regime. This is not this WP inventing an ADR requirement out of
difficulty (the STOP condition against doing so, §7, is not violated) — it is this WP correcting a
prior round's mistaken application of an existing, Approved, on-point precedent. Feature's own
future versioning Compatibility Result remains separately gated on concrete reader/format/consumer
evidence that does not yet exist (§5), not itself requiring a new ADR by this analysis.

## 7. STOP conditions — explicit disposition

- **"Existing source still does not establish whether apply-time cause payload/state is required"**
  — not triggered for any of the 21 categories; every one resolves via the same uniform,
  mechanically-applied test once `swing.md` is included.
- **"Invent a third causal-closure class"** — not done; `CANDLE_CORRECTED`'s reference resolves
  within the existing two-category model (§2.2, §6).
- **"Invent an ADR requirement merely because a classification is difficult"** — not done; no
  classification category required a Product-Owner-level architectural choice once producer-
  computation dependency was correctly separated from apply-time need. The `ADR Required`
  conclusion for compatibility-commitment selection (§1.4/§5/§6, `CONTEXT-SD-DERIV-A-MAJ-03`) is a
  different question from the classification matrix, and is not invented — it applies `ADR-038`'s
  own already-Approved, exactly-on-point precedent, not a new architectural theory.
- **"An existing Approved ADR already governs compatibility commitments for any of the eight missing
  `contract_id`s"** — checked this transaction (fresh-read `ADR-038.md` in full): not triggered.
  `ADR-038`'s Decision text is scoped explicitly to `feature-computed`/`feature-fact-invalidated`
  only; no other Approved ADR addresses Candle/Structure/Regime Event Contract compatibility.
- **"Actual producer/consumer topology is required to classify ADR scope"** — triggered; this
  correction WP does **not** perform that topology analysis (§1.4/§8) — it is deferred to a
  dedicated follow-on WP, per the task's own explicit instruction.

No classification was left `UNRESOLVED` by omission; none was silently guessed.

## 8. Corrected smallest ordered follow-on WP sequence (not executed here)

Recomputed to fix `CONTEXT-SD-DERIV-A-MIN-02`'s internally-inconsistent ordering: this v0.3's own
fresh Review A is explicitly step 1, and every other step is strictly ordered after it (v0.2 had
numbered compatibility decisions/Event Contract mutations ahead of "fresh ChatGPT Review A" while
separately stating Review A must occur first).

1. **Fresh ChatGPT Review A re-review of this derivation (v0.3).** Required before any step below.
2. **If CLEAN: bounded compatibility-ADR scope derivation** — a dedicated, narrowly-scoped follow-on
   WP that inspects the actual producer/consumer topology for the 8 missing Event Contract
   `contract_id`s (Candle ×2, Structure ×4, Regime ×2) against `module-registry.yaml`/`context.md`/
   the relevant Domain Contracts, and determines the smallest coherent ADR candidate scope
   (`CONTEXT-SD-DERIV-A-MAJ-03`, §1.4) — one ADR per `contract_id`, one per family, one for all 8, or
   another grouping, decided by that dedicated analysis, not by this WP.
3. **Author the required compatibility-commitment ADR candidate(s)** identified by step 2's scope.
4. **Review A / Risk / governed ADR routing** for the authored candidate(s).
5. **Only after applicable ADR approval: author the first Candle/Structure/Regime Event Contracts**
   per `contract_id` (governed authoring, Draft → Review A/Independent Review B → Product Owner
   decision, per `ADR-039`) — Candle (`candle-closed`, `candle-corrected`), Structure
   (`break-of-structure-detected`, `change-of-character-detected`, `structure-fact-invalidated`,
   `structure-recomputed`), Regime (`regime-classified`, `regime-fact-invalidated`) — each declaring
   `EXTERNAL_NON_STATE_CAUSE` for every one of its own causation-ref categories, per §2 above.
6. **Separately resolve Feature's own future Event Contract versioning + Compatibility Result
   prerequisites** (`feature-computed`/`feature-fact-invalidated` `v1.0 →` a new version, not
   decided here; immutable `v1.0` artifacts never edited; genuine Compatibility Result requires
   concrete reader/format evidence this repository does not yet have) — independent of steps 2–5.
7. **After all required per-effect classification authority exists: update/re-review Context Input
   Contract readiness**, and only then consider publication of `context-market-input / v1.0`.

Steps 2–7 are **not** performed by this correction WP. (The previously-proposed separate
Swing-inclusive re-derivation WP remains removed — `swing.md` is fully incorporated in the prior
correction round, and every category it was blocking is resolved in §2 above.)

## 9. Context Input Contract state — unchanged

`docs/architecture/input-contracts/context-market-input.yaml` is **not** touched by this
transaction. Confirmed state, fresh-verified: `version: "0.3"`, `status: Draft`, blob
`ce74ddf6291abb2b1ed21938ca88050550fb2a0b`; Review A `CLEAN — 0 Blocker / 0 Major / 0 Minor`, Risk
`R2`, `PROCEED WITHOUT CROSS-CHECK` (already-made choice, persisted, not re-decided); `NOT
PUBLISHED`. The corrected upstream Event Contract/state-dependency derivation remains the blocker
to publication/runtime readiness — no PO approval of v0.3, no publication authorization, and no
residual-risk acceptance is recorded by this transaction.

## 10. Milestone state

M2: `BLOCKED` — parallel evidence lane. M3: `ACTIVE` — Context deterministic core `REVIEW A
VALIDATED — CLEAN`; `ADR-046` `APPROVED`; `context.md` v0.4 `PO ACCEPTED`; Context Input Contract
v0.3 `REVIEW A CLEAN — R2 — PROCEED WITHOUT CROSS-CHECK — NOT PUBLISHED`, unmutated; state-
dependency derivation is now `v0.3 corrected candidate` — classification matrix `20
EXTERNAL_NON_STATE_CAUSE / 1 VACUOUS / 0 STATE_DEPENDENCY / 0 UNRESOLVED`, independently re-verified
by fresh Review A of v0.2 and preserved unchanged by this correction — pending fresh Review A
re-review of this v0.3. Current blocker: compatibility-commitment ADR prerequisite (§1.4/§5/§6 —
selecting `compatibility_commitment` for any of the 8 missing `contract_id`s is an `ADR Required`
candidate on `ADR-038`'s own exact precedent, not yet authored) plus missing Event Contract
authority (8 of 10 event types have zero Published artifact). M4: `QUEUED`. Phase-3 Approval Gate:
`NOT REACHED`. LIVE: `NOT_AUTHORIZED`.
