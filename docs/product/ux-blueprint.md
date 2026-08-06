---
id: ux-blueprint
title: UX Blueprint
version: "0.7"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-02"
last_review: null
next_review: null
---

# UX Blueprint

> **Vai trò của tài liệu này:** Artifact thứ ba và cuối cùng của Package 0.3-C (Phase 0.3 — Product Requirement · Use Case & Workflow · UX Blueprint), phụ thuộc trực tiếp [`product-requirement.md`](./product-requirement.md) v0.2 Draft (Package 0.3-A, `Consolidated Stable`) VÀ [`use-case-workflow.md`](./use-case-workflow.md) v0.3 Draft (Package 0.3-B, `Consolidated Stable`). Dịch 21 Use Case (`UC-001`–`UC-021`) thành UX representation — workspace, navigation, screen, view, panel, flow, action, state, handoff — cho hành vi ĐÃ được `product-requirement.md`/`use-case-workflow.md` kiểm soát. Draft, chưa Approved/Locked, **`Consolidated Stable`**. Tài liệu này KHÔNG tạo product behavior/requirement/domain semantics mới — MỌI workspace/navigation item/screen/view/panel/flow/action/state/handoff PHẢI truy vết về một hoặc nhiều `UC-XXX` VÀ một hoặc nhiều `PR-XXX` đã tồn tại. KHÔNG sở hữu pixel dimension/visual branding/production component code (Phase 1 Figma-level prototype); KHÔNG sở hữu domain semantics (thuộc `/docs/domain/`, không sửa); KHÔNG sở hữu architecture (Phase 1, `/docs/architecture/`).

**Authority boundary:** tài liệu này sở hữu **UX representation content** cho Phase 0.3 — KHÔNG sở hữu product requirement content (thuộc `product-requirement.md`, Package 0.3-A, không sửa), KHÔNG sở hữu use-case/workflow content (thuộc `use-case-workflow.md`, Package 0.3-B, không sửa), KHÔNG sở hữu domain semantics/state machine/authority/cardinality/transition (thuộc `/docs/domain/`, không sửa/redefine), KHÔNG sở hữu architecture quyết định (Phase 1, `/docs/architecture/`), KHÔNG đóng Open Question nào (`OQ-002`/`OQ-003` vẫn `Open`, xem §15), KHÔNG authorize Live, KHÔNG tuyên bố Phase 0.3/Phase 0 hoàn thành, KHÔNG mark chính nó `Consolidated Stable`.

**Quy tắc traceability nguồn (kế thừa nguyên vẹn `product-requirement.md`/`use-case-workflow.md`):** mọi UX element PHẢI có một hoặc nhiều `UC-XXX` VÀ một hoặc nhiều `PR-XXX` áp dụng. Không nơi nào một UX element tồn tại chỉ vì "seems useful." Nơi KHÔNG có `UC`/`PR` nào authorize hành vi: (a) KHÔNG thêm nó, HOẶC (b) đánh dấu tường minh như một deferred dependency (§15) — KHÔNG BAO GIỜ tự phát minh. KHÔNG `UC-XXX`/`PR-XXX` ID mới nào được tạo tại đây.

**F-06 lifecycle-axis correction (2026-08-03, Phase 0 Exit Readiness Audit MAJOR finding):** một transaction trước đó (Package 0.3-C stabilization) đã populate `approved_by: Product Owner`/`approved_at: "2026-08-03"` trong khi `status` vẫn `Draft` — tổ hợp KHÔNG được định nghĩa tại Chapter 0 Document Lifecycle (§7.1: `approved_by`/`approved_at` populate tại `Approved`, KHÔNG phải `Draft`). Đây là **lỗi conflate hai trục lifecycle tách biệt** (package lifecycle `Consolidated Stable` vs. artifact lifecycle `Draft`/`Approved`/`Locked`) — KHÔNG phải một withdrawal của Package 0.3-C consolidation. Sửa: `approved_by`/`approved_at` reset về `null` (khớp `status: Draft`); `version`/`status`/UX semantics/traceability/stable ID **KHÔNG đổi**. Package 0.3-C **vẫn `Consolidated Stable`** (package lifecycle, không đổi) — hai trục nay tách biệt tường minh trở lại, đúng pattern đã dùng nhất quán cho `product-requirement.md`/`use-case-workflow.md` (`approved_by: null` dù package đã `Consolidated Stable`).

**v0.2 — bounded correction, đóng `P03C-MAJ-01`/`P03C-B-MAJ-01`/`P03C-B-MAJ-02`/`P03C-MIN-01`/`P03C-MIN-02`/`P03C-MIN-03` (2026-08-03):** (1) mọi `WS-XXX`/`NAV-XXX`/`SCR-XXX`/`VIEW-XXX`/`FLOW-XXX`/`STATE-XXX` ID nay truy vết TRỰC TIẾP một hoặc nhiều `UC-XXX` VÀ một hoặc nhiều `PR-XXX` tường minh (KHÔNG còn "cross-cutting"/"mọi UC" không liệt kê) — §5, §5a, §7 (SCR-006/SCR-007 bổ sung `PR-001`/`PR-006`/`PR-013`), §8 (mọi `FLOW-XXX` thêm field `UC traceability`/`PR traceability` riêng), §11 (mọi `STATE-XXX` thêm cột `UC traceability`), §14 (bảy ma trận trực tiếp bắt buộc); (2) thêm §5a — sáu đặc tả `NAV-001`–`NAV-006` first-class; (3) sửa `FLOW-001`/§4: quan sát market-analysis (`SCR-001`) KHÔNG còn phụ thuộc chọn Strategy Instance trước — `VIEW-001`/`VIEW-002` chỉ là commit-gate TRƯỚC `SCR-002`/`SCR-003`, KHÔNG phải entry-prerequisite của `SCR-001`; (4) thêm `UX-P-5` (§3) — phân tách read-only inspection navigation vs. authoritative progression/action, áp dụng tường minh cho outcome PASSED/FAILED/INDETERMINATE của Research verification (`VIEW-002`). KHÔNG PR/UC mới nào được tạo; KHÔNG behavior domain nào đổi; Package 0.3-C vẫn `Draft`, chưa `Consolidated Stable`.

**v0.3 — final narrowly bounded correction, đóng `P03C-MAJ-01`/`P03C-B-MAJ-01`/`P03C-B-MAJ-02` (2026-08-03):** (1) traceability v0.2 syntactically exhaustive nhưng materially overbroad — thu hẹp: `WS-001` (§5) từ union gần-toàn-bộ xuống ĐÚNG 5 item shell thực sự sở hữu (bỏ "Lifecycle-stage navigation bar"/"Evidence-authority labels"/"Blocked-state presentation" khỏi bảng trace — các item đó thuộc `NAV-XXX`/từng `SCR`/`VIEW`/`STATE-XXX` riêng, KHÔNG phải WS-001); `STATE-001` loading thu hẹp còn ĐÚNG `SCR-001`/`SCR-002`/`SCR-003` (ba screen duy nhất tường minh ghi "STATE-001" tại Primary states, KHÔNG còn 16); `STATE-002` empty thu hẹp còn ĐÚNG bốn genuine empty-collection screen (`SCR-004`/`SCR-005`/`SCR-007`/`SCR-011`, bỏ `SCR-003`/`SCR-008`/`SCR-009` — unfilled-form/không-genuinely-empty); `FLOW-001` PR traceability thu hẹp còn ĐÚNG 7 PR biểu diễn stage-ordering/gate/handoff (giữ UC-001–021 vì FLOW-001 chính là primary journey); §14 rebuilt lại theo union đã thu hẹp, thêm traceability-quality rule tường minh. (2) `P03C-B-MAJ-01` — Paper Strategy Instance binding: mở rộng `UX-INV-3` (§3) áp dụng pin cho Replay/Backtest/Paper (KHÔNG chỉ Research); `VIEW-001` hỗ trợ pin cho Paper; `SCR-006`/`SCR-007` hiển thị tường minh danh tính Strategy Instance/Version pin trước khi resolve PAPER Decision lineage và xuyên suốt C7 inspection; định nghĩa ranh giới UX-visible start/active/end của Paper pin (KHÔNG PaperSession entity/session/storage/timeout); thêm `STATE-028`/`STATE-029` phân biệt bốn nguyên nhân Paper blocked; `NAV-004` cập nhật tương ứng. (3) `P03C-B-MAJ-02` — thêm `VIEW-006` Strategy Instance Creation/Binding (first-class, 6 `VIEW`, 17 screen/view tổng, đóng `UC-019`→`VIEW-006`→`UC-002` handoff); sửa `VIEW-001` (KHÔNG tự tạo Instance), `SCR-010` exits, `FLOW-006`, cross-stage handoff Improve→Research (§9) đồng nhất. KHÔNG PR/UC mới; KHÔNG `PaperSession`/permission architecture/schema mới; Package 0.3-C vẫn `Draft`, chưa `Consolidated Stable`.

**v0.4 — final traceability-only correction, đóng `P03C-MAJ-01` (2026-08-03, KHÔNG behavior change):** review độc lập từng PR còn lại tại `STATE-001`/`STATE-002` sau v0.3 và loại bỏ mọi mapping chỉ giữ vì "parent screen sở hữu PR đó" thay vì vì chính state materially kiểm soát/hiển thị nó. `STATE-001` (loading) thu hẹp từ 9 PR xuống 2 (`PR-003`, `PR-018` — required context retained trong lúc pending); `STATE-002` (empty) thu hẹp từ 13 PR xuống 4 (`PR-007`, `PR-021`, `PR-032`, `PR-034` — absence/minimum-count/comparison-availability/non-fabrication). Gán `PR-004`/`PR-005`/`PR-014` (trước đây "không có UX acceptance surface") vào đúng SCR nào MATERIALLY hiển thị chúng: `PR-004`/`PR-005` → `SCR-004`/`SCR-006`/`SCR-008` (Decision outcome + evidence trace hiển thị tường minh); `PR-014` → `SCR-006`/`SCR-007`/`STATE-012`–`STATE-021` (explicit Risk/ExecutionResult/Position lifecycle-transition presentation). Sau v0.4, tất cả 34 PR có ít nhất một acceptance surface direct. §14 (bảy ma trận) rebuilt tương ứng. KHÔNG UX behavior/navigation/flow/state/authority/lifecycle semantics nào đổi; KHÔNG stable ID nào thêm/bớt/đổi tên; mọi finding đã resolved trước đó (`P03C-B-MAJ-01`/`P03C-B-MAJ-02`/`P03C-MIN-01`/`P03C-MIN-02`/`P03C-MIN-03`) giữ nguyên. Package 0.3-C vẫn `Draft`, chưa `Consolidated Stable`.

**v0.5 — final mechanical traceability correction, đóng `P03C-MAJ-01` (2026-08-03, KHÔNG behavior change):** loại bỏ đúng hai mapping không hợp lệ còn sót lại tại `STATE-002` sau v0.4: `PR-007 → STATE-002` và `PR-032 → STATE-002`. `PR-007`'s acceptance evidence "với NOT_EXECUTED, người dùng thấy rõ zero Fill" mô tả outcome của MỘT Order đã tồn tại (đã sở hữu bởi `STATE-016`/`STATE-017`), KHÔNG phải trường hợp "chưa Order/Fill nào tồn tại" mà `STATE-002` tại SCR-007 đại diện. `PR-032` governs truy vấn outcome xuyên suốt Strategy Definition Version CŨ (đã sở hữu bởi `VIEW-005`/`STATE-025`/`STATE-026`/`NAV-006`/`FLOW-005`/`FLOW-006`), KHÔNG phải minimum-record-count của Strategy Instance hiện tại để so sánh tại SCR-011. `STATE-002` PR traceability nay ĐÚNG `PR-021`, `PR-034` — UC traceability (`UC-007`/`UC-008`/`UC-009`/`UC-010`/`UC-012`/`UC-013`/`UC-014`/`UC-015`/`UC-020`) và applicable screens (`SCR-004`/`SCR-005`/`SCR-007`/`SCR-011`) KHÔNG đổi. `PR-007` và `PR-032` giữ nguyên toàn bộ acceptance surface hợp lệ khác (`PR-007`: `SCR-006`/`SCR-007`/`FLOW-004`/`STATE-015`/`STATE-016`; `PR-032`: `NAV-006`/`SCR-011`/`VIEW-005`/`FLOW-005`/`FLOW-006`/`STATE-025`/`STATE-026`). §14 (STATE→UC/PR, PR→UX) cập nhật tương ứng. KHÔNG UX behavior/navigation/flow/state/authority/lifecycle semantics nào đổi; KHÔNG stable ID nào thêm/bớt/đổi tên; mọi finding đã resolved trước đó giữ nguyên. Package 0.3-C vẫn `Draft`, chưa `Consolidated Stable`.

**v0.6 — CANDIDATE semantic clarification (2026-08-06), KHÔNG Approved/Consolidated, pending Review A/Independent Review B/Product Owner decision — Product Owner authorized (timestamp 2026-08-06T09:21:00+07:00) bounded source-semantics clarification cho VIEW-003 replay parity verification:** `use-case-workflow.md` v0.7 (CANDIDATE) thêm một outcome workflow-visible thứ ba cho `UC-005` — **INDETERMINATE** — bên cạnh match/mismatch đã có, dùng khi parity recomputation evidence thiếu/stale/invalidated/ambiguous/non-evaluable (`decision.md` §9a.6, CANDIDATE cùng transaction). `VIEW-003` (§7 spec block) trước đây CHỈ resolve về hai state (`STATE-007` parity match, `STATE-008` parity mismatch) — KHÔNG đủ để biểu diễn outcome thứ ba này. Nay THÊM một stable state identifier MỚI — **`STATE-030` — parity indeterminate** — vào catalogue §13 (29 → 30 trạng thái). Đây là **Product/UX semantic candidate requiring review**, KHÔNG phải mechanical/cosmetic — mở rộng catalogue acceptance-surface identifier, do đó đóng vai trò input bắt buộc cho Review A/Independent Review B trước khi coi `STATE-030` là Consolidated. `VIEW-003` "Information displayed"/"Evidence consumed"/"Primary states"/"Empty-unavailable-blocked states" cập nhật để phản ánh ba outcome; §14e (STATE→UC/PR)/§14f (UC→UX)/§14g (PR→UX) cập nhật đồng bộ để thêm `STATE-030`. KHÔNG stable ID nào khác thêm/bớt/đổi tên; KHÔNG screen/nav/flow mới; `NAV-003`/`VIEW-002` giữ nguyên unresolved; KHÔNG chọn computation owner/module/package/dependency edge/ADR; KHÔNG Approve/Lock/Consolidate.

**v0.7 — CANDIDATE bounded correction (2026-08-06), KHÔNG Approved/Consolidated, pending bounded verification/Independent Review B/Product Owner decision — đóng bốn Review A finding trên `decision.md` §9a v0.4 (`P16-V003-A-MAJ-01`/`P16-V003-A-MAJ-02`/`P16-V003-A-MAJ-03`/`P16-V003-A-MIN-01`, xem `decision.md` v0.5):** `VIEW-003` §7 spec block wording cập nhật — INDETERMINATE (`STATE-030`, vẫn CANDIDATE — 29→30 catalogue amendment KHÔNG đổi bởi correction này) nay tường minh bao gồm trường hợp implementation identity (`decision_implementation_version`) established tại recorded Decision nhưng không resolve/reproduce được ở một phía, và trường hợp digest-definition (khi dùng digest) unresolved/incompatible. KHÔNG thêm state/screen/view/flow/action mới; KHÔNG đổi ba-outcome model (MATCH/MISMATCH/INDETERMINATE); §14e/§14f/§14g KHÔNG đổi (đã có `STATE-030` từ v0.6). `NAV-003`/`VIEW-002` giữ nguyên unresolved. KHÔNG chọn computation owner/module/package/dependency edge/ADR; KHÔNG redesign VIEW-003; KHÔNG Approve/Lock/Consolidate.

## 1. Purpose and authority boundary

Tài liệu này trả lời: **"Với 21 Use Case đã `Consolidated Stable` tại Package 0.3-B, người dùng nội bộ THỰC SỰ nhìn thấy gì, điều hướng ra sao, và tương tác qua screen/view/action cụ thể nào?"** — ở mức **UX representation** (đủ chi tiết cho Figma-level prototype VÀ Phase 1 architecture hiểu được), KHÔNG ở mức pixel/branding/component code/API/database/backend. Là điểm tiêu thụ CUỐI của Phase 0.3 — KHÔNG package nào phụ thuộc Package 0.3-C.

## 2. Approved actor and operating context

Kế thừa nguyên vẹn `use-case-workflow.md` §2 (KHÔNG đổi):

```text
Primary actor:  "Ride user" — một actor DUY NHẤT, thành viên nội bộ workspace (UC-001–UC-021).

Operating context (walking-skeleton, PRESERVE CHÍNH XÁC):
  internal team                  (ADR-007)
  single workspace                (một Account vận hành thực tế)
  one Account currently operated  (Account first-class, PR-002)
  crypto-only                     (ADR-007)
  2–3 exchanges                   (ADR-007, PR-003)

KHÔNG giới thiệu: multi-tenant administration; organization switching; public profile; community/
chat; signal marketplace; multi-asset UX; Live execution UX.
```

## 3. UX principles and invariants

Mười invariant dưới đây restate nguyên vẹn `WF-INV-1`–`WF-INV-10` (`use-case-workflow.md` §3) ở mức UX — KHÔNG tạo yêu cầu mới, áp dụng xuyên suốt MỌI screen/view tại §7:

