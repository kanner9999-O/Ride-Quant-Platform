# structure-engine

Authoritative Structure Engine: Swing pivot detection/confirmation/invalidation
(`docs/domain/swing.md`) and BOS/CHoCH structure orientation
(`docs/domain/structure.md`). `module_id: structure-engine` per
`docs/architecture/module-registry.yaml`. Implementation language (Python)
resolved by [ADR-033](../../docs/adr/ADR-033.md) (Approved).

This is the **analytical core only** — no broker, no RPC/HTTP, no
Go↔Python transport, no deployment/process topology, no real event log, no
venue connectivity. Those are all separate, future governed decisions
(ADR-033 §"Explicitly out of scope").

## What this module owns

- Swing candidate/confirmed/invalidated facts (`swing.md`).
- BOS/CHoCH structure facts, `StructureFactInvalidated`, `StructureRecomputed`,
  and current structure orientation (`structure.md`).

## What this module consumes

Exactly `candle-closed` / `candle-corrected` — never `CandleObserved`
(provisional) or `CandleCurrentView` (non-authoritative). `depends_on:
[market-data-ingestion]` (`module-registry.yaml`, unchanged).

## What this module never does

- Consume Raw Regime — ADR-003/ADR-014 independence is structural: this
  package has no import of, and no dependency on, any `raw-regime-engine`
  module. `forbidden_dependencies: [structure-engine]` is declared on the
  *other* side (`raw-regime-engine`'s own registry entry) — this module's own
  code simply never references it, by construction.
- Assign its own Quality Tier — `structure-engine` carries no
  Product-Owner-approved `quality_tier` in `module-registry.yaml`. Tier
  classification is a separate governed prerequisite before any formal
  Chapter 13 Quality Gate evaluation.
- Decide runtime topology, choose a broker/RPC mechanism, or wire real
  venue/event-log infrastructure.

## Package layout

```
src/structure_engine/
  identity.py    deterministic opaque subject-id derivation (module-local — swing.md
                 §17 / structure.md §16 both leave the concrete algorithm unspecified)
  envelope.py    Chapter 8 §8.2 event-record identity shapes (EventRecordRef/StreamRef/ProducerRef)
  publish.py     in-process, per-stream contiguous sequence allocation (ADR-009) — a
                 bounded stand-in for the stream-registry.yaml infrastructure that does
                 not exist yet (Phase 1), same role as market-data-ingestion's Go
                 publish.Memory
  candle.py      authoritative Candle input (CandleScope/OHLCV/CandleFact)
  swing.py       SwingDefinition/SwingScope/events + SwingEngine
  structure.py   StructureDefinition/StructureScope/events + StructureEngine
  errors.py      explicit technical failure modes (Error Handling Convention §7)
tests/
  test_swing.py      Swing behavior: candidate/confirm/invalidate, price basis,
                      equal-level tie policy, revision lifecycle, correction, dedup,
                      ordering discipline, historical direct path, deterministic replay
  test_structure.py  Structure behavior: BOS/CHoCH, comparison policy, §6a total-order
                      tie-break, revision-qualified consumption, correction cascade,
                      no-repaint, dedup
```

Both engines are pure, deterministic, in-process, and hold no network
dependency — a caller drives them by calling `ingest_candle`/`on_candle`/
`on_swing_confirmed`/`on_swing_invalidated` in cursor order. This is the
**same authoritative code path** for Replay/Backtest/Paper/Live (Chapter 3
§3.1) — orchestration may differ per mode, the analytical logic never does.

## First-Python-build toolchain (this module is the first Python module built in this repository)

Minimum supported Python version verified fresh against the official
CPython devguide (`https://devguide.python.org/versions/`) at build time
(2026-08-21): **Python >= 3.13** — the newest non-prerelease branch still in
active `Bugfix` maintenance (EOL October 2029), giving the longest support
runway of any non-prerelease release at this boundary. Validated against the
actual local interpreter, Python 3.13.6.

Minimal tooling selected (per `docs/engineering/coding-standard.md` §1/§2's
explicit first-build deferral):

| Concern | Tool | Pinned version | Why |
|---|---|---|---|
| Formatter | `ruff format` | `0.16.4` | One tool covers both formatting and lint (below), avoiding a second dependency; verified as the current release on PyPI at build time. |
| Lint / static analysis | `ruff check` | `0.16.4` | Catches unused imports/unreachable code (Coding Standard §2). |
| Type checking | `mypy --strict` | `2.3.1` | Catches basic type mismatches (Coding Standard §2) — financial-domain code benefits from strict typing; verified current on PyPI. |
| Test framework | `pytest` | `9.1.1` | Idiomatic per `docs/engineering/testing.md` §9 (parametrization, explicit exception-type assertions); verified current on PyPI. |

No numerical/data-science stack (NumPy/Pandas/Polars/TA-Lib/Pydantic) is
used — the module has **zero runtime dependencies**; `decimal.Decimal`
(stdlib) already provides lossless arbitrary-precision arithmetic, so no
custom decimal type was needed (unlike Go, which lacks one in its standard
library). Package/dependency mechanism: a plain PEP 621 `pyproject.toml`
with exact-pinned `dev` extras — no third-party package manager needed for a
zero-runtime-dependency package.

## Build / test locally

```bash
cd python/structure-engine
python3.13 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

ruff format .
ruff check .
mypy
pytest tests/ -v
```

Coverage may be collected for local diagnostics (`coverage run -m pytest
&& coverage report`) but is **NON-FORMAL / INFORMATIONAL ONLY** — this
module's Quality Tier is unresolved, so no formal Chapter 13 Quality Gate
result can be claimed for it yet.

## ADR Scope Rule

`ADR_NOT_REQUIRED` — this is a module-local implementation of already-governed
authority (ADR-033's language decision, `swing.md`/`structure.md`'s existing
Domain Contract semantics, Chapter 3 §3.1's authoritative-implementation
rule). No new/changed Event or Domain Contract semantic, no dependency graph
change, no authority transfer, no cross-module semantic contract, no
runtime-topology decision, no security/custody boundary — every design
choice made while building this module stayed within that bound; where a
domain contract explicitly deferred a concrete algorithm (identity
derivation, equal-level tie-break operationalization, correction-window
substitution model), this module pins one bounded, documented interpretation
in code, not a governance decision.
