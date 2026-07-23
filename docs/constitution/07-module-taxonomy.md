---
id: 07-module-taxonomy
title: Module Taxonomy
version: "2.1"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-18"
next_review: null
depends_on: ["02-platform-invariants", "03-engineering-principles", "04-domain-principles"]
---

# 7. Module Taxonomy

Hệ thống có **3 loại module khác nhau** — không phải mọi thứ đều là "Engine". Phân loại theo **bản chất trách nhiệm chính** của module, KHÔNG theo việc module có publish event hay không (xem 7.2), và KHÔNG theo việc module có business logic hay không (xem 7.3).

## 7.1 Ba loại module

| Loại | Bản chất trách nhiệm chính | Ràng buộc |
|---|---|---|
| **Type 1 — Compute Engine** | Biến đổi/suy diễn domain information thành analytical hoặc domain output. **Không sở hữu external side effect** | Tuân [I-3 No Repaint/No Look-Ahead](./02-platform-invariants.md) — không dùng dữ liệu tương lai để sinh output quá khứ |
| **Type 2 — Projection** | Materialize derived state/read-model từ authoritative source (CQRS). **Không sở hữu authoritative domain decision** | Deterministic và rebuild được từ authoritative source ([I-12](./02-platform-invariants.md)); ràng buộc chi tiết xem 7.4 |
| **Type 3 — Runtime Service** | Sở hữu interaction, coordination, control, hoặc side-effect boundary với thế giới bên ngoài | Được phép phát sinh authoritative event thuộc đúng responsibility của nó |

## 7.2 Publish event KHÔNG quyết định loại module

`"Produces an event" ≠ "Compute Engine"`. Mọi loại module đều có thể publish event thuộc responsibility của mình:

- **Risk Gateway** (Type 3) phát sinh `RiskApproved`/`RiskRejected` — authoritative fact thuộc đúng responsibility kiểm soát của nó, không vì thế trở thành Compute Engine.
- **Execution Engine** (Type 3) phát sinh `OrderSubmitted`/`ExecutionAccepted` — kết quả của side effect nó sở hữu.
- **Projection** (Type 2) phát sinh operational event về chính nó (xem 7.4).

Mỗi module có **một primary taxonomy type** (phục vụ registry), nhưng có thể khai báo secondary responsibilities. Taxonomy KHÔNG thay thế responsibility ownership.

## 7.3 Loại module KHÔNG quyết định quyền sở hữu business logic

Việc một module thuộc Type 3 (Runtime Service) **không** có nghĩa nó chỉ làm I/O thuần túy:

- **Risk Gateway** là Type 3 (sở hữu control/gating boundary) — nhưng theo [Chapter 3 §3.1](./03-engineering-principles.md) (Locked), nó **sở hữu và bắt buộc phải có** authoritative Risk Policy Logic (exposure limit, approve/reject, risk-increasing detection, kill switch scope).
- **Exchange Adapter** cũng là Type 3, nhưng chỉ làm venue I/O — không sở hữu domain policy nào.

**Nguyên tắc:** Module Taxonomy trả lời *"bản chất trách nhiệm của module là gì"*; Responsibility Ownership ([Chapter 3 §3.1](./03-engineering-principles.md)) trả lời *"logic nghiệp vụ nào thuộc module nào"*. Hai câu hỏi độc lập.

## 7.4 Ràng buộc riêng của Projection

**Bị cấm:** phát sinh authoritative domain fact, domain decision, hoặc state transition thuộc capability khác. Projection không bao giờ là authoritative source cho một domain concept ([I-12](./02-platform-invariants.md)).

**Được phép:** fold/aggregate event theo type; tính giá trị dẫn xuất thuần túy từ event đã có; rẽ nhánh theo loại event để cập nhật read-model; và phát sinh **operational metadata event về chính nó** — checkpoint advanced, rebuild started/completed, lag detected, health, notification read-model đã cập nhật — miễn các output đó không được dùng như authoritative source thay cho domain event gốc.

*(Quy tắc này KHÔNG cấm cấu trúc điều khiển `if/switch` — mọi projection đều cần chúng để fold theo event type. Điều bị cấm là **authoritative domain fact/decision**, không phải cú pháp.)*

**Rebuild determinism:** Projection phải deterministic và rebuild được từ authoritative source **cùng với projection implementation version, schema, và configuration đã pin**. Chỉ có event log mà không pin version/config thì không đảm bảo tái dựng đúng historical read-model sau khi projection logic thay đổi.

**Criticality (nhất quán [I-6 Fail-Safe by Scope](./02-platform-invariants.md)):** projection **không critical** được phép degrade có kiểm soát mà không dừng toàn platform. NHƯNG derived ≠ luôn non-critical — một projection được dùng làm dependency của decision/risk/execution (ví dụ exposure read-model mà Risk Gateway đọc, order-state projection dùng reconcile) phải **khai báo criticality và failure policy tường minh**; khi tính đúng đắn hoặc độ freshness của nó không xác định, consumer phải fail-safe theo I-6. Điều này không biến projection thành authoritative source.

## 7.5 Thẩm quyền phân loại từng module cụ thể

Chapter 7 định nghĩa **3 loại module tồn tại**. Việc **module cụ thể nào thuộc loại nào** là registry, không phải nguyên tắc — thuộc Phase 0.2/Phase 1, ghi tại một artifact riêng: `/docs/architecture/module-registry.yaml`.

**Không dùng `context-map.yaml`** — artifact đó đã được [Chapter 4 §4.2](./04-domain-principles.md) (Locked) định nghĩa sở hữu đúng 3 phần (capability registry, context registry, relationship map). Thêm module registry vào đó là mở rộng phạm vi một artifact đã Locked, phải qua ADR — không được để Chapter 7 tự mở rộng.

Phân chia thẩm quyền:
```
Business Capability / Domain Context identity + relationship  → context-map.yaml (Chapter 4)
Domain concept semantics                                      → Domain Contract (/docs/domain/)
Implementation module identity, taxonomy type, mapping        → module-registry.yaml (Chapter 7)
Runtime facts                                                 → event log
```

Ví dụ cấu trúc module-registry.yaml:
```yaml
modules:
  - id: risk-gateway
    module_type: runtime_service      # primary taxonomy type
    responsibilities: [risk_policy_evaluation, execution_gating]
    implements_capabilities: [risk-policy]
    serves_contexts: [risk-management]
    emits: [RiskApproved, RiskRejected]
    status: active
```

**Module boundary ≠ Domain Context boundary** — một Domain Context có thể được triển khai bởi nhiều module; một module orchestration có thể phục vụ nhiều context. Không suy luận cái này từ cái kia.

Reference pipeline (bản nháp định hướng, chưa phải kiến trúc chính thức) nằm tại [`/docs/architecture/README.md`](../architecture/README.md) — chốt ở Phase 1 System Architecture.
