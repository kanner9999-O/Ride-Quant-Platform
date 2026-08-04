---
id: feature-context-architecture
title: "Package 1.3-B — Feature & Context Engine Architecture"
version: "0.1"
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

**CANDIDATE — status: Draft, KHÔNG Consolidated Stable, KHÔNG Approved.** Package 1.3-B v0.1 là candidate đầu tiên, author dựa trên Package 1.1 `Consolidated Stable` và Package 1.3-A `Consolidated Stable` (xem §1), theo [`phase-1-plan.md`](../phase-1-plan.md) v0.4 (`Approved`) §8 Package 1.3-B block. Chưa qua Review A/Independent Review B, chưa có Product Owner consolidation decision.

## 0. Vai trò của tài liệu này

Package 1.3-B elaborate **kiến trúc kỹ thuật** cho hai module ĐÃ được Package 1.1 (`Consolidated Stable`, [`module-registry.yaml`](../module-registry.yaml) v0.3 blob `ab09d031183014c1af259895dadf86aaf644cc04`, [`system-decomposition.md`](../system-decomposition.md) v0.3 blob `c72dfdf54d2ac86bc7ad83de742dda485da11328`) thiết lập identity/taxonomy/dependency: `feature-engine`, `context-aggregator`. Tài liệu này **KHÔNG redefine** module identity/taxonomy/dependency đã pin ở Package 1.1 — chỉ elaborate: responsibility boundary chi tiết hơn, dependency direction, selective fan-in treatment, definition-version pinning, event-time/recorded-time treatment, determinism/replay/no-repaint, Context aggregation/projection semantics, Context criticality/failure policy, correction/invalidation propagation, stale/incomplete Context behavior, security/trust-boundary identification, và open gap — đúng phạm vi `phase-1-plan.md` §8 Package 1.3-B "Purpose: Kiến trúc kỹ thuật cho Feature Engine (fan-in có chọn lọc từ Structure) và Context Aggregation (CQRS, aggregator)".

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
module-registry.yaml v0.3 (Consolidated Stable):  module identity/taxonomy/dependency
                                                    authority — KHÔNG redefine tại đây
