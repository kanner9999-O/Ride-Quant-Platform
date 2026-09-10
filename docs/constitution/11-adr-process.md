---
id: 11-adr-process
title: ADR Process
version: "2.3"
status: Locked
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: Product Owner
approved_at: "2026-09-10T15:51+07:00"
created_at: "2026-07-16"
last_review: "2026-09-10"
next_review: null
depends_on: ["00-governance", "02-platform-invariants"]
---

# 11. ADR Process

Chapter 11 khóa quy trình và metadata contract của ADR. Document Lifecycle, Freeze Policy và ADR Scope Rule thuộc [Chapter 0](./00-governance.md); authority mapping thuộc [I-12](./02-platform-invariants.md).

> **Governance migration (v2.2, historical — controlling from 2026-08-18T17:25:00+07:00 until the v2.3 boundary below):** §11.5/§11.9 dưới đây kích hoạt mô hình đã được Product Owner approve tại [ADR-031](../adr/ADR-031.md) (Approved) — cùng nội dung Mode A/Mode B với [Chapter 0 §3 v1.2](./00-governance.md) (Locked, cùng activation boundary). Atomic Activation Boundary (ADR-031 §11) hoàn tất TẠI ĐÚNG activation commit này, đồng bộ CÙNG Chapter 0 §3 và Chapter 12 (v1.6, Locked) — Product Owner decision nguyên văn "ACTIVATE ADR-031 GOVERNANCE MIGRATION," 2026-08-18T17:25:00+07:00. Đoạn này giữ nguyên như bằng chứng lịch sử chính xác của migration đó; KHÔNG còn mô tả mô hình đang controlling kể từ boundary v2.3 dưới đây trở đi — current lifecycle/model state authoritative tại MANIFEST theo I-12.
>
> **Governance migration (v2.3, ACTIVE):** §11.5/§11.9 dưới đây kích hoạt mô hình đã được Product Owner approve tại [ADR-042](../adr/ADR-042.md) (Approved) — cùng nội dung với [Chapter 0 §3 v1.3](./00-governance.md) (Locked, cùng activation boundary). Atomic Activation Boundary hoàn tất TẠI ĐÚNG activation commit này, đồng bộ CÙNG Chapter 0 §3, [Chapter 12](./12-approval-gates.md) (v1.7, Locked), ADR template, Global Execution Rules (v0.6, EFFECTIVE), Phase-3 rules (v0.3, EFFECTIVE), và MANIFEST — retire `ADR-031` Mode A/Mode B như mandatory approval-eligibility mechanism, thay bằng Review A mandatory + Risk Classification (R0/R1/R2) + optional advisory cross-check tại R2 (Product Owner chọn). `ADR-031` KHÔNG bị sửa (bất biến, Chapter 11 §11.3); định nghĩa của nó vẫn còn giá trị lịch sử; current lifecycle state của nó nay `Superseded` (bởi `ADR-042`), ghi tại MANIFEST theo I-12. Product Owner decision nguyên văn: "APPROVE ADR-042 v0.5 AND ITS ATOMIC GOVERNANCE ACTIVATION at reviewed semantic boundary 64fc05becc6ca4245229db79b3fb6c5d9187e622, based on current main e975d44f813b1ee91d2dbf3793376ca1827dc0f1," `2026-09-10T15:51+07:00`.

## 11.1 Template và phạm vi

Canonical template: [`/docs/templates/adr-template.md`](../templates/adr-template.md).

Mỗi ADR là một file riêng trong `/docs/adr/`, gồm tối thiểu: Context, Decision, Alternatives considered, Concerns/Risks, Scale check và Consequences.

## 11.2 ADR identity

- Một authority cấp số ADR cho toàn repo.
- ADR number là identity duy nhất, vĩnh viễn.
- Số đã cấp không được tái sử dụng.
- ADR đã rời `Draft` không được renumber.
- Path là file convention; authority của identity là số ADR.

## 11.3 Immutability boundary

Tại Product Owner approval boundary, toàn bộ ADR file immutable byte-for-byte:

- decision content bất biến;
- frontmatter bất biến;
- approval metadata bất biến;
- `status` trong file là approval snapshot;
- không thêm `superseded_by`, `deprecated_at` hoặc metadata khác vào ADR cũ.

