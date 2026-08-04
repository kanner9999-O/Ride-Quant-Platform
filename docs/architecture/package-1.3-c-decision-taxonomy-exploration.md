---
id: package-1.3-c-decision-taxonomy-exploration
title: "Package 1.3-C — Decision Taxonomy Exploratory Evidence"
version: "0.1"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-04"
last_review: null
next_review: null
depends_on: ["ADR-015", "ADR-016", "07-module-taxonomy", "08-event-model", "09-plugin-model"]
---

# Package 1.3-C — Decision Taxonomy Exploratory Evidence

> **NON-AUTHORITATIVE — EXPLORATORY — NOT APPROVED — NOT IMPLEMENTATION-READY — EVIDENCE FOR ADR-016 ONLY.**
>
> Tài liệu này KHÔNG phải architecture decision, KHÔNG phải Package 1.3-C completion, KHÔNG selects/approves một taxonomy nào (hybrid HAY split), KHÔNG sửa ADR-015/ADR-016/Package 1.1 artifact/`phase-1-plan.md`. Mọi nội dung dưới đây là **candidate evidence** phục vụ DUY NHẤT [ADR-016](../adr/ADR-016.md) resume trigger — không thứ gì trong tài liệu này có hiệu lực kiến trúc cho tới khi qua Review A + Independent Review B + Product Owner decision, ghi nhận trong một ADR `Approved`.

## 0. Authorizing scope

Tài liệu này được author dưới **Gate 1 — Exploratory authoring authorization** ([`phase-1-plan.md`](./phase-1-plan.md) §6.1, v0.4 Approved, blob `fe272215a28563cf68c4eb28feb525c547240c6d`), mở qua Product Owner decision "I authorize opening Gate 1 for bounded Package 1.3-C exploratory architecture work." (2026-08-04). **Gate 2** (normal Package 1.3-C authorization — 1.3-B `Consolidated Stable`, Package 1.1 `Consolidated Stable`, ADR-016 `Approved`) **vẫn `blocked`**, không đổi bởi tài liệu này.

```text
Controlling artifacts (không đổi bởi tài liệu này):
  docs/adr/ADR-015.md                         v0.3, Approved, blob 37f2712aa0b204dcc6c58687226a4adcbeaa2f4f
  docs/adr/ADR-016.md                         v0.4, Draft, Decision Deferred, blob 5385ff81e6da480a7bee8c71279d82a16c1913cd
  docs/architecture/module-registry.yaml      v0.2, blob 2dd1e1fae8f886b605896864b432f3f79a3726d1
  docs/architecture/system-decomposition.md   v0.2, blob 45d745315ba36ea4ca53b5bb4bcd2aa6ca076293
  docs/architecture/phase-1-plan.md           v0.4, Approved, blob fe272215a28563cf68c4eb28feb525c547240c6d
```

Mục đích duy nhất: sản xuất evidence cho [ADR-016 §"Required deferral trigger"](../adr/ADR-016.md) mục 1–2 (authoritative responsibility definition + Package 1.3-C architecture candidate) và evaluation cho mục 3 (Chapter 7 §7.1). Mục 4 (Review A + Independent Review B) và mục 5 (Product Owner decision qua Approved ADR) **nằm ngoài phạm vi** tài liệu này.

## 1. Core question

Ba trách nhiệm cần phân biệt tường minh (đúng ADR-016 §"Lý do deferral" và §"Required deferral trigger" mục 1):

```text
1. Strategy Plugin advisory output — output của strategy-plugin-host (Chapter 9 §9.1, §9.4).
2. Platform-owned deterministic Decision evaluation — NẾU tồn tại như một trách nhiệm riêng biệt.
3. Authoritative Decision validation và append — sở hữu bởi decision-engine (Chapter 3 §3.1,
   ADR-010, Chapter 8 §8.4/§8.5).
```

**Trách nhiệm 3 đã xác lập** (Chapter 3 §3.1 khóa Decision identity ownership tại Decision Engine; decision.md/Package 0.2-C4 `Consolidated Stable` khóa entity/event shape). **Trách nhiệm 1 đã xác lập** (Chapter 9 §9.1: Strategy Plugin là Compute Engine điển hình, sinh candidate/advisory signal, KHÔNG sở hữu external side effect, KHÔNG authoritative). Câu hỏi CHƯA xác lập là **trách nhiệm 2 — có tồn tại hay không, và nếu có, nó nằm ở module nào.**

### 1.1 Có bằng chứng domain-level cho trách nhiệm 2 hay không (phân tích, KHÔNG giả định)

`decision.md` §5c (`rule_evidence`, entity `DecisionRecorded`, Package 0.2-C4, `Consolidated Stable`) định nghĩa một **bounded, platform-schema-owned rule family** — `rule_family: PRICE_CROSSES_REFERENCE_SERIES` (v0.1: đúng MỘT giá trị, KHÔNG DSL/parser/rule graph tự do) — với `crossing_policy`/`previous_condition_met`/`current_condition_met` là các trường **deterministic comparison** (`current_price_value > current_reference_value`, v.v.) mà `decision.md` §5e mô tả tường minh là **"rule evaluation THẬT"** tạo ra `result` (LONG/SHORT/NO_ACTION). Đồng thời, `decision_rule_ref` (§5c) — CHỌN rule nào — thuộc thẩm quyền `strategy_definition_version_id` (`strategy.md`, Strategy-side), KHÔNG thuộc Decision.

