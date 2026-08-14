---
id: use-case-workflow
title: Use Case & Workflow
version: "0.11"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-02"
last_review: null
next_review: null
---

# Use Case & Workflow

> **Vai trò của tài liệu này:** Artifact thứ hai của Package 0.3-B (Phase 0.3 — Product Requirement · Use Case & Workflow · UX Blueprint), phụ thuộc trực tiếp [`product-requirement.md`](./product-requirement.md) v0.2 Draft (Package 0.3-A, `Consolidated Stable`). Dịch 34 requirement (`PR-001`–`PR-034`) thành hành vi user journey/use case cụ thể, testable — sở hữu **user journey, use-case behavior, precondition, trigger, main flow, alternate flow, observable outcome, handoff** cho sáu giai đoạn Research→Replay→Backtest→Paper→Review→Improve. Draft, chưa Approved/Locked, **chưa `Consolidated Stable`**. Tài liệu này KHÔNG tạo product requirement mới — MỌI bước workflow PHẢI truy vết về một hoặc nhiều `PR-XXX` đã tồn tại; KHÔNG sở hữu screen design/UX component (thuộc Package 0.3-C, chưa author); KHÔNG sở hữu domain semantics (thuộc `/docs/domain/`, không sửa); KHÔNG sở hữu architecture (Phase 1).

**Authority boundary:** tài liệu này sở hữu **use-case/workflow content** cho Phase 0.3 — KHÔNG sở hữu product requirement content (thuộc `product-requirement.md`, Package 0.3-A, không sửa), KHÔNG sở hữu screen layout/wireframe/component hierarchy (thuộc Package 0.3-C `ux-blueprint.md`, chưa author), KHÔNG sở hữu domain semantics/state machine (thuộc `/docs/domain/`, không sửa/redefine), KHÔNG sở hữu architecture quyết định (Phase 1, `/docs/architecture/`), KHÔNG đóng Open Question nào (`OQ-002`/`OQ-003` vẫn `Open`, xem §10), KHÔNG authorize Live, KHÔNG tuyên bố Phase 0.3/Phase 0 hoàn thành, KHÔNG mark chính nó `Consolidated Stable`.

**Quy tắc traceability nguồn (kế thừa nguyên vẹn `product-requirement.md` §"Authority boundary", đóng `P03A-MIN-02`):** mọi Use Case/workflow step PHẢI có một hoặc nhiều `PR-XXX` áp dụng — CÓ THỂ kết hợp nhiều PR; mọi PR trích dẫn phải material (đóng góp thực chất cho behavior mô tả); không Use Case nào được phép mồ côi PR traceability.

**v0.2 — bounded correction (đóng consolidated Review A + Independent Review B findings, hai Major + năm Minor):** (1) `P03B-MAJ-01` — Backtest → Paper handoff và UC-011 viết lại: Backtest/Research Decision identity KHÔNG BAO GIỜ được carry forward/promote/reuse làm authoritative PAPER Decision ancestor; PAPER entry đòi hỏi một PAPER-context authoritative Decision lineage RIÊNG BIỆT; cơ chế thiết lập chính xác PAPER-context Decision là deferred dependency (§9d); workflow có thể dừng TRƯỚC PAPER execution khi không có PAPER-context Decision lineage eligible. (2) `P03B-MAJ-02` — UC-020 viết lại: tách bạch tường minh Backtest comparison (non-PAPER authority) khỏi PAPER comparison (authoritative); cross-mode viewing CHỈ là juxtaposition hiển thị, KHÔNG merge identity/authority, KHÔNG unified execution-outcome fact, KHÔNG normalization/scoring chung. (3) `P03B-MIN-01` — UC-011 reframe: "Initiate/request PAPER execution" thay vì "Submit a PAPER Order" — user cung cấp intent, KHÔNG authoritative Order payload. (4) `P03B-MIN-02` — UC-021 thêm bounded alternate/failure path khi historical evidence không khả dụng — bỏ overclaim "luôn khả dụng." (5) `P03B-MIN-03` — UC-007 bỏ ngôn ngữ "đã bị loại bỏ" (implied deletion lifecycle), thay bằng "run identity không resolve được/evidence không khả dụng" + bốn nguyên tắc fallback. (6) `P03B-MIN-04` — UC-020 khôi phục traceability đầy đủ `PR-031`/`PR-032`, phản ánh yêu cầu historical old-version evidence của `PR-032` trong Main flow/Evidence consumed. (7) `P03B-MIN-05` — UC-003 thêm observable verification outcome PASSED/FAILED/INDETERMINATE — KHÔNG tạo entity/event "ResearchVerification" mới. Bounded — không đổi 21 Use Case ID, không đổi sáu-giai-đoạn lifecycle, không đóng OQ-002/OQ-003, không Approve/Lock/Consolidate.

**v0.3 — narrow delta correction (đóng `P03B-DELTA-MIN-01`):** UC-021 viết lại đầy đủ — trước đây CHỈ operationalize Decision fact lịch sử, dù Goal/UC-020 dependency đòi hỏi phạm vi rộng hơn. Nay UC-021 resolve ĐỘC LẬP, tách bạch, hai họ evidence lịch sử cho một Strategy Definition Version cũ: **Backtest evidence family** (Decision/RiskEvaluation trace, simulated economic evidence, exposure/position progression, strategy-level evaluable result, run identity/version/configuration context — non-PAPER authority) VÀ **PAPER evidence family** (Decision, Trade Intent, RiskEvaluation, Execution Intent, Order, OrderSubmissionRequest, ExecutionResult, Fill, Position — authoritative, với ExecutionResultComputation/PaperExecutionObservation làm supporting evidence khi cần, KHÔNG redefine semantics). Danh tính Strategy Definition Version LUÔN hiển thị. Missing evidence được identify theo TỪNG họ/loại — KHÔNG ngụ ý toàn bộ lịch sử mất khi chỉ một phần thiếu; evidence khả dụng khác vẫn hiển thị nhưng đánh dấu incomplete. UC-020 cập nhật tương ứng để tiêu thụ đúng mode-separated scope này, KHÔNG ngụ ý UC-021 trả về một cross-mode evidence object chung. Bounded — không thêm/renumber Use Case, không domain entity/schema/unified outcome model/retention policy/architecture mới, giữ nguyên toàn bộ bảy finding đã đóng ở v0.2.

**v0.4 — bounded correction (đóng `F-03`, Phase 0 Exit Readiness Audit MAJOR finding — restore complete PR→UC→UX lineage cho `PR-004`/`PR-005`):** `product-requirement.md` v0.2 định nghĩa `PR-004` (Xem Decision với outcome tường minh — LONG/SHORT + Strategy Instance nguồn gốc) và `PR-005` (Xem evidence trace đầy đủ cho một Decision — input snapshot, causation chain) nhưng trước v0.4 không Use Case nào trích dẫn hai PR này, dù Package 0.3-C UX Blueprint v0.4 đã gán chúng vào `SCR-004`/`SCR-006`/`SCR-008` — tạo khoảng trống PR→UC→UX lineage. Inspect `UC-007`/`UC-008`/`UC-009`/`UC-011`/`UC-016` (ứng viên hợp lý nhất theo behavior mô tả): `UC-007` Main flow bước 2 đã tường minh ghi "mỗi Decision hiển thị outcome + evidence trace" — khớp trực tiếp CẢ HAI PR, thêm `PR-004`/`PR-005`. `UC-011` Preconditions/Main flow yêu cầu tường minh Decision outcome LONG/SHORT của PAPER-context Decision lineage VÀ Observable outcome hiển thị toàn bộ chuỗi C7 evidence — thêm `PR-004`/`PR-005`. `UC-016` Goal/Main flow CHÍNH LÀ truy vết evidence trace/causation chain đầy đủ về Decision gốc (bao gồm outcome + Strategy Instance nguồn gốc của Decision đó) — thêm `PR-004`/`PR-005`. `UC-008`/`UC-009` KHÔNG thêm — cả hai tiêu thụ evidence đã có của UC-007 (economic evidence/evaluable result phái sinh), KHÔNG tự mình hiển thị lại Decision outcome/evidence trace gốc. KHÔNG Use Case mới tạo; không renumber; `UC-001`–`UC-021` giữ nguyên identity. §5 catalogue VÀ §6 detailed block của ba UC cập nhật đồng bộ (§9a: "mỗi Use Case tại §6 lặp lại chính xác mapping đó"). `SCR-004`/`SCR-006`/`SCR-008` (Package 0.3-C, KHÔNG sửa) đã trace đúng `UC-007`/`UC-011`/`UC-016` từ trước — lineage nay resolve đầy đủ, revalidated KHÔNG cần sửa nội dung `ux-blueprint.md`.

**v0.5 — bounded semantic correction (đóng `P03B-V04-A-MAJ-01`):** v0.4 chỉ MECHANICALLY gán `PR-004`/`PR-005` vào trường "PR traceability" của `UC-007`/`UC-011`/`UC-016`, nhưng chưa operationalize đầy đủ acceptance evidence của hai PR đó trong behavior thực tế (Main flow/Observable outcome/Evidence consumed). Nay: `UC-007` Main flow bước 2 viết lại — mỗi Decision hiển thị tường minh đúng một outcome (LONG/SHORT/không có exposure mới), Strategy Instance CHÍNH XÁC + Strategy Definition Version/configuration context nguồn gốc, VÀ evidence đã dùng để tạo ra Decision đó (recorded input snapshot/causation reference/RiskEvaluation liên quan) — resolve TRỰC TIẾP từ recorded fact, KHÔNG suy diễn/tính lại sau sự kiện. `UC-011` Preconditions/Main flow/Observable outcome viết lại — tách bạch tường minh **upstream Decision evidence** (outcome + Strategy Instance/Definition Version nguồn gốc + input snapshot/evidence reference, hiển thị TRƯỚC khi khởi tạo PAPER execution) khỏi **downstream C7 causation** (fact do CHÍNH hành động khởi tạo sinh ra) — downstream chain KHÔNG tự nó ngụ ý thỏa evidence trace của Decision. `UC-016` thêm Main flow bước 3 mới — khi đạt tới Decision gốc, hiển thị tường minh **Decision explainability evidence** (input snapshot/configuration → Decision), tách biệt khỏi **downstream lineage** ở bước 2 (Position/Fill → ... → Decision). `UC-008`/`UC-009` KHÔNG đổi, KHÔNG nhận `PR-004`/`PR-005`. §5 catalogue giữ nguyên (đã đúng từ v0.4); chỉ §6 detailed block của ba UC, §9b annotation, và §12 acceptance criteria cập nhật. Backtest vẫn non-PAPER simulated (KHÔNG entity Backtest mới, KHÔNG gọi material này authoritative PAPER Order/ExecutionResult/Fill/Position, domain representation vẫn deferred); PAPER-context Decision separation, no-clone/no-carry-forward/no-promote/no-reuse, canonical semantic-decision hash, `OQ-002`/`OQ-003` `Open`, Live `Unauthorized` giữ nguyên vẹn. Bounded — không đổi 21 Use Case ID, không đổi sáu-giai-đoạn lifecycle, không thêm PR/UC mới.

**v0.6 — final consolidated correction (đóng `P03B-V05-B-MAJ-01`, frozen finding):** v0.5 sửa gap operationalization của `PR-004`/`PR-005` nhưng tự nó mắc causal-direction error tại `UC-007`: nhóm evidence "đã dùng để tạo ra Decision" liệt kê CẢ "RiskEvaluation liên quan" — SAI, vì RiskEvaluation (risk.md §1) là bản ghi đánh giá MỘT Trade Intent, mà Trade Intent chỉ tồn tại SAU KHI Decision result = LONG/SHORT (decision.md §9) — RiskEvaluation luôn causally downstream của Decision, KHÔNG BAO GIỜ là input tạo ra nó. Sửa: `UC-007` Main flow bước 2 tách bạch tường minh BA nhóm — (A) Decision outcome LONG/SHORT/NO_ACTION (decision.md `result` enum); (B) upstream Decision origin/explainability — Strategy Instance/Definition Version/configuration, recorded input snapshot, recorded evaluation/configuration evidence, KHÔNG còn chứa RiskEvaluation; (C) downstream lineage KHI TỒN TẠI — Trade Intent/RiskEvaluation/Execution Intent/related fact, hiển thị tách biệt khỏi B với phát biểu tường minh "causally derived from/related to Decision, KHÔNG phải evidence dùng để tạo ra nó." Cùng phân biệt áp dụng đồng bộ tại Observable outcome, Evidence consumed, PR traceability rationale, và §12 acceptance criterion 21. `UC-011`/`UC-016`/`UC-008`/`UC-009` KHÔNG đổi — finding chỉ về `UC-007`. `UC-001`–`UC-021` giữ nguyên identity; KHÔNG PR/UC/domain entity mới; Backtest non-PAPER/PAPER-context Decision separation/OQ-002/OQ-003 Open/Live Unauthorized giữ nguyên vẹn. Đây là correction cuối cùng cho frozen finding này — bounded delta verification tiếp theo chỉ xét lại đúng phạm vi này, KHÔNG mở lại toàn bộ Package 0.3-B review.

**VIEW-003 Replay Parity Semantic Clarification — Consolidated Stable (lifecycle, Product Owner decision, verbatim: "APPROVE CONSOLIDATION"; date 2026-08-06, giờ không được chỉ định trong yêu cầu transaction) — mechanical lifecycle transaction, `version: "0.8"` UNCHANGED.** Review evidence: Review A (REVISE trên v0.7, đóng bốn finding `P16-V003-A-MAJ-01`/`P16-V003-A-MAJ-02`/`P16-V003-A-MAJ-03`/`P16-V003-A-MIN-01` qua v0.8 — cùng finding set đóng tại `decision.md` v0.5) → bounded correction verification: CLEAN → Independent Review B: CLEAN → Product Owner consolidation decision. `lifecycle: candidate → Consolidated Stable` — KHÔNG semantic content nào đổi: `UC-005` Main flow/Alternate-failure branch outcome MATCH/MISMATCH/INDETERMINATE, `UC-001`–`UC-021` identity, Backtest non-PAPER/PAPER-context separation — byte-identical, CHỈ lifecycle-state label thay đổi. `decision.md` §9a nay cũng `Consolidated Stable` (xem `decision.md` v0.5 banner) — pointer KHÔNG còn trỏ tới nội dung pending review. `status: Draft`, `approved_by: null`, `approved_at: null` KHÔNG đổi. `OQ-002`/`OQ-003` VẪN `Open`; `NAV-003`/`VIEW-002` VẪN unresolved; Package 1.6 lifecycle KHÔNG đổi bởi transaction này. KHÔNG owner/module/package/dependency edge/API path/ADR/implementation authority nào được chọn tại transaction này.

**v0.7 — CANDIDATE semantic clarification (2026-08-06) — HISTORICAL, superseded bởi VIEW-003 Consolidated Stable banner trên; tại thời điểm authoring: KHÔNG Approved/Consolidated, pending Review A/Independent Review B/Product Owner decision — Product Owner authorized (timestamp 2026-08-06T09:21:00+07:00) bounded source-semantics clarification cho VIEW-003 replay parity verification:** `UC-005` (§6) thêm một branch outcome thứ ba, tường minh — bên cạnh match/mismatch đã có, nay hỗ trợ **INDETERMINATE**, dùng khi input evidence cho parity recomputation thiếu/stale/invalidated/ambiguous/non-evaluable — KHÔNG ép buộc hệ thống trả về match hay mismatch giả tạo trong tình huống này. Định nghĩa canonical semantic-decision hash được dùng bởi `UC-005` nay resolve cụ thể tại `decision.md` §9a (Canonical Decision Semantic Representation/Digest, CANDIDATE cùng transaction) — xem `product-requirement.md` v0.3. Bounded — KHÔNG thêm/renumber Use Case, KHÔNG đổi `UC-001`–`UC-021` identity nào khác ngoài `UC-005`, KHÔNG domain entity/event mới (branch outcome này là workflow-visible, non-authoritative — cùng pattern đã dùng cho `UC-003` PASSED/FAILED/INDETERMINATE tại v0.2), KHÔNG chọn computation owner/module/package/dependency edge/ADR, KHÔNG đóng `OQ-002`/`OQ-003`, KHÔNG Approve/Lock/Consolidate.

