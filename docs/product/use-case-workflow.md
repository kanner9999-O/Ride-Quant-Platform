---
id: use-case-workflow
title: Use Case & Workflow
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

# Use Case & Workflow

> **Vai trò của tài liệu này:** Artifact thứ hai của Package 0.3-B (Phase 0.3 — Product Requirement · Use Case & Workflow · UX Blueprint), phụ thuộc trực tiếp [`product-requirement.md`](./product-requirement.md) v0.2 Draft (Package 0.3-A, `Consolidated Stable`). Dịch 34 requirement (`PR-001`–`PR-034`) thành hành vi user journey/use case cụ thể, testable — sở hữu **user journey, use-case behavior, precondition, trigger, main flow, alternate flow, observable outcome, handoff** cho sáu giai đoạn Research→Replay→Backtest→Paper→Review→Improve. Draft, chưa Approved/Locked, **chưa `Consolidated Stable`**. Tài liệu này KHÔNG tạo product requirement mới — MỌI bước workflow PHẢI truy vết về một hoặc nhiều `PR-XXX` đã tồn tại; KHÔNG sở hữu screen design/UX component (thuộc Package 0.3-C, chưa author); KHÔNG sở hữu domain semantics (thuộc `/docs/domain/`, không sửa); KHÔNG sở hữu architecture (Phase 1).

**Authority boundary:** tài liệu này sở hữu **use-case/workflow content** cho Phase 0.3 — KHÔNG sở hữu product requirement content (thuộc `product-requirement.md`, Package 0.3-A, không sửa), KHÔNG sở hữu screen layout/wireframe/component hierarchy (thuộc Package 0.3-C `ux-blueprint.md`, chưa author), KHÔNG sở hữu domain semantics/state machine (thuộc `/docs/domain/`, không sửa/redefine), KHÔNG sở hữu architecture quyết định (Phase 1, `/docs/architecture/`), KHÔNG đóng Open Question nào (`OQ-002`/`OQ-003` vẫn `Open`, xem §10), KHÔNG authorize Live, KHÔNG tuyên bố Phase 0.3/Phase 0 hoàn thành, KHÔNG mark chính nó `Consolidated Stable`.

**Quy tắc traceability nguồn (kế thừa nguyên vẹn `product-requirement.md` §"Authority boundary", đóng `P03A-MIN-02`):** mọi Use Case/workflow step PHẢI có một hoặc nhiều `PR-XXX` áp dụng — CÓ THỂ kết hợp nhiều PR; mọi PR trích dẫn phải material (đóng góp thực chất cho behavior mô tả); không Use Case nào được phép mồ côi PR traceability.

## 1. Purpose and authority boundary

Tài liệu này trả lời: **"Với 34 requirement đã `Consolidated Stable` tại Package 0.3-A, người dùng nội bộ THỰC SỰ tương tác với Ride như thế nào, theo trình tự nào, với hành vi quan sát được cụ thể ra sao?"** — ở mức **user journey/use-case behavior**, KHÔNG ở mức screen/UI (Package 0.3-C) hay implementation (Phase 1). Là input bắt buộc cho Package 0.3-C (`ux-blueprint.md`) — Package 0.3-C PHẢI truy vết ngược mọi screen/flow về đúng một hoặc nhiều `UC-XXX` ID tại đây, KHÔNG được tự phát minh use case mới ở tầng UX.

## 2. Actors and approved operating context

```text
Primary actor:        "Ride user" — thành viên nội bộ của một team vận hành nhiều Strategy trên vốn
                       của chính team đó (product-requirement.md §3). Vai trò định hướng thiết kế sản
                       phẩm (Retail Trader/Professional Trader/Quant Researcher/Strategy Developer,
                       Vision §1.5) KHÔNG tạo hành vi workflow khác biệt ở walking-skeleton này — một
                       actor DUY NHẤT được dùng xuyên suốt tài liệu (PR-001–PR-003).

Operating context (kế thừa nguyên vẹn product-requirement.md §6, KHÔNG đổi):
  internal trading workspace     (ADR-007 — KHÔNG multi-tenant)
  single workspace                (một Account vận hành thực tế, Account first-class — PR-002)
  crypto-only                     (ADR-007 — KHÔNG đa tài sản)
  2–3 exchanges                   (ADR-007, PR-003)

Không actor hệ thống/nội bộ nào khác (ví dụ "Risk Gateway", "Execution Engine") được đối xử như actor
use-case — chúng là authoritative pipeline boundary đã đóng tại Domain Contract, CHỈ xuất hiện trong
Main flow như bước hệ thống hiển thị (system-visible behavior), KHÔNG phải actor khởi xướng use case.
```

## 3. Workflow-wide invariants

Chín invariant dưới đây restate nguyên vẹn `PR-XXX` đã `Consolidated Stable` — KHÔNG tạo yêu cầu mới, áp dụng xuyên suốt MỌI Use Case tại §6:

```text
WF-INV-1  Một Ride user session luôn scoped theo ĐÚNG MỘT Account hiện tại của workspace.       (PR-002)
WF-INV-2  Instrument/Venue thao tác luôn nằm trong tập TradableListing đã đăng ký.                (PR-003)
WF-INV-3  Một phiên Research/Replay/Backtest luôn dùng ĐÚNG MỘT Strategy Instance, cố định
          trong suốt phiên đó.                                                          (PR-001, PR-016)
WF-INV-4  Mọi Decision/Risk Action hiển thị PHẢI tái dựng được từ evidence bất biến, một
          causation trace duy nhất.                                                            (PR-009)
WF-INV-5  So sánh Decision semantic giữa Replay/Backtest/Paper luôn dùng `canonical
          semantic-decision hash` — KHÔNG BAO GIỜ dùng lại thuật ngữ "Decision hash" chung
          chung.                                                                               (PR-010)
WF-INV-6  Không output nào (Decision/RiskEvaluation/ExecutionResult/Fill/Position) từng hiển
          thị bị sửa/xóa ngầm — mọi correction là fact mới, append-only.                        (PR-011)
WF-INV-7  Trạng thái hiển thị tại một historical cursor luôn deterministic, không phụ thuộc
          network sau khi chuẩn bị.                                                            (PR-012)
WF-INV-8  Mọi giá trị tài chính hiển thị PHẢI lossless, khớp byte-for-byte giá trị đã ghi
          nhận.                                                                                (PR-013)
WF-INV-9  Mọi lifecycle state hiển thị PHẢI phản ánh transition đã khai báo tường minh trong
          Domain Contract sở hữu entity đó.                                                    (PR-014)
WF-INV-10 Live là lifecycle boundary bị hoãn (`OQ-002`) — KHÔNG use case nào tại đây kết
          thúc bằng một hành động Live authoritative.                                (PR-027, Preserve scope)
```

## 4. Primary end-to-end journey

Hành trình chính (walking skeleton, KHÔNG bao trùm mọi persona/edge case — đúng kỷ luật đã pin tại `product-requirement.md`):

```text
Ride user (§2):
  1. Research     — chọn Instrument/Venue (PR-003), quan sát market-analysis state (PR-015), chọn/
                     cấu hình Strategy Instance (PR-001/PR-016) — KHÔNG side-effect (PR-017).
  2. Replay        — chọn canonical Replay Cursor, xem lại chính xác state lịch sử đã ghi nhận
                     (PR-008/PR-018), tuỳ chọn parity recomputation (PR-019/PR-020).
  3. Backtest      — chạy Decision logic của Strategy Instance qua một khoảng lịch sử bounded
                     (PR-021), xem Decision/RiskEvaluation trace, simulated economic evidence/
                     exposure progression (PR-033), và strategy-level evaluable result so sánh
                     được cross-run/cross-version (PR-022/PR-034).
  4. Paper         — submit Order PAPER, đi qua chuỗi C7 đầy đủ, nhận ExecutionResult/Fill/
                     Position (PR-007/PR-024–PR-027).
  5. Review        — truy vết causation trace Decision→Position (PR-028), so sánh reconstructed
                     vs recorded state (PR-029), xác nhận không recompute lịch sử (PR-030).
  6. Improve       — tạo Strategy Definition Version mới (PR-031), so sánh outcome cũ/mới, giữ
                     nguyên truy cập evidence version cũ (PR-032) — VÒNG LẶP trở lại Research với
                     Strategy Instance mới.
```

