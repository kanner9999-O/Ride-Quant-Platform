---
id: phase-1-plan
title: "Phase 1 — System Architecture: Planning Baseline"
version: "0.1"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-03"
last_review: null
next_review: null
depends_on: ["00-governance", "02-platform-invariants", "03-engineering-principles", "04-domain-principles", "07-module-taxonomy", "08-event-model", "09-plugin-model", "10-compatibility-capability-contract", "11-adr-process", "12-approval-gates", "13-quality-gates", "14-roadmap"]
---

# Phase 1 — System Architecture: Planning Baseline

## 0. Vai trò của tài liệu này

Đây là **planning artifact đầu tiên của Phase 1** ([Chapter 14 §14.2](../constitution/14-roadmap.md), Locked — "Phase 1 — System Architecture") — sở hữu **work breakdown, dependency order, authority map, review/gate structure** cho toàn bộ Phase 1. Tài liệu này **KHÔNG** author Software Architecture/UX Architecture/API/Database/Engine/Security & Custody Baseline thực tế — mọi nội dung kiến trúc cụ thể (module interface, API schema, database schema, deployment infrastructure, cloud provider, programming framework, custody implementation, authentication implementation, Engine algorithm, source code) **deferred** tới đúng package tương ứng được định nghĩa tại §8.

**KHÔNG phải Phase 1 DoD.** §10 chỉ là **planning input** cho một Phase 1 DoD artifact riêng sau này (theo đúng pattern `phase-0-dod.md` đã dùng cho Phase 0) — tài liệu này KHÔNG tự claim là DoD, KHÔNG khóa completion criteria chính thức.

**KHÔNG tạo ADR nào.** §7 chỉ **phân loại khả năng** (ADR LIKELY REQUIRED / CONDITIONALLY REQUIRED / NO NEW ADR EXPECTED) cho các decision class dự kiến — **không quyết định** bất kỳ decision nào trong số đó. ADR determination thực tế xảy ra khi decision cụ thể được đề xuất, đúng [Chapter 0 §4b](../constitution/00-governance.md) (ADR Scope Rule).

**KHÔNG approve bất kỳ Phase 1 package nào**, **KHÔNG tuyên bố Phase 1 hoàn thành**, **KHÔNG authorize Live**. Phase 1 hiện `Active`, `not Complete` (xem [MANIFEST](../MANIFEST.md)).

## 1. Canonical project state (kế thừa, không đổi)

```text
Phase 0 Approval Gate:              Approved
Phase 0 — Vision & Foundation:      Complete
Phase 1 — System Architecture:      Active (Authorized to Begin, planning baseline nay authored)
Live:                                Unauthorized
OQ-001:                              Partially Resolved (không đổi)
OQ-002:                              Open (không đổi)
OQ-003:                              Open (không đổi)
```

"Authorized to Begin" ([MANIFEST](../MANIFEST.md), Phase 0 Approval Gate — Decision) nghĩa là planning/authoring dưới governance hiện có ĐƯỢC PHÉP bắt đầu — **KHÔNG** pre-approve bất kỳ Phase 1 deliverable/architecture decision nào. Tài liệu này là hành động ĐẦU TIÊN thực thi quyền đó.

## 2. Authority boundary (bắt buộc bảo toàn)

```text
Constitution (Chapter 0–14, Locked):        highest architectural authority
Approved/Locked ADR:                        decision authority
Domain Contract (/docs/domain/):            domain semantic authority
product-requirement.md (Package 0.3-A):     product requirement authority
use-case-workflow.md (Package 0.3-B):       behavior/workflow authority
ux-blueprint.md (Package 0.3-C):            user-facing acceptance-surface authority
Phase 1 architecture artifact (kể cả
  tài liệu này):                            technical realization authority ONLY
```

Phase 1 architecture **KHÔNG** được silently redefine Product hay Domain semantics. Bất kỳ package Phase 1 nào phát hiện Product/Domain semantics chưa đủ để thiết kế kiến trúc (ví dụ `DD-001`/`DD-003`, xem §11) phải **dừng lại và escalate** — KHÔNG tự phát minh semantics ở tầng kiến trúc để lấp khoảng trống.

## 3. Phase 1 scope (nguyên văn Chapter 14 §14.2)

```text
Phase 1 — System Architecture
  Software · UX Architecture · Security & Custody Baseline · API · Database · Engine
  → ADR cho quyết định kiến trúc thuộc diện ADR Required (Governance §4b)
  → Approval Gate
```

Sáu workstream trên là **exhaustive cho Phase 1 theo Roadmap** — tài liệu này KHÔNG thêm workstream ngoài danh sách đó, KHÔNG bỏ sót workstream nào.

## 4. Workstream → Package decomposition

| # | Workstream (Roadmap §14.2) | Quyết định phân rã | Lý do |
|---|---|---|---|
| 1 | Software Architecture | **Một package nền tảng** — Package 1.1 | Module boundary/dependency graph phải resolve TRƯỚC mọi package khác ([Chapter 7 §7.5](../constitution/07-module-taxonomy.md): `module-registry.yaml` là Phase 1 artifact, mọi tier-resolution/ownership-binding khác phụ thuộc nó, [Chapter 13 §13.4](../constitution/13-quality-gates.md)) |
| 2 | Security & Custody Baseline | **Cross-cutting gate/evidence set** — Package 1.2 | I-4 (Strategy Isolation)/I-7 (Plugin Non-Bypass)/I-11 (Secrets & Custody) áp dụng NGANG qua mọi workstream khác, không phải một pipeline stage tuần tự — mỗi package khác phải thỏa baseline này trước khi tự nó `Consolidated Stable` |
| 3 | Engine Architecture | **Bốn subpackage bounded**, đúng ranh giới dependency-wave đã pin (§5) — Package 1.3-A/B/C/D | Engine pipeline có 8 giai đoạn/entity domain riêng biệt đã author ở Package 0.2-B1–B4/C1–C7 (Structure/Regime/Feature/Context/Strategy/Decision/Risk/Execution) — một package đơn sẽ vi phạm bounded-package convention đã dùng nhất quán cho Phase 0.2 |
| 4 | API Architecture | **Một package** — Package 1.4 | Command/query/event contract topology là một concern thống nhất (Chapter 10), dù tiêu thụ output của cả 4 subpackage Engine |
| 5 | Database Architecture | **Một package** — Package 1.5 | Storage/persistence/source-of-truth boundary là một concern thống nhất (Chapter 8 §8.1, I-12), dù áp cho mọi Engine |
| 6 | UX Architecture | **Một package** — Package 1.6 | Package 0.3-C UX Blueprint đã `Consolidated Stable`, phạm vi đã bounded (17 screen/view); technical realization của nó là một concern thống nhất |