**v0.8 — CANDIDATE bounded correction (2026-08-06) — HISTORICAL, superseded bởi VIEW-003 Consolidated Stable banner trên; tại thời điểm authoring: KHÔNG Approved/Consolidated, pending bounded verification/Independent Review B/Product Owner decision — đóng bốn Review A finding trên `decision.md` §9a v0.4 (`P16-V003-A-MAJ-01`/`P16-V003-A-MAJ-02`/`P16-V003-A-MAJ-03`/`P16-V003-A-MIN-01`, xem `decision.md` v0.5):** `UC-005` (§6) Main flow bước 2/Alternate-failure (b) cập nhật — INDETERMINATE nay bao gồm tường minh trường hợp implementation identity (`decision_implementation_version`) đã establish tại recorded Decision NHƯNG một trong hai phía không resolve/reproduce được, VÀ trường hợp digest-definition (khi dùng digest) unresolved/incompatible. KHÔNG thêm branch outcome thứ tư — vẫn đúng ba outcome MATCH/MISMATCH/INDETERMINATE (v0.7). KHÔNG thêm/renumber Use Case, KHÔNG đổi `UC-001`–`UC-021` identity nào khác ngoài `UC-005`, KHÔNG domain entity/event mới, KHÔNG chọn computation owner/module/package/dependency edge/ADR, KHÔNG redesign VIEW-003, KHÔNG đóng `OQ-002`/`OQ-003`, KHÔNG Approve/Lock/Consolidate.

**v0.9 — CANDIDATE bounded semantic correction (2026-08-14), đóng `P2-BCC-MAJ-01` (Phase-2
Full-Scope Backward Consistency Check MAJOR finding) — KHÔNG Approved/Consolidated, pending Review
A/Independent Review B/Product Owner decision:** `UC-004` Main flow bước 2/3 và Evidence consumed
viết lại — trước đây mô tả "Toàn bộ authoritative event stream Decision→...→Position" và ngụ ý
Position là một fact có `recorded_time` như mọi fact khác trong lineage, mâu thuẫn trực tiếp với
`position.md` §1 (Position là `kind: read_model`, derived projection, non-authoritative, KHÔNG có
event stream riêng, dẫn xuất hoàn toàn từ `eligible_as_position_contributing_fill`, fill.md §6).
Sửa: tách bạch tường minh (a) authoritative recorded fact lineage Decision→Trade Intent→
RiskEvaluation→Execution Intent→Order→ExecutionResult→Fill — hiển thị theo `recorded_time ≤ C`
(no-look-ahead, KHÔNG đổi) — KHỎI (b) Position — derived, deterministic, non-authoritative
projection, reconstruct TẠI CÙNG cursor C, KHÔNG PHẢI fact riêng, KHÔNG event stream riêng.
Position VẪN LÀ một phần bắt buộc của `ReplayState(C)` hiển thị (KHÔNG loại bỏ khỏi lineage) —
CHỈ authority-class của nó được sửa cho khớp `position.md` đã pin từ trước. KHÔNG đổi canonical
Replay Cursor, no-look-ahead rule, UC-004 identity/Goal/Trigger/Preconditions/Alternate-failure/
PR traceability/Domain vocabulary/Out-of-scope boundary, KHÔNG UC mới/renumber, KHÔNG domain
entity/event mới (`ReplayPosition` KHÔNG tạo), KHÔNG sửa `position.md`/`fill.md`/`replay-event.md`
(Domain Contract, không sửa). `UC-020`/`UC-021` (đã tự phân biệt Backtest non-PAPER vs PAPER
authoritative từ trước, `P03B-DELTA-MIN-01`) KHÔNG chạm — finding này CHỈ về `UC-004`. Trạng thái:
**CANDIDATE, pending governed review** — KHÔNG tự consolidate, KHÔNG ghi đè lịch sử Review/
Consolidated Stable đã có (banner `VIEW-003 Replay Parity Semantic Clarification — Consolidated
Stable` phía trên giữ nguyên, áp dụng cho `UC-005`, KHÔNG áp dụng cho `UC-004`).

**v0.10 — CANDIDATE bounded semantic correction (2026-08-14), đóng `P2-BCC-MAJ01-A-MAJ-01`
(Review A finding trên P2-BCC-MAJ-01 authority correction candidate v0.9) — KHÔNG Approved/
Consolidated, pending bounded Review A re-review/Independent Review B/Product Owner decision:**
`UC-004` Goal viết lại — trước đây "xem lại CHÍNH XÁC state authoritative đã tồn tại tại cursor
đó" vẫn dùng ngôn ngữ "state authoritative" phổ quát cho TOÀN BỘ `ReplayState(C)`, mâu thuẫn chi
tiết đã sửa tại Main flow bước 2/3 và Evidence consumed (v0.9, đóng `P2-BCC-MAJ-01`) — nơi Position
đã tách bạch tường minh là derived/non-authoritative. Sửa: Goal nay nói "xem lại CHÍNH XÁC
historical ReplayState(C) tại cursor đó — gồm authoritative recorded fact VÀ derived projection
theo authority class của từng constituent" — khớp nhất quán với chi tiết đã có. Đã rà soát toàn bộ
`PR-018`/`UC-004`/`SCR-002` cho các equivalent khác — KHÔNG tìm thấy wording nào khác phân loại
TOÀN BỘ `ReplayState(C)` là authoritative (Main flow/Evidence consumed/Observable outcome của
UC-004 đã tách bạch từ v0.9, KHÔNG cần sửa thêm). KHÔNG đổi Main flow bước 2/3, Evidence
consumed, no-look-ahead, full lineage-through-Position, UC-004 identity/Trigger/Preconditions/
Alternate-failure/PR traceability/Domain vocabulary/Out-of-scope. `PR-018`/`PR-019` KHÔNG chạm
(product-requirement.md v0.5 giữ nguyên — PR-018 đã tách bạch đúng từ v0.5, KHÔNG cần sửa).
Trạng thái: **CANDIDATE, pending governed review** — `P2-BCC-MAJ01-A-MAJ-01` CLOSED bởi candidate
correction này, NHƯNG `P2-BCC-MAJ-01` (Phase-wide BCC finding) VẪN OPEN cho tới khi bounded Review
A re-review CLEAN + Independent Review B CLEAN + Product Owner consolidation/revalidation +
prototype Batch 02 correction + affected prototype re-review + full-scope BCC rerun.

**v0.11 — CANDIDATE bounded semantic correction (2026-08-14), đóng `P2-BCC-MAJ01-A2-MAJ-01`
(Review A finding trên P2-BCC-MAJ-01 authority correction candidate v0.10) — KHÔNG Approved/
Consolidated, pending bounded Review A re-review/Independent Review B/Product Owner decision:**
`UC-004` Observable outcome viết lại — trước đây "Người dùng thấy chính xác state đã ghi nhận tại
cursor đã chọn ..." vẫn ngụ ý TOÀN BỘ `ReplayState(C)` (kể cả Position) là một "state đã ghi
nhận," mâu thuẫn `position.md` §1 (Position derived, deterministic, non-authoritative, KHÔNG
recorded fact/event stream riêng) dù chính câu đó đã nối thêm mệnh đề phân tách authoritative
fact lineage khỏi Position projection. Sửa: Observable outcome nay nói "Người dùng thấy chính xác
historical ReplayState(C) được tái dựng tại cursor đã chọn — authoritative fact lineage VÀ
Position projection tương ứng, với authority class tách biệt rõ" — ngôn ngữ historical
reconstruction trung lập, KHÔNG ngụ ý toàn bộ ReplayState/Position đã được ghi nhận/authoritative.
KHÔNG đổi Goal/Trigger/Preconditions/Inputs/Main flow/Alternate-failure/Evidence consumed/Evidence
produced/PR traceability/Domain vocabulary/Out-of-scope boundary của UC-004. `PR-018`/`PR-019`
(product-requirement.md, KHÔNG chạm)/`SCR-002` (ux-blueprint.md, KHÔNG chạm) KHÔNG đổi. Trạng
thái: **CANDIDATE, pending governed review** — `P2-BCC-MAJ01-A2-MAJ-01` CLOSED bởi candidate
correction này, NHƯNG `P2-BCC-MAJ-01` (Phase-wide BCC finding) VẪN OPEN cho tới khi governed
review/consolidation/prototype correction/re-review/full-scope BCC rerun hoàn tất.

## 1. Purpose and authority boundary

Tài liệu này trả lời: **"Với 34 requirement đã `Consolidated Stable` tại Package 0.3-A, người dùng nội bộ THỰC SỰ tương tác với Ride như thế nào, theo trình tự nào, với hành vi quan sát được cụ thể ra sao?"** — ở mức **user journey/use-case behavior**, KHÔNG ở mức screen/UI (Package 0.3-C) hay implementation (Phase 1). Là input bắt buộc cho Package 0.3-C (`ux-blueprint.md`) — Package 0.3-C PHẢI truy vết ngược mọi screen/flow về đúng một hoặc nhiều `UC-XXX` ID tại đây, KHÔNG được tự phát minh use case mới ở tầng UX.

## 2. Actors and approved operating context

```text
Primary actor:        "Ride user" — thành viên nội bộ của một team vận hành nhiều Strategy trên vốn
                       của chính team đó (product-requirement.md §3). Vai trò định hướng thiết kế sản
                       phẩm (Retail Trader/Professional Trader/Quant Researcher/Strategy Developer,
                       Vision §1.5) KHÔNG tạo hành vi workflow khác biệt ở walking-skeleton này — một
                       actor DUY NHẤT được dùng xuyên suốt tài liệu (PR-001–PR-003).

Operating context (kế thừa nguyên vẹn product-requirement.md §6, KHÔNG đổi):
  internal trading workspace     (ADR-007 — KHÔNG multi-tenant)
  single workspace                (một Account vận hành thực tế, Account first-class — PR-002)
  crypto-only                     (ADR-007 — KHÔNG đa tài sản)
  2–3 exchanges                   (ADR-007, PR-003)

Không actor hệ thống/nội bộ nào khác (ví dụ "Risk Gateway", "Execution Engine") được đối xử như actor
use-case — chúng là authoritative pipeline boundary đã đóng tại Domain Contract, CHỈ xuất hiện trong
Main flow như bước hệ thống hiển thị (system-visible behavior), KHÔNG phải actor khởi xướng use case.
```

## 3. Workflow-wide invariants

Chín invariant dưới đây restate nguyên vẹn `PR-XXX` đã `Consolidated Stable` — KHÔNG tạo yêu cầu mới, áp dụng xuyên suốt MỌI Use Case tại §6:

```text
WF-INV-1  Một Ride user session luôn scoped theo ĐÚNG MỘT Account hiện tại của workspace.       (PR-002)
WF-INV-2  Instrument/Venue thao tác luôn nằm trong tập TradableListing đã đăng ký.                (PR-003)
WF-INV-3  Một phiên Research/Replay/Backtest luôn dùng ĐÚNG MỘT Strategy Instance, cố định
          trong suốt phiên đó.                                                          (PR-001, PR-016)
WF-INV-4  Mọi Decision/Risk Action hiển thị PHẢI tái dựng được từ evidence bất biến, một
          causation trace duy nhất.                                                            (PR-009)
WF-INV-5  So sánh Decision semantic giữa Replay/Backtest/Paper luôn dùng `canonical
          semantic-decision hash` — KHÔNG BAO GIỜ dùng lại thuật ngữ "Decision hash" chung
          chung.                                                                               (PR-010)
WF-INV-6  Không output nào (Decision/RiskEvaluation/ExecutionResult/Fill/Position) từng hiển
          thị bị sửa/xóa ngầm — mọi correction là fact mới, append-only.                        (PR-011)
WF-INV-7  Trạng thái hiển thị tại một historical cursor luôn deterministic, không phụ thuộc
          network sau khi chuẩn bị.                                                            (PR-012)
WF-INV-8  Mọi giá trị tài chính hiển thị PHẢI lossless, khớp byte-for-byte giá trị đã ghi
          nhận.                                                                                (PR-013)
WF-INV-9  Mọi lifecycle state hiển thị PHẢI phản ánh transition đã khai báo tường minh trong
          Domain Contract sở hữu entity đó.                                                    (PR-014)
WF-INV-10 Live là lifecycle boundary bị hoãn (`OQ-002`) — KHÔNG use case nào tại đây kết
          thúc bằng một hành động Live authoritative.                                (PR-027, Preserve scope)
```

## 4. Primary end-to-end journey

Hành trình chính (walking skeleton, KHÔNG bao trùm mọi persona/edge case — đúng kỷ luật đã pin tại `product-requirement.md`):

```text
Ride user (§2):
  1. Research     — chọn Instrument/Venue (PR-003), quan sát market-analysis state (PR-015), chọn/
                     cấu hình Strategy Instance (PR-001/PR-016) — KHÔNG side-effect (PR-017).
  2. Replay        — chọn canonical Replay Cursor, xem lại chính xác state lịch sử đã ghi nhận
                     (PR-008/PR-018), tuỳ chọn parity recomputation (PR-019/PR-020).
  3. Backtest      — chạy Decision logic của Strategy Instance qua một khoảng lịch sử bounded
                     (PR-021), xem Decision/RiskEvaluation trace, simulated economic evidence/
                     exposure progression (PR-033), và strategy-level evaluable result so sánh
                     được cross-run/cross-version (PR-022/PR-034).
  4. Paper         — khởi tạo (initiate) PAPER execution dựa trên một PAPER-context authoritative
                     Decision lineage RIÊNG BIỆT (KHÔNG phải Decision từ Backtest/Research), đi qua
                     chuỗi C7 đầy đủ, nhận ExecutionResult/Fill/Position (PR-007/PR-024–PR-027).
  5. Review        — truy vết causation trace Decision→Position (PR-028), so sánh reconstructed
                     vs recorded state (PR-029), xác nhận không recompute lịch sử (PR-030).
  6. Improve       — tạo Strategy Definition Version mới (PR-031), so sánh outcome cũ/mới, giữ
                     nguyên truy cập evidence version cũ (PR-032) — VÒNG LẶP trở lại Research với
                     Strategy Instance mới.
```

Live KHÔNG phải một bước trong hành trình này — chỉ được nhắc như lifecycle boundary bị hoãn (§10, `OQ-002`).

## 5. Use Case catalogue

