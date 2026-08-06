---
id: package-1.6-upstream-resolution-exploration
title: "Package 1.6 Upstream Resolution — Source Clarification Exploration"
version: "0.2"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-05"
last_review: null
next_review: null
depends_on: ["00-governance"]
---

# Package 1.6 Upstream Resolution — Source Clarification Exploration

**`NON-AUTHORITATIVE` · `EXPLORATORY` · `NOT APPROVED` · `NOT IMPLEMENTATION-READY` · `DECISION EVIDENCE ONLY`**

**Package lifecycle: `exploratory candidate` — status: Draft, KHÔNG Approved.** Tài liệu này KHÔNG author architecture, KHÔNG chọn dependency edge, KHÔNG đăng ký module, KHÔNG chuyển giao responsibility, KHÔNG sửa Product/Domain semantics, KHÔNG author/approve ADR, KHÔNG sửa Package 1.1/1.4/1.5/1.6, KHÔNG consolidate bất cứ gì, KHÔNG mở Gate 2/Phase 2/LIVE. Mọi nội dung dưới đây LÀ decision evidence CHO một transaction tương lai — KHÔNG PHẢI chính quyết định đó.

**v0.2 — bounded correction (2026-08-05), đóng ba Review A finding trên v0.1 (`P16-UR-A-MAJ-01`/`P16-UR-A-MAJ-02`/`P16-UR-A-MIN-01`), KHÔNG design/select/author mới:** (a) `P16-UR-A-MAJ-01` — §2.2/§2.4/§5/§7.1 sửa: bỏ claim "DD-001 và API reachability là hai vấn đề độc lập" — xác nhận lại `depends_on`/`owns_authoritative_state` LÀ hai field registry tách biệt VÀ thêm edge KHÔNG resolve DD-001 (registry-mechanics fact, GIỮ NGUYÊN), NHƯNG bổ sung: nguồn hiện tại CHƯA established Backtest run-identity ownership classification (authoritative fact/non-authoritative result/correlation tag/khác) hay create/query contract semantics đầy đủ — semantic eligibility cho edge VẪN contingent trên clarification đó; Candidate A GIỮ NGUYÊN như một candidate CHƯA chọn, KHÔNG bị reject, CHỈ qualify lại mức độ evidence. (b) `P16-UR-A-MAJ-02` — §6/§7.2/§7.3/§8 sửa: thay "ADR CONDITIONALLY REQUIRED" mơ hồ bằng khung ba nhánh tường minh (A: source clarification only — không quyết định; B: ADR có thể không cần, subject to Governance §4b review riêng, NẾU một module hiện có đã sở hữu đầy đủ trách nhiệm và không cần thay đổi gì; C: ADR REQUIRED nếu cần responsibility expansion/computation-owner selection/module mới/dependency edge/multi-module orchestration boundary/hard-to-reverse contract ownership) — áp dụng riêng biệt cho VIEW-002 VÀ VIEW-003 (KHÔNG combine mặc định), kết luận: MỌI candidate khả thi đã evaluate cho CẢ HAI rơi vào Nhánh C → ADR REQUIRED. (c) `P16-UR-A-MIN-01` — §5/§7.1/§7.2/§7.3 sửa: bỏ claim "package_lifecycle revert Consolidated Stable → candidate" như một transition tự động — xác nhận baseline Consolidated Stable VẪN controlling cho tới khi một lifecycle transaction được authorize riêng biệt; semantic modification đòi hỏi governed reopening/successor candidate transaction, VÀ Review A + Independent Review B + Product Owner reconsolidation decision MỚI TRƯỚC KHI trở lại Consolidated Stable; áp dụng nhất quán cho Package 1.1/1.3-A/1.3-C/1.4/1.5. Mọi nội dung khác của v0.1 GIỮ NGUYÊN — KHÔNG option/edge/owner/module/responsibility/contract nào được chọn.

## 0. Product Owner authorization (nguyên văn, bắt buộc ghi nhận)

**Authorization timestamp: 2026-08-05T19:39:00+07:00**

```text
"I authorize bounded upstream-resolution work for the Package 1.6 v0.2 binding
prerequisites concerning NAV-003, VIEW-002, and VIEW-003.

This authorization permits read-only source analysis and bounded authoring of the
Product, Domain, and ADR evidence required to decide:

1. whether command-query-api-surface should gain a registered dependency on
   backtest-orchestrator for NAV-003;
2. the controlling semantics and eligible owner for VIEW-002 Research verification;
3. the controlling semantics, eligible owner, and package assignment for VIEW-003
   parity verification.

This authorization does not approve any dependency edge, module, responsibility
transfer, Product or Domain semantic change, ADR decision, registry change, API
exposure, or UX binding.

Package 1.1 through Package 1.5 remain Consolidated Stable unless and until a
separately reviewed and approved semantic transaction explicitly reopens one.

Package 1.6 remains candidate and blocked from Independent Review B and
consolidation.

Phase 1 remains Active and not Complete. Gate 2 and Phase 2 remain unopened. LIVE
remains Unauthorized."
```

**Xác nhận tường minh:** authorization trên CHỈ cho phép read-only source analysis VÀ bounded authoring của decision evidence — tài liệu này tuân thủ nghiêm ngặt phạm vi đó, KHÔNG vượt quá.

## 1. Governing authority và controlling sources đã đọc trực tiếp

```text
docs/architecture/phase-1-plan.md v0.4 (Approved) — package-boundary/DD-001/DD-003/
  OQ-001-003 authority, §11.
docs/architecture/module-registry.yaml v0.7 (Consolidated Stable) — backtest-
  orchestrator/command-query-api-surface/review-evidence-service/replay-integration-
  service/decision-evaluation-engine/decision-authority-service registry fact.
docs/architecture/system-decomposition.md v0.7 (Consolidated Stable) — semantic parity.
docs/architecture/api-architecture.md v0.3 (Consolidated Stable) — command-query-api-
  surface exposure boundary, §2.1/§6.
docs/architecture/database-architecture.md v0.2 (Consolidated Stable) — review-
  evidence-service persistence boundary, §2.1/§4/§10.
docs/architecture/ux-architecture.md v0.2 (candidate) — NAV-003/VIEW-002/VIEW-003
  technically-blocked status, §4.1/§4.3/§13.
docs/product/product-requirement.md — PR-XXX authority, đặc biệt PR-010/PR-019/
  PR-017/PR-021-023/PR-033/PR-034, VÀ `canonical semantic-decision hash` definition
  pointer.
docs/product/use-case-workflow.md — UC-003/UC-005/UC-006/UC-007/UC-010 full text,
  WF-INV-5.
docs/product/ux-blueprint.md — VIEW-002/VIEW-003/NAV-003 spec, STATE-007/008/022-024,
  UX-INV-5.
docs/domain/decision.md v0.3 (Package 0.2-C4, Consolidated Stable) — fold algorithm/
  visible-valid-head, KHÔNG chứa định nghĩa "hash" (exhaustive grep, §4 dưới).
docs/domain/strategy.md v0.3 (Package 0.2-C3, Consolidated Stable) — Strategy
  Definition Version/Strategy Instance/Configuration Version axis status.
docs/domain/replay-event.md v0.3 (Package 0.2-C7, Consolidated Stable) — canonical
  Replay Cursor reuse, ReplayStateProjection integration-contract-only scope.
Constitution Chapter 0 §4b (Locked) — ADR Scope Rule (ADR Required/Optional/Not
  Required table).
docs/MANIFEST.md — Package 0.2-C3/C4/C7 Consolidated Stable confirmation; OQ-001/002/
  003 status.
```

