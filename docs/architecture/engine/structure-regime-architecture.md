---
id: structure-regime-architecture
title: "Package 1.3-A — Data Ingestion & Structure/Regime Engine Architecture"
version: "0.2"
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

# Package 1.3-A — Data Ingestion & Structure/Regime Engine Architecture

**CONSOLIDATED STABLE (package lifecycle, 2026-08-04, Product Owner decision) — artifact status: Draft, KHÔNG Approved/Locked.** Package 1.3-A v0.1 đạt `Consolidated Stable` SAU Review A CLEAN + Independent Review B CLEAN (Blocker 0/Major 0/Minor 0) và Product Owner consolidation decision (2026-08-04, §15), theo [`phase-1-plan.md`](../phase-1-plan.md) v0.4 (`Approved`) §8 Package 1.3-A block. `Consolidated Stable` LÀ package lifecycle/readiness state (Chapter 0 §7.1) — KHÔNG có nghĩa artifact `Approved`/`Locked`; `status: Draft`, `approved_by: null`, `approved_at: null` KHÔNG đổi, đúng package-lifecycle/artifact-lifecycle separation đã dùng nhất quán trong toàn bộ session này (cùng pattern Package 0.2-B4/Package 1.1).

**v0.2 — bounded candidate amendment (2026-08-06), KHÔNG Approved/Consolidated, pending Review A/Independent Review B/Product Owner decision riêng biệt — Product Owner authorized một localized amendment cho NAV-003 Gap B (theo `package-1.6-upstream-resolution-exploration.md` NAV-003 exploration result: `READY FOR BOUNDED AUTHORING`):** Package 1.3-A v0.1 `Consolidated Stable` baseline (bốn module: `market-reference-service`/`market-data-ingestion`/`structure-engine`/`raw-regime-engine`, §0/§2) GIỮ NGUYÊN byte-for-byte, KHÔNG re-open, KHÔNG re-review. Thêm **§13a MỚI** — MỘT classification statement bounded cho khái niệm "Backtest run identity" (`backtest-orchestrator`, đăng ký `phase.elaborated_by: "1.3-A"` tại `module-registry.yaml` v0.7 NHƯNG chưa từng được elaborate tại tài liệu này trước v0.2) — CHỈ trả lời câu hỏi "run identity LÀ loại khái niệm gì" (NAV-003 Gap B, xem `package-1.6-upstream-resolution-exploration.md` §2.2/§2.5 mục 2), KHÔNG trả lời "ai expose nó qua route/edge/API nào" (NAV-003 Gap A, VẪN unresolved, VẪN ADR Required). §13a LÀ candidate content, TÁCH BIỆT khỏi bốn-module `Consolidated Stable` baseline — Package 1.3-A's package lifecycle KHÔNG đổi bởi v0.2 (VẪN ghi nhận `Consolidated Stable` cho phạm vi v0.1 gốc; §13a pending review riêng của chính nó trước khi coi là Consolidated). KHÔNG dependency edge/owner/API path/schema/storage/transport nào được chọn; KHÔNG `owns_authoritative_state` nào resolve; KHÔNG DD-001 resolve; KHÔNG Product/UX semantics sửa; KHÔNG NAV-003 Gap A/VIEW-002 resolve; KHÔNG Package 1.6 lifecycle đổi; KHÔNG `module-registry.yaml` sửa tại transaction này.

## 0. Vai trò của tài liệu này

Package 1.3-A elaborate **kiến trúc kỹ thuật** cho bốn module ĐÃ được Package 1.1 (`Consolidated Stable`, [`module-registry.yaml`](../module-registry.yaml) v0.3 blob `ab09d031183014c1af259895dadf86aaf644cc04`, [`system-decomposition.md`](../system-decomposition.md) v0.3 blob `c72dfdf54d2ac86bc7ad83de742dda485da11328`) thiết lập identity/taxonomy/dependency: `market-reference-service`, `market-data-ingestion`, `structure-engine`, `raw-regime-engine`. Tài liệu này **KHÔNG redefine** module identity/taxonomy/dependency đã pin ở Package 1.1 — chỉ elaborate: responsibility boundary chi tiết hơn, data flow, event-time/correction handling, determinism/replay constraint, no-repaint requirement, failure/stale-data boundary, security/trust-boundary identification, và open gap — đúng phạm vi `phase-1-plan.md` §8 Package 1.3-A "Outputs: module boundary chi tiết, data flow, event contract giữa Data Layer/Structure Engine/Regime Engine (KHÔNG schema cụ thể)".

**KHÔNG thuộc phạm vi tài liệu này:** field-level event schema (đã khóa tại `candle.md`/`swing.md`/`structure.md`/`regime.md`, Package 0.2-A/B1/B2, `Consolidated Stable`); Engine algorithm/source code; database schema; deployment/runtime topology cụ thể; Feature Engine fan-in logic (Package 1.3-B); security/custody implementation (Package 1.2).

## 1. Governing authority

