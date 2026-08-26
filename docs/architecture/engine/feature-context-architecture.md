---
id: feature-context-architecture
title: "Package 1.3-B — Feature & Context Engine Architecture"
version: "0.3"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-04"
last_review: null
next_review: null
depends_on: ["00-governance", "02-platform-invariants", "03-engineering-principles", "04-domain-principles", "05-time-model", "06-identity-model", "07-module-taxonomy", "08-event-model", "13-quality-gates", "14-roadmap"]
---

# Package 1.3-B — Feature & Context Engine Architecture

**CANDIDATE (package lifecycle, reverted from Consolidated Stable, 2026-08-26, vai trò: `Feature Input Contract + Frontier Design Executor`) — artifact status: Draft, KHÔNG Approved/Locked.** v0.2 → v0.3: genuine semantic addition, NOT a bounded parity/wording correction — new §4.6 "Feature-scoped Input Contract selection và frontier design" (Chapter 8 §8.3.4 — mechanical Phase-1 instantiation of Approved ADR-036 Consequences step 6, no new architecture decision: the contract-selection mapping is fully derived from already-Approved `feature.md` §6/§14, and `included_streams` is fully derived from Approved `ADR-036`'s topology as concretized in Approved `docs/architecture/stream-registry.yaml` v0.1); §13's `stream-registry.yaml / producer_ref resolution` gap entry updated to reflect that `stream-registry.yaml` and three Feature-scoped Input Contract Drafts now exist (artifact-existence half resolved), while `stream_ref`/`producer_ref` code population, Event Contract authoring, and Context's own Input Contract remain explicitly open. Three new concrete artifacts created: `docs/architecture/input-contracts/feature-candle-input.yaml`, `feature-regime-input.yaml`, `feature-swing-distance-input.yaml` (all Draft, v1, `stream_registry_version: v1`). `feature.md`/`context.md`/`module-registry.yaml`/`system-decomposition.md`/any ADR: NOT modified. Does not implement `feature-engine`, does not author any Event Contract, does not close `P3-FEATURE-A-MAJ-04`/`P3-FEATURE-A-MAJ-06`. `package_lifecycle` reverts to `candidate` — a fresh Review A + Independent Review B + Product Owner reconsolidation round on this exact candidate is required before this baseline returns to `Consolidated Stable`, same precedent already established for `system-decomposition.md`'s own ADR-023/ADR-036 alignment cycles.

**CONSOLIDATED STABLE (package lifecycle, 2026-08-04, Product Owner decision) — artifact status: Draft, KHÔNG Approved/Locked.** Package 1.3-B v0.2 đạt `Consolidated Stable` SAU Review A CLEAN (Blocker 0/Major 0/Minor 1) + Independent Review B REVISE (Blocker 0/Major 3/Minor 1) trên v0.1 → bounded correction tại HEAD `71007bf1063c012001eb34465f41c0ce4905b7cf` (đóng `P13B-IRB-MAJ-01`/`P13B-IRB-MAJ-02`/`P13B-IRB-MAJ-03`/`P13B-A-MIN-01`/`P13B-IRB-MIN-01`) → final bounded verification CLEAN (mọi Major finding đóng, không Minor nào còn cần correction) + Product Owner consolidation decision (2026-08-04, §15). `Consolidated Stable` LÀ package lifecycle/readiness state (Chapter 0 §7.1) — KHÔNG có nghĩa artifact `Approved`/`Locked`; `status: Draft`, `approved_by: null`, `approved_at: null` KHÔNG đổi, đúng package-lifecycle/artifact-lifecycle separation đã dùng nhất quán trong toàn bộ session này (cùng pattern Package 0.2-B4/Package 1.1/Package 1.3-A). **Open gap bảo lưu tường minh, KHÔNG blocking:** `context.md` dùng khuôn "authoritative event record" cho `MarketContextSnapshot` trong khi `context-aggregator` vẫn `module_type: projection`, `owns_authoritative_state: false`, rebuildable, KHÔNG authoritative source cho upstream hay business domain state — tension này KHÔNG được resolve bởi consolidation này, xem §13. Consolidation quyết định này KHÔNG chọn một Context authority model mới.

**v0.2 — bounded correction (2026-08-04), đóng `P13B-IRB-MAJ-01`/`P13B-IRB-MAJ-02`/`P13B-IRB-MAJ-03`/`P13B-A-MIN-01`/`P13B-IRB-MIN-01`** (findings confirmed từ Review A/Independent Review B trên v0.1). Root cause: `module-registry.yaml` v0.3 (khi v0.1 author) thiếu `market-data-ingestion` trong `depends_on` của `feature-engine`/`context-aggregator` dù cả hai đã trực tiếp tiêu thụ `candle-closed`/`candle-corrected` theo đúng `feature.md`/`context.md` (Package 0.2-B3/B4, Consolidated Stable, KHÔNG đổi), và `context-aggregator.emits` thiếu `event` dù `context.md` §3/§4 đã khóa `MarketContextSnapshot`/`MarketContextFactInvalidated` là event category — MỘT registry gap tại Package 1.1, KHÔNG một kiến trúc option mới. `module-registry.yaml`/`system-decomposition.md` v0.3 → **v0.4** sửa đúng gap này (bounded parity correction riêng, KHÔNG ADR, `package_lifecycle: Consolidated Stable` KHÔNG reset). Tài liệu này (v0.1 → v0.2) cập nhật §2/§3/§4/§5 để khớp `module-registry.yaml` v0.4, VÀ sửa terminology (§5.2/§8) — thay `authoritative MarketContextSnapshot` bằng `eligible cursor-bounded MarketContextSnapshot projection record` — làm rõ record-integrity (immutable/cursor-bounded/lineage-preserving) tách biệt khỏi authoritative domain-state ownership, KHÔNG đổi Context sang authoritative ownership. KHÔNG expand architecture scope, KHÔNG đổi Feature/Context responsibility, KHÔNG invent event mới, KHÔNG tạo universal fan-in, KHÔNG tạo ADR.

## 0. Vai trò của tài liệu này

Package 1.3-B elaborate **kiến trúc kỹ thuật** cho hai module ĐÃ được Package 1.1 (`Consolidated Stable`, [`module-registry.yaml`](../module-registry.yaml) v0.4 blob `6c4daa3eda3ef560b201de516dd019564d264c08`, [`system-decomposition.md`](../system-decomposition.md) v0.4 blob `8e60b9e6051956cfbe83f33e1c82f404bc082e37`) thiết lập identity/taxonomy/dependency: `feature-engine`, `context-aggregator`. Tài liệu này **KHÔNG redefine** module identity/taxonomy/dependency đã pin ở Package 1.1 — chỉ elaborate: responsibility boundary chi tiết hơn, dependency direction, selective fan-in treatment, definition-version pinning, event-time/recorded-time treatment, determinism/replay/no-repaint, Context aggregation/projection semantics, Context criticality/failure policy, correction/invalidation propagation, stale/incomplete Context behavior, security/trust-boundary identification, và open gap — đúng phạm vi `phase-1-plan.md` §8 Package 1.3-B "Purpose: Kiến trúc kỹ thuật cho Feature Engine (fan-in có chọn lọc từ Structure) và Context Aggregation (CQRS, aggregator)".

**KHÔNG thuộc phạm vi tài liệu này:** field-level event schema (đã khóa tại `feature.md` v0.2/`context.md` v0.2, Package 0.2-B3/B4, `Consolidated Stable`); Engine algorithm/formula/source code; database schema; deployment/runtime topology cụ thể; Strategy/Decision logic (Package 1.3-C); Package 1.3-A content (Data Ingestion/Structure/Raw Regime — `Consolidated Stable`, KHÔNG redefine).

## 1. Governing authority

```text
Constitution (Chapter 0–14, Locked):              highest architectural authority
Approved ADR-014 (supersedes ADR-003, scoped):    controlling authority cho Feature
                                                    computation fan-in vs Context snapshot
                                                    aggregation boundary
Domain Contract (feature.md v0.2, context.md v0.2 controlling domain semantic authority —
  — Package 0.2-B3/B4, Consolidated Stable):        Consolidated Stable, KHÔNG redefine tại
                                                    đây
module-registry.yaml v0.4 (Consolidated Stable):  module identity/taxonomy/dependency
                                                    authority — KHÔNG redefine tại đây
system-decomposition.md v0.4 (Consolidated        official Phase 1 module dependency graph
  Stable):                                         — KHÔNG redefine tại đây
structure-regime-architecture.md v0.1 (Package    upstream Structure Engine/Raw Regime
  1.3-A, Consolidated Stable):                     Engine boundary — KHÔNG redefine tại đây
phase-1-plan.md v0.4 (Approved):                  Phase 1 work-breakdown/package-boundary
                                                    authority
Package 1.3-B (tài liệu này):                     technical elaboration authority ONLY, cho
                                                    đúng hai module trong scope
```

Package 1.3-B KHÔNG redefine domain entity/event semantics, module identity/taxonomy, hay ADR-014 decision nào — mọi nội dung dưới đây chỉ **elaborate** kiến trúc kỹ thuật trong ranh giới đã pin.

## 2. Module scope (hai module, pin nguyên trạng từ Package 1.1)

Hai module dưới đây trích dẫn NGUYÊN VĂN `module-registry.yaml` v0.4 (identity/taxonomy KHÔNG đổi — `depends_on`/`emits` corrected tại v0.4, đóng `P13B-IRB-MAJ-01`/`P13B-IRB-MAJ-02`/`P13B-IRB-MAJ-03`, xem banner) — cột "Elaboration" là nội dung MỚI của tài liệu này:

| module_id | module_type | owns_authoritative_state | depends_on | emits | forbidden_dependencies |
|---|---|---|---|---|---|
| `feature-engine` | compute_engine | true | `market-data-ingestion`, `structure-engine`, `raw-regime-engine` | `event` | (none) |
| `context-aggregator` | projection | false | `market-data-ingestion`, `structure-engine`, `raw-regime-engine`, `feature-engine` | `event`, `query` | (none) |

**Xác nhận (yêu cầu task):** `depends_on` ở registry-level là ranh giới **permitted connectivity** — module ĐƯỢC PHÉP tiêu thụ contract từ module đích, KHÔNG phải "mọi instance computation PHẢI tiêu thụ cả hai/cả ba/cả bốn module đó cùng lúc". Ranh giới thực sự per-computation nằm ở `feature_definition_version`/`context_definition_version` (ADR-014 "Definition-pinned direct fan-in" — xem §4.5/§5.6). **`market-data-ingestion` có mặt trong cả hai `depends_on`** vì cả `feature-engine` (§4.3) và `context-aggregator` (§5.4) đều trực tiếp tiêu thụ `candle-closed`/`candle-corrected` — quan hệ này ĐÃ tồn tại trong `feature.md`/`context.md` từ trước (Package 0.2-B3/B4, Consolidated Stable, KHÔNG đổi bởi correction này), nhưng trước v0.4 KHÔNG được registry phản ánh; correction v0.4 chỉ đồng bộ registry với Domain Contract đã pin, KHÔNG tạo quan hệ mới.

## 3. Data flow (dependency-direction view — KHÔNG runtime topology)

```text
Market Data Ingestion (Package 1.3-A, Consolidated Stable)
  emits: candle-closed, candle-corrected
         │                                                │
         ├────────────────────┬───────────────────────────┤ (context cutoff/trigger
         │ (reference price/   │                           │  source, §7.0 — direct,
         │  candle path,       │                           │  §5.4)
         │  feature.md §7.1/   │                           │
         │  §7.3, §4.3)        │                           │
         ▼                     │                           │
Structure Engine (Package 1.3-A)  Raw Regime Engine (Package 1.3-A, Consolidated Stable)
  emits: break-of-structure-        emits: regime-classified, regime-fact-invalidated
    detected, change-of-character-
    detected, structure-fact-
    invalidated, structure-
    recomputed, swing-candidate-
    detected, swing-confirmed,
    swing-invalidated
         │                    │                    │                          │
         │ (Swing layer       │ (regime path,       │ (Structure orientation + │
         │  ONLY —            │  optional per        │  cả hai Regime dimension │
         │  feature.md §14)   │  feature_definition_ │  + ba Feature value,     │
         │                    │  version)            │  ADR-014 Context         │
         │                    │                      │  aggregation)            │
         ▼                    ▼                      │                          │
    Feature Engine (compute_engine, selective fan-in) │                          │
      emits: feature-computed, feature-fact-invalidated                        │
         │                                            │                          │
         └───────────────────┬────────────────────────┴──────────────────────────┘
                              ▼
                    Context Aggregator (projection)
                      emits: market-context-snapshot,
                        market-context-fact-invalidated (event); GetCurrentContext,
                        GetContextHistory (query)
                              │
                              ▼
              Strategy/Decision Engine (Package 1.3-C — KHÔNG thuộc phạm vi tài liệu này)
```

**Xác nhận tường minh (yêu cầu task):** đây là responsibility/dependency view — KHÔNG phải authorization triển khai một synchronous pipeline hay runtime topology cụ thể. Việc chọn cơ chế thực thi cụ thể thuộc Engineering/Phase 1 execution-topology decision (`phase-1-plan.md` §7), KHÔNG quyết định tại Package 1.3-B.

**Xác nhận tường minh (correction v0.2, `P13B-IRB-MAJ-01`/`P13B-IRB-MAJ-02`):** Feature Engine VÀ Context Aggregator đều tiêu thụ `candle-closed`/`candle-corrected` **trực tiếp** từ Market Data Ingestion — Feature Engine cho giá tham chiếu/`upstream_source: candle` path (feature.md §7.1/§7.3, §4.3); Context Aggregator cho `context_cutoff_source_ref` (cadence/cutoff driver, context.md §7.0/§11, §5.4). Đây KHÔNG phải quan hệ MỚI được tạo tại correction này — quan hệ này đã tồn tại nguyên vẹn tại `feature.md`/`context.md` (Package 0.2-B3/B4, Consolidated Stable) từ trước khi Package 1.3-B v0.1 được author; correction chỉ đồng bộ registry `depends_on` (đã thiếu edge này) với Domain Contract đã pin.

**Điểm kiến trúc quan trọng (ADR-014, KHÔNG suy diễn mới):** Context Aggregator fan-in **trực tiếp** từ `structure-engine`/`raw-regime-engine`/`feature-engine` — KHÔNG route qua Feature Engine như một intermediary bắt buộc. Đây là chính amendment ADR-014 pin ("Context snapshot aggregation" là một operation khác "Feature computation fan-in", cả hai được phép fan-in trực tiếp từ Structure/Regime theo đúng vai trò riêng — xem ADR-014 "Canonical distinction").

## 4. Module boundary — Feature Engine

**Trách nhiệm (Package 1.1, KHÔNG đổi):** "Fan-in CÓ CHỌN LỌC (Definition-pinned direct fan-in, ADR-014) từ Structure và Regime output thành Feature."

### 4.1 Selective fan-in — KHÔNG universal join requirement

Feature Engine sở hữu **ba founding feature type** (`feature.md` §1 enum đóng: `volatility_metric`, `directional_persistence_metric`, `distance_to_last_confirmed_swing`), mỗi type pin đúng MỘT input path qua chính `feature_definition_version` đang dùng — KHÔNG có feature type nào bắt buộc consume cả Structure lẫn Regime cùng lúc:

```text
volatility_metric / directional_persistence_metric (feature.md §7.1/§7.2):
  upstream_source: candle   → tính độc lập từ Candle authoritative — KHÔNG chạm Regime.
  upstream_source: regime   → expose lại computed_metric của RegimeClassified đúng
                               dimension — KHÔNG chạm Structure/Swing.
  Một feature_definition_version PHẢI pin ĐÚNG MỘT trong hai path — không ambiguous,
  không để implementation tự chọn ngầm.

distance_to_last_confirmed_swing (feature.md §7.3):
  Đúng 1 Candle (giá tham chiếu) + đúng 1 SwingConfirmed (Eligible Swing, feature.md §9a)
  — KHÔNG chạm Regime, KHÔNG chạm Structure's BOS/CHoCH event.
```

**Xác nhận tường minh (yêu cầu task — "Do not invent universal join requirements"):** module-level `depends_on: [market-data-ingestion, structure-engine, raw-regime-engine]` (§2, v0.4) là **union** của permitted connectivity cho ba feature type khác nhau, KHÔNG phải một yêu cầu mỗi computation phải join cả ba module đó. Chỉ khi một `feature_definition_version` tương lai thực sự cần cả Structure lẫn Regime cùng lúc (ADR-014 "selective cross-domain synthesis" — chưa dùng ở B3 minimal scope) thì synchronization mới xảy ra bên trong CHÍNH một Feature Definition đó — vẫn KHÔNG phải một universal rule.

**Ranh giới Swing vs Structure (quan trọng, dễ hiểu nhầm):** `distance_to_last_confirmed_swing` tiêu thụ `SwingConfirmed`/`SwingInvalidated` — hai event thuộc **Lớp 1 (Swing detection)** bên trong module `structure-engine` (Package 1.3-A §4.1) — **KHÔNG BAO GIỜ** tiêu thụ `BreakOfStructureDetected`/`ChangeOfCharacterDetected`/`StructureFactInvalidated`/`StructureRecomputed` (Lớp 2, BOS/CHoCH — `feature.md` §14 cấm tường minh). Module-level dependency edge `feature-engine → structure-engine` được thỏa mãn HOÀN TOÀN qua Lớp 1 — Feature Engine không có quan hệ nào với Lớp 2 của `structure-engine`.

### 4.2 Authoritative ownership

```text
Feature Engine sở hữu authoritative:
  FeatureComputed / FeatureFactInvalidated fact — đúng ba founding feature type
  (feature.md §1/§3/§4).

Feature Engine KHÔNG sở hữu:
  Candle fact (Market Data Ingestion, Package 1.3-A); Swing/Structure fact (Structure
  Engine, Package 1.3-A); Regime fact (Raw Regime Engine, Package 1.3-A); Context snapshot
  (Context Aggregator, §5 dưới); feature_definition_version policy VALUE cụ thể
  (configuration instance, Phase 1).
```

### 4.3 Inputs/outputs theo contract category

```text
Consumes (event):  candle-closed, candle-corrected (giá tham chiếu +
                    upstream_source: candle path); swing-confirmed, swing-invalidated
                    (distance_to_last_confirmed_swing); regime-classified,
                    regime-fact-invalidated (upstream_source: regime path)
                    — feature.md §14, KHÔNG hơn.
Emits (event):      feature-computed, feature-fact-invalidated
Consumes (query):   — (không có; module-registry.yaml `consumes: [event]`)
```

**Không tiêu thụ (feature.md §14, xác nhận tường minh):** `CandleObserved`; `CandleCurrentView`; `SwingCandidateDetected`; `SwingCurrentView`; bất kỳ Structure event nào; `RegimeCurrentView`; Context projection; Strategy/Decision/Risk/Account/Execution fact.

### 4.4 Definition-version pinning (Referenced Authoritative Artifact, Chapter 8 §8.1.1)

```text
feature_definition_version — pin: upstream_source (candle|regime, đúng một);
  required_upstream_definition_version (regime_definition_version khi upstream_source=
  regime); window_candle_count (khi upstream_source=candle); formula_id/parameters;
  swing_direction/distance_representation/reference_price_field/
  eligible_swing_effective_cutoff_policy/eligible_swing_selection_policy/
  required_swing_definition_version (distance_to_last_confirmed_swing); unit/
  decimal_precision_policy/warm_up_policy/missing_input_policy/correction_policy;
  input_normalization_policy/current_view_selection_policy (feature.md §6).
Bất biến sau khi tham chiếu — đổi tham số semantic tạo feature_definition_version MỚI,
  KHÔNG mutate version cũ (Chapter 8 §8.1.1).
```

### 4.5 Definition-pinned direct fan-in (ADR-014 — bắt buộc, KHÔNG suy diễn thêm)

```text
Direct upstream fan-in is permitted only for authoritative upstream roles, contract IDs
and contract versions explicitly enumerated and pinned by the consuming Feature
Definition. Undeclared upstream contracts, implementation-selected dependencies and
implicit fallback inputs are prohibited.
```

Feature Engine KHÔNG có một quyền chung để đọc mọi Structure/Regime event ở cấp LAYER — chỉ những gì `feature_definition_version` cụ thể đã pin (ADR-014 "Feature" clause; `feature-engine.depends_on` ở §2 là connectivity RANH GIỚI, KHÔNG phải authorization tự động cho mọi input).

### 4.6 Feature-scoped Input Contract selection và frontier design (Chapter 8 §8.3.4 — instantiates Approved ADR-036 Consequences step 6)

**Not a new architecture decision.** This subsection is a mechanical Phase-1 design-spec instantiation of already-Approved authority: which Feature-scoped Input Contract instance applies to which `feature_type`/`upstream_source` combination is already fully determined by `feature.md` §6/§14 (Approved-scope Domain Contract semantics, unchanged), and which streams each contract may include is already fully determined by Approved `ADR-036`'s topology, concretized in Approved `docs/architecture/stream-registry.yaml` v0.1 (`registry_version: v1`). This subsection only records the resulting mapping and the minimum frontier/completeness design Chapter 8 §8.3.4 requires every Input Contract to declare.

**Contract selection — derived, not chosen, from `feature.md` §6/§14:**

```text
feature_type ∈ {volatility_metric, directional_persistence_metric}
  AND upstream_source: candle   → input_contract_ref: {contract_id: feature-candle-input,
                                   contract_version: v1}
                                   included_streams: [market-data-ingestion-candle]

feature_type ∈ {volatility_metric, directional_persistence_metric}
  AND upstream_source: regime   → input_contract_ref: {contract_id: feature-regime-input,
                                   contract_version: v1}
                                   included_streams: [raw-regime-engine-regime]

feature_type = distance_to_last_confirmed_swing
                                 → input_contract_ref: {contract_id: feature-swing-distance-input,
                                   contract_version: v1}
                                   included_streams: [market-data-ingestion-candle,
                                   structure-engine-swing]
```

`upstream_source: candle` and `upstream_source: regime` are mutually exclusive on the same `feature_definition_version` (`feature.md` §6: "PHẢI chọn ĐÚNG MỘT") — a Feature Definition never pins more than one Input Contract. Concrete artifacts: `docs/architecture/input-contracts/feature-candle-input.yaml`, `feature-regime-input.yaml`, `feature-swing-distance-input.yaml` (all `status: Draft`, `stream_registry_version: v1` pinned to the Approved Genesis registry). All three use `merge_policy: {algorithm: deterministic-causal-topological-order, concurrent_tie_break: [stream_id, sequence]}` — Chapter 8's own single mandated interleave algorithm (ADR-009 §2.1/§2.3), not a per-contract choice — and `causal_closure_policy: {mode: declared-state-dependencies, dependency_authority: per_effect_event_contract}`, the model ADR-009 §2.4 itself exemplifies as the mechanism for an apply set spanning multiple event types/Event Contract versions (exactly Feature's situation: Candle/Swing/Regime each have their own Event Contract). **Open gap, explicitly not closed here:** `declared-state-dependencies` classification requires each consumed event type's own Event Contract to exist and declare state-dependency classification — Candle/Swing/Regime/Feature Event Contracts are not yet authored in this repository. Until they exist, this policy is correctly *pinned as architecture* but not yet *operationally provable* — the same fail-closed posture `computation_cursor` already carries (`feature.md` §12, `ADR-035` Approved): implementation must fail-closed, not assume the classification silently.

