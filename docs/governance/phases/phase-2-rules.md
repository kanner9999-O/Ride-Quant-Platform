---
id: phase-2-rules
title: "Phase 2 — Product Prototype: Execution Rules"
version: "0.1"
operational_state: EFFECTIVE
owner: Product Owner
accepted_by: Product Owner
accepted_at: "2026-08-10"
created_at: "2026-08-10"
phase: 2
phase_name: "Product Prototype"
---

# Phase 2 — Product Prototype: Execution Rules

**Vai trò của tài liệu này:** per-phase operational execution rule cho Phase 2 — Product Prototype (Chapter 14 §14.3: "HTML/React/Figma — công cụ không quan trọng"), đúng khung `docs/governance/phases/phase-rules-template.md`. Document này được author VÀ accepted TRƯỚC KHI Phase 2 substantive work bắt đầu, đúng template's mandatory rule (fail-closed "criteria defined before used"). `operational_state: EFFECTIVE` nghĩa LÀ ruleset này đã established/binding — KHÔNG nghĩa LÀ Phase 2 substantive work đã authorize; rule-authoring transaction ≠ phase-authorization transaction (đúng G-PHASE-003, KHÔNG executor nào tự declare phase transition). Rule tại đây CÓ THỂ siết chặt (tighten) Global Execution Rules (`../execution-rules.md` v0.2) cho phạm vi Phase 2, NHƯNG KHÔNG BAO GIỜ override Global Rules hay bất kỳ authority cao hơn.

```text
phase:              2
phase_name:         Product Prototype
operational_state:  EFFECTIVE
accepted_by:        Product Owner
accepted_at:        2026-08-10
```

## Inherited Global Rules

Toàn bộ `docs/governance/execution-rules.md` v0.2 (G-AUTH/G-VERIFY/G-ADR/G-TXN/G-REV/G-BUDGET/G-ID/G-QG/G-PHASE/G-ORCH) áp dụng NGUYÊN VẸN, bao gồm `G-VERIFY-001` (verify-before-claim) mới bổ sung v0.2. Tài liệu này CHỈ thêm rule bổ sung/siết chặt riêng cho Phase 2, KHÔNG redefine bất kỳ Global rule nào.

## Lessons from Phase 1 (nguồn cho các control dưới)

```text
- Phase 1 Process Retrospective #001 (`../retrospectives/phase1-
  retrospective-001.md`) đề xuất trực tiếp ba control tại §8.4
  PHASE2_CONTROL: P2-TXN-001, P2-ADR-CHAIN-001, P2-BUDGET-001 — mỗi control
  derive từ evidence cụ thể (§2/§4/§5/§7 retrospective), KHÔNG speculative.
- §7 retrospective (governance-chain self-replication): P1-ADR-001/P1-QG-
  001 chặn được ADR-count amplification VÀ scope reopening, NHƯNG KHÔNG
  chặn correction-round amplification BÊN TRONG một ADR đơn lẻ (ADR-023
  v0.1→v0.5). P2-REVIEW-001 generalize lesson này cùng Global G-REV-001/
  002/004 thành một review-depth-by-change-type table tường minh, phòng
  risk review effort tăng theo transaction count thay vì semantic risk
  thật.
- P2-PROTOTYPE-001 KHÔNG có Phase 1 lesson trực tiếp — Phase 1 LÀ
  architecture, không tạo prototype/UX artifact nào. Đây LÀ containment
  control ban đầu (anticipatory ceiling), cho phép bởi exception clause
  của `phase-rules-template.md` §5 ("control mang tính containment/ceiling
  hiển nhiên tại thời điểm phase mở"): Phase 2 mở ra một work-type MỚI
  (prototype/UX, khối lượng screen/component dự kiến lớn) mà pattern
  "governance-chain self-replication" (§7 trên) CÓ THỂ lặp lại ở granularity
  "mỗi screen" nếu KHÔNG có ceiling tường minh NGAY từ đầu phase — cùng lý
  do P1-QG-001 được established tại Phase 1.
```

## P2-ADR — Phase 2 ADR controls

```text
P2-ADR-CHAIN-001  Correction-chain circuit breaker: nếu một ADR/
                  architectural artifact đạt BA (3) correction round liên
                  tiếp KHÔNG stabilize (KHÔNG kể approval round) — dừng
                  NGAY, KHÔNG author round correction thứ 4 tiếp theo.
                  Thay vào đó:
                    1. một root-cause consolidation transaction bounded;
                    2. re-resolve current authority/ground truth trực tiếp
                       (đúng G-VERIFY-001);
                    3. một consolidated correction DUY NHẤT tiếp theo.
                  KHÔNG tạo governance microtransaction chỉ để "tiếp tục
                  chain" mà không re-resolve root cause.
                  [Formalize retrospective §8.4/§7 — ADR-023's 5-version
                  chain (v0.1→v0.5) LÀ instance rõ nhất; P1-ADR-001/P1-QG-
                  001 chặn ADR-count amplification NHƯNG KHÔNG chặn
                  correction-round amplification BÊN TRONG một ADR — gap
                  này LÀ lý do rule tồn tại.]
```

