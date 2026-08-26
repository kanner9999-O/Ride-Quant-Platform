---
id: execution-rules
title: "Ride Quant Platform — Global Execution Rules"
version: "0.5"
operational_state: EFFECTIVE
owner: Product Owner
accepted_by: Product Owner
accepted_at: "2026-08-26"
created_at: "2026-08-09"
---

# Global Execution Rules

**Vai trò của tài liệu này:** đây LÀ **operational governance** — quy tắc THỰC THI giao dịch (transaction), KHÔNG PHẢI Constitution chapter, KHÔNG PHẢI ADR, KHÔNG tạo architecture authority nào. `operational_state: EFFECTIVE` LÀ một lifecycle field RIÊNG của loại tài liệu này — KHÔNG PHẢI Constitution's `Draft/Approved/Locked` (Chapter 0 §7.1), KHÔNG PHẢI ADR's `Draft/Approved` (Chapter 11 §11.3). Rule này áp dụng CHO MỌI phase; per-phase rule (`docs/governance/phases/phase-<n>-rules.md`) CÓ THỂ siết chặt (tighten) nhưng KHÔNG BAO GIỜ được override rule này hay bất kỳ authority cao hơn nào.

**Product Owner instruction being formalized (nguyên văn ý, transaction 2026-08-09):** "Every project phase must have explicit phase-specific execution rules used to improve working efficiency and incorporate lessons learned." Global rules áp dụng xuyên suốt mọi phase; per-phase rules CHỈ áp dụng cho đúng phase của nó.

## Authority hierarchy (bắt buộc, KHÔNG redefine higher authority nào)

```text
1. Constitution / Locked governance          (docs/constitution/*.md, Locked)
2. Approved ADR                              (docs/adr/ADR-*.md, status: Approved)
3. Approved Phase Plan / accepted Phase DoD   (phase-1-plan.md Approved; phase-N-dod.md accepted+incorporated)
4. MANIFEST current state                    (docs/MANIFEST.md, I-12 single source of truth)
5. Global Execution Rules                    (tài liệu này)
6. Current Phase Rules                       (docs/governance/phases/phase-<n>-rules.md)
7. Review/history evidence                   (CHANGELOG.md, review tables, ADR §"Independent reviews")
8. Conversation memory                       (agent/session context — cache ONLY, KHÔNG authoritative)
```

Rule cao hơn LUÔN thắng. Khi một rule ở tầng thấp hơn mâu thuẫn tầng cao hơn, rule thấp hơn SAI VÀ phải sửa — KHÔNG BAO GIỜ ngược lại.

## G-AUTH — Authority

```text
G-AUTH-001  Không tồn tại "chat-only governance rule" bền vững — MỌI rule LÂU DÀI
            PHẢI ghi vào repository (tài liệu này hoặc phase rule); một chỉ dẫn
            chỉ tồn tại trong hội thoại KHÔNG ràng buộc transaction tương lai.
G-AUTH-002  Repository authority LUÔN được resolve TRƯỚC memory — trước khi hành
            động dựa trên một fact nhớ được, verify lại trực tiếp trên file hiện
            tại (git/MANIFEST), KHÔNG tin tưởng snapshot cũ.
G-AUTH-003  Authority cao hơn LUÔN thắng — không có ngoại lệ ngầm định; xung đột
            được resolve theo đúng thứ tự §Authority hierarchy trên.
G-AUTH-004  Conversation memory LÀ cache — hữu ích để tăng tốc, KHÔNG BAO GIỜ LÀ
            nguồn sự thật; mọi claim quan trọng PHẢI verify lại trên repository
            tại thời điểm dùng.
```

## G-VERIFY — Verify before claim

