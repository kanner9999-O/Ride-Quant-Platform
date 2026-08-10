# go/

Root cho mọi module có ngôn ngữ triển khai = Go (ADR-008: Market Data Ingestion · Risk Gateway · Execution Engine layer). Quy ước đầy đủ: `docs/engineering/monorepo.md`.

Chưa có module nào build tại đây. Khi Phase 3 bắt đầu build một module Go cụ thể, source directory của nó phải đặt tên đúng `module_id` trong `docs/architecture/module-registry.yaml` (ví dụ `go/market-data-ingestion/`).
