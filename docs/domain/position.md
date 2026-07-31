---
id: position
title: Position
version: "0.2"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-07-31"
last_review: null
next_review: null
---

# Position

> **Vai trò của tài liệu này:** Domain Contract thứ ba của Package 0.2-C7 (Execution Result, Fill, Position and Replay Integration Foundation) — định nghĩa **Position**, một PROJECTION deterministic, non-authoritative, dẫn xuất TRỌN VẸN từ `eligible_as_position_contributing_fill` (fill.md §6). Draft, chưa Approved/Locked. Thuộc capability `execution-management` / context `position-management` (đăng ký tại [`context-map.yaml`](./context-map.yaml), không đổi trong bounded correction này). Kiến trúc controlling: [`fill.md`](./fill.md) v0.2 Draft §6 (`eligible_as_position_contributing_fill`, KHÔNG sửa), [Chapter 7 §7.4](../constitution/07-module-taxonomy.md) (Locked, Projection semantics). Tài liệu này CHỈ implement field/invariant mà các nguồn trên yêu cầu.

Position **KHÔNG phải** một authoritative fact độc lập, KHÔNG có event stream riêng, KHÔNG có mutable command trực tiếp — nó là **một hàm thuần túy, deterministic của `eligible_as_position_contributing_fill(fill_id, C)`** (fill.md §6, continuing cursor-bound validity rule) tại một cursor cho trước — **KHÔNG** của `FillCurrentView` latest-state.

**Ví dụ walking-skeleton (tiếp `fill.md`):** một Fill eligible LONG hoặc SHORT duy nhất → Position LONG hoặc SHORT, `net_quantity = fill_quantity`, `average_entry_price = fill_price`. **v0.2 (đóng `C7-MAJ-04`, MỚI):** Position projection nay có `projection_status ∈ {EVALUABLE, NON_EVALUABLE}` — deterministic xử lý CẢ BA trường hợp: zero eligible Fill (`EVALUABLE`, FLAT), đúng một eligible Fill (`EVALUABLE`, LONG/SHORT), NHIỀU eligible Fill lineage (`NON_EVALUABLE`, `UNSUPPORTED_MULTIPLE_FILL_LINEAGES`) — KHÔNG BAO GIỜ silently chọn một Fill, aggregate, hay report FLAT sai khi có nhiều Fill xung đột.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B/C1–C7:** Position Current View (nếu có) KHÔNG BAO GIỜ authority; rebuild deterministic hoàn toàn từ `eligible_as_position_contributing_fill`; KHÔNG compensating Position event khi Fill invalidate — recompute trực tiếp.

**v0.2 — bounded correction, đóng `C7-MAJ-04` (consolidated Review A + Independent Review B findings):** thêm `projection_status ∈ {EVALUABLE, NON_EVALUABLE}` VÀ `projection_reason_code = UNSUPPORTED_MULTIPLE_FILL_LINEAGES` (§1/§2) — khi > 1 eligible Fill lineage đóng góp cho CÙNG Position key, projection PHẢI trả về `NON_EVALUABLE` (KHÔNG `FLAT`, KHÔNG chọn một Fill, KHÔNG aggregate, KHÔNG weighted average) VÀ expose `contributing_fill_refs` (danh sách đầy đủ Fill xung đột). Position projection nay consume `eligible_as_position_contributing_fill` (fill.md §6, MỚI) THAY VÌ trực tiếp fold `FillCurrentView`/Fill stream — đảm bảo Position tự động loại trừ Fill orphan (ExecutionResult không còn EXECUTED head) NGAY LẬP TỨC, KHÔNG phụ thuộc thời điểm `FillFactInvalidated` được append (đóng liên đới `C7-MAJ-03`, xem `fill.md` §6). Bounded — không đổi Position structural key, non-negative magnitude representation, Position non-authority, C1–C6 semantics, PAPER-only boundary.