## 2. NAV-003 clarification evidence (bắt buộc, yêu cầu task)

### 2.1 Source extraction

```text
Controlling identifier:   NAV-003; SCR-003 (Backtest Run Setup, UC-006, PR-021/022/
  023); SCR-004 (Backtest Run Detail, UC-007/008/009, PR-004/005/009/021/022/033/034);
  SCR-005 (Backtest Run Comparison, UC-010, PR-034).

Exact behavior ĐÃ established (direct source fact, KHÔNG suy diễn):
  UC-006: khởi động một Backtest run bounded (start/end), stable run identity/context
    gắn Strategy Instance/Definition Version/policy version; chạy Decision logic qua
    CÙNG pipeline với Replay/Paper (WF-INV parity); KHÔNG tạo Order/ExecutionResult
    PAPER/Live; KHÔNG route mạng tới exchange thật. Evidence produced: "Decision/
    RiskEvaluation sequence gắn run identity."
  UC-007: xem chuỗi Decision (+ downstream RiskEvaluation liên quan) của một run,
    tách bạch upstream explainability evidence khỏi downstream lineage.
  UC-010: so sánh cross-run/cross-version, non-PAPER authority, KHÔNG unified
    execution-outcome fact, KHÔNG normalization/scoring chung.
  Registry: `backtest-orchestrator` (module-registry.yaml v0.7) — `module_type:
    runtime_service`, `depends_on: [strategy-engine, decision-evaluation-engine,
    decision-authority-service, risk-gateway]` (khớp CHÍNH XÁC "cùng pipeline" của
    UC-006), `forbidden_dependencies: [execution-engine, paper-execution-boundary,
    execution-result-processor, fill-processor, position-projection]` (Backtest
    authority boundary — non-PAPER, KHÔNG tái sử dụng PAPER fact), `phase.
    elaborated_by: "1.3-A"`.

Exact behavior KHÔNG established:
  Concrete Backtest Domain Contract/entity/event/schema (DD-001, Deferred, Product
    Owner decision tương lai).
  Cơ chế simulation/PnL/fee/slippage/accounting (product-required nhưng domain-
    representation deferred, UC-006 Out-of-scope boundary).
  Liệu "Decision/RiskEvaluation sequence gắn run identity" (UC-006 Evidence produced)
    LÀ một authoritative fact CỦA backtest-orchestrator (vd. một "BacktestRunContext"
    fact riêng), HAY CHỈ LÀ Decision/RiskEvaluation fact ĐÃ tồn tại (thuộc decision-
    authority-service/risk-gateway) được gắn thêm một correlation tag — nguồn hiện tại
    KHÔNG phân biệt rõ hai khả năng này.

Authority ĐÃ established: `backtest-orchestrator` module identity/type/dependency/
  forbidden-dependency/phase-assignment (Package 1.1, Consolidated Stable). Orchestration
  BOUNDARY (identity/context binding) — established. `owns_authoritative_state`
  TRUE/FALSE value — KHÔNG resolved (`deferred`, chờ DD-001).

Ownership/contract/routing info CÒN thiếu:
  `command-query-api-surface.depends_on` (Package 1.4 v0.3, Consolidated Stable)
    KHÔNG chứa `backtest-orchestrator` — KHÔNG route API nào tồn tại từ UX tới module
    này.
  Run-identity-to-Decision correlation exposure mechanism (ai expose, dưới contract
    category nào) — KHÔNG established.
```

### 2.2 DD-001 phân tách bắt buộc (API reachability KHÁC authoritative-fact claim)

```text
Xác nhận tường minh (bằng chứng, KHÔNG quyết định, v0.2 correction đóng `P16-UR-A-
MAJ-01`): `depends_on` VÀ `owns_authoritative_state` LÀ HAI field registry tách biệt
(registry fact, KHÔNG đổi) — DD-001 (module-registry.yaml notes, nguyên văn) NGĂN
CHẶN resolve `owns_authoritative_state` của backtest-orchestrator thành `true`/`false`
dứt khoát; thêm một `depends_on` edge, TỰ THÂN, KHÔNG resolve DD-001 (registry
mechanics fact, bảo toàn). Bằng chứng hỗ trợ mechanics đó: `command-query-api-
surface.depends_on` (Package 1.4 v0.3) ĐÃ route tới `position-projection`/`review-
evidence-service` (cả hai `owns_authoritative_state: false`) — routing edge KHÔNG ĐÒI
HỎI một giá trị `owns_authoritative_state` cụ thể nào ở tầng registry MECHANICS.

Xác nhận tường minh bổ sung (bắt buộc, sửa over-claim của v0.1): fact registry-mechanics
trên KHÔNG chứng minh rằng quyết định thêm edge cho backtest-orchestrator LÀ semantically
độc lập hay đã sẵn sàng ("ready") — nguồn hiện tại CHƯA established liệu Backtest run
identity/context (UC-006 "Evidence produced") LÀ: (a) một authoritative fact riêng của
backtest-orchestrator; (b) một non-authoritative orchestration result thuần túy; (c)
một correlation tag gắn lên fact đã tồn tại (Decision/RiskEvaluation); HAY (d) một khái
niệm khác do một Domain Contract tương lai kiểm soát. Nguồn hiện tại CŨNG CHƯA
established đầy đủ create/query contract semantics của Backtest (command shape để khởi
tạo run, query shape để trace/so sánh) — UC-006/007/010 mô tả BEHAVIOR mức Product,
KHÔNG PHẢI một contract category/field-level semantics đã pin đủ để route API. DO ĐÓ:
semantic eligibility cho việc expose backtest-orchestrator qua API VẪN contingent trên
việc làm rõ run identity, correlation ownership, VÀ command/query boundary — CHƯA đủ
điều kiện để coi quyết định edge LÀ một routing-mechanics-only question. MỘT SỐ routing
design (vd. xác nhận `depends_on`/`owns_authoritative_state` độc lập ở tầng registry)
CÓ THỂ tiến hành trong khi VẪN bảo toàn DD-001 nguyên vẹn — NHƯNG Package 1.6
exploration KHÔNG được claim full semantic independence hay sự sẵn sàng ("readiness")
cho quyết định edge đó. Candidate A (§2.4) VẪN LÀ một candidate CHƯA chọn, KHÔNG bị
reject — chỉ bị qualify lại đúng mức độ evidence hỗ trợ nó.
```

### 2.3 Graph mismatch hiện tại (chính xác)

```text
ux-application-shell.depends_on: [command-query-api-surface]                (v0.7)
command-query-api-surface.depends_on: 16 module — KHÔNG bao gồm
  backtest-orchestrator                                                     (v0.3)
backtest-orchestrator.depends_on: [strategy-engine, decision-evaluation-engine,
  decision-authority-service, risk-gateway]                                 (v0.7)

⟹ UX KHÔNG có route hợp lệ nào tới backtest-orchestrator — KHÔNG trực tiếp (không
  registered edge), KHÔNG gián tiếp qua command-query-api-surface's registered
  dependency set (backtest-orchestrator KHÔNG nằm trong đó).
```

### 2.4 Bốn candidate resolution — đánh giá, KHÔNG chọn (bắt buộc, yêu cầu task)

