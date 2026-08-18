---
id: ADR-XXX
title: ""
version: "0.1"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "YYYY-MM-DD"
last_review: null
next_review: null
depends_on: []
addresses: []
resolves: []
supersedes: []
---

# ADR-XXX: [Tên quyết định]

**Context:** Vấn đề gì buộc phải quyết định?

**Decision:** Quyết định là gì?

**Alternatives considered:** Đã cân nhắc phương án nào khác, vì sao loại bỏ?

**Independent reviews / Concerns / Risks noted:**

| Reviewer principal | Role at review boundary | Execution ID | Review boundary | Independence mode | Isolation attestation | Concern | Risk | Recommendation |
|---|---|---|---|---|---|---|---|---|
| | AI Technical Architect | | | | | | | |
| | AI Technical Architect | | | | | | | |

> Trước approval phải có tối thiểu hai independent review execution đủ điều kiện, đúng Chapter 0 §3 / Chapter 11 §11.5: hai principal identity khác nhau (Mode A — `DISTINCT_PRINCIPAL`), HOẶC cùng một principal qua hai execution/session cô lập thỏa execution-isolation evidence contract (Mode B — `SAME_PRINCIPAL_DISTINCT_EXECUTION`, [ADR-031](../adr/ADR-031.md) §5). Reviewer evidence là historical attribution, không phải permanent governance rule.
>
> Cột hướng dẫn (KHÔNG lặp lại toàn bộ evidence contract — xem [Chapter 0 §3](../constitution/00-governance.md) / [Chapter 11 §11.5](../constitution/11-adr-process.md) / [ADR-031](../adr/ADR-031.md) §5 cho định nghĩa đầy đủ): **Independence mode** ghi `DISTINCT_PRINCIPAL` (Mode A) hoặc `SAME_PRINCIPAL_DISTINCT_EXECUTION` (Mode B). **Execution ID** / **Isolation attestation**: với Mode A, ghi `N/A` (không bắt buộc — principal đã khác nhau); với Mode B, CẢ HAI bắt buộc — Execution ID phải là provider-native session ID nếu có, hoặc một deterministic workflow-generated ID; Isolation attestation phải xác nhận tường minh review đó chạy trong context/session tách biệt, KHÔNG bên trong review kia. Một nhãn tự do một mình KHÔNG PHẢI bằng chứng isolation.

**Scale check:**

```yaml
scale_check:
  current_scale: ""
  expected_scale:
    strategy: 0
    exchange: 0
    plugin: 0
  decision_still_valid: null
  reason: ""
  reason_if_no: ""
```

**Consequences:** Đánh đổi nào phải chấp nhận?

**Accepted risks:** Chỉ điền khi Product Owner tiến hành dù có Risk cao liên quan Platform Invariant.

> Sau Product Owner approval, toàn bộ ADR file bất biến byte-for-byte. Không thêm `superseded_by`, không đổi status, không bump version. Current lifecycle state và reverse relation sống trong MANIFEST.