```text
UX-INV-1   Mọi screen luôn hiển thị Account context của workspace (một Account duy nhất).   (WF-INV-1)
UX-INV-2   Mọi Instrument/Venue selector CHỈ liệt kê TradableListing đã đăng ký.               (WF-INV-2)
UX-INV-3   Strategy Instance context, một khi pin cho phiên Replay/Backtest/Paper, hiển
           thị READ-ONLY (không đổi giữa chừng) cho tới khi phiên kết thúc. Quan sát Research
           (SCR-001) KHÔNG yêu cầu pin trước (§4/§8 FLOW-001).                                  (WF-INV-3)
UX-INV-4   Mọi Decision/Risk Action hiển thị PHẢI kèm evidence trace truy cập được — KHÔNG
           giá trị "mồ côi" nguồn gốc.                                                         (WF-INV-4)
UX-INV-5   Mọi so sánh Decision semantic hiển thị nhãn `canonical semantic-decision hash` —
           KHÔNG BAO GIỜ nhãn "Decision hash" chung chung.                                     (WF-INV-5)
UX-INV-6   Mọi correction hiển thị CẢ fact gốc LẪN fact thay thế, có liên kết tường minh —
           KHÔNG BAO GIỜ chỉ hiển thị giá trị "đã sửa" ẩn nguồn gốc.                            (WF-INV-6)
UX-INV-7   Mọi historical cursor view hiển thị deterministic, gắn nhãn cursor tường minh.       (WF-INV-7)
UX-INV-8   Mọi giá trị tài chính hiển thị PHẢI khớp byte-for-byte giá trị đã ghi nhận — KHÔNG
           làm tròn/format sai lệch giá trị gốc.                                               (WF-INV-8)
UX-INV-9   Mọi trạng thái lifecycle hiển thị PHẢI ánh xạ đúng một authoritative domain state
           — UX state (§11) là presentation-only, KHÔNG tạo domain state mới.                  (WF-INV-9)
UX-INV-10  KHÔNG action/screen/label nào ngụ ý Live — Live luôn hiển thị `Unauthorized`.        (WF-INV-10)
```

**Paper Strategy Instance binding contract (v0.3 — mở rộng UX-INV-3, đóng `P03C-B-MAJ-01`):**

```text
Trước khi bounded Replay/Backtest/Paper behavior bắt đầu:
  đúng một Strategy Instance đã được chọn và pin (qua VIEW-001).

Trong khi bounded interaction đó còn active:
  pin hiển thị tường minh;
  pin READ-ONLY (không đổi giữa chừng);
  Strategy Definition Version identity vẫn hiển thị cạnh pin.

Sau khi bounded interaction đó kết thúc:
  một Strategy Instance KHÁC có thể được chọn cho một bounded interaction sau đó.

Research quan sát thuần tuý (SCR-001) KHÔNG yêu cầu pin — chỉ Replay/Backtest/Paper (bounded, tạo
authoritative/simulated fact) mới yêu cầu.

Ranh giới UX-visible của Paper pin cụ thể (KHÔNG PaperSession entity/session identifier/storage/
timeout/persistence mechanism/backend lifecycle nào được định nghĩa):

  start:   ngay sau khi VIEW-001 hoàn tất chọn/pin cho Paper — TRƯỚC khi SCR-006 resolve PAPER-context
           Decision lineage.
  active:  xuyên suốt khởi tạo, RiskEvaluation, execution observation, ExecutionResult, Fill, Position
           inspection tại SCR-006/SCR-007.
  end:     khi người dùng thoát bounded Paper interaction và không còn Paper initiation/execution
           detail nào active.
  sau end: một bounded Paper interaction sau đó có thể chọn/pin một Strategy Instance đã đăng ký KHÁC.
```

**Bổ sung UX-specific (không phải PR restatement, mà nguyên tắc trình bày thuần UX, áp dụng nhất quán):**

```text
UX-P-1  Mọi evidence hiển thị PHẢI mang nhãn mode (Research/Replay/Backtest/Paper) VÀ authority
        (authoritative / non-authoritative simulated / non-authoritative recomputation) — không có
        evidence "vô danh" nguồn.
UX-P-2  Mọi hành động người dùng có thể khởi xướng (user action) PHẢI phân biệt trực quan với hành
        vi hệ thống tự động thực hiện (system-owned action) — đặc biệt tại Paper (§7 SCR-006).
UX-P-3  Mọi trạng thái "không khả dụng"/"blocked"/"insufficient" PHẢI disclose lý do — KHÔNG màn
        hình trống không giải thích.
UX-P-4  Không UI nào ngụ ý một domain entity/event chưa tồn tại (BacktestOrder, ReplayDecision,
        ResearchVerification, unified outcome, v.v.) — mọi wording dùng thuật ngữ mô tả
        (descriptive), KHÔNG thuật ngữ domain đã đóng đinh chưa được authorize.
UX-P-5  Read-only inspection navigation LUÔN được phân tách tường minh khỏi authoritative
        progression/action (v0.2, đóng `P03C-MIN-02`):
          Read-only inspection navigation:  điều hướng tới một destination CHỈ để xem evidence/
                                             context/empty state/blocked reason đã tồn tại — LUÔN
                                             khả dụng khi destination có thể hiển thị an toàn thứ đó,
                                             KỂ CẢ khi một upstream verification/guard chưa PASSED.
          Authoritative progression/action: hành động tạo/khởi tạo authoritative fact mới (tạo
                                             Backtest run, khởi tạo PAPER execution, v.v.) — LUÔN bị
                                             chặn khi upstream verification/required-authority guard
                                             chưa thoả (STATE-XXX blocked/failed liên quan).
        "Global navigation luôn hiển thị" KHÔNG có nghĩa: bypass verification; tạo Backtest run; khởi
        tạo PAPER execution; hoặc bất kỳ authoritative action nào khác. Người dùng có thể điều hướng
        tới một destination downstream để xem read-only hoặc thấy blocked state, nhưng KHÔNG hành
        động authoritative nào được phép cho tới khi guard thoả. Nguyên tắc này KHÔNG định nghĩa
        permission architecture/route guard/authorization middleware/session token — đó là Phase 1
        architecture concern, KHÔNG phải UX Blueprint.

        Áp dụng tường minh cho Research verification (VIEW-002, UC-003):
          PASSED:        cho phép tiến tới authoritative progression khác theo precondition riêng của
                          destination đó (VIEW-001 → VIEW-002 → SCR-002/SCR-003, §8 FLOW-001).
          FAILED:        Research KHÔNG coi là verified thành công — reason + fact bị ảnh hưởng vẫn
                          hiển thị (STATE-023); authoritative progression downstream (khởi tạo Backtest
                          run tại SCR-003, khởi tạo PAPER execution tại SCR-006) bị CHẶN. Người dùng
                          vẫn có thể điều hướng read-only tới SCR-002/SCR-003/SCR-006 để xem blocked
                          state.
          INDETERMINATE: Research KHÔNG coi là verified thành công — evidence thiếu/chưa resolve vẫn
                          hiển thị (STATE-024); authoritative progression downstream bị CHẶN tương tự
                          FAILED.
```

## 4. Information architecture

**Thứ tự entry của Research (v0.2, đóng `P03C-MIN-01`):** `SCR-001` là entry-first screen của `NAV-001` — quan sát market-analysis (UC-001) KHÔNG phụ thuộc Strategy Instance đã pin. `VIEW-001`/`VIEW-002` là commit-gate, CHỈ bắt buộc khi người dùng chuẩn bị chuyển sang `SCR-002`(Replay)/`SCR-003`(Backtest) — KHÔNG phải entry-prerequisite của `SCR-001` (xem FLOW-001, §8).

```text
Ride Workspace (WS-001)
│
├── Global context bar (Account · Instrument/Venue · Strategy Instance khi đã pin · historical cursor
│                        khi áp dụng)
│
├── NAV-001 Research
│     SCR-001 Market Analysis Workspace          (UC-001, entry-first — KHÔNG cần Strategy Instance)
│     VIEW-001 Strategy Instance Selector         (UC-002, commit-gate TRƯỚC Replay/Backtest, global
│                                                   panel truy cập được từ mọi stage)
│     VIEW-002 Research Verification Result       (UC-003, commit-gate, SAU VIEW-001, TRƯỚC SCR-002/
│                                                   SCR-003)
│
├── NAV-002 Replay
│     SCR-002 Replay Cursor & Historical Reconstruction   (UC-004)
│     VIEW-003 Parity Recomputation Result                 (UC-005)
│
├── NAV-003 Backtest
│     SCR-003 Backtest Run Setup                  (UC-006)
│     SCR-004 Backtest Run Detail                 (UC-007, UC-008, UC-009)
│     SCR-005 Backtest Run Comparison             (UC-010)
│
├── NAV-004 Paper
│     SCR-006 Paper Execution Initiation          (UC-011)
│     SCR-007 Paper Order/Execution Detail        (UC-012, UC-013, UC-014, UC-015)
│
├── NAV-005 Review
│     SCR-008 Decision → Position Lineage Trace   (UC-016)
│     SCR-009 Historical State Comparison         (UC-017)
│     VIEW-004 Correction Inspection               (UC-018)
│
└── NAV-006 Improve
      SCR-010 Strategy Definition Version Creation   (UC-019)
      VIEW-006 Strategy Instance Creation/Binding     (UC-019/UC-002, v0.3, đóng `P03C-B-MAJ-02`)
      SCR-011 Strategy Version Comparison             (UC-020)
      VIEW-005 Old-Version Evidence Access            (UC-021)
```

**VIEW-006 (v0.3, đóng `P03C-B-MAJ-02`):** SCR-010 tạo Strategy Definition Version mới; VIEW-006 là bounded product handoff để đăng ký một Strategy Instance RIÊNG BIỆT gắn version đó; VIEW-001 (§7.1) sau đó chọn/pin Instance vừa đăng ký. `SCR-010`/`UC-019` KHÔNG tự tạo Strategy Instance — VIEW-006 mới sở hữu hành vi đó (§7.6).

Thông tin kiến trúc này TRỰC TIẾP ánh xạ sáu-giai-đoạn (`use-case-workflow.md` §4) — KHÔNG thêm giai đoạn/workspace/navigation destination nào ngoài sáu giai đoạn đã `Consolidated Stable`.

## 5. Global workspace/navigation model

**WS-001 — Ride Workspace Shell (v0.3 — materially bounded mapping, đóng `P03C-MAJ-01`/`P03C-B-MAJ-01`/`P03C-B-MAJ-02`)**

WS-001 CHỈ sở hữu behavior thực sự thuộc về SHELL (container luôn hiển thị) — KHÔNG sở hữu behavior riêng của từng destination (đó thuộc `NAV-XXX`, §5a, và `SCR-XXX`/`VIEW-XXX`, §7). v0.3 thu hẹp bảng dưới đây từ union gần-toàn-bộ (v0.2) xuống ĐÚNG những item shell thực sự sở hữu/hiển thị — mỗi dòng chỉ cite UC/PR trực tiếp yêu cầu hoặc phụ thuộc vật chất vào context đó, KHÔNG dùng destination/transient-state/parent-journey làm fallback coverage cho requirement chưa có chỗ gắn.

| Item sở hữu bởi WS-001 | UC traceability | PR traceability |
|---|---|---|
| Current Account context (hiển thị READ-ONLY, một Account duy nhất, UX-INV-1; KHÔNG switcher — chưa UC/PR nào authorize) | UC-011 (duy nhất UC có "Account context hợp lệ" tường minh là required context tại §7 — SCR-006) | PR-002 |
| Instrument/Venue context (selector, giới hạn TradableListing đã đăng ký, UX-INV-2) | UC-001 (SCR-001 required context), UC-011 (SCR-006 required context) | PR-003 |
| Strategy Instance context (hiển thị pin READ-ONLY một khi đã chọn qua VIEW-001, UX-INV-3 — WS-001 CHỈ hiển thị, KHÔNG sở hữu hành vi chọn) | UC-002, UC-011 (Paper pin, v0.3, đóng `P03C-B-MAJ-01` — xem Paper Strategy Instance binding §3) | PR-001, PR-016 |
| Historical cursor context (hiển thị khi đang ở SCR-002/SCR-009 — canonical Replay Cursor value + effective historical context, §12) | UC-004, UC-017 | PR-008, PR-012, PR-029 |
| Live Unauthorized label (STATE-027, tĩnh, toàn cục) | UC-011, UC-015 | PR-027 |

**Item KHÔNG còn thuộc bảng trực tiếp của WS-001 (v0.3 — thu hẹp, đóng `P03C-MAJ-01`):**

```text
Lifecycle-stage navigation bar (sự tồn tại/thứ tự sáu NAV):
  Cấu trúc sáu-giai-đoạn kế thừa nguyên vẹn `product-requirement.md` §6/`use-case-workflow.md` §4 —
  KHÔNG một PR-XXX/UC-XXX riêng nào "sở hữu" chính sự tồn tại của thanh nav; hành vi điều hướng/
  blocked/read-only CỤ THỂ của từng destination sở hữu bởi NAV-001–NAV-006 (§5a, đã có UC/PR riêng
  đầy đủ). WS-001 không cần, và KHÔNG còn, tự nhận một UC/PR union giả cho item này.

Evidence/authority labels (mode/authority badge trên evidence):
  Nhãn này hiển thị BÊN TRONG nội dung từng SCR/VIEW (§7, field "Authority labels"), KHÔNG phải bởi
  chrome/container của shell — sở hữu bởi từng SCR/VIEW liên quan, KHÔNG bởi WS-001. UX-P-1 (§3) vẫn
  là nguyên tắc trình bày xuyên suốt, nhưng nguyên tắc trình bày KHÔNG tự động tạo material ownership
  của WS-001 với mọi UC hiển thị evidence.

Blocked/unavailable-state presentation (reason-disclosure nói chung):
  Mỗi `STATE-XXX` đã có UC/PR trực tiếp riêng tại §11 — WS-001 không cần, và KHÔNG còn, tự nhận một
  UC-001–UC-021 union giả cho nguyên tắc UX-P-3. WS-001 chỉ sở hữu duy nhất STATE-027 (Live
  Unauthorized, dòng cuối bảng trên) vì đó là nhãn TĨNH TOÀN CỤC render bởi chính shell, KHÔNG phải
  per-destination.
```

**Account-switching — tường minh KHÔNG thêm:** đúng chỉ dẫn "Do not add Account-switching behavior unless directly authorized" — chưa `UC-XXX`/`PR-XXX` nào authorize multi-Account UX; Account context tại đây CHỈ hiển thị (first-class, read-only), KHÔNG switcher.

**Giới hạn tường minh (v0.3):** WS-001 KHÔNG "sở hữu toàn bộ workflow behavior" — bảng trên CHỈ liệt kê phần tử thực sự render bởi shell container VÀ có UC/PR trực tiếp/materially-controlling. Behavior điều hướng/blocked/read-only cụ thể của từng destination sở hữu bởi `NAV-001`–`NAV-006` (§5a); behavior chi tiết của từng screen/view sở hữu bởi `SCR-XXX`/`VIEW-XXX` (§7); RiskEvaluation semantics, Backtest economic evidence, Fill economics, Position derivation, correction lineage, version creation, old-version evidence-family resolution KHÔNG BAO GIỜ map vào WS-001 — các behavior đó thuộc đúng SCR/VIEW sở hữu chúng.

## 5a. Navigation destination specifications

Sáu đặc tả `NAV-001`–`NAV-006` dưới đây (v0.2, đóng `P03C-MIN-03`) là first-class specification cho từng destination top-level — KHÔNG phải routing architecture/permission model (đó là Phase 1 concern). Mỗi đặc tả tuân thủ UX-P-5 (§3): read-only inspection navigation luôn khả dụng khi destination có thể hiển thị an toàn evidence/context/empty/blocked state; authoritative progression/action bị chặn riêng khi guard chưa thoả.

**NAV-001 — Research**
```text
Stable ID:                   NAV-001
Name:                        Research
Purpose:                     Điều hướng tới quan sát market-analysis state thuần tuý, không side-effect.
Destination:                 SCR-001 (Market Analysis Workspace).
Required context:            Instrument/Venue đã chọn (TradableListing đã đăng ký, UX-INV-2). KHÔNG
                              yêu cầu Strategy Instance — quan sát market-analysis bắt đầu ĐƯỢC mà
                              KHÔNG cần pin Strategy Instance trước (v0.2, đóng `P03C-MIN-01`).
Available navigation
behavior:                     Luôn khả dụng từ mọi stage khác (global nav bar, WS-001). Vào thẳng
                              SCR-001. Strategy Instance chỉ trở nên cần thiết khi người dùng chuyển
                              sang hành vi yêu cầu nó (commit vào VIEW-001 → VIEW-002 trước Replay/
                              Backtest, §4/§8 FLOW-001).
Read-only inspection
behavior:                     SCR-001 luôn hiển thị market-analysis hiện có cho Instrument/Venue đã
                              chọn, kể cả khi Strategy Instance chưa pin.
Blocked behavior:             STATE-003 (invalid Instrument/Venue) khi Instrument/Venue chưa hợp lệ;
                              STATE-005 (missing historical evidence) khi thiếu dữ liệu.
UC traceability:              UC-001.
PR traceability:              PR-003, PR-015, PR-017.
Out-of-scope boundary:        KHÔNG routing implementation; KHÔNG bắt buộc Strategy Instance làm entry
                              precondition.
```

**NAV-002 — Replay**
```text
Stable ID:                   NAV-002
Name:                        Replay
Purpose:                     Điều hướng tới historical reconstruction tại một canonical Replay Cursor.
Destination:                 SCR-002 (Replay Cursor & Historical Reconstruction).
Required context:            Strategy Instance đã pin (VIEW-001 → VIEW-002 PASSED, commit-gate, §4).
                              KHÔNG reconstruction nào bắt đầu khi thiếu context này.
Available navigation
behavior:                     Khả dụng từ global nav bar tại mọi stage. Khi CHƯA có Strategy Instance
                              pin: điều hướng có thể mở SCR-002 ở trạng thái blocked/prompt (STATE-004),
                              HOẶC redirect trong UX tới VIEW-001 đã tồn tại — KHÔNG tự phát minh cơ chế
                              routing kỹ thuật cụ thể nào ngoài hai khả năng UX này (Phase 1 quyết định
                              triển khai chính xác).
Read-only inspection
behavior:                     Khi Strategy Instance đã pin nhưng verification (VIEW-002) chưa PASSED
                              (FAILED/INDETERMINATE, UX-P-5): người dùng vẫn có thể điều hướng tới
                              SCR-002 để xem blocked reason — KHÔNG historical reconstruction nào chạy.
Blocked behavior:             STATE-004 (missing Strategy Instance) TRƯỚC khi pin; STATE-006 (Replay
                              reference unavailable) khi cursor không resolve được.
UC traceability:              UC-002 (Strategy Instance precondition), UC-004.
PR traceability:              PR-001, PR-016, PR-008, PR-018, PR-020.
Out-of-scope boundary:        KHÔNG thiết kế cơ chế redirect kỹ thuật (route guard/middleware) — CHỈ mô
                              tả hai khả năng UX-level hợp lệ.
```

