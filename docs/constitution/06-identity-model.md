---
id: 06-identity-model
title: Identity Model
version: "2.4"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-18"
next_review: null
depends_on: ["02-platform-invariants", "04-domain-principles", "05-time-model"]
---

# 6. Identity Model

## 6.1 Nguyên tắc ID

Mọi entity/event có ý nghĩa nghiệp vụ đều mang một identifier bất biến. Constitution định nghĩa **nguyên tắc** ID, không liệt kê danh sách ID cụ thể của từng domain entity — danh sách đó thuộc Domain Contract tại `/docs/domain/` (theo [Chapter 4](./04-domain-principles.md), tránh hardcode domain trong Constitution).

Yêu cầu với mọi ID:
- **Unique** trong scope đã khai báo. Scope phải được **khai báo tường minh** trong Domain Contract của entity (global / per-Account / per-Context / per-Venue...) — không mặc định global. Ví dụ: `OrderID` có thể unique per-Account chứ không cần global; venue-assigned order ID chỉ unique trong phạm vi 1 venue.
- **Globally resolvable khi đi qua boundary:** nếu ID không globally unique, mọi reference đi qua Account/Context/Venue/integration boundary PHẢI mang đủ scope/namespace để resolve duy nhất đối tượng. Cấm truyền local ID trần khi consumer phải ngầm đoán Context/Account/Venue/entity type.

```yaml
# Sai — consumer không biết order nào nếu OrderID chỉ unique per-Account
order_id: "123"

# Đúng — qualified reference, tự đủ để resolve
subject_ref:
  context_id: execution
  account_id: account_01
  entity_type: order
  entity_id: "123"
```

*Nguyên tắc: local uniqueness được phép; ambiguous cross-boundary reference thì không.*
- **Immutable** — không bao giờ tái sử dụng hoặc sửa sau khi cấp phát.

Về **cách sinh ID**, phân biệt 2 nhu cầu khác nhau (không gộp thành 1 yêu cầu "distributed-safe" tuyệt đối):
- **Identity uniqueness** — chỉ cần đảm bảo không đụng độ. Có thể sinh phân tán không cần điều phối tập trung (ULID, UUIDv7...). Đây là mặc định cho hầu hết entity/event.
- **Ordering/sequence assignment** — khi một stream cần **total order** hoặc **monotonic sequence** (ví dụ event log của một partition, hay authoritative ordering cho arbitrage đa sàn theo [Chapter 5 §5.4](./05-time-model.md)), việc cấp phát vị trí thứ tự CÓ THỂ cần một single-writer/coordinator cho stream đó. Đây KHÔNG bị cấm — nó là cơ chế hợp lệ và đôi khi bắt buộc. Constitution không ép mọi ID phải sinh được hoàn toàn phi tập trung.

Ranh giới: *uniqueness* của ID và *ordering position* là 2 mối quan tâm tách biệt (xem §6.3) — một entity có thể có ID sinh phân tán, nhưng vị trí của nó trong một ordered stream do ordering authority cấp.

**Thời điểm cấp ID:** ID phải được cấp **trước hoặc tại thời điểm** entity/event đầu tiên tồn tại — không cấp muộn sau khi đã có side effect. Điều này bắt buộc cho [I-10 Idempotent Execution](./02-platform-invariants.md): execution intent phải có client-assigned ID **trước khi** gửi lệnh ra venue, để retry/reconcile dựa trên ID đó (nếu ID cấp sau khi venue đã nhận lệnh, không thể chống duplicate).

Cơ chế cụ thể (ULID, UUIDv7, Snowflake, KSUID...) là **quyết định kiến trúc → ADR**, không chốt trong Constitution. Nguyên tắc trên tồn tại lâu hơn bất kỳ lựa chọn công nghệ ID nào.

## 6.2 Ba loại identity — Event, Entity, và Value Object

Phân biệt này bắt buộc để nhất quán với [I-3 No Repaint](./02-platform-invariants.md), [I-13 State Transition Integrity](./02-platform-invariants.md), và [Chapter 4 Domain Contract](./04-domain-principles.md) (có `kind: value_object`):