```text
Constitution (Chapter 0–14, Locked):              highest architectural authority
Approved/Locked ADR (ADR-003/ADR-009/ADR-014):    decision authority cho Structure/Regime
                                                    independence + ordering mechanism
Domain Contract (candle.md v0.4, swing.md,        domain semantic authority — Consolidated
  structure.md, regime.md — Package 0.2-A/B1/B2,   Stable, KHÔNG redefine tại đây
  Consolidated Stable):
module-registry.yaml v0.3 (Consolidated Stable):  module identity/taxonomy/dependency
                                                    authority — KHÔNG redefine tại đây
system-decomposition.md v0.3 (Consolidated        official Phase 1 module dependency graph
  Stable):                                         — KHÔNG redefine tại đây
phase-1-plan.md v0.4 (Approved):                  Phase 1 work-breakdown/package-boundary
                                                    authority
Package 1.3-A (tài liệu này):                     technical elaboration authority ONLY, cho
                                                    đúng bốn module trong scope
```

Package 1.3-A KHÔNG redefine domain entity/event semantics, module identity/taxonomy, hay existing ADR decision nào — mọi nội dung dưới đây chỉ **elaborate** kiến trúc kỹ thuật trong ranh giới đã pin.

## 2. Module scope (bốn module, pin nguyên trạng từ Package 1.1)

Bốn module dưới đây trích dẫn NGUYÊN VĂN `module-registry.yaml` v0.3 (identity/taxonomy/dependency KHÔNG đổi) — cột "Elaboration" là nội dung MỚI của tài liệu này:

| module_id | module_type | owns_authoritative_state | depends_on | forbidden_dependencies |
|---|---|---|---|---|
| `market-reference-service` | runtime_service | true | [] (root) | [] |
| `market-data-ingestion` | runtime_service | true | `market-reference-service` | [] |
| `structure-engine` | compute_engine | true | `market-data-ingestion` | [] |
| `raw-regime-engine` | compute_engine | true | `market-data-ingestion` | `structure-engine` |

### 2.1 Market Reference Service

**Trách nhiệm (Package 1.1, KHÔNG đổi):** sở hữu authoritative Instrument/Venue identity, precision/tick/lot metadata, trading calendar/session (`context-map.yaml` capability `market-reference`, context `instrument-venue-reference`).

**Elaboration:**

```text
Root module — không phụ thuộc module Phase 1 nào khác. Là dependency của Market Data
Ingestion (venue/instrument identity resolution TRƯỚC khi ingest Candle).
Authority: Instrument/Venue identity opaque, stable (Chapter 6 §6.1/§6.8) — domain logic
tiêu thụ downstream (Market Data Ingestion, Structure/Regime Engine qua scope field trong
Candle subject) KHÔNG được parse instrument_id/venue_id để suy diễn thông tin.
```

### 2.2 Market Data Ingestion

**Trách nhiệm (Package 1.1, KHÔNG đổi):** quan sát và ghi nhận Candle observed/closed/corrected từ venue theo bitemporal semantics (Chapter 5); chuẩn hóa venue-specific schema về canonical domain language.

**Elaboration:**

```text
Depends on Market Reference Service (resolve Instrument/Venue identity + calendar/session
TRƯỚC khi normalize venue-specific event thành candle-observed/candle-closed/candle-
corrected/candle-data-gap-observed canonical form — candle.md §14 venue neutrality).
Sở hữu authoritative Candle fact (owns_authoritative_state: true) — nguồn duy nhất cho
candle-observed/candle-closed/candle-corrected/candle-data-gap-observed trong toàn hệ
thống (I-12).
security_classification: trust_boundary_candidate (§8 dưới) — external venue connection
boundary, identification only, KHÔNG auth/isolation design (Package 1.2 scope).
```

## 3. Data flow (responsibility/dependency view — KHÔNG runtime topology)

```text
Market Reference Service (root)
   │
   ▼
Market Data Ingestion  ──emits──► candle-observed / candle-closed / candle-corrected /
   │                              candle-data-gap-observed
   ├──────────────┐
   ▼              ▼
Structure Engine   Raw Regime Engine        (ĐỘC LẬP HOÀN TOÀN với nhau — ADR-003, hiệu
   │                    │                    lực qua ADR-014 — xem §11)
   ▼                    ▼
market-structure       raw-regime-analysis
(BreakOfStructure      (RegimeClassified /
 Detected /             RegimeFactInvalidated)
 ChangeOfCharacter
 Detected /
 StructureFactInvalidated /
 StructureRecomputed)
   │                    │
   └────────┬───────────┘
            ▼
     Feature Engine (Package 1.3-B — fan-in CÓ CHỌN LỌC, KHÔNG thuộc phạm vi tài liệu này)
```

**Xác nhận tường minh (yêu cầu task):** đây là responsibility/dependency view — KHÔNG phải authorization triển khai một synchronous pipeline hay runtime topology cụ thể (process/container/host, đồng bộ/bất đồng bộ, message broker). Việc chọn cơ chế thực thi cụ thể thuộc Engineering/Phase 1 execution-topology decision (`phase-1-plan.md` §7: "ADR LIKELY REQUIRED" nếu thiết lập lần đầu) — KHÔNG quyết định tại Package 1.3-A.

## 4. Module boundary — Structure Engine

**Trách nhiệm (Package 1.1, KHÔNG đổi):** suy diễn Swing/BOS/CHoCH và structure semantics từ Candle — analytical output, không external side effect.

### 4.1 Internal responsibility split (elaboration — KHÔNG một module mới, vẫn MỘT `structure-engine` identity theo Package 1.1)