Current lifecycle state và reverse supersession relation thuộc MANIFEST.

## 11.4 Metadata contract

| Field | Semantic |
|---|---|
| `version` | Draft revision được review; bất biến sau approval |
| `status` | Authoring/approval snapshot; tại approval phải là `Approved` |
| `reviewers` | Actor identities đã review boundary; historical evidence |
| `addresses` | OQ ADR đang xử lý; không đổi current OQ state |
| `resolves` | Evidence rằng ADR approval là transition cause đóng OQ |
| `depends_on` | Dependency phải Approved trước approval boundary hiện tại |
| `supersedes` | Forward relation từ ADR mới tới ADR cũ |

`superseded_by` không thuộc canonical ADR schema. Reverse lookup nằm tại MANIFEST hoặc derived index.

`depends_on` phải acyclic.

## 11.5 Review and acceptance gate

Trước Product Owner decision:

- Review A bắt buộc — reviewer giữ role `AI Technical Architect` tại review boundary; role eligibility thuộc về principal (đúng Chapter 0 §3), execution/session kế thừa eligibility từ principal, KHÔNG có role riêng; Review A phải độc lập kiểm tra trực tiếp candidate/repository authority, không kế thừa kết luận Executor làm ground truth;
- Risk Classification bắt buộc, ngay sau Review A — đúng một trong R0/R1/R2 (định nghĩa đầy đủ tại [ADR-042](../adr/ADR-042.md)); R0/R1 mặc định `NO CROSS-CHECK`; R2: Review A recommend optional cross-check, KHÔNG BAO GIỜ tự động yêu cầu, Product Owner chọn `CROSS-CHECK` hoặc `PROCEED WITHOUT CROSS-CHECK`;
- optional cross-check (chỉ R2, chỉ khi Product Owner chọn): advisory only, không veto, KHÔNG approval prerequisite, KHÔNG cần persisted transcript/evidence/execution-ID, KHÔNG cần Mode A/Mode B bookkeeping; vắng mặt KHÔNG BAO GIỜ làm mất điều kiện approval;
- reviewer identity (principal identity, role, review boundary) của Review A được pin;
- reviewer ngang hàng, không veto;
- Product Owner là authority duy nhất approve/reject.

Validator kiểm tra eligibility và consistency (Review A resolved, Risk Classification resolved đúng một R0/R1/R2), không phải approval authority — không kiểm tra cross-check existence/choice/evidence (§11.9 dưới).

## 11.6 Approval transition phải atomic

Approve một ADR là một documentation change duy nhất:

- ADR final draft → `status: Approved`;
- set `approved_by` / `approved_at`;
- pin reviewer evidence;
- `addresses` / `resolves` phản ánh đúng evidence;
- MANIFEST cập nhật current ADR state;
- nếu có OQ transition, MANIFEST cập nhật cùng change;
- nếu supersede ADR cũ, MANIFEST cập nhật old-state và reverse relation cùng change.

Không được approve ADR trước rồi cập nhật MANIFEST/OQ ở change sau. Sau approval, ADR file không được sửa lại.

## 11.7 Authority của OQ status

Theo I-12:

- MANIFEST là authority cho current OQ state;
- ADR là authority cho architecture decision và evidence/transition cause;
- `ADR.resolves` không tự ghi đè MANIFEST;
- lệch nhau là integrity violation; tooling không âm thầm ghi đè;
- dashboard/index rebuild current OQ state từ MANIFEST.

ADR supersede không tự động mở lại OQ; ADR thay thế và MANIFEST phải khai báo rõ OQ tiếp tục `Resolved` hay trở lại `Open`.

## 11.8 Supersede và deprecate

### Supersede

Atomic change gồm:

- ADR mới Approved với `supersedes: [ADR-cũ]`;
- MANIFEST ghi ADR cũ `Superseded`;
- MANIFEST ghi reverse relation;
- MANIFEST ghi ADR mới current state;
- OQ transition, nếu có, cập nhật cùng change.

ADR cũ không bị mutate.

### Deprecate không có ADR thay thế

MANIFEST đổi current state ADR cũ thành `Deprecated`, kèm rationale/evidence reference. ADR file cũ không bị mutate.

## 11.9 Validator contract