**Quan sát (evidence, KHÔNG phải kết luận thẩm quyền):** Domain Contract đã tự tách hai câu hỏi khác nhau — "rule nào được chọn" (Strategy-owned, `decision_rule_ref`) và "rule đó hiện có TRUE hay không tại cursor" (schema thuộc `decision.md`, platform-owned rule-evidence shape). Đây LÀ bằng chứng domain-level rằng một khái niệm "deterministic evaluation" tồn tại trong domain model — nhưng **Domain Contract KHÔNG gán khái niệm đó cho một module nào** (module taxonomy là thẩm quyền tách biệt, Chapter 7 §7.0). Vì vậy: **trách nhiệm 2 tồn tại như một khái niệm DOMAIN đã xác lập một phần** (rule-evidence shape), nhưng **KHÔNG xác lập ở tầng MODULE** — module nào tính toán `current_condition_met`/emit `rule_evidence` (Strategy Plugin tự tính rồi báo cáo, hay platform tự tính độc lập từ Candle/Feature fact) là chính xác câu hỏi Trigger 1 cần một authoritative responsibility definition để trả lời. Tài liệu này KHÔNG tự trả lời câu hỏi đó — chỉ ghi nhận nó tồn tại và có evidence domain-level liên quan.

## 2. Required semantic vocabulary (taxonomy-level only)

```text
Strategy advisory output:      non-authoritative recommendation, proposal, hoặc evaluation
                                input do một Strategy Plugin sinh ra (Chapter 9 §9.1, compute_engine,
                                swappable/promotable/rollback-able theo plugin lifecycle §9.8).

Decision evaluation:           deterministic, platform-owned evaluation CÓ THỂ transform hoặc
                                assess advisory output TRƯỚC authority validation, NẾU justified
                                (xem §1.1 — domain-level evidence tồn tại một phần qua rule_evidence
                                shape, nhưng module placement CHƯA xác lập).

Decision authority:            trách nhiệm validate invariant, thiết lập authoritative Decision
                                fact, và kiểm soát append (Chapter 3 §3.1: Decision Engine).

Decision record:                kết quả authoritative bất biến SAU KHI validate/append thành công
                                (`DecisionRecorded`, decision.md §5 — Consolidated Stable, KHÔNG
                                đổi bởi tài liệu này).
```

Không field-level schema nào được author tại đây — mọi field cụ thể (schema `DecisionRecorded`/`DecisionEvaluationAttemptRecorded`) đã tồn tại và `Consolidated Stable` tại `decision.md` (Package 0.2-C4), chỉ được **cite**, không redefine.

## 3. Required authority questions

```text
Who may propose?
  Strategy Plugin (qua strategy-plugin-host) — advisory output, non-authoritative, có thể bị
  bỏ (abandon)/thử lại tự do, KHÔNG tạo partial authoritative state.

Who may evaluate?
  CHƯA xác lập ở tầng module (§1.1) — HOẶC Strategy Plugin tự evaluate (rule check là một phần
  advisory computation), HOẶC một platform-owned evaluation responsibility riêng biệt tồn tại.
  Cả hai candidate dưới đây (§4/§5) mô hình hóa nhánh THỨ HAI (platform tự evaluate) — vì đây
  là nhánh cần bounded candidate để đối chiếu Chapter 7 §7.1; nhánh Plugin-tự-evaluate không
  cần một candidate mới (nó đã được mô hình hóa bởi strategy-plugin-host hiện có).

Who may validate?
  decision-engine (Candidate A) HOẶC Decision Authority Service (Candidate B) — validate proposal
  identity/version/cursor/eligibility TRƯỚC append (ADR-016 §"Alternatives considered" B).

Who may reject?
  DecisionEvaluationAttempt (decision.md §2, Consolidated Stable) ghi nhận MỌI outcome kể cả
  reject/failure (INELIGIBLE/INPUT_UNAVAILABLE/FAILED_BEFORE_EVALUATION) — entity này ĐÃ tồn
  tại độc lập taxonomy question, không đổi bởi candidate nào dưới đây. Ai GHI attempt đó phụ
  thuộc candidate (§4/§5).

Who may establish the authoritative Decision fact?
  DUY NHẤT decision-engine (Candidate A) hoặc Decision Authority Service (Candidate B) — atomic
  append, single point of authoritative write trong CẢ HAI candidate (không đổi giữa A/B).

Who owns idempotency?
  Candidate A: một điểm — decision-engine, theo decision.md §13 (`decision_computation_
  idempotency_policy`/`decision_evaluation_attempt_idempotency_policy`).
  Candidate B: hai điểm — Decision Evaluation Engine (idempotent-by-design, pure compute, tự
  thân KHÔNG cần policy riêng vì stateless) + Decision Authority Service (áp policy decision.md
  §13 tại append, không đổi so với A).

Who owns deterministic replay semantics?
  Candidate A: một module pin một bộ version (evaluation logic + input, cùng identity).
  Candidate B: hai trục pin riêng — Decision Evaluation Engine pin logic/rule version; Decision
  Authority Service pin exact evaluation-proposal artifact reference (Chapter 8 §8.1.1 Referenced
  Authoritative Artifact pattern) — replay phải resolve CẢ HAI để tái dựng đúng.

Who owns audit/explainability trace continuity?
  Candidate A: một điểm trace (decision.md §9 Explanation contract, không đổi).
  Candidate B: hai bản ghi liên kết qua `causation_refs` — pattern NÀY ĐÃ tồn tại trong domain
  model (DecisionRecorded.causation_refs trỏ DecisionEvaluationAttemptRecorded tương ứng, decision.md
  §5, Consolidated Stable) — Candidate B tái sử dụng CÙNG pattern causation cho một liên kết
  THÊM (proposal → attempt/append), không phát minh cơ chế mới.

Which responsibility is allowed to be bypassed?
  Non-authoritative proposal/evaluation attempt — CÓ THỂ bị abandon/discard/retry tự do KHÔNG
  hệ quả (ADR-016: "CHƯA phải Decision fact"; decision.md §2: attempt_outcome != DECIDED không
  tạo Decision nào) — đây là trách nhiệm DUY NHẤT được phép "bỏ qua" mà không cần cơ chế bypass
  đặc biệt, vì bản chất non-authoritative của nó.

Which responsibility must never be bypassed?
  Authoritative Decision validation/append (I-2 Decision Parity, I-7 Plugin Non-Bypass) VÀ downstream
  Risk Gateway (I-4, I-7 — Decision Trade Intent PHẢI qua Risk Gateway, không exception).
```