Live KHÔNG phải một bước trong hành trình này — chỉ được nhắc như lifecycle boundary bị hoãn (§10, `OQ-002`).

## 5. Use Case catalogue

| UC-ID | Title | Stage | Primary PR(s) |
|---|---|---|---|
| UC-001 | Inspect market-analysis state | Research | PR-003, PR-015, PR-017 |
| UC-002 | Select/configure Strategy Instance | Research | PR-001, PR-016 |
| UC-003 | Confirm Research session produced no side-effect | Research | PR-017 |
| UC-004 | Choose canonical Replay Cursor and reconstruct historical state | Replay | PR-008, PR-018, PR-020 |
| UC-005 | Run optional parity recomputation and view match/mismatch finding | Replay | PR-010, PR-019 |
| UC-006 | Start a bounded Backtest run bound to Strategy/version/configuration | Backtest | PR-021, PR-022, PR-023 |
| UC-007 | Inspect Decision/RiskEvaluation trace for a Backtest run | Backtest | PR-021, PR-009 |
| UC-008 | Inspect simulated economic evidence and exposure/position progression | Backtest | PR-033 |
| UC-009 | Inspect strategy-level evaluable result for a Backtest run | Backtest | PR-034 |
| UC-010 | Compare Backtest runs or Strategy Definition Versions | Backtest | PR-034 |
| UC-011 | Submit a PAPER Order through the approved pipeline | Paper | PR-007, PR-024 |
| UC-012 | Inspect ExecutionResult for a submitted Order | Paper | PR-007, PR-024 |
| UC-013 | Inspect Fill simulation evidence | Paper | PR-025 |
| UC-014 | Inspect Position or NON_EVALUABLE outcome | Paper | PR-026 |
| UC-015 | Confirm no real exchange order was placed | Paper | PR-027 |
| UC-016 | Trace Decision → Position lineage | Review | PR-028 |
| UC-017 | Compare reconstructed and recorded historical state | Review | PR-029 |
| UC-018 | Inspect a correction without repainting history | Review | PR-011, PR-030 |
| UC-019 | Create a new Strategy Definition Version | Improve | PR-031 |
| UC-020 | Compare historical outcomes across Strategy Definition Versions | Improve | PR-031, PR-032 |
| UC-021 | Preserve access to old-version evidence | Improve | PR-032 |

21 Use Case, `UC-001`–`UC-021`, bao trùm đầy đủ danh sách minimum coverage bắt buộc cho cả sáu giai đoạn.

## 6. Detailed Use Cases

### 9.1-equivalent — Research

**UC-001 — Inspect market-analysis state**
```text
Primary actor:         Ride user (§2).
Goal:                   Xem trạng thái phân tích thị trường (Candle/Swing/Structure/Regime/Feature/
                        Market Context) tại một thời điểm/khoảng thời gian, KHÔNG tạo side-effect.
Trigger:                Người dùng bắt đầu một phiên Research cho một Instrument/Venue.
Preconditions:          Instrument/Venue nằm trong tập TradableListing đã đăng ký (PR-003).
Inputs:                 Instrument/Venue đã chọn; thời điểm hoặc khoảng thời gian quan tâm.
Main flow:              1. Người dùng chọn Instrument/Venue hợp lệ (WF-INV-2).
                        2. Người dùng chọn thời điểm/khoảng thời gian quan tâm.
                        3. Hệ thống hiển thị Candle/Swing/Structure/Regime/Feature/Market Context tại
                           thời điểm đó, đọc trực tiếp từ authoritative event stream tương ứng —
                           KHÔNG tạo fact mới.
Alternate/failure:      Instrument/Venue không hợp lệ → §8 "invalid Instrument/Venue selection".
                        Không có dữ liệu lịch sử tại thời điểm chọn → §8 "missing historical evidence".
Observable outcome:     Người dùng thấy đầy đủ market-analysis state tại thời điểm đã chọn.
Evidence consumed:      Candle/Swing/Structure/Regime/Feature/Market Context authoritative fact stream.
Evidence produced:      KHÔNG — quan sát thuần túy (đóng PR-015/PR-017).
PR traceability:        PR-003, PR-015, PR-017.
Domain vocabulary used: candle.md, swing.md, structure.md, regime.md, feature.md, context.md,
                        instrument.md, venue.md.
Out-of-scope boundary:  KHÔNG hiển thị chi tiết chart/UI component (Package 0.3-C); KHÔNG tính toán
                        chỉ báo mới ngoài Feature type đã đăng ký (feature.md).
```

**UC-002 — Select/configure Strategy Instance**
```text
Primary actor:         Ride user (§2).
Goal:                   Chọn ĐÚNG MỘT Strategy Instance (gắn một Strategy Definition Version) làm cơ
                        sở cho toàn bộ phiên Research/Replay/Backtest tiếp theo.
Trigger:                Người dùng chuẩn bị chuyển từ quan sát thuần túy (UC-001) sang cam kết một
                        phiên Replay/Backtest.
Preconditions:          Tồn tại ít nhất một Strategy Instance đã đăng ký (strategy.md).
Inputs:                 Strategy Instance được chọn từ danh sách đã đăng ký.
Main flow:              1. Người dùng chọn một Strategy Instance.
                        2. Hệ thống pin Strategy Instance đó là cố định cho phiên (WF-INV-3) — KHÔNG
                           cho phép đổi giữa chừng một phiên Replay/Backtest đang chạy.
Alternate/failure:      Không có Strategy Instance nào tồn tại/được chọn → §8 "missing Strategy
                        Instance".
Observable outcome:     Phiên làm việc có ĐÚNG MỘT Strategy Instance pin cố định.
Evidence consumed:      Strategy Instance/Strategy Definition Version đã đăng ký.
Evidence produced:      KHÔNG authoritative fact mới — lựa chọn Strategy Instance tự nó KHÔNG phải
                        Decision Pipeline fact.
PR traceability:        PR-001, PR-016.
Domain vocabulary used: strategy.md.
Out-of-scope boundary:  KHÔNG tạo Strategy Definition Version mới tại đây (đó là UC-019, Improve).
```

**UC-003 — Confirm Research session produced no side-effect**
```text
Primary actor:         Ride user (§2).
Goal:                   Xác nhận một phiên Research đã kết thúc mà KHÔNG tạo bất kỳ authoritative
                        Decision Pipeline fact nào.
Trigger:                Người dùng kết thúc phiên Research (hoặc chuyển sang Replay/Backtest).
Preconditions:          Một phiên Research (UC-001/UC-002) đã diễn ra.
Inputs:                 Khoảng thời gian của phiên Research vừa kết thúc.
Main flow:              1. Hệ thống hiển thị xác nhận: không Decision/RiskEvaluation/Execution
                           Intent/Order/ExecutionResult mới nào xuất hiện trong event log trong
                           khoảng thời gian phiên Research.
Alternate/failure:      KHÔNG áp dụng — đây là một verification step, không có nhánh thất bại người
                        dùng-khởi-xướng; nếu hệ thống phát hiện fact mới xuất hiện ngoài dự kiến, đó
                        là governance/implementation concern ngoài phạm vi tài liệu này.
Observable outcome:     Người dùng có bằng chứng tường minh rằng Research không side-effect.
Evidence consumed:      Event log của Decision/RiskEvaluation/Execution Intent/Order/ExecutionResult
                        stream trong khoảng thời gian phiên.
Evidence produced:      KHÔNG.
PR traceability:        PR-017.
Domain vocabulary used: decision.md.
Out-of-scope boundary:  KHÔNG định nghĩa cơ chế audit/log kỹ thuật cụ thể (Phase 1).
```

### 9.2-equivalent — Replay

