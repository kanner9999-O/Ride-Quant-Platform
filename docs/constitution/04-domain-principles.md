---
id: 04-domain-principles
title: Domain Principles
version: "2.4"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-18"
next_review: null
depends_on: ["02-platform-invariants", "03-engineering-principles"]
---

# 4. Domain Principles

## 4.1 Ubiquitous Language (nhất quán trong context, không toàn cục)

Trong mỗi **Domain Context**, một thuật ngữ phải có đúng một nghĩa canonical. Cùng một lexical term được phép mang semantic khác nhau giữa các Domain Context, nhưng phải được namespace rõ ràng và mô tả trong Context Map.

Ví dụ hợp lệ (cùng từ, khác nghĩa theo context):
- `Position` trong Execution Context = trạng thái venue/order-fill; `Position` trong Portfolio Context = exposure tổng hợp.
- `Signal` trong Strategy Context = analytical recommendation; không được mặc định hiểu là executable order ở Execution Context.

```yaml
term: Position
context: Portfolio
canonical_name: PortfolioPosition
```

**Quy tắc contract giữa các context:** published contract phải dùng tên và semantic không mơ hồ; consumer không được mặc định coi internal model của provider là internal model của chính mình. Đây là điều ngăn hệ thống trượt dần thành một global shared domain model (khiến các capability mất tính độc lập, đổi 1 concept kéo theo toàn hệ thống).

## 4.2 Context Map (authoritative artifact)

Context Map là authoritative record cho **cả identity/definition lẫn quan hệ** của Domain Context và Business Capability — nơi duy nhất giải quyết semantic collision (theo [I-12](./02-platform-invariants.md): identity và relationship của context/capability chỉ tồn tại ở 1 nơi, không rải rác trong từng Domain Contract).

**Authoritative source:** `/docs/domain/context-map.yaml` (một file duy nhất). Sở hữu 3 phần:

1. **Capability registry** — định nghĩa mỗi Business Capability (id, title, responsibility, status).
2. **Context registry** — định nghĩa mỗi Domain Context (id, title, capability_id nó thuộc về, responsibility, owned_contracts, status).
3. **Relationship map** — quan hệ giữa các context, direction theo từng contract edge.

```yaml
capabilities:
  - id: market-structure
    title: Market Structure
    responsibility: "Produce authoritative market-structure interpretation."
    status: active                # active | deprecated | superseded

contexts:
  - id: market-structure-analysis
    title: Market Structure Analysis
    capability_id: market-structure
    responsibility: "Define Swing, BOS, CHoCH and related structure semantics."
    owned_contracts: [swing, break-of-structure]
    status: active

relationships:
  - provider_context_id: execution
    consumer_context_id: portfolio
    contract_id: ExecutionFill.v1
    relationship_type: published_language     # direction theo message/contract flow
    status: active                            # active | deprecated | superseded — nhất quán với capability/context
    semantic_mappings:
      ExecutionPosition: PortfolioPosition
    translation_policy: anti_corruption_layer
    # model_influence (DDD upstream/downstream) khai báo RIÊNG khi cần —
    # message flow direction ≠ model influence direction:
    model_influence:
      upstream_context_id: execution
      downstream_context_id: portfolio
```

**Nguyên tắc bắt buộc:** mọi `capability_id` và `domain_context_id` dùng trong bất kỳ Domain Contract nào phải **tồn tại sẵn trong registry** của Context Map. Domain Contract KHÔNG được tự định nghĩa capability/context mới chỉ bằng cách ghi một ID chưa đăng ký. Internal model của một context không tự động trở thành model của context khác — mọi semantic translation phải khai báo tại Context Map hoặc contract mà nó tham chiếu.

Phân chia authority rõ ràng:
```
Capability/Context identity + boundary  → context-map.yaml (registry)
Cross-context relationship              → context-map.yaml (relationships)
Domain concept semantics                → Domain Contract (/docs/domain/<concept>.md)
Runtime facts                           → event log
```

(Chưa bắt buộc dùng đầy đủ jargon DDD như Customer/Supplier, Conformist, Shared Kernel ngay bây giờ — nhưng artifact và authority phải rõ trước khi bắt đầu tạo `/docs/domain/`.)

## 4.3 Domain Contract (thuật ngữ canonical — không dùng "Domain Model" song song)

Mỗi khái niệm miền có một Domain Contract. Vì domain concept có nhiều loại (entity, value object, policy, domain service, command, event, read model...), template dùng field `kind` và phân biệt required/conditional thay vì ép mọi concept cùng cấu trúc:

