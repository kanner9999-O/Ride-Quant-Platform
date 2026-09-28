---
id: context-event-contract-compatibility-adr-scope-001
title: "Compatibility-Commitment ADR Scope Derivation — Missing Context-Upstream Event Contracts"
kind: analysis
version: "0.2"
status: Draft
owner: Product Owner
generated_at: "2026-09-28"
---

# CONTEXT-EVENT-CONTRACT-COMPAT-ADR-SCOPE-001

**Analysis / scope-derivation artifact only.** Does not choose any `compatibility_commitment`
value; does not author an ADR; does not author or publish any Event Contract; does not modify any
Input Contract; does not change module/domain topology.

## 0. Boundary and fresh-verification record

Starting HEAD `129e08a699291445568c79c489969536b3318682` — confirmed exact, `main == origin/main`,
working tree clean before this transaction.

`docs/project/context-upstream-state-dependency-derivation-001.md` confirmed matched pinned blob
`3b474c702b9b8c7d122438258451f8eaab6ab860` exactly (`version: "0.3"`) before this transaction's own
`CONTEXT-SD-DERIV-A-MIN-03` deterministic wording fold-in, which bumps it to `0.4` (new blob
`a8b10628f4c156f67b25d18868dec4d6434971d9`, confirmed after).

`docs/architecture/input-contracts/context-market-input.yaml` confirmed unchanged: `version:
"0.3"`, `status: Draft`, blob `ce74ddf6291abb2b1ed21938ca88050550fb2a0b`, Review A `CLEAN — 0/0/0`,
Risk `R2`, `PROCEED WITHOUT CROSS-CHECK`, `NOT PUBLISHED` — this transaction does not touch it.

Fresh-read in full this transaction: `docs/adr/ADR-038.md` (blob
`ef931de871786ccd27119528b680d4d85e06c9f2`), Chapter 0 §4b (`docs/constitution/00-governance.md`,
blob `30fec19d299e3a2455d30c8c19315f4f141834f9`), Chapter 10 §10.3/§10.3.1/§10.7
(`docs/constitution/10-compatibility-capability-contract.md`, blob
`016e46bcad0826e983a51ee24c8ec4c3217aeba1`), Chapter 8 Event Contract authority
(`docs/constitution/08-event-model.md`, blob `4a27db556e6ee8f9b7ac085194a10c63677b035f`),
`docs/architecture/module-registry.yaml` (blob `8535f92efeb76ffb226791d201dc0b3fb71f06c0`),
`docs/domain/context-map.yaml` (blob `d2813e774093eb9c7510f9e41955612240726f89`),
`docs/domain/candle.md`, `docs/domain/swing.md`, `docs/domain/structure.md`,
`docs/domain/regime.md`, `docs/domain/feature.md`, `docs/domain/context.md` (all six blobs
confirmed unchanged from every prior WP that fresh-read them this session, cross-verified again
here). Fresh-read this correction transaction: `docs/constitution/11-adr-process.md` (§11.3,
§11.8's `supersedes` whole-file relation) — not previously pinned for this artifact.

**Fresh Review A of v0.1:** `REVISION_REQUIRED — 0 Blocker / 1 Major / 1 Minor`, Risk `R1`, ADR
Scope `ADR_NOT_REQUIRED`. Findings `CONTEXT-COMPAT-SCOPE-A-MAJ-01` (Model C rejection overreach —
architectural/domain independence was treated as an ADR-packaging prohibition, which no cited
authority actually states) and `CONTEXT-COMPAT-SCOPE-A-MIN-01` (false registry-edge documentation
gap — `feature-engine.depends_on: [structure-engine]` is fully corroborated via Swing consumption,
not an unresolved inconsistency) — both addressed/remediated in this v0.2, **not self-closed**
(closure is a fresh Review A re-review determination).

## A. Authority basis

**Chapter 8, line 257 (authority-division table):** *"Event class / payload / semantic / stream
eligibility → Event Contract."* Each Event Contract, once authored, is the sole owner of its own
`event_class`, payload shape/semantic, and `allowed_streams`. §8.6 delegates compatibility/schema
versioning rules to Chapter 10, not defining them itself.

**Chapter 10 §10.3.1:** defines the valid compatibility-commitment choice space
(`backward-only`/`forward-only`/`bidirectional`/`explicit no-commitment`) and *mandates* every
published contract declare one — but **does not itself select a value for any specific contract**.
An undeclared compatibility direction on a contract in evaluation scope is an *invalid
declaration* → `eligible = false` (fail-closed, I-6).

**Chapter 10 §10.7 (downstream impact assessment):** *"Assessment phải resolve được tập consumer
đang pin phiên bản/contract bị ảnh hưởng"* — minimum factors include the **dependency graph** (who
pins what) and **output semantic**. If the consumer set cannot be resolved, `eligibility = false`
by default (I-6) — never assumed compatible. This WP's own §B below is exactly this required
consumer-set resolution, performed once per `contract_id`, ahead of any eventual compatibility
decision.

