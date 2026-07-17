---
id: 03-engineering-principles
title: Engineering Principles
version: "1.0"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-16"
next_review: null
depends_on: ["02-platform-invariants"]
---

# 3. Engineering Principles

## 3.1 Phân bổ ngôn ngữ có kỷ luật
- **Python** = lõi logic nghiệp vụ (Feature Engineering, Strategy, Backtest) — vì cần giữ [Parity Principle](./02-platform-invariants.md) (I-2): cùng một hàm chạy ở cả Research và Production.
- **Go** = biên hệ thống (Market Data Ingestion, Risk Gateway, Execution Engine) — nơi cần concurrency, I/O, độ tin cậy. Go/Rust **không được chứa logic nghiệp vụ**; nếu để lọt logic vào đây, Parity Principle sẽ bị phá vỡ ngầm.

## 3.2 Engineering Foundation (tài liệu SỐNG, không bất biến)
Bao gồm: Monorepo structure, Coding Standard, Naming Convention, Logging Convention, Configuration Convention, Error Handling Convention, Versioning (SemVer bắt buộc), Dependency Injection, Testing Convention, Documentation Convention (chính là cấu trúc `/docs` này), CI/CD Convention.

Quy ước naming mẫu:
- Event: `PAST_TENSE_UPPER_SNAKE` — ví dụ `SWING_CREATED`, `REGIME_UPDATED`, `DECISION_APPROVED`.
- Interface: `IStructureEngine`, `IRiskGateway`.
- DTO: `SwingDTO`, `DecisionDTO`.

**Nguyên tắc bắt buộc:** Engineering Foundation **không có đặc quyền** miễn trừ khỏi ADR. Muốn sửa convention → phải có ADR mới, version tăng, không sửa ngầm.