| UC-ID | Title | Stage | Primary PR(s) |
|---|---|---|---|
| UC-001 | Inspect market-analysis state | Research | PR-003, PR-015, PR-017 |
| UC-002 | Select/configure Strategy Instance | Research | PR-001, PR-016 |
| UC-003 | Confirm Research session produced no side-effect | Research | PR-017 |
| UC-004 | Choose canonical Replay Cursor and reconstruct historical state | Replay | PR-008, PR-018, PR-020 |
| UC-005 | Run optional parity recomputation and view match/mismatch/indeterminate finding | Replay | PR-010, PR-019 |
| UC-006 | Start a bounded Backtest run bound to Strategy/version/configuration | Backtest | PR-021, PR-022, PR-023 |
| UC-007 | Inspect Decision/RiskEvaluation trace for a Backtest run | Backtest | PR-021, PR-009, PR-004, PR-005 |
| UC-008 | Inspect simulated economic evidence and exposure/position progression | Backtest | PR-033 |
| UC-009 | Inspect strategy-level evaluable result for a Backtest run | Backtest | PR-034 |
| UC-010 | Compare Backtest runs or Strategy Definition Versions | Backtest | PR-034 |
| UC-011 | Initiate PAPER execution through the approved pipeline | Paper | PR-007, PR-024, PR-004, PR-005 |
| UC-012 | Inspect ExecutionResult for a submitted Order | Paper | PR-007, PR-024 |
| UC-013 | Inspect Fill simulation evidence | Paper | PR-025 |
| UC-014 | Inspect Position or NON_EVALUABLE outcome | Paper | PR-026 |
| UC-015 | Confirm no real exchange order was placed | Paper | PR-027 |
| UC-016 | Trace Decision → Position lineage | Review | PR-028, PR-004, PR-005 |
| UC-017 | Compare reconstructed and recorded historical state | Review | PR-029 |
| UC-018 | Inspect a correction without repainting history | Review | PR-011, PR-030 |
| UC-019 | Create a new Strategy Definition Version | Improve | PR-031 |
| UC-020 | Compare historical outcomes across Strategy Definition Versions | Improve | PR-031, PR-032 |
| UC-021 | Preserve access to old-version evidence | Improve | PR-032 |

21 Use Case, `UC-001`–`UC-021`, bao trùm đầy đủ danh sách minimum coverage bắt buộc cho cả sáu giai đoạn.

## 6. Detailed Use Cases

### 9.1-equivalent — Research

**UC-001 — Inspect market-analysis state**
```text
Primary actor:         Ride user (§2).
Goal:                   Xem trạng thái phân tích thị trường (Candle/Swing/Structure/Regime/Feature/
                        Market Context) tại một thời điểm/khoảng thời gian, KHÔNG tạo side-effect.
Trigger:                Người dùng bắt đầu một phiên Research cho một Instrument/Venue.
Preconditions:          Instrument/Venue nằm trong tập TradableListing đã đăng ký (PR-003).
Inputs:                 Instrument/Venue đã chọn; thời điểm hoặc khoảng thời gian quan tâm.
Main flow:              1. Người dùng chọn Instrument/Venue hợp lệ (WF-INV-2).
                        2. Người dùng chọn thời điểm/khoảng thời gian quan tâm.
                        3. Hệ thống hiển thị Candle/Swing/Structure/Regime/Feature/Market Context tại
                           thời điểm đó, đọc trực tiếp từ authoritative event stream tương ứng —
                           KHÔNG tạo fact mới.
Alternate/failure:      Instrument/Venue không hợp lệ → §8 "invalid Instrument/Venue selection".
                        Không có dữ liệu lịch sử tại thời điểm chọn → §8 "missing historical evidence".
Observable outcome:     Người dùng thấy đầy đủ market-analysis state tại thời điểm đã chọn.
Evidence consumed:      Candle/Swing/Structure/Regime/Feature/Market Context authoritative fact stream.
Evidence produced:      KHÔNG — quan sát thuần túy (đóng PR-015/PR-017).
PR traceability:        PR-003, PR-015, PR-017.
Domain vocabulary used: candle.md, swing.md, structure.md, regime.md, feature.md, context.md,
                        instrument.md, venue.md.
Out-of-scope boundary:  KHÔNG hiển thị chi tiết chart/UI component (Package 0.3-C); KHÔNG tính toán
                        chỉ báo mới ngoài Feature type đã đăng ký (feature.md).
```

**UC-002 — Select/configure Strategy Instance**
```text
Primary actor:         Ride user (§2).
Goal:                   Chọn ĐÚNG MỘT Strategy Instance (gắn một Strategy Definition Version) làm cơ
                        sở cho toàn bộ phiên Research/Replay/Backtest tiếp theo.
Trigger:                Người dùng chuẩn bị chuyển từ quan sát thuần túy (UC-001) sang cam kết một
                        phiên Replay/Backtest.
Preconditions:          Tồn tại ít nhất một Strategy Instance đã đăng ký (strategy.md).
Inputs:                 Strategy Instance được chọn từ danh sách đã đăng ký.
Main flow:              1. Người dùng chọn một Strategy Instance.
                        2. Hệ thống pin Strategy Instance đó là cố định cho phiên (WF-INV-3) — KHÔNG
                           cho phép đổi giữa chừng một phiên Replay/Backtest đang chạy.
Alternate/failure:      Không có Strategy Instance nào tồn tại/được chọn → §8 "missing Strategy
                        Instance".
Observable outcome:     Phiên làm việc có ĐÚNG MỘT Strategy Instance pin cố định.
Evidence consumed:      Strategy Instance/Strategy Definition Version đã đăng ký.
Evidence produced:      KHÔNG authoritative fact mới — lựa chọn Strategy Instance tự nó KHÔNG phải
                        Decision Pipeline fact.
PR traceability:        PR-001, PR-016.
Domain vocabulary used: strategy.md.
Out-of-scope boundary:  KHÔNG tạo Strategy Definition Version mới tại đây (đó là UC-019, Improve).
```

**UC-003 — Confirm Research session produced no side-effect**
```text
Primary actor:         Ride user (§2).
Goal:                   Xác nhận (verify), với một kết quả quan sát được tường minh, một phiên Research
                        đã kết thúc mà KHÔNG tạo bất kỳ authoritative Decision Pipeline fact nào bị cấm.
Trigger:                Người dùng kết thúc phiên Research (hoặc chuyển sang Replay/Backtest).
Preconditions:          Một phiên Research (UC-001/UC-002) đã diễn ra.
Inputs:                 Khoảng thời gian của phiên Research vừa kết thúc.
Main flow:              1. Hệ thống kiểm tra event log của Decision/RiskEvaluation/Execution Intent/
                           Order/ExecutionResult stream trong khoảng thời gian phiên Research.
                        2. Hệ thống trả về ĐÚNG MỘT trong ba kết quả verification, quan sát được
                           (workflow-visible), KHÔNG phải một domain entity/event mới:
                             PASSED        — không prohibited fact nào (Decision/RiskEvaluation/
                                             Execution Intent/Order/ExecutionResult) được quan sát.
                             FAILED        — một hoặc nhiều prohibited authoritative fact được quan
                                             sát trong khoảng thời gian phiên.
                             INDETERMINATE — evidence cần thiết (event log đầy đủ cho khoảng thời
                                             gian đó) không resolve được trọn vẹn.
Alternate/failure:      NẾU FAILED hoặc INDETERMINATE: workflow KHÔNG được coi là đã verify thành
                        công (KHÔNG tiến hành như thể Research sạch); status vẫn quan sát được; reason
                        + fact/evidence bị ảnh hưởng được disclosed tường minh; KHÔNG downstream
                        authoritative action nào xảy ra. KHÔNG định nghĩa incident handling/rollback/
                        correction automation/architecture cho trường hợp FAILED — đó là governance
                        concern ngoài phạm vi tài liệu này.
Observable outcome:     Người dùng thấy kết quả verification (PASSED/FAILED/INDETERMINATE) cho phiên
                        Research, kèm reason khi khác PASSED.
Evidence consumed:      Event log của Decision/RiskEvaluation/Execution Intent/Order/ExecutionResult
                        stream trong khoảng thời gian phiên.
Evidence produced:      KHÔNG authoritative fact — kết quả verification là workflow-visible result
                        DUY NHẤT, KHÔNG tạo một entity/event "ResearchVerification" hay tương đương.
PR traceability:        PR-017.
Domain vocabulary used: decision.md.
Out-of-scope boundary:  KHÔNG định nghĩa cơ chế audit/log kỹ thuật cụ thể (Phase 1); KHÔNG tạo domain
                        entity/event mới cho kết quả verification; KHÔNG định nghĩa incident/rollback
                        automation.
```

### 9.2-equivalent — Replay

**UC-004 — Choose canonical Replay Cursor and reconstruct historical state**
```text
Primary actor:         Ride user (§2).
Goal:                   Chọn một canonical Replay Cursor và xem lại CHÍNH XÁC historical
                        ReplayState(C) tại cursor đó (historical reconstruction — mặc định) — gồm
                        authoritative recorded fact VÀ derived projection theo authority class của
                        từng constituent (v0.10, đóng `P2-BCC-MAJ01-A-MAJ-01`).
Trigger:                Người dùng, với Strategy Instance đã pin (UC-002), chọn chuyển sang Replay.
Preconditions:          Strategy Instance đã chọn (WF-INV-3); Instrument/Venue hợp lệ (WF-INV-2).
Inputs:                 Một canonical Replay Cursor (thời điểm lịch sử).
Main flow:              1. Người dùng chọn một Replay Cursor.
                        2. Hệ thống resolve và hiển thị ReplayState(C) TẠI cursor đó, gồm HAI thành
                           phần tách bạch authority (v0.9, đóng `P2-BCC-MAJ-01`): (a) lineage
                           authoritative recorded fact Decision→Trade Intent→RiskEvaluation→
                           Execution Intent→Order→ExecutionResult→Fill — CHỈ fact có recorded_time ≤ C
                           (no-look-ahead); VÀ (b) Position — MỘT derived, deterministic,
                           non-authoritative projection (position.md §1/§2), KHÔNG PHẢI một fact có
                           recorded_time riêng, KHÔNG có event stream riêng — reconstruct TRỌN VẸN
                           TẠI CÙNG cursor C từ tập Fill eligible tại C (`eligible_as_position_
                           contributing_fill`, fill.md §6).
                        3. Hệ thống KHÔNG tạo Decision hay bất kỳ authoritative fact nào trong bước
                           này (Replay authority boundary, product-requirement.md §9.2) — Position
                           projection reconstruction CŨNG KHÔNG tạo fact/event mới nào (position.md
                           §1: "KHÔNG có event stream riêng").
Alternate/failure:      Cursor tham chiếu artifact không materialize được → §8 "Replay cursor with
                        unavailable references".
Observable outcome:     Người dùng thấy chính xác historical ReplayState(C) được tái dựng tại cursor
                        đã chọn (v0.11, đóng `P2-BCC-MAJ01-A2-MAJ-01`) — authoritative fact lineage
                        VÀ Position projection tương ứng, với authority class tách biệt rõ.
Evidence consumed:      Authoritative event stream Decision→Trade Intent→RiskEvaluation→Execution
                        Intent→Order→ExecutionResult→Fill (v0.9, đóng `P2-BCC-MAJ-01` — Position KHÔNG
                        còn liệt kê trong "event stream," xem bước 2(b)); Position derived projection
                        (position.md §2, reconstruct tại CÙNG cursor C, non-authoritative); canonical
                        Replay Cursor (Chapter 8 §8.5).
Evidence produced:      KHÔNG authoritative fact mới — historical reconstruction thuần túy.
PR traceability:        PR-008, PR-018, PR-020.
Domain vocabulary used: replay-event.md, decision.md, trade-intent.md, risk.md, execution-intent.md,
                        order.md, execution-result.md, fill.md, position.md.
Out-of-scope boundary:  KHÔNG chạy lại simulation/computation nào (đó là parity recomputation, UC-005,
                        và luôn tuỳ chọn/tách biệt).
```

**UC-005 — Run optional parity recomputation and view match/mismatch/indeterminate finding**
```text
Primary actor:         Ride user (§2).
Goal:                   Tuỳ chọn kiểm chứng lại (parity recomputation) rằng Decision logic tái tính
                        toán khớp Decision đã ghi nhận tại cursor đang xem (UC-004) — deterministic,
                        non-authoritative.
Trigger:                Người dùng, đang xem historical reconstruction (UC-004), chọn kích hoạt parity
                        recomputation.
Preconditions:          UC-004 đã hoàn tất — một ReplayState(C) đang hiển thị.
Inputs:                 Yêu cầu kích hoạt parity recomputation từ người dùng (tuỳ chọn, KHÔNG mặc
                        định).
Main flow:              1. Người dùng kích hoạt parity recomputation.
                        2. Hệ thống tái tính toán Decision logic (semantic verification, non-
                           authoritative) dưới ĐÚNG CÙNG chín pinned axis đã establish tại recorded
                           Decision (decision.md §9a.4 — v0.8: bao gồm implementation identity
                           `decision_implementation_version` khi recorded Decision đã establish, và
                           digest-definition version khi dùng digest) và so sánh qua Canonical
                           Decision Semantic Representation, structured comparison (decision.md §9a,
                           CANDIDATE — v0.5).
                        3. Hệ thống hiển thị kết quả MATCH, MISMATCH, hoặc INDETERMINATE — KHÔNG BAO
                           GIỜ tự động ghi đè, thay thế, hay tạo Decision mới từ kết quả này (Replay
                           authority boundary).
Alternate/failure:      (a) Kết quả mismatch → §8 "parity mismatch" (hiển thị finding, KHÔNG hành động
                        authoritative nào tự động xảy ra). (b) Recorded-side hoặc recomputed-side
                        evidence thiếu/stale/invalidated/ambiguous/non-evaluable → hệ thống hiển thị
                        INDETERMINATE (decision.md §9a.6), KHÔNG ép buộc match hay mismatch giả tạo —
                        KHÔNG hành động authoritative nào tự động xảy ra. (c) **(CANDIDATE — v0.8,
                        đóng `P16-V003-A-MAJ-01`)** Recorded Decision đã establish implementation
                        identity (`decision_implementation_version`) NHƯNG một trong hai phía không
                        resolve/reproduce được đúng identity đó, HOẶC digest-definition (khi dùng
                        digest) unresolved/incompatible giữa hai phía → hệ thống hiển thị
                        INDETERMINATE, KHÔNG tự động MATCH chỉ vì Representation khớp.
Observable outcome:     Người dùng thấy MATCH, MISMATCH, hoặc INDETERMINATE, KHÔNG có Decision mới/thay
                        thế nào xuất hiện.
Evidence consumed:      Decision đã ghi nhận tại cursor, canonical semantic-decision hash definition
                        (decision.md §9a).
Evidence produced:      Kết quả so sánh (non-authoritative, KHÔNG phải một fact được ghi vào event
                        log Decision Pipeline).
PR traceability:        PR-010, PR-019.
Domain vocabulary used: decision.md, replay-event.md.
Out-of-scope boundary:  KHÔNG tạo `ReplayDecision` hay bất kỳ domain fact mới nào; KHÔNG định nghĩa cơ
                        chế lưu trữ kết quả recomputation (Phase 1).
```

### 9.3-equivalent — Backtest

**UC-006 — Start a bounded Backtest run bound to Strategy/version/configuration**
```text
Primary actor:         Ride user (§2).
Goal:                   Khởi động một Backtest run qua một khoảng lịch sử bounded (start/end), dưới
                        MỘT stable run identity/context, gắn Strategy Instance/Definition Version/
                        configuration tường minh.
Trigger:                Người dùng, với Strategy Instance đã pin (UC-002), chọn chuyển sang Backtest.
Preconditions:          Strategy Instance đã chọn (WF-INV-3); khoảng thời gian lịch sử có dữ liệu.
Inputs:                 Khoảng thời gian bounded (start/end).
Main flow:              1. Người dùng nhập khoảng thời gian bounded.
                        2. Hệ thống gán một stable Backtest run identity/context duy nhất, gắn CHÍNH
                           XÁC Strategy Instance/Strategy Definition Version/policy version đang dùng.
                        3. Hệ thống chạy Decision logic (CÙNG pipeline với Replay/Paper — WF-INV
                           parity) qua khoảng thời gian đó — KHÔNG tạo Order/ExecutionResult PAPER
                           hay Live.
                        4. Hệ thống xác nhận: KHÔNG route mạng tới bất kỳ exchange endpoint thật nào
                           trong suốt run.
Alternate/failure:      Không đủ dữ liệu lịch sử cho khoảng đã chọn → §8 "missing historical evidence".
Observable outcome:     Một Backtest run identity tồn tại, gắn đúng khoảng thời gian + version tuple.
Evidence consumed:      Strategy Instance/Definition Version, market-analysis state lịch sử.
Evidence produced:      Decision/RiskEvaluation sequence gắn run identity (KHÔNG Order/ExecutionResult
                        PAPER/Live — Backtest authority boundary).
PR traceability:        PR-021, PR-022, PR-023.
Domain vocabulary used: decision.md, risk.md, strategy.md.
Out-of-scope boundary:  KHÔNG author entity/event "BacktestOrder"/"BacktestExecutionResult" hay tương
                        đương; KHÔNG định nghĩa simulation algorithm (product-required nhưng domain-
                        representation deferred, §9).
```

