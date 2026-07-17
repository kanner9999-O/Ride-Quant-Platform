---
id: 01-vision
title: Vision
version: "1.0"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-16"
next_review: null
depends_on: ["00-governance"]
---

# 1. Vision

Ride Quant Platform là một nền tảng giao dịch định lượng (quant trading platform) cho thị trường Crypto, trong đó toàn bộ chuỗi giá trị — **dữ liệu thị trường → phân tích → ra quyết định → quản lý rủi ro → thực thi → nghiên cứu** — được mô-đun hóa, giải thích được (Explainable), và có khả năng sống và mở rộng trong 5–10 năm.

**Đặc điểm phạm vi đã xác nhận:**
- Đa chiến lược (multi-strategy): arbitrage, market making, trend-following, và các trường phái khác được thêm vào sau này qua cơ chế plugin — không giả định trước một trường phái duy nhất.
- Đa sàn (2–3 sàn lớn ban đầu), có tiềm năng cross-exchange arbitrage.
- Yêu cầu độ trễ: hàng chục–hàng trăm mili-giây (không phải HFT sub-millisecond).
- Đội ngũ kỹ thuật: Python + Go/Rust hỗn hợp.
- Đây là một **Trading Workstation** (như Bloomberg Terminal hay VSCode cho developer), không phải một backend có giao diện gắn thêm — trải nghiệm người dùng, mô hình miền (domain model), và kiến trúc ảnh hưởng lẫn nhau ngay từ đầu.
