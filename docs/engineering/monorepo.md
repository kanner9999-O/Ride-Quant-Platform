---
id: engineering-monorepo
title: "Engineering Foundation — Monorepo Structure"
version: "0.5"
status: Approved
owner: Product Owner
reviewers: []
approved_by: Product Owner
approved_at: "2026-08-11"
created_at: "2026-08-10"
last_review: null
next_review: null
depends_on: ["../constitution/03-engineering-principles", "../adr/ADR-008", "../adr/ADR-024", "../constitution/14-roadmap"]
---

# Engineering Foundation — Monorepo Structure

**Vai trò của tài liệu này:** convention document đầu tiên của Phase 1.5 — Engineering Foundation (Chapter 3 §3.2: "nội dung chi tiết từng mục được điền dần khi Phase 1.5 triển khai"), phạm vi CHỈ category **Monorepo** (Chapter 14 §14.2's Phase 1.5 scope list) — đúng `EF-TXN-002` (một category = một transaction bounded). KHÔNG Constitution chapter, KHÔNG ADR, KHÔNG redefine Module Taxonomy/dependency graph — `docs/architecture/module-registry.yaml` vẫn LÀ single source of truth cho `module_id`/dependency; tài liệu này CHỈ quy định CHỖ ĐẶT source code tương ứng, KHÔNG tự quyết định lại bất kỳ module boundary nào.

**APPROVED (2026-08-11) — status: Draft → Approved.** Product Owner decision: **"APPROVE MONOREPO CONVENTION V0.5."** Reviewed candidate: v0.5, blob `d1fe7f8c8116e1473863279934a300ae20e1045d` (Review A bounded re-review `CLEAN`; Independent Review B `READY_FOR_PRODUCT_OWNER_DECISION`; Blocker 0/Major 0/Minor 1). `version: "0.5"` KHÔNG đổi (pure mechanical lifecycle approval — KHÔNG bump). Tài liệu này VẪN LÀ living document (Chapter 3 §3.2 "tài liệu SỐNG, không bất biến"; Chapter 0 §7.1 lifecycle Draft→...→Approved→Locked) — `Approved` KHÔNG đồng nghĩa immutable byte-for-byte như ADR (Chapter 11 §11.3 KHÔNG áp dụng ở đây); thay đổi tương lai vẫn hợp lệ qua version bump + re-review (Chapter 0 §8).

**Residual Minor `EF-MONO-ADR024-B-MIN-01`** (v0.4-era provenance/self-description inconsistency — một số framing nói nội dung dưới "không đổi" dù v0.5 đã sửa §1 rationale; KHÔNG chạm repository-topology decision/authority boundary/language allocation/module mapping/Rust deferral/`module_id` naming/tooling deferral) — Product Owner ACCEPT làm non-blocking: **`OPEN, carried forward` — KHÔNG đóng SAI ("closed"/"resolved") bởi approval này**, đúng pattern Gate 2's sáu accepted Minor (`MANIFEST.md` "Phase 1 Approval Gate — Decision" §Residual-risk acceptance). Text của finding này CHỈ được đóng khi thực sự sửa tại một version tương lai.

**Approval này KHÔNG đổi Monorepo semantics nào** (§1–§6 dưới byte-equivalent) — KHÔNG chạm `ADR-024`/`ADR-008`/`module-registry.yaml` (ADR-024 immutable, verified byte-identical), KHÔNG tạo ADR-025, KHÔNG mở Coding Standard hay Engineering Foundation category khác, KHÔNG authorize Phase 2, KHÔNG authorize LIVE.

**Authority alignment (v0.4, sửa tại transaction alignment SAU khi `ADR-024` Approved):**

```text
Repository-topology decision:  Approved via ADR-024 (v0.2, Approved
                                2026-08-11, Product Owner decision
                                "APPROVE ADR-024 V0.2", resulting blob
                                d15ba39a02eb170f4daa1e791d4e00af58f81e63).
Convention lifecycle
  (chính tài liệu monorepo.md này):  VẪN `status: Draft`.
```

Quyết định "một-repo" tại §1 (platform-wide, ảnh hưởng >1 module, Chapter 0 §4b — xem §6 cho lịch sử classification) KHÔNG CÒN LÀ đề xuất chờ ADR — `ADR-024` LÀ authority hiện tại cho chính quyết định repository-topology đó. §1–§5 dưới đây nay elaborate CONSEQUENCES filesystem/source-layout của quyết định Approved đó (nội dung KHÔNG đổi so với trước, đã reviewed clean — CHỈ authority-framing đổi).

**`ADR-024` Approved KHÔNG tự động approve/accept chính convention document này** — đây LÀ hai quyết định tách biệt: ADR quyết định repository TOPOLOGY (platform-wide, >1-module, ADR Scope Rule); convention document elaborate filesystem/source-layout CONSEQUENCES của topology đó (Engineering Foundation category, Chapter 3 §3.2). Product Owner lifecycle decision cho chính `monorepo.md` (accept/approve tài liệu này) LÀ một transaction riêng biệt, CHƯA thực hiện tại đây — `status: Draft` VẪN giữ.

## 1. Repository model

**Authority: `ADR-024` v0.2 (Approved 2026-08-11).** Nội dung dưới đây KHÔNG đổi so với candidate trước — CHỈ nay LÀ elaboration của một quyết định Approved, KHÔNG CÒN LÀ proposal chờ authority.

```text
[v0.5 sửa, đóng EF-MONO-ADR024-A-MAJ-01: rationale dưới trước đây ngụ ý
  multi-repo → version-drift → vi phạm I-12 (SAI, cùng lỗi ADR-024 v0.1
  đã sửa trước approval) VÀ dùng team-scale wording stale "1 Product
  Owner + AI Architect". Thay bằng ĐÚNG rationale Approved tại ADR-024
  v0.2 §6, KHÔNG suy diễn lại.]

Toàn bộ Ride Quant Platform — docs + code — sống trong ĐÚNG một
  repository (monorepo). I-12 (Chapter 2) yêu cầu MỘT authoritative
  source per concept/scope — KHÔNG yêu cầu MỘT Git repository duy nhất;
  một multi-repo model versioned/pinned/automated VẪN thỏa I-12. Single
  Monorepo được CHỌN (đúng ADR-024 v0.2 §6) vì, tại quy mô hiện tại (1
  Product Owner kiêm Chief Architect + 2 AI Technical Architect
  [ChatGPT, Claude] + 1 Software Engineer [Thạch] — bốn actor, KHÔNG có
  independent module/domain team nào — verify `docs/team/team.yaml`),
  nó cho: atomic change xuyên contract+consumer; coordination đơn giản
  hơn; ít release/version coordination surface; consistency check toàn
  repo dễ hơn. Đánh đổi được chấp nhận: repo/CI phình to theo thời
  gian; ownership isolation cấp repo yếu hơn; cần path-aware CI sau
  này; blast radius lớn hơn cho lỗi tooling/config cấp repo. Multi-repo
  trở nên hấp dẫn hơn NẾU team độc lập thật xuất hiện sau này (ADR-024
  §9 Scale Check `reason_if_no`).
```

## 2. Root-level structure

```text
docs/     ĐÃ tồn tại — Constitution/ADR/architecture/governance/product/
          domain/team/... (KHÔNG đổi bởi tài liệu này).
python/   Root cho MỌI module có ngôn ngữ triển khai = Python (ADR-008).
go/       Root cho MỌI module có ngôn ngữ triển khai = Go (ADR-008).

Rust: KHÔNG có root — ADR-008 "Rust KHÔNG dùng ngay", reserved. Root
  `rust/` CHỈ tạo khi một ADR mới thật sự đưa Rust vào dùng.
```

## 3. Per-module source directory naming

```text
Khi một module BẮT ĐẦU được build (Phase 3, theo dependency graph
  module-registry.yaml) — source directory của nó PHẢI đặt tên CHÍNH
  XÁC theo module_id trong module-registry.yaml (single source of truth,
  tránh drift/duplicate naming), đặt dưới root ngôn ngữ tương ứng:
    python/<module_id>/   hoặc   go/<module_id>/

Tài liệu này KHÔNG pre-create bất kỳ module directory nào — Roadmap
  Chapter 14 §14.2 đặt việc build module ở Phase 3, "build ĐÚNG theo
  dependency graph". Tạo trước 23 folder rỗng cho module chưa build LÀ
  speculative, vi phạm EF-TXN-001.
```

## 4. Language assignment — ADR-008 pins theo layer/capability, KHÔNG theo `module_id`

```text
[v0.2 sửa v0.1, đóng EF-MONO-A-MAJ-01 — xem §Change history.]

ADR-008 (Approved) pin ngôn ngữ theo LAYER/CAPABILITY, verify trực tiếp
  nguyên văn tại chính ADR-008.md §Decision:
  Python:  Feature Engineering · Strategy · Decision logic · Backtest
           Engine
  Go:      Market Data Ingestion · Risk Gateway · Execution Engine
  Rust:    KHÔNG dùng ngay (reserved)

ADR-008 KHÔNG liệt kê bất kỳ module_id nào — ADR-008 approved 2026-07-18,
  TRƯỚC KHI module-registry.yaml (v1.1, generated_at 2026-08-10) tồn tại.
  Verify trực tiếp module-registry.yaml (grep toàn file): KHÔNG module
  entry nào có field `language`/tương đương, KHÔNG entry nào reference
  ADR-008. Do đó: tại thời điểm tài liệu này author, KHÔNG một module_id
  nào (trong 26 module_id hiện có) được pin ngôn ngữ bởi authority hiện
  hữu nào — kể cả các module_id CÓ TÊN nghe giống layer của ADR-008 (vd
  `feature-engine`, `market-data-ingestion`, `risk-gateway`,
  `execution-engine`...). Tên giống nhau KHÔNG PHẢI authority — đó là
  suy diễn, KHÔNG PHẢI ADR-008 "trực tiếp named" module_id đó.

Tài liệu này KHÔNG tự tạo một module→language mapping mới để lấp khoảng
  trống đó (tránh tự tạo authority không thuộc phạm vi Monorepo
  convention). Quy tắc CHUYỂN GIAO: một module_id CHỈ được đặt dưới
  `python/` hoặc `go/` khi language của chính module đó đã được resolve
  LEGITIMATELY — tức HOẶC (a) một authority hiện hữu khác pin trực tiếp
  module đó (PHẢI verify trực tiếp trước khi dùng, KHÔNG suy diễn/mở
  rộng thành mapping chung), HOẶC (b) một governed decision SAU này (Phase
  3 build transaction của chính module đó, áp layer principle ADR-008
  theo đúng bản chất capability, HOẶC một ADR mới nếu thật sự ambiguous/
  không fit layer nào). KHÔNG đoán/gán trước cho bất kỳ module_id nào tại
  tài liệu này.
```

## 5. Workspace/package-manager tooling — deferred

```text
Go:     dùng cơ chế Go workspace tiêu chuẩn (go.work/go.mod) khi module
        Go đầu tiên được build — KHÔNG cần chọn 3rd-party tool (Go không
        có alternative package manager cần quyết định).
Python: package-manager cụ thể (pip/poetry/uv/...) CHƯA chọn — deferred
        tới transaction build module Python đầu tiên (Phase 3) hoặc một
        transaction Coding-Standard-category riêng. Chọn brand cụ thể
        NGAY BÂY GIỜ, khi chưa có module Python nào tồn tại, LÀ
        speculative tooling.

KHÔNG root workspace manifest nào (go.work/pyproject.toml) được tạo tại
  transaction này — chưa có module nào cần chúng; tạo trước LÀ gold-
  plating cho nhu cầu chưa tồn tại.
```

## 6. ADR-scope check (`EF-ADR-001`) — RESOLVED tại v0.4 (`ADR-024` Approved); lịch sử classification GIỮ NGUYÊN làm evidence

```text
[v0.4: kết luận "ADR Required" dưới đây (đúng từ v0.3) ĐÃ RESOLVE —
  ADR-024 v0.2 Approved 2026-08-11 (xem preamble). Nội dung phân tích
  dưới GIỮ NGUYÊN, KHÔNG xóa/viết lại — LÀ historical evidence cho
  chính classification "ADR Required" đã dẫn tới ADR-024. Đoạn "Kết
  luận"/"Số ADR cụ thể" cuối §6 (trước v0.4 suy đoán) đã sửa thành
  current-state resolved — xem cuối §6.]

[v0.1/v0.2 kết luận SAI "ADR Not Required" — sửa tại v0.3. Root cause:
  v0.1/v0.2 chỉ kiểm tra "khó đảo ngược" (reversibility) và bỏ sót vế
  đầu của chính rule đang trích dẫn. Xem correction dưới.]

Chapter 0 §4b nguyên văn (verify trực tiếp tại 00-governance.md):
  "ADR Required" áp dụng cho — trong SỐ NHIỀU điều kiện khác — "quyết
  định ảnh hưởng >1 module HOẶC khó đảo ngược". Đây LÀ điều kiện OR
  (đủ MỘT trong hai vế, KHÔNG cần CẢ HAI) — v0.1/v0.2 chỉ đánh giá vế
  "khó đảo ngược" ("đổi tên/cấu trúc folder trước khi có code LÀ hoàn
  toàn reversible") rồi kết luận ADR Not Required, bỏ sót hoàn toàn vế
  ">1 module" — đây LÀ lỗi áp rule sai (conjunctive thay vì disjunctive).

`EF-ADR-001` (phase-1.5-rules.md) restate ĐÚNG cùng rule: "ADR CHỈ bắt
  buộc khi thay đổi thuộc diện ADR Required (... quyết định >1 module
  HOẶC khó đảo ngược)" — cùng OR, KHÔNG redefine.

Áp dụng lại cho §1 (quyết định "một-repo"): đây LÀ quyết định
  platform-wide — áp dụng cho TOÀN BỘ 26 module trong module-registry.yaml
  (mọi module tương lai đều sống trong monorepo này), rõ ràng thỏa vế
  ">1 module". Reversibility KHÔNG hủy trigger này — OR nghĩa là MỘT vế
  đủ, "dễ đảo ngược" KHÔNG miễn trừ vế ">1 module" đã thỏa.

Kết luận (v0.3, giữ nguyên đúng): **ADR Required** cho quyết định
  "một-repo" tại §1 — §2 (root python/go split) và §3 (naming
  convention) LÀ derivative của §1.

**Current state (v0.4, RESOLVED):** `ADR-024` LÀ ADR đó — authored,
  Independent-reviewed (Review A `CLEAN`, Independent Review B
  `READY_FOR_PRODUCT_OWNER_DECISION`), VÀ Approved bởi Product Owner
  (2026-08-11, "APPROVE ADR-024 V0.2"). §1's quyết định "một-repo" VÀ
  §2/§3's derivative consequence (root python/go split, module_id-based
  naming) nay LÀ authoritative theo `ADR-024`, KHÔNG CÒN LÀ đề xuất chờ
  approval. `monorepo.md` (chính tài liệu này) VẪN `status: Draft` —
  ADR Approved KHÔNG tự động approve convention document (xem preamble).
Lịch sử thay đổi ghi tại CHANGELOG.md.
```

## Change history

```text
v0.1  2026-08-10  Established — vai trò: `Phase 1.5 Monorepo Foundation
      Executor`. Bounded EF-TXN-002 category transaction (Monorepo
      only). Root-level structure: docs/ (unchanged) + python/ + go/
      (per Approved ADR-008 language layers); Rust root deferred
      (ADR-008 "reserved", not used now). Per-module directory naming
      pinned to module-registry.yaml's module_id (single source of
      truth) — NO module directories pre-created (EF-TXN-001, avoids
      speculative Phase-3 scaffolding). Language assignment resolved
      ONLY for the modules ADR-008 already names explicitly (6 Python,
      3 Go by direct cross-reference); remaining 17 module_id left
      unresolved, explicitly deferred to each module's own Phase 3 build
      transaction. Workspace/package-manager tooling (go.work/
      pyproject.toml/package-manager brand) deferred — not created, no
      Python/Go module exists yet to require one. ADR-scope check
      (EF-ADR-001): ADR Not Required (Chapter 0 §4b) — convention/
      tooling change, fully reversible, no Platform Invariant/Event
      Schema/Module Taxonomy/dependency-graph/Governance-process change.
      `status: Draft` — not self-approved (G-ORCH-002 no auto-approval);
      Product Owner review/approval is a separate transaction if
      desired.
v0.2  2026-08-10  Bounded semantic correction, đóng `EF-MONO-A-MAJ-01`.
      v0.1 §4 sai: presented một 6-Python/3-Go module_id mapping như
      thể ADR-008 "trực tiếp named" các module_id đó — SAI, verify trực
      tiếp cho thấy ADR-008 (approved 2026-07-18) pin ngôn ngữ theo
      LAYER/CAPABILITY (Feature Engineering/Strategy/Decision logic/
      Backtest Engine → Python; Market Data Ingestion/Risk Gateway/
      Execution Engine → Go), KHÔNG liệt kê module_id nào — ADR-008 CÓ
      TRƯỚC module-registry.yaml (v1.1). Verify trực tiếp
      module-registry.yaml: KHÔNG entry nào có field `language`, KHÔNG
      entry nào reference ADR-008. Sửa: bỏ hoàn toàn mapping 9-module_id
      "đã resolve" — tường minh nói KHÔNG module_id nào (trong 26) được
      pin ngôn ngữ bởi authority hiện hữu, tên module_id giống layer
      ADR-008 KHÔNG PHẢI authority. KHÔNG tự tạo module→language mapping
      mới thay thế — pin quy tắc chuyển giao: module_id CHỈ vào
      `python/`/`go/` khi language của chính nó resolve legitimately
      (authority hiện hữu verify trực tiếp, HOẶC governed decision sau
      này tại Phase 3 build transaction/ADR mới). Preserved nguyên vẹn:
      single-monorepo decision, root python/go convention, Rust
      deferral, module_id-based directory naming. KHÔNG chạm §1/§2/§3/
      §5/§6 semantics, KHÔNG EF category khác, KHÔNG module taxonomy/
      dependency graph nào sửa. `status` VẪN `Draft`.
v0.3  2026-08-10  Bounded correction, đóng `EF-MONO-B-MAJ-01`/
      `EF-MONO-B-MAJ-02` (Independent Review B, verdict `NOT_READY`).
      §6 v0.1/v0.2 kết luận SAI "ADR Not Required" — chỉ kiểm tra vế
      "khó đảo ngược" của Chapter 0 §4b/`EF-ADR-001`, bỏ sót vế ">1
      module" (rule LÀ OR, KHÔNG cần cả hai). Quyết định "một-repo" (§1)
      LÀ platform-wide, ảnh hưởng >1 module — sửa kết luận thành **ADR
      Required**. KHÔNG invent số ADR cụ thể (ground truth hiện tại
      KHÔNG đủ xác định identity kế tiếp dứt khoát — P1-ADR-001 ceiling
      cần re-evaluate hậu-Gate-2, thuộc transaction ADR-authoring riêng).
      Bổ sung preamble: candidate CHƯA authoritative/final, §1–§5 LÀ
      proposal, quyết định monorepo BLOCK chờ ADR + Product Owner
      approve ADR đó — transaction này KHÔNG tự approve/establish
      quyết định, KHÔNG tự author ADR. Đồng thời sửa `python/README.md`/
      `go/README.md`: bỏ ví dụ module_id cụ thể (`feature-engine`,
      `market-data-ingestion`) hàm ý gán ngôn ngữ — chỉ giữ pattern
      generic `<module_id>/`, thêm ghi chú "chỉ đặt sau khi language
      resolve legitimately qua governance". KHÔNG author ADR, KHÔNG
      approve candidate, KHÔNG đổi §1/§2/§3's nội dung đề xuất, KHÔNG
      đổi §4/§5, KHÔNG module taxonomy/dependency graph nào sửa.
      `status` VẪN `Draft`.
v0.4  2026-08-11  Authority-alignment transaction (KHÔNG bounded
      correction — không đóng finding review nào), vai trò: `Phase 1.5
      Monorepo ADR-024 Alignment Executor`. `ADR-024` v0.2 (Approved
      2026-08-11, "APPROVE ADR-024 V0.2", blob
      `d15ba39a02eb170f4daa1e791d4e00af58f81e63`) LÀ authority mới cho
      §1's repository-topology decision — preamble viết lại: bỏ
      "CHƯA authoritative/final"/"BLOCK chờ ADR" (stale), thay bằng
      "Approved via ADR-024" + "convention lifecycle VẪN Draft" (hai
      quyết định tách biệt, KHÔNG conflate). §1 thêm authority pointer
      1 dòng (KHÔNG đổi nội dung code block). §6 giữ nguyên TOÀN BỘ
      lịch sử phân tích "ADR Required" (v0.1-v0.3, làm historical
      evidence dẫn tới ADR-024) — CHỈ sửa "Kết luận"/"Số ADR cụ thể"
      cuối §6 thành current-state RESOLVED (ADR-024 identity/Approved
      fact, KHÔNG CÒN suy đoán identity). `depends_on` thêm
      `../adr/ADR-024`. KHÔNG đổi §2/§3/§4/§5 (root split/naming/
      language-assignment-deferral/tooling-deferral nguyên vẹn) —
      KHÔNG module→language mapping nào thêm, KHÔNG `module-registry.
      yaml`/`ADR-008`/`ADR-024` nào sửa (ADR-024 immutable, KHÔNG chạm).
      **KHÔNG approve/Lock `monorepo.md`** — `status` VẪN `Draft`, chờ
      Product Owner lifecycle decision riêng biệt cho chính tài liệu
      này.
v0.5  2026-08-11  Bounded correction, đóng `EF-MONO-ADR024-A-MAJ-01`
      (Review A finding). §1's rationale text (KHÔNG PHẢI authority
      pointer thêm tại v0.4, mà chính nội dung ```text``` block) VẪN
      giữ premise tiền-ADR-024-v0.2: ngụ ý multi-repo → version-drift →
      vi phạm I-12, VÀ dùng team-scale wording stale "1 Product Owner +
      AI Architect" — CÙNG lỗi ADR-024 v0.1 đã sửa trước khi Approved,
      nhưng chưa propagate vào chính convention document này tại v0.4's
      alignment. Sửa: §1 nay trích ĐÚNG rationale Approved tại ADR-024
      v0.2 §6 — I-12 yêu cầu MỘT authoritative source per concept/
      scope, KHÔNG MỘT Git repository; multi-repo versioned/automated
      VẪN thỏa I-12; Single Monorepo chọn vì atomic cross-contract
      change/coordination đơn giản/ít release surface/consistency check
      dễ hơn TẠI QUY MÔ HIỆN TẠI; đánh đổi (repo/CI growth/ownership
      isolation yếu/path-aware CI sau này/blast radius) được chấp nhận;
      multi-repo hấp dẫn hơn NẾU team độc lập xuất hiện. Team-scale sửa
      thành chính xác `team.yaml`: 1 Product Owner (kiêm Chief
      Architect) + 2 AI Technical Architect (ChatGPT, Claude) + 1
      Software Engineer (Thạch), KHÔNG independent module/domain team
      nào. **KHÔNG đổi lựa chọn** (Single Monorepo VẪN được chọn) —
      KHÔNG đổi §2/§3/§4/§5/§6/preamble/ADR-024 authority pointer,
      KHÔNG module→language mapping nào thêm, KHÔNG chạm
      `module-registry.yaml`/`ADR-008`/`ADR-024` (ADR-024 immutable,
      verified byte-identical). `status` VẪN `Draft`.
ACCEPTANCE  2026-08-11  Product Owner lifecycle approval — mechanical,
      vai trò: `Phase 1.5 Monorepo Convention Approval Recorder`.
      Quyết định: "APPROVE MONOREPO CONVENTION V0.5." Reviewed
      candidate: v0.5, blob
      `d1fe7f8c8116e1473863279934a300ae20e1045d` (Review A bounded
      re-review `CLEAN`; Independent Review B
      `READY_FOR_PRODUCT_OWNER_DECISION`; Blocker 0/Major 0/Minor 1).
      `status: Draft -> Approved`, `approved_by: null -> Product
      Owner`, `approved_at: null -> "2026-08-11"`. `version` KHÔNG bump
      (pure mechanical lifecycle approval). Residual Minor
      `EF-MONO-ADR024-B-MIN-01` (v0.4-era provenance/self-description
      inconsistency, KHÔNG semantic/authority/mapping impact) ACCEPTED
      làm non-blocking — **`OPEN, carried forward`, KHÔNG đóng
      "closed"/"resolved"** bởi approval này; CHỈ đóng khi text thực sự
      sửa tại version tương lai. KHÔNG semantic content nào đổi (§1–§6
      byte-equivalent ngoài banner/lifecycle metadata/change history
      này). Tài liệu VẪN LÀ living document — `Approved` KHÔNG immutable
      byte-for-byte như ADR. KHÔNG chạm `ADR-024`/`ADR-008`/
      `module-registry.yaml` (ADR-024 immutable, verified
      byte-identical), KHÔNG tạo ADR-025, KHÔNG mở Engineering
      Foundation category khác, KHÔNG authorize Phase 2/LIVE.
```