**Frontier/completeness design (minimum required by Chapter 8 §8.3.4, no invented numeric threshold):**

```text
mechanism:                    committed-stream-position-vector — cursor.stream_positions is
                               an explicit per-stream committed-position vector over exactly
                               the contract's included_streams (Chapter 8 §8.5.3's stream-
                               universe intersection), never a single global sequence/order
                               (ADR-009 §2.1/§2.3, unchanged).
completeness_rule:            all-included-streams-gap-free-committed-prefix — a frontier is
                               complete only when every included stream's committed position
                               represents a contiguous, gap-free prefix (Chapter 8 §8.3.2's
                               per-stream contiguous-sequence invariant, applied per stream,
                               never inferred from wall clock).
in-scope causal prerequisites: per causal_closure_policy above, every in-scope causation_ref
                               must be cursor-visible AND applied before its effect (Chapter 8
                               §8.3.4's in-scope rule) before authoritative-apply; unresolved
                               in-scope prerequisite at a claimed-complete cursor is an
                               integrity violation, fail-safe (I-6), never treated as complete.
late_arrival_behavior:        defer-to-later-cursor — a later-appended event never mutates an
                               already-issued cursor or an already-authoritative fact; it
                               becomes visible only to a subsequent computation's own cursor,
                               handled entirely through feature.md's own existing correction/
                               invalidation lineage (§9, append-only invalidate-and-replace) —
                               no new correction mechanism introduced here.
incomplete_frontier_behavior: defer-or-fail-safe-no-speculative-apply — when frontier
                               completeness cannot be proven, the processor MUST buffer/defer
                               or fail-safe (I-6); speculative apply against an incomplete
                               frontier is prohibited in every execution mode.
buffer_limit_policy:          unbounded-defer-fail-safe — deliberately NO numeric buffer/
                               watermark threshold: Chapter 8 §8.3.4 permits watermark/bounded-
                               lateness mechanisms only when their clock/frontier source is
                               itself pinned, eventized, and replay-reproducible (no such
                               eventized frontier signal exists in this repository today) —
                               inventing an arbitrary number here would be exactly the
                               unauthoritative-placeholder pattern ADR-036 already rejected for
                               stream identity. If a bounded-lateness mechanism becomes an
                               actual operational need, it is a separate future governed
                               design (a genuinely new, numerically-justified choice), not
                               invented in this Phase-1 design spec.
lifecycle_frontier / registry
  applicability:               unchanged from Chapter 8 §8.5/§8.5.1-§8.5.3 and ADR-009 §2.6 —
                               computation_cursor.lifecycle_frontier and .stream_registry_version
                               are applied exactly as already Locked/Approved, not redefined
                               here; this subsection adds no new field and no new relational
                               invariant beyond what §8.5.1/§8.5.2 already require.
cross-mode parity:            Live/Backtest/Paper/Replay all pin the same
                               {input_contract_ref, stream_registry_version} for a given
                               computation (Chapter 8 §8.3.4's cross-mode requirement,
                               `feature.md` §17, unchanged) — no mode-specific contract
                               variant is introduced.
```