KHÔNG package nào ngoài chín package trên (1.1, 1.2, 1.3-A, 1.3-B, 1.3-C, 1.3-D, 1.4, 1.5, 1.6) được author dưới Phase 1 tại baseline này — thêm package mới đòi hỏi cập nhật tài liệu này trước (version bump), không tự phát sinh ở downstream.

## 5. Dependency graph

### 5.1 Engine pipeline (bảo toàn nguyên vẹn từ `docs/architecture/README.md` — bản nháp Chapter 7, CHƯA chính thức)

```text
Data Layer
   ├──────────────┐
   ▼              ▼
Structure Engine   Raw Regime Engine        (độc lập — KHÔNG phụ thuộc lẫn nhau)
   │                    │
   │              Structure-aware Regime      (lớp bổ sung, KHÔNG thay Raw Regime)
   └────────┬───────────┘
            ▼
     Feature Engine (fan-in CÓ CHỌN LỌC — tiêu thụ Structure output, [ADR-014](../adr/ADR-014.md))
            ▼
    Context Aggregation (CQRS, aggregator — KHÔNG sở hữu upstream computation, [Chapter 7 §7.4](../constitution/07-module-taxonomy.md))
            ▼
        Strategy ──► Decision ──► Trade Intent ──► RiskEvaluation ──► Execution Intent ──► Execution
```

Bảo toàn tường minh (theo yêu cầu task):
- Raw Regime độc lập khỏi Structure khi cần ([ADR-003](../adr/ADR-003.md), decision content vẫn hiệu lực qua [ADR-014](../adr/ADR-014.md));
- Structure-aware Regime là lớp BỔ SUNG, không thay thế Raw Regime;
- Feature Engine tiêu thụ Structure output (fan-in có chọn lọc theo Definition-pinned direct fan-in, ADR-014 v0.2);
- Context là aggregator, KHÔNG sở hữu upstream computation ([Chapter 7 §7.4](../constitution/07-module-taxonomy.md): Projection cấm phát sinh authoritative domain fact/decision);
- Decision TRƯỚC Trade Intent; Trade Intent TRƯỚC RiskEvaluation; RiskEvaluation TRƯỚC Execution Intent (`decision.md`/`trade-intent.md`/`risk.md`/`execution-intent.md`, Package 0.2-C3–C5, tất cả `Consolidated Stable`).

### 5.2 Package dependency graph (Phase 1)

```text
1.1 System Decomposition & Module Registry
      │
      ├──────────────┬─────────────────────────────┐
      ▼              ▼                             ▼
1.2 Security &   1.3-A Data/Structure/         (1.6 UX Architecture —
    Custody          Regime Engine                component/interaction
    Baseline         Architecture                  decomposition CÓ THỂ bắt
    (cross-cutting,      │                          đầu sớm, xem §6)
    tiếp tục qua          ▼
    toàn bộ Phase 1)  1.3-B Feature/Context
      │                   Engine Architecture
      │                   │
      │                   ▼
      │              1.3-C Strategy/Decision
      │                   Engine Architecture
      │                   │
      │                   ▼
      │              1.3-D Risk Gateway/Execution
      │                   Engine Architecture
      │                   │
      └───────────────────┼───────────────────┐
                           ▼                   ▼
                      1.4 API              1.5 Database
                      Architecture         Architecture
                           │                   │
                           └─────────┬─────────┘
                                     ▼
                            1.6 UX Architecture
                            (Consolidated Stable
                             boundary — cần 1.4)
```

### 5.3 Dependency lên Phase 0 artifact (mọi package)

| Package | Domain Contract | Product Requirement | Use Case & Workflow | UX Blueprint | ADR hiện có |
|---|---|---|---|---|---|
| 1.1 | `context-map.yaml`, `/docs/domain/README.md` (capability/context registry) | — | — | — | ADR-011 (governance) |
| 1.2 | `account.md` (I-11 adjacent) | PR liên quan Live-gate | — | — | ADR-012 (Account-to-Boundary Cardinality) |
| 1.3-A | `candle.md`, `structure.md`, `swing.md`, `regime.md` | `PR-XXX` liên quan Backtest/Replay | UC-004–UC-010 (Replay/Backtest) | SCR liên quan Backtest | ADR-003 (superseded), ADR-014, ADR-009 (ordering) |
| 1.3-B | `feature.md`, `context.md` | — | — | — | ADR-014 (Feature/Context fan-in boundary) |
| 1.3-C | `strategy.md`, `decision.md` | UC-001–UC-003, UC-007 | UC-007, UC-011, UC-016 | SCR-004/006/008 | ADR-009, ADR-010, ADR-013 (Strategy Definition Version axis) |
| 1.3-D | `risk.md`, `execution-intent.md`, `order.md`, `execution-result.md`, `fill.md`, `position.md` | UC-011–UC-015 | UC-011–UC-015 | Screen liên quan Paper | ADR-012 |
| 1.4 | mọi Domain Contract (published contract surface) | toàn bộ 34 `PR-XXX` | toàn bộ 21 `UC-XXX` | toàn bộ acceptance surface | Chapter 10 (Locked, không phải ADR) |
| 1.5 | mọi Domain Contract (persistence boundary) | — | UC-016–UC-018 (Review/trace) | — | Chapter 8 §8.1 (Locked) |
| 1.6 | — | toàn bộ | toàn bộ | toàn bộ 17 screen/view | — |

## 6. Authoring sequence & parallelism

