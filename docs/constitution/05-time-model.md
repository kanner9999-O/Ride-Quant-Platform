---
id: 05-time-model
title: Time Model
version: "2.4"
status: Locked
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: Product Owner
approved_at: "2026-07-18"
created_at: "2026-07-16"
last_review: "2026-07-18"
next_review: null
depends_on: ["04-domain-principles", "02-platform-invariants"]
---

# 5. Time Model

Toàn chapter thống nhất năm khái niệm: **Effective Time**, **Recorded Time**, **Ordering Authority**, **Causality**, **Replay Cursor**. Canonical field names chỉ gồm `effective_time`, `recorded_time`, `decision_time` (khi là Decision) — **không dùng `event_time`** làm field name (nó từng mang 2 nghĩa đối nghịch, đã loại bỏ).

## 5.1 Hai trục thời gian (Bitemporal Model)

Mọi dữ liệu thời gian phân biệt hai trục độc lập — nền tảng để [I-3 No Repaint/No Look-Ahead](./02-platform-invariants.md) kiểm chứng được:

| Trục (canonical field) | Định nghĩa | Trả lời câu hỏi |
|---|---|---|
| **Effective Time** (`effective_time`) | Thời điểm/khoảng thời gian mà dữ liệu MÔ TẢ về | "Dữ liệu này nói về lúc nào?" (candle khung 10:00 → effective_time = 10:00) |
| **Recorded Time** (`recorded_time`, còn gọi knowledge time) | Thời điểm hệ thống BIẾT ĐẾN dữ liệu đó (ghi vào durable event log) | "Hệ thống biết điều này từ khi nào?" (candle 10:00 ghi lúc 10:00:30 → recorded_time = 10:00:30) |

**Correction là event mới:** khi dữ liệu bị sửa (ví dụ sàn gửi correction cho candle 10:00 vào lúc 10:07), correction là event mới với `effective_time = 10:00`, `recorded_time = 10:07` — event gốc không bị sửa/xóa (I-3 append-only).

**Recorded time bất biến:** một khi event đã ghi với `recorded_time`, giá trị đó bất biến (I-3) — không "sửa lại cho đúng giờ thật" về sau, kể cả khi phát hiện clock lệch. Sửa nhận thức về thời gian = ghi correction event mới, không sửa `recorded_time` cũ.

**Đối chiếu với I-3 (Locked):** I-3 dùng cụm "`effective/event time`" và "`knowledge/recorded time`". "event time của candle là 10:00" trong I-3 nghĩa là **Effective Time** theo chương này. Ánh xạ alias tương thích (chỉ để đọc I-3, KHÔNG dùng làm field name): effective/event → `effective_time`; knowledge/recorded → `recorded_time`.

## 5.2 Các mốc thời gian

| Mốc (canonical) | Định nghĩa | Vai trò |
|---|---|---|
| **Market Time** (`market_time`) | Timestamp do sàn cung cấp; với dữ liệu có khoảng (candle) là thời điểm bắt đầu khoảng. Là một nguồn XÁC ĐỊNH `effective_time` cho market-data event | Effective axis. Chỉ có khi source cung cấp hoặc Domain Contract xác định được — không tạo giả |
| **Recorded Time** (`recorded_time`) | Thời điểm ghi vào durable event log | Recorded axis. Bắt buộc cho MỌI authoritative event |
| **Replay Cursor** | Vị trí giả lập khi replay (xem 5.3) — không phải mốc bitemporal của bản thân event, mà là simulation-control cursor | Điều khiển replay visibility |

**Processing Observation** (KHÔNG dùng cho ordering/replay/decision): quan sát vận hành về việc một processor xử lý event — gồm `processor`, `attempt`, `started_at`, `completed_at`. Là **per-attempt observation** (một event xử lý nhiều lần/nhiều processor sẽ có nhiều observation), không phải một timestamp duy nhất của event. Chỉ dùng đo latency/observability; cấm dùng cho ordering, replay visibility, hay decision logic (sẽ phá determinism I-2/I-3 vì thay đổi giữa các lần chạy).

**Quy tắc timestamp bắt buộc:**
- Mọi authoritative event có `recorded_time`.
- Market-data event có `market_time` KHI source cung cấp hoặc Domain Contract xác định được — không tạo `market_time` giả cho event phi thị trường (ví dụ DecisionApproved không có market_time).
- Không mốc nào được lấy từ đồng hồ hệ thống lúc đọc lại — tất cả là giá trị đã ghi bất biến trong event.
- Ordering trong pipeline theo **Ordering Authority** (§5.4), không dựa thuần physical timestamp.