```text
G-VERIFY-001  TRƯỚC KHI khẳng định bất kỳ exact repository fact nào dùng
              trong governance/architecture decision content — bao gồm
              blob SHA, version/lifecycle status, module taxonomy,
              dependency edge, module/edge count, authority mapping, hoặc
              registry parity — PHẢI verify TRỰC TIẾP chống lại repository
              ground truth (git hash-object, python+yaml, hoặc script-
              verify tương đương) tại CHÍNH transaction đó.
              Memory, prompt trước, MANIFEST prose, hoặc historical
              evidence CÓ THỂ dùng để LOCATE fact, NHƯNG KHÔNG BAO GIỜ
              thay thế verification khi fact đó decision-relevant.
              Rule này áp dụng TRƯỚC KHI author claim, KHÔNG CHỈ sau khi
              một reviewer phát hiện discrepancy.
```

## G-ADR — ADR control

```text
G-ADR-001   KHÔNG "gap → ADR" reflex — một finding/gap KHÔNG tự động nghĩa là cần
            một ADR mới; đa số gap resolve qua alignment/correction/grant/
            configuration, KHÔNG cần quyết định architecture mới.
G-ADR-002   ADR CHỈ author cho quyết định architecture THẬT SỰ khó đảo ngược, ảnh
            hưởng nhiều module, hoặc rơi đúng ADR Scope Rule (Constitution
            Chapter 0 §4b) — KHÔNG dùng ADR cho quyết định có thể sửa rẻ/dễ dàng.
G-ADR-003   KHÔNG tạo một ADR mới CHỈ để "hoàn tất" ADR trước theo default — mỗi
            ADR PHẢI có lý do độc lập của chính nó, KHÔNG suy diễn từ "ADR trước
            còn một open item."
G-ADR-004   Bắt buộc chạy ADR inflation/scope check TRƯỚC KHI đề xuất một ADR mới
            (xem §Orchestration self-check dưới) — nếu existing authority/
            alignment/grant/configuration CÓ THỂ resolve gap, KHÔNG author ADR.
```

## G-TXN — Transaction control

```text
G-TXN-001   Mỗi transaction CHỈ MỘT primary decision/action — KHÔNG bundle nhiều
            quyết định độc lập vào cùng một transaction.
G-TXN-002   Ưu tiên bounded correction (sửa đúng finding) thay vì lifecycle
            amplification (bump version/reconsolidate/re-review toàn bộ) khi
            finding thực sự bounded.
G-TXN-003   Deterministic bookkeeping fix (evidence/metadata correction KHÔNG đổi
            semantic) ĐƯỢC PHÉP fold vào một transaction đã required SẴN, nếu an
            toàn VÀ transaction đó VẪN semantically mechanical — KHÔNG smuggle một
            semantic change dưới vỏ bookkeeping.
G-TXN-004   Một transaction đánh dấu "mechanical" PHẢI GIỮ semantically mechanical
            xuyên suốt — nếu content semantic thực sự đổi, đổi nhãn transaction
            (KHÔNG mechanical nữa), KHÔNG âm thầm mở rộng scope dưới nhãn cũ.
```

## G-REV — Review control

```text
G-REV-001   Ưu tiên đánh giá semantic risk THẬT SỰ hơn lặp lại bookkeeping review
            — review effort tỷ lệ với rủi ro semantic, KHÔNG với số lượng
            transaction.
G-REV-002   Bounded correction nhận bounded re-review (CHỈ phạm vi đã sửa), KHÔNG
            tự động kích hoạt full Review A/B lại toàn bộ artifact trừ khi
            semantic KHÔNG liên quan bị chạm.
G-REV-003   Independent Review B PHẢI giữ độc lập THẬT SỰ — KHÔNG dựa trên
            evidence của Review A mà không tự verify lại trực tiếp trên registry/
            artifact.
G-REV-004   Dừng correction churn khi KHÔNG có Major/Blocker mới phát sinh — một
            chuỗi bounded-correction-trên-bounded-correction vô hạn LÀ một process
            defect, cần dừng lại VÀ đánh giá lại root cause thay vì tiếp tục vá.
```

### NON-NORMATIVE INTERPRETATION — Semantic Sufficiency

**KHÔNG một rule ID mới nào được tạo ở đây.** Đây là diễn giải Product Owner-approved cho cách áp dụng `G-REV-001`/`G-REV-004` đã tồn tại — KHÔNG tạo Governance/Approval process mới, KHÔNG đổi severity taxonomy, KHÔNG đổi review eligibility, KHÔNG đổi lifecycle gate, KHÔNG đổi ADR Scope Rule (Constitution Chapter 0 §4b, KHÔNG chạm), KHÔNG đổi Product Owner authority.