```text
A. Thêm command-query-api-surface -> backtest-orchestrator dependency edge:
   Semantic fit:          MỘT PHẦN, contingent (v0.2 correction, đóng `P16-UR-A-
                          MAJ-01`) — mẫu hình 16-edge hiện có VÀ nhu cầu command/query
                          của UC-006/007/010 hỗ trợ hướng đi này Ở MỨC routing-mechanics,
                          NHƯNG semantic eligibility ĐẦY ĐỦ VẪN contingent trên làm rõ
                          run identity/correlation ownership VÀ command/query contract
                          boundary (§2.2 bổ sung) — CHƯA đủ evidence để gọi đây là "CAO"
                          không điều kiện.
   Authority effect:      KHÔNG resolve DD-001 (§2.2) — owns_authoritative_state VẪN
                          deferred; NHƯNG việc DD-001 KHÔNG resolve KHÔNG đồng nghĩa
                          candidate này đã semantically sẵn sàng (§2.2 bổ sung).
   Graph changes:         MỘT edge mới, module-registry.yaml + system-decomposition.md
                          (semantic parity, KHÔNG mechanical).
   Package 1.1 hệ quả:    Registry content change → semantic (KHÔNG mechanical), đúng
                          tiền lệ đã dùng (custody-signing-service v0.7 assignment) —
                          package_lifecycle revert Consolidated Stable → candidate LÀ
                          MỘT lifecycle transaction governed riêng biệt, KHÔNG tự động
                          xảy ra (§5 qualification, đóng `P16-UR-A-MIN-01`) — cần MỘT
                          vòng Review A + Independent Review B + Product Owner
                          consolidation decision MỚI, TRƯỚC KHI baseline sửa đổi trở
                          lại Consolidated Stable.
   Package 1.4 hệ quả:    api-architecture.md §2.1 transcribe `depends_on` verbatim —
                          registry change làm transcription đó stale, cần một Package
                          1.4 correction transaction (parity update) — cùng qualification
                          governed-reopening như trên (§5), KHÔNG tự động.
   ADR trigger:           Governance §4b — "Module Taxonomy/dependency graph" thay
                          đổi → ADR Required, KHÔNG mơ hồ.
   DD-001 preservation:   BẢO TOÀN — edge addition KHÔNG đóng DD-001 (NHƯNG xem xác
                          nhận bổ sung ở §2.2: bảo toàn DD-001 KHÔNG đồng nghĩa candidate
                          đã đủ điều kiện semantic).
   Rejection reason:      KHÔNG bị reject — VẪN LÀ một candidate CHƯA chọn — NHƯNG
                          chi phí thật: kích hoạt ADR + reopen HAI package đã
                          Consolidated Stable (1.1 VÀ 1.4) qua governed lifecycle
                          transaction, CỘNG một prerequisite semantic clarification
                          (§2.2) CHƯA thỏa.

B. Route qua module hiện có khác (decision-authority-service/risk-gateway, đã có
   route API Surface):
   Semantic fit:          MỘT PHẦN — decision-authority-service/risk-gateway sở hữu
                          Decision/RiskEvaluation fact CỦA run đó, NHƯNG run-identity-
                          to-Decision correlation mapping LÀ trách nhiệm backtest-
                          orchestrator (UC-006 "gán MỘT stable run identity") — nguồn
                          hiện tại KHÔNG xác nhận decision-authority-service/risk-
                          gateway tự expose correlation đó.
   Authority effect:      KHÔNG rõ — phụ thuộc câu hỏi mở dưới.
   Graph changes:         KHÔNG (nếu correlation đã sẵn có qua route hiện tại) — NHƯNG
                          KHÔNG xác nhận được từ nguồn hiện tại.
   Package 1.1/1.4 hệ quả: Tiềm năng KHÔNG có, NẾU correlation available — CHƯA
                          confirmed.
   ADR trigger:           Khả năng KHÔNG cần (nếu không thêm edge) — NHƯNG câu hỏi
                          correlation-availability tự nó cần một clarification riêng
                          (có thể KHÔNG phải ADR, có thể là Package 1.3-A/system-
                          decomposition xác nhận).
   DD-001 preservation:   BẢO TOÀN.
   Rejection reason:      KHÔNG loại trừ hẳn — NHƯNG KHÔNG đủ evidence để xác nhận
                          viable; ghi nhận như unresolved question (§2.5), KHÔNG như
                          một candidate sẵn sàng.

C. Đổi Product/UX semantics (vd. redefine NAV-003 để KHÔNG cần live backend binding,
   hoặc defer NAV-003 sang phase sau):
   Semantic fit:          NGOÀI thẩm quyền transaction này — authorization tường minh
                          KHÔNG cho phép Product/Domain semantic change (§0). Ghi nhận
                          CHỈ để đầy đủ, KHÔNG evaluate sâu hơn — đòi hỏi một Product/
                          UX transaction governed RIÊNG BIỆT, ngoài phạm vi tài liệu
                          này.

D. Giữ blocked (status quo, Package 1.6 v0.2 hiện tại):
   Semantic fit:          N/A — trạng thái hiện tại.
   Authority effect:      KHÔNG.
   Graph/package hệ quả:  KHÔNG.
   ADR trigger:           KHÔNG (không quyết định nào được thực hiện).
   DD-001 preservation:   BẢO TOÀN trivially.
   Chi phí:               Package 1.6 KHÔNG đạt Independent Review B/consolidation
                          cho các screen chạm NAV-003 vô thời hạn.
```

### 2.5 Câu hỏi chưa resolve (NAV-003)

```text
1. decision-authority-service/risk-gateway có (hoặc nên) expose run-identity
   correlation như một query dimension độc lập, KHÔNG cần backtest-orchestrator làm
   trung gian? (liên quan Candidate B)
2. "Decision/RiskEvaluation sequence gắn run identity" (UC-006) LÀ authoritative fact
   riêng của backtest-orchestrator, hay chỉ là correlation tag trên fact đã tồn tại?
   (ảnh hưởng trực tiếp DD-001 scope VÀ Candidate A/B lựa chọn)
```

## 3. VIEW-002 clarification evidence (bắt buộc, yêu cầu task)

### 3.1 Source extraction — UC-003 (nguyên văn, KHÔNG mở rộng)

