---
id: decision
title: Decision
version: "0.5"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-07-31"
last_review: null
next_review: null
---

# Decision

> **Vai trò của tài liệu này:** Một trong hai Domain Contract của Package 0.2-C4 (Trade Intent and Decision Foundation) — định nghĩa **Decision** (bản ghi authoritative của MỘT lần Strategy Instance đánh giá deterministic tại một computation cursor cụ thể) và **DecisionEvaluationAttempt** (bản ghi authoritative của MỘT LẦN THỬ đánh giá — kể cả khi không dẫn tới Decision, v0.2). Draft, chưa Approved/Locked. Thuộc capability `decision-management` / context `strategy-decision` (đăng ký MỚI tại [`context-map.yaml`](./context-map.yaml) trong transaction gốc). Kiến trúc controlling: [ADR-010](../adr/ADR-010.md) **Approved** (Decision Time Model — `decision_time`/`decision_context_cursor`/Append-and-Revalidate), [Chapter 8 §8.2.1/§8.4/§8.4.1/§8.5](../constitution/08-event-model.md) (Locked, decision-class event cardinality + canonical Replay Cursor schema), [ADR-013](../adr/ADR-013.md) v0.3 Approved (bốn trục evidence độc lập, qua `strategy.md`), [`strategy.md`](./strategy.md) v0.3 Draft §9a/§10 (computation eligibility + chín-field evidence). Tài liệu này CHỈ implement field/invariant mà các nguồn trên yêu cầu, KHÔNG lặp lại toàn văn, KHÔNG tự quyết architecture mới ngoài phạm vi đã khóa.

Decision **KHÔNG phải** Strategy/Strategy Instance (`strategy.md`, đã author), KHÔNG phải Trade Intent (`trade-intent.md`, file riêng), KHÔNG phải Risk Action/Risk Approval, KHÔNG phải Execution Intent/Order/Fill/Position/Replay Event (Package 0.2-C5–C7, chưa author), KHÔNG phải một workflow engine hay rule DSL. Nó là **bản ghi authoritative, bitemporal, deterministic, tự-giải-thích được** của một lần đánh giá — trả lời chính xác bảy câu hỏi: Strategy Instance nào đánh giá? Trục evidence chính xác nào được dùng? Rule nào được đánh giá? Input authoritative nào visible? Kết quả gì? Tại sao? Có tạo Trade Intent không?

**Ví dụ walking-skeleton duy nhất dùng để validate thiết kế (KHÔNG phải yêu cầu xây dựng DSL tổng quát):** "Go LONG khi candle hiện tại đóng cửa strictly above EMA(period), và candle trước đóng cửa ≤ EMA trước đó." Chín Scenario chấp nhận (1–9, xem §18) đều dựa trên ví dụ này.

**`decision-evaluation-attempt-recorded`/`decision-recorded`/`decision-fact-invalidated`/`decision-revalidated`/`decision-current-view` là canonical contract concept ID** — đúng giá trị `id:` trong từng khối YAML dưới đây, tách biệt display name/`event_type`, cùng nguyên tắc mọi Domain Contract trước.

**Áp dụng ngay từ v0.1 mọi bài học đã trả giá xuyên suốt Package 0.2-B/C1/C2/C3** (đóng trước, không chờ review round phát hiện): opaque identity không derive từ scope; envelope binding cho `*FactInvalidated`; fold algorithm "visible-valid-head per slice" cho Current View; Current View KHÔNG BAO GIỜ authority; canonical policy identifier khai báo ĐÚNG MỘT NƠI, độc lập theo context.

**Phạm vi bounded tường minh:** KHÔNG author Risk/Execution Intent/Order/Fill/Position/Replay Event (Package 0.2-C5–C7). KHÔNG định nghĩa order type/limit price/stop price/exchange payload. KHÔNG định nghĩa position sizing/capital allocation/portfolio arbitration. KHÔNG xây dựng DSL/expression language/parser/rule graph/strategy compiler tổng quát — chỉ một **bounded typed rule-evidence shape** đủ cho walking skeleton (§5c). KHÔNG redefine Candle/Feature/Context contract — mọi input authoritative tham chiếu qua `event_record_ref` opaque. KHÔNG author UI copy/natural-language generation. KHÔNG sửa `strategy.md`/ADR-013/ADR-010/Constitution/C1-C3 semantics. KHÔNG author Risk rejection semantics. KHÔNG định nghĩa database transaction/outbox/message-broker technology (§16). KHÔNG general workflow/saga engine.

**v0.2 — bounded correction, đóng `C4-MAJ-01`/`C4-MAJ-02`/`C4-MAJ-03`/`C4-MAJ-04`/`C4-MAJ-05`/`C4-MAJ-06` (consolidated Review A + Independent Review B findings):** (a) `C4-MAJ-01` — bỏ `trade_intent_outcome`/`SUPPRESSED_DUPLICATE` khỏi Decision evidence; duplicate handling nay là hành vi idempotency (§13 `decision_computation_idempotency_policy`), KHÔNG phải Decision result. (b) `C4-MAJ-02` — Decision KHÔNG còn tự tuyên bố "đã issue Trade Intent"; derivation Decision→Trade Intent idempotent qua `originating_decision_id` là unique key, canonical `trade_intent_derivation_idempotency_policy` (trade-intent.md §10). (c) `C4-MAJ-03` — thêm correction lineage cho `DecisionRecorded`: `decision_id` vẫn bất biến/globally-unique/KHÔNG tái sử dụng cho fact khác, nhưng một logical computation key (`strategy_instance_id`, `decision_context_cursor`) nay CÓ THỂ có nhiều `DecisionRecorded` theo thời gian qua invalidate + same-key replacement (decision_id MỚI, `supersedes_fact_ref` trỏ fact bị invalidate) — visible-valid-head per logical key (§8 fold algorithm mới). (d) `C4-MAJ-04` — thêm `DecisionEvaluationAttempt`/`DecisionEvaluationAttemptRecorded` (§2/§4) — MỌI lần thử đánh giá (kể cả ineligible/missing-input/failed) nay là một authoritative fact, KHÔNG còn represented bằng absence. (e) `C4-MAJ-05` — thêm invariant thứ tự effective/recorded-time giữa Trade Intent và Decision gốc (trade-intent.md §3/§9). (f) `C4-MAJ-06` — thêm `eligible_for_new_risk_evaluation` origin-validity rule (trade-intent.md §6a). Bounded — không đổi bốn trục evidence độc lập, bounded EMA rule evidence, Configuration Version ownership của rule parameter, structured explanation, `decision_time`/`decision_context_cursor` (ADR-010), input visibility/no-look-ahead, Trade Intent Account/TradableListing equivalence, Trade Intent lifecycle ISSUED/WITHDRAWN/EXPIRED, Current View non-authority, C1–C3 semantics, C4/C5 boundary.

**v0.3 — micro-correction, đóng `C4-DELTA-MAJ-01`/`C4-DELTA-MAJ-02` (consolidated Review A + Independent Review B findings trên baseline v0.2):** (a) `C4-DELTA-MAJ-01` — loại bỏ `resulting_decision_id` khỏi `DecisionEvaluationAttempt` entity schema/`DecisionEvaluationAttemptRecorded` payload/invariants/canonical policy/scenario — attempt DECIDED và DecisionRecorded nay liên hệ MỘT CHIỀU DUY NHẤT (Attempt ghi trước, `DecisionRecorded.causation_refs` trỏ ngược lại attempt), loại bỏ circular append-order dependency; query chiều ngược (Decision nào ứng với một attempt) resolve qua cơ chế ĐÃ CÓ (`GetDecisionForComputation` §8, hoặc reverse `causation_refs` lookup) — KHÔNG event/field liên kết mới. (b) `C4-DELTA-MAJ-02` — tách `evaluation_attempt_id` (identity cá nhân MỘT lần thử) khỏi logical computation key (`strategy_instance_id`, `decision_context_cursor` — nhóm NHIỀU attempt); idempotency nay scoped theo `evaluation_attempt_id` (canonical `decision_evaluation_attempt_idempotency_policy: STABLE_ATTEMPT_ID_SAME_PAYLOAD_IS_IDEMPOTENT`, đối xứng `instrument.md` §17), KHÔNG còn theo logical key — nhiều attempt (outcome khác nhau, ví dụ FAILED_BEFORE_EVALUATION rồi DECIDED) CÙNG một logical key nay hợp lệ; nhiều attempt DECIDED cùng key PHẢI resolve/reuse cùng một Decision qua `decision_computation_idempotency_policy` (tầng Decision, không phải tầng Attempt) — không tạo hai Decision head trừ khi correction lineage (§11) cho phép. Bounded — không đổi Decision correction lineage, `decision_id` semantics, `decision_time`, `decision_context_cursor`, no-look-ahead, bốn trục evidence, bounded EMA rule evidence, explanation, Decision-to-Trade-Intent derivation, Trade Intent time ordering, `eligible_for_new_risk_evaluation`, Trade Intent lifecycle, C1–C3 semantics, C4/C5 boundary. KHÔNG thêm attempt lifecycle/scheduler/retry workflow.

**VIEW-003 Replay Parity Semantic Clarification — Consolidated Stable (§9a lifecycle, Product Owner decision, verbatim: "APPROVE CONSOLIDATION"; date 2026-08-06, giờ không được chỉ định trong yêu cầu transaction) — mechanical lifecycle transaction, `version: "0.5"` UNCHANGED.** Review evidence: Review A (REVISE trên §9a v0.4, đóng bốn finding `P16-V003-A-MAJ-01`/`P16-V003-A-MAJ-02`/`P16-V003-A-MAJ-03`/`P16-V003-A-MIN-01` qua v0.5) → bounded correction verification: CLEAN → Independent Review B: CLEAN → Product Owner consolidation decision. `package/section lifecycle: candidate → Consolidated Stable` — KHÔNG semantic content nào đổi: Canonical Decision Semantic Representation (§9a.1)/Digest (§9a.2) field set, chín pinned axis (§9a.4), outcome model MATCH/MISMATCH/INDETERMINATE (§9a.6), authority boundary (parity KHÔNG tạo/approve/replace/invalidate Decision), ba trục định danh độc lập (`decision_contract_document_version`/`decision_semantic_representation_definition_id`+`version`/`decision_semantic_digest_definition_id`+`version`, §9a.5b) — byte-identical, CHỈ lifecycle-state label thay đổi. §1–§8/§10–§18 KHÔNG đổi (byte-identical). decision.md v0.3 `Consolidated Stable` (Package 0.2-C4) VẪN nguyên vẹn, KHÔNG re-open. `status: Draft`, `approved_by: null`, `approved_at: null` KHÔNG đổi. `NAV-003`/`VIEW-002` VẪN unresolved; Package 1.6 lifecycle KHÔNG đổi bởi transaction này. KHÔNG owner/module/package/dependency edge/API path/ADR/implementation authority nào được chọn tại transaction này.

**v0.4 — CANDIDATE semantic clarification (2026-08-06) — HISTORICAL, superseded bởi VIEW-003 Consolidated Stable banner trên; tại thời điểm authoring: KHÔNG Approved/Consolidated, pending Review A/Independent Review B/Product Owner decision — Product Owner authorized (timestamp 2026-08-06T09:21:00+07:00) bounded source-semantics clarification cho VIEW-003 replay parity verification:** thêm §9a MỚI — **Canonical Decision Semantic Representation** (và, khi cần một giá trị đơn: **Canonical Decision Semantic Digest**) — lần đầu tiên cung cấp định nghĩa CỤ THỂ cho thuật ngữ `canonical semantic-decision hash` (product-requirement.md PR-010/PR-019, use-case-workflow.md UC-005, ux-blueprint.md VIEW-003) mà trước v0.4 CHỈ là một pointer chưa resolve ("định nghĩa bởi Decision Contract authoritative" nhưng KHÔNG field-list nào tồn tại tại decision.md v0.1–v0.3). §9a derive field CHỈ từ §5b/§5c/§5d/§5e ĐÃ established (KHÔNG field Decision mới nào invent); định nghĩa recorded-side selection correction-aware qua §8 fold algorithm (KHÔNG redefine); định nghĩa recomputed-side constraint (non-authoritative, KHÔNG append/replace/correct Decision, KHÔNG invoke Decision Authority acceptance, KHÔNG tiêu thụ downstream Risk/Execution outcome); định nghĩa outcome model BA giá trị workflow-visible non-authoritative (MATCH/MISMATCH/INDETERMINATE — INDETERMINATE MỚI, trước v0.3 CHỈ có MATCH/MISMATCH tại UC-005/ux-blueprint.md); xác nhận authority boundary (parity KHÔNG tạo/approve/replace/invalidate Decision). KHÔNG chọn computation owner/module/package assignment/dependency edge/ADR/API exposure/UX implementation — TẤT CẢ VẪN unresolved, ngoài phạm vi transaction này (xem package-1.6-upstream-resolution-exploration.md v0.2, KHÔNG sửa). Baseline v0.3 Consolidated Stable (Package 0.2-C4) VẪN controlling cho tới khi §9a này qua đúng review cycle riêng biệt. Bounded — KHÔNG đổi §1–§8/§10–§18 nội dung hiện có, KHÔNG redefine fold algorithm/correction lineage/canonical policy identifier đã pin, KHÔNG đổi Decision-to-Trade-Intent cardinality, KHÔNG chọn hash algorithm/serialization technology.

