---
id: context-event-contract-compatibility-adr-scope-001
title: "Compatibility-Commitment ADR Scope Derivation — Missing Context-Upstream Event Contracts"
kind: analysis
version: "0.1"
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
here).

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
7. **Registry edges not corroborating this specific event:** `feature-engine.depends_on` includes
   `structure-engine`, and `feature-engine`'s own `responsibilities` text says *"Fan-in... từ
   Structure và Regime output"* — but `feature.md`'s own explicit `events_consumed`/Input Contracts
   section (§14) denies consuming any Structure event. This is a genuine, fresh-verified
   registry-topology-vs-event-level-evidence divergence (§G below) — resolved here in favor of the
   Domain Contract's own explicit text, per this WP's event-level-evidence-first rule. `Feature`
   consumes `Swing` (a different `contract_id` family, `swing-confirmed`/`swing-invalidated`,
   `market-structure-analysis` context) — never Structure's own four events.
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
7. Registry edges not corroborating: same `feature-engine → structure-engine` non-corroboration as
   B.3.
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
7. Registry edges not corroborating: same `feature-engine → structure-engine` non-corroboration.
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
7. Registry edges not corroborating: same non-corroboration as B.3–B.5.
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
where topology genuinely differs per `contract_id`, which it does not here. **Rejected**: more
files than the evidence coherently supports, not smaller scope, just more duplication.

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
reviewable per family, and packaging does not couple architecturally unrelated domains (Candle,
Structure, and Regime are already-established independent families — see Model C below). **This is
the smallest coherent packaging supported by actual repository evidence, not merely the
pre-analysis hypothesis** — independently re-derived from `context-map.yaml`'s own relationship
inventory, not assumed.

### Model C — one ADR for all 8

Would bundle three **architecturally independent** producer relationships (`market-data-ingestion`,
`structure-engine`, `raw-regime-engine` — Structure and Regime are constitutionally independent of
each other per `ADR-003`/`ADR-014`, confirmed by `raw-regime-engine.forbidden_dependencies:
[structure-engine]` in `module-registry.yaml`), three distinct owning Domain Contracts, and three
materially different consumer sets (4 vs. 1 vs. 2 modules) into a single decision. This directly
violates the packaging-coherence criterion *"bundling does not couple unrelated domains merely for
bookkeeping convenience"* — fewer files, not more coherent. **Rejected.**

## E. Recommended smallest coherent ADR scope

Three candidate ADR packages, `contract_id`s enumerated exactly:

1. **Candle Event Contract Compatibility Commitment** — `candle-closed`, `candle-corrected`.
2. **Structure Event Contract Compatibility Commitment** — `break-of-structure-detected`,
   `change-of-character-detected`, `structure-fact-invalidated`, `structure-recomputed`.
3. **Regime Event Contract Compatibility Commitment** — `regime-classified`,
   `regime-fact-invalidated`.

No compatibility-commitment *value* is chosen for any package by this WP. Each package's eventual
ADR may, per Chapter 10 §10.3.1's own per-`contract_id` declaration requirement, state a single
shared value for all `contract_id`s in its package or distinct values per `contract_id`, as that
ADR's own governed decision determines — not predetermined here.

## F. Rejected packaging models

- **Model A (8 ADRs):** rejected — duplicates identical within-family topology/rationale for no
  semantic-isolation benefit; not the smallest *coherent* scope, only a larger file count.
- **Model C (1 ADR for all 8):** rejected — couples three architecturally independent
  producer/Domain-Contract/consumer relationships that the Constitution's own `ADR-003`/`ADR-014`
  already established as independent; incoherent bundling for file-count minimization alone.

## G. Open evidence gaps

1. **`feature-engine.depends_on: [structure-engine]` (`module-registry.yaml`) does not correspond
   to any Structure event consumption** — `feature.md` §14 explicitly excludes all four Structure
   events. The registry's own `feature-engine.responsibilities` text (*"Fan-in... từ Structure và
   Regime output"*) appears to describe this same tension without resolving it. This is not a
   blocking conflict for this WP's own scope-derivation purpose (event-level Domain Contract
   evidence controls, per this WP's own explicit priority rule, and both `context-map.yaml` and
   `feature.md` agree Feature does not consume Structure events) — but it is a genuine,
   unresolved documentation inconsistency between `module-registry.yaml`'s prose and `feature.md`'s
   own authoritative event list, flagged here for a future, separate, narrowly-scoped correction
   (not performed by this WP — out of scope, no registry/Domain Contract file touched).
2. No other evidence gap was found — `context-map.yaml`'s relationship inventory for these 8
   `contract_id`s is exhaustive and internally consistent with every owning Domain Contract's own
   text (cross-checked, §B).

## H. Exact next WP sequence (not executed here)

1. **Fresh ChatGPT Review A of this scope-derivation artifact.**
2. **If `CLEAN`: author the three recommended compatibility-commitment ADR candidates** (Candle,
   Structure, Regime — §E), each a Draft ADR enumerating its own `contract_id`s, topology, and
   `ADR_REQUIRED` rationale from §B/§C above — still **not** selecting any commitment value in that
   authoring step; the value is the ADR's own Decision content, reached through its own Review
   A/Independent Review B/Product Owner cycle.
3. **Review A / Independent Review B / Product Owner decision, per ADR, for each of the three
   candidates** — independent of one another; one package reaching a decision does not gate the
   others.
4. **Only after applicable ADR approval: author the first Candle/Structure/Regime Event Contracts**
   per `contract_id` (governed authoring under `ADR-039`), each declaring `EXTERNAL_NON_STATE_CAUSE`
   for every one of its own causation-ref categories (per
   `docs/project/context-upstream-state-dependency-derivation-001.md` v0.4) and the
   `compatibility_commitment` value its governing ADR decided.
5. **Separately resolve Feature's own future Event Contract versioning + Compatibility Result
   prerequisites** — independent of steps 2–4.
6. **After all required per-effect classification and compatibility authority exists: update/
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
v0.3 `REVIEW A CLEAN — R2 — PROCEED WITHOUT CROSS-CHECK — NOT PUBLISHED`; state-dependency
derivation `v0.4`, Review A `CLEAN — 0/0/1` (Minor folded into this transaction), matrix unchanged
(`20 EXTERNAL_NON_STATE_CAUSE / 1 VACUOUS / 0 STATE_DEPENDENCY / 0 UNRESOLVED`); current blocker:
Event Contract compatibility-commitment ADR(s) (3 recommended candidates, `contract_id`s
enumerated, not yet authored) plus missing Event Contract authority (8 of 10 event types). M4:
`QUEUED`. Phase-3 Approval Gate: `NOT REACHED`. LIVE: `NOT_AUTHORIZED`.
