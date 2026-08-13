---
id: phase1.5-retrospective-001
title: "Phase 1.5 Process Retrospective #001"
retrospective_version: "1.0"
retrospective_status: Final
performed_at: "2026-08-13"
satisfies_rule: EF-RETRO-001
phase1_5_retrospective_status: COMPLETE
phase2_substantive_work: NOT_YET_AUTHORIZED
---

# Phase 1.5 Process Retrospective #001

**Vai trò của tài liệu này:** đây LÀ Phase 1.5 process retrospective (`governance/phases/phase-1.5-rules.md` §Retrospective requirement, `EF-RETRO-001`) — KHÔNG một ADR, KHÔNG architecture authoring, KHÔNG sửa Phase 1.5 Approval Gate decision đã record (`MANIFEST.md` "Phase 1.5 Approval Gate — Decision" section, byte-identical), KHÔNG một Phase 2 authorization transaction. Tài liệu này CHỈ đánh giá THẬT SỰ Phase 1.5 execution history (evidence-based, KHÔNG generic process advice), classify lesson theo đúng tám hạng mục tối thiểu của `P1-RETRO-001`'s structure, CỘNG THÊM đánh giá riêng hiệu quả của bảy rule `EF-ADR-001`/`EF-ADR-002`/`EF-TXN-001`/`EF-TXN-002`/`EF-REV-001`/`EF-BUDGET-001`/`EF-VERIFY-001` (`EF-RETRO-001`'s yêu cầu bổ sung riêng).

## 1. Method

```text
Evidence source: git log (57 Phase 1.5 commit, 196539c58a9413dd59497e40
  75ce23a84abb09f1..2e12b9bfbb3332a5df964eb6620430954f8e8bc0), docs/
  CHANGELOG.md (lines 1-7255, Phase 1.5 window), docs/MANIFEST.md
  (current state), git blob/word-count inspection trực tiếp cho
  lifecycle/blob/budget claim, docs/governance/phases/phase-1.5-rules.md
  (governing rule text), docs/engineering/*.md + docs/adr/ADR-024.md..
  ADR-030.md (final Approved state).
KHÔNG generic advice — mọi finding dưới đây pin bằng chứng cụ thể (commit
  SHA, finding ID, số liệu đo được, trực tiếp từ repository, KHÔNG từ
  memory).
```

## 2. Wasted/unnecessary transactions

```text
Đánh giá: KHÔNG một transaction NÀO trong 57 commit LÀ hoàn toàn thừa
  (mỗi transaction đóng đúng một finding/bounded scope cụ thể hoặc thực
  hiện đúng một mechanical lifecycle step — KHÔNG scope creep phát hiện
  qua toàn bộ Phase 1.5, EF-TXN-001 giữ vững 100%, xem §8.3).
Trường hợp đáng chú ý (KHÔNG wasted, NHƯNG rule churn thật): commit
  `4091c0c` ("Add Global rule G-ORCH-004: mandatory next-task prompt")
  bị bounded-corrected NGAY sau đó bởi `2990fc0` ("scope G-ORCH-004 to
  primary orchestrator role") — CÙNG session, rule mis-scoped lần đầu
  (áp cho MỌI role, kể cả executor/reviewer) rồi phải sửa hẹp lại. Rule
  gốc KHÔNG bị thu hồi (giữ nguyên ý tưởng), CHỈ scope bị hẹp lại — giá
  trị durable VẪN giữ (rule hiện hành đúng), NHƯNG đây LÀ ví dụ rõ nhất
  của "author trước, scope-check sau" thay vì ngược lại.
Trường hợp đáng chú ý thứ hai (repeated correction, KHÔNG wasted nhưng
  preventable): Logging convention correction v0.2 (`5a82385`, đóng
  `EF-LOG-A-MAJ-01`/`02`/`03`) KHÔNG đóng triệt để `EF-LOG-A-MAJ-02` —
  một correction v0.3 riêng (`97d4ce9`, "close remaining EF-LOG-A-MAJ-02
  leak") cần thiết để đóng nốt phần còn sót. Đây LÀ một preventable
  authoring defect (first-pass fix không đủ triệt để), KHÔNG phải
  reviewer disagreement hay finding mới.
```

## 3. Avoidable ADRs / ADR candidates

