---
id: 09-plugin-model
title: Plugin Model
version: "2.0"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-18"
next_review: null
depends_on: ["02-platform-invariants", "07-module-taxonomy", "08-event-model"]
---

# 9. Plugin Model

## 9.1 Plugin là gì — và thuộc phạm vi Module Taxonomy

**Plugin** là một **extension module**: runtime application component được thêm vào platform sau, có published boundary rõ ràng, và **không** được mặc định trở thành thành phần nội bộ của Decision Pipeline ([I-7](./02-platform-invariants.md)).

**Plugin KHÔNG phải một loại artifact riêng nằm ngoài taxonomy.** Vì nó là runtime application component (đúng định nghĩa [Chapter 7 §7.0](./07-module-taxonomy.md)), mỗi plugin:
- phải có **một primary taxonomy type** trong 3 loại của Chapter 7 (Compute Engine / Projection / Runtime Service) — Strategy Plugin điển hình là **Compute Engine** (suy diễn domain information thành output, không sở hữu external side effect);
- được đăng ký trong **`/docs/architecture/module-registry.yaml`** cùng mọi module khác ([Chapter 7 §7.5](./07-module-taxonomy.md)).

**KHÔNG tạo plugin registry riêng** — làm vậy sẽ có hai nguồn cho cùng một sự thật "component nào tồn tại và thuộc loại gì" (vi phạm [I-12](./02-platform-invariants.md)).

## 9.2 Plugin tương tác qua published contract

Plugin **chỉ** được tương tác qua **published contract**: versioned event · query/read contract · command contract ([I-7](./02-platform-invariants.md)). Cấm gọi trực tiếp implementation nội bộ hoặc mutable state của module khác; cấm truy cập storage thuộc module khác.

**KHÔNG phát biểu plugin "mặc định là consumer của Event Bus":**
- Về **authority**: [Chapter 8 §8.1](./08-event-model.md) (Locked) khóa rằng transport/broker cụ thể KHÔNG phải source of truth — authority nằm ở durable append-only event log. Nói plugin "consume Event Bus" là mô tả plugin theo **transport**, không theo **contract**.
- Về **phạm vi**: I-7 đã được siết ở Chapter 7 review — không phải plugin nào cũng cần là event consumer; một plugin chỉ cần **query/read contract** là hợp lệ. Ép mọi plugin thành event-bus consumer là ràng buộc thừa.

## 9.3 Strategy = Plugin

Mỗi strategy là một plugin độc lập, mang metadata riêng: strategy-level philosophy · tham số · version.

**Thẩm quyền của metadata này:** nội dung và schema thuộc **Domain Contract / module-registry**, **KHÔNG hardcode tên file hay format cụ thể trong Constitution** (bài học lặp lại từ I-2 field list, I-13 state machine, ADR-008 ngôn ngữ: artifact cụ thể sống ở registry/ADR, Constitution giữ nguyên tắc). Chọn format cụ thể là quyết định thuộc diện **ADR Required** nếu ảnh hưởng nhiều module.

**Strategy-level philosophy KHÔNG được nâng thành Platform Invariant** — đây là ranh giới đã khóa ở [Chapter 2](./02-platform-invariants.md): triết lý của một chiến lược cụ thể thuộc về metadata của chính nó, không áp cho toàn platform.

## 9.4 Decision Advisor — plugin tham gia Decision Pipeline

Một plugin (kể cả AI module) muốn **tham gia Decision Pipeline** phải được khai báo và kiểm soát như **Strategy Plugin hoặc Decision Advisor** (I-7), và khi đó chịu **toàn bộ** ràng buộc đã Locked ở Chapter 8 + ADR-010:

| Ràng buộc | Nguồn |
|---|---|
| Không gọi trực tiếp Exchange API; mọi intent qua Risk Gateway | [I-4](./02-platform-invariants.md) |
| Event Decision phải khai báo `event_class: decision` trong Event Contract | [Ch8 §8.4](./08-event-model.md) |
| Bắt buộc mang `decision_time` (effective axis) — `effective_time` prohibited | [ADR-010](../adr/ADR-010.md) |
| Bắt buộc mang `decision_context_cursor` hợp lệ (đủ 5 field canonical) | [Ch8 §8.5.1](./08-event-model.md) |
| Tuân relational invariants, gồm `cursor.recorded_time ≤ DecisionEvent.recorded_time` | [Ch8 §8.5.2](./08-event-model.md) |
| Append-and-Revalidate khi có registry transition | [ADR-010 §2.6](../adr/ADR-010.md) |

**Không có ngoại lệ cho AI module.** Việc một plugin dùng mô hình học máy không thay đổi bất kỳ ràng buộc nào ở trên — [I-1](./02-platform-invariants.md) vẫn yêu cầu decision tái dựng được từ immutable evidence (gồm model/strategy version, configuration version).

## 9.5 Versioning & compatibility — thuộc Chapter 10

Mỗi plugin có version độc lập với platform version; cập nhật một plugin không ảnh hưởng plugin khác.

**Quy tắc versioning/compatibility cụ thể** (SemVer, `schemaVersion`, capability declaration, Capability Matrix, hành vi khi không khớp) **thuộc [Chapter 10](./10-compatibility-capability-contract.md)** — Chapter 9 chỉ tuyên bố *tính độc lập*, không định nghĩa lại cơ chế. *(Lưu ý dependency: Chapter 10 khai báo `depends_on: [09-plugin-model]`, nên Chapter 9 KHÔNG được tham chiếu ngược vào chi tiết của Chapter 10 để tránh vòng.)*

## 9.6 Plugin lifecycle

Đăng ký, kích hoạt, và gỡ bỏ plugin là thay đổi cấu trúc runtime → thuộc diện **ADR Required** ([Governance §4b](./00-governance.md)) khi ảnh hưởng nhiều module hoặc Decision Pipeline.

**Ràng buộc bắt buộc:** thay đổi version hoặc trạng thái của một plugin đang tham gia Decision Pipeline **không được làm mất evidence của Decision đã tính** — Decision đã tồn tại vẫn phải tái dựng được với đúng plugin version đã dùng (I-1). Protocol cụ thể (drain, activation boundary, in-flight handling) thuộc **Phase 1 design spec**; Constitution chỉ khóa yêu cầu bảo toàn evidence.