```text
1. G-REV-001 + G-REV-004 tối ưu cho semantic risk reduction THẬT SỰ, KHÔNG
   phải cho prose hoàn hảo hay zero-Minor document — mục tiêu là loại đúng
   rủi ro có thật, KHÔNG phải một con số Minor bằng không.
2. Absence of unresolved Blocker/Major KHÔNG tự nó approve một artifact —
   MỌI lifecycle/independent-review/Product Owner requirement hiện có VẪN
   áp dụng nguyên vẹn, KHÔNG rule nào ở đây bypass chúng.
3. Một finding CHỈ thuộc documentation (wording/formatting/historical
   labeling/duplicated hoặc non-authoritative prose) KHÔNG nên tự động kích
   hoạt một standalone correction/re-review transaction riêng theo mặc định
   KHI higher authority (Constitution/Approved ADR/MANIFEST) ĐÃ resolve đúng
   semantics — churn thêm không giảm rủi ro thật.
4. Một finding như vậy CÓ THỂ carry-forward hoặc fold vào một transaction
   tương lai ĐÃ required sẵn, khi an toàn (đúng `G-TXN-003`'s fold
   precedent, KHÔNG đổi).
5. Escalation VẪN đúng đắn khi issue CÓ THỂ misstate authority thật,
   contract/implementation behavior, auditability/reproducibility, safety,
   HOẶC khi Product Owner tường minh yêu cầu sửa — điểm 3/4 KHÔNG áp dụng
   cho các trường hợp này.
6. Zero Minor KHÔNG phải một ADR/package/review exit criterion bổ sung TRỪ
   KHI một rule higher-authority tường minh yêu cầu vậy — không suy diễn
   ngầm một ngưỡng mới.
7. Diễn giải này KHÔNG làm yếu `G-REV-002`, Independent Review B, hay bất kỳ
   yêu cầu remediate Blocker/Major nào — chỉ áp dụng cho phạm vi
   documentation-only, non-blocking Minor đã mô tả ở điểm 3.
```

## G-BUDGET — Prompt budgets

```text
Mechanical transaction:          target 250–500 từ
Bounded correction:              target 400–800 từ
Architecture/ADR authoring:      target 700–1,200 từ; hard ceiling 1,400 từ
Independent review:              target 800–1,500 từ; hard ceiling 2,000 từ

G-BUDGET-001  Tránh lặp lại cùng một invariant/nguyên tắc nhiều lần trong cùng một
              tài liệu — cite MỘT lần, tham chiếu ngắn gọn ở những chỗ khác.
```

## G-ID — Identity/evidence

```text
G-ID-001    Phân biệt tường minh "reviewed semantic candidate identity" (blob đã
            qua Review A/B) khỏi "resulting lifecycle-record identity" (blob SAU
            khi một mechanical lifecycle transaction — vd approval/consolidation —
            edit prose/status field) — HAI blob CÓ THỂ khác nhau dù semantic
            content giống hệt.
G-ID-002    KHÔNG dùng mutable reference (`"latest"`/`"current"`/`">="`/một range)
            ở bất kỳ chỗ nào đòi hỏi exact identity — LUÔN pin đúng version/blob cụ
            thể.
G-ID-003    MANIFEST ưu tiên compact current-state resolution (exact version/
            status/blob hiện tại) — lịch sử chi tiết thuộc CHỦ YẾU về CHANGELOG.md/
            evidence table, KHÔNG lặp lại toàn bộ history trong mỗi MANIFEST row.
```

## G-QG — Quality Gate / evaluator

