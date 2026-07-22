---
id: 06-identity-model
title: Identity Model
version: "2.0"
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
- **Unique** trong scope đã khai báo (global, hoặc per-Account, hoặc per-Context — Domain Contract xác định scope).
- **Immutable** — không bao giờ tái sử dụng hoặc sửa sau khi cấp phát.
- **Distributed-safe** — sinh được ở nhiều service/node đồng thời không đụng độ, không cần khóa tập trung.

Cơ chế cụ thể (ULID, UUIDv7, Snowflake, KSUID...) là **quyết định kiến trúc → ADR**, không chốt trong Constitution. Nguyên tắc trên tồn tại lâu hơn bất kỳ lựa chọn công nghệ ID nào.

## 6.2 Hai loại identity — Event Identity vs Entity Identity

Phân biệt này bắt buộc để nhất quán với [I-3 No Repaint](./02-platform-invariants.md) và [I-13 State Transition Integrity](./02-platform-invariants.md):

| Loại | Bản chất | Quy tắc ID | Ví dụ |
|---|---|---|---|
| **Event Identity** | Sự kiện bất biến, append-only | Mỗi event là 1 ID mới; "sửa" = event mới liên kết ngược (ví dụ `invalidates: <id cũ>`) — KHÔNG sửa event cũ | Một Swing được publish rồi invalidate: 2 event, 2 ID, liên kết ngược |
| **Entity Identity** | Đối tượng có vòng đời trạng thái (I-13) | Giữ NGUYÊN 1 ID xuyên suốt mọi state transition; đổi state KHÔNG đổi ID | Một Position đi OPEN→PARTIAL→CLOSED vẫn là cùng 1 `PositionID` |

**Điểm mấu chốt (sửa mâu thuẫn tiềm tàng với I-13):** "một phiên bản mới = một ID mới" CHỈ áp dụng cho Event Identity, KHÔNG áp cho Entity Identity. Một stateful entity giữ nguyên ID qua toàn bộ state machine của nó (state transition được ghi bằng transition event riêng theo I-13, mỗi transition event có Event Identity riêng, nhưng entity vẫn 1 ID).

## 6.3 ID và Ordering — tách bạch

ID có thể mang thông tin thời gian (ví dụ ULID/UUIDv7 nhúng timestamp) để sortable — nhưng **thứ tự authoritative KHÔNG được suy ra từ ID**. Ordering authoritative tuân theo [Chapter 5 §5.4 Ordering Authority](./05-time-model.md): dùng ID có nhúng timestamp để sort chính là dựa gián tiếp vào physical clock — đúng loại lỗi cross-node ordering mà Chapter 5 cấm.

Vai trò của tính sortable trong ID: chỉ để tối ưu index/storage locality, KHÔNG phải nguồn của business ordering hay causal ordering.

## 6.4 Account là Identity first-class (multi-tenant readiness)

`Account` là entity first-class ngay từ Phase 0.2 (xem [ADR-007](../adr/ADR-007.md)) — Position/Order/Execution scope theo AccountID ngay từ đầu, dù Phase 0-3 chỉ có 1 Account. Chừa chỗ multi-tenant (nhiều Account + cách ly quyền truy cập) mà không redesign Position Ledger. Account thuộc loại Entity Identity (§6.2) — giữ nguyên ID suốt vòng đời.

## 6.5 Vai trò với Explainability

Identity ổn định là nền tảng bắt buộc để [I-1 Explainability](./02-platform-invariants.md) khả thi: truy vết một quyết định 3 năm sau chỉ khả thi khi mọi entity/event liên quan có ID bất biến, không tái sử dụng — nếu ID bị reuse, correlation/causation chain của I-1 sẽ trỏ nhầm.