**v0.5 — CANDIDATE bounded correction (2026-08-06) — HISTORICAL, superseded bởi VIEW-003 Consolidated Stable banner trên; tại thời điểm authoring: KHÔNG Approved/Consolidated, pending bounded verification/Independent Review B/Product Owner decision — đóng bốn Review A finding trên §9a v0.4 (`P16-V003-A-MAJ-01`, `P16-V003-A-MAJ-02`, `P16-V003-A-MAJ-03`, `P16-V003-A-MIN-01`):** (1) `P16-V003-A-MAJ-01` — Implementation/provenance equivalence: `decision_implementation_version` (plugin_version_ref + package_build_artifact_ref) VẪN loại trừ khỏi Representation (§9a.1, ý nghĩa semantic tách biệt khỏi implementation identity KHÔNG đổi), NHƯNG nay BẮT BUỘC (KHÔNG optional) tại parity result envelope khi recorded Decision ĐÃ establish các reference đó; recomputation PHẢI dùng ĐÚNG CÙNG pinned implementation identity với recorded side (§9a.4); nếu required reference không resolve/reproduce được ở một trong hai phía → INDETERMINATE (§9a.6); output/Representation bằng nhau dưới implementation identity KHÁC NHAU KHÔNG đủ để tuyên bố một deterministic parity verification. (2) `P16-V003-A-MAJ-02` — Digest qualification: sửa tuyên bố sai "Representation và Digest logic tương đương chỉ vì digest derivation deterministic" — Representation (structured, §9a.1) LÀ semantic comparison authority; Digest (§9a.2) CHỈ LÀ compact derived evidence, đòi hỏi CHÍNH NÓ một digest-definition identity/version riêng (`decision_semantic_digest_definition_id`/`decision_semantic_digest_definition_version`, §9a.5b) ràng buộc canonical encoding/field ordering/absent-vs-null treatment/digest algorithm qua một technical contract quản trị riêng (KHÔNG chọn công nghệ tại transaction này); cho tới khi contract đó tồn tại, so sánh Representation trực tiếp LÀ cơ sở hợp lệ DUY NHẤT cho MATCH; digest equality ĐƠN ĐỘC KHÔNG được thiết lập MATCH; digest mismatch CHỈ được thiết lập MISMATCH khi cả hai digest cùng derive dưới CÙNG một valid digest-definition version TỪ Representation đã resolve thành công; digest-definition unresolved/incompatible → INDETERMINATE. (3) `P16-V003-A-MAJ-03` — Independent definition identity: thay thế việc dùng lẫn version của tài liệu decision.md làm representation-definition identity bằng BA trục độc lập tường minh (§9a.5b) — `decision_contract_document_version` (version của decision.md NHƯ một tài liệu, KHÔNG phải comparison identity), `decision_semantic_representation_definition_id`/`decision_semantic_representation_definition_version` (identity/version ĐỘC LẬP của field-set + comparison semantics, bất biến sau khi reference, KHÔNG tái sử dụng ID, persistently resolvable, verifiable content identity — Chapter 8 §8.1.1), `decision_semantic_digest_definition_id`/`decision_semantic_digest_definition_version` (CÓ THỂ VẪN unresolved/chưa established tại candidate này). Một sửa đổi decision.md KHÔNG liên quan (vd. sửa lỗi chính tả nơi khác) KHÔNG tự động bump representation-definition version; ngược lại, một thay đổi field-set/comparison-semantics (như chính correction §9a v0.5 này) ĐÒI HỎI representation-definition version mới — `decision_semantic_representation_definition_id: "DSR-001"`, `decision_semantic_representation_definition_version: "2"` (CANDIDATE, bump từ giá trị ngầm định "1" tại v0.4 — nơi định danh này CHƯA tách biệt tường minh khỏi document version, nay tách biệt lần đầu). (4) `P16-V003-A-MIN-01` — Complete pinned-axis wording: mọi câu "cùng pinned version axis" (§9a.1/§9a.3/§9a.4/§9a.5/§9a.6) nay liệt kê ĐẦY ĐỦ chín trục — Strategy Instance; Strategy Definition Version; Configuration Version; Decision rule identity/version; Decision implementation provenance (khi có); canonical Replay Cursor; input evidence reference; semantic-representation-definition version; digest-definition version (khi dùng digest) — bất kỳ trục bắt buộc nào không resolve nhất quán → INDETERMINATE. KHÔNG redesign VIEW-003; KHÔNG chọn parity computation owner/module/package assignment/dependency edge/ADR; KHÔNG sửa architecture artifact/registry/system decomposition/Package 1.6; KHÔNG resolve NAV-003/VIEW-002; KHÔNG authorize implementation/Gate 2/Phase 2/LIVE. Baseline §9a v0.4 (CANDIDATE, chưa Consolidated) và decision.md v0.3 Consolidated Stable (Package 0.2-C4) đều giữ nguyên là lịch sử preserved — v0.5 CHỈ correct nội dung §9a candidate, KHÔNG retroactively claim Consolidated.

## 1. Decision — `kind: entity`

```yaml
id: decision
kind: entity
capability_id: decision-management
domain_context_id: strategy-decision
description: >
  Bản ghi authoritative của MỘT lần Strategy Instance đánh giá deterministic tại một
  decision_context_cursor cụ thể (ADR-010 §2.3, Chapter 8 §8.4). MỘT DecisionRecorded fact là
  BẤT BIẾN sau khi ghi — mọi field (strategy evidence, rule evidence, input evidence, result) cố
  định tại thời điểm ghi. decision_id BẤT BIẾN, globally unique, KHÔNG BAO GIỜ tái sử dụng cho
  fact khác — kể cả một correction replacement mang decision_id HOÀN TOÀN MỚI (v0.2, đóng
  C4-MAJ-03). Correction lineage (§11) cho phép MỘT logical computation key (strategy_instance_id,
  decision_context_cursor) có NHIỀU DecisionRecorded theo thời gian: fact SAI invalidate qua
  DecisionFactInvalidated (§6), fact THAY THẾ mang decision_id MỚI + supersedes_fact_ref trỏ fact
  bị invalidate, CÙNG logical key. Tại một cursor, đúng MỘT visible valid head cho mỗi logical key
  (§8 fold algorithm). Revalidation (§7, ADR-010 §2.6/Chapter 8 §8.4.1) là một fact VẬN HÀNH riêng,
  KHÔNG phải correction.
invariants:
  - "decision_id là opaque, globally unique trong toàn Ride, gán tại DecisionRecorded — KHÔNG derive/resolve từ strategy_instance_id, decision_context_cursor, hay bất kỳ field nội dung nào. Bất biến, KHÔNG tái sử dụng cho subject khác (Chapter 6 §6.1) — kể cả correction replacement (§11)."
  - "MỘT Decision thuộc ĐÚNG MỘT Strategy Instance (`strategy_instance_id`, ref: strategy) — không multi-instance Decision, không aggregate nhiều Instance."
  - "MỘT Decision đánh giá ĐÚNG MỘT rule invocation — `decision_rule_ref` + rule evidence (§5c) pin một lần đánh giá cụ thể, KHÔNG batch nhiều rule."
  - "**v0.2 (đóng C4-MAJ-03):** Logical computation key = (strategy_instance_id, decision_context_cursor) — tại một cursor cho trước, đúng MỘT visible valid head DecisionRecorded cho mỗi key (§8 fold algorithm). MỘT key CÓ THỂ có nhiều DecisionRecorded lịch sử qua correction lineage (§11) — mỗi fact có decision_id RIÊNG, liên kết qua supersedes_fact_ref."
  - "**v0.2 (đóng C4-MAJ-01/02):** Retry của MỘT logical computation attempt (chưa từng invalidate) với evidence bundle giống hệt PHẢI idempotent no-op — trả về decision_id/evaluation_attempt_id đã tồn tại, KHÔNG tạo bản ghi thứ hai (§13 `decision_computation_idempotency_policy`, §2 DecisionEvaluationAttempt). Retry với evidence khác (chưa invalidate predecessor) PHẢI reject tường minh (deterministic conflict) — KHÔNG BAO GIỜ tạo hai DecisionRecorded VALID cùng key với evidence khác nhau MÀ KHÔNG qua correction lineage tường minh (§11)."
  - "Decision KHÔNG mutable dưới bất kỳ hình thức nào — không PATCH event, không revision event tại chỗ. Historical Decision (kể cả đã bị supersede) vẫn resolvable sau khi Strategy Instance pause/retire (strategy.md §5/§7) — Decision là bằng chứng lịch sử độc lập lifecycle hiện tại của Instance (Chapter 9 §9.3)."
schema:
  decision_id: {type: string, required: true, description: "opaque, stable — xem invariants"}
  strategy_instance_id: {type: string, required: true, ref: strategy, description: "đúng một Strategy Instance"}
  decision_context_cursor: {type: object, required: true, description: "Replay Cursor hợp lệ (ADR-010 §2.3, Chapter 8 §8.5.1) — xem §3"}
  decision_time: {type: timestamp, required: true, description: "effective-axis value của Decision (ADR-010 §2.2, THAY effective_time — Chapter 8 §8.2.1)"}
  decision_rule_ref: {type: string, required: true, description: "PHẢI khớp đúng decision_rule_ref của strategy_definition_version_id đang pin (strategy.md §1) — xem §5c"}
  result: {type: enum, values: [LONG, SHORT, NO_ACTION], required: true, description: "xem §5e"}
  supersedes_fact_ref: {type: event_record_ref, required: false, description: "v0.2, đóng C4-MAJ-03 — VẮNG MẶT cho Decision gốc; BẮT BUỘC cho correction replacement, xem §11"}
events_emitted: [DecisionRecorded, DecisionFactInvalidated, DecisionRevalidated]
events_consumed: []
commands: []
queries: []
```

## 2. DecisionEvaluationAttempt — `kind: entity` (v0.2, đóng `C4-MAJ-04`; v0.3 corrected `C4-DELTA-MAJ-01`/`C4-DELTA-MAJ-02`)

**Vai trò:** bản ghi authoritative của MỘT LẦN THỬ Strategy Instance đánh giá — KHÔNG PHÂN BIỆT kết quả có dẫn tới Decision hay không. **Mọi lần thử ĐỀU được ghi nhận — KHÔNG BAO GIỜ represented bằng event absence.** Đây là subject MỚI, RIÊNG BIỆT khỏi Decision — một attempt outcome `DECIDED` chứng minh rule đã đánh giá thành công VÀ một Decision append được kỳ vọng theo sau (§4 §5 — one-way sequence, KHÔNG forward reference); ba outcome còn lại (`INELIGIBLE`/`INPUT_UNAVAILABLE`/`FAILED_BEFORE_EVALUATION`) KHÔNG dẫn tới Decision nào.

**v0.3 (đóng `C4-DELTA-MAJ-02`) — hai identity KHÁC NHAU, KHÔNG gộp:**

```text
evaluation_attempt_id:      định danh MỘT LẦN THỬ cá nhân — opaque, globally unique, per attempt
logical computation key:    (strategy_instance_id, decision_context_cursor) — nhóm NHIỀU attempt
                             CÓ THỂ chia sẻ CÙNG key, mỗi attempt có evaluation_attempt_id RIÊNG
```

MỘT logical computation key CÓ THỂ có NHIỀU `DecisionEvaluationAttemptRecorded` theo thời gian, KỂ CẢ với `attempt_outcome` KHÁC NHAU (ví dụ `FAILED_BEFORE_EVALUATION` rồi sau đó retry thành công `DECIDED` tại CÙNG cursor) — điều này KHÔNG phải data-integrity violation.

```yaml
id: decision-evaluation-attempt
kind: entity
capability_id: decision-management
domain_context_id: strategy-decision
description: >
  Bản ghi authoritative, BẤT BIẾN, của MỘT lần thử đánh giá — độc lập việc lần thử đó có dẫn tới
  Decision hay không. Thay thế hoàn toàn cơ chế "no event when ineligible/missing-input" của v0.1 —
  mọi outcome (DECIDED/INELIGIBLE/INPUT_UNAVAILABLE/FAILED_BEFORE_EVALUATION) đều là một
  DecisionEvaluationAttemptRecorded fact tường minh (§4). v0.3: evaluation_attempt_id (identity cá
  nhân) và logical computation key (strategy_instance_id, decision_context_cursor — nhóm nhiều
  attempt) là HAI khái niệm tách biệt (đóng C4-DELTA-MAJ-02).
invariants:
  - "evaluation_attempt_id là opaque, globally unique trong toàn Ride, gán tại DecisionEvaluationAttemptRecorded — KHÔNG derive từ strategy_instance_id/decision_context_cursor. Bất biến, KHÔNG tái sử dụng."
  - "**v0.3 (đóng C4-DELTA-MAJ-02):** Idempotency áp dụng theo TỪNG evaluation_attempt_id — retry CÙNG evaluation_attempt_id + CÙNG payload → idempotent no-op (trả evaluation_attempt_id đã tồn tại); CÙNG evaluation_attempt_id + payload KHÁC → deterministic conflict, reject (§13 `decision_evaluation_attempt_idempotency_policy`, đối xứng `instrument.md` §17 `activation_request_idempotency_policy`)."
  - "**v0.3 (đóng C4-DELTA-MAJ-02):** Logical computation key (strategy_instance_id, decision_context_cursor) KHÔNG BẮT BUỘC unique — nhiều DecisionEvaluationAttemptRecorded (evaluation_attempt_id RIÊNG cho mỗi cái) CÓ THỂ tồn tại cùng key, KỂ CẢ với attempt_outcome khác nhau (ví dụ FAILED_BEFORE_EVALUATION rồi DECIDED). Đây KHÔNG phải data-integrity violation — cursor cố định chỉ đảm bảo tính deterministic của MỖI evaluation_attempt_id riêng lẻ khi retry đúng ID đó, KHÔNG áp đặt 'một outcome duy nhất cho cả key.'"
  - "**v0.3 (đóng C4-DELTA-MAJ-01):** attempt_outcome = DECIDED KHÔNG mang, KHÔNG yêu cầu resulting_decision_id — trường này ĐÃ BỊ LOẠI BỎ. Attempt DECIDED CHỈ chứng minh rule đã đánh giá thành công VÀ một DecisionRecorded append được kỳ vọng NGAY SAU (§4/§5, one-way sequence). Muốn biết Decision nào tương ứng một attempt DECIDED, PHẢI resolve TỪ authoritative Decision history — qua `GetDecisionForComputation(strategy_instance_id, decision_context_cursor, cursor)` (§8) HOẶC reverse-lookup DecisionRecorded có `causation_refs` chứa chính attempt event này — KHÔNG BAO GIỜ qua một field lưu sẵn trên Attempt."
  - "attempt_outcome ∈ {INELIGIBLE, INPUT_UNAVAILABLE, FAILED_BEFORE_EVALUATION}: KHÔNG Decision nào được tạo cho lần thử này. FAILED_BEFORE_EVALUATION tường minh RETRYABLE — một attempt DECIDED sau đó tại CÙNG logical key hoàn toàn hợp lệ (v0.3, đóng C4-DELTA-MAJ-02)."
  - "**v0.3 (đóng C4-DELTA-MAJ-02, Scenario 4):** khi một attempt_outcome = DECIDED được ghi tại một logical key ĐÃ CÓ một DecisionRecorded VALID (visible-valid-head, §8), attempt MỚI PHẢI resolve/reuse decision_id đã tồn tại đó (nếu evidence giống hệt — Decision-layer idempotency, §1/§13 `decision_computation_idempotency_policy`) hoặc deterministic conflict (nếu evidence khác) — TUYỆT ĐỐI KHÔNG được tạo decision_id thứ hai cho CÙNG key trừ khi decision_id đầu tiên ĐÃ invalidate VÀ correction lineage (§11) cho phép replacement. Nhiều attempt DECIDED (evaluation_attempt_id khác nhau) CÓ THỂ cùng trỏ về đúng MỘT Decision qua cơ chế idempotency này — KHÔNG BAO GIỜ tạo hai Decision head cho cùng logical key."
  - "DecisionEvaluationAttempt KHÔNG có correction lineage riêng, KHÔNG có lifecycle/state machine, KHÔNG có scheduler/retry workflow — retry đơn thuần là ghi một DecisionEvaluationAttemptRecorded MỚI (evaluation_attempt_id mới) tại cùng logical key, deferred §16."
schema:
  evaluation_attempt_id: {type: string, required: true, description: "opaque, stable, per-attempt identity — xem invariants"}
  strategy_instance_id: {type: string, required: true, ref: strategy}
  decision_context_cursor: {type: object, required: true, description: "cùng shape Decision (§3) — một phần logical computation key, KHÔNG phải unique key riêng của attempt"}
  attempt_outcome: {type: enum, values: [DECIDED, INELIGIBLE, INPUT_UNAVAILABLE, FAILED_BEFORE_EVALUATION], required: true}
  reason_code: {type: string, required: false, description: "BẮT BUỘC khi attempt_outcome != DECIDED; TUYỆT ĐỐI ABSENT khi DECIDED — xem §4 cho enum đóng"}
  checked_evidence_refs: {type: array, items: event_record_ref, required: false, description: "authoritative fact đã kiểm tra để xác định outcome — CÓ THỂ RỖNG khi outcome liên quan absence hoàn toàn của input, xem §4"}
events_emitted: [DecisionEvaluationAttemptRecorded]
events_consumed: []
commands: []
queries: []
```

