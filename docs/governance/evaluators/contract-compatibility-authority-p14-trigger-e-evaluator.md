---
id: contract-compatibility-authority-p14-trigger-e-evaluator
title: "Evaluator Implementation/Procedure — contract-compatibility-authority — Package 1.4 Trigger E"
implementation_version: "1.1"
implementation_status: Active
evaluator_module: contract-compatibility-authority
owner: Product Owner
established_by: Product Owner
established_at: "2026-08-10"
superseded_by: null
---

# Evaluator Implementation/Procedure — `contract-compatibility-authority` — Package 1.4 Trigger E

**Vai trò của tài liệu này:** đây LÀ evaluator implementation/procedure manifest (Chapter 10 [§10.4.1](../../constitution/10-compatibility-capability-contract.md) — "evaluator implementation version + exact artifact hoặc immutable manifest") — KHÔNG PHẢI executable production code, KHÔNG PHẢI một runtime service, KHÔNG PHẢI một ADR, KHÔNG thay đổi Declaration ([ADR-023](../../adr/ADR-023.md) §4.1/§5) hay Grant ([`contract-compatibility-authority-p14-trigger-e-grant.md`](../grants/contract-compatibility-authority-p14-trigger-e-grant.md) v1.0). Tài liệu này định nghĩa CHÍNH XÁC procedure deterministic mà evaluator sẽ dùng để sinh Package 1.4 Trigger E Compatibility Result trong một transaction governed TƯƠNG LAI — KHÔNG tự thực hiện evaluation, KHÔNG tạo Compatibility Result tại đây.

**v1.1 — bounded correction (2026-08-10), sửa một semantic defect tại v1.0's Input 1 resolution rule, KHÔNG modify Compatibility Result #001 (bất biến historical evidence), KHÔNG tạo ADR-024, KHÔNG sửa ADR-022/ADR-023/Package 1.1/Package 1.4/Grant document, vai trò: `P1.4 Trigger E Evaluator v1.1 Bounded Correction Executor`:** v1.0's §4 Input 1 SAI khi yêu cầu previous comparison subject PHẢI tự nó từng LÀ policy-root-active component theo ADR-022 §5.2 TẠI thời điểm nó áp dụng — ADR-022 KHÔNG yêu cầu điều đó. ADR-022 §4.1 tường minh xác định v0.7 LÀ historical pre-alignment subject (tồn tại TRƯỚC KHI ADR-022 approve, KHÔNG BAO GIỜ policy-governed tại thời điểm publish của chính nó); §5.2 CHỈ yêu cầu artifact HIỆN TẠI (current, v0.8) + Chapter 10 hợp thành active policy root TẠI evaluation boundary — đây LÀ policy applicability requirement cho SUBJECT ĐANG được đánh giá, KHÔNG PHẢI một điều kiện lịch sử áp lên baseline so sánh. Phân biệt đúng: **comparison subject identity ≠ policy applicability identity**. Sửa: §4 Input 1 nay resolve previous subject LÀ `api-architecture.md` v0.7 (exact historical blob `fb2a4a4a04c20d373227d92869abe7cb99f59db0`, commit `0c09903` — trạng thái Consolidated Stable NGAY TRƯỚC KHI ADR-022 alignment transition sang v0.8, resolved từ repository authority git-verified) — KHÔNG còn yêu cầu v0.7 tự nó từng policy-root-active; v0.7 CHỈ cần LÀ một exact-pinned historical artifact identity hợp lệ (KHÔNG mutable reference). **KHÔNG đổi:** Input 2 (current subject, v0.8, blob `b79493e44daf5154333068454d565cb8053ed7dd`) VẪN PHẢI policy-root-active TẠI evaluation boundary theo ADR-022 §5.2 (§6 KHÔNG đổi) — CHỈ subject ĐANG được judge mới cần policy-governed NGAY TẠI evaluation boundary, KHÔNG PHẢI historical baseline; Input 3–6 (§4); bốn comparison dimension (§5); backward-only compatibility rule (§6); sáu-case reason classification (§7); determinism/replay guarantee (§8); fail-closed behavior (§9); scope exclusions (§3); tất cả KHÔNG đổi. Compatibility Result #001 (`governance/compatibility-results/p14-trigger-e-compatibility-result-001.md`) VẪN bất biến, KHÔNG sửa — Result đó cite implementation v1.0 tại đúng thời điểm nó tạo, VẪN LÀ historical evidence hợp lệ dưới identity v1.0 của chính nó (đúng nguyên tắc §8: một evaluation MỚI dùng v1.1 sẽ sinh Result identity MỚI, KHÔNG hồi tố Result cũ). `module-registry.yaml`/`system-decomposition.md`/`api-architecture.md`/ADR-022/ADR-023/Grant document KHÔNG sửa tại transaction này (byte-identical, git diff empty). `QG-P14-E-EVID-01`/`G2-RDY-BLK-03` VẪN open, Phase 1 Quality Gate VẪN `FAIL — evidence`, Gate 2 VẪN CLOSED — transaction này KHÔNG tạo Compatibility Result mới, KHÔNG rerun Quality Gate.