```text
BẮT BUỘC TUẦN TỰ:
  1.1 → 1.3-A → 1.3-B → 1.3-C → 1.3-D          (engine pipeline dependency, §5.1)
  1.3-D → 1.4, 1.3-D → 1.5                       (API/Database cần full contract surface
                                                  của Risk/Execution — Decision→Trade Intent→
                                                  RiskEvaluation→Execution Intent PHẢI resolve
                                                  trước khi API/Database đóng boundary cho
                                                  execution path)

ĐƯỢC PHÉP SONG SONG SAU MỘT SHARED BASELINE:
  1.2 (Security & Custody Baseline) — bắt đầu SONG SONG với 1.3-A ngay khi 1.1 có baseline
    module list (KHÔNG cần đợi 1.1 Consolidated Stable đầy đủ); PHẢI đạt baseline đủ dùng
    TRƯỚC KHI 1.3-D (Execution chạm custody-adjacent boundary, I-11) và 1.4/1.5 (authentication/
    authorization boundary) tự Consolidated Stable.
  1.4 và 1.5 — SONG SONG với nhau sau khi 1.3-D Consolidated Stable (không phụ thuộc lẫn
    nhau — API định nghĩa contract shape, Database định nghĩa storage/durability, cả hai
    grounded trên cùng upstream engine contract, KHÔNG định nghĩa lại authority của nhau).
  1.6 (UX Architecture) — component/interaction decomposition THUẦN TÚY dựa trên Package
    0.3-C UX Blueprint (đã Consolidated Stable, độc lập engine internals) CÓ THỂ bắt đầu
    SỚM, song song với 1.3-A/B/C/D — NHƯNG KHÔNG được tự Consolidated Stable cho tới khi
    1.4 API Architecture cung cấp data/command contract surface nó bind vào.

PHẢI CHỜ ADR:
  Bất kỳ package nào chạm decision class "ADR LIKELY REQUIRED" (§7) phải dừng tại đúng
  boundary đó, KHÔNG tự quyết ở tầng architecture document — package đó CHỈ đạt
  `Consolidated Stable` sau khi ADR liên quan `Approved` (nếu ADR đó ảnh hưởng trực tiếp
  đến nội dung package).

PHẢI CHỜ PACKAGE KHÁC `CONSOLIDATED STABLE`:
  1.3-B chờ 1.3-A; 1.3-C chờ 1.3-B; 1.3-D chờ 1.3-C (đúng dependency graph §5.2) — KHÔNG
  author "trước" bằng cách giả định output của package chưa Consolidated Stable.
```

**Tường minh theo yêu cầu task:** KHÔNG claim cả sáu workstream có thể bắt đầu độc lập. Chỉ 1.1 là điểm khởi đầu KHÔNG phụ thuộc; mọi package khác có ít nhất một dependency (bảng §5.2/§5.3) trước khi tự nó có thể authoring đầy đủ hoặc Consolidated Stable.

## 7. ADR-scope anticipation map (planning guidance — KHÔNG quyết định)

| Workstream/Package | Decision class dự kiến | Phân loại | Căn cứ |
|---|---|---|---|
| 1.1 | System decomposition / module dependency graph | **ADR LIKELY REQUIRED** | [Governance §4b](../constitution/00-governance.md): "Module Taxonomy/dependency graph" → Required |
| 1.1 | Process/runtime boundary (service vs in-process) lần đầu thiết lập | **ADR LIKELY REQUIRED** | Thiết lập dependency graph lần đầu — cùng lý do trên |
| 1.1 | Điều chỉnh process/runtime boundary sau khi đã thiết lập | **ADR CONDITIONALLY REQUIRED** | Chỉ Required nếu đổi dependency graph/authority model đã pin; điều chỉnh không đổi graph là ADR Optional |
| 1.1 | Module hybrid declaration (một module mang ≥2 taxonomy type core) | **ADR LIKELY REQUIRED** | [Chapter 7 §7.1](../constitution/07-module-taxonomy.md) điều kiện 4: hybrid case bắt buộc ADR |
| 1.2 | Security trust boundary / authority-permission model | **ADR LIKELY REQUIRED** | [Chapter 9 §9.10](../constitution/09-plugin-model.md): "thay đổi authority/permission model" → Required |
| 1.2 | Custody boundary (I-11 technical realization) | **ADR LIKELY REQUIRED** | I-11 là invariant có mức nhạy cảm cao nhất; thiết lập cơ chế cụ thể khó đảo ngược ([Governance §4b](../constitution/00-governance.md)) |
| 1.2 | Deployment-independent module isolation (điều chỉnh không đổi authority) | **ADR CONDITIONALLY REQUIRED** | Chỉ Required nếu đổi dependency graph/authority — cấu hình triển khai thuần túy không |
| 1.3-A/B/C/D | Engine execution topology (đồng bộ/bất đồng bộ, orchestration) | **ADR LIKELY REQUIRED** | [Chapter 9 §9.10](../constitution/09-plugin-model.md): "thay đổi Decision Pipeline topology" → Required |
| 1.3-A/B/C/D | Data ownership / storage boundary MỚI chưa được Chapter 8/Domain Contract xác lập | **ADR LIKELY REQUIRED** | I-12 — thiết lập authoritative source mới cho một concept chưa có nguồn là quyết định cấu trúc |
| 1.3-A/B/C/D | Data ownership đã ngầm định resolve từ Domain Contract/Chapter 8 hiện có | **NO NEW ADR EXPECTED** | Domain Contract (Phase 0.2, `Consolidated Stable`) và Chapter 8 §8.1 đã khóa; Engine Architecture chỉ CONSUME, không redefine |
| 1.3-A/B/C/D | Thêm plugin type/capability mới (ví dụ Strategy Plugin taxonomy mở rộng) | **ADR LIKELY REQUIRED** | [Chapter 9 §9.10](../constitution/09-plugin-model.md): "thêm plugin type/capability mới" → Required |
| 1.4 | Event-bus/broker topology (transport choice cụ thể) | **NO NEW ADR EXPECTED** | [Chapter 8 §8.1](../constitution/08-event-model.md): transport KHÔNG phải authoritative source — đổi transport không đổi authority |
| 1.4 | Event log schema / Event Envelope structural change | **ADR LIKELY REQUIRED** | Thay đổi published contract → [Chapter 9 §9.10](../constitution/09-plugin-model.md) |
| 1.4 | API versioning/compatibility strategy trong khuôn khổ Chapter 10 hiện có | **NO NEW ADR EXPECTED** | [Chapter 10 §10.3](../constitution/10-compatibility-capability-contract.md) đã Locked, chỉ áp dụng |
| 1.4 | Mở rộng/diễn giải Chapter 10 theo hướng đổi published-contract semantics | **ADR CONDITIONALLY REQUIRED** | Chỉ Required nếu thực sự đổi semantics đã Locked, không chỉ mechanism (§10.9 defer) |
| 1.5 | Database source-of-truth boundary MỚI (concept chưa có authoritative source) | **ADR LIKELY REQUIRED** | Cùng lý do I-12 ở 1.3 |
| 1.5 | Database source-of-truth đã ngầm định resolve (projection/read-model, Chapter 7 §7.4) | **NO NEW ADR EXPECTED** | Đã khóa: Projection không bao giờ authoritative |
| 1.5 | Chọn công nghệ database cụ thể (không đổi authority boundary) | **NO NEW ADR EXPECTED** | Technology choice không phải authority structure — [Chapter 3 §3.1](../constitution/03-engineering-principles.md) pattern (ADR-008 chỉ ghi ngôn ngữ, không ghi mọi tech choice) |
| 1.6 | UX component/interaction architecture trong phạm vi UX Blueprint đã bounded | **NO NEW ADR EXPECTED** | Package 0.3-C đã `Consolidated Stable`, technical realization không tự nó là architecture decision thuộc diện §4b |
| 1.6 | Frontend module isolation ảnh hưởng module dependency graph tổng thể | **ADR CONDITIONALLY REQUIRED** | Chỉ Required nếu thực sự đổi dependency graph (1.1) |