**Chapter 0 §4b (ADR Scope Rule):** *"quyết định ảnh hưởng >1 module... → Bắt buộc"* (ADR Required)
— independently sufficient, disjunctive from other triggers (same reading `ADR-038` itself relied
on, citing `ADR-025`'s precedent).

**`ADR-038`'s exact, fresh-read precedent (Approved, `docs/adr/ADR-038.md`):**
- *"Scope classification — `ADR Required`."*
- *"Chapter 10 §10.3.1 defines the valid choice space for a compatibility commitment... but does
  not itself select a value for any specific contract — that selection is a genuine semantic
  decision this repository has not yet made."*
- *"[Chapter 0 §4b]'s `>1` module trigger is independently sufficient... `feature-engine` publishes
  `FeatureComputed`/`FeatureFactInvalidated`; `context-aggregator` consumes both (confirmed edge,
  `module-registry.yaml` + `context.md`) — a compatibility commitment governing what future schema
  evolution may assume about that already-active consumer relationship affects more than one
  module by construction."*
- The Decision is scoped explicitly and only to the two enumerated `contract_id`s
  (`feature-computed`, `feature-fact-invalidated`) it bundles into one ADR — establishing that one
  ADR *may* govern more than one `contract_id` when scope is explicit, every included `contract_id`
  is enumerated, and the reasoning is coherent across them (both share the same producer, the same
  owning Domain Contract, and the same confirmed consumer edge).

**`docs/architecture/module-registry.yaml` (v1.7):** owns module identity/taxonomy/`depends_on`
edges — **topology corroboration only**, per this WP's own explicit event-level-evidence-first
rule; a `depends_on` edge is never itself proof that a specific event type is consumed.

**`docs/domain/context-map.yaml`:** owns the authoritative, `contract_id`-level
`provider_context_id → consumer_context_id` relationship inventory (`relationships:` section) —
the single most precise, already-governed evidence source for exactly which context/module
consumes exactly which event type. Used here as the **primary** event-level evidence, cross-checked
against each owning Domain Contract's own `events_consumed`/"Input contracts" section.

## B. Per-contract topology matrix

All eight rows fresh-verified against `context-map.yaml`'s own `relationships:` entries (exhaustive
grep confirmed exactly 16 relationship entries exist for these 8 `contract_id`s — 4+4+1+1+1+1+2+2
— no more, no fewer) and cross-checked against each owning Domain Contract's own text.

### B.1 `candle-closed`

1. Owning Domain Contract: `candle.md` (§4).
2. Producer module: `market-data-ingestion`.
3. Producer capability/context: `market-data` / `market-data-observation`.
4. Current direct consumers (event-level, `context-map.yaml`): `market-structure-analysis`
   (`structure-engine`), `raw-regime-analysis` (`raw-regime-engine`), `feature-engineering`
   (`feature-engine`), `context-projection` (`context-aggregator`) — **4 consumer contexts**.