## 3. Canonical event envelope — áp dụng cho mọi Decision/DecisionEvaluationAttempt event (§4–§7)

Mọi event trong tài liệu này là **authoritative event record** theo [Chapter 8 §8.2](../constitution/08-event-model.md) (Locked). Trường hợp `event_class: decision` (CHỈ `DecisionRecorded`, §5) áp dụng thêm cardinality riêng theo [Chapter 8 §8.2.1](../constitution/08-event-model.md)/[§8.4](../constitution/08-event-model.md); `DecisionEvaluationAttemptRecorded`/`DecisionFactInvalidated`/`DecisionRevalidated` KHÔNG thuộc `event_class: decision` — dùng envelope tiêu chuẩn.

```yaml
envelope:
  event_id: {cardinality: required}
  event_type: {cardinality: required}               # PAST_TENSE_UPPER_SNAKE (Chapter 3 §3.2)
  event_contract_ref: {cardinality: required}
  schema_version: {cardinality: required}
  recorded_time: {cardinality: required}             # khi Ride ghi nhận fact này
  subject_ref: {cardinality: "required — shape canonical, xem dưới. Trên DecisionFactInvalidated, PHẢI kế thừa nguyên vẹn từ fact đang bị invalidate."}
  stream_ref: {cardinality: required}                # Phase 1, chưa author
  sequence: {cardinality: required}
  producer_ref: {cardinality: required}              # Phase 1, chưa author
  correlation_id: {cardinality: "required khi computation thuộc một correlation flow tường minh (ví dụ chuỗi attempt→decision, hoặc chuỗi revalidation); optional khi độc lập"}
  causation_refs: {cardinality: "DecisionEvaluationAttemptRecorded: zero-or-more (Decision Engine internal computation trigger, Phase 1, chưa author). DecisionRecorded: KHÔNG BAO GIỜ rỗng — PHẢI chứa DecisionEvaluationAttemptRecorded tương ứng (§5), CỘNG DecisionFactInvalidated của predecessor nếu là correction replacement (§11). DecisionFactInvalidated/DecisionRevalidated: KHÔNG BAO GIỜ rỗng."}
  related_event_refs: {cardinality: "zero-to-many, non-causal — Chapter 8 §8.2.3."}
  effective_time: {cardinality: "PROHIBITED trên DecisionRecorded (event_class: decision — Chapter 8 §8.2.1, ADR-010 §2.2, thay bằng decision_time). REQUIRED trên DecisionEvaluationAttemptRecorded/DecisionFactInvalidated/DecisionRevalidated (không phải event_class: decision) — xem §4/§6/§7 cho giá trị chính xác."}
  decision_time: {cardinality: "REQUIRED trên DecisionRecorded — PROHIBITED trên mọi event khác (Chapter 8 §8.2.1). Effective-axis time value, ADR-010 §2.2 — semantic domain cụ thể xem §5."}
  decision_context_cursor: {cardinality: "REQUIRED (envelope-level, ADR-010) trên DecisionRecorded — PROHIBITED trên mọi event khác (Chapter 8 §8.2.1). Replay Cursor hợp lệ, xem shape dưới. DecisionEvaluationAttemptRecorded mang decision_context_cursor như PAYLOAD field thường (§4), KHÔNG phải envelope-level ADR-010 field — event_class khác nhau."}
  market_time: {cardinality: "PROHIBITED — Decision/DecisionEvaluationAttempt là computation authoritative, không phải quan sát trực tiếp venue (Chapter 5 §5.2)."}
  source_identity: {cardinality: "PROHIBITED — luôn phát sinh nội bộ từ Decision Engine (Phase 1, chưa author), KHÔNG BAO GIỜ từ external feed có khả năng retry/redelivery (Chapter 6 §6.6)."}

decision_context_cursor (shape, đúng canonical Replay Cursor — Chapter 8 §8.5.1, KHÔNG một schema gần giống):
  recorded_time: <timestamp>                          # required — knowledge boundary
  input_contract_ref: {contract_id: <string>, contract_version: <string>}   # required — versioned, immutable (§8.1.1)
  stream_registry_version: <string>                   # required
  lifecycle_frontier:                                  # required
    stream_id: <string>                                # canonical lifecycle stream
    position: {kind: <genesis | event>, sequence: <integer>}
  stream_positions: {<stream_id>: <sequence>, ...}     # required — map, mọi stream thuộc universe của cursor

subject_ref (Decision):
  context_id: strategy-decision
  subject_kind: entity
  subject_type: Decision
  subject_id: <decision_id — opaque, stable, xem §1>
  scope:
    strategy_instance_id: <string>

subject_ref (DecisionEvaluationAttempt, §2):
  context_id: strategy-decision
  subject_kind: entity
  subject_type: DecisionEvaluationAttempt
  subject_id: <evaluation_attempt_id — opaque, stable, xem §2>
  scope:
    strategy_instance_id: <string>

event_types:
  DecisionEvaluationAttemptRecorded: DECISION_EVALUATION_ATTEMPT_RECORDED
  DecisionRecorded: DECISION_RECORDED
  DecisionFactInvalidated: DECISION_FACT_INVALIDATED
  DecisionRevalidated: DECISION_REVALIDATED
```

`stream_ref`/`producer_ref`/registry-cụ-thể-sau-`decision_context_cursor` (Stream Registry/Input Contract implementation, canonical Audit Stream) — Phase 1, chưa tồn tại cụ thể. `decision_context_cursor` field SHAPE và cardinality/invariant (§8.5.1/§8.5.2) là BẮT BUỘC ngay từ v0.1 (ADR-010/Chapter 8 Approved/Locked, không thể defer field structure) — chỉ MECHANISM resolve (registry cụ thể) là Phase 1.

**Relational invariants bắt buộc trên `decision_context_cursor`** (Chapter 8 §8.5.2, tái khẳng định KHÔNG lặp lại toàn văn):
```text
cursor.recorded_time ≤ DecisionRecorded.recorded_time            (Cursor → Decision, §8.5.2)
input_event.recorded_time ≤ cursor.recorded_time                 (mọi input evidence event, §2.4 ADR-010)
lifecycle_event.recorded_time ≤ cursor.recorded_time              (Lifecycle → Cursor, §8.5.2)
cursor.stream_registry_version = registry version mà input_contract_ref pin  (Registry → Contract, §8.5.2)
```
Vi phạm bất kỳ điều nào → **invalid `decision_context_cursor`, DecisionRecorded PHẢI bị từ chối khi append** (Chapter 8 §8.5.1). Đây chính là cơ chế thực thi no-look-ahead (I-3) cho Decision.

## 4. `DecisionEvaluationAttemptRecorded` — `kind: event` (v0.2, đóng `C4-MAJ-04`)

Kế thừa envelope §3 (KHÔNG thuộc `event_class: decision`).

```yaml
id: decision-evaluation-attempt-recorded
kind: event
capability_id: decision-management
domain_context_id: strategy-decision
description: >
  Fact AUTHORITATIVE DUY NHẤT ghi nhận MỘT lần thử đánh giá — LUÔN LUÔN phát, bất kể outcome. Thay
  thế hoàn toàn precondition-absence policy của v0.1 (§5a). v0.3 (đóng C4-DELTA-MAJ-01): KHÔNG
  còn payload field `resulting_decision_id` — attempt DECIDED và DecisionRecorded liên hệ MỘT
  CHIỀU qua `causation_refs` của chính DecisionRecorded (§5), KHÔNG qua forward reference trên
  Attempt (tránh circular append-order dependency).
invariants:
  - "payload.evaluation_attempt_id PHẢI khớp đúng subject_ref.subject_id."
  - "envelope.effective_time = decision_context_cursor.recorded_time (payload) — mặc định, trừ khi backfill lịch sử tường minh pin giá trị khác."
  - "attempt_outcome = DECIDED: reason_code/checked_evidence_refs TUYỆT ĐỐI ABSENT (evidence đầy đủ sống trên DecisionRecorded, §5). **v0.3 (đóng C4-DELTA-MAJ-01):** KHÔNG payload field nào trỏ tới Decision — attempt này CHỈ chứng minh 'rule đã đánh giá thành công, một Decision append được kỳ vọng ngay sau'; DecisionRecorded (§5) chịu trách nhiệm trỏ NGƯỢC LẠI attempt này qua `causation_refs` (one-way sequence: Attempt DECIDED ghi TRƯỚC, DecisionRecorded ghi SAU và tham chiếu attempt qua causation_refs — KHÔNG BAO GIỜ ngược lại)."
  - "attempt_outcome = INELIGIBLE: reason_code BẮT BUỘC, MỘT trong {STRATEGY_INSTANCE_NOT_ACTIVE, DEFINITION_VERSION_NOT_VALID, ACCOUNT_NOT_ACTIVE, EVIDENCE_AXIS_UNRESOLVABLE, INSTRUMENT_SELECTION_INELIGIBLE} (map trực tiếp năm điều kiện có thể fail của strategy.md §9a); checked_evidence_refs khuyến nghị trỏ fact strategy.md/account.md xác nhận điều kiện fail."
  - "attempt_outcome = INPUT_UNAVAILABLE: reason_code BẮT BUỘC, MỘT trong {REQUIRED_PRICE_INPUT_MISSING_OR_PENDING, REQUIRED_REFERENCE_INPUT_MISSING_OR_PENDING}; checked_evidence_refs CÓ THỂ RỖNG khi input hoàn toàn absent (không có fact nào để reference)."
  - "attempt_outcome = FAILED_BEFORE_EVALUATION: reason_code = ENGINE_COMPUTATION_BOUNDARY_ERROR (v0.1 CHỈ một giá trị — KHÔNG model broad runtime exception taxonomy/observability infrastructure, deferred §16); checked_evidence_refs thường rỗng. **v0.3 (đóng C4-DELTA-MAJ-02):** tường minh RETRYABLE — một DecisionEvaluationAttemptRecorded MỚI (evaluation_attempt_id khác) tại CÙNG logical computation key sau đó là hợp lệ, KHÔNG bị coi là mâu thuẫn với attempt này."
  - "**v0.3 (đóng C4-DELTA-MAJ-02):** Idempotency scoped theo TỪNG evaluation_attempt_id (§2, §13 `decision_evaluation_attempt_idempotency_policy`) — KHÔNG theo logical computation key. Nhiều DecisionEvaluationAttemptRecorded (evaluation_attempt_id RIÊNG) CÓ THỂ tồn tại cùng (strategy_instance_id, decision_context_cursor), KỂ CẢ với attempt_outcome khác nhau — KHÔNG phải data-integrity violation."
  - "No-look-ahead: mọi checked_evidence_refs PHẢI thỏa fact.recorded_time ≤ decision_context_cursor.recorded_time (đối xứng §5d)."
payload:
  evaluation_attempt_id: {type: string, required: true}
  strategy_instance_id: {type: string, required: true}
  decision_context_cursor: {type: object, required: true, description: "cùng shape §3 — payload field, KHÔNG phải envelope-level ADR-010 field (event này không thuộc event_class: decision)"}
  attempt_outcome: {type: enum, values: [DECIDED, INELIGIBLE, INPUT_UNAVAILABLE, FAILED_BEFORE_EVALUATION], required: true}
  reason_code: {type: enum, values: [STRATEGY_INSTANCE_NOT_ACTIVE, DEFINITION_VERSION_NOT_VALID, ACCOUNT_NOT_ACTIVE, EVIDENCE_AXIS_UNRESOLVABLE, INSTRUMENT_SELECTION_INELIGIBLE, REQUIRED_PRICE_INPUT_MISSING_OR_PENDING, REQUIRED_REFERENCE_INPUT_MISSING_OR_PENDING, ENGINE_COMPUTATION_BOUNDARY_ERROR], required: false}
  checked_evidence_refs: {type: array, items: event_record_ref, required: false}
```