**Nhắc lại (task yêu cầu):** bảng trên là **planning guidance only**. Final ADR determination xảy ra khi decision cụ thể được đề xuất, đúng [Governance §4b](../constitution/00-governance.md) — tài liệu này KHÔNG author hay approve bất kỳ ADR nào.

## 8. Package definitions

### Package 1.1 — System Decomposition & Module Registry

```text
Package ID:              1.1
Name:                     System Decomposition & Module Registry
Purpose:                  Thiết lập module dependency graph chính thức + khởi tạo
                          module-registry.yaml (Chapter 7 §7.5) — nền tảng cho mọi
                          package Phase 1 khác.
Inputs:                   Chapter 7 (Module Taxonomy, Locked), context-map.yaml
                          (Chapter 4, capability/context registry), reference pipeline
                          bản nháp tại docs/architecture/README.md.
Outputs:                  docs/architecture/module-registry.yaml (mỗi module: id,
                          module_type, responsibilities, implements_capabilities,
                          serves_contexts, emits, status); docs/architecture/system-
                          decomposition.md (dependency graph chính thức, thay bản nháp
                          Chapter 7 hiện tại).
Explicit non-goals:       KHÔNG author module interface cụ thể; KHÔNG chọn deployment
                          infrastructure/cloud provider; KHÔNG author API schema.
Dependencies:              Không phụ thuộc package Phase 1 nào khác (điểm khởi đầu).
Expected artifact paths:  docs/architecture/module-registry.yaml,
                          docs/architecture/system-decomposition.md
ADR dependencies:          Có thể phát sinh ADR mới (system decomposition, process/
                          runtime boundary — xem §7); không phụ thuộc ADR có sẵn ngoài
                          ADR-011 (governance).
Applicable quality-gate
  triggers:                Trigger A (universal). Trigger B/C KHÔNG áp dụng (không
                          executable implementation ở giai đoạn architecture). Trigger D
                          KHÔNG áp dụng (chưa định nghĩa concrete boundary). Trigger E
                          ÁP DỤNG CÓ ĐIỀU KIỆN nếu module-registry.yaml được coi là
                          published schema cho downstream tooling.
Review A scope:            Coherence với Chapter 7 taxonomy; dependency graph không mâu
                          thuẫn Chapter 8/I-12; không god-module (Chapter 7 §7.1).
Independent Review B
  scope:                   Độc lập xác nhận cùng phạm vi trên + kiểm tra không có module
                          nào bỏ sót so với domain contract đã author (Package 0.2-B1–B4/
                          C1–C7).
Product Owner decision
  point:                   Sau khi Review A + Review B CLEAN (hoặc finding resolved) —
                          Product Owner quyết Consolidated Stable cho 1.1.
Consolidation condition:  Zero unresolved Blocker/Major; mọi module đã author ở Phase
                          0.2 có entry tương ứng; không ADR LIKELY REQUIRED nào còn treo
                          chưa Approved nếu ADR đó ảnh hưởng trực tiếp nội dung đã pin.
```

### Package 1.2 — Security & Custody Baseline (cross-cutting)

```text
Package ID:              1.2
Name:                     Security & Custody Baseline
Purpose:                  Xác lập baseline evidence set cho I-4 (Strategy Isolation),
                          I-7 (Plugin Non-Bypass), I-11 (Secrets & Custody) — áp dụng
                          NGANG qua mọi package Phase 1 khác, không phải một deliverable
                          tuần tự độc lập.
Inputs:                   Chapter 2 (I-4/I-7/I-11, Locked), Chapter 9 (Plugin Model,
                          Locked), ADR-007 (Vision boundary — internal/crypto-only).
Outputs:                  docs/architecture/security-custody-baseline.md — trust
                          boundary map, isolation requirement per module class,
                          checklist mà mọi package khác PHẢI thỏa trước khi tự
                          Consolidated Stable.
Explicit non-goals:       KHÔNG design authentication implementation cụ thể; KHÔNG
                          design custody implementation cụ thể (key management, HSM,
                          v.v.); KHÔNG chọn security vendor/tool.
Dependencies:              1.1 (cần baseline module list để map trust boundary theo
                          module) — CHỈ cần baseline, KHÔNG cần 1.1 Consolidated Stable
                          đầy đủ.
Expected artifact paths:  docs/architecture/security-custody-baseline.md
ADR dependencies:          Likely tạo ADR riêng cho security trust boundary + custody
                          boundary (xem §7) — package 1.2 PHẢI dừng tại đúng boundary đó
                          chờ ADR Approved trước khi tự Consolidated Stable cho phần
                          liên quan.
Applicable quality-gate
  triggers:                Trigger A (universal). Trigger D (security) ÁP DỤNG CÓ ĐIỀU
                          KIỆN — khi baseline định nghĩa một concrete isolation/custody
                          boundary (không phải khi còn ở mức nguyên tắc chung). Trigger
                          B/C deferred tới implementation.
Review A scope:            Baseline có bao phủ đủ I-4/I-7/I-11 Scope đã khai báo; không
                          vi phạm ADR-007 boundary (internal/crypto-only).
Independent Review B
  scope:                   Độc lập kiểm tra checklist đủ để MỌI package khác (1.3-A..D,
                          1.4, 1.5) tham chiếu được, không mơ hồ.
Product Owner decision
  point:                   Sau Review A/B CLEAN cho baseline (chưa cần đợi mọi package
                          khác dùng xong checklist).
Consolidation condition:  Baseline checklist explicit, versioned, pinned; zero
                          unresolved Blocker/Major; ADR liên quan (nếu có) Approved cho
                          đúng phần baseline đã pin.
```