## 1. Purpose

Đóng đúng prerequisite còn thiếu của Chapter 10 §10.4.1's provenance checklist cho Compatibility Result tương lai: **evaluator implementation version + exact artifact hoặc immutable manifest**. Trước tài liệu này, evaluator module (Declaration) VÀ evaluator Grant ĐÃ tồn tại, NHƯNG KHÔNG một artifact nào pin CHÍNH XÁC evaluator sẽ tính toán compatibility judgment NHƯ THẾ NÀO — thiếu artifact này, một Compatibility Result tương lai sẽ KHÔNG thể pin "evaluator implementation version + exact artifact" theo đúng yêu cầu, VÀ sẽ KHÔNG deterministic/replayable (§10.4.1 mục "grant artifact tồn tại ≠ grant đang có hiệu lực", nguyên tắc tương tự áp dụng cho implementation artifact).

## 2. Implementation identity

```text
implementation_id:       contract-compatibility-authority-p14-trigger-e-evaluator
implementation_version:  "1.1"
implementation_status:   Active
content identity:        git blob hash của CHÍNH file này — resolvable/pinned tại
                          docs/MANIFEST.md (I-12 tracking convention, GIỐNG HỆT mọi
                          artifact khác — KHÔNG khác biệt đặc quyền; MANIFEST CHỈ
                          tracking identity/version/blob, KHÔNG phải authority cho
                          nội dung procedure — cùng phân biệt đã dùng cho Grant
                          document, §5 của chính nó).
evaluator_module:         contract-compatibility-authority (module_type:
                          compute_engine, Package 1.1 v1.1, Consolidated Stable).
bound Grant:              contract-compatibility-authority-p14-trigger-e-grant
                          v1.0 (Active, unrevoked, blob
                          b45e8efe313749c0809440b259d1517bfe1c8ea0) — procedure này
                          CHỈ hợp lệ để dùng KHI Grant đó ĐANG active/unrevoked TẠI
                          evaluation boundary (§9 dưới) — implementation artifact
                          KHÔNG tự cấp quyền, `module identity ≠ evaluator grant`
                          VẪN giữ nguyên.
```

## 3. Authorized scope (đúng SUBSET của Declaration §5 VÀ Grant §4 — KHÔNG mở rộng)

Procedure này CHỈ được phép áp dụng cho đúng phạm vi ADR-023 §5 VÀ Grant v1.0 §4 đã cấp — KHÔNG một phạm vi nào rộng hơn. Xem trực tiếp [ADR-023 §5](../../adr/ADR-023.md) và [Grant §4](../grants/contract-compatibility-authority-p14-trigger-e-grant.md) — KHÔNG lặp lại danh sách tại đây (tránh hai nguồn lệch nhau, I-12) — CHỈ tham chiếu.

## 4. Input resolution rules (exact-pin bắt buộc — KHÔNG mutable `latest`/`current` reference)

