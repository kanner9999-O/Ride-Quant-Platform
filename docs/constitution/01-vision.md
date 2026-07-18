---
id: 01-vision
title: Vision
version: "2.0"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-17"
next_review: null
depends_on: ["00-governance"]
supersedes_content_from: "v1.0 (bản mô tả ngắn, xem CHANGELOG)"
---

# 1. Vision

> Building the next generation of professional traders through an explainable, measurable and continuously improving trading process.

**Ride Quant Platform** ("Ride") là một nền tảng giao dịch định lượng — về bản chất là một **Trading Operating System** hỗ trợ toàn bộ vòng đời của một trader chuyên nghiệp: Research → Replay → Backtest → Paper Trading → Live Trading → Review → Improve.

## 1.1 Current Scope (Phase 0-3) — xem [ADR-007](../adr/ADR-007.md)

Để tránh mơ hồ khi bước vào Domain Model (Phase 0.2), phạm vi **giai đoạn hiện tại** được chốt rõ, tách biệt khỏi tầm nhìn dài hạn ở Mục 11:

| Trục | Phase 0-3 (hiện tại) | Dài hạn (5-10 năm, xem Mục 11) |
|---|---|---|
| **Đối tượng phục vụ** | Nội bộ — 1 team vận hành nhiều strategy trên vốn của chính mình. Không xây multi-tenant/RBAC ngay. | Có thể mở SaaS multi-tenant — kiến trúc đã chừa chỗ qua `Account` first-class (xem [06-identity-model.md](./06-identity-model.md)) |
| **Phạm vi tài sản** | Crypto only, 2-3 sàn (như đã chốt từ ADR-001~003) | Có thể đa tài sản (stock, forex...) — Domain Model không hardcode giả định crypto-only |

## 1.2 Why Ride Exists

Trading là một nghề đòi hỏi nhiều năm học hỏi, kỷ luật và cải thiện liên tục — không phải một lối tắt đến tự do tài chính. Phần lớn trader thất bại không vì thiếu thông minh hay nỗ lực, mà vì thiếu một quy trình vận hành chuyên nghiệp.

Workflow trading hiện nay bị phân mảnh qua nhiều công cụ rời rạc: Exchange, TradingView, Excel, Notes, Journal, Risk Calculator, Backtesting Software. Thông tin phân tán, quyết định khó review lại, quản lý rủi ro thiếu nhất quán, sai lầm lặp lại, hiệu suất không đo lường được khách quan. Theo thời gian, trading trở nên cảm tính thay vì hệ thống.

Ride tồn tại để giải quyết vấn đề này — không phải bằng cách đưa thêm 1 indicator hay 1 tín hiệu trading, mà bằng một workflow hoàn chỉnh giúp trader nghiên cứu, thực thi, review và liên tục cải thiện quá trình ra quyết định.

## 1.3 Product Positioning

Ride là một **Explainable Quant Trading Platform**, chiến lược-bất-khả-tri (strategy-agnostic) — hỗ trợ nhiều phương pháp giao dịch, thị trường và công nghệ tương lai mà không cần thay đổi nền tảng kiến trúc.

Ride ban đầu được thiết kế cho **cá nhân/1 team trader chuyên nghiệp** vận hành nhiều strategy trên vốn của chính mình — không phải sản phẩm SaaS đại chúng. Kiến trúc chủ đích được thiết kế để hỗ trợ multi-workspace/multi-tenant trong tương lai mà không cần redesign (xem [ADR-007](../adr/ADR-007.md)).

Ride ban đầu được xây dựng cho **thị trường Crypto**. Kiến trúc giữ tính asset-agnostic để mở rộng sang thị trường khác sau này (xem [ADR-007](../adr/ADR-007.md)).

## 1.4 Mission (What Ride does — khác với Vision ở trên là "Future State", và khác Long-term Vision ở Mục 1.11 là "Platform Evolution")

Ride giúp trader: học nhanh hơn, giảm thua lỗ do quy trình kém, ra quyết định giải thích được, quản lý rủi ro hệ thống, đo lường hiệu suất khách quan, cải thiện liên tục qua feedback có cấu trúc.

**Ride không hứa hẹn lợi nhuận.** Ride cung cấp hạ tầng cho phép cải thiện dài hạn.

## 1.5 Target Users (vai trò, KHÔNG phải nhóm khách hàng độc lập — xem 1.3)

Ride phục vụ những người xem trading là một nghề: Retail Trader, Professional Trader, Quant Researcher, Strategy Developer. Đây là các **vai trò/persona** dùng để định hướng thiết kế tính năng ("tính năng này phục vụ persona nào"), không phải các tenant/khách hàng độc lập cần cách ly hạ tầng — Target Users và Deployment Model là 2 khái niệm tách biệt (giống VSCode phục vụ nhiều loại developer nhưng không phải multi-tenant SaaS).

## 1.6 Core Beliefs

**Trading is a Profession** — quản lý như mọi ngành nghề chuyên nghiệp khác: process, discipline, risk management, journaling, measurement, review, continuous improvement.