## P2-TXN — Phase 2 transaction controls

```text
P2-TXN-001  Transaction proportionality: mỗi primary transaction CHỈ MỘT
            semantic decision (đúng Global G-TXN-001); deterministic
            bookkeeping CÓ THỂ fold vào transaction đó (đúng G-TXN-003).
            Correction mechanical/factual (transcription fix, KHÔNG
            semantic judgment) KHÔNG tự động kích hoạt full semantic
            review — self-verification ĐƯỢC PHÉP khi ground truth
            reproduce được CHÍNH XÁC tại chính transaction đó (script-
            verify trực tiếp, đúng G-VERIFY-001). Nếu meaning/authority/
            responsibility/contract semantics/architecture đổi, PHẢI dùng
            governed semantic path (Review A/B đầy đủ) — KHÔNG dùng self-
            verification cho bất kỳ semantic judgment nào.
            [Formalize retrospective §8.4 — resolves §2's open judgment
            call re: Package 1.5 fix/BCC follow-up split.]
```

## P2-REV — Phase 2 review controls

```text
P2-REVIEW-001  Risk-proportional review: review depth tỷ lệ với LOẠI thay
               đổi, KHÔNG với số lượng transaction (đúng Global G-REV-001):

                 new architecture / authority / contract decision
                   -> full governed review (Review A/B) đúng như hiện tại

                 bounded semantic correction
                   -> bounded re-review, CHỈ phạm vi semantic đã chạm
                      (G-REV-002)

                 mechanical/factual correction
                   -> deterministic verification (G-VERIFY-001) — KHÔNG
                      tự động full A+B review

                 evidence/bookkeeping recording
                   -> validation only, TRỪ KHI chính recording đó lộ ra
                      một semantic conflict chưa từng thấy

               KHÔNG review-round amplification KHI KHÔNG có Major/Blocker
               mới hoặc semantic change thật (đúng G-REV-004).
               [Generalize retrospective §7 self-replication finding —
               table hóa Global G-REV-001/002/004 cho use tại Phase 2, nơi
               volume transaction dự kiến cao (prototype/UX batch).]
```

## P2-BUDGET — Phase 2 prompt/efficiency controls

```text
P2-BUDGET-001  Prompt/MANIFEST budget: Global §G-BUDGET áp dụng nguyên vẹn
               (KHÔNG redefine ceiling). Bổ sung mechanical enforcement
               riêng Phase 2 (đóng retrospective §8.2 TIGHTEN finding —
               G-ID-001/G-BUDGET-001 tồn tại nhưng KHÔNG enforce nhất quán
               Phase 1):
                 - MANIFEST table cell PHẢI ≤ 1,500 từ tại thời điểm MỖI
                   edit — vượt ngưỡng BẮT BUỘC compact-rewrite (move
                   history sang CHANGELOG.md) TRƯỚC KHI transaction được
                   coi hoàn tất, KHÔNG prepend thêm đoạn mới vào row đã
                   vượt ngưỡng.
                 - Phase 2 prompt mặc định cấu trúc delta-only: Goal /
                   Baseline / Required delta / Forbidden changes /
                   Validation / Report — KHÔNG lặp lại toàn bộ historical
                   authority chain trừ khi cần để resolve quyết định hiện
                   tại.
                 - MANIFEST LÀ current-state index, KHÔNG PHẢI narrative
                   transaction log — lịch sử chi tiết thuộc CHANGELOG.md/
                   evidence artifact riêng, KHÔNG đặt review/ADR history
                   lớn vào MANIFEST table cell.
               [Formalize retrospective §8.4/§5 — ADR-023's MANIFEST row
               đạt 8,512 từ trong MỘT cell, ~6x hard ceiling.]
```

## P2-PROTOTYPE — Batch prototype/UX review

