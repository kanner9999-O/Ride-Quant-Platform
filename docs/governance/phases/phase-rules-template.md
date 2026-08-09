---
id: phase-rules-template
title: "Phase Execution Rules — Template"
version: "0.1"
operational_state: TEMPLATE
owner: Product Owner
created_at: "2026-08-09"
---

# Phase Execution Rules — Template

**Vai trò của tài liệu này:** template cấu trúc CHO MỌI `docs/governance/phases/phase-<n>-rules.md` tương lai — bản thân tài liệu này **KHÔNG PHẢI** một effective ruleset (`operational_state: TEMPLATE`, KHÔNG `EFFECTIVE`), KHÔNG áp dụng cho bất kỳ phase nào. Nó CHỈ khóa **cấu trúc bắt buộc** — nội dung cụ thể PHẢI derive từ lesson thật của phase trước đó, KHÔNG được author trước một cách speculative.

## Mandatory rule (bắt buộc cho MỌI phase tương lai)

> Một phase tương lai PHẢI có phase-specific execution-rule artifact của chính nó, author VÀ được Product Owner accept tường minh, **TRƯỚC KHI** substantive work của phase đó bắt đầu — cùng nguyên tắc "criteria defined before used" đã áp dụng cho Phase DoD (Chapter 12 §12.1).

Fail-closed: KHÔNG có phase rule artifact accepted → substantive work của phase đó CHƯA được phép bắt đầu (đúng nguyên tắc "eligibility incomplete" của Chapter 12 §12.2, áp dụng tương tự cho operational governance).

**KHÔNG author trước speculative Phase 2/3/4+ rule file nào** — mỗi phase rule PHẢI viết TẠI thời điểm phase đó chuẩn bị bắt đầu, dựa trên retrospective/lesson learned THẬT của phase liền trước (xem §Retrospective requirement dưới).

## Cấu trúc bắt buộc (mọi phase file PHẢI chứa đủ 12 mục sau, đúng thứ tự)

```text
1.  Phase identity                (phase số, tên, roadmap source)
2.  Operational state              (operational_state field — EFFECTIVE, KHÔNG
                                    Constitution/ADR lifecycle terminology)
3.  Product Owner acceptance        (accepted_by/accepted_at, decision evidence)
4.  Inherited Global Rules          (xác nhận execution-rules.md áp dụng nguyên
                                    vẹn, liệt kê CHỈ phần bổ sung/siết chặt riêng)
5.  Lessons from previous phase     (nguồn cụ thể cho mọi control bên dưới —
                                    KHÔNG control nào không có lesson gốc, trừ
                                    control mang tính containment/ceiling hiển
                                    nhiên tại thời điểm phase mở)
6.  Phase-specific ADR controls     (ceiling/ngưỡng nếu áp dụng, no-prerequisite-
                                    splitting rule)
7.  Transaction controls            (amplification-minimization rule riêng phase)
8.  Review controls                 (bounded-review rule riêng phase)
9.  Prompt/efficiency controls       (tham chiếu Global §G-BUDGET, siết thêm nếu
                                    cần)
10. Known process risks             (rủi ro cụ thể đã quan sát/dự đoán cho phase
                                    đó)
11. Gate-path controls              (trình tự dự kiến tới gate kế tiếp, điều kiện
                                    dừng authoring architecture mới)
12. Retrospective requirement        (điều kiện PHẢI thực hiện trước khi phase
                                    KẾ TIẾP substantive work bắt đầu)
13. Change history                  (mọi version bump, lý do, ngày)
```

(Mục 13 "Change history" LÀ bổ sung bắt buộc ngoài 12 mục nội dung — mọi phase rule file version-hóa như bất kỳ living document nào khác trong repository, I-12.)

## Ràng buộc chung (đúng Global Rules, KHÔNG redefine)

```text
- Phase rule CÓ THỂ siết chặt (tighten) Global Execution Rules cho phạm vi phase
  đó — KHÔNG BAO GIỜ override Global Rules hay bất kỳ authority cao hơn
  (Constitution/Approved ADR/Approved Phase Plan/accepted DoD/MANIFEST).
- Khi một phase rule mâu thuẫn authority cao hơn, authority cao hơn thắng — phase
  rule đó SAI VÀ phải sửa (đúng G-AUTH-003).
- Stable rule ID (vd `P<n>-ADR-001`) KHÔNG BAO GIỜ được tái sử dụng cho một nghĩa
  khác trong cùng phase, dù rule đó sau này bị bỏ — đánh dấu deprecated tường
  minh, KHÔNG xóa/recycle ID.
- Phase rule KHÔNG tự tạo architecture authority, KHÔNG modify Constitution/
  Approved ADR/Phase Plan/DoD, KHÔNG override MANIFEST fact, KHÔNG tự approve
  phase/gate transition nào.
```

## Retrospective requirement (bắt buộc trong mọi phase rule file)

Mỗi phase rule file PHẢI khóa một điều kiện retrospective tương tự Phase 1's `P1-RETRO-001` — thực hiện TRƯỚC KHI phase KẾ TIẾP substantive work bắt đầu, đánh giá tối thiểu: wasted transaction, avoidable ADR, repeated review cycle, prompt-size problem, bookkeeping defect, rule hữu ích/thất bại, rule nên promote lên Global, control cụ thể cho phase kế tiếp.

## Change history

```text
v0.1  2026-08-09  Established — vai trò: `Governance Execution Rulebook
      Structuring Executor`. Template khóa 12-mục structure bắt buộc cho mọi
      phase rule file tương lai, cùng mandatory "phase rule trước substantive
      work" rule. `operational_state: TEMPLATE` — bản thân file này KHÔNG một
      effective ruleset, KHÔNG cần Product Owner acceptance riêng.
```
