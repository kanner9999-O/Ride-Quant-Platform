---
id: 14-roadmap
title: Roadmap
version: "1.2"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-28"
next_review: null
depends_on: ["00-governance", "01-vision", "02-platform-invariants", "03-engineering-principles", "04-domain-principles", "05-time-model", "06-identity-model", "07-module-taxonomy", "08-event-model", "09-plugin-model", "10-compatibility-capability-contract", "11-adr-process", "12-approval-gates", "13-quality-gates"]
---

# 14. Roadmap

> **Trạng thái:** `In Review`. Theo [Chapter 12 §12.3](./12-approval-gates.md) (Locked), khi còn `In Review` chương này được prose-reference như **intended owner** của phase sequence và DoD content, nhưng nội dung draft **chưa phải binding Locked authority**. Các yêu cầu dưới đây chỉ trở thành authoritative phase plan mà [Chapter 12 §12.1–§12.2](./12-approval-gates.md) và [Chapter 13 §13.12](./13-quality-gates.md) tham chiếu **sau khi** Product Owner Approve/Lock.

## 14.1 Phạm vi và thẩm quyền

Chapter 14 sở hữu **phase sequence · nội dung/deliverable của từng Phase · nơi ở và cardinality của Definition of Done (DoD) · khai báo gate set áp cho phase deliverable**.

Chapter 14 **không** sở hữu và **không định nghĩa lại**:

- **cơ chế phase approval** — thuộc [Chapter 12](./12-approval-gates.md) (Locked);
- **quality gate semantics/applicability** — thuộc [Chapter 13](./13-quality-gates.md) (Locked);
- **ADR Scope Rule** — thuộc [Chapter 0 §4b](./00-governance.md) / [Chapter 11](./11-adr-process.md);
- **module taxonomy/dependency graph** — thuộc [Chapter 7](./07-module-taxonomy.md);
- **current version/status/state của tài liệu** — thuộc [MANIFEST](../MANIFEST.md) theo [I-12](./02-platform-invariants.md).

**Đơn vị chịu Approval Gate là `Phase`.** Sub-phase (ví dụ 0.1/0.2/0.3) là **work unit bên trong** một Phase — sub-phase **không** tự mở Approval Gate riêng. `Phase 1.5` là một **Phase** đầy đủ (không phải sub-phase) và có Approval Gate riêng.

## 14.2 Phase sequence

Theo [Chapter 12](./12-approval-gates.md) (Locked): **mọi Phase kết thúc bằng một Approval Gate trước khi Phase kế tiếp bắt đầu — không được nhảy phase.** Sequence dưới đây khai báo Approval Gate cho **mọi** Phase, không có ngoại lệ.

```text
Phase 0 — Vision & Foundation
  0.1  Constitution (Chapter 0–14) + governance activation
  0.2  Domain Model & Domain Contract (/docs/domain/)
       — sub-phase này được tham chiếu bởi Chapter 6 §6.4 (Account first-class)
         và Chapter 7 §7.5 (module-registry placement)
  0.3  Product Requirement · Use Case & Workflow · UX Blueprint
  → ADR cho quyết định Domain thuộc diện ADR Required (Governance §4b, không phải mọi định nghĩa)
  → Approval Gate

Phase 1 — System Architecture
  Software · UX Architecture · Security & Custody Baseline · API · Database · Engine
  → ADR cho quyết định kiến trúc thuộc diện ADR Required (Governance §4b)
  → Approval Gate

Phase 1.5 — Engineering Foundation (tài liệu SỐNG, sửa qua ADR)
  Monorepo · Coding Standard · Naming · Logging · Config · Error Handling · Testing · CI/CD
  → Approval Gate

Phase 2 — Product Prototype (HTML/React/Figma — công cụ không quan trọng)
  → Approval Gate

Phase 3 — Core Backend (build ĐÚNG theo dependency graph ở 07-module-taxonomy.md)
  Data Layer → Structure Engine & Raw Regime Engine (song song, độc lập)
             → Feature Engine → Context Projection
             → Strategy → Decision → Risk Gateway → Execution
  → Quality Gate theo Tier (13-quality-gates.md) — cấp module/artifact
  → Approval Gate

Phase 4 — Frontend
  → Approval Gate

Phase 5 — Integration
  → Approval Gate

Phase 6 — Simulation Platform
  Replay · Backtest · Walk-Forward · Paper Trade · Monte Carlo · Stress Test · Scenario Test
  → Kiểm chứng Parity Principle (I-2) ở CẤP PLATFORM — KHÔNG thay thế Parity Test
    cấp module mà Chapter 13 §13.4 đã yêu cầu cho Tier 1 tại Phase 3
  → Approval Gate

Phase 7 — Deployment
  → Approval Gate

Phase 8 — Research Platform (tách biệt khỏi Production)
  Strategy Comparison · Parameter/Genetic Optimization · Feature Importance
  · Regime Analysis · Performance Attribution
  → Approval Gate

Phase 9 — Observability
  Metrics · Logs · Tracing · Alerts · Dashboard · Health
  → Approval Gate

Ghi chú:
  - AI Layer KHÔNG là một Phase riêng — theo Invariant I-7, nó chỉ là
    consumer mới của published contract, trừ khi tham gia Decision (khi đó là
    Decision Advisor, theo 09-plugin-model.md).
```

## 14.3 Definition of Done — cardinality và nơi ở

