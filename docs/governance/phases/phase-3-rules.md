---
id: phase-3-rules
title: "Phase 3 — Core Backend: Execution Rules"
version: "0.2"
operational_state: CANDIDATE
owner: Product Owner
accepted_by: null
accepted_at: null
created_at: "2026-08-18"
phase: 3
phase_name: "Core Backend"
---

# Phase 3 — Core Backend: Execution Rules

**Vai trò của tài liệu này:** per-phase operational execution rule CANDIDATE cho Phase 3 — Core Backend (Chapter 14 §14.3: "build ĐÚNG theo dependency graph ở `07-module-taxonomy.md`"), đúng khung `docs/governance/phases/phase-rules-template.md`. Document này được author TRƯỚC KHI Phase 3 substantive work bắt đầu, đúng template's mandatory rule (fail-closed "criteria defined before used"). **`operational_state: CANDIDATE`** — ruleset này CHƯA được Product Owner accept, CHƯA `EFFECTIVE`. Phase 3 substantive governed implementation VẪN `PENDING_PHASE3_EXECUTION_RULE_ESTABLISHMENT` cho tới khi một transaction acceptance riêng biệt (Review A → Independent Review B → Product Owner decision → deterministic MANIFEST recording) đổi `operational_state` sang `EFFECTIVE`. Rule tại đây CÓ THỂ siết chặt (tighten) Global Execution Rules (`../execution-rules.md` v0.4) cho phạm vi Phase 3, NHƯNG KHÔNG BAO GIỜ override Global Rules hay bất kỳ authority cao hơn.

```text
phase:              3
phase_name:         Core Backend
operational_state:  CANDIDATE
accepted_by:        null
accepted_at:        null
```

## 1. Phase identity

```text
Phase:                3 — Core Backend
Roadmap source:        docs/constitution/14-roadmap.md, v1.6, Locked, blob
                       f2cd722218bd80b40241e26530a1919811fedad9 (verified
                       trực tiếp, git hash-object).
Canonical dependency sequence (Chapter 14 §14.2 — quote nguyên văn,
  KHÔNG redefine, tài liệu này KHÔNG có authority sửa architecture):
    Data Layer
    -> Structure Engine & Raw Regime Engine (song song, độc lập)
    -> Feature Engine
    -> Context Projection
    -> Strategy
    -> Decision
    -> Risk Gateway
    -> Execution
    -> Quality Gate theo Tier (13-quality-gates.md, cấp module/artifact)
    -> Approval Gate
Phase 3 lifecycle (MANIFEST, xác nhận trực tiếp trước khi author file
  này): AUTHORIZED TO BEGIN (Product Owner decision 2026-08-18T14:17:00
  +07:00), current_phase = "Phase 3 — Core Backend". Phase 3 substantive
  governed implementation: PENDING_PHASE3_EXECUTION_RULE_ESTABLISHMENT —
  chính là điều kiện file CANDIDATE này định thỏa mãn (SAU KHI accept).
```

## 2. Operational state

```text
operational_state: CANDIDATE (KHÔNG EFFECTIVE). Ruleset này KHÔNG binding
  cho bất kỳ transaction Phase 3 nào cho tới khi Product Owner accept
  tường minh VÀ MANIFEST record deterministic acceptance — đúng trình tự
  §Change history/§13 dưới đây, KHÔNG được rút gọn.
```

## 3. Product Owner acceptance