**UC-004 — Choose canonical Replay Cursor and reconstruct historical state**
```text
Primary actor:         Ride user (§2).
Goal:                   Chọn một canonical Replay Cursor và xem lại CHÍNH XÁC state authoritative đã
                        tồn tại tại cursor đó (historical reconstruction — mặc định).
Trigger:                Người dùng, với Strategy Instance đã pin (UC-002), chọn chuyển sang Replay.
Preconditions:          Strategy Instance đã chọn (WF-INV-3); Instrument/Venue hợp lệ (WF-INV-2).
Inputs:                 Một canonical Replay Cursor (thời điểm lịch sử).
Main flow:              1. Người dùng chọn một Replay Cursor.
                        2. Hệ thống resolve và hiển thị ReplayState(C) — Decision→Trade Intent→
                           RiskEvaluation→Execution Intent→Order→ExecutionResult→Fill→Position lineage
                           TẠI cursor đó — CHỈ fact có recorded_time ≤ C (no-look-ahead).
                        3. Hệ thống KHÔNG tạo Decision hay bất kỳ authoritative fact nào trong bước
                           này (Replay authority boundary, product-requirement.md §9.2).
Alternate/failure:      Cursor tham chiếu artifact không materialize được → §8 "Replay cursor with
                        unavailable references".
Observable outcome:     Người dùng thấy chính xác state đã ghi nhận tại cursor đã chọn.
Evidence consumed:      Toàn bộ authoritative event stream Decision→...→Position, canonical Replay
                        Cursor (Chapter 8 §8.5).
Evidence produced:      KHÔNG authoritative fact mới — historical reconstruction thuần túy.
PR traceability:        PR-008, PR-018, PR-020.
Domain vocabulary used: replay-event.md, decision.md, trade-intent.md, risk.md, execution-intent.md,
                        order.md, execution-result.md, fill.md, position.md.
Out-of-scope boundary:  KHÔNG chạy lại simulation/computation nào (đó là parity recomputation, UC-005,
                        và luôn tuỳ chọn/tách biệt).
```

**UC-005 — Run optional parity recomputation and view match/mismatch finding**
```text
Primary actor:         Ride user (§2).
Goal:                   Tuỳ chọn kiểm chứng lại (parity recomputation) rằng Decision logic tái tính
                        toán khớp Decision đã ghi nhận tại cursor đang xem (UC-004) — deterministic,
                        non-authoritative.
Trigger:                Người dùng, đang xem historical reconstruction (UC-004), chọn kích hoạt parity
                        recomputation.
Preconditions:          UC-004 đã hoàn tất — một ReplayState(C) đang hiển thị.
Inputs:                 Yêu cầu kích hoạt parity recomputation từ người dùng (tuỳ chọn, KHÔNG mặc
                        định).
Main flow:              1. Người dùng kích hoạt parity recomputation.
                        2. Hệ thống tái tính toán Decision logic (semantic verification, non-
                           authoritative) và so sánh với Decision đã ghi nhận qua `canonical
                           semantic-decision hash` (WF-INV-5).
                        3. Hệ thống hiển thị kết quả match/mismatch — KHÔNG BAO GIỜ tự động ghi đè,
                           thay thế, hay tạo Decision mới từ kết quả này (Replay authority boundary).
Alternate/failure:      Kết quả mismatch → §8 "parity mismatch" (hiển thị finding, KHÔNG hành động
                        authoritative nào tự động xảy ra).
Observable outcome:     Người dùng thấy match/mismatch, KHÔNG có Decision mới/thay thế nào xuất hiện.
Evidence consumed:      Decision đã ghi nhận tại cursor, canonical semantic-decision hash definition
                        (decision.md).
Evidence produced:      Kết quả so sánh (non-authoritative, KHÔNG phải một fact được ghi vào event
                        log Decision Pipeline).
PR traceability:        PR-010, PR-019.
Domain vocabulary used: decision.md, replay-event.md.
Out-of-scope boundary:  KHÔNG tạo `ReplayDecision` hay bất kỳ domain fact mới nào; KHÔNG định nghĩa cơ
                        chế lưu trữ kết quả recomputation (Phase 1).
```

### 9.3-equivalent — Backtest

**UC-006 — Start a bounded Backtest run bound to Strategy/version/configuration**
```text
Primary actor:         Ride user (§2).
Goal:                   Khởi động một Backtest run qua một khoảng lịch sử bounded (start/end), dưới
                        MỘT stable run identity/context, gắn Strategy Instance/Definition Version/
                        configuration tường minh.
Trigger:                Người dùng, với Strategy Instance đã pin (UC-002), chọn chuyển sang Backtest.
Preconditions:          Strategy Instance đã chọn (WF-INV-3); khoảng thời gian lịch sử có dữ liệu.
Inputs:                 Khoảng thời gian bounded (start/end).
Main flow:              1. Người dùng nhập khoảng thời gian bounded.
                        2. Hệ thống gán một stable Backtest run identity/context duy nhất, gắn CHÍNH
                           XÁC Strategy Instance/Strategy Definition Version/policy version đang dùng.
                        3. Hệ thống chạy Decision logic (CÙNG pipeline với Replay/Paper — WF-INV
                           parity) qua khoảng thời gian đó — KHÔNG tạo Order/ExecutionResult PAPER
                           hay Live.
                        4. Hệ thống xác nhận: KHÔNG route mạng tới bất kỳ exchange endpoint thật nào
                           trong suốt run.
Alternate/failure:      Không đủ dữ liệu lịch sử cho khoảng đã chọn → §8 "missing historical evidence".
Observable outcome:     Một Backtest run identity tồn tại, gắn đúng khoảng thời gian + version tuple.
Evidence consumed:      Strategy Instance/Definition Version, market-analysis state lịch sử.
Evidence produced:      Decision/RiskEvaluation sequence gắn run identity (KHÔNG Order/ExecutionResult
                        PAPER/Live — Backtest authority boundary).
PR traceability:        PR-021, PR-022, PR-023.
Domain vocabulary used: decision.md, risk.md, strategy.md.
Out-of-scope boundary:  KHÔNG author entity/event "BacktestOrder"/"BacktestExecutionResult" hay tương
                        đương; KHÔNG định nghĩa simulation algorithm (product-required nhưng domain-
                        representation deferred, §9).
```

**UC-007 — Inspect Decision/RiskEvaluation trace for a Backtest run**
```text
Primary actor:         Ride user (§2).
Goal:                   Xem toàn bộ chuỗi Decision/RiskEvaluation sinh ra bởi một Backtest run (UC-006).
Trigger:                Người dùng chọn xem chi tiết một Backtest run đã/đang chạy.
Preconditions:          Một Backtest run identity tồn tại (UC-006).
Inputs:                 Backtest run identity.
Main flow:              1. Người dùng chọn một Backtest run.
                        2. Hệ thống hiển thị chuỗi Decision/RiskEvaluation đầy đủ của run đó, mỗi
                           Decision hiển thị outcome + evidence trace (WF-INV-4).
Alternate/failure:      Run không tồn tại/đã bị loại bỏ → §8 "missing historical evidence" (biến thể
                        cho Backtest run).
Observable outcome:     Người dùng thấy trình tự Decision/RiskEvaluation đầy đủ của run.
Evidence consumed:      Decision/RiskEvaluation fact gắn run identity.
Evidence produced:      KHÔNG — quan sát thuần túy.
PR traceability:        PR-021, PR-009.
Domain vocabulary used: decision.md, risk.md.
Out-of-scope boundary:  KHÔNG hiển thị chi tiết UI/chart (Package 0.3-C).
```

