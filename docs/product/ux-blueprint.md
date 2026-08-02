---
id: ux-blueprint
title: UX Blueprint
version: "0.1"
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

> **Vai trò của tài liệu này:** Artifact thứ ba và cuối cùng của Package 0.3-C (Phase 0.3 — Product Requirement · Use Case & Workflow · UX Blueprint), phụ thuộc trực tiếp [`product-requirement.md`](./product-requirement.md) v0.2 Draft (Package 0.3-A, `Consolidated Stable`) VÀ [`use-case-workflow.md`](./use-case-workflow.md) v0.3 Draft (Package 0.3-B, `Consolidated Stable`). Dịch 21 Use Case (`UC-001`–`UC-021`) thành UX representation — workspace, navigation, screen, view, panel, flow, action, state, handoff — cho hành vi ĐÃ được `product-requirement.md`/`use-case-workflow.md` kiểm soát. Draft, chưa Approved/Locked, **chưa `Consolidated Stable`**. Tài liệu này KHÔNG tạo product behavior/requirement/domain semantics mới — MỌI workspace/navigation item/screen/view/panel/flow/action/state/handoff PHẢI truy vết về một hoặc nhiều `UC-XXX` VÀ một hoặc nhiều `PR-XXX` đã tồn tại. KHÔNG sở hữu pixel dimension/visual branding/production component code (Phase 1 Figma-level prototype); KHÔNG sở hữu domain semantics (thuộc `/docs/domain/`, không sửa); KHÔNG sở hữu architecture (Phase 1, `/docs/architecture/`).

**Authority boundary:** tài liệu này sở hữu **UX representation content** cho Phase 0.3 — KHÔNG sở hữu product requirement content (thuộc `product-requirement.md`, Package 0.3-A, không sửa), KHÔNG sở hữu use-case/workflow content (thuộc `use-case-workflow.md`, Package 0.3-B, không sửa), KHÔNG sở hữu domain semantics/state machine/authority/cardinality/transition (thuộc `/docs/domain/`, không sửa/redefine), KHÔNG sở hữu architecture quyết định (Phase 1, `/docs/architecture/`), KHÔNG đóng Open Question nào (`OQ-002`/`OQ-003` vẫn `Open`, xem §15), KHÔNG authorize Live, KHÔNG tuyên bố Phase 0.3/Phase 0 hoàn thành, KHÔNG mark chính nó `Consolidated Stable`.

**Quy tắc traceability nguồn (kế thừa nguyên vẹn `product-requirement.md`/`use-case-workflow.md`):** mọi UX element PHẢI có một hoặc nhiều `UC-XXX` VÀ một hoặc nhiều `PR-XXX` áp dụng. Không nơi nào một UX element tồn tại chỉ vì "seems useful." Nơi KHÔNG có `UC`/`PR` nào authorize hành vi: (a) KHÔNG thêm nó, HOẶC (b) đánh dấu tường minh như một deferred dependency (§15) — KHÔNG BAO GIỜ tự phát minh. KHÔNG `UC-XXX`/`PR-XXX` ID mới nào được tạo tại đây.

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
UX-INV-3   Strategy Instance context, một khi pin cho phiên Research/Replay/Backtest, hiển
           thị READ-ONLY (không đổi giữa chừng) cho tới khi phiên kết thúc.                    (WF-INV-3)
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
```

## 4. Information architecture

```text
Ride Workspace (WS-001)
│
├── Global context bar (Account · Instrument/Venue · Strategy Instance · historical cursor khi áp dụng)
│
├── NAV-001 Research
│     SCR-001 Market Analysis Workspace          (UC-001)
│     VIEW-001 Strategy Instance Selector         (UC-002, global panel, truy cập được từ mọi stage)
│     VIEW-002 Research Verification Result       (UC-003)
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
      SCR-011 Strategy Version Comparison             (UC-020)
      VIEW-005 Old-Version Evidence Access            (UC-021)