**Phạm vi bounded tường minh:** KHÔNG author close/reduce/reversal arithmetic. KHÔNG portfolio aggregation/cross-account/cross-listing netting. KHÔNG realized/unrealized PnL. KHÔNG margin/leverage/liquidation. KHÔNG accounting ledger. KHÔNG FX conversion. KHÔNG mutable Position command trực tiếp. KHÔNG weighted-average/netting arithmetic cho nhiều Fill — khi xảy ra, projection trả `NON_EVALUABLE` tường minh (§2), KHÔNG tự ý tính toán. KHÔNG redefine Fill contract. KHÔNG sửa `fill.md`/`execution-result.md`/`order.md`/`execution-intent.md`/`risk.md`/`decision.md`/`trade-intent.md`/C1–C6/ADR/Constitution.

## 1. Position — `kind: read_model` (Type 2 Projection, Chapter 7 §7.4)

**Không phải authoritative event/entity — KHÔNG có event stream riêng.** Position là derived projection thuần túy — rebuild được hoàn toàn từ `fill.md` §6 `eligible_as_position_contributing_fill` tại một cursor.

```yaml
id: position
kind: read_model
capability_id: execution-management
domain_context_id: position-management
description: >
  PROJECTION deterministic của eligible_as_position_contributing_fill (fill.md §6) cho một Position
  key (account_id, environment, instrument_selection_ref). KHÔNG authoritative — KHÔNG mutable
  command trực tiếp, KHÔNG event/subject riêng, rebuild được hoàn toàn (Chapter 7 §7.4). **v0.2
  (đóng C7-MAJ-04):** PHẢI formally handle zero/một/nhiều eligible Fill lineage — KHÔNG BAO GIỜ
  silently chọn một Fill hay report FLAT sai khi có xung đột.
invariants:
  - "position_key = (account_id, environment, instrument_selection_ref) — BẤT BIẾN theo cấu trúc."
  - "net_quantity (khi có mặt) LUÔN non-negative magnitude — direction VÀ magnitude tách biệt tường minh (§3)."
  - "**v0.2 (đóng C7-MAJ-04):** `projection_status = EVALUABLE` ⟺ eligible Fill count ∈ {0, 1}. `projection_status = NON_EVALUABLE` ⟺ eligible Fill count > 1 — KHI NON_EVALUABLE: `position_direction`/`net_quantity`/`quantity_unit`/`average_entry_price`/`price_currency` TUYỆT ĐỐI ABSENT (KHÔNG fabricate/aggregate/chọn một); `projection_reason_code = UNSUPPORTED_MULTIPLE_FILL_LINEAGES` BẮT BUỘC có mặt; `contributing_fill_refs` BẮT BUỘC có mặt, liệt kê ĐẦY ĐỦ mọi Fill eligible xung đột."
  - "`projection_reason_code`/`contributing_fill_refs` TUYỆT ĐỐI ABSENT khi `projection_status = EVALUABLE`."
  - "EVALUABLE + zero eligible Fill: FLAT — `position_direction` ABSENT, `net_quantity = 0`."
  - "EVALUABLE + đúng một eligible Fill: `position_direction` có mặt CHÍNH XÁC MỘT trong {LONG, SHORT}, `net_quantity > 0`."
  - "Position PHẢI recompute TRỌN VẸN từ scratch mỗi khi eligible_as_position_contributing_fill result thay đổi cho bất kỳ Fill liên quan (Fill invalidate/replace, HOẶC ExecutionResult invalidate/replace — v0.2, đóng C7-MAJ-03 liên đới) — KHÔNG mutate incremental, KHÔNG compensating Position event/command nào tồn tại (§4)."
schema:
  position_key: {type: string, required: true, description: "derived, = f(account_id, environment, instrument_selection_ref)"}
  account_id: {type: string, required: true, ref: account}
  environment: {type: enum, values: [PAPER], required: true}
  instrument_selection_ref:
    type: object
    required: true
    fields:
      instrument_id: {type: string, required: true}
      venue_id: {type: string, required: true}
      listing_id: {type: string, required: true}
  projection_status: {type: enum, values: [EVALUABLE, NON_EVALUABLE], required: true, description: "v0.2 (đóng C7-MAJ-04) — xem invariants"}
  projection_reason_code: {type: enum, values: [UNSUPPORTED_MULTIPLE_FILL_LINEAGES], required: false, description: "BẮT BUỘC khi projection_status=NON_EVALUABLE; TUYỆT ĐỐI ABSENT khi EVALUABLE"}
  contributing_fill_refs: {type: array, items: event_record_ref, required: false, description: "BẮT BUỘC khi projection_status=NON_EVALUABLE — danh sách ĐẦY ĐỦ mọi Fill eligible xung đột; TUYỆT ĐỐI ABSENT khi EVALUABLE"}
  position_direction: {type: enum, values: [LONG, SHORT], required: false, description: "chỉ có mặt khi EVALUABLE VÀ net_quantity > 0 — TUYỆT ĐỐI ABSENT khi FLAT hoặc NON_EVALUABLE"}
  net_quantity: {type: decimal, required: false, description: "chỉ có mặt khi EVALUABLE — non-negative magnitude, 0 khi FLAT, > 0 khi LONG/SHORT; TUYỆT ĐỐI ABSENT khi NON_EVALUABLE"}
  quantity_unit: {type: string, required: false, description: "chỉ có mặt khi EVALUABLE VÀ net_quantity > 0"}
  average_entry_price: {type: decimal, required: false, description: "chỉ có mặt khi EVALUABLE VÀ net_quantity > 0 — v0.2 (đúng một Fill eligible) = fill_price của Fill đó nguyên vẹn"}
  price_currency: {type: string, required: false, description: "chỉ có mặt khi EVALUABLE VÀ net_quantity > 0"}
  position_context_cursor: {type: object, required: true, description: "Replay Cursor hợp lệ, TÁI SỬ DỤNG nguyên vẹn Chapter 8 §8.5.1"}
  last_fill_recorded_time: {type: timestamp, required: false, description: "chỉ có mặt khi EVALUABLE VÀ net_quantity > 0"}
queries: [GetPositionForKey, GetPositionHistory]
```