**There is No Perfect Strategy** — không có chiến lược hoàn hảo, chỉ có chiến lược phù hợp nhất với từng trader, cần liên tục cải thiện.

**Continuous Improvement Over Prediction** — học nhanh quan trọng hơn đúng tạm thời. Mọi trade đều tạo ra tri thức: lệnh thắng cho tự tin, lệnh thua cho feedback.

## 1.7 Product Principles

Mọi tính năng thêm vào Ride phải phục vụ ít nhất 1 nguyên tắc dưới đây.

**Everything Must Be Explainable** — người dùng luôn hiểu được tại sao 1 vị thế tồn tại/đóng, context nào sinh ra quyết định, strategy/engine nào đóng góp. *(Đây là diễn giải giá trị/lý do của [I-1 Explainability](./02-platform-invariants.md) — định nghĩa kỹ thuật chính xác nằm ở Platform Invariants, không lặp lại ở đây theo I-12.)* Replay, Event Sourcing, Decision Log, Context Projection, Explainability Store tồn tại vì đúng 1 lý do: đảm bảo mọi quyết định quan trọng có thể tái dựng, review và hiểu được.

**Everything Must Be Reproducible** — cùng 1 quyết định phải cho cùng 1 kết quả bất kể execution mode (Replay/Backtest/Paper/Live), tất cả chạy qua cùng 1 decision pipeline. *(Đây chính là [I-2 Parity Principle](./02-platform-invariants.md).)*

**Everything Must Be Measurable** — mọi hành vi, quyết định, và kết quả trong Ride phải đo lường được khách quan (không chỉ mô tả định tính). Đây là nguyên tắc đối xứng với "Explainable" trong tagline mở đầu chương (Explainable, Measurable, Continuously Improving) — Replay, Journal, Risk, Review, Analytics, Backtest đều dựa trên khả năng đo lường được, không phải cảm nhận chủ quan.

**Research Before Capital** — mọi strategy phải được validate trước khi triển khai vốn thật. *(Khuyến nghị: nên chính thức hóa thành điều kiện bắt buộc trong Quality Gates — Capability Matrix phải xác nhận Backtest=YES và Paper Trade=YES trước khi 1 strategy được phép chuyển trạng thái Live; xem [13-quality-gates.md](./13-quality-gates.md) — cần ADR riêng khi định nghĩa Strategy Lifecycle ở Phase 0.2/Phase 3.)*

**Evidence Over Opinion** — ưu tiên bằng chứng đo lường được hơn ý kiến chủ quan khi có thể.

**Build Better Traders** — Ride tồn tại để cải thiện trader, không phải tăng tần suất giao dịch, không tối đa hóa screen time, không khuyến khích giao dịch cảm tính.

## 1.8 Success Definition & North Star

Ride thành công khi trader: hệ thống hóa hơn, cải thiện nhanh hơn, hiểu cả lệnh thắng lẫn thua, phụ thuộc cảm xúc ít hơn, xây tự tin qua bằng chứng thay vì trực giác.

**North Star:** giúp trader chuyên nghiệp hóa hơn qua một quy trình giao dịch giải thích được, đo lường được, và liên tục cải thiện.

## 1.9 Non-Goals

Ride không cố gắng: dự đoán tương lai, đánh bại thị trường, đảm bảo lợi nhuận, thay thế phán đoán của con người. Ride cải thiện chất lượng quyết định — trader vẫn chịu trách nhiệm cho quyết định đó.

## 1.10 Out of Scope

Ride chủ đích KHÔNG trở thành: Pump Signal Platform, Chat Room, Social Trading Network, Copy Trading Platform, Leaderboard Platform, AI Price Prediction Platform. Bất kỳ tính năng nào khuyến khích làm theo mù quáng thay vì hiểu biết đều bị từ chối.

## 1.11 Long-term Vision (5-10 năm — KHÁC với Current Scope ở Mục 1.1)

Trong 5-10 năm tới, Ride hướng tới trở thành nền tảng nền móng hỗ trợ toàn bộ vòng đời trading chuyên nghiệp. Strategy, sàn giao dịch, asset class và công nghệ mới nên tích hợp tự nhiên vào platform mà không cần thay đổi kiến trúc nền tảng — kể cả việc mở rộng sang **multi-tenant** (nhiều trader độc lập) và **đa tài sản** (ngoài crypto), miễn là không phải redesign từ đầu (xem ADR-007 cho cách kiến trúc hiện tại đã chừa chỗ cho việc này). Ride phát triển qua khả năng mở rộng (extensibility), không phải qua độ phức tạp.

## 1.12 Closing Statement

Ride không xây trader giỏi hơn bằng cách cho họ tín hiệu tốt hơn. Ride xây trader giỏi hơn bằng cách cho họ một quy trình tốt hơn — vì lợi nhuận bền vững là kết quả của quyết định kỷ luật, không phải dự đoán đơn lẻ.
