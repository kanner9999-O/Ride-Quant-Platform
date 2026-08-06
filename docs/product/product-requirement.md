---
id: product-requirement
title: Product Requirement
version: "0.3"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-07-31"
last_review: null
next_review: null
---

# Product Requirement

> **Vai trò của tài liệu này:** Artifact đầu tiên của Package 0.3-A (Phase 0.3 — Product Requirement · Use Case & Workflow · UX Blueprint). Draft, chưa Approved/Locked, **chưa `Consolidated Stable`**. Dịch [Chapter 1 Vision](../constitution/01-vision.md) (Locked v2.3) thành các requirement cụ thể, testable, bounded — KHÔNG lặp lại nguyên văn Vision, KHÔNG tự quyết architecture. Controlling sources: [Chapter 1](../constitution/01-vision.md) (Vision), [Chapter 2](../constitution/02-platform-invariants.md) (Platform Invariants, Locked), [Chapter 4](../constitution/04-domain-principles.md) (Domain Principles, Locked), [ADR-007](../adr/ADR-007.md) (Locked — nội bộ/single-workspace/crypto-only/2-3 sàn), và toàn bộ Domain Contract `Consolidated Stable` tại [`/docs/domain/`](../domain/README.md) (Package 0.2-A/B/C). Tài liệu này CHỈ dùng vocabulary ĐÃ tồn tại trong Domain Contract — KHÔNG định nghĩa concept domain mới.

**v0.2 — bounded correction (đóng consolidated Review A + Independent Review B findings, `P03A-MAJ-01`/`P03A-MIN-01`/`P03A-MIN-02`/`P03A-B-MIN-03`):** (1) `P03A-MAJ-01` — Backtest (§9.3) nay yêu cầu simulated economic evidence VÀ exposure/position progression quan sát/evaluate được (`PR-033`, MỚI) VÀ strategy-level evaluable result so sánh được cross-run/cross-version (`PR-034`, MỚI), gắn stable run identity (`PR-021` cập nhật) — CỘNG một **Backtest authority boundary** tường minh (KHÔNG tái sử dụng PAPER Order/ExecutionResult/Fill/Position, KHÔNG author entity/event Backtest, KHÔNG định nghĩa simulation/fee/slippage/accounting/PnL). (2) `P03A-MIN-01` — thay thuật ngữ chung chung "Decision hash" bằng `canonical semantic-decision hash` (`PR-010`/`PR-019`), định nghĩa rõ theo Decision Contract authoritative, loại trừ runtime identity/envelope/transport/processing metadata — KHÔNG hardcode danh sách field canonical. (3) `P03A-MIN-02` — bỏ quy tắc "resolve về đúng một nguồn" — thay bằng "một hoặc nhiều applicable authoritative source, có thể kết hợp, mọi nguồn phải material" (Authority boundary, §14 item 3). (4) `P03A-B-MIN-03` — `PR-019` viết lại tách bạch historical reconstruction (mặc định) và parity recomputation (tuỳ chọn, non-authoritative) — CỘNG một **Replay authority boundary** tường minh (không append Decision trùng lặp, không tạo Replay authority stream, không mutate Decision đã ghi nhận, không `ReplayDecision`). Bounded — không đổi 32 requirement gốc ngoài các sửa đổi tường minh trên, không đổi sáu-giai-đoạn lifecycle, không đóng OQ-002/OQ-003, không Approve/Lock/Consolidate.

**v0.3 — CANDIDATE semantic clarification (2026-08-06), KHÔNG Approved/Consolidated, pending Review A/Independent Review B/Product Owner decision — Product Owner authorized (timestamp 2026-08-06T09:21:00+07:00) bounded source-semantics clarification cho VIEW-003 replay parity verification:** `canonical semantic-decision hash` (PR-010/PR-019) NAY resolve tới một định nghĩa CỤ THỂ — `decision.md` v0.4 §9a (CANDIDATE, cùng transaction) cung cấp **Canonical Decision Semantic Representation** VÀ **Canonical Decision Semantic Digest** lần đầu tiên; PRD này VẪN KHÔNG hardcode danh sách field (đúng nguyên tắc I-2 Verification, KHÔNG đổi) — CHỈ cập nhật pointer từ "chưa resolve" thành "resolve tại decision.md §9a." PR-010/PR-019 acceptance evidence cập nhật thêm outcome INDETERMINATE (bên cạnh match/mismatch đã có) — đúng §9a.6 outcome model MỚI. Bounded — KHÔNG đổi 34 requirement gốc ngoài cập nhật pointer/outcome trên, KHÔNG chọn computation owner/module/package/dependency edge/ADR, KHÔNG đổi Backtest/Replay authority boundary đã pin, KHÔNG Approve/Lock/Consolidate.

**Authority boundary:** tài liệu này sở hữu **product requirement content** cho Phase 0.3 — KHÔNG sở hữu domain semantics (thuộc `/docs/domain/`, không sửa), KHÔNG sở hữu architecture quyết định (thuộc Phase 1, `/docs/architecture/`), KHÔNG sở hữu UX screen/flow design chi tiết (thuộc Package 0.3-C `ux-blueprint.md`, chưa author), KHÔNG đóng Open Question nào (`OQ-002`/`OQ-003` vẫn `Open`, xem §13), KHÔNG authorize Live, KHÔNG tuyên bố Phase 0.3/Phase 0 hoàn thành.

**v0.2 (đóng `P03A-MIN-02`) — quy tắc traceability nguồn, KHÔNG còn "đúng một":**
```text
Every PR must have one or more applicable authoritative sources.

A PR may combine:
  Vision product intent
  Platform Invariant guarantees
  Consolidated Stable Domain Contract semantics or vocabulary

Every cited source must materially support the requirement.

No PR may be orphaned or supported only by non-authoritative material.
```
Một requirement CÓ THỂ đồng thời truy vết Vision, Platform Invariant, VÀ Domain Contract — không bị ép resolve về đúng một nguồn duy nhất; điều kiện bắt buộc DUY NHẤT là mọi nguồn được trích dẫn phải material (đóng góp thực chất), và không PR nào được phép mồ côi nguồn hoặc chỉ dựa vào tài liệu non-authoritative.

## 1. Document purpose and authority boundary

Tài liệu này trả lời: **"Ride phải làm được gì cho người dùng nội bộ, trong ranh giới Phase 0-3 đã chốt (ADR-007), để hiện thực hóa Vision?"** — ở mức **product behavior**, KHÔNG ở mức implementation. Nó là input bắt buộc cho Package 0.3-B (`use-case-workflow.md`) và Package 0.3-C (`ux-blueprint.md`) — cả hai PHẢI truy vết ngược về đúng một `PR-XXX` ID tại đây, KHÔNG được tự phát minh requirement mới ở tầng workflow/UX.