Structure Engine sở hữu **hai lớp trách nhiệm nội bộ**, cả hai đều thuộc DUY NHẤT module `structure-engine` (Package 1.1 KHÔNG tách chúng thành hai module):

```text
Lớp 1 — Swing detection (swing.md, Package 0.2-B1):
  SwingCandidateDetected (provisional) / SwingConfirmed (authoritative) / SwingInvalidated.
  Pivot detection theo swing_definition_version (left/right evidence count, price_basis,
  equal_level_policy — policy KHÔNG hardcode một trường phái, xem §7).

Lớp 2 — BOS/CHoCH detection (structure.md, Package 0.2-B1):
  BreakOfStructureDetected / ChangeOfCharacterDetected / StructureFactInvalidated /
  StructureRecomputed. Tiêu thụ Eligible Swing (SwingConfirmed, theo total order §7 dưới)
  + trực tiếp candle-closed/candle-corrected (breaking candle confirmation — structure.md
  §12: Swing Domain Contract KHÔNG theo dõi Candle sau SwingConfirmed, nên Structure Engine
  PHẢI tự tiêu thụ Candle trực tiếp, không chỉ qua Swing fact).
```

**Lý do hai lớp cùng một module (KHÔNG phải quyết định mới — kế thừa từ `structure-engine.responsibilities` đã pin tại Package 1.1):** Swing và BOS/CHoCH cùng thuộc capability `market-structure`/context `market-structure-analysis` (`context-map.yaml`, Chapter 4 §4.2), cùng chia sẻ Candle input authority, và BOS/CHoCH correction cascade (§10 dưới) PHẢI xử lý cả `SwingInvalidated` lẫn `CandleCorrected` trực tiếp trong cùng transaction boundary. Package 1.3-A KHÔNG tách lại — chỉ elaborate ranh giới hai lớp trách nhiệm bên trong.

### 4.2 Authoritative ownership

```text
Structure Engine sở hữu authoritative:
  Swing fact (candidate/confirmed/invalidated), Structure fact (BOS/CHoCH/invalidated/
  recomputed), structure orientation state machine.

Structure Engine KHÔNG sở hữu:
  Candle fact (thuộc Market Data Ingestion); Regime fact (ADR-003 — độc lập hoàn toàn,
  KHÔNG events_consumed nào từ raw-regime-analysis); Feature fan-in logic (Package 1.3-B);
  swing_definition_version/structure_definition_version policy VALUE cụ thể (configuration
  instance, Phase 1, KHÔNG phải kiến trúc — chỉ schema tối thiểu đã khóa ở Domain Contract).
```

### 4.3 Inputs/outputs theo contract category

```text
Consumes (event):  candle-closed, candle-corrected   (trực tiếp, structure.md §12 — KHÔNG
                    candle-observed provisional, KHÔNG candle-current-view non-authoritative)
Emits (event):      break-of-structure-detected, change-of-character-detected,
                    structure-fact-invalidated, structure-recomputed,
                    swing-candidate-detected, swing-confirmed, swing-invalidated
Consumes (query):   — (không có; mọi input là event, đúng module-registry.yaml
                    `consumes: [event]`)
```

## 5. Module boundary — Raw Regime Engine

**Trách nhiệm (Package 1.1, KHÔNG đổi):** suy diễn Regime (trending/ranging/volatile) trực tiếp từ raw market data, ĐỘC LẬP HOÀN TOÀN với Structure Engine (ADR-003, hiệu lực qua ADR-014).

### 5.1 Authoritative ownership

```text
Raw Regime Engine sở hữu authoritative:
  RegimeClassified/RegimeFactInvalidated fact — Volatility + Directional Persistence
  dimension (regime.md §"Ngoài phạm vi" — Activity/Volume, Liquidity, Data-quality, và
  Structure-aware Regime KHÔNG thuộc phạm vi contract hiện có, xem §13 dưới).

Raw Regime Engine KHÔNG sở hữu:
  Candle fact; Structure/Swing fact; Feature fan-in logic; regime_definition_version
  policy VALUE cụ thể (configuration instance, Phase 1).
```

### 5.2 Inputs/outputs theo contract category

```text
Consumes (event):  candle-closed, candle-corrected   (chính xác hai, regime.md §13 — KHÔNG
                    candle-observed, KHÔNG candle-current-view, KHÔNG Swing/Structure)
Emits (event):      regime-classified, regime-fact-invalidated
```

### 5.3 MỘT fact cho MỖI completed valid window (elaboration)

Khác Structure (event-driven theo break condition), Raw Regime Engine phát sinh **một `RegimeClassified` cho MỖI completed analysis window** — kể cả khi class không đổi so với window liền trước (regime.md §9). Đây là một ràng buộc kiến trúc quan trọng cho throughput/storage estimate tại Package 1.4/1.5 (KHÔNG resolve tại đây — chỉ ghi nhận).

## 6. Feature Engine boundary (downstream — KHÔNG thuộc phạm vi Package 1.3-A)