**UC-007 — Inspect Decision/RiskEvaluation trace for a Backtest run**
```text
Primary actor:         Ride user (§2).
Goal:                   Xem toàn bộ chuỗi Decision (VÀ downstream RiskEvaluation liên quan, khi có)
                        sinh ra bởi một Backtest run (UC-006) — với MỖI Decision hiển thị đầy đủ
                        outcome, upstream explainability evidence đã dùng để TẠO RA nó, VÀ downstream
                        lineage do nó sinh ra khi tồn tại — hai loại tách biệt tường minh, KHÔNG gộp.
Trigger:                Người dùng chọn xem chi tiết một Backtest run đã/đang chạy.
Preconditions:          Một Backtest run identity tồn tại (UC-006).
Inputs:                 Backtest run identity.
Main flow:              1. Người dùng chọn một Backtest run.
                        2. Hệ thống hiển thị chuỗi Decision đầy đủ của run đó. Với MỖI Decision, hệ
                           thống hiển thị tường minh, tách bạch BA nhóm:
                             A. Decision outcome — đúng một trong LONG/SHORT/NO_ACTION (decision.md
                                §5e/§5b `result` enum; NO_ACTION = không có exposure mới).
                             B. Decision origin VÀ upstream explainability — evidence đã dùng để TẠO
                                RA Decision đó: Strategy Instance CHÍNH XÁC đã tạo ra Decision; Strategy
                                Definition Version/configuration context đã dùng (UC-006); recorded
                                input snapshot/reference; recorded Decision evaluation/configuration
                                evidence (rule evaluation input theo `result` — decision.md §5e) — tất
                                cả resolve TRỰC TIẾP từ recorded fact, KHÔNG suy diễn/tính lại sau sự
                                kiện.
                             C. Downstream lineage liên quan, KHI TỒN TẠI — Trade Intent (khi result
                                LONG/SHORT, decision.md §9), RiskEvaluation đánh giá Trade Intent đó
                                (risk.md), Execution Intent (khi RiskEvaluation APPROVED), và related
                                downstream fact khác nếu có — hiển thị NHƯ MỘT NHÓM TÁCH BIỆT khỏi B.
                           Downstream fact tại C là fact được **causally derived from hoặc related to**
                           Decision đó — CHÚNG KHÔNG PHẢI evidence đã dùng để tạo ra Decision.
                           RiskEvaluation đặc biệt: nó luôn thuộc nhóm C (downstream), KHÔNG BAO GIỜ
                           thuộc nhóm B — RiskEvaluation đánh giá Trade Intent SINH RA SAU Decision
                           (risk.md §1: RiskEvaluation là bản ghi một lần Risk Gateway đánh giá MỘT
                           Trade Intent, KHÔNG phải input đầu vào của chính Decision).
Alternate/failure:      Backtest run identity không resolve được, hoặc run evidence hiện không khả
                        dụng → workflow dừng; state (run identity, nếu đã biết) vẫn quan sát được;
                        reason được disclosed; KHÔNG downstream authoritative action nào xảy ra (§8
                        "Backtest run identity does not resolve" — bốn nguyên tắc fallback, KHÔNG
                        ngụ ý một run state machine/deletion event/archival lifecycle nào).
Observable outcome:     Người dùng thấy trình tự Decision đầy đủ của run — MỖI Decision kèm ba nhóm
                        tách biệt: (A) outcome tường minh LONG/SHORT/NO_ACTION; (B) upstream explain-
                        ability — Strategy Instance/Definition Version nguồn gốc VÀ recorded input
                        snapshot/evaluation evidence đã dùng để TẠO RA Decision đó; (C) downstream
                        lineage khi tồn tại — Trade Intent/RiskEvaluation/Execution Intent/related fact
                        do Decision đó SINH RA. (C) KHÔNG được trình bày như thể là evidence của (B) —
                        downstream fact causally derived from/related to Decision, KHÔNG phải evidence
                        dùng để tạo ra nó.
Evidence consumed:      Decision fact gắn run identity; recorded input snapshot/evaluation evidence của
                        mỗi Decision (nhóm B — upstream); Strategy Instance/Definition Version context
                        (UC-006); downstream Trade Intent/RiskEvaluation/Execution Intent fact khi tồn
                        tại (nhóm C — downstream lineage, hiển thị tách biệt, KHÔNG phải input của
                        Decision).
Evidence produced:      KHÔNG — quan sát thuần túy, KHÔNG suy diễn/tính lại evidence sau sự kiện.
PR traceability:        PR-021, PR-009, PR-004, PR-005 (v0.5 → v0.6, đóng `P03B-V05-B-MAJ-01` — sửa
                        causal-direction error: v0.5 liệt kê "RiskEvaluation liên quan" như một phần
                        evidence dùng để TẠO RA Decision (nhóm (c) cũ) — SAI, vì RiskEvaluation đánh
                        giá Trade Intent SINH RA SAU Decision (risk.md §1), KHÔNG phải input của chính
                        Decision. Nay Main flow bước 2 tách bạch tường minh nhóm B (upstream Decision
                        explainability — Strategy Instance/Definition Version/configuration, recorded
                        input snapshot, recorded evaluation evidence) khỏi nhóm C (downstream lineage —
                        Trade Intent/RiskEvaluation/Execution Intent/related fact), với phát biểu tường
                        minh downstream fact "causally derived from/related to" Decision, KHÔNG phải
                        evidence tạo ra nó. PR-004 qua outcome LONG/SHORT/NO_ACTION + Strategy Instance
                        nguồn gốc tường minh (nhóm A+B); PR-005 qua recorded input snapshot/evaluation
                        evidence tại nhóm B, resolve trực tiếp từ recorded fact, KHÔNG suy diễn — KHÔNG
                        còn conflate với downstream RiskEvaluation. Backtest vẫn non-PAPER simulated —
                        KHÔNG gọi material này là authoritative PAPER Order/ExecutionResult/Fill/
                        Position, KHÔNG entity Backtest mới, domain representation vẫn deferred (§9d)).
Domain vocabulary used: decision.md, risk.md.
Out-of-scope boundary:  KHÔNG hiển thị chi tiết UI/chart (Package 0.3-C); KHÔNG entity/event Backtest
                        mới (`BacktestOrder`/`BacktestExecutionResult` hay tương đương); KHÔNG gọi
                        Backtest material này authoritative PAPER Order/ExecutionResult/Fill/Position.
```

**UC-008 — Inspect simulated economic evidence and exposure/position progression**
```text
Primary actor:         Ride user (§2).
Goal:                   Xem deterministic simulated economic evidence gắn mỗi Decision dẫn tới
                        simulated exposure change, VÀ exposure/position progression theo thời gian
                        xuyên suốt khoảng interval của run — TÁCH BIỆT hoàn toàn khỏi PAPER/Live
                        authority.
Trigger:                Người dùng, đang xem một Backtest run (UC-007), chọn xem economic evidence.
Preconditions:          Backtest run identity tồn tại, có ít nhất một Decision dẫn tới simulated
                        exposure change.
Inputs:                 Backtest run identity.
Main flow:              1. Hệ thống hiển thị simulated economic evidence deterministic cho mỗi điểm
                           Decision→simulated exposure change.
                        2. Hệ thống hiển thị exposure/position progression theo thời gian trong suốt
                           khoảng interval.
                        3. Hệ thống xác nhận (hoặc cho phép audit) rằng KHÔNG PAPER Order/
                           ExecutionResult/Fill/Position nào được tạo/tái sử dụng bởi run này
                           (Backtest authority boundary).
Alternate/failure:      Run không có Decision nào dẫn tới simulated exposure change (ví dụ toàn bộ
                        Decision đều không có exposure mới) → §8 "Backtest run with insufficient
                        evaluable evidence".
Observable outcome:     Người dùng thấy economic evidence + exposure progression, KHÔNG lẫn với PAPER
                        fact.
Evidence consumed:      Decision/RiskEvaluation sequence của run (UC-007).
Evidence produced:      Simulated economic evidence + exposure/position progression — **product-
                        required, domain-representation deferred** (KHÔNG có Domain Contract Backtest
                        chính thức, §9).
PR traceability:        PR-033.
Domain vocabulary used: decision.md, risk.md (nguồn evidence); execution-result.md/fill.md/position.md
                        (tham chiếu CHỈ để định nghĩa ranh giới KHÔNG được tái sử dụng).
Out-of-scope boundary:  KHÔNG định nghĩa simulation algorithm, fee/slippage model, accounting/PnL
                        formula; KHÔNG tạo "BacktestFill"/"BacktestPosition" hay tương đương.
```

**UC-009 — Inspect strategy-level evaluable result for a Backtest run**
```text
Primary actor:         Ride user (§2).
Goal:                   Xem một strategy-level evaluable result cho một Backtest run đã hoàn tất, dẫn
                        xuất từ Decision/RiskEvaluation + exposure progression (UC-007/UC-008), gắn
                        CHÍNH XÁC version tuple đã dùng.
Trigger:                Người dùng, sau khi Backtest run hoàn tất, chọn xem kết quả tổng hợp.
Preconditions:          Backtest run đã hoàn tất, có economic evidence/exposure progression (UC-008).
Inputs:                 Backtest run identity đã hoàn tất.
Main flow:              1. Hệ thống dẫn xuất một strategy-level evaluable result từ toàn bộ run.
                        2. Hệ thống hiển thị kết quả đó gắn CHÍNH XÁC Strategy Instance/Definition
                           Version/configuration context đã dùng (UC-006) — KHÔNG threshold/target cụ
                           thể nào được định nghĩa/hiển thị như KPI chính thức (`OQ-003`).
Alternate/failure:      Run chưa hoàn tất, hoặc thiếu evidence evaluable (UC-008 alternate) → §8
                        "Backtest run with insufficient evaluable evidence".
Observable outcome:     Người dùng thấy một kết quả evaluable, gắn đúng run/version context.
Evidence consumed:      Economic evidence + exposure progression (UC-008), version tuple (UC-006).
Evidence produced:      Strategy-level evaluable result — product-required, domain-representation
                        deferred (§9).
PR traceability:        PR-034, PR-022.
Domain vocabulary used: strategy.md; decision.md/risk.md (nguồn evidence).
Out-of-scope boundary:  KHÔNG định nghĩa concrete KPI threshold/target (`OQ-003`); KHÔNG performance
                        attribution formula.
```

**UC-010 — Compare Backtest runs or Strategy Definition Versions**
```text
Primary actor:         Ride user (§2).
Goal:                   So sánh strategy-level evaluable result (UC-009) của hai Backtest run — khác
                        khoảng interval, hoặc khác Strategy Definition Version.
Trigger:                Người dùng chọn từ hai Backtest run trở lên để so sánh.
Preconditions:          Cả hai run đều đã hoàn tất, mỗi run có một strategy-level evaluable result
                        (UC-009).
Inputs:                 Hai (hoặc nhiều) Backtest run identity.
Main flow:              1. Người dùng chọn các run cần so sánh.
                        2. Hệ thống hiển thị kết quả evaluable của từng run cạnh nhau, gắn đúng run/
                           version context của từng run — KHÔNG gộp/aggregate thành một con số duy
                           nhất.
Alternate/failure:      Một trong các run được chọn thiếu evaluable result (UC-009 alternate) → §8
                        "Backtest run with insufficient evaluable evidence" cho run đó, các run khác
                        vẫn hiển thị.
Observable outcome:     Người dùng so sánh được kết quả nhiều run cạnh nhau mà không cần công cụ
                        ngoài hệ thống.
Evidence consumed:      Strategy-level evaluable result của từng run (UC-009).
Evidence produced:      KHÔNG — so sánh thuần túy hiển thị, KHÔNG tạo fact mới.
PR traceability:        PR-034.
Domain vocabulary used: strategy.md.
Out-of-scope boundary:  KHÔNG định nghĩa công thức so sánh/scoring tổng hợp qua nhiều run (aggregation
                        formula ngoài phạm vi, `OQ-003`).
```

### 9.4-equivalent — Paper