```text
accepted_by: null
accepted_at: null
Trình tự bắt buộc TRƯỚC KHI operational_state chuyển EFFECTIVE:
  1. candidate authoring (transaction này);
  2. Review A (bounded, phạm vi toàn bộ candidate — architecture/authority
     class, đúng P3-REVIEW-001 §8 dưới, KHÔNG PHẢI mechanical);
  3. Independent Review B, đúng review gate ACTIVE tại [Chapter 0
     §3](../../constitution/00-governance.md) / [Chapter 11
     §11.5](../../constitution/11-adr-process.md) (v1.2/v2.2, Locked,
     [ADR-031](../../adr/ADR-031.md)) — Mode A (`DISTINCT_PRINCIPAL`) HOẶC
     Mode B (`SAME_PRINCIPAL_DISTINCT_EXECUTION`, execution-isolation
     evidence contract). Tài liệu này KHÔNG redefine eligibility — CHỈ
     tham chiếu; P3-IDENTITY-001 §8 dưới áp dụng mechanical pre-check
     TRƯỚC KHI đếm review nào vào prerequisite;
  4. Product Owner acceptance decision, tường minh, KHÔNG suy diễn từ im
     lặng — yêu cầu trực tiếp "một phase rule artifact accepted TRƯỚC KHI
     substantive work" đến từ [`phase-rules-template.md`](./phase-rules-template.md)
     §Mandatory rule (authority trực tiếp cho CHÍNH yêu cầu này). Chapter
     12 §12.1 CHỈ LÀ nguyên tắc tương tự "criteria defined before used"
     được template đó tham chiếu làm minh họa — KHÔNG PHẢI authority trực
     tiếp cho phase-rule acceptance (Chapter 12 tự thân orchestrate Phase
     Approval Gate, KHÔNG phải per-phase-rule acceptance);
  5. deterministic acceptance + MANIFEST current-state recording (transaction
     riêng, mechanical, đúng G-TXN-003).
  CHỈ SAU (5), Phase 3 substantive governed implementation mới PERMITTED —
  KHÔNG BƯỚC nào trong năm bước trên được bỏ qua/gộp tắt.
```

## 4. Inherited Global Rules

```text
Toàn bộ docs/governance/execution-rules.md v0.4 (G-AUTH/G-VERIFY/G-ADR/
  G-TXN/G-REV/G-BUDGET/G-ID/G-QG/G-PHASE/G-ORCH) áp dụng NGUYÊN VẸN. Tài
  liệu này CHỈ thêm rule bổ sung/siết chặt riêng cho Phase 3, KHÔNG
  redefine bất kỳ Global rule nào.
```

### P3-VERIFY-001 (Phase-3-scoped tightening của G-VERIFY-001 — KHÔNG một Global rule mới, KHÔNG G-VERIFY-002)

```text
P3-VERIFY-001  Khi một transaction Phase 3 cite verdict/kết quả của một
               review, Quality Gate, test, coverage, benchmark, BCC,
               decision, hay evidence artifact KHÁC làm input cho một
               lifecycle/current-state claim: nội dung được cite PHẢI
               verify chống lại chính artifact/report/evidence GỐC tại
               đúng boundary liên quan — prompt assertion MỘT MÌNH KHÔNG
               PHẢI evidence.
               Tối thiểu verify: (a) evidence identity; (b) subject/
               boundary; (c) verdict/kết quả thật; (d) freshness/
               applicability khi liên quan; (e) evaluator/reviewer
               identity khi áp dụng.
               Với executable evidence (test/coverage/benchmark): một kết
               quả trước đó KHÔNG được coi LÀ fresh sau khi subject
               implementation đổi, TRỪ KHI evidence contract tự nó chứng
               minh continued applicability.
               Nguồn: Gate-3 sequence (commit 16f34c4 -> 7f94a54, xem
               `phase2-retrospective-001.md` §6/§8) — một lifecycle-
               recording transaction đã ghi Product Owner decision LÀ
               authoritative dựa trên Review B verdict được ASSERT trong
               prompt ("CLEAN"), KHÔNG verify chống lại Claude's report
               THẬT (`REVISION_REQUIRED`) — chỉ được sửa bởi một bounded
               correction riêng biệt SAU.
               Rule này CHỈ Phase-3-scoped — mở rộng KHÁI NIỆM G-VERIFY-
               001 (blob/taxonomy fact) sang NỘI DUNG evidence artifact
               được cite, NHƯNG KHÔNG tự tạo/tuyên bố một Global rule mới
               (`G-VERIFY-002`). Một Global promotion transaction riêng
               biệt, SAU retrospective Phase 3, LÀ nơi duy nhất có thẩm
               quyền làm điều đó (xem §"Deferred Global promotion
               candidates" dưới).
```

## 5. Lessons from previous phase (nguồn cho các control dưới)