## 4. Candidate A — Bounded non-overlapping hybrid

```text
Module identity:            decision-engine (identity KHÔNG đổi — module-registry.yaml v0.2,
                             candidate, KHÔNG sửa bởi tài liệu này).
Taxonomy types involved:    primary runtime_service (Chapter 7 Type 3); secondary "compute-like"
                             decision_evaluation (potential hybrid, Chapter 7 §7.1).
Responsibility boundary:    MỘT module sở hữu CẢ deterministic evaluation của Strategy advisory
                             output tại decision_context_cursor LẪN authoritative Decision/Trade
                             Intent identity + append.
Inputs/outputs (category):  IN — Strategy advisory output (qua strategy-plugin-host, cursor-
                             bounded), Strategy Definition Version pin (ADR-013), Context
                             Aggregator snapshot (cursor-bounded). OUT — DecisionEvaluationAttempt
                             Recorded (mọi outcome), DecisionRecorded (chỉ DECIDED), Trade Intent
                             identity cho downstream.
Authority boundary:         decision-engine LÀ authority DUY NHẤT cho Decision/Trade Intent fact
                             — không module nào khác được tạo fact này.
Source-of-truth boundary:   decision.md entity (Decision, DecisionEvaluationAttempt) — decision-
                             engine là writer DUY NHẤT của cả hai.
Idempotency ownership:      một điểm — decision-engine, đúng decision.md §13 (hai policy: Decision-
                             level + Attempt-level, cùng module enforce cả hai).
Replay behavior:            replay tái dựng cả attempt outcome lẫn Decision result từ CÙNG module,
                             evaluation-logic version pin cùng identity với module — không cần
                             thêm trục pin nào ngoài input/config hiện có (strategy_definition_
                             version_id, configuration_version_ref — đã có sẵn theo decision.md §5b).
Explainability trace
  ownership:                một điểm trace — toàn bộ evidence chain (strategy/rule/input evidence,
                             attempt outcome) trong CÙNG module, đúng decision.md §9.
Plugin non-bypass
  enforcement:               module-registry.yaml decision-engine entry đã khai `forbidden_
                             dependencies: [execution-engine, paper-execution-boundary]`; `depends_
                             on: [strategy-engine, strategy-plugin-host, context-aggregator]` —
                             decision-engine TIÊU THỤ Plugin advisory output (query/event) nhưng
                             Plugin KHÔNG BAO GIỜ có quyền ghi Decision fact (I-7), enforce ở
                             module-boundary level (registry) VÀ Chapter 9 §9.4/§9.5.
Failure/rejection
  boundary:                  mọi failure category (INELIGIBLE/INPUT_UNAVAILABLE/FAILED_BEFORE_
                             EVALUATION) ghi nhận trong CÙNG module — không cross-module handoff
                             rejection state.
Why reasonably separable
  or not:                    KHÔNG kết luận tại đây (xem §7 Chapter 7 §7.1 evaluation) — candidate
                             này mô hình hóa trạng thái "giữ nguyên", KHÔNG tự chứng minh nó là
                             lựa chọn đúng.
```

## 5. Candidate B — Non-overlapping split

```text
Module identity:            decision-evaluation-engine (compute_engine, HYPOTHETICAL — không
                             tồn tại trong module-registry.yaml, đề xuất evidence-only) +
                             decision-authority-service (runtime_service, HYPOTHETICAL rename/
                             narrowing của decision-engine entry NẾU candidate này được chọn
                             tương lai — module-registry.yaml KHÔNG đổi tại tài liệu này).
Taxonomy types involved:    Decision Evaluation Engine = compute_engine (Chapter 7 Type 1 —
                             biến đổi domain information thành output, KHÔNG external side
                             effect — khớp chính xác định nghĩa). Decision Authority Service =
                             runtime_service (Chapter 7 Type 3, không đổi từ decision-engine
                             hiện tại).
Responsibility boundary:
```

### 5.1 Decision Evaluation Engine (compute_engine)