## 2. Product problem

Trading là một nghề đòi hỏi quy trình chuyên nghiệp, không phải may mắn ([Vision §1.2](../constitution/01-vision.md)). Workflow hiện tại của trader bị phân mảnh qua nhiều công cụ rời rạc (Exchange, TradingView, Excel, Notes, Journal, Risk Calculator, Backtesting Software), khiến quyết định khó review lại, quản lý rủi ro thiếu nhất quán, sai lầm lặp lại, hiệu suất không đo lường khách quan được. Ride giải quyết vấn đề này bằng một quy trình hợp nhất — nghiên cứu, thực thi, review, cải thiện — trong một hệ thống duy nhất, giải thích được và có bằng chứng đầy đủ cho mọi quyết định.

## 3. Target users within approved internal scope

Theo [Vision §1.5](../constitution/01-vision.md) VÀ ranh giới đã chốt tại [ADR-007](../adr/ADR-007.md) (nội bộ, một workspace, KHÔNG multi-tenant): người dùng của Phase 0-3 là **thành viên nội bộ của một team vận hành nhiều Strategy trên vốn của chính team đó** — vai trò định hướng thiết kế sản phẩm (Retail Trader / Professional Trader / Quant Researcher / Strategy Developer, [Vision §1.5](../constitution/01-vision.md)) chứ KHÔNG phải các workspace/tenant tách biệt. Một Account duy nhất tồn tại trong Phase 0-3 (ADR-007 — Account là first-class entity ngay từ Domain Model, nhưng chỉ một Account được vận hành thực tế); người dùng thao tác qua Strategy Instance ([`strategy.md`](../domain/strategy.md)) gắn với Account đó.

## 4. User outcomes

Người dùng nội bộ, sau khi dùng Ride, phải đạt được (bám sát [Vision §1.4/§1.8](../constitution/01-vision.md), diễn giải thành outcome quan sát được — KHÔNG phải KPI cụ thể, xem §13):

- Xem lại được **chính xác** input, context, và lý do đứng sau bất kỳ Decision nào đã ghi nhận (không suy diễn/dựng lại sau sự kiện).
- So sánh được kết quả một Strategy Instance giữa Replay/Backtest/Paper mà không nghi ngờ có sự khác biệt logic ẩn.
- Biết chính xác vì sao một Trade Intent bị Risk Gateway từ chối hoặc chấp thuận.
- Xem được Position hiện tại bắt nguồn từ đúng những Fill nào, với economics đã ghi nhận, KHÔNG phải suy luận lại.
- Cải thiện một Strategy qua version mới mà KHÔNG mất khả năng truy vết version cũ.

## 5. Product principles inherited from Vision

Sáu nguyên tắc dưới đây kế thừa nguyên vẹn [Vision §1.7](../constitution/01-vision.md) — mọi requirement tại §7–§9 PHẢI phục vụ ít nhất một nguyên tắc:

1. **Everything Must Be Explainable** — diễn giải sản phẩm của [I-1](../constitution/02-platform-invariants.md).
2. **Everything Must Be Reproducible** — diễn giải sản phẩm của [I-2](../constitution/02-platform-invariants.md).
3. **Everything Must Be Measurable** — yêu cầu evidence đo lường được tồn tại; KHÔNG yêu cầu threshold/target cụ thể (`OQ-003`, §13).
4. **Research Before Capital** — mọi Strategy phải qua Research/Replay/Backtest/Paper trước khi có thể tiến gần Live (Live tự nó vẫn `OQ-002`, §13).
5. **Evidence Over Opinion** — ưu tiên bằng chứng đo lường được hơn ý kiến chủ quan.
6. **Build Better Traders** — sản phẩm phục vụ cải thiện quy trình, KHÔNG tối đa hóa tần suất giao dịch/screen time.

## 6. Product scope

```text
Target operating model:
  internal trading workspace    (ADR-007 — KHÔNG multi-tenant)
  single workspace               (một Account vận hành thực tế, Account là first-class entity)
  crypto-only                    (ADR-007 — KHÔNG đa tài sản)
  2–3 exchanges                  (ADR-007)

Primary lifecycle (walking skeleton):
  Research → Replay → Backtest → Paper → Review → Improve

Live: đề cập DUY NHẤT như một lifecycle boundary bị hoãn (deferred) — KHÔNG author hành vi Live tại đây.
```

Phạm vi sản phẩm CHỈ bao trùm hành vi user-facing PHÍA TRÊN Domain Contract đã `Consolidated Stable` (Package 0.2-A/B/C) — KHÔNG mở rộng/redefine bất kỳ entity/event/invariant nào đã đóng tại đó.

## 7. Functional requirements

**PR-001 — Chọn Strategy Instance để vận hành**
```text
Statement:          Người dùng PHẢI chọn được ĐÚNG MỘT Strategy Instance (gắn một Strategy Definition
                     Version cụ thể) để Research/Replay/Backtest/Paper hoạt động dựa trên đó.
Rationale:           Không có Strategy Instance xác định, không Decision nào có thể sinh ra deterministic
                     (đúng bài học "logical computation key" xuyên suốt Phase 0.2).
Source:              Vision §1.5; strategy.md (Strategy Definition Version + Strategy Instance).
Acceptance evidence: Với mọi Decision được tạo ra trong một phiên làm việc, Decision đó resolve được về
                     ĐÚNG MỘT Strategy Instance đã chọn tại đầu phiên — không có Decision "mồ côi" Strategy.
```

**PR-002 — Toàn bộ hoạt động scoped theo một Account**
```text
Statement:          Mọi Trade Intent/RiskEvaluation/Execution Intent/Order/ExecutionResult/Fill/Position
                     người dùng thao tác PHẢI thuộc đúng một Account (Account hiện tại của workspace).
Rationale:           ADR-007 — Account first-class ngay từ Phase 0.2, single-operator hiện tại.
Source:              ADR-007; account.md.
Acceptance evidence: Không có bất kỳ fact nào (Trade Intent .. Position) thiếu account_id hợp lệ, và
                     account_id đó khớp Account duy nhất của workspace.
```

