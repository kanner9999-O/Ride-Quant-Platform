---
id: phase-1.5-rules
title: "Phase 1.5 — Engineering Foundation: Execution Rules"
version: "0.2"
operational_state: EFFECTIVE
owner: Product Owner
accepted_by: Product Owner
accepted_at: "2026-08-10"
created_at: "2026-08-10"
phase: 1.5
phase_name: "Engineering Foundation"
---

# Phase 1.5 — Engineering Foundation: Execution Rules

**Vai trò của tài liệu này:** per-phase operational execution rule cho Phase 1.5 — Engineering Foundation (Chapter 14 §14.2: Monorepo · Coding Standard · Naming · Logging · Config · Error Handling · Testing · CI/CD; "tài liệu SỐNG, sửa qua ADR"), đúng khung `docs/governance/phases/phase-rules-template.md`. Document này LÀ `EFFECTIVE` kể từ Product Owner acceptance (2026-08-10, xem §Product Owner acceptance dưới) — v0.2 semantic candidate (Review A `CLEAN` sau khi đóng `EF-RULES-A-MAJ-01`, Independent Review B `READY_FOR_PRODUCT_OWNER_ACCEPTANCE`, Blocker 0/Major 0/Minor 0) accepted nguyên vẹn, KHÔNG sửa rule semantics nào tại transaction acceptance này.

**Stable-ID prefix `EF-` (KHÔNG dùng `P15-`):** verify trực tiếp (đúng `G-VERIFY-001`) tại chính transaction này cho thấy `P15-` ĐÃ mang nghĩa khác trong repository — `P15-BCC-MAJ-01`/`P15-A-MAJ-01..02`/`P15-A-MIN-01..02` (CHANGELOG.md, MANIFEST.md) là finding ID của **Package 1.5** (`database-architecture.md` v0.3, một architecture package BÊN TRONG Phase 1), hoàn toàn khác **Phase 1.5** (Engineering Foundation, Phase kế tiếp sau Phase 1). Tái dùng `P15-` cho rule ID tại đây sẽ vi phạm nguyên tắc "Stable rule ID KHÔNG BAO GIỜ tái sử dụng cho một nghĩa khác" (`phase-rules-template.md` §Ràng buộc chung). Rule tại đây dùng prefix `EF-` (Engineering Foundation) để tránh collision này tường minh.

```text
phase:              1.5
phase_name:         Engineering Foundation
operational_state:  EFFECTIVE
accepted_by:        Product Owner
accepted_at:        2026-08-10
```

## Product Owner acceptance

```text
Quyết định: "I accept Phase 1.5 Execution Rules v0.2." (Product Owner,
  2026-08-10)

Reviewed semantic candidate (KHÔNG đổi bởi acceptance transaction này):
  version:  0.2
  blob:     8b2380a64053ff58743d8d07b4ea775c7d1c1a6e
  Review A:               CLEAN (sau khi đóng EF-RULES-A-MAJ-01)
  Independent Review B:   READY_FOR_PRODUCT_OWNER_ACCEPTANCE
  Blocker / Major / Minor: 0 / 0 / 0

Resulting lifecycle-record (blob SAU khi transaction acceptance này edit
  operational_state/accepted_by/accepted_at/§Product Owner acceptance/
  §Change history — prose/metadata field, KHÔNG rule semantics):
  version:              0.2 (KHÔNG bump — pure mechanical acceptance,
                        cùng pattern ADR-023 v0.5 approval, Chapter 11
                        §11.4)
  operational_state:    DRAFT -> EFFECTIVE
  blob:                 xem MANIFEST.md row cho blob chính xác sau commit
                        này (đúng G-ID-001 — reviewed semantic blob ≠
                        resulting lifecycle-record blob, PHẢI phân biệt
                        tường minh)

KHÔNG rule EF-* nào sửa semantics tại transaction acceptance này (byte-
  equivalent ngoài vùng operational_state/accepted_by/accepted_at/§Product
  Owner acceptance/§Change history). Kể từ acceptance này: Phase 1.5
  substantive governed work KHÔNG còn bị block bởi rule-acceptance
  prerequisite (đúng phase-rules-template.md's mandatory rule) — CÁC
  prerequisite KHÁC (Phase 1.5 DoD, execution plan...) KHÔNG được suy diễn
  là satisfied bởi transaction này, CHƯA tồn tại, cần transaction riêng.
```

