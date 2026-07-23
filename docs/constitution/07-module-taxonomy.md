---
id: 07-module-taxonomy
title: Module Taxonomy
version: "2.0"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-18"
next_review: null
depends_on: ["02-platform-invariants", "03-engineering-principles", "04-domain-principles"]
---

# 7. Module Taxonomy

Hệ thống có **3 loại module khác nhau** — không phải mọi thứ đều là "Engine". Phân loại theo **trách nhiệm chính** của module đối với dữ liệu, không theo việc module có business logic hay không (việc module nào sở hữu loại logic nào do [Chapter 3 §3.1](./03-engineering-principles.md) quyết định — xem 7.2).

## 7.1 Ba loại module

| Loại | Trách nhiệm chính | Ràng buộc |
|---|---|---|
| **Type 1 — Compute Engine** | **Sinh ra fact mới** từ input: tính toán, suy diễn, rồi publish event mới | Phải tuân [I-3 No Repaint/No Look-Ahead](./02-platform-invariants.md) — không dùng dữ liệu tương lai để sinh output quá khứ |
| **Type 2 — Projection** | **Không sinh fact mới.** Subscribe event và aggregate thành read-model (CQRS) | Phải rebuild được 100% từ authoritative source ([I-12](./02-platform-invariants.md) — derived representation). Không được ra **quyết định nghiệp vụ** hay sinh fact mới (xem 7.3) |
| **Type 3 — Runtime Service** | Vận hành hệ thống: I/O với thế giới bên ngoài, điều phối, thực thi, kiểm soát | Là loại module, KHÔNG phải tuyên bố rằng module đó không có business logic (xem 7.2) |

## 7.2 Loại module KHÔNG quyết định quyền sở hữu business logic

Đây là điểm dễ hiểu nhầm nhất. Việc một module thuộc Type 3 (Runtime Service) **không** có nghĩa nó chỉ làm I/O thuần túy:

- **Risk Gateway** là Type 3 (nó vận hành, kiểm soát, chặn/cho qua execution) — nhưng theo [Chapter 3 §3.1](./03-engineering-principles.md) (Locked), nó **sở hữu và bắt buộc phải có authoritative Risk Policy Logic** (exposure limit, approve/reject, risk-increasing detection, kill switch scope). Đây là business logic hợp lệ của đúng responsibility đó.
- **Exchange Adapter** cũng là Type 3, nhưng chỉ làm venue I/O — không sở hữu domain policy nào.

**Nguyên tắc:** Module Taxonomy trả lời *"module này làm gì với dữ liệu"*; Responsibility Ownership ([Chapter 3 §3.1](./03-engineering-principles.md)) trả lời *"logic nghiệp vụ nào thuộc về module nào"*. Hai câu hỏi độc lập — không suy ra câu trả lời của câu này từ câu kia.

## 7.3 Ràng buộc riêng của Projection

Projection **không được ra quyết định nghiệp vụ và không được sinh fact mới**. Cụ thể:

- Được phép: fold/aggregate event theo type, tính giá trị dẫn xuất thuần túy từ event đã có (tổng, đếm, trạng thái hiện tại), rẽ nhánh theo loại event để cập nhật read-model.
- Không được phép: sinh ra một fact chưa từng tồn tại trong event log, ra quyết định ảnh hưởng tới Decision/Risk/Execution, hoặc trở thành authoritative source cho bất kỳ concept nào.

*(Lưu ý: quy tắc này KHÔNG cấm cấu trúc điều khiển `if/switch` — mọi projection đều cần chúng để fold theo event type. Điều bị cấm là **quyết định nghiệp vụ** và **sinh fact mới**, không phải cú pháp.)*

Theo [I-6 Fail-Safe by Scope](./02-platform-invariants.md), Projection không critical được phép degrade có kiểm soát mà không làm dừng toàn platform — vì nó không tham gia decision/risk/execution.

## 7.4 Thẩm quyền phân loại từng module cụ thể

Chapter 7 định nghĩa **3 loại module tồn tại**. Việc **module cụ thể nào thuộc loại nào** là registry, không phải nguyên tắc — thuộc Phase 0.2, ghi tại `/docs/domain/context-map.yaml` cùng chỗ với capability/context registry ([Chapter 4 §4.2](./04-domain-principles.md), authoritative source cho mọi registry của domain/implementation boundary). Constitution không liệt kê danh sách module cụ thể để tránh phải sửa Constitution mỗi khi thêm/tách module.

Reference pipeline (bản nháp định hướng, chưa phải kiến trúc chính thức) nằm tại [`/docs/architecture/README.md`](../architecture/README.md) — sẽ được chốt ở Phase 1 System Architecture.
