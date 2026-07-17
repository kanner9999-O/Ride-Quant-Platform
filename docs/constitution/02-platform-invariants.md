---
id: 02-platform-invariants
title: Platform Invariants
version: "1.0"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-16"
next_review: null
depends_on: ["00-governance", "01-vision"]
---

# 2. Platform Invariants (Bất biến — áp dụng cho MỌI chiến lược, không thương lượng)

Đây là ranh giới quan trọng nhất của toàn bộ Constitution: **Platform Invariants khác với Strategy-level Philosophy.** Platform Invariants áp dụng cho toàn hệ thống, không phụ thuộc trường phái chiến lược nào. Triết lý của một chiến lược cụ thể (ví dụ "giữ vị thế đến khi bị vô hiệu hóa thay vì TP cố định" của Ride Negation Strategy) **không được** đưa vào đây — nó thuộc về `strategy.json`/metadata của riêng chiến lược đó, vì các chiến lược khác (market making, arbitrage) có thể mâu thuẫn với nó.

| # | Invariant | Diễn giải |
|---|---|---|
| I-1 | **Explainability** | Mọi quyết định giao dịch phải truy vết được ngược lại đến: dữ liệu đầu vào, phiên bản model/strategy, feature snapshot — tại đúng thời điểm nó xảy ra, không phải suy luận lại sau. |
| I-2 | **Parity Principle** | Live, Replay, và Backtest phải chạy qua **cùng một Event Pipeline** và cùng logic code. Không được có hai codebase logic khác nhau cho research và production. |
| I-3 | **No Repaint** | Một sự kiện (Swing, Structure, Signal...) một khi đã publish thì bất biến. Thay đổi trạng thái phải thông qua một event mới (ví dụ `Invalidated`), không được sửa/ghi đè event cũ. |
| I-4 | **Strategy Isolation** | Strategy/Decision Engine không bao giờ được gọi trực tiếp Exchange API. Mọi trade intent phải đi qua Risk Gateway trước khi tới Execution. |
| I-5 | **External Decision Dependency phải Event-Sourced** | Bất kỳ dữ liệu bên ngoài nào mutable-theo-thời-gian và được dùng để ra quyết định (funding rate, sentiment, news score, output của LLM Decision Advisor...) đều phải được ghi thành một event bất biến tại thời điểm capture (`FundingSnapshotCaptured`, `LLMDecisionGenerated`...). Replay chỉ đọc lại event đã lưu, **không bao giờ** gọi lại nguồn dữ liệu bên ngoài. |
| I-6 | **Fail-Safe Default** | Khi một engine gặp lỗi, hệ thống mặc định dừng an toàn (fail-safe), không tiếp tục chạy với dữ liệu/trạng thái không chắc chắn (fail-open). |
| I-7 | **Plugin Non-Bypass** | Mọi module mới (kể cả AI Assistant tương lai) mặc định là một consumer của Event Bus. Nếu module đó muốn tham gia vào Decision Pipeline, nó phải được xây dựng như một Strategy Plugin / Decision Advisor — tuân theo Risk Gateway như mọi strategy khác, không được truy cập trực tiếp Core Engine hay Exchange. |
| I-8 | **Kill Switch / Circuit Breaker** | Hệ thống phải luôn có khả năng dừng khẩn cấp — cả toàn platform lẫn theo từng sàn riêng lẻ (per-exchange), thủ công lẫn tự động. Circuit breaker của một sàn kích hoạt không được ảnh hưởng tới các sàn khác đang hoạt động bình thường. |
| I-9 | **Numerical Precision** | Mọi giá trị tiền tệ và số lượng phải dùng biểu diễn fixed-point/decimal, **không bao giờ** dùng floating point. |
| I-10 | **Idempotent Execution** | Mọi lệnh gửi tới Exchange phải mang một idempotency key duy nhất. Retry không bao giờ được phép tạo ra lệnh trùng lặp trên sàn thật. |
| I-11 | **Secrets & Custody Isolation** | API key, secret, private key không bao giờ được lưu dạng plaintext (bắt buộc qua Vault/KMS). Strategy/Decision Engine **không bao giờ** được cấp quyền truy cập trực tiếp secret của sàn — chỉ Execution Engine/Exchange Adapter mới có quyền này (least privilege). |
| I-12 | **Single Source of Truth** | Mỗi khái niệm (dữ liệu, trạng thái, quyết định, tài liệu) chỉ có đúng **một** nguồn sự thật. Mọi nơi khác chỉ tham chiếu, không duplicate. Áp dụng cả tầng runtime (Event Bus — I-2/Event Model) lẫn tầng tài liệu (Manifest, Decision Log, Domain Model/Glossary). |