**PR-003 — Chọn Instrument/Venue trong tập đã đăng ký**
```text
Statement:          Người dùng CHỈ được chọn Instrument/Venue nằm trong tập TradableListing đã đăng ký
                     (crypto, 2-3 sàn) — KHÔNG nhập tự do một symbol/venue chưa đăng ký.
Rationale:           ADR-007 crypto-only/2-3 sàn; instrument.md/venue.md là nguồn authoritative duy nhất
                     cho identity Instrument/Venue.
Source:              ADR-007; instrument.md; venue.md.
Acceptance evidence: Mọi lựa chọn Instrument/Venue trong UI resolve được về một TradableListing đã tồn
                     tại — lựa chọn ngoài tập đó bị từ chối trước khi tạo bất kỳ fact nào.
```

**PR-004 — Xem Decision với outcome tường minh**
```text
Statement:          Người dùng PHẢI xem được, cho mỗi Decision đã ghi nhận, outcome (LONG/SHORT hoặc
                     không có exposure mới) và Strategy Instance đã tạo ra nó.
Rationale:           Decision là fact authoritative trung tâm của Decision Pipeline.
Source:              Vision §1.7 (Explainable); decision.md.
Acceptance evidence: Với mọi Decision hiển thị, người dùng xác định được outcome và Strategy Instance
                     nguồn gốc mà KHÔNG cần truy vấn hệ thống khác.
```

**PR-005 — Xem evidence trace đầy đủ cho một Decision**
```text
Statement:          Người dùng PHẢI xem được, cho bất kỳ Decision nào, evidence trace đầy đủ đã dùng để
                     tạo ra nó (input snapshot, strategy/config version, causation chain tới Trade
                     Intent/RiskEvaluation/Execution Intent/Order/ExecutionResult liên quan nếu có).
Rationale:           Diễn giải trực tiếp I-1 Explainability ở tầng sản phẩm.
Source:              I-1; decision.md; risk.md; execution-intent.md; order.md; execution-result.md.
Acceptance evidence: Evidence trace hiển thị KHÔNG cần suy luận lại sau sự kiện — mọi phần tử trace là
                     fact đã ghi nhận, resolve trực tiếp qua causation_refs/correlation_id.
```

**PR-006 — Xem lý do Risk Gateway chấp thuận/từ chối**
```text
Statement:          Với mỗi Trade Intent, người dùng PHẢI xem được RiskEvaluation kết quả (APPROVED /
                     REJECTED / NON_EVALUABLE) VÀ evidence đã dùng để đi tới kết quả đó.
Rationale:           Risk Gateway là ranh giới bắt buộc trước Execution (I-4 Strategy Isolation).
Source:              I-4; risk.md.
Acceptance evidence: Với mọi Trade Intent, người dùng đọc được result + reason code (khi
                     REJECTED/NON_EVALUABLE) mà không cần diễn giải log thô.
```

**PR-007 — Xem toàn bộ chuỗi PAPER execution**
```text
Statement:          Người dùng PHẢI xem được, cho mỗi Order, chuỗi OrderSubmissionRequest → computation
                     authorization → PaperExecutionObservation → ExecutionResult → Fill (nếu có), toàn
                     bộ trong môi trường PAPER.
Rationale:           Đây là walking-skeleton execution boundary hiện tại (Live deferred, §13).
Source:              order.md; execution-result.md; fill.md.
Acceptance evidence: Với mọi Order EXECUTED, người dùng xác định được đúng một Fill với economics khớp
                     evidence đã ghi nhận; với NOT_EXECUTED, người dùng thấy rõ zero Fill.
```

**PR-008 — Tái dựng end-to-end state tại một thời điểm lịch sử**
```text
Statement:          Người dùng PHẢI chọn được một thời điểm lịch sử và xem lại chính xác state toàn
                     chuỗi Decision→...→Position TẠI thời điểm đó — KHÔNG phải latest-state hiện tại.
Rationale:           Đây là nền tảng cho Replay/Review/Improve — không thể cải thiện thứ không tái dựng
                     lại được.
Source:              I-3; replay-event.md (canonical Replay Cursor, Chapter 8 §8.5).
Acceptance evidence: Trạng thái hiển thị tại một cursor lịch sử KHÔNG đổi dù dữ liệu mới phát sinh sau
                     đó — no-look-ahead giữ nguyên.
```

## 8. Non-functional product requirements

**Chỉ liệt kê guarantee ĐÃ được Constitution/Domain Contract bảo đảm — KHÔNG yêu cầu mới.**

**PR-009 — Explainability guarantee (product-facing)**
```text
Statement:          Mọi Decision và Risk Action hiển thị cho người dùng PHẢI tái dựng được từ evidence
                     bất biến, trong một causation trace duy nhất.
Rationale:           Guarantee đã tồn tại ở tầng platform; đây là restatement product-facing, không phải
                     yêu cầu mới.
Source:              I-1 (Locked).
Acceptance evidence: 100% Decision/Risk Action hiển thị vượt qua trace-completeness kiểm tra (I-1
                     Verification).
```

**PR-010 — Decision Parity guarantee (product-facing)**
```text
Statement:          Với cùng input/config/version, Replay, Backtest và Paper PHẢI tạo cùng một Decision
                     theo canonical semantic-decision hash — execution outcome được phép khác nhau nhưng
                     phải giải thích được.
Rationale:           Guarantee đã tồn tại ở tầng platform; đây là restatement product-facing, không phải
                     yêu cầu mới.
Source:              I-2 (Locked).
Acceptance evidence: Golden event-log comparison giữa Replay/Backtest/Paper cho cùng input trả về cùng
                     canonical semantic-decision hash (I-2 Verification). **(v0.3, CANDIDATE)** So sánh
                     có thể trả về MATCH, MISMATCH, hoặc INDETERMINATE (evidence thiếu/stale/invalidated/
                     ambiguous/non-evaluable) — xem `decision.md` §9a.6.
```

**Định nghĩa `canonical semantic-decision hash` (v0.2, đóng `P03A-MIN-01`, dùng xuyên suốt PR-010/PR-019; v0.3 — pointer resolve, CANDIDATE):** hash so sánh semantic Decision, định nghĩa BỞI Decision Contract authoritative (`decision.md`, tại `/docs/domain/`) — **KHÔNG hardcode danh sách field canonical tại PRD này** (đúng I-2 Verification: "danh sách field cụ thể sống trong Domain/Event Contract... KHÔNG hardcode trong Constitution"). So sánh semantic này PHẢI **loại trừ**: runtime identity, event-envelope field, transport metadata, và processing metadata — chỉ so sánh nội dung quyết định (Decision content) thực chất. Execution outcome (fill price, timing, venue behavior...) VẪN được phép khác nhau giữa Replay/Backtest/Paper — canonical semantic-decision hash chỉ áp dụng ở tầng Decision, KHÔNG áp dụng ở tầng Execution Result (đúng I-2 "Parity nằm ở tầng Decision, không phải tầng Execution Result"). **(v0.3, CANDIDATE)** Pointer nay resolve cụ thể tới `decision.md` §9a — **Canonical Decision Semantic Representation** (danh sách include/exclude field) VÀ **Canonical Decision Semantic Digest** (giá trị hash đơn khi cần) — kèm `decision_semantic_representation_version` định danh phiên bản của chính định nghĩa so sánh này. So sánh có thể trả về ba outcome workflow-visible, non-authoritative: MATCH / MISMATCH / INDETERMINATE (§9a.6) — INDETERMINATE dùng khi input evidence thiếu/stale/invalidated/ambiguous/non-evaluable, KHÔNG ép buộc MATCH hay MISMATCH giả tạo.

