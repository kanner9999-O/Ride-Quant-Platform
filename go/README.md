# go/

Root cho module có ngôn ngữ triển khai = Go (ADR-008: Market Data Ingestion · Risk Gateway · Execution Engine layer — layer-level, KHÔNG pin `module_id` cụ thể nào). Quy ước đầy đủ, bao gồm ADR-scope status hiện tại: `docs/engineering/monorepo.md`.

Một module CHỈ được đặt dưới `go/<module_id>/` sau khi language của chính module đó đã resolve legitimately qua governance (authority hiện hữu verify trực tiếp, hoặc governed decision — xem `docs/engineering/monorepo.md` §4). KHÔNG module_id cụ thể nào được gán ngôn ngữ tại đây — việc gán diễn ra tại chính build transaction của module đó.

**`go/market-data-ingestion/`** (Phase 3 Data Layer Batch 01, 2026-08-19): direct existing authority — ADR-008 names "Market Data Ingestion" explicitly as a Go layer, and `module-registry.yaml`'s `market-data-ingestion` responsibilities match that layer's capability nature (external venue connection boundary, `trust_boundary_candidate`). See `go/market-data-ingestion/README.md` for scope, gaps, and deferrals (notably: `market-reference-service`, the other Data Layer module in this batch, is NOT built here — its language does not resolve under ADR-008 and its Domain Contracts are still Draft with unresolved design gaps).
