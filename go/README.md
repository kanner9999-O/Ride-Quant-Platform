# go/

Root cho module có ngôn ngữ triển khai = Go (ADR-008: Market Data Ingestion · Risk Gateway · Execution Engine layer — layer-level, KHÔNG pin `module_id` cụ thể nào). Quy ước đầy đủ, bao gồm ADR-scope status hiện tại: `docs/engineering/monorepo.md`.

Chưa có module nào build tại đây. Một module CHỈ được đặt dưới `go/<module_id>/` sau khi language của chính module đó đã resolve legitimately qua governance (authority hiện hữu verify trực tiếp, hoặc governed decision — xem `docs/engineering/monorepo.md` §4). KHÔNG module_id cụ thể nào được gán ngôn ngữ tại đây.