```text
Đã established (direct source fact):
  Research-session interval identity: MỘT PHẦN — "Inputs: Khoảng thời gian của phiên
    Research vừa kết thúc" (input tồn tại), NHƯNG cơ chế xác định boundary (start/end,
    timezone, edge-case) KHÔNG định nghĩa; KHÔNG "ResearchSession" entity nào tồn tại
    (UC-003 tự xác nhận: "KHÔNG tạo entity/event 'ResearchVerification' hay tương
    đương").
  Required evidence stream: ĐẦY ĐỦ — "event log của Decision/RiskEvaluation/Execution
    Intent/Order/ExecutionResult stream trong khoảng thời gian phiên" (Main flow bước
    1, tường minh năm loại stream).
  Evidence-completeness rule: MỘT PHẦN — INDETERMINATE định nghĩa qua ĐIỀU KIỆN
    ("evidence cần thiết... không resolve được trọn vẹn") NHƯNG KHÔNG định nghĩa CƠ
    CHẾ xác định "trọn vẹn" (cursor/watermark check? timeout? explicit completeness
    flag?) — KHÔNG có trong nguồn.
  PASSED condition: ĐẦY ĐỦ — "không prohibited fact nào... được quan sát."
  FAILED condition: ĐẦY ĐỦ — "một hoặc nhiều prohibited authoritative fact được quan
    sát."
  INDETERMINATE condition: established ở NGUYÊN TẮC (§ trên), KHÔNG ở MECHANISM.
  Correction/cursor/version treatment: KHÔNG established — UC-003 KHÔNG đề cập điều
    gì xảy ra nếu một correction (invalidate/supersede) tới cho một fact TRONG khoảng
    đã check SAU KHI verification đã tính xong.
  Output classification: ĐẦY ĐỦ, tường minh — "KHÔNG authoritative fact — kết quả
    verification LÀ workflow-visible result DUY NHẤT, KHÔNG tạo một entity/event
    'ResearchVerification' hay tương đương" (UC-003 Evidence produced, nguyên văn).

Missing semantic item (danh sách đầy đủ, bắt buộc yêu cầu task):
  1. Research-session interval identity — cơ chế xác định boundary CỤ THỂ.
  2. Evidence-completeness determination mechanism.
  3. Correction-arrival-during-window handling.
  4. Computation owner/layer — module NÀO thực thi existence-check trên năm stream.
```

### 3.2 Eligible ownership candidate — đánh giá, KHÔNG chọn

```text
review-evidence-service:
  PRO: đã là cross-cutting read/evidence aggregator; `depends_on` (Package 1.5 v0.2)
       overlap ĐÁNG KỂ với bốn/năm stream UC-003 cần (decision-authority-service,
       risk-gateway, execution-engine, execution-result-processor).
  CON: registered `responsibilities` (module-registry.yaml v0.7) CHỈ ghi "Decision→
       Position lineage trace, historical-state comparison, correction inspection
       (UC-016-018)" — UC-003 KHÔNG nằm trong danh sách đó; assign đòi hỏi MỞ RỘNG
       responsibility đã đăng ký, KHÔNG CHỈ routing add.

replay-integration-service:
  CON: vai trò đăng ký LÀ canonical-Replay-Cursor point-in-time reconstruction —
       KHÔNG PHẢI một existence-check-over-interval computation; semantic fit yếu.

decision/risk/execution owner tự thực hiện (multi-source query):
  CON: KHÔNG module nào trong số này thấy được CẢ năm stream cùng lúc (mỗi module
       chỉ sở hữu stream của chính nó) — cần một aggregation layer mới, KHÔNG rõ ở
       API Surface hay client-side (cùng ambiguity đã ghi nhận tại Package 1.6 v0.2
       §13 gap #1).

backtest-orchestrator:
  KHÔNG áp dụng — VIEW-002 LÀ Research-stage screen (NAV-001), KHÔNG liên quan
       Backtest.

Module MỚI:
  Khả thi về nguyên tắc, NHƯNG đòi hỏi Package 1.1 registration MỚI — ngoài thẩm
       quyền transaction này (authorization §0 tường minh cấm "register a module").

Giữ blocked:
  Trạng thái hiện tại (Package 1.6 v0.2) — valid, không chi phí thêm ngoài Independent
       Review B blocker đã tồn tại.
```