### Package 1.3-A — Data Ingestion & Structure/Regime Engine Architecture

```text
Package ID:              1.3-A
Name:                     Data Ingestion & Structure/Regime Engine Architecture
Purpose:                  Kiến trúc kỹ thuật cho Data Layer → Structure Engine → Raw
                          Regime Engine / Structure-aware Regime — giữ nguyên độc lập
                          Raw Regime/Structure theo ADR-003/ADR-014.
Inputs:                   candle.md, structure.md, swing.md, regime.md (Package 0.2-A/
                          B1/B2, Consolidated Stable), ADR-003 (superseded, decision
                          content hiệu lực qua ADR-014), ADR-009 (ordering), 1.1
                          Consolidated Stable.
Outputs:                  docs/architecture/engine/structure-regime-architecture.md —
                          module boundary chi tiết, data flow, event contract giữa Data
                          Layer/Structure Engine/Regime Engine (KHÔNG schema cụ thể).
Explicit non-goals:       KHÔNG author event schema (thuộc Domain Contract, đã xong);
                          KHÔNG author Engine algorithm; KHÔNG database schema.
Dependencies:              1.1 (module registry).
Expected artifact paths:  docs/architecture/engine/structure-regime-architecture.md
ADR dependencies:          Engine execution topology (§7) nếu orchestration model mới
                          được đề xuất; ngược lại KHÔNG cần ADR mới ngoài ADR-003/009/014
                          đã có.
Applicable quality-gate
  triggers:                Trigger A. Trigger C (Parity Test, Tier 1) — DEFERRED tới
                          implementation (Trigger C chỉ áp khi có executable). Trigger
                          B/D/E theo §9 (phần lớn deferred).
Review A scope:            Structure/Regime độc lập được bảo toàn tường minh; không
                          redefine domain semantics của candle.md/structure.md/regime.md.
Independent Review B
  scope:                   Độc lập xác nhận Feature Engine consumption boundary (§5.1)
                          chưa bị vi phạm sớm ở tầng này.
Product Owner decision
  point:                   Sau Review A/B CLEAN.
Consolidation condition:  Zero unresolved Blocker/Major; ADR execution-topology (nếu
                          có) Approved; không domain semantic mới bị invent.
```

### Package 1.3-B — Feature & Context Engine Architecture

```text
Package ID:              1.3-B
Name:                     Feature & Context Engine Architecture
Purpose:                  Kiến trúc kỹ thuật cho Feature Engine (fan-in có chọn lọc từ
                          Structure) và Context Aggregation (CQRS, aggregator).
Inputs:                   feature.md, context.md (Package 0.2-B3/B4, Consolidated
                          Stable), ADR-014 (Feature/Context fan-in boundary), 1.3-A
                          Consolidated Stable.
Outputs:                  docs/architecture/engine/feature-context-architecture.md.
Explicit non-goals:       KHÔNG author Context làm authoritative decision owner (cấm
                          tường minh, Chapter 7 §7.4); KHÔNG schema cụ thể.
Dependencies:              1.3-A.
Expected artifact paths:  docs/architecture/engine/feature-context-architecture.md
ADR dependencies:          KHÔNG new ADR mặc định (ADR-014 đã khóa fan-in boundary) —
                          CONDITIONALLY REQUIRED nếu kiến trúc đề xuất mở rộng fan-in
                          ngoài phạm vi ADR-014.
Applicable quality-gate
  triggers:                Trigger A. Trigger C deferred. Trigger D KHÔNG áp dụng (không
                          custody/isolation boundary ở Compute Engine/Projection thuần).
Review A scope:            Context KHÔNG sở hữu upstream computation (Chapter 7 §7.4);
                          Feature fan-in đúng ADR-014 Definition-pinned direct fan-in.
Independent Review B
  scope:                   Độc lập xác nhận Context criticality/failure policy tường
                          minh nếu Context là dependency của Decision (§7.4 yêu cầu).
Product Owner decision
  point:                   Sau Review A/B CLEAN.
Consolidation condition:  Zero unresolved Blocker/Major; không vi phạm ADR-014 boundary.
```

### Package 1.3-C — Strategy & Decision Engine Architecture

```text
Package ID:              1.3-C
Name:                     Strategy & Decision Engine Architecture
Purpose:                  Kiến trúc kỹ thuật cho Strategy Engine → Decision Engine,
                          bao gồm Plugin hosting boundary (Strategy Plugin).
Inputs:                   strategy.md, decision.md (Package 0.2-C3/C4, Consolidated
                          Stable), ADR-009 (ordering), ADR-010 (Decision effective-time),
                          ADR-013 (Strategy Definition Version axis), Chapter 9 (Plugin
                          Model), UC-001–UC-003/UC-007/UC-011/UC-016, 1.3-B Consolidated
                          Stable.
Outputs:                  docs/architecture/engine/strategy-decision-architecture.md —
                          bao gồm Plugin hosting/isolation boundary tham chiếu Chapter 9.
Explicit non-goals:       KHÔNG author Strategy Plugin algorithm; KHÔNG redefine
                          Strategy Definition/Strategy Instance/Plugin Definition
                          identity (Chapter 9 §9.3 đã khóa); KHÔNG resolve DD-003 (PAPER-
                          context Decision establishment mechanism) — chỉ tham chiếu như
                          input còn thiếu.
Dependencies:              1.3-B.
Expected artifact paths:  docs/architecture/engine/strategy-decision-architecture.md
ADR dependencies:          Engine execution topology (Decision Pipeline topology thay
                          đổi → ADR Required, §7); plugin type/capability mới (nếu có).
Applicable quality-gate
  triggers:                Trigger A. Trigger C (Parity Test, Tier 1, decision-pipeline)
                          deferred tới implementation nhưng PHẢI được thiết kế để pipeline
                          tương lai pass được (parity-by-design). Trigger E CÓ ĐIỀU KIỆN
                          nếu kiến trúc publish contract mới ngoài Domain Contract hiện có.
Review A scope:            Decision Pipeline topology không vi phạm I-2 (Decision Parity)
                          by design; Plugin hosting boundary đúng Chapter 9 §9.2 (published
                          contract only).
Independent Review B
  scope:                   Độc lập xác nhận DD-003 KHÔNG bị tự resolve ngầm ở tầng
                          architecture — mechanism cụ thể vẫn phải escalate.
Product Owner decision
  point:                   Sau Review A/B CLEAN.
Consolidation condition:  Zero unresolved Blocker/Major; ADR Decision-Pipeline-topology
                          (nếu có) Approved; DD-003 vẫn explicit Deferred, không bị đóng
                          ngầm.
```

