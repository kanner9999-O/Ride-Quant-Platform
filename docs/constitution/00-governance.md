---
id: 00-governance
title: Governance
version: "1.5"
status: Draft
owner: Product Owner
reviewers: [ChatGPT]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: null
next_review: null
depends_on: []
---

# 0. Governance

Chapter 0 — đứng trước cả Vision, vì nó quy định CÁCH mọi quyết định khác được tạo ra.

> **Ghi chú lịch sử:** phiên bản đầu của chương này có luật "Approval 3/3" + Challenge Round (nghi lễ theo vòng) + Devil's Advocate. Sau review của ChatGPT (round 2), các cơ chế này được đơn giản hóa để phù hợp quy mô 1 Product Owner + 2 AI Architect — xem [ADR-005](../adr/ADR-005.md) cho lịch sử quyết định.
>
> **Governance migration:** phiên bản 1.1 kích hoạt mô hình đã được Product Owner chấp thuận tại [ADR-011](../adr/ADR-011.md): ADR file bất biến sau approval, review gate dựa trên role với tối thiểu hai independent reviewers, và MANIFEST là authority cho current ADR/OQ state.
>
> **Governance migration (v1.2, historical — controlling from 2026-08-18T17:25:00+07:00 until the v1.3 boundary below):** phiên bản 1.2 kích hoạt mô hình đã được Product Owner approve tại [ADR-031](../adr/ADR-031.md) (Approved) — mở rộng independent-review eligibility từ principal-only sang Mode A (`DISTINCT_PRINCIPAL`, giữ nguyên preferred khi practical) HOẶC Mode B (`SAME_PRINCIPAL_DISTINCT_EXECUTION`, có execution-isolation evidence contract, ADR-031 §5). Atomic Activation Boundary (ADR-031 §11) hoàn tất TẠI ĐÚNG activation commit này, cùng lúc với Chapter 11 §11.5/§11.9 (v2.2, Locked) và Chapter 12 (v1.6, Locked) wording sync, cùng ADR template evidence-table update — Product Owner decision nguyên văn "ACTIVATE ADR-031 GOVERNANCE MIGRATION," 2026-08-18T17:25:00+07:00. This paragraph is preserved as accurate history of that migration; it no longer describes the currently controlling model from the v1.3 boundary below forward — current lifecycle/model state is authoritative at MANIFEST per I-12.
>
> **Governance migration (v1.3, ACTIVE):** phiên bản 1.3 kích hoạt mô hình đã được Product Owner approve tại [ADR-042](../adr/ADR-042.md) (Approved) — Atomic Activation Boundary hoàn tất TẠI ĐÚNG activation commit này, đồng bộ CÙNG [Chapter 11](./11-adr-process.md) §11.5/§11.9 (v2.3, Locked), [Chapter 12](./12-approval-gates.md) (v1.7, Locked), ADR template, Global Execution Rules (v0.6, EFFECTIVE), Phase-3 rules (v0.3, EFFECTIVE), và MANIFEST (ADR-042's own "single coherent atomic governance action," per its Migration section) — retires the `ADR-031` Mode A/Mode B mandatory-two-independent-review gate above and replaces it with: Review A remains the single mandatory formal technical review; a mandatory Risk Classification step (R0/R1/R2) follows Review A; R2 recommends, but never requires, an optional advisory cross-check chosen by the Product Owner. `ADR-031` itself is not modified (immutable, Chapter 11 §11.3) and its own definitions remain valid historical record — only its role as the *mandatory* approval-eligibility mechanism is retired; its current lifecycle state is `Superseded` (by `ADR-042`), recorded at MANIFEST per I-12. Product Owner decision nguyên văn: "APPROVE ADR-042 v0.5 AND ITS ATOMIC GOVERNANCE ACTIVATION at reviewed semantic boundary 64fc05becc6ca4245229db79b3fb6c5d9187e622, based on current main e975d44f813b1ee91d2dbf3793376ca1827dc0f1," `2026-09-10T15:51+07:00`. **This v1.3 paragraph remains the currently controlling description** — the v1.5 candidate below does not change it.
>
> **v1.5 CANDIDATE (2026-09-23, corrected — `POST-ADR045-A-MAJ-02`) — `Draft`, NOT reviewed, NOT approved, NOT controlling.** Authored per §5.1 (a Locked living document cannot be edited in place at the same version — a new candidate version must be authored and pass its own fresh approval gate). [`ADR-045`](../adr/ADR-045.md) (`Draft`, `supersedes: [ADR-042]`) proposes a bounded **Delegated Technical Resolution** lane — an eligible `AI Technical Architect`'s Review A may close a routine R0/R1 decision applying already-approved authority to a bounded technical/evidence case, WITHOUT a separate Product Owner Decision step, but only when a closed, conjunctive eligibility predicate (`D1`–`D12`, `ADR-045`) is satisfied; R2 and every Product-Owner-reserved decision class (ADR approval, Approval Gates, product direction/scope/priority, governance/approval-process change, Platform Invariant/Event Schema/module-taxonomy change, explicit risk acceptance, LIVE authorization) are **never** delegated. §3 below now contains exactly ONE future controlling routing model — a single branching workflow (Review A where required → Risk Classification → routing to either Product Owner Decision or `DELEGATED TECHNICAL RESOLUTION`), replacing the v1.3/v1.4 unconditional single-route diagram, which is preserved directly below it strictly as historical text, clearly labeled as no longer the live model once this candidate activates — not a second, competing live workflow. **This v1.4 wording (single route, every decision reaches Product Owner) remains controlling until this v1.5 candidate is itself reviewed, approved, and activated** together with `ADR-045`, Global Execution Rules v0.7, and MANIFEST — after that activation, the new branching workflow becomes the sole current §3 routing model. See MANIFEST for the current authoritative pointer (I-12). No other section of this chapter is touched by this candidate.

## 1. Purpose

Quy định cách mọi quyết định kiến trúc/kỹ thuật của Ride Quant Platform được đề xuất, phản biện, và chốt — để đủ chặt không đổ vỡ, nhưng đủ đơn giản để không tốn thời gian quản lý quy trình hơn viết sản phẩm.

## 2. Roles

| Role | Quyền hạn / Nhiệm vụ | Ai đang giữ role này? |
|---|---|---|
| **Product Owner** | Quyết định cuối cùng về scope, priority, và **approve/reject mọi ADR**. Không AI nào có quyền override. | xem [`/team/team.yaml`](../team/team.yaml) |
| **Chief Architect** | Thẩm quyền kỹ thuật cao nhất về tính đúng đắn kiến trúc — vai trò kỹ thuật, tách biệt khỏi Product Owner dù có thể do cùng một người nắm giữ. Tham gia phản biện ngang hàng với AI Technical Architect. | xem `/team/team.yaml` |
| **AI Technical Architect** | Phản biện kiến trúc độc lập, kiểm tra tính nhất quán giữa các Phase/dependency/DDD/CQRS/Event Sourcing, viết tài liệu/thiết kế chi tiết, sau này review implementation. **Có thể có nhiều người/AI cùng giữ role này, tất cả NGANG HÀNG nhau** — không có "Lead" hay hệ thống cấp bậc giữa các AI Technical Architect. Khác nhau ở trọng tâm công việc, không phải cấp bậc. | xem `/team/team.yaml` |
| **Module Owner** | Chịu trách nhiệm kỹ thuật cho 1 Engine/module cụ thể. | Gán theo từng module khi Phase 3 bắt đầu, xem `/team/team.yaml` |
| **Software Engineer / QA Engineer / Research Engineer** | Roles thực thi. Không có quyền tự ý thay đổi kiến trúc; thay đổi thuộc ADR Scope Rule phải qua ADR. | xem `/team/team.yaml` |

**Nguyên tắc:** Constitution chỉ định nghĩa **Role**, không ghi tên người/AI cụ thể trong governance rule. Việc gán Người/AI ↔ Role sống trong `/team/team.yaml`.

> Tên cụ thể trong review evidence là historical attribution, không phải thứ tự ưu tiên hay governance rule vĩnh viễn.

## 2b. Conflict Resolution

Nếu Product Owner và Chief Architect là 2 người khác nhau và bất đồng: Product Owner thắng về business priority, nhưng ADR phải ghi rõ phản đối của Chief Architect theo Concern/Risk.

## 3. Decision Workflow

**v1.5 CANDIDATE — the sole future controlling routing model (`POST-ADR045-A-CORR-002` remediation — corrects a v1.5 draft that left the historical single-route diagram below live as a second, competing normative workflow alongside a separate Route A/Route B addendum; NOT controlling until this candidate activates together with [`ADR-045`](../adr/ADR-045.md), [Chapter 11](./11-adr-process.md) v2.4, Global Execution Rules v0.7, and MANIFEST — the historical diagram immediately below this one remains the ONLY controlling description until then):**

`ADR-045` now carries the FULL, self-contained R0/R1/R2 definitions
(`X-MAJ-02` correction) — once activated, `ADR-045` is the current
definition authority for the R0/R1/R2 taxonomy platform-wide; before
activation, `ADR-042` (Approved) remains that source, unchanged.

```text
Requirement / governed decision
→ Review A, where required
→ Risk Classification (R0/R1/R2 — definition source: ADR-042 before
  activation, ADR-045 after activation, unchanged in substance)
→ routing:

    PO-reserved decision class, OR R2, OR ADR_REQUIRED, OR
    Delegation Eligibility (D1-D12, ADR-045) not satisfied
        → Product Owner Decision

    R0/R1 AND Review A returns CLEAN AND D1-D12 all satisfied
    (ADR-045, closed, conjunctive)
        → DELEGATED TECHNICAL RESOLUTION
           (explicitly NOT an approval, NOT an Approved/Locked/Phase-
           Approved/Module-Approved/LIVE-Authorized transition — ADR-045)

→ downstream step follows the decision class:

    Product Owner Decision route
        → applicable Approved/Locked/Phase-Approved/Module-Approved/
          LIVE-Authorized transition, whichever this decision class
          governs
        → Sang Phase tiếp theo (nếu áp dụng)

    Delegated Technical Resolution route
        → bounded technical disposition
        → deterministic recording/execution
        (never creates, and never implies, any Product-Owner-reserved
        lifecycle state — ADR-045)
```

Once activated, the Product Owner Decision route remains the **only**
route for: ADR approval/rejection; Phase/Module Approval Gate decisions;
product direction, scope, priority, and value tradeoffs; governance/
approval-process changes; Platform Invariant/Event Schema/module-
taxonomy/dependency changes; any decision requiring an ADR under §4b;
every R2 decision; explicit risk acceptance; LIVE authorization; any
decision a governing authority explicitly reserves to Product Owner; and
any decision the Product Owner explicitly calls in/reserves for
themself, which no AI may override (`ADR-045` `D10`). The Delegated
Technical Resolution route never touches these — see `ADR-045` for the
full closed eligibility predicate. R2 is **never** delegated.

**Historical — v1.3/v1.4 single-route diagram (currently controlling;
becomes historical text only once the branching model above activates —
not a second live workflow):**

```text
Requirement
→ Review A
→ Risk Classification (R0/R1/R2)
→ Product Owner Decision
→ ADR Accepted
→ ADR Locked
→ Sang Phase tiếp theo
```

*(Sơ đồ v1.3 candidate — `ACT-A-MAJ-01` remediation, đóng contradiction với "Review gate" dưới đây: KHÔNG còn plural "Reviews" hay một "Architecture Review" stage riêng biệt/mandatory — đúng một Review A, theo sau bởi Risk Classification bắt buộc R0/R1/R2; tại R2, Product Owner CÓ THỂ chọn một optional advisory cross-check, KHÔNG một mandatory stage riêng trong sơ đồ này.)*

*(Accepted = quyết định đã được Product Owner chốt; Locked = current lifecycle state được MANIFEST ghim sau khi decision artifact đã ổn định. Với ADR, file đã bất biến ngay tại approval boundary.)*

**Review gate (v1.4 candidate — `POST-ADR042-A-MAJ-01` remediation: v1.3's own heading here still read "candidate... NOT ACTIVE cho tới atomic activation," stale/false the moment ADR-042 v0.5 activated at commit `8788895e8de8e8940e165abe3e4230ff15cf57bf` — factual/lifecycle-wording correction only, no semantic change. ACTIVE since that boundary; xem banner "Governance migration (v1.3, ACTIVE)" phía trên. This bullet list describes Review A/Risk Classification mechanics that remain unchanged under the v1.5 candidate above — only what happens *after* Risk Classification differs between the two diagrams):**

- **Review A bắt buộc.** Trước khi Product Owner quyết một ADR hoặc tài liệu thuộc approval gate, phải có đúng một Review A — reviewer phải đang giữ role `AI Technical Architect` tại review boundary. Role eligibility LUÔN thuộc về **principal** (person/AI đã đăng ký giữ role tại `/team/team.yaml`), KHÔNG BAO GIỜ thuộc về một execution/session cụ thể. Review A phải độc lập kiểm tra trực tiếp candidate/repository authority — không kế thừa kết luận của Executor làm ground truth.
- **Risk Classification bắt buộc, ngay sau Review A.** Mỗi decision được phân đúng một trong ba lớp — R0 (mechanical/không rủi ro semantic), R1 (bounded semantic/rủi ro implementation bình thường), R2 (rủi ro semantic/architecture cao). **Definition source (`X-MAJ-02` correction):** trước khi `ADR-045` activate, nguồn định nghĩa LÀ [ADR-042](../adr/ADR-042.md) (đã Approved) — SAU KHI `ADR-045` activate, nguồn định nghĩa hiện tại LÀ [`ADR-045`](../adr/ADR-045.md) (tự chứa đầy đủ R0/R1/R2, KHÔNG đổi substance so với ADR-042). R0/R1 mặc định `NO CROSS-CHECK`. R2: Review A `RECOMMEND OPTIONAL INDEPENDENT CROSS-CHECK` — KHÔNG BAO GIỜ tự động yêu cầu; Product Owner chọn `CROSS-CHECK` hoặc `PROCEED WITHOUT CROSS-CHECK`.
- **Optional cross-check** (chỉ khi Product Owner chọn, chỉ tại R2): advisory only, không veto, KHÔNG là approval prerequisite, KHÔNG cần persisted transcript/report, KHÔNG cần Mode A/Mode B bookkeeping, KHÔNG bắt buộc xuất hiện trong ADR/MANIFEST/CHANGELOG. Sự vắng mặt của cross-check KHÔNG BAO GIỜ làm decision mất điều kiện approval.
- Các reviewer ngang hàng; không reviewer nào có veto.
- Product Owner là authority duy nhất approve/reject.
- Nếu Review A execution KHÔNG resolve được, HOẶC Risk Classification KHÔNG resolve đúng một trong R0/R1/R2, tại review boundary — decision CHƯA đủ điều kiện đi tới Product Owner approval gate (fail-closed). Sự vắng mặt của một optional cross-check KHÔNG BAO GIỜ là lý do fail-closed.
- Constitution khóa role (`AI Technical Architect`), Review A mandatory, Risk Classification mandatory, và optional-cross-check semantics; actor ↔ role assignment sống trong `/team/team.yaml`. [ADR-031](../adr/ADR-031.md)'s Mode A/Mode B execution-identity model (Approved, immutable) không còn là mandatory approval-eligibility mechanism kể từ activation này — định nghĩa của nó vẫn còn giá trị tham khảo lịch sử, có thể dùng để mô tả provenance của một optional cross-check nếu muốn, nhưng KHÔNG BAO GIỜ là bookkeeping bắt buộc.

Mỗi review output tối thiểu:

```text
Concern:        điều gì đáng lưu ý
Risk:           mức độ ảnh hưởng nếu bỏ qua
Recommendation: nên làm gì
```

Nếu một Concern có Risk cao và liên quan trực tiếp đến vi phạm [Platform Invariant](./02-platform-invariants.md), nhưng Product Owner vẫn quyết định tiến hành, ADR phải ghi rõ `Chấp nhận rủi ro: ...`. Đây là transparency requirement, không phải veto.

## 4. ADR Workflow

Dùng template tại [`/docs/templates/adr-template.md`](../templates/adr-template.md). Mỗi ADR bắt buộc có **Scale check**.

## 4b. ADR Scope Rule — khi nào cần ADR

| Loại | Ví dụ | Có cần ADR? |
|---|---|---|
| **ADR Required** | Thêm/sửa Platform Invariant · thay đổi Event Schema · Module Taxonomy/dependency graph · Governance/Approval process · quyết định ảnh hưởng >1 module hoặc khó đảo ngược · sửa/supersede ADR đã Locked | **Bắt buộc** |
| **ADR Optional** | Thay đổi nội bộ một module không đổi contract nhưng ảnh hưởng đáng kể | Tùy đánh giá |
| **ADR Not Required** | UI thẩm mỹ · refactor không đổi behavior/contract · typo/formatting | **Không cần** |

## 5. Freeze Policy & ADR Immutable Rule

### 5.1 Living documents

Constitution chapter, architecture specification và domain contract là living documents có version. Khi đã `Approved` hoặc `Locked`, không được sửa trực tiếp cùng version. Muốn thay đổi phải tăng version, mở ADR nếu thuộc ADR Scope Rule và đi qua approval gate.

### 5.2 ADR file immutability

ADR là immutable decision record.

```text
Draft / In Review
→ được sửa tại chỗ

Product Owner approval boundary
→ toàn bộ ADR file bị đóng băng byte-for-byte
```

Sau approval:

- không sửa decision content;
- không sửa frontmatter;
- không đổi `status` trong file ADR;
- không thêm `superseded_by`, `deprecated_at` hoặc lifecycle metadata;
- không tạo `rev2/rev3` cho cùng ADR identity.

Muốn thay đổi quyết định phải tạo ADR mới. ADR mới khai báo `supersedes: [ADR-cũ]` khi có quyết định thay thế.

Current lifecycle state (`Approved`, `Locked`, `Superseded`, `Deprecated`) và reverse lookup `superseded_by` được ghi authoritative trong `MANIFEST.md`. File ADR cũ giữ nguyên byte-for-byte từ approval boundary.

Git history là audit evidence, không thay thế authority mapping của I-12.

## 5b. Single Source of Truth — áp dụng trong Governance

Định nghĩa đầy đủ nằm tại **I-12**.

- Decision Log sống trong `MANIFEST.md`.
- Version/status hiện tại của tài liệu được ghim tại `MANIFEST.md`.
- Current lifecycle state của ADR và reverse supersession relation sống tại `MANIFEST.md`.
- Current OQ status sống tại `MANIFEST.md`; ADR giữ decision evidence và transition cause.

**Decision ≠ Documentation:** ADR lưu quyết định; Constitution lưu quy tắc; architecture lưu thiết kế; domain lưu khái niệm nghiệp vụ.

## 6. Disagree and Commit

Sau khi ADR đã Approved, chỉ mở lại khi có sự cố truy vết được về quyết định hoặc yêu cầu mới mâu thuẫn cấu trúc với quyết định cũ.

## 7. Document Lifecycle

### 7.1 Living documents

```text
Not Started → Draft → In Review → Revision Requested → Approved → Locked
                                                              ↓
                                                    Deprecated / Superseded
```

### 7.2 ADR

```text
Draft → In Review → Revision Requested → Approved
```

Tại `Approved`, ADR file freeze vĩnh viễn. `Locked`, `Deprecated`, `Superseded` sau đó là **current lifecycle state tại MANIFEST**, không phải mutation của ADR file.

## 8. Versioning Policy

Living document có SemVer riêng và được ghim tại MANIFEST.

Đối với ADR, `version` chỉ dùng trước approval để nhận diện draft được review. Sau approval không bump version và không sửa file; thay đổi quyết định dùng ADR identity mới.

## 9. Review Policy

Living document có `owner`, `reviewers`, `approved_by`, `last_review`, `next_review`. Với ADR, các field được pin tại approval boundary và sau đó bất biến.