**PR-011 — No silent rewrite guarantee**
```text
Statement:          Không output nào (Decision, RiskEvaluation, ExecutionResult, Fill, Position) từng
                     hiển thị cho người dùng bị sửa/xóa ngầm — mọi thay đổi là một fact mới, append-only.
Rationale:           Guarantee đã tồn tại ở tầng platform; đây là restatement product-facing, không phải
                     yêu cầu mới.
Source:              I-3 (Locked); mười-invariant correction lineage pattern (đồng nhất xuyên suốt mọi
                     Domain Contract Phase 0.2).
Acceptance evidence: Mọi correction hiển thị dưới dạng fact mới với liên kết tường minh tới fact cũ —
                     không có edit/delete trực tiếp nào quan sát được.
```

**PR-012 — Deterministic historical reconstruction guarantee**
```text
Statement:          Trạng thái hiển thị tại một cursor lịch sử PHẢI deterministic và không phụ thuộc
                     network/external state một khi đã "chuẩn bị" (prepared).
Rationale:           Guarantee đã tồn tại ở tầng platform; đây là restatement product-facing, không phải
                     yêu cầu mới.
Source:              I-5 (Locked); replay-event.md.
Acceptance evidence: Replay tại cùng cursor, chạy nhiều lần, cho cùng kết quả — kể cả khi ngắt mạng sau
                     bước chuẩn bị (I-5 Verification).
```

**PR-013 — Lossless financial precision guarantee**
```text
Statement:          Mọi giá trị tài chính hiển thị (fill_price, fill_quantity, net_quantity) PHẢI chính
                     xác, KHÔNG mất precision qua bất kỳ bước hiển thị nào.
Rationale:           Guarantee đã tồn tại ở tầng platform; đây là restatement product-facing, không phải
                     yêu cầu mới.
Source:              I-9 (Locked); fill.md; position.md.
Acceptance evidence: Giá trị hiển thị khớp byte-for-byte với giá trị decimal đã ghi nhận trong
                     PaperExecutionObservation/Fill.
```

**PR-014 — Explicit state-machine transition guarantee**
```text
Statement:          Mọi lifecycle state hiển thị (Order/RiskEvaluation/ExecutionResult/...) PHẢI chỉ
                     phản ánh transition đã khai báo tường minh trong Domain Contract sở hữu entity đó.
Rationale:           Guarantee đã tồn tại ở tầng platform; đây là restatement product-facing, không phải
                     yêu cầu mới.
Source:              I-13 (Locked).
Acceptance evidence: Không trạng thái nào hiển thị mà không truy vết được về một transition event hợp
                     lệ trong state machine authoritative tương ứng.
```

## 9. Lifecycle requirements

### 9.1 Research

**PR-015 — Quan sát market analysis state không side-effect**
```text
Statement:          Người dùng PHẢI xem được Candle/Swing/Structure/Regime/Feature/Market Context tại
                     bất kỳ thời điểm nào mà KHÔNG tạo ra bất kỳ authoritative fact mới nào.
Rationale:           Research là giai đoạn quan sát thuần túy — trước khi cam kết Replay/Backtest.
Source:              candle.md; swing.md; structure.md; regime.md; feature.md; context.md.
Acceptance evidence: Sau một phiên Research, event log của những stream trên không tăng thêm fact nào.
```

**PR-016 — Chọn/cấu hình Strategy Instance trước khi cam kết Replay/Backtest**
```text
Statement:          Người dùng PHẢI cấu hình xong Strategy Instance (PR-001) TRƯỚC KHI Replay/Backtest
                     bắt đầu — không được đổi Strategy Instance giữa chừng một phiên Replay/Backtest.
Rationale:           Đảm bảo Decision Parity (I-2) — logic quyết định không đổi giữa các bước trong một
                     phiên.
Source:              I-2; strategy.md.
Acceptance evidence: Mọi Decision trong MỘT phiên Replay/Backtest trace về đúng MỘT Strategy Instance.
```

**PR-017 — Research không tạo authoritative Decision Pipeline fact**
```text
Statement:          Hoạt động Research KHÔNG được tạo Decision/RiskEvaluation/Execution Intent/
                     Order/ExecutionResult.
Rationale:           Ranh giới rõ ràng giữa "quan sát" và "quyết định" — tránh Research vô tình sinh fact
                     có hệ quả.
Source:              I-3 (No Look-Ahead — không side-effect ngầm); decision.md.
Acceptance evidence: Sau một phiên Research, KHÔNG có Decision/RiskEvaluation/Execution
                     Intent/Order/ExecutionResult mới nào xuất hiện trong event log.
```

### 9.2 Replay

**PR-018 — Chọn canonical Replay Cursor và xem state tái dựng**
```text
Statement:          Người dùng PHẢI chọn được một canonical Replay Cursor và xem đúng ReplayState(C) tại
                     cursor đó — bao gồm toàn bộ lineage Decision→...→Position.
Rationale:           Replay Cursor là cơ chế duy nhất pin "thời điểm lịch sử" tường minh.
Source:              Chapter 8 §8.5 (Locked); replay-event.md.
Acceptance evidence: ReplayState hiển thị tại cursor C chỉ chứa fact có recorded_time ≤ C (no-look-ahead).
```

