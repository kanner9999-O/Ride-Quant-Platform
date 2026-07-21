---
id: 03-engineering-principles
title: Engineering Principles
version: "1.2"
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

## 3.1 One Canonical Business Logic Implementation

**Nguyên tắc (không đổi theo công nghệ):** Mọi decision logic (Strategy, Feature Engineering, Decision Engine) phải có đúng **một implementation duy nhất**, dùng chung cho cả Research (Backtest/Replay/Paper) và Production (Live) — đây là hệ quả trực tiếp của [I-2 Decision Parity](./02-platform-invariants.md). Biên hệ thống (Market Data Ingestion, Risk Gateway, Execution Engine) cần concurrency/I/O/độ tin cậy, nhưng **không được chứa logic nghiệp vụ** — nếu để lọt logic vào đây, Decision Parity sẽ bị phá vỡ ngầm.

**Công nghệ/ngôn ngữ cụ thể hiện tại** (Python cho lõi logic, Go cho biên hệ thống, Rust reserved) được ghi đầy đủ tại [ADR-008](../adr/ADR-008.md) — **không lặp lại ở đây** (theo tinh thần I-12 Single Source of Truth: một quyết định công nghệ chỉ nên có 1 nơi ghi, tránh 2 tài liệu cùng nói 1 điều rồi lệch nhau khi đổi). Thay đổi công nghệ là một ADR mới, Principle ở mục này không cần đổi theo.

**Lưu ý quan trọng — Parity phụ thuộc canonical implementation, không phụ thuộc số lượng instance chạy:** Risk Gateway phải dùng **cùng một canonical implementation (Risk Decision Contract)** cho Backtest/Replay/Paper/Live — tuyệt đối không được viết một bản risk-check "rút gọn" riêng cho Backtest vì lý do tốc độ (lỗi kinh điển trong lịch sử hệ thống trading thật: risk model backtest lệch khỏi risk model production). Điều này **không có nghĩa là chỉ được chạy đúng 1 process/instance** — canonical implementation hoàn toàn có thể chạy dưới nhiều replica (horizontal scaling, HA) miễn tất cả replica cùng chạy chung 1 codebase/contract, không phải 2 implementation khác nhau cùng "tự nhận" là tương thích.

## 3.2 Engineering Foundation (tài liệu SỐNG, không bất biến)

Bao gồm: Monorepo structure, Coding Standard, Naming Convention, Logging Convention, Configuration Convention, Error Handling Convention, Versioning, Dependency Injection, Testing Convention, Documentation Convention, CI/CD Convention. Đây là danh sách khung — nội dung chi tiết từng mục được điền dần khi Phase 1.5 (Engineering Foundation) triển khai, không phải toàn bộ đã định nghĩa xong tại đây.

Quy ước naming mẫu (trừu tượng, không domain-specific):
- Event: `PAST_TENSE_UPPER_SNAKE` — ví dụ `ENTITY_CREATED`, `ORDER_FILLED`, `POSITION_CLOSED`.
- Interface: `IStructureEngine`, `IRiskGateway`.
- DTO: `SwingDTO`, `DecisionDTO`.

**Tránh trùng lặp với chapter khác (theo I-12 Single Source of Truth):**
- **Testing Convention** ở đây chỉ quy định style/tooling (framework, cấu trúc test file, naming test case) — coverage/tier requirement đã có đầy đủ ở [13-quality-gates.md](./13-quality-gates.md), không định nghĩa lại.
- **Versioning** ở đây là quy ước chung cho code/package — SemVer cho Engine schema/capability đã có đầy đủ ở [10-compatibility-capability-contract.md](./10-compatibility-capability-contract.md), không định nghĩa lại.
- **Documentation Convention** chính là cấu trúc `/docs` này — metadata schema (owner/reviewers/status/version) và Document Lifecycle đã định nghĩa ở [Governance §7-9](./00-governance.md), không định nghĩa lại ở đây.

**Nguyên tắc bắt buộc:** Engineering Foundation **không có đặc quyền** miễn trừ khỏi ADR. Muốn sửa convention → phải có ADR mới, version tăng, không sửa ngầm.

## 3.3 Backlog

- Hiệu năng Backtest Engine ở quy mô dữ liệu lớn (nhiều năm lịch sử, nhiều strategy song song): cần benchmark/profiling thực tế trước để xác định bottleneck cụ thể, sau đó mới đánh giá candidate technology phù hợp — chưa quyết định giải pháp, tránh chọn công nghệ trước khi đo vấn đề thật.