```yaml
id: swing
kind: entity                # entity | value_object | policy | domain_service | command | event | read_model
capability_id: market-structure          # stable machine-readable ID, KHÔNG phải display name
domain_context_id: market-structure-analysis  # stable ID — display title đổi được mà không hỏng references

description: "..."
invariants: []              # required cho mọi kind

schema: {}                  # required KHI concept có data representation (entity/value_object/event/command/read_model); khai báo type/precision cho giá trị tài chính (I-9: decimal/fixed-point, không float)
# Với kind = policy | domain_service, thay schema bằng:
inputs: []                  # khi có
outputs: []                 # khi có
preconditions: []           # khi có
postconditions: []          # khi có

state_machine: {}           # required KHI stateful (I-13), bỏ qua nếu không có vòng đời
events_emitted: []          # khi có
events_consumed: []         # khi có
commands: []                # khi có
queries: []                 # khi có
```

Required fields khác nhau theo `kind`: `invariants` bắt buộc cho mọi kind; `schema` bắt buộc khi concept có data representation; `policy`/`domain_service` dùng inputs/outputs/pre/postconditions thay cho schema — không ép `schema: {}` rỗng chỉ để hợp lệ hình thức.

Ví dụ entity có state machine (theo [I-13](./02-platform-invariants.md)):

```yaml
state_machine:
  states: [CANDIDATE, CONFIRMED, INVALIDATED]
  transitions:
    - {from: CANDIDATE, to: CONFIRMED}
    - {from: CANDIDATE, to: INVALIDATED}
    - {from: CONFIRMED, to: INVALIDATED}
  terminal_states: [INVALIDATED]
```

**Glossary hợp nhất với Domain Contract** — không tách hai tài liệu riêng (tránh lệch nhau theo thời gian). Mỗi file trong `/docs/domain/` (ví dụ `swing.md`) là Domain Contract đầy đủ, là authoritative source duy nhất cho khái niệm đó (theo [I-12](./02-platform-invariants.md)). Ownership của Domain Contract theo `owner` trong metadata của tài liệu — chưa tạo role "Capability Owner" riêng khi team chưa cần (xem 4.4).

## 4.4 Ba loại boundary — không đồng nhất, không tách rời

Domain architecture phân biệt ba boundary khác nhau, **không mặc định quan hệ 1:1 vĩnh viễn**:

- **Business Capability** — ranh giới trách nhiệm nghiệp vụ có semantic tương đối nhất quán (trả lời "hệ thống phải có khả năng làm gì"). Đây đúng nghĩa mà [Chapter 3 §3.1](./03-engineering-principles.md) đã dùng (Strategy/Decision capability, Risk Policy capability...) — Chapter 4 giữ nguyên cách dùng đó, không tái định nghĩa gây lệch.
- **Domain Context** — model/language boundary cụ thể, nằm trong hoặc tương ứng với một capability (nơi Ubiquitous Language ở 4.1 có nghĩa nhất quán).
- **Module/Engine** — đơn vị implementation.

Quan hệ:
```
Business Capability  1 ── 1..n  Domain Context
Domain Context       1 ── 0..n  implementation module
```
(0..n vì: context ở giai đoạn modeling có thể chưa có module; capability đã xác định nhưng implementation chưa tồn tại — không ép "mọi Context phải có sẵn ít nhất 1 Module" ngay Phase 0.)

Giai đoạn đầu (Phase 0-3), mapping có thể là 1:1 — ví dụ: Risk Policy Capability ↔ Risk Policy Context ↔ Risk Gateway. Nhưng Constitution **không đóng đinh 1:1 vĩnh viễn**: sau này một capability (ví dụ Execution) hoàn toàn có thể tách thành nhiều context (Order Lifecycle, Venue Routing, Fill Reconciliation) và nhiều module (Execution Engine, Binance Adapter, Bybit Adapter) mà không bị coi là thay đổi Constitution.

Module kỹ thuật dùng chung (shared library) không được sở hữu semantic/domain state của nhiều context — shared technical component KHÔNG đồng nghĩa shared domain model.

**Giao tiếp giữa các context/capability:** chỉ qua published contract — event, query/read contract, command contract (nhất quán [I-4](./02-platform-invariants.md), [I-7](./02-platform-invariants.md)) — không truy cập trực tiếp state/implementation nội bộ của nhau.

**Ownership:** mỗi Module có Module Owner theo [Governance §2](./00-governance.md). Ownership của Domain Context/Business Capability, nếu sau này cần một role riêng, phải định nghĩa qua ADR và cập nhật Governance — **không mặc định Module Owner đồng thời là Capability Owner** (một capability có thể gồm nhiều module của nhiều owner khác nhau).

## 4.5 Trình tự Domain Modeling

Domain Modeling (Business Capability + Domain Context + Domain Contract) phải đủ ổn định **trước khi** UX Blueprint được phê duyệt, vì UX workflow phụ thuộc vào concept, state, và capability đã xác định. Approval Gate cụ thể được định nghĩa tại [Chapter 12](./12-approval-gates.md); Roadmap (Chapter 14) chỉ thể hiện trình tự phase và tham chiếu quy tắc này, không phải nguồn authoritative của Domain Principle (luồng dependency: Chapter 4 → Chapter 12 → Chapter 14, không đi ngược).
