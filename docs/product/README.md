---
id: product-index
title: Product Requirement & UX Index
status: Draft
version: "0.8"
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
| **0.3-B — Use Case & Workflow** | [`use-case-workflow.md`](./use-case-workflow.md) v0.3 Draft — 21 Use Case (`UC-001`–`UC-021`), truy vết `PR-001`–`PR-034` | Draft — **`Consolidated Stable`** (xem dưới) |
| **0.3-C — UX Blueprint** | [`ux-blueprint.md`](./ux-blueprint.md) v0.5 Draft — 17 screen/view (`SCR-001`–`SCR-011`, `VIEW-001`–`VIEW-006`), 1 `WS-001`, 6 `NAV-001`–`NAV-006`, truy vết TRỰC TIẾP, materially bounded `UC-001`–`UC-021`/`PR-001`–`PR-034` (tất cả 34 PR có acceptance surface) | Draft — **Final mechanical traceability correction hoàn tất, chưa `Consolidated Stable`** — chờ ChatGPT mechanical final review |

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

## Package 0.3-B — Use Case & Workflow `Consolidated Stable`

**Phạm vi (scope tối thiểu, walking-skeleton):** dịch 34 requirement (`PR-001`–`PR-034`, Package 0.3-A `Consolidated Stable`) thành 21 Use Case cụ thể, testable, bounded (`UC-001`–`UC-021`) — 3 Research, 2 Replay, 5 Backtest, 5 Paper, 3 Review, 3 Improve — sở hữu user journey/use-case behavior/precondition/trigger/main flow/alternate flow/observable outcome/handoff cho sáu-giai-đoạn lifecycle. KHÔNG tạo product requirement mới — mọi Use Case truy vết `PR-XXX` đã tồn tại. Preserve nguyên vẹn Replay authority boundary (historical reconstruction vs parity recomputation, không `ReplayDecision`) và Backtest authority boundary (không tái sử dụng PAPER fact, không entity Backtest mới) từ `product-requirement.md` v0.2.

**v0.2 — bounded correction (đóng consolidated Review A + Independent Review B findings, hai Major + năm Minor):** (1) `P03B-MAJ-01` — Backtest→Paper handoff + UC-011 viết lại: Backtest/Research Decision identity KHÔNG BAO GIỜ carry-forward/promote/reuse làm PAPER Decision ancestor; PAPER entry đòi hỏi PAPER-context authoritative Decision lineage RIÊNG BIỆT; cơ chế thiết lập chính xác là deferred dependency (§9d); workflow dừng TRƯỚC PAPER execution khi thiếu lineage eligible. (2) `P03B-MAJ-02` — UC-020 viết lại tách bạch Backtest comparison (non-PAPER authority) khỏi PAPER comparison (authoritative); cross-mode CHỈ juxtaposition, KHÔNG unified outcome fact/normalization/scoring chung. (3) `P03B-MIN-01` — UC-011 reframe "Initiate PAPER execution" thay vì "Submit Order." (4) `P03B-MIN-02` — UC-021 thêm bounded alternate/failure khi evidence không khả dụng, bỏ overclaim "luôn khả dụng." (5) `P03B-MIN-03` — UC-007 bỏ ngôn ngữ "đã bị loại bỏ," thay bằng "run identity không resolve được" + bốn nguyên tắc fallback. (6) `P03B-MIN-04` — UC-020 khôi phục traceability đầy đủ `PR-031`/`PR-032`. (7) `P03B-MIN-05` — UC-003 thêm observable outcome PASSED/FAILED/INDETERMINATE, không tạo entity "ResearchVerification."