**Attempt→Decision query (non-authoritative convenience, KHÔNG cần linking event mới, đóng `C4-DELTA-MAJ-01`):** cho một attempt DECIDED, resolve Decision tương ứng qua HAI cách tương đương — (a) `GetDecisionForComputation(strategy_instance_id, decision_context_cursor, cursor)` (§8), cùng `strategy_instance_id`/`decision_context_cursor` với attempt; hoặc (b) reverse-lookup trực tiếp trên authoritative DecisionRecorded stream cho fact có `causation_refs` chứa chính `event_record_ref` của attempt này. Cả hai đều dùng field/cơ chế ĐÃ CÓ SẴN (`causation_refs`, logical computation key) — KHÔNG tạo event/field liên kết mới.

## 5. `DecisionRecorded` — `kind: event` (`event_class: decision`)

Kế thừa envelope §3 CỘNG `decision_time`/`decision_context_cursor` (envelope-level) bắt buộc, `effective_time`/`market_time`/`source_identity` cấm. Payload đặc thù:

```yaml
id: decision-recorded
kind: event
capability_id: decision-management
domain_context_id: strategy-decision
description: >
  Fact AUTHORITATIVE cho một lần Strategy Instance đánh giá deterministic — thiết lập TOÀN BỘ nội
  dung (chín-field strategy evidence tại cursor, rule evidence, input evidence, result) cùng lúc,
  BẤT BIẾN. CHỈ được phát khi DecisionEvaluationAttemptRecorded (§4) tương ứng có attempt_outcome =
  DECIDED (§5a). v0.2 (đóng C4-MAJ-01): KHÔNG còn field trade_intent_outcome — Decision KHÔNG tự
  tuyên bố đã issue Trade Intent (xem §10, trade-intent.md §10).
invariants:
  - "payload.decision_id PHẢI khớp đúng subject_ref.subject_id VÀ payload.strategy_instance_id PHẢI khớp đúng subject_ref.scope.strategy_instance_id."
  - "envelope.decision_time = thời điểm domain Decision có hiệu lực — mặc định bằng decision_context_cursor.recorded_time trừ khi backfill lịch sử tường minh pin giá trị khác."
  - "causation_refs PHẢI chứa DecisionEvaluationAttemptRecorded (§4) tương ứng, attempt_outcome = DECIDED, cùng strategy_instance_id/decision_context_cursor — chứng minh attempt đã ghi nhận DECIDED TRƯỚC khi Decision này được tạo. Đây là quan hệ MỘT CHIỀU (v0.3, đóng C4-DELTA-MAJ-01): attempt KHÔNG mang bất kỳ tham chiếu nào tới Decision (không resulting_decision_id) — chỉ Decision mới trỏ ngược lại attempt, loại bỏ hoàn toàn phụ thuộc vòng (circular append-order dependency) giữa hai event."
  - "**v0.3 (đóng C4-DELTA-MAJ-02, Scenario 4):** nếu logical computation key (strategy_instance_id, decision_context_cursor) ĐÃ CÓ một DecisionRecorded VALID (visible-valid-head, §8) tại thời điểm ghi, DecisionRecorded MỚI PHẢI resolve/reuse decision_id đã tồn tại (evidence giống hệt — §1 idempotency) HOẶC bị reject (evidence khác, chưa invalidate predecessor) — TUYỆT ĐỐI KHÔNG tạo decision_id thứ hai cho CÙNG key trừ khi predecessor ĐÃ invalidate VÀ correction lineage (§11) cho phép. Nhiều attempt DECIDED (evaluation_attempt_id khác nhau, §2) tại cùng key CÓ THỂ cùng dẫn tới đúng MỘT Decision qua cơ chế này."
  - "TẤT CẢ chín field strategy evidence (§5b) PHẢI resolve deterministic từ authoritative Strategy/Account/Instrument/Venue event stream TẠI ĐÚNG decision_context_cursor — KHÔNG dùng StrategyInstanceCurrentView/AccountCurrentView/InstrumentCurrentView/VenueCurrentView/TradableListingCurrentView latest-state (strategy.md §9a/§10, account.md §13, instrument.md §7/§15)."
```

**§5a — Precondition: DecisionEvaluationAttempt DECIDED (thay hoàn toàn absence-policy v0.1, đóng `C4-MAJ-04`).** DecisionRecorded CHỈ được phát SAU KHI một `DecisionEvaluationAttemptRecorded` (§4) đã ghi nhận `attempt_outcome = DECIDED` cho cùng logical computation key:

```text
1. eligible_for_new_computation(strategy_instance_id, decision_context_cursor) == true   (strategy.md §9a, sáu điều kiện)
2. Mọi required input evidence (§5d) VISIBLE và resolvable TẠI decision_context_cursor
→ NẾU CẢ HAI thỏa: DecisionEvaluationAttemptRecorded(attempt_outcome=DECIDED) ghi trước, RỒI DecisionRecorded phát — result (§5e) phản ánh rule evaluation THẬT.
→ NẾU (1) false: DecisionEvaluationAttemptRecorded(attempt_outcome=INELIGIBLE) ghi — KHÔNG DecisionRecorded nào phát.
→ NẾU (2) false: DecisionEvaluationAttemptRecorded(attempt_outcome=INPUT_UNAVAILABLE) ghi — KHÔNG DecisionRecorded nào phát.
→ NẾU lỗi kỹ thuật/domain boundary xảy ra TRƯỚC KHI đánh giá được cả (1) lẫn (2): DecisionEvaluationAttemptRecorded(attempt_outcome=FAILED_BEFORE_EVALUATION) ghi — KHÔNG DecisionRecorded nào phát.
```

**Bốn trường hợp trên PHÂN BIỆT tường minh, MỌI trường hợp ĐỀU là một fact THẬT (§4) — KHÔNG còn absence-based distinguishing (v0.2, đóng C4-MAJ-04):** `DECIDED` (dẫn Decision, result LONG/SHORT/NO_ACTION) ≠ `INELIGIBLE` (strategy.md §9a fail, reason_code cụ thể) ≠ `INPUT_UNAVAILABLE` (input missing/pending, reason_code cụ thể) ≠ `FAILED_BEFORE_EVALUATION` (technical/domain boundary, KHÔNG broad exception telemetry).

**§5b — Strategy evidence (chín field, PIN tại decision_context_cursor, COPY làm scalar bất biến — đúng I-1: "Model/strategy version + strategy instance ID; configuration version; code/build version" PHẢI frozen tại decision time):**

```yaml
strategy_evidence:
  strategy_definition_id: {type: string, required: true, description: "strategy.md §10"}
  strategy_definition_version_id: {type: string, required: true, description: "exact immutable pin, KHÔNG BAO GIỜ 'latest' — ADR-013 §2.3"}
  plugin_version_ref: {type: string, required: true, description: "trục 2/4 — strategy.md §11"}
  configuration_version_ref: {type: string, required: true, description: "trục 3/4 — strategy.md §11"}
  package_build_artifact_ref: {type: string, required: true, description: "trục 4/4 — exact executable identity đang chạy, ADR-013 §2.5; hai executable khác bytes PHẢI khác giá trị này (Scenario 7-đối-ứng-F, §18)"}
  account_id: {type: string, required: true, ref: account, description: "đúng một Account, strategy.md §5"}
  environment: {type: enum, values: [PAPER, LIVE], required: true, description: "resolve qua account_id TẠI cursor — KHÔNG dùng AccountCurrentView (account.md §13)"}
  instrument_selection_ref:
    instrument_id: {type: string, required: true}
    venue_id: {type: string, required: true}
    listing_id: {type: string, required: true}
```

**Invariant bổ sung:** bốn trục evidence (`strategy_definition_version_id`/`plugin_version_ref`/`configuration_version_ref`/`package_build_artifact_ref`) PHẢI persistently resolvable TẠI cursor (Chapter 8 §8.1.1 mục 4, strategy.md §9a/§11) — nếu KHÔNG, DecisionEvaluationAttemptRecorded ghi `attempt_outcome=INELIGIBLE`, `reason_code=EVIDENCE_AXIS_UNRESOLVABLE` (§4), KHÔNG DecisionRecorded nào được phát.

**§5c — Rule evidence (bounded typed rule-reference, KHÔNG DSL/parser/rule graph):**

```yaml
rule_evidence:
  decision_rule_ref: {type: string, required: true, description: "PHẢI khớp đúng decision_rule_ref của strategy_definition_version_id đang pin (strategy.md §1) — semantic rule identity thuộc Strategy Definition Version, KHÔNG thuộc Decision"}
  rule_family: {type: enum, values: [PRICE_CROSSES_REFERENCE_SERIES], required: true, description: "v0.1: đúng một giá trị — bounded, mở rộng sau bằng giá trị enum MỚI khi có rule family khác, KHÔNG redesign shape hiện có"}
  price_source: {type: enum, values: [CLOSE, HIGH, LOW, OPEN], required: true, description: "copied scalar, nguồn authoritative = configuration_version_ref (§5b) — KHÔNG hardcode trên Strategy Definition Version trừ khi rule coi giá trị này là fixed business semantics"}
  reference_series_type: {type: enum, values: [EMA], required: true, description: "copied scalar — nguồn authoritative = configuration_version_ref"}
  reference_series_period: {type: integer, required: true, description: "copied scalar (ví dụ 50 hoặc 100) — nguồn authoritative = configuration_version_ref, KHÔNG trên Strategy Definition Version"}
  crossing_policy: {type: enum, values: [STRICT_CROSS, SIMPLY_ABOVE], required: true, description: "copied scalar — nguồn authoritative = configuration_version_ref. STRICT_CROSS: previous_condition_met AND current_condition_met. SIMPLY_ABOVE: chỉ current_condition_met."}
  evaluation_timing: {type: enum, values: [CANDLE_CLOSE, INTRABAR], required: true, description: "v0.1 CHỈ hỗ trợ CANDLE_CLOSE — INTRABAR reserved, PROHIBITED dùng thực tế (§16)"}
  previous_price_value: {type: decimal, required: true}
  previous_reference_value: {type: decimal, required: true}
  current_price_value: {type: decimal, required: true}
  current_reference_value: {type: decimal, required: true}
  previous_condition_met: {type: boolean, required: true, description: "previous_price_value <= previous_reference_value"}
  current_condition_met: {type: boolean, required: true, description: "current_price_value > current_reference_value"}
```

**Invariant:** `rule_family = PRICE_CROSSES_REFERENCE_SERIES` PHẢI đi kèm CẢ chín sub-field trên. Với `evaluation_timing = CANDLE_CLOSE`, `current_price_fact_ref`/`previous_price_fact_ref` (§5d) PHẢI trỏ candle fact ở lifecycle state CLOSED.

**§5d — Input evidence (authoritative reference, KHÔNG chỉ copied value — KHÔNG redefine Candle/Feature/Context contract):**

```yaml
input_evidence:
  previous_price_fact_ref: {type: event_record_ref, required: true}
  current_price_fact_ref: {type: event_record_ref, required: true}
  previous_reference_fact_ref: {type: event_record_ref, required: true, description: "nguồn cụ thể (Feature type hay contract khác) deferred §16, opaque reference"}
  current_reference_fact_ref: {type: event_record_ref, required: true}
  timeframe: {type: string, required: true, description: "copied scalar, nguồn authoritative = configuration_version_ref"}
```

**Invariant no-look-ahead (I-3, ADR-010 §2.4):** mọi `*_fact_ref` trong `input_evidence` PHẢI thỏa `fact.recorded_time ≤ decision_context_cursor.recorded_time` — vi phạm → invalid DecisionRecorded (Scenario 4-đối-ứng-D, §18).

**§5e — Result:**

```yaml
result: {type: enum, values: [LONG, SHORT, NO_ACTION], required: true, description: "rule evaluation THẬT — LONG/SHORT khi current_condition_met true theo crossing_policy; NO_ACTION khi false."}
```

**v0.2 (đóng `C4-MAJ-01`):** `trade_intent_outcome` field ĐÃ BỊ LOẠI BỎ — Decision KHÔNG còn tuyên bố Trade Intent đã issue hay chưa. Xem §10 (Decision-to-Trade-Intent cardinality) cho derivation model mới; trade-intent.md §10 cho canonical `trade_intent_derivation_idempotency_policy`.

## 6. `DecisionFactInvalidated` — `kind: event`

Kế thừa envelope §3 (KHÔNG thuộc `event_class: decision`). `causation_refs` không rỗng.

```yaml
id: decision-fact-invalidated
kind: event
capability_id: decision-management
domain_context_id: strategy-decision
description: >
  Phủ định MỘT DecisionRecorded ĐÃ SAI thực tế (KHÔNG phải registry-transition staleness — trường
  hợp đó dùng DecisionRevalidated, §7). v0.2 (đóng C4-MAJ-03): correction lineage nay CHO PHÉP
  một replacement DecisionRecorded MỚI (decision_id khác, supersedes_fact_ref trỏ về đây) CÙNG
  logical computation key — xem §11.
invariants:
  - "envelope.subject_ref PHẢI BẰNG HỆT subject_ref của invalidated_fact_ref."
  - "envelope.effective_time PHẢI BẰNG HỆT decision_time của DecisionRecorded bị invalidate (DecisionFactInvalidated không mang decision_time — kế thừa giá trị effective-axis của fact gốc vào effective_time tiêu chuẩn của chính nó)."
  - "invalidated_fact_ref PHẢI trỏ một DecisionRecorded, CHƯA từng nhận invalidation khác — một fact chỉ bị invalidate đúng một lần. KHÔNG BAO GIỜ trỏ một DecisionFactInvalidated/DecisionRevalidated/DecisionEvaluationAttemptRecorded khác."
  - "envelope.recorded_time PHẢI muộn hơn recorded_time của invalidated_fact_ref."
  - "Replay tại cursor trước recorded_time của invalidation KHÔNG được thấy invalidation này (chống look-ahead)."
  - "**v0.2 (đóng C4-MAJ-03):** sau invalidation, decision_id đó VĨNH VIỄN TERMINALLY_INVALID (§8) — KHÔNG BAO GIỜ có replacement dưới CÙNG decision_id. Nhưng logical computation key (strategy_instance_id, decision_context_cursor) của fact bị invalidate CÓ THỂ nhận một DecisionRecorded MỚI (decision_id khác, supersedes_fact_ref = event này) — xem §11 cho invariant đầy đủ."
  - "Nếu decision_id bị invalidate đã có TradeIntentIssued (trade-intent.md §3) trỏ về nó, TradeIntent liên quan KHÔNG tự động invalidate — Trade Intent lifecycle độc lập (trade-intent.md §7), correction Decision KHÔNG cascade tự động sang Trade Intent đã issue. Origin-validity của Trade Intent đó cho Risk evaluation MỚI được xử lý qua `eligible_for_new_risk_evaluation` (trade-intent.md §6a), KHÔNG qua cascade tự động ở đây."
payload:
  invalidated_fact_ref: {type: event_record_ref, required: true}
  invalidation_reason: {type: string, required: false}
```