```text
Input 1 — Previous Package 1.4 published-contract semantic artifact:
  Resolution:  chính xác MỘT `api-architecture.md` version/content-identity
               (blob) LÀ historical prior comparison subject — PHẢI cite exact
               version number VÀ exact blob, resolved từ repository authority
               (git-verified), KHÔNG "previous"/"prior"/"last" như một
               reference tự do. **(v1.1, sửa v1.0's over-broad rule):**
               comparison subject identity ≠ policy applicability identity —
               subject này KHÔNG cần tự nó từng LÀ policy-root-active
               component theo ADR-022 §5.2 TẠI thời điểm nó publish (ADR-022
               KHÔNG yêu cầu điều đó; §4.1 tường minh xác định v0.7 LÀ
               historical pre-alignment subject, tồn tại TRƯỚC KHI ADR-022
               approve). Subject CHỈ cần LÀ một artifact identity đã published
               hợp lệ, exact-pinned, KHÔNG mutable.
  Fail-closed: nếu KHÔNG version/blob nào resolve được từ repository authority
               LÀM previous subject (vd đây LÀ Package 1.4 artifact ĐẦU TIÊN
               từng publish, chưa có "previous" nào tồn tại) → evaluation
               KHÔNG thể chứng minh backward compatibility (KHÔNG có baseline
               để so) → reason "insufficient evidence / unable to evaluate"
               (§7), KHÔNG "proved compatible".

Input 2 — Current Package 1.4 published-contract semantic artifact:
  Resolution:  chính xác MỘT `api-architecture.md` version/content-identity
               (blob) đang policy-root-active THEO MANIFEST TẠI evaluation
               boundary (ADR-022 §5.2 điều kiện mục 2, MANIFEST-resolved) —
               PHẢI exact-pin version/blob TẠI thời điểm evaluation, KHÔNG một
               reference "current"/"latest" tự cập nhật.

Input 3 — Chapter 10 policy artifact:
  Resolution:  Chapter 10 (`docs/constitution/10-compatibility-capability-
               contract.md`) exact content identity, `status: Locked`,
               MANIFEST-resolvable (ADR-022 §5.2 điều kiện mục 1) TẠI evaluation
               boundary — PHẢI exact-pin version/blob hiện hành tại thời điểm
               đó (hiện tại: v2.7, blob
               016e46bcad0826e983a51ee24c8ec4c3217aeba1 — KHÔNG giả định giữ
               nguyên vĩnh viễn, evaluation TƯƠNG LAI PHẢI re-resolve tại chính
               thời điểm nó chạy).

Input 4 — ADR-022 compatibility commitment/policy-root authority:
  Resolution:  ADR-022 (`docs/adr/ADR-022.md`) exact content identity,
               `status: Approved`, `version: "0.3"` — PHẢI exact-pin blob hiện
               hành (049a3d941493a0fcb3a0f44733f17534e158f9b0) TẠI evaluation
               boundary; §3.2 (backward-only commitment) VÀ §4.1 (policy root
               composition) LÀ nguồn duy nhất cho compatibility rule (§6 dưới).

Input 5 — Applicable policy authority/applicability facts:
  Resolution:  MANIFEST.md's dòng cho CẢ Input 3 VÀ Input 2, xác nhận ĐỒNG THỜI
               CẢ HAI điều kiện mục 1 VÀ mục 2 của ADR-022 §5.2 TẠI evaluation
               boundary — nếu KHÔNG CẢ HAI điều kiện đồng thời thỏa, policy root
               INCOMPLETE → fail closed (§7, "invalid declaration"/"unresolvable
               reference" tùy tình huống cụ thể).

Input 6 — Evaluator Grant v1.0 và trạng thái activation/applicability:
  Resolution:  đọc trực tiếp `grant_status`/`revoked`/`revoked_at` field của
               `contract-compatibility-authority-p14-trigger-e-grant.md` TẠI
               evaluation boundary — PHẢI exact-pin grant_version + blob ĐANG
               active tại thời điểm đó; NẾU `revoked: true` HOẶC một Grant
               version mới hơn đã supersede bản đang cite → evaluation KHÔNG
               được thực hiện dưới Grant đó (fail closed, §7 "invalid
               declaration").
```

## 5. Comparison procedure (deterministic, đúng bốn dimension đã authorized — KHÔNG hơn)