```text
Structure Engine VÀ Raw Regime Engine đều CHỈ publish output (event) — KHÔNG định nghĩa,
KHÔNG giả định consumer logic. Feature Engine (module-registry.yaml, Package 1.3-B, CHƯA
elaborate) là điểm fan-in CÓ CHỌN LỌC DUY NHẤT từ cả hai luồng (ADR-003: "Feature Engine:
fan-in CÓ CHỌN LỌC từ cả hai — không phải feature nào cũng cần cả Structure lẫn Regime;
đây là nơi xử lý đồng bộ hóa (join) giữa 2 luồng event nếu cần").
```

**Xác nhận tường minh (yêu cầu task):** tài liệu này KHÔNG author bất kỳ Feature Engine consumption logic nào — `feature-engine.depends_on: [structure-engine, raw-regime-engine]` đã pin tại Package 1.1 `module-registry.yaml` là RANH GIỚI duy nhất cần bảo toàn ở đây; nội dung fan-in cụ thể thuộc Package 1.3-B.

## 7. Determinism và replay constraints (I-2)

```text
Definition Version pinning (Referenced Authoritative Artifact, Chapter 8 §8.1.1):
  swing_definition_version    — left_count/right_count/price_basis/equal_level_policy
  structure_definition_version — break_price_basis/comparison_policy/equal_level_policy/
                                  relevant_swing_selection_policy (§6a structure.md)
  regime_definition_version   — window_candle_count/metric_formula_id/class_thresholds/
                                  threshold_comparison_policy/gap_policy/
                                  decimal_precision_policy

Mode parity (I-2):  cùng definition_version + cùng Candle causal ancestry → cùng tập
                     Swing/Structure/Regime fact, mọi execution mode (Live/Backtest/Paper/
                     Replay) — bắt buộc, đúng swing.md §12/structure.md §11/regime.md §12.

Deterministic total order (khi cần chọn giữa nhiều ứng viên — tie-breaking):
  Structure: 8-tiêu-chí Eligible Swing total order (structure.md §6a).
  Regime:    7-tiêu-chí total order (regime.md §11) — window_end DESC, window_start DESC,
             recorded_time ASC, stream_id ASC, registry_version ASC, sequence ASC (chỉ khi
             stream_id+registry_version hòa), event_id ASC.
  Cả hai:    lexicographic — tiêu chí đầu tiên khác nhau quyết định, KHÔNG đánh giá tiêu
             chí sau; cấm so sánh `sequence` thô xuyên stream khác nhau như global order
             (Chapter 8 §8.3.3, ADR-009).

Ordering mechanism (ADR-009):  per-stream contiguous sequence + explicit causation, KHÔNG
  global total order — Structure/Regime Engine PHẢI tôn trọng causal precedence (Chapter 8
  §8.3.4): không xử lý một `CandleCorrected`/`SwingInvalidated` trước khi fact nó sửa đã
  được apply. Protocol/implementation chi tiết của ADR-009 (giao thức cụ thể cho
  per-stream sequence) là Phase 1 elaboration KHÔNG khóa tại tài liệu này (§13 dưới).
```

## 8. No-repaint requirements (I-3)

```text
Structure Engine:
  BreakOfStructureDetected/ChangeOfCharacterDetected KHÔNG BAO GIỜ bị ghi đè tại chỗ — chỉ
  phủ định qua StructureFactInvalidated với nguyên nhân tường minh, KHÔNG BAO GIỜ vì "giá
  tiếp tục di chuyển" (đó luôn là BOS/CHoCH MỚI). Replay tại cursor T chỉ thấy fact có
  recorded_time ≤ T — không backfill lịch sử (structure.md §8).

Raw Regime Engine:
  RegimeClassified KHÔNG BAO GIỜ bị ghi đè tại chỗ — chỉ phủ định qua RegimeFactInvalidated
  + replacement, luôn append-only. Cursor-correct pending correction: replay giữa
  invalidation và replacement thấy đúng PENDING_CORRECTION, không âm thầm dùng giá trị cũ
  (regime.md §12).

Swing (internal to Structure Engine):
  SwingConfirmed KHÔNG BAO GIỜ bị ghi đè tại chỗ — chỉ phủ định qua SwingInvalidated với
  invalidation_cause: upstream_correction — KHÔNG BAO GIỜ qua market_evolution (giá tiếp
  tục di chuyển sau confirm KHÔNG làm Swing sai — đó là input hợp lệ cho BOS/CHoCH, không
  phải lý do invalidate Swing chính nó, swing.md §8).

Chung cho cả ba:  append-only (I-3) — không event nào bị xóa/mutate; correction luôn là
  fact MỚI trỏ ngược fact bị sửa qua causation_refs.
```

## 9. Correction handling (event-time vs recorded-time)

Bitemporal discipline (Chapter 5): `effective_time`/`pivot_effective_time`/`analysis_window` (KHI fact có hiệu lực trong domain) tách biệt hoàn toàn khỏi `recorded_time` (KHI Ride biết fact đó) — mọi correction chỉ đổi trục thứ hai, KHÔNG BAO GIỜ đổi trục thứ nhất của chính fact gốc.

### 9.1 Correction propagation — Structure (dependency-forward cascade)