```text
G-QG-001    Quality Gate ≠ Approval Gate (Chapter 13 §13.1) — gate pass CHỈ sinh
            eligibility evidence, Product Owner VẪN LÀ authority duy nhất quyết
            định phase/gate transition.
G-QG-002    Một reevaluation authorization (Grant) KHÔNG được tự động tái sử dụng
            ngầm cho scope/boundary khác — mỗi Grant PHẢI resolve đúng scope đã
            declare, KHÔNG suy diễn mở rộng.
G-QG-003    `module identity ≠ evaluator grant` — registry membership KHÔNG đồng
            nghĩa quyền đánh giá (Chapter 10 §10.4.1).
G-QG-004    Quyền đánh giá đi qua đúng `Declaration → Grant → Enforcement →
            Verification` (Chapter 9 §9.6) — KHÔNG bỏ qua tầng nào.
G-QG-005    `granted ⊆ declared` — Grant KHÔNG BAO GIỜ vượt scope Declaration đã
            pin.
G-QG-006    Grant CHỈ cấp quyền vận hành (operational authority) — Grant KHÔNG
            BAO GIỜ tự tạo một architecture responsibility mới; responsibility
            PHẢI Declaration-tier trước (module-registry.yaml), Grant CHỈ kích
            hoạt quyền đã Declare.
G-QG-007    Một Compatibility Result CHỈ được tạo SAU KHI toàn bộ authority/
            evidence chain đã exact-pin đầy đủ (Chapter 10 §10.4.1) — KHÔNG suy
            diễn/rút gọn chain.
```

## G-PHASE — Phase progression

```text
G-PHASE-001   Phase kế tiếp KHÔNG BAO GIỜ được suy diễn tự động — chuyển phase LÀ
              một Product Owner decision tường minh (Chapter 12 §12.2), KHÔNG một
              hệ quả ngầm định của việc hoàn tất công việc.
G-PHASE-002   Một carry-forward/deferred gap KHÔNG tự động LÀ gate blocker — CHỈ
              gate-blocking khi một tiêu chí authoritative (DoD/Quality Gate/
              Constitution) tường minh nói vậy.
G-PHASE-003   Phase transition VẪN LÀ Product Owner authority duy nhất — không
              executor/reviewer nào tự declare phase transition.
```

## G-ORCH — Orchestration self-check

Trước MỌI governed executor/reviewer prompt, bắt buộc tự hỏi:

```text
1. Tôi đang dựa trên repository authority (verify lại trực tiếp), KHÔNG PHẢI
   memory?
2. Một ADR mới có THỰC SỰ cần thiết không? (G-ADR-004 check)
3. Đây có PHẢI đúng một bounded transaction không? (G-TXN-001)
4. Prompt size có nằm trong budget không? (§G-BUDGET)
5. Exact identity (blob/version) có được xử lý đúng không? (§G-ID)
6. Tôi có đang tạo một review/micro-transaction KHÔNG CẦN THIẾT không?
7. Tôi đang đóng vai primary orchestrator hay executor/reviewer tại
   session này? Nếu orchestrator — đã cung cấp full next-task prompt/
   Product Owner decision action chưa? Nếu executor/reviewer — tôi có
   đang tự động author full prompt KHÔNG CẦN THIẾT không (mặc định CHỈ
   trả về concise next governed action, trừ khi task yêu cầu hoặc tôi
   đang tường minh LÀM orchestrator)? (G-ORCH-004)
```