**PR-019 — Historical reconstruction (mặc định) và parity recomputation (tuỳ chọn) — Replay KHÔNG tạo Decision mới**
```text
Statement:          Replay tại một cursor, THEO MẶC ĐỊNH, thực hiện historical reconstruction — resolve
                     và hiển thị CHÍNH XÁC các authoritative fact (bao gồm Decision) ĐÃ TỒN TẠI tại cursor
                     đó, KHÔNG tạo Decision mới. Người dùng CÓ THỂ tuỳ chọn kích hoạt một parity
                     recomputation — một bước semantic verification deterministic, non-authoritative, so
                     sánh Decision tái tính toán với Decision đã ghi nhận qua canonical semantic-decision
                     hash (PR-010) — kết quả recomputation đó KHÔNG BAO GIỜ tự động trở thành, thay thế,
                     hay ghi đè Decision authoritative.
Rationale:           Tách bạch tường minh "xem lại state đã có" (historical reconstruction, mặc định) và
                     "kiểm chứng lại logic có khớp không" (parity recomputation, tuỳ chọn) — tránh Replay
                     bị hiểu ngầm là tự động tạo ra một Decision Pipeline/authority thứ hai chạy song
                     song.
Source:              I-2; I-3; I-12; decision.md; replay-event.md (ReplayStateProjection — KHÔNG
                     authoritative, §3 "Không duplicate authority").
Acceptance evidence: Chạy Replay tại một cursor (historical reconstruction) KHÔNG làm tăng số lượng
                     Decision fact trong event log. Khi người dùng kích hoạt parity recomputation, kết
                     quả so sánh dùng canonical semantic-decision hash (PR-010) và hiển thị MATCH,
                     MISMATCH, hoặc INDETERMINATE **(v0.3, CANDIDATE — xem `decision.md` §9a.6)** —
                     mismatch/indeterminate KHÔNG tự động ghi đè hay tạo Decision mới, chỉ hiển thị như
                     một finding cần xem xét.
```

**Replay authority boundary (v0.2, đóng `P03A-B-MIN-03`):**
```text
Replay:
  KHÔNG append một authoritative Decision fact trùng lặp
  KHÔNG tạo một Replay authority stream song song
  KHÔNG thay thế hay mutate Decision đã ghi nhận
  vẫn tuân thủ no-look-ahead và visibility-at-cursor rules (I-3; replay-event.md §2)

Historical reconstruction (mặc định): resolve và hiển thị fact authoritative ĐÃ TỒN TẠI tại canonical
Replay Cursor — KHÔNG computation mới, KHÔNG authoritative fact mới.

Parity recomputation (tuỳ chọn): semantic verification deterministic, non-authoritative — mọi so sánh
PHẢI dùng canonical semantic-decision hash (PR-010) — kết quả KHÔNG BAO GIỜ tự động trở thành fact
authoritative. Kết quả là MATCH, MISMATCH, hoặc INDETERMINATE (v0.3, CANDIDATE — decision.md §9a.6) —
cả ba đều workflow-visible, non-authoritative.

Authoritative Decision creation KHÔNG bao giờ bị gây ra ngầm chỉ bằng việc chạy Replay.

KHÔNG tạo, KHÔNG đặt tên một domain fact "ReplayDecision" hay tương đương — Replay KHÔNG sở hữu authority
của Decision Pipeline (đúng replay-event.md §3).
```

**PR-020 — Replay không phụ thuộc network sau bước chuẩn bị**
```text
Statement:          Sau khi mọi artifact tham chiếu đã materialize, phiên Replay PHẢI chạy thành công dù
                     ngắt kết nối mạng.
Rationale:           Diễn giải trực tiếp I-5 cho stage Replay.
Source:              I-5.
Acceptance evidence: Self-contained Replay test (I-5 Verification) pass cho phiên Replay của người dùng.
```

### 9.3 Backtest

**PR-021 — Chạy Decision logic qua một khoảng lịch sử bounded, gắn stable run identity**
```text
Statement:          Người dùng PHẢI chạy được Decision logic của Strategy Instance đã chọn qua một
                     khoảng thời gian lịch sử có giới hạn rõ ràng (start/end), dưới MỘT stable Backtest
                     run identity/context duy nhất, và xem toàn bộ chuỗi Decision/RiskEvaluation sinh ra
                     — KHÔNG tạo Order/ExecutionResult PAPER hay Live.
Rationale:           Backtest dùng chung decision logic/pipeline với Replay/Paper/Live (I-2) nhưng KHÔNG
                     chạm execution layer. Một run identity ổn định là điều kiện tiên quyết để mọi
                     evidence khác của run đó (PR-022–PR-034) truy vết được về đúng một context.
Source:              I-2; I-4; decision.md; risk.md.
Acceptance evidence: Sau một phiên Backtest, KHÔNG có Order/ExecutionResult/Fill mới nào xuất hiện —
                     chỉ Decision/RiskEvaluation, mọi fact đó trace về ĐÚNG MỘT run identity/context.
```

**PR-022 — Kết quả Backtest gắn với version tuple tường minh**
```text
Statement:          Mọi kết quả Backtest hiển thị PHẢI gắn liền với đúng một Strategy Definition Version
                     + policy version đã dùng — hiển thị được cho người dùng.
Rationale:           Diễn giải I-1 cho stage Backtest — không có kết quả "vô danh".
Source:              I-1; strategy.md.
Acceptance evidence: Mỗi kết quả Backtest hiển thị resolve được về đúng một version tuple, không mơ hồ.
```

**PR-023 — Backtest không yêu cầu kết nối Live**
```text
Statement:          Backtest PHẢI chạy được hoàn toàn từ dữ liệu lịch sử đã có — KHÔNG yêu cầu kết nối
                     tới sàn giao dịch thật.
Rationale:           Diễn giải I-5 cho stage Backtest; giữ Backtest tách biệt hoàn toàn khỏi Live.
Source:              I-5.
Acceptance evidence: Một phiên Backtest hoàn tất thành công trong môi trường không có route mạng tới bất
                     kỳ exchange endpoint nào.
```

**PR-033 — Backtest sinh simulated economic evidence và exposure/position progression (v0.2, MỚI, đóng `P03A-MAJ-01`)**
```text
Statement:          Với mỗi Backtest run (stable run identity, PR-021), người dùng PHẢI xem được (a)
                     deterministic simulated economic evidence cho mỗi điểm trong chuỗi Decision/
                     RiskEvaluation của run đó dẫn tới một simulated exposure change, VÀ (b) exposure/
                     position progression theo thời gian xuyên suốt khoảng interval đã chạy — HOÀN TOÀN
                     TÁCH BIỆT khỏi PAPER/Live authority (§ Backtest authority boundary, dưới).
Rationale:           Nếu Backtest chỉ dừng ở chuỗi Decision/RiskEvaluation (PR-021) mà không cho thấy kết
                     quả kinh tế mô phỏng, người dùng không thể evaluate Strategy trước khi dùng vốn thật
                     — vi phạm trực tiếp "Research Before Capital" (Vision §1.6).
Source:              I-1; I-2; Vision §1.6 (Research Before Capital); decision.md; risk.md
                     (nguồn Decision/RiskEvaluation evidence); execution-result.md/fill.md/position.md
                     (tham chiếu CHỈ để định nghĩa ranh giới PAPER authority mà Backtest KHÔNG được tái sử
                     dụng — xem Backtest authority boundary).
Acceptance evidence: Với mọi Backtest run, người dùng xem được (i) simulated economic evidence
                     deterministic gắn với mỗi Decision dẫn tới exposure change, (ii) exposure/position
                     progression theo thời gian trong khoảng interval, VÀ (iii) audit event log xác nhận
                     KHÔNG có PAPER Order/ExecutionResult/Fill/Position nào được tạo/tái sử dụng bởi run
                     đó.
```