### Package 1.3-D — Risk Gateway & Execution Engine Architecture

```text
Package ID:              1.3-D
Name:                     Risk Gateway & Execution Engine Architecture
Purpose:                  Kiến trúc kỹ thuật cho Risk Gateway (Trade Intent → Risk
                          Evaluation → Execution Intent) và Execution Engine (→ Order →
                          ExecutionResult → Fill → Position).
Inputs:                   risk.md, execution-intent.md, order.md, execution-result.md,
                          fill.md, position.md (Package 0.2-C5/C6/C7, Consolidated
                          Stable), ADR-012 (Account-to-Boundary Cardinality), UC-011–
                          UC-015, 1.3-C Consolidated Stable, 1.2 baseline (custody-
                          adjacent boundary, I-11).
Outputs:                  docs/architecture/engine/risk-execution-architecture.md.
Explicit non-goals:       KHÔNG author Risk Policy algorithm cụ thể (exposure limit
                          formula, v.v. — thuộc risk.md, đã bounded); KHÔNG design
                          custody implementation; KHÔNG author Venue Adapter protocol
                          chi tiết.
Dependencies:              1.3-C, 1.2 (custody-adjacent boundary baseline PHẢI tồn tại
                          trước khi 1.3-D tự Consolidated Stable — không cần trước khi
                          bắt đầu authoring).
Expected artifact paths:  docs/architecture/engine/risk-execution-architecture.md
ADR dependencies:          Custody boundary (§7, LIKELY REQUIRED) nếu Execution chạm
                          custody-adjacent decision; engine execution topology nếu đổi
                          Decision Pipeline topology xa hơn 1.3-C đã pin.
Applicable quality-gate
  triggers:                Trigger A. Trigger C (Chaos Test, Tier 0 — Risk Gateway/
                          Execution Engine/Position Ledger) deferred tới implementation
                          nhưng PHẢI thiết kế chaos-testable by design. Trigger D
                          (security/custody) CÓ ĐIỀU KIỆN — áp dụng khi kiến trúc định
                          nghĩa concrete custody-adjacent boundary.
Review A scope:            Decision → Trade Intent → RiskEvaluation → Execution Intent
                          thứ tự bảo toàn; Risk Policy logic KHÔNG rò rỉ ra ngoài Risk
                          Gateway (Chapter 3 §3.1).
Independent Review B
  scope:                   Độc lập xác nhận I-8 (Kill Switch)/I-10 (Idempotent Execution)
                          scope được map đúng module trong kiến trúc.
Product Owner decision
  point:                   Sau Review A/B CLEAN.
Consolidation condition:  Zero unresolved Blocker/Major; ADR custody-boundary (nếu ảnh
                          hưởng trực tiếp) Approved; 1.2 baseline đủ dùng cho phần custody-
                          adjacent đã pin.
```

### Package 1.4 — API Architecture

```text
Package ID:              1.4
Name:                     API Architecture
Purpose:                  Command/query/event contract topology cho toàn bộ platform —
                          bề mặt API mà UX Architecture (1.6) và external integration
                          (nếu có) bind vào.
Inputs:                   Chapter 10 (Compatibility/Capability Contract, Locked), Chapter
                          8 (Event Model, Locked), output contract surface của 1.3-A/B/
                          C/D (Consolidated Stable), toàn bộ 34 PR-XXX/21 UC-XXX (traceability
                          từ product layer).
Outputs:                  docs/architecture/api-architecture.md — API surface map
                          (command/query/event theo mỗi capability), versioning strategy
                          áp dụng Chapter 10 §10.3, KHÔNG schema cụ thể từng field.
Explicit non-goals:       KHÔNG author API schema chi tiết (field-level); KHÔNG chọn
                          API technology (REST/GraphQL/gRPC); KHÔNG authentication
                          implementation.
Dependencies:              1.3-A, 1.3-B, 1.3-C, 1.3-D (cần contract surface đầy đủ của
                          engine pipeline).
Expected artifact paths:  docs/architecture/api-architecture.md
ADR dependencies:          Event log schema/Envelope structural change (nếu có, LIKELY
                          REQUIRED); API versioning strategy trong khuôn khổ Chapter 10
                          hiện có — KHÔNG new ADR mặc định.
Applicable quality-gate
  triggers:                Trigger A. Trigger E (schema/contract compatibility) ÁP DỤNG
                          — API Architecture publish contract theo đúng nghĩa Chapter 10
                          §10.3. Trigger B/C/D deferred tới implementation.
Review A scope:            API surface trace đầy đủ về Domain Contract/Use Case đã tồn
                          tại — không mồ côi, không invent capability mới ngoài PR-XXX.
Independent Review B
  scope:                   Độc lập xác nhận versioning strategy khớp Chapter 10 §10.3,
                          không redefine compatibility policy đã Locked.
Product Owner decision
  point:                   Sau Review A/B CLEAN.
Consolidation condition:  Zero unresolved Blocker/Major; mọi capability engine đã
                          Consolidated Stable (1.3-A..D) có bề mặt API tương ứng, không
                          bỏ sót.
```

### Package 1.5 — Database Architecture