```

Thông tin kiến trúc này TRỰC TIẾP ánh xạ sáu-giai-đoạn (`use-case-workflow.md` §4) — KHÔNG thêm giai đoạn/workspace/navigation destination nào ngoài sáu giai đoạn đã `Consolidated Stable`.

## 5. Global workspace/navigation model

**WS-001 — Ride Workspace Shell**
```text
Global navigation:            NAV-001..006 — sáu lifecycle stage, thứ tự cố định
                               Research → Replay → Backtest → Paper → Review → Improve.
Current Account context:       Hiển thị READ-ONLY (một Account duy nhất, UX-INV-1). KHÔNG
                               Account-switching UI — chưa có UC/PR nào authorize hành vi đó.
Instrument/Venue context:      Selector, giới hạn TradableListing đã đăng ký (UX-INV-2, UC-001/
                               UC-011).
Strategy Instance context:     Selector/pin (VIEW-001, UC-002) — READ-ONLY một khi phiên Research/
                               Replay/Backtest đã bắt đầu (UX-INV-3).
Lifecycle-stage navigation:    NAV-001..006, luôn hiển thị, cho phép chuyển giữa các giai đoạn (KHÔNG
                               ép buộc thứ tự kỹ thuật — Replay/Backtest độc lập, §9).
Evidence/authority labels:     Nhãn mode + authority nhất quán trên MỌI evidence hiển thị (UX-P-1) —
                               xem §10 cho mô hình đầy đủ.
Historical cursor context:     Hiển thị khi đang ở Replay (SCR-002)/Review (SCR-009) — canonical
                               Replay Cursor value + effective historical context (§12).
Blocked/unavailable-state
presentation:                  Nhất quán xuyên suốt mọi STATE-XXX (§11) — reason luôn disclosed.
```

**Account-switching — tường minh KHÔNG thêm:** đúng chỉ dẫn "Do not add Account-switching behavior unless directly authorized" — chưa `UC-XXX`/`PR-XXX` nào authorize multi-Account UX; Account context tại đây CHỈ hiển thị (first-class, read-only), KHÔNG switcher.

## 6. Screen and view catalogue

| ID | Name | Stage | UC(s) | Primary PR(s) |
|---|---|---|---|---|
| SCR-001 | Market Analysis Workspace | Research | UC-001 | PR-003, PR-015, PR-017 |
| VIEW-001 | Strategy Instance Selector | Research (global) | UC-002 | PR-001, PR-016 |
| VIEW-002 | Research Verification Result | Research | UC-003 | PR-017 |
| SCR-002 | Replay Cursor & Historical Reconstruction | Replay | UC-004 | PR-008, PR-018, PR-020 |
| VIEW-003 | Parity Recomputation Result | Replay | UC-005 | PR-010, PR-019 |
| SCR-003 | Backtest Run Setup | Backtest | UC-006 | PR-021, PR-022, PR-023 |
| SCR-004 | Backtest Run Detail | Backtest | UC-007, UC-008, UC-009 | PR-009, PR-021, PR-022, PR-033, PR-034 |
| SCR-005 | Backtest Run Comparison | Backtest | UC-010 | PR-034 |
| SCR-006 | Paper Execution Initiation | Paper | UC-011 | PR-007, PR-024 |
| SCR-007 | Paper Order/Execution Detail | Paper | UC-012, UC-013, UC-014, UC-015 | PR-007, PR-024, PR-025, PR-026, PR-027 |
| SCR-008 | Decision → Position Lineage Trace | Review | UC-016 | PR-028 |
| SCR-009 | Historical State Comparison | Review | UC-017 | PR-029 |
| VIEW-004 | Correction Inspection | Review | UC-018 | PR-011, PR-030 |
| SCR-010 | Strategy Definition Version Creation | Improve | UC-019 | PR-031 |
| SCR-011 | Strategy Version Comparison | Improve | UC-020 | PR-031, PR-032 |
| VIEW-005 | Old-Version Evidence Access | Improve | UC-021 | PR-032 |

16 screen/view artifact (11 `SCR`, 5 `VIEW`) — bao trùm đầy đủ `UC-001`–`UC-021`, không thiếu, không dư. Không excessive ID nào tạo cho phần tử decorative.

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

**VIEW-001 — Strategy Instance Selector**
```text
Name:                    Strategy Instance Selector
Lifecycle stage:         Research (global panel, truy cập được từ workspace shell tại mọi stage trước
                         khi phiên pin).