```text
- deterministic; đọc cursor-bounded/version-pinned input (Strategy advisory output, Context
  Aggregator snapshot, Strategy Definition Version pin);
- sinh evaluation proposal KHÔNG authoritative (immutable, identity + version riêng để pin cho
  deterministic replay — cùng nguyên tắc Referenced Authoritative Artifact, Chapter 8 §8.1.1,
  áp dụng tương tự cho artifact loại proposal);
- KHÔNG sở hữu Decision hay Trade Intent identity (`owns_authoritative_state: false`, cùng
  convention `strategy-plugin-host` hiện có);
- KHÔNG được bypass Decision Authority Service hay Risk Gateway.
```

### 5.2 Decision Authority Service (runtime_service)

```text
- validate proposal identity/version/cursor/eligibility;
- reject proposal cũ/trùng/invalid;
- sở hữu Decision và Trade Intent identity (không đổi từ decision-engine hiện tại);
- thực hiện atomic authoritative Decision append DUY NHẤT (single point of authoritative write,
  không đổi so với Candidate A).
```

### 5.3 Evidence dimensions (cùng cấu trúc §4)

```text
Inputs/outputs (category):  Decision Evaluation Engine IN — Strategy advisory output, Context
                             snapshot, Strategy Definition Version pin. OUT — evaluation proposal
                             artifact (non-authoritative). Decision Authority Service IN —
                             evaluation proposal artifact. OUT — DecisionEvaluationAttemptRecorded
                             (mọi outcome), DecisionRecorded (DECIDED), Trade Intent identity.
Authority boundary:         DUY NHẤT Decision Authority Service được tạo Decision/Trade Intent
                             fact — Decision Evaluation Engine KHÔNG có quyền này (khớp Chapter
                             7 Type 1: "Không sở hữu external side effect").
Source-of-truth boundary:   Decision Authority Service là writer DUY NHẤT của decision.md entity.
                             Evaluation proposal artifact là MỘT LOẠI ARTIFACT MỚI CHƯA có Domain
                             Contract — governance gap thật (không phải field-level schema tại
                             đây, chỉ ghi nhận sự tồn tại của gap).
Idempotency ownership:       HAI điểm (xem §3 "Who owns idempotency") — chi phí thêm so với
                             Candidate A, không phải blocker.
Replay behavior:            HAI trục pin (xem §3 "Who owns deterministic replay semantics") —
                             chi phí thêm, khả thi nếu thiết kế đúng (không tự động unsafe).
Explainability trace
  ownership:                HAI bản ghi liên kết causation_refs (xem §3) — audit trail chi tiết
                             hơn (proposal reject riêng biệt observable) nhưng thêm độ phức tạp
                             trace so với Candidate A.
Plugin non-bypass
  enforcement:               Decision Evaluation Engine `forbidden_dependencies` PHẢI loại trừ
                             execution-engine/risk-gateway/paper-execution-boundary (cùng pattern
                             strategy-plugin-host); Decision Evaluation Engine output PHẢI đi
                             qua Decision Authority Service — KHÔNG route trực tiếp Trade Intent/
                             Risk Gateway.
Failure/rejection
  boundary:                  HAI điểm rejection — (a) Decision Evaluation Engine fail TRƯỚC khi
                             sinh proposal (map attempt_outcome INELIGIBLE/INPUT_UNAVAILABLE/
                             FAILED_BEFORE_EVALUATION, decision.md §2 — entity ĐÃ tồn tại, không
                             đổi); (b) Decision Authority Service reject một proposal ĐÃ sinh
                             hợp lệ nhưng stale/duplicate/invalid tại validation — outcome NÀY
                             CHƯA có mapping tường minh trong decision.md's `attempt_outcome`
                             enum hiện có (bốn giá trị: DECIDED/INELIGIBLE/INPUT_UNAVAILABLE/
                             FAILED_BEFORE_EVALUATION) — **governance gap ghi nhận, KHÔNG tự
                             resolve tại đây** (đòi hỏi Domain Contract correction ngoài phạm vi
                             tài liệu này nếu Candidate B được chọn tương lai).
Why reasonably separable
  or not:                    KHÔNG kết luận tại đây (xem §7).
```

### 5.4 Xác nhận không rò rỉ Decision authority (yêu cầu task)

```text
Strategy Plugin Host:        KHÔNG — forbidden_dependencies hiện có (execution-engine/risk-
                              gateway/paper-execution-boundary) không đổi; Plugin output vẫn
                              non-authoritative advisory, không được validate/append trực tiếp.
Decision Evaluation Engine:  KHÔNG — compute_engine, owns_authoritative_state: false (đề xuất,
                              khớp Chapter 7 Type 1), không quyền tạo Decision/Trade Intent fact.
Context Aggregator:          KHÔNG đổi — projection, Chapter 7 §7.4 cấm authoritative domain
                              fact/decision, không chạm bởi candidate này.
Event Bus:                   KHÔNG đổi — transport, Chapter 8 §8.1 không phải authoritative
                              source, không chạm bởi candidate này.
Projection/read model:       KHÔNG đổi — Chapter 7 §7.4, không authoritative, không chạm bởi
                              candidate này.
```

## 6. Candidate comparison