## 7. `DecisionRevalidated` — `kind: event`

Kế thừa envelope §3 (KHÔNG thuộc `event_class: decision`). `causation_refs` không rỗng — PHẢI chứa `DecisionRecorded` gốc. Thực thi chính xác **Append-and-Revalidate policy** (ADR-010 §2.6, Chapter 8 §8.4.1) — KHÔNG phải correction, là một fact VẬN HÀNH độc lập.

```yaml
id: decision-revalidated
kind: event
capability_id: decision-management
domain_context_id: strategy-decision
description: >
  Kết quả revalidation của một DecisionRecorded đã in-flight qua registry transition (ADR-010
  §2.6). Decision gốc VẪN append như immutable historical fact (KHÔNG tự động có execution
  eligibility) — event này ghi nhận kết quả revalidate làm authoritative fact.
invariants:
  - "causation_refs PHẢI trỏ chính xác DecisionRecorded gốc (§5) — KHÔNG dùng success của Decision khác (Chapter 8 §8.4.1, mục 1)."
  - "PHẢI ghi evidence registry/knowledge boundary đã dùng để revalidate — field revalidated_against_registry_version, revalidated_against_frontier_ref (mục 2)."
  - "outcome = SUCCEEDED chỉ cấp execution eligibility TRONG registry applicability interval của chính lần revalidate này (mục 5) — registry transition xảy ra SAU đó khiến eligibility quay lại blocked. Cơ chế enforcement cụ thể (atomic check, fencing token) là Phase 1 (§16); boundary semantic pin tại đây."
  - "outcome = STALE hoặc REJECTED: Decision gốc KHÔNG bị sửa/xóa — chỉ ghi nhận revalidation KHÔNG cấp eligibility. Nếu target stream đã retire, preservation fact riêng trên canonical Audit Stream áp dụng (Chapter 8 §8.4.1 — deferred §16)."
  - "Một DecisionRecorded có thể nhận NHIỀU DecisionRevalidated qua thời gian — KHÔNG giới hạn một-lần-duy-nhất."
payload:
  original_decision_ref: {type: event_record_ref, required: true}
  outcome: {type: enum, values: [SUCCEEDED, STALE, REJECTED], required: true}
  revalidated_against_registry_version: {type: string, required: true}
  revalidated_against_frontier_ref: {type: event_record_ref, required: true}
  reason: {type: string, required: false}
```

**Preservation fact trên canonical Audit Stream (Chapter 8 §8.4.1 mục 6)** — Phase 1, chưa author cụ thể (§16), đòi hỏi Stream Registry/Audit Stream infrastructure chưa tồn tại.

## 8. `DecisionCurrentView` — `kind: read_model` (optional, recommended)

**Không phải authoritative event.** Rebuild được từ §5–§7.

```text
Trước khi bất kỳ DecisionRecorded nào tồn tại cho một logical computation key:
  → KHÔNG có DecisionCurrentView row nào tồn tại
  → GetDecisionForComputation trả về NOT_FOUND / ABSENT
```

**v0.2 (đóng `C4-MAJ-03`) — khóa cursor theo LOGICAL COMPUTATION KEY, KHÔNG còn theo decision_id đơn lẻ** (vì decision_id đổi qua correction lineage): view chính là `GetDecisionForComputation(strategy_instance_id, decision_context_cursor, cursor)`. Một lookup phụ theo decision_id cụ thể (`GetDecisionByld`) vẫn khả dụng để biết một decision_id CỤ THỂ còn VALID hay đã bị supersede/invalidate.

`view_state` chỉ có **hai** giá trị — `VALID`, `PENDING_CORRECTION`. Khi `PENDING_CORRECTION`, `pending_correction_class` BẮT BUỘC có mặt — **v0.2: CHỈ MỘT giá trị khả dĩ** (đóng C4-MAJ-03 — logical key luôn CÓ THỂ nhận replacement, KHÔNG còn khái niệm "vĩnh viễn chết" cho subject này):

```text
view_state = VALID              → pending_correction_class: CẤM (phải absent)
view_state = PENDING_CORRECTION → pending_correction_class = AWAITING_SAME_SUBJECT_REPLACEMENT (LUÔN LUÔN — một logical key bị invalidate luôn CÓ THỂ nhận DecisionRecorded thay thế qua §11, dù không bắt buộc phải có ngay)
```

**Fold algorithm v0.2 (visible-valid-head per LOGICAL COMPUTATION KEY, đóng `C4-MAJ-03`):**

```text
1. Group mọi DecisionRecorded/DecisionFactInvalidated theo logical computation key (strategy_instance_id,
   decision_context_cursor).
2. Trong một key, dựng chain theo supersedes_fact_ref: D1 (gốc, KHÔNG supersedes_fact_ref) → D2
   (supersedes_fact_ref = D1) → D3 (supersedes_fact_ref = D2) → ... (mỗi liên kết PHẢI resolve đúng
   MỘT predecessor — cấm fork, §11 invariant 6).
3. Với mỗi Di trong chain, resolve DecisionFactInvalidated visibility tại cursor (recorded_time <= cursor).
4. Duyệt chain từ D1: dừng tại link ĐẦU TIÊN chưa bị invalidate visible tại cursor — đó là visible
   valid head. current decision_id = head đó.
5. NẾU link cuối cùng đã duyệt bị invalidate visible VÀ KHÔNG CÓ link kế tiếp visible tại cursor →
   view_state = PENDING_CORRECTION, pending_correction_class = AWAITING_SAME_SUBJECT_REPLACEMENT,
   DỪNG — không resolve field nào khác.
6. NẾU tìm được head hợp lệ → view_state = VALID, resolve toàn bộ payload DecisionRecorded của head
   đó làm scope hiện tại.
7. Fold mọi DecisionRevalidated visible (§7) của head hiện hành, total-order recorded_time ASC,
   event_id ASC — revalidation_status = outcome MỚI NHẤT visible (hoặc absent nếu chưa revalidate).
```

```yaml
id: decision-current-view
kind: read_model
capability_id: decision-management
domain_context_id: strategy-decision
description: >
  Projection tiện dụng cho query/UI, KHÔNG BAO GIỜ là input hợp lệ cho Trade Intent/Risk/Execution
  hay bất kỳ computation nào khác — cùng nguyên tắc Current-View-never-authority. Downstream field
  PHẢI resolve qua authoritative Decision event stream (`ref: decision`) TẠI CÙNG cursor mà
  computation đó đang dùng (§14). Cache chỉ chấp nhận khi ĐỒNG THỜI cursor-addressable VÀ provably
  equivalent với authoritative reconstruction.
invariants:
  - "Phải rebuild được hoàn toàn từ authoritative event stream (Chapter 7 §7.4 rebuild determinism)."
  - "KHÔNG được dùng làm input cho Trade Intent/Risk/Execution/Order/Fill/Position hay computation nào khác — CHỈ query/UI."
  - "view_state PHẢI đúng theo Bước 4–5 của fold algorithm — visible-valid-head chain quyết định, KHÔNG BAO GIỜ fallback về một fact đã invalidate."
  - "pending_correction_class BẮT BUỘC có mặt khi view_state = PENDING_CORRECTION (luôn = AWAITING_SAME_SUBJECT_REPLACEMENT); CẤM có mặt khi view_state = VALID."
schema:
  strategy_instance_id: {type: string, required: true, description: "một phần logical computation key"}
  decision_context_cursor: {type: object, required: true, description: "phần còn lại logical computation key"}
  current_decision_id: {type: string, required: false, description: "decision_id của visible valid head — chỉ có mặt khi view_state = VALID"}
  scope: {result: string, required: true, description: "chỉ có mặt khi view_state = VALID — toàn bộ payload head hiện hành"}
  view_state: {type: enum, values: [VALID, PENDING_CORRECTION], required: true}
  pending_correction_class: {type: enum, values: [AWAITING_SAME_SUBJECT_REPLACEMENT], required: false}
  revalidation_status: {type: enum, values: [SUCCEEDED, STALE, REJECTED], required: false}
  last_recorded_time: timestamp
queries: [GetDecisionForComputation, GetDecisionById, GetDecisionHistory]
```

## 9. Explanation contract

**Explanation là derived, non-authoritative rendering — KHÔNG UI copy, KHÔNG natural-language generation infrastructure.** Structured evaluation facts (§5c `rule_evidence`) là authoritative; text rendering CHỈ là một hàm thuần túy của evidence đã có.

```text
Explanation(decision_id) = deterministic render của {rule_evidence, input_evidence, result} — KHÔNG
computation mới, KHÔNG external lookup, KHÔNG dùng bất kỳ giá trị nào không có mặt trong §5b–§5e.
```

Ví dụ walking-skeleton (đúng Scenario 1, §18) — render tương đương:

```text
Previous close <= previous EMA: true      (rule_evidence.previous_condition_met)
Current close > current EMA: true          (rule_evidence.current_condition_met)
Crossing policy: strict                    (rule_evidence.crossing_policy = STRICT_CROSS)
Result: LONG                               (result)
```

**Invariant:** hai Decision với cùng `rule_evidence`/`input_evidence`/`result` PHẢI cho cùng explanation render (deterministic). Explanation KHÔNG có event/subject riêng — một PROJECTION thuần túy của DecisionRecorded.

## 9a. Parity/replay comparison semantics — Canonical Decision Semantic Representation (v0.4 → v0.5, **CONSOLIDATED STABLE — KHÔNG Approved**, §9a lifecycle: candidate → Consolidated Stable, Product Owner consolidation decision — xem banner trên)

**Vai trò:** làm rõ semantics cho parity/replay comparison — thuật ngữ `canonical semantic-decision hash` đã dùng xuyên suốt `product-requirement.md` (PR-010/PR-019), `use-case-workflow.md` (UC-005), VÀ `ux-blueprint.md` (VIEW-003) TỪ v0.1/v0.2 các tài liệu đó, NHƯNG decision.md v0.1–v0.3 KHÔNG BAO GIỜ chứa định nghĩa CỤ THỂ nào cho thuật ngữ này (exhaustive search xác nhận, xem package-1.6-upstream-resolution-exploration.md §4.2). §9a này CUNG CẤP định nghĩa đó LẦN ĐẦU TIÊN — nay `Consolidated Stable` (đã qua Review A + bounded correction verification CLEAN + Independent Review B CLEAN + Product Owner consolidation decision, xem banner trên) — KHÔNG PHẢI `Approved`/`Locked`. Baseline decision.md v0.3 (Package 0.2-C4, Consolidated Stable) VÀ §9a v0.5 (Consolidated Stable) NAY ĐỀU LÀ controlling, cùng nhau — KHÔNG conflict, KHÔNG §1–§8/§10–§18 nào bị re-open.

**Phạm vi bounded tường minh:** §9a KHÔNG chọn hash algorithm/serialization technology; KHÔNG chọn module/owner nào thực thi parity computation; KHÔNG assign Phase 1 package; KHÔNG thêm dependency edge; KHÔNG redefine fold algorithm (§8) hay correction lineage (§11) ngoài phạm vi tham chiếu cần thiết; KHÔNG tạo Domain entity/event mới trừ khi tường minh nói khác dưới đây.

### 9a.1 Canonical Decision Semantic Representation

**Định nghĩa:** một tập field CỐ ĐỊNH, derive TRỰC TIẾP từ §5b/§5c/§5d/§5e (DecisionRecorded payload, ĐÃ established, KHÔNG field mới nào invent) — dùng để xác định hai DecisionRecorded (một recorded, một recomputed) có CÙNG Ý NGHĨA (semantic meaning) hay không. Representation LÀ một khái niệm CẤU TRÚC (structured value) — §9a.2 định nghĩa Digest riêng cho trường hợp cần một giá trị đơn compact.

```yaml
canonical_decision_semantic_representation:
  result: {ref: "§5e", description: "Decision semantic type/outcome — LONG/SHORT/NO_ACTION; NO_ACTION LÀ explicit no-action/abstain semantics đã established"}
  instrument_selection_ref: {ref: "§5b strategy_evidence.instrument_selection_ref", description: "{instrument_id, venue_id, listing_id} — Instrument/Venue market-reference identity"}
  strategy_instance_id: {ref: "§1/§5", description: "Strategy Instance identity — implicitly pin Account/environment qua strategy.md §5 (environment resolve qua account_id); KHÔNG duplicate account_id/environment như field riêng tại representation này"}
  strategy_definition_version_id: {ref: "§5b strategy_evidence.strategy_definition_version_id", description: "Strategy Definition Version identity"}
  configuration_version_ref: {ref: "§5b strategy_evidence.configuration_version_ref", description: "Configuration Version identity"}
  decision_rule_ref: {ref: "§5c rule_evidence.decision_rule_ref", description: "Decision rule identity"}
  rule_family: {ref: "§5c rule_evidence.rule_family", description: "rule-set identity/version — bounded enum"}
  decision_context_cursor: {ref: "§1/§3, Chapter 8 §8.5.1", description: "decision-context cursor identity — canonical Replay Cursor value tại đó Decision có hiệu lực"}
  normalized_rule_parameters: {ref: "§5c", description: "price_source, reference_series_type, reference_series_period, crossing_policy, evaluation_timing, previous_price_value, previous_reference_value, current_price_value, current_reference_value, previous_condition_met, current_condition_met — normalized semantic parameter trực tiếp quyết định result"}
  input_evidence_refs: {ref: "§5d", description: "previous_price_fact_ref, current_price_fact_ref, previous_reference_fact_ref, current_reference_fact_ref, timeframe — controlling input-evidence reference PHẢI dùng CÙNG giá trị ở cả hai phía so sánh"}
```