```text
CandleCorrected
  → (a) Candle là pivot/evidence của Swing → SwingInvalidated → StructureFactInvalidated
        (invalidation_cause: swing_invalidated) cho BOS/CHoCH có broken_swing_ref trỏ Swing đó
  → (b) Candle là breaking_candle_refs của BOS/CHoCH KHÔNG qua Swing nào bị invalidate →
        StructureFactInvalidated (invalidation_cause: breaking_candle_corrected) trực tiếp

Cascade tiếp tục DEPENDENCY-FORWARD (KHÔNG "most-recent-first") theo chuỗi orientation gốc
(E(k+1) phụ thuộc E(k) khi E(k+1).prior_orientation = E(k).new_orientation) — mỗi fact phụ
thuộc nhận StructureFactInvalidated theo đúng thứ tự traverse, kết thúc bằng ĐÚNG MỘT
StructureRecomputed refold toàn bộ Swing/Candle fact còn hiệu lực (structure.md §10).
```

### 9.2 Correction propagation — Regime (independent per-window, KHÔNG cascade)

```text
CandleCorrected ảnh hưởng candle_evidence_refs của một RegimeClassified window
  → RegimeFactInvalidated + replacement RegimeClassified — BẮT BUỘC kể cả khi class kết
    quả không đổi (evidence phải luôn trung thực, I-1 Explainability).

MỘT CandleCorrected có thể ảnh hưởng NHIỀU window overlapping đồng thời (rolling window) —
mỗi window được invalidate + replace ĐỘC LẬP, KHÔNG dependency-forward ordering giữa các
window (khác Structure — regime.md §10: "một đơn giản hóa thực sự so với Structure, không
phải một thiếu sót", vì các RegimeClassified của window khác nhau không phụ thuộc kết luận
của nhau).
```

**Kiến trúc consequence (elaboration, KHÔNG redefine domain semantics):** Structure Engine cần transaction/processing boundary xử lý được MỘT cascade nhiều-fact có thứ tự phụ thuộc; Raw Regime Engine chỉ cần xử lý MỘT correction độc lập cho MỖI window bị ảnh hưởng, không cần dependency ordering giữa chúng — đây là khác biệt kiến trúc thật giữa hai module, không phải một thiếu sót cần "sửa cho giống nhau".

## 10. Failure và stale-data boundaries

```text
Candle ingestion fail-closed (Market Data Ingestion, candle.md §11, 5-bước precedence):
  1. Xác lập idempotency identity (native source_identity hoặc fallback đã khai báo).
  2. KHÔNG resolve được identity → fail closed/quarantine — KHÔNG append CandleClosed,
     KHÔNG dedupe, KHÔNG phát CandleCorrected. Thiếu provenance KHÔNG phải bằng chứng cho
     correction.
  3. Cùng identity, payload giống hệt → duplicate, zero effect. Payload khác → provenance
     integrity violation → fail closed/quarantine (KHÔNG âm thầm coi là correction).
  4. Identity khác, cùng subject, payload authoritative đổi → CandleCorrected (yêu cầu
     provenance riêng cho correction).
  5. Identity khác, cùng payload → duplicate (nếu equivalence semantics khai báo) hoặc
     quarantine/fail-closed chờ reconciliation (không có nhánh thứ ba).

Missing/gap data (candle.md §12):
  Session hợp lệ đóng          → ngoài phạm vi candle.md, do Venue/session authority quyết
                                  (instrument-venue-reference, CHƯA author — §13 gap dưới).
  Session mở, không trade      → CandleClosed complete_zero_volume CHỈ khi đủ NĂM điều kiện
                                  provenance (candle.md §12) — KHÔNG suy diễn từ im lặng.
  Thiếu/trễ/không khả dụng     → CẤM tự tổng hợp OHLC giả; CandleDataGapObserved là tín
                                  hiệu tường minh best-effort, vắng mặt KHÔNG chứng minh đủ
                                  dữ liệu.

Downstream stale-data propagation (Structure/Raw Regime):
  Left/right-side evidence chưa đủ  → valid absence (KHÔNG missing-data condition) — Swing
                                       giữ CANDIDATE, không auto-invalidate vì "chưa đủ thời
                                       gian" (swing.md §11).
  Data gap trong evidence window    → KHÔNG confirm speculative qua gap, KHÔNG tự invalidate
                                       chỉ vì gap — chờ CandleClosed authoritative resolve gap.
  Regime window thiếu evidence      → tuân regime_definition_version.gap_policy — deterministic,
                                       đồng nhất mọi execution mode (regime.md §12).
```

## 11. Independence preservation (ADR-003/ADR-014 — bảo toàn tường minh)

```text
Raw Regime Engine ĐỘC LẬP HOÀN TOÀN với Structure Engine — forbidden_dependencies:
  [structure-engine] tại module-registry.yaml (Package 1.1, KHÔNG đổi bởi tài liệu này).

Structure Engine input CHỈ từ Candle (candle-closed/candle-corrected) + Swing fact tự sinh
  nội bộ — KHÔNG events_consumed nào từ raw-regime-analysis (structure.md §12: "Không tiêu
  thụ Regime — ADR-003 khóa Structure độc lập hoàn toàn với Raw Regime").

Raw Regime Engine input CHỈ từ Candle — KHÔNG tiêu thụ Swing/Structure (regime.md §13:
  "Swing/Structure (ADR-003 — độc lập hoàn toàn)").

Feature Engine LÀ điểm fan-in CÓ CHỌN LỌC DUY NHẤT — nơi hai luồng CÓ THỂ được đồng bộ hóa
  (join) nếu cần, KHÔNG PHẢI tại Structure/Raw Regime Engine (ADR-003 Alternatives
  considered: "Regime hybrid nhưng do chính Regime Engine fan-in từ Structure — loại bỏ vì
  vẫn giữ coupling một chiều không cần thiết").
```

