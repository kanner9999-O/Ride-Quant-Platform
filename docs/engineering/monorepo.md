---
id: engineering-monorepo
title: "Engineering Foundation — Monorepo Structure"
version: "0.3"
status: Draft
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-08-10"
last_review: null
next_review: null
depends_on: ["../constitution/03-engineering-principles", "../adr/ADR-008", "../constitution/14-roadmap"]
---

# Engineering Foundation — Monorepo Structure

**Vai trò của tài liệu này:** convention document đầu tiên của Phase 1.5 — Engineering Foundation (Chapter 3 §3.2: "nội dung chi tiết từng mục được điền dần khi Phase 1.5 triển khai"), phạm vi CHỈ category **Monorepo** (Chapter 14 §14.2's Phase 1.5 scope list) — đúng `EF-TXN-002` (một category = một transaction bounded). KHÔNG Constitution chapter, KHÔNG ADR, KHÔNG redefine Module Taxonomy/dependency graph — `docs/architecture/module-registry.yaml` vẫn LÀ single source of truth cho `module_id`/dependency; tài liệu này CHỈ quy định CHỖ ĐẶT source code tương ứng, KHÔNG tự quyết định lại bất kỳ module boundary nào.

**Candidate này CHƯA authoritative/final (v0.3, đóng `EF-MONO-B-MAJ-01`/`EF-MONO-B-MAJ-02` — Independent Review B `NOT_READY`):** quyết định "một-repo" tại §1 LÀ platform-wide, ảnh hưởng >1 module — thuộc diện **ADR Required** (Chapter 0 §4b, xem §6). Toàn bộ nội dung §1–§5 dưới đây LÀ đề xuất (proposal) tạm giữ nguyên nội dung để tài liệu ADR tương lai tham chiếu, KHÔNG PHẢI quyết định đã establish. Quyết định monorepo platform-wide bị **BLOCK**, chờ (a) một ADR transaction riêng biệt VÀ (b) Product Owner approve chính ADR đó. Transaction v0.3 này KHÔNG tự approve/establish quyết định monorepo, KHÔNG tự author ADR đó.

## 1. Repository model

```text
Toàn bộ Ride Quant Platform — docs + code — sống trong ĐÚNG một
  repository (monorepo). Lý do: contract/schema shared (Event Contract,
  Domain Contract, module-registry.yaml dependency graph) cần đổi đồng
  bộ, đúng I-12 Single Source of Truth — nhiều repo sẽ tạo version-drift
  risk giữa contract producer/consumer không cần thiết ở quy mô hiện tại
  (1 Product Owner + AI Architect, chưa multi-team).
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

## 6. ADR-scope check (`EF-ADR-001`) — SỬA tại v0.3, đóng `EF-MONO-B-MAJ-01`

```text
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

Kết luận (sửa): **ADR Required** cho quyết định "một-repo" tại §1.
  §2 (root python/go split) và §3 (naming convention) LÀ derivative của
  §1 — VẪN LÀ đề xuất (proposal), KHÔNG PHẢI quyết định established,
  cho tới khi ADR đó Approved.
Số ADR cụ thể: KHÔNG invent tại đây — repository ground truth hiện tại
  (ADR-001..023 tồn tại, ADR-023 LÀ file cuối) KHÔNG đủ để xác định
  identity kế tiếp một cách dứt khoát (P1-ADR-001's ADR ceiling — scoped
  riêng Phase 1, "trước Gate 2" — cần đánh giá lại có còn áp dụng hậu-
  Gate-2/Phase-1.5 hay không; đây LÀ việc của chính transaction author
  ADR, KHÔNG PHẢI transaction correction này). Transaction ADR-authoring
  riêng biệt PHẢI tự resolve identity + chạy G-ADR-004 inflation/scope
  check trước khi author.
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
```