**UC-011 — Initiate PAPER execution through the approved pipeline**
```text
Primary actor:         Ride user (§2).
Goal:                   Khởi tạo (initiate/request) PAPER execution — người dùng cung cấp INTENT tiến
                        hành, KHÔNG một Order payload authoritative — dựa trên một PAPER-context
                        authoritative Decision lineage RIÊNG BIỆT, đi qua TRỌN VẸN chuỗi C7 do hệ
                        thống sở hữu: Decision (PAPER-context) → Trade Intent → RiskEvaluation →
                        Execution Intent → Order → OrderSubmissionRequest →
                        ExecutionResultComputation → PaperExecutionObservation → ExecutionResult →
                        Fill → Position, environment PAPER.
Trigger:                Người dùng yêu cầu khởi tạo PAPER execution — evidence từ Research/Replay/
                        Backtest CHỈ INFORM phán đoán của người dùng (KHÔNG phải hard precondition hệ
                        thống, xem §7 Backtest → Paper handoff).
Preconditions:          Một PAPER-context authoritative Decision lineage (LONG/SHORT) ELIGIBLE tồn tại
                        cho Strategy Instance đang dùng; Account/Instrument/Venue hợp lệ (WF-INV-1/
                        WF-INV-2). TRƯỚC khi khởi tạo, người dùng PHẢI thấy tường minh: outcome
                        LONG/SHORT của Decision đó; Strategy Instance CHÍNH XÁC đang dùng; Strategy
                        Definition Version/configuration context gắn Strategy Instance đó; VÀ recorded
                        input snapshot/evidence reference đã dùng để tạo ra Decision đó — tất cả
                        resolve TRỰC TIẾP từ recorded fact, KHÔNG suy diễn/tính lại sau sự kiện. Decision
                        này TUYỆT ĐỐI KHÔNG phải Decision phát sinh từ Backtest (UC-006–UC-010) hay
                        Research (UC-001–UC-003) được carry-forward/promote/reuse — nó là một
                        authoritative Decision fact RIÊNG BIỆT trong PAPER context. Cơ chế CHÍNH XÁC
                        thiết lập PAPER-context Decision này (điều gì trigger nó, ai/cái gì ghi nhận nó)
                        là một **deferred domain/workflow dependency** (§9d) — KHÔNG được định nghĩa
                        tại đây.
Inputs:                 Yêu cầu/intent khởi tạo PAPER execution từ người dùng — KHÔNG quantity/order
                        type/sizing do người dùng cung cấp (những field đó, nếu cần, thuộc execution
                        semantics hệ thống sở hữu, ngoài phạm vi tài liệu này).
Main flow:              1. Người dùng yêu cầu khởi tạo PAPER execution.
                        2. Hệ thống resolve PAPER-context authoritative Decision lineage eligible cho
                           Strategy Instance đang dùng — NẾU không tồn tại, workflow dừng TRƯỚC PAPER
                           execution (xem Alternate/failure). NẾU eligible: hệ thống hiển thị tường
                           minh **upstream Decision evidence** — outcome LONG/SHORT của Decision đó,
                           Strategy Instance/Definition Version nguồn gốc, VÀ recorded input snapshot/
                           evidence reference đã dùng để tạo ra Decision đó — TÁCH BIỆT tường minh khỏi
                           **downstream causation** (bước 3–9 dưới đây, fact do CHÍNH hành động khởi
                           tạo PAPER execution sinh ra).
                        3. PAPER-context Decision (LONG/SHORT) phát sinh Trade Intent (hệ thống sở
                           hữu).
                        4. Trade Intent đi qua Risk Gateway → RiskEvaluation (APPROVED/REJECTED/
                           NON_EVALUABLE).
                        5. Nếu APPROVED: RiskEvaluation phát sinh Execution Intent (hệ thống sở hữu).
                        6. Execution Intent phát sinh Order (system-owned authoritative internal
                           instruction), rồi OrderSubmissionRequest (system-owned authoritative
                           request tới PAPER boundary).
                        7. Hệ thống authorize ExecutionResultComputation, chạy bounded PAPER
                           simulation, ghi nhận PaperExecutionObservation.
                        8. Hệ thống ghi nhận ExecutionResult (EXECUTED hoặc NOT_EXECUTED),
                           environment PAPER.
                        9. Nếu EXECUTED: đúng một Fill được tạo, rồi Position được cập nhật (derive
                           từ eligible Fill lineage).
Alternate/failure:      KHÔNG có PAPER-context Decision lineage eligible → workflow dừng TRƯỚC PAPER
                        execution; state (Strategy Instance đang dùng) vẫn quan sát được; reason "no
                        eligible PAPER-context Decision lineage" disclosed; KHÔNG Trade Intent/
                        RiskEvaluation/Execution Intent/Order nào được tạo (§8). RiskEvaluation
                        REJECTED/NON_EVALUABLE → §8, dừng chuỗi tại đó, KHÔNG Execution Intent/Order
                        nào được tạo. ExecutionResult NOT_EXECUTED → §8, zero Fill.
Observable outcome:     Người dùng thấy HAI loại evidence tách biệt tường minh: (1) **upstream Decision
                        evidence** — outcome LONG/SHORT, Strategy Instance/Definition Version nguồn
                        gốc, recorded input snapshot/evidence reference đã dùng để tạo ra Decision —
                        hiển thị TRƯỚC khi khởi tạo (bước 2); (2) **downstream causation** — toàn bộ
                        chuỗi C7 tiến triển tới đúng một ExecutionResult (EXECUTED hoặc NOT_EXECUTED),
                        fact SINH RA BỞI hành động khởi tạo (bước 3–9). HOẶC người dùng thấy workflow
                        dừng trước PAPER execution vì thiếu PAPER-context Decision eligible. Downstream
                        causation KHÔNG tự nó ngụ ý đã thỏa evidence trace của Decision (loại 1) — hai
                        loại PHẢI hiển thị tách biệt, KHÔNG gộp.
Evidence consumed:      PAPER-context authoritative Decision lineage (RIÊNG BIỆT, KHÔNG phải Backtest/
                        Research Decision) — bao gồm recorded input snapshot/evidence reference đã dùng
                        để tạo ra Decision đó; Account/Instrument/Venue context. Backtest/Research
                        evidence (nếu người dùng đã xem) CHỈ inform judgment của người dùng — KHÔNG
                        phải input authoritative cho chuỗi hệ thống này.
Evidence produced:      Trade Intent, RiskEvaluation, Execution Intent (nếu APPROVED), Order
                        (system-owned), OrderSubmissionRequest (system-owned), ExecutionResultComputation,
                        PaperExecutionObservation, ExecutionResult, Fill (nếu EXECUTED).
PR traceability:        PR-007, PR-024, PR-004, PR-005 (v0.4 → v0.5, đóng `P03B-V04-A-MAJ-01` —
                        Preconditions/Main flow bước 2 nay operationalize đầy đủ CẢ HAI PR TRƯỚC khi
                        khởi tạo: PR-004 qua outcome LONG/SHORT + Strategy Instance/Definition Version
                        nguồn gốc tường minh; PR-005 qua recorded input snapshot/evidence reference đã
                        dùng tạo Decision, TÁCH BIỆT tường minh khỏi downstream C7 causation — downstream
                        chain KHÔNG còn được ngụ ý là tự thỏa PR-005 cho upstream Decision evidence.
                        Preserve nguyên vẹn: PAPER-context Decision identity riêng biệt, KHÔNG clone/
                        carry-forward/promote/reuse, user chỉ cung cấp initiation intent KHÔNG
                        authoritative Order payload, workflow dừng TRƯỚC PAPER execution khi thiếu
                        eligible lineage).
Domain vocabulary used: decision.md, trade-intent.md, risk.md, execution-intent.md, order.md,
                        execution-result.md, fill.md, position.md.
Out-of-scope boundary:  KHÔNG định nghĩa order type/sizing UI do người dùng cung cấp; KHÔNG author
                        Live routing (deferred, `OQ-002`); KHÔNG định nghĩa cơ chế chính xác thiết lập
                        PAPER-context Decision (deferred domain/workflow dependency, §9d); KHÔNG clone/
                        copy/recreate Decision fact từ Backtest/Research dưới bất kỳ hình thức nào.
```

**UC-012 — Inspect ExecutionResult for a submitted Order**
```text
Primary actor:         Ride user (§2).
Goal:                   Xem ExecutionResult (EXECUTED/NOT_EXECUTED) của một Order đã submit (UC-011),
                        environment PAPER.
Trigger:                Người dùng chọn xem chi tiết một Order đã submit.
Preconditions:          Order đã đi qua UC-011, có ExecutionResult visible-valid.
Inputs:                 Order identity.
Main flow:              1. Người dùng chọn Order.
                        2. Hệ thống hiển thị ExecutionResult (EXECUTED hoặc NOT_EXECUTED), environment
                           PAPER, gắn đúng OrderSubmissionRequest/computation gốc.
Alternate/failure:      NOT_EXECUTED → §8, người dùng thấy rõ zero Fill kèm theo.
Observable outcome:     Người dùng xác định chính xác kết quả execution của Order.
Evidence consumed:      ExecutionResult authoritative fact (execution-result.md §8).
Evidence produced:      KHÔNG.
PR traceability:        PR-007, PR-024.
Domain vocabulary used: order.md, execution-result.md.
Out-of-scope boundary:  KHÔNG hiển thị chi tiết computation/observation nội bộ ngoài những gì PR-007
                        yêu cầu.
```

**UC-013 — Inspect Fill simulation evidence**
```text
Primary actor:         Ride user (§2).
Goal:                   Xem simulation evidence (policy/configuration/build/deterministic-input ref)
                        VÀ economics (quantity/price) của một Fill, khớp CHÍNH XÁC
                        PaperExecutionObservation đã ghi nhận.
Trigger:                Người dùng chọn xem chi tiết một Fill (từ ExecutionResult EXECUTED, UC-012).
Preconditions:          ExecutionResult EXECUTED tồn tại, có đúng một Fill.
Inputs:                 Fill identity (qua execution_result_id).
Main flow:              1. Người dùng chọn Fill.
                        2. Hệ thống hiển thị fill_quantity/fill_price/price_currency VÀ bốn trục
                           simulation evidence (policy/configuration/build/deterministic-input ref),
                           khớp byte-for-byte PaperExecutionObservation gốc (WF-INV-8).
Alternate/failure:      Fill không tồn tại (ExecutionResult NOT_EXECUTED) → §8 "Fill absent".
Observable outcome:     Người dùng xác nhận economics của Fill khớp chính xác evidence đã ghi nhận,
                        KHÔNG có giá trị tính lại độc lập.
Evidence consumed:      Fill + PaperExecutionObservation (fill.md §1/§3, execution-result.md §1).
Evidence produced:      KHÔNG.
PR traceability:        PR-025.
Domain vocabulary used: fill.md, execution-result.md.
Out-of-scope boundary:  KHÔNG định nghĩa simulation algorithm/fee/slippage (execution-result.md đã
                        đóng phạm vi này — KHÔNG mở rộng).
```

**UC-014 — Inspect Position or NON_EVALUABLE outcome**
```text
Primary actor:         Ride user (§2).
Goal:                   Xem Position hiện tại cho một Account/Instrument; khi nhiều Fill lineage xung
                        đột, thấy disclosure tường minh NON_EVALUABLE thay vì một con số tuỳ chọn.
Trigger:                Người dùng chọn xem Position cho một Account/Instrument.
Preconditions:          Ít nhất một Fill tồn tại cho Account/Instrument đó (hoặc zero — FLAT).
Inputs:                 Account/Instrument selection.
Main flow:              1. Hệ thống derive Position từ eligible Fill lineage (position.md §2).
                        2. NẾU 0 eligible Fill: hiển thị FLAT. NẾU 1 eligible Fill: hiển thị LONG/
                           SHORT + net_quantity/average_entry_price. NẾU > 1 eligible Fill xung đột:
                           hiển thị `NON_EVALUABLE` + `contributing_fill_refs` đầy đủ — KHÔNG chọn một
                           Fill/aggregate/report FLAT sai.
Alternate/failure:      NON_EVALUABLE → §8 "Position NON_EVALUABLE".
Observable outcome:     Người dùng thấy đúng trạng thái Position, kể cả khi không thể xác định.
Evidence consumed:      eligible_as_position_contributing_fill (fill.md §6), Position projection
                        (position.md §2).
Evidence produced:      KHÔNG — Position là derived projection, KHÔNG authoritative fact riêng.
PR traceability:        PR-026.
Domain vocabulary used: position.md, fill.md.
Out-of-scope boundary:  KHÔNG định nghĩa weighted-average/netting formula cho nhiều Fill (position.md
                        đã đóng — KHÔNG mở rộng, `OQ-003`-adjacent nhưng ngoài phạm vi).
```

**UC-015 — Confirm no real exchange order was placed**
```text
Primary actor:         Ride user (§2).
Goal:                   Xác nhận Paper Trading KHÔNG tạo ra bất kỳ lệnh thật nào trên sàn giao dịch
                        bên ngoài.
Trigger:                Người dùng, sau UC-011, kiểm tra tính an toàn của phiên Paper Trading.
Preconditions:          Một phiên Paper Trading (UC-011) đã diễn ra.
Inputs:                 Khoảng thời gian của phiên Paper Trading.
Main flow:              1. Hệ thống hiển thị xác nhận: environment của mọi Order/ExecutionResult
                           trong phiên là PAPER; không route mạng nào đi tới exchange endpoint thật.
Alternate/failure:      Người dùng cố gắng chuyển sang Live → §8 "attempt to use Live behavior".
Observable outcome:     Người dùng có bằng chứng tường minh Paper Trading không đặt lệnh thật.
Evidence consumed:      environment field trên Order/ExecutionResult (order.md, execution-result.md).
Evidence produced:      KHÔNG.
PR traceability:        PR-027.
Domain vocabulary used: order.md, execution-result.md.
Out-of-scope boundary:  KHÔNG định nghĩa cơ chế audit network kỹ thuật cụ thể (Phase 1).
```

### 9.5-equivalent — Review

**UC-016 — Trace Decision → Position lineage**
```text
Primary actor:         Ride user (§2).
Goal:                   Với một Position contribution bất kỳ, truy vết ngược toàn bộ causation trace
                        về Decision gốc đã sinh ra nó — khi đạt tới Decision gốc, hiển thị đầy đủ
                        outcome, Strategy Instance/Definition Version nguồn gốc, VÀ recorded input
                        snapshot/evidence đã dùng để tạo ra Decision đó.
Trigger:                Người dùng chọn một Fill/Position contribution để review.
Preconditions:          Fill/Position contribution tồn tại (UC-013/UC-014).
Inputs:                 Fill/Position identity.
Main flow:              1. Người dùng chọn một Fill đóng góp Position.
                        2. Hệ thống hiển thị **downstream lineage** (causation trace ngược): Fill→
                           ExecutionResult→Order→Execution Intent→RiskEvaluation→Trade Intent→Decision
                           gốc — KHÔNG mắt xích thiếu.
                        3. Khi đạt tới Decision gốc, hệ thống hiển thị tường minh **Decision
                           explainability evidence** (input snapshot/configuration → Decision) — TÁCH
                           BIỆT khỏi downstream lineage tại bước 2: outcome (LONG/SHORT/không có
                           exposure mới); Strategy Instance CHÍNH XÁC đã tạo ra Decision đó VÀ Strategy
                           Definition Version/configuration context đã dùng; recorded input snapshot/
                           evidence reference đã dùng để tạo ra Decision đó — resolve TRỰC TIẾP từ
                           recorded fact, KHÔNG suy diễn/tính lại sau sự kiện, KHÔNG fact mới nào được
                           tạo.
Alternate/failure:      Mắt xích thiếu (KHÔNG dự kiến theo Domain Contract đã Consolidated Stable) →
                        ngoài phạm vi tài liệu này (governance/data-integrity concern).
Observable outcome:     Người dùng truy vết được trọn vẹn từ Position ngược về Decision gốc — thấy rõ
                        hai chiều tách biệt: **downstream lineage** (Decision → Position, bước 2) VÀ
                        **Decision explainability evidence** (input snapshot/configuration → Decision,
                        bước 3) — outcome, Strategy Instance/Definition Version nguồn gốc, và evidence
                        đã dùng tạo Decision đều hiển thị tường minh tại đầu trace ngược, KHÔNG suy
                        diễn/tính lại.
Evidence consumed:      Toàn bộ causation_refs/correlation_id chain Decision→...→Position; recorded
                        input snapshot/evidence reference của chính Decision gốc; Strategy Instance/
                        Definition Version context gắn Decision đó.
Evidence produced:      KHÔNG — quan sát thuần túy, KHÔNG suy diễn/tính lại evidence.
PR traceability:        PR-028, PR-004, PR-005 (v0.4 → v0.5, đóng `P03B-V04-A-MAJ-01` — Main flow nay
                        tách bạch tường minh downstream lineage [Position → Decision, bước 2, PR-028]
                        khỏi Decision explainability evidence [outcome + Strategy Instance/Definition
                        Version nguồn gốc + recorded input snapshot, bước 3 MỚI, đóng PR-004/PR-005] —
                        bước 3 KHÔNG suy diễn/tính lại, resolve trực tiếp từ recorded fact, KHÔNG fact
                        mới).
Domain vocabulary used: decision.md, trade-intent.md, risk.md, execution-intent.md, order.md,
                        execution-result.md, fill.md, position.md.
Out-of-scope boundary:  KHÔNG hiển thị chi tiết UI trace visualization (Package 0.3-C).
```

**UC-017 — Compare reconstructed and recorded historical state**
```text
Primary actor:         Ride user (§2).
Goal:                   So sánh state tái dựng qua Replay (UC-004) tại một cursor lịch sử với state đã
                        hiển thị tại đúng thời điểm đó khi ghi nhận ban đầu, xác nhận không silent
                        drift.
Trigger:                Người dùng, đang Review, chọn so sánh một cursor lịch sử.
Preconditions:          UC-004 đã chạy cho cursor đó.
Inputs:                 Replay Cursor cần so sánh.
Main flow:              1. Hệ thống resolve ReplayState(C) hiện tại (UC-004).
                        2. Hệ thống so sánh với state đã từng hiển thị/ghi nhận tại đúng cursor đó.
                        3. NẾU không có correction nào xảy ra giữa hai thời điểm → hiển thị "No
                           conflict". NẾU có correction → hiển thị khác biệt tường minh kèm fact
                           correction liên quan (KHÔNG ẩn/repaint).
Alternate/failure:      Correction visible SAU historical cursor đang xem → §8 "correction visible
                        after historical cursor".
Observable outcome:     Người dùng xác nhận không có silent drift, hoặc thấy rõ correction nào đã áp
                        dụng.
Evidence consumed:      ReplayState(C) (UC-004), correction/invalidation fact liên quan nếu có.
Evidence produced:      Kết quả so sánh — non-authoritative, KHÔNG phải fact mới.
PR traceability:        PR-029.
Domain vocabulary used: replay-event.md.
Out-of-scope boundary:  KHÔNG định nghĩa cơ chế lưu snapshot lịch sử cụ thể (Phase 1).
```