```text
Package ID:              1.5
Name:                     Database Architecture
Purpose:                  Storage/persistence architecture — event log store, projection/
                          read-model store, source-of-truth boundary per domain concept.
Inputs:                   Chapter 8 §8.1 (event log authoritative source, Locked), I-12
                          (Single Source of Truth), 1.1 (module registry), output của
                          1.3-A/B/C/D (Consolidated Stable).
Outputs:                  docs/architecture/database-architecture.md — store-per-concept
                          map, projection rebuild strategy, KHÔNG schema DDL cụ thể.
Explicit non-goals:       KHÔNG author database schema (DDL); KHÔNG chọn database
                          technology cụ thể (trừ khi ảnh hưởng authority boundary); KHÔNG
                          migration script.
Dependencies:              1.1, 1.3-A, 1.3-B, 1.3-C, 1.3-D.
Expected artifact paths:  docs/architecture/database-architecture.md
ADR dependencies:          Database source-of-truth boundary MỚI (nếu concept nào chưa
                          có authoritative source resolve từ Chapter 8/Domain Contract —
                          LIKELY REQUIRED); technology choice thuần túy — KHÔNG cần ADR.
Applicable quality-gate
  triggers:                Trigger A. Trigger E CÓ ĐIỀU KIỆN nếu store định nghĩa schema
                          publish riêng ngoài event log. Trigger B/C/D deferred.
Review A scope:            Không projection nào được coi authoritative thay authoritative
                          source (Chapter 7 §7.4); rebuild determinism (Chapter 7 §7.4)
                          thiết kế đúng.
Independent Review B
  scope:                   Độc lập xác nhận mọi domain concept có đúng MỘT authoritative
                          store resolve được — không ambiguous/competing store.
Product Owner decision
  point:                   Sau Review A/B CLEAN.
Consolidation condition:  Zero unresolved Blocker/Major; ADR source-of-truth-boundary
                          (nếu có) Approved.
```

### Package 1.6 — UX Architecture

```text
Package ID:              1.6
Name:                     UX Architecture
Purpose:                  Technical realization của Package 0.3-C UX Blueprint (17
                          screen/view, WS-001, NAV-001–006) — component decomposition,
                          state management, frontend module boundary.
Inputs:                   ux-blueprint.md (Package 0.3-C, Consolidated Stable), 1.4 API
                          Architecture (data/command contract surface để bind).
Outputs:                  docs/architecture/ux-architecture.md.
Explicit non-goals:       KHÔNG author component code; KHÔNG chọn frontend framework;
                          KHÔNG pixel-level design; KHÔNG redefine screen/flow/state đã
                          bounded ở ux-blueprint.md.
Dependencies:              1.4 (để Consolidated Stable — authoring component/interaction
                          decomposition thuần túy dựa trên UX Blueprint CÓ THỂ bắt đầu
                          sớm hơn, xem §6).
Expected artifact paths:  docs/architecture/ux-architecture.md
ADR dependencies:          Frontend module isolation ảnh hưởng dependency graph tổng
                          thể (CONDITIONALLY REQUIRED, xem §7) — mặc định KHÔNG new ADR.
Applicable quality-gate
  triggers:                Trigger A. Trigger B/C (Tier 3, ưu tiên E2E) deferred tới
                          implementation. Trigger D/E KHÔNG áp dụng mặc định.
Review A scope:            Mọi SCR/VIEW/WS/NAV/FLOW/STATE trace được về component
                          architecture — không mồ côi, không invent UX behavior mới
                          ngoài ux-blueprint.md.
Independent Review B
  scope:                   Độc lập xác nhận data-binding khớp đúng API Architecture
                          (1.4) contract surface, không tự phát minh contract riêng.
Product Owner decision
  point:                   Sau Review A/B CLEAN.
Consolidation condition:  Zero unresolved Blocker/Major; 1.4 Consolidated Stable; toàn
                          bộ acceptance surface UX Blueprint có component tương ứng.
```

## 9. Quality-gate trigger map (tổng hợp)

| Package | Trigger A (universal) | Trigger B (coverage) | Trigger C (tier/chaos/parity) | Trigger D (boundary) | Trigger E (schema/contract) |
|---|---|---|---|---|---|
| 1.1 | Áp dụng | Deferred (implementation) | N/A | N/A | Điều kiện (nếu registry là published schema) |
| 1.2 | Áp dụng | Deferred | N/A | Điều kiện (khi định nghĩa concrete boundary) | N/A |
| 1.3-A | Áp dụng | Deferred | Deferred (Tier 1 Parity — thiết kế parity-by-design) | N/A | N/A |
| 1.3-B | Áp dụng | Deferred | Deferred | N/A | N/A |
| 1.3-C | Áp dụng | Deferred | Deferred (Tier 1 Parity — decision-pipeline) | N/A | Điều kiện |
| 1.3-D | Áp dụng | Deferred | Deferred (Tier 0 Chaos — Risk/Execution/Position) | Điều kiện (custody-adjacent) | N/A |
| 1.4 | Áp dụng | Deferred | N/A | N/A | **Áp dụng** (publish contract) |
| 1.5 | Áp dụng | Deferred | N/A | N/A | Điều kiện |
| 1.6 | Áp dụng | Deferred (Tier 3) | Deferred | N/A | N/A |

Ghi chú bắt buộc (task yêu cầu): Phase 1 là **architecture artifact**, KHÔNG phải implementation — Trigger B (coverage)/C (tier/chaos/parity thực thi) **deferred tới implementation** cho MỌI package (không executable implementation tại giai đoạn này, đúng logic `phase-0-dod.md` §2 đã áp dụng cho Product artifact). Trigger D chỉ **conditional** — áp dụng KHI VÀ CHỈ KHI artifact kiến trúc thực sự định nghĩa một concrete boundary (không áp dụng cho tuyên bố nguyên tắc chung). Trigger A luôn áp dụng — invariant conformance BY DESIGN phải verify được ngay ở tầng architecture, dù chưa có code.

## 10. Candidate Phase 1 completion criteria (planning input — KHÔNG phải Phase 1 DoD chính thức)

**Đánh dấu tường minh: đây là input cho một Phase 1 DoD artifact riêng sau này (theo pattern `phase-0-dod.md`), KHÔNG tự nó là DoD, KHÔNG được Product Owner accept tại tài liệu này.**