**NAV-003 — Backtest**
```text
Stable ID:                   NAV-003
Name:                        Backtest
Purpose:                     Điều hướng tới khởi động/xem một Backtest run bounded.
Destination:                 SCR-003 (Backtest Run Setup); SCR-004/SCR-005 (danh sách run đã có).
Required context:            Strategy Instance đã pin (VIEW-001 → VIEW-002 PASSED, commit-gate, §4) —
                              cùng ràng buộc bounded như NAV-002 Replay. KHÔNG run nào khởi động khi
                              thiếu context này.
Available navigation
behavior:                     Khả dụng từ global nav bar tại mọi stage. Khi CHƯA có Strategy Instance
                              pin: cùng hai khả năng UX như NAV-002 (blocked/prompt tại SCR-003 HOẶC
                              redirect tới VIEW-001) — KHÔNG invent routing implementation.
Read-only inspection
behavior:                     Danh sách Backtest run đã có (SCR-004/SCR-005) vẫn xem được read-only kể
                              cả khi Strategy Instance hiện tại khác với Instance đã tạo run đó.
Blocked behavior:             STATE-004 (missing Strategy Instance) TRƯỚC khi pin; STATE-005 (missing
                              historical evidence); STATE-010 (Backtest run identity unresolved).
UC traceability:              UC-002 (Strategy Instance precondition), UC-006.
PR traceability:              PR-001, PR-016, PR-021, PR-022, PR-023.
Out-of-scope boundary:        KHÔNG thiết kế cơ chế redirect kỹ thuật; KHÔNG simulation
                              algorithm/scheduling (deferred, §15).
```

**NAV-004 — Paper (v0.3 — bốn nguyên nhân blocked riêng biệt, đóng `P03C-B-MAJ-01`)**
```text
Stable ID:                   NAV-004
Name:                        Paper
Purpose:                     Điều hướng tới khởi tạo/xem PAPER execution.
Destination:                 SCR-006 (Paper Execution Initiation); SCR-007 (Paper Order/Execution
                              Detail).
Required context:            Để INITIATE (SCR-006 action, KHÔNG phải để inspect), THEO ĐÚNG THỨ TỰ: (1)
                              Account/Instrument/Venue context hợp lệ (UX-INV-1/UX-INV-2); (2) một
                              Strategy Instance đã chọn VÀ pin cho Paper (qua VIEW-001, riêng biệt với
                              pin Replay/Backtest trước đó nếu có); (3) một eligible PAPER-context
                              Decision lineage RIÊNG BIỆT resolve được cho Strategy Instance đã pin đó
                              (KHÔNG carry-forward/promote từ Backtest/Research).
Available navigation
behavior:                     Khả dụng từ global nav bar tại mọi stage — điều hướng tới SCR-006/SCR-007
                              KHÔNG bị chặn bởi việc thiếu các điều kiện trên (UX-P-5): navigation LUÔN
                              mở được để xem trạng thái hiện tại.
Read-only inspection
behavior:                     SCR-006/SCR-007 luôn hiển thị read-only (Order/ExecutionResult/Fill/
                              Position đã có, hoặc trạng thái "chưa có") — KHÔNG bị vô hiệu hoá trừ khi
                              chính upstream behavior (ví dụ chưa có Order nào) yêu cầu STATE-002 empty.
Blocked behavior:             Khởi tạo PAPER execution (authoritative action tại SCR-006) bị CHẶN,
                              PHÂN BIỆT tường minh theo nguyên nhân — KHÔNG BAO GIỜ gộp thành một thông
                              báo chung: STATE-003 (invalid Instrument/Venue); STATE-028 (Paper Strategy
                              Instance not selected); STATE-029 (Paper Strategy Instance selected but
                              not pinned); STATE-011 (PAPER Decision lineage unavailable, CHỈ sau khi
                              Strategy Instance đã pin).
UC traceability:              UC-002, UC-011.
PR traceability:              PR-001, PR-006, PR-007, PR-016, PR-024.
Out-of-scope boundary:        KHÔNG order type/sizing/execution-model UI; KHÔNG cơ chế chính xác thiết
                              lập PAPER-context Decision (deferred, §15); KHÔNG permission
                              architecture/route guard (UX-P-5, §3).
```

**NAV-005 — Review**
```text
Stable ID:                   NAV-005
Name:                        Review
Purpose:                     Điều hướng tới trace causation Decision→Position hoặc so sánh historical
                              state.
Destination:                 SCR-008 (Decision → Position Lineage Trace); SCR-009 (Historical State
                              Comparison); VIEW-004 (Correction Inspection).
Required context:             Để mở một trace/comparison CỤ THỂ: một Fill/Position contribution (SCR-008)
                              hoặc một Replay Cursor đã chạy tại SCR-002 (SCR-009) phải tồn tại. KHÔNG
                              evidence review nào bị bịa đặt khi thiếu.
Available navigation
behavior:                     Khả dụng từ global nav bar tại mọi stage. Khi chưa có Fill/Position/cursor
                              cụ thể để trace/so sánh: destination hiển thị STATE-002 (empty) — KHÔNG
                              bịa evidence để lấp chỗ trống.
Read-only inspection
behavior:                     Toàn bộ SCR-008/SCR-009/VIEW-004 là read-only thuần tuý (§7.5) — KHÔNG
                              authoritative action nào tồn tại tại Review.
Blocked behavior:             KHÔNG áp dụng theo nghĩa "blocked" (Review không tạo authoritative fact,
                              §7.5) — chỉ có STATE-002 empty khi thiếu evidence nguồn.
UC traceability:              UC-016, UC-017, UC-018.
PR traceability:              PR-028, PR-029, PR-011, PR-030.
Out-of-scope boundary:        KHÔNG tự phát minh review evidence khi trace/so sánh trống; KHÔNG snapshot
                              storage mechanism (Phase 1).
```

**NAV-006 — Improve (v0.3 — thêm VIEW-006, đóng `P03C-B-MAJ-02`)**
```text
Stable ID:                   NAV-006
Name:                        Improve
Purpose:                     Điều hướng tới tạo Strategy Definition Version mới, đăng ký Strategy
                              Instance cho version đó, hoặc so sánh outcome giữa các version.
Destination:                 SCR-010 (Strategy Definition Version Creation); VIEW-006 (Strategy Instance
                              Creation/Binding); SCR-011 (Strategy Version Comparison); VIEW-005
                              (Old-Version Evidence Access).
Required context:             Để tạo version mới (SCR-010): một Strategy Definition (identity) đã tồn
                              tại. Để đăng ký Instance (VIEW-006): một Strategy Definition Version mới
                              vừa tạo (từ SCR-010). Để so sánh (SCR-011): ít nhất hai Strategy Instance
                              gắn hai Strategy Definition Version khác nhau.
Available navigation
behavior:                     Khả dụng từ global nav bar tại mọi stage. KHÔNG tổ chức/quản trị Strategy
                              (organization/strategy-administration) nào được giới thiệu tại đây —
                              Improve CHỈ sở hữu version creation + Instance registration (VIEW-006) +
                              comparison đã UC/PR authorize.
Read-only inspection
behavior:                     SCR-011/VIEW-005 luôn xem được read-only outcome/evidence đã có, kể cả
                              version không active (VIEW-005, §7.6).
Blocked behavior:             KHÔNG áp dụng tại tầng UX cho SCR-010 (validation nội dung thuộc
                              strategy.md, §7.6); registration unavailable cho VIEW-006 khi thiếu danh
                              tính version mới (§7.6); STATE-026 (old-version evidence partially
                              unavailable) cho VIEW-005 khi một họ evidence thiếu.
UC traceability:              UC-019, UC-002 (VIEW-006 registration→pin handoff, v0.3), UC-020, UC-021.
PR traceability:              PR-031, PR-001, PR-016 (VIEW-006, v0.3), PR-032.
Out-of-scope boundary:        KHÔNG organization/strategy-administration behavior; KHÔNG định nghĩa
                              nội dung/schema Strategy Definition cụ thể (thuộc strategy.md).
```

## 6. Screen and view catalogue

| ID | Name | Stage | UC(s) | Primary PR(s) |
|---|---|---|---|---|
| SCR-001 | Market Analysis Workspace | Research | UC-001 | PR-003, PR-015, PR-017 |
| VIEW-001 | Strategy Instance Selector | Research (global) | UC-002 | PR-001, PR-016 |
| VIEW-002 | Research Verification Result | Research | UC-003 | PR-017 |
| SCR-002 | Replay Cursor & Historical Reconstruction | Replay | UC-004 | PR-008, PR-018, PR-020 |
| VIEW-003 | Parity Recomputation Result | Replay | UC-005 | PR-010, PR-019 |
| SCR-003 | Backtest Run Setup | Backtest | UC-006 | PR-021, PR-022, PR-023 |
| SCR-004 | Backtest Run Detail | Backtest | UC-007, UC-008, UC-009 | PR-004, PR-005, PR-009, PR-021, PR-022, PR-033, PR-034 |
| SCR-005 | Backtest Run Comparison | Backtest | UC-010 | PR-034 |
| SCR-006 | Paper Execution Initiation | Paper | UC-002, UC-011 | PR-001, PR-004, PR-005, PR-006, PR-007, PR-014, PR-016, PR-024 |
| SCR-007 | Paper Order/Execution Detail | Paper | UC-012, UC-013, UC-014, UC-015 | PR-007, PR-013, PR-014, PR-024, PR-025, PR-026, PR-027 |
| SCR-008 | Decision → Position Lineage Trace | Review | UC-016 | PR-004, PR-005, PR-028 |
| SCR-009 | Historical State Comparison | Review | UC-017 | PR-029 |
| VIEW-004 | Correction Inspection | Review | UC-018 | PR-011, PR-030 |
| SCR-010 | Strategy Definition Version Creation | Improve | UC-019 | PR-031 |
| VIEW-006 | Strategy Instance Creation/Binding | Improve | UC-019, UC-002 | PR-031, PR-001, PR-016 |
| SCR-011 | Strategy Version Comparison | Improve | UC-020 | PR-031, PR-032 |
| VIEW-005 | Old-Version Evidence Access | Improve | UC-021 | PR-032 |

17 screen/view artifact (11 `SCR`, 6 `VIEW`, v0.3 — thêm `VIEW-006`, đóng `P03C-B-MAJ-02`) — bao trùm đầy đủ `UC-001`–`UC-021`, không thiếu, không dư. Không excessive ID nào tạo cho phần tử decorative.

## 7. Detailed screen/view specifications

### 7.1 Research

**SCR-001 — Market Analysis Workspace**
```text
Name:                    Market Analysis Workspace
Lifecycle stage:         Research
Purpose:                 Hiển thị market-analysis state (Candle/Swing/Structure/Regime/Feature/Market
                         Context) tại một thời điểm/khoảng thời gian, KHÔNG side-effect.
Primary actor:           Ride user.
Entry points:            NAV-001 (Research); trực tiếp sau khi chọn Instrument/Venue tại global context
                         bar (§5).
Exit points:             Chuyển sang VIEW-001 (chọn/cấu hình Strategy Instance) để cam kết Replay/
                         Backtest; hoặc chuyển NAV khác.
Required context:        Instrument/Venue đã chọn, nằm trong TradableListing đã đăng ký (UX-INV-2).
Information displayed:   Candle/Swing/Structure/Regime/Feature/Market Context tại thời điểm/khoảng
                         thời gian đã chọn — đọc trực tiếp authoritative event stream.
Available user actions:  Chọn Instrument/Venue; chọn thời điểm/khoảng thời gian quan tâm.
System-owned actions:    Đọc/hiển thị stream — KHÔNG ghi fact nào.
Evidence consumed:       Candle/Swing/Structure/Regime/Feature/Market Context authoritative stream.
Evidence produced:       KHÔNG (quan sát thuần túy).
Authority labels:        mode=Research; authority=authoritative (recorded fact, read-only).
Primary states:          STATE-001 loading; nội dung market-analysis hiển thị đầy đủ.
Empty/unavailable/
blocked states:          STATE-003 invalid Instrument/Venue; STATE-005 missing historical evidence.
UC traceability:         UC-001.
PR traceability:         PR-003, PR-015, PR-017.
Domain vocabulary
referenced:              candle.md, swing.md, structure.md, regime.md, feature.md, context.md,
                         instrument.md, venue.md.
Out-of-scope boundary:   KHÔNG chart component/pixel layout cụ thể (Phase 1 Figma); KHÔNG chỉ báo
                         mới ngoài Feature type đã đăng ký.
```

**VIEW-001 — Strategy Instance Selector (v0.3 — mở rộng Paper, đóng `P03C-B-MAJ-01`)**
```text
Name:                    Strategy Instance Selector
Lifecycle stage:         Global panel (Research/Replay/Backtest/Paper), truy cập được từ workspace
                         shell tại mọi stage trước khi bounded interaction pin.
Purpose:                 Chọn/pin ĐÚNG MỘT Strategy Instance ĐÃ ĐĂNG KÝ làm cơ sở cho một bounded
                         interaction — Replay, Backtest, HOẶC Paper (v0.3, mở rộng từ chỉ
                         Replay/Backtest). Luôn là selector/pinner của Strategy Instance ĐÃ TỒN TẠI —
                         TUYỆT ĐỐI KHÔNG tạo/đăng ký Strategy Instance mới tại đây (đó là VIEW-006,
                         §7.6).
Primary actor:           Ride user.
Entry points:            Global context bar (§5); từ SCR-001 khi chuẩn bị cam kết Replay/Backtest
                         (commit-gate, §4/§8); từ NAV-004/SCR-006 khi chưa có Strategy Instance pin cho
                         Paper (STATE-028); từ VIEW-006 ngay sau khi một Strategy Instance mới được
                         đăng ký (§7.6).
Exit points:             SCR-002 (Replay) hoặc SCR-003 (Backtest) hoặc SCR-006 (Paper, pin xong TRƯỚC
                         khi resolve PAPER-context Decision lineage) hoặc tiếp tục SCR-001, với Strategy
                         Instance context đã pin (read-only, UX-INV-3).
Required context:        Ít nhất một Strategy Instance đã đăng ký (từ VIEW-006 hoặc đăng ký trước đó).
Information displayed:   Danh sách Strategy Instance đã đăng ký (gắn Strategy Definition Version).
Available user actions:  Chọn một Strategy Instance đã đăng ký để pin cho bounded interaction hiện tại.
System-owned actions:    Pin Strategy Instance đó cố định cho bounded interaction (UX-INV-3) — chặn đổi
                         giữa chừng; khi gọi từ NAV-004/SCR-006, trả control về SCR-006 sau khi pin.
Evidence consumed:       Strategy Instance/Strategy Definition Version đã đăng ký (strategy.md).
Evidence produced:       KHÔNG authoritative fact — lựa chọn tự nó KHÔNG phải Decision Pipeline fact.
Authority labels:        mode=Research/Replay/Backtest/Paper (theo bounded interaction gọi VIEW-001);
                         authority=authoritative (registration record).
Primary states:          Strategy Instance đã pin, hiển thị read-only.
Empty/unavailable/
blocked states:          STATE-004 missing Strategy Instance; STATE-028/STATE-029 (Paper-specific, khi
                         gọi từ SCR-006 — §7.4).
UC traceability:         UC-002, UC-011 (Paper pin, v0.3).
PR traceability:         PR-001, PR-016.
Domain vocabulary
referenced:              strategy.md.
Out-of-scope boundary:   KHÔNG tạo/đăng ký Strategy Definition Version hay Strategy Instance mới tại
                         đây (thuộc SCR-010/VIEW-006, Improve, §7.6).
```

**VIEW-002 — Research Verification Result**
```text
Name:                    Research Verification Result
Lifecycle stage:         Research
Purpose:                 Hiển thị kết quả verification tường minh (PASSED/FAILED/INDETERMINATE) rằng
                         phiên Research không tạo prohibited authoritative fact.
Primary actor:           Ride user.
Entry points:            Tự động khi người dùng kết thúc phiên Research (SCR-001) hoặc chuyển stage.
Exit points:             Trở lại SCR-001 (PASSED, tiếp tục), hoặc dừng tại view này (FAILED/
                         INDETERMINATE) chờ người dùng xem xét.
Required context:        Một phiên Research đã diễn ra.
Information displayed:   Kết quả verification (đúng một trong ba); nếu khác PASSED — reason + fact/
                         evidence bị ảnh hưởng.
Available user actions:  Xem chi tiết reason (khi FAILED/INDETERMINATE); tiếp tục (khi PASSED).
System-owned actions:    Kiểm tra event log Decision/RiskEvaluation/Execution Intent/Order/
                         ExecutionResult trong khoảng thời gian phiên; trả về kết quả tri-state.
Evidence consumed:       Event log của các stream trên, khoảng thời gian phiên.
Evidence produced:       KHÔNG authoritative fact — kết quả workflow-visible DUY NHẤT.
Authority labels:        mode=Research; authority=workflow-visible verification result (KHÔNG một
                         domain entity/event).
Primary states:          STATE-022 Research verification PASSED.
Empty/unavailable/
blocked states:          STATE-023 Research verification FAILED; STATE-024 Research verification
                         INDETERMINATE.
UC traceability:         UC-003.
PR traceability:         PR-017.
Domain vocabulary
referenced:              decision.md.
Out-of-scope boundary:   KHÔNG entity/event "ResearchVerification"; KHÔNG incident/rollback workflow.
```

### 7.2 Replay

