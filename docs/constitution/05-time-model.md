---
id: 05-time-model
title: Time Model
version: "2.3"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-18"
next_review: null
depends_on: ["04-domain-principles", "02-platform-invariants"]
---

# 5. Time Model

## 5.1 Hai trục thời gian (Bitemporal Model)

Mọi dữ liệu thời gian trong hệ thống phân biệt hai trục độc lập — đây là nền tảng để [I-3 No Repaint/No Look-Ahead](./02-platform-invariants.md) kiểm chứng được:

| Trục | Định nghĩa | Trả lời câu hỏi |
|---|---|---|
| **Effective Time** | Thời điểm/khoảng thời gian mà dữ liệu MÔ TẢ về | "Dữ liệu này nói về lúc nào?" (candle khung 10:00 → effective time = 10:00) |
| **Recorded Time** (knowledge time) | Thời điểm hệ thống BIẾT ĐẾN dữ liệu đó (ghi vào event log) | "Hệ thống biết điều này từ khi nào?" (candle 10:00 publish lúc 10:00:30 → recorded time = 10:00:30) |

**Correction là event mới:** khi dữ liệu bị sửa (ví dụ sàn gửi correction cho candle 10:00 vào lúc 10:07), correction là một event mới với `effective_time = 10:00` nhưng `recorded_time = 10:07` — event gốc không bị sửa/xóa (nhất quán I-3 append-only).

**Recorded time bất biến:** một khi event đã ghi với `recorded_time` (event_time), giá trị đó bất biến (I-3) — không "sửa lại cho đúng giờ thật" về sau, kể cả khi phát hiện clock lệch. Sửa nhận thức về thời gian = ghi event correction mới, không sửa recorded_time cũ.

**Đối chiếu thuật ngữ với I-3 (Locked):** I-3 dùng cụm "`effective/event time`" và "`knowledge/recorded time`" — trong ngữ cảnh đó, "event time của candle là 10:00" nghĩa là **Effective Time** theo định nghĩa chương này. Chương này canonical hóa: dùng **Effective Time** và **Recorded Time** làm cặp thuật ngữ chính thức; các cách gọi trong I-3 là alias tương thích (effective/event → Effective; knowledge/recorded → Recorded), không mâu thuẫn.

## 5.2 Bốn mốc thời gian vận hành

Trên nền 2 trục ở trên, hệ thống ghi nhận các mốc cụ thể. Ba mốc đầu thuộc bitemporal model (dùng cho ordering, replay, decision); Processing Time là **operational observability metadata** — tách riêng vì nó KHÔNG bao giờ được dùng cho ordering, replay visibility, hay decision logic (nếu dùng sẽ phá determinism của I-2/I-3, vì processing time thay đổi giữa các lần chạy lại).

**Mốc bitemporal (authoritative cho ordering/replay/decision):**

| Mốc | Định nghĩa | Thuộc trục |
|---|---|---|
| **Market Time** | Timestamp do sàn cung cấp — với dữ liệu có khoảng (candle), là thời điểm bắt đầu khoảng đó. Có thể vắng mặt hoặc không đáng tin với một số nguồn (derived data nội bộ, sàn không gửi timestamp, clock sàn lệch) — khi đó Effective Time được xác định theo policy khai báo trong Domain Contract của nguồn đó, không mặc định luôn có Market Time | Effective |
| **Event Time** | Thời điểm event được ghi vào durable event log nội bộ | Recorded |
| **Replay Time** | Con trỏ thời gian giả lập khi replay | Recorded (xem 5.3) |

**Mốc vận hành (KHÔNG dùng cho ordering/replay/decision):**

| Mốc | Định nghĩa | Mục đích |
|---|---|---|
| **Processing Time** | Thời điểm một engine xử lý xong event | Chỉ để đo latency/observability nội bộ. Cấm dùng cho ordering, replay visibility, hoặc bất kỳ decision logic nào. |

**Quy tắc:**
- Mọi event tối thiểu mang cả `market_time` và `event_time` (Dual Timestamping) — bắt buộc để phát hiện dữ liệu trễ/stale khi arbitrage đa sàn.
- Event ordering trong pipeline theo **ordering authority** (xem §5.4 — không dựa thuần physical `event_time`); **Market Time** dùng tính độ trễ và phát hiện stale data giữa các sàn.
- Không mốc nào ở trên được lấy từ đồng hồ hệ thống lúc đọc lại — tất cả là giá trị đã ghi bất biến trong event.

