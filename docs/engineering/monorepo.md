---
id: engineering-monorepo
title: "Engineering Foundation — Monorepo Structure"
version: "0.1"
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

## 4. Language assignment — chỉ resolve phần ĐÃ authoritative

```text
ADR-008 (Approved) chỉ named tường minh:
  Python:  Feature Engineering · Strategy · Decision logic · Backtest
           Engine
  Go:      Market Data Ingestion · Risk Gateway · Execution Engine

Cross-reference trực tiếp (verify tại module-registry.yaml, KHÔNG suy
  diễn) — các module_id sau ĐÃ resolve nhờ khớp tên/capability trực tiếp
  với ADR-008:
  Python:  feature-engine · strategy-engine · strategy-plugin-host ·
           decision-evaluation-engine · decision-authority-service ·
           backtest-orchestrator
  Go:      market-data-ingestion · risk-gateway · execution-engine

TẤT CẢ module_id còn lại trong module-registry.yaml (17 module — vd
  market-reference-service/structure-engine/raw-regime-engine/context-
  aggregator/account-service/custody-signing-service/exchange-adapter/
  plugin-release-manager/execution-result-processor/fill-processor/
  position-projection/replay-integration-service/paper-execution-
  boundary/command-query-api-surface/review-evidence-service/ux-
  application-shell/contract-compatibility-authority) KHÔNG có language
  assignment authoritative nào tại thời điểm tài liệu này author — CHƯA
  resolve, KHÔNG suy đoán/gán tại đây (tránh reopen/mở rộng ADR-008 vượt
  authority hiện có). Module build transaction (Phase 3) của từng module
  PHẢI tự resolve language của chính nó tại thời điểm đó — bằng cách áp
  layer principle của ADR-008 ("lõi logic" = Python, "biên hệ thống" =
  Go) theo đúng bản chất capability của module, HOẶC mở một ADR mới nếu
  thật sự ambiguous/không fit layer nào.
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
```