```text
7 ADR tạo (ADR-024..ADR-030), MỘT category (Testing) KHÔNG tạo ADR
  (`ADR_NOT_REQUIRED`, xác nhận qua một ADR Scope Check transaction
  riêng, read-only, TRƯỚC KHI author testing.md).
Phân biệt tường minh: Chapter 3 §3.2 (Engineering Foundation framework,
  11 mục) CHỈ pre-resolve baseline-existence cho BA mục (Testing,
  Versioning, Documentation Convention) qua một carve-out sentence rõ
  ràng — TÁM mục còn lại (bao gồm cả bảy category Phase 1.5 tạo ADR)
  KHÔNG có pre-resolution đó. Với MỖI trong bảy category đó, quyết định
  "một cross-module [X] Convention baseline" tự nó thỏa Chapter 0 §4b's
  disjunctive-OR ADR Scope Rule qua nhánh "affects >1 module" (một
  convention baseline áp dụng CHO TOÀN BỘ monorepo, theo định nghĩa ảnh
  hưởng nhiều hơn một module) — KHÔNG một trường hợp nào trong bảy đây
  LÀ tùy chọn/hypothetical, mỗi ADR đều actually-triggered.
Testing: dedicated ADR Scope Check (read-only, TRƯỚC KHI author) xác
  nhận Chapter 3 §3.2's carve-out sentence áp dụng trực tiếp — KHÔNG cần
  ADR. Đây LÀ ví dụ rõ nhất trong toàn bộ Phase 1.5 của ADR Scope
  checking NGĂN được ADR inflation (nếu KHÔNG check trước, có thể đã
  tạo ADR-031 không cần thiết).
Kết luận: KHÔNG ADR nào avoidable trong bảy ADR đã tạo — VÀ Testing's
  ADR_NOT_REQUIRED cũng đúng, KHÔNG một ADR nào bị bỏ sót đáng lẽ cần.
  ZERO ADR inflation, ZERO ADR thiếu.
```

## 4. Repeated review/correction churn và root cause

```text
Bằng chứng định lượng: 19 bounded-correction-round commit / 57 tổng
  commit (~33%). Artifact churn cao nhất: `monorepo.md` — 5 version
  (v0.1 draft → v0.2 correction `EF-MONO-A-MAJ-01` [Review A] → v0.3
  correction `EF-MONO-B-MAJ-01`/`02` [Independent Review B — HAI finding
  KHÁC finding của Review A] → v0.4 align-to-Approved-ADR-024 [KHÔNG
  phải correction, semantic sync] → v0.5 correction
  `EF-MONO-ADR024-A-MAJ-01`), so với 2 version cho hầu hết category
  khác (draft → 1 correction → approved).
Root cause monorepo.md's churn: KHÔNG một root cause đơn lẻ giống Phase
  1's "assert trước, verify sau" — thay vào đó LÀ ba finding-class riêng
  biệt (ADR-scope-disposition wording sai, README example implied
  settled assignment sai, và một finding phát sinh SAU KHI ADR-024 được
  Approved buộc convention phải align lại) — mỗi round đóng đúng MỘT
  finding-class, KHÔNG lặp lại cùng lỗi (khác Phase 1's ADR-023, nơi BA
  round liên tiếp CÙNG một root cause). Đây LÀ churn hợp lý (mỗi vấn đề
  thật, riêng biệt), KHÔNG phải churn do thiếu kỷ luật.
ADR-030 (CI/CD): 2 correction round liên tiếp (v0.1→v0.2 đóng
  `ADR030-A-MAJ-01` [Review A, flaky-test authority misattribution]
  →v0.3 đóng `ADR030-B-MAJ-01` [Independent Review B trên v0.2, LIVE-
  authority overreach — unsupported attribution tới ADR-007/account.md]).
  Hai finding này THUỘC hai class hoàn toàn khác nhau — bằng chứng trực
  tiếp cho "Independent Review B tìm defect khác Review A" (xem §9).
Reviewer disagreement: KHÔNG một trường hợp nào quan sát được trong
  Phase 1.5 — Independent Review B luôn HOẶC xác nhận CLEAN (0 new
  finding) HOẶC bổ sung finding MỚI, KHÔNG BAO GIỜ overrule một verdict
  CLEAN đã có của Review A.
Factual/provenance churn (Minor, pure stale wording, KHÔNG semantic):
  `EF-CONFIG-B-MIN-01` (stale "v0.1" wording), `EF-ERR-B-MIN-01` (stale
  "v0.1" wording, nhiều mục), `EF-MONO-ADR024-B-MIN-01` (v0.4-era
  provenance wording) — 3/9 accepted residual (33%) LÀ pure provenance
  staleness, KHÔNG semantic/authority defect.
```

## 5. Prompt-size / EF-BUDGET-001 (MANIFEST cell word count)