**PR-034 — Backtest sinh strategy-level evaluable result, so sánh được cross-run/cross-version (v0.2, MỚI, đóng `P03A-MAJ-01`)**
```text
Statement:          Với mỗi Backtest run đã hoàn tất, người dùng PHẢI xem được một strategy-level
                     evaluable result (dẫn xuất từ chuỗi Decision/RiskEvaluation + exposure progression
                     của run đó, PR-033), gắn CHÍNH XÁC với Strategy Instance/Strategy Definition
                     Version/configuration context đã dùng (PR-022), VÀ so sánh được kết quả đó với kết
                     quả của Backtest run KHÁC (khoảng interval khác, hoặc Strategy Definition Version
                     khác) — KHÔNG định nghĩa threshold/target cụ thể nào tại đây.
Rationale:           "Continuous Improvement Over Prediction" (Vision §1.6) và nguyên tắc Measurable (§5)
                     đòi hỏi Backtest sinh một kết quả SO SÁNH ĐƯỢC — không chỉ một chuỗi sự kiện thô —
                     nhưng KHÔNG được định nghĩa concrete KPI (`OQ-003`, §13).
Source:              Vision §1.6/§1.8; §5 (nguyên tắc Measurable); strategy.md (Strategy Definition
                     Version); I-12 (durable append-only log — cho phép truy vấn xuyên version).
Acceptance evidence: Hai Backtest run (Strategy Definition Version khác nhau, HOẶC cùng version nhưng
                     interval khác nhau) đều resolve được một strategy-level evaluable result RIÊNG, gắn
                     đúng run identity/version context (PR-021/PR-022) — người dùng so sánh được hai kết
                     quả đó cạnh nhau mà không cần công cụ ngoài hệ thống.
```

**Backtest authority boundary (v0.2, đóng `P03A-MAJ-01`):**
```text
Backtest output KHÔNG BAO GIỜ được đại diện như authoritative PAPER hay Live fact.

Backtest KHÔNG được tạo hoặc tái sử dụng, làm Backtest authority:
  PAPER Order            (order.md)
  PAPER ExecutionResult  (execution-result.md)
  PAPER Fill             (fill.md)
  PAPER Position         (position.md)
  Live execution fact    (chưa author, deferred)

PRD này yêu cầu simulated economic result quan sát được (PR-033/PR-034) NHƯNG hoãn lại (defer) Backtest
Domain Contract/event schema chính xác — chưa quyết cơ chế/entity cụ thể.

KHÔNG author tại đây, và KHÔNG được suy diễn từ PR-033/PR-034: một entity/event "BacktestOrder",
"BacktestFill", "BacktestPosition", "BacktestExecutionResult", hay tương đương. KHÔNG định nghĩa execution
algorithm, fee model, slippage model, accounting ledger, hay PnL formula — những nội dung đó ngoài phạm
vi Package 0.3-A (xem §13 Deferred questions).
```

### 9.4 Paper

**PR-024 — Submit Order PAPER và nhận đúng một ExecutionResult**
```text
Statement:          Người dùng PHẢI submit được một Order hợp lệ và nhận về đúng một ExecutionResult
                     (EXECUTED hoặc NOT_EXECUTED), environment PAPER.
Rationale:           Walking-skeleton execution boundary hiện tại.
Source:              order.md; execution-result.md.
Acceptance evidence: Mỗi Order hợp lệ dẫn tới đúng một ExecutionResult visible-valid, environment=PAPER.
```

**PR-025 — Xem simulation evidence đầy đủ cho mỗi Fill**
```text
Statement:          Với mỗi Fill, người dùng PHẢI xem được simulation evidence (policy/configuration/
                     build/deterministic-input ref) VÀ economics (quantity/price) đã dùng để tạo ra nó,
                     khớp CHÍNH XÁC PaperExecutionObservation đã ghi nhận.
Rationale:           Diễn giải trực tiếp C7-MAJ-01/C7-MAJ-02 (đã đóng tại execution-result.md/fill.md).
Source:              execution-result.md §1; fill.md §1/§3.
Acceptance evidence: Economics hiển thị của Fill khớp byte-for-byte Observation đã ghi nhận — không có
                     giá trị tính lại độc lập.
```

**PR-026 — Xem Position với disclosure rõ ràng khi không evaluable**
```text
Statement:          Người dùng PHẢI xem được Position hiện tại cho một Account/Instrument; khi có nhiều
                     Fill lineage xung đột, hệ thống PHẢI disclose tường minh trạng thái không thể xác
                     định (NON_EVALUABLE) thay vì hiển thị một con số tuỳ chọn.
Rationale:           Diễn giải trực tiếp C7-MAJ-04 (đã đóng tại position.md).
Source:              position.md §1/§2.
Acceptance evidence: Khi eligible Fill count > 1 cho cùng Position key, UI hiển thị trạng thái
                     NON_EVALUABLE + danh sách Fill xung đột — KHÔNG hiển thị một Position số cụ thể.
```

**PR-027 — Paper Trading không đặt lệnh thật**
```text
Statement:          Không hành động Paper Trading nào được phép tạo ra một lệnh thật trên sàn giao dịch
                     bên ngoài.
Rationale:           Ranh giới PAPER/Live tường minh — Live vẫn `OQ-002` (§13), chưa authorize.
Source:              Vision §1.9/§1.10 (Non-Goals/Out of Scope); execution-result.md (environment: PAPER
                     duy nhất được author).
Acceptance evidence: Audit egress network của phiên Paper Trading không có bất kỳ lệnh ghi nào gửi tới
                     exchange endpoint thật.
```

### 9.5 Review