Cho hai artifact content identity đã exact-pin (Input 1, Input 2), procedure so sánh ĐÚNG BỐN dimension sau, theo đúng thứ tự, mỗi dimension độc lập:

```text
Dimension 1 — Route existence:
  Với mỗi command/query/event route CÓ trong Input 1 (previous): route đó CÓ
  còn tồn tại (cùng route identity) trong Input 2 (current) không? Route bị
  loại bỏ khỏi Input 2 mà KHÔNG thuộc một deprecation cycle đã cam kết (Chapter
  10 §10.3's "gỡ bỏ deprecated element là breaking") → breaking.

Dimension 2 — Routing/module ownership semantics:
  Với mỗi route tồn tại ở CẢ hai artifact: module sở hữu/route đích của route
  đó trong Input 1 CÓ giữ nguyên trong Input 2 không? Đổi module ownership của
  một route đã published (KHÔNG PHẢI internal refactor minh bạch với consumer)
  → breaking.

Dimension 3 — Authoritative vs non-authoritative classification:
  Với mỗi route/module tồn tại ở CẢ hai artifact: phân loại authoritative/
  non-authoritative (đúng `owns_authoritative_state`, tham chiếu module-
  registry.yaml TẠI evaluation boundary, KHÔNG tự invent) CÓ giữ nguyên không?
  Đổi phân loại này của một route đã published → breaking (đổi authority
  semantics mà consumer đã tin cậy).

Dimension 4 — Published outcome-type semantics:
  Với mỗi route tồn tại ở CẢ hai artifact: bộ outcome-type đã published
  (`PASSED / FAILED / INDETERMINATE`, `MATCH / MISMATCH / INDETERMINATE`, v.v.)
  CÓ giữ nguyên hoặc SUPERSET (chỉ thêm outcome mới, KHÔNG xóa/đổi nghĩa outcome
  cũ) không? Xóa/redefine một outcome-type đã published → breaking; thêm một
  outcome-type MỚI, KHÔNG đổi outcome cũ → KHÔNG breaking (backward-compatible
  bổ sung).

Explicit exclusion: field-level schema KHÔNG được so sánh — Package 1.4 KHÔNG
  có concrete field-level schema contract tại Phase 1 scope (`api-architecture.
  md` frontmatter title, ADR-022 §4 mục 1 đã xác nhận) — so sánh field-level LÀ
  ngoài phạm vi procedure này, KHÔNG được thêm bởi bất kỳ evaluation nào dùng
  procedure v1.1 này.
```

## 6. Compatibility rule (backward-only, đúng ADR-022 §3.2 — KHÔNG redefine)

```text
Commitment:  backward compatibility ONLY (ADR-022 §3.2, KHÔNG đổi).
Rule:        Input 2 (current) ĐƯỢC coi backward-compatible VỚI Input 1
             (previous) KHI VÀ CHỈ KHI CẢ BỐN dimension (§5) KHÔNG breaking.
             MỘT dimension breaking DUY NHẤT → toàn bộ kết luận `eligible:
             false` (KHÔNG "một phần compatible" — Chapter 10 §10.4 mục 5 cấm
             trạng thái "một phần" ngầm).
Forward/both compatibility: KHÔNG đánh giá — ngoài commitment đã pin (ADR-022
             §3.2, KHÔNG mở rộng bởi procedure này).
```

## 7. Result semantics (eligible + reason classification — đúng Chapter 10 §10.4.2)