| Loại | Bản chất | Quy tắc ID | Ví dụ |
|---|---|---|---|
| **Event Record Identity** (`event_id`) | Bản ghi sự kiện bất biến, append-only | Mỗi event record có 1 `event_id` MỚI, bất biến, duy nhất. Mỗi record PHẢI tham chiếu identity của domain subject mà nó mô tả (`subject_id`/`entity_id` theo Event Contract) | `SwingPublished` (evt_001) và `SwingInvalidated` (evt_002) là 2 record, 2 `event_id` — nhưng cùng trỏ về `subject_id: swing_123` |
| **Entity Identity** (`entity_id`) | Đối tượng có vòng đời trạng thái (I-13) | Giữ NGUYÊN 1 ID xuyên suốt mọi state transition; đổi state KHÔNG đổi ID | Một Position đi OPEN→PARTIAL→CLOSED vẫn là cùng 1 `PositionID` |
| **Value Object** | Giá trị bất biến, KHÔNG có identity riêng — bằng nhau khi các thuộc tính bằng nhau (equality by value) | KHÔNG cấp ID. Được so sánh/lưu theo giá trị, không theo identity | Một `Price`, một `Money{amount, currency}`, một `TimeRange` |

**Điểm mấu chốt 1 — `New Event ID ≠ New Entity ID`:** một event record mới LUÔN có `event_id` mới, nhưng điều đó KHÔNG tự động tạo ra domain entity identity mới. Correction, invalidation, hay state transition đều tạo event record mới trong khi subject có thể giữ nguyên `entity_id`. Việc một correction/replacement tạo entity MỚI hay giữ entity CŨ là **semantic do Domain Contract quyết định** ([Chapter 4](./04-domain-principles.md)), không được suy ra chỉ từ việc có event mới.

```yaml
# Đúng: 2 event record, 1 domain subject
swing_id: swing_123          # entity identity — không đổi
events:
  - event_id: evt_001        # event record identity
    event_type: SwingPublished
    subject_id: swing_123
  - event_id: evt_002        # event record identity mới
    event_type: SwingInvalidated
    subject_id: swing_123    # VẪN là subject cũ
    causation_id: evt_001
```

**Điểm mấu chốt 2 (nhất quán I-13):** một stateful entity giữ nguyên `entity_id` qua toàn bộ state machine — mỗi transition ghi bằng transition event riêng có `event_id` riêng, nhưng entity vẫn 1 ID.

**Điểm mấu chốt 3 (nhất quán Chapter 4):** không phải mọi domain concept đều có identity — value object (`kind: value_object` trong Domain Contract) KHÔNG được cấp ID, tránh ép identity lên thứ vốn chỉ là giá trị.

## 6.3 ID và Ordering — tách bạch

ID có thể mang thông tin thời gian (ví dụ ULID/UUIDv7 nhúng timestamp) để sortable — nhưng **thứ tự authoritative KHÔNG được suy ra từ ID**. Ordering authoritative tuân theo [Chapter 5 §5.4 Ordering Authority](./05-time-model.md): dùng ID có nhúng timestamp để sort chính là dựa gián tiếp vào physical clock — đúng loại lỗi cross-node ordering mà Chapter 5 cấm.

Vai trò của tính sortable trong ID: chỉ để tối ưu index/storage locality, KHÔNG phải nguồn của business ordering hay causal ordering.

## 6.4 Account là Identity first-class (multi-account readiness)

`Account` là first-class trading identity và là **scope bắt buộc** của Position/Order/Execution ngay từ Phase 0.2 (xem [ADR-007](../adr/ADR-007.md)), dù Phase 0-3 chỉ có 1 Account. Account thuộc loại Entity Identity (§6.2) — giữ nguyên ID suốt vòng đời.

**Account ≠ Tenant:** việc scope theo AccountID tạo ra **multi-account readiness** (một chủ thể vận hành nhiều tài khoản: venue account, paper account, simulation account, portfolio ledger account...) — KHÔNG tự động tạo ra multi-tenant isolation. Tenant/workspace/organization identity và access isolation là boundary RIÊNG, không được đồng nhất với AccountID; nếu sản phẩm chuyển sang multi-tenant, đó là quyết định kiến trúc riêng cần ADR.

## 6.5 Internal Identity vs External Reference

ID do hệ thống Ride cấp phát (**internal identity**) phải tách biệt với ID do bên ngoài cấp (**external reference** — venue order ID, exchange trade ID, broker account number...):

- Internal identity tuân thủ mọi nguyên tắc ở §6.1 (Ride kiểm soát uniqueness/immutability/scope).
- External reference được **lưu như một thuộc tính** của entity, KHÔNG dùng làm primary identity của entity đó — vì Ride không kiểm soát chúng: có thể trùng giữa các venue, format thay đổi theo venue, hoặc được venue tái sử dụng.
- Ánh xạ internal ↔ external là dữ liệu, không phải identity. Ví dụ: một Order có `OrderID` internal (Ride cấp, dùng cho I-10 idempotency trước khi gửi lệnh) và lưu kèm `venue_order_id` (venue trả về sau) như attribute — reconcile dựa trên cặp này.