```text
- docs/governance/retrospectives/phase2-retrospective-001.md v1.0, Final,
  P2-RETRO-001 COMPLETE, LÀ nguồn DUY NHẤT cho mọi control dưới — KHÔNG
  control nào không có lesson gốc từ retrospective này, TRỪ P3-MODULE-
  BATCH-001 (generalize trực tiếp một pattern ĐÃ verify hiệu quả, §9's
  P2-PROTOTYPE-001 KEEP finding, KHÔNG speculative).
- §4/§8 retrospective (Gate-3 lifecycle-recording defect): lifecycle
  recorder chấp nhận nội dung review được assert trong prompt thay vì
  verify chống lại report thật — root cause MỚI, generalize thành
  `P3-VERIFY-001` (§4 trên).
- §7 retrospective (governance-chain self-replication): pattern self-
  replication Phase 1 (ADR-scoped) KHÔNG lặp lại dạng ADR ở Phase 2 (0
  ADR), NHƯNG lặp lại dạng non-ADR (Batch 02's 4-round correction chain,
  Gate-3's 2-round sequence) — `P2-ADR-CHAIN-001`'s phạm vi hẹp KHÔNG bao
  phủ. `P3-CORRECTION-CHAIN-001` (§6 dưới) generalize phạm vi.
- §9.1 retrospective (P2-TXN-001 TIGHTEN): bốn bookkeeping-reconciliation
  transaction riêng biệt xảy ra vì fold CHỈ được PHÉP, KHÔNG BAO GIỜ mặc
  định. `P3-TXN-001` (§7 dưới) đổi default.
- §9.3 retrospective (P2-REVIEW-001 TIGHTEN): rule's escape clause "nếu
  recording lộ semantic conflict" lẽ ra áp dụng tại Gate-3 bước 1 nhưng
  KHÔNG kích hoạt. `P3-REVIEW-001` (§8 dưới) thêm bước dừng tường minh.
- §9.4 retrospective (P2-BUDGET-001 KEEP table-cell + TIGHTEN section):
  100% table cell ≤ 257 từ (KEEP), NHƯNG hai decision-bundle section vượt
  1,500 từ (BCC 1,525; Gate-3 1,707) — scope gap. `P3-BUDGET-001` (§9
  dưới) mở rộng.
- §8 mục 1 retrospective (Gate-3 actor-identity): catch CHỈ xảy ra vì
  executor tình cờ cross-check `team.yaml`, KHÔNG một mechanical gate.
  `P3-IDENTITY-001` (§8 dưới) formalize pre-check.
- §9.5 retrospective (P2-PROTOTYPE-001 KEEP): 100% batch-level
  containment, zero per-screen exception. `P3-MODULE-BATCH-001`
  generalize sang module-level batching cho Phase 3's implementation-
  heavy work.
```

## 6. Phase-specific ADR controls

```text
Phase 2 tạo ZERO ADR (verified trực tiếp, retrospective §3) — KHÔNG
  invent một ADR ceiling tùy tiện cho Phase 3 KHÔNG có evidence. Thay vào
  đó:
  - ADR CHỈ author khi Chapter 0 §4b ADR Scope Rule THẬT SỰ trigger
    (Platform Invariant/Event Schema/Module Taxonomy/dependency
    graph/Governance process/quyết định ảnh hưởng >1 module hoặc khó đảo
    ngược) — KHÔNG "gap → ADR" reflex (đúng Global G-ADR-001).
  - KHÔNG split implementation prerequisite thành nhiều ADR CHỈ vì
    implementation phức tạp — độ phức tạp implementation TỰ NÓ KHÔNG PHẢI
    lý do cho một ADR (đúng G-ADR-002/G-ADR-003).
  - Nếu một ADR HOẶC bất kỳ architectural artifact nào sau này thực sự
    đạt correction-chain threshold, `P3-CORRECTION-CHAIN-001` ngay dưới
    áp dụng — KHÔNG rule ADR ceiling riêng cần thiết trước khi có bằng
    chứng.
```

### P3-CORRECTION-CHAIN-001 (generalize P2-ADR-CHAIN-001 — phạm vi mở rộng ngoài ADR)

