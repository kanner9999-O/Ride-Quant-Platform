---
id: product-index
title: Product Requirement & UX Index
status: Draft
version: "0.3"
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
| **0.3-A — Product Requirement** | [`product-requirement.md`](./product-requirement.md) v0.2 Draft — 34 requirement (`PR-001`–`PR-034`), truy vết Vision/Platform Invariant/Domain Contract | Draft — **`Consolidated Stable`** (xem dưới) |
| **0.3-B — Use Case & Workflow** | chưa author — phụ thuộc 0.3-A `Consolidated Stable` (đã thỏa) | Chưa bắt đầu, **Unauthorized** |
| **0.3-C — UX Blueprint** | chưa author — phụ thuộc 0.3-B `Consolidated Stable` | Chưa bắt đầu, **Unauthorized** |

**Thứ tự authoring bắt buộc:** 0.3-A → 0.3-B → 0.3-C, tuần tự — mỗi package phụ thuộc trực tiếp package trước (đúng [Chapter 4 §4.5](../constitution/04-domain-principles.md) và dependency logic: không thể viết use case cho requirement chưa tồn tại, không thể thiết kế UX cho use case chưa tồn tại).

## Package 0.3-A — Product Requirement `Consolidated Stable`

**Phạm vi (scope tối thiểu, walking-skeleton):** dịch [Vision](../constitution/01-vision.md) thành 34 requirement cụ thể, testable, bounded (`PR-001`–`PR-034`) — 8 functional, 6 non-functional (restating existing Constitution/Domain Contract guarantee, không thêm yêu cầu mới), 20 lifecycle (Research/Replay/Backtest/Paper/Review/Improve). Bounded theo [ADR-007](../adr/ADR-007.md): nội bộ, single-workspace, crypto-only, 2-3 sàn. Live được nhắc tới DUY NHẤT như một lifecycle boundary bị hoãn (`OQ-002`).

**v0.2 — bounded correction (đóng consolidated Review A + Independent Review B findings, một Major + ba Minor):** (1) `P03A-MAJ-01` — Backtest nay yêu cầu simulated economic evidence/exposure progression (`PR-033`, MỚI) VÀ strategy-level evaluable result so sánh cross-run/cross-version (`PR-034`, MỚI), cộng một Backtest authority boundary tường minh (KHÔNG tái sử dụng PAPER fact làm Backtest authority). (2) `P03A-MIN-01` — thay "Decision hash" bằng `canonical semantic-decision hash` (`PR-010`/`PR-019`), định nghĩa theo Decision Contract authoritative. (3) `P03A-MIN-02` — bỏ quy tắc "resolve về đúng một nguồn," thay bằng "một hoặc nhiều applicable authoritative source, có thể kết hợp." (4) `P03A-B-MIN-03` — `PR-019` viết lại tách bạch historical reconstruction (mặc định) vs parity recomputation (tuỳ chọn), cộng một Replay authority boundary (không `ReplayDecision`, không Decision trùng lặp).

**KHÔNG author:** screen layout/wireframe/component hierarchy/UX architecture; backend/frontend/API/database/security/custody/deployment architecture; exchange adapter design; concrete KPI/Product Metrics (`OQ-003`); Live-gate criteria (`OQ-002`); multi-tenant/multi-asset design; Domain Contract semantic mới; Backtest entity/event/schema; simulation/fee/slippage/accounting/PnL model; `ReplayDecision`/Replay authority stream mới.

**Trạng thái review:**

- Author self-review (authoring, v0.1): **hoàn tất.**
- ChatGPT Review A + Independent Review B (baseline v0.1): **hoàn tất** — một Major + ba Minor finding (`P03A-MAJ-01`/`P03A-MIN-01`/`P03A-MIN-02`/`P03A-B-MIN-03`) consolidated.
- Bounded correction commit (v0.1 → v0.2), Product Owner authorized: **hoàn tất** — đóng toàn bộ bốn finding, xem chi tiết trên.
- ChatGPT Delta Review A (trên v0.2): **Clean** — 0 blocking finding.
- Independent Delta Review B (trên v0.2): **Clean** — 0 blocking finding.
- Consolidation: **hoàn tất (transaction này)** — Product Owner authorized: "Package 0.3-A — Product Requirement: Consolidated Stable". **Package 0.3-A nay `Consolidated Stable`.**