```text
eligible: true   KHI VÀ CHỈ KHI CẢ BỐN dimension (§5) KHÔNG breaking, VÀ tất cả
                  sáu Input (§4) resolve được thành công, VÀ Grant (Input 6)
                  active/unrevoked/đúng scope tại evaluation boundary.
                  reason: "đã chứng minh tương thích" (proved compatible).

eligible: false  áp dụng CHÍNH XÁC một trong sáu reason sau (Chapter 10
                  §10.4.2, KHÔNG trộn lẫn):
  - "đã chứng minh tương thích" ngược lại — "đã chứng minh không tương thích"
    (proved incompatible): ÍT NHẤT một dimension (§5) breaking, VÀ toàn bộ
    Input resolve thành công.
  - "không đủ evidence / không đánh giá được" (insufficient evidence/unable to
    evaluate): Input 1 (previous baseline) KHÔNG resolve được (§4 Input 1
    fail-closed case), HOẶC một dimension KHÔNG thể xác định do dữ liệu thiếu
    (KHÔNG PHẢI do breaking THẬT SỰ).
  - "khai báo invalid" (invalid declaration): Grant (Input 6) revoked, sai
    scope, hoặc CHƯA active tại evaluation boundary; HOẶC policy root (Input
    5) KHÔNG đồng thời thỏa cả hai điều kiện ADR-022 §5.2.
  - "reference không resolve được" (unresolvable reference): Input 2, 3, hoặc
    4 KHÔNG resolve được exact version/blob tại MANIFEST (vd blob không tồn
    tại/mutable reference bị dùng nhầm).
  - "policy mismatch" (policy mismatch): compatibility rule-set version được
    evaluation cite KHÔNG khớp policy root version ĐANG active tại MANIFEST
    (Input 3/5) tại đúng evaluation boundary.

KHÔNG trạng thái "một phần" nào — mọi kết luận NGOÀI đúng sáu case trên LÀ
  KHÔNG hợp lệ theo procedure v1.1 này.
```

## 8. Determinism / replay guarantee

```text
Given identical pinned inputs (Input 1–6, §4, đúng exact version/blob) VÀ
  cùng implementation_version ("1.1") CỦA CHÍNH tài liệu này → evaluator PHẢI
  sinh CÙNG MỘT kết luận (eligible + reason) — KHÔNG phụ thuộc thời điểm chạy
  lại, KHÔNG phụ thuộc runtime state không được represent trong pinned
  evidence, KHÔNG phụ thuộc diễn giải hội thoại/tác nhân thực hiện.
Procedure v1.1 này KHÔNG BAO GIỜ mutate dưới cùng implementation_version
  identity (đúng Chapter 10 §10.4.3 mục 5's lifecycle-transition-authoritative
  rule, áp dụng tương tự cho evaluator implementation artifact) — một thay đổi
  procedure BẮT BUỘC một implementation_version MỚI (§10 dưới), KHÔNG sửa file
  này tại chỗ dưới `1.1`. Cùng nguyên tắc ĐÃ áp dụng cho v1.0 (lịch sử, KHÔNG
  còn mutate — vẫn LÀ identity cite bởi Compatibility Result #001).
Re-evaluation SAU một pinned input đổi (vd artifact mới, policy mới, Grant
  mới) sinh một Compatibility Result MỚI, KHÔNG sửa/hồi tố result lịch sử
  (đúng Chapter 10 §10.4.4, "đánh giá lại sinh result MỚI, không sửa lịch sử").
```

## 9. Fail-closed behavior (I-6)

```text
Bất kỳ Input nào (§4) KHÔNG resolve được exact version/content-identity tại
  evaluation boundary → evaluation DỪNG, KHÔNG issue `eligible: true`, chọn
  reason classification tương ứng (§7) — KHÔNG BAO GIỜ suy diễn/giả định một
  giá trị pinned nào thiếu.
Grant (Input 6) revoked/sai scope/chưa active tại evaluation boundary →
  evaluation DỪNG, `eligible: false`, reason "khai báo invalid" — evaluation
  KHÔNG được thực hiện dưới một Grant không hợp lệ dù mọi Input khác resolve
  thành công.
Đây LÀ default fail-safe (I-6) — KHÔNG một exception nào được author bởi
  procedure v1.1 này.
```

## 10. What this artifact does NOT do