**SCR-002 — Replay Cursor & Historical Reconstruction**
```text
Name:                    Replay Cursor & Historical Reconstruction
Lifecycle stage:         Replay
Purpose:                 Chọn canonical Replay Cursor và xem CHÍNH XÁC state authoritative đã tồn tại
                         tại cursor đó (historical reconstruction — mặc định).
Primary actor:           Ride user.
Entry points:            NAV-002 (Replay), sau khi Strategy Instance đã pin (VIEW-001).
Exit points:             VIEW-003 (tuỳ chọn parity recomputation); hoặc chuyển NAV khác (Backtest/
                         Review).
Required context:        Strategy Instance đã chọn; Instrument/Venue hợp lệ; canonical Replay Cursor.
Information displayed:   ReplayState(C) — Decision→Trade Intent→RiskEvaluation→Execution Intent→
                         Order→ExecutionResult→Fill→Position lineage TẠI cursor, chỉ fact có
                         recorded_time ≤ C.
Available user actions:  Chọn Replay Cursor; xem lineage tại cursor.
System-owned actions:    Resolve + hiển thị ReplayState(C) — KHÔNG tạo Decision hay authoritative fact
                         nào (Replay authority boundary).
Evidence consumed:       Toàn bộ authoritative event stream Decision→...→Position; canonical Replay
                         Cursor (Chapter 8 §8.5).
Evidence produced:       KHÔNG — historical reconstruction thuần túy.
Authority labels:        mode=Replay; authority=authoritative recorded fact (default reconstruction,
                         §12).
Primary states:          STATE-001 loading; lineage hiển thị đầy đủ tại cursor.
Empty/unavailable/
blocked states:          STATE-006 Replay reference unavailable.
UC traceability:         UC-004.
PR traceability:         PR-008, PR-018, PR-020.
Domain vocabulary
referenced:              replay-event.md, decision.md, trade-intent.md, risk.md, execution-intent.md,
                         order.md, execution-result.md, fill.md, position.md.
Out-of-scope boundary:   KHÔNG chạy lại simulation/computation (đó là VIEW-003, luôn tuỳ chọn/tách
                         biệt).
```

**VIEW-003 — Parity Recomputation Result**
```text
Name:                    Parity Recomputation Result
Lifecycle stage:         Replay
Purpose:                 Tuỳ chọn kiểm chứng Decision logic tái tính toán khớp Decision đã ghi nhận —
                         deterministic, non-authoritative.
Primary actor:           Ride user.
Entry points:            Nút hành động tuỳ chọn tại SCR-002 (KHÔNG mặc định kích hoạt).
Exit points:             Trở lại SCR-002; nếu mismatch, có thể chuyển sang Review (SCR-009) để xem xét
                         thêm.
Required context:        SCR-002 đã hoàn tất, một ReplayState(C) đang hiển thị.
Information displayed:   Kết quả MATCH, MISMATCH, hoặc INDETERMINATE **(CANDIDATE — v0.6)**, dùng
                         `canonical semantic-decision hash` (UX-INV-5), resolve tại `decision.md` §9a
                         Canonical Decision Semantic Representation/Digest.
Available user actions:  Kích hoạt parity recomputation (tuỳ chọn, người dùng chủ động).
System-owned actions:    Tái tính toán Decision logic (semantic verification, non-authoritative) dưới
                         ĐÚNG CÙNG pinned axis đã establish tại recorded Decision, bao gồm implementation
                         identity khi có (`decision_implementation_version`, decision.md §9a.4/§9a.5a,
                         **CANDIDATE — v0.7, đóng `P16-V003-A-MAJ-01`**); so sánh qua structured
                         Canonical Decision Semantic Representation (decision.md §9a.1/§9a.2 — digest
                         equality đơn độc KHÔNG đủ, **CANDIDATE — v0.7, đóng `P16-V003-A-MAJ-02`**);
                         hiển thị MATCH, MISMATCH, hoặc INDETERMINATE (evidence thiếu/stale/invalidated/
                         ambiguous/non-evaluable, HOẶC implementation identity/digest-definition không
                         resolve/reproduce được, decision.md §9a.6) — KHÔNG BAO GIỜ tự động ghi đè/thay
                         thế/tạo Decision mới.
Evidence consumed:       Decision đã ghi nhận tại cursor; canonical semantic-decision hash definition
                         (decision.md §9a).
Evidence produced:       Kết quả so sánh (non-authoritative, KHÔNG một fact trong event log Decision
                         Pipeline).
Authority labels:        mode=Replay; authority=non-authoritative recomputation (rõ ràng tách biệt
                         khỏi "recorded authoritative Decision" ở SCR-002, §12).
Primary states:          STATE-007 parity match.
Empty/unavailable/
blocked states:          STATE-008 parity mismatch; STATE-030 parity indeterminate (CANDIDATE — v0.6,
                         xem §13).
UC traceability:         UC-005.
PR traceability:         PR-010, PR-019.
Domain vocabulary
referenced:              decision.md, replay-event.md.
Out-of-scope boundary:   KHÔNG hành động "Save recomputed Decision as authoritative"/"Replace recorded
                         Decision"/"Promote parity result"; KHÔNG `ReplayDecision`; KHÔNG cơ chế lưu
                         trữ kết quả recomputation (Phase 1).
```

### 7.3 Backtest

**SCR-003 — Backtest Run Setup**
```text
Name:                    Backtest Run Setup
Lifecycle stage:         Backtest
Purpose:                 Khởi động một Backtest run qua khoảng lịch sử bounded, dưới một stable run
                         identity/context, gắn Strategy Instance/Definition Version/configuration.
Primary actor:           Ride user.
Entry points:            NAV-003 (Backtest), sau khi Strategy Instance đã pin (VIEW-001).
Exit points:             SCR-004 (Backtest Run Detail) khi run đã khởi động.
Required context:        Strategy Instance đã chọn; khoảng thời gian lịch sử có dữ liệu.
Information displayed:   Form nhập khoảng thời gian bounded (start/end); xác nhận Strategy Instance/
                         Definition Version/policy version đang dùng.
Available user actions:  Nhập khoảng thời gian bounded; khởi động run.
System-owned actions:    Gán stable Backtest run identity/context; chạy Decision logic (cùng pipeline
                         Replay/Paper) — KHÔNG tạo Order/ExecutionResult PAPER/Live; xác nhận không
                         route mạng tới exchange thật.
Evidence consumed:       Strategy Instance/Definition Version; market-analysis state lịch sử.
Evidence produced:       Decision/RiskEvaluation sequence gắn run identity (KHÔNG Order/ExecutionResult
                         PAPER/Live).
Authority labels:        mode=Backtest; authority=non-PAPER simulated; representation=product-required,
                         domain-representation deferred where applicable (§10).
Primary states:          STATE-001 loading; run identity tạo thành công.
Empty/unavailable/
blocked states:          STATE-005 missing historical evidence.
UC traceability:         UC-006.
PR traceability:         PR-021, PR-022, PR-023.
Domain vocabulary
referenced:              decision.md, risk.md, strategy.md.
Out-of-scope boundary:   KHÔNG entity/event "BacktestOrder"/"BacktestExecutionResult"; KHÔNG simulation
                         algorithm cụ thể (deferred, §15).
```

**SCR-004 — Backtest Run Detail**
```text
Name:                    Backtest Run Detail
Lifecycle stage:         Backtest
Purpose:                 Xem Decision/RiskEvaluation trace, simulated economic evidence, exposure/
                         position progression, VÀ strategy-level evaluable result cho một Backtest run.
Primary actor:           Ride user.
Entry points:            SCR-003 (sau khi run khởi động); danh sách run đã chạy (từ NAV-003).
Exit points:             SCR-005 (so sánh với run khác); SCR-006 (Paper — judgment gate, KHÔNG hard
                         handoff, §9).
Required context:        Một Backtest run identity tồn tại.
Information displayed:   Ba panel/tab: (a) Decision/RiskEvaluation trace đầy đủ, mỗi Decision kèm
                         outcome + evidence trace; (b) simulated economic evidence gắn mỗi Decision→
                         simulated exposure change, VÀ exposure/position progression theo thời gian;
                         (c) strategy-level evaluable result gắn CHÍNH XÁC version tuple — KHÔNG
                         threshold/target cụ thể (`OQ-003`).
Available user actions:  Chọn run để xem; điều hướng giữa ba panel/tab.
System-owned actions:    Hiển thị trace/evidence/result; xác nhận KHÔNG PAPER Order/ExecutionResult/
                         Fill/Position nào được tạo/tái sử dụng bởi run này.
Evidence consumed:       Decision/RiskEvaluation fact gắn run identity (UC-007); economic evidence/
                         exposure progression (UC-008); version tuple (UC-006).
Evidence produced:       Simulated economic evidence + exposure/position progression + strategy-level
                         evaluable result — **product-required, domain-representation deferred** (§15).
Authority labels:        mode=Backtest (hiển thị TƯỜNG MINH trên MỌI panel); authority=non-PAPER
                         simulated evidence (§10) — KHÔNG BAO GIỜ hiển thị như authoritative PAPER
                         ExecutionResult/Fill/Position/submitted Order/exchange execution.
Primary states:          Trace/evidence/result hiển thị đầy đủ.
Empty/unavailable/
blocked states:          STATE-002 empty (danh sách run rỗng, chưa run nào tồn tại); STATE-009 Backtest
                         evidence insufficient; STATE-010 Backtest run identity unresolved.
UC traceability:         UC-007, UC-008, UC-009.
PR traceability:         PR-004, PR-005, PR-009, PR-021, PR-022, PR-033, PR-034 (v0.4 — thêm PR-004/
                         PR-005: "mỗi Decision kèm outcome + evidence trace" tại field "Information
                         displayed" bên trên materially khớp PR-004/PR-005, đóng `P03C-MAJ-01`).
Domain vocabulary
referenced:              decision.md, risk.md (nguồn evidence, non-PAPER); strategy.md; execution-
                         result.md/fill.md/position.md (tham chiếu CHỈ để định nghĩa ranh giới KHÔNG
                         tái sử dụng).
Out-of-scope boundary:   KHÔNG "BacktestFill"/"BacktestPosition"; KHÔNG simulation algorithm/fee/
                         slippage/accounting/PnL formula; KHÔNG concrete KPI threshold (`OQ-003`).
```

**SCR-005 — Backtest Run Comparison**
```text
Name:                    Backtest Run Comparison
Lifecycle stage:         Backtest
Purpose:                 So sánh strategy-level evaluable result của hai (hoặc nhiều) Backtest run —
                         khác interval hoặc khác Strategy Definition Version.
Primary actor:           Ride user.
Entry points:            SCR-004 (chọn "so sánh"); danh sách run (NAV-003).
Exit points:             Trở lại SCR-004 cho một run cụ thể; SCR-011 (nếu so sánh liên quan version).
Required context:        Ít nhất hai Backtest run đã hoàn tất.
Information displayed:   Kết quả evaluable của từng run CẠNH NHAU, gắn đúng run/version context —
                         KHÔNG gộp/aggregate thành một con số.
Available user actions:  Chọn các run cần so sánh.
System-owned actions:    Hiển thị side-by-side, KHÔNG tạo fact mới.
Evidence consumed:       Strategy-level evaluable result của từng run (SCR-004/UC-009).
Evidence produced:       KHÔNG.
Authority labels:        mode=Backtest (mọi cột); authority=non-PAPER simulated (mọi cột).
Primary states:          So sánh hiển thị đầy đủ cạnh nhau.
Empty/unavailable/
blocked states:          STATE-002 empty (dưới hai Backtest run hoàn tất để so sánh); STATE-009
                         Backtest evidence insufficient (cho run cụ thể thiếu, các run khác vẫn hiển
                         thị).
UC traceability:         UC-010.
PR traceability:         PR-034.
Domain vocabulary
referenced:              strategy.md.
Out-of-scope boundary:   KHÔNG công thức so sánh/scoring/aggregation tổng hợp qua nhiều run
                         (`OQ-003`).
```

### 7.4 Paper

**SCR-006 — Paper Execution Initiation (v0.3 — Strategy Instance pin identity, đóng `P03C-B-MAJ-01`)**
```text
Name:                    Paper Execution Initiation
Lifecycle stage:         Paper
Purpose:                 Người dùng khởi tạo (initiate/request) PAPER execution — KHÔNG authoritative
                         Order payload — dựa trên một Strategy Instance ĐÃ PIN cho Paper VÀ một
                         PAPER-context authoritative Decision lineage RIÊNG BIỆT.
Primary actor:           Ride user (khởi tạo intent); hệ thống sở hữu toàn bộ chuỗi authoritative
                         (UX-P-2).
Entry points:            NAV-004 (Paper); người dùng TỰ QUYẾT ĐỊNH sau khi xem Backtest/Research (§9
                         judgment gate — KHÔNG hard handoff kỹ thuật). Nếu chưa có Strategy Instance
                         pin cho Paper, NAV-004 mở SCR-006 ở STATE-028 và cung cấp lối vào VIEW-001.
Exit points:             SCR-007 (Paper Order/Execution Detail) — hoặc dừng tại chính screen này nếu
                         thiếu Strategy Instance pin (STATE-028/029) hoặc không có PAPER-context
                         Decision lineage eligible (STATE-011).
Required context:        (1) Một Strategy Instance đã chọn VÀ pin cho bounded Paper interaction này
                         (qua VIEW-001, PR-001/PR-016) — pin này ĐỘC LẬP với pin đã dùng ở phiên
                         Replay/Backtest trước đó nếu có; (2) một PAPER-context authoritative Decision
                         lineage (LONG/SHORT) ELIGIBLE tồn tại cho Strategy Instance đã pin đó — Decision
                         này TUYỆT ĐỐI KHÔNG phải Decision từ Backtest/Research được carry-forward/
                         promote/reuse; (3) Account/Instrument/Venue context hợp lệ.
Information displayed:   Danh tính Strategy Instance đã pin; danh tính Strategy Definition Version gắn
                         Instance đó; Account/Instrument/Venue identity; nhãn mode=Paper,
                         authority=authoritative PAPER — TẤT CẢ hiển thị TRƯỚC khi resolve PAPER-context
                         Decision lineage. Xác nhận PAPER-context Decision lineage eligible (nếu có) —
                         KHÔNG form nhập quantity/order type/sizing/fee/slippage/execution model (chưa
                         UC/PR nào authorize input đó).
Available user actions:  Chọn/pin Strategy Instance cho Paper (qua VIEW-001, nếu chưa pin); yêu cầu
                         khởi tạo PAPER execution (intent, KHÔNG authoritative payload) sau khi pin.
                         TUYỆT ĐỐI KHÔNG có action "Execute this Backtest Decision in Paper"/"Promote
                         to Paper"/"Convert Backtest Decision" — những action này KHÔNG được thiết kế.
System-owned actions:    Resolve PAPER-context Decision lineage CHO ĐÚNG Strategy Instance đã pin; phát
                         sinh Trade Intent (system-owned) → RiskEvaluation → (nếu APPROVED) Execution
                         Intent (system-owned) → Order (system-owned) → OrderSubmissionRequest
                         (system-owned) → ExecutionResultComputation → PaperExecutionObservation →
                         ExecutionResult → (nếu EXECUTED) Fill → Position — MỖI fact trong chuỗi hiển
                         thị resolve trực tiếp về đúng Strategy Instance pin đó.
Evidence consumed:       Strategy Instance pin (VIEW-001); PAPER-context authoritative Decision lineage
                         (RIÊNG BIỆT); Account/Instrument/Venue context. Backtest/Research evidence
                         (nếu đã xem) CHỈ inform judgment — KHÔNG input authoritative.
Evidence produced:       Trade Intent, RiskEvaluation, Execution Intent (nếu APPROVED), Order,
                         OrderSubmissionRequest, ExecutionResultComputation, PaperExecutionObservation,
                         ExecutionResult, Fill (nếu EXECUTED) — TẤT CẢ system-owned, TẤT CẢ resolve về
                         Strategy Instance pin.
Authority labels:        mode=Paper; authority=authoritative PAPER (toàn bộ chuỗi, KHÔNG Live).
Primary states:          RiskEvaluation APPROVED (tiếp tục); chuỗi tiến triển tới ExecutionResult.
Empty/unavailable/
blocked states:          STATE-028 Paper Strategy Instance not selected (v0.3 — phân biệt tường minh
                         với STATE-029/STATE-011); STATE-029 Paper Strategy Instance selected but not
                         pinned (v0.3); STATE-011 PAPER Decision lineage unavailable (blocked TRƯỚC
                         PAPER execution, CHỈ sau khi Strategy Instance đã pin); STATE-013 Risk REJECTED;
                         STATE-014 Risk NON_EVALUABLE (cả hai dừng TRƯỚC Execution Intent/Order). Bốn
                         nguyên nhân blocked này KHÔNG BAO GIỜ gộp lại thành một thông báo chung chung —
                         mỗi cái disclose reason riêng.
UC traceability:         UC-002 (Strategy Instance pin precondition), UC-011.
PR traceability:         PR-001, PR-004, PR-005, PR-006, PR-007, PR-014, PR-016, PR-024 (v0.4 — thêm
                         PR-004 (Decision lineage outcome LONG/SHORT tại "Required context"), PR-005
                         (evidence chain tại "Evidence consumed"/"System-owned actions"), PR-014
                         (RiskEvaluation APPROVED/REJECTED/NON_EVALUABLE tại "Primary/blocked states"),
                         đóng `P03C-MAJ-01`).
Domain vocabulary
referenced:              decision.md, trade-intent.md, risk.md, execution-intent.md, order.md,
                         execution-result.md, fill.md, position.md.
Out-of-scope boundary:   KHÔNG order type/sizing/fee/slippage/execution-model UI do người dùng cung
                         cấp; KHÔNG Live routing (deferred, `OQ-002`); KHÔNG cơ chế chính xác thiết
                         lập PAPER-context Decision (deferred, §15); KHÔNG clone/copy/recreate Decision
                         từ Backtest/Research; KHÔNG PaperSession entity/session identifier/storage/
                         timeout/persistence mechanism.
```