## 2. Position fold (deterministic projection algorithm, v0.2 đóng `C7-MAJ-04`)

```text
1. Group mọi Fill (fill.md §3, KHÔNG dùng FillCurrentView) theo Position key derived từ
   (Fill.account_id, Fill.environment, Fill.instrument_selection_ref).
2. Với mỗi Fill trong group, đánh giá eligible_as_position_contributing_fill(fill_id, C) (fill.md
   §6) — TẬP eligible_fills = { Fill | eligible_as_position_contributing_fill(Fill.fill_id, C) ==
   true }.
3. NẾU |eligible_fills| == 0:
   projection_status = EVALUABLE
   position_direction ABSENT, net_quantity = 0 (FLAT)
   projection_reason_code/contributing_fill_refs ABSENT
4. NẾU |eligible_fills| == 1 (Fill duy nhất F):
   projection_status = EVALUABLE
   position_direction = F.direction
   net_quantity = F.fill_quantity
   quantity_unit = F.quantity_unit
   average_entry_price = F.fill_price
   price_currency = F.price_currency
   last_fill_recorded_time = F.envelope.recorded_time
   projection_reason_code/contributing_fill_refs ABSENT
5. NẾU |eligible_fills| > 1:
   projection_status = NON_EVALUABLE
   projection_reason_code = UNSUPPORTED_MULTIPLE_FILL_LINEAGES
   contributing_fill_refs = { event_record_ref của MỌI Fill trong eligible_fills }
   position_direction/net_quantity/quantity_unit/average_entry_price/price_currency TUYỆT ĐỐI
   ABSENT — KHÔNG chọn một Fill, KHÔNG aggregate, KHÔNG weighted average, KHÔNG report FLAT.
6. Position PHẢI rebuild TỪ ĐẦU tại mọi cursor C được yêu cầu — KHÔNG cache mutate incremental làm
   nguồn authoritative.
```

