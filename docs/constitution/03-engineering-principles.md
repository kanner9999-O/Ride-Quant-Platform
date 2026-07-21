---
id: 03-engineering-principles
title: Engineering Principles
version: "1.3"
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

## 3.1 One Canonical Business Logic Implementation (theo từng bounded context)

**Nguyên tắc:** Trong mỗi bounded context nghiệp vụ, tại mỗi capability/version phải có đúng **một authoritative implementation** được phép phát sinh Decision/Risk quyết định chính thức cho toàn bộ execution mode (Backtest, Replay, Paper Trading, Live) — hệ quả trực tiếp của [I-2 Decision Parity](./02-platform-invariants.md). Alternative, experimental, shadow, hoặc migration implementation được phép tồn tại song song nhưng KHÔNG được phát sinh authoritative Decision cho đến khi vượt parity validation và được promote qua đúng quy trình governance.

**Phân chia trách nhiệm theo bounded context (không phải "business logic chỉ được ở 1 nơi"):**
- Strategy/Decision domain logic → Decision Engine. Không được rò rỉ sang Market Data Ingestion, Risk Gateway, hay Execution Engine.
- Risk Policy logic (exposure limit, approve/reject, risk-increasing detection, kill switch scope) → Risk Gateway **sở hữu và bắt buộc phải có** — đây LÀ business logic hợp lệ của đúng bounded context này, không phải loại "logic nghiệp vụ" bị cấm khỏi biên hệ thống. Risk Gateway không được tái triển khai Strategy/Decision logic.
- Venue/execution behavior → Execution Engine/Adapter.

**Công nghệ/ngôn ngữ cụ thể hiện tại** (Python cho Strategy/Decision, Go cho Market Data Ingestion/Risk Gateway/Execution, Rust reserved) được ghi đầy đủ tại [ADR-008](../adr/ADR-008.md) — **không lặp lại ở đây** (theo tinh thần I-12: một quyết định công nghệ chỉ nên có 1 nơi ghi). Thay đổi công nghệ là một ADR mới, Principle ở mục này không cần đổi theo.

**Lưu ý quan trọng — Parity phụ thuộc authoritative implementation, không phụ thuộc số lượng instance:** Risk Gateway phải dùng cùng **authoritative implementation version + configuration + policy version + canonical contract**, đã qua parity validation, cho mọi execution mode — *codebase* và *contract* không đồng nghĩa (2 implementation có thể cùng contract nhưng khác semantic bên trong), nên cần ghim đủ cả version lẫn parity validation, không chỉ "cùng contract". Tuyệt đối không viết một bản risk-check "rút gọn" song song mà không qua parity validation trước (lỗi kinh điển trong lịch sử hệ thống trading thật). Điều này **không giới hạn số lượng instance/replica** chạy — canonical ở đây nói về logic/version, hoàn toàn có thể horizontal scaling/HA với nhiều replica cùng 1 authoritative implementation.

## 3.2 Engineering Foundation (tài liệu SỐNG, không bất biến)

Bao gồm: Monorepo structure, Coding Standard, Naming Convention, Logging Convention, Configuration Convention, Error Handling Convention, Versioning, Dependency Injection, Testing Convention, Documentation Convention, CI/CD Convention. Đây là danh sách khung — nội dung chi tiết từng mục được điền dần khi Phase 1.5 (Engineering Foundation) triển khai, không phải toàn bộ đã định nghĩa xong tại đây.

Quy ước naming mẫu (minh họa cụ thể cho Ride, không phải canonical domain vocabulary bắt buộc):
- Event: `PAST_TENSE_UPPER_SNAKE` — ví dụ `ORDER_FILLED`, `POSITION_CLOSED`.
- Interface: `IStructureEngine`, `IRiskGateway`.
- DTO: `SwingDTO`, `DecisionDTO`.

**Tránh trùng lặp với chapter khác (theo I-12 Single Source of Truth):**
- **Testing Convention** ở đây chỉ quy định style/tooling (framework, cấu trúc test file, naming test case) — coverage/tier requirement đã có đầy đủ ở [13-quality-gates.md](./13-quality-gates.md), không định nghĩa lại.
- **Versioning** ở đây là quy ước chung cho code/package — SemVer cho Engine schema/capability đã có đầy đủ ở [10-compatibility-capability-contract.md](./10-compatibility-capability-contract.md), không định nghĩa lại.
- **Documentation Convention** chính là cấu trúc `/docs` này — metadata schema (owner/reviewers/status/version) và Document Lifecycle đã định nghĩa ở [Governance §7-9](./00-governance.md), không định nghĩa lại ở đây.

**Nguyên tắc bắt buộc:** Engineering Foundation **không được miễn trừ khỏi Governance và ADR Scope Rule** ([Chapter 0 §4b](./00-governance.md)). Mọi thay đổi convention phải version hóa và review theo đúng mức ảnh hưởng đã phân loại ở đó — ADR chỉ bắt buộc khi thay đổi thuộc diện **ADR Required**; thay đổi **ADR Optional**/**ADR Not Required** (refactor không đổi behavior/contract, sửa lỗi chính tả/formatting...) không cần ADR nhưng vẫn phải để lại lịch sử thay đổi rõ ràng (commit message, CHANGELOG) — không sửa ngầm hoàn toàn không dấu vết.

## 3.3 Backlog

- Hiệu năng Backtest Engine ở quy mô dữ liệu lớn (nhiều năm lịch sử, nhiều strategy song song): cần benchmark/profiling thực tế trước để xác định bottleneck cụ thể, sau đó mới đánh giá candidate technology phù hợp — chưa quyết định giải pháp, tránh chọn công nghệ trước khi đo vấn đề thật.
