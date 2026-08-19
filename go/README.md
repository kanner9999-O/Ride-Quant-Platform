# go/

Root cho module có ngôn ngữ triển khai = Go (ADR-008: Market Data Ingestion · Risk Gateway · Execution Engine layer — layer-level, KHÔNG pin `module_id` cụ thể nào). Quy ước đầy đủ, bao gồm ADR-scope status hiện tại: `docs/engineering/monorepo.md`.

Một module CHỈ được đặt dưới `go/<module_id>/` sau khi language của chính module đó đã resolve legitimately qua governance (authority hiện hữu verify trực tiếp, hoặc governed decision — xem `docs/engineering/monorepo.md` §4). KHÔNG module_id cụ thể nào được gán ngôn ngữ tại đây — việc gán diễn ra tại chính build transaction của module đó.

**`go/market-data-ingestion/`** (Phase 3 Data Layer Batch 01, 2026-08-19): direct existing authority — ADR-008 names "Market Data Ingestion" explicitly as a Go layer, and `module-registry.yaml`'s `market-data-ingestion` responsibilities match that layer's capability nature (external venue connection boundary, `trust_boundary_candidate`). See `go/market-data-ingestion/README.md` for scope, gaps, and deferrals.

**`go/market-reference-service/`** (Phase 3 Data Layer completion, 2026-08-19): governed decision — **ADR-032 v0.2 (Approved)** resolves the language allocation (Go, on ADR-008 capability-nature grounds) that did not resolve directly at Batch 01. See `go/market-reference-service/README.md` for scope, ADR-032 §B.3 two-axis bitemporal contract compliance, and deferrals (notably: the full `ActiveListingReservation` arbitration protocol, `instrument.md` §16, is intentionally not implemented — only its structurally-mandatory happy path is).
