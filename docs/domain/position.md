---
id: position
title: Position
version: "0.1"
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

> **Vai trò của tài liệu này:** Domain Contract thứ ba của Package 0.2-C7 (Execution Result, Fill, Position and Replay Integration Foundation) — định nghĩa **Position**, một PROJECTION deterministic, non-authoritative, dẫn xuất TRỌN VẸN từ visible-valid [`fill.md`](./fill.md) Fill history. Draft, chưa Approved/Locked. Thuộc capability `execution-management` / context `position-management` (đăng ký MỚI tại [`context-map.yaml`](./context-map.yaml)). Kiến trúc controlling: [`fill.md`](./fill.md) v0.1 Draft (Fill, KHÔNG sửa), [Chapter 7 §7.4](../constitution/07-module-taxonomy.md) (Locked, Projection semantics — Type 2 Projection, đối xứng `context.md`'s MarketContextSnapshot). Tài liệu này CHỈ implement field/invariant mà các nguồn trên yêu cầu, KHÔNG tự quyết architecture mới ngoài phạm vi đã khóa.

Position **KHÔNG phải** một authoritative fact độc lập, KHÔNG có event stream riêng, KHÔNG có mutable command trực tiếp — nó là **một hàm thuần túy, deterministic của visible-valid Fill history** tại một cursor cho trước. Position trả lời chính xác bốn câu hỏi: Account/environment/TradableListing nào đang được xem xét? Net exposure hiện tại (direction + quantity) là gì? Average entry price là gì? Fill nào (visible-valid) đóng góp vào projection này?

**Ví dụ walking-skeleton (tiếp `fill.md`):** một Fill LONG hoặc SHORT duy nhất → Position LONG hoặc SHORT, `net_quantity = fill_quantity`, `average_entry_price = fill_price`. **v0.1 bounded rule (disclosed, §7):** đúng MỘT visible-valid Fill đóng góp vào một Position key — tránh silently author portfolio netting/aggregation. Hai mươi bốn Scenario chấp nhận toàn Package 0.2-C7 (1–24) — phần liên quan trực tiếp Position liệt kê tại §9.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B/C1–C7:** Position Current View (nếu có) KHÔNG BAO GIỜ authority; rebuild deterministic hoàn toàn từ authoritative Fill event stream; KHÔNG compensating Position event khi Fill invalidate — recompute trực tiếp.

**Phạm vi bounded tường minh:** KHÔNG author close/reduce/reversal arithmetic — v0.1 CHỈ authorize `OPEN_EXPOSURE` (order.md §1), Position chỉ CÓ THỂ chuyển FLAT→LONG/SHORT qua đúng một Fill, KHÔNG signed netting giữa nhiều Fill. KHÔNG portfolio aggregation/cross-account/cross-listing netting. KHÔNG realized/unrealized PnL. KHÔNG margin/leverage/liquidation. KHÔNG accounting ledger. KHÔNG FX conversion. KHÔNG mutable Position command trực tiếp — Position CHỈ là derived projection. KHÔNG redefine Fill contract. KHÔNG sửa `fill.md`/`execution-result.md`/`order.md`/`execution-intent.md`/`risk.md`/`decision.md`/`trade-intent.md`/C1–C6/ADR/Constitution.

## 1. Position — `kind: read_model` (Type 2 Projection, Chapter 7 §7.4)

**Không phải authoritative event/entity — KHÔNG có event stream riêng.** Position là derived projection thuần túy — rebuild được hoàn toàn từ authoritative `fill.md` §3–§4 event stream tại một cursor.

```yaml
id: position
kind: read_model
capability_id: execution-management
domain_context_id: position-management
description: >
  PROJECTION deterministic của visible-valid Fill history (fill.md §5 fold) cho một Position key
  (account_id, environment, instrument_selection_ref). KHÔNG authoritative — KHÔNG mutable command
  trực tiếp, KHÔNG event/subject riêng, rebuild được hoàn toàn từ Fill event stream (Chapter 7 §7.4
  rebuild determinism).
invariants:
  - "position_key = (account_id, environment, instrument_selection_ref) — BẤT BIẾN theo cấu trúc, KHÔNG derive từ Fill fact cụ thể nào."
  - "net_quantity LUÔN non-negative magnitude — direction VÀ magnitude tách biệt tường minh, KHÔNG combine signed quantity với direction (§3)."
  - "FLAT ⟺ net_quantity == 0 (position_direction TUYỆT ĐỐI ABSENT). LONG/SHORT ⟺ net_quantity > 0 VÀ position_direction có mặt CHÍNH XÁC MỘT trong hai giá trị."
  - "**v0.1 bounded rule (§7, disclosed):** đúng MỘT visible-valid Fill (fill.md §5 fold, per execution_result_id lineage) đóng góp vào một Position key tại một thời điểm — v0.1 KHÔNG author same-direction weighted aggregation cho nhiều Fill riêng biệt cùng key (tránh silently author portfolio netting/aggregation, xem §7 cho lý do đầy đủ)."
  - "Position PHẢI recompute TRỌN VẸN từ scratch mỗi khi Fill history thay đổi (invalidate/replace, fill.md §4/§6) — KHÔNG mutate incremental, KHÔNG compensating Position event/command nào tồn tại (§4)."
schema:
  position_key: {type: string, required: true, description: "derived, = f(account_id, environment, instrument_selection_ref) — KHÔNG opaque identity riêng, hoàn toàn structural"}
  account_id: {type: string, required: true, ref: account}
  environment: {type: enum, values: [PAPER], required: true}
  instrument_selection_ref:
    type: object
    required: true
    fields:
      instrument_id: {type: string, required: true}
      venue_id: {type: string, required: true}
      listing_id: {type: string, required: true}
  position_direction: {type: enum, values: [LONG, SHORT], required: false, description: "chỉ có mặt khi net_quantity > 0 (§1 invariant) — TUYỆT ĐỐI ABSENT khi FLAT"}
  net_quantity: {type: decimal, required: true, description: "non-negative magnitude — 0 khi FLAT, > 0 khi LONG/SHORT"}
  quantity_unit: {type: string, required: false, description: "chỉ có mặt khi net_quantity > 0"}
  average_entry_price: {type: decimal, required: false, description: "chỉ có mặt khi net_quantity > 0 — v0.1 (đúng một Fill đóng góp) = fill_price của Fill đó nguyên vẹn"}
  price_currency: {type: string, required: false, description: "chỉ có mặt khi net_quantity > 0, = fill.md §1 price_currency"}
  position_context_cursor: {type: object, required: true, description: "Replay Cursor hợp lệ, TÁI SỬ DỤNG nguyên vẹn Chapter 8 §8.5.1 — cursor tại đó projection này được tính"}
  last_fill_recorded_time: {type: timestamp, required: false, description: "chỉ có mặt khi net_quantity > 0 — recorded_time của Fill visible-valid đóng góp"}
queries: [GetPositionForKey, GetPositionHistory]
```

## 2. Position fold (deterministic projection algorithm)

**Fold algorithm — MỘT quy tắc chung, đúng pattern "rebuild from authoritative stream" đã proven xuyên suốt Package 0.2 (Chapter 7 §7.4):**

```text
1. Group mọi Fill (fill.md §3, KHÔNG dùng FillCurrentView latest-state) theo Position key derived từ
   (Fill.account_id, Fill.environment, Fill.instrument_selection_ref).
2. Với mỗi group, tính visible-valid-head Fill CHO TỪNG execution_result_id lineage riêng biệt (đúng
   fold algorithm fill.md §5 — explicit supersedes_fact_ref chain per execution_result_id) tại cursor C.
3. Tổng hợp mọi visible-valid Fill (một per execution_result_id lineage còn hợp lệ) thuộc group này —
   v0.1 bounded rule (§1 invariant, §7): TỐI ĐA MỘT Fill lineage được PHÉP đóng góp cho một Position
   key tại v0.1 walking skeleton (một Order → một Execution Intent → một Position key duy nhất trong
   ví dụ bounded).
4. NẾU zero Fill visible-valid đóng góp → position_direction ABSENT, net_quantity = 0 (FLAT).
5. NẾU đúng một Fill visible-valid đóng góp:
   position_direction = Fill.direction (LONG hoặc SHORT, đối xứng trực tiếp — v0.1 KHÔNG suy luận
   thêm)
   net_quantity = Fill.fill_quantity
   average_entry_price = Fill.fill_price
   quantity_unit = Fill.quantity_unit
   price_currency = Fill.price_currency
   last_fill_recorded_time = Fill.envelope.recorded_time
6. Position PHẢI rebuild TỪ ĐẦU tại mọi cursor C được yêu cầu — KHÔNG cache mutate incremental làm
   nguồn authoritative (cache CHỈ chấp nhận khi provably equivalent với reconstruction từ đầu).
```

**Vì v0.1 CHỈ authorize `OPEN_EXPOSURE`** (order.md §1, execution-intent.md §1) — Position KHÔNG BAO GIỜ cần close/reduce/reversal arithmetic ở v0.1; một Fill LONG luôn tạo Position LONG mới từ FLAT, một Fill SHORT luôn tạo Position SHORT mới từ FLAT — KHÔNG có concept "giảm Position hiện có" trong walking skeleton này.

## 3. Representation — magnitude tách biệt khỏi direction

```text
net_quantity KHÔNG BAO GIỜ signed — LUÔN non-negative magnitude, đúng yêu cầu "Do not combine
signed quantity with direction."

FLAT:        net_quantity = 0,   position_direction ABSENT
LONG:        net_quantity > 0,   position_direction = LONG
SHORT:       net_quantity > 0,   position_direction = SHORT
```

Đây là bounded representation đơn giản nhất phù hợp walking skeleton v0.1 — direction và magnitude là HAI trường tách biệt tường minh, KHÔNG gộp thành một signed scalar (tránh nhầm lẫn dấu ± với LONG/SHORT semantics, đúng bài học đã áp dụng cho `current_instrument_exposure_value` tại `risk.md` §5b1 — GROSS, KHÔNG signed).

## 4. Position recomputation sau Fill correction

**Position KHÔNG được correct bằng mutation trực tiếp — KHÔNG compensating Position event/command nào tồn tại.** Mọi thay đổi Position LUÔN đi qua Fill correction (`fill.md` §4/§6):

```text
Fill F1 visible-valid → Position LONG hoặc SHORT (§2 bước 5)

invalidate F1 (fill.md §4)
  → Position projection (§2) EXCLUDES F1 khỏi bước 3
  → NẾU không còn Fill visible-valid nào khác cho key này → Position recompute FLAT (§2 bước 4)
  → KHÔNG compensating Position event nào được emit — Position CHỈ là kết quả recompute, KHÔNG
    phải một fact riêng cần "sửa"

replacement F2 xuất hiện (fill.md §6)
  → Position projection (§2) recompute lại, F2 nay đóng góp
  → Position trở lại LONG/SHORT theo payload F2 (Scenario 16, §9)
```

**Khi ExecutionResult gốc chuyển EXECUTED→NOT_EXECUTED (execution-result.md §7/fill.md §4 coupling rule):** Fill bị bắt buộc invalidate — Position recompute theo, thường về FLAT trừ khi Fill khác (execution_result_id lineage khác) vẫn đóng góp cho cùng key (Scenario 17, §9).

## 5. Downstream reference contract

Package tương lai (chưa author, ngoài phạm vi C7) tham chiếu Position qua ĐÚNG các field sau, KHÔNG hơn:

```yaml
position_key: {type: string, description: "= §1, derived structural key"}
account_id: {type: string, ref: account, description: "= §1"}
environment: {type: enum, values: [PAPER], description: "= §1"}
instrument_selection_ref: {type: object, description: "= §1"}
position_direction: {type: enum, values: [LONG, SHORT], description: "= §1, ABSENT khi FLAT"}
net_quantity: {type: decimal, description: "= §1 — GUARANTEE: non-negative magnitude"}
quantity_unit: {type: string, description: "= §1"}
average_entry_price: {type: decimal, description: "= §1"}
```

**Downstream authority rule:** mọi consumer PHẢI resolve Position TRỰC TIẾP qua fold algorithm (§2) TẠI ĐÚNG cursor mà chính computation đó đang dùng — KHÔNG BAO GIỜ dùng một Position cache/snapshot làm authoritative input trừ khi provably equivalent với reconstruction từ đầu (§1 invariant). `position.md` KHÔNG author semantics của bất kỳ package downstream nào (chưa tồn tại).

## 6. Prohibitions

**Position KHÔNG được sở hữu:** Fill/ExecutionResult/Order identity semantics; close/reduce/reversal arithmetic; portfolio-level aggregation/cross-account/cross-listing netting; realized/unrealized PnL; margin/leverage/liquidation; accounting ledger; FX conversion; authoritative event stream riêng (Position KHÔNG có `PositionRecorded`/`PositionChanged` event nào); mutable command trực tiếp; general workflow/saga engine; UI copy/natural-language generation infrastructure.

## 7. Ngoài phạm vi — defer

- **Multiple-Fill-per-Position-key aggregation (disclosed v0.1 judgment call):** task yêu cầu chọn MỘT trong hai lựa chọn — (a) same-direction weighted aggregation, hoặc (b) bound v0.1 tới một active Fill per Position key. **Quyết định: (b) — v0.1 walking skeleton bound tới đúng MỘT visible-valid Fill lineage đóng góp cho một Position key** (§1/§2). Lý do: walking skeleton hiện tại (một Execution Intent → một Order → zero/một Fill) tự nhiên không bao giờ sản sinh nhiều Fill lineage cùng key trong phạm vi C7; weighted aggregation là một phép tính CÓ Ý NGHĨA kinh tế (average cost basis qua nhiều lần vào lệnh) mà task không yêu cầu xây dựng, và author nó bây giờ sẽ là silently author một dạng portfolio-netting semantics ngoài bounded scope — nếu nhiều Order/Fill cùng Position key xuất hiện trong Phase sau, cần một correction/extension riêng, KHÔNG retrofit ở đây.
- Position Current View/snapshot table cụ thể (nếu cần cache) — v0.1 CHỈ pin fold algorithm (§2) là nguồn sự thật; caching layer cụ thể deferred Phase 1, PHẢI provably equivalent nếu triển khai.
- Close/Reduce/Reversal Position arithmetic — hoàn toàn ngoài phạm vi vì v0.1 execution_action CHỈ `OPEN_EXPOSURE` (order.md §1).
- Cross-Position/portfolio-level view — hoàn toàn ngoài phạm vi.

## 8. Open questions ngoài phạm vi

- Cơ chế cache/materialization cụ thể cho Position projection tại scale — chưa quyết, Phase 1.
- Không đóng OQ-002/OQ-003.

## 9. Acceptance scenarios (validation, không phải executable test tại C7 — phần liên quan trực tiếp Position)

**Scenario 13 — Position from LONG Fill:** LONG Fill → Position `LONG`, `net_quantity = fill_quantity`, `average_entry_price = fill_price`.

**Scenario 14 — Position from SHORT Fill:** SHORT Fill → Position `SHORT`, `net_quantity = fill_quantity`, `average_entry_price = fill_price`.

**Scenario 15 — Fill invalidation:** F1 visible → Position LONG/SHORT → invalidate F1 → Position recompute → `FLAT` nếu không còn Fill valid khác cho key này.

**Scenario 16 — Fill replacement:** F1 invalidate → F2 replacement → Position recompute từ F2.

**Scenario 17 — Result correction EXECUTED→NOT_EXECUTED:** F1 bắt buộc invalidate theo (fill.md §4/§6, execution-result.md §7) → Position recompute — về FLAT (walking skeleton, đúng MỘT Fill lineage).

**Scenario 21 — Replay before Fill correction:** cursor TRƯỚC invalidation → predecessor Fill visible → predecessor Position visible (LONG/SHORT).

**Scenario 22 — Replay after Fill invalidation:** cursor SAU invalidation, TRƯỚC replacement → Position recomputed KHÔNG có Fill invalid đó (thường FLAT).

**Scenario 23 — Replay after replacement Fill:** replacement visible → Position recomputed từ replacement Fill.