```text
P3-CORRECTION-CHAIN-001  Nếu BẤT KỲ một governed artifact đơn lẻ nào —
                  bao gồm code/module package, architecture artifact,
                  evidence artifact, rules artifact, hay Phase-3
                  deliverable khác — đạt BA (3) correction round liên
                  tiếp KHÔNG stabilize (semantic correction round, KHÔNG
                  tính mechanical bookkeeping fix), DỪNG NGAY trước round
                  thứ tư bình thường. Thay vào đó:
                    1. một root-cause consolidation transaction bounded;
                    2. re-resolve authoritative ground truth trực tiếp
                       (đúng G-VERIFY-001/P3-VERIFY-001);
                    3. re-evaluate liệu review scope round trước có quá
                       hẹp không (đúng nguyên nhân thật Batch 02's 4-round
                       chain — mỗi round bounded đúng scope riêng, KHÔNG
                       round nào re-derive authority-class semantics từ
                       Domain Contract gốc);
                    4. một consolidated correction proposal DUY NHẤT;
                    5. bounded review tỷ lệ đúng với consolidated
                       semantic delta (đúng P3-REVIEW-001 §8).
                  KHÔNG tạo governance microtransaction chỉ để "tiếp tục
                  chain" mà không re-resolve root cause.
                  Rule này KHÔNG override Global G-REV hay ADR governance
                  — CHỈ siết chặt Phase 3 workflow, VÀ mở rộng phạm vi
                  `P2-ADR-CHAIN-001` (Phase 2, ADR-only) sang MỌI governed
                  artifact — generalize trực tiếp từ Batch 02's 4-round
                  chain (`45126d9`→`e8fb6fd`, later lộ ra P2-BCC-MAJ-01)
                  VÀ Gate-3's 2-round sequence (`16f34c4`→`7f94a54`), cả
                  hai NGOÀI phạm vi P2-ADR-CHAIN-001's ADR-only scope
                  (retrospective §7/§9.2).
```

## 7. Transaction controls

### P3-TXN-001 (đổi default fold — nguồn: retrospective §9.1)

```text
P3-TXN-001  Mỗi primary transaction CHỈ MỘT semantic decision (đúng
            Global G-TXN-001) — giữ nguyên. Khi một semantic transaction
            đạt kết quả terminal hợp lệ, deterministic current-state
            bookkeeping do CHÍNH kết quả đó gây ra PHẢI mặc định được ghi
            trong CÙNG transaction, KHI an toàn VÀ reproducible (đảo
            ngược default so với `P2-TXN-001`'s "CÓ THỂ fold" — nay LÀ
            "PHẢI fold TRỪ KHI có lý do").
            Một bookkeeping transaction riêng biệt CHỈ được phép khi:
              - atomic recording KHÔNG thể an toàn thực hiện cùng lúc;
              - independent evidence PHẢI tồn tại trước;
              - CHÍNH bookkeeping đó phát hiện semantic conflict (route
                sang P3-REVIEW-001, KHÔNG tự "sửa" evidence);
              - một rule cao hơn đòi hỏi tách biệt.
            Lý do hoãn PHẢI ghi tường minh khi deferred.
            Mục tiêu: tránh lặp lại bốn bookkeeping-reconciliation
            transaction riêng biệt của Phase 2 (`4c085fd`/`988e3c3`/
            `30c405b`/`0803728` — retrospective §2/§9.1).
            KHÔNG dùng fold để giấu một semantic decision thứ hai trong
            cùng transaction — đúng Global G-TXN-004 (transaction
            "mechanical" PHẢI giữ mechanical xuyên suốt).
```

## 8. Review controls

### P3-REVIEW-001 (tighten P2-REVIEW-001 — nguồn: retrospective §9.3)

```text
P3-REVIEW-001  Review depth tỷ lệ với LOẠI thay đổi (đúng Global
               G-REV-001), giữ nguyên table Phase 2:

                 new architecture / authority / contract semantics
                   -> full governed review (Review A/B)

                 bounded semantic correction
                   -> bounded semantic re-review, CHỈ phạm vi đã chạm

                 mechanical factual correction
                   -> deterministic verification khi reproducible, KHÔNG
                      tự động full A+B

                 evidence/bookkeeping recording
                   -> validation only theo default

               THÊM (đóng Gate-3 failure, retrospective §8 mục 3): NẾU
               một recording/verification transaction phát hiện evidence
               được cite MÂU THUẪN với assertion đang được ghi — DỪNG
               NGAY việc recording đó. KHÔNG "sửa" evidence bên trong
               transaction recorder. Route sang governed semantic/
               evidence-remediation path riêng (Review A/B đầy đủ nếu
               semantic, hoặc bounded correction nếu factual — KHÔNG tự
               quyết định tại chính recorder).
               KHÔNG review-round amplification khi KHÔNG có Major/
               Blocker mới (đúng Global G-REV-004).
```

### P3-IDENTITY-001 (reviewer/evaluator identity mechanical pre-check — nguồn: retrospective §8 mục 1)