Purpose:                 Chọn ĐÚNG MỘT Strategy Instance làm cơ sở cho phiên Research/Replay/Backtest.
Primary actor:           Ride user.
Entry points:            Global context bar (§5); từ SCR-001 khi chuẩn bị cam kết Replay/Backtest.
Exit points:             SCR-002 (Replay) hoặc SCR-003 (Backtest) hoặc tiếp tục SCR-001, với Strategy
                         Instance context đã pin (read-only, UX-INV-3).
Required context:        Ít nhất một Strategy Instance đã đăng ký.
Information displayed:   Danh sách Strategy Instance đã đăng ký (gắn Strategy Definition Version).
Available user actions:  Chọn một Strategy Instance.
System-owned actions:    Pin Strategy Instance đó cố định cho phiên (WF-INV-3) — chặn đổi giữa chừng.
Evidence consumed:       Strategy Instance/Strategy Definition Version đã đăng ký (strategy.md).
Evidence produced:       KHÔNG authoritative fact — lựa chọn tự nó KHÔNG phải Decision Pipeline fact.
Authority labels:        mode=Research; authority=authoritative (registration record).
Primary states:          Strategy Instance đã pin, hiển thị read-only.
Empty/unavailable/
blocked states:          STATE-004 missing Strategy Instance.
UC traceability:         UC-002.
PR traceability:         PR-001, PR-016.
Domain vocabulary
referenced:              strategy.md.
Out-of-scope boundary:   KHÔNG tạo Strategy Definition Version mới tại đây (đó là SCR-010, Improve).
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
Information displayed:   Kết quả match/mismatch, dùng `canonical semantic-decision hash` (UX-INV-5).
Available user actions:  Kích hoạt parity recomputation (tuỳ chọn, người dùng chủ động).
System-owned actions:    Tái tính toán Decision logic (semantic verification, non-authoritative); so
                         sánh qua canonical semantic-decision hash; hiển thị match/mismatch — KHÔNG
                         BAO GIỜ tự động ghi đè/thay thế/tạo Decision mới.
Evidence consumed:       Decision đã ghi nhận tại cursor; canonical semantic-decision hash definition
                         (decision.md).
Evidence produced:       Kết quả so sánh (non-authoritative, KHÔNG một fact trong event log Decision
                         Pipeline).
Authority labels:        mode=Replay; authority=non-authoritative recomputation (rõ ràng tách biệt
                         khỏi "recorded authoritative Decision" ở SCR-002, §12).
Primary states:          STATE-007 parity match.
Empty/unavailable/
blocked states:          STATE-008 parity mismatch.
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
blocked states:          STATE-009 Backtest evidence insufficient; STATE-010 Backtest run identity
                         unresolved.
UC traceability:         UC-007, UC-008, UC-009.
PR traceability:         PR-009, PR-021, PR-022, PR-033, PR-034.
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
blocked states:          STATE-009 Backtest evidence insufficient (cho run cụ thể thiếu, các run khác
                         vẫn hiển thị).
UC traceability:         UC-010.
PR traceability:         PR-034.
Domain vocabulary
referenced:              strategy.md.
Out-of-scope boundary:   KHÔNG công thức so sánh/scoring/aggregation tổng hợp qua nhiều run
                         (`OQ-003`).
```

### 7.4 Paper

**SCR-006 — Paper Execution Initiation**
```text
Name:                    Paper Execution Initiation
Lifecycle stage:         Paper
Purpose:                 Người dùng khởi tạo (initiate/request) PAPER execution — KHÔNG authoritative
                         Order payload — dựa trên một PAPER-context authoritative Decision lineage
                         RIÊNG BIỆT.