## Inherited Global Rules

Toàn bộ `docs/governance/execution-rules.md` v0.2 (`G-AUTH`/`G-VERIFY`/`G-ADR`/`G-TXN`/`G-REV`/`G-BUDGET`/`G-ID`/`G-QG`/`G-PHASE`/`G-ORCH`) áp dụng NGUYÊN VẸN, bao gồm `G-VERIFY-001`. Tài liệu này CHỈ thêm rule bổ sung/siết chặt riêng cho Phase 1.5, KHÔNG redefine bất kỳ Global rule nào.

## Lessons from Phase 1 (nguồn cho các control dưới)

```text
- Retrospective §4/§6 (docs/governance/retrospectives/phase1-
  retrospective-001.md): root cause chung của Phase 1's finding lớn nhất
  LÀ registry/taxonomy/blob claim asserted TRƯỚC KHI script-verify. Phase
  1.5 sinh ra một LOẠI claim mới cùng risk profile: exact tool/library/
  dependency VERSION, CI pipeline config, lint/format rule — cần cùng
  discipline, tightened riêng cho loại claim này (§EF-VERIFY dưới).
- Retrospective §5/§8.2: MANIFEST compact-state rule (G-ID-001/G-BUDGET-
  001) tồn tại nhưng KHÔNG enforce nhất quán (8,512-từ single cell). Rule
  ĐÚNG, cần mechanical enforcement riêng Phase 1.5 cũng như đã làm cho
  Phase 2 (`P2-BUDGET-001`) — Phase 1.5 dự kiến sinh nhiều bookkeeping
  entry (mỗi convention/tool decision) nên risk này áp dụng tương tự.
- Retrospective §7: governance-chain self-replication (ADR-023 5-version
  chain) — containment scope theo "số ADR" KHÔNG chặn correction-round
  amplification BÊN TRONG một artifact đơn. Rule tương đương cho Phase
  1.5 (`EF-ADR-002`) áp dụng cho MỌI Foundation artifact (convention doc/
  config/CI pipeline), KHÔNG CHỈ ADR — vì Phase 1.5 hiếm khi sinh ADR
  (Chapter 3 §"Nguyên tắc bắt buộc" ưu tiên convention/version hóa hơn
  ADR), correction chain thực tế nhiều khả năng xảy ra trên convention
  document/config, không phải ADR.
- Chapter 3 §"Nguyên tắc bắt buộc" (Engineering Principles, Locked v1.4):
  Engineering Foundation KHÔNG miễn trừ ADR Scope Rule (Chapter 0 §4b) —
  NHƯNG ADR CHỈ bắt buộc cho thay đổi thuộc diện ADR Required; ADR
  Optional/Not Required (refactor không đổi behavior/contract, style/
  tooling convention) KHÔNG cần ADR, chỉ cần lịch sử thay đổi rõ ràng
  (commit/CHANGELOG). Nguồn trực tiếp cho `EF-ADR-001`.
- Chapter 14 §14.2 (Locked v1.6): Phase 1.5 scope = Monorepo · Coding
  Standard · Naming · Logging · Config · Error Handling · Testing ·
  CI/CD — KHÔNG liệt kê architecture/module-taxonomy/domain content nào.
  Nguồn trực tiếp cho `EF-TXN-001` (foundation-only scope).
- `EF-TXN-002` (batching) và phần "new work-type" của `EF-REV-001` KHÔNG
  có lesson Phase 1 trực tiếp — Phase 1 LÀ architecture, không sinh
  tooling/config/CI artifact nào. Cho phép bởi exception clause của
  `phase-rules-template.md` §5 ("control mang tính containment/ceiling
  hiển nhiên tại thời điểm phase mở"), cùng logic đã dùng cho
  `P2-PROTOTYPE-001`.
```