**SCR-007 — Paper Order/Execution Detail (v0.3 — Strategy Instance identity continuity, đóng `P03C-B-MAJ-01`)**
```text
Name:                    Paper Order/Execution Detail
Lifecycle stage:         Paper
Purpose:                 Xem ExecutionResult, Fill simulation evidence, Position (hoặc NON_EVALUABLE),
                         VÀ xác nhận không lệnh thật nào được đặt.
Primary actor:           Ride user.
Entry points:            SCR-006 (sau khi chuỗi PAPER hoàn tất); danh sách Order (NAV-004).
Exit points:             SCR-008 (Review — trace causation); NAV-004 (Order khác).
Required context:        Order đã đi qua SCR-006, có ExecutionResult visible-valid.
Information displayed:   Danh tính Strategy Instance đã pin, Strategy Definition Version, Account/
                         Instrument/Venue (giữ nguyên liên tục từ SCR-006 — KHÔNG đổi giữa chừng,
                         UX-INV-3), mode=Paper, authority=authoritative PAPER. Bốn panel/tab: (a)
                         ExecutionResult (EXECUTED/NOT_EXECUTED), environment PAPER; (b) Fill simulation
                         evidence (policy/configuration/build/deterministic-input ref) + economics, khớp
                         byte-for-byte PaperExecutionObservation; (c) Position hiện tại (FLAT/LONG/
                         SHORT/NON_EVALUABLE); (d) xác nhận environment=PAPER trên mọi fact, không route
                         mạng tới exchange thật.
Available user actions:  Chọn Order/Fill để xem chi tiết; điều hướng giữa bốn panel/tab.
System-owned actions:    Derive Position từ eligible Fill lineage; disclose NON_EVALUABLE khi nhiều
                         Fill lineage xung đột (KHÔNG chọn một/aggregate/report FLAT sai). Xác nhận
                         ExecutionResult/Fill/Position VÀ upstream C7 lineage TẤT CẢ resolve về đúng
                         Strategy Instance pin đã thiết lập tại SCR-006.
Evidence consumed:       ExecutionResult, Fill, PaperExecutionObservation, Position projection,
                         environment field, Strategy Instance pin identity (liên tục từ SCR-006).
Evidence produced:       KHÔNG (quan sát thuần túy trên panel này — fact đã tạo tại SCR-006).
Authority labels:        mode=Paper; authority=authoritative PAPER (ExecutionResult/Fill/Position);
                         Position tự thân là derived projection, KHÔNG authoritative fact riêng.
Primary states:          STATE-015 ExecutionResult EXECUTED; STATE-018/019/020 Position FLAT/LONG/
                         SHORT.
Empty/unavailable/
blocked states:          STATE-002 empty (chưa Order/Fill nào tồn tại); STATE-016 ExecutionResult
                         NOT_EXECUTED; STATE-017 Fill absent; STATE-021 Position NON_EVALUABLE.
UC traceability:         UC-012, UC-013, UC-014, UC-015.
PR traceability:         PR-007, PR-013, PR-014, PR-024, PR-025, PR-026, PR-027 (v0.4 — thêm PR-014:
                         ExecutionResult EXECUTED/NOT_EXECUTED, Fill absent, Position FLAT/LONG/SHORT/
                         NON_EVALUABLE tại "Primary/blocked states" là explicit lifecycle-transition
                         presentation, đóng `P03C-MAJ-01`).
Domain vocabulary
referenced:              order.md, execution-result.md, fill.md, position.md.
Out-of-scope boundary:   KHÔNG chi tiết computation/observation nội bộ ngoài PR-007 yêu cầu; KHÔNG
                         weighted-average/netting formula cho nhiều Fill (`OQ-003`-adjacent, ngoài
                         phạm vi); KHÔNG cơ chế audit network kỹ thuật cụ thể (Phase 1).
```

### 7.5 Review

**SCR-008 — Decision → Position Lineage Trace**
```text
Name:                    Decision → Position Lineage Trace
Lifecycle stage:         Review
Purpose:                 Với một Position contribution bất kỳ, truy vết ngược toàn bộ causation trace
                         về Decision gốc.
Primary actor:           Ride user.
Entry points:            SCR-007 (chọn một Fill/Position contribution); NAV-005 (Review).
Exit points:             SCR-009 (so sánh reconstructed/recorded state); VIEW-004 (nếu correction phát
                         hiện).
Required context:        Fill/Position contribution tồn tại.
Information displayed:   Causation trace ngược: Fill→ExecutionResult→Order→Execution Intent→
                         RiskEvaluation→Trade Intent→Decision gốc — KHÔNG mắt xích thiếu.
Available user actions:  Chọn một Fill đóng góp Position để trace.
System-owned actions:    Resolve causation_refs/correlation_id chain đầy đủ.
Evidence consumed:       Toàn bộ causation_refs/correlation_id chain Decision→...→Position.
Evidence produced:       KHÔNG.
Authority labels:        mode=Review; authority=authoritative (mọi fact trong chain).
Primary states:          Trace hiển thị đầy đủ, không đứt đoạn.
Empty/unavailable/
blocked states:          KHÔNG áp dụng (mắt xích thiếu KHÔNG dự kiến theo Domain Contract đã
                         Consolidated Stable — ngoài phạm vi UX, governance/data-integrity concern).
UC traceability:         UC-016.
PR traceability:         PR-004, PR-005, PR-028 (v0.4 — thêm PR-004 (Decision gốc + Strategy Instance
                         nguồn gốc tại field "Information displayed") và PR-005 (causation trace đầy đủ,
                         cùng nội dung PR-005 yêu cầu — input snapshot/causation chain), đóng
                         `P03C-MAJ-01`).
Domain vocabulary
referenced:              decision.md, trade-intent.md, risk.md, execution-intent.md, order.md,
                         execution-result.md, fill.md, position.md.
Out-of-scope boundary:   KHÔNG chi tiết UI trace visualization/pixel layout (Phase 1 Figma).
```

**SCR-009 — Historical State Comparison**
```text
Name:                    Historical State Comparison
Lifecycle stage:         Review
Purpose:                 So sánh state tái dựng qua Replay tại một cursor lịch sử với state đã hiển
                         thị/ghi nhận tại đúng thời điểm đó, xác nhận không silent drift.
Primary actor:           Ride user.
Entry points:            SCR-002 (Replay, "so sánh với recorded state"); NAV-005 (Review).
Exit points:             VIEW-004 (nếu correction được phát hiện).
Required context:        SCR-002 đã chạy cho cursor cần so sánh.
Information displayed:   Kết quả so sánh: "No conflict" (không correction giữa hai thời điểm) HOẶC
                         khác biệt tường minh kèm fact correction liên quan (KHÔNG ẩn/repaint).
Available user actions:  Chọn Replay Cursor cần so sánh.
System-owned actions:    Resolve ReplayState(C) hiện tại; so sánh với state đã từng ghi nhận tại đúng
                         cursor đó.
Evidence consumed:       ReplayState(C) (SCR-002); correction/invalidation fact liên quan nếu có.
Evidence produced:       Kết quả so sánh — non-authoritative, KHÔNG fact mới.
Authority labels:        mode=Review; authority=authoritative recorded fact + non-authoritative
                         comparison result (nhãn tách biệt).
Primary states:          "No conflict."
Empty/unavailable/
blocked states:          Correction visible sau historical cursor → chuyển hiển thị khác biệt (dẫn
                         VIEW-004).
UC traceability:         UC-017.
PR traceability:         PR-029.
Domain vocabulary
referenced:              replay-event.md.
Out-of-scope boundary:   KHÔNG cơ chế lưu snapshot lịch sử cụ thể (Phase 1).
```

**VIEW-004 — Correction Inspection**
```text
Name:                    Correction Inspection
Lifecycle stage:         Review
Purpose:                 Xem một correction (fact mới thay thế fact cũ) mà KHÔNG giá trị lịch sử nào bị
                         sửa/xóa ngầm (No Repaint).
Primary actor:           Ride user.
Entry points:            SCR-009 (khi correction phát hiện); trực tiếp từ bất kỳ fact nào có
                         `supersedes_fact_ref`.
Exit points:             Trở lại SCR-008/SCR-009.
Required context:        Một correction fact (`*FactInvalidated` + replacement) tồn tại.
Information displayed:   Fact gốc (vẫn resolvable, append-only) VÀ fact replacement (nếu có), liên kết
                         tường minh (`supersedes_fact_ref`) — KHÔNG chỉ giá trị "đã sửa" ẩn nguồn gốc.
Available user actions:  Chọn một fact để kiểm tra correction.
System-owned actions:    Hiển thị CẢ HAI trạng thái (trước/sau correction) — hành vi bắt buộc, không
                         nhánh lỗi.
Evidence consumed:       Fact gốc + `*FactInvalidated` + fact replacement (nếu có).
Evidence produced:       KHÔNG.
Authority labels:        mode=Review; authority=authoritative (cả fact gốc và fact thay thế).
Primary states:          Correction hiển thị đầy đủ (gốc + thay thế + lineage).
Empty/unavailable/
blocked states:          KHÔNG áp dụng — hiển thị luôn cả hai trạng thái là hành vi bắt buộc.
UC traceability:         UC-018.
PR traceability:         PR-011, PR-030.
Domain vocabulary
referenced:              decision.md, risk.md, execution-result.md, fill.md.
Out-of-scope boundary:   KHÔNG UI diff visualization cụ thể (Phase 1 Figma).
```

### 7.6 Improve

**SCR-010 — Strategy Definition Version Creation**
```text
Name:                    Strategy Definition Version Creation
Lifecycle stage:         Improve
Purpose:                 Tạo một Strategy Definition Version mới, tách biệt hoàn toàn khỏi version cũ.
Primary actor:           Ride user.
Entry points:            NAV-006 (Improve), sau Review (SCR-008/SCR-009/VIEW-004).
Exit points:             VIEW-006 (đăng ký Strategy Instance RIÊNG BIỆT gắn version mới, v0.3, §7.6);
                         SCR-011 (so sánh version, khi áp dụng); SCR-001 (quan sát read-only tuỳ chọn có
                         thể bắt đầu KHÔNG cần pin, §4/FLOW-006). KHÔNG nói VIEW-001 tự tạo Instance.
Required context:        Một Strategy Definition (identity) đã tồn tại.
Information displayed:   Form nội dung Strategy Definition Version mới (nội dung/schema cụ thể thuộc
                         `strategy.md`, KHÔNG sửa tại đây).
Available user actions:  Tạo Strategy Definition Version mới.
System-owned actions:    Gán version identity mới, tách biệt version cũ (append-only).
Evidence consumed:       Strategy Definition (identity) hiện có.
Evidence produced:       Strategy Definition Version mới (strategy.md).
Authority labels:        mode=Improve; authority=authoritative (strategy.md registration).
Primary states:          Version mới tạo thành công, độc lập version cũ.
Empty/unavailable/
blocked states:          KHÔNG áp dụng tại tầng UX (validation nội dung thuộc strategy.md).
UC traceability:         UC-019.
PR traceability:         PR-031.
Domain vocabulary
referenced:              strategy.md, ADR-013.
Out-of-scope boundary:   KHÔNG định nghĩa nội dung/schema Strategy Definition cụ thể; KHÔNG đăng ký
                         Strategy Instance tại đây (đó là VIEW-006 bên dưới).
```

**VIEW-006 — Strategy Instance Creation/Binding (v0.3, mới, đóng `P03C-B-MAJ-02`)**
```text
Stable ID:               VIEW-006
Name:                    Strategy Instance Creation/Binding
Lifecycle stage:         Improve
Purpose:                 Sau khi SCR-010 tạo một Strategy Definition Version mới: người dùng yêu cầu
                         đăng ký một Strategy Instance RIÊNG BIỆT gắn CHÍNH XÁC version mới đó. Đây là
                         bounded product handoff giữa "tạo version" (SCR-010/UC-019) và "chọn/pin
                         Instance để dùng" (VIEW-001/UC-002) — KHÔNG phải chính bản thân UC-019, KHÔNG
                         phải chính bản thân UC-002.
Primary actor:           Ride user.
Entry points:            SCR-010 (ngay sau khi Strategy Definition Version mới tạo thành công).
Exit points:             VIEW-001 (chọn/pin Strategy Instance vừa đăng ký, §7.1) — hoặc trở lại SCR-010.
Required context:        Một Strategy Definition Version mới vừa tạo (từ SCR-010) đã tồn tại, gắn một
                         Strategy Definition (identity) đã có.
Information displayed:   Danh tính Strategy Definition; danh tính Strategy Definition Version mới; xác
                         nhận rằng một Strategy Instance RIÊNG BIỆT sẽ gắn với chính xác version đó;
                         sau khi đăng ký thành công — danh tính Strategy Instance đã đăng ký.
Available user actions:  Tạo/đăng ký Strategy Instance cho Strategy Definition Version này. KHÔNG field
                         cấu hình nào khác được giới thiệu ngoài xác nhận đăng ký.
System-owned actions:    Đăng ký một Strategy Instance identity RIÊNG BIỆT; gắn Instance đó với Strategy
                         Definition Version đã chọn; trả Instance vừa đăng ký làm khả dụng để VIEW-001
                         chọn/pin.
Evidence consumed:       Strategy Definition (identity) authoritative; Strategy Definition Version mới
                         authoritative (từ SCR-010).
Evidence produced:       Strategy Instance identity đã đăng ký; liên kết hiển thị tường minh với Strategy
                         Definition Version đã chọn (strategy.md).
Authority labels:        mode=Improve; authority=authoritative (strategy.md registration).
Primary states:          registration ready (Strategy Definition Version mới sẵn sàng để đăng ký
                         Instance); registration completed (Instance đã đăng ký thành công).
Empty/unavailable/
blocked states:          registration unavailable — khi thiếu danh tính Strategy Definition Version
                         mới (ví dụ điều hướng trực tiếp tới VIEW-006 mà không qua SCR-010) — tái sử
                         dụng nguyên tắc bốn-phần fallback (§11): workflow dừng, danh tính hiện có vẫn
                         hiển thị, reason disclosed, không authoritative action nào xảy ra. KHÔNG state
                         mới nào được tạo cho trường hợp này — không cần vì đây là guard đơn giản trước
                         một action, tương tự cách SCR-010 tự xử lý validation nội dung.
UC traceability:         UC-019 (upstream — tạo Strategy Definition Version VÀ handoff, KHÔNG tự tạo
                         Strategy Instance), UC-002 (Strategy Instance sau đó được VIEW-001 chọn/pin).
PR traceability:         PR-031 (tạo/tách biệt Strategy Definition Version mới), PR-001 (yêu cầu Strategy
                         Instance đã chọn để vận hành), PR-016 (Strategy Instance selection/binding
                         behavior — VIEW-006 là bước đăng ký TRƯỚC bước chọn đó).
Domain vocabulary
referenced:              strategy.md.
Out-of-scope boundary:   KHÔNG định nghĩa schema/field/validation cho Strategy Instance; KHÔNG
                         API/database/command/event implementation; KHÔNG chọn/pin Instance cho một
                         bounded interaction cụ thể tại đây (đó là VIEW-001); KHÔNG domain entity mới
                         ngoài khái niệm Strategy Instance đã tồn tại (strategy.md).
```

**SCR-011 — Strategy Version Comparison**
```text
Name:                    Strategy Version Comparison
Lifecycle stage:         Improve
Purpose:                 So sánh outcome giữa Strategy Instance gắn version cũ (kể cả không còn active)
                         và version mới — same-mode HOẶC cross-mode side-by-side.
Primary actor:           Ride user.
Entry points:            SCR-010 (sau khi tạo version mới); SCR-005 (nếu so sánh liên quan Backtest);
                         NAV-006.
Exit points:             VIEW-005 (nếu version cũ không active, cần resolve evidence riêng); vòng lặp
                         Research (SCR-001) với Strategy Instance mới.
Required context:        Ít nhất hai Strategy Instance, gắn hai Strategy Definition Version khác nhau.
Information displayed:   Ba chế độ so sánh — **Backtest vs Backtest** (Decision/RiskEvaluation trace +
                         simulated economic evidence + exposure/position progression + strategy-level
                         evaluable result, non-PAPER authority, SCR-004); **PAPER vs PAPER**
                         (authoritative Decision/RiskEvaluation/Order/ExecutionResult/Fill/Position,
                         SCR-006/SCR-007); **cross-mode side-by-side** (CẢ HAI họ cạnh nhau, MỖI bên
                         gắn nhãn mode/authority/evidence-type/Strategy Instance identity/Strategy
                         Definition Version identity tường minh).
Available user actions:  Chọn Strategy Instance cần so sánh; chọn mode so sánh (Backtest/PAPER/cross-
                         mode).
System-owned actions:    Hiển thị side-by-side, tách biệt hoàn toàn — KHÔNG unified outcome card,
                         KHÔNG single normalized score, KHÔNG common execution result, KHÔNG authority-
                         equivalent comparison, KHÔNG automatic cross-mode ranking.
Evidence consumed:       Decision/RiskEvaluation/simulated economic evidence/exposure progression/
                         strategy-level result (Backtest, non-PAPER, SCR-004) VÀ/HOẶC authoritative
                         Decision/RiskEvaluation/Order/ExecutionResult/Fill/Position (PAPER, SCR-006/
                         SCR-007) — BAO GỒM evidence version không active, resolve qua VIEW-005 theo
                         TỪNG họ độc lập (KHÔNG cross-mode evidence object chung).
Evidence produced:       KHÔNG — so sánh hiển thị thuần túy.
Authority labels:        mode=Backtest và/hoặc PAPER (gắn nhãn RIÊNG cho từng cột/panel); authority=
                         non-PAPER simulated / authoritative PAPER (KHÔNG BAO GIỜ trộn lẫn).
Primary states:          So sánh hiển thị đầy đủ, nhãn mode/authority/evidence-type rõ ràng.
Empty/unavailable/
blocked states:          STATE-002 empty (dưới hai Strategy Instance đã đăng ký để so sánh) — hiển thị
                         rỗng cho Instance thiếu, KHÔNG lỗi toàn bộ so sánh; evidence version cũ chưa
                         resolve → VIEW-005 Alternate/failure áp dụng cho đúng phần đó.
UC traceability:         UC-020.
PR traceability:         PR-031, PR-032.
Domain vocabulary
referenced:              strategy.md, decision.md, risk.md (Backtest, non-PAPER); execution-result.md,
                         fill.md, position.md (PAPER, authoritative) — HAI HỌ TÁCH BIỆT.
Out-of-scope boundary:   KHÔNG gọi Backtest material là ExecutionResult/Fill/Position authoritative;
                         KHÔNG unified Backtest/PAPER outcome entity/schema; KHÔNG công thức so sánh/
                         scoring/normalization cross-mode (`OQ-003`).
```