## 5.3 Ngữ nghĩa Replay (định nghĩa vận hành, không chỉ tên gọi)

Replay tại thời điểm T nghĩa là: **chỉ quan sát được các event có `event_time (recorded) ≤ T`** — bất kể effective time của chúng là gì.

Hệ quả trực tiếp (khớp ví dụ trong I-3): candle có effective time 10:00, correction được ghi lúc recorded time 10:07 → Replay tại 10:03 thấy candle gốc, KHÔNG thấy correction — dù correction "nói về" thời điểm 10:00 nằm trước con trỏ replay. Nhìn theo trục effective để quyết định visibility là look-ahead bias, bị cấm bởi I-3.

Replay dùng lại Event Time đã ghi trong log, không dùng đồng hồ hệ thống hiện tại (nhất quán [I-5](./02-platform-invariants.md): Replay execution không phụ thuộc nguồn ngoài).

**Out-of-order arrival:** một event có thể đến và được ghi (recorded time muộn) trong khi effective time của nó nằm trước nhiều event đã ghi trước đó (ví dụ: fill từ sàn bị trễ mạng, đến sau nhưng mô tả thời điểm sớm hơn). Ordering và replay visibility luôn theo **recorded time (event_time)** — event đến sau thì replay chỉ thấy nó ở đúng thời điểm nó được ghi, không "chèn ngược" vào quá khứ theo effective time (chèn ngược = look-ahead bias, cấm bởi I-3). Việc diễn giải lại chuỗi sự kiện theo effective time (nếu nghiệp vụ cần) là trách nhiệm của consumer/projection tại tầng đọc, không phải của ordering trong event log.

## 5.4 Ordering Authority & Clock

**Vấn đề:** `event_time` được sinh ra từ một đồng hồ vật lý tại thời điểm ghi event. Ngay cả khi các node được đồng bộ NTP, sai số vài mili-giây vẫn tồn tại — nghĩa là hai event gần nhau từ hai node khác nhau có thể có `event_time` không phản ánh đúng thứ tự thật. Với arbitrage đa sàn (use case cốt lõi của Ride), thứ tự sự kiện giữa hai sàn quyết định trực tiếp lãi/lỗ, nên **không được dựa thuần vào physical clock để quyết định thứ tự authoritative**.

**Nguyên tắc (contract — không chốt cơ chế). Phân biệt 2 mức bảo đảm khác nhau:**

*Mức 1 — Intra-partition determinism (chống look-ahead, phục vụ I-3/Replay):*
- Ordering authoritative trong mỗi partition/stream phải là **total order deterministic** — replay cùng một log luôn cho cùng một thứ tự, không phụ thuộc physical clock lúc đọc lại.
- Đây là điều kiện đủ để Replay không bị look-ahead bias trong phạm vi 1 stream.

*Mức 2 — Cross-context causal correctness (đúng nhân quả liên sàn/liên stream, phục vụ decision đa nguồn):*
- Khi thứ tự giữa 2 stream thực sự quan trọng về nghiệp vụ (ví dụ 2 sàn trong 1 arbitrage decision), hệ thống phải bảo toàn quan hệ **nhân quả** (nếu event B được tạo ra do đã quan sát event A, thì mọi nơi phải thấy A trước B) — không phải chỉ cần "một thứ tự cố định nào đó" như Mức 1.
- Total order deterministic (Mức 1) KHÔNG tự động cho ra causal correctness (Mức 2): có thể có một thứ tự cố định nhưng SAI về nhân quả nếu chỉ sắp theo physical timestamp giữa 2 node lệch clock.

**Nguyên tắc chung cho cả 2 mức:**
- Physical `event_time` dùng để đo latency, phát hiện stale/clock-skew, và hiển thị — nhưng **không phải một mình nó** quyết định thứ tự authoritative giữa các event.
- Cross-partition/cross-node causal ordering phải dựa trên cơ chế ordering deterministic bảo toàn nhân quả, không phải so sánh trực tiếp 2 physical timestamp.
- Clock skew giữa các node là vấn đề vận hành cần giám sát.

**Cơ chế cụ thể** (sequence number per partition, logical/Lamport clock, hybrid logical clock, hay kết hợp) là **quyết định kiến trúc của [Event Model — Chapter 8](./08-event-model.md)**, không chốt tại Time Model — vì nó gắn với cấu trúc event log thật, không phải khái niệm thời gian. Xem OQ-005.