**Assumptions (tường minh, không weight ngầm):** (1) Cả hai candidate giả định thiết kế ĐÚNG (correct-by-design) — không so sánh implementation lỗi giả định. (2) Không tiêu chí nào được gán trọng số — bảng dưới trình bày TỪNG tiêu chí độc lập, KHÔNG tính điểm tổng hợp; việc weight tiêu chí nào quan trọng hơn là Product Owner decision tại thời điểm resume, KHÔNG phải kết luận của tài liệu evidence này. (3) "Reversibility" đánh giá theo chi phí ĐẢO NGƯỢC candidate sau khi đã implement — KHÔNG đánh giá trước implementation.

| Tiêu chí | Candidate A (hybrid) | Candidate B (split) |
|---|---|---|
| Responsibility cohesion | Cao — một module, hai trách nhiệm liên kết chặt | Trung bình — tách rõ "tính toán" khỏi "cam kết", nhưng ranh giới với `strategy-plugin-host` chưa rõ |
| Separability | Không kết luận (§7) | Không kết luận (§7 áp cho A; kỹ thuật khả thi theo ADR-016, không đồng nghĩa nên chọn) |
| Authority clarity | Cao — một điểm authority | Cao — Decision Authority Service vẫn một điểm authority duy nhất (không đổi so với A) |
| Least privilege | Trung bình — module cần cả quyền compute lẫn quyền ghi authoritative | Cao — Decision Evaluation Engine đọc-only, ít quyền hơn; Decision Authority Service giữ quyền ghi riêng |
| Plugin non-bypass | Giữ nguyên — không đổi | Giữ nguyên — không đổi, xem §5.4 |
| Source-of-truth clarity | Cao — một writer | Cao cho Decision entity; THÊM một artifact loại mới (evaluation proposal) chưa có Domain Contract — governance gap |
| Idempotency | Một điểm enforce | Hai điểm enforce — chi phí thêm |
| Deterministic replay | Một trục pin | Hai trục pin — khả thi nếu thiết kế đúng, chi phí thêm |
| Explainability | Một điểm trace | Hai bản ghi liên kết — audit chi tiết hơn nhưng phức tạp hơn |
| Testability | Trung bình — cần toàn bộ Decision Authority machinery để test evaluation logic | Cao — Decision Evaluation Engine test độc lập |
| Failure isolation | Một failure domain, đơn giản | Hai failure domain — cần recoverable-append-gap design (precedent: risk.md `RiskEvaluationAttemptRecorded` → `RiskEvaluation`, C5-MAJ-01) |
| Transactional consistency | Không cần đồng bộ liên-module | Chapter 8 không cấm cross-module evaluation (ADR-016 §"Chapter 7 condition 1 re-evaluation"); Append-and-Revalidate (ADR-010 §2.6) là precedent gap evaluation→append được chấp nhận |
| Operational complexity | Thấp — một module deploy/monitor | Cao hơn — thêm một module deploy/monitor/version |
| Dependency complexity | Thấp — không thêm edge | Cao hơn — thêm một node + một edge trong dependency graph |
| Reversibility | Cao — internal code-level separation (evaluation logic tách biệt append logic BÊN TRONG module) khả thi mà không cần published-contract change | Thấp hơn sau khi implement — đảo ngược đòi hỏi merge lại module + rút published contract "evaluation proposal" đã publish |
| Future multi-strategy/plugin extensibility | Không rõ ràng hơn/kém hơn — scale theo throughput của MỘT module | Không rõ ràng hơn/kém hơn — NẾU ranh giới với `strategy-plugin-host` không rõ, nguy cơ hai compute path song song trùng lặp theo từng plugin type (§5.3 "god-module risk" ngược, xem ADR-016) — giả định cần candidate resolve ranh giới TRƯỚC khi kết luận extensibility tốt hơn |

Không tổng hợp điểm số duy nhất — bảng trên là input evidence cho Review A/Independent Review B/Product Owner decision, KHÔNG phải một kết luận đã weight.

## 7. Chapter 7 §7.1 evaluation (Candidate A)

Đánh giá Candidate A đối chiếu đầy đủ bốn điều kiện Chapter 7 §7.1 ([Chapter 7](../constitution/07-module-taxonomy.md)). Mỗi điều kiện trả về giá trị CHÍNH XÁC một trong ba: `SATISFIED` / `NOT SATISFIED` / `NOT ESTABLISHED`, kèm bằng chứng TÍCH CỰC — KHÔNG suy luận từ thiếu chi tiết.