**Loại trừ tường minh (bắt buộc, KHÔNG đưa vào representation):**

```text
decision_id                        — opaque database/event identity (§1) — KHÔNG semantic content.
envelope field (event_id,
  recorded_time, published_at,
  v.v., §3)                        — append sequence/storage timestamp/transport metadata — KHÔNG
                                    semantic content.
subject_ref                        — envelope identity wrapper — KHÔNG semantic content.
causation_refs                     — correlation/causation identifier (§5, trỏ
                                    DecisionEvaluationAttemptRecorded) — decision.md KHÔNG
                                    establish causation_refs LÀ một phần semantic identity (chứng
                                    minh ORDER/audit, KHÔNG chứng minh MEANING) — loại trừ.
supersedes_fact_ref                 — correction-lineage MECHANISM (§11), dùng để SELECT visible-
                                    valid head (§9a.3) — KHÔNG PHẢI một phần semantic payload
                                    được so sánh.
account_id, environment (§5b)       — implicitly pinned qua strategy_instance_id (strategy.md §5)
                                    — KHÔNG duplicate như field riêng (tránh redundant/derived
                                    field).
plugin_version_ref,
  package_build_artifact_ref (§5b,
  ADR-013 trục 2/4)                — LÀ implementation/build identity (CODE NÀO đã chạy), KHÔNG
                                    xác định Ý NGHĨA quyết định — loại trừ khỏi representation so
                                    sánh (Representation payload KHÔNG đổi bởi v0.5). **(v0.5, đóng
                                    `P16-V003-A-MAJ-01`)** VẪN bắt buộc pin ĐẦY ĐỦ tại parity result
                                    envelope như `decision_implementation_version` (§9a.5a) — KHÔNG
                                    optional khi recorded Decision đã establish các reference này —
                                    VÀ recomputation PHẢI dùng ĐÚNG CÙNG pinned implementation
                                    identity với recorded side (§9a.4), KHÔNG chỉ pin như context bị
                                    động; nếu required reference không resolve/reproduce được ở một
                                    trong hai phía → INDETERMINATE (§9a.6), KHÔNG MATCH/MISMATCH.
Explanation (§9)                    — deterministic PURE render của {rule_evidence, input_evidence,
                                    result} ĐÃ có trong representation — so sánh prose rendering LÀ
                                    redundant VÀ fragile trước formatting change — loại trừ.
signature, secret, custody material — KHÔNG áp dụng cho Decision (Package 1.2 boundary) — xác nhận
                                    tường minh KHÔNG BAO GIỜ xuất hiện.
Risk/Execution/Order/Fill/Position
  outcome                          — §15 Prohibitions đã xác nhận Decision KHÔNG sở hữu các concept
                                    này — loại trừ tuyệt đối.
```

### 9a.2 Canonical Decision Semantic Digest (tuỳ chọn, non-authoritative derived evidence — v0.5, đóng `P16-V003-A-MAJ-02`)

```text
**Sửa v0.5:** v0.4 tuyên bố SAI "so sánh CÓ THỂ dùng trực tiếp Representation HOẶC Digest, kết quả
  logic tương đương, miễn digest derivation deterministic" — deterministic derivation KHÔNG tự động
  ngụ ý logical equivalence giữa Representation và Digest tại tầng GOVERNANCE, vì digest phụ thuộc
  một canonical encoding/field-ordering/absent-vs-null treatment/algorithm CHƯA được pin ở đâu.

Canonical Decision Semantic Representation (§9a.1, structured) LÀ semantic comparison authority.
Canonical Decision Semantic Digest LÀ evidence phái sinh COMPACT, derive TỪ (VÀ CHỈ TỪ)
  Representation (§9a.1) — KHÔNG derive từ bất kỳ field nào bị loại trừ tại §9a.1 — nhưng Digest
  TỰ NÓ KHÔNG PHẢI authority, CHỈ là một biểu diễn tiện dụng CÓ ĐIỀU KIỆN.

Sử dụng Digest đòi hỏi CHÍNH NÓ một digest-definition identity/version riêng biệt —
  `decision_semantic_digest_definition_id`/`decision_semantic_digest_definition_version` (§9a.5b) —
  ràng buộc tối thiểu bốn yếu tố qua một technical contract quản trị RIÊNG (KHÔNG author/chọn công
  nghệ tại §9a này — ngoài phạm vi transaction này):
    canonical encoding (thứ tự serialize field);
    field ordering;
    absent-versus-null treatment (field vắng mặt vs field = null);
    digest/hash algorithm cụ thể.

CHO TỚI KHI digest-definition contract đó tồn tại VÀ được govern riêng: so sánh Representation
  CẤU TRÚC trực tiếp (structured comparison) LÀ cơ sở hợp lệ DUY NHẤT cho MATCH (§9a.6).

Digest equality ĐƠN ĐỘC (không kèm structured Representation comparison hợp lệ dưới cùng digest-
  definition version đã govern) KHÔNG được thiết lập MATCH.

Digest mismatch CHỈ được thiết lập MISMATCH khi CẢ HAI điều kiện đúng: (a) cả hai digest được sinh
  ra dưới CÙNG một digest-definition version đã govern hợp lệ; VÀ (b) cả hai digest derive từ
  Representation đã resolve THÀNH CÔNG ở cả hai phía (§9a.1/§9a.3/§9a.4).

Digest-definition unresolved, KHÔNG tồn tại, HOẶC incompatible giữa hai phía → INDETERMINATE
  (§9a.6) — KHÔNG BAO GIỜ tự ý coi digest mismatch LÀ semantic MISMATCH khi digest-definition chưa
  govern/chưa khớp.

Digest concept VẪN available/candidate tại §9a này nhưng non-authoritative VÀ non-substitutive cho
  structured Representation comparison cho tới khi digest-definition technical contract được author
  VÀ Consolidated riêng biệt.
```

### 9a.3 Recorded-side selection (correction-aware, cursor-bounded)

```text
Recorded Decision dùng cho so sánh PHẢI LÀ visible-valid-head (§8 fold algorithm, KHÔNG redefine
  tại đây) cho logical computation key (strategy_instance_id, decision_context_cursor) TẠI canonical
  Replay Cursor đang xét (§1/§8/§11, KHÔNG đổi).
Loại trừ invalidated/superseded head theo đúng §8 Bước 3–4 (resolve DecisionFactInvalidated
  visibility, dừng tại link đầu tiên KHÔNG bị invalidate).
KHÔNG so sánh với mutable-latest ngoài cursor đã chọn — cùng nguyên tắc `DecisionCurrentView`
  KHÔNG BAO GIỜ authority (§8, KHÔNG đổi).
Multiple eligible head, missing key resolution, HOẶC ambiguous lineage (§8 Bước 5, view_state =
  PENDING_CORRECTION) KHÔNG THỂ tạo ra MATCH/MISMATCH — PHẢI INDETERMINATE (§9a.6).
```

### 9a.4 Recomputed-side constraint (non-authoritative)

```text
Recomputation PHẢI dùng ĐÚNG semantic input VÀ ĐẦY ĐỦ chín trục pinned đã established của Decision
  recorded đang test (v0.5, đóng `P16-V003-A-MIN-01`, thay thế danh sách rút gọn tại v0.4) —
  KHÔNG được tự chọn version/input/identity khác cho bất kỳ trục nào dưới đây:
    (1) Strategy Instance (strategy_instance_id);
    (2) Strategy Definition Version (strategy_definition_version_id);
    (3) Configuration Version (configuration_version_ref);
    (4) Decision rule identity/version (decision_rule_ref, rule_family);
    (5) Decision implementation provenance, KHI CÓ established tại recorded Decision
        (decision_implementation_version — plugin_version_ref + package_build_artifact_ref, §9a.5a);
    (6) canonical Replay Cursor (decision_context_cursor);
    (7) input evidence reference (input_evidence_refs);
    (8) semantic-representation-definition version (decision_semantic_representation_definition_id/
        version, §9a.5b);
    (9) digest-definition version, KHI dùng Digest (decision_semantic_digest_definition_id/version,
        §9a.5b, §9a.2).

**(v0.5, đóng `P16-V003-A-MAJ-01`) Implementation-identity constraint:** khi recorded Decision đã
  establish `decision_implementation_version` (trục 5), recomputation PHẢI chạy dưới ĐÚNG CÙNG
  pinned implementation identity đó (KHÔNG "code/build mới nhất hiện tại") — nếu recorded Decision
  đã establish trục này VÀ một trong hai phía KHÔNG resolve/reproduce được đúng identity đó, kết
  quả PHẢI LÀ INDETERMINATE (§9a.6), KHÔNG MATCH/MISMATCH. Representation (§9a.1) bằng nhau giữa
  hai phía trong khi implementation identity KHÁC NHAU hoặc KHÔNG xác nhận được KHÔNG đủ căn cứ để
  tuyên bố một deterministic parity verification — trường hợp này PHẢI INDETERMINATE, KHÔNG tự động
  MATCH chỉ vì Representation khớp.

Nếu BẤT KỲ trục nào trong chín trục trên KHÔNG resolve nhất quán giữa recorded/recomputed side →
  INDETERMINATE (§9a.6).

Recomputation KHÔNG được:
  append một Decision authoritative MỚI (§1/§5 authority KHÔNG đổi).
  thay thế hay correct Decision đã ghi nhận (§11 correction lineage KHÔNG áp dụng cho parity —
    parity KHÔNG PHẢI một correction).
  invoke Decision Authority acceptance (§1) chỉ để thực hiện parity — parity LÀ một side
    computation, KHÔNG một write path vào Decision authoritative stream.
  tiêu thụ Risk/Execution outcome (Package 0.2-C5+, chưa author/ngoài phạm vi) làm Decision
    input — Decision input CHỈ từ §5b/§5c/§5d, KHÔNG downstream fact nào.
  dùng mutable-latest Strategy/Configuration value — PHẢI dùng ĐÚNG version axis đã pin tại
    recorded side (trên), KHÔNG "phiên bản mới nhất hiện tại."

Parity recomputation KHÔNG liên quan Append-and-Revalidate (§7 DecisionRevalidated, ADR-010
  §2.6) — hai khái niệm HOÀN TOÀN tách biệt: DecisionRevalidated LÀ một fact vận hành về
  execution-eligibility qua registry transition; parity recomputation LÀ một verification
  non-authoritative về semantic equality, KHÔNG tạo fact nào, KHÔNG liên quan registry/
  eligibility. KHÔNG conflate hai khái niệm.

Module/owner nào thực thi recomputation KHÔNG được chọn tại §9a này — ngoài phạm vi tài liệu
  này (xem package-1.6-upstream-resolution-exploration.md, KHÔNG sửa bởi transaction này).
```

### 9a.5 Definition/version identity — parity result envelope (v0.5 — restructure, đóng `P16-V003-A-MAJ-03`)

**Sửa v0.5:** v0.4 dùng version của CHÍNH tài liệu decision.md (`v0.4`) LÀM identity cho representation-definition — conflate hai khái niệm khác nhau: "decision.md thay đổi NHƯ một tài liệu" versus "field-set/comparison-semantics của Representation thay đổi." Một sửa đổi decision.md KHÔNG liên quan §9a (vd. sửa lỗi chính tả tại §1–§8) sẽ SAI nếu tự động bump identity so sánh của parity. §9a.5 nay tách BA trục độc lập tường minh:

#### 9a.5a Parity result envelope — pinned axes (repeat từ Representation cho audit/provenance)

```text
Mọi parity result PHẢI pin đầy đủ:
  strategy_instance_id, strategy_definition_version_id, configuration_version_ref,
    decision_rule_ref, rule_family: đã có trong Representation (§9a.1), pin LẶP LẠI tại result
    envelope cho mục đích audit/provenance tách biệt khỏi payload so sánh.
  decision_implementation_version: {type: object, required: CONDITIONAL — v0.5, đóng
    `P16-V003-A-MAJ-01`: BẮT BUỘC (KHÔNG optional) khi recorded Decision ĐÃ establish
    plugin_version_ref VÀ/HOẶC package_build_artifact_ref (§5b); vắng mặt CHỈ hợp lệ khi recorded
    Decision tự nó KHÔNG establish các reference này. description: "plugin_version_ref +
    package_build_artifact_ref (§5b) — pin NHƯ implementation-identity context/provenance, KHÔNG
    PHẢI một phần Representation so sánh (§9a.1 loại trừ) — recomputation PHẢI reproduce ĐÚNG
    CÙNG giá trị này khi required (§9a.4); KHÔNG resolve được → INDETERMINATE."
  canonical_replay_cursor: đã có trong Representation (decision_context_cursor) — KHÔNG duplicate,
    tham chiếu lại.
  eligible_input_evidence_refs: đã có trong Representation (input_evidence_refs) — KHÔNG
    duplicate, tham chiếu lại.
```

#### 9a.5b Independent definition identities (v0.5, đóng `P16-V003-A-MAJ-03` — BA trục tách biệt, KHÔNG gộp)

