---
id: 05-time-model
title: Time Model
version: "2.0"
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

**Đối chiếu thuật ngữ với I-3 (Locked):** I-3 dùng cụm "`effective/event time`" và "`knowledge/recorded time`" — trong ngữ cảnh đó, "event time của candle là 10:00" nghĩa là **Effective Time** theo định nghĩa chương này. Chương này canonical hóa: dùng **Effective Time** và **Recorded Time** làm cặp thuật ngữ chính thức; các cách gọi trong I-3 là alias tương thích (effective/event → Effective; knowledge/recorded → Recorded), không mâu thuẫn.

## 5.2 Bốn mốc thời gian vận hành

Trên nền 2 trục ở trên, hệ thống ghi nhận 4 mốc cụ thể:

| Mốc | Định nghĩa | Thuộc trục |
|---|---|---|
| **Market Time** | Timestamp do sàn cung cấp — với dữ liệu có khoảng (candle), là thời điểm bắt đầu khoảng đó | Effective |
| **Event Time** | Thời điểm event được ghi vào durable event log nội bộ | Recorded |
| **Processing Time** | Thời điểm một engine xử lý xong event | Vận hành (không thuộc 2 trục, chỉ đo latency nội bộ) |
| **Replay Time** | Con trỏ thời gian giả lập khi replay | Recorded (xem 5.3) |

**Quy tắc:**
- Mọi event tối thiểu mang cả `market_time` và `event_time` (Dual Timestamping) — bắt buộc để phát hiện dữ liệu trễ/stale khi arbitrage đa sàn.
- Event ordering trong pipeline theo **Event Time** (recorded); **Market Time** dùng tính độ trễ và phát hiện stale data giữa các sàn.
- Không mốc nào ở trên được lấy từ đồng hồ hệ thống lúc đọc lại — tất cả là giá trị đã ghi bất biến trong event.

## 5.3 Ngữ nghĩa Replay (định nghĩa vận hành, không chỉ tên gọi)

Replay tại thời điểm T nghĩa là: **chỉ quan sát được các event có `event_time (recorded) ≤ T`** — bất kể effective time của chúng là gì.

Hệ quả trực tiếp (khớp ví dụ trong I-3): candle có effective time 10:00, correction được ghi lúc recorded time 10:07 → Replay tại 10:03 thấy candle gốc, KHÔNG thấy correction — dù correction "nói về" thời điểm 10:00 nằm trước con trỏ replay. Nhìn theo trục effective để quyết định visibility là look-ahead bias, bị cấm bởi I-3.

Replay dùng lại Event Time đã ghi trong log, không dùng đồng hồ hệ thống hiện tại (nhất quán [I-5](./02-platform-invariants.md): Replay execution không phụ thuộc nguồn ngoài).

## 5.4 Clock authority

`event_time` do component ghi event log cấp phát, là authoritative cho thứ tự nội bộ. Đồng hồ máy chủ phải được đồng bộ (NTP hoặc tương đương); độ lệch clock giữa các node là vấn đề vận hành cần giám sát nhưng **không** thay đổi nguyên tắc: một khi event đã ghi với `event_time`, giá trị đó bất biến và là căn cứ duy nhất cho ordering/replay — không "sửa lại cho đúng giờ thật" về sau (I-3).