system-decomposition.md v0.3 (Consolidated        official Phase 1 module dependency graph
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

Hai module dưới đây trích dẫn NGUYÊN VĂN `module-registry.yaml` v0.3 (identity/taxonomy/dependency KHÔNG đổi) — cột "Elaboration" là nội dung MỚI của tài liệu này:

| module_id | module_type | owns_authoritative_state | depends_on | forbidden_dependencies |
|---|---|---|---|---|
| `feature-engine` | compute_engine | true | `structure-engine`, `raw-regime-engine` | (none) |
| `context-aggregator` | projection | false | `structure-engine`, `raw-regime-engine`, `feature-engine` | (none) |

**Xác nhận (yêu cầu task):** `depends_on` ở registry-level là ranh giới **permitted connectivity** — module ĐƯỢC PHÉP tiêu thụ contract từ module đích, KHÔNG phải "mọi instance computation PHẢI tiêu thụ cả hai/cả ba module đó cùng lúc". Ranh giới thực sự per-computation nằm ở `feature_definition_version`/`context_definition_version` (ADR-014 "Definition-pinned direct fan-in" — xem §4.5/§5.6).

## 3. Data flow (dependency-direction view — KHÔNG runtime topology)

```text
Structure Engine (Package 1.3-A, Consolidated Stable)   Raw Regime Engine (Package 1.3-A,
  emits: break-of-structure-detected,                     Consolidated Stable)
    change-of-character-detected,                         emits: regime-classified,
    structure-fact-invalidated, structure-recomputed,        regime-fact-invalidated
    swing-candidate-detected, swing-confirmed,
    swing-invalidated
         │                    │                    │
         │ (Swing layer       │ (regime path,       │ (Structure orientation +
         │  ONLY —            │  optional per        │  cả hai Regime dimension +
         │  feature.md §14)   │  feature_definition_ │  ba Feature value, ADR-014
         │                    │  version)            │  Context aggregation)
         ▼                    ▼                      │
    Feature Engine (compute_engine, selective fan-in) │
      emits: feature-computed, feature-fact-invalidated
         │                                            │
         └───────────────────┬────────────────────────┘
                              ▼
                    Context Aggregator (projection)
                      emits: market-context-snapshot,
                        market-context-fact-invalidated
                              │
                              ▼
              Strategy/Decision Engine (Package 1.3-C — KHÔNG thuộc phạm vi tài liệu này)
```

**Xác nhận tường minh (yêu cầu task):** đây là responsibility/dependency view — KHÔNG phải authorization triển khai một synchronous pipeline hay runtime topology cụ thể. Việc chọn cơ chế thực thi cụ thể thuộc Engineering/Phase 1 execution-topology decision (`phase-1-plan.md` §7), KHÔNG quyết định tại Package 1.3-B.

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

**Xác nhận tường minh (yêu cầu task — "Do not invent universal join requirements"):** module-level `depends_on: [structure-engine, raw-regime-engine]` (§2) là **union** của permitted connectivity cho ba feature type khác nhau, KHÔNG phải một yêu cầu mỗi computation phải join cả hai luồng. Chỉ khi một `feature_definition_version` tương lai thực sự cần cả Structure lẫn Regime cùng lúc (ADR-014 "selective cross-domain synthesis" — chưa dùng ở B3 minimal scope) thì synchronization mới xảy ra bên trong CHÍNH một Feature Definition đó — vẫn KHÔNG phải một universal rule.

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
downstream of         module-level depends_on: [structure-engine, raw-regime-engine,
Feature Engine:       feature-engine] (§2) — Context fan-in SONG SONG từ cả ba, KHÔNG
                      route qua Feature Engine (§3 "Điểm kiến trúc quan trọng").
not owner of upstream Context KHÔNG tự tính một engineered Feature mới, KHÔNG tái sản xuất
computation:          công thức/transformation của Feature Engine (context.md §17,
                      ADR-014 prohibition list).
not Decision          Context là "authoritative market-state snapshot, KHÔNG phải một
authority:            decision" (context.md §17) — KHÔNG đưa ra kết luận Strategy/Decision/
                      Risk/Account/Position/Execution; KHÔNG xác định execution eligibility;
                      KHÔNG authorize/reject/size/route một order (ADR-014 prohibition,
                      xem §5.4 dưới).
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
Emits (query):      MarketContextSnapshot/MarketContextFactInvalidated (event, đúng
                    module-registry.yaml Notes — projection được phép "phát sinh
                    operational metadata event về chính nó", Chapter 7 §7.4); GetCurrentContext,
                    GetContextHistory (query, module-registry.yaml `emits: [query]`).
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

**Xác nhận tường minh (Independent Review B scope, `phase-1-plan.md` §8 Package 1.3-B block):** `context-aggregator` LÀ dependency của Decision evaluation — `module-registry.yaml` v0.3 (`decision-evaluation-engine.depends_on: [strategy-engine, strategy-plugin-host, context-aggregator]`, Package 1.1 `Consolidated Stable`). Theo Chapter 7 §7.4: "một projection được dùng làm dependency của decision/risk/execution... phải khai báo criticality và failure policy tường minh; khi tính đúng đắn hoặc độ freshness của nó không xác định, consumer phải fail-safe theo I-6."

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
  (a) computation cursor của Decision evaluation KHÔNG có MarketContextSnapshot
      authoritative tương ứng (absence) — Decision evaluation KHÔNG được tiến hành với
      một window cũ hơn thay thế ngầm;
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
  v0.3, KHÔNG đổi) — không chạm external network boundary trực tiếp, không sở hữu
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
  domain fact" (module-registry.yaml Notes, Chapter 7 §7.4):
  context.md mô tả MarketContextSnapshot/MarketContextFactInvalidated bằng đúng khuôn
  envelope "authoritative event record" (Chapter 8 §8.2, giống hệt cấu trúc
  candle-closed/swing-confirmed/regime-classified/feature-computed — full lineage,
  supersedes_fact_ref, causation_refs) — trong khi module-registry.yaml (Package 1.1,
  Consolidated Stable) phân loại context-aggregator là Type 2 Projection,
  owns_authoritative_state: false, và Chapter 7 §7.4 tường minh cấm Projection "phát
  sinh authoritative domain fact". Package 1.3-B đọc hai nguồn này theo hướng: snapshot
  event của Context "authoritative" CHỈ theo nghĩa hẹp — chính bản ghi snapshot đó
  deterministic/append-only/có lineage đúng chuẩn envelope (data-integrity property,
  Chapter 7 §7.4 cho phép Projection "phát sinh operational metadata event về chính
  nó") — KHÔNG có nghĩa Context trở thành authoritative SOURCE cho Structure/Regime/
  Feature/Strategy/Decision (đó vẫn là cấm tuyệt đối, ADR-014 + context.md §17). Đây là
  MỘT cách đọc hợp lý, KHÔNG PHẢI một resolution chính thức — hai tài liệu nguồn (context.md
  Package 0.2-B4, module-registry.yaml Package 1.1) đều đã Consolidated Stable TRƯỚC
  Package 1.3-B và KHÔNG tự mâu thuẫn tường minh với nhau về mặt văn bản đã pin. Package
  1.3-B KHÔNG sửa context.md/module-registry.yaml, KHÔNG tạo ADR cho tension này — điều
  kiện ADR rule của task (fan-in ngoài ADR-014 / đổi authority boundary hiện có) KHÔNG bị
  kích hoạt vì Package 1.3-B không đề xuất mở rộng fan-in hay đổi boundary nào. Ghi nhận
  tường minh cho Product Owner awareness — carry forward, KHÔNG blocking.

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

stream-registry.yaml / producer_ref resolution:  cùng gap Package 1.3-A §13 —
  stream_ref/producer_ref của feature-computed/market-context-snapshot resolve từ
  stream-registry.yaml (Chapter 8 §8.3.1, Phase 1, CHƯA author) — KHÔNG author tại đây.

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
  (module-registry.yaml/system-decomposition.md v0.3, Consolidated Stable).
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
                              với module-registry.yaml v0.3 (Consolidated Stable) — không
                              silent semantic invention; §13 terminology tension KHÔNG bị
                              lấp bằng một resolution tự phát minh; no-repaint/
                              determinism/replay treatment (§6/§7) đúng Domain Contract
                              invariant, không suy diễn thêm.
Independent Review B
  scope:                     Độc lập xác nhận Context criticality/failure policy tường
                              minh (§8) — đúng Chapter 7 §7.4 yêu cầu vì Context LÀ
                              dependency của Decision (decision-evaluation-engine.depends_on
                              chứa context-aggregator, module-registry.yaml v0.3); xác nhận
                              §4.1 KHÔNG invent universal join requirement; xác nhận mọi
                              open gap (§13) được ghi nhận trung thực, KHÔNG bị silently
                              resolved; xác nhận KHÔNG Decision authority nào rò rỉ vào
                              tài liệu này (§5.1/§5.3/§12).
Product Owner decision
  point:                     Sau Review A/B CLEAN.
Consolidation condition:     Zero unresolved Blocker/Major; không vi phạm ADR-014
                              boundary.
```
