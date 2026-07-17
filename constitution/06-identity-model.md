---
id: 06-identity-model
title: Identity Model
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

# 6. Identity Model

Mọi entity miền đều có ID bất biến: `SwingID`, `StructureID`, `RegimeID`, `FeatureID`, `DecisionID`, `PositionID`, `OrderID`, `ExecutionID`, `StrategyInstanceID`...

**Quy tắc:**
- ID dạng sortable theo thời gian (ví dụ ULID), tránh đụng độ giữa các service phân tán.
- ID **không bao giờ tái sử dụng hoặc sửa**. Một phiên bản mới của entity = một ID mới, có field liên kết ngược (ví dụ `invalidates: <SwingID cũ>`).
- Đây là nền tảng bắt buộc để [Explainability](./02-platform-invariants.md) (I-1) khả thi trên thực tế.