**UC-008 — Inspect simulated economic evidence and exposure/position progression**
```text
Primary actor:         Ride user (§2).
Goal:                   Xem deterministic simulated economic evidence gắn mỗi Decision dẫn tới
                        simulated exposure change, VÀ exposure/position progression theo thời gian
                        xuyên suốt khoảng interval của run — TÁCH BIỆT hoàn toàn khỏi PAPER/Live
                        authority.
Trigger:                Người dùng, đang xem một Backtest run (UC-007), chọn xem economic evidence.
Preconditions:          Backtest run identity tồn tại, có ít nhất một Decision dẫn tới simulated
                        exposure change.
Inputs:                 Backtest run identity.
Main flow:              1. Hệ thống hiển thị simulated economic evidence deterministic cho mỗi điểm
                           Decision→simulated exposure change.
                        2. Hệ thống hiển thị exposure/position progression theo thời gian trong suốt
                           khoảng interval.
                        3. Hệ thống xác nhận (hoặc cho phép audit) rằng KHÔNG PAPER Order/
                           ExecutionResult/Fill/Position nào được tạo/tái sử dụng bởi run này
                           (Backtest authority boundary).
Alternate/failure:      Run không có Decision nào dẫn tới simulated exposure change (ví dụ toàn bộ
                        Decision đều không có exposure mới) → §8 "Backtest run with insufficient
                        evaluable evidence".
Observable outcome:     Người dùng thấy economic evidence + exposure progression, KHÔNG lẫn với PAPER
                        fact.
Evidence consumed:      Decision/RiskEvaluation sequence của run (UC-007).
Evidence produced:      Simulated economic evidence + exposure/position progression — **product-
                        required, domain-representation deferred** (KHÔNG có Domain Contract Backtest
                        chính thức, §9).
PR traceability:        PR-033.
Domain vocabulary used: decision.md, risk.md (nguồn evidence); execution-result.md/fill.md/position.md
                        (tham chiếu CHỈ để định nghĩa ranh giới KHÔNG được tái sử dụng).
Out-of-scope boundary:  KHÔNG định nghĩa simulation algorithm, fee/slippage model, accounting/PnL
                        formula; KHÔNG tạo "BacktestFill"/"BacktestPosition" hay tương đương.
```

**UC-009 — Inspect strategy-level evaluable result for a Backtest run**
```text
Primary actor:         Ride user (§2).
Goal:                   Xem một strategy-level evaluable result cho một Backtest run đã hoàn tất, dẫn
                        xuất từ Decision/RiskEvaluation + exposure progression (UC-007/UC-008), gắn
                        CHÍNH XÁC version tuple đã dùng.
Trigger:                Người dùng, sau khi Backtest run hoàn tất, chọn xem kết quả tổng hợp.
Preconditions:          Backtest run đã hoàn tất, có economic evidence/exposure progression (UC-008).
Inputs:                 Backtest run identity đã hoàn tất.
Main flow:              1. Hệ thống dẫn xuất một strategy-level evaluable result từ toàn bộ run.
                        2. Hệ thống hiển thị kết quả đó gắn CHÍNH XÁC Strategy Instance/Definition
                           Version/configuration context đã dùng (UC-006) — KHÔNG threshold/target cụ
                           thể nào được định nghĩa/hiển thị như KPI chính thức (`OQ-003`).
Alternate/failure:      Run chưa hoàn tất, hoặc thiếu evidence evaluable (UC-008 alternate) → §8
                        "Backtest run with insufficient evaluable evidence".
Observable outcome:     Người dùng thấy một kết quả evaluable, gắn đúng run/version context.
Evidence consumed:      Economic evidence + exposure progression (UC-008), version tuple (UC-006).
Evidence produced:      Strategy-level evaluable result — product-required, domain-representation
                        deferred (§9).
PR traceability:        PR-034, PR-022.
Domain vocabulary used: strategy.md; decision.md/risk.md (nguồn evidence).
Out-of-scope boundary:  KHÔNG định nghĩa concrete KPI threshold/target (`OQ-003`); KHÔNG performance
                        attribution formula.
```

**UC-010 — Compare Backtest runs or Strategy Definition Versions**
```text
Primary actor:         Ride user (§2).
Goal:                   So sánh strategy-level evaluable result (UC-009) của hai Backtest run — khác
                        khoảng interval, hoặc khác Strategy Definition Version.
Trigger:                Người dùng chọn từ hai Backtest run trở lên để so sánh.
Preconditions:          Cả hai run đều đã hoàn tất, mỗi run có một strategy-level evaluable result
                        (UC-009).
Inputs:                 Hai (hoặc nhiều) Backtest run identity.
Main flow:              1. Người dùng chọn các run cần so sánh.
                        2. Hệ thống hiển thị kết quả evaluable của từng run cạnh nhau, gắn đúng run/
                           version context của từng run — KHÔNG gộp/aggregate thành một con số duy
                           nhất.
Alternate/failure:      Một trong các run được chọn thiếu evaluable result (UC-009 alternate) → §8
                        "Backtest run with insufficient evaluable evidence" cho run đó, các run khác
                        vẫn hiển thị.
Observable outcome:     Người dùng so sánh được kết quả nhiều run cạnh nhau mà không cần công cụ
                        ngoài hệ thống.
Evidence consumed:      Strategy-level evaluable result của từng run (UC-009).
Evidence produced:      KHÔNG — so sánh thuần túy hiển thị, KHÔNG tạo fact mới.
PR traceability:        PR-034.
Domain vocabulary used: strategy.md.
Out-of-scope boundary:  KHÔNG định nghĩa công thức so sánh/scoring tổng hợp qua nhiều run (aggregation
                        formula ngoài phạm vi, `OQ-003`).
```

### 9.4-equivalent — Paper

**UC-011 — Submit a PAPER Order through the approved pipeline**
```text
Primary actor:         Ride user (§2).
Goal:                   Submit một Order hợp lệ, đi qua TRỌN VẸN chuỗi C7: Decision → Trade Intent →
                        RiskEvaluation → Execution Intent → Order → OrderSubmissionRequest →
                        ExecutionResultComputation → PaperExecutionObservation → ExecutionResult →
                        Fill → Position, environment PAPER.
Trigger:                Người dùng quyết định thực thi (PAPER) dựa trên một Decision hiện có (thường
                        sau khi đã Research/Replay/Backtest — judgment gate của người dùng, KHÔNG phải
                        hard precondition hệ thống, xem §7).
Preconditions:          Một Decision (LONG/SHORT) đã tồn tại cho Strategy Instance đang dùng; Account/
                        Instrument/Venue hợp lệ (WF-INV-1/WF-INV-2).
Inputs:                 Decision hiện có làm nguồn cho Trade Intent.
Main flow:              1. Decision (LONG/SHORT) phát sinh Trade Intent.
                        2. Trade Intent đi qua Risk Gateway → RiskEvaluation (APPROVED/REJECTED/
                           NON_EVALUABLE).
                        3. Nếu APPROVED: RiskEvaluation phát sinh Execution Intent.
                        4. Execution Intent phát sinh Order, rồi OrderSubmissionRequest.
                        5. Hệ thống authorize ExecutionResultComputation, chạy bounded PAPER
                           simulation, ghi nhận PaperExecutionObservation.
                        6. Hệ thống ghi nhận ExecutionResult (EXECUTED hoặc NOT_EXECUTED),
                           environment PAPER.
                        7. Nếu EXECUTED: đúng một Fill được tạo, rồi Position được cập nhật (derive
                           từ eligible Fill lineage).
Alternate/failure:      RiskEvaluation REJECTED/NON_EVALUABLE → §8, dừng chuỗi tại đó, KHÔNG Execution
                        Intent/Order nào được tạo. ExecutionResult NOT_EXECUTED → §8, zero Fill.
Observable outcome:     Người dùng thấy toàn bộ chuỗi C7 tiến triển tới đúng một ExecutionResult
                        (EXECUTED hoặc NOT_EXECUTED).
Evidence consumed:      Decision hiện có, Account/Instrument/Venue context.
Evidence produced:      Trade Intent, RiskEvaluation, Execution Intent (nếu APPROVED), Order,
                        OrderSubmissionRequest, ExecutionResultComputation, PaperExecutionObservation,
                        ExecutionResult, Fill (nếu EXECUTED).
PR traceability:        PR-007, PR-024.
Domain vocabulary used: decision.md, trade-intent.md, risk.md, execution-intent.md, order.md,
                        execution-result.md, fill.md, position.md.
Out-of-scope boundary:  KHÔNG định nghĩa order type/sizing UI; KHÔNG author Live routing (deferred,
                        `OQ-002`).
```