**VIEW-005 — Old-Version Evidence Access**
```text
Name:                    Old-Version Evidence Access
Lifecycle stage:         Improve
Purpose:                 Với một Strategy Definition Version không còn active: danh tính LUÔN hiển thị;
                         resolve evidence lịch sử ĐỘC LẬP theo TỪNG họ (Backtest, non-PAPER / PAPER,
                         authoritative) khi có thể.
Primary actor:           Ride user.
Entry points:            SCR-011 (Strategy Version Comparison, khi một Instance gắn version không
                         active); SCR-010.
Exit points:             Trở lại SCR-011 với evidence resolved (một phần hoặc đầy đủ).
Required context:        Strategy Definition Version cũ đã từng chạy trong Backtest và/hoặc Paper.
Information displayed:   Danh tính version (LUÔN hiển thị). Backtest evidence family (Decision/
                         RiskEvaluation trace, simulated economic evidence, exposure/position
                         progression, strategy-level evaluable result, run identity/version/
                         configuration context — non-PAPER) khi áp dụng. PAPER evidence family
                         (Decision, Trade Intent, RiskEvaluation, Execution Intent, Order,
                         OrderSubmissionRequest, ExecutionResult, Fill, Position — authoritative PAPER,
                         với ExecutionResultComputation/PaperExecutionObservation làm supporting
                         evidence khi cần) khi áp dụng — HAI HỌ HIỂN THỊ TÁCH BIỆT hoàn toàn.
Available user actions:  Chọn mode cần resolve (Backtest, PAPER, hoặc cả hai).
System-owned actions:    Resolve từng họ evidence ĐỘC LẬP; đánh dấu "incomplete" cho phần evidence
                         khả dụng khi một phần khác thiếu.
Evidence consumed:       Backtest evidence family VÀ/HOẶC PAPER evidence family, khi áp dụng.
Evidence produced:       KHÔNG — KHÔNG tạo unified old-version evidence entity/aggregate gộp hai họ.
Authority labels:        mode=Backtest (non-PAPER) và/hoặc mode=PAPER (authoritative) — nhãn RIÊNG cho
                         từng họ, KHÔNG BAO GIỜ gộp.
Primary states:          STATE-025 old-version evidence complete.
Empty/unavailable/
blocked states:          STATE-026 old-version evidence partially unavailable — workflow dừng CHO ĐÚNG
                         phần bị ảnh hưởng; danh tính/mode/authority vẫn hiển thị; evidence khả dụng
                         khác vẫn hiển thị nhưng đánh dấu incomplete; reason disclosed; KHÔNG fabricate,
                         KHÔNG silently omit, KHÔNG ngụ ý toàn bộ lịch sử Strategy không khả dụng.
UC traceability:         UC-021.
PR traceability:         PR-032.
Domain vocabulary
referenced:              strategy.md, decision.md, risk.md (Backtest, evidence-source vocabulary only);
                         trade-intent.md, execution-intent.md, order.md, execution-result.md, fill.md,
                         position.md (PAPER, authoritative).
Out-of-scope boundary:   KHÔNG retention duration/archive tiering/retrieval latency/restoration
                         process/storage architecture/evidence availability SLA; KHÔNG unified old-
                         version evidence aggregate; KHÔNG gọi Backtest material là ExecutionResult/
                         Fill/Position/PAPER execution outcome; KHÔNG redefine ExecutionResultComputation/
                         PaperExecutionObservation semantics.
```

## 8. Lifecycle stage flows

**FLOW-001 — Primary end-to-end journey (walking skeleton) (v0.2 — sửa thứ tự Research, đóng `P03C-MIN-01`)**
```text
WS-001 → NAV-001 → SCR-001 (Research, quan sát market-analysis, UC-001 — KHÔNG cần Strategy Instance
                    đã pin, §4) →

  [commit gate — khi người dùng chuẩn bị chuyển sang Replay/Backtest, KHÔNG phải entry-prerequisite của
  SCR-001]:
  VIEW-001 (chọn Strategy Instance, UC-002) → VIEW-002 (Research Verification Result, UC-003) →
    [PASSED] → SCR-002 (Replay, UC-004) hoặc SCR-003 (Backtest, UC-006)
    [FAILED/INDETERMINATE] → authoritative progression bị CHẶN (UX-P-5) — read-only vẫn khả dụng →

SCR-002 (Replay, UC-004) → [tuỳ chọn VIEW-003, UC-005] →
SCR-003 → SCR-004 → [tuỳ chọn SCR-005] (Backtest, UC-006–UC-010) →
[judgment gate, §9] → SCR-006 → SCR-007 (Paper, UC-011–UC-015) →
SCR-008 → SCR-009 → [tuỳ chọn VIEW-004] (Review, UC-016–UC-018) →
SCR-010 → SCR-011 → [tuỳ chọn VIEW-005] (Improve, UC-019–UC-021) →
VÒNG LẶP về SCR-001 (Research, Strategy Instance MỚI qua VIEW-001 tại commit gate kế tiếp).

Live KHÔNG phải một bước — chỉ nhắc như lifecycle boundary bị hoãn (§15, `OQ-002`), KHÔNG NAV/SCR nào
dẫn tới Live.

UC traceability:  UC-001–UC-021 (toàn bộ — FLOW-001 là primary end-to-end journey, hợp lệ giữ full-range
                  vì đây CHÍNH LÀ artifact đại diện toàn bộ vòng đời, không phải fallback coverage).
PR traceability:  (v0.3 — thu hẹp, đóng `P03C-MAJ-01`: CHỈ requirement vật chất biểu diễn stage
                  ordering/entry-exit/gate/handoff của CHÍNH flow này — KHÔNG union mọi PR chi tiết của
                  từng child screen, các PR đó đã sở hữu riêng tại §7/§14c)
                  PR-001, PR-016 (selection/pinning gate — VIEW-001 commit-gate); PR-017 (Research
                  verification guard — VIEW-002); PR-034 (Backtest evaluable result — INFORM judgment
                  tại Backtest→Paper handoff, FLOW-003); PR-024 (PAPER-context Decision lineage riêng
                  biệt — handoff guard tại SCR-006); PR-028 (causation trace sẵn sàng — Paper→Review
                  handoff, entry precondition SCR-008); PR-031 (Strategy Definition Version mới —
                  Review→Improve handoff target, SCR-010); PR-003, PR-015 (Research loop-back re-entry,
                  Improve→Research, cùng SCR-001).
```

**FLOW-002 — Strategy Instance selection/pin (global)**
```text
Trigger: người dùng chuẩn bị cam kết Replay/Backtest, hoặc bắt đầu phiên mới.
VIEW-001 → chọn Strategy Instance → hệ thống pin (read-only, UX-INV-3) → context hiển thị trên toàn
bộ global context bar (§5) cho tới khi phiên kết thúc.
UC traceability:  UC-002.
PR traceability:  PR-001, PR-016.
```

**FLOW-003 — Backtest → Paper handoff (judgment gate, KHÔNG hard handoff)**
```text
SCR-004/SCR-005 (Backtest evidence, non-PAPER, INFORM judgment) → người dùng TỰ QUYẾT ĐỊNH → SCR-006
(Paper) → [nếu chưa có Strategy Instance pin cho Paper] VIEW-001 (pin, STATE-028/029, v0.3) → SCR-006
resolve PAPER-context Decision lineage RIÊNG BIỆT. KHÔNG action nào tự động chuyển Backtest Decision
thành PAPER Decision — pin Strategy Instance cho Paper ĐỘC LẬP với pin đã dùng ở Backtest. Nếu Decision
lineage không eligible, workflow dừng NGAY tại SCR-006 (STATE-011).
UC traceability:  UC-009 (Backtest evaluable result, INFORM), UC-010 (Backtest comparison, INFORM
                  tuỳ chọn), UC-011 (Paper initiation, guard).
PR traceability:  PR-034 (Backtest evaluable evidence), PR-024 (PAPER Decision lineage riêng biệt).
```

**FLOW-004 — Paper execution initiation (system-owned chain)**
```text
SCR-006: người dùng yêu cầu khởi tạo → hệ thống resolve PAPER-context Decision → Trade Intent →
RiskEvaluation → [APPROVED] → Execution Intent → Order → OrderSubmissionRequest →
ExecutionResultComputation → PaperExecutionObservation → ExecutionResult → [EXECUTED] → Fill →
Position → SCR-007 hiển thị kết quả.
UC traceability:  UC-011 (khởi tạo), UC-012, UC-013, UC-014 (SCR-007 hiển thị kết quả chuỗi).
PR traceability:  PR-006 (RiskEvaluation), PR-007 (chuỗi PAPER), PR-024 (Order/ExecutionResult), PR-025
                  (Fill), PR-026 (Position).
```

**FLOW-005 — Old-version evidence access (từ so sánh)**
```text
SCR-011 (phát hiện Strategy Instance gắn version không active) → VIEW-005 → resolve Backtest family
và/hoặc PAPER family ĐỘC LẬP → trở lại SCR-011 với evidence (đầy đủ hoặc đánh dấu incomplete).
UC traceability:  UC-020 (phát hiện tại so sánh), UC-021 (resolve old-version evidence).
PR traceability:  PR-031, PR-032.
```

**FLOW-006 — Improve → Research loop-back (v0.3 — thêm VIEW-006, đóng `P03C-B-MAJ-02`; đóng `P03C-MIN-01`)**
```text
SCR-010 (tạo Strategy Definition Version mới) →
SCR-001 (quan sát read-only Research TUỲ CHỌN, vòng lặp, KHÔNG cần pin — có thể bắt đầu SONG SONG
         hoặc BỎ QUA bước dưới) →
  [khi cần commit vào Replay/Backtest với version mới, nếu chưa có Instance eligible]:
  VIEW-006 (đăng ký Strategy Instance RIÊNG BIỆT gắn version mới) →
  VIEW-001 (chọn/pin Strategy Instance vừa đăng ký) →
  VIEW-002 (Research verification) →
    [PASSED] → SCR-002/SCR-003.

Lối tắt tuỳ chọn: SCR-010 → VIEW-006 trực tiếp (bỏ qua quan sát Research trước) khi người dùng muốn
đăng ký Instance ngay. Evidence version cũ vẫn truy cập qua VIEW-005 bất kỳ lúc nào, KHÔNG phụ thuộc
thứ tự trên. VIEW-001 KHÔNG BAO GIỜ tự tạo Strategy Instance — đăng ký thuộc VIEW-006.
UC traceability:  UC-019 (tạo version mới VÀ handoff), UC-002 (đăng ký qua VIEW-006 + chọn/pin qua
                  VIEW-001), UC-001 (Research loop-back entry, tuỳ chọn), UC-003 (commit-gate
                  verification), UC-021 (old-version evidence vẫn truy cập).
PR traceability:  PR-031 (version mới + VIEW-006 registration), PR-001, PR-016 (VIEW-006 registration +
                  VIEW-001 selection), PR-003, PR-015, PR-017 (SCR-001 loop-back + VIEW-002 guard),
                  PR-032 (VIEW-005 old-version access).
```

## 9. Cross-screen and cross-stage handoffs

Kế thừa nguyên vẹn `use-case-workflow.md` §7 (KHÔNG đổi semantics, CHỈ ánh xạ UX):

```text
Research → Replay:    SCR-001/VIEW-002 (exit: Strategy Instance pinned, verification PASSED) → SCR-002
                       (entry: Strategy Instance giữ nguyên, WF-INV-3/UX-INV-3).

Replay → Backtest:    SCR-002/VIEW-003 (exit) → SCR-003 (entry: Strategy Instance giữ nguyên). Hai
                       capability ĐỘC LẬP — KHÔNG hard precondition kỹ thuật (§7 use-case-workflow.md).

Backtest → Paper:     SCR-004/SCR-005 (exit: evaluable result đã xem, INFORM judgment DUY NHẤT) →
                       judgment gate người dùng → SCR-006 (entry: Strategy Instance pin cho Paper RIÊNG
                       BIỆT, qua VIEW-001 nếu chưa có, PLUS PAPER-context Decision lineage RIÊNG BIỆT
                       bắt buộc — xem FLOW-003). KHÔNG Backtest/Research Decision identity nào mang
                       sang PAPER.

Paper → Review:       SCR-006/SCR-007 (exit: ExecutionResult resolved) → SCR-008 (entry: causation
                       chain đầy đủ sẵn sàng).

Review → Improve:     SCR-008/SCR-009/VIEW-004 (exit: causation traced, state compared, correction
                       inspected nếu có) → SCR-010 (entry: quyết định người dùng tạo version mới).

Improve → Research:   SCR-010/SCR-011/VIEW-005 (exit: version mới tạo, evidence version cũ vẫn truy
                       cập qua identity — resolvability không phải guarantee tuyệt đối) → SCR-001 (quan
                       sát read-only TUỲ CHỌN, KHÔNG cần pin) → khi cần commit: VIEW-006 (đăng ký
                       Strategy Instance RIÊNG BIỆT gắn version mới, v0.3) → VIEW-001 (chọn/pin Instance
                       vừa đăng ký) → VIEW-002 (verification) — xem FLOW-006. VIEW-001 KHÔNG BAO GIỜ tự
                       tạo Strategy Instance.
```

## 10. Evidence and authority presentation model

**Mô hình nhãn bắt buộc, áp dụng nhất quán trên MỌI screen/view tại §7 (đóng UX-P-1):**

```text
Mode label:       Research | Replay | Backtest | Paper | Review | Improve — LUÔN hiển thị, xác định
                   NGUỒN GỐC evidence đang xem.

Authority label:   authoritative (recorded fact, Domain Contract-owned) |
                   non-PAPER simulated (Backtest evidence, product-required/domain-representation
                   deferred where applicable, §15) |
                   non-authoritative recomputation (Replay parity result, deterministic, KHÔNG tự động
                   trở thành authoritative) — LUÔN hiển thị CẠNH evidence, KHÔNG BAO GIỜ ẩn.

Representation label (CHỈ khi authority=non-PAPER simulated):
                   product-required, domain-representation deferred where applicable — disclose tường
                   minh rằng KHÔNG có Domain Contract Backtest chính thức, KHÔNG ngụ ý một entity/
                   schema đã tồn tại.
```

**Ba nguyên tắc phân tách bắt buộc (nhắc lại tường minh, áp dụng UX-wide):**

```text
1. Backtest evidence KHÔNG BAO GIỜ hiển thị như authoritative PAPER ExecutionResult/Fill/Position/
   submitted Order/exchange execution — dùng thuật ngữ mô tả (simulated economic evidence, exposure
   progression, strategy-level evaluable result), KHÔNG thuật ngữ domain đã đóng đinh.
2. Recorded authoritative Decision (SCR-002) và recomputed non-authoritative comparison result
   (VIEW-003) LUÔN hiển thị với nhãn tách biệt — KHÔNG BAO GIỜ trộn lẫn hình thức trình bày.
3. User-initiated intent (SCR-006, "yêu cầu khởi tạo") và system-owned authoritative execution (Trade
   Intent→...→Position) LUÔN phân biệt trực quan (UX-P-2) — KHÔNG form nào ngụ ý người dùng "điền"
   một Order authoritative.
```

## 11. Loading, empty, unavailable, blocked, failed and NON_EVALUABLE states

**Bảng `STATE-XXX` — 30 trạng thái presentation-only (UX state, KHÔNG domain state mới, UX-INV-9) — v0.3 thu hẹp `STATE-001`/`STATE-002` xuống ĐÚNG bounded material surface (đóng `P03C-MAJ-01`), thêm `STATE-028`/`STATE-029` (đóng `P03C-B-MAJ-01`). v0.4 thu hẹp thêm PR traceability của `STATE-001`/`STATE-002` (mỗi PR còn lại phải materially control state reason/retained context/absence/minimum-count/non-fabrication — KHÔNG còn PR nào giữ lại chỉ vì parent screen sở hữu nó), thêm `PR-014` vào `STATE-012`–`STATE-021` (explicit lifecycle-transition presentation, đóng `P03C-MAJ-01`). v0.5 sửa hai mapping không hợp lệ còn sót tại `STATE-002` — loại `PR-007`/`PR-032` (đóng `P03C-MAJ-01`, xem rationale bên dưới). **v0.6 — thêm `STATE-030` (CANDIDATE semantic clarification, KHÔNG Approved/Consolidated, pending Review A/Independent Review B — Product/UX semantic candidate requiring review, đây LÀ một catalogue amendment, KHÔNG mechanical/cosmetic) — biểu diễn outcome INDETERMINATE thứ ba cho VIEW-003 parity recomputation (`decision.md` §9a.6, `use-case-workflow.md` v0.7 UC-005).** Loading/empty KHÔNG còn dùng làm acceptance surface fallback cho behavior của screen đích — chỉ những screen mà Blueprint TƯỜNG MINH ghi "STATE-001 loading" tại field "Primary states" (§7), hoặc genuinely có collection/record rỗng, mới được liệt kê:**