## EF-ADR — Phase 1.5 ADR controls

```text
EF-ADR-001  Convention/configuration trước ADR; không reopen architecture
            thiếu conflict cụ thể: đúng Chapter 3 §"Nguyên tắc bắt buộc"
            (Locked v1.4) + Chapter 0 §4b — Phase 1.5 change mặc định đi
            qua convention/config version hóa + lịch sử rõ ràng (commit/
            CHANGELOG), KHÔNG tự động mở ADR. ADR CHỈ bắt buộc khi thay
            đổi thuộc diện ADR Required (Platform Invariant/Event Schema/
            Module Taxonomy/dependency graph/Governance process/quyết
            định >1 module hoặc khó đảo ngược). Phase 1 architecture đã
            `Approved`/Gate 2 `PASSED` KHÔNG được reopen bởi bất kỳ
            Foundation transaction nào TRỪ KHI một architecture conflict
            THẬT SỰ cụ thể được phát hiện (KHÔNG phải preference/style
            khác biệt) VÀ existing authority/alignment/convention KHÔNG
            THỂ resolve nó (đúng G-ADR-001/G-ADR-004, cùng logic
            P1-ADR-002's "existing authority trước ADR mới").
EF-ADR-002  Correction-chain circuit breaker (Foundation artifact): nếu
            MỘT convention document/config/CI pipeline definition đạt BA
            (3) correction round liên tiếp KHÔNG stabilize — dừng NGAY,
            KHÔNG author round thứ 4. Thay vào đó: (1) root-cause
            consolidation transaction bounded; (2) re-resolve current
            tool/version/config ground truth trực tiếp (`EF-VERIFY-001`);
            (3) một consolidated correction DUY NHẤT tiếp theo. Áp dụng
            CHO MỌI Foundation artifact (KHÔNG CHỈ ADR, khác phạm vi
            `P2-ADR-CHAIN-001` vì Phase 1.5 hiếm sinh ADR — xem
            `EF-ADR-001`).
```

## EF-TXN — Phase 1.5 transaction controls

```text
EF-TXN-001  Foundation-only scope: mỗi transaction Phase 1.5 CHỈ thiết
            lập nội dung nằm trong Chapter 14 §14.2's Phase 1.5 scope
            list (Monorepo/Coding Standard/Naming/Logging/Config/Error
            Handling/Testing/CI-CD) — KHÔNG vượt ra ngoài danh sách này
            (KHÔNG mở rộng scope vượt Roadmap authority). Trong đúng
            danh sách đó, CHỈ thiết lập mức foundation hợp lý cần cho
            downstream platform phase/work ĐÃ BIẾT theo Chapter 14 §14.2
            sequence (Phase 2 Product Prototype VÀ các phase/work biết
            trước khác sau đó — KHÔNG CHỈ riêng nhu cầu của Phase 2) —
            KHÔNG gold-plating/tooling suy đoán trước (speculative
            capability chưa có nhu cầu cụ thể từ bất kỳ downstream
            phase/work đã biết nào).
            [v0.2 (2026-08-10), đóng `EF-RULES-A-MAJ-01`: v0.1 wording
            "CHỈ mức tối thiểu cần cho phase kế tiếp" đọc được như CHỈ
            giới hạn theo nhu cầu riêng của Phase 2 — sai; Phase 1.5
            scope xác định bởi Roadmap §14.2's 8-category list, KHÔNG
            bởi nhu cầu của một phase kế tiếp cụ thể nào.]
EF-TXN-002  Batch related engineering-foundation work: các quyết định
            liên quan trong CÙNG một category (vd toàn bộ Coding
            Standard, hoặc toàn bộ CI/CD pipeline) nên gộp vào MỘT
            transaction bounded theo category, KHÔNG chia nhỏ theo từng
            file/rule riêng lẻ theo default — đúng G-TXN-001 (một primary
            decision/transaction) áp cho CẤP category, KHÔNG cấp mỗi
            config key. Category riêng lẻ CÓ THỂ tách transaction riêng
            khi rủi ro/semantic khác biệt đủ lớn (vd đổi ngôn ngữ/
            framework core khác hẳn convention nhỏ).
```