5. Domain Contract evidence: `structure.md` §12 (*"Structure tiêu thụ... candle-closed,
   candle-corrected"*); `regime.md` §13 (*"Raw Regime tiêu thụ chính xác hai contract...
   candle-closed, candle-corrected"*); `feature.md` §14 (*"candle-closed — ...(path candle);
   distance_to_last_confirmed_swing (giá tham chiếu)"*); `context.md` §16 (*"candle-closed —
   cadence/cutoff driver"*).
6. `module-registry.yaml` corroboration: `structure-engine.depends_on` includes
   `market-data-ingestion`; `raw-regime-engine.depends_on` includes `market-data-ingestion`;
   `feature-engine.depends_on` includes `market-data-ingestion`; `context-aggregator.depends_on`
   includes `market-data-ingestion` — all four edges present, all four corroborated by event-level
   evidence.
7. Registry edges not corroborating this specific event: none for this `contract_id`.
8. Downstream blast radius: widest of all 8 — 4 consumer modules across all three independent
   analytical families plus the projection layer.
9. Chapter 0 §4b `>1`-module trigger: **applies independently** (5 modules total: 1 producer + 4
   consumers).
10. Compatibility commitment already governed: **NO** — no Event Contract exists for
    `candle-closed`.
11. Missing decision: `compatibility_commitment` value for `candle-closed`.

### B.2 `candle-corrected`

1. Owning Domain Contract: `candle.md` (§5).
2. Producer module: `market-data-ingestion`.
3. Producer capability/context: `market-data` / `market-data-observation`.
4. Current direct consumers: identical set to B.1 — `market-structure-analysis`,
   `raw-regime-analysis`, `feature-engineering`, `context-projection` — **4 consumer contexts**
   (confirmed by 4 separate `context-map.yaml` relationship entries, each carrying its own
   `consumer_obligation` for invalidate/recompute).
5. Domain Contract evidence: same four citations as B.1, each Domain Contract's own text pairs
   `candle-closed`/`candle-corrected` identically.
6. `module-registry.yaml` corroboration: identical to B.1 — all four edges present and
   corroborated.
7. Registry edges not corroborating this specific event: none.
8. Downstream blast radius: identical to B.1 — 4 consumer modules.
9. Chapter 0 §4b `>1`-module trigger: **applies independently** (5 modules total).
10. Compatibility commitment already governed: **NO**.
11. Missing decision: `compatibility_commitment` value for `candle-corrected`.

### B.3 `break-of-structure-detected`

1. Owning Domain Contract: `structure.md` (§3).
2. Producer module: `structure-engine`.
3. Producer capability/context: `market-structure` / `market-structure-analysis`.
4. Current direct consumers: **`context-projection` (`context-aggregator`) only** — exactly one
   `context-map.yaml` relationship entry exists for this `contract_id`.
5. Domain Contract evidence: `context.md` §16 (*"break-of-structure-detected — Structure role
   (§7.1)"*). `feature.md` §14 **explicitly excludes it**: *"Không tiêu thụ:... bất kỳ Structure
   event nào (`BreakOfStructureDetected`/`ChangeOfCharacterDetected`/`StructureFactInvalidated`/
   `StructureRecomputed`)..."* — confirmed, not inferred.
6. `module-registry.yaml` corroboration: `context-aggregator.depends_on` includes
   `structure-engine` — corroborated.
7. **Registry edge scope, corrected (`CONTEXT-COMPAT-SCOPE-A-MIN-01`):** `feature-engine.depends_on`
   also includes `structure-engine` — this edge **is fully corroborated**, not a non-corroborating
   registry gap. `structure-engine` is the single registered module boundary for **both** Swing and
   Structure analytical output (`structure-engine.responsibilities`: *"Suy diễn Swing/BOS/CHoCH và
   structure semantics từ Candle"*), and `feature.md` §14/`context-map.yaml`'s own
   `market-structure-analysis → feature-engineering` relationship entries confirm Feature genuinely
   consumes `swing-confirmed`/`swing-invalidated` produced by this same module — this alone fully
   corroborates the `depends_on` edge. It is **not** evidence that Feature consumes any of the four
   Structure Event Contracts (`break-of-structure-detected`/`change-of-character-detected`/
   `structure-fact-invalidated`/`structure-recomputed`) — `feature.md` §14 explicitly excludes all
   four, and `context-map.yaml` records no relationship entry targeting `feature-engineering` for
   any of them. A single module-level `depends_on` edge can legitimately corroborate one event
   family (Swing) while remaining silent on another (the four Structure events) produced by the
   very same module — exactly why module-level `depends_on` must never be read as proof of
   consumption for one specific `contract_id` (§A).
8. Downstream blast radius: 1 consumer module (`context-aggregator`).
9. Chapter 0 §4b `>1`-module trigger: **applies independently** (2 modules: producer
   `structure-engine` + consumer `context-aggregator` — the identical minimum-cardinality shape
   `ADR-038` itself found sufficient for Feature's own two `contract_id`s).
10. Compatibility commitment already governed: **NO**.
11. Missing decision: `compatibility_commitment` value for `break-of-structure-detected`.

### B.4 `change-of-character-detected`

1. Owning Domain Contract: `structure.md` (§4).
2. Producer module: `structure-engine`.
3. Producer capability/context: `market-structure` / `market-structure-analysis`.
4. Current direct consumers: **`context-projection` only** (one relationship entry).
5. Domain Contract evidence: `context.md` §16 (*"change-of-character-detected — Structure role"*);
   `feature.md` §14 exclusion (same citation as B.3).
6. `module-registry.yaml` corroboration: `context-aggregator.depends_on` includes
   `structure-engine` — corroborated.
7. Registry edge scope: same corrected framing as B.3 item 7 — `feature-engine.depends_on:
   [structure-engine]` is fully corroborated via Swing consumption, not evidence of Structure-event
   consumption.
8. Downstream blast radius: 1 consumer module.
9. Chapter 0 §4b `>1`-module trigger: **applies independently** (2 modules).
10. Compatibility commitment already governed: **NO**.
11. Missing decision: `compatibility_commitment` value for `change-of-character-detected`.

### B.5 `structure-fact-invalidated`

1. Owning Domain Contract: `structure.md` (§5).
2. Producer module: `structure-engine`.
3. Producer capability/context: `market-structure` / `market-structure-analysis`.
4. Current direct consumers: **`context-projection` only** — with an explicit
   `consumer_obligation` (*"Consumer nhận StructureFactInvalidated... PHẢI invalidate hoặc
   recompute snapshot đó"*).
5. Domain Contract evidence: `context.md` §16 (*"structure-fact-invalidated — Structure role,
   correction"*); `feature.md` §14 exclusion (same citation).
6. `module-registry.yaml` corroboration: `context-aggregator.depends_on` includes
   `structure-engine` — corroborated.
7. Registry edge scope: same corrected framing as B.3 item 7.
8. Downstream blast radius: 1 consumer module.
9. Chapter 0 §4b `>1`-module trigger: **applies independently** (2 modules).
10. Compatibility commitment already governed: **NO**.
11. Missing decision: `compatibility_commitment` value for `structure-fact-invalidated`.

### B.6 `structure-recomputed`

1. Owning Domain Contract: `structure.md` (§5a).
2. Producer module: `structure-engine`.
3. Producer capability/context: `market-structure` / `market-structure-analysis`.
4. Current direct consumers: **`context-projection` only** (one relationship entry).
5. Domain Contract evidence: `context.md` §16 (*"structure-recomputed — Structure role, correction
   settle"*); `feature.md` §14 exclusion (same citation).
6. `module-registry.yaml` corroboration: `context-aggregator.depends_on` includes
   `structure-engine` — corroborated.
7. Registry edge scope: same corrected framing as B.3 item 7.
8. Downstream blast radius: 1 consumer module.
9. Chapter 0 §4b `>1`-module trigger: **applies independently** (2 modules).
10. Compatibility commitment already governed: **NO**.
11. Missing decision: `compatibility_commitment` value for `structure-recomputed`.

### B.7 `regime-classified`

1. Owning Domain Contract: `regime.md` (§3).
2. Producer module: `raw-regime-engine`.
3. Producer capability/context: `market-regime` / `raw-regime-analysis`.
4. Current direct consumers: `feature-engineering` (`feature-engine`), `context-projection`
   (`context-aggregator`) — **2 consumer contexts** (two `context-map.yaml` relationship entries).
5. Domain Contract evidence: `feature.md` §14 (*"regime-classified — volatility_metric/
   directional_persistence_metric (path regime)"*); `context.md` §16 (*"regime-classified — hai
   Regime role (§7.2)"*).
6. `module-registry.yaml` corroboration: `feature-engine.depends_on` includes `raw-regime-engine`;
   `context-aggregator.depends_on` includes `raw-regime-engine` — both edges present, both
   corroborated by event-level evidence.
7. Registry edges not corroborating: none for this `contract_id`.
8. Downstream blast radius: 2 consumer modules.
9. Chapter 0 §4b `>1`-module trigger: **applies independently** (3 modules: 1 producer + 2
   consumers).
10. Compatibility commitment already governed: **NO**.
11. Missing decision: `compatibility_commitment` value for `regime-classified`.

### B.8 `regime-fact-invalidated`

1. Owning Domain Contract: `regime.md` (§4).
2. Producer module: `raw-regime-engine`.
3. Producer capability/context: `market-regime` / `raw-regime-analysis`.
4. Current direct consumers: `feature-engineering`, `context-projection` — **2 consumer contexts**
   (each with its own `consumer_obligation` invalidate/recompute clause).
5. Domain Contract evidence: `feature.md` §14 (*"regime-fact-invalidated — như trên,
   correction"*); `context.md` §16 (*"regime-fact-invalidated — như trên, correction"*).
6. `module-registry.yaml` corroboration: same two edges as B.7, both corroborated.
7. Registry edges not corroborating: none.
8. Downstream blast radius: 2 consumer modules.
9. Chapter 0 §4b `>1`-module trigger: **applies independently** (3 modules).
10. Compatibility commitment already governed: **NO**.
11. Missing decision: `compatibility_commitment` value for `regime-fact-invalidated`.

## C. ADR trigger assessment per contract

Identical disposition shape for all eight, per the task's own requested format — reproduced per
contract for completeness, not because the answer differs in form (only the verified topology
column differs, per §B above):

| `contract_id` | Existing authority requires explicit commitment | Existing authority chooses value | Cross-module impact (verified) | `ADR_REQUIRED` |
|---|---|---|---|---|
| `candle-closed` | YES (Ch.10 §10.3.1) | NO | 1 producer + 4 consumers | **YES** |
| `candle-corrected` | YES | NO | 1 producer + 4 consumers | **YES** |
| `break-of-structure-detected` | YES | NO | 1 producer + 1 consumer | **YES** |
| `change-of-character-detected` | YES | NO | 1 producer + 1 consumer | **YES** |
| `structure-fact-invalidated` | YES | NO | 1 producer + 1 consumer | **YES** |
| `structure-recomputed` | YES | NO | 1 producer + 1 consumer | **YES** |
| `regime-classified` | YES | NO | 1 producer + 2 consumers | **YES** |
| `regime-fact-invalidated` | YES | NO | 1 producer + 2 consumers | **YES** |

All eight independently satisfy Chapter 0 §4b's `>1`-module trigger — even the four Structure
`contract_id`s, whose single confirmed consumer (`context-aggregator`) still makes producer +
consumer = 2 modules, the identical minimum cardinality `ADR-038` itself already found sufficient.
No `compatibility_commitment` value is chosen for any of the eight by this WP.

## D. Packaging comparison

### Model A — one ADR per `contract_id` (8 ADRs)

Within each family, every `contract_id`'s topology (producer, owning Domain Contract, consumer
set) is **identical** to its siblings (candle-closed/candle-corrected: same 4 consumers;
structure's four: same 1 consumer; regime's two: same 2 consumers — confirmed §B). Eight separate
ADRs would repeat the identical topology assessment and rationale 4, 2, and 2 times respectively,
for zero additional semantic-isolation benefit — the isolation Model A buys is only meaningful
where topology genuinely differs per `contract_id`, which it does not here. This is not a rejection
by file count alone (the task's own caution, honored): it is that Model B already supplies the
identical explicit, independently-evidenced, per-`contract_id` decision surface Model A would, at a
coarser and equally reviewable grain, with zero information loss and zero duplication. **Not
recommended** — evidence-grounded preference against unnecessary file proliferation, not a
governance prohibition.

### Model B — one ADR per domain/producer family (3 ADRs)

- **Candle ADR** (`candle-closed`, `candle-corrected`): one producer (`market-data-ingestion`), one
  owning Domain Contract (`candle.md`), identical 4-consumer topology for both `contract_id`s.
  Coherent.
- **Structure ADR** (`break-of-structure-detected`, `change-of-character-detected`,
  `structure-fact-invalidated`, `structure-recomputed`): one producer (`structure-engine`), one
  owning Domain Contract (`structure.md`), identical single-consumer (`context-aggregator`)
  topology for all four. Coherent.
- **Regime ADR** (`regime-classified`, `regime-fact-invalidated`): one producer
  (`raw-regime-engine`), one owning Domain Contract (`regime.md`), identical 2-consumer topology
  for both. Coherent.

Each package: every `contract_id` explicitly enumerable, every contract's producer/consumer impact
independently evidenced (§B), no contract's value inferred from another, rationale remains
reviewable per family. **This is a coherent, evidence-supported packaging** — independently
re-derived from `context-map.yaml`'s own relationship inventory, not assumed from the pre-analysis
hypothesis — offering the finest-grained future supersession of the three models (Chapter 11 §11.8,
see Model C below) at a still-fully-bounded per-family review surface. It is **not**, however, the
uniquely authority-required packaging — see §E for the corrected determination.

### Model C — one ADR for all 8 (re-evaluated, `CONTEXT-COMPAT-SCOPE-A-MAJ-01`)

**v0.1 rejected this model primarily because Candle/Structure/Regime are separate architectural
families under `ADR-003`/`ADR-014` (Structure and Regime constitutionally independent of each
other, confirmed by `raw-regime-engine.forbidden_dependencies: [structure-engine]`).** Fresh
Review A correctly found that reasoning overreaching: `ADR-003`/`ADR-014` govern producer/domain
dependency, fan-in semantics, and Structure/Regime computational independence — they say nothing
about ADR-packaging granularity. Chapter 11 (`docs/constitution/11-adr-process.md`, fresh-read in
full this transaction) requires only a valid ADR structure (Context/Decision/Alternatives/
Risks/Scale/Consequences) with explicit, evidenced authority — it states no "one domain per ADR,"
"one producer per ADR," or "one `contract_id` per ADR" rule anywhere. **Runtime/domain independence
is not, by itself, an ADR-packaging prohibition**, and `ADR-038`'s own precedent already
demonstrates a single ADR legitimately bundling more than one `contract_id`.

**Corrected test applied:** can one ADR express a single coherent architectural decision surface —
*"first-publication compatibility commitments for the bounded set of Context-upstream Event
Contracts required to make `context-market-input` operationally resolvable"* — while preserving
independent, explicit, per-`contract_id` decisions and evidence, via a decision table shaped
exactly like `contract_id | owning domain | producer | verified consumers |
compatibility_commitment | rationale`, with no value inferred across rows? Checked against the six
specific disqualifying conditions the task itself names:

1. *Obscures materially different decision rationale* — **not triggered**; §B above already
   supplies each `contract_id`'s own independently-evidenced rationale, directly transcribable into
   per-row cells.
2. *Requires one contract's value to constrain another* — **not triggered**; nothing in §B's
   topology creates a cross-`contract_id` value dependency.
3. *Creates ambiguous ownership* — **not triggered**; each row's owning Domain Contract/producer is
   already unambiguous (§B).
4. *Makes future supersession/versioning unable to identify which decision governs which
   contract* — **not triggered within the document itself** (an explicit table identifies each
   `contract_id`'s own decision unambiguously) — but see the genuine, narrower concern below.
5. *Creates review scope too broad to reason about safely* — arguable, not clearly triggered; 8
   rows of already-derived topology (this WP's own §B) is not, on its face, unsafely broad for one
   review pass.
6. *Violates an actual governance rule* — **not found**; Chapter 11 imposes no one-subject-per-ADR
   rule, and `ADR-038` itself already bundled 2 `contract_id`s without objection.

**Model C is therefore NOT disqualified by architectural independence alone, and is not rejected in
this corrected analysis.**

**A genuine, narrower, evidence-grounded consideration remains, distinct from the withdrawn
architectural-independence rationale:** Chapter 11 §11.8 (fresh-read this transaction) defines
`supersedes` as a **whole-ADR-file relation** — *"ADR mới Approved với `supersedes: [ADR-cũ]`"* —
there is no partial/per-decision-item supersession mechanism anywhere in Chapter 11. If a single
Model-C ADR bundles all 8 `contract_id`s and a **future** governed change needs to revise only, say,
Structure's own compatibility commitment, that future ADR would need to supersede the **entire**
8-contract document — either re-stating/re-affirming Candle's and Regime's untouched decisions, or
leaving readers to reconstruct still-valid content from a now-`Superseded` file. Under Model B, that
same future change supersedes only the affected 2- or 4-`contract_id` package, leaving the other two
families' own ADRs completely undisturbed. This is a genuine bounded-reviewability/
future-evolution-granularity consideration — it does **not** disqualify Model C, but it is a real,
non-fabricated reason a reviewer could prefer Model B's finer supersession grain (see §E).

## E. Packaging determination — NOT uniquely required by repository authority (corrected, `CONTEXT-COMPAT-SCOPE-A-MAJ-01`)

v0.1 presented Model B as *the* smallest coherent, authority-required scope. That overstated what
the evidence actually supports. Re-derived in this correction: **repository authority (Chapter 0
§4b, Chapter 10 §10.3.1, Chapter 11, `ADR-038`'s own precedent) does not uniquely force a choice
between Model B and Model C.** Both are governance-valid:

- **Model B — 3 family-scoped ADRs**, `contract_id`s enumerated exactly:
  1. **Candle Event Contract Compatibility Commitment** — `candle-closed`, `candle-corrected`.
  2. **Structure Event Contract Compatibility Commitment** — `break-of-structure-detected`,
     `change-of-character-detected`, `structure-fact-invalidated`, `structure-recomputed`.
  3. **Regime Event Contract Compatibility Commitment** — `regime-classified`,
     `regime-fact-invalidated`.

  Each package independently coherent (§D); finest-grained future supersession of the three models
  (Chapter 11 §11.8's whole-file `supersedes` relation means only the affected family's ADR need be
  superseded by a later change); smallest per-transaction review surface.

- **Model C — 1 ADR for all 8**, all eight `contract_id`s enumerated in one explicit per-`contract_id`
  decision table (`contract_id | owning domain | producer | verified consumers |
  compatibility_commitment | rationale`), no value inferred across rows. Coherent single
  architectural subject — *first-publication compatibility commitments for the Context-upstream
  Event Contract set required to make `context-market-input` operationally resolvable* (§D); fewer
  approval-loop iterations, consistent with the stated operating-model preference for batching where
  semantic boundaries permit.

**`MULTIPLE GOVERNANCE-VALID PACKAGING OPTIONS REMAIN: Model B and Model C.`** Neither is uniquely
required by repository authority. Reducing this to a single choice trades finer-grained future
supersession and smaller per-transaction review surface (favoring Model B) against fewer
approval-loop iterations and reduced technical ceremony (favoring Model C, per the stated operating
model) — a genuine Product-Owner-level packaging preference, not a technical/governance derivation
this WP can resolve on its own. This WP does **not** pick on the Product Owner's behalf.

**Non-binding technical note (a preference, not an authority requirement):** Model B is offered as
the smaller, more bounded per-transaction review surface with finer-grained future supersession
(§D) — stated here only as a technical recommendation available to whichever packaging decision is
made, never as the determined answer.

No compatibility-commitment *value* is chosen for any package, under either model, by this WP. A
Model-B package's eventual ADR, or Model C's decision table, may — per Chapter 10 §10.3.1's own
per-`contract_id` declaration requirement — state a single shared value for multiple `contract_id`s
or distinct values per `contract_id`, as that ADR's own governed decision determines — not
predetermined here.

## F. Not-recommended / governance-valid-but-unselected packaging models

- **Model A (8 ADRs):** not recommended (§D) — duplicates identical within-family topology/
  rationale for no benefit Model B does not already provide at a coarser, still-fully-explicit
  grain; an evidence-grounded preference against unnecessary file proliferation, **not** a
  governance prohibition.
- **Model C (1 ADR for all 8):** **not rejected** (corrected from v0.1's overreach,
  `CONTEXT-COMPAT-SCOPE-A-MAJ-01`, §D) — governance-valid, one of the two options in §E's
  `MULTIPLE GOVERNANCE-VALID PACKAGING OPTIONS REMAIN` determination. Listed here only to record
  that it remains a live option, not a disqualified one.

## G. Open evidence gaps

1. **`feature-engine.depends_on: [structure-engine]` — no registry inconsistency for this edge
   (corrected, `CONTEXT-COMPAT-SCOPE-A-MIN-01`).** v0.1 characterized this edge as a genuine,
   unresolved documentation inconsistency because `feature.md` does not consume any of the four
   Structure Event Contracts. That conclusion was false. `structure-engine` is the registered module
   boundary responsible for **both** Swing and Structure output (`structure-engine.responsibilities`:
   *"Suy diễn Swing/BOS/CHoCH và structure semantics từ Candle"*), and `feature.md` §14 confirms
   Feature genuinely consumes `swing-confirmed`/`swing-invalidated` from within that same
   `market-structure-analysis` boundary — this fully corroborates the module-level edge. The edge is
   simply **broader** than the four Structure `contract_id`s alone, because module-level `depends_on`
   captures the entire registered producer boundary (Swing + Structure), not any single event
   family within it. This is exactly why module-level `depends_on` must never be used as proof of
   consumption for one specific Event Contract (§A) — it was previously mischaracterized as an open
   gap; that characterization is withdrawn. This correction does **not** add Feature as a consumer
   of any of the four Structure Event Contracts — per-contract topology (§B) is otherwise unchanged.
2. No other evidence gap was found — `context-map.yaml`'s relationship inventory for these 8
   `contract_id`s is exhaustive and internally consistent with every owning Domain Contract's own
   text (cross-checked, §B).

## H. Exact next WP sequence (not executed here)

1. **Fresh ChatGPT Review A of this corrected scope-derivation artifact (v0.2).**
2. **If `CLEAN`: route the minimal Product Owner packaging choice** — Model B (3 family-scoped
   ADRs) vs. Model C (1 ADR for all 8, explicit per-`contract_id` decision table) — per §E's
   `MULTIPLE GOVERNANCE-VALID PACKAGING OPTIONS REMAIN` determination. This is a packaging-format
   decision only; it does not itself select any `compatibility_commitment` value.
3. **Author the compatibility-commitment ADR candidate(s) matching the chosen packaging** — 3 Draft
   ADRs (Model B) or 1 Draft ADR with an explicit per-`contract_id` decision table (Model C) — each
   enumerating its own `contract_id`s, topology, and `ADR_REQUIRED` rationale from §B/§C above —
   still **not** selecting any commitment value in that authoring step; the value is each ADR's own
   Decision content, reached through its own Review A/Independent Review B/Product Owner cycle.
4. **Review A / Independent Review B / Product Owner decision, per ADR, for each authored
   candidate** — independent of one another; one package reaching a decision does not gate the
   others.
5. **Only after applicable ADR approval: author the first Candle/Structure/Regime Event Contracts**
   per `contract_id` (governed authoring under `ADR-039`), each declaring `EXTERNAL_NON_STATE_CAUSE`
   for every one of its own causation-ref categories (per
   `docs/project/context-upstream-state-dependency-derivation-001.md` v0.4) and the
   `compatibility_commitment` value its governing ADR decided.
6. **Separately resolve Feature's own future Event Contract versioning + Compatibility Result
   prerequisites** — independent of steps 2–5.
7. **After all required per-effect classification and compatibility authority exists: update/
   re-review Context Input Contract readiness**, and only then consider publication of
   `context-market-input / v1.0`.

## I. Context Input Contract state — unchanged

`docs/architecture/input-contracts/context-market-input.yaml` is **not** touched by this
transaction. Confirmed: `version: "0.3"`, `status: Draft`, blob
`ce74ddf6291abb2b1ed21938ca88050550fb2a0b`; Review A `CLEAN — 0 Blocker / 0 Major / 0 Minor`, Risk
`R2`, `PROCEED WITHOUT CROSS-CHECK`, `NOT PUBLISHED`.

## J. Milestone state

M2: `BLOCKED` — parallel evidence lane. M3: `ACTIVE` — Context deterministic core `REVIEW A
VALIDATED — CLEAN`; `ADR-046` `APPROVED`; `context.md` v0.4 `PO ACCEPTED`; Context Input Contract
v0.3 `REVIEW A CLEAN — R2 — PROCEED WITHOUT CROSS-CHECK — NOT PUBLISHED`, unmutated; state-
dependency derivation `v0.4`, Review A `CLEAN — 0/0/1` (`CONTEXT-SD-DERIV-A-MIN-03` `CLOSED —
REVIEW A VALIDATED`), matrix unchanged (`20 EXTERNAL_NON_STATE_CAUSE / 1 VACUOUS / 0
STATE_DEPENDENCY / 0 UNRESOLVED`), not touched by this correction; current blocker: Event Contract
compatibility-commitment ADR decision scope — corrected this transaction from a single
authority-required recommendation to `MULTIPLE GOVERNANCE-VALID PACKAGING OPTIONS REMAIN` (Model B,
3 family-scoped ADRs, vs. Model C, 1 ADR for all 8 with an explicit per-`contract_id` decision
table), a Product-Owner-level packaging preference not resolved here — plus missing Event Contract
authority (8 of 10 event types). M4: `QUEUED`. Phase-3 Approval Gate: `NOT REACHED`. LIVE:
`NOT_AUTHORIZED`.