**v0.3 — narrow delta correction (đóng `P03B-DELTA-MIN-01`):** UC-021 trước đây CHỈ operationalize Decision fact lịch sử dù Goal/UC-020 dependency đòi hỏi phạm vi rộng hơn. Viết lại đầy đủ: UC-021 nay resolve ĐỘC LẬP, tách bạch, CẢ HAI họ evidence lịch sử cho một Strategy Definition Version cũ — **Backtest evidence family** (Decision/RiskEvaluation trace, simulated economic evidence, exposure/position progression, strategy-level evaluable result, run identity/version/configuration context, non-PAPER authority) VÀ **PAPER evidence family** (Decision, Trade Intent, RiskEvaluation, Execution Intent, Order, OrderSubmissionRequest, ExecutionResult, Fill, Position, authoritative, với ExecutionResultComputation/PaperExecutionObservation làm supporting evidence khi cần). Danh tính version LUÔN hiển thị; missing evidence identify theo TỪNG họ/loại, KHÔNG ngụ ý toàn bộ lịch sử mất khi một phần thiếu. UC-020 cập nhật tương ứng — KHÔNG ngụ ý UC-021 trả về một cross-mode evidence object chung.

**KHÔNG author:** screen layout/wireframe/component hierarchy (Package 0.3-C, chưa author); Domain Contract semantic/state machine mới; Backtest/Replay domain fact mới; API/database/backend/frontend/infrastructure architecture; security/custody/deployment; Product Metric threshold (`OQ-003`); Live-gate criteria (`OQ-002`); mở rộng multi-tenant/đa tài sản; unified Backtest/PAPER outcome model; PAPER Decision-generation semantics mới; retention/archival/retrieval/storage architecture; Research verification domain entity/event; unified old-version evidence aggregate; evidence availability SLA.

**Trạng thái review:**

- Author self-review (authoring, v0.1): **hoàn tất.**
- ChatGPT Review A + Independent Review B (baseline v0.1): **hoàn tất** — hai Major + năm Minor finding (`P03B-MAJ-01`/`P03B-MAJ-02`/`P03B-MIN-01`–`P03B-MIN-05`) consolidated.
- Bounded correction commit (v0.1 → v0.2), Product Owner authorized: **hoàn tất** — đóng toàn bộ bảy finding.
- ChatGPT Delta Review A + Independent Delta Review B (trên v0.2): **hoàn tất** — một Minor finding delta (`P03B-DELTA-MIN-01`, UC-021 scope mismatch) consolidated.
- Narrow delta correction commit (v0.2 → v0.3), Product Owner authorized: **hoàn tất** — đóng `P03B-DELTA-MIN-01`.
- ChatGPT second Delta Review A (trên v0.3): **Clean** — 0 blocking finding.
- Independent second Delta Review B (trên v0.3): **Clean** — 0 blocking finding.
- Consolidation: **hoàn tất (transaction này)** — Product Owner authorized: "Package 0.3-B — Use Case & Workflow: Consolidated Stable". **Package 0.3-B nay `Consolidated Stable`.**

**Kết luận consolidation:** ChatGPT second Delta Review A (Clean) và Independent second Delta Review B (Clean) trên `use-case-workflow.md` v0.3, **0 finding còn lại chưa xử lý** (finding ledger đầy đủ — hai Major + năm Minor qua bounded correction v0.1→v0.2, một Minor qua narrow delta correction v0.2→v0.3, tại mục baseline dưới đây). Product Owner authorized: "Package 0.3-B — Use Case & Workflow: Consolidated Stable".

## `Consolidated Stable` baseline — Package 0.3-B

**Exact reviewed artifact baseline (pinned):**

```text
use-case-workflow.md   v0.3   Draft   blob affbb723b577cde4c8627dd689550e3bfbffb5d1
product/README.md      v0.6   Draft   blob 9e69e5fa98afda60592c376fe1a341007d267c0b (pre-consolidation)
consolidated baseline HEAD:  73b100f9854864f53bc7c4f86261db9c2aab8e0c
```

**Finding ledger — tất cả resolved qua bounded correction (v0.1 → v0.2) và narrow delta correction (v0.2 → v0.3):**

