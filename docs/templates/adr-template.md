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

**Review A / Risk Classification / Concerns / Risks noted:**

| Reviewer principal | Role at review boundary | Review boundary | Concern | Risk | Recommendation |
|---|---|---|---|---|---|
| | AI Technical Architect | | | | |

> Trước approval phải có đúng một Review A eligible, đúng Chapter 0 §3 / Chapter 11 §11.5 — reviewer giữ role `AI Technical Architect` tại review boundary, độc lập kiểm tra trực tiếp candidate/repository authority. Reviewer evidence là historical attribution, không phải permanent governance rule.

**Risk Classification (bắt buộc, ngay sau Review A):**

```text
class: R0 | R1 | R2       # đúng một, định nghĩa đầy đủ tại ADR-042
reason: ""                 # vì sao thuộc lớp này
cross_check: N/A | PROCEED WITHOUT CROSS-CHECK | CROSS-CHECK   # CHỈ áp dụng khi class: R2;
                                                                 # N/A cho R0/R1 (không phải một gap)
```

> R0/R1 mặc định `NO CROSS-CHECK` — Review A đủ. R2: Review A phải nói ngắn gọn cho Product Owner vì sao là R2 và cross-check có thể giảm rủi ro/uncertainty gì; Product Owner chọn `CROSS-CHECK` hoặc `PROCEED WITHOUT CROSS-CHECK`. Optional cross-check — khi Product Owner chọn dùng — là advisory only, không veto, KHÔNG là approval prerequisite, KHÔNG cần persisted transcript/report/execution-ID/Mode A/Mode B bookkeeping trong file này; nếu Product Owner tường thuật lại kết luận của nó, ghi ngắn gọn tại Concern/Risk/Recommendation phía trên như bất kỳ input nào khác — không tạo thêm bảng/field riêng. Sự vắng mặt của cross-check KHÔNG BAO GIỜ làm ADR mất điều kiện approval.

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