**Xác nhận (yêu cầu task):** hai module KHÔNG chia sẻ state, KHÔNG gọi lẫn nhau, KHÔNG có dependency edge nào giữa `structure-engine` và `raw-regime-engine` theo bất kỳ hướng nào — pin nguyên trạng, không đổi bởi Package 1.3-A.

## 12. Security / trust-boundary identification (Package 1.2 elaborates further)

```text
Market Data Ingestion:  security_classification: trust_boundary_candidate (Package 1.1,
  KHÔNG đổi) — external venue connection boundary (WS/REST tới exchange/data vendor).
  IDENTIFICATION ONLY tại tài liệu này — KHÔNG auth mechanism, KHÔNG credential/key
  handling, KHÔNG network ACL design (Package 1.2 scope, Chapter 2 I-11).

Market Reference Service, Structure Engine, Raw Regime Engine:  security_classification:
  none (Package 1.1, KHÔNG đổi) — không chạm external network boundary trực tiếp, không sở
  hữu credential/secret material.

Trigger D (quality-gate, boundary-triggered):  CÓ ĐIỀU KIỆN cho market-data-ingestion —
  identified nhưng KHÔNG design; evaluate thực sự khi Package 1.2 định nghĩa concrete
  boundary (đúng phase-1-plan.md §9).
```

## 13. Open Domain và architecture gaps (KHÔNG resolve, chỉ carry forward)

```text
Structure-aware Regime (KHÔNG được invent tại tài liệu này, đúng yêu cầu task):
  regime.md §15 tự khóa: "Structure-aware Regime là một concept TƯƠNG LAI khác, KHÔNG phải
  phần mở rộng của regime.md." Domain Context/Capability cho responsibility này KHÔNG đăng
  ký tại context-map.yaml (Chapter 4 §4.2) — Package 1.1's raw-regime-engine note đã ghi
  nhận: "Package 1.1 CANNOT bind a module to this responsibility without first registering
  the missing Domain Context/Capability." Package 1.3-A KHÔNG tạo module/capability/context
  mới cho gap này — vẫn BLOCKED trên Domain Context/Capability registration (Product Owner
  + Domain Contract authoring decision, ngoài phạm vi Package 1.1/1.3-A).

Swing/Structure/Regime Definition Version registry mechanism:
  swing_definition_version/structure_definition_version/regime_definition_version đều là
  "opaque, immutable pin — Referenced Authoritative Artifact" (Chapter 8 §8.1.1) nhưng cơ
  chế lưu trữ/versioning CỤ THỂ của registry này (nơi các version này được author/publish/
  resolve) là Phase 1 concern CHƯA elaborate — candle.md/swing.md/structure.md/regime.md
  đều tự defer nó ("Phase 1, chưa author"). Package 1.3-A ghi nhận gap này KHÔNG resolve —
  cần một registry mechanism riêng (có thể là artifact mới hoặc mở rộng module-registry
  pattern) tại Package 1.3-A/B/C hoặc package kế tiếp.

ADR-009 ordering protocol implementation:
  ADR-009 tự khóa "Protocol/implementation chi tiết được deferred sang Phase 1" — Package
  1.3-A chỉ áp dụng nguyên tắc (per-stream contiguous sequence + explicit causation, KHÔNG
  global total order) mà KHÔNG author protocol cụ thể (đó là implementation, ngoài phạm vi
  kiến trúc architecture-level).

stream-registry.yaml / module-registry.yaml producer_ref resolution:
  candle.md §2 tự ghi nhận stream_ref/producer_ref resolve từ stream-registry.yaml (Chapter
  8 §8.3.1, Phase 1, CHƯA author) — Package 1.3-A KHÔNG author stream-registry.yaml (field-
  level/schema concern, ngoài phạm vi architecture-level của tài liệu này).

Venue/session authority (instrument-venue-reference domain context):
  candle.md §12 "Venue/session hợp lệ đóng" case defer về context instrument-venue-
  reference — Domain Contract cho context này CHƯA author (Package 0.2-C, ngoài phạm vi
  Package 1.3-A) dù capability/context đã đăng ký tại context-map.yaml.
```

## 13a. Backtest run-identity classification — NAV-003 Gap B (bounded candidate, KHÔNG Consolidated, v0.2)

**Phạm vi:** mục này CHỈ trả lời câu hỏi "run identity" (`backtest-orchestrator`, UC-006 "Evidence produced: Decision/RiskEvaluation sequence gắn run identity", `use-case-workflow.md:327-328`) LÀ loại khái niệm gì — KHÔNG trả lời ai expose nó, qua edge/module/API path nào (câu hỏi đó VẪN unresolved, xem §13a.4 dưới). `backtest-orchestrator` được đăng ký `phase.elaborated_by: "1.3-A"` (`module-registry.yaml` v0.7) nhưng CHƯA từng được elaborate tại §0/§2/§4/§5 của tài liệu này — mục này KHÔNG mở rộng bốn-module `Consolidated Stable` scope đó, CHỈ thêm một classification statement bounded cho đúng MỘT khái niệm.