## EF-REV — Phase 1.5 review controls

```text
EF-REV-001  Review depth tỷ lệ semantic risk (đúng Global G-REV-001),
            table hóa riêng cho loại artifact Phase 1.5 hay gặp:

              convention/config quyết định ảnh hưởng nhiều module hoặc
              khó đảo ngược (vd chọn monorepo tool, CI provider)
                -> full review tương xứng mức ảnh hưởng (KHÔNG bắt buộc
                   full Review A/B như ADR nếu KHÔNG thuộc ADR Required,
                   nhưng KHÔNG chỉ validation qua loa)

              mechanical/tooling/config change (version bump, lint rule
              thêm, CI step thêm, format style)
                -> deterministic verification (`EF-VERIFY-001`) — chạy/
                   kiểm trực tiếp tool/config, KHÔNG cần reviewer thứ hai
                   độc lập nếu ground truth reproduce được chính xác

              bookkeeping/documentation update (MANIFEST/CHANGELOG entry
              cho quyết định đã có)
                -> validation only, TRỪ KHI chính entry đó lộ ra một
                   semantic conflict chưa từng thấy

            KHÔNG review-round amplification khi KHÔNG có Major/Blocker
            mới hoặc semantic change thật (đúng G-REV-004).
```

## EF-BUDGET — Phase 1.5 prompt/efficiency controls

```text
EF-BUDGET-001  Global §G-BUDGET áp dụng nguyên vẹn (KHÔNG redefine
               ceiling). Bổ sung mechanical enforcement riêng Phase 1.5
               (cùng lý do đã tighten cho `P2-BUDGET-001`, retrospective
               §5/§8.2):
                 - MANIFEST table cell PHẢI ≤ 1,500 từ tại thời điểm MỖI
                   edit — vượt ngưỡng BẮT BUỘC compact-rewrite (move
                   history sang CHANGELOG.md) TRƯỚC KHI transaction được
                   coi hoàn tất.
                 - Phase 1.5 prompt mặc định cấu trúc delta-only: Goal /
                   Baseline / Required delta / Forbidden changes /
                   Validation / Report.
                 - MANIFEST LÀ current-state index cho từng convention/
                   tool category (version/status hiện tại), KHÔNG PHẢI
                   narrative log — lịch sử chi tiết thuộc CHANGELOG.md.
```

## EF-VERIFY — Tool/version/config verification (siết `G-VERIFY-001` riêng Phase 1.5)

```text
EF-VERIFY-001  Trước khi ghi nhận bất kỳ exact tool/library/dependency
               version, CI provider/step config, lint/format rule
               version, hay monorepo tool version vào decision content
               (MANIFEST/CHANGELOG/convention doc) — PHẢI verify TRỰC
               TIẾP (chạy tool/kiểm lockfile/package manifest thực tế,
               KHÔNG suy diễn từ memory/tên phiên bản "thường dùng") tại
               CHÍNH transaction đó, đúng `G-VERIFY-001` áp dụng cho loại
               claim cụ thể của Phase 1.5.
```

## Known process risks (Phase 1.5)