Validator là blocking consistency gate, không phải approval authority.

Tối thiểu kiểm tra:

- ADR number unique, không reuse;
- đúng một Review A execution resolve được: principal identity, role (`AI Technical Architect`), review boundary;
- Risk Classification present và resolve đúng một trong R0/R1/R2 (định nghĩa [ADR-042](../adr/ADR-042.md));
- `depends_on` tồn tại, Approved, acyclic;
- `resolves` khớp MANIFEST OQ transition;
- `supersedes` khớp MANIFEST current state/reverse relation;
- Approved ADR file không bị mutate;
- MANIFEST không stale;
- fail-closed CHỈ khi: Review A execution KHÔNG resolve được, HOẶC Risk Classification KHÔNG resolve đúng một R0/R1/R2 — validator BÁO eligibility incomplete, KHÔNG tự suy diễn pass.
- **KHÔNG kiểm tra** (đã retire kể từ activation này): cross-check existence, absence, invocation choice, reviewer identity, transcript, evidence, execution/session ID, hoặc result của một optional cross-check — đây KHÔNG BAO GIỜ là approval-eligibility input; validator KHÔNG BAO GIỜ fail vì một optional cross-check hoặc cross-check-choice record vắng mặt. Mode A/Mode B ([ADR-031](../adr/ADR-031.md), Approved, bất biến) không còn là validator-checked eligibility mechanism — định nghĩa của nó vẫn còn giá trị lịch sử/tham khảo nếu một cross-check muốn tự mô tả provenance, nhưng validator KHÔNG BAO GIỜ yêu cầu nó.

Tooling/operator cụ thể defer Phase 1.

**Non-retroactivity / bootstrap boundary (`ACT-A-MAJ-03` remediation — bắt buộc tường minh, tránh self-bootstrap contradiction tại chính activation boundary này):**

- Validator criteria mới ở trên (Review A execution + Risk Classification) áp dụng **prospectively** — CHỈ cho decision được govern bởi model này TỪ SAU activation boundary trở đi (đồng bộ atomic cùng [ADR-042](../adr/ADR-042.md), MANIFEST, và toàn bộ amendment bundle, đúng [ADR-042](../adr/ADR-042.md)'s Migration).
- ADR/approval-gate decision đã hoàn tất TRƯỚC activation boundary VẪN valid dưới đúng review rule effective tại original approval boundary của nó (Mode A/Mode B, minimum-two-review) — KHÔNG bị đòi hỏi hồi tố R0/R1/R2 Risk Classification, KHÔNG bị re-open, KHÔNG bị re-review.
- Historical two-review evidence (existing "Independent reviews" table trong ADR cũ, MANIFEST review-evidence record) giữ nguyên valid, KHÔNG bị rewrite hay re-verify bởi validator criteria mới.
- Chính [ADR-042](../adr/ADR-042.md)'s own approval/activation transaction được govern bởi mandatory-two-review model **effective TRƯỚC activation boundary này** (Chapter 0 §3/Chapter 11 §11.5/§11.9 pre-activation text, [ADR-031](../adr/ADR-031.md) Mode A/Mode B) — KHÔNG BAO GIỜ bởi chính validator criteria mới nó tạo ra ([ADR-042](../adr/ADR-042.md) tự nói rõ: "this ADR is not used to bootstrap its own rules"). Validator criteria mới CHỈ bắt đầu áp dụng cho decision SAU đúng activation boundary đó — never for ADR-042's own approval decision itself.
- KHÔNG validator nào được invalidate một approval lịch sử CHỈ VÌ nó thiếu Risk Classification hoặc dùng legacy two-review evidence — thiếu hai điều đó KHÔNG PHẢI một fail-closed condition cho decision đã hoàn tất trước activation boundary.

## 11.10 Quy tắc bắt buộc

- Quyết định kiến trúc mới hoặc thay đổi quyết định phase trước phải có ADR theo Chapter 0 §4b.
- Không phase nào Approved nếu còn quyết định kỹ thuật quan trọng chưa thành ADR.
- Không phase nào tự sửa quyết định phase trước ngoài governance workflow.
- Không partial activation.

## 11.11 Ngoài phạm vi

Implementation validator/CI, storage/index format và workflow automation chi tiết thuộc Phase 1.