## 6.6 Idempotency & Deduplication Identity

**Event identity KHÔNG thay thế idempotency identity.** Cùng một business fact từ bên ngoài có thể đến nhiều lần qua nhiều đường: WebSocket push, REST reconciliation, reconnect replay, consumer retry. Mỗi lần nhận, Ride cấp một `event_id` mới hợp lệ — nhưng chúng mô tả **cùng một fill/order duy nhất**. Nếu chỉ dựa vào `event_id`, Position Ledger sẽ double-count.

Phân biệt:
- `event_id` — bản ghi nào trong Ride (mỗi delivery một ID mới, luôn hợp lệ).
- **Source/dedup identity** — delivery này có phải cùng một authoritative source fact đã xử lý chưa.

**Quy tắc:** với source có khả năng retry/redelivery, Integration/Event Contract PHẢI xác định deduplication identity kèm scope tương ứng. Hai delivery của cùng một authoritative source fact KHÔNG được tạo ra hai business effect chỉ vì chúng có hai `event_id` khác nhau.

```yaml
event_id: evt_internal_02      # record mới mỗi lần nhận
source_identity:               # bằng chứng "cùng một fact"
  venue: binance
  account_id: account_01
  type: trade_id
  value: "998877"
```

Lưu ý phân biệt với §6.1 (ID cấp trước side effect): §6.1 giải quyết **outbound** (execution intent phải có client-assigned ID trước khi gửi venue — I-10); mục này giải quyết **inbound** (duplicate source facts đến từ venue). Cơ chế dedup cụ thể thuộc [Chapter 8](./08-event-model.md)/Integration Contract.

## 6.7 Correlation & Causation Identity (nối chuỗi cho Explainability)

Ngoài ID của bản thân entity/event, [I-1 Explainability](./02-platform-invariants.md) yêu cầu truy được **chuỗi nhân quả** giữa các event — nên cần thêm 2 loại identity liên kết, tách biệt với entity ID:

- **Correlation ID** — nhóm tất cả event thuộc cùng một luồng xử lý logic (ví dụ: từ MarketData → Feature → Decision → RiskApproval → Execution của cùng 1 quyết định đều mang chung 1 correlation_id). Trả lời "những event nào thuộc cùng một câu chuyện".
- **Causation ID** — trỏ tới ID của event trực tiếp gây ra event này (parent). Trả lời "event này sinh ra do event nào".

Hai ID này là hạ tầng bắt buộc để reconstruct causation chain của I-1 — không được nhầm với entity ID (một entity có thể xuất hiện trong nhiều correlation khác nhau).

**Ranh giới sở hữu (tránh trùng thẩm quyền với Chapter 8 — I-12):** Chapter 6 sở hữu *sự tồn tại và ngữ nghĩa* của correlation/causation identity (chúng PHẢI có, nghĩa của chúng là gì). [Chapter 8 Event Model](./08-event-model.md) sở hữu *cách chúng nằm trong event schema* (field name, format, vị trí trong envelope, cardinality). Hai chapter không định nghĩa chồng lấn — Chapter 8 tham chiếu §6.7 cho ngữ nghĩa, không định nghĩa lại ngữ nghĩa.

## 6.8 ID là opaque — không mang business meaning

ID phải là **opaque identifier** — không được nhúng business meaning mà hệ thống suy diễn ngược ra để dùng trong logic. Không parse ID để lấy thông tin (loại entity, account, thời gian, venue...) rồi ra quyết định dựa trên đó. Lý do: nếu logic phụ thuộc cấu trúc bên trong ID, thì đổi format ID (ví dụ ULID → UUIDv7, hay đổi scheme khi scale) sẽ phá vỡ business logic ở nơi không ngờ tới. Thông tin nghiệp vụ phải là field tường minh của entity, không giấu trong ID. (ID CÓ THỂ mang timestamp cho mục đích sortable/index theo §6.3 — nhưng đó là tối ưu storage, không phải business meaning để logic suy diễn.)

## 6.9 Vai trò với Explainability

Identity ổn định là nền tảng bắt buộc để [I-1 Explainability](./02-platform-invariants.md) khả thi: truy vết một quyết định 3 năm sau chỉ khả thi khi mọi entity/event liên quan có ID bất biến, không tái sử dụng — nếu ID bị reuse, correlation/causation chain sẽ trỏ nhầm.