Primary actor:           Ride user (khởi tạo intent); hệ thống sở hữu toàn bộ chuỗi authoritative
                         (UX-P-2).
Entry points:            NAV-004 (Paper); người dùng TỰ QUYẾT ĐỊNH sau khi xem Backtest/Research (§9
                         judgment gate — KHÔNG hard handoff kỹ thuật).
Exit points:             SCR-007 (Paper Order/Execution Detail) — hoặc dừng tại chính screen này nếu
                         không có PAPER-context Decision lineage eligible.
Required context:        Một PAPER-context authoritative Decision lineage (LONG/SHORT) ELIGIBLE tồn
                         tại cho Strategy Instance đang dùng — Decision này TUYỆT ĐỐI KHÔNG phải
                         Decision từ Backtest/Research được carry-forward/promote/reuse.
Information displayed:   Xác nhận PAPER-context Decision lineage eligible (nếu có) — KHÔNG form nhập
                         quantity/order type/sizing/fee/slippage/execution model (chưa UC/PR nào
                         authorize input đó).
Available user actions:  Yêu cầu khởi tạo PAPER execution (intent, KHÔNG authoritative payload).
                         TUYỆT ĐỐI KHÔNG có action "Execute this Backtest Decision in Paper"/"Promote
                         to Paper"/"Convert Backtest Decision" — những action này KHÔNG được thiết kế.
System-owned actions:    Resolve PAPER-context Decision lineage; phát sinh Trade Intent (system-owned)
                         → RiskEvaluation → (nếu APPROVED) Execution Intent (system-owned) → Order
                         (system-owned) → OrderSubmissionRequest (system-owned) →
                         ExecutionResultComputation → PaperExecutionObservation → ExecutionResult →
                         (nếu EXECUTED) Fill → Position.
Evidence consumed:       PAPER-context authoritative Decision lineage (RIÊNG BIỆT); Account/Instrument/
                         Venue context. Backtest/Research evidence (nếu đã xem) CHỈ inform judgment —
                         KHÔNG input authoritative.
Evidence produced:       Trade Intent, RiskEvaluation, Execution Intent (nếu APPROVED), Order,
                         OrderSubmissionRequest, ExecutionResultComputation, PaperExecutionObservation,
                         ExecutionResult, Fill (nếu EXECUTED) — TẤT CẢ system-owned.
Authority labels:        mode=Paper; authority=authoritative PAPER (toàn bộ chuỗi, KHÔNG Live).
Primary states:          RiskEvaluation APPROVED (tiếp tục); chuỗi tiến triển tới ExecutionResult.
Empty/unavailable/
blocked states:          STATE-011 PAPER Decision lineage unavailable (blocked TRƯỚC PAPER execution);
                         STATE-013 Risk REJECTED; STATE-014 Risk NON_EVALUABLE (cả hai dừng TRƯỚC
                         Execution Intent/Order).
UC traceability:         UC-011.
PR traceability:         PR-007, PR-024.
Domain vocabulary
referenced:              decision.md, trade-intent.md, risk.md, execution-intent.md, order.md,
                         execution-result.md, fill.md, position.md.
Out-of-scope boundary:   KHÔNG order type/sizing/fee/slippage/execution-model UI do người dùng cung
                         cấp; KHÔNG Live routing (deferred, `OQ-002`); KHÔNG cơ chế chính xác thiết
                         lập PAPER-context Decision (deferred, §15); KHÔNG clone/copy/recreate Decision
                         từ Backtest/Research.
```

**SCR-007 — Paper Order/Execution Detail**
```text
Name:                    Paper Order/Execution Detail
Lifecycle stage:         Paper
Purpose:                 Xem ExecutionResult, Fill simulation evidence, Position (hoặc NON_EVALUABLE),
                         VÀ xác nhận không lệnh thật nào được đặt.