**UC-012 — Inspect ExecutionResult for a submitted Order**
```text
Primary actor:         Ride user (§2).
Goal:                   Xem ExecutionResult (EXECUTED/NOT_EXECUTED) của một Order đã submit (UC-011),
                        environment PAPER.
Trigger:                Người dùng chọn xem chi tiết một Order đã submit.
Preconditions:          Order đã đi qua UC-011, có ExecutionResult visible-valid.
Inputs:                 Order identity.
Main flow:              1. Người dùng chọn Order.
                        2. Hệ thống hiển thị ExecutionResult (EXECUTED hoặc NOT_EXECUTED), environment
                           PAPER, gắn đúng OrderSubmissionRequest/computation gốc.
Alternate/failure:      NOT_EXECUTED → §8, người dùng thấy rõ zero Fill kèm theo.
Observable outcome:     Người dùng xác định chính xác kết quả execution của Order.
Evidence consumed:      ExecutionResult authoritative fact (execution-result.md §8).
Evidence produced:      KHÔNG.
PR traceability:        PR-007, PR-024.
Domain vocabulary used: order.md, execution-result.md.
Out-of-scope boundary:  KHÔNG hiển thị chi tiết computation/observation nội bộ ngoài những gì PR-007
                        yêu cầu.
```

**UC-013 — Inspect Fill simulation evidence**
```text
Primary actor:         Ride user (§2).
Goal:                   Xem simulation evidence (policy/configuration/build/deterministic-input ref)
                        VÀ economics (quantity/price) của một Fill, khớp CHÍNH XÁC
                        PaperExecutionObservation đã ghi nhận.
Trigger:                Người dùng chọn xem chi tiết một Fill (từ ExecutionResult EXECUTED, UC-012).
Preconditions:          ExecutionResult EXECUTED tồn tại, có đúng một Fill.
Inputs:                 Fill identity (qua execution_result_id).
Main flow:              1. Người dùng chọn Fill.
                        2. Hệ thống hiển thị fill_quantity/fill_price/price_currency VÀ bốn trục
                           simulation evidence (policy/configuration/build/deterministic-input ref),
                           khớp byte-for-byte PaperExecutionObservation gốc (WF-INV-8).
Alternate/failure:      Fill không tồn tại (ExecutionResult NOT_EXECUTED) → §8 "Fill absent".
Observable outcome:     Người dùng xác nhận economics của Fill khớp chính xác evidence đã ghi nhận,
                        KHÔNG có giá trị tính lại độc lập.
Evidence consumed:      Fill + PaperExecutionObservation (fill.md §1/§3, execution-result.md §1).
Evidence produced:      KHÔNG.
PR traceability:        PR-025.
Domain vocabulary used: fill.md, execution-result.md.
Out-of-scope boundary:  KHÔNG định nghĩa simulation algorithm/fee/slippage (execution-result.md đã
                        đóng phạm vi này — KHÔNG mở rộng).
```

**UC-014 — Inspect Position or NON_EVALUABLE outcome**
```text
Primary actor:         Ride user (§2).
Goal:                   Xem Position hiện tại cho một Account/Instrument; khi nhiều Fill lineage xung
                        đột, thấy disclosure tường minh NON_EVALUABLE thay vì một con số tuỳ chọn.
Trigger:                Người dùng chọn xem Position cho một Account/Instrument.
Preconditions:          Ít nhất một Fill tồn tại cho Account/Instrument đó (hoặc zero — FLAT).
Inputs:                 Account/Instrument selection.
Main flow:              1. Hệ thống derive Position từ eligible Fill lineage (position.md §2).
                        2. NẾU 0 eligible Fill: hiển thị FLAT. NẾU 1 eligible Fill: hiển thị LONG/
                           SHORT + net_quantity/average_entry_price. NẾU > 1 eligible Fill xung đột:
                           hiển thị `NON_EVALUABLE` + `contributing_fill_refs` đầy đủ — KHÔNG chọn một
                           Fill/aggregate/report FLAT sai.
Alternate/failure:      NON_EVALUABLE → §8 "Position NON_EVALUABLE".
Observable outcome:     Người dùng thấy đúng trạng thái Position, kể cả khi không thể xác định.
Evidence consumed:      eligible_as_position_contributing_fill (fill.md §6), Position projection
                        (position.md §2).
Evidence produced:      KHÔNG — Position là derived projection, KHÔNG authoritative fact riêng.
PR traceability:        PR-026.
Domain vocabulary used: position.md, fill.md.
Out-of-scope boundary:  KHÔNG định nghĩa weighted-average/netting formula cho nhiều Fill (position.md
                        đã đóng — KHÔNG mở rộng, `OQ-003`-adjacent nhưng ngoài phạm vi).
```

**UC-015 — Confirm no real exchange order was placed**
```text
Primary actor:         Ride user (§2).
Goal:                   Xác nhận Paper Trading KHÔNG tạo ra bất kỳ lệnh thật nào trên sàn giao dịch
                        bên ngoài.
Trigger:                Người dùng, sau UC-011, kiểm tra tính an toàn của phiên Paper Trading.
Preconditions:          Một phiên Paper Trading (UC-011) đã diễn ra.
Inputs:                 Khoảng thời gian của phiên Paper Trading.
Main flow:              1. Hệ thống hiển thị xác nhận: environment của mọi Order/ExecutionResult
                           trong phiên là PAPER; không route mạng nào đi tới exchange endpoint thật.
Alternate/failure:      Người dùng cố gắng chuyển sang Live → §8 "attempt to use Live behavior".
Observable outcome:     Người dùng có bằng chứng tường minh Paper Trading không đặt lệnh thật.
Evidence consumed:      environment field trên Order/ExecutionResult (order.md, execution-result.md).
Evidence produced:      KHÔNG.
PR traceability:        PR-027.
Domain vocabulary used: order.md, execution-result.md.
Out-of-scope boundary:  KHÔNG định nghĩa cơ chế audit network kỹ thuật cụ thể (Phase 1).
```

### 9.5-equivalent — Review

**UC-016 — Trace Decision → Position lineage**
```text
Primary actor:         Ride user (§2).
Goal:                   Với một Position contribution bất kỳ, truy vết ngược toàn bộ causation trace
                        về Decision gốc đã sinh ra nó.
Trigger:                Người dùng chọn một Fill/Position contribution để review.
Preconditions:          Fill/Position contribution tồn tại (UC-013/UC-014).
Inputs:                 Fill/Position identity.
Main flow:              1. Người dùng chọn một Fill đóng góp Position.
                        2. Hệ thống hiển thị causation trace ngược: Fill→ExecutionResult→Order→
                           Execution Intent→RiskEvaluation→Trade Intent→Decision gốc — KHÔNG mắt xích
                           thiếu.
Alternate/failure:      Mắt xích thiếu (KHÔNG dự kiến theo Domain Contract đã Consolidated Stable) →
                        ngoài phạm vi tài liệu này (governance/data-integrity concern).
Observable outcome:     Người dùng truy vết được trọn vẹn từ Position ngược về Decision gốc.
Evidence consumed:      Toàn bộ causation_refs/correlation_id chain Decision→...→Position.
Evidence produced:      KHÔNG.
PR traceability:        PR-028.
Domain vocabulary used: decision.md, trade-intent.md, risk.md, execution-intent.md, order.md,
                        execution-result.md, fill.md, position.md.
Out-of-scope boundary:  KHÔNG hiển thị chi tiết UI trace visualization (Package 0.3-C).
```

**UC-017 — Compare reconstructed and recorded historical state**
```text
Primary actor:         Ride user (§2).
Goal:                   So sánh state tái dựng qua Replay (UC-004) tại một cursor lịch sử với state đã
                        hiển thị tại đúng thời điểm đó khi ghi nhận ban đầu, xác nhận không silent
                        drift.
Trigger:                Người dùng, đang Review, chọn so sánh một cursor lịch sử.
Preconditions:          UC-004 đã chạy cho cursor đó.
Inputs:                 Replay Cursor cần so sánh.
Main flow:              1. Hệ thống resolve ReplayState(C) hiện tại (UC-004).
                        2. Hệ thống so sánh với state đã từng hiển thị/ghi nhận tại đúng cursor đó.
                        3. NẾU không có correction nào xảy ra giữa hai thời điểm → hiển thị "No
                           conflict". NẾU có correction → hiển thị khác biệt tường minh kèm fact
                           correction liên quan (KHÔNG ẩn/repaint).
Alternate/failure:      Correction visible SAU historical cursor đang xem → §8 "correction visible
                        after historical cursor".
Observable outcome:     Người dùng xác nhận không có silent drift, hoặc thấy rõ correction nào đã áp
                        dụng.
Evidence consumed:      ReplayState(C) (UC-004), correction/invalidation fact liên quan nếu có.
Evidence produced:      Kết quả so sánh — non-authoritative, KHÔNG phải fact mới.
PR traceability:        PR-029.
Domain vocabulary used: replay-event.md.
Out-of-scope boundary:  KHÔNG định nghĩa cơ chế lưu snapshot lịch sử cụ thể (Phase 1).
```