## 5.3 Replay Cursor & Replay Semantics

**Replay visibility** (event nào được thấy) và **authoritative ordering** (thứ tự giữa các event) là hai câu hỏi khác nhau — không gộp:
- *Visibility* dựa trên **Recorded Time boundary**: replay tại cursor T chỉ thấy event có `recorded_time ≤ T`, bất kể effective time.
- *Ordering* giữa các event đã visible dựa trên **Ordering Authority** (§5.4), không phải so sánh `recorded_time` trực tiếp.

**Replay Cursor = Recorded Time boundary + opaque ordering position (khi cần).** Timestamp một mình không đủ khi nhiều event cùng `recorded_time` — cursor phải kèm một ordering position để cắt chính xác tại ranh giới giữa hai event cùng thời điểm. Representation cụ thể của ordering position (offset, sequence...) là quyết định của [Chapter 8](./08-event-model.md), không chốt ở đây.

Hệ quả (khớp ví dụ I-3): candle effective_time 10:00, correction recorded_time 10:07 → replay tại cursor 10:03 thấy candle gốc, KHÔNG thấy correction. Quyết định visibility theo effective time = look-ahead bias, cấm bởi I-3.

**Out-of-order arrival:** event có thể được ghi (recorded_time muộn) trong khi effective_time nằm trước nhiều event đã ghi trước đó (ví dụ fill trễ mạng). Replay visibility theo `recorded_time` — event đến sau chỉ thấy được ở đúng cursor position nó được ghi, không "chèn ngược" theo effective_time (chèn ngược = look-ahead, cấm I-3). Diễn giải lại chuỗi theo effective_time (nếu nghiệp vụ cần) là việc của consumer/projection tầng đọc.

Replay không dùng đồng hồ hệ thống hiện tại (nhất quán [I-5](./02-platform-invariants.md): Replay execution không phụ thuộc nguồn ngoài).

## 5.4 Ordering Authority & Clock

**Vấn đề:** `recorded_time` được sinh từ đồng hồ vật lý tại thời điểm ghi event. Ngay cả khi các node đồng bộ NTP, sai số vài mili-giây vẫn tồn tại — hai event gần nhau từ hai node khác nhau có thể có `recorded_time` không phản ánh đúng thứ tự thật. Với arbitrage đa sàn (use case cốt lõi của Ride), thứ tự sự kiện giữa hai sàn quyết định trực tiếp lãi/lỗ, nên **không được dựa thuần vào physical clock để quyết định thứ tự authoritative**.

**Nguyên tắc (contract — không chốt cơ chế). Phân biệt 2 mức bảo đảm:**

*Mức 1 — Intra-partition determinism (chống look-ahead, phục vụ I-3/Replay):*
- Ordering authoritative trong mỗi partition/stream phải là **total order deterministic** — replay cùng một log luôn cho cùng một thứ tự, không phụ thuộc physical clock lúc đọc lại.
- Đủ để Replay không bị look-ahead bias trong phạm vi 1 stream.

*Mức 2 — Cross-context causal correctness (đúng nhân quả liên sàn/liên stream, phục vụ decision đa nguồn):*
- Khi thứ tự giữa 2 stream quan trọng về nghiệp vụ (2 sàn trong 1 arbitrage decision), phải bảo toàn quan hệ **nhân quả** (nếu event B được tạo do đã quan sát event A, mọi nơi phải thấy A trước B) — không chỉ cần "một thứ tự cố định nào đó" như Mức 1.
- Total order deterministic (Mức 1) KHÔNG tự động cho causal correctness (Mức 2): có thể có thứ tự cố định nhưng SAI nhân quả nếu sắp theo physical timestamp giữa 2 node lệch clock.

**Nguyên tắc chung:**
- Physical `recorded_time` dùng đo latency, phát hiện stale/clock-skew, hiển thị — nhưng **không một mình** quyết định thứ tự authoritative.
- Cross-partition/cross-node causal ordering phải dựa cơ chế ordering deterministic bảo toàn nhân quả, không so sánh trực tiếp 2 physical timestamp.
- Clock skew giữa các node là vấn đề vận hành cần giám sát.

**Cơ chế cụ thể** (sequence number per partition, logical/Lamport clock, hybrid logical clock, hay kết hợp) và **representation của opaque ordering position** trong Replay Cursor (§5.3) là **quyết định của [Event Model — Chapter 8](./08-event-model.md)** — gắn với cấu trúc event log thật, không phải khái niệm thời gian. Xem OQ-005.