**Xác nhận tường minh:** KHÔNG ownership nào được assign chỉ vì data proximity (review-evidence-service's overlap KHÔNG TỰ ĐỘNG nghĩa là nó sở hữu computation này — registered responsibility PHẢI mở rộng tường minh trước, đúng nguyên tắc đã pin tại Package 1.4 P14-A-MAJ-01/Package 1.6 P16-A-MAJ-02).

## 4. VIEW-003 clarification evidence (bắt buộc, yêu cầu task — phân tích riêng biệt khỏi VIEW-002)

### 4.1 Source extraction — UC-005 VÀ Domain Contract semantics

```text
Compared Decision:               ĐẦY ĐỦ — "Decision đã ghi nhận tại cursor" (recorded,
                                  visible-valid-head per decision.md §8 fold algorithm,
                                  Consolidated Stable) vs. Decision logic tái tính toán
                                  (UC-005 Main flow bước 2).
Canonical Replay Cursor:          ĐẦY ĐỦ — Chapter 8 §8.5.1 (Locked), tái sử dụng
                                  nguyên vẹn bởi replay-event.md (Package 0.2-C7,
                                  Consolidated Stable).
Strategy Instance:                ĐẦY ĐỦ — strategy.md §5 (Package 0.2-C3, Consolidated
                                  Stable).
Strategy Definition Version:      ĐẦY ĐỦ — strategy.md §1.
Configuration Version:            MỘT PHẦN — MỘT trong bốn trục evidence độc lập bắt
                                  buộc (ADR-013 §2.4, Approved/Locked architecture),
                                  NHƯNG nội dung Domain Contract chi tiết của chính nó
                                  "chưa author ở C3" (strategy.md §5, nguyên văn) — trục
                                  ĐÃ pin kiến trúc, entity CHƯA author đầy đủ.
Rule/input evidence:              MỘT PHẦN — decision.md có structured-explanation/
                                  input-snapshot model CHUNG cho Decision, NHƯNG UC-005
                                  KHÔNG tự định nghĩa field/evidence CỤ THỂ nào dùng
                                  riêng cho parity recomputation — dựa vào model chung,
                                  KHÔNG một đặc tả riêng.
Canonical semantic-decision hash: KHÔNG established ở mức field-list (GAP xác nhận
                                  bằng exhaustive grep, §4.2 dưới).
Correction-aware visible-valid
  Decision head:                  ĐẦY ĐỦ — decision.md §8 fold algorithm "visible-
                                  valid-head per logical computation key" (Consolidated
                                  Stable, C4-MAJ-03).
MATCH/MISMATCH behavior:          ĐẦY ĐỦ — UC-005 Main flow bước 3; STATE-007/
                                  STATE-008 (ux-blueprint.md §11).
Missing/non-evaluable behavior:   KHÔNG established — UC-005 CHỈ có MỘT alternate/
                                  failure path ("Kết quả mismatch") — KHÔNG "missing
                                  evidence"/"cannot evaluate" path nào được định nghĩa.
INDETERMINATE established hay
  chỉ proposed:                   KHÔNG established Ở BẤT KỲ mức nào (KHÔNG ở UC-005,
                                  KHÔNG ở ux-blueprint.md §11 STATE catalogue — CHỈ
                                  STATE-007/STATE-008 tồn tại, KHÔNG "STATE parity
                                  indeterminate" nào được đăng ký) — tương phản tường
                                  minh với VIEW-002 (BA outcome: PASSED/FAILED/
                                  INDETERMINATE, STATE-022/023/024).
```

### 4.2 `canonical semantic-decision hash` — gap xác nhận bằng exhaustive search (bắt buộc, yêu cầu task)

```text
product-requirement.md §"Định nghĩa canonical semantic-decision hash" (nguyên văn):
  "hash so sánh semantic Decision, định nghĩa BỞI Decision Contract authoritative
  (decision.md, tại /docs/domain/) — KHÔNG hardcode danh sách field canonical tại PRD
  này."

Kết quả grep exhaustive trên docs/domain/decision.md (Package 0.2-C4, Consolidated
  Stable, v0.3): ZERO occurrence của từ "hash" — KHÔNG có định nghĩa, KHÔNG danh sách
  field loại trừ/bao gồm, KHÔNG thuật toán so sánh nào tồn tại tại decision.md.

Kết luận (evidence-based, bắt buộc ghi nhận): product-requirement.md/use-case-
  workflow.md/ux-blueprint.md ĐỀU tham chiếu `canonical semantic-decision hash` như
  một khái niệm "định nghĩa bởi decision.md" — NHƯNG decision.md, tại v0.3 Consolidated
  Stable hiện tại, KHÔNG chứa định nghĩa đó. Đây LÀ gap CỤ THỂ NHẤT, well-evidenced
  NHẤT trong toàn bộ tài liệu này — KHÔNG một suy diễn, LÀ một fact trực tiếp từ
  exhaustive source search.
```

### 4.3 Eligible ownership candidate — đánh giá, KHÔNG chọn

```text
decision-evaluation-engine:
  PRO: registered responsibility LÀ compute Decision-evaluation logic (compute_engine,
       non-authoritative) — module ORIGINAL sinh ra proposal mà decision-authority-
       service accept; re-run cùng logic cho mục đích parity-check có gần gũi semantic
       cao.
  CON: registered `depends_on` (module-registry.yaml v0.7) = [strategy-engine,
       strategy-plugin-host, context-aggregator] — KHÔNG có edge tới replay-
       integration-service hay bất kỳ "cursor-bounded historical re-execution"
       capability nào; re-run tại một cursor lịch sử tùy ý KHÔNG rõ có nằm trong
       registered scope hiện tại hay không.

replay-integration-service:
  PRO: sở hữu canonical Replay Cursor concept, ĐÃ assemble ReplayState(C) bằng fold
       authoritative stream tại cursor — ứng viên tự nhiên để MỞ RỘNG thêm "re-run và
       so sánh."
  CON: contract CỦA CHÍNH NÓ (replay-event.md, nguyên văn) tường minh: "CHỈ tham chiếu
       (ref:) các stream đã tồn tại, KHÔNG author fact mới, KHÔNG duplicate authority"
       — hiện tại scoped THUẦN fold/reconstruction, KHÔNG một recomputation-và-diff
       engine; mở rộng để TỰ recompute (KHÔNG CHỈ fold recorded fact) LÀ một
       responsibility expansion đáng kể.

review-evidence-service:
  CON: cùng lý do §3.2 — registered scope (UC-016-018) KHÔNG bao gồm parity
       verification.

decision-authority-service:
  CON: LÀ authoritative acceptance boundary, KHÔNG PHẢI một recomputation/comparison
       engine; gán thêm trách nhiệm "tự recompute và so sánh với chính mình" có rủi ro
       kiến trúc — dễ bị hiểu nhầm thành decision-authority-service "tự re-approve"
       Decision của nó, cần bounded rất cẩn thận nếu chọn hướng này.

Module non-authoritative MỚI:
  Khả thi về nguyên tắc (tương tự tinh thần custody-signing-service tách riêng cho
       một authority hẹp) — NHƯNG LÀ module registration MỚI, ngoài thẩm quyền
       transaction này.

Giữ blocked:
  Valid, trạng thái hiện tại.
```

## 5. Package-assignment analysis (bắt buộc, yêu cầu task — KHÔNG invent package thứ mười)

**Xác nhận tường minh bắt buộc (v0.2 correction, đóng `P16-UR-A-MIN-01`):** MỌI "Package
lifecycle" hệ quả liệt kê dưới đây KHÔNG PHẢI một transition tự động — một package
`Consolidated Stable` KHÔNG "revert thẳng sang candidate" chỉ vì evidence này gợi ý một
semantic modification. Baseline `Consolidated Stable` hiện tại VẪN LÀ controlling cho
tới khi một lifecycle transaction được authorize riêng biệt (Product Owner) thực hiện
thay đổi đó. Bất kỳ semantic modification nào (edge mới, `responsibilities` expansion)
đòi hỏi MỘT governed reopening transaction HOẶC một successor candidate transaction —
SAU đó, Review A + Independent Review B + Product Owner reconsolidation decision MỚI
PHẢI hoàn tất TRƯỚC KHI baseline đã sửa đổi trở lại `Consolidated Stable`. Cơ chế
lifecycle CHÍNH XÁC (vd. có cần một transaction riêng để "mở" package trước khi sửa,
hay sửa VÀ mở là cùng một transaction — đúng tiền lệ custody-signing-service) KHÔNG
được quyết định bởi exploration này — CHỈ ghi nhận rằng KHÔNG có transition tự động
nào tồn tại.

```text
NAV-003 edge addition (Candidate A, §2.4):
  Package hợp pháp elaborate: Package 1.1 (registry dependency-graph authority, ĐÃ
    established, phase-1-plan.md) + Package 1.4 (API contract-surface authority, ĐÃ
    established) — CẢ HAI package ĐÃ tồn tại, KHÔNG cần phase-1-plan.md amendment.
  Registry alignment:      CẦN — Package 1.1 correction transaction (thêm edge), đúng
                           tiền lệ (custody-signing-service).
  Package lifecycle:       CẦN governed reopening transaction (KHÔNG tự động, xem xác
                           nhận trên) cho CẢ Package 1.1 VÀ Package 1.4 (parity
                           transcription correction) — Review A/Independent Review B/
                           Product Owner reconsolidation MỚI PHẢI hoàn tất cho MỖI
                           package trước khi trở lại Consolidated Stable.

VIEW-002 computation ownership (NẾU assign review-evidence-service, §3.2):
  Package hợp pháp elaborate: Package 1.5 (ĐÃ elaborate review-evidence-service) +
                           Package 1.1 (registry `responsibilities` field update —
                           một RESPONSIBILITY EXPANSION, KHÔNG CHỈ edge).
  Phase-1-plan.md amendment: KHÔNG cần (Package 1.5 vẫn LÀ package hợp pháp cho module
                           này, đúng phase-1-plan.md hiện tại).
  Registry alignment:      CẦN — Package 1.1 correction để mở rộng `responsibilities`.
  Package lifecycle:       CẦN governed reopening transaction (KHÔNG tự động) cho
                           Package 1.1 VÀ Package 1.5, cùng nguyên tắc trên.

VIEW-003 computation ownership (NẾU assign replay-integration-service HOẶC decision-
  evaluation-engine, §4.3):
  Package hợp pháp elaborate: NẾU replay-integration-service → Package 1.3-A (structure-
                           regime-architecture.md, hiện Consolidated Stable) + Package
                           1.1. NẾU decision-evaluation-engine → Package 1.3-C
                           (strategy-decision-architecture.md, hiện Consolidated Stable)
                           + Package 1.1.
  Phase-1-plan.md amendment: KHÔNG cần — package đích ĐÃ hợp pháp cho module tương ứng.
  Registry alignment:      CẦN — Package 1.1 correction (`responsibilities` expansion).
  Package lifecycle:       CẦN governed reopening transaction (KHÔNG tự động) cho
                           Package 1.1 VÀ Package 1.3-A HOẶC Package 1.3-C (BA package
                           Consolidated Stable phải qua transaction riêng — chi phí
                           cascading LỚN HƠN NAV-003/VIEW-002, mỗi package tự đi qua
                           vòng Review A/Independent Review B/Product Owner
                           reconsolidation CỦA RIÊNG NÓ).

Module MỚI (bất kỳ candidate nào, nếu chọn):
  Vẫn CẦN Package 1.1 registration authority — KHÔNG tự động cần một package Phase 1
    thứ mười; module MỚI vẫn được MỘT trong chín package hiện có elaborate (tùy domain
    concern), KHÔNG invent package mới. Tài liệu này KHÔNG đề xuất module mới nào.
```

## 6. ADR trigger analysis (Governance §4b, áp dụng riêng biệt — bắt buộc, yêu cầu task)

**Khung phân loại ba nhánh (v0.2 correction, đóng `P16-UR-A-MAJ-02`, thay thế "CONDITIONALLY REQUIRED" mơ hồ của v0.1):**

```text
A. Source clarification only:
   Tài liệu exploration NÀY (v0.2) tự nó KHÔNG quyết định architecture nào — mọi nội
   dung ở đây LÀ evidence, KHÔNG author/approve ADR. Nhánh A áp dụng cho CHÍNH
   transaction này, KHÔNG áp dụng cho candidate resolution tương lai.

B. ADR CÓ THỂ KHÔNG cần (subject to Governance §4b review riêng, KHÔNG tự quyết tại
   đây): NẾU controlling sources (một khi làm rõ đầy đủ) chứng minh MỘT module hiện có
   đã sở hữu ĐẦY ĐỦ trách nhiệm liên quan, VÀ KHÔNG dependency edge/contract-category/
   module-boundary change nào cần thiết để expose nó — trường hợp này CÓ THỂ rơi vào
   "ADR Not Required"/"ADR Optional" (§4b), NHƯNG phải qua một Governance §4b review
   riêng biệt để xác nhận, KHÔNG tự động.

C. ADR REQUIRED — NẾU resolution đòi hỏi BẤT KỲ mục nào sau: (i) registered
   responsibility expansion; (ii) computation-owner selection (chọn module nào thực
   thi một computation trước đây chưa ai sở hữu); (iii) module MỚI; (iv) dependency
   edge MỚI; (v) multi-module orchestration boundary MỚI; (vi) hard-to-reverse
   contract ownership decision.
```

```text
NAV-003 dependency edge:
  ADR REQUIRED (Nhánh C, mục iv) — khớp CHÍNH XÁC §4b table entry "Module Taxonomy/
  dependency graph" thay đổi → "Bắt buộc." KHÔNG mơ hồ.

VIEW-002 responsibility/contract ownership (đánh giá riêng biệt theo khung ba nhánh):
  Mọi candidate đã evaluate tại §3.2 (review-evidence-service/replay-integration-
  service/multi-source aggregation/module mới) ĐỀU rơi vào Nhánh C — review-evidence-
  service candidate đòi hỏi registered responsibility expansion (mục i); multi-source
  aggregation candidate đòi hỏi computation-owner selection CỘNG khả năng một
  orchestration boundary mới (mục ii/v); module mới đòi hỏi mục iii. KHÔNG candidate
  nào trong bốn candidate đã evaluate rơi vào Nhánh B (KHÔNG module hiện có nào ĐÃ sở
  hữu đầy đủ trách nhiệm nà KHÔNG cần thay đổi gì) — CHỈ candidate "giữ blocked" (KHÔNG
  resolve gì) tránh được câu hỏi ADR, NHƯNG đó KHÔNG PHẢI một resolution. KẾT LUẬN: ADR
  REQUIRED cho MỌI resolution path khả thi đã evaluate tại §3.2.

VIEW-003 responsibility/module/contract ownership (đánh giá riêng biệt theo khung ba
  nhánh, KHÔNG dùng lại kết luận VIEW-002):
  Mọi candidate đã evaluate tại §4.3 (decision-evaluation-engine/replay-integration-
  service/review-evidence-service/decision-authority-service/module mới) ĐỀU rơi vào
  Nhánh C — bốn candidate mở rộng module hiện có đòi hỏi registered responsibility
  expansion (mục i) CỘNG computation-owner selection (mục ii, vì `canonical semantic-
  decision hash` computation trước đây chưa ai sở hữu, §4.2); candidate module mới đòi
  hỏi mục iii VÀ iv. KHÔNG candidate nào rơi vào Nhánh B. KẾT LUẬN: ADR REQUIRED cho
  MỌI resolution path khả thi đã evaluate tại §4.3 — ĐỘC LẬP với kết luận VIEW-002,
  KHÔNG suy ra từ nó.

Xác nhận tường minh: BA quyết định này KHÔNG combine mặc định thành MỘT ADR duy nhất
  — mỗi decision (NAV-003/VIEW-002/VIEW-003) có phạm vi module/package/responsibility
  khác nhau, PHẢI đánh giá VÀ author ADR riêng biệt, đúng yêu cầu task "Do not combine
  the decisions by default." Kết luận "ADR REQUIRED" trên KHÔNG PHẢI approval hay
  soạn thảo nội dung ADR — CHỈ LÀ phân loại theo Governance §4b áp dụng cho candidate
  đã evaluate, KHÔNG chọn owner/module/edge nào.
```

## 7. Candidate decision records (ba bản ghi trung lập, bắt buộc yêu cầu task)

### 7.1 Candidate NAV-003 resolution

```text
Options:                  A. Thêm edge command-query-api-surface→backtest-orchestrator.
                          B. Route qua module hiện có (chưa xác nhận viable).
                          C. Đổi Product/UX semantics (ngoài thẩm quyền).
                          D. Giữ blocked.
Evidence for A:            Khớp mẫu hình routing-mechanics 16-edge hiện có; KHÔNG đe
                          dọa DD-001 Ở TẦNG mechanics — NHƯNG semantic eligibility đầy
                          đủ VẪN contingent (§2.2 v0.2 correction), KHÔNG "cao" không
                          điều kiện.
Evidence against A:        Kích hoạt ADR Required + reopen hai package Consolidated
                          Stable (1.1, 1.4) qua governed lifecycle transaction (§5
                          qualification); CỘNG prerequisite semantic clarification
                          (run identity/correlation/command-query boundary, §2.2)
                          CHƯA thỏa.
Unresolved question:       §2.5 (hai câu hỏi) CỘNG §2.2's prerequisite semantic
                          clarification (run identity/correlation/command-query
                          contract boundary).
Prerequisite decision:     Xác nhận run-identity correlation ownership (§2.5 mục 2)
                          VÀ làm rõ Backtest create/query contract semantics (§2.2)
                          TRƯỚC KHI chọn giữa A và B — CẢ HAI PHẢI thỏa, KHÔNG CHỈ
                          mục §2.5.
Affected artifact (nếu A): module-registry.yaml, system-decomposition.md, api-
                          architecture.md, ux-architecture.md (correction theo sau).
Lifecycle consequence:     Package 1.1 VÀ Package 1.4 CẦN một governed lifecycle
                          reopening transaction (KHÔNG tự động) trước khi trở lại
                          Consolidated Stable (§5 qualification, đóng `P16-UR-A-
                          MIN-01`) — Review A + Independent Review B + Product Owner
                          reconsolidation decision MỚI PHẢI hoàn tất cho MỖI package;
                          Package 1.6 vẫn candidate cho tới khi binding resolve.
Recommendation:            Evidence KHÔNG đủ để nghiêng dứt khoát về Candidate A tại
                          v0.2 — routing-mechanics fit tồn tại NHƯNG semantic-readiness
                          prerequisite (§2.2) CHƯA thỏa; câu hỏi §2.5 mục 2
                          (authoritative-fact ownership của run-identity correlation)
                          VÀ Backtest create/query contract semantics (§2.2) NÊN resolve
                          trước khi tiến hành ADR authoring, vì cả hai ảnh hưởng NỘI
                          DUNG ADR đó.
Xác nhận tường minh:       Recommendation trên KHÔNG PHẢI approval — CHỈ là quan sát
                          dựa trên evidence đã thu thập, chờ Product Owner/governed
                          transaction quyết định.
```

### 7.2 Candidate VIEW-002 clarification/ownership path

```text
Options:                  review-evidence-service (expand); replay-integration-
                          service (weak fit); multi-source aggregation tại API
                          Surface (layer chưa xác định); module mới; giữ blocked.
Evidence for:              review-evidence-service có overlap dependency cao nhất với
                          bốn/năm stream cần thiết.
Evidence against:          Bốn missing semantic item (§3.1) CHƯA resolve — assign
                          ownership TRƯỚC KHI semantics đầy đủ sẽ lặp lại chính lỗi
                          Package 1.4 P14-A-MAJ-01/Package 1.6 P16-A-MAJ-02 (ownership
                          suy từ data proximity, KHÔNG từ contract established).
Unresolved question:       Cả bốn missing semantic item (§3.1) PHẢI resolve trước khi
                          ownership có thể được assign một cách có căn cứ.
Prerequisite decision:     (a) Định nghĩa Research-session interval identity mechanism;
                          (b) định nghĩa evidence-completeness mechanism; (c) định
                          nghĩa correction-arrival handling — CẢ BA có thể cần một
                          Product/UX Domain Contract clarification TRƯỚC KHI ownership
                          quyết định có ý nghĩa.
Affected artifact (tiềm
  năng):                   use-case-workflow.md (UC-003 elaboration, nếu Product Owner
                          chọn làm rõ), module-registry.yaml (`responsibilities`, nếu
                          review-evidence-service chọn), database-architecture.md/api-
                          architecture.md/ux-architecture.md (correction theo sau).
ADR trigger:               ADR REQUIRED cho mọi candidate resolution path khả thi đã
                          evaluate (§6, v0.2 correction) — KHÔNG candidate nào rơi vào
                          Nhánh B (KHÔNG module hiện có nào đã sở hữu đầy đủ trách
                          nhiệm mà không cần thay đổi gì).
Lifecycle consequence:     Package 1.1 + package elaborate module được chọn CẦN một
                          governed lifecycle reopening transaction (KHÔNG tự động, §5
                          qualification) trước khi trở lại Consolidated Stable — Review
                          A + Independent Review B + Product Owner reconsolidation
                          decision MỚI PHẢI hoàn tất cho MỖI package liên quan; Package
                          1.6 vẫn blocked cho tới khi resolve.
Recommendation:            Evidence KHÔNG đủ mạnh để nghiêng về một candidate cụ thể —
                          bốn missing semantic item PHẢI resolve TRƯỚC (khả năng đòi
                          hỏi một Product/UX clarification transaction, KHÔNG chỉ một
                          architecture ownership assignment).
Xác nhận tường minh:       KHÔNG có recommendation approval nào tại đây — CHỈ ghi nhận
                          evidence gap cần lấp trước.
```

### 7.3 Candidate VIEW-003 clarification/ownership/package path

```text
Options:                  decision-evaluation-engine (expand); replay-integration-
                          service (expand); review-evidence-service (weak fit);
                          decision-authority-service (architecturally risky); module
                          non-authoritative mới; giữ blocked.
Evidence for:              replay-integration-service sở hữu canonical Replay Cursor
                          concept sẵn có — gần gũi semantic nhất về mặt "cursor-bounded
                          computation."
Evidence against:          replay-integration-service's OWN contract tường minh cấm
                          "author fact mới" — recomputation LÀ một hành động khác biệt
                          khỏi "fold recorded fact"; decision-evaluation-engine THIẾU
                          registered dependency tới bất kỳ historical-cursor capability
                          nào; `canonical semantic-decision hash` — thành phần TRUNG
                          TÂM của toàn bộ phép so sánh — HOÀN TOÀN chưa định nghĩa
                          (§4.2), khiến MỌI ownership assignment tại thời điểm này là
                          prematured.
Unresolved question:       `canonical semantic-decision hash` field-list definition
                          (§4.2, gap nghiêm trọng nhất); INDETERMINATE/missing-evidence
                          path cho VIEW-003 (KHÔNG established, §4.1) — Product Owner
                          cần quyết định liệu VIEW-003 có nên có ba outcome (giống
                          VIEW-002) hay giữ nguyên hai outcome (MATCH/MISMATCH).
Prerequisite decision:     (a) decision.md correction để định nghĩa `canonical
                          semantic-decision hash` field-list (Package 0.2-C4 semantic
                          transaction, NGOÀI phạm vi Package 1.x architecture); (b)
                          Product Owner quyết định VIEW-003 có cần INDETERMINATE
                          equivalent hay không; (c) CẢ HAI PHẢI resolve TRƯỚC KHI
                          ownership có ý nghĩa được assign.
Affected artifact (tiềm
  năng):                   decision.md (semantic amendment, nếu Product Owner chọn),
                          ux-blueprint.md (nếu STATE mới cần thêm), module-registry.yaml
                          (`responsibilities`), system-decomposition.md, api-
                          architecture.md, database-architecture.md/ux-architecture.md
                          (correction theo sau).
ADR trigger:               ADR REQUIRED cho mọi candidate resolution path khả thi đã
                          evaluate (§6, v0.2 correction), ĐỘC LẬP với kết luận VIEW-002
                          — KHÔNG candidate nào rơi vào Nhánh B.
Lifecycle consequence:     TIỀM NĂNG LỚN NHẤT trong ba candidate — có thể chạm Domain
                          Contract semantic (decision.md, Package 0.2-C4, đã
                          Consolidated Stable) CỘNG hai/ba package architecture (1.1 +
                          1.3-A hoặc 1.3-C + 1.4/1.5/1.6 theo sau) — MỖI package/Domain
                          Contract liên quan CẦN governed reopening RIÊNG (KHÔNG tự
                          động, §5 qualification): Review A + Independent Review B +
                          Product Owner reconsolidation decision MỚI cho từng artifact
                          trước khi trở lại Consolidated Stable.
Recommendation:            Evidence xác nhận rõ ràng: `canonical semantic-decision
                          hash` definition gap PHẢI resolve TRƯỚC bất kỳ ownership
                          decision nào — đây LÀ prerequisite cứng, KHÔNG một candidate
                          nào trong sáu candidate có thể tiến triển có ý nghĩa nếu
                          thiếu định nghĩa đó.
Xác nhận tường minh:       KHÔNG có recommendation approval nào — CHỈ xác nhận một
                          prerequisite cứng đã tìm thấy qua evidence.
```

## 8. Ordered transaction map (bắt buộc, yêu cầu task — trình tự governed nhỏ nhất)

```text
Bước 1 — Source clarification (transaction NÀY, hoàn tất khi Review A của chính
  tài liệu này CLEAN): KHÔNG quyết định gì, CHỈ decision evidence.

Bước 2 — Product/Domain semantic amendment (CÓ ĐIỀU KIỆN, riêng biệt cho từng vấn
  đề):
  (a) NAV-003: CÓ THỂ cần (v0.2 correction, đóng `P16-UR-A-MAJ-01`) — UC-006/007/010
      mô tả BEHAVIOR mức Product NHƯNG KHÔNG established đầy đủ Backtest run-identity
      ownership classification (authoritative fact/non-authoritative result/
      correlation tag/khác, §2.2) hay create/query contract semantics đầy đủ; một
      clarification (Domain Contract amendment HOẶC một xác nhận đủ tại tầng
      architecture, tùy Product Owner) khả năng CẦN TRƯỚC KHI edge decision có căn cứ
      semantic đầy đủ.
  (b) VIEW-002: CÓ THỂ cần — bốn missing semantic item (§3.1) khả năng đòi hỏi một
      use-case-workflow.md correction transaction (Product Owner authorized) TRƯỚC
      khi ownership decision.
  (c) VIEW-003: CẦN — decision.md correction để định nghĩa `canonical semantic-
      decision hash` field-list (§4.2 prerequisite cứng); VÀ một Product Owner
      quyết định về INDETERMINATE-equivalent cho VIEW-003.
  Bước này PHẢI tách biệt khỏi Bước 3 — semantic amendment là Domain Contract
  authority (Package 0.2-C4/C3), KHÔNG PHẢI Phase 1 architecture authority.

Bước 3 — ADR authoring/review/approval (riêng biệt cho MỖI vấn đề, KHÔNG combine mặc
  định, §6, v0.2 correction đóng `P16-UR-A-MAJ-02`): NAV-003 ADR (Required); VIEW-002
  ADR (Required cho mọi candidate khả thi đã evaluate, sau Bước 2b); VIEW-003 ADR
  (Required cho mọi candidate khả thi đã evaluate, sau Bước 2c) — phân loại theo khung
  ba nhánh A/B/C (§6), KHÔNG "Conditionally Required" mơ hồ.

Bước 4 — Package 1.1 alignment (riêng biệt cho từng edge/responsibility change đã ADR
  Approve): registry dependency edge (NAV-003) VÀ/HOẶC `responsibilities` field
  expansion (VIEW-002/VIEW-003) — MỖI thay đổi LÀ một Package 1.1 correction
  transaction riêng, đúng tiền lệ đã dùng (custody-signing-service).

Bước 5 — Package elaboration (riêng biệt theo module bị ảnh hưởng): Package 1.5
  (review-evidence-service, nếu VIEW-002 chọn); Package 1.3-A HOẶC 1.3-C (replay-
  integration-service/decision-evaluation-engine, nếu VIEW-003 chọn) — MỖI package
  correction là MỘT transaction riêng, MỖI package tự đi qua vòng Review A +
  Independent Review B + Product Owner consolidation decision CỦA RIÊNG NÓ.

Bước 6 — Package 1.4 exposure (API Architecture correction): parity-transcription
  update cho edge/responsibility mới — transaction riêng, SAU Bước 4/5 hoàn tất cho
  đúng module liên quan.

Bước 7 — Package 1.6 correction (binding update): cập nhật NAV-003/VIEW-002/VIEW-003
  Table A/B để phản ánh route ĐÃ resolve — transaction riêng, SAU Bước 6.

Bước 8 — Bounded verification (Package 1.6): xác nhận correction Bước 7 CLEAN.

Bước 9 — Independent Review B (Package 1.6): CHỈ khả thi SAU Bước 8 CLEAN VÀ CẢ HAI
  Major prerequisite (NAV-003, VIEW-002/VIEW-003) đã resolve qua Bước 1–8.

Xác nhận tường minh (bắt buộc): Bước 2/3/4/5/6/7 PHẢI VẪN riêng biệt — KHÔNG bundle
  NAV-003 VÀ VIEW-002 VÀ VIEW-003 vào MỘT ADR/registry-correction/package-correction
  duy nhất, dù chúng phát sinh từ cùng Package 1.6 v0.2 correction. Mỗi vấn đề có
  phạm vi module/package/Domain-Contract khác nhau (§5/§6) — trộn lẫn sẽ vi phạm
  nguyên tắc bounded-transaction đã dùng xuyên suốt toàn bộ Phase 1 tới nay.
```

## 9. Preserved invariants (bắt buộc, yêu cầu task)

```text
Package 1.1–1.5 VẪN Consolidated Stable trong transaction này — KHÔNG artifact nào bị
  sửa.
Package 1.6 VẪN candidate — KHÔNG version bump, KHÔNG content edit tại
  ux-architecture.md.
DD-001 VÀ DD-003 VẪN Deferred.
`ux-application-shell` VẪN non-authoritative.
API Surface VẪN routing/exposure-only.
Review Evidence Service VẪN non-authoritative VÀ no-recompute, trừ khi một transaction
  approved TƯƠNG LAI đổi registered responsibility của nó.
Decision Authority Service VẪN authoritative CHỈ cho accepted Decision fact.
Position VẪN non-authoritative.
PAPER, Replay, VÀ Backtest VẪN tách biệt.
KHÔNG LIVE path hay authority nào được thêm.
LIVE VẪN Unauthorized.
```

## 10. Explicit non-goals (bắt buộc, yêu cầu task)

```text
KHÔNG approve/select một dependency edge nào.
KHÔNG đăng ký module nào.
KHÔNG chuyển giao responsibility nào.
KHÔNG amend Product/Domain semantics nào (decision.md/strategy.md/use-case-
  workflow.md/ux-blueprint.md KHÔNG sửa).
KHÔNG author/approve ADR nào.
KHÔNG sửa Package 1.1/1.4/1.5/1.6 architecture.
KHÔNG consolidate bất kỳ package nào.
KHÔNG mở Gate 2/Phase 2/LIVE.
KHÔNG combine ba quyết định (NAV-003/VIEW-002/VIEW-003) thành một quyết định/ADR duy
  nhất.
```

## 11. Review and lifecycle treatment

```text
Package 1.6 upstream-resolution exploration:
  version: 0.2
  status: Draft
  package lifecycle/readiness: exploratory candidate
  NON-AUTHORITATIVE, NOT APPROVED, NOT IMPLEMENTATION-READY
  Review A findings (P16-UR-A-MAJ-01/P16-UR-A-MAJ-02/P16-UR-A-MIN-01) corrected —
    pending bounded verification

Package 1.6 upstream-resolution exploration v0.1 LÀ candidate đầu tiên — v0.2 LÀ
  bounded correction đóng ba Review A finding trên v0.1 (banner đầu tài liệu), KHÔNG
  invalidate phần v0.1 KHÔNG bị finding chạm tới (Product Owner authorization, ba-vấn-
  đề separation, source extraction, graph mismatch, VIEW-002 missing semantic item,
  VIEW-003 semantic-hash gap, KHÔNG owner/dependency selection, KHÔNG package thứ
  mười — TẤT CẢ GIỮ NGUYÊN), KHÔNG design/select/author mới.

Package 1.6 (ux-architecture.md): version 0.2, candidate, KHÔNG thay đổi bởi tài liệu
  này — Independent Review B VẪN blocked, VẪN not Consolidated Stable.

Package 1.1–1.5: Consolidated Stable, KHÔNG thay đổi.

Phase 1: Active, not Complete. Gate 2: Not Ready. Phase 2: Not Opened. LIVE:
  Unauthorized — TẤT CẢ KHÔNG thay đổi bởi tài liệu này.
```