**UC-018 — Inspect a correction without repainting history**
```text
Primary actor:         Ride user (§2).
Goal:                   Xem một correction (fact mới thay thế fact cũ) mà KHÔNG bất kỳ giá trị lịch sử
                        nào bị sửa/xóa ngầm (No Repaint).
Trigger:                Người dùng phát hiện hoặc được thông báo một correction tồn tại (từ UC-017 hoặc
                        trực tiếp).
Preconditions:          Một correction fact (`*FactInvalidated` + replacement) tồn tại cho một Decision/
                        RiskEvaluation/ExecutionResult/Fill/Position liên quan.
Inputs:                 Fact identity cần kiểm tra correction.
Main flow:              1. Người dùng chọn một fact.
                        2. Hệ thống hiển thị fact gốc (vẫn resolvable, append-only) VÀ fact replacement
                           (nếu có), với liên kết tường minh (supersedes_fact_ref) — KHÔNG hiển thị chỉ
                           một giá trị "đã sửa" ẩn danh nguồn gốc.
Alternate/failure:      KHÔNG áp dụng — hiển thị luôn cả hai trạng thái (trước/sau correction) là hành
                        vi bắt buộc, không có nhánh lỗi.
Observable outcome:     Người dùng thấy rõ ràng: giá trị nào là gốc, giá trị nào là correction, và tại
                        sao (invalidation reference).
Evidence consumed:      Fact gốc + `*FactInvalidated` + fact replacement (nếu có).
Evidence produced:      KHÔNG — quan sát thuần túy.
PR traceability:        PR-011, PR-030.
Domain vocabulary used: decision.md, risk.md, execution-result.md, fill.md (correction lineage pattern
                        đồng nhất xuyên suốt).
Out-of-scope boundary:  KHÔNG định nghĩa UI diff visualization (Package 0.3-C).
```

### 9.6-equivalent — Improve

**UC-019 — Create a new Strategy Definition Version**
```text
Primary actor:         Ride user (§2).
Goal:                   Tạo một Strategy Definition Version mới, tách biệt hoàn toàn khỏi version cũ.
Trigger:                Người dùng, sau Review (UC-016–UC-018), quyết định cải thiện Strategy.
Preconditions:          Một Strategy Definition (identity) đã tồn tại (strategy.md).
Inputs:                 Nội dung Strategy Definition Version mới.
Main flow:              1. Người dùng tạo một Strategy Definition Version mới.
                        2. Hệ thống gán version identity mới, tách biệt version cũ (append-only,
                           strategy.md).
                        3. Một Strategy Instance mới có thể gắn version mới này (quay lại UC-002).
Alternate/failure:      KHÔNG áp dụng tại tầng product — mọi validation nội dung cụ thể thuộc phạm vi
                        strategy.md (không sửa tại đây).
Observable outcome:     Một Strategy Definition Version mới tồn tại, độc lập version cũ.
Evidence consumed:      Strategy Definition (identity) hiện có.
Evidence produced:      Strategy Definition Version mới (strategy.md).
PR traceability:        PR-031.
Domain vocabulary used: strategy.md, ADR-013.
Out-of-scope boundary:  KHÔNG định nghĩa nội dung/schema Strategy Definition cụ thể (thuộc
                        strategy.md, không sửa).
```

**UC-020 — Compare historical outcomes across Strategy Definition Versions**
```text
Primary actor:         Ride user (§2).
Goal:                   So sánh Decision/Execution outcome giữa Strategy Instance gắn version cũ và
                        Strategy Instance gắn version mới (UC-019).
Trigger:                Người dùng, sau khi tạo version mới, muốn so sánh với version cũ.
Preconditions:          Có ít nhất hai Strategy Instance, gắn hai Strategy Definition Version khác
                        nhau, mỗi cái có Decision/Execution outcome (qua Backtest §9.3 và/hoặc Paper
                        §9.4).
Inputs:                 Hai (hoặc nhiều) Strategy Instance identity.
Main flow:              1. Người dùng chọn các Strategy Instance cần so sánh.
                        2. Hệ thống hiển thị Decision/Execution outcome của từng Strategy Instance
                           tách biệt hoàn toàn, không lẫn lộn (WF-INV-3 áp dụng per-instance).
Alternate/failure:      Một Strategy Instance chưa có outcome nào (chưa Backtest/Paper) → hiển thị rỗng
                        cho Instance đó, KHÔNG lỗi cho toàn bộ so sánh.
Observable outcome:     Người dùng so sánh được outcome giữa các version.
Evidence consumed:      Decision/Execution outcome của từng Strategy Instance (UC-007–UC-014).
Evidence produced:      KHÔNG — so sánh hiển thị thuần túy.
PR traceability:        PR-031.
Domain vocabulary used: strategy.md, decision.md.
Out-of-scope boundary:  KHÔNG định nghĩa công thức so sánh/scoring tổng hợp (`OQ-003`).
```

**UC-021 — Preserve access to old-version evidence**
```text
Primary actor:         Ride user (§2).
Goal:                   Truy vấn được Decision/Execution outcome của một Strategy Definition Version
                        không còn active.
Trigger:                Người dùng, sau khi chuyển sang version mới, cần xem lại evidence version cũ.
Preconditions:          Strategy Definition Version cũ đã từng chạy (có Decision/Execution outcome).
Inputs:                 Strategy Definition Version cũ (identity).
Main flow:              1. Người dùng chọn một Strategy Definition Version cũ.
                        2. Hệ thống resolve toàn bộ Decision lịch sử gắn với version đó qua đúng
                           authoritative event stream — KHÔNG mất truy cập dù version không còn active.
Alternate/failure:      KHÔNG áp dụng — durable append-only log (I-12) đảm bảo truy cập luôn khả dụng.
Observable outcome:     Người dùng truy vấn được đầy đủ evidence lịch sử của version cũ.
Evidence consumed:      Toàn bộ Decision fact gắn Strategy Definition Version cũ.
Evidence produced:      KHÔNG.
PR traceability:        PR-032.
Domain vocabulary used: strategy.md, decision.md.
Out-of-scope boundary:  KHÔNG định nghĩa retention/archival policy cụ thể (Phase 1).
```

## 7. Cross-stage handoffs