**PR-028 — Xem causation trace đầy đủ Decision→Position**
```text
Statement:          Người dùng PHẢI xem được, cho một Position contribution bất kỳ, toàn bộ causation
                     trace ngược về Decision gốc đã sinh ra nó (Decision→Trade Intent→RiskEvaluation→
                     Execution Intent→Order→ExecutionResult→Fill→Position).
Rationale:           Diễn giải trực tiếp I-1 cho stage Review — review chỉ có giá trị khi evidence đầy
                     đủ, không đứt đoạn.
Source:              I-1; toàn bộ chuỗi Domain Contract Package 0.2-C4–C7.
Acceptance evidence: Với mọi Fill đóng góp Position, người dùng truy vết ngược được tới đúng một Decision
                     gốc mà không có mắt xích thiếu.
```

**PR-029 — So sánh Replay-reconstructed state với state đã ghi nhận**
```text
Statement:          Người dùng PHẢI so sánh được state tái dựng qua Replay tại một cursor lịch sử với
                     state đã hiển thị tại đúng thời điểm đó khi ghi nhận ban đầu, để xác nhận không có
                     silent drift.
Rationale:           Diễn giải I-2/I-3 cho stage Review — review phải phát hiện được sai lệch nếu có.
Source:              I-2; I-3; replay-event.md.
Acceptance evidence: So sánh trả về "No conflict" khi không có correction nào xảy ra giữa hai thời điểm;
                     khi có correction, khác biệt hiển thị tường minh kèm fact correction liên quan.
```

**PR-030 — Review không recompute historical outcome**
```text
Statement:          Review CHỈ hiển thị fact đã ghi nhận — KHÔNG được tính lại/diễn giải lại
                     Decision/RiskEvaluation/ExecutionResult outcome theo logic khác với logic đã tạo ra
                     fact đó.
Rationale:           Diễn giải trực tiếp I-3 (No Repaint) — nguyên tắc "KHÔNG BAO GIỜ tự computation/
                     reinterpret" xuyên suốt mọi Domain Contract Phase 0.2 (ví dụ execution-result.md
                     §1, `result_type` chỉ copy từ Observation).
Source:              I-3; execution-result.md.
Acceptance evidence: Giá trị hiển thị trong Review khớp byte-for-byte giá trị đã ghi nhận tại thời điểm
                     fact đó được tạo — không có version tính-lại nào tồn tại song song.
```

### 9.6 Improve

**PR-031 — Version hóa Strategy với truy vết đầy đủ**
```text
Statement:          Người dùng PHẢI tạo được một Strategy Definition Version mới, và mọi Decision từ
                     Strategy Instance mới PHẢI truy vết được chính xác về version đó — tách biệt hoàn
                     toàn khỏi version cũ.
Rationale:           "Continuous Improvement Over Prediction" (Vision §1.6) đòi hỏi so sánh version được,
                     không phải ghi đè.
Source:              Vision §1.6; strategy.md; ADR-013.
Acceptance evidence: Hai Strategy Instance gắn hai Strategy Definition Version khác nhau sinh ra hai tập
                     Decision tách biệt hoàn toàn, không lẫn lộn.
```

**PR-032 — Truy vấn outcome xuyên suốt các Strategy Definition Version**
```text
Statement:          Người dùng PHẢI truy vấn được Decision/Execution outcome của MỌI Strategy Definition
                     Version đã từng chạy — kể cả version cũ đã ngừng dùng.
Rationale:           Cải thiện đòi hỏi so sánh outcome cũ và mới — không mất truy cập lịch sử.
Source:              I-12 (Single Source of Truth — durable append-only log); strategy.md; decision.md.
Acceptance evidence: Một Strategy Definition Version không còn active vẫn resolve được toàn bộ Decision
                     lịch sử gắn với nó, qua đúng authoritative event stream.
```

## 10. Traceability

| PR-ID range | Vision | Platform Invariant | Domain Contract |
|---|---|---|---|
| PR-001–PR-003 | §1.5 | — | strategy.md, account.md, instrument.md, venue.md |
| PR-004–PR-005 | §1.7 | I-1 | decision.md, risk.md, execution-intent.md, order.md, execution-result.md |
| PR-006 | §1.7 | I-4 | risk.md |
| PR-007 | — | — | order.md, execution-result.md, fill.md |
| PR-008 | — | I-3 | replay-event.md |
| PR-009 | §1.7 | I-1 | decision.md, risk.md |
| PR-010 | §1.7 | I-2 | — (cross-mode guarantee) |
| PR-011 | §1.7 | I-3 | mọi Domain Contract (correction lineage pattern) |
| PR-012 | — | I-5 | replay-event.md |
| PR-013 | — | I-9 | fill.md, position.md |
| PR-014 | — | I-13 | order.md, risk.md, execution-result.md |
| PR-015–PR-017 | §1.6 | I-2, I-3 | candle.md…context.md, strategy.md |
| PR-018–PR-020 | — | I-2, I-3, I-5 | replay-event.md |
| PR-021–PR-023 | §1.6 | I-2, I-4, I-5, I-1 | decision.md, risk.md, strategy.md |
| PR-033–PR-034 (v0.2, MỚI) | §1.6/§1.8 | I-1, I-2, I-12 | decision.md, risk.md, strategy.md (evidence nguồn); execution-result.md/fill.md/position.md (tham chiếu CHỈ để định nghĩa PAPER authority boundary Backtest không được tái sử dụng — Backtest tự thân chưa có Domain Contract, §13) |
| PR-024–PR-027 | §1.9/§1.10 | — | order.md, execution-result.md, fill.md, position.md |
| PR-028–PR-030 | §1.7 | I-1, I-2, I-3 | decision.md…position.md (full chain) |
| PR-031–PR-032 | §1.6 | I-12 | strategy.md, decision.md |

## 11. Non-Goals

Kế thừa nguyên vẹn [Vision §1.9](../constitution/01-vision.md): Ride KHÔNG cố gắng dự đoán tương lai, đánh bại thị trường, đảm bảo lợi nhuận, hay thay thế phán đoán con người. Bổ sung tường minh cho Phase 0.3: PRD này KHÔNG cố gắng định nghĩa concrete Product Metrics/KPI (`OQ-003`) hay Live-gate criteria (`OQ-002`) — cả hai vẫn `Open`, xem §13.

## 12. Out-of-Scope

Kế thừa nguyên vẹn [Vision §1.10](../constitution/01-vision.md): Ride chủ đích KHÔNG là Pump Signal Platform, Chat Room, Social Trading Network, Copy Trading Platform, Leaderboard Platform, AI Price Prediction Platform.

**Ngoài phạm vi tường minh của riêng tài liệu này (Package 0.3-A):**