[Chapter 12 §12.1](./12-approval-gates.md) (Locked) đã khóa **rule**: mỗi Phase phải có DoD cụ thể, được viết ra và Product Owner chấp nhận **trước khi** Phase đó mở Approval Gate; `Approved` là outcome của gate, **không** được là một mục trong DoD. Chapter 14 **không định nghĩa lại** rule đó — chương này đáp ứng phần [Chapter 12 §12.3](./12-approval-gates.md) delegate cho nó: **DoD content thuộc về đâu và resolve thế nào**.

- **Cardinality:** mỗi Phase phải resolve được **đúng một** authoritative DoD artifact cho Phase đó. Nhiều DoD cạnh tranh cho cùng một Phase → không resolve được → fail-closed.
- **Tồn tại trước gate:** DoD của Phase N phải tồn tại và được chấp nhận **trước khi** Phase N mở Approval Gate — cùng nguyên tắc "criteria defined before used" ([Chapter 12 §12.1](./12-approval-gates.md), [Chapter 13 §13.7](./13-quality-gates.md)).
- **Resolvable + versioned/pinned:** DoD artifact phải explicit, versioned và pin được vào đúng Phase; **cấm** mutable reference kiểu "bản mới nhất".
- **Fail-closed:** DoD không tồn tại, không resolve được, hoặc chưa được chấp nhận → **eligibility incomplete** theo [Chapter 12 §12.2](./12-approval-gates.md), **không** phải reviewer veto và **không** phải Product Owner rejection.
- **Không tạo state store cạnh tranh:** current version/status của DoD artifact resolve từ **MANIFEST** theo [I-12](./02-platform-invariants.md).

**Storage/format/filename cụ thể của DoD artifact defer** — Constitution khóa *tồn tại + property*, không khóa cơ chế (§14.6).

## 14.4 Quality gate declaration cho phase deliverable

[Chapter 13 §13.12](./13-quality-gates.md) (Locked) khai báo: **Phase deliverable → gate set mà approved phase plan/roadmap ([Chapter 14](./14-roadmap.md)) khai báo áp dụng.** Đây là delegation Chapter 14 phải đáp ứng — nếu để trống, prerequisite [Chapter 12 §12.2(5)](./12-approval-gates.md) không có nguồn resolve.

- **Gate set áp cho phase deliverable của mỗi Phase phải được khai báo tường minh trong DoD artifact của chính Phase đó** (§14.3), và phải resolve được **trước** gate evaluation.
- **Không khai báo được → fail-closed** (§14.3), **không** được mặc định "không gate nào áp dụng".
- **Chapter 14 KHÔNG định nghĩa lại gate applicability cấp artifact.** Trigger A–E của [Chapter 13 §13.12](./13-quality-gates.md) (universal invariant conformance · executable-implementation-triggered coverage · tier-triggered · responsibility/boundary-triggered · lifecycle-triggered) vẫn thuộc Chapter 13 và áp độc lập với khai báo ở đây.
- **Quality Gate KHÔNG chỉ tồn tại ở Phase 3.** Dòng `Quality Gate theo Tier` trong sequence Phase 3 (§14.2) là **nhấn mạnh** giai đoạn build module, **không** phải giới hạn phạm vi. Mọi Phase Approval Gate đều chịu [Chapter 12 §12.2(5)](./12-approval-gates.md): applicable quality gates phải **thực sự PASS**.
- **Quality Gate ≠ Approval Gate** ([Chapter 13 §13.1](./13-quality-gates.md)): gate pass chỉ sinh eligibility evidence; Product Owner vẫn là authority duy nhất quyết định phase transition.

## 14.5 Authority boundary

| Concern | Authority |
|---|---|
| Phase sequence · phase deliverable · DoD cardinality/nơi ở · gate-set declaration cho phase deliverable | **Chapter 14 (chương này)** |
| Phase approval orchestration · DoD rule · prerequisite aggregation | [Chapter 12](./12-approval-gates.md) |
| Quality criteria · gate semantics · gate applicability cấp artifact · evidence contract | [Chapter 13](./13-quality-gates.md) |
| Review eligibility (số lượng, role, no-veto) | [Chapter 0 §3](./00-governance.md) / [Chapter 11 §11.5](./11-adr-process.md) |
| ADR Scope Rule · ADR lifecycle | [Chapter 0 §4b](./00-governance.md) / [Chapter 11](./11-adr-process.md) |
| Module taxonomy · dependency graph · module→tier registry | [Chapter 7](./07-module-taxonomy.md) |
| Platform invariants + verification | [Chapter 2](./02-platform-invariants.md) |
| Current version/status/state · Decision Log · OQ state | [MANIFEST](../MANIFEST.md) theo [I-12](./02-platform-invariants.md) |

Chapter 14 **không** tạo competing authority; **không** tự mở phase transition; **không** thay Product Owner quyết định.

## 14.6 Ngoài phạm vi — defer

- **Storage/format/filename cụ thể** của DoD artifact và của gate-set declaration (§14.3–§14.4) — Constitution khóa *tồn tại + property*, không khóa filename/schema/tooling.
- **Nội dung DoD cụ thể của từng Phase** — viết khi Phase đó chuẩn bị mở gate, theo đúng §14.3.
- **Không đóng open question:** chương này **không** giải quyết **OQ-002** (Strategy Lifecycle Live-gate) hay **OQ-003** (Product Metrics). Việc Phase 6 có Paper Trade và Phase 7 có Deployment **không** đồng nghĩa "được phép lên Live" — điều kiện đó vẫn thuộc OQ-002, nhất quán [Chapter 9 §9.10](./09-plugin-model.md), [Chapter 10 §10.8.2](./10-compatibility-capability-contract.md) và [Chapter 13 §13.1](./13-quality-gates.md) (không chapter nào được đóng ngầm OQ-002).