```text
P3-IDENTITY-001  TRƯỚC KHI một review/evaluation result được tính vào
                 một governance prerequisite (Chapter 12 §12.2 mục 8 hoặc
                 tương đương), mechanically resolve VÀ pin: actor
                 identity, role, registered alias (nếu áp dụng), VÀ exact
                 review/evaluation boundary — đối chiếu trực tiếp
                 `docs/team/team.yaml` (SSOT). KHÔNG cho phép một
                 execution/session label (vd một chuỗi "execution
                 identity" tùy ý) tự động trở thành actor identity TRỪ
                 KHI governance tường minh established cơ chế đó
                 (team.yaml's registered alias, giống "Independent Review
                 B" ↔ Claude).
                 Nguồn: Gate-3's actor-identity mismatch (draft ban đầu
                 gán CẢ Review A LẪN Review B cho "ChatGPT," phân biệt chỉ
                 bởi một execution-identity string KHÔNG đăng ký) — catch
                 tại thời điểm đó CHỈ xảy ra vì diligence thủ công, KHÔNG
                 một mechanical gate (retrospective §8 mục 1).
                 Đây LÀ một Phase-3 operational pre-check — KHÔNG redefine
                 Chapter 0 §3/Chapter 11 §11.5's reviewer-independence
                 authority (Mode A `DISTINCT_PRINCIPAL` / Mode B
                 `SAME_PRINCIPAL_DISTINCT_EXECUTION`, ACTIVE kể từ
                 ADR-031), CHỈ thêm một bước verify mechanical TRƯỚC KHI
                 đếm — với Mode B, bước này bao gồm verify execution-
                 isolation evidence contract (ADR-031 §5) đã thỏa, KHÔNG
                 CHỈ registered alias.
```

## 9. Prompt/efficiency controls

### P3-BUDGET-001 (tighten P2-BUDGET-001 — nguồn: retrospective §9.4)

```text
P3-BUDGET-001  Global §G-BUDGET áp dụng nguyên vẹn (KHÔNG redefine
               ceiling). Giữ nguyên MANIFEST table cell ≤ 1,500 từ tại
               thời điểm MỖI edit (P2-BUDGET-001, HELD 100% suốt Phase 2
               — max 257 từ, retrospective §5/§9.4).
               MỞ RỘNG: standalone MANIFEST current-state/decision-bundle
               section (KHÔNG PHẢI table cell — vd "Approval Gate —
               Decision" pattern) NÊN giữ ≤ 1,500 từ tại mỗi edit. Nếu
               PHẢI vượt do nội dung decision-bundle tối thiểu bất biến
               (Chapter 14 §14.4.1/§14.4.2 yêu cầu), thì:
                 - CHỈ giữ current/pinned decision content bắt buộc;
                 - di chuyển narrative/process history sang CHANGELOG.md/
                   evidence artifact riêng;
                 - ghi tường minh LÝ DO section đó KHÔNG thể compact thêm.
               KHÔNG áp đặt một hard truncation bất khả thi vi phạm yêu
               cầu Chapter 14 immutable-decision-bundle-content.
               Prompt structure mặc định delta-only (Goal/Baseline/
               Required delta/Forbidden changes/Validation/Report), giữ
               nguyên P2-BUDGET-001's nguyên tắc.
               [Đóng retrospective §9.4 TIGHTEN finding — BCC section
               1,525 từ, Gate-3 section 1,707 từ, cả hai vượt CHÍNH con
               số 1,500 dùng cho table cell dù KHÔNG kỹ thuật table cell.]
```

### P3-MODULE-BATCH-001 (generalize P2-PROTOTYPE-001 — nguồn: retrospective §9.5 KEEP)

```text
P3-MODULE-BATCH-001  Module-level change batching: Phase 3 (implementation-
                  heavy, đúng Chapter 14 §14.2 dependency graph) review
                  theo default LÀ một coherent module/milestone delta,
                  KHÔNG theo từng source file/function riêng lẻ. Internal
                  commit/iteration CÓ THỂ xảy ra BÊN TRONG một coherent
                  work unit KHÔNG cần A/B governance cycle riêng cho mỗi
                  file.
                  Ngoại lệ (đòi hỏi governance riêng, KHÔNG gộp vào batch
                  default):
                    - new architecture/authority/contract decision;
                    - security/custody boundary change;
                    - Tier/Quality-Gate applicability change;
                    - dependency graph change;
                    - cross-module semantic contract change.
                  Generalize trực tiếp `P2-PROTOTYPE-001`'s batch-
                  containment lesson (100% hiệu quả suốt Phase 2, ZERO
                  per-screen exception, retrospective §9.5 KEEP) — KHÔNG
                  redefine Roadmap module ordering (§1 trên, bất biến).
```