- Screen layout, wireframe, component hierarchy, UX architecture (Package 0.3-C, chưa author).
- Backend/frontend/API/database architecture, security/custody architecture, deployment (Phase 1, `/docs/architecture/`).
- Exchange adapter design cụ thể.
- Concrete KPI threshold/target, Product Metrics cụ thể (`OQ-003`).
- Live-gate criteria cụ thể (`OQ-002`).
- Multi-tenant design, đa tài sản expansion (ngoài phạm vi ADR-007 Phase 0-3).
- Bất kỳ Domain Contract semantic mới nào — mọi vocabulary dùng ở đây đã tồn tại tại Package 0.2-A/B/C, `Consolidated Stable`.

## 13. Deferred questions

```text
OQ-002:
  Open
  Strategy Lifecycle Live-gate deferred — cần ADR khi Phase 3 định nghĩa Strategy Lifecycle
  (MANIFEST.md Open Questions). PRD này CHỈ đề cập Live như một lifecycle boundary bị hoãn (§6, §9.4
  PR-027) — KHÔNG định nghĩa điều kiện chuyển Live.

OQ-003:
  Open
  Concrete Product Metrics deferred — Vision §1.8 đã ghi nhận cần "tài liệu Product Metrics riêng,
  không nhét KPI chi tiết vào Vision"; PRD này yêu cầu evidence đo lường được PHẢI tồn tại (PR-009–
  PR-014, §5 nguyên tắc "Measurable") nhưng KHÔNG định nghĩa threshold/target cụ thể nào.

Backtest/Research Domain Contract modeling:
  Chưa tồn tại — không có backtest.md/research.md nào được author tại Package 0.2-A/B/C. Requirement
  tại §9.1/§9.3 (bao gồm PR-033/PR-034, v0.2, đóng P03A-MAJ-01) mô tả hành vi product-level — Backtest
  PHẢI sinh simulated economic evidence/exposure progression/strategy-level result quan sát được — truy
  vết về Platform Invariant + Domain Contract hiện có (decision.md, risk.md, strategy.md), và tham chiếu
  execution-result.md/fill.md/position.md CHỈ để định nghĩa ranh giới PAPER authority mà Backtest KHÔNG
  được tái sử dụng (xem Backtest authority boundary, §9.3). KHÔNG giả định một Domain Contract
  "Backtest"/"Research" đã tồn tại; KHÔNG author entity/event/schema Backtest tại đây. Việc có cần author
  Domain Contract riêng cho Backtest/Research hay không là quyết định Product Owner, ngoài phạm vi Package
  0.3-A.
```

## 14. Acceptance criteria for Package 0.3-A

```text
1. Toàn bộ 15 mục nội dung bắt buộc (§1–§15) có mặt và đầy đủ.
2. Mọi PR-ID duy nhất, liên tục theo global sequence (PR-001–PR-034, không đánh số lại bất kỳ PR-ID ổn
   định nào đã tồn tại — PR-033/PR-034 là ID mới, append cuối), mỗi PR có đủ Statement/Rationale/Source/
   Acceptance evidence.
3. Mọi PR-ID có MỘT HOẶC NHIỀU applicable authoritative source (Vision/Platform Invariant/Domain Contract
   Consolidated Stable) — CÓ THỂ kết hợp nhiều nguồn; mọi nguồn trích dẫn phải material; không PR nào mồ
   côi nguồn hay chỉ dựa vào tài liệu non-authoritative (đúng quy tắc §"Authority boundary", KHÔNG còn
   "đúng một").
4. Không thuật ngữ mơ hồ (easy to use/fast/scalable/secure/professional/user-friendly) xuất hiện mà
   không kèm observable evidence cụ thể.
5. Không nội dung nào thuộc danh sách "Explicit constraints" (screen layout, wireframe, backend/frontend/
   API/database/security/custody/deployment architecture, exchange adapter design, concrete KPI, Product
   Metrics, Live-gate criteria, multi-tenant/multi-asset design, Domain Contract semantics mới, Backtest
   entity/event/schema, execution/fee/slippage/accounting/PnL model, `ReplayDecision` hay Replay authority
   stream mới).
6. Không sửa bất kỳ Domain Contract/ADR/Constitution nào — vocabulary dùng lại nguyên vẹn.
7. `OQ-002`/`OQ-003` giữ nguyên `Open`, không bị đóng ngầm.
8. YAML frontmatter hợp lệ, `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`.
9. Baseline sẵn sàng cho ChatGPT Delta Review A + Independent Delta Review B trên CÙNG một commit/blob.
10. Backtest (PR-021–PR-023, PR-033–PR-034) sinh simulated economic outcome quan sát/evaluate được mà
    KHÔNG tái sử dụng PAPER Order/ExecutionResult/Fill/Position làm Backtest authority.
11. Replay (PR-018–PR-020) không thể bị diễn giải là ngầm tạo authoritative Decision mới — historical
    reconstruction vs parity recomputation tách bạch tường minh, không `ReplayDecision` nào được đặt tên.
12. `Decision hash` (thuật ngữ chung chung) đã được thay bằng `canonical semantic-decision hash` xuyên
    suốt PR-010/PR-019 và acceptance evidence liên quan.
```

## 15. Handoff requirements for Package 0.3-B

Package 0.3-B (`use-case-workflow.md`) PHẢI:

1. Tham chiếu Use Case/Workflow về đúng một hoặc nhiều `PR-XXX` ID tại đây — KHÔNG tự phát minh requirement mới ở tầng workflow.
2. Giữ nguyên khung sáu-giai-đoạn (Research→Replay→Backtest→Paper→Review→Improve, §9) — không thêm giai đoạn mới nếu chưa có Product Owner authorization riêng.
3. Giữ nguyên walking-skeleton discipline — một hành trình người dùng chính (§ walking-skeleton, không phải toàn bộ persona/edge case).
4. KHÔNG đóng `OQ-002`/`OQ-003` — kế thừa nguyên trạng `Open` từ §13.
5. KHÔNG author screen layout/wireframe/component hierarchy — đó là phạm vi Package 0.3-C.
6. KHÔNG định nghĩa Domain Contract semantic mới — mọi state/transition tham chiếu phải resolve về Domain Contract đã `Consolidated Stable`.
7. (v0.2, MỚI) Kế thừa nguyên vẹn **Backtest authority boundary** (§9.3) và **Replay authority boundary** (§9.2) — KHÔNG mô tả Backtest workflow như thể nó tạo/tái sử dụng PAPER fact; KHÔNG mô tả Replay workflow như thể nó tạo Decision mới hay một `ReplayDecision`.
8. (v0.2, MỚI) Mọi so sánh Decision semantic trong workflow PHẢI dùng đúng thuật ngữ `canonical semantic-decision hash` (PR-010) — KHÔNG dùng lại thuật ngữ chung chung "Decision hash".