```text
- Architecture-reopening-via-tooling-preference risk: một quyết định
  tooling/convention có thể ngầm kéo theo yêu cầu đổi module boundary/
  dependency graph đã Approved — đóng bởi `EF-ADR-001` (yêu cầu conflict
  cụ thể, KHÔNG preference).
- Correction-round self-replication trên convention document/config
  (KHÔNG cần là ADR để risk này xảy ra) — đóng bởi `EF-ADR-002`.
- Config/tool-version claim asserted từ memory thay vì verify thực tế
  (cùng root cause class với Phase 1's taxonomy/blob finding, retrospective
  §4) — đóng bởi `EF-VERIFY-001`.
- Category fragmentation risk: mỗi rule/file nhỏ trong một category
  (Coding Standard, CI/CD...) trở thành transaction governed riêng —
  đóng bởi `EF-TXN-002` batching.
- MANIFEST/prompt budget drift (đúng pattern đã quan sát Phase 1) — đóng
  bởi `EF-BUDGET-001`.
```

## Gate-path controls

```text
Trình tự dự kiến tới Approval Gate của chính Phase 1.5 (Phase 1.5 LÀ một
  Phase đầy đủ, có Approval Gate riêng — Chapter 14 §14.1), SAU KHI
  Product Owner accept văn bản này (chuyển DRAFT -> EFFECTIVE) VÀ Phase
  1.5 substantive work hoàn tất theo scope §14.2:
    Product Owner acceptance của chính rule file này (điều kiện tiên
      quyết, §Product Owner acceptance trên)
    → Phase 1.5 Foundation work theo batch (cadence EF-TXN-002)
    → Phase 1.5 DoD accepted (transaction riêng, KHÔNG author tại đây)
    → Phase-level Gate review(s) đúng Chapter 12 yêu cầu
    → Product Owner Approval Gate decision cho Phase 1.5
  KHÔNG reopen Phase 1 architecture giữa các bước này TRỪ KHI một
  conflict thật được phát hiện (`EF-ADR-001`). KHÔNG author Phase 2 rule/
  authorization nào tại Phase 1.5 — Phase 2 vẫn chờ đúng sequence Chapter
  14 §14.2 (Phase 1.5 phải Approval Gate xong trước).
```

## Retrospective requirement

```text
EF-RETRO-001  TRƯỚC KHI Phase 2 substantive work bắt đầu, PHẢI thực hiện
              một Phase 1.5 process retrospective, cùng cấu trúc tối
              thiểu `P1-RETRO-001` (wasted transaction, avoidable ADR,
              repeated review cycle, prompt-size problem, bookkeeping
              defect, rule hữu ích/thất bại, rule nên promote Global,
              Phase-2-specific control mới/refine) — CỘNG THÊM đánh giá
              riêng hiệu quả của `EF-ADR-001`/`EF-ADR-002`/`EF-TXN-001`/
              `EF-TXN-002`/`EF-REV-001`/`EF-BUDGET-001`/`EF-VERIFY-001`.
              Retrospective LÀ điều kiện TRƯỚC substantive Phase 2 work —
              KHÔNG tự động đóng, đòi hỏi một transaction riêng thực hiện
              nó. [LƯU Ý: Phase 2 substantive work có HAI retrospective
              tiên quyết theo sequence Chapter 14 §14.2 — `P1-RETRO-001`
              (Phase 1, đã COMPLETE) VÀ `EF-RETRO-001` (Phase 1.5, đây) —
              cả hai PHẢI COMPLETE, KHÔNG cái nào miễn trừ cái kia.]
```

## Change history

