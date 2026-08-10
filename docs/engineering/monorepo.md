---
id: engineering-monorepo
title: "Engineering Foundation — Monorepo Structure"
version: "0.2"
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

## 6. ADR-scope check (`EF-ADR-001`)

```text
Quyết định tại tài liệu này: (a) một-repo (monorepo model); (b) hai root
  cấp cao theo NGÔN NGỮ đã Approved sẵn (ADR-008); (c) quy ước tên
  directory-per-module PHẢI khớp module_id đã có sẵn trong registry.
KHÔNG mục nào: thêm/sửa Platform Invariant, đổi Event Schema, đổi Module
  Taxonomy/dependency graph (module-registry.yaml byte-identical), thay
  đổi Governance/Approval process, hay ảnh hưởng quyết định kiến trúc
  khó đảo ngược nào — đổi tên/cấu trúc folder trước khi có code LÀ hoàn
  toàn reversible.
Kết luận (Chapter 0 §4b + Chapter 3 §"Nguyên tắc bắt buộc"): **ADR Not
  Required** — convention/tooling change, refactor-class, không đổi
  behavior/contract nào. Lịch sử thay đổi ghi tại CHANGELOG.md (đúng yêu
  cầu "không cần ADR nhưng vẫn phải để lại lịch sử thay đổi rõ ràng").
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
```
