---
id: 03-engineering-principles
title: Engineering Principles
version: "1.4"
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

## 3.1 One Authoritative Implementation per Business Capability

**Nguyên tắc:** Tại mỗi business capability và capability version phải có đúng một **authoritative implementation** được phép phát sinh authoritative output cho toàn bộ execution mode (Backtest, Replay, Paper Trading, Live). Alternative, experimental, shadow, hoặc migration implementation được phép tồn tại song song nhưng KHÔNG được phát sinh authoritative output cho đến khi vượt parity validation và được promote qua đúng quy trình governance.

- Đối với **Strategy/Decision capability**, yêu cầu này thực thi trực tiếp [I-2 Decision Parity](./02-platform-invariants.md).
- Đối với **Risk capability**, yêu cầu này bảo đảm Risk Policy authority, reproducibility, và explainability ([I-1](./02-platform-invariants.md)) — đây là yêu cầu **bổ sung của Chapter 3**, KHÔNG phải mở rộng phạm vi của I-2 (I-2 chỉ định nghĩa parity ở tầng Decision, không tự động bao gồm Risk Action — mở rộng phạm vi 1 invariant đã Locked cần ADR riêng, chưa làm ở đây).

**Phân chia theo responsibility ownership** (chưa dùng thuật ngữ "bounded context" — khái niệm này sẽ được canonical hóa chính thức ở Chapter 4 Domain Principles, hiện chưa Locked; dùng "capability/responsibility ownership" ở đây để tránh tạo dependency ngầm vào một chapter chưa có nội dung chính thức):
- Strategy/Decision logic → Decision Engine. Không được rò rỉ sang Market Data Ingestion, Risk Gateway, hay Execution Engine.
- Risk Policy logic (exposure limit, approve/reject, risk-increasing detection, kill switch scope) → Risk Gateway sở hữu và bắt buộc phải có — đây LÀ business logic hợp lệ của đúng responsibility này, không phải loại "logic nghiệp vụ" bị cấm khỏi biên hệ thống. Risk Gateway không được tái triển khai Strategy/Decision logic.
- Venue/execution behavior → Execution Engine/Adapter.

**Công nghệ/ngôn ngữ cụ thể hiện tại** (Python cho Strategy/Decision, Go cho Market Data Ingestion/Risk Gateway/Execution, Rust reserved) được ghi đầy đủ tại [ADR-008](../adr/ADR-008.md) — **không lặp lại ở đây** (theo tinh thần I-12: một quyết định công nghệ chỉ nên có 1 nơi ghi). Thay đổi công nghệ là một ADR mới, Principle ở mục này không cần đổi theo.

**Lưu ý quan trọng — đồng bộ version/config chỉ bắt buộc khi tuyên bố parity hoặc tái dựng cùng run identity:** Khi các execution mode được dùng để so sánh parity hoặc tái dựng cùng một run identity (ví dụ kiểm tra Backtest có khớp Live không), chúng phải pin cùng authoritative implementation version, configuration, policy version, và canonical contract, đã qua parity validation. Ngoài phạm vi đó, các experiment độc lập (canary version ở Paper, policy configuration mới thử ở Backtest, historical version tái dựng ở Replay...) được phép dùng version/configuration khác — miễn **không tuyên bố parity với Live baseline** khi identity không trùng. *Codebase* và *contract* không đồng nghĩa (2 implementation có thể cùng contract nhưng khác semantic bên trong) — khi thực sự cần parity, phải ghim đủ version + config + policy version + contract + parity validation, không chỉ "cùng contract". Không giới hạn số lượng instance/replica chạy — canonical ở đây nói về logic/version, hoàn toàn có thể horizontal scaling/HA với nhiều replica cùng 1 authoritative implementation.

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
