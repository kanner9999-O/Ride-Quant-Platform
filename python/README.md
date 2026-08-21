# python/

Root cho module có ngôn ngữ triển khai = Python (ADR-008: Feature Engineering · Strategy · Decision logic · Backtest Engine layer — layer-level, KHÔNG pin `module_id` cụ thể nào). Quy ước đầy đủ, bao gồm ADR-scope status hiện tại: `docs/engineering/monorepo.md`.

`structure-engine`'s language allocation resolved via [ADR-033](../docs/adr/ADR-033.md) (Approved 2026-08-21) — the first module built under this root. Any other `module_id` placed here in the future must have its own language legitimately resolved first (an existing authority verified directly, or a governed decision — `docs/engineering/monorepo.md` §4); this file does not itself assign language to any module.

## Modules

- [`structure-engine/`](./structure-engine/) — Swing pivot / BOS / CHoCH structure inference (`structure.md`, `swing.md`). See its own `README.md` for build/test instructions.
- [`raw-regime-engine/`](./raw-regime-engine/) — `volatility` / `directional_persistence` regime classification directly over Candle facts (`regime.md`), structurally independent of `structure-engine` ([ADR-014](../docs/adr/ADR-014.md)). See its own `README.md` for build/test instructions.