```text
Condition 1 — responsibilities không thể tách hợp lý về semantic/transaction boundary:
  NOT ESTABLISHED.
  Bằng chứng: §1.1 xác nhận domain model đã tách một phần khái niệm "rule chọn" (Strategy-
  owned) khỏi "rule evaluation THẬT" (decision.md schema) — đây là bằng chứng domain-level
  RẰNG tách KHÔNG hiển nhiên bất khả thi. Đồng thời, Candidate B (§5) chứng minh một split
  kỹ thuật-khả-thi CÓ THỂ được mô tả cụ thể (module identity, boundary, inputs/outputs, authority
  — không cần author Decision algorithm để mô tả CẤU TRÚC split, dù ranh giới CHÍNH XÁC với
  strategy-plugin-host vẫn chưa resolve). KHÔNG có bằng chứng TÍCH CỰC nào cho "không thể tách"
  — chỉ có một câu hỏi ranh giới CHƯA trả lời (Trigger 1 domain). Tài liệu này tự nó KHÔNG PHẢI
  "authoritative responsibility definition" (ADR-016 định nghĩa nguồn hợp lệ: Domain Contract
  correction, ADR mới, hoặc Product Owner decision qua Decision Workflow — evidence artifact
  không thuộc ba loại này) — do đó điều kiện 1 GIỮ NGUYÊN NOT ESTABLISHED, không đổi bởi tài
  liệu này.

Condition 2 — ownership không vi phạm Chapter 3 §3.1 hay Context Map:
  NOT ESTABLISHED.
  Bằng chứng: Chapter 3 §3.1 xác nhận Decision identity ownership thuộc Decision Engine — điều
  này ĐÚNG cho CẢ HAI candidate (Candidate A giữ trong một module; Candidate B giữ tại Decision
  Authority Service, không đổi authority). Nhưng liệu "decision_evaluation" secondary
  responsibility CỤ THỂ (nếu giữ hybrid) có vi phạm ranh giới Compute-Engine-like trách nhiệm
  của `strategy-plugin-host` hay không phụ thuộc CHÍNH XÁC ranh giới chưa resolve (cùng gap ở
  điều kiện 1) — chưa chọn được boundary thì chưa đánh giá dứt khoát được theo hướng nào.

Condition 3 — primary type và secondary role khai báo tường minh trong module-registry:
  SATISFIED (cho representation candidate HIỆN TẠI).
  Bằng chứng: `module-registry.yaml` v0.2 `decision-engine` entry ĐÃ khai `module_type:
  runtime_service` + `hybrid.secondary_responsibility: decision_evaluation` tường minh (dòng
  298-318, blob 2dd1e1fae8f886b605896864b432f3f79a3726d1 — KHÔNG đổi bởi tài liệu này). Điều
  kiện 3 hỏi "đã khai báo tường minh chưa" — CÓ. Điều kiện này KHÔNG hỏi "đã đúng/đã approve
  chưa" (Package 1.1 vẫn candidate, KHÔNG Consolidated Stable) — hai câu hỏi khác nhau, đúng
  phân biệt ADR-016 đã lập.

Condition 4 — quyết định ghi bằng ADR (Governance §4b):
  NOT SATISFIED.
  Bằng chứng: ADR-016 vẫn `status: Draft`, `approved_by: null` — chưa Approved. Sự tồn tại của
  tài liệu evidence này (Draft, non-authoritative) KHÔNG tự nó thỏa điều kiện 4 — điều kiện 4
  CHỈ thỏa khi một ADR chứa quyết định thực sự được hỗ trợ bằng chứng VÀ đã `Approved`. Đúng
  yêu cầu task: giá trị này PHẢI giữ NOT SATISFIED cho tới khi ADR-016 Approved.
```

**Kết luận §7:** không điều kiện nào trong bốn điều kiện đạt trạng thái cho phép Candidate A (hybrid) được coi governance-valid tại thời điểm này — Package 1.1's `decision-engine` hybrid entry giữ nguyên `proposed`/`unresolved`/`NOT governance-valid`, đúng ADR-016 hiện tại (KHÔNG đổi bởi tài liệu này).

## 8. Split validation (Candidate B)

```text
No overlapping authority:            Addressed — Decision Authority Service DUY NHẤT sở hữu
                                      Decision/Trade Intent identity; Decision Evaluation Engine
                                      owns_authoritative_state: false (§5.1/§5.4).
No hidden authoritative append:      Addressed — evaluation proposal KHÔNG BAO GIỜ tự nó là
                                      Decision fact; chỉ Decision Authority Service append.
No Plugin authority leakage:         Addressed — §5.4 xác nhận cả năm component (Plugin Host,
                                      Evaluation Engine, Context Aggregator, Event Bus, Projection)
                                      đều KHÔNG có Decision authority.
Clear proposal-versus-fact
  distinction:                        Addressed — evaluation proposal (non-authoritative, có thể
                                      abandon/retry) tách biệt tường minh khỏi DecisionRecorded
                                      (authoritative, bất biến) — đúng vocabulary §2.
Clear transaction ownership:         Addressed — atomic append DUY NHẤT tại Decision Authority
                                      Service (không đổi so với Candidate A); Decision Evaluation
                                      Engine không sở hữu transaction ghi authoritative nào.
Deterministic replay:                Addressed với chi phí thêm — khả thi NẾU thiết kế đúng (hai
                                      trục pin, §5.3), không tự động unsafe, nhưng CHƯA có
                                      candidate proposal-artifact contract cụ thể (governance gap
                                      ghi nhận, không tự resolve).
Idempotent evaluation:               Addressed — Decision Evaluation Engine idempotent-by-design
                                      (pure deterministic compute, khớp Chapter 7 Type 1).
Idempotent authority append:         Addressed — không đổi từ decision.md §13 policy hiện có
                                      (Consolidated Stable, không sửa).
Trace continuity:                    Addressed — tái sử dụng pattern causation_refs đã tồn tại
                                      trong domain model (§3), không phát minh cơ chế mới.
Failure isolation:                   Addressed với residual gap ghi nhận — §5.3(b): rejection tại
                                      Decision Authority Service (proposal hợp lệ nhưng stale/
                                      duplicate/invalid) CHƯA có mapping tường minh trong
                                      `attempt_outcome` enum hiện có của decision.md — governance
                                      gap, KHÔNG tự resolve tại tài liệu này (đòi hỏi Domain
                                      Contract correction ngoài phạm vi nếu Candidate B chọn).
```