```text
Bằng chứng định lượng (word count trực tiếp mỗi MANIFEST table cell
  hiện tại): 8 Engineering Foundation convention row (dòng 208-215) —
  128 đến 170 từ/cell. 7 ADR row (ADR-024..030, dòng 69-75) — 141 đến
  169 từ/cell. Phase DoD table row (Phase 0/1/1.5, dòng 235-237) — 538
  đến 636 từ/cell (lớn nhất repository hiện tại, NHƯNG vẫn dưới xa
  ceiling 1,500 từ).
So sánh trực tiếp Phase 1: dòng dài nhất Phase 1 (ADR-023) LÀ 8,512 từ
  trong MỘT cell — gấp ~13-60x mọi cell Phase 1.5. `EF-BUDGET-001`
  (siết `G-ID-001`/`G-BUDGET-001` cho riêng Phase 1.5, đề xuất
  `P2-BUDGET-001` từ Phase 1 retrospective) giữ vững HOÀN TOÀN — KHÔNG
  một cell nào vượt ceiling, KHÔNG cần compact-rewrite emergency nào
  xuyên suốt 57 transaction.
Kết luận: `EF-BUDGET-001` LÀ minh chứng rõ ràng nhất "TIGHTEN" từ Phase
  1 retrospective (mechanical enforcement thay vì prose reminder) hoạt
  động ĐÚNG — sự khác biệt định lượng (128-636 từ so với 8,512 từ) LÀ
  bằng chứng trực tiếp.
```

## 6. Lifecycle/bookkeeping defects

```text
KHÔNG một "reviewed semantic blob ≠ resulting lifecycle-record blob"
  conflation nào phát hiện trong 57 commit (khác Phase 1's Result #001
  finding) — MỌI approval/acceptance transaction phân biệt tường minh
  hai blob (G-ID-001), verified trực tiếp mỗi lần.
MỘT lỗi transcription blob PHÁT HIỆN TRỰC TIẾP trong chính session ghi
  nhận Phase 1.5 Approval Gate decision (transaction NGAY TRƯỚC
  retrospective này): khi soạn "Phase 1.5 Approval Gate — Decision"
  section, blob post-acceptance của `phase-1.5-dod.md` bị gõ sai một
  ký tự khi line-wrap thủ công (`...2193c2b` thay vì `...2193b8c` —
  transposition lỗi trong wrapping, KHÔNG phải copy-paste từ nguồn sai).
  Lỗi được bắt VÀ sửa NGAY (Python string-concatenation verify trực
  tiếp cả ba blob trước khi commit) — TRƯỚC KHI commit, KHÔNG bao giờ
  trở thành authoritative sai. Đây LÀ bằng chứng trực tiếp, sống, cho
  hypothesis "transaction verification prevented executor reports from
  becoming implicit authority" (xem §9) — verify-before-commit discipline
  hoạt động ĐÚNG THIẾT KẾ, dù chính executor (tôi) LÀ nguồn lỗi ban đầu.
Residual tracking: chín residual Minor accepted xuyên suốt Phase 1.5
  (`EF-MONO-ADR024-B-MIN-01`, `ADR026-A-MIN-01`, `EF-NAME-A2-MIN-01`,
  `EF-NAME-B-MIN-01`, `ADR027-B-MIN-01`, `EF-CONFIG-B-MIN-01`,
  `EF-ERR-B-MIN-01`, `EF-DOD-B-MIN-01`, `EF-DOD-B-MIN-02`) — verified
  KHÔNG một cái nào bị đóng sai ("closed") qua git-grep trực tiếp mỗi
  transaction tiếp theo trích dẫn chúng; carry-forward wording nhất
  quán ("OPEN — accepted non-blocking") xuyên suốt.
current_phase / next-phase authorization separation: giữ vững đúng
  pattern Phase 1's Gate 2 (xem §7 dưới) — Phase 1.5 Approval Gate
  decision (2e12b9b) KHÔNG tự động đổi `current_phase`, đúng thiết kế.
```

## 7. current_phase / next-phase authorization separation (governance-pattern reuse)

```text
Phase 1.5's Approval Gate decision transaction áp dụng ĐÚNG pattern đã
  thiết lập tại Phase 1's Gate 2 (`current_phase` KHÔNG tự động chuyển
  khi Gate/Approval PASSED, chờ một "Start Authorization" transaction
  riêng biệt SAU retrospective) — pattern này chính nó LÀ một Phase-1
  lesson được tái sử dụng thành công, KHÔNG một finding mới, NHƯNG xác
  nhận giá trị của việc pin pattern này thành precedent tường minh
  trong MANIFEST (thay vì để executor tương lai tự suy luận lại).
KHÔNG governance-chain self-replication kiểu ADR-023 (5-version SAME-
  root-cause chain) quan sát được trong Phase 1.5 — churn cao nhất
  (monorepo.md, §4) LÀ multi-root-cause hợp lý, KHÔNG same-root-cause
  lặp lại. `EF-ADR-002`'s circuit breaker (3 correction round LIÊN TỤC
  không stabilize) KHÔNG BAO GIỜ bị kích hoạt trong Phase 1.5 — near-
  miss gần nhất (monorepo.md, 2 correction round liên tục trước một
  align step) KHÔNG chạm ngưỡng 3.
```

## 8. EF-* rule effectiveness dispositions (yêu cầu bổ sung của `EF-RETRO-001`)

