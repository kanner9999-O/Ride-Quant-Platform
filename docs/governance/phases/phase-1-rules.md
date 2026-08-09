---
id: phase-1-rules
title: "Phase 1 — System Architecture: Execution Rules"
version: "0.1"
operational_state: EFFECTIVE
owner: Product Owner
accepted_by: Product Owner
accepted_at: "2026-08-09"
created_at: "2026-08-09"
phase: 1
phase_name: "System Architecture"
---

# Phase 1 — System Architecture: Execution Rules

**Vai trò của tài liệu này:** per-phase operational execution rule cho Phase 1 — System Architecture, đúng khung `docs/governance/phases/phase-rules-template.md`. `operational_state: EFFECTIVE` LÀ lifecycle field RIÊNG của loại tài liệu governance-operational này — KHÔNG PHẢI Constitution `Draft/Approved/Locked`, KHÔNG PHẢI ADR `Draft/Approved`. Rule tại đây CÓ THỂ siết chặt (tighten) Global Execution Rules (`../execution-rules.md`) cho phạm vi Phase 1, NHƯNG KHÔNG BAO GIỜ override Global Rules hay bất kỳ authority cao hơn (Constitution/Approved ADR/Approved Phase Plan/accepted DoD/MANIFEST).

```text
phase:              1
phase_name:         System Architecture
operational_state:  EFFECTIVE
accepted_by:        Product Owner
accepted_at:        2026-08-09
```

## Inherited Global Rules

Toàn bộ `docs/governance/execution-rules.md` v0.1 (G-AUTH/G-ADR/G-TXN/G-REV/G-BUDGET/G-ID/G-QG/G-PHASE/G-ORCH) áp dụng NGUYÊN VẸN — tài liệu này CHỈ thêm rule bổ sung/siết chặt riêng cho Phase 1, KHÔNG redefine bất kỳ Global rule nào.

## Lessons from Phase 1 (nguồn cho các control dưới)

```text
- Package 1.4 Trigger E chain (ADR-022 → alignment → reconsolidation → post-
  reconsolidation identity fix → ADR-023) cho thấy: một chain governance có xu
  hướng tự nhân bản transaction nếu KHÔNG có ceiling/containment rule tường minh
  — mỗi ADR/correction hợp lý riêng lẻ, NHƯNG cộng dồn tạo review/transaction
  overhead lớn hơn cần thiết.
- Lifecycle-recording transaction (Approve/Consolidate) từng vô tình đổi file
  blob mà KHÔNG ai kỳ vọng — dẫn tới một finding riêng (`P14V08-POSTCON-MAJ-01`)
  chỉ để sửa một exact-identity reference stale. Bài học: LUÔN phân biệt reviewed
  blob khỏi resulting blob NGAY tại transaction gốc (G-ID-001).
- Một bounded-correction-trên-bounded-correction (ADR-022 v0.1→v0.2→v0.3) VẪN hợp
  lý VÌ mỗi finding LÀ Major/genuine — nhưng nếu chuỗi này tiếp tục KHÔNG giới
  hạn, cần một rule dừng lại VÀ đánh giá root cause (G-REV-004).
```

## P1-ADR — Phase 1 ADR controls

```text
P1-ADR-001  ADR ceiling: ADR-023 LÀ ADR tối đa đã dự kiến trước Gate 2 cho Phase
            1. ADR-024 trở lên đòi hỏi CẢ BA điều kiện:
              1. một architecture conflict THẬT SỰ mới phát hiện (KHÔNG phải một
                 procedural prerequisite còn sót từ ADR trước);
              2. chứng minh được existing authority/alignment/grant/configuration
                 KHÔNG THỂ resolve conflict đó;
              3. một exception justification tường minh hướng tới Product Owner
                 (KHÔNG tự ý author ADR-024+ mà không nêu lý do vượt ceiling này).
            [Đây LÀ rule riêng Phase 1 — KHÔNG đưa vào Global Rules, vì con số
            "ADR-023" chỉ có nghĩa trong phạm vi Phase 1 hiện tại.]

P1-ADR-002  No prerequisite splitting: KHÔNG tiếp tục tạo ADR mới CHỈ vì một ADR
            trước để lại một procedural prerequisite (vd Grant, alignment,
            configuration). Trình tự ưu tiên TRƯỚC KHI cân nhắc một ADR khác:
              existing authority → alignment transaction → versioned grant/
              configuration → evidence pinning.
            CHỈ quay lại xem xét ADR mới nếu trình tự trên KHÔNG đủ để resolve
            (đúng G-ADR-001/G-ADR-004).
```

## P1-TXN — Phase 1 transaction controls