| ID | State | UC traceability | PR traceability | Applicable screen/view |
|---|---|---|---|---|
| STATE-001 | loading (v0.4 — thu hẹp thêm, đóng `P03C-MAJ-01`; xem rationale bên dưới bảng) | UC-001 (SCR-001), UC-004 (SCR-002), UC-006 (SCR-003) | PR-003, PR-018 | SCR-001, SCR-002, SCR-003 (CHỈ ba — không còn 16) |
| STATE-002 | empty (v0.5 — thu hẹp thêm, đóng `P03C-MAJ-01`; xem rationale bên dưới bảng) | UC-007, UC-008, UC-009 (SCR-004), UC-010 (SCR-005), UC-012, UC-013, UC-014, UC-015 (SCR-007), UC-020 (SCR-011) | PR-021, PR-034 | SCR-004 (danh sách Backtest run rỗng — chưa run nào tồn tại), SCR-005 (dưới hai Backtest run hoàn tất để so sánh), SCR-007 (chưa Order/Fill nào tồn tại), SCR-011 (dưới hai Strategy Instance đã đăng ký để so sánh) |
| STATE-003 | invalid Instrument/Venue | UC-001, UC-011 | PR-003 | SCR-001, SCR-006 |
| STATE-004 | missing Strategy Instance | UC-002 | PR-001 | VIEW-001 |
| STATE-005 | missing historical evidence | UC-001, UC-006 | PR-015, PR-021 | SCR-001, SCR-003 |
| STATE-006 | Replay reference unavailable | UC-004 | PR-020 | SCR-002 |
| STATE-007 | parity match | UC-005 | PR-010, PR-019 | VIEW-003 |
| STATE-008 | parity mismatch | UC-005 | PR-010, PR-019 | VIEW-003 |
| STATE-009 | Backtest evidence insufficient | UC-007, UC-008, UC-009, UC-010 | PR-033, PR-034 | SCR-004, SCR-005 |
| STATE-010 | Backtest run identity unresolved | UC-007, UC-008, UC-009 | PR-021 | SCR-004 |
| STATE-011 | PAPER Decision lineage unavailable | UC-011 | PR-024 | SCR-006 |
| STATE-012 | Risk APPROVED | UC-011 | PR-006, PR-014 (v0.4 — explicit RiskEvaluation tri-state transition presentation, đóng `P03C-MAJ-01`) | SCR-006 |
| STATE-013 | Risk REJECTED | UC-011 | PR-006, PR-014 (v0.4) | SCR-006 |
| STATE-014 | Risk NON_EVALUABLE | UC-011 | PR-006, PR-014 (v0.4) | SCR-006 |
| STATE-015 | ExecutionResult EXECUTED | UC-012 | PR-007, PR-014 (v0.4), PR-024 | SCR-007 |
| STATE-016 | ExecutionResult NOT_EXECUTED | UC-012 | PR-007, PR-014 (v0.4), PR-024 | SCR-007 |
| STATE-017 | Fill absent | UC-013 | PR-014 (v0.4), PR-025 | SCR-007 |
| STATE-018 | Position FLAT | UC-014 | PR-014 (v0.4), PR-026 | SCR-007 |
| STATE-019 | Position LONG | UC-014 | PR-014 (v0.4), PR-026 | SCR-007 |
| STATE-020 | Position SHORT | UC-014 | PR-014 (v0.4), PR-026 | SCR-007 |
| STATE-021 | Position NON_EVALUABLE | UC-014 | PR-014 (v0.4), PR-026 | SCR-007 |
| STATE-022 | Research verification PASSED | UC-003 | PR-017 | VIEW-002 |
| STATE-023 | Research verification FAILED | UC-003 | PR-017 | VIEW-002 |
| STATE-024 | Research verification INDETERMINATE | UC-003 | PR-017 | VIEW-002 |
| STATE-025 | old-version evidence complete | UC-021 | PR-032 | VIEW-005 |
| STATE-026 | old-version evidence partially unavailable | UC-021 | PR-032 | VIEW-005 |
| STATE-027 | Live unauthorized | UC-011, UC-015 | PR-027 (`OQ-002` open) | WS-001 (global), SCR-006 |
| STATE-028 | Paper Strategy Instance not selected (v0.3, đóng `P03C-B-MAJ-01`) | UC-002, UC-011 | PR-001, PR-016 | SCR-006, VIEW-001 |
| STATE-029 | Paper Strategy Instance selected but not pinned (v0.3, đóng `P03C-B-MAJ-01`) | UC-002, UC-011 | PR-001, PR-016 | SCR-006, VIEW-001 |
| STATE-030 | parity indeterminate (v0.6, **CANDIDATE — Product/UX semantic candidate requiring review, KHÔNG Approved/Consolidated**) | UC-005 | PR-010, PR-019 | VIEW-003 |

**Rationale PR traceability `STATE-001`/`STATE-002` (v0.4/v0.5, đóng `P03C-MAJ-01`):**

```text
STATE-001 (loading) → PR-003, PR-018 (thu hẹp từ 9 xuống 2):
  PR-003 (Instrument/Venue trong tập đã đăng ký) = required context RETAINED trong lúc pending tại
    SCR-001/SCR-002 — context đó KHÔNG đổi/biến mất trong lúc chờ load.
  PR-018 (chọn canonical Replay Cursor, xem state tái dựng) = required context RETAINED trong lúc
    pending tại SCR-002 — giá trị cursor hiển thị tường minh trong lúc chờ (§12).
  Loại: PR-008/015/017/020/021/022/023 — TẤT CẢ về nội dung/guarantee CUỐI CÙNG hiển thị SAU khi
    load xong (no-look-ahead, no-side-effect, network-independence, run identity, version tuple) —
    KHÔNG phải thứ mà chính trạng thái loading (spinner/pending indicator) hiển thị hay kiểm soát.

STATE-002 (empty) → PR-021, PR-034 (v0.5 — thu hẹp thêm từ 4 xuống 2, đóng `P03C-MAJ-01`):
  PR-021 (SCR-004) = absence của record loại "stable Backtest run identity" — chính PR-021 định
    nghĩa identity đó, nên "chưa run nào tồn tại" là boundary case trực tiếp của PR-021.
  PR-034 (SCR-005) = "so sánh được kết quả đó với kết quả của Backtest run KHÁC" — trực tiếp đòi hỏi
    minimum-record-count (≥2 run) để so sánh có nghĩa.
  Loại (v0.5, sửa hai mapping không hợp lệ còn sót từ v0.4): PR-007 — acceptance evidence "với
    NOT_EXECUTED, người dùng thấy rõ zero Fill" mô tả outcome ExecutionResult NOT_EXECUTED của MỘT
    Order đã tồn tại (đã có STATE-016/STATE-017 riêng), KHÔNG phải trường hợp "chưa Order/Fill nào
    tồn tại" mà STATE-002 tại SCR-007 đại diện — hai khái niệm khác nhau, PR-007 không materially
    kiểm soát cái sau. PR-032 — governs truy vấn outcome xuyên suốt Strategy Definition Version CŨ
    (old-version querying, đã sở hữu bởi VIEW-005/STATE-025/STATE-026/NAV-006/FLOW-005/FLOW-006),
    KHÔNG phải minimum-record-count của Strategy Instance hiện tại để so sánh tại SCR-011 — hai
    concern khác nhau, PR-032 không materially kiểm soát cái sau.
  Loại (không đổi từ v0.4): PR-009/013/022/024/025/026/027/031/033 — nội dung/outcome CHI TIẾT của
    record MỘT KHI nó tồn tại (economics, Position value, version tuple, explainability, no-real-
    order guarantee) — KHÔNG phải sự vắng mặt/minimum-count của chính record đó.
```

**Nguyên tắc bắt buộc cho MỌI `STATE-XXX` "unavailable/blocked/failed":** đúng bốn nguyên tắc fallback đã pin tại `use-case-workflow.md` §8 — `workflow stops` / `state remains observable` / `reason is disclosed` / `no downstream authoritative action occurs`. KHÔNG UX state nào tự phát minh domain lifecycle transition để hỗ trợ hiển thị — `STATE-XXX` là presentation state, KHÔNG BAO GIỜ authoritative domain state (UX-INV-9).

## 12. Historical cursor and correction UX

**Hiển thị bắt buộc cho mọi historical view (SCR-002, SCR-009):**

```text
canonical Replay Cursor:        Giá trị cursor hiển thị tường minh (Chapter 8 §8.5) — người dùng luôn
                                 biết ĐANG xem tại thời điểm nào.
Effective historical context:   Fact có recorded_time ≤ cursor — hiển thị rõ boundary.
Recorded facts available:       Toàn bộ lineage Decision→...→Position TẠI cursor, KHÔNG latest-state.
No-look-ahead boundary:         Tường minh — KHÔNG fact nào có recorded_time > cursor được hiển thị.
Corrections recorded after
the cursor:                     Hiển thị RIÊNG (SCR-009 "khác biệt tường minh"), KHÔNG lẫn vào state
                                 tại cursor gốc.
```

**Correction UX (VIEW-004) — bắt buộc:**

```text
Original fact:                        LUÔN hiển thị, resolvable (append-only).
Invalidation/correction relationship: `supersedes_fact_ref` hiển thị tường minh — liên kết trực tiếp.
Replacement fact khi present:         Hiển thị cạnh fact gốc, KHÔNG thay thế im lặng.
Giá trị visible tại cursor nào:       Rõ ràng — SCR-002 tại cursor T chỉ thấy fact có recorded_time ≤
                                       T; correction ghi SAU T KHÔNG visible tại T.
```

TUYỆT ĐỐI KHÔNG thiết kế UI thay thế fact gốc im lặng, hoặc chỉ hiển thị giá trị đã sửa mà không có lineage (UX-INV-6).

## 13. Strategy-version comparison UX

Kế thừa nguyên vẹn SCR-011/VIEW-005 (§7.6) — tóm tắt:

```text
Ba chế độ (UC-020):        Backtest vs Backtest | PAPER vs PAPER | cross-mode side-by-side.
Cross-mode labeling:       mode, authority, evidence type, Strategy Instance identity, Strategy
                            Definition Version identity — TẤT CẢ hiển thị RIÊNG cho mỗi bên.
Cấm tường minh:            unified outcome card; single normalized score; common execution result;
                            authority-equivalent comparison; automatic cross-mode ranking.
Old-version access:        VIEW-005 — danh tính version LUÔN hiển thị; hai họ evidence resolve ĐỘC
                            LẬP; missing evidence identify theo TỪNG họ/loại — KHÔNG ngụ ý toàn bộ
                            lịch sử mất.
OQ-003:                     Vẫn `Open` — KHÔNG threshold/target/scoring formula nào được hiển thị như
                            KPI chính thức.
```

## 14. Traceability matrices

**v0.4 — narrowed further, đóng `P03C-MAJ-01` (traceability-only, KHÔNG behavior change).** v0.3 đã thu hẹp union gần-toàn-bộ của v0.2 nhưng vẫn giữ lại một số mapping chỉ vì "parent screen sở hữu PR đó" thay vì vì state/artifact TỰ NÓ materially hiển thị/kiểm soát requirement. v0.4 review độc lập từng PR tại `STATE-001`/`STATE-002` (thu hẹp thêm) và gán `PR-004`/`PR-005`/`PR-014` (trước đây "không có UX acceptance surface") vào đúng SCR/VIEW nào MATERIALLY hiển thị outcome/evidence-trace/lifecycle-transition mà chúng yêu cầu.

**Quy tắc chất lượng traceability (giữ nguyên nguyên văn từ v0.3, SIẾT CHẶT áp dụng — KHÔNG thêm ngoại lệ cho loading/empty):**

```text
Một parent screen sở hữu một requirement KHÔNG tự động khiến MỌI presentation state của screen đó
trở thành acceptance surface cho requirement đó.

Presence trong một destination, transient state, hoặc parent journey KHÔNG tự nó tạo material
ownership đối với detailed requirement của destination đó. Một PR/UC chỉ được cite tại một artifact
khi artifact đó THỰC SỰ hiển thị/kiểm soát/gate hành vi mà PR/UC đó yêu cầu — KHÔNG phải vì artifact
đó "đi qua" hoặc "chứa" một destination sở hữu PR/UC đó.

Một STATE chỉ map vào requirement materially kiểm soát: state reason / retained context / blocked
hoặc unavailable action / incompleteness / observability / non-fabrication. Detailed outcome,
evidence, và lifecycle requirement vẫn map vào đúng SCR/VIEW/STATE artifact THỰC SỰ hiển thị chúng —
KHÔNG map vào generic loading/empty state chỉ vì screen đó sở hữu requirement.
```

**14a. WS → UC/PR**

| ID | UC traceability | PR traceability |
|---|---|---|
| WS-001 | UC-001, UC-002, UC-004, UC-011, UC-015, UC-017 | PR-001, PR-002, PR-003, PR-008, PR-012, PR-016, PR-027, PR-029 |

**14b. NAV → UC/PR**

| ID | UC traceability | PR traceability |
|---|---|---|
| NAV-001 | UC-001 | PR-003, PR-015, PR-017 |
| NAV-002 | UC-002, UC-004 | PR-001, PR-008, PR-016, PR-018, PR-020 |
| NAV-003 | UC-002, UC-006 | PR-001, PR-016, PR-021, PR-022, PR-023 |
| NAV-004 | UC-002, UC-011 | PR-001, PR-006, PR-007, PR-016, PR-024 |
| NAV-005 | UC-016, UC-017, UC-018 | PR-011, PR-028, PR-029, PR-030 |
| NAV-006 | UC-002, UC-019, UC-020, UC-021 | PR-001, PR-016, PR-031, PR-032 |

**14c. SCR/VIEW → UC/PR**

| ID | UC traceability | PR traceability |
|---|---|---|
| SCR-001 | UC-001 | PR-003, PR-015, PR-017 |
| VIEW-001 | UC-002, UC-011 | PR-001, PR-016 |
| VIEW-002 | UC-003 | PR-017 |
| SCR-002 | UC-004 | PR-008, PR-018, PR-020 |
| VIEW-003 | UC-005 | PR-010, PR-019 |
| SCR-003 | UC-006 | PR-021, PR-022, PR-023 |
| SCR-004 | UC-007, UC-008, UC-009 | PR-004, PR-005, PR-009, PR-021, PR-022, PR-033, PR-034 |
| SCR-005 | UC-010 | PR-034 |
| SCR-006 | UC-002, UC-011 | PR-001, PR-004, PR-005, PR-006, PR-007, PR-014, PR-016, PR-024 |
| SCR-007 | UC-012, UC-013, UC-014, UC-015 | PR-007, PR-013, PR-014, PR-024, PR-025, PR-026, PR-027 |
| SCR-008 | UC-016 | PR-004, PR-005, PR-028 |
| SCR-009 | UC-017 | PR-029 |
| VIEW-004 | UC-018 | PR-011, PR-030 |
| SCR-010 | UC-019 | PR-031 |
| VIEW-006 | UC-002, UC-019 | PR-001, PR-016, PR-031 |
| SCR-011 | UC-020 | PR-031, PR-032 |
| VIEW-005 | UC-021 | PR-032 |

Mọi `UC-001`–`UC-021` xuất hiện trong ít nhất một SCR/VIEW primary. VIEW-001 và SCR-006 chia sẻ UC-002/UC-011 vì v0.3 mở rộng Strategy Instance pin sang Paper (đóng `P03C-B-MAJ-01`); VIEW-006 chia sẻ UC-002/UC-019 vì nó là bounded handoff giữa hai UC đó (đóng `P03C-B-MAJ-02`); SCR-004: UC-007/008/009; SCR-007: UC-012–015 — mỗi UC vẫn có behavior quan sát được RIÊNG, đúng field "Information displayed"/"Primary states" tại §7. v0.4: SCR-004/SCR-006/SCR-008 thêm PR-004/PR-005 (Decision outcome + evidence trace materially hiển thị tại field "Information displayed"/"Evidence consumed" — xem §7); SCR-006/SCR-007 thêm PR-014 (explicit lifecycle-transition — Risk/ExecutionResult/Position tri-state/multi-state tại field "Primary/blocked states").

**14d. FLOW → UC/PR**

| ID | UC traceability | PR traceability |
|---|---|---|
| FLOW-001 | UC-001–UC-021 (toàn bộ — hợp lệ vì FLOW-001 CHÍNH LÀ primary end-to-end journey, không phải fallback coverage) | PR-001, PR-003, PR-015, PR-016, PR-017, PR-024, PR-028, PR-031, PR-034 (thu hẹp còn ĐÚNG PR biểu diễn stage-ordering/gate/handoff của flow, KHÔNG union chi tiết child-screen — không đổi từ v0.3, PR-004/005/014 KHÔNG material ở tầng flow-transition) |
| FLOW-002 | UC-002 | PR-001, PR-016 |
| FLOW-003 | UC-009, UC-010, UC-011 | PR-024, PR-034 |
| FLOW-004 | UC-011, UC-012, UC-013, UC-014 | PR-006, PR-007, PR-024, PR-025, PR-026 |
| FLOW-005 | UC-020, UC-021 | PR-031, PR-032 |
| FLOW-006 | UC-001, UC-002, UC-003, UC-019, UC-021 | PR-001, PR-003, PR-015, PR-016, PR-017, PR-031, PR-032 |

**14e. STATE → UC/PR** (condensed direct duplicate của bảng đầy đủ §11 — KHÔNG "see" reference; v0.4 thu hẹp thêm STATE-001/STATE-002, thêm PR-014 vào STATE-012–STATE-021; v0.6 thêm STATE-030, CANDIDATE)

```text
STATE-001 → UC-001,004,006 / PR-003,018
STATE-002 → UC-007,008,009,010,012,013,014,015,020 / PR-021,034
STATE-003 → UC-001,011 / PR-003              STATE-017 → UC-013 / PR-014,025
STATE-004 → UC-002 / PR-001                  STATE-018 → UC-014 / PR-014,026
STATE-005 → UC-001,006 / PR-015,021          STATE-019 → UC-014 / PR-014,026
STATE-006 → UC-004 / PR-020                  STATE-020 → UC-014 / PR-014,026
STATE-007 → UC-005 / PR-010,019              STATE-021 → UC-014 / PR-014,026
STATE-008 → UC-005 / PR-010,019              STATE-022 → UC-003 / PR-017
STATE-009 → UC-007,008,009,010 / PR-033,034  STATE-023 → UC-003 / PR-017
STATE-010 → UC-007,008,009 / PR-021          STATE-024 → UC-003 / PR-017
STATE-011 → UC-011 / PR-024                  STATE-025 → UC-021 / PR-032
STATE-012 → UC-011 / PR-006,014              STATE-026 → UC-021 / PR-032
STATE-013 → UC-011 / PR-006,014              STATE-027 → UC-011,015 / PR-027
STATE-014 → UC-011 / PR-006,014              STATE-028 → UC-002,011 / PR-001,016
STATE-015 → UC-012 / PR-007,014,024          STATE-029 → UC-002,011 / PR-001,016
STATE-016 → UC-012 / PR-007,014,024          STATE-030 → UC-005 / PR-010,019 (v0.6, CANDIDATE)
```

**14f. UC → UX artifacts** (nghịch đảo 14a–14e, xác nhận đầy đủ `UC-001`–`UC-021` — không đổi từ v0.3, v0.4 chỉ sửa PR; v0.6 thêm STATE-030 vào UC-005, CANDIDATE)