**Kết luận consolidation:** ChatGPT Delta Review A (Clean) và Independent Delta Review B (Clean) trên `product-requirement.md` v0.2, **0 finding còn lại chưa xử lý** (finding ledger đầy đủ — một Major + ba Minor qua bounded correction v0.1→v0.2, tại mục baseline dưới đây). Product Owner authorized: "Package 0.3-A — Product Requirement: Consolidated Stable".

## `Consolidated Stable` baseline — Package 0.3-A

**Exact reviewed artifact baseline (pinned):**

```text
product-requirement.md   v0.2   Draft   blob fce5cd55f4cd71decfd59afcf2ab109cecf3c3f8
product/README.md        v0.2   Draft   blob 0426407cebbf2ef13497da4a45746984d5697dd4 (pre-consolidation)
consolidated baseline HEAD:  a8e39c92a73ba05b9f9a196bd75e4ea4037cb285
```

**Finding ledger — tất cả resolved qua bounded correction (v0.1 → v0.2):**

```text
P03A-MAJ-01      — Resolved (PR-033/PR-034 MỚI — Backtest simulated economic evidence/exposure
                    progression/strategy-level evaluable result, cộng Backtest authority boundary)
P03A-MIN-01      — Resolved (thay "Decision hash" bằng canonical semantic-decision hash, PR-010/PR-019)
P03A-MIN-02      — Resolved (bỏ quy tắc "đúng một nguồn", thay bằng "một hoặc nhiều applicable source")
P03A-B-MIN-03    — Resolved (PR-019 tách bạch historical reconstruction/parity recomputation, cộng
                    Replay authority boundary)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

**`Consolidated Stable` là package lifecycle/readiness state — KHÔNG phải document approval status**, đúng định nghĩa đã khóa cho mọi package trước đó (xem [`/docs/domain/README.md`](../domain/README.md) mục Package 0.2-A): authoring + bounded correction hoàn tất cho phạm vi 0.3-A; ChatGPT Delta Review A hoàn tất (Clean); Independent Delta Review B hoàn tất (Clean); mọi qualifying finding đã xử lý; artifact đã review được pin chính xác; package đủ ổn định để Package 0.3-B (Use Case & Workflow) bắt đầu planning — **không** ngụ ý Product Owner Approval cho `product-requirement.md`, **không** ngụ ý Lock, **không** authorize Package 0.3-B tự động, **không** đóng OQ-002/OQ-003, **không** authorize Live, **không** tuyên bố Phase 0.3 hoàn thành. `product-requirement.md` **vẫn giữ `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte không đổi** — artifact lifecycle và package lifecycle là hai trục tách biệt.

**Package lifecycle states (pinned tại transaction này):**

```text
Package 0.3-A:    Consolidated Stable
Package 0.3-B:    Unauthorized
Package 0.3-C:    Unauthorized
```

## Ngoài phạm vi Phase 0.3 — defer

- Package 0.3-B (Use Case & Workflow) — dependency đã thỏa (0.3-A `Consolidated Stable`), nhưng **CHƯA bắt đầu, CHƯA author, KHÔNG được authorize bởi transaction này** — cần Product Owner scope authorization riêng, tương tự cơ chế đã áp dụng cho mọi package Phase 0.2.
- Phase 0 DoD, Phase 0 Approval Gate work (thuộc [Chapter 12](../constitution/12-approval-gates.md), một transaction riêng, lớn hơn, sau khi 0.3-A/B/C đều `Consolidated Stable`).
- Phase 1 System/UX Architecture, API/Database/Engine design (`/docs/architecture/`, chưa bắt đầu).
- Concrete Product Metrics (`OQ-003`), Strategy Lifecycle Live-gate (`OQ-002`).

**Package 0.2-A/B/C vẫn `Consolidated Stable`, byte-for-byte không đổi.** Package 0.3-B/0.3-C vẫn `Unauthorized`. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.3 là sub-phase đang active; Phase 0 vẫn active và chưa hoàn tất; Phase 1 vẫn unauthorized.