```text
Candidate completion criteria:
  - Cả chín package (1.1, 1.2, 1.3-A/B/C/D, 1.4, 1.5, 1.6) đạt Consolidated Stable tại
    MANIFEST.
  - Mọi ADR phát sinh từ §7 (LIKELY REQUIRED, khi decision cụ thể được đề xuất) đã
    Approved.
  - Zero unresolved Blocker/Major finding trên bất kỳ Phase 1 deliverable nào.
  - Full-scope Backward Consistency Check (Chapter 12 §12.4) = No conflict giữa toàn bộ
    Phase 1 deliverable và mọi authority Locked (Constitution, Domain Contract, Product
    layer, ADR).

Required evidence classes:
  - Review A + Independent Review B evidence per package (Chapter 0 §3 minimum-two).
  - Applicable Quality Gate evidence — Trigger A (mọi package) tại thời điểm gate; Trigger
    B/C/D/E theo đúng bảng §9 (phần lớn vẫn deferred tới Phase 3 tại thời điểm Phase 1
    gate — Phase 1 KHÔNG implementation).
  - Module-registry.yaml (1.1) là exact reviewed baseline cho mọi tier-resolution tương
    lai (Chapter 13 §13.4).

Required package lifecycle states:
  - Mọi package Consolidated Stable (package lifecycle) — artifact tự nó có thể vẫn
    Draft (approved_by null), đúng pattern Phase 0 đã dùng nhất quán.

ADR closure expectation:
  - Mọi ADR LIKELY REQUIRED đã phát sinh trong Phase 1 phải Approved trước Phase 1 gate;
    ADR CONDITIONALLY REQUIRED resolve theo từng trường hợp cụ thể tại thời điểm quyết
    định phát sinh — không mặc định cần ADR nếu điều kiện trigger không xảy ra.

Cross-package consistency expectation:
  - Không authority cạnh tranh giữa 1.3-A/B/C/D (đúng dependency graph §5.2); 1.4/1.5
    không redefine authority của nhau; 1.6 không tự phát minh contract ngoài 1.4.

Full-scope BCC requirement:
  - Đúng theo Chapter 12 §12.4, đánh giá TOÀN BỘ Phase 1 deliverable đối chiếu Constitution/
    Domain Contract/Product layer/ADR đã Locked — KHÔNG per-package BCC thay thế được.

Final Phase 1 Approval Gate inputs (dự kiến, chưa xác nhận):
  - Phase 1 DoD artifact riêng (chưa author) — accepted + incorporated theo đúng Chapter
    14 §14.3.1 pattern đã dùng cho Phase 0.
  - Chín package Consolidated Stable + review evidence.
  - Full-scope BCC No Conflict.
  - Product Owner decision fact.
```

## 11. Deferred/open items mang sang Phase 1 (tham chiếu, KHÔNG tự resolve)

```text
DD-001  Backtest Domain Contract/entity/event/schema — Deferred, đích Phase 1
        architecture/domain design. Constraint: KHÔNG suy diễn từ PAPER entity
        (BacktestOrder/BacktestFill/BacktestPosition/BacktestExecutionResult KHÔNG được
        invent). Liên quan trực tiếp: Package 1.3-A (Backtest run trace, UC-006/UC-007).
        Quyết định author Domain Contract riêng cho Backtest vẫn là Product Owner
        decision tương lai, NGOÀI phạm vi tài liệu này.

DD-003  PAPER-context authoritative Decision establishment mechanism — Deferred, đích
        Phase 1, mandatory TRƯỚC KHI UC-011 runtime design. Liên quan trực tiếp: Package
        1.3-C (Strategy/Decision Engine Architecture). Package 1.3-C KHÔNG được tự phát
        minh mechanism này — chỉ escalate.

OQ-001  Data Retention Policy & Access Control Model chi tiết — Partially Resolved,
        RBAC cụ thể vẫn mở. Liên quan: Package 1.2 (Security & Custody Baseline), Package
        1.5 (Database Architecture — retention).

OQ-002  Strategy Lifecycle Gate (Backtest=YES + Paper=YES trước Live) — Open. Liên quan:
        Package 1.3-C/1.3-D (không tự đóng ngầm OQ-002 bằng cách tuyên bố lifecycle gate
        đã đủ điều kiện, đúng Chapter 9 §9.10 cảnh báo).

OQ-003  Product Metrics cụ thể cho "Measurable" — Open. Liên quan: Package 1.4 (API có
        thể cần expose metric surface), không resolve tại Phase 1 architecture.
```

Tài liệu này KHÔNG thay đổi trạng thái bất kỳ mục nào ở trên — chỉ tổng hợp tham chiếu cho package planning.

## 12. Self-review

```text
1.  Complete Chapter 14 Phase 1 scope?               ĐẠT — 6/6 workstream (§3–§4).
2.  No missing workstream?                            ĐẠT — Software/UX/Security&Custody/
                                                       API/Database/Engine đều có package
                                                       tương ứng (§4).
3.  Dependency direction coherent?                     ĐẠT — engine pipeline bảo toàn
                                                       nguyên vẹn (§5.1), package graph
                                                       nhất quán (§5.2).
4.  Parallelism không vi phạm dependency?              ĐẠT — §6 chỉ cho phép song song sau
                                                       shared baseline đã pin, không claim
                                                       sáu workstream độc lập.
5.  ADR planning không pre-decide outcome?             ĐẠT — §7 chỉ phân loại LIKELY/
                                                       CONDITIONALLY/NO, không quyết định
                                                       nội dung ADR nào.
6.  Product/Domain authority không bị redefine?        ĐẠT — §2 khóa boundary tường minh;
                                                       mọi package §8 explicit non-goals
                                                       cấm redefine semantics.
7.  Quality gate không áp dụng sớm?                    ĐẠT — §9 tường minh Trigger B/C
                                                       deferred tới implementation, D chỉ
                                                       conditional.
8.  Không implementation design leak?                  ĐẠT — mọi package §8 "Explicit
                                                       non-goals" cấm schema/interface/
                                                       algorithm/infrastructure cụ thể.
9.  Mọi package có completion/review boundary rõ?      ĐẠT — 9/9 package đủ Review A/
                                                       Review B/PO decision point/
                                                       Consolidation condition (§8).
10. Phase 1 vẫn not Complete?                          ĐẠT — §1/§10 không tuyên bố hoàn
                                                       thành; §10 chỉ là candidate input.
11. Không Phase 1 package tự approve?                  ĐẠT — mọi Consolidation condition
                                                       yêu cầu Review A+B+PO decision,
                                                       không self-certify (đúng nguyên tắc
                                                       anti-self-certification, Chapter 13
                                                       §13.4.1).
12. Live vẫn Unauthorized?                             ĐẠT — không mục nào trong tài liệu
                                                       chạm Live authorization.
```

## 13. Scope restrictions honored (xác nhận tường minh)

```text
KHÔNG author: concrete module interface, API schema, database schema, deployment
  infrastructure, cloud provider, programming framework, custody implementation,
  authentication implementation, Engine algorithm, source code, Phase 1 ADR.
KHÔNG approve: bất kỳ Phase 1 package nào.
KHÔNG declare: Phase 1 Complete.
KHÔNG authorize: Live.
OQ-001/OQ-002/OQ-003: chỉ referenced (§11), lifecycle state không đổi.
```