**Scope containment:** this subsection does not modify `feature.md`, does not author or modify any Event Contract, does not implement `feature-engine`, and does not close `P3-FEATURE-A-MAJ-04`/`P3-FEATURE-A-MAJ-06` — per `ADR-036`'s own Consequences ordering, Feature implementation remediation (canonical `computation_cursor` population, history-preserving as-of state, restart/replay tests, `eligible_swing_selection_superseded` emission) remains a separate, still-pending governed transaction.

## 5. Module boundary — Context Aggregator

**Trách nhiệm (Package 1.1, KHÔNG đổi):** "CQRS read-model tổng hợp Structure+Regime+Feature+market state cho Strategy tiêu thụ." Notes (Package 1.1, KHÔNG đổi): "Type 2 Projection (Chapter 7 §7.4) — KHÔNG BAO GIỜ sở hữu business decision; cấm phát sinh authoritative domain fact."

### 5.1 Projection / non-authoritative / rebuildable / downstream (bắt buộc — yêu cầu task)

```text
projection:          module_type: projection (Package 1.1, module-registry.yaml §2) —
                      materialize derived state từ authoritative source (Chapter 7 §7.4).
non-authoritative:    owns_authoritative_state: false (Package 1.1) — KHÔNG là authoritative
                      source cho bất kỳ domain concept nào (I-12); Structure/Regime/Feature
                      giữ nguyên là authoritative source DUY NHẤT cho chính domain của
                      chúng — Context CHỈ sao chép, KHÔNG thay thế (context.md §17, ADR-014).
rebuildable:          MarketContextSnapshot/MarketContextFactInvalidated rebuild được hoàn
                      toàn từ authoritative event stream cùng context_definition_version +
                      implementation version đã pin (context.md §5, Chapter 7 §7.4 rebuild
                      determinism).
downstream of         module-level depends_on: [market-data-ingestion, structure-engine,
Feature Engine:       raw-regime-engine, feature-engine] (§2, v0.4) — Context fan-in
                      SONG SONG từ cả bốn, KHÔNG route Structure/Regime/Feature qua Feature
                      Engine (§3 "Điểm kiến trúc quan trọng"); `market-data-ingestion` là
                      context cutoff/trigger source riêng (§5.4, §7.0), KHÔNG phải một
                      trong bảy context_values role.
not owner of upstream Context KHÔNG tự tính một engineered Feature mới, KHÔNG tái sản xuất
computation:          công thức/transformation của Feature Engine (context.md §17,
                      ADR-014 prohibition list).
not Decision          Context là "authoritative market-state snapshot, KHÔNG phải một
authority:            decision" (context.md §17, TRÍCH DẪN nguyên văn Domain Contract —
                      xem §5.2 "Terminology" cho cách Package 1.3-B đọc "authoritative"
                      tại đây, KHÔNG redefine text này) — KHÔNG đưa ra kết luận Strategy/
                      Decision/Risk/Account/Position/Execution; KHÔNG xác định execution
                      eligibility; KHÔNG authorize/reject/size/route một order (ADR-014
                      prohibition, xem §5.4 dưới).
```

