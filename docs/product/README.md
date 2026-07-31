---
id: product-index
title: Product Requirement & UX Index
status: Draft
version: "0.1"
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-07-31"
last_review: null
next_review: null
---

# Product — Phase 0.3 (Product Requirement · Use Case & Workflow · UX Blueprint)

Thư mục này chứa artifact của **Phase 0.3** ([Chapter 14 §14.2](../constitution/14-roadmap.md), Locked) — sub-phase kế tiếp sau [Phase 0.2 — Domain Model & Domain Contract](../domain/README.md) (`Complete`, Product Owner decision 2026-07-31, baseline `95fdb01ea662e741fa08f4c2d79727cc13c1a54a`). Mỗi artifact = 1 deliverable, decompose thành ba package theo đúng danh sách Roadmap.

## Dependency prerequisite

Toàn bộ artifact tại đây PHẢI dùng lại nguyên vẹn vocabulary đã đăng ký tại [`/docs/domain/`](../domain/README.md) (Package 0.2-A/B/C, tất cả `Consolidated Stable`) — KHÔNG định nghĩa domain concept mới. Controlling Constitution sources: [Chapter 1](../constitution/01-vision.md) (Vision, Locked), [Chapter 2](../constitution/02-platform-invariants.md) (Platform Invariants, Locked), [Chapter 4 §4.5](../constitution/04-domain-principles.md) (Domain Modeling phải ổn định trước khi UX Blueprint được phê duyệt — Locked). [ADR-007](../adr/ADR-007.md) (Locked) khóa ranh giới sản phẩm: nội bộ, single-workspace, crypto-only, 2-3 sàn.

**Không có Locked chapter nào định nghĩa format riêng cho Product Requirement/Use Case & Workflow/UX Blueprint** (khác Domain Contract, vốn có [Chapter 4 §4.3](../constitution/04-domain-principles.md)) — `product-requirement.md` (Package 0.3-A) đồng thời là **conformance example đầu tiên** cho format artifact loại này, đúng vai trò `candle.md` đã đóng cho Domain Contract tại Package 0.2-A.

## Drafting packages

| Package | Nội dung | Trạng thái |
|---|---|---|
| **0.3-A — Product Requirement** | [`product-requirement.md`](./product-requirement.md) v0.1 Draft — 32 requirement (`PR-001`–`PR-032`), truy vết Vision/Platform Invariant/Domain Contract | Draft — **Authoring baseline, chưa `Consolidated Stable`** — chờ ChatGPT Review A + Independent Review B |
| **0.3-B — Use Case & Workflow** | chưa author — phụ thuộc 0.3-A `Consolidated Stable` | Chưa bắt đầu, chưa authorize |
| **0.3-C — UX Blueprint** | chưa author — phụ thuộc 0.3-B `Consolidated Stable` | Chưa bắt đầu, chưa authorize |

**Thứ tự authoring bắt buộc:** 0.3-A → 0.3-B → 0.3-C, tuần tự — mỗi package phụ thuộc trực tiếp package trước (đúng [Chapter 4 §4.5](../constitution/04-domain-principles.md) và dependency logic: không thể viết use case cho requirement chưa tồn tại, không thể thiết kế UX cho use case chưa tồn tại).

## Package 0.3-A — Product Requirement (authoring baseline)

**Phạm vi (scope tối thiểu, walking-skeleton):** dịch [Vision](../constitution/01-vision.md) thành 32 requirement cụ thể, testable, bounded (`PR-001`–`PR-032`) — 8 functional, 6 non-functional (restating existing Constitution/Domain Contract guarantee, không thêm yêu cầu mới), 18 lifecycle (Research/Replay/Backtest/Paper/Review/Improve, 3 tới 4 mỗi giai đoạn). Bounded theo [ADR-007](../adr/ADR-007.md): nội bộ, single-workspace, crypto-only, 2-3 sàn. Live được nhắc tới DUY NHẤT như một lifecycle boundary bị hoãn (`OQ-002`).

**KHÔNG author:** screen layout/wireframe/component hierarchy/UX architecture; backend/frontend/API/database/security/custody/deployment architecture; exchange adapter design; concrete KPI/Product Metrics (`OQ-003`); Live-gate criteria (`OQ-002`); multi-tenant/multi-asset design; Domain Contract semantic mới.

**Trạng thái review:**

- Author self-review (authoring, v0.1): **hoàn tất.**
- ChatGPT Review A: **chưa chạy** — baseline này gửi đi làm điểm khởi đầu.
- Independent Review B: **chưa chạy.**
- Consolidation: **chưa bắt đầu** — Package 0.3-A **CHƯA** đạt `Consolidated Stable`.

**Không tuyên bố hoàn thành hay approval nào (mục 0.3-A):** `product-requirement.md` `status: Draft`, `version: "0.1"`, `approved_by: null`, `approved_at: null`; không Product Owner Approve; không Lock; không Consolidate; không đóng `OQ-002`/`OQ-003`; không authorize Live; không sửa bất kỳ Domain Contract/ADR/Constitution nào; Package 0.2-A/B/C vẫn `Consolidated Stable`, không đổi.

## Ngoài phạm vi Phase 0.3 — defer

- Phase 0 DoD, Phase 0 Approval Gate work (thuộc [Chapter 12](../constitution/12-approval-gates.md), một transaction riêng, lớn hơn, sau khi 0.3-A/B/C đều `Consolidated Stable`).
- Phase 1 System/UX Architecture, API/Database/Engine design (`/docs/architecture/`, chưa bắt đầu).
- Concrete Product Metrics (`OQ-003`), Strategy Lifecycle Live-gate (`OQ-002`).

**Package 0.2-A/B/C vẫn `Consolidated Stable`, byte-for-byte không đổi.** OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.3 là sub-phase đang active — Phase 0 vẫn active và chưa hoàn tất; Phase 1 vẫn unauthorized.