```text
13a.1 Classification (candidate, pending review):

  Backtest run identity LÀ một correlation/grouping concept — dùng để truy vấn hoặc
    liên kết (query/relate) các Decision fact VÀ RiskEvaluation fact ĐÃ tồn tại, gắn
    chúng vào một bounded run context (Strategy Instance/Definition Version/policy
    version/thời gian, UC-006). Run identity KHÔNG PHẢI một Domain entity/event mới,
    KHÔNG PHẢI một authoritative fact riêng của backtest-orchestrator.

13a.2 Authority — KHÔNG đổi:

  Decision content VẪN authoritative dưới đúng Decision authority hiện có
    (decision-authority-service/decision.md, Package 0.2-C4, Consolidated Stable) —
    KHÔNG đổi bởi run identity.
  RiskEvaluation content VẪN authoritative dưới đúng Risk authority hiện có
    (risk-gateway/risk.md, Consolidated Stable) — KHÔNG đổi bởi run identity.
  Gán run identity cho một Decision/RiskEvaluation sequence KHÔNG làm
    backtest-orchestrator authoritative cho MỘT trong hai fact type đó —
    backtest-orchestrator.owns_authoritative_state VẪN `deferred` (DD-001, module-
    registry.yaml v0.7) — KHÔNG resolve tại mục này.

13a.3 KHÔNG mới — bounded xác nhận:

  KHÔNG Domain entity mới (không "BacktestRunContext" hay tương đương được author).
  KHÔNG Domain event mới.
  KHÔNG field mới thêm vào Decision/RiskEvaluation schema (decision.md/risk.md
    KHÔNG sửa, byte-identical, KHÔNG re-open).
  KHÔNG dependency edge nào thêm/đổi (module-registry.yaml KHÔNG sửa tại transaction
    này).
  KHÔNG owner assign cho việc expose run-identity query (module/service nào thực thi
    correlation query — KHÔNG quyết định).
  KHÔNG API path/schema/storage model/transport nào chọn.
  KHÔNG `owns_authoritative_state` nào resolve; KHÔNG DD-001 resolve.

13a.4 KHÔNG resolve (NAV-003 Gap A — VẪN unresolved, VẪN carry forward):

  Route API/dependency edge cho SCR-003/SCR-004/SCR-005 (`ux-architecture.md` §13 gap
    #2, `TECHNICALLY BLOCKED`) — VẪN unresolved. Câu hỏi "ai/qua đâu expose run-
    identity correlation" (Candidate A/B, `package-1.6-upstream-resolution-
    exploration.md` §2.4) VẪN mở, VẪN đòi hỏi một ADR riêng (§13a.5 dưới) trước khi
    quyết định.
  VIEW-002 (Research verification ownership) — KHÔNG liên quan, KHÔNG chạm bởi mục
    này, VẪN unresolved độc lập.
  Package 1.6 (`ux-architecture.md`) lifecycle — VẪN `candidate`, VẪN blocked cho
    Independent Review B/consolidation.

13a.5 Governance §4b assessment (bắt buộc, bounded):

  Constitution Chapter 0 §4b ADR Scope Rule table: "ADR Required" áp dụng cho "Thêm/
    sửa Platform Invariant · thay đổi Event Schema · Module Taxonomy/dependency graph
    · Governance/Approval process · quyết định ảnh hưởng >1 module hoặc khó đảo ngược
    · sửa/supersede ADR đã Locked."
  Đánh giá cho CHÍNH classification statement này (§13a.1-13a.3, KHÔNG bao gồm §13a.4's
    unresolved Gap A): KHÔNG thêm/sửa Platform Invariant; KHÔNG thay đổi Event Schema
    (tường minh KHÔNG entity/event mới, §13a.3); KHÔNG thay đổi Module Taxonomy/
    dependency graph (`module-registry.yaml` KHÔNG sửa); KHÔNG thay đổi Governance/
    Approval process; KHÔNG sửa/supersede ADR đã Locked. "Ảnh hưởng >1 module" — mục
    này MÔ TẢ quan hệ giữa ba module ĐÃ đăng ký (backtest-orchestrator/decision-
    authority-service/risk-gateway) NHƯNG KHÔNG thay đổi registered contract/
    responsibility/dependency của module nào trong ba module đó — CHỈ xác nhận
    (confirm) một cách đọc semantic ĐÃ ngụ ý bởi UC-006 (`use-case-workflow.md:327-
    328`) mà chưa từng được viết tường minh ở tầng architecture. "Khó đảo ngược" —
    KHÔNG, mục này KHÔNG cấp quyền/route/ownership nào — reversible bằng một correction
    transaction khác nếu classification này sai.
  Kết luận (bounded, KHÔNG tự động exempt): classification statement này KHÔNG khớp
    bất kỳ tiêu chí "ADR Required" nào tại §4b table — rơi vào "ADR Not Required" hoặc
    "ADR Optional" (§4b: "Thay đổi nội bộ một module không đổi contract nhưng ảnh
    hưởng đáng kể"). Đây LÀ một đánh giá bounded của transaction này, KHÔNG PHẢI một
    self-declared exemption chính thức — Gap A's edge/owner/API-path decision (§13a.4)
    VẪN LÀ MỘT quyết định riêng, KHÔNG liên quan tới kết luận này, VÀ VẪN `ADR
    Required` không mơ hồ (khớp CHÍNH XÁC "Module Taxonomy/dependency graph" table
    entry, đúng kết luận đã ghi tại `package-1.6-upstream-resolution-exploration.md`
    §6) — KHÔNG bị thay đổi/giảm nhẹ bởi §13a này.

Explicit non-goals (§13a):

  KHÔNG dependency edge nào thêm.
  KHÔNG owner nào assign cho query exposure/computation.
  KHÔNG API path/schema/storage model/transport nào chọn.
  KHÔNG `backtest-orchestrator.owns_authoritative_state` resolve.
  KHÔNG DD-001 resolve.
  KHÔNG Product/workflow/UX semantics sửa (`product-requirement.md`/`use-case-
    workflow.md`/`ux-blueprint.md` KHÔNG sửa).
  KHÔNG NAV-003 Gap A resolve.
  KHÔNG VIEW-002 resolve.
  KHÔNG Package 1.6 lifecycle đổi.
  KHÔNG consolidate §13a hay Package 1.3-A tại transaction này — §13a LÀ candidate,
    pending Review A/Independent Review B/Product Owner decision riêng biệt trước khi
    được coi là Consolidated.
  KHÔNG `module-registry.yaml` sửa tại transaction này.
```