**Không tuyên bố Candidate B đã selected hay approved** — validation trên xác nhận tính khả thi kỹ thuật/cấu trúc, KHÔNG phải một quyết định.

## 9. Effect on ADR-015 baseline

```text
Candidate A:
  no ADR-015 baseline change — pin hiện tại (`decision-engine` primary runtime_service + hybrid
  secondary decision_evaluation) ĐÃ khớp chính xác candidate này, không cần sửa gì.

Candidate B:
  a future module rename       — CÓ THỂ (decision-engine → decision-authority-service, hoặc giữ
                                  tên, chỉ thu hẹp responsibilities + xóa field `hybrid`).
  a future module split        — CÓ (thêm module_id mới `decision-evaluation-engine`,
                                  compute_engine).
  a future dependency-edge
    amendment                  — CÓ (risk-gateway.depends_on hiện trỏ `decision-engine` — cần
                                  resolve lại; decision-authority-service.depends_on cần thêm
                                  edge tới decision-evaluation-engine).
  a superseding ADR            — KHÔNG BẮT BUỘC ADR-015 bị supersede — ADR-015 pin baseline
                                  Package 1.1 v0.2 CÓ THỂ nhận bounded follow-up correction (cùng
                                  pattern đã dùng cho P11-A-MAJ-01/02, KHÔNG cần re-approve toàn
                                  bộ ADR-015) NẾU ADR-016 (hoặc bản kế nhiệm) đạt `Approved` với
                                  Alternative B selected — chính ADR-016 là cơ chế ghi nhận quyết
                                  định taxonomy này (Governance §4b), KHÔNG phải một ADR mới
                                  supersede ADR-015.
```

**Phân biệt bắt buộc (yêu cầu task):** mục trên là **evidence of compatibility** (candidate nào tương thích/không tương thích với pin hiện tại, và cần correction loại nào NẾU chọn) — **KHÔNG phải authorization to change the baseline**. `docs/adr/ADR-015.md` và `docs/architecture/module-registry.yaml`/`system-decomposition.md` **KHÔNG bị sửa** bởi tài liệu này (verified byte-identical, xem §"Frozen files" trong báo cáo transaction).

## 10. ADR-016 resume-trigger mapping

```text
Trigger 1 — authoritative responsibility definition:
  candidate evidence produced, NOT authoritative. §1.1/§2/§3 phân tích domain evidence hiện có
  và đề xuất vocabulary/authority-question answers ở mức taxonomy — nhưng tài liệu này KHÔNG
  phải Domain Contract correction, KHÔNG phải ADR, KHÔNG phải Product Owner decision qua Decision
  Workflow (ba nguồn hợp lệ duy nhất theo ADR-016) — do đó KHÔNG tự thỏa Trigger 1.

Trigger 2 — Package 1.3-C architecture candidate:
  produced. §4 (Candidate A, bounded hybrid) và §5 (Candidate B, non-overlapping split) đều
  author đầy đủ evidence dimensions yêu cầu (module identity, taxonomy type, responsibility
  boundary, inputs/outputs, authority/source-of-truth boundary, idempotency, replay,
  explainability, Plugin non-bypass, failure boundary).

Trigger 3 — Chapter 7 §7.1 validation:
  produced. §7 đánh giá đầy đủ bốn điều kiện cho Candidate A với bằng chứng tích cực (KHÔNG suy
  luận từ thiếu chi tiết); §8 validate Candidate B đối chiếu mười tiêu chí split-specific.

Trigger 4 — Review A + Independent Review B:
  not satisfied. Tài liệu này CHƯA qua review nào — `reviewers: []` tại frontmatter.

Trigger 5 — Product Owner decision trong một Approved ADR:
  not satisfied. ADR-016 vẫn `Draft`, `approved_by: null` — không đổi bởi tài liệu này.
```

**Do đó: ADR-016 KHÔNG được coi là resumed hay resolved bởi tài liệu này.** Disposition ADR-016 giữ nguyên `DEFERRED`.

## 11. Required conclusion (neutral evidence)

Dựa trên evidence đã sản xuất tại §1–§10:

```text
Candidate A lacks positive evidence for condition 1 — §7 xác nhận NOT ESTABLISHED, không phải
"thỏa" theo hướng giữ hybrid; domain evidence tại §1.1 nghiêng nhẹ về hướng "tách được", nhưng
KHÔNG đủ để đảo ngược thành bằng chứng tích cực cho tách.

Candidate B is technically credible — §5/§8 chứng minh một split có cấu trúc rõ ràng (authority/
source-of-truth/idempotency/replay/trace đều Addressed hoặc Addressed-với-chi-phí), NHƯNG mang
theo MỘT governance gap thật (proposal-rejection outcome chưa có mapping trong attempt_outcome
enum hiện có, §5.3/§8) và MỘT câu hỏi ranh giới CHƯA giải quyết với strategy-plugin-host (§6
"Future multi-strategy/plugin extensibility", §1.1) — giống hệt root cause khiến condition 1
NOT ESTABLISHED cho Candidate A.

Both remain viable pending review — không candidate nào có bằng chứng đủ mạnh để loại candidate
còn lại tại evidence-authoring stage này; cả hai chia sẻ CÙNG MỘT root uncertainty (ranh giới
Plugin advisory output ↔ platform Decision evaluation), không phải hai uncertainty độc lập.
```