## 10. Known process risks (Phase 3)

```text
1. Correction-chain self-replication qua non-ADR artifact (code/module/
   evidence) — đóng bởi P3-CORRECTION-CHAIN-001 (§6).
2. Stale test/coverage/benchmark evidence SAU KHI code thay đổi — đóng
   bởi P3-VERIFY-001's executable-evidence freshness clause (§4).
3. Lifecycle recorder tin assertion được cite thay vì verify chống lại
   nguồn thật — đóng bởi P3-VERIFY-001 (§4) + P3-REVIEW-001's stop clause
   (§8).
4. Reviewer/evaluator actor-identity mismatch — đóng bởi P3-IDENTITY-001
   (§8).
5. Bookkeeping amplification (nhiều transaction riêng biệt cho một kết
   quả) — đóng bởi P3-TXN-001 (§7).
6. MANIFEST decision-bundle bloat (non-table-cell section) — đóng bởi
   P3-BUDGET-001 (§9).
7. File-by-file review amplification — đóng bởi P3-MODULE-BATCH-001 (§9).
8. Implementation đi trước Roadmap dependency order (Data Layer trước
   khi Structure Engine/Raw Regime Engine sẵn sàng, hoặc Strategy trước
   Feature Engine/Context Projection) — KHÔNG rule mới cần thiết, Chapter
   14 §14.2's sequence tự nó LÀ authority; mọi transaction Phase 3 PHẢI
   verify trực tiếp dependency state (đúng G-VERIFY-001) trước khi author
   một module ngoài thứ tự.
9. Vô tình conflate Phase 3 start với LIVE authorization — Phase 3
   lifecycle AUTHORIZED TO BEGIN KHÔNG BAO GIỜ ngụ ý deployment/exchange-
   connectivity/real-order-execution/custody/credential-use/LIVE-trading
   authorization nào (đúng MANIFEST "Phase 3 Start Authorization" section,
   PAPER-only/LIVE Unauthorized giữ nguyên xuyên suốt).
```

## 11. Gate-path controls

```text
Trình tự dự kiến tới Phase 3's Approval Gate (Chapter 12 §12.2), SAU KHI
  Phase 3 substantive governed implementation được PERMITTED riêng biệt
  (§3 trên — rule này KHÔNG tự authorize):
    Phase 3 module/artifact implementation (cadence P3-MODULE-BATCH-001)
    -> Quality Gate theo Tier cho từng module/artifact (Chapter 13 §13.4,
       theo đúng Tier applicability đã Locked — tài liệu này KHÔNG tự
       quyết định Tier/applicability nào vượt ngoài authority hiện có)
    -> Phase-wide Backward Consistency Check nếu áp dụng (Chapter 12
       §12.4)
    -> Phase-level Gate review(s) đúng số lượng/độc lập Chapter 12 yêu
       cầu (P3-IDENTITY-001 áp dụng cho mỗi review)
    -> Product Owner Phase 3 Approval Gate decision
  KHÔNG author architecture MỚI giữa các bước này TRỪ KHI một gate-
  blocking conflict THẬT SỰ được phát hiện (cùng ceiling logic P1-ADR-
  001/P2-ADR-CHAIN-001/P3-CORRECTION-CHAIN-001).
  Roadmap dependency order (§1 trên) VÀ Quality Gate/BCC/Phase-level
  review/Product-Owner-final-decision prerequisite (Chapter 12/13) ĐỀU
  PHẢI giữ nguyên — rule này KHÔNG redefine bất kỳ điều nào.
  **Phase-3 DoD VÀ canonical gate-set declaration LÀ future governed
  work** — KHÔNG author/accept tại tài liệu này (`docs/phase-dod/
  phase-3-dod.md` KHÔNG tồn tại, transaction này KHÔNG tạo). KHÔNG một
  Approval Gate nào được mở cho tới khi Chapter 12/14 prerequisite (DoD
  accepted+incorporated, deliverable complete, dependency state phù hợp,
  ADR closure, Quality Gate PASS, BCC No conflict, validator/freshness
  pass, ≥2 independent review) ĐỀU thỏa.
```