```text
UC-001 → FLOW-001, FLOW-006, NAV-001, SCR-001, STATE-001, STATE-003, STATE-005, WS-001
UC-002 → FLOW-001, FLOW-002, FLOW-006, NAV-002, NAV-003, NAV-004, NAV-006, SCR-006, STATE-004,
          STATE-028, STATE-029, VIEW-001, VIEW-006, WS-001
UC-003 → FLOW-001, FLOW-006, STATE-022, STATE-023, STATE-024, VIEW-002
UC-004 → FLOW-001, NAV-002, SCR-002, STATE-001, STATE-006, WS-001
UC-005 → FLOW-001, STATE-007, STATE-008, STATE-030, VIEW-003
UC-006 → FLOW-001, NAV-003, SCR-003, STATE-001, STATE-005
UC-007 → FLOW-001, SCR-004, STATE-002, STATE-009, STATE-010
UC-008 → FLOW-001, SCR-004, STATE-002, STATE-009, STATE-010
UC-009 → FLOW-001, FLOW-003, SCR-004, STATE-002, STATE-009, STATE-010
UC-010 → FLOW-001, FLOW-003, SCR-005, STATE-002, STATE-009
UC-011 → FLOW-001, FLOW-003, FLOW-004, NAV-004, SCR-006, STATE-003, STATE-011, STATE-012, STATE-013,
          STATE-014, STATE-027, STATE-028, STATE-029, VIEW-001, WS-001
UC-012 → FLOW-001, FLOW-004, SCR-007, STATE-002, STATE-015, STATE-016
UC-013 → FLOW-001, FLOW-004, SCR-007, STATE-002, STATE-017
UC-014 → FLOW-001, FLOW-004, SCR-007, STATE-002, STATE-018, STATE-019, STATE-020, STATE-021
UC-015 → FLOW-001, SCR-007, STATE-002, STATE-027, WS-001
UC-016 → FLOW-001, NAV-005, SCR-008
UC-017 → FLOW-001, NAV-005, SCR-009, WS-001
UC-018 → FLOW-001, NAV-005, VIEW-004
UC-019 → FLOW-001, FLOW-006, NAV-006, SCR-010, VIEW-006
UC-020 → FLOW-001, FLOW-005, NAV-006, SCR-011, STATE-002
UC-021 → FLOW-001, FLOW-005, FLOW-006, NAV-006, STATE-025, STATE-026, VIEW-005
```

**14g. PR → UX artifacts** (nghịch đảo 14a–14e, xác nhận đầy đủ `PR-001`–`PR-034`; v0.4 gán `PR-004`/`PR-005`/`PR-014` vào acceptance surface THỰC SỰ — xem rationale tại §11 và field PR traceability của SCR-004/006/007/008 tại §7. Sau v0.4, TẤT CẢ 34 PR có ít nhất một acceptance surface direct — không còn PR nào "upstream invariant without surface". v0.6 thêm STATE-030 vào PR-010/PR-019, CANDIDATE)

```text
PR-001 → FLOW-001, FLOW-002, FLOW-006, NAV-002, NAV-003, NAV-004, NAV-006, SCR-006, STATE-004,
          STATE-028, STATE-029, VIEW-001, VIEW-006, WS-001
PR-002 → WS-001
PR-003 → FLOW-001, FLOW-006, NAV-001, SCR-001, STATE-001, STATE-003, WS-001
PR-004 → SCR-004, SCR-006, SCR-008 (v0.4, mới — Decision outcome hiển thị tường minh)
PR-005 → SCR-004, SCR-006, SCR-008 (v0.4, mới — evidence trace đầy đủ hiển thị tường minh)
PR-006 → FLOW-004, NAV-004, SCR-006, STATE-012, STATE-013, STATE-014
PR-007 → FLOW-004, NAV-004, SCR-006, SCR-007, STATE-015, STATE-016
PR-008 → NAV-002, SCR-002, WS-001
PR-009 → SCR-004
PR-010 → STATE-007, STATE-008, STATE-030, VIEW-003
PR-011 → NAV-005, VIEW-004
PR-012 → WS-001
PR-013 → SCR-007
PR-014 → SCR-006, SCR-007, STATE-012, STATE-013, STATE-014, STATE-015, STATE-016, STATE-017,
          STATE-018, STATE-019, STATE-020, STATE-021 (v0.4, mới — explicit lifecycle-transition
          presentation)
PR-015 → FLOW-001, FLOW-006, NAV-001, SCR-001, STATE-005
PR-016 → FLOW-001, FLOW-002, FLOW-006, NAV-002, NAV-003, NAV-004, NAV-006, SCR-006, STATE-028,
          STATE-029, VIEW-001, VIEW-006, WS-001
PR-017 → FLOW-001, FLOW-006, NAV-001, SCR-001, STATE-022, STATE-023, STATE-024, VIEW-002
PR-018 → NAV-002, SCR-002, STATE-001
PR-019 → STATE-007, STATE-008, STATE-030, VIEW-003
PR-020 → NAV-002, SCR-002, STATE-006
PR-021 → NAV-003, SCR-003, SCR-004, STATE-002, STATE-005, STATE-010
PR-022 → NAV-003, SCR-003, SCR-004
PR-023 → NAV-003, SCR-003
PR-024 → FLOW-001, FLOW-003, FLOW-004, NAV-004, SCR-006, SCR-007, STATE-011, STATE-015, STATE-016
PR-025 → FLOW-004, SCR-007, STATE-017
PR-026 → FLOW-004, SCR-007, STATE-018, STATE-019, STATE-020, STATE-021
PR-027 → SCR-007, STATE-027, WS-001
PR-028 → FLOW-001, NAV-005, SCR-008
PR-029 → NAV-005, SCR-009, WS-001
PR-030 → NAV-005, VIEW-004
PR-031 → FLOW-001, FLOW-005, FLOW-006, NAV-006, SCR-010, SCR-011, VIEW-006
PR-032 → FLOW-005, FLOW-006, NAV-006, SCR-011, STATE-025, STATE-026, VIEW-005
PR-033 → SCR-004, STATE-009
PR-034 → FLOW-001, FLOW-003, SCR-004, SCR-005, STATE-002, STATE-009
```

**14h. Lifecycle Stage → Screens/Views** (bổ sung, không phải một trong bảy ma trận bắt buộc)

```text
Research  → SCR-001, VIEW-001, VIEW-002
Replay    → SCR-002, VIEW-003
Backtest  → SCR-003, SCR-004, SCR-005
Paper     → SCR-006, SCR-007
Review    → SCR-008, SCR-009, VIEW-004
Improve   → SCR-010, VIEW-006, SCR-011, VIEW-005
```

**14i. Screen/View → Domain vocabulary** — xem field "Domain vocabulary referenced" trong từng khối tại §7 (đầy đủ, không lặp lại).

**14j. Deferred dependency → affected screens/views** — xem §15.

## 15. Deferred dependencies and Open Questions

```text
Backtest domain representation:
  Status:              Deferred (không đổi từ product-requirement.md/use-case-workflow.md).
  Affected screens:     SCR-003, SCR-004, SCR-005, SCR-011 (Backtest panel), VIEW-005 (Backtest family).
  UX may display now:   simulated economic evidence, exposure/position progression, strategy-level
                        evaluable result — dùng thuật ngữ mô tả, gắn nhãn "product-required, domain-
                        representation deferred" (§10).
  UX must not invent:   BacktestOrder/BacktestFill/BacktestPosition/BacktestExecutionResult hay tương
                        đương; simulation algorithm; fee/slippage/accounting/PnL formula.
  Blocks later
  implementation:       Domain Contract cho Backtest (nếu Product Owner quyết định author) sẽ định
                        nghĩa representation chính xác — Phase 1 KHÔNG được tự suy diễn schema từ UX
                        này.

Research domain representation:
  Status:              KHÔNG cần standalone Research entity (không đổi).
  Affected screens:     SCR-001, VIEW-001, VIEW-002.
  UX may display now:   Quan sát thuần túy trên Domain Contract đã có (candle.md…context.md,
                        strategy.md); verification result tri-state (VIEW-002).
  UX must not invent:   Entity/event "Research"/"ResearchVerification" riêng.
  Blocks later
  implementation:       KHÔNG — Research luôn resolve qua Domain Contract hiện có.

PAPER-context authoritative Decision establishment mechanism:
  Status:              Deferred (không đổi).
  Affected screens:     SCR-006 (Paper Execution Initiation).
  UX may display now:   "Paper entry available" / "Paper entry blocked: no eligible PAPER-context
                        Decision lineage" (STATE-011) — KHÔNG cơ chế cụ thể.
  UX must not invent:   Action "Execute this Backtest Decision in Paper"/"Promote to Paper"/"Convert
                        Backtest Decision"; bất kỳ workflow ngầm nào tạo PAPER-context Decision từ
                        Backtest/Research.
  Blocks later
  implementation:       Cơ chế chính xác (trigger, ai/cái gì ghi nhận PAPER-context Decision) là
                        Product Owner decision/Domain Contract correction tương lai — Phase 1 KHÔNG
                        được tự thiết kế cơ chế này từ UX Blueprint.

OQ-002 (Live-gate):
  Status:              Open.
  Affected screens:     WS-001 (global label), SCR-006.
  UX may display now:   "Live: Unauthorized" (STATE-027) — nhãn tĩnh, KHÔNG action nào dẫn tới Live.
  UX must not invent:   Live execution UX, Live-gate criteria, điều kiện chuyển Live.
  Blocks later
  implementation:       Live UX/architecture CHỈ được author sau khi OQ-002 đóng qua ADR (Phase 3,
                        theo MANIFEST Open Questions).

OQ-003 (Product Metrics):
  Status:              Open.
  Affected screens:     SCR-004, SCR-005, SCR-009, SCR-011 (mọi nơi hiển thị "evaluable result"/so
                        sánh).
  UX may display now:   Evidence đo lường được (evaluable result, so sánh side-by-side) — KHÔNG
                        threshold/target/scoring formula.
  UX must not invent:   Concrete KPI, unified score, automatic ranking.
  Blocks later
  implementation:       Product Metrics document riêng (Vision §1.8) sẽ định nghĩa formula — Phase 1
                        KHÔNG được tự suy diễn từ UX này.
```

## 16. Explicit Non-Goals and Out-of-Scope

Kế thừa nguyên vẹn [`product-requirement.md`](./product-requirement.md) §11/§12 VÀ [`use-case-workflow.md`](./use-case-workflow.md) §11 — KHÔNG lặp lại toàn văn.

**Ngoài phạm vi tường minh của riêng tài liệu này (Package 0.3-C):**

- Pixel dimension, visual branding, exact color, font choice, production component code, CSS, frontend framework — thuộc Figma-level prototype/Phase 1 implementation, KHÔNG author tại đây.
- API contract, database query, backend service, event transport, deployment topology — Phase 1 architecture.
- Security, custody, deployment.
- Retention/archive/retrieval/storage architecture.
- Multi-tenant administration, organization switching, public profile, community/chat, signal marketplace, multi-asset UX, Live execution UX (§2).
- Domain Contract state/authority/cardinality/transition mới — mọi UX element CHỈ tham chiếu state machine đã `Consolidated Stable`.
- Backtest/Replay domain fact mới (`BacktestOrder`/`BacktestFill`/`BacktestPosition`/`BacktestExecutionResult`/`ReplayDecision`/`ResearchVerification` hay tương đương).
- Unified Backtest/PAPER outcome model; automatic normalization/scoring/ranking.
- Product requirement/Use Case mới — mọi UX element CHỈ dùng `PR-XXX`/`UC-XXX` đã tồn tại.
- (v0.3) `PaperSession` entity, session identifier, session storage, timeout, persistence mechanism, backend lifecycle cho Strategy Instance pin — CHỈ ranh giới UX-visible (§3) được định nghĩa.
- (v0.3) Schema/field/validation/API/database/command/event implementation cho Strategy Instance registration (`VIEW-006`) — CHỈ bounded product handoff được định nghĩa.
- (v0.3) Permission architecture, route guard, authorization middleware, session token cho bất kỳ blocked/read-only distinction nào (`UX-P-5`, `NAV-XXX`).

## 17. Package 0.3-C acceptance criteria

```text
1. Toàn bộ 18 mục nội dung bắt buộc (§1–§18, bao gồm §5a — sáu đặc tả NAV first-class, v0.2) có mặt và
   đầy đủ.
2. Tất cả 21 Use Case (UC-001–UC-021) có UX coverage — xác nhận tại §14f (UC → UX artifacts).
3. Mọi UX artifact (WS/NAV/SCR/VIEW/FLOW/STATE) truy vết TRỰC TIẾP, CHÍNH XÁC, BOUNDED, materially
   applicable/controlling một hoặc nhiều UC-XXX VÀ một hoặc nhiều PR-XXX (v0.3 — không còn "cross-
   cutting"/wording gián tiếp LẪN không còn generic-artifact-as-fallback-coverage; presence trong một
   destination/transient state/parent journey KHÔNG tự tạo material ownership, §14) — không phần tử
   nào tồn tại chỉ vì "seems useful."
4. KHÔNG product requirement hay Use Case behavior mới nào tồn tại — không PR-XXX/UC-XXX mới được tạo.
5. Replay authority (historical reconstruction, SCR-002) và parity (non-authoritative recomputation,
   VIEW-003) hiển thị tách biệt tường minh — nhãn mode/authority riêng.
6. Backtest (non-PAPER simulated, SCR-003/004/005) và PAPER (authoritative, SCR-006/007) authority
   hiển thị tách biệt tường minh trên mọi screen liên quan.
7. Paper entry (SCR-006) KHÔNG BAO GIỜ promote một Backtest/Research Decision — PAPER-context Decision
   lineage luôn RIÊNG BIỆT.
8. User initiation (SCR-006, "yêu cầu khởi tạo") và system-owned execution authority (Trade Intent→...
   →Position) hiển thị phân biệt trực quan (UX-P-2).
9. Cross-mode evidence (SCR-011) KHÔNG BAO GIỜ unified — mỗi họ giữ nhãn mode/authority/evidence-type
   riêng.
10. Research verification (VIEW-002) có đủ ba outcome PASSED/FAILED/INDETERMINATE (STATE-022/023/024).
11. Old-version evidence families (VIEW-005) — Backtest và PAPER — resolve ĐỘC LẬP, KHÔNG gộp.
12. Evidence không đầy đủ (STATE-026) LUÔN hiển thị "incomplete" tường minh — KHÔNG BAO GIỜ trình bày
    như hoàn chỉnh.
13. No-repaint (VIEW-004) và historical cursor (SCR-002/SCR-009) behavior được đại diện đầy đủ tại §12.
14. NON_EVALUABLE state (STATE-021 Position, và tương tự) được đại diện tường minh, KHÔNG chọn một
    Fill/aggregate ngầm.
15. Live hiển thị `Unauthorized` (STATE-027) xuyên suốt — KHÔNG action/screen nào dẫn tới Live.
16. `OQ-002`/`OQ-003` giữ nguyên `Open` — không bị đóng ngầm bởi bất kỳ UX label/flow nào.
17. KHÔNG API/database/backend/frontend/infrastructure semantics nào được giới thiệu — §7 CHỈ mô tả
    behavior, KHÔNG component code/pixel/branding.
18. YAML frontmatter hợp lệ, `version: "0.6"`, `status: Draft`, `approved_by: null`, `approved_at: null`
    — Package 0.3-C vẫn Draft, KHÔNG `Consolidated Stable`. `STATE-030` (v0.6) là CANDIDATE, pending
    Review A/Independent Review B — KHÔNG tính là đã Consolidated cùng 29 STATE trước đó.
19. Paper Strategy Instance binding (v0.3): SCR-006/SCR-007 hiển thị tường minh danh tính Strategy
    Instance/Version pin trước khi resolve PAPER Decision lineage và xuyên suốt C7 inspection; bốn
    nguyên nhân blocked (STATE-003/028/029/011) LUÔN phân biệt tường minh, KHÔNG BAO GIỜ gộp; KHÔNG
    PaperSession entity/session/storage/timeout nào được định nghĩa.
20. Strategy Instance creation UX (v0.3): VIEW-006 sở hữu đăng ký Strategy Instance gắn Strategy
    Definition Version mới; VIEW-001 KHÔNG BAO GIỜ tự tạo Instance — CHỈ chọn/pin Instance đã đăng ký.
21. Baseline sẵn sàng cho ChatGPT Final Delta Review A + Independent Review B trên CÙNG một commit/blob.
```

## 18. Phase 1 handoff requirements

Phase 1 (System/UX Architecture, `/docs/architecture/`, chưa bắt đầu) PHẢI, khi tiêu thụ tài liệu này:

1. Tham chiếu mọi component/API/data-model quyết định về đúng một hoặc nhiều `WS-XXX`/`NAV-XXX`/`SCR-XXX`/`VIEW-XXX`/`FLOW-XXX`/`STATE-XXX` ID tại đây — KHÔNG tự phát minh UX behavior mới ở tầng architecture mà không truy vết ngược `UC-XXX`/`PR-XXX`.
2. KHÔNG tự suy diễn cơ chế cho bất kỳ deferred dependency nào tại §15 (Backtest domain representation, PAPER-context Decision establishment, OQ-002, OQ-003) — những quyết định đó thuộc Product Owner/Domain Contract correction tương lai, KHÔNG phải Phase 1 tự quyết.
3. Giữ nguyên MỌI ranh giới authority đã pin tại §10 (Replay historical reconstruction vs parity recomputation; Backtest non-PAPER vs PAPER authoritative; user intent vs system-owned execution) khi thiết kế API/data contract — KHÔNG API nào được thiết kế theo cách ngầm hợp nhất hai authority tách biệt.
4. KHÔNG author security/custody/deployment/retention/storage architecture dựa trên suy diễn từ UX Blueprint này mà không có quyết định Product Owner/ADR riêng.
5. Giữ nguyên walking-skeleton operating scope (§2) — KHÔNG mở rộng multi-tenant/multi-asset/Live UX khi thiết kế architecture cho Phase 1 walking-skeleton đầu tiên.
6. Xác nhận Live vẫn `Unauthorized` — KHÔNG architecture Live nào được author cho tới khi `OQ-002` đóng qua ADR.