```text
Research → Replay
  Exit condition (Research):   Strategy Instance đã chọn (UC-002); Instrument/Venue hợp lệ; KHÔNG
                                side-effect fact nào được tạo (UC-003).
  Evidence carried forward:    Strategy Instance identity, Instrument/Venue selection.
  Entry condition (Replay):    Strategy Instance PHẢI GIỮ NGUYÊN trong suốt phiên Replay (WF-INV-3).
  PR traceability:             PR-001, PR-016.

Replay → Backtest
  Exit condition (Replay):     Người dùng đã xem historical reconstruction (UC-004), tuỳ chọn parity
                                recomputation (UC-005).
  Evidence carried forward:    Strategy Instance identity (KHÔNG đổi); hiểu biết về historical state
                                đã xem.
  Entry condition (Backtest):  Strategy Instance GIỮ NGUYÊN (WF-INV-3); khoảng thời gian bounded được
                                chọn mới cho Backtest run.
  PR traceability:             PR-016, PR-021.
  Lưu ý:                       Replay và Backtest là hai capability ĐỘC LẬP — Replay KHÔNG phải hard
                                precondition kỹ thuật của Backtest; hai bước liên tiếp trong hành trình
                                walking-skeleton (§4) nhưng không có PR nào ép buộc thứ tự kỹ thuật.

Backtest → Paper
  Exit condition (Backtest):   Người dùng đã xem strategy-level evaluable result (UC-009), tuỳ chọn so
                                sánh cross-run/cross-version (UC-010).
  Evidence carried forward:    Decision hiện có (nếu người dùng chọn thực thi dựa trên Decision từ
                                Backtest/Research) — KHÔNG có Backtest fact nào được "chuyển" thành
                                PAPER fact (Backtest authority boundary).
  Entry condition (Paper):     Người dùng TỰ QUYẾT ĐỊNH tiến hành Paper — đây là judgment gate của
                                người dùng, phù hợp "Research Before Capital" (Vision §1.6), KHÔNG phải
                                hard precondition được PR nào enforce kỹ thuật.
  PR traceability:             PR-034 (evidence để quyết định); PR-024 (Paper tự thân độc lập).

Paper → Review
  Exit condition (Paper):      ExecutionResult đã resolve (EXECUTED/NOT_EXECUTED); nếu EXECUTED, Fill/
                                Position đã derive (UC-011–UC-015).
  Evidence carried forward:    Toàn bộ causation chain Decision→...→Position.
  Entry condition (Review):    Evidence đầy đủ, không đứt đoạn, sẵn sàng cho causation trace (UC-016).
  PR traceability:             PR-007, PR-028.

Review → Improve
  Exit condition (Review):     Người dùng đã trace causation (UC-016), so sánh reconstructed/recorded
                                state (UC-017), inspect correction nếu có (UC-018).
  Evidence carried forward:    Nhận định về hiệu quả Strategy hiện tại (KHÔNG phải một fact hệ thống —
                                judgment của người dùng).
  Entry condition (Improve):   Người dùng quyết định tạo Strategy Definition Version mới (UC-019).
  PR traceability:             PR-031.

Improve → Research (vòng lặp)
  Exit condition (Improve):    Strategy Definition Version mới đã tạo (UC-019); evidence version cũ
                                vẫn truy cập được (UC-021).
  Evidence carried forward:    Strategy Definition Version mới — dùng để tạo Strategy Instance mới
                                (UC-002, vòng lặp).
  Entry condition (Research):  Giống hệt Research→Replay ở trên, với Strategy Instance MỚI.
  PR traceability:             PR-031, PR-032, PR-001.
```

## 8. Failure and non-evaluable paths

Với mọi scenario KHÔNG có controlling behavior tường minh trong `product-requirement.md`/Domain Contract, áp dụng ĐÚNG bốn nguyên tắc sau (KHÔNG tự phát minh resolution semantics):

```text
workflow stops
state remains observable
reason is disclosed
no downstream authoritative action occurs
```

| Scenario | Behavior | PR/Domain traceability |
|---|---|---|
| Missing Strategy Instance | Workflow dừng tại UC-002; state (không có Instance nào chọn) hiển thị rõ; reason "no Strategy Instance selected" disclosed; không Decision nào được tạo. | PR-001 (không controlling resolution cụ thể — fallback bốn nguyên tắc trên). |
| Invalid Instrument/Venue selection | Workflow dừng tại UC-001/UC-011; lựa chọn ngoài tập TradableListing bị từ chối TRƯỚC khi tạo bất kỳ fact nào; reason disclosed. | PR-003 (reject trước khi tạo fact — có controlling rule). |
| Missing historical evidence | Workflow dừng tại UC-001/UC-006; state hiển thị "no data at this point/interval"; reason disclosed; không fact nào được tạo. | PR-015, PR-021 (không controlling resolution cụ thể — fallback bốn nguyên tắc). |
| Replay cursor with unavailable references | Workflow dừng tại UC-004; cursor được chọn nhưng reconstruction không hoàn tất; reason disclosed (artifact không materialize); không Decision nào được tạo. | PR-020/I-5 (self-contained Replay — không controlling resolution cho reference thiếu — fallback). |
| Parity mismatch | Workflow KHÔNG dừng runtime — hiển thị finding match/mismatch (UC-005); mismatch KHÔNG tự động ghi đè/tạo Decision; cần Product Owner/reviewer xem xét ngoài phạm vi runtime tự động. | PR-010, PR-019 (có controlling rule — Replay authority boundary). |
| Backtest run insufficient evaluable evidence | Workflow dừng tại UC-008/UC-009; run identity vẫn tồn tại và observable; reason "no simulated exposure change produced" disclosed; không strategy-level result nào được hiển thị như evaluable. | PR-033, PR-034 (fallback bốn nguyên tắc — chưa có controlling resolution cụ thể). |
| RiskEvaluation REJECTED | Workflow dừng tại UC-011 bước 2; result + reason code hiển thị (risk.md); KHÔNG Execution Intent/Order nào được tạo. | PR-006 (có controlling rule). |
| RiskEvaluation NON_EVALUABLE | Giống REJECTED — workflow dừng, result + reason code hiển thị, KHÔNG Execution Intent/Order. | PR-006 (có controlling rule). |
| Order NOT_EXECUTED | ExecutionResult hiển thị NOT_EXECUTED; zero Fill hiển thị rõ; không downstream action. | PR-007, PR-024 (có controlling rule). |
| Fill absent | UC-013 hiển thị "no Fill for this ExecutionResult" (NOT_EXECUTED case); không economics nào được hiển thị/suy diễn. | PR-025 (có controlling rule, hệ quả của NOT_EXECUTED). |
| Position NON_EVALUABLE | UC-014 hiển thị `NON_EVALUABLE` + `contributing_fill_refs` đầy đủ — KHÔNG chọn một Fill/aggregate/report FLAT. | PR-026 (có controlling rule tường minh). |
| Correction visible after historical cursor | UC-017 hiển thị khác biệt tường minh kèm fact correction liên quan — KHÔNG ẩn/repaint giá trị gốc (UC-018). | PR-011, PR-029, PR-030 (có controlling rule). |
| Attempt to use Live behavior | Workflow dừng NGAY LẬP TỨC; state hiển thị "Live is Unauthorized, OQ-002 Open"; reason disclosed; KHÔNG downstream authoritative action, KHÔNG route mạng tới exchange thật. | PR-027, `OQ-002` (có controlling rule tường minh). |

## 9. Evidence and traceability requirements

### 9a. Use Case → PR mapping

Xem bảng đầy đủ tại §5 (cột "Primary PR(s)") — mỗi Use Case tại §6 lặp lại chính xác mapping đó trong field "PR traceability".

### 9b. Workflow stage → PR mapping

```text
Research  → PR-001, PR-002, PR-003, PR-015, PR-016, PR-017
Replay    → PR-008, PR-009, PR-010, PR-012, PR-018, PR-019, PR-020
Backtest  → PR-021, PR-022, PR-023, PR-033, PR-034
Paper     → PR-002, PR-003, PR-007, PR-013, PR-014, PR-024, PR-025, PR-026, PR-027
Review    → PR-009, PR-011, PR-028, PR-029, PR-030
Improve   → PR-031, PR-032
```

### 9c. Use Case → Domain vocabulary mapping

```text
UC-001            candle.md, swing.md, structure.md, regime.md, feature.md, context.md, instrument.md,
                   venue.md
UC-002            strategy.md
UC-003            decision.md
UC-004            replay-event.md, decision.md, trade-intent.md, risk.md, execution-intent.md,
                   order.md, execution-result.md, fill.md, position.md
UC-005            decision.md, replay-event.md
UC-006–UC-010     decision.md, risk.md, strategy.md (Backtest evidence — domain-representation
                   deferred, §9d); execution-result.md/fill.md/position.md (boundary reference only)
UC-011–UC-015     decision.md, trade-intent.md, risk.md, execution-intent.md, order.md,
                   execution-result.md, fill.md, position.md
UC-016            decision.md, trade-intent.md, risk.md, execution-intent.md, order.md,
                   execution-result.md, fill.md, position.md
UC-017            replay-event.md
UC-018            decision.md, risk.md, execution-result.md, fill.md
UC-019–UC-021     strategy.md, decision.md, ADR-013
```

### 9d. Explicit deferred-domain dependency list