```text
EF-ADR-001 (convention trước ADR, no reopening thiếu conflict):
  Disposition: EFFECTIVE.
  Bằng chứng: Testing's ADR_NOT_REQUIRED outcome (§3) — dedicated Scope
    Check TRƯỚC KHI author, ngăn ADR không cần thiết. ZERO Phase 1
    architecture reopening trong toàn bộ 57 commit (verified git log
    trực tiếp: module-registry.yaml/Constitution/Domain Contract KHÔNG
    sửa từ trước commit 196539c tới 2e12b9b). Bảy ADR còn lại đều
    actually-triggered qua Chapter 0 §4b's ">1 module" nhánh (§3).

EF-ADR-002 (correction-chain circuit breaker, 3 round liên tục):
  Disposition: NOT_MATERIALLY_TESTED.
  Bằng chứng: breaker KHÔNG BAO GIỜ kích hoạt (KHÔNG artifact nào đạt 3
    correction round LIÊN TỤC không gián đoạn) — near-miss gần nhất LÀ
    monorepo.md (2 round liên tục, sau đó một align step [KHÔNG phải
    correction] cắt chuỗi, rồi 1 round nữa) — ngưỡng "liên tục" (đúng
    literal wording) chưa từng bị chạm, dù tổng churn (5 version) LÀ
    cao nhất Phase 1.5. Rule tồn tại như containment CHƯA từng cần dùng
    tới — CHƯA đủ bằng chứng để khẳng định threshold "3" đúng hay cần
    sửa.

EF-TXN-001 (foundation-only scope, KHÔNG vượt Chapter 14 §14.2's 8
  category):
  Disposition: EFFECTIVE.
  Bằng chứng: git log xác nhận trực tiếp — `docs/architecture/`,
    `docs/domain/`, `docs/constitution/` (module-registry.yaml, mọi
    Constitution chapter, mọi domain artifact) HOÀN TOÀN KHÔNG sửa
    trong cửa sổ 196539c..2e12b9b. 100% transaction Phase 1.5 nằm trong
    đúng 8 category (`docs/engineering/*.md`, `docs/adr/ADR-024..030`,
    `docs/phase-dod/phase-1.5-dod.md`, `docs/governance/phases/
    phase-1.5-rules.md`, MANIFEST/CHANGELOG bookkeeping).

EF-TXN-002 (batch theo category, KHÔNG chia nhỏ theo file/rule):
  Disposition: PARTIALLY_EFFECTIVE.
  Bằng chứng tích cực: ADR-024's correction đóng BA finding trong MỘT
    round (`ADR024-B-MAJ-01`/`-MIN-01`/`A-MIN-01`, commit `e55acdc`);
    Coding Standard's "align to ADR-025" transaction đóng BA finding
    trong MỘT round (`2543dab`, "close three findings"); CI/CD gộp
    trọn category (ADR + convention) thành 5 transaction bounded, KHÔNG
    chia nhỏ theo file riêng lẻ.
  Bằng chứng giới hạn: mỗi category VẪN tách RIÊNG ADR-transaction-
    chain khỏi convention-transaction-chain (vd Monorepo = 6 transaction
    ADR + 5 transaction convention = 11 transaction cho MỘT category) —
    "category" trong thực hành nghĩa LÀ "category × {ADR, convention}"
    chứ KHÔNG hoàn toàn một batch duy nhất; rule KHÔNG rõ liệu đây có
    tính LÀ vi phạm batching hay LÀ granularity hợp lý (ADR và living-
    convention LÀ hai lifecycle khác nhau, hợp lý tách theo Chapter 11).

EF-REV-001 (review depth tỷ lệ semantic risk, bảng 3 tier):
  Disposition: PARTIALLY_EFFECTIVE.
  Bằng chứng: tier "full review" (Review A + Independent Review B) áp
    dụng NHẤT QUÁN cho MỌI category, kể cả Testing (`ADR_NOT_REQUIRED`
    CONFIRMED qua dual review, không CHỈ deterministic verification).
    KHÔNG một transaction Phase 1.5 nào rơi vào tier 2 ("mechanical/
    tooling/config change" — deterministic verification, không cần
    reviewer thứ hai) hay tier 3 ("bookkeeping only") theo đúng nghĩa
    hẹp của bảng, VÌ KHÔNG category nào chọn tool/version/CI-provider cụ
    thể (mọi lựa chọn CỤ THỂ bị defer tường minh — xem `EF-VERIFY-001`
    dưới). Rule's phân tầng risk-proportional CHƯA từng được thực sự
    test ở tier thấp hơn — mọi thứ mặc định tier cao nhất, KHÔNG rõ đây
    LÀ do rule KHÔNG cần dùng tới (đúng, KHÔNG có mechanical/tooling
    claim nào) hay do thực hành default an toàn quá mức.

EF-BUDGET-001 (mechanical MANIFEST cell ≤1,500 từ):
  Disposition: EFFECTIVE.
  Bằng chứng: §5 trên — 128-636 từ/cell throughout, KHÔNG một vi phạm
    nào, so với Phase 1's 8,512-từ outlier. Rule mechanical enforcement
    (đề xuất `P2-BUDGET-001` từ Phase 1 retrospective, áp dụng sớm cho
    Phase 1.5 qua `EF-BUDGET-001`) chứng minh hoạt động đúng khi được
    tighten từ prose sang ngưỡng số cụ thể.

EF-VERIFY-001 (verify trực tiếp tool/version/CI-config TRƯỚC KHI ghi
  vào decision content):
  Disposition: NOT_MATERIALLY_TESTED.
  Bằng chứng: grep trực tiếp toàn bộ `docs/engineering/*.md` cho
    tool/version signal cụ thể (GitHub Actions/GitLab CI/Jenkins/
    pytest/poetry/eslint/black/exact Python hay Go version) — MỌI chỗ
    xuất hiện LÀ ví dụ minh họa TRUNG LẬP ("CI provider CỤ THỂ NÀO...
    KHÔNG author tại đây"), KHÔNG một lựa chọn/pin CỤ THỂ nào được ghi
    vào decision content. `.github/` absent, KHÔNG dependency manifest
    nào tồn tại (`package.json`/`pyproject.toml`/`go.mod`/
    `requirements.txt`) — verified trực tiếp. Rule's trigger condition
    (assert một exact version/tool/config) KHÔNG BAO GIỜ xảy ra Phase
    1.5 — Phase 1.5 CHỦ ĐỘNG ở lại policy/convention level, deferred
    mọi concrete tool selection. Rule tồn tại, ĐÚNG thiết kế, CHƯA có cơ
    hội thực tế để kiểm chứng.
```

## 9. Key lessons — hypothesis testing (bắt buộc theo task, KHÔNG giả định đúng trước)

```text
H1 "convention-first scope checking reduced ADR inflation":
  SUPPORTED. Bằng chứng trực tiếp: Testing ADR Scope Check (§3/§8,
  EF-ADR-001) ngăn một ADR không cần thiết qua kiểm tra TRƯỚC KHI
  author — instance CỤ THỂ, KHÔNG suy diễn.

H2 "bounded corrections reduced semantic churn":
  SUPPORTED, với giới hạn. 19/57 (~33%) transaction LÀ bounded
  correction, MỖI cái đóng ĐÚNG phạm vi finding của nó (verified section-
  by-section byte-diff mỗi lần, theo established methodology) — KHÔNG
  scope creep quan sát được. NHƯNG bounded correction KHÔNG ngăn được
  churn tự nó xảy ra nhiều lần trên MỘT artifact (monorepo.md 5 version,
  ADR-030 3 version) — "bounded" giữ MỖI round nhỏ/an toàn, KHÔNG giữ
  TỔNG SỐ round thấp.

H3 "provenance/stale wording caused disproportionate Minor findings":
  PARTIALLY SUPPORTED. 3/9 accepted residual (33%) VÀ 3/16 tổng Minor
  finding phân biệt được (~19%) LÀ pure provenance/stale-wording
  (`EF-CONFIG-B-MIN-01`, `EF-ERR-B-MIN-01`, `EF-MONO-ADR024-B-MIN-01`)
  — một tỷ lệ đáng kể NHƯNG KHÔNG áp đảo (phần lớn Minor VẪN LÀ substance
  nhỏ, vd Alternative-wording overstatement `ADR026-A-MIN-01`/
  `ADR027-B-MIN-01`, KHÔNG pure staleness).

H4 "independent Review B found materially different defects from
  Review A":
  SUPPORTED, bằng chứng mạnh, hai instance riêng biệt. (1) ADR-030:
  Review A tìm `ADR030-A-MAJ-01` (flaky-test policy authority
  misattribution); Independent Review B (trên v0.2) tìm
  `ADR030-B-MAJ-01` (unsupported LIVE-authority attribution) — hai class
  hoàn toàn khác nhau. (2) monorepo.md: Review A tìm `EF-MONO-A-MAJ-01`;
  Independent Review B tìm `EF-MONO-B-MAJ-01`/`02` (ADR-scope-disposition
  + README-example finding) — cũng khác class. KHÔNG một trường hợp
  Review B overrule Review A quan sát được (KHÔNG disagreement, CHỈ bổ
  sung).

H5 "transaction verification prevented executor reports from becoming
  implicit authority":
  SUPPORTED, bằng chứng sống trực tiếp trong chính retrospective window
  (§6): một transcription-blob-typo tự chính executor gây ra bị bắt VÀ
  sửa TRƯỚC KHI commit qua verify-before-commit step (Python string-
  concatenation cross-check cả ba blob) — lỗi KHÔNG BAO GIỜ trở thành
  authoritative. G-VERIFY-001/G-ID-001 discipline hoạt động ĐÚNG THIẾT
  KẾ dù chính nguồn gốc lỗi LÀ executor, KHÔNG phải reviewer bên ngoài.

H6 "prompt budget controls should be strengthened before Phase 2":
  REJECTED (KHÔNG được ủng hộ bởi evidence). §5/§8 (`EF-BUDGET-001`)
  cho thấy ngưỡng hiện tại (≤1,500 từ/cell) giữ vững THOẢI MÁI (128-636
  từ thực tế, KHÔNG gần ngưỡng) — KHÔNG một dấu hiệu strain nào quan sát
  được đòi hỏi siết thêm. Ngưỡng hiện tại ĐÃ đủ, KHÔNG cần thay đổi
  trước Phase 2 dựa trên bằng chứng Phase 1.5.
```

## 10. Rule dispositions

### 10.1 KEEP (hoạt động đúng, giữ nguyên)

```text
EF-ADR-001, EF-TXN-001, EF-BUDGET-001:            EFFECTIVE, giữ nguyên
                                                   (§8).
Bounded correction pattern (section-by-section
  byte-diff verify mỗi round):                    hoạt động tốt xuyên
                                                   suốt 19 correction
                                                   round, KHÔNG scope
                                                   creep phát hiện.
Verify-before-commit discipline (G-VERIFY-001/
  G-ID-001, kể cả tự-kiểm lỗi executor):           hoạt động ĐÚNG THIẾT
                                                   KẾ — §6/§9 H5.
Dual independent review (Review A + Independent
  Review B):                                       hoạt động tốt — bắt
                                                   được defect class
                                                   khác nhau nhất quán
                                                   (§9 H4), KHÔNG một
                                                   Major/Blocker nào lọt
                                                   qua tới Approval Gate.
current_phase / next-phase-authorization
  separation pattern (tái dùng từ Phase 1):        hoạt động đúng, §7.
```

### 10.2 TIGHTEN (rule đúng nhưng thực thi/định nghĩa chưa rõ, cần siết)

```text
EF-TXN-002 (batch theo category):                 TIGHTEN — PARTIALLY_
                                                   EFFECTIVE (§8).
                                                   Rule wording KHÔNG rõ
                                                   liệu "category" nghĩa
                                                   LÀ một batch duy nhất
                                                   hay category × {ADR,
                                                   convention} (thực tế
                                                   quan sát được LÀ vế
                                                   sau). Cần làm rõ
                                                   tường minh, KHÔNG đổi
                                                   semantic phase 1.5 đã
                                                   qua (tại đây, CHỈ ghi
                                                   nhận ambiguity —
                                                   KHÔNG sửa rule tại
                                                   transaction này).
Logging convention v0.2→v0.3 "leak" pattern (§2):  ghi nhận preventable-
                                                   authoring-defect class
                                                   — bounded correction
                                                   nên bao gồm một
                                                   explicit re-check
                                                   "finding đã đóng TRIỆT
                                                   ĐỂ, KHÔNG một phần"
                                                   bước trước khi coi
                                                   round hoàn tất
                                                   (KHÔNG rule mới tại
                                                   đây — ghi nhận cho
                                                   §11 PHASE2_CONTROL).
```

### 10.3 PROMOTE_GLOBAL (lesson Phase-1.5-specific đáng promote lên mọi phase)

```text
"Full-scope BCC qua git-log absence-of-touch verification" (§8 EF-
  TXN-001 evidence method — kiểm trực tiếp `git log -- <boundary-path>`
  từ phase-start commit tới thời điểm hiện tại, xác nhận KHÔNG commit
  nào chạm boundary path ngoài scope) — kỹ thuật rẻ, deterministic,
  reusable cho MỌI phase tương lai, đã dùng nhất quán xuyên suốt Phase
  1.5's mọi approval transaction. Đề xuất pin kỹ thuật này tường minh
  vào Global BCC guidance (Chapter 12 §12.4 thực hành, KHÔNG đổi
  Constitution semantics — CHỈ pin một "how-to" mechanical technique).
"MANIFEST table-cell mechanical word-count ceiling" (`EF-BUDGET-001`,
  §5/§8/§9 H6) — đã chứng minh hiệu quả qua HAI phase liên tiếp (Phase
  1 xác định vấn đề, Phase 1.5 xác nhận fix hoạt động: 8,512 từ →
  128-636 từ). Đề xuất PROMOTE nguyên văn `EF-BUDGET-001`'s ngưỡng
  ≤1,500 từ/cell thành Global rule (`G-BUDGET` extension), thay vì để
  mỗi phase-rules tự lặp lại cùng con số.
Batched multi-finding bounded-correction (đóng ≥2 finding liên quan
  trong MỘT round, khi cùng risk-tier — §8 EF-TXN-002 bằng chứng tích
  cực) — pattern đã hoạt động tốt (ADR-024, Coding Standard) nhưng KHÔNG
  codified tường minh ở tầng Global. Đề xuất bổ sung một câu rõ ràng vào
  `G-TXN` guidance.
```

### 10.4 PHASE2_CONTROL (control cụ thể cho Phase 2, dựa trên lesson thật, KHÔNG suy đoán)

```text
P2-CHURN-001 (đề xuất, refine `EF-ADR-002`/Phase-1's `P2-ADR-CHAIN-001`):
  đếm circuit-breaker threshold theo TỔNG SỐ version bump trên một
  artifact (bao gồm CẢ align/sync step, KHÔNG CHỈ correction round) —
  monorepo.md's near-miss (§7/§8) cho thấy đếm CHỈ "correction liên tục"
  có thể bỏ sót tổng churn thật khi một align step chen giữa. "Refine
  then promote" — CHƯA đủ dữ liệu để khẳng định ngưỡng cụ thể, cần thêm
  ít nhất một phase nữa quan sát trước khi promote Global. Bounded: CHỈ
  áp dụng khi Phase 2 sinh artifact cần align lại theo Approved authority
  mới (tương tự monorepo.md align ADR-024) — KHÔNG bắt buộc cho mọi
  artifact.
P2-AUTHORITY-VERIFY-001 (đề xuất, mở rộng `G-VERIFY-001`): mở rộng
  phạm vi `G-VERIFY-001` hiện tại (registry/taxonomy/blob fact) để bao
  gồm tường minh "authority/permission claim" (ai/cái gì có quyền
  authorize một action) — trực tiếp derive từ `ADR030-B-MAJ-01` (LIVE-
  authority attribution tới ADR-007/account.md KHÔNG verify trực tiếp
  scope thật của hai tài liệu đó trước khi assert). "Required before
  Phase 2 start" — Phase 2 (Product Prototype) LÀ phase gần LIVE-adjacent
  hơn Phase 1.5, risk của loại lỗi này tăng, KHÔNG speculative.
P2-DOUBLECLOSE-001 (đề xuất, nhẹ, dựa trên Logging v0.2→v0.3 leak, §2/
  §10.2): mỗi bounded correction PHẢI include một explicit "finding
  fully closed, KHÔNG partial" self-check trước khi coi round hoàn tất
  — "useful but optional," rủi ro thấp (chỉ một instance quan sát được
  Phase 1.5), KHÔNG bắt buộc chặn Phase 2 start.
```

### 10.5 RETIRE (rule thất bại, nên bỏ/viết lại)

```text
KHÔNG rule EF-* nào cần RETIRE. Mọi rule hoặc EFFECTIVE (EF-ADR-001,
  EF-TXN-001, EF-BUDGET-001), PARTIALLY_EFFECTIVE với giá trị rõ ràng
  (EF-TXN-002, EF-REV-001), hoặc NOT_MATERIALLY_TESTED (EF-ADR-002,
  EF-VERIFY-001 — tồn tại đúng thiết kế, chỉ chưa có cơ hội test, KHÔNG
  bằng chứng nào cho thấy chúng SAI hay redundant). KHÔNG finding nào
  ủng hộ việc bỏ một rule.
```

## 11. Quantitative summary

```text
Foundation category (Chapter 14 §14.2):        8 (Monorepo, Coding
                                                Standard, Naming,
                                                Logging, Config, Error
                                                Handling, Testing,
                                                CI/CD)
ADR created:                                   7 (ADR-024..ADR-030)
ADR_NOT_REQUIRED outcome:                      1 (Testing)
Total Phase 1.5 commit (196539c..2e12b9b,
  inclusive):                                  57
Bounded-correction-round commit:               19 (~33% of 57)
Distinct Major finding (Phase-1.5-scope,
  excludes Package-1.5/P15- architecture
  finding — different taxonomy, xem phase-1.5-
  rules.md banner):                            21
Distinct Minor finding (Phase-1.5-scope,
  excludes P15-/architecture, excludes 2 regex-
  truncated citation fragments):                16
Blocker finding:                               0
Accepted residual (still OPEN, non-blocking,
  post-Approval-Gate):                          9
Closed-before-approval finding (21 Major + 16
  Minor - 9 residual):                          28
Approval/acceptance lifecycle transaction
  (rule acceptance + 7 ADR approval + 8
  convention approval + DoD acceptance +
  Approval Gate decision):                      18
Artifact với churn cao nhất:                   monorepo.md (5 version,
                                                v0.1-v0.5)
Independent-Review-B-found-different-defect
  instance:                                     2 (ADR-030, monorepo.md
                                                — §9 H4)
```

## 12. Summary table

| # | Category | Top finding | Disposition |
|---|---|---|---|
| 1 | Wasted transactions | None fully wasted; G-ORCH-004 mis-scoped then narrowed same-session; Logging v0.2→v0.3 partial-fix leak | No new control mandatory; ghi nhận P2-DOUBLECLOSE-001 |
| 2 | Avoidable ADRs | None — 7/7 ADR actually-triggered (>1 module), Testing correctly ADR_NOT_REQUIRED | KEEP (EF-ADR-001) |
| 3 | Repeated churn | monorepo.md 5-version multi-root-cause churn; ADR-030 2-round Review-A/B-different-defect | PROMOTE_GLOBAL (dual-review value), P2-CHURN-001 |
| 4 | Prompt-size | MANIFEST cells 128-636 words vs Phase 1's 8,512-word outlier | KEEP/PROMOTE_GLOBAL (EF-BUDGET-001) |
| 5 | Lifecycle/blob defects | Zero blob-conflation defects; one self-caught transcription typo pre-commit | KEEP (verify-before-commit discipline) |
| 6 | Self-replication | None (no same-root-cause 3+ round chain); EF-ADR-002 never triggered | NOT_MATERIALLY_TESTED, P2-CHURN-001 refine |
| 7 | Rules that worked | EF-ADR-001, EF-TXN-001, EF-BUDGET-001 all EFFECTIVE with direct evidence | KEEP |
| 8 | Rules partially tested | EF-TXN-002, EF-REV-001 PARTIALLY_EFFECTIVE; EF-ADR-002, EF-VERIFY-001 NOT_MATERIALLY_TESTED | TIGHTEN wording (EF-TXN-002), no RETIRE |

## 13. What this retrospective does NOT do

```text
KHÔNG sửa DoD/ADR/convention/Constitution/Domain Contract nào.
KHÔNG sửa Phase 1.5 Approval Gate decision đã record (`MANIFEST.md`
  "Phase 1.5 Approval Gate — Decision" section, byte-identical).
KHÔNG đóng bất kỳ residual nào trong chín accepted residual Minor
  (VẪN OPEN, carried forward, KHÔNG chạm).
KHÔNG tự động promote bất kỳ đề xuất nào ở §10.3 (`PROMOTE_GLOBAL`)
  lên `execution-rules.md` — đây LÀ đề xuất, một transaction governed
  riêng biệt (rule-authoring) sẽ cần thực sự thêm chúng.
KHÔNG tự động thêm bất kỳ control nào ở §10.4 (`PHASE2_CONTROL`) vào
  Phase 2 rules — Phase 2 rules CHƯA tồn tại, đòi hỏi transaction riêng.
KHÔNG authorize/bắt đầu Phase 2 substantive work.
KHÔNG authorize LIVE.
```

## 14. Relationship / citations

`docs/governance/phases/phase-1.5-rules.md` — `EF-RETRO-001`, bảy rule `EF-ADR-001`/`EF-ADR-002`/`EF-TXN-001`/`EF-TXN-002`/`EF-REV-001`/`EF-BUDGET-001`/`EF-VERIFY-001`. `docs/governance/retrospectives/phase1-retrospective-001.md` — structure precedent (`P1-RETRO-001`), nguồn `G-VERIFY-001`/`P2-BUDGET-001` đề xuất mà `EF-VERIFY-001`/`EF-BUDGET-001` kế thừa. `docs/MANIFEST.md` — "Phase 1.5 Approval Gate — Decision" section (Approval Gate PASSED, unchanged bởi transaction này).

## 15. Change history

```text
v1.0  2026-08-13  Established — vai trò: `EF-RETRO-001 Phase 1.5 Process
      Retrospective Executor`. Evidence-based retrospective trên 57
      Phase 1.5 commit (196539c..2e12b9b), 37 distinct finding (21
      Major/16 Minor/0 Blocker, Phase-1.5-scope), 9 accepted residual.
      Top finding: monorepo.md's 5-version churn LÀ multi-root-cause
      hợp lý (KHÔNG same-root-cause repetition kiểu Phase 1's ADR-023);
      Independent Review B tìm defect class khác Review A trong CẢ HAI
      trường hợp churn cao nhất (ADR-030, monorepo.md) — reinforcing
      giá trị dual-review. `EF-ADR-001`/`EF-TXN-001`/`EF-BUDGET-001`:
      EFFECTIVE. `EF-TXN-002`/`EF-REV-001`: PARTIALLY_EFFECTIVE.
      `EF-ADR-002`/`EF-VERIFY-001`: NOT_MATERIALLY_TESTED (chưa từng
      kích hoạt/chưa có tool-version claim nào để verify). KHÔNG rule
      nào RETIRE. Sáu hypothesis kiểm tra tường minh (§9): bốn
      SUPPORTED (H1/H2/H4/H5), một PARTIALLY SUPPORTED (H3), một
      REJECTED (H6 — budget control KHÔNG cần siết thêm). Ba
      Global-promotion đề xuất (§10.3), ba Phase-2-specific control đề
      xuất (§10.4, một "required before Phase 2 start" —
      P2-AUTHORITY-VERIFY-001). `EF-RETRO-001`: COMPLETE. Phase 2
      substantive work: VẪN NOT YET AUTHORIZED. LIVE: VẪN NOT
      AUTHORIZED.
```