```text
KHÔNG thực hiện evaluation tại transaction này — KHÔNG Compatibility Result
  nào tạo (đó LÀ một transaction governed riêng biệt, tương lai, cite CHÍNH
  XÁC implementation_id/version của tài liệu này).
KHÔNG thay đổi Declaration (ADR-023 §4.1/§5) hay Grant (§4 của Grant document)
  — CHỈ định nghĩa procedure sẽ được dùng bên trong scope ĐÃ cấp.
KHÔNG tạo/sửa architecture responsibility — module-registry.yaml/system-
  decomposition.md KHÔNG sửa (byte-identical, git diff empty).
KHÔNG sửa ADR-022/ADR-023/api-architecture.md/Grant document (byte-identical).
KHÔNG rerun Phase 1 Quality Gate — QG-P14-E-EVID-01/G2-RDY-BLK-03 KHÔNG đổi
  (VẪN OPEN), Gate 2 VẪN CLOSED, Phase 2 VẪN NOT AUTHORIZED.
KHÔNG author Enforcement (runtime authority)/Verification (I-7 checks) — VẪN
  deferred tới implementation stage, đúng ADR-023 §9 (KHÔNG đổi).
```

## 11. Relationship / citations

[`ADR-022`](../../adr/ADR-022.md) v0.3 (Approved) — compatibility commitment (§3.2)/policy root (§4.1)/canonical authority (§5.2), KHÔNG redefine, procedure này CHỈ implement đúng rule ĐÃ pin. [`ADR-023`](../../adr/ADR-023.md) v0.5 (Approved) — Declaration/scope (§4.1/§5), KHÔNG redefine. [`contract-compatibility-authority-p14-trigger-e-grant.md`](../grants/contract-compatibility-authority-p14-trigger-e-grant.md) v1.0 (Active) — Grant mà procedure này CHỈ được dùng dưới đó, KHÔNG tự cấp quyền. [`docs/constitution/10-compatibility-capability-contract.md`](../../constitution/10-compatibility-capability-contract.md) §10.4/§10.4.1/§10.4.2/§10.4.3 (Locked) — nguồn của MỌI provenance/determinism/reason-classification requirement mà procedure này thực thi.

## 12. Change history

```text
v1.0  2026-08-10  Established — vai trò: `Package 1.4 Trigger E Evaluator
      Implementation Artifact Executor`. Evidence/procedure work dưới existing
      Approved authority (ADR-022 v0.3, ADR-023 v0.5) VÀ active Grant v1.0 —
      KHÔNG một quyết định architecture mới, KHÔNG ADR-024. Định nghĩa
      deterministic bốn-dimension compatibility procedure (route existence,
      routing/module ownership, authoritative/non-authoritative classification,
      published outcome-type semantics) cho backward-only commitment (ADR-022
      §3.2), sáu exact-pin input resolution rule, sáu-case reason
      classification (Chapter 10 §10.4.2), fail-closed behavior (I-6). KHÔNG
      field-level schema evaluation. Compatibility Result CHƯA tạo — transaction
      governed riêng biệt tương lai. `QG-P14-E-EVID-01`/`G2-RDY-BLK-03` VẪN
      OPEN, Phase 1 Quality Gate VẪN FAIL — evidence, Gate 2 VẪN CLOSED.

v1.1  2026-08-10  Bounded correction — vai trò: `P1.4 Trigger E Evaluator
      v1.1 Bounded Correction Executor`. Sửa v1.0's §4 Input 1: previous
      comparison subject KHÔNG còn yêu cầu tự nó từng policy-root-active
      (ADR-022 KHÔNG yêu cầu điều đó) — nay resolve LÀ `api-architecture.md`
      v0.7, exact historical blob `fb2a4a4a04c20d373227d92869abe7cb99f59db0`
      (Consolidated Stable, NGAY TRƯỚC ADR-022 alignment sang v0.8). Input 2
      (current subject) VẪN PHẢI policy-root-active tại evaluation boundary
      (KHÔNG đổi). Bốn dimension/backward-only rule/reason classification/
      determinism/fail-closed/scope exclusions KHÔNG đổi. Compatibility Result
      #001 (cite implementation v1.0) VẪN bất biến, KHÔNG sửa — v1.0 identity
      giữ nguyên lịch sử. `module-registry.yaml`/`system-decomposition.md`/
      `api-architecture.md`/ADR-022/ADR-023/Grant document KHÔNG sửa. KHÔNG
      Compatibility Result mới tạo, KHÔNG rerun Quality Gate.
      `QG-P14-E-EVID-01`/`G2-RDY-BLK-03` VẪN OPEN, Gate 2 VẪN CLOSED.
```