**UC-018 — Inspect a correction without repainting history**
```text
Primary actor:         Ride user (§2).
Goal:                   Xem một correction (fact mới thay thế fact cũ) mà KHÔNG bất kỳ giá trị lịch sử
                        nào bị sửa/xóa ngầm (No Repaint).
Trigger:                Người dùng phát hiện hoặc được thông báo một correction tồn tại (từ UC-017 hoặc
                        trực tiếp).
Preconditions:          Một correction fact (`*FactInvalidated` + replacement) tồn tại cho một Decision/
                        RiskEvaluation/ExecutionResult/Fill/Position liên quan.
Inputs:                 Fact identity cần kiểm tra correction.
Main flow:              1. Người dùng chọn một fact.
                        2. Hệ thống hiển thị fact gốc (vẫn resolvable, append-only) VÀ fact replacement
                           (nếu có), với liên kết tường minh (supersedes_fact_ref) — KHÔNG hiển thị chỉ
                           một giá trị "đã sửa" ẩn danh nguồn gốc.
Alternate/failure:      KHÔNG áp dụng — hiển thị luôn cả hai trạng thái (trước/sau correction) là hành
                        vi bắt buộc, không có nhánh lỗi.
Observable outcome:     Người dùng thấy rõ ràng: giá trị nào là gốc, giá trị nào là correction, và tại
                        sao (invalidation reference).
Evidence consumed:      Fact gốc + `*FactInvalidated` + fact replacement (nếu có).
Evidence produced:      KHÔNG — quan sát thuần túy.
PR traceability:        PR-011, PR-030.
Domain vocabulary used: decision.md, risk.md, execution-result.md, fill.md (correction lineage pattern
                        đồng nhất xuyên suốt).
Out-of-scope boundary:  KHÔNG định nghĩa UI diff visualization (Package 0.3-C).
```

### 9.6-equivalent — Improve

**UC-019 — Create a new Strategy Definition Version**
```text
Primary actor:         Ride user (§2).
Goal:                   Tạo một Strategy Definition Version mới, tách biệt hoàn toàn khỏi version cũ.
Trigger:                Người dùng, sau Review (UC-016–UC-018), quyết định cải thiện Strategy.
Preconditions:          Một Strategy Definition (identity) đã tồn tại (strategy.md).
Inputs:                 Nội dung Strategy Definition Version mới.
Main flow:              1. Người dùng tạo một Strategy Definition Version mới.
                        2. Hệ thống gán version identity mới, tách biệt version cũ (append-only,
                           strategy.md).
                        3. Một Strategy Instance mới có thể gắn version mới này (quay lại UC-002).
Alternate/failure:      KHÔNG áp dụng tại tầng product — mọi validation nội dung cụ thể thuộc phạm vi
                        strategy.md (không sửa tại đây).
Observable outcome:     Một Strategy Definition Version mới tồn tại, độc lập version cũ.
Evidence consumed:      Strategy Definition (identity) hiện có.
Evidence produced:      Strategy Definition Version mới (strategy.md).
PR traceability:        PR-031.
Domain vocabulary used: strategy.md, ADR-013.
Out-of-scope boundary:  KHÔNG định nghĩa nội dung/schema Strategy Definition cụ thể (thuộc
                        strategy.md, không sửa).
```

**UC-020 — Compare historical outcomes across Strategy Definition Versions**
```text
Primary actor:         Ride user (§2).
Goal:                   So sánh outcome giữa Strategy Instance gắn version cũ (KỂ CẢ version không còn
                        active, PR-032) và Strategy Instance gắn version mới (UC-019) — CÙNG mode
                        (Backtest-vs-Backtest, hoặc PAPER-vs-PAPER) HOẶC cross-mode side-by-side — mọi
                        so sánh giữ nguyên tách bạch identity/authority giữa hai họ evidence.
Trigger:                Người dùng, sau khi tạo version mới (UC-019), muốn so sánh với version cũ —
                        BAO GỒM version đã ngừng active (PR-032).
Preconditions:          Có ít nhất hai Strategy Instance, gắn hai Strategy Definition Version khác
                        nhau, mỗi cái có evidence trong Backtest (§9.3, UC-007–UC-009) VÀ/HOẶC Paper
                        (§9.4, UC-011–UC-014) — BAO GỒM Strategy Instance gắn version không còn active
                        (evidence resolve theo UC-021).
Inputs:                 Hai (hoặc nhiều) Strategy Instance identity; lựa chọn mode so sánh (same-mode
                        Backtest, same-mode PAPER, hoặc cross-mode side-by-side).
Main flow:              1. Người dùng chọn các Strategy Instance cần so sánh VÀ mode so sánh.
                        2. NẾU same-mode Backtest: hệ thống hiển thị Decision/RiskEvaluation trace +
                           simulated economic evidence + exposure/position progression + strategy-
                           level evaluable result (UC-007–UC-009) của từng Instance, non-PAPER
                           authority, tách biệt hoàn toàn.
                        3. NẾU same-mode PAPER: hệ thống hiển thị authoritative Decision/RiskEvaluation/
                           Order/ExecutionResult/Fill/Position evidence (UC-011–UC-014) của từng
                           Instance, tách biệt hoàn toàn.
                        4. NẾU cross-mode: hệ thống hiển thị CẢ HAI họ evidence cạnh nhau — MỖI bên gắn
                           nhãn tường minh: mode (Backtest/PAPER), authority (non-PAPER simulated /
                           authoritative PAPER), và evidence type — KHÔNG tạo một unified execution-
                           outcome fact, KHÔNG tự động normalize, KHÔNG công thức scoring chung giữa
                           hai họ.
                        5. Với Strategy Instance gắn version KHÔNG còn active: hệ thống resolve evidence
                           lịch sử của nó theo TỪNG mode/họ ĐỘC LẬP qua UC-021 (Backtest và/hoặc PAPER,
                           KHÔNG gộp) — danh tính version LUÔN hiển thị, mỗi họ evidence hiển thị khi
                           resolve được, đánh dấu "incomplete" nếu một phần thiếu (PR-032). UC-021
                           KHÔNG trả về một cross-mode evidence object chung cho UC-020 tiêu thụ.
Alternate/failure:      Một Strategy Instance chưa có outcome nào (chưa Backtest/Paper) → hiển thị rỗng
                        cho Instance đó, KHÔNG lỗi cho toàn bộ so sánh. Evidence của version cũ không
                        resolve được (một họ/loại evidence cụ thể) → áp dụng UC-021 Alternate/failure
                        cho ĐÚNG phần đó — KHÔNG toàn bộ so sánh, KHÔNG toàn bộ version đó.
Observable outcome:     Người dùng so sánh được outcome giữa các version — CÙNG mode HOẶC cross-mode
                        với nhãn mode/authority/evidence-type rõ ràng — KHÔNG BAO GIỜ thấy một "unified
                        execution outcome" gộp Backtest và PAPER làm một.
Evidence consumed:      Decision/RiskEvaluation/simulated economic evidence/exposure progression/
                        strategy-level result (Backtest, non-PAPER authority, UC-007–UC-009) VÀ/HOẶC
                        authoritative Decision/RiskEvaluation/Order/ExecutionResult/Fill/Position
                        (PAPER, UC-011–UC-014) của từng Strategy Instance — BAO GỒM evidence của
                        version không còn active, resolve theo TỪNG họ độc lập qua UC-021 (PR-032) —
                        UC-021 KHÔNG trả về một cross-mode evidence object chung.
Evidence produced:      KHÔNG — so sánh hiển thị thuần túy, KHÔNG tạo fact mới, KHÔNG tạo unified
                        outcome entity.
PR traceability:        PR-031, PR-032.
Domain vocabulary used: strategy.md, decision.md, risk.md (họ evidence Backtest, non-PAPER authority);
                        execution-result.md, fill.md, position.md (họ evidence PAPER, authoritative) —
                        HAI HỌ TÁCH BIỆT, KHÔNG gộp.
Out-of-scope boundary:  KHÔNG gọi Backtest material là `ExecutionResult`/`Fill`/`Position`/execution
                        outcome authoritative dưới bất kỳ hình thức nào; KHÔNG định nghĩa một unified
                        Backtest/PAPER outcome entity/schema; KHÔNG công thức so sánh/scoring/
                        normalization tổng hợp cross-mode (`OQ-003`); KHÔNG yêu cầu Package 0.3-C phát
                        minh một unified outcome model; KHÔNG ngụ ý UC-021 trả về một cross-mode
                        evidence object chung cho hai họ evidence (đóng `P03B-DELTA-MIN-01`).
```

**UC-021 — Preserve access to old-version evidence**
```text
Primary actor:         Ride user (§2).
Goal:                   Với một Strategy Definition Version không còn active: (a) danh tính version
                        LUÔN hiển thị, kể cả khi một phần evidence không khả dụng; (b) resolve, ĐỘC
                        LẬP theo TỪNG họ evidence áp dụng được (Backtest, non-PAPER authority / PAPER,
                        authoritative), evidence lịch sử KHI CÓ THỂ — KHÔNG fabricate, KHÔNG silently
                        omit, KHÔNG gộp hai họ thành một representation chung (mirror tách bạch đã pin
                        tại UC-020, đóng `P03B-DELTA-MIN-01`).
Trigger:                Người dùng, sau khi chuyển sang version mới (UC-019) hoặc từ một so sánh
                        (UC-020), cần xem lại evidence lịch sử của version cũ — cho một hoặc cả hai
                        mode (Backtest và/hoặc PAPER).
Preconditions:          Strategy Definition Version cũ đã từng chạy trong Backtest (§9.3, UC-006–
                        UC-010) VÀ/HOẶC Paper (§9.4, UC-011–UC-015) — CÓ THỂ chỉ một trong hai mode,
                        hoặc cả hai.
Inputs:                 Strategy Definition Version cũ (identity); lựa chọn mode cần resolve (Backtest,
                        PAPER, hoặc cả hai — mirror lựa chọn mode tại UC-020).
Main flow:              1. Người dùng chọn một Strategy Definition Version cũ — danh tính version đó
                           LUÔN hiển thị, kể cả khi không còn active VÀ kể cả khi một phần evidence bên
                           dưới không khả dụng.
                        2. NẾU Backtest evidence được yêu cầu: hệ thống resolve, ĐỘC LẬP, họ evidence
                           Backtest gắn version đó — Decision/RiskEvaluation trace, simulated economic
                           evidence, exposure/position progression, strategy-level evaluable result,
                           run identity/version/configuration context (UC-007–UC-009) — non-PAPER
                           authority. KHÔNG gọi material này là authoritative `ExecutionResult`/`Fill`/
                           `Position`/PAPER execution outcome dưới bất kỳ hình thức nào.
                        3. NẾU PAPER evidence được yêu cầu: hệ thống resolve, ĐỘC LẬP, authoritative
                           lineage PAPER gắn version đó — Decision, Trade Intent, RiskEvaluation,
                           Execution Intent, Order, OrderSubmissionRequest, ExecutionResult, Fill,
                           Position (UC-011–UC-014), CÓ THỂ bao gồm ExecutionResultComputation/
                           PaperExecutionObservation làm supporting evidence khi cần (KHÔNG redefine
                           semantics của chúng) — Fill economics từ PaperExecutionObservation, Position
                           từ eligible Fill lineage, `NON_EVALUABLE` vẫn quan sát được khi áp dụng.
                        4. NẾU cả hai họ được yêu cầu: hiển thị TÁCH BIỆT hoàn toàn — KHÔNG merge
                           thành một representation/entity chung, giữ nguyên identity/authority riêng
                           của từng họ (đúng nguyên tắc UC-020).
Alternate/failure:      NẾU MỘT PHẦN evidence được yêu cầu (một họ, hoặc một loại evidence trong một
                        họ) KHÔNG khả dụng/KHÔNG resolve được:
                          workflow dừng CHO ĐÚNG phần evidence request bị ảnh hưởng (KHÔNG toàn bộ)
                          danh tính Strategy Definition Version VẪN hiển thị
                          mode (Backtest/PAPER) VẪN hiển thị
                          authority (non-PAPER simulated/authoritative PAPER) VẪN hiển thị
                          evidence khả dụng khác (nếu có) VẪN hiển thị NHƯNG đánh dấu "incomplete"
                          họ/loại evidence bị thiếu được identify rõ (cái gì thiếu, thuộc họ nào)
                          reason được disclosed
                          KHÔNG evidence nào bị fabricate
                          KHÔNG phần thiếu nào bị ẩn/silently omit
                          KHÔNG kết luận (kể cả một phần) được trình bày như đã hoàn chỉnh
                          KHÔNG downstream authoritative action nào xảy ra
                        TUYỆT ĐỐI KHÔNG ngụ ý TOÀN BỘ lịch sử Strategy không khả dụng chỉ vì MỘT họ/
                        loại evidence thiếu.
Observable outcome:     Người dùng thấy danh tính version LUÔN hiển thị; evidence family/type nào
                        resolve được hiển thị đầy đủ, tách biệt theo mode/authority; evidence family/
                        type nào không resolve được thì bị đánh dấu rõ kèm lý do — KHÔNG BAO GIỜ một
                        kết luận fabricated/ẩn thiếu sót, KHÔNG BAO GIỜ suy diễn "toàn bộ lịch sử mất"
                        từ một phần thiếu.
Evidence consumed:      Backtest evidence family (Decision/RiskEvaluation trace, simulated economic
                        evidence, exposure/position progression, strategy-level evaluable result, run
                        identity/version/configuration context — non-PAPER authority, khi áp dụng);
                        PAPER evidence family (Decision, Trade Intent, RiskEvaluation, Execution
                        Intent, Order, OrderSubmissionRequest, ExecutionResult, Fill, Position —
                        authoritative, khi áp dụng, kèm ExecutionResultComputation/
                        PaperExecutionObservation làm supporting evidence khi cần).
Evidence produced:      KHÔNG — resolve/quan sát thuần túy, KHÔNG tạo fact mới, KHÔNG tạo một unified
                        old-version evidence entity/aggregate gộp hai họ.
PR traceability:        PR-032.
Domain vocabulary used: strategy.md, decision.md, risk.md (họ evidence Backtest — evidence-source
                        vocabulary only, non-PAPER, khi áp dụng); trade-intent.md, execution-intent.md,
                        order.md, execution-result.md, fill.md, position.md (họ evidence PAPER —
                        authoritative, khi áp dụng) — HAI HỌ TÁCH BIỆT, KHÔNG gộp.
Out-of-scope boundary:  KHÔNG định nghĩa retention duration, archive tiering, retrieval latency,
                        restoration process, storage architecture, hay evidence availability SLA cụ
                        thể (Phase 1); KHÔNG tạo một unified old-version evidence aggregate/entity gộp
                        hai họ; KHÔNG gọi Backtest material là `ExecutionResult`/`Fill`/`Position`/
                        PAPER execution outcome; KHÔNG redefine semantics của `ExecutionResultComputation`/
                        `PaperExecutionObservation`; KHÔNG tạo entity/event Backtest mới.
```

## 7. Cross-stage handoffs