**Không kết luận nào trong số sau được đưa ra (forbidden, đúng yêu cầu task):** hybrid approved; split approved; ADR-016 resolved; Package 1.1 unblocked; official architecture selected.

## 12. Required stop-condition check

```text
Forbidden implementation/schema scope entered?          KHÔNG — không field-level schema, không
                                                          API/database schema, không Decision
                                                          algorithm nào được author (§2/§5 chỉ
                                                          cite Domain Contract hiện có).
Conflict với ADR-015 hoặc Approved ADR khác?             KHÔNG — §9 xác nhận Candidate A không
                                                          cần sửa pin; Candidate B chỉ mô tả effect
                                                          GIẢ ĐỊNH, không tự authorize, không mâu
                                                          thuẫn nội dung ADR-015 hiện có.
Product/Domain/Constitution semantics chưa authorize
  bị yêu cầu?                                            KHÔNG — §1.1 chỉ CITE decision.md §5c/§5e
                                                          đã Consolidated Stable, không redefine.
Repository baseline đổi?                                 KHÔNG — HEAD xác nhận khớp expected trước
                                                          khi author (xem báo cáo transaction).
Scope mở rộng ngoài ADR-016 evidence?                    KHÔNG — toàn bộ nội dung map trực tiếp
                                                          về ADR-016 §"Required deferral trigger"
                                                          mục 1-3.
```

**Không stop condition nào đạt tới** — transaction tiếp tục tới commit.

## 13. Self-review

```text
Authority vs evaluation:
  Concern: liệu §3 có ngầm gán "evaluate" cho một module cụ thể không?
  Risk: nếu có, tài liệu tự mâu thuẫn với §1.1's kết luận "module placement CHƯA xác lập".
  Recommendation: §3 "Who may evaluate?" tường minh ghi "CHƯA xác lập ở tầng module" TRƯỚC khi
  mô tả hai candidate là các MÔ HÌNH khả dĩ (không phải câu trả lời đã chọn) — verified, không
  cần sửa thêm.

Proposal vs authoritative fact:
  Concern: §5.1's "evaluation proposal" có thể bị đọc nhầm là một Decision fact.
  Risk: nhầm lẫn governance nếu reader bỏ qua "KHÔNG authoritative" qualifier.
  Recommendation: mọi lần nhắc "evaluation proposal" trong tài liệu đều kèm "KHÔNG authoritative"
  hoặc tương đương — verified qua rà soát §5/§8.

Hybrid vs split neutrality:
  Concern: §6 bảng so sánh có thể đọc như nghiêng về Candidate B (nhiều dòng "Addressed"/"Cao"
  hơn ở cột B tại một số tiêu chí kỹ thuật).
  Risk: neutrality bị vi phạm nếu không cân bằng bằng các tiêu chí A thắng (operational/dependency
  complexity, reversibility, explainability nhẹ nghiêng A) và root uncertainty CHUNG (§11).
  Recommendation: §11 explicit nêu CẢ HAI candidate chia sẻ CÙNG root uncertainty, không kết luận
  candidate nào thắng — verified.

Current vs future tense:
  Concern: §5's "decision-authority-service" có thể đọc như đã tồn tại.
  Risk: vi phạm "NOT implementation-ready"/"NOT authoritative" label nếu đọc thoáng.
  Recommendation: §5 mở đầu bằng "HYPOTHETICAL" tường minh cho cả hai module identity mới —
  verified.

Candidate vs approved architecture:
  Concern: §9's "a future module split" có thể đọc như một kế hoạch đã cam kết.
  Risk: ngụ ý authorization vượt phạm vi evidence-only.
  Recommendation: §9 kết bằng phân biệt tường minh "evidence of compatibility" KHÔNG PHẢI
  "authorization to change the baseline" — verified, đúng yêu cầu task.

Evidence vs decision:
  Concern: §7's "SATISFIED" cho condition 3 có thể bị đọc nhầm thành "candidate A hợp lệ".
  Risk: condition 3 chỉ xác nhận ĐÃ KHAI BÁO, không xác nhận ĐÚNG/APPROVED — nếu không phân biệt
  rõ, reader có thể kết luận sai Package 1.1 sẵn sàng Consolidated Stable.
  Recommendation: §7 condition 3 tường minh nhắc lại "KHÔNG hỏi đã đúng/đã approve chưa — Package
  1.1 vẫn candidate" — verified.

ADR-015 compatibility vs permission to modify:
  Concern: đã giải quyết tại §9 self-review ở trên — không lặp lại.

Trigger produced vs trigger satisfied:
  Concern: §10's "produced" cho Trigger 2/3 có thể bị đọc nhầm thành "satisfied"/"resumed".
  Risk: nếu đọc nhầm, có thể dẫn tới hành động sai (coi ADR-016 đã sẵn sàng resume mà chưa qua
  Review A/B + Product Owner decision).
  Recommendation: §10 kết bằng câu tường minh "ADR-016 KHÔNG được coi là resumed hay resolved bởi
  tài liệu này" — verified; §11 cũng liệt kê "ADR-016 resolved" vào danh sách forbidden
  conclusions.
```

Không self-approve — tài liệu này `status: Draft`, `approved_by: null`, chờ Review A + Independent Review B + Product Owner decision đúng ADR-016 §"Required deferral trigger" mục 4-5.