```text
G-ORCH-001  Repository mutation report (kết quả tool call thực tế — diff/blob/
            pipe-count) PHẢI được verify lại TRƯỚC KHI accept một transaction là
            hoàn tất — KHÔNG tin report tường thuật mà không kiểm chứng trực
            tiếp.
G-ORCH-002  KHÔNG auto-approval — mọi Approved/Consolidated Stable/Accepted state
            transition đòi hỏi một Product Owner decision tường minh được cung
            cấp trong transaction request.
G-ORCH-003  KHÔNG auto-consolidation — package lifecycle KHÔNG tự chuyển
            Consolidated Stable chỉ vì nội dung "trông sẵn sàng."
G-ORCH-004  Trách nhiệm next-action PHÂN BIỆT theo vai trò tại session
            hiện tại — sau khi một governed task được verify và xác nhận
            hoàn tất:

            1. PRIMARY ORCHESTRATOR (session điều phối chính xuyên suốt
               nhiều task/transaction, vd ChatGPT/primary orchestration
               session): PHẢI cung cấp NGAY hành động tiếp theo cụ thể
               trong CHÍNH response đó — KHÔNG để lại cho một turn sau.
                 - Nếu task tiếp theo do một executor/reviewer khác thực
                   hiện (session/actor khác): response PHẢI bao gồm một
                   prompt hoàn chỉnh, copy-paste được, VÀ chỉ rõ prompt
                   đó phải gửi cho actor/session nào.
                 - Nếu task tiếp theo đòi hỏi một Product Owner decision
                   (KHÔNG phải executor/reviewer action): response PHẢI
                   cung cấp CHÍNH XÁC decision phrase/action mà Product
                   Owner cần trả lời — KHÔNG mô tả chung.

            2. EXECUTOR/REVIEWER (thực hiện một bounded governed
               transaction, vd Claude Code): MẶC ĐỊNH CHỈ trả về một
               `next governed action` súc tích — KHÔNG tự động author
               full copy-paste prompt cho task tiếp theo, TRỪ KHI:
                 (a) transaction hiện tại tường minh yêu cầu prompt đó;
                     HOẶC
                 (b) chính executor/reviewer đó đang hoạt động tường
                     minh LÀM primary orchestrator (KHÔNG PHẢI bounded
                     executor role thông thường).

            3. Rule này CHỈ đòi hỏi CUNG CẤP next action (dạng phù hợp
               với vai trò tại mục 1/2 trên) — KHÔNG tự động thực thi,
               KHÔNG tự approve, KHÔNG tự authorize Phase transition/LIVE
               nào (đúng G-ORCH-002/G-PHASE), TRỪ KHI KHÔNG CÒN governed
               task hợp lệ nào để thực hiện.
```

## Change history