Primary actor:           Ride user.
Entry points:            SCR-006 (sau khi chuỗi PAPER hoàn tất); danh sách Order (NAV-004).
Exit points:             SCR-008 (Review — trace causation); NAV-004 (Order khác).
Required context:        Order đã đi qua SCR-006, có ExecutionResult visible-valid.
Information displayed:   Bốn panel/tab: (a) ExecutionResult (EXECUTED/NOT_EXECUTED), environment PAPER;
                         (b) Fill simulation evidence (policy/configuration/build/deterministic-input
                         ref) + economics, khớp byte-for-byte PaperExecutionObservation; (c) Position
                         hiện tại (FLAT/LONG/SHORT/NON_EVALUABLE); (d) xác nhận environment=PAPER trên
                         mọi fact, không route mạng tới exchange thật.
Available user actions:  Chọn Order/Fill để xem chi tiết; điều hướng giữa bốn panel/tab.
System-owned actions:    Derive Position từ eligible Fill lineage; disclose NON_EVALUABLE khi nhiều
                         Fill lineage xung đột (KHÔNG chọn một/aggregate/report FLAT sai).
Evidence consumed:       ExecutionResult, Fill, PaperExecutionObservation, Position projection,
                         environment field.
Evidence produced:       KHÔNG (quan sát thuần túy trên panel này — fact đã tạo tại SCR-006).
Authority labels:        mode=Paper; authority=authoritative PAPER (ExecutionResult/Fill/Position);
                         Position tự thân là derived projection, KHÔNG authoritative fact riêng.
Primary states:          STATE-015 ExecutionResult EXECUTED; STATE-018/019/020 Position FLAT/LONG/
                         SHORT.
Empty/unavailable/
blocked states:          STATE-016 ExecutionResult NOT_EXECUTED; STATE-017 Fill absent; STATE-021
                         Position NON_EVALUABLE.
UC traceability:         UC-012, UC-013, UC-014, UC-015.
PR traceability:         PR-007, PR-024, PR-025, PR-026, PR-027.
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
PR traceability:         PR-028.
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
Exit points:             VIEW-001 (Strategy Instance Selector, tạo Instance mới gắn version mới) — vòng
                         lặp trở lại Research (§9).
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
Out-of-scope boundary:   KHÔNG định nghĩa nội dung/schema Strategy Definition cụ thể.
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
blocked states:          Strategy Instance chưa có outcome nào → hiển thị rỗng cho Instance đó, KHÔNG
                         lỗi toàn bộ so sánh; evidence version cũ chưa resolve → VIEW-005 Alternate/
                         failure áp dụng cho đúng phần đó.
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

**FLOW-001 — Primary end-to-end journey (walking skeleton)**
```text
WS-001 → VIEW-001 (chọn Strategy Instance) → SCR-001 (Research, UC-001/UC-003) →
SCR-002 (Replay, UC-004) → [tuỳ chọn VIEW-003, UC-005] →
SCR-003 → SCR-004 → [tuỳ chọn SCR-005] (Backtest, UC-006–UC-010) →
[judgment gate, §9] → SCR-006 → SCR-007 (Paper, UC-011–UC-015) →
SCR-008 → SCR-009 → [tuỳ chọn VIEW-004] (Review, UC-016–UC-018) →
SCR-010 → SCR-011 → [tuỳ chọn VIEW-005] (Improve, UC-019–UC-021) →
VÒNG LẶP về VIEW-001 với Strategy Instance MỚI.

Live KHÔNG phải một bước — chỉ nhắc như lifecycle boundary bị hoãn (§15, `OQ-002`), KHÔNG NAV/SCR nào
dẫn tới Live.
```

**FLOW-002 — Strategy Instance selection/pin (global)**
```text
Trigger: người dùng chuẩn bị cam kết Replay/Backtest, hoặc bắt đầu phiên mới.
VIEW-001 → chọn Strategy Instance → hệ thống pin (read-only, UX-INV-3) → context hiển thị trên toàn
bộ global context bar (§5) cho tới khi phiên kết thúc.
UC/PR: UC-002, PR-001/PR-016.
```