```text
Research → Replay
  Exit condition (Research):   Strategy Instance đã chọn (UC-002); Instrument/Venue hợp lệ; KHÔNG
                                side-effect fact nào được tạo (UC-003).
  Evidence carried forward:    Strategy Instance identity, Instrument/Venue selection.
  Entry condition (Replay):    Strategy Instance PHẢI GIỮ NGUYÊN trong suốt phiên Replay (WF-INV-3).
  PR traceability:             PR-001, PR-016.

Replay → Backtest
  Exit condition (Replay):     Người dùng đã xem historical reconstruction (UC-004), tuỳ chọn parity
                                recomputation (UC-005).
  Evidence carried forward:    Strategy Instance identity (KHÔNG đổi); hiểu biết về historical state
                                đã xem.
  Entry condition (Backtest):  Strategy Instance GIỮ NGUYÊN (WF-INV-3); khoảng thời gian bounded được
                                chọn mới cho Backtest run.
  PR traceability:             PR-016, PR-021.
  Lưu ý:                       Replay và Backtest là hai capability ĐỘC LẬP — Replay KHÔNG phải hard
                                precondition kỹ thuật của Backtest; hai bước liên tiếp trong hành trình
                                walking-skeleton (§4) nhưng không có PR nào ép buộc thứ tự kỹ thuật.

Backtest → Paper (v0.2, đóng `P03B-MAJ-01`)
  Exit condition (Backtest):   Người dùng đã xem strategy-level evaluable result (UC-009), tuỳ chọn so
                                sánh cross-run/cross-version (UC-010).
  Backtest evidence:           INFORM phán đoán của người dùng DUY NHẤT — KHÔNG một input authoritative
                                cho bất kỳ fact PAPER nào.
  Backtest/Research Decision
  identity:                    TUYỆT ĐỐI KHÔNG được carry forward, KHÔNG được promote, KHÔNG được
                                reuse làm authoritative Decision ancestor của một PAPER Trade Intent —
                                dưới bất kỳ hình thức nào (KHÔNG clone/copy/recreate).
  PAPER entry:                 Đòi hỏi một PAPER-context authoritative Decision lineage RIÊNG BIỆT
                                (UC-011 Preconditions) — TÁCH BIỆT hoàn toàn khỏi Decision lineage của
                                Backtest/Research.
  Decision parity:             CÓ THỂ verify semantic equivalence (canonical semantic-decision hash,
                                WF-INV-5) giữa Decision Backtest và Decision PAPER NẾU cả hai tồn tại —
                                NHƯNG KHÔNG BAO GIỜ merge fact identity, KHÔNG merge authority, KHÔNG
                                convert Backtest fact thành PAPER fact.
  Evidence carried forward:    Nhận định của người dùng (non-authoritative); KHÔNG Backtest/Research
                                Decision fact identity nào được mang sang PAPER.
  Entry condition (Paper):     Người dùng TỰ QUYẾT ĐỊNH khởi tạo PAPER execution (UC-011) — judgment
                                gate của người dùng, phù hợp "Research Before Capital" (Vision §1.6),
                                KHÔNG phải hard precondition kỹ thuật được PR nào enforce. Workflow
                                DỪNG trước PAPER execution nếu không có PAPER-context Decision lineage
                                eligible (UC-011 Alternate/failure).
  Deferred dependency:         Cơ chế CHÍNH XÁC PAPER-context authoritative Decision lineage được thiết
                                lập là deferred domain/workflow dependency (§9d) — KHÔNG định nghĩa tại
                                đây.
  PR traceability:             PR-034 (evidence để inform quyết định); PR-024 (Paper tự thân độc lập,
                                đòi hỏi PAPER-context Decision riêng).

Paper → Review
  Exit condition (Paper):      ExecutionResult đã resolve (EXECUTED/NOT_EXECUTED); nếu EXECUTED, Fill/
                                Position đã derive (UC-011–UC-015).
  Evidence carried forward:    Toàn bộ causation chain Decision→...→Position.
  Entry condition (Review):    Evidence đầy đủ, không đứt đoạn, sẵn sàng cho causation trace (UC-016).
  PR traceability:             PR-007, PR-028.

Review → Improve
  Exit condition (Review):     Người dùng đã trace causation (UC-016), so sánh reconstructed/recorded
                                state (UC-017), inspect correction nếu có (UC-018).
  Evidence carried forward:    Nhận định về hiệu quả Strategy hiện tại (KHÔNG phải một fact hệ thống —
                                judgment của người dùng).
  Entry condition (Improve):   Người dùng quyết định tạo Strategy Definition Version mới (UC-019).
  PR traceability:             PR-031.

Improve → Research (vòng lặp)
  Exit condition (Improve):    Strategy Definition Version mới đã tạo (UC-019); danh tính Strategy
                                Definition Version cũ vẫn hiển thị, evidence lịch sử resolve được khi
                                có thể — KHÔNG guarantee tuyệt đối truy cập tức thời (UC-021, đóng
                                `P03B-MIN-02`).
  Evidence carried forward:    Strategy Definition Version mới — dùng để tạo Strategy Instance mới
                                (UC-002, vòng lặp).
  Entry condition (Research):  Giống hệt Research→Replay ở trên, với Strategy Instance MỚI.
  PR traceability:             PR-031, PR-032, PR-001.
```

## 8. Failure and non-evaluable paths

Với mọi scenario KHÔNG có controlling behavior tường minh trong `product-requirement.md`/Domain Contract, áp dụng ĐÚNG bốn nguyên tắc sau (KHÔNG tự phát minh resolution semantics):

```text
workflow stops
state remains observable
reason is disclosed
no downstream authoritative action occurs
```

| Scenario | Behavior | PR/Domain traceability |
|---|---|---|
| Missing Strategy Instance | Workflow dừng tại UC-002; state (không có Instance nào chọn) hiển thị rõ; reason "no Strategy Instance selected" disclosed; không Decision nào được tạo. | PR-001 (không controlling resolution cụ thể — fallback bốn nguyên tắc trên). |
| Invalid Instrument/Venue selection | Workflow dừng tại UC-001/UC-011; lựa chọn ngoài tập TradableListing bị từ chối TRƯỚC khi tạo bất kỳ fact nào; reason disclosed. | PR-003 (reject trước khi tạo fact — có controlling rule). |
| Missing historical evidence | Workflow dừng tại UC-001/UC-006; state hiển thị "no data at this point/interval"; reason disclosed; không fact nào được tạo. | PR-015, PR-021 (không controlling resolution cụ thể — fallback bốn nguyên tắc). |
| Replay cursor with unavailable references | Workflow dừng tại UC-004; cursor được chọn nhưng reconstruction không hoàn tất; reason disclosed (artifact không materialize); không Decision nào được tạo. | PR-020/I-5 (self-contained Replay — không controlling resolution cho reference thiếu — fallback). |
| Parity mismatch/indeterminate | Workflow KHÔNG dừng runtime — hiển thị finding MATCH/MISMATCH/INDETERMINATE (UC-005; INDETERMINATE CANDIDATE v0.7, decision.md §9a.6); mismatch/indeterminate KHÔNG tự động ghi đè/tạo Decision; cần Product Owner/reviewer xem xét ngoài phạm vi runtime tự động. | PR-010, PR-019 (có controlling rule — Replay authority boundary). |
| Backtest run insufficient evaluable evidence | Workflow dừng tại UC-008/UC-009; run identity vẫn tồn tại và observable; reason "no simulated exposure change produced" disclosed; không strategy-level result nào được hiển thị như evaluable. | PR-033, PR-034 (fallback bốn nguyên tắc — chưa có controlling resolution cụ thể). |
| RiskEvaluation REJECTED | Workflow dừng tại UC-011 bước 2; result + reason code hiển thị (risk.md); KHÔNG Execution Intent/Order nào được tạo. | PR-006 (có controlling rule). |
| RiskEvaluation NON_EVALUABLE | Giống REJECTED — workflow dừng, result + reason code hiển thị, KHÔNG Execution Intent/Order. | PR-006 (có controlling rule). |
| Order NOT_EXECUTED | ExecutionResult hiển thị NOT_EXECUTED; zero Fill hiển thị rõ; không downstream action. | PR-007, PR-024 (có controlling rule). |
| Fill absent | UC-013 hiển thị "no Fill for this ExecutionResult" (NOT_EXECUTED case); không economics nào được hiển thị/suy diễn. | PR-025 (có controlling rule, hệ quả của NOT_EXECUTED). |
| Position NON_EVALUABLE | UC-014 hiển thị `NON_EVALUABLE` + `contributing_fill_refs` đầy đủ — KHÔNG chọn một Fill/aggregate/report FLAT. | PR-026 (có controlling rule tường minh). |
| Correction visible after historical cursor | UC-017 hiển thị khác biệt tường minh kèm fact correction liên quan — KHÔNG ẩn/repaint giá trị gốc (UC-018). | PR-011, PR-029, PR-030 (có controlling rule). |
| Attempt to use Live behavior | Workflow dừng NGAY LẬP TỨC; state hiển thị "Live is Unauthorized, OQ-002 Open"; reason disclosed; KHÔNG downstream authoritative action, KHÔNG route mạng tới exchange thật. | PR-027, `OQ-002` (có controlling rule tường minh). |
| No eligible PAPER-context Decision lineage (v0.2, MỚI, đóng `P03B-MAJ-01`) | Workflow dừng TRƯỚC PAPER execution (UC-011 bước 2); state (Strategy Instance đang dùng) vẫn observable; reason "no eligible PAPER-context Decision lineage" disclosed; KHÔNG Trade Intent/RiskEvaluation/Execution Intent/Order nào được tạo; KHÔNG Backtest/Research Decision nào được clone/promote để lấp khoảng trống. | PR-024 (có controlling rule — Backtest→Paper handoff, §7). |
| Backtest run identity does not resolve (v0.2, MỚI, đóng `P03B-MIN-03`) | Workflow dừng tại UC-007; state (run identity, nếu đã biết) vẫn observable; reason disclosed; KHÔNG downstream authoritative action; KHÔNG ngụ ý run state machine/deletion event/archival lifecycle nào. | PR-021 (fallback bốn nguyên tắc — chưa có controlling resolution cụ thể). |
| Historical evidence for old Strategy Definition Version unavailable — một họ/loại evidence cụ thể (v0.3, cập nhật, đóng `P03B-MIN-02`/`P03B-DELTA-MIN-01`) | Workflow dừng CHO ĐÚNG phần evidence request bị ảnh hưởng tại UC-021/UC-020 (KHÔNG toàn bộ); danh tính Strategy Definition Version + mode + authority vẫn hiển thị; evidence khả dụng khác vẫn hiển thị nhưng đánh dấu incomplete; họ/loại evidence thiếu được identify rõ; reason disclosed; KHÔNG fabricate, KHÔNG silently omit, KHÔNG kết luận (kể cả một phần) trình bày như hoàn chỉnh; KHÔNG ngụ ý toàn bộ lịch sử Strategy không khả dụng. | PR-032 (có controlling rule — UC-021 Alternate/failure). |
| Research verification FAILED/INDETERMINATE (v0.2, MỚI, đóng `P03B-MIN-05`) | Workflow KHÔNG tiến hành như đã verify thành công (UC-003); status vẫn observable; reason + evidence bị ảnh hưởng disclosed; KHÔNG downstream authoritative action; KHÔNG entity/event "ResearchVerification" nào được tạo. | PR-017 (có controlling rule — UC-003 tri-state outcome). |

## 9. Evidence and traceability requirements

### 9a. Use Case → PR mapping

Xem bảng đầy đủ tại §5 (cột "Primary PR(s)") — mỗi Use Case tại §6 lặp lại chính xác mapping đó trong field "PR traceability".

### 9b. Workflow stage → PR mapping

```text
Research  → PR-001, PR-002, PR-003, PR-015, PR-016, PR-017
Replay    → PR-008, PR-009, PR-010, PR-012, PR-018, PR-019, PR-020
Backtest  → PR-021, PR-022, PR-023, PR-033, PR-034, PR-004, PR-005 (UC-007, mapping từ `F-03` v0.4,
             behavior operationalize đầy đủ tại `P03B-V04-A-MAJ-01` v0.5, causal-direction error sửa
             tại `P03B-V05-B-MAJ-01` v0.6 — RiskEvaluation nay đúng downstream, không còn upstream)
Paper     → PR-002, PR-003, PR-007, PR-013, PR-014, PR-024, PR-025, PR-026, PR-027, PR-004, PR-005
             (UC-011, mapping từ `F-03` v0.4, behavior operationalize đầy đủ tại `P03B-V04-A-MAJ-01`
             v0.5)
Review    → PR-009, PR-011, PR-028, PR-029, PR-030, PR-004, PR-005 (UC-016, mapping từ `F-03` v0.4,
             behavior operationalize đầy đủ tại `P03B-V04-A-MAJ-01` v0.5)
Improve   → PR-031, PR-032
```

### 9c. Use Case → Domain vocabulary mapping

```text
UC-001            candle.md, swing.md, structure.md, regime.md, feature.md, context.md, instrument.md,
                   venue.md
UC-002            strategy.md
UC-003            decision.md
UC-004            replay-event.md, decision.md, trade-intent.md, risk.md, execution-intent.md,
                   order.md, execution-result.md, fill.md, position.md
UC-005            decision.md, replay-event.md
UC-006–UC-010     decision.md, risk.md, strategy.md (Backtest evidence — domain-representation
                   deferred, §9d); execution-result.md/fill.md/position.md (boundary reference only)
UC-011–UC-015     decision.md, trade-intent.md, risk.md, execution-intent.md, order.md,
                   execution-result.md, fill.md, position.md
UC-016            decision.md, trade-intent.md, risk.md, execution-intent.md, order.md,
                   execution-result.md, fill.md, position.md
UC-017            replay-event.md
UC-018            decision.md, risk.md, execution-result.md, fill.md
UC-019            strategy.md, decision.md, ADR-013
UC-020 (v0.2)     strategy.md, decision.md, risk.md (họ evidence Backtest, non-PAPER authority);
                   execution-result.md, fill.md, position.md (họ evidence PAPER, authoritative) — hai
                   họ TÁCH BIỆT, KHÔNG gộp (đóng P03B-MAJ-02)
UC-021 (v0.3)     strategy.md, decision.md, risk.md (họ evidence Backtest — evidence-source vocabulary
                   only, non-PAPER, khi áp dụng); trade-intent.md, execution-intent.md, order.md,
                   execution-result.md, fill.md, position.md (họ evidence PAPER — authoritative, khi
                   áp dụng) — hai họ TÁCH BIỆT, KHÔNG gộp (đóng P03B-DELTA-MIN-01)
```

### 9d. Explicit deferred-domain dependency list

```text
Backtest Domain Contract/entity/event/schema:  KHÔNG tồn tại. UC-006–UC-010 mô tả hành vi product-
  level BẮT BUỘC (deterministic simulated economic evidence, exposure/position progression, strategy-
  level evaluable result) nhưng KHÔNG giả định "BacktestOrder"/"BacktestFill"/"BacktestPosition"/
  "BacktestExecutionResult" hay bất kỳ entity nào tương đương đã tồn tại — labeled "product-required,
  domain-representation deferred" tại UC-008/UC-009. Quyết định author Domain Contract riêng cho
  Backtest là Product Owner decision, ngoài phạm vi Package 0.3-A/0.3-B.

Research Domain Contract:  Tương tự — KHÔNG tồn tại research.md; UC-001–UC-003 mô tả hành vi quan sát
  thuần túy trên Domain Contract ĐÃ có (candle.md…context.md, strategy.md), KHÔNG giả định entity
  Research riêng.

PAPER-context authoritative Decision establishment mechanism (v0.2, MỚI, đóng `P03B-MAJ-01`):  Một
  PAPER-context authoritative Decision lineage RIÊNG BIỆT (TÁCH BIỆT khỏi Decision lineage của
  Backtest/Research) là precondition BẮT BUỘC cho UC-011 (§9.4) — NHƯNG cơ chế CHÍNH XÁC cách Decision
  đó được sinh ra/trigger/ghi nhận trong PAPER context KHÔNG được kiểm soát tường minh bởi
  `product-requirement.md` hiện có hay bất kỳ Domain Contract nào tại `/docs/domain/`. Tài liệu này
  KHÔNG tự phát minh cơ chế đó — chỉ pin YÊU CẦU (PAPER entry cần PAPER-context Decision lineage
  riêng) và BOUNDARY (Backtest/Research Decision KHÔNG BAO GIỜ được carry-forward/promote/reuse làm
  ancestor của nó). Quyết định cơ chế cụ thể là Product Owner decision/Domain Contract correction
  tương lai, ngoài phạm vi Package 0.3-A/0.3-B.
```