```text
1. decision_contract_document_version: {type: string, description: "version của decision.md NHƯ
     một TÀI LIỆU (frontmatter `version`, hiện = 0.5) — KHÔNG PHẢI comparison identity. Thay đổi
     document version (kể cả thay đổi KHÔNG liên quan §9a) KHÔNG tự động bump hai trục dưới đây."}

2. decision_semantic_representation_definition_id / decision_semantic_representation_definition_version:
     {type: string/string, required: true, description: "identity/version ĐỘC LẬP của field-set +
     comparison semantics tại §9a.1/§9a.3/§9a.4/§9a.6 — Chapter 8 §8.1.1 năm điều kiện Referenced
     Authoritative Artifact áp dụng đầy đủ: versioned, immutable-after-reference, no ID reuse,
     persistently resolvable, verifiable content identity. Giá trị hiện tại (Consolidated Stable,
     tách biệt lần đầu khỏi document version tại v0.5): id = `DSR-001`, version = `2` — bump từ giá trị ngầm
     định trước đó (`1`, chưa tách biệt tường minh tại v0.4) vì chính correction v0.5 này đổi
     comparison semantics (bắt buộc implementation-identity pin khi established, MATCH criterion
     mở rộng, §9a.4/§9a.6). Một thay đổi field-set/comparison-semantics TƯƠNG LAI PHẢI bump
     version này; unrelated decision.md document revision KHÔNG bump."}

3. decision_semantic_digest_definition_id / decision_semantic_digest_definition_version:
     {type: string/string, required: false, description: "identity/version ĐỘC LẬP cho canonical
     encoding + digest derivation (§9a.2) — KHÁC BIỆT khỏi (2), quản trị qua technical contract
     RIÊNG (KHÔNG author tại đây). Giá trị tại candidate này: **CHƯA ESTABLISHED / unresolved** —
     KHÔNG chọn placeholder giả; digest-based comparison KHÔNG valid cho tới khi trục này được
     author và Consolidated riêng biệt (§9a.2). Trong lúc unresolved: bất kỳ yêu cầu digest-based
     comparison nào → INDETERMINATE (§9a.6), KHÔNG MATCH/MISMATCH."}
```

### 9a.6 Outcome model — MATCH / MISMATCH / INDETERMINATE (workflow-visible, non-authoritative — v0.5 tightened, đóng `P16-V003-A-MAJ-01`/`P16-V003-A-MAJ-02`/`P16-V003-A-MIN-01`)

```text
Đúng BA outcome, KHÔNG hơn, KHÔNG collapse INDETERMINATE vào MISMATCH:

MATCH:          TẤT CẢ đúng: (a) CẢ HAI phía (recorded, recomputed) evaluable dưới CÙNG ĐẦY ĐỦ
                chín pinned axis (§9a.4 — Strategy Instance, Strategy Definition Version,
                Configuration Version, Decision rule identity/version, Decision implementation
                provenance khi có, canonical Replay Cursor, input evidence reference, semantic-
                representation-definition version §9a.5b, digest-definition version §9a.5b khi
                dùng digest); (b) Canonical Decision Semantic Representation (§9a.1) của cả hai
                BẰNG NHAU qua structured comparison trực tiếp (§9a.2 — digest equality ĐƠN ĐỘC
                KHÔNG đủ); VÀ (c) **(v0.5)** khi recorded Decision đã establish
                `decision_implementation_version`, recomputation đã reproduce ĐÚNG CÙNG identity
                đó (§9a.4) — Representation bằng nhau dưới implementation identity KHÁC NHAU/KHÔNG
                xác nhận được KHÔNG đủ căn cứ cho MATCH (→ INDETERMINATE).

MISMATCH:       CẢ HAI phía evaluable dưới CÙNG đầy đủ chín pinned axis (bao gồm cùng
                implementation identity khi established) VÀ Representation của hai phía KHÁC
                NHAU qua structured comparison — HOẶC (§9a.2, v0.5) digest mismatch được thiết lập
                CHỈ khi cả hai digest sinh dưới CÙNG digest-definition version đã govern hợp lệ TỪ
                Representation đã resolve thành công ở cả hai phía.

INDETERMINATE:  một so sánh hợp lệ KHÔNG THỂ hoàn tất vì evidence bắt buộc, version identity,
                cursor state, visible-valid head (§9a.3), bất kỳ trục nào trong chín pinned axis
                (§9a.4), definition identity (§9a.5b), HOẶC recomputation input (§9a.4) missing/
                stale/invalidated/ambiguous/incompatible/non-evaluable — bao gồm, KHÔNG giới hạn:
                input_evidence_refs KHÔNG resolve được tại cursor; decision_context_cursor tự nó
                KHÔNG resolve/valid; recorded-side visible-valid-head ở trạng thái
                PENDING_CORRECTION KHÔNG CÓ successor (§8 Bước 5); nhiều eligible head hoặc
                lineage ambiguous (data-integrity condition, PHẢI INDETERMINATE nếu phát hiện,
                KHÔNG tự ý chọn một head); `decision_semantic_representation_definition_id`/
                `version` (§9a.5b) KHÔNG khớp/KHÔNG resolve giữa hai phía; **(v0.5)** recorded
                Decision đã establish `decision_implementation_version` NHƯNG một trong hai phía
                KHÔNG resolve/reproduce được đúng identity đó; **(v0.5)** digest-based comparison
                được yêu cầu nhưng `decision_semantic_digest_definition_id`/`version` unresolved/
                incompatible giữa hai phía; recomputation KHÔNG thể chạy dưới ĐÚNG CÙNG pinned axis
                đã chọn tại recorded side (bất kỳ trục nào trong chín trục).

TẤT CẢ BA outcome LÀ workflow-visible, non-authoritative — KHÔNG một Domain fact/entity mới nào
được tạo cho bất kỳ outcome nào (cùng nguyên tắc UC-003's "workflow-visible result DUY NHẤT,
KHÔNG authoritative fact," áp dụng tương đương ở đây) — mặc định treatment LÀ query/workflow
result THUẦN TÚY. §9a KHÔNG tạo một "ParityResult" Domain entity/event mới — KHÔNG existing
source semantics nào yêu cầu một entity như vậy; nếu evidence tương lai chứng minh cần thiết, đó
LÀ một correction/authoring transaction RIÊNG, ngoài phạm vi §9a này.
```

### 9a.7 Authority boundary (bắt buộc, xác nhận tường minh)

```text
Parity comparison KHÔNG tạo, KHÔNG approve, KHÔNG thay thế, KHÔNG invalidate, KHÔNG correct một
  Decision nào — parity CHỈ đọc VÀ so sánh, KHÔNG một write path nào vào Decision authoritative
  stream (§1/§5/§11 authority KHÔNG đổi).
MATCH KHÔNG re-authorize Decision đã recorded — Decision đó ĐÃ authoritative từ trước (§1); MATCH
  CHỈ xác nhận thêm, KHÔNG tạo/củng cố authority mới.
MISMATCH KHÔNG tự động invalidate Decision đã recorded — correction lineage (§11) VẪN đòi hỏi
  đúng quy trình invalidate-rồi-replace tường minh riêng, KHÔNG tự động kích hoạt bởi một
  MISMATCH finding.
INDETERMINATE KHÔNG ngụ ý mismatch — hai khái niệm PHẢI tách biệt tường minh trong mọi
  presentation.
Parity output KHÔNG có Risk, Execution, Order, Fill, Position, hay LIVE authority nào — hoàn toàn
  ngoài phạm vi các authority đó (§15 Prohibitions, KHÔNG đổi).
Owner/module/API/UX technical realization của parity computation KHÔNG được resolve tại §9a này —
  VẪN unresolved, ngoài phạm vi transaction này (xem package-1.6-upstream-resolution-
  exploration.md v0.2, KHÔNG sửa bởi transaction này).
```

## 10. Decision-to-Trade-Intent cardinality (v0.2, đóng `C4-MAJ-01`/`C4-MAJ-02`)

```text
result = LONG hoặc SHORT  →  zero HOẶC MỘT TradeIntentIssued (trade-intent.md §3), keyed UNIQUE bởi
                              originating_decision_id — derivation idempotent, xem trade-intent.md §10
                              `trade_intent_derivation_idempotency_policy: ONE_VALID_INTENT_PER_ORIGINATING_DECISION`

result = NO_ACTION  →  ZERO Trade Intent LUÔN LUÔN
```

**Một Decision → tối đa MỘT Trade Intent** (v0.1 walking skeleton — KHÔNG multi-intent portfolio decomposition). **v0.2 — Decision KHÔNG còn tự tuyên bố đã issue Trade Intent hay chưa (đóng `C4-MAJ-01`, loại bỏ `trade_intent_outcome`)** — việc một Decision LONG/SHORT đã có Trade Intent hay chưa là một CÂU HỎI resolve TRỰC TIẾP bằng cách query authoritative Trade Intent stream lọc theo `originating_decision_id` (trade-intent.md §10), KHÔNG BAO GIỜ dựa vào một field trên chính Decision. Đây là gap TRANSIENT bình thường (Decision và Trade Intent là hai authoritative stream RIÊNG, KHÔNG có cross-stream atomicity ngầm định) — recovery logic (Phase 1) resolve deterministic từ Decision `result` + Trade Intent stream lookup, KHÔNG từ một cờ trạng thái trên Decision.

## 11. Correction lineage (v0.2, đóng `C4-MAJ-03`)

Correction lineage scoped chính xác theo LOGICAL COMPUTATION KEY `(strategy_instance_id, decision_context_cursor)` — mỗi key có chuỗi lineage RIÊNG.

```text
D1 (DecisionRecorded, KHÔNG supersedes_fact_ref)
  → DecisionFactInvalidated targeting D1
  → D2 (DecisionRecorded MỚI — decision_id KHÁC D1, CÙNG strategy_instance_id, CÙNG
    decision_context_cursor, supersedes_fact_ref = fact D1 — không phải trỏ FactInvalidated)

Correction tiếp theo:
D2 → DecisionFactInvalidated targeting D2 → D3, supersedes_fact_ref = D2
  (KHÔNG được supersedes_fact_ref = D1 — cấm nhảy cóc)
```

**Mười invariant bắt buộc** (đối xứng `strategy.md` §13/`account.md`, điều chỉnh cho decision_id KHÔNG bất biến xuyên chain):

1. Decision gốc (D1, KHÔNG có predecessor) KHÔNG có `supersedes_fact_ref`.
2. Replacement (correction) BẮT BUỘC có `supersedes_fact_ref`, trỏ đúng fact bị invalidate.
3. Replacement PHẢI CÙNG `strategy_instance_id` VÀ CÙNG `decision_context_cursor` với fact bị supersede (logical key bất biến xuyên chain, dù `decision_id` đổi).
4. `causation_refs` của replacement PHẢI chứa chính `DecisionFactInvalidated` targeting predecessor — predecessor PHẢI đã invalidate VÀ visible TRƯỚC khi replacement được ghi.
5. Replacement PHẢI supersede đúng lineage head hiện tại — không nhảy cóc qua một head trung gian.
6. Một fact bị invalidate có **tối đa một** replacement authoritative trực tiếp — cấm fork.
7. Replacement không được "visible" (`recorded_time`) trước invalidation tương ứng.
8. Mọi lineage member lịch sử giữ nguyên trong log — append-only (I-3), không mutate; `decision_id` cũ (D1) vẫn resolvable mãi mãi qua `GetDecisionById`.
9. Một fact đã invalidate **không bao giờ** bị tái sử dụng ngầm — `DecisionCurrentView` (§8) phải loại trừ nó tường minh.
10. **Retry của cùng logical key với evidence KHÁC, KHI predecessor CHƯA invalidate, VẪN LÀ conflict** (KHÔNG tự động trở thành correction) — correction CHỈ hợp lệ qua chuỗi tường minh invalidate-rồi-replace ở trên; deterministic conflict path (§1 invariant) áp dụng cho mọi retry không đi qua đường này.

**`DecisionRevalidated` KHÔNG phải correction lineage** — chuỗi VẬN HÀNH độc lập (§7), một DecisionRecorded có thể nhận nhiều DecisionRevalidated theo thời gian, KHÔNG invalidate/thay thế Decision gốc.

## 12. Time semantics và bitemporal correctness

- `decision_time` — effective axis, THAY `effective_time` cho DecisionRecorded. PROHIBITED trên mọi event khác trong tài liệu này.
- `recorded_time` — recorded axis, universal.
- `decision_context_cursor` (envelope-level) — knowledge boundary vector, REQUIRED trên DecisionRecorded, PROHIBITED trên event khác (§3).
- **No-future-input (I-3, ADR-010 §2.4):** `input_event.recorded_time ≤ decision_context_cursor.recorded_time ≤ DecisionRecorded.recorded_time`.
- **Replay tại cursor T** chỉ thấy fact có `recorded_time ≤ T` — invalidation/revalidation/replacement ghi SAU T KHÔNG visible tại T. Replay TRƯỚC một correction thấy D1; replay SAU correction thấy D2 (Scenario 2, §18).
- `market_time` PROHIBITED xuyên suốt tài liệu này.

## 13. Canonical policy identifiers — nguồn duy nhất (context `strategy-decision`)

**Bốn canonical policy identifier, khai báo ĐÚNG MỘT LẦN tại đây cho context `strategy-decision`:**

```yaml
initial_fact_correction_policy: INVALIDATE_ONLY_NO_SAME_ID_REPLACEMENT_FOR_IMMUTABLE_SCOPE_SUBJECTS
decision_computation_idempotency_policy: STABLE_KEY_SAME_EVIDENCE_IS_IDEMPOTENT
decision_evaluation_attempt_idempotency_policy: STABLE_ATTEMPT_ID_SAME_PAYLOAD_IS_IDEMPOTENT
decision_correction_lineage_policy: SAME_LOGICAL_KEY_NEW_ID_INVALIDATE_THEN_REPLACE
```

**`initial_fact_correction_policy`** — v0.2: áp dụng CHỈ cho `DecisionEvaluationAttemptRecorded` (§4, KHÔNG có same-ID replacement — attempt sai thực tế deferred §16). `DecisionRecorded` KHÔNG còn dùng policy này thuần túy — xem `decision_correction_lineage_policy` dưới.

**`decision_computation_idempotency_policy: STABLE_KEY_SAME_EVIDENCE_IS_IDEMPOTENT`** — logical computation key = `(strategy_instance_id, decision_context_cursor)`; retry cùng key + cùng evidence (chưa invalidate) → idempotent no-op; retry cùng key + evidence KHÁC (chưa invalidate predecessor) → reject tường minh (§1, §11 invariant 10). **Đây là policy CỦA DECISION** — áp dụng khi ghi `DecisionRecorded`, KHÔNG phải của Attempt (xem policy dưới).