**FLOW-003 — Backtest → Paper handoff (judgment gate, KHÔNG hard handoff)**
```text
SCR-004/SCR-005 (Backtest evidence, non-PAPER, INFORM judgment) → người dùng TỰ QUYẾT ĐỊNH → SCR-006
(Paper). KHÔNG action nào tự động chuyển Backtest Decision thành PAPER Decision. SCR-006 resolve một
PAPER-context Decision lineage RIÊNG BIỆT — nếu không eligible, workflow dừng NGAY tại SCR-006
(STATE-011).
UC/PR: UC-009/UC-010 → UC-011; PR-034 (evidence), PR-024 (Paper độc lập).
```

**FLOW-004 — Paper execution initiation (system-owned chain)**
```text
SCR-006: người dùng yêu cầu khởi tạo → hệ thống resolve PAPER-context Decision → Trade Intent →
RiskEvaluation → [APPROVED] → Execution Intent → Order → OrderSubmissionRequest →
ExecutionResultComputation → PaperExecutionObservation → ExecutionResult → [EXECUTED] → Fill →
Position → SCR-007 hiển thị kết quả.
UC/PR: UC-011, PR-007/PR-024.
```

**FLOW-005 — Old-version evidence access (từ so sánh)**
```text
SCR-011 (phát hiện Strategy Instance gắn version không active) → VIEW-005 → resolve Backtest family
và/hoặc PAPER family ĐỘC LẬP → trở lại SCR-011 với evidence (đầy đủ hoặc đánh dấu incomplete).
UC/PR: UC-020 → UC-021, PR-031/PR-032.
```

**FLOW-006 — Improve → Research loop-back**
```text
SCR-010 (Strategy Definition Version mới) → VIEW-001 (tạo Strategy Instance mới gắn version mới) →
SCR-001 (Research, vòng lặp) — evidence version cũ vẫn truy cập qua VIEW-005 bất kỳ lúc nào.
UC/PR: UC-019 → UC-002; PR-031, PR-001.
```

## 9. Cross-screen and cross-stage handoffs

Kế thừa nguyên vẹn `use-case-workflow.md` §7 (KHÔNG đổi semantics, CHỈ ánh xạ UX):

