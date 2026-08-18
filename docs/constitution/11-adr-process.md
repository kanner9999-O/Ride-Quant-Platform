---
id: 11-adr-process
title: ADR Process
version: "2.2"
status: Draft
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: null
next_review: null
depends_on: ["00-governance", "02-platform-invariants"]
---

# 11. ADR Process

Chapter 11 khóa quy trình và metadata contract của ADR. Document Lifecycle, Freeze Policy và ADR Scope Rule thuộc [Chapter 0](./00-governance.md); authority mapping thuộc [I-12](./02-platform-invariants.md).

> **Governance migration CANDIDATE (v2.2, CHƯA activate):** §11.5/§11.9 dưới đây LÀ candidate, chuẩn bị kích hoạt mô hình đã được Product Owner approve tại [ADR-031](../adr/ADR-031.md) (Approved) — cùng nội dung Mode A/Mode B với [Chapter 0 §3 v1.2 candidate](./00-governance.md). CHƯA active — active CHỈ tại Atomic Activation Boundary riêng biệt, cùng lúc với Chapter 0 §3, khi TOÀN BỘ artifact mandatory (Chapter 0 §3, Chapter 11 §11.5, Chapter 11 §11.9) đồng bộ VÀ Product Owner approve trong CÙNG một hành động (KHÔNG partial activation). Trước boundary đó, v2.1's principal-only rule VẪN nguyên vẹn có hiệu lực.

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

- tối thiểu hai independent reviews;
- reviewer giữ role `AI Technical Architect` tại review boundary — role eligibility thuộc về principal (đúng Chapter 0 §3), execution/session kế thừa eligibility từ principal, KHÔNG có role riêng;
- independence được thỏa bởi Mode A (`DISTINCT_PRINCIPAL` — hai principal khác nhau) HOẶC Mode B (`SAME_PRINCIPAL_DISTINCT_EXECUTION` — cùng principal, hai execution cô lập, CHỈ khi execution-isolation evidence contract [ADR-031](../adr/ADR-031.md) §5 thỏa đầy đủ);
- reviewer identity (principal identity, execution identity nếu Mode B, review boundary, independence mode) được pin;
- reviewer ngang hàng, không veto;
- Product Owner là authority duy nhất approve/reject.

Validator kiểm tra eligibility và consistency, không phải approval authority.

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
- minimum-two eligible independent review EXECUTIONS (KHÔNG chỉ "reviewer," đúng principal-vs-execution distinction, [ADR-031](../adr/ADR-031.md));
- mỗi execution resolve được: principal identity, role (`AI Technical Architect`), review boundary, independence mode;
- Mode A: hai principal identity khác nhau;
- Mode B: hai execution cô lập của CÙNG principal ĐÚNG execution-isolation evidence contract (ADR-031 §5) — bao gồm distinct execution identifier VÀ explicit isolation attestation; một nhãn tự do một mình KHÔNG đủ;
- `depends_on` tồn tại, Approved, acyclic;
- `resolves` khớp MANIFEST OQ transition;
- `supersedes` khớp MANIFEST current state/reverse relation;
- Approved ADR file không bị mutate;
- MANIFEST không stale;
- fail-closed: nếu independence mode (Mode A HOẶC Mode B) KHÔNG resolve đầy đủ tại review boundary, validator BÁO eligibility incomplete — KHÔNG tự suy diễn pass.

Tooling/operator cụ thể defer Phase 1.

## 11.10 Quy tắc bắt buộc

- Quyết định kiến trúc mới hoặc thay đổi quyết định phase trước phải có ADR theo Chapter 0 §4b.
- Không phase nào Approved nếu còn quyết định kỹ thuật quan trọng chưa thành ADR.
- Không phase nào tự sửa quyết định phase trước ngoài governance workflow.
- Không partial activation.

## 11.11 Ngoài phạm vi

Implementation validator/CI, storage/index format và workflow automation chi tiết thuộc Phase 1.
