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

| Reviewer identity | Role at review boundary | Concern | Risk | Recommendation |
|---|---|---|---|---|
| | AI Technical Architect | | | |
| | AI Technical Architect | | | |

> Trước approval phải có tối thiểu hai independent review execution đủ điều kiện, đúng Chapter 0 §3 / Chapter 11 §11.5: hai principal identity khác nhau (Mode A — `DISTINCT_PRINCIPAL`), HOẶC cùng một principal qua hai execution/session cô lập thỏa execution-isolation evidence contract (Mode B — `SAME_PRINCIPAL_DISTINCT_EXECUTION`, [ADR-031](../adr/ADR-031.md)). Reviewer evidence là historical attribution, không phải permanent governance rule.

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