```text
Research → Replay:    SCR-001/VIEW-002 (exit: Strategy Instance pinned, verification PASSED) → SCR-002
                       (entry: Strategy Instance giữ nguyên, WF-INV-3/UX-INV-3).

Replay → Backtest:    SCR-002/VIEW-003 (exit) → SCR-003 (entry: Strategy Instance giữ nguyên). Hai
                       capability ĐỘC LẬP — KHÔNG hard precondition kỹ thuật (§7 use-case-workflow.md).

Backtest → Paper:     SCR-004/SCR-005 (exit: evaluable result đã xem, INFORM judgment DUY NHẤT) →
                       judgment gate người dùng → SCR-006 (entry: PAPER-context Decision lineage
                       RIÊNG BIỆT bắt buộc — xem FLOW-003). KHÔNG Backtest/Research Decision identity
                       nào mang sang PAPER.

Paper → Review:       SCR-006/SCR-007 (exit: ExecutionResult resolved) → SCR-008 (entry: causation
                       chain đầy đủ sẵn sàng).

Review → Improve:     SCR-008/SCR-009/VIEW-004 (exit: causation traced, state compared, correction
                       inspected nếu có) → SCR-010 (entry: quyết định người dùng tạo version mới).

Improve → Research:   SCR-010/SCR-011/VIEW-005 (exit: version mới tạo, evidence version cũ vẫn truy
                       cập qua identity — resolvability không phải guarantee tuyệt đối) → VIEW-001 →
                       SCR-001 (vòng lặp, Strategy Instance MỚI) — xem FLOW-006.
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

**Bảng `STATE-XXX` — 27 trạng thái presentation-only (UX state, KHÔNG domain state mới, UX-INV-9):**

| ID | State | UC/PR traceability | Applicable screen/view |
|---|---|---|---|
| STATE-001 | loading | (cross-cutting, mọi UC) | Mọi SCR/VIEW |
| STATE-002 | empty | (cross-cutting) | Mọi SCR/VIEW (ví dụ SCR-005/SCR-011 khi chưa chọn run/Instance) |
| STATE-003 | invalid Instrument/Venue | PR-003 | SCR-001, SCR-006 |
| STATE-004 | missing Strategy Instance | PR-001 | VIEW-001 |
| STATE-005 | missing historical evidence | PR-015, PR-021 | SCR-001, SCR-003 |
| STATE-006 | Replay reference unavailable | PR-020 | SCR-002 |
| STATE-007 | parity match | PR-010, PR-019 | VIEW-003 |
| STATE-008 | parity mismatch | PR-010, PR-019 | VIEW-003 |
| STATE-009 | Backtest evidence insufficient | PR-033, PR-034 | SCR-004, SCR-005 |
| STATE-010 | Backtest run identity unresolved | PR-021 | SCR-004 |
| STATE-011 | PAPER Decision lineage unavailable | PR-024 | SCR-006 |
| STATE-012 | Risk APPROVED | PR-006 | SCR-006 |
| STATE-013 | Risk REJECTED | PR-006 | SCR-006 |
| STATE-014 | Risk NON_EVALUABLE | PR-006 | SCR-006 |
| STATE-015 | ExecutionResult EXECUTED | PR-007, PR-024 | SCR-007 |
| STATE-016 | ExecutionResult NOT_EXECUTED | PR-007, PR-024 | SCR-007 |
| STATE-017 | Fill absent | PR-025 | SCR-007 |
| STATE-018 | Position FLAT | PR-026 | SCR-007 |
| STATE-019 | Position LONG | PR-026 | SCR-007 |
| STATE-020 | Position SHORT | PR-026 | SCR-007 |
| STATE-021 | Position NON_EVALUABLE | PR-026 | SCR-007 |
| STATE-022 | Research verification PASSED | PR-017 | VIEW-002 |
| STATE-023 | Research verification FAILED | PR-017 | VIEW-002 |
| STATE-024 | Research verification INDETERMINATE | PR-017 | VIEW-002 |
| STATE-025 | old-version evidence complete | PR-032 | VIEW-005 |
| STATE-026 | old-version evidence partially unavailable | PR-032 | VIEW-005 |
| STATE-027 | Live unauthorized | PR-027, `OQ-002` | WS-001 (global), SCR-006 |

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

**14a. Workspace/Screen/View → UC**

| ID | UC(s) |
|---|---|
| WS-001 | (shell, không map UC trực tiếp — chứa NAV-001..006) |
| SCR-001 | UC-001 |
| VIEW-001 | UC-002 |
| VIEW-002 | UC-003 |
| SCR-002 | UC-004 |
| VIEW-003 | UC-005 |
| SCR-003 | UC-006 |
| SCR-004 | UC-007, UC-008, UC-009 |
| SCR-005 | UC-010 |
| SCR-006 | UC-011 |
| SCR-007 | UC-012, UC-013, UC-014, UC-015 |
| SCR-008 | UC-016 |
| SCR-009 | UC-017 |
| VIEW-004 | UC-018 |
| SCR-010 | UC-019 |
| SCR-011 | UC-020 |
| VIEW-005 | UC-021 |

**14b. Workspace/Screen/View → PR** — xem cột "Primary PR(s)" tại §6 (bảng đầy đủ, không lặp lại).

**14c. UC → Workspace/Screen/View** (nghịch đảo của 14a, xác nhận đầy đủ `UC-001`–`UC-021`)

```text
UC-001 → SCR-001         UC-008 → SCR-004         UC-015 → SCR-007
UC-002 → VIEW-001        UC-009 → SCR-004          UC-016 → SCR-008
UC-003 → VIEW-002        UC-010 → SCR-005          UC-017 → SCR-009
UC-004 → SCR-002         UC-011 → SCR-006          UC-018 → VIEW-004
UC-005 → VIEW-003        UC-012 → SCR-007          UC-019 → SCR-010
UC-006 → SCR-003         UC-013 → SCR-007          UC-020 → SCR-011
UC-007 → SCR-004         UC-014 → SCR-007          UC-021 → VIEW-005
```

Mọi `UC-001`–`UC-021` xuất hiện trong ĐÚNG MỘT primary UX artifact (một số UC chia sẻ một SCR khi tightly-related — SCR-004: UC-007/008/009; SCR-007: UC-012–015 — mỗi UC vẫn có behavior quan sát được RIÊNG trong screen đó, đúng field "Information displayed"/"Primary states" tại §7).

**14d. Lifecycle Stage → Screens/Views**

```text
Research  → SCR-001, VIEW-001, VIEW-002
Replay    → SCR-002, VIEW-003
Backtest  → SCR-003, SCR-004, SCR-005
Paper     → SCR-006, SCR-007
Review    → SCR-008, SCR-009, VIEW-004
Improve   → SCR-010, SCR-011, VIEW-005
```

**14e. State → UC/PR** — xem bảng đầy đủ tại §11 (cột "UC/PR traceability" — mỗi `STATE-XXX` cite đúng PR; UC suy ra từ cột "Applicable screen/view" đối chiếu §14a).

**14f. Screen/View → Domain vocabulary** — xem field "Domain vocabulary referenced" trong từng khối tại §7 (đầy đủ, không lặp lại).

**14g. Deferred dependency → affected screens/views** — xem §15.

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

## 17. Package 0.3-C acceptance criteria

```text
1. Toàn bộ 18 mục nội dung bắt buộc (§1–§18) có mặt và đầy đủ.
2. Tất cả 21 Use Case (UC-001–UC-021) có UX coverage — xác nhận tại §14a/§14c.
3. Mọi UX artifact (WS/NAV/SCR/VIEW/FLOW/STATE) truy vết một hoặc nhiều UC-XXX VÀ một hoặc nhiều
   PR-XXX — không phần tử nào tồn tại chỉ vì "seems useful."
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
18. YAML frontmatter hợp lệ, `version: "0.1"`, `status: Draft`, `approved_by: null`, `approved_at: null`
    — Package 0.3-C vẫn Draft, KHÔNG `Consolidated Stable`.