```text
v0.1  2026-08-09  Established — vai trò: `Governance Execution Rulebook
      Structuring Executor`. Formalize Product Owner instruction: mỗi phase PHẢI
      có phase-specific execution rules để cải thiện hiệu quả làm việc VÀ tích
      hợp lesson learned. Global rules established (§Authority–§G-ORCH trên).
      accepted_by: Product Owner, accepted_at: 2026-08-09.
v0.2  2026-08-10  Bổ sung Global rule mới `G-VERIFY-001` ("verify before
      claim") — promote từ Phase 1 Process Retrospective #001
      (`docs/governance/retrospectives/phase1-retrospective-001.md` §8.3
      PROMOTE_GLOBAL), rule giá trị cao nhất rút từ Phase 1: ADR-023's ba
      correction round (v0.2/v0.3/v0.4) VÀ Compatibility Result #001's stale
      v0.7 blob citation CÙNG root cause — taxonomy/registry/blob claim
      asserted TRƯỚC KHI script-verify chống lại ground truth. v0.1 content
      (§Authority–§G-ORCH) KHÔNG đổi. accepted_by: Product Owner,
      accepted_at: 2026-08-10.
v0.3  2026-08-11  Bổ sung Global rule mới `G-ORCH-004` — formalize Product
      Owner instruction nguyên văn: "Sau mỗi task thì tao cần prompt của
      task tiếp theo." Sau khi một governed task verify/xác nhận hoàn tất,
      orchestrator PHẢI cung cấp NGAY next-task action trong CHÍNH response
      đó: một prompt hoàn chỉnh copy-paste được (kèm actor/session nhận)
      nếu task tiếp theo do executor/reviewer khác thực hiện, HOẶC decision
      phrase/action chính xác nếu task tiếp theo cần Product Owner decision
      — KHÔNG dừng ở mô tả roadmap/"tiếp theo sẽ..." chung. Rule KHÔNG tự
      authorize phase transition/LIVE/override Product Owner authority nào
      — CHỈ đòi hỏi CUNG CẤP action, KHÔNG tự thực thi. §G-ORCH self-check
      bổ sung mục 7 tương ứng. v0.1/v0.2 content (§Authority–G-ORCH-003)
      KHÔNG đổi, KHÔNG rule ID nào renumber. accepted_by: Product Owner,
      accepted_at: 2026-08-11.
v0.4  2026-08-11  Bounded semantic correction cho `G-ORCH-004`, đóng
      Product Owner clarification: mandatory full next-task prompt CHỈ
      áp cho PRIMARY ORCHESTRATOR (session điều phối chính, vd ChatGPT),
      KHÔNG tự động áp cho executor/reviewer (vd Claude Code) — tránh
      executor/reviewer report bị kéo dài không cần thiết. Sửa: `G-ORCH-
      004` tách hai vai trò rõ ràng — (1) primary orchestrator VẪN PHẢI
      cung cấp NGAY full prompt/decision action, giữ nguyên yêu cầu gốc
      v0.3; (2) executor/reviewer MẶC ĐỊNH CHỈ trả về một `next governed
      action` súc tích, KHÔNG tự động author full prompt TRỪ KHI task
      hiện tại yêu cầu HOẶC chính executor/reviewer đó đang tường minh
      LÀM orchestrator. §G-ORCH self-check mục 7 sửa tương ứng — phân
      biệt orchestrator (full prompt) khỏi executor/reviewer (concise
      action). KHÔNG đổi `G-ORCH-001`/`G-ORCH-002`/`G-ORCH-003`, KHÔNG
      rule ID nào renumber, KHÔNG rule orchestration mới nào thêm, KHÔNG
      đổi transaction/review/ADR policy. accepted_by: Product Owner,
      accepted_at: 2026-08-11.
v0.5  2026-08-26  Semantic-Sufficiency Clarification — vai trò: `Global
      Execution Rules v0.5 Semantic-Sufficiency Clarification Executor`.
      Product Owner decision nguyên văn: "APPROVE GLOBAL EXECUTION RULES
      V0.5 SEMANTIC-SUFFICIENCY CLARIFICATION AT BOUNDARY
      edfa1e2c9f30b8bc9fdf389f9821bf787587b04c, WITH NO NEW GOVERNANCE
      PROCESS, NO NEW RULE ID, AND NO ADR." Motivating lesson: the ADR-036/
      Package 1.1 alignment sequence (ADR-036 v0.1→v0.3 bounded corrections,
      the Package 1.1 alignment transaction, then its own v1.4→v1.5 bounded
      correction for two non-blocking Review-B Minors, then reconsolidation)
      showed a pattern of documentation-only/non-blocking findings each
      triggering a full standalone bounded-correction-plus-re-review round,
      consistent with `G-REV-001`/`G-REV-004`'s letter but producing more
      process churn than the actual semantic risk warranted. Adds a
      NON-NORMATIVE INTERPRETATION — Semantic Sufficiency block immediately
      after `G-REV-001..004` (no new `G-*` rule ID) clarifying, WITHOUT
      creating a new gate: (1) `G-REV-001`/`G-REV-004` optimize for real
      semantic risk reduction, not perfect prose or zero-Minor documents;
      (2) absence of unresolved Blocker/Major does NOT itself approve an
      artifact, all existing lifecycle/independent-review/Product Owner
      requirements still apply; (3) a documentation-only issue should not
      by default trigger a standalone correction/re-review transaction when
      higher authority already resolves the correct semantics; (4) such an
      issue may be carried forward or folded into an already-required
      future transaction when safe (`G-TXN-003` precedent); (5) escalation
      remains appropriate when the issue can misstate real authority,
      contract/implementation behavior, auditability/reproducibility,
      safety, or when Product Owner explicitly requires correction; (6)
      zero Minor is NOT an additional ADR/package/review exit criterion
      unless a higher-authority rule explicitly requires it; (7) this
      interpretation does not weaken `G-REV-002`, Independent Review B, or
      any Blocker/Major remediation requirement. This is a clarification of
      EXISTING rules, NOT a new process — `G-REV-001..004` wording, all
      other rule IDs/wording, the Authority hierarchy, ADR Scope Rule,
      review eligibility, and lifecycle gates are all unchanged, byte-
      identical. No ADR authored. accepted_by: Product Owner, accepted_at:
      2026-08-26.
```