```text
P03B-MAJ-01        — Resolved (Backtest→Paper handoff + UC-011 — PAPER-context authoritative Decision
                      lineage riêng biệt bắt buộc, Backtest/Research Decision không carry-forward)
P03B-MAJ-02        — Resolved (UC-020 tách bạch Backtest comparison non-PAPER authority khỏi PAPER
                      comparison authoritative, cross-mode chỉ juxtaposition)
P03B-MIN-01        — Resolved (UC-011 reframe "Initiate PAPER execution")
P03B-MIN-02        — Resolved (UC-021 bounded alternate/failure khi evidence không khả dụng)
P03B-MIN-03        — Resolved (UC-007 bỏ ngôn ngữ deletion lifecycle)
P03B-MIN-04        — Resolved (UC-020 khôi phục traceability PR-031/PR-032)
P03B-MIN-05        — Resolved (UC-003 observable outcome PASSED/FAILED/INDETERMINATE)
P03B-DELTA-MIN-01  — Resolved (UC-021 viết lại đầy đủ, resolve độc lập cả Backtest VÀ PAPER evidence
                      family cho old-version evidence, UC-020 cập nhật tương ứng)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

**`Consolidated Stable` là package lifecycle/readiness state — KHÔNG phải document approval status**, đúng định nghĩa đã khóa cho mọi package trước đó: authoring + bounded correction + narrow delta correction hoàn tất cho phạm vi 0.3-B; ChatGPT second Delta Review A hoàn tất (Clean); Independent second Delta Review B hoàn tất (Clean); mọi qualifying finding đã xử lý; artifact đã review được pin chính xác; package đủ ổn định để Package 0.3-C (UX Blueprint) bắt đầu planning — **không** ngụ ý Product Owner Approval cho `use-case-workflow.md`, **không** ngụ ý Lock, **không** authorize Package 0.3-C tự động, **không** đóng OQ-002/OQ-003, **không** authorize Live, **không** tuyên bố Phase 0.3 hoàn thành. `use-case-workflow.md` **vẫn giữ `version: "0.3"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte không đổi** — artifact lifecycle và package lifecycle là hai trục tách biệt.

**Package lifecycle states (pinned tại transaction này):**

```text
Package 0.3-A:    Consolidated Stable
Package 0.3-B:    Consolidated Stable
Package 0.3-C:    Unauthorized
```

## Package 0.3-C — UX Blueprint (final mechanical traceability correction, v0.5)

**Phạm vi (scope tối thiểu, walking-skeleton):** dịch 21 Use Case (`UC-001`–`UC-021`, Package 0.3-B `Consolidated Stable`) thành 17 screen/view (11 `SCR`, 6 `VIEW`), 1 workspace shell (`WS-001`), 6 navigation destination (`NAV-001`–`NAV-006`), 6 interaction flow (`FLOW-001`–`FLOW-006`), 29 presentation state (`STATE-001`–`STATE-029`) — bao trùm đầy đủ sáu-giai-đoạn lifecycle. KHÔNG tạo product requirement/use case mới — mọi UX element truy vết TRỰC TIẾP, materially bounded `UC-XXX` VÀ `PR-XXX` đã tồn tại. Đủ chi tiết cho Figma-level prototype VÀ Phase 1 architecture, KHÔNG pixel/branding/component code/API/database.

**Preserve nguyên vẹn:** Replay authority (historical reconstruction mặc định vs parity recomputation tuỳ chọn, `canonical semantic-decision hash`, không `ReplayDecision`); Backtest authority (non-PAPER simulated, không tái sử dụng PAPER fact, không entity Backtest mới); Paper user/system authority (user initiate intent, system sở hữu Trade Intent→...→Position); cross-mode comparison tách biệt (không unified outcome); Research verification tri-state (PASSED/FAILED/INDETERMINATE); old-version evidence hai họ độc lập — tất cả từ `use-case-workflow.md` v0.3.

**KHÔNG author:** pixel dimension/visual branding/exact color/font/production component code/CSS/frontend framework; API contract/database query/backend service/event transport/deployment topology; security/custody/deployment; retention/archive/storage architecture; multi-tenant administration/organization switching/public profile/community/signal marketplace/multi-asset UX/Live execution UX; Domain Contract state/authority/cardinality/transition mới; Backtest/Replay/Research domain fact mới; unified Backtest/PAPER outcome model; automatic normalization/scoring/ranking; product requirement hay Use Case mới.

**Trạng thái review:**