## 12. Retrospective requirement

```text
P3-RETRO-001  TRƯỚC KHI Phase 4 substantive work bắt đầu, PHẢI thực hiện
              một Phase 3 process retrospective, cùng cấu trúc tối thiểu
              P1-RETRO-001/P2-RETRO-001 (wasted transaction, avoidable
              ADR, repeated review/correction churn, prompt-size/budget
              problem, bookkeeping/lifecycle defect, rule hữu ích/thất
              bại, rule nên promote Global, Phase-4-specific control mới)
              — CỘNG THÊM đánh giá riêng:
                - test/coverage/benchmark evidence freshness failure
                  (P3-VERIFY-001's executable-evidence clause);
                - module-batching effectiveness (P3-MODULE-BATCH-001);
                - dependency-order violation (§10 mục 8);
                - hiệu quả của TỪNG P3 control (P3-CORRECTION-CHAIN-001/
                  P3-TXN-001/P3-VERIFY-001/P3-REVIEW-001/P3-BUDGET-001/
                  P3-IDENTITY-001/P3-MODULE-BATCH-001) — KEEP/TIGHTEN/
                  RETIRE, evidence-based, giống đúng phương pháp
                  `phase2-retrospective-001.md`.
              Retrospective LÀ điều kiện TRƯỚC substantive Phase 4 work —
              KHÔNG tự động đóng, đòi hỏi một transaction riêng thực hiện
              nó. Rule này TỰ NÓ KHÔNG authorize Phase 4.
```

## Deferred Global promotion candidates (KHÔNG activate — reference only)

```text
Retrospective (`phase2-retrospective-001.md` §10) đề xuất ba candidate
  promote lên Global Execution Rules — tài liệu CANDIDATE này KHÔNG sửa
  `docs/governance/execution-rules.md`, KHÔNG activate bất kỳ candidate
  nào Global/effective:
    - Evidence-content verification (P3-VERIFY-001 §4 trên LÀ Phase-3-
      scoped implementation CỦA candidate này — đề xuất Global tên
      `G-VERIFY-002` VẪN CHỈ LÀ đề xuất, NOT ACTIVATED GLOBALLY BY THIS
      DOCUMENT).
    - Mechanical per-edit budget enforcement (P2-BUDGET-001/P3-BUDGET-001
      đã chứng minh hoạt động khi thi hành per-edit — đề xuất Global
      promotion cho `G-BUDGET-001`'s enforcement mechanism, NOT ACTIVATED
      GLOBALLY BY THIS DOCUMENT).
    - Batch/module-level containment pattern (P2-PROTOTYPE-001/
      P3-MODULE-BATCH-001 — đề xuất generalize vượt ngoài Phase 2/3 cho
      mọi phase tương lai sinh khối lượng artifact-instance cao, NOT
      ACTIVATED GLOBALLY BY THIS DOCUMENT).
  Global promotion (SỬA `execution-rules.md`) LÀ một governance amendment
  transaction riêng biệt, SAU Phase 3 retrospective (P3-RETRO-001) HOẶC
  sớm hơn nếu Product Owner tường minh quyết định — KHÔNG tự động, KHÔNG
  bởi tài liệu này.
```

## ADR Scope Rule check (self-certification cho chính tài liệu này)

```text
Tài liệu này LÀ một phase-specific operational rules artifact, tạo dưới
  delegation ĐÃ established bởi `phase-rules-template.md` (chính template
  đó established qua transaction riêng trước đây, KHÔNG phải bởi file
  này). Nó siết chặt (tighten) workflow BÊN TRONG Phase 3 — KHÔNG sửa
  Constitution, KHÔNG sửa Global Execution Rules (`execution-rules.md`
  KHÔNG chạm, verified git diff --quiet), KHÔNG sửa Module Taxonomy/Event
  Schema/architecture/Approved ADR semantics nào, KHÔNG redefine Roadmap
  dependency graph (§1 quote nguyên văn).
Kết luận: ADR_NOT_REQUIRED.
KHÔNG conflict authority cao hơn nào phát hiện trực tiếp qua inspection
  §00-governance.md/§12-approval-gates.md/§14-roadmap.md — nếu một
  conflict thật xuất hiện sau này, xử lý tại chính thời điểm đó (đúng
  §6's "no speculative ADR ceiling").
```

