---
id: 06-identity-model
title: Identity Model
version: "2.1"
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
| **Event Identity** | Sự kiện bất biến, append-only | Mỗi event là 1 ID mới; "sửa" = event mới liên kết ngược (ví dụ `invalidates: <id cũ>`) — KHÔNG sửa event cũ | Một Swing được publish rồi invalidate: 2 event, 2 ID, liên kết ngược |
| **Entity Identity** | Đối tượng có vòng đời trạng thái (I-13) | Giữ NGUYÊN 1 ID xuyên suốt mọi state transition; đổi state KHÔNG đổi ID | Một Position đi OPEN→PARTIAL→CLOSED vẫn là cùng 1 `PositionID` |
| **Value Object** | Giá trị bất biến, KHÔNG có identity riêng — bằng nhau khi các thuộc tính bằng nhau (equality by value) | KHÔNG cấp ID. Được so sánh/lưu theo giá trị, không theo identity | Một `Price`, một `Money{amount, currency}`, một `TimeRange` |

**Điểm mấu chốt 1 (nhất quán I-13):** "một phiên bản mới = một ID mới" CHỈ áp dụng cho Event Identity, KHÔNG áp cho Entity Identity. Một stateful entity giữ nguyên ID qua toàn bộ state machine (mỗi state transition ghi bằng transition event riêng có Event Identity riêng, nhưng entity vẫn 1 ID).

**Điểm mấu chốt 2 (nhất quán Chapter 4):** không phải mọi domain concept đều có identity — value object (`kind: value_object` trong Domain Contract) KHÔNG được cấp ID, tránh ép identity lên thứ vốn chỉ là giá trị.

## 6.3 ID và Ordering — tách bạch

ID có thể mang thông tin thời gian (ví dụ ULID/UUIDv7 nhúng timestamp) để sortable — nhưng **thứ tự authoritative KHÔNG được suy ra từ ID**. Ordering authoritative tuân theo [Chapter 5 §5.4 Ordering Authority](./05-time-model.md): dùng ID có nhúng timestamp để sort chính là dựa gián tiếp vào physical clock — đúng loại lỗi cross-node ordering mà Chapter 5 cấm.

Vai trò của tính sortable trong ID: chỉ để tối ưu index/storage locality, KHÔNG phải nguồn của business ordering hay causal ordering.

## 6.4 Account là Identity first-class (multi-tenant readiness)

`Account` là entity first-class ngay từ Phase 0.2 (xem [ADR-007](../adr/ADR-007.md)) — Position/Order/Execution scope theo AccountID ngay từ đầu, dù Phase 0-3 chỉ có 1 Account. Chừa chỗ multi-tenant (nhiều Account + cách ly quyền truy cập) mà không redesign Position Ledger. Account thuộc loại Entity Identity (§6.2) — giữ nguyên ID suốt vòng đời.

## 6.5 Correlation & Causation Identity (nối chuỗi cho Explainability)

Ngoài ID của bản thân entity/event, [I-1 Explainability](./02-platform-invariants.md) yêu cầu truy được **chuỗi nhân quả** giữa các event — nên cần thêm 2 loại identity liên kết, tách biệt với entity ID:

- **Correlation ID** — nhóm tất cả event thuộc cùng một luồng xử lý logic (ví dụ: từ MarketData → Feature → Decision → RiskApproval → Execution của cùng 1 quyết định đều mang chung 1 correlation_id). Trả lời "những event nào thuộc cùng một câu chuyện".
- **Causation ID** — trỏ tới ID của event trực tiếp gây ra event này (parent). Trả lời "event này sinh ra do event nào".

Hai ID này là hạ tầng bắt buộc để reconstruct causation chain của I-1 — không được nhầm với entity ID (một entity có thể xuất hiện trong nhiều correlation khác nhau). Cấu trúc/format cụ thể do [Chapter 8 Event Model](./08-event-model.md) sở hữu; Chapter 6 chỉ quy định 2 loại identity này PHẢI tồn tại.

## 6.6 Vai trò với Explainability

Identity ổn định là nền tảng bắt buộc để [I-1 Explainability](./02-platform-invariants.md) khả thi: truy vết một quyết định 3 năm sau chỉ khả thi khi mọi entity/event liên quan có ID bất biến, không tái sử dụng — nếu ID bị reuse, correlation/causation chain sẽ trỏ nhầm.