**`decision_evaluation_attempt_idempotency_policy: STABLE_ATTEMPT_ID_SAME_PAYLOAD_IS_IDEMPOTENT`** (v0.3, sửa, đóng `C4-DELTA-MAJ-02` — đối xứng `instrument.md` §17 `activation_request_idempotency_policy: STABLE_ID_SAME_PAYLOAD_IS_IDEMPOTENT`) — idempotency scoped theo TỪNG `evaluation_attempt_id` cá nhân, KHÔNG theo logical computation key: retry CÙNG `evaluation_attempt_id` + CÙNG payload → idempotent no-op; CÙNG `evaluation_attempt_id` + payload KHÁC → deterministic conflict. **Logical computation key KHÔNG BẮT BUỘC unique** — nhiều `DecisionEvaluationAttemptRecorded` (mỗi cái một `evaluation_attempt_id` riêng) CÓ THỂ tồn tại cùng key, KỂ CẢ với `attempt_outcome` khác nhau (ví dụ `FAILED_BEFORE_EVALUATION` rồi `DECIDED` — retry hợp lệ, KHÔNG data-integrity violation). Việc nhiều attempt DECIDED tại cùng key phải resolve về đúng MỘT Decision là trách nhiệm của `decision_computation_idempotency_policy` ở TẦNG DECISION (§1/§5), KHÔNG phải của policy này.

**`decision_correction_lineage_policy: SAME_LOGICAL_KEY_NEW_ID_INVALIDATE_THEN_REPLACE`** (v0.2, mới, đóng `C4-MAJ-03`) — correction DecisionRecorded KHÔNG same-ID replacement (decision_id vẫn bất biến/không tái sử dụng per-fact), NHƯNG logical computation key CÓ THỂ nhận DecisionRecorded MỚI (decision_id khác) sau khi predecessor invalidate — mười invariant đầy đủ tại §11. Đây là pattern MỚI, khác biệt cả `INVALIDATE_ONLY_NO_SAME_ID_REPLACEMENT...` (không có replacement nào) lẫn correction lineage chuẩn kiểu `StrategyInstanceStatusChanged` (subject_id/decision_id bất biến xuyên chain) — Decision cần decision_id per-fact bất biến (immutability yêu cầu tường minh) VÀ khả năng correction (C4-MAJ-03), nên kết hợp: chain theo logical key, KHÔNG theo subject_id.

## 14. Downstream reference contract (cho Trade Intent §3, và Package 0.2-C5 Risk — chưa author)

`trade-intent.md` và Package 0.2-C5 (Risk, chưa author) tham chiếu Decision qua ĐÚNG các field sau, KHÔNG hơn:

```yaml
decision_id: {type: string, required: true, ref: decision}
strategy_instance_id: {type: string, description: "= subject_ref.scope.strategy_instance_id"}
decision_context_cursor: {type: object, description: "= §3 — cùng logical computation key"}
account_id: {type: string, ref: account, description: "= strategy_evidence.account_id, §5b"}
instrument_selection_ref: {type: object, description: "= strategy_evidence.instrument_selection_ref, §5b — {instrument_id, venue_id, listing_id}"}
result: {type: enum, values: [LONG, SHORT, NO_ACTION], description: "= §5e"}
decision_time: {type: timestamp, description: "= §3"}
```

**Downstream authority rule — MỘT quy tắc duy nhất, không ngoại lệ:** downstream contract PHẢI resolve mọi field trên TRỰC TIẾP từ authoritative Decision event stream (§4–§7) TẠI ĐÚNG cursor mà chính computation đó đang dùng. `DecisionCurrentView` latest-state (§8) KHÔNG BAO GIỜ được dùng làm input. **Consumer cần biết "decision_id X còn valid hay đã bị supersede" PHẢI dùng `GetDecisionById` (§8) hoặc reconstruct trực tiếp — KHÔNG giả định decision_id một khi tồn tại thì mãi mãi là visible-valid-head cho key của nó** (đóng C4-MAJ-06, xem trade-intent.md §6a). `decision.md` KHÔNG author semantics của Trade Intent contents/lifecycle hay Risk.

## 15. Prohibitions

**Decision/DecisionEvaluationAttempt KHÔNG được sở hữu:** Strategy/Strategy Instance identity semantics; Trade Intent contents/lifecycle/derivation idempotency (thuộc `trade-intent.md`); Risk approval/rejection, risk limit, position sizing (Package 0.2-C5, chưa author); Execution Intent/Order/Fill/Position/Replay Event semantics (Package 0.2-C5–C7); order type/limit price/stop price/exchange payload; DSL/expression language/parser/rule graph/strategy compiler tổng quát; UI copy/natural-language generation infrastructure; Candle/Feature/Context contract schema; database transaction/outbox/message-broker technology; general workflow/saga engine; broad runtime exception telemetry/observability infrastructure.

## 16. Ngoài phạm vi — defer

- Stream Registry/Input Contract/canonical Audit Stream implementation cụ thể.
- Preservation fact event type cụ thể trên Audit Stream (Chapter 8 §8.4.1 mục 6).
- Cơ chế fencing/atomic-check cụ thể cho revalidation validity interval.
- Nguồn cụ thể của `previous_reference_fact_ref`/`current_reference_fact_ref` (EMA hay reference-series khác).
- `evaluation_timing = INTRABAR`; `rule_family` khác `PRICE_CROSSES_REFERENCE_SERIES`.
- Multi-intent/portfolio decomposition từ một Decision.
- Correction lineage riêng cho `DecisionEvaluationAttempt` (v0.2, edge case hiếm, immutable append-only đủ cho v0.1/v0.2).
- Granular exception/technical-failure sub-taxonomy cho `FAILED_BEFORE_EVALUATION` — v0.2 CHỈ một reason_code (`ENGINE_COMPUTATION_BOUNDARY_ERROR`), KHÔNG model broad runtime exception telemetry.
- Implementation technology cho cross-stream Decision→Trade Intent recovery (retry queue/outbox/saga) — boundary semantic pin tại §10/trade-intent.md §10, KHÔNG chọn công nghệ.
- Risk rejection/approval semantics, capital/sizing, order type — hoàn toàn ngoài phạm vi Domain Contract này (Package 0.2-C5–C7).

## 17. Open questions ngoài phạm vi

- Cơ chế cụ thể generate `decision_id`/`evaluation_attempt_id` — chưa quyết, Phase 1.
- Retention/resolvability horizon cụ thể cho Decision/DecisionEvaluationAttempt đã lâu.
- Preservation-fact Event Contract cụ thể (Chapter 8 §8.4.1 mục 6) — chờ Stream Registry/Audit Stream Phase 1.
- Không đóng OQ-002/OQ-003.

## 18. Acceptance scenarios (validation, không phải executable test tại C4)

**Scenario 1 — Valid append order (đóng `C4-DELTA-MAJ-01`):** Attempt A1 (evaluation_attempt_id=A1, `attempt_outcome=DECIDED`, KHÔNG resulting_decision_id) ghi TRƯỚC → Decision D1 (`causation_refs` chứa A1) ghi SAU → thứ tự append hợp lệ, KHÔNG circular dependency (A1 không tham chiếu D1 trước khi D1 tồn tại). D1 → Trade Intent T1.

**Scenario 1a — Same-key retry, evaluation_attempt_id giống hệt (đóng `C4-MAJ-01`/`C4-MAJ-02`):** Retry CÙNG `evaluation_attempt_id=A1` + cùng payload → idempotent no-op, trả về A1 đã tồn tại (KHÔNG DecisionEvaluationAttemptRecorded thứ hai) → D1/T1 không đổi.

**Scenario 2 — Decision correction (đóng `C4-MAJ-03`; attempt context đóng `C4-DELTA-MAJ-02` Scenario 5):** A1 DECIDED → D1 tại cursor C ghi sai → invalidate D1 → A2 DECIDED tại CÙNG cursor C (evaluation_attempt_id KHÁC A1) → D2, `supersedes_fact_ref = D1` → đúng một visible valid head (D2) tại cursor sau correction. Replay TRƯỚC correction thấy D1; replay SAU correction thấy D2 (§8 fold algorithm, §12). Đây LÀ trường hợp hợp lệ DUY NHẤT một logical key có hai Decision head khác nhau theo thời gian — vì D1 ĐÃ invalidate trước khi D2 ghi (§11).

**Scenario 3 — Ineligible attempt (đóng `C4-MAJ-04`):** `DecisionEvaluationAttemptRecorded(attempt_outcome=INELIGIBLE)` ghi nhận — KHÔNG Decision, KHÔNG Trade Intent — phân biệt tường minh với "không có attempt nào" (§4, một fact THẬT tồn tại, không phải absence).

**Scenario 4 — Missing input (đóng `C4-MAJ-04`):** `DecisionEvaluationAttemptRecorded(attempt_outcome=INPUT_UNAVAILABLE, reason_code=REQUIRED_PRICE_INPUT_MISSING_OR_PENDING hoặc REQUIRED_REFERENCE_INPUT_MISSING_OR_PENDING)` ghi nhận — reason_code identify đúng boundary evidence thiếu (§4).

**Scenario 5 — Engine failure before evaluation (đóng `C4-MAJ-04`):** `DecisionEvaluationAttemptRecorded(attempt_outcome=FAILED_BEFORE_EVALUATION, reason_code=ENGINE_COMPUTATION_BOUNDARY_ERROR)` — KHÔNG model broad exception telemetry, một reason_code bounded duy nhất (§4/§16).

**Scenario 6 — Cross-stream recovery (đóng `C4-MAJ-01`/`C4-MAJ-02`):** D1 LONG tồn tại (từ attempt A1 DECIDED); TradeIntentIssued append ban đầu bị miss; retry/recovery bằng `originating_decision_id` (trade-intent.md §10) → đúng MỘT T1 (idempotent derivation, KHÔNG duplicate). Decision KHÔNG BAO GIỜ tự tuyên bố "đã issue" sai sự thật — vì nó KHÔNG còn field nào tuyên bố điều đó (§5e/§10).

**Scenario 7 — Time ordering (đóng `C4-MAJ-05`, xem trade-intent.md §3/§9):** `Decision.decision_time = 10:00`; `TradeIntent.effective_time = 09:59` → reject (vi phạm invariant `effective_time >= decision_time`); `TradeIntent.effective_time >= 10:00` → allowed.

**Scenario 8 — Decision invalidation (đóng `C4-MAJ-06`, xem trade-intent.md §6a):** D1 LONG → T1 ISSUED; D1 sau đó invalidate (KHÔNG có replacement ngay) → T1 vẫn historical, nhưng `eligible_for_new_risk_evaluation(T1, cursor sau invalidation) = false` (D1 không còn là visible valid head cho logical key của nó) — KHÔNG tự động xóa/rewrite T1; replay trước invalidation không đổi.

**Scenario 9 — Corrected Decision derives new Intent (đóng `C4-MAJ-03`/`C4-MAJ-06`):** D1 → T1; D1 invalidate; D2 (correction replacement, `supersedes_fact_ref=D1`) LONG → D2 CÓ THỂ derive T2 (`trade_intent_id` MỚI, `originating_decision_id=D2`). T1 và T2 là hai historical fact PHÂN BIỆT — T1 gắn D1 (nay không còn visible-valid-head), T2 gắn D2 (visible-valid-head hiện hành).

**Scenario 10 — Configuration difference (kế thừa Scenario C cũ):** cùng candle, `reference_series_period=50` (EMA50) → `result=LONG`; `reference_series_period=100` (EMA100) → `result=NO_ACTION` — hai DecisionRecorded riêng biệt (khác `configuration_version_ref`, §5b, khác `decision_id`, khác logical key vì khác cursor/evidence tổ hợp).

**Scenario 11 — Future correction hidden (kế thừa Scenario D cũ):** một candle/EMA value CORRECT (recorded SAU `decision_context_cursor` gốc) KHÔNG visible khi replay tại cursor gốc — invariant §3 (`input_event.recorded_time ≤ cursor.recorded_time`) chặn tường minh.

**Scenario 12 — Exact executable difference (kế thừa Scenario F cũ):** cùng Strategy Definition Version + Configuration Version, `package_build_artifact_ref` khác (rebuild non-reproducible, ADR-013 §2.5) → hai `strategy_evidence.package_build_artifact_ref` khác giá trị trên hai DecisionRecorded riêng biệt.

**Scenario 13 — Retry after engine failure (đóng `C4-DELTA-MAJ-02`):** A1 (evaluation_attempt_id=A1, key=(S,C), `attempt_outcome=FAILED_BEFORE_EVALUATION`) ghi nhận; A2 (evaluation_attempt_id=A2, CÙNG key (S,C), `attempt_outcome=DECIDED`) ghi nhận sau đó — HỢP LỆ, KHÔNG mâu thuẫn với A1 (§2/§4, FAILED_BEFORE_EVALUATION tường minh retryable); D1 (`causation_refs` chứa A2, cùng key) ghi theo sau A2.

**Scenario 14 — Same attempt retry (đóng `C4-DELTA-MAJ-02`):** Retry `evaluation_attempt_id=A1` với payload giống hệt → trả về A1 đã tồn tại (idempotent no-op). Retry `evaluation_attempt_id=A1` với payload KHÁC → deterministic conflict, reject (§2/§13 `decision_evaluation_attempt_idempotency_policy`).

**Scenario 15 — Multiple successful attempts (đóng `C4-DELTA-MAJ-02`, Scenario 4):** A1 DECIDED → D1 (key S,C). A2 DECIDED tại CÙNG key (evaluation_attempt_id KHÁC A1) — PHẢI resolve/reuse D1 nếu evidence giống hệt (Decision-layer idempotency, §1/§13 `decision_computation_idempotency_policy`), hoặc deterministic conflict nếu evidence khác. A2 TUYỆT ĐỐI KHÔNG được tạo D2 trừ khi D1 ĐÃ invalidate VÀ correction lineage (§11) cho phép (Scenario 5 dưới).

**Scenario 16 — No attempt (đóng `C4-MAJ-04`, tái xác nhận):** KHÔNG có `DecisionEvaluationAttemptRecorded` nào tồn tại cho một logical key — trạng thái này PHẢI phân biệt được tường minh với BẤT KỲ attempt đã ghi nhận nào (kể cả `INELIGIBLE`/`INPUT_UNAVAILABLE`/`FAILED_BEFORE_EVALUATION`) — absence hoàn toàn (chưa từng thử) ≠ một attempt fact THẬT với outcome không dẫn tới Decision (§2/§4, Scenario 3–5).