**Vì v0.1/v0.2 CHỈ authorize `OPEN_EXPOSURE`** — Position KHÔNG BAO GIỜ cần close/reduce/reversal arithmetic. Bước 5 (NON_EVALUABLE) là cơ chế TƯỜNG MINH thay thế cho "giả định ngầm chỉ một Fill" của v0.1 — v0.2 KHÔNG còn giả định KHÔNG kiểm chứng, mà chủ động phát hiện VÀ báo cáo trường hợp vi phạm giả định đó.

## 3. Representation — magnitude tách biệt khỏi direction

```text
net_quantity (khi EVALUABLE) KHÔNG BAO GIỜ signed — LUÔN non-negative magnitude.

FLAT (EVALUABLE):        net_quantity = 0,   position_direction ABSENT
LONG (EVALUABLE):        net_quantity > 0,   position_direction = LONG
SHORT (EVALUABLE):       net_quantity > 0,   position_direction = SHORT
NON_EVALUABLE:           net_quantity ABSENT, position_direction ABSENT
```

Direction và magnitude là HAI trường tách biệt tường minh, KHÔNG gộp thành một signed scalar (đúng bài học `risk.md` §5b1's `current_instrument_exposure_value` GROSS, KHÔNG signed).

## 4. Position recomputation sau Fill/ExecutionResult correction

**Position KHÔNG được correct bằng mutation trực tiếp — KHÔNG compensating Position event/command nào tồn tại.** Mọi thay đổi Position LUÔN đi qua recompute `eligible_as_position_contributing_fill` (fill.md §6):

```text
Fill F1 eligible → Position LONG hoặc SHORT (§2 bước 4)

invalidate ExecutionResult mà F1 tham chiếu (execution-result.md §7) — v0.2, đóng C7-MAJ-03:
  → eligible_as_position_contributing_fill(F1, C) chuyển false NGAY LẬP TỨC tại cursor invalidate đó
  → Position projection (§2) EXCLUDES F1 khỏi eligible_fills — KHÔNG chờ FillFactInvalidated
  → NẾU không còn Fill eligible nào khác → Position recompute FLAT (§2 bước 3)
  → KHÔNG compensating Position event nào được emit

invalidate F1 trực tiếp (fill.md §4, độc lập)
  → tương tự — F1 loại khỏi eligible_fills, Position recompute

replacement F2 xuất hiện (fill.md §7, CHỈ khi ExecutionResult vẫn visible-valid EXECUTED)
  → Position projection (§2) recompute lại, F2 nay đóng góp (nếu eligible)
  → Position trở lại LONG/SHORT theo payload F2 (Scenario 16, §9)
```

## 5. Downstream reference contract

Package tương lai (chưa author, ngoài phạm vi C7) tham chiếu Position qua ĐÚNG các field sau, KHÔNG hơn:

```yaml
position_key: {type: string, description: "= §1, derived structural key"}
account_id: {type: string, ref: account, description: "= §1"}
environment: {type: enum, values: [PAPER], description: "= §1"}
instrument_selection_ref: {type: object, description: "= §1"}
projection_status: {type: enum, values: [EVALUABLE, NON_EVALUABLE], description: "= §1 — BẮT BUỘC kiểm tra TRƯỚC khi đọc bất kỳ economics field nào"}
position_direction: {type: enum, values: [LONG, SHORT], description: "= §1, ABSENT khi FLAT hoặc NON_EVALUABLE"}
net_quantity: {type: decimal, description: "= §1 — GUARANTEE: non-negative magnitude, CHỈ có mặt khi EVALUABLE"}
quantity_unit: {type: string, description: "= §1"}
average_entry_price: {type: decimal, description: "= §1"}
```

**Downstream authority rule:** mọi consumer PHẢI resolve Position TRỰC TIẾP qua fold algorithm (§2) TẠI ĐÚNG cursor mà chính computation đó đang dùng — VÀ PHẢI kiểm tra `projection_status` TRƯỚC khi đọc bất kỳ economics field nào (`NON_EVALUABLE` nghĩa là KHÔNG có câu trả lời deterministic an toàn, consumer PHẢI xử lý tường minh, KHÔNG mặc định FLAT/zero).

## 6. Prohibitions

**Position KHÔNG được sở hữu:** Fill/ExecutionResult/PaperExecutionObservation/Order identity semantics; close/reduce/reversal arithmetic; portfolio-level aggregation/cross-account/cross-listing netting; weighted-average/netting arithmetic cho nhiều Fill (khi cần, trả `NON_EVALUABLE`, KHÔNG tự ý tính); realized/unrealized PnL; margin/leverage/liquidation; accounting ledger; FX conversion; authoritative event stream riêng; mutable command trực tiếp; general workflow/saga engine; UI copy/natural-language generation infrastructure.

## 7. Ngoài phạm vi — defer

- **Multiple-Fill-per-Position-key resolution (v0.2, đóng `C7-MAJ-04`, disclosed):** v0.2 KHÔNG author bất kỳ aggregation/netting/weighted-average logic nào cho trường hợp nhiều eligible Fill lineage cùng Position key — projection formally trả `NON_EVALUABLE` thay vì silently sai hoặc giả định không kiểm chứng (khác v0.1's implicit "bound tới một Fill"). Nếu Phase sau cần hỗ trợ nhiều Fill lineage hợp lệ đồng thời (ví dụ nhiều Order cùng Account/Listing), cần một correction/extension riêng định nghĩa CHÍNH XÁC công thức aggregation — KHÔNG retrofit ở đây.
- Position Current View/snapshot table cụ thể (nếu cần cache).
- Close/Reduce/Reversal Position arithmetic.
- Cross-Position/portfolio-level view.

## 8. Open questions ngoài phạm vi

- Cơ chế cache/materialization cụ thể cho Position projection tại scale.
- Công thức aggregation/netting chính xác cho multiple-Fill support (nếu Phase sau cần) — chưa quyết.
- Không đóng OQ-002/OQ-003.

## 9. Acceptance scenarios (v0.2 — phần liên quan trực tiếp Position; xem `execution-result.md`/`fill.md`/`replay-event.md` cho phần còn lại)

**Scenario 28 — Zero Fill Position (v0.2, MỚI, đóng `C7-MAJ-04`):** eligible Fill count = 0 → `projection_status=EVALUABLE`, FLAT.

**Scenario 13 — Position from LONG Fill (v0.2: One Fill Position — eligible Fill count = 1, `projection_status=EVALUABLE`):** LONG Fill eligible → Position `LONG`, `net_quantity = fill_quantity`, `average_entry_price = fill_price`.

**Scenario 14 — Position from SHORT Fill:** SHORT Fill eligible → Position `SHORT`, tương tự (cùng `projection_status=EVALUABLE` framing, Scenario 13).

**Scenario 29 — Multiple Fill Position (v0.2, MỚI, đóng `C7-MAJ-04`):** eligible Fill count > 1 → `projection_status=NON_EVALUABLE`, `projection_reason_code=UNSUPPORTED_MULTIPLE_FILL_LINEAGES`, `contributing_fill_refs` liệt kê đầy đủ — KHÔNG fabricated Position economics, KHÔNG chọn một Fill, KHÔNG aggregate.

**Scenario 15 — Fill invalidation:** F1 eligible → Position LONG/SHORT → invalidate F1 → Position recompute → `FLAT` nếu không còn Fill eligible khác.

**Scenario 16 — Fill replacement:** F1 invalidate → F2 replacement (ExecutionResult vẫn EXECUTED) → Position recompute từ F2.

**Scenario 17 — Result correction EXECUTED→NOT_EXECUTED (v0.2, REVISED, đóng `C7-MAJ-03`):** F1 trở derived-ineligible NGAY LẬP TỨC khi ExecutionResult invalidate (fill.md §6) — KHÔNG chờ `FillFactInvalidated`. Position recompute → FLAT (walking skeleton, đúng một Fill lineage).