## 14. Explicit non-goals

```text
KHÔNG author field-level event schema (đã khóa tại candle.md/swing.md/structure.md/
  regime.md, Package 0.2-A/B1/B2, Consolidated Stable) — chỉ contract CATEGORY
  (event/query/command).
KHÔNG author Engine algorithm/computation logic cụ thể (break confirmation formula,
  regime classification formula — thuộc Domain Contract policy schema, đã khóa).
KHÔNG author database schema/DDL.
KHÔNG chọn deployment infrastructure/cloud provider/message broker/runtime topology.
KHÔNG chọn programming language/framework.
KHÔNG author stream-registry.yaml hay bất kỳ Definition Version registry mechanism cụ thể
  nào (§13 — ghi nhận gap, không resolve).
KHÔNG design authentication/authorization/custody implementation (Package 1.2).
KHÔNG redefine module identity/taxonomy/dependency đã pin tại Package 1.1
  (module-registry.yaml/system-decomposition.md v0.3, Consolidated Stable).
KHÔNG author Feature Engine fan-in logic (Package 1.3-B).
KHÔNG resolve Structure-aware Regime Domain Context/Capability gap.
KHÔNG tạo/approve ADR nào.
KHÔNG approve/consolidate Package 1.3-A (tài liệu này).
KHÔNG mark Package 1.3-A Consolidated Stable.
KHÔNG pass Gate 2.
KHÔNG tuyên bố Phase 1 hoàn thành.
KHÔNG mở Phase 2.
KHÔNG authorize Live.
```

## 15. Review and consolidation conditions

```text
Review A scope:              Structure/Regime độc lập được bảo toàn tường minh (§11 —
                              KHÔNG dependency edge nào giữa structure-engine/raw-regime-
                              engine theo bất kỳ hướng nào); không redefine domain semantics
                              của candle.md/swing.md/structure.md/regime.md; module boundary
                              elaboration (§4/§5) nhất quán với module-registry.yaml v0.3
                              (Consolidated Stable) — không silent semantic invention;
                              Structure-aware Regime gap KHÔNG bị lấp bằng semantics tự
                              phát minh (§13); no-repaint/determinism/replay treatment (§7/
                              §8) đúng Domain Contract invariant, không suy diễn thêm.
Independent Review B
  scope:                     Độc lập xác nhận Feature Engine consumption boundary (§6) CHƯA
                              bị vi phạm sớm ở tầng này — Structure/Raw Regime Engine chỉ
                              publish, KHÔNG định nghĩa consumer logic; xác nhận correction
                              propagation (§9.1/§9.2) khớp CHÍNH XÁC structure.md §10/
                              regime.md §10 KHÔNG lệch; xác nhận mọi open gap (§13) được ghi
                              nhận trung thực, KHÔNG bị silently resolved.
Product Owner decision
  point:                     SAU khi Review A + Review B CLEAN. **Cập nhật (2026-08-04,
                              Product Owner consolidation decision):** Review A CLEAN +
                              Independent Review B CLEAN hoàn tất (Blocker 0/Major 0/Minor
                              0). Product Owner đã quyết định: "I approve consolidation of
                              Package 1.3-A v0.1 as the current Consolidated Stable
                              architecture baseline." — Package 1.3-A nay **`Consolidated
                              Stable`**.
Consolidation condition:     Zero unresolved Blocker/Major (**THỎA**); ADR execution-
                              topology (không phát sinh — §3) N/A; không domain semantic mới
                              bị invent (**THỎA**); module identity/taxonomy/dependency khớp
                              module-registry.yaml v0.3 (Consolidated Stable) không lệch
                              (**THỎA**). **Mọi điều kiện consolidation ĐÃ thỏa — Package
                              1.3-A v0.1 nay `Consolidated Stable`.**
```