### 5.2 Aggregation / projection semantics (as-of selection, KHÔNG tính toán lại)

Context sở hữu **as-of aggregation**, KHÔNG computation (ADR-014 "Canonical distinction: Feature fan-in = computation/transformation/synthesis; Context fan-in = as-of aggregation/snapshot assembly"):

```text
Context THỰC HIỆN (context.md §17):
  as-of selection của bảy authoritative ref (1 Candle cutoff source + Structure + hai
    Regime dimension + ba Feature type) tại một context_cutoff deterministic (§11 dưới);
  two-phase Eligible Upstream Fact selection (context.md §8 — Phase 1 eligibility filtering
    per-candidate độc lập, Phase 2 role-specific current selection CHỈ trên survivor Phase
    1, KHÔNG tham chiếu ngược — đóng lớp lỗi RA-B4-MAJ-01/IRB-B4-MAJ-01);
  sao chép NGUYÊN VẸN giá trị upstream vào context_values — KHÔNG diễn giải thêm
    (structure_orientation từ Structure fact; volatility/directional_persistence_regime_
    class từ hai RegimeClassified fact; ba Feature value từ ba FeatureComputed fact);
  assemble bảy fact ref thành MỘT market-state snapshot version-pinned
    (context_definition_version).

Context KHÔNG BAO GIỜ (context.md §17, ADR-014):
  tự derive trade signal; chấm điểm setup; kết luận Strategy/Decision/Risk/Account/
  Position/Execution; xác định execution eligibility; authorize/reject/size/route order;
  đổi tên một conclusion domain khác thành "context value" để lách ownership.
```

**Terminology (correction v0.2, `P13B-A-MIN-01`/`P13B-IRB-MIN-01` — bắt buộc, KHÔNG resolve bằng cách đổi Context sang authoritative ownership):**

```text
MarketContextSnapshot/MarketContextFactInvalidated records LÀ:
  immutable       — KHÔNG BAO GIỜ ghi đè tại chỗ (§8 no-repaint).
  cursor-bounded  — record đúng CHÍNH XÁC computation cursor/context_cutoff tại thời điểm
                    phát sinh (§7, §11).
  lineage-preserving — correction/invalidation lineage đầy đủ, append-only (§9.2).
  eligible        — kết quả của two-phase Eligible Upstream Fact selection (§5.2 trên,
                    context.md §8) — record CHỈ tồn tại khi bảy fact ref eligible tại
                    computation point đó.

context-aggregator VẪN LÀ:
  projection                        (module-registry.yaml, module_type: projection)
  owns_authoritative_state: false   (module-registry.yaml — KHÔNG đổi bởi correction này)
  rebuildable                       (§5.1 — rebuild từ authoritative event stream)
  KHÔNG authoritative source cho upstream (Structure/Regime/Feature/Candle) HAY bất kỳ
    business domain state nào (Strategy/Decision/Risk/Account/Position/Execution).
```