## Change history

```text
v0.1  2026-08-18  Author candidate — vai trò: `Phase 3 Execution Rules
      Authoring Executor`. Derive toàn bộ bảy control
      (P3-CORRECTION-CHAIN-001, P3-TXN-001, P3-VERIFY-001, P3-REVIEW-001,
      P3-BUDGET-001, P3-IDENTITY-001, P3-MODULE-BATCH-001) trực tiếp từ
      `docs/governance/retrospectives/phase2-retrospective-001.md` v1.0
      (P2-RETRO-001 COMPLETE) — KHÔNG lesson nào invented. `P3-RETRO-001`
      established (retrospective requirement cho Phase 4). KHÔNG ADR
      ceiling tùy tiện (Phase 2 tạo 0 ADR — KHÔNG evidence cho một số cụ
      thể). `P3-VERIFY-001` LÀ Phase-3-scoped tightening của Global
      `G-VERIFY-001` — KHÔNG tự tạo/activate `G-VERIFY-002` Global (đề
      xuất Global promotion VẪN deferred, xem §"Deferred Global promotion
      candidates"). `operational_state: CANDIDATE`, `accepted_by: null`,
      `accepted_at: null` — CHƯA Product Owner acceptance, CHƯA
      `EFFECTIVE`. `docs/governance/execution-rules.md` KHÔNG sửa
      (byte-identical, git diff empty). Phase 3 substantive governed
      implementation VẪN `PENDING_PHASE3_EXECUTION_RULE_ESTABLISHMENT`.
v0.2  2026-08-19  Bounded correction — vai trò: `Phase-3 Rules Bounded
      Correction Executor`, đóng `P3-RULES-A-MAJ-01` (Major, Review A).
      Defect: §3's acceptance sequence tự định nghĩa lỗi thời — bước 3
      hardcode "Independent Review B (actor riêng biệt)" thay vì tham
      chiếu review gate ACTIVE tại Chapter 0 §3/Chapter 11 §11.5 (nay
      Mode A/Mode B, kể từ ADR-031 activation, 2026-08-18T17:25:00+07:00);
      bước 4 cite Chapter 12 §12.1 NHƯ THỂ đó LÀ direct authority cho
      phase-rule acceptance — SAI, Chapter 12 orchestrate Phase Approval
      Gate, KHÔNG phải per-phase-rule acceptance; direct authority thật
      LÀ `phase-rules-template.md` §Mandatory rule. Sửa: bước 3 nay tham
      chiếu Chapter 0 §3/Chapter 11 §11.5 (Locked, ACTIVE, ADR-031) —
      Mode A HOẶC Mode B, KHÔNG redefine eligibility tại đây; bước 4 cite
      `phase-rules-template.md` §Mandatory rule LÀM direct authority,
      Chapter 12 §12.1 CHỈ LÀ nguyên tắc tương tự tham chiếu minh họa.
      `P3-IDENTITY-001` (§8, tham chiếu trực tiếp từ §3 bước 3) sửa tương
      ứng — "distinct-actor authority" (stale) → "reviewer-independence
      authority (Mode A/Mode B)", thêm execution-isolation-evidence-
      contract note cho Mode B. KHÔNG broaden scope — bảy P3 control
      khác, §Gate-path/§Retrospective/§Known process risks/§Deferred
      Global promotion candidates/§ADR Scope Rule check KHÔNG chạm
      (byte-equivalent ngoài hai đoạn trên). `operational_state:
      CANDIDATE` (KHÔNG đổi), `accepted_by: null`, `accepted_at: null`
      (KHÔNG đổi) — VẪN CHƯA Product Owner acceptance, CHƯA `EFFECTIVE`.
      `P3-RULES-A-MAJ-01`: `CLOSED_BY_BOUNDED_CORRECTION`,
      `PENDING_REVIEW_A_REREVIEW` — KHÔNG claim CLEAN. ADR-031/
      Constitution/Global Execution Rules KHÔNG sửa (byte-identical, git
      diff empty). Phase 3 substantive governed implementation VẪN
      `PENDING_PHASE3_EXECUTION_RULE_ESTABLISHMENT`.
```