```text
Backtest Domain Contract/entity/event/schema:  KHÔNG tồn tại. UC-006–UC-010 mô tả hành vi product-
  level BẮT BUỘC (deterministic simulated economic evidence, exposure/position progression, strategy-
  level evaluable result) nhưng KHÔNG giả định "BacktestOrder"/"BacktestFill"/"BacktestPosition"/
  "BacktestExecutionResult" hay bất kỳ entity nào tương đương đã tồn tại — labeled "product-required,
  domain-representation deferred" tại UC-008/UC-009. Quyết định author Domain Contract riêng cho
  Backtest là Product Owner decision, ngoài phạm vi Package 0.3-A/0.3-B.

Research Domain Contract:  Tương tự — KHÔNG tồn tại research.md; UC-001–UC-003 mô tả hành vi quan sát
  thuần túy trên Domain Contract ĐÃ có (candle.md…context.md, strategy.md), KHÔNG giả định entity
  Research riêng.
```

## 10. Deferred questions

```text
OQ-002:
  Open
  Strategy Lifecycle Live-gate deferred — kế thừa nguyên vẹn từ product-requirement.md §13. UC-015 CHỈ
  xác nhận Paper KHÔNG đặt lệnh thật; §8 "attempt to use Live behavior" CHỈ dừng workflow và disclose
  — KHÔNG định nghĩa điều kiện chuyển Live.

OQ-003:
  Open
  Concrete Product Metrics deferred — kế thừa nguyên vẹn từ product-requirement.md §13. UC-009/UC-010
  yêu cầu strategy-level evaluable result quan sát/so sánh được nhưng KHÔNG định nghĩa threshold/target/
  công thức scoring cụ thể nào.

Backtest/Research Domain Contract modeling:
  Kế thừa nguyên vẹn từ product-requirement.md §13 — xem §9d ở trên cho chi tiết áp dụng tại tầng
  workflow.
```

## 11. Explicit Non-Goals and Out-of-Scope

Kế thừa nguyên vẹn [`product-requirement.md`](./product-requirement.md) §11/§12 (Non-Goals/Out-of-Scope) — KHÔNG lặp lại toàn văn.

**Ngoài phạm vi tường minh của riêng tài liệu này (Package 0.3-B):**

- Screen layout, wireframe, component hierarchy, UX flow diagram chi tiết (Package 0.3-C, chưa author) — mọi Use Case tại §6 CHỈ mô tả behavior, KHÔNG mô tả UI cụ thể.
- Domain Contract state machine/transition mới (mọi Use Case CHỈ tham chiếu state machine đã `Consolidated Stable`).
- Backtest/Replay domain fact mới (`BacktestOrder`/`BacktestFill`/`BacktestPosition`/`BacktestExecutionResult`/`ReplayDecision` hay tương đương).
- Tái sử dụng PAPER fact làm Backtest authority.
- API/database/backend/frontend/infrastructure architecture.
- Security/custody/deployment.
- Product Metric threshold/target cụ thể (`OQ-003`).
- Live-gate criteria cụ thể (`OQ-002`).
- Mở rộng multi-tenant/đa tài sản (ngoài ADR-007 Phase 0-3).
- Product requirement mới — mọi Use Case CHỈ dùng `PR-XXX` đã tồn tại tại `product-requirement.md`.

## 12. Acceptance criteria for Package 0.3-B

```text
1. Toàn bộ 13 mục nội dung bắt buộc (§1–§13) có mặt và đầy đủ.
2. 21 Use Case (UC-001–UC-021), ID duy nhất, liên tục — bao trùm đầy đủ minimum coverage list cho cả
   sáu giai đoạn (Research/Replay/Backtest/Paper/Review/Improve).
3. Mỗi Use Case có đủ mười ba trường: Title/Primary actor/Goal/Trigger/Preconditions/Inputs/Main flow/
   Alternate-or-failure flows/Observable outcome/Evidence produced-or-consumed/PR traceability/Domain
   vocabulary used/Out-of-scope boundary.
4. Mọi workflow step truy vết được về một hoặc nhiều `PR-XXX` ID đã tồn tại tại `product-requirement.md`
   — KHÔNG có Use Case/step mồ côi PR traceability, KHÔNG product requirement mới nào được tạo.
5. Replay authority boundary giữ nguyên: historical reconstruction (mặc định) tách bạch parity
   recomputation (tuỳ chọn, non-authoritative); KHÔNG `ReplayDecision`; KHÔNG Decision trùng lặp; mọi so
   sánh dùng `canonical semantic-decision hash`.
6. Backtest authority boundary giữ nguyên: KHÔNG tái sử dụng PAPER Order/ExecutionResult/Fill/Position
   làm Backtest authority; KHÔNG entity/event Backtest mới; simulation/fee/slippage/accounting/PnL
   KHÔNG được định nghĩa; bước thiếu domain representation được label "product-required, domain-
   representation deferred", KHÔNG lấp đầy khoảng trống ngầm.
7. Paper workflow (UC-011–UC-015) dùng ĐÚNG chuỗi C7: Decision→Trade Intent→RiskEvaluation→Execution
   Intent→Order→OrderSubmissionRequest→ExecutionResultComputation→PaperExecutionObservation→
   ExecutionResult→Fill→Position — Fill economics từ PaperExecutionObservation, Position từ eligible
   Fill lineage, NON_EVALUABLE khi xung đột, KHÔNG lệnh thật.
8. Mọi failure/non-evaluable path tại §8 tuân thủ ĐÚNG bốn nguyên tắc fallback (workflow stops/state
   observable/reason disclosed/no downstream authoritative action) khi KHÔNG có controlling behavior
   tường minh — KHÔNG tự phát minh resolution semantics.
9. KHÔNG sửa `product-requirement.md`/Domain Contract/ADR/Constitution/architecture nào.
10. `OQ-002`/`OQ-003` giữ nguyên `Open`, không bị đóng ngầm; Live vẫn `Unauthorized`.
11. YAML frontmatter hợp lệ, `version: "0.1"`, `status: Draft`, `approved_by: null`, `approved_at: null`.
12. Baseline sẵn sàng cho ChatGPT Review A + Independent Review B trên CÙNG một commit/blob.
```

## 13. Handoff requirements for Package 0.3-C

Package 0.3-C (`ux-blueprint.md`) PHẢI:

1. Tham chiếu mọi screen/flow về đúng một hoặc nhiều `UC-XXX` ID tại đây — KHÔNG tự phát minh use case/workflow behavior mới ở tầng UX.
2. Giữ nguyên khung sáu-giai-đoạn (Research→Replay→Backtest→Paper→Review→Improve, §4/§6) — không thêm giai đoạn mới nếu chưa có Product Owner authorization riêng.
3. Giữ nguyên walking-skeleton discipline — 21 Use Case là bộ hành vi tối thiểu, KHÔNG mở rộng thêm behavior mới mà không có PR/UC tương ứng.
4. KHÔNG đóng `OQ-002`/`OQ-003` — kế thừa nguyên trạng `Open` từ §10.
5. Kế thừa nguyên vẹn **Replay authority boundary** (§6 UC-004/UC-005) và **Backtest authority boundary** (§6 UC-006–UC-010) — KHÔNG thiết kế screen/flow như thể Backtest tạo/tái sử dụng PAPER fact, hay Replay tạo Decision mới/`ReplayDecision`.
6. KHÔNG author screen layout/wireframe/component hierarchy VƯỢT QUÁ những gì cần để thể hiện behavior đã mô tả tại §6 — Package 0.3-C sở hữu HÌNH THỨC hiển thị, KHÔNG sở hữu behavior/logic (đã đóng tại đây).
7. KHÔNG định nghĩa Domain Contract semantic mới — mọi state/transition tham chiếu phải resolve về Domain Contract đã `Consolidated Stable`.
8. Với mỗi Failure/non-evaluable path tại §8, screen/flow tương ứng PHẢI thể hiện đúng bốn nguyên tắc (workflow stops/state observable/reason disclosed/no downstream authoritative action) — KHÔNG thiết kế UI ngụ ý một resolution semantics chưa được định nghĩa.