Gọi một record là "eligible cursor-bounded MarketContextSnapshot projection record" (record-integrity — deterministic, append-only, đúng lineage) — KHÔNG gọi nó "authoritative MarketContextSnapshot" (có thể bị đọc nhầm thành authoritative domain-state ownership, Chapter 7 §7.4 cấm cho Projection). Hai tính chất này **tách biệt**: một record có thể record-integrity hoàn hảo (immutable, cursor-bounded, lineage-preserving) mà KHÔNG phải là authoritative SOURCE cho domain concept nó tổng hợp — đây chính xác là vị trí của `context-aggregator`. Xem §13 cho phạm vi correction này KHÔNG resolve (context.md's own "authoritative event record" envelope framing — Domain Contract text, ngoài phạm vi thay đổi của Package 1.3-B).

### 5.3 Authoritative ownership (không có gì — xác nhận tường minh)

```text
Context Aggregator KHÔNG sở hữu authoritative:
  Structure orientation (Structure Engine sở hữu); Regime class (Raw Regime Engine sở
  hữu); Feature value (Feature Engine sở hữu); Candle fact (Market Data Ingestion sở
  hữu); bất kỳ Strategy/Decision/Risk/Account/Position/Execution semantic nào (Package
  0.2-C/Package 1.3-C, chưa author).

Context Aggregator sở hữu (projection-scoped, KHÔNG phải domain-decision authority):
  MarketContextSnapshot/MarketContextFactInvalidated evidence-assembly identity —
  context_subject_id, correction lineage của CHÍNH snapshot fact đó, MarketContextCurrentView
  read-model shape — xem §13 cho open gap về ranh giới thuật ngữ này.
```

### 5.4 Inputs/outputs theo contract category

```text
Consumes (event):  candle-closed, candle-corrected (context cutoff source, §7.0);
                    break-of-structure-detected, change-of-character-detected,
                    structure-fact-invalidated, structure-recomputed (Structure role,
                    §7.1); regime-classified, regime-fact-invalidated (hai Regime role,
                    §7.2); feature-computed, feature-fact-invalidated (ba Feature role,
                    §7.3) — context.md §16, KHÔNG hơn.
Emits (event):      market-context-snapshot, market-context-fact-invalidated — eligible
                    cursor-bounded MarketContextSnapshot/MarketContextFactInvalidated
                    projection record (correction v0.2, `P13B-A-MIN-01`/`P13B-IRB-MIN-01`
                    — KHÔNG gọi "authoritative", xem §5.2/§13); module-registry.yaml v0.4
                    `emits: [event, query]` (correction v0.4, đóng `P13B-IRB-MAJ-03`) —
                    projection được phép "phát sinh operational metadata event về chính
                    nó", Chapter 7 §7.4; record-integrity (immutable/cursor-bounded/
                    lineage-preserving), KHÔNG authoritative domain-state ownership.
Emits (query):      GetCurrentContext, GetContextHistory.
```

**Không tiêu thụ (context.md §16, xác nhận tường minh):** `CandleObserved`; bất kỳ `*-current-view` nào (kể cả chính `MarketContextCurrentView`); `SwingCandidateDetected`; `Swing` event trực tiếp (Structure đã tự tiêu thụ Swing — Context không đi vòng qua Structure để lấy lại Swing); Strategy/Decision/Risk/Account/Position/Execution/Order/Fill.

### 5.5 Definition-version pinning (Referenced Authoritative Artifact, Chapter 8 §8.1.1)

```text
context_definition_version — pin: required_structure_definition_version;
  required_volatility_regime_definition_version;
  required_directional_persistence_regime_definition_version;
  required_volatility_metric_feature_definition_version;
  required_directional_persistence_metric_feature_definition_version;
  required_distance_to_last_confirmed_swing_feature_definition_version;
  computation_cadence_policy (DRIVEN_BY_CANDLE_CLOSE);
  context_cutoff_policy (CONTEXT_EFFECTIVE_WINDOW_END_INCLUSIVE);
  window_alignment_policy (LATEST_VALID_AT_OR_BEFORE_CONTEXT_CUTOFF);
  eligible_upstream_fact_selection_policy; missing_input_policy (enum đóng, §8 dưới);
  input_normalization_policy; current_view_selection_policy (context.md §6).
Bất biến sau khi tham chiếu — đổi tham số semantic tạo context_definition_version MỚI.
```

### 5.6 Definition-pinned direct fan-in (ADR-014 — cùng nguyên tắc §4.5, áp dụng cho Context)

```text
Layer capability does not authorize an input. The consuming Definition authorizes and
pins the input.
```

Context KHÔNG có một quyền chung để tự thêm một upstream dimension mới — thêm một role mới BẮT BUỘC một `context_definition_version` mới VÀ một Domain Contract revision tường minh cho `context.md` (ADR-014 "Context" clause), KHÔNG tự phát sinh ngầm tại Package 1.3-B.

## 6. Determinism, replay và no-repaint constraints (I-2/I-3)

```text
Mode parity (I-2):  cùng definition_version + cùng upstream causal ancestry → cùng tập
                     fact, mọi execution mode (Live/Backtest/Paper/Replay) — bắt buộc,
                     đúng feature.md §13/context.md §15.

Feature Engine no-repaint:
  FeatureComputed KHÔNG BAO GIỜ ghi đè tại chỗ — chỉ phủ định qua FeatureFactInvalidated
  + replacement, append-only (I-3, feature.md §13). Deterministic total order 7-tiêu-chí
  cho FeatureCurrentView (feature.md §11); Eligible-Swing total order 8-tiêu-chí cho
  distance_to_last_confirmed_swing (feature.md §9a — CHỈ chạy SAU khi effective-time
  cutoff filter §9a bước 3 đã lọc, KHÔNG bao giờ hợp thức hóa một Swing ineligible).

Context Aggregator no-repaint:
  MarketContextSnapshot KHÔNG BAO GIỜ ghi đè tại chỗ — chỉ phủ định qua
  MarketContextFactInvalidated + replacement, append-only (I-3, context.md §15).
  Deterministic total order 7-tiêu-chí cho MarketContextCurrentView (context.md §13);
  Eligible Upstream Fact two-phase selection + 7-tiêu-chí tie-break total order CHỈ dùng
  trong Phase 2 (context.md §8).

No look-ahead qua batch recomputation (cả hai): historical Backtest/Replay tại cursor
  MUỘN PHẢI reconstruct MỖI fact chỉ dùng input thỏa CẢ HAI điều kiện tại đúng computation
  cursor của CHÍNH fact đó — recorded-time visible VÀ effective-time eligible (feature.md
  §13, đóng RA-B3-MAJ-01/IRB-B3-MAJ-01; context.md §15, cùng nguyên tắc áp dụng cho cả
  bảy role). Một fact effective muộn hơn KHÔNG BAO GIỜ "nhảy vào" một computation point
  sớm hơn nó ineligible, dù nó recorded-time visible tại cursor batch muộn.

Ordering mechanism (ADR-009): per-stream contiguous sequence + explicit causation, KHÔNG
  global total order — cấm so sánh sequence thô xuyên hai stream identity khác nhau
  (Chapter 8 §8.3.3) — áp dụng đồng nhất cho cả feature-engine và context-aggregator.
  Protocol/implementation cụ thể của ADR-009 là Phase 1 elaboration KHÔNG khóa tại tài
  liệu này (§13 dưới, cùng gap Package 1.3-A đã ghi nhận).
```

## 7. Event-time và recorded-time treatment

```text
effective_window / effective_time  — [window_start, window_end) của CHÍNH fact đó (feature.md
                                      §3/§12; context.md §3/§14) — mỗi fact có window riêng.
recorded_time                       — khi Ride tính/ghi nhận fact này (envelope bắt buộc).
market_time                         — PROHIBITED cho cả Feature và Context (derived/computed
                                      fact, không phải quan sát trực tiếp venue).

Feature input eligibility (feature.md §12, hai điều kiện ĐỘC LẬP, cả hai PHẢI đúng):
  (a) input.recorded_time <= computation cursor           — recorded-time visibility
  (b) input effective time thỏa cutoff riêng feature_type — effective-time eligibility

Context input eligibility (context.md §14, cùng nguyên tắc, áp dụng cho cả bảy role):
  (a) role fact.recorded_time <= computation cursor       — recorded-time visibility
  (b) role fact effective boundary <= context_cutoff       — effective-time eligibility
                                                              (INCLUSIVE — context.md §8
                                                              bước 3, khác Feature's Eligible-
                                                              Swing cutoff EXCLUSIVE, feature.md
                                                              §9a bước 3 — hai policy riêng
                                                              biệt, KHÔNG đồng nhất giả định)

context_cutoff = effective_window.window_end của context_cutoff_source_ref (Candle) —
  computation_cadence_policy: DRIVEN_BY_CANDLE_CLOSE (context.md §6/§11): mỗi Candle
  authoritative mới định nghĩa đúng MỘT computation point Context mới.
```

**Xác nhận tường minh:** cutoff-inclusivity của Context (`INCLUSIVE`) và cutoff-exclusivity của Feature's Eligible-Swing (`EXCLUSIVE`) là hai policy semantic khác nhau, pin riêng tại từng Domain Contract (feature.md §6/§9a; context.md §6/§8) — Package 1.3-B KHÔNG hòa hợp/thống nhất chúng thành một quy tắc chung, chỉ ghi nhận đúng nguyên trạng.

## 8. Context criticality và failure policy (Chapter 7 §7.4 + I-6 — bắt buộc, Context là dependency của Decision)

**Xác nhận tường minh (Independent Review B scope, `phase-1-plan.md` §8 Package 1.3-B block):** `context-aggregator` LÀ dependency của Decision evaluation — `module-registry.yaml` v0.4 (`decision-evaluation-engine.depends_on: [strategy-engine, strategy-plugin-host, context-aggregator]`, Package 1.1 `Consolidated Stable`). Theo Chapter 7 §7.4: "một projection được dùng làm dependency của decision/risk/execution... phải khai báo criticality và failure policy tường minh; khi tính đúng đắn hoặc độ freshness của nó không xác định, consumer phải fail-safe theo I-6."

```text
Criticality:              Context Aggregator LÀ critical dependency cho Decision
                           evaluation — KHÔNG được coi non-critical/best-effort khi phục
                           vụ Decision Evaluation Engine (Package 1.3-C).

Khi missing context LÀ valid absence (context.md §9, KHÔNG phải lỗi):
  Trước MarketContextSnapshot ĐẦU TIÊN cho một context_subject_id (UNCOMPUTED) — KHÔNG
    có row, GetCurrentContext trả NOT_FOUND/ABSENT (§5, §13 — no-row semantics).
  Bất kỳ trong bảy role fact rơi vào absent/invalidated-without-replacement/pending-
    correction/definition-version-mismatch/effective-time-ineligible tại một computation
    point → KHÔNG MarketContextSnapshot nào phát cho điểm đó (missing_input_policy:
    NO_SNAPSHOT_WHEN_ANY_REQUIRED_ROLE_MISSING_OR_PENDING, enum đóng, context.md §9).
  Đây là valid absence THEO THIẾT KẾ — Context TỰ nó đã fail-closed ở tầng aggregation,
    KHÔNG bao giờ phát null-filled/partial/stale-fallback snapshot (context.md §9 cấm
    tuyệt đối: null filling; stale fallback trình bày như current; partial snapshot;
    implementation-selected behavior; copy snapshot cũ hơn như đại diện điểm hiện thiếu).

Khi context LÀ incomplete hoặc stale (context.md §13, view_state):
  view_state: PENDING_CORRECTION — lineage head của target window có
    MarketContextFactInvalidated visible, replacement CHƯA visible. Đây là giá trị
    tường minh consumer PHẢI đọc được — KHÔNG BAO GIỜ fallback ngầm về giá trị đã
    invalidate, KHÔNG BAO GIỜ fallback về window cũ hơn target window.
  Freshness của một row VALID được consumer tự đánh giá qua effective_window +
    last_recorded_time — Context KHÔNG tự định nghĩa một staleness threshold riêng
    ngoài view_state hai giá trị (VALID/PENDING_CORRECTION) đã pin — không có giá trị
    thứ ba (context.md §5 invariant).

Khi Decision evaluation PHẢI fail closed (kiến trúc-level requirement, KHÔNG author
  Decision algorithm tại đây — Package 1.3-C elaborate cơ chế cụ thể):
  (a) computation cursor của Decision evaluation KHÔNG có eligible cursor-bounded
      MarketContextSnapshot projection record tương ứng (absence) — Decision evaluation
      KHÔNG được tiến hành với một window cũ hơn thay thế ngầm;
  (b) lineage head applicable đang view_state: PENDING_CORRECTION — Decision evaluation
      KHÔNG được coi giá trị đã invalidate là còn hợp lệ;
  (c) required context_definition_version của Decision Evaluation Engine không khớp
      context_definition_version đã pin tại snapshot có sẵn (definition-version mismatch).
  Cả ba trường hợp trên là fail-safe-by-scope (I-6) tại consumer — Package 1.3-B chỉ
  pin YÊU CẦU boundary này, KHÔNG author cơ chế/algorithm cụ thể của Decision Evaluation
  Engine (Package 1.3-C, forbidden scope của tài liệu này).

Provenance/cursor metadata PHẢI remain traceable (context.md §3):
  context_cutoff_source_ref + sáu role fact ref (structure_fact_ref,
  volatility_regime_fact_ref, directional_persistence_regime_fact_ref, ba
  feature_fact_refs) + normalized_input_fact_refs (bảy phần tử) + effective_window +
  supersedes_fact_ref (khi correction) — MỌI Decision evaluation tương lai tiêu thụ một
  MarketContextSnapshot PHẢI giữ được exact evidence reference này qua causation_refs
  (Chapter 8 §8.2.3) khi tự nó phát sinh authoritative event — cơ chế wiring cụ thể là
  Package 1.3-C scope, KHÔNG author tại đây.
```

## 9. Correction và invalidation propagation

### 9.1 Feature Engine correction lineage (feature.md §9)

```text
Scoped chính xác theo (feature_subject_id, effective_window) — mỗi window lineage RIÊNG.
FeatureComputed F1 → FeatureFactInvalidated targeting F1 → replacement F2
  (supersedes_fact_ref = F1) — KHÔNG nhảy cóc qua head trung gian.
Một upstream correction (Candle/Swing/Regime) ảnh hưởng NHIỀU Feature fact overlapping
  → invalidate + replacement ĐỘC LẬP cho MỖI window bị ảnh hưởng, KHÔNG dependency-forward
  ordering giữa các window độc lập (trừ khi một Feature-to-Feature dependency tường minh
  được author — B3 KHÔNG author, feature.md §10).
```

### 9.2 Context Aggregator correction lineage (context.md §12)

```text
Scoped chính xác theo (context_subject_id, effective_window) — mỗi window lineage RIÊNG.
MarketContextSnapshot C1 → MarketContextFactInvalidated targeting C1 → replacement C2
  (supersedes_fact_ref = C1) — KHÔNG nhảy cóc.
Một upstream correction (Candle/Structure/Regime/Feature) ảnh hưởng NHIỀU
  MarketContextSnapshot overlapping → invalidate + replacement ĐỘC LẬP cho MỖI window,
  KHÔNG dependency-forward ordering giữa các window độc lập — Context KHÔNG cần tái tạo
  cascade nội bộ của Structure (Package 1.3-A §9.1), CHỈ tiêu thụ kết quả
  StructureFactInvalidated/StructureRecomputed ĐÃ HOÀN TẤT từ structure-engine.
Nhiều role bị ảnh hưởng đồng thời bởi CÙNG một correction gốc trên MỘT snapshot → chỉ
  phát ĐÚNG MỘT MarketContextFactInvalidated, affected_upstream_roles liệt kê đủ mọi
  role, causation_refs liệt kê đủ mọi nguyên nhân (đóng dedup-cascade attack scenario,
  đúng nguyên tắc structure.md §10).
```

**Kiến trúc consequence (elaboration, KHÔNG redefine domain semantics):** Context Aggregator KHÔNG cần một transaction boundary xử lý cascade nhiều-fact có thứ tự phụ thuộc (khác Structure Engine, Package 1.3-A §9.1) — mỗi window Context được invalidate/replace độc lập, đúng pattern Raw Regime Engine (Package 1.3-A §9.2) đã thiết lập; Context CHỈ cần consume đúng MỘT correction event settled cho mỗi role bị ảnh hưởng, không tự cascade nội bộ.

## 10. Stale/incomplete Context behavior — tổng hợp (xem chi tiết §8/§9)

```text
Stale (view_state: PENDING_CORRECTION)      → §8 "Khi context LÀ incomplete hoặc stale"
Incomplete (một trong bảy role missing)     → §8 "Khi missing context LÀ valid absence"
                                               — KHÔNG snapshot phát sinh cho điểm đó,
                                               KHÔNG partial snapshot BAO GIỜ tồn tại
                                               (context.md §9 cấm tuyệt đối).
Rebuild sau invalidation                    → §9.2 correction lineage; MarketContextCurrentView
                                               rebuild deterministic từ authoritative event
                                               stream (Chapter 7 §7.4 rebuild determinism,
                                               §5.1 "rebuildable").
```

Không có nhánh "degraded Context" nào ngoài hai trạng thái đã pin (VALID/PENDING_CORRECTION cho row đã tồn tại; NOT_FOUND/ABSENT khi row chưa tồn tại) — Package 1.3-B KHÔNG invent một staleness/degradation state thứ ba nào ngoài những gì `context.md` §5/§13 đã khóa.

## 11. Security / trust-boundary identification

```text
Feature Engine, Context Aggregator:  security_classification: none (module-registry.yaml
  v0.4, KHÔNG đổi bởi correction v0.2/registry v0.4 — chỉ depends_on/emits đổi) — không
  chạm external network boundary trực tiếp, không sở hữu
  credential/secret material. Cả hai tiêu thụ CHỈ internal authoritative event stream
  (Candle/Swing/Structure/Regime/Feature) — external venue trust boundary đã được cô lập
  hoàn toàn tại Market Data Ingestion (Package 1.3-A §12, trust_boundary_candidate).

Trigger D (quality-gate, boundary-triggered):  KHÔNG áp dụng cho cả hai module
  (phase-1-plan.md §8 Package 1.3-B block: "Trigger D KHÔNG áp dụng — không
  custody/isolation boundary ở Compute Engine/Projection thuần").
```

## 12. Preserved boundaries (xác nhận tường minh, yêu cầu task)

```text
Structure Engine và Raw Regime Engine independence:  KHÔNG đổi (Package 1.3-A §11) —
  KHÔNG dependency edge nào giữa structure-engine/raw-regime-engine theo bất kỳ hướng
  nào; tài liệu này KHÔNG thêm/sửa edge này.

Feature Engine như downstream selective fan-in:  giữ nguyên §4 — KHÔNG universal join,
  KHÔNG Feature-to-Feature dependency (feature.md §10, deferred).

Decision Evaluation Engine ngoài phạm vi Package 1.3-B:  KHÔNG author algorithm/logic
  của decision-evaluation-engine — chỉ ghi nhận nó LÀ consumer của context-aggregator
  (§8) như một architecture fact đã pin tại Package 1.1.

Decision Authority Service ngoài phạm vi Package 1.3-B:  KHÔNG chạm — module này không
  nằm trong dependency trực tiếp của feature-engine/context-aggregator.

Context Aggregator non-authoritative:  KHÔNG đổi — §5.1/§5.3 xác nhận owns_authoritative_
  state: false, KHÔNG là authoritative source cho Structure/Regime/Feature.

Decision → Risk → Execution chain:  KHÔNG chạm — ngoài phạm vi hoàn toàn của hai module
  trong Package 1.3-B.

Package 1.3-A correction semantics:  KHÔNG sửa Package 1.3-A — Structure dependency-
  forward cascade / Regime independent-per-window (Package 1.3-A §9.1/§9.2) trích dẫn
  nguyên văn tại §9 trên, KHÔNG redefine.
```

## 13. Open Domain và architecture gaps (KHÔNG resolve, chỉ carry forward)

```text
Terminology tension — "authoritative event record" (context.md §2, Chapter 8 §8.2 envelope
  framing) vs "projection, owns_authoritative_state: false, cấm phát sinh authoritative
  domain fact" (module-registry.yaml Notes, Chapter 7 §7.4) — **PARTIALLY addressed tại
  v0.2 (`P13B-A-MIN-01`/`P13B-IRB-MIN-01`), KHÔNG fully resolved:**
  context.md (Package 0.2-B4, Consolidated Stable, KHÔNG đổi bởi Package 1.3-B) mô tả
  MarketContextSnapshot/MarketContextFactInvalidated bằng đúng khuôn envelope
  "authoritative event record" (Chapter 8 §8.2, giống hệt cấu trúc
  candle-closed/swing-confirmed/regime-classified/feature-computed — full lineage,
  supersedes_fact_ref, causation_refs) — trong khi module-registry.yaml (Package 1.1,
  Consolidated Stable) phân loại context-aggregator là Type 2 Projection,
  owns_authoritative_state: false, và Chapter 7 §7.4 tường minh cấm Projection "phát
  sinh authoritative domain fact". **v0.2 correction đã sửa PHẦN Package 1.3-B tự kiểm
  soát được:** tài liệu này (§5.2 "Terminology") nay nhất quán gọi record của Context là
  "eligible cursor-bounded MarketContextSnapshot projection record" (record-integrity —
  immutable/cursor-bounded/lineage-preserving), KHÔNG còn gọi nó "authoritative
  MarketContextSnapshot" như một khẳng định của CHÍNH tài liệu này — tách bạch tường minh
  record-integrity khỏi authoritative domain-state ownership, KHÔNG đổi
  `owns_authoritative_state` sang `true`. **PHẦN KHÔNG resolve (ngoài phạm vi Package
  1.3-B):** chính văn bản `context.md` §2 vẫn dùng khuôn "authoritative event record" cho
  MarketContextSnapshot — Domain Contract này KHÔNG được sửa bởi Package 1.3-B (§14 non-
  goal), nên tension giữa văn bản context.md và văn bản module-registry.yaml VẪN tồn tại
  ở tầng Domain Contract, độc lập với cách Package 1.3-B tự diễn giải nó. Package 1.3-B
  KHÔNG sửa context.md/module-registry.yaml's Chapter 7 classification, KHÔNG tạo ADR cho
  tension này — điều kiện ADR rule của task (fan-in ngoài ADR-014 / đổi authority boundary
  hiện có) KHÔNG bị kích hoạt vì Package 1.3-B không đề xuất mở rộng fan-in hay đổi
  boundary nào, kể cả tại correction v0.2 này. Ghi nhận tường minh cho Product Owner
  awareness — carry forward, KHÔNG blocking. **Cập nhật (2026-08-04, Product Owner
  consolidation decision):** Package 1.3-B v0.2 nay `Consolidated Stable` VỚI ĐÚNG gap này
  bảo lưu tường minh, KHÔNG resolve — Product Owner quote: "...with the context.md
  authority-terminology tension preserved as an explicit non-blocking open gap."
  Consolidation KHÔNG chọn một Context authority model mới, KHÔNG đổi
  `owns_authoritative_state`, KHÔNG sửa `context.md`.

Structure-aware Regime (Package 1.3-A §13, KHÔNG thay đổi):  vẫn blocked trên Domain
  Context/Capability registration — Feature/Context không tạo thêm phụ thuộc mới vào
  gap này.

Swing/Structure/Regime/Feature/Context Definition Version registry mechanism:
  feature_definition_version/context_definition_version đều "opaque, immutable pin —
  Referenced Authoritative Artifact" (Chapter 8 §8.1.1) nhưng cơ chế lưu trữ/versioning
  CỤ THỂ của registry này là Phase 1 concern CHƯA elaborate (feature.md §20/context.md
  §22 tự defer, cùng Package 1.3-A §13 đã ghi nhận cho Swing/Structure/Regime).

ADR-009 ordering protocol implementation:  cùng gap Package 1.3-A §13 — Package 1.3-B
  chỉ áp dụng nguyên tắc (per-stream contiguous sequence + explicit causation), KHÔNG
  author protocol cụ thể.

stream-registry.yaml / producer_ref resolution — PARTIALLY addressed (v0.3, KHÔNG fully
  resolved): `docs/architecture/stream-registry.yaml` v0.1 (Approved) và ba Feature-scoped
  Input Contract Draft (`docs/architecture/input-contracts/feature-*.yaml`, §4.6 trên) nay
  tồn tại và persistently resolvable (Chapter 8 §8.1.1) — resolves the artifact-existence
  half of this gap for Feature's `included_streams`/`stream_registry_version`. **VẪN mở:**
  (a) `stream_ref.registry_version`/`producer_ref` population in actual
  `market-data-ingestion`/`structure-engine`/`raw-regime-engine`/`feature-engine` code
  (`"v0"`/flat placeholders identified by ADR-036, not yet replaced — Phase 3 implementation,
  KHÔNG author tại đây); (b) Candle/Swing/Regime/Feature Event Contracts still not authored
  (needed for `causal_closure_policy: declared-state-dependencies` to be operationally
  provable, §4.6); (c) Context Aggregator's own `producer_ref`/`stream_ref` resolution —
  Context has no Feature-scoped Input Contract of its own, still fully open, unchanged by
  this correction. Same gap Package 1.3-A §13 also carries for market-data-ingestion/
  structure-engine/raw-regime-engine's own producer_ref population.

Feature Definition dual-path ambiguity (feature.md §20, author-level note, KHÔNG governance
  OQ):  khi upstream_source: regime, liệu Feature Definition có cần convert unit/
  decimal_precision_policy khác với Regime's own computed_metric hay không — chưa quyết,
  không chặn Package 1.3-B.

Decision evaluation fail-closed MECHANISM cụ thể (§8):  Package 1.3-B pin YÊU CẦU
  boundary (Decision evaluation PHẢI fail closed khi Context absent/pending/mismatch) —
  cơ chế thực thi cụ thể (retry, circuit breaker, alerting, timeout) là Package 1.3-C
  scope, CHƯA author tại đây.
```

## 14. Explicit non-goals

```text
KHÔNG author field-level event schema (đã khóa tại feature.md/context.md, Package
  0.2-B3/B4, Consolidated Stable) — chỉ contract CATEGORY (event/query/command).
KHÔNG author Engine algorithm/formula/threshold cụ thể (formula_id, class_thresholds,
  eligible_swing_selection_policy VALUE — thuộc Domain Contract policy schema, đã khóa).
KHÔNG author database schema/DDL.
KHÔNG chọn deployment infrastructure/cloud provider/message broker/runtime topology.
KHÔNG chọn programming language/framework.
KHÔNG author stream-registry.yaml hay bất kỳ Definition Version registry mechanism cụ
  thể nào (§13 — ghi nhận gap, không resolve).
KHÔNG author Context làm authoritative decision owner (Chapter 7 §7.4, cấm tường minh —
  phase-1-plan.md §8 Package 1.3-B explicit non-goal).
KHÔNG redefine module identity/taxonomy/dependency đã pin tại Package 1.1
  (module-registry.yaml/system-decomposition.md v0.4, Consolidated Stable).
KHÔNG redefine Structure Engine/Raw Regime Engine boundary đã pin tại Package 1.3-A
  (Consolidated Stable).
KHÔNG author Package 1.3-C/1.3-D.
KHÔNG author Strategy hay Decision logic (chỉ pin YÊU CẦU boundary criticality/failure
  policy tại §8 — KHÔNG author cơ chế/algorithm cụ thể).
KHÔNG resolve Domain Contract nào còn thiếu.
KHÔNG author field-level API/database schema.
KHÔNG chọn framework/broker/database/deployment topology.
KHÔNG author source code hay test.
KHÔNG tạo/approve ADR nào.
KHÔNG mark Package 1.3-B Consolidated Stable.
KHÔNG pass Gate 2.
KHÔNG tuyên bố Phase 1 hoàn thành.
KHÔNG mở Phase 2.
KHÔNG authorize Live.
```

## 15. Review and consolidation conditions

```text
Review A scope:              Context KHÔNG sở hữu upstream computation (Chapter 7 §7.4);
                              Feature fan-in đúng ADR-014 Definition-pinned direct fan-in
                              (§4.5/§5.6); module boundary elaboration (§4/§5) nhất quán
                              với module-registry.yaml v0.4 (Consolidated Stable) — không
                              silent semantic invention; §13 terminology tension KHÔNG bị
                              lấp bằng một resolution tự phát minh; §5.2 terminology
                              ("eligible cursor-bounded ... projection record") KHÔNG đổi
                              Context sang authoritative ownership; no-repaint/
                              determinism/replay treatment (§6/§7) đúng Domain Contract
                              invariant, không suy diễn thêm; §2/§3 market-data-ingestion
                              edge khớp CHÍNH XÁC feature.md §7.1/§7.3 và context.md
                              §7.0/§11 (P13B-IRB-MAJ-01/MAJ-02 correction verification).
Independent Review B
  scope:                     Độc lập xác nhận Context criticality/failure policy tường
                              minh (§8) — đúng Chapter 7 §7.4 yêu cầu vì Context LÀ
                              dependency của Decision (decision-evaluation-engine.depends_on
                              chứa context-aggregator, module-registry.yaml v0.4); xác nhận
                              §4.1 KHÔNG invent universal join requirement; xác nhận mọi
                              open gap (§13) được ghi nhận trung thực, KHÔNG bị silently
                              resolved; xác nhận KHÔNG Decision authority nào rò rỉ vào
                              tài liệu này (§5.1/§5.3/§12); xác nhận `context-aggregator`
                              vẫn `owns_authoritative_state: false` sau correction v0.2/v0.4
                              (P13B-IRB-MAJ-03 verification — emits: [event, query] KHÔNG
                              làm Context trở thành authoritative source).
Product Owner decision
  point:                     Sau Review A/B CLEAN. **Cập nhật (2026-08-04, Product Owner
                              consolidation decision):** Review A CLEAN (Blocker 0/Major
                              0/Minor 1) trên v0.1; Independent Review B REVISE (Blocker
                              0/Major 3/Minor 1) trên v0.1 — ba Major xác nhận là
                              `P13B-IRB-MAJ-01`/`P13B-IRB-MAJ-02`/`P13B-IRB-MAJ-03`, một
                              Minor xác nhận là `P13B-A-MIN-01`/`P13B-IRB-MIN-01`. Bounded
                              correction hoàn tất tại HEAD
                              `71007bf1063c012001eb34465f41c0ce4905b7cf` (v0.1 → v0.2,
                              `module-registry.yaml`/`system-decomposition.md` v0.3 →
                              v0.4). Final bounded verification: CLEAN — mọi Major finding
                              đóng, không Minor nào còn cần correction. Product Owner đã
                              quyết định: "I approve consolidation of Package 1.3-B v0.2
                              as the current Consolidated Stable architecture baseline,
                              with the context.md authority-terminology tension preserved
                              as an explicit non-blocking open gap." — Package 1.3-B nay
                              **`Consolidated Stable`**.
Consolidation condition:     Zero unresolved Blocker/Major (**THỎA** — ba Major đóng qua
                              bounded correction, final verification CLEAN); không vi
                              phạm ADR-014 boundary (**THỎA**). §13 terminology-tension
                              open gap bảo lưu tường minh, KHÔNG blocking, KHÔNG resolve
                              bởi consolidation này (**THỎA, theo đúng Product Owner
                              decision quote**). **Mọi điều kiện consolidation ĐÃ thỏa —
                              Package 1.3-B v0.2 nay `Consolidated Stable`.**
```