- Author self-review (authoring, v0.1): **hoàn tất.**
- ChatGPT Review A (v0.1 baseline): **hoàn tất** — findings `P03C-MAJ-01`/`P03C-MIN-01`/`P03C-MIN-02`/`P03C-MIN-03`.
- Independent Review B (v0.1 baseline): **hoàn tất** — findings `P03C-B-MAJ-01`/`P03C-B-MAJ-02` (subsumed vào `P03C-MAJ-01` traceability overhaul).
- Bounded correction (v0.2): **hoàn tất** — đóng toàn bộ sáu finding (`P03C-MAJ-01`, `P03C-B-MAJ-01`, `P03C-B-MAJ-02`, `P03C-MIN-01`, `P03C-MIN-02`, `P03C-MIN-03`); gửi ChatGPT/Independent Review B delta review.
- Delta review (v0.2): **hoàn tất** — xác nhận v0.2 traceability syntactically exhaustive nhưng materially overbroad (`P03C-MAJ-01`/`P03C-B-MAJ-01`/`P03C-B-MAJ-02` chưa đóng đầy đủ); Paper Strategy Instance binding chưa đầy đủ (`P03C-B-MAJ-01`); Strategy Instance creation UX thiếu first-class view (`P03C-B-MAJ-02`).
- Final narrowly bounded correction (v0.3): **hoàn tất** — đóng `P03C-MAJ-01`/`P03C-B-MAJ-01`/`P03C-B-MAJ-02`; gửi ChatGPT Final Delta Review A/Independent Review B.
- Delta review (v0.3): **hoàn tất** — xác nhận `P03C-B-MAJ-01`/`P03C-B-MAJ-02` đóng đầy đủ; `P03C-MAJ-01` chưa đóng hoàn toàn — traceability v0.3 vẫn giữ một số mapping chỉ vì parent screen sở hữu PR đó (chưa materially bounded triệt để) và ba PR (`PR-004`/`PR-005`/`PR-014`) chưa gán acceptance surface thực tế.
- Final traceability-only correction (v0.4): **hoàn tất** — đóng `P03C-MAJ-01`; gửi ChatGPT Traceability Delta Review A/Independent Review B.
- Delta review (v0.4): **hoàn tất** — xác nhận `P03C-MAJ-01` gần như đóng; hai mapping không hợp lệ còn sót tại `STATE-002` (`PR-007`, `PR-032`).
- Final mechanical traceability correction (v0.5): **hoàn tất** — loại bỏ `PR-007 → STATE-002` và `PR-032 → STATE-002`; đóng `P03C-MAJ-01`; gửi ChatGPT mechanical final review.
- Consolidation: **chưa bắt đầu** — Package 0.3-C **CHƯA** đạt `Consolidated Stable`, chờ delta review Clean cả hai phía.

**Không tuyên bố hoàn thành hay approval nào (mục 0.3-C):** `ux-blueprint.md` `status: Draft`, `version: "0.5"`, `approved_by: null`, `approved_at: null`; không Product Owner Approve; không Lock; không Consolidate; không đóng `OQ-002`/`OQ-003`; không authorize Live; không sửa `product-requirement.md`/`use-case-workflow.md`/Domain Contract/ADR/Constitution/architecture nào; Package 0.3-A/0.3-B vẫn `Consolidated Stable`, không đổi.

## Ngoài phạm vi Phase 0.3 — defer

- Phase 0 DoD, Phase 0 Approval Gate work (thuộc [Chapter 12](../constitution/12-approval-gates.md), một transaction riêng, lớn hơn, sau khi 0.3-A/B/C đều `Consolidated Stable`).
- Phase 1 System/UX Architecture, API/Database/Engine design (`/docs/architecture/`, chưa bắt đầu) — `ux-blueprint.md` §18 pin handoff requirement cho Phase 1, KHÔNG tự author architecture.
- Concrete Product Metrics (`OQ-003`), Strategy Lifecycle Live-gate (`OQ-002`).

**Package 0.2-A/B/C vẫn `Consolidated Stable`, byte-for-byte không đổi. Package 0.3-A/0.3-B vẫn `Consolidated Stable`, byte-for-byte không đổi.** Package 0.3-C: final mechanical traceability correction v0.5 hoàn tất, chưa `Consolidated Stable`. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.3 là sub-phase đang active; Phase 0 vẫn active và chưa hoàn tất; Phase 1 vẫn unauthorized.