```text
v0.1  2026-08-10  Authored (DRAFT) — vai trò: `Phase 1.5 Rules Authoring
      Executor`. Derives controls từ Phase 1 Process Retrospective #001
      (`../retrospectives/phase1-retrospective-001.md`), Chapter 3
      §"Nguyên tắc bắt buộc" (Engineering Foundation ADR Scope Rule), và
      Chapter 14 §14.1/§14.2 (Phase 1.5 = full Phase, scope list). Bảy
      rule: `EF-ADR-001` (convention trước ADR, no reopening thiếu
      conflict), `EF-ADR-002` (correction-chain circuit breaker, mọi
      Foundation artifact), `EF-TXN-001` (foundation-only scope),
      `EF-TXN-002` (batch theo category), `EF-REV-001` (risk-proportional
      review table), `EF-BUDGET-001` (mechanical MANIFEST/prompt budget),
      `EF-VERIFY-001` (tighten G-VERIFY-001 cho tool/version/config
      claim). Prefix `EF-` chọn tường minh để tránh collision với `P15-`
      (đã mang nghĩa Package 1.5, khác Phase 1.5 — xem banner đầu tài
      liệu). `operational_state: DRAFT` — KHÔNG accepted_by/accepted_at
      fabricate; Product Owner acceptance CHƯA thực hiện, đòi hỏi
      transaction riêng trước khi Phase 1.5 substantive work được phép
      bắt đầu.
v0.2  2026-08-10  Bounded semantic correction, đóng `EF-RULES-A-MAJ-01`.
      `EF-TXN-001` wording v0.1 ("CHỈ mức tối thiểu cần cho phase kế
      tiếp") đọc được như CHỈ giới hạn Phase 1.5 theo nhu cầu riêng của
      Phase 2 — sai. Sửa: giữ nguyên full Roadmap §14.2 8-category scope
      (Monorepo/Coding Standard/Naming/Logging/Config/Error Handling/
      Testing/CI-CD), đổi tiêu chí "tối thiểu" sang "foundation hợp lý
      cần cho downstream platform phase/work ĐÃ BIẾT" (KHÔNG CHỈ riêng
      Phase 2), giữ nguyên anti-gold-plating constraint, KHÔNG mở rộng
      scope vượt Roadmap authority. KHÔNG rule ID nào thêm/xóa, KHÔNG
      rule khác (`EF-ADR-001`/`EF-ADR-002`/`EF-TXN-002`/`EF-REV-001`/
      `EF-BUDGET-001`/`EF-VERIFY-001`/`EF-RETRO-001`) sửa semantic.
      `operational_state` VẪN `DRAFT`, accepted_by/accepted_at VẪN
      `PENDING` — KHÔNG mark EFFECTIVE tại transaction này.
ACCEPTANCE  2026-08-10  Product Owner acceptance — mechanical lifecycle
      recording, vai trò: `Phase 1.5 Rules Acceptance Recorder`. Quyết
      định: "I accept Phase 1.5 Execution Rules v0.2." Reviewed semantic
      candidate: v0.2, blob `8b2380a64053ff58743d8d07b4ea775c7d1c1a6e`
      (Review A `CLEAN` sau `EF-RULES-A-MAJ-01`, Independent Review B
      `READY_FOR_PRODUCT_OWNER_ACCEPTANCE`, Blocker/Major/Minor 0/0/0).
      `operational_state: DRAFT -> EFFECTIVE`, `accepted_by: PENDING ->
      Product Owner`, `accepted_at: PENDING -> "2026-08-10"`. `version`
      KHÔNG bump (pure mechanical acceptance, cùng pattern ADR-023 v0.5
      approval, Chapter 11 §11.4) — VẪN `0.2`. KHÔNG rule EF-* nào sửa
      semantics (thay đổi CHỈ nằm ở operational_state/accepted_by/
      accepted_at/§Product Owner acceptance/§Change history/preamble
      lifecycle note — đúng G-ID-001, reviewed semantic blob
      `8b2380a64...` ≠ resulting lifecycle-record blob sau transaction
      này). Phase 1.5 substantive governed work KHÔNG còn bị block bởi
      rule-acceptance prerequisite — prerequisite KHÁC (DoD, execution
      plan) CHƯA tồn tại, KHÔNG suy diễn satisfied. KHÔNG authorize
      Phase 2/LIVE, KHÔNG reopen Phase 1.
```