## 10. Deferred questions

```text
OQ-002:
  Open
  Strategy Lifecycle Live-gate deferred — kế thừa nguyên vẹn từ product-requirement.md §13. UC-015 CHỈ
  xác nhận Paper KHÔNG đặt lệnh thật; §8 "attempt to use Live behavior" CHỈ dừng workflow và disclose
  — KHÔNG định nghĩa điều kiện chuyển Live.

OQ-003:
  Open
  Concrete Product Metrics deferred — kế thừa nguyên vẹn từ product-requirement.md §13. UC-009/UC-010
  yêu cầu strategy-level evaluable result quan sát/so sánh được nhưng KHÔNG định nghĩa threshold/target/
  công thức scoring cụ thể nào.

Backtest/Research Domain Contract modeling:
  Kế thừa nguyên vẹn từ product-requirement.md §13 — xem §9d ở trên cho chi tiết áp dụng tại tầng
  workflow.
```

## 11. Explicit Non-Goals and Out-of-Scope

Kế thừa nguyên vẹn [`product-requirement.md`](./product-requirement.md) §11/§12 (Non-Goals/Out-of-Scope) — KHÔNG lặp lại toàn văn.

**Ngoài phạm vi tường minh của riêng tài liệu này (Package 0.3-B):**

- Screen layout, wireframe, component hierarchy, UX flow diagram chi tiết (Package 0.3-C, chưa author) — mọi Use Case tại §6 CHỈ mô tả behavior, KHÔNG mô tả UI cụ thể.
- Domain Contract state machine/transition mới (mọi Use Case CHỈ tham chiếu state machine đã `Consolidated Stable`).
- Backtest/Replay domain fact mới (`BacktestOrder`/`BacktestFill`/`BacktestPosition`/`BacktestExecutionResult`/`ReplayDecision` hay tương đương).
- Tái sử dụng PAPER fact làm Backtest authority.
- API/database/backend/frontend/infrastructure architecture.
- Security/custody/deployment.
- Product Metric threshold/target cụ thể (`OQ-003`).
- Live-gate criteria cụ thể (`OQ-002`).
- Mở rộng multi-tenant/đa tài sản (ngoài ADR-007 Phase 0-3).
- Product requirement mới — mọi Use Case CHỈ dùng `PR-XXX` đã tồn tại tại `product-requirement.md`.

## 12. Acceptance criteria for Package 0.3-B

```text
1. Toàn bộ 13 mục nội dung bắt buộc (§1–§13) có mặt và đầy đủ.
2. 21 Use Case (UC-001–UC-021), ID duy nhất, liên tục — bao trùm đầy đủ minimum coverage list cho cả
   sáu giai đoạn (Research/Replay/Backtest/Paper/Review/Improve).
3. Mỗi Use Case có đủ mười ba trường: Title/Primary actor/Goal/Trigger/Preconditions/Inputs/Main flow/
   Alternate-or-failure flows/Observable outcome/Evidence produced-or-consumed/PR traceability/Domain
   vocabulary used/Out-of-scope boundary.
4. Mọi workflow step truy vết được về một hoặc nhiều `PR-XXX` ID đã tồn tại tại `product-requirement.md`
   — KHÔNG có Use Case/step mồ côi PR traceability, KHÔNG product requirement mới nào được tạo.
5. Replay authority boundary giữ nguyên: historical reconstruction (mặc định) tách bạch parity
   recomputation (tuỳ chọn, non-authoritative); KHÔNG `ReplayDecision`; KHÔNG Decision trùng lặp; mọi so
   sánh dùng `canonical semantic-decision hash`.
6. Backtest authority boundary giữ nguyên: KHÔNG tái sử dụng PAPER Order/ExecutionResult/Fill/Position
   làm Backtest authority; KHÔNG entity/event Backtest mới; simulation/fee/slippage/accounting/PnL
   KHÔNG được định nghĩa; bước thiếu domain representation được label "product-required, domain-
   representation deferred", KHÔNG lấp đầy khoảng trống ngầm.
7. Paper workflow (UC-011–UC-015) dùng ĐÚNG chuỗi C7: Decision→Trade Intent→RiskEvaluation→Execution
   Intent→Order→OrderSubmissionRequest→ExecutionResultComputation→PaperExecutionObservation→
   ExecutionResult→Fill→Position — Fill economics từ PaperExecutionObservation, Position từ eligible
   Fill lineage, NON_EVALUABLE khi xung đột, KHÔNG lệnh thật.
8. Mọi failure/non-evaluable path tại §8 tuân thủ ĐÚNG bốn nguyên tắc fallback (workflow stops/state
   observable/reason disclosed/no downstream authoritative action) khi KHÔNG có controlling behavior
   tường minh — KHÔNG tự phát minh resolution semantics.
9. KHÔNG sửa `product-requirement.md`/Domain Contract/ADR/Constitution/architecture nào.
10. `OQ-002`/`OQ-003` giữ nguyên `Open`, không bị đóng ngầm; Live vẫn `Unauthorized`.
11. YAML frontmatter hợp lệ, `version: "0.6"`, `status: Draft`, `approved_by: null`, `approved_at: null`.
12. Baseline sẵn sàng cho ChatGPT Delta Review A + Independent Delta Review B trên CÙNG một commit/blob.
13. (v0.2) UC-011 KHÔNG BAO GIỜ carry-forward/promote/reuse Backtest/Research Decision identity làm
    authoritative PAPER Decision ancestor — PAPER entry đòi hỏi PAPER-context authoritative Decision
    lineage RIÊNG BIỆT; workflow dừng TRƯỚC PAPER execution khi lineage đó không eligible.
14. (v0.2) UC-020 tách bạch tường minh Backtest comparison (non-PAPER authority) khỏi PAPER comparison
    (authoritative); cross-mode viewing CHỈ juxtaposition hiển thị, KHÔNG merge identity/authority,
    KHÔNG unified execution-outcome fact; UC-020 material-trace cả `PR-031` LẪN `PR-032`.
15. (v0.2) UC-003 trả về đúng một trong PASSED/FAILED/INDETERMINATE, quan sát được, KHÔNG tạo entity/
    event "ResearchVerification" mới.
16. (v0.2) UC-007 KHÔNG ngụ ý run deletion lifecycle; UC-021 KHÔNG guarantee tuyệt đối evidence luôn
    khả dụng — cả hai dùng bốn nguyên tắc fallback khi cần.
17. (v0.2) KHÔNG entity/event Backtest mới (`BacktestOrder`/`BacktestFill`/`BacktestPosition`/
    `BacktestExecutionResult`) được invent; KHÔNG `ReplayDecision`/Replay authority stream mới; KHÔNG
    unified Backtest/PAPER outcome model nào được yêu cầu hay author.
18. (v0.3, MỚI) UC-021 resolve ĐỘC LẬP, tách bạch, CẢ HAI họ evidence lịch sử (Backtest non-PAPER
    authority VÀ PAPER authoritative) cho một Strategy Definition Version cũ — KHÔNG chỉ Decision fact
    đơn lẻ; danh tính version LUÔN hiển thị; missing evidence được identify theo TỪNG họ/loại, KHÔNG
    ngụ ý toàn bộ lịch sử mất khi chỉ một phần thiếu; KHÔNG tạo unified old-version evidence aggregate.
19. (v0.3, MỚI) UC-020 tiêu thụ đúng mode-separated scope của UC-021 — KHÔNG ngụ ý UC-021 trả về một
    cross-mode evidence object chung; ba comparison mode (Backtest-vs-Backtest, PAPER-vs-PAPER,
    cross-mode side-by-side) và toàn bộ nhãn mode/authority/evidence-type giữ nguyên.
20. (v0.4, đóng `F-03`) `PR-004`/`PR-005` material-trace tại `UC-007`/`UC-011`/`UC-016` — mỗi UC
    hiển thị tường minh Decision outcome/Strategy Instance nguồn gốc (PR-004) và/hoặc evidence trace
    đầy đủ/causation chain (PR-005) tại chính field Main flow/Observable outcome/Goal của nó, KHÔNG
    gán mồ côi; `UC-008`/`UC-009` KHÔNG nhận hai PR này vì chỉ tiêu thụ evidence phái sinh từ UC-007.
21. (v0.5, đóng `P03B-V04-A-MAJ-01`) `UC-007`/`UC-011`/`UC-016` operationalize đầy đủ acceptance
    evidence của `PR-004`/`PR-005` (v0.4 chỉ mechanically gán ID, chưa hiện thực hoá behavior): mỗi
    Decision hiển thị đúng một outcome (LONG/SHORT/NO_ACTION), Strategy Instance CHÍNH XÁC + Strategy
    Definition Version/configuration context nguồn gốc, VÀ recorded input snapshot/evaluation evidence
    đã dùng để tạo ra Decision đó — resolve TRỰC TIẾP từ recorded fact, KHÔNG suy diễn/tính lại sau sự
    kiện (v0.6 sửa causal-direction error tại `UC-007` — xem mục 22: RiskEvaluation KHÔNG phải evidence
    tạo ra Decision, luôn downstream). `UC-011` tách bạch tường minh upstream Decision evidence (hiển
    thị TRƯỚC khi khởi tạo) khỏi downstream C7 causation (fact do hành động khởi tạo sinh ra) —
    downstream chain KHÔNG tự nó ngụ ý thỏa PR-005. `UC-016` thêm bước 3 mới (Decision explainability
    evidence) tách biệt khỏi bước 2 downstream lineage. `UC-008`/`UC-009` KHÔNG đổi, KHÔNG nhận
    `PR-004`/`PR-005`. Backtest vẫn non-PAPER simulated, domain representation vẫn deferred;
    PAPER-context Decision separation, no-clone/no-carry-forward/no-promote/no-reuse giữ nguyên.
22. (v0.6, MỚI, đóng `P03B-V05-B-MAJ-01`, frozen finding) `UC-007` sửa causal-direction error: v0.5
    liệt kê "RiskEvaluation liên quan" như evidence dùng để TẠO RA Decision — SAI, vì RiskEvaluation
    (risk.md §1) đánh giá MỘT Trade Intent, mà Trade Intent chỉ tồn tại SAU KHI Decision result =
    LONG/SHORT (decision.md §9) — RiskEvaluation luôn causally downstream, KHÔNG BAO GIỜ là input tạo
    ra Decision. Main flow bước 2 nay tách bạch tường minh BA nhóm: (A) Decision outcome LONG/SHORT/
    NO_ACTION; (B) upstream Decision origin/explainability — Strategy Instance/Definition Version/
    configuration, recorded input snapshot, recorded evaluation/configuration evidence, KHÔNG còn chứa
    RiskEvaluation; (C) downstream lineage khi tồn tại — Trade Intent/RiskEvaluation/Execution Intent/
    related fact — hiển thị tách biệt khỏi B, với phát biểu tường minh downstream fact "causally
    derived from/related to Decision, KHÔNG phải evidence dùng để tạo ra nó." Cùng phân biệt áp dụng
    đồng bộ tại Observable outcome/Evidence consumed/PR traceability của `UC-007`. `UC-011`/`UC-016`/
    `UC-008`/`UC-009` KHÔNG đổi — finding chỉ về `UC-007`. `UC-001`–`UC-021` giữ nguyên identity; KHÔNG
    PR/UC/domain entity mới; Backtest non-PAPER/PAPER-context Decision separation/OQ-002/OQ-003 Open/
    Live Unauthorized giữ nguyên vẹn.
```

## 13. Handoff requirements for Package 0.3-C

Package 0.3-C (`ux-blueprint.md`) PHẢI:

1. Tham chiếu mọi screen/flow về đúng một hoặc nhiều `UC-XXX` ID tại đây — KHÔNG tự phát minh use case/workflow behavior mới ở tầng UX.
2. Giữ nguyên khung sáu-giai-đoạn (Research→Replay→Backtest→Paper→Review→Improve, §4/§6) — không thêm giai đoạn mới nếu chưa có Product Owner authorization riêng.
3. Giữ nguyên walking-skeleton discipline — 21 Use Case là bộ hành vi tối thiểu, KHÔNG mở rộng thêm behavior mới mà không có PR/UC tương ứng.
4. KHÔNG đóng `OQ-002`/`OQ-003` — kế thừa nguyên trạng `Open` từ §10.
5. Kế thừa nguyên vẹn **Replay authority boundary** (§6 UC-004/UC-005) và **Backtest authority boundary** (§6 UC-006–UC-010) — KHÔNG thiết kế screen/flow như thể Backtest tạo/tái sử dụng PAPER fact, hay Replay tạo Decision mới/`ReplayDecision`.
6. KHÔNG author screen layout/wireframe/component hierarchy VƯỢT QUÁ những gì cần để thể hiện behavior đã mô tả tại §6 — Package 0.3-C sở hữu HÌNH THỨC hiển thị, KHÔNG sở hữu behavior/logic (đã đóng tại đây).
7. KHÔNG định nghĩa Domain Contract semantic mới — mọi state/transition tham chiếu phải resolve về Domain Contract đã `Consolidated Stable`.
8. Với mỗi Failure/non-evaluable path tại §8, screen/flow tương ứng PHẢI thể hiện đúng bốn nguyên tắc (workflow stops/state observable/reason disclosed/no downstream authoritative action) — KHÔNG thiết kế UI ngụ ý một resolution semantics chưa được định nghĩa.
9. (v0.2, MỚI) KHÔNG thiết kế screen/flow cho UC-011 ngụ ý người dùng cung cấp một Order payload authoritative (quantity/order type/sizing) — chỉ intent khởi tạo; KHÔNG thiết kế UI ngụ ý một Decision từ Backtest/Research "trở thành" Decision PAPER.
10. (v0.2, MỚI) KHÔNG thiết kế screen/flow cho UC-020 gộp Backtest và PAPER evidence thành một "kết quả" duy nhất — mọi hiển thị cross-mode PHẢI giữ nhãn mode/authority/evidence-type tách biệt tường minh.
11. (v0.2, MỚI) KHÔNG thiết kế screen/flow cho UC-003 ngụ ý một trạng thái nhị phân (pass/fail) đơn giản hoá — PHẢI thể hiện đủ ba outcome PASSED/FAILED/INDETERMINATE.
12. (v0.2, MỚI) KHÔNG thiết kế screen/flow cho UC-021/UC-007 ngụ ý evidence/run identity luôn khả dụng tuyệt đối — PHẢI thể hiện rõ trạng thái "không khả dụng, lý do disclosed" khi áp dụng.
13. (v0.3, MỚI) KHÔNG thiết kế screen/flow cho UC-021 gộp Backtest evidence family và PAPER evidence family thành một representation/entity chung — mỗi họ PHẢI hiển thị tách biệt với nhãn mode/authority riêng, kể cả khi cả hai họ được yêu cầu cùng lúc; khi một phần evidence thiếu, PHẢI thể hiện rõ "incomplete" cho đúng phần đó — KHÔNG ngụ ý toàn bộ lịch sử Strategy Definition Version không khả dụng.