```text
P2-PROTOTYPE-001  Batch prototype/UX review: Phase 2 prototype/UX work
                  (HTML/React/Figma — công cụ không quan trọng, đúng
                  Chapter 14 §14.3) được review theo BATCH/milestone gắn
                  kết, KHÔNG theo từng screen/component riêng lẻ theo
                  default. Screen/component riêng lẻ CÓ THỂ iterate BÊN
                  TRONG một batch KHÔNG cần A/B/PO cycle riêng — TRỪ KHI
                  screen/component đó tạo mới một architecture/authority/
                  contract/security/Product-level decision đòi hỏi
                  governance riêng (cùng nguyên tắc G-ADR-002 — ADR CHỈ
                  cho quyết định thật khó đảo ngược).
                  [Anticipatory containment — xem §Lessons trên; không có
                  Phase 1 lesson trực tiếp, cho phép bởi phase-rules-
                  template.md §5 exception clause.]
```

## Known process risks (Phase 2)

```text
- Correction-round self-replication risk (BÊN TRONG một artifact đơn):
  đóng bởi P2-ADR-CHAIN-001 (3-round ceiling).
- MANIFEST/prompt budget drift risk (rule đúng, enforcement lỏng — đúng
  pattern đã quan sát Phase 1): đóng bởi P2-BUDGET-001 mechanical ceiling.
- Review effort tăng theo transaction count thay vì semantic risk thật:
  đóng bởi P2-REVIEW-001 table.
- Screen-by-screen governance amplification risk (Phase 2 prototype/UX
  batch, granularity mới chưa từng có ở Phase 1): đóng bởi P2-PROTOTYPE-
  001.
```

## Gate-path controls

```text
Trình tự dự kiến tới Approval Gate kế tiếp (Gate 3, Chapter 12 §12.2), SAU
  KHI Phase 2 substantive work được Product Owner authorize riêng biệt
  (rule này KHÔNG tự authorize):
    Phase 2 prototype/UX batch work (cadence P2-PROTOTYPE-001)
    → Phase-wide Backward Consistency Check nếu áp dụng (Chapter 12 §12.4)
    → Phase-level Gate review(s) đúng số lượng/độc lập Chapter 12 yêu cầu
    → Product Owner Gate 3 decision
  KHÔNG author architecture MỚI giữa các bước này TRỪ KHI một gate-blocking
  conflict THẬT SỰ được phát hiện (cùng ceiling logic P1-ADR-001). Một ADR
  ceiling cụ thể (số ADR tối đa dự kiến, kiểu `P1-ADR-001`) CHƯA khóa tại
  đây — KHÔNG author trước speculative; sẽ khóa riêng nếu/khi Phase 2 thực
  sự sinh ra một ADR chain cần containment.
```

## Retrospective requirement

```text
P2-RETRO-001  TRƯỚC KHI Phase 3 substantive work bắt đầu, PHẢI thực hiện
              một Phase 2 process retrospective, cùng cấu trúc tối thiểu
              P1-RETRO-001 (wasted transaction, avoidable ADR, repeated
              review cycle, prompt-size problem, bookkeeping defect, rule
              hữu ích/thất bại, rule nên promote Global, Phase-3-specific
              control mới) — CỘNG THÊM đánh giá riêng hiệu quả của
              P2-TXN-001/P2-ADR-CHAIN-001/P2-REVIEW-001/P2-BUDGET-001/
              P2-PROTOTYPE-001 (rule nào hoạt động đúng — KEEP, rule nào
              cần TIGHTEN/RETIRE cho Phase 3).
              Retrospective LÀ điều kiện TRƯỚC substantive Phase 3 work —
              KHÔNG tự động đóng, đòi hỏi một transaction riêng thực hiện
              nó.
```

## Change history

```text
v0.1  2026-08-10  Established — vai trò: `Pre-Phase-2 Process Hardening
      Executor`. Formalize ba control đề xuất tại Phase 1 Process
      Retrospective #001 (`../retrospectives/phase1-retrospective-001.md`
      §8.4 PHASE2_CONTROL): P2-TXN-001 (transaction proportionality),
      P2-ADR-CHAIN-001 (correction-chain circuit breaker), P2-BUDGET-001
      (MANIFEST/prompt mechanical budget). Bổ sung hai control mới ngoài
      đề xuất trực tiếp của retrospective: P2-REVIEW-001 (risk-
      proportional review, generalize §7 self-replication finding + Global
      G-REV) và P2-PROTOTYPE-001 (batch prototype/UX review, anticipatory
      containment cho work-type mới của Phase 2, đúng phase-rules-
      template.md §5 exception clause). accepted_by: Product Owner,
      accepted_at: 2026-08-10, operational_state: EFFECTIVE — ruleset
      established/binding ngay, NHƯNG Phase 2 substantive work VẪN CHƯA
      authorize bởi transaction này (rule-authoring ≠ phase-authorization,
      đúng G-PHASE-003).
```