```text
P1-TXN-001  Minimize transaction amplification: KHÔNG biến mỗi metadata/evidence
            discrepancy thành một lifecycle transaction governed mới. Fold
            deterministic bookkeeping fix vào transaction hợp lệ TIẾP THEO khi
            Global G-TXN-003 cho phép (an toàn + semantically mechanical).
```

## P1-REV — Phase 1 review controls

```text
P1-REV-001  Avoid repeated full review: bounded correction nhận bounded
            re-review — CHỈ full Review A/B lại khi semantic KHÔNG liên quan tới
            finding bị chạm (đúng G-REV-002).
```

## P1-ID — Phase 1 identity/evidence lesson

```text
P1-ID-001   Lifecycle/blob lesson: một lifecycle-recording transaction (Approve/
            Consolidate/Reconsolidate) CÓ THỂ đổi file blob DÙ KHÔNG semantic
            content nào đổi (chỉ prose/status field). LUÔN ghi tách biệt tường
            minh trong report VÀ MANIFEST:
              reviewed semantic blob      (blob đã qua Review A/B)
              resulting current artifact  (blob SAU lifecycle transaction chính
                                            nó)
            KHÔNG giả định hai giá trị này giống nhau (đúng Global G-ID-001, áp
            dụng cụ thể cho Phase 1's Package 1.1/1.4 lifecycle chain).
```

## P1-QG — Trigger E scope containment

```text
P1-QG-001   Phần Package 1.4 Trigger E còn lại (Grant, Enforcement/Verification
            design defer, Compatibility Result pinning) PHẢI giữ giới hạn ĐÚNG
            authority/evidence chain tối thiểu cần thiết. KHÔNG reopen (trừ khi
            một transaction riêng biệt tường minh yêu cầu):
              NAV-003 · VIEW-002 · VIEW-003 · DD-001 · DD-003 ·
              UX accessibility gap · database retention gap · LIVE ·
              bất kỳ deferred gap nào KHÔNG liên quan trực tiếp Trigger E.
```

## Gate-path controls

```text
P1-GATE-001  Direct Gate 2 path: SAU KHI Package 1.4 Trigger E THỰC SỰ đóng
             (Compatibility Result pinned, evidence chain đầy đủ), trình tự dự
             kiến LÀ:
               Phase-wide Backward Consistency Check (Chapter 12 §12.4)
               → hai (2) eligible independent Phase-level Gate review
               → Product Owner Gate 2 decision
             KHÔNG author architecture MỚI nào giữa các bước này TRỪ KHI một
             gate-blocking architecture conflict THẬT SỰ được phát hiện (cùng
             ceiling logic P1-ADR-001).
```

## Known process risks (Phase 1)

```text
- Governance-chain self-replication risk: mỗi bounded finding hợp lý riêng lẻ CÓ
  THỂ cộng dồn thành review overhead lớn nếu KHÔNG có ceiling/containment (đóng
  bởi P1-ADR-001/P1-QG-001).
- Blob-drift-after-lifecycle-transaction risk: lifecycle-recording transaction
  đổi blob ngoài dự kiến, tạo finding riêng nếu KHÔNG track tường minh (đóng bởi
  P1-ID-001).
- Scope-creep-via-"while we're here" risk: một bounded correction có thể bị kéo
  giãn sang sửa thêm nội dung KHÔNG liên quan — P1-TXN-001/Global G-TXN-004 chặn
  pattern này.
```

## Retrospective requirement

```text
P1-RETRO-001  TRƯỚC KHI Phase 2 substantive work bắt đầu, PHẢI thực hiện một
              Phase 1 process retrospective, bao gồm:
                - wasted transactions (transaction lẽ ra không cần);
                - avoidable ADRs (ADR lẽ ra không cần author);
                - repeated review cycles (bounded-correction chain quá dài);
                - prompt-size problems (vi phạm §G-BUDGET);
                - bookkeeping defects (loại `P14V08-POSTCON-MAJ-01`);
                - rules hữu ích (giữ lại/tighten thêm);
                - rules thất bại (bỏ/viết lại);
                - rules nên promote lên Global (áp dụng mọi phase, không riêng
                  Phase 1);
                - Phase-2-specific control cần tạo mới (dựa trên lesson thật, KHÔNG
                  đoán trước).
              Retrospective LÀ điều kiện TRƯỚC substantive Phase 2 work — KHÔNG
              tự động đóng, đòi hỏi một transaction riêng thực hiện nó.
```

## Change history

```text
v0.1  2026-08-09  Established — vai trò: `Governance Execution Rulebook
      Structuring Executor`. Formalize Phase 1 execution rules per Product Owner
      instruction (docs/governance/execution-rules.md v0.1 §formalizing note).
      accepted_by: Product Owner, accepted_at: 2026-08-09, operational_state:
      EFFECTIVE.
```