19. Baseline sẵn sàng cho ChatGPT Review A + Independent Review B trên CÙNG một commit/blob.
```

## 18. Phase 1 handoff requirements

Phase 1 (System/UX Architecture, `/docs/architecture/`, chưa bắt đầu) PHẢI, khi tiêu thụ tài liệu này:

1. Tham chiếu mọi component/API/data-model quyết định về đúng một hoặc nhiều `WS-XXX`/`NAV-XXX`/`SCR-XXX`/`VIEW-XXX`/`FLOW-XXX`/`STATE-XXX` ID tại đây — KHÔNG tự phát minh UX behavior mới ở tầng architecture mà không truy vết ngược `UC-XXX`/`PR-XXX`.
2. KHÔNG tự suy diễn cơ chế cho bất kỳ deferred dependency nào tại §15 (Backtest domain representation, PAPER-context Decision establishment, OQ-002, OQ-003) — những quyết định đó thuộc Product Owner/Domain Contract correction tương lai, KHÔNG phải Phase 1 tự quyết.
3. Giữ nguyên MỌI ranh giới authority đã pin tại §10 (Replay historical reconstruction vs parity recomputation; Backtest non-PAPER vs PAPER authoritative; user intent vs system-owned execution) khi thiết kế API/data contract — KHÔNG API nào được thiết kế theo cách ngầm hợp nhất hai authority tách biệt.
4. KHÔNG author security/custody/deployment/retention/storage architecture dựa trên suy diễn từ UX Blueprint này mà không có quyết định Product Owner/ADR riêng.
5. Giữ nguyên walking-skeleton operating scope (§2) — KHÔNG mở rộng multi-tenant/multi-asset/Live UX khi thiết kế architecture cho Phase 1 walking-skeleton đầu tiên.
6. Xác nhận Live vẫn `Unauthorized` — KHÔNG architecture Live nào được author cho tới khi `OQ-002` đóng qua ADR.
