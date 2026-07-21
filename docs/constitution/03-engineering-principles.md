---
id: 03-engineering-principles
title: Engineering Principles
version: "1.1"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-18"
next_review: null
depends_on: ["02-platform-invariants"]
---

# 3. Engineering Principles

## 3.1 Phân bổ ngôn ngữ có kỷ luật

Quyết định chi tiết và lý do xem [ADR-008](../adr/ADR-008.md). Tóm tắt:

- **Python** = lõi logic nghiệp vụ (Feature Engineering, Strategy, Decision, Backtest) — vì cần giữ [I-2 Decision Parity](./02-platform-invariants.md): cùng một hàm chạy ở cả Research và Production.
- **Go** = biên hệ thống (Market Data Ingestion, Risk Gateway, Execution Engine) — nơi cần concurrency, I/O, độ tin cậy. Go **không được chứa logic nghiệp vụ**; nếu để lọt logic vào đây, Decision Parity sẽ bị phá vỡ ngầm.
- **Rust KHÔNG dùng ngay** — reserved cho critical path tương lai nếu latency profile thay đổi (hiện tại vài trăm ms không cần Rust). Đưa Rust vào là quyết định kiến trúc mới, cần ADR riêng.

**Lưu ý quan trọng — Parity không phụ thuộc ngôn ngữ, mà phụ thuộc code path:** Risk Gateway viết bằng Go (không phải Python) KHÔNG vi phạm I-2, **miễn** Backtest/Replay/Paper/Live đều gọi qua đúng **1 Risk Gateway service instance** — tuyệt đối không được viết một bản risk-check Python "rút gọn" riêng cho Backtest vì lý do tốc độ. Đây là lỗi kinh điển trong lịch sử hệ thống trading thật (risk model backtest lệch khỏi risk model production, dẫn đến kết quả backtest đẹp nhưng live thua lỗ vì risk check thật chặt hơn).

## 3.2 Engineering Foundation (tài liệu SỐNG, không bất biến)

Bao gồm: Monorepo structure, Coding Standard, Naming Convention, Logging Convention, Configuration Convention, Error Handling Convention, Versioning, Dependency Injection, Testing Convention, Documentation Convention, CI/CD Convention. Đây là danh sách khung — nội dung chi tiết từng mục được điền dần khi Phase 1.5 (Engineering Foundation) triển khai, không phải toàn bộ đã định nghĩa xong tại đây.

Quy ước naming mẫu:
- Event: `PAST_TENSE_UPPER_SNAKE` — ví dụ `SWING_CREATED`, `REGIME_UPDATED`, `DECISION_APPROVED`.
- Interface: `IStructureEngine`, `IRiskGateway`.
- DTO: `SwingDTO`, `DecisionDTO`.

**Tránh trùng lặp với chapter khác (theo I-12 Single Source of Truth):**
- **Testing Convention** ở đây chỉ quy định style/tooling (framework, cấu trúc test file, naming test case) — coverage/tier requirement đã có đầy đủ ở [13-quality-gates.md](./13-quality-gates.md), không định nghĩa lại.
- **Versioning** ở đây là quy ước chung cho code/package — SemVer cho Engine schema/capability đã có đầy đủ ở [10-compatibility-capability-contract.md](./10-compatibility-capability-contract.md), không định nghĩa lại.
- **Documentation Convention** chính là cấu trúc `/docs` này — metadata schema (owner/reviewers/status/version) và Document Lifecycle đã định nghĩa ở [Governance §7-9](./00-governance.md), không định nghĩa lại ở đây.

**Nguyên tắc bắt buộc:** Engineering Foundation **không có đặc quyền** miễn trừ khỏi ADR. Muốn sửa convention → phải có ADR mới, version tăng, không sửa ngầm.

## 3.3 Backlog

- Hiệu năng Backtest Engine (Python) ở quy mô dữ liệu lớn (nhiều năm lịch sử, nhiều strategy song song) — cân nhắc vectorization (Polars), song song hóa (Ray/Dask) khi cần. Chưa quyết định cụ thể, để ngỏ tới khi Phase 3/Phase 6 (Simulation Platform) có nhu cầu thực tế đo lường được.
