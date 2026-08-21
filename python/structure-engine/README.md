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
(2026-08-21): **Python >= 3.13**.

**Corrected rationale (P3-PYBASE-A-MIN-07):** an earlier revision of this
document incorrectly claimed 3.13 was "the newest non-prerelease branch...
giving the longest support runway of any non-prerelease release." That was
false — the same devguide table shows Python 3.14 is *already* `Bugfix`
status (not merely prerelease) with a *longer* runway (EOL October 2030 vs
3.13's October 2029). The actual, honest reason for the `>=3.13` floor: this
first build was authored and validated against the locally available
interpreter, Python 3.13.6, which was in active `Bugfix` maintenance (not
merely security-only) at build time with ample remaining runway — a
validated *compatibility floor*, not a claim of being the newest or
longest-supported branch. `requires-python = ">=3.13"` is a floor, not a
ceiling: newer interpreters, including 3.14, remain fully compatible and are
not excluded by this pin.

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

### Reproducible build/dev environment (P3-PYBASE-A-MAJ-06)

Every piece of the toolchain state is exact-pinned, not just the three
top-level dev tools:

- **Build backend:** `[build-system].requires` pins `setuptools==84.0.0`
  exactly (was previously an open `>=75` range — corrected).
- **Full transitive dev/build dependency state:**
  [`requirements-dev.lock.txt`](./requirements-dev.lock.txt) — generated via
  `pip freeze --exclude-editable` from a fresh venv, covering everything
  `ruff`/`mypy`/`pytest` themselves pull in (not just the three direct pins).
- **Exact interpreter used:** Python 3.13.6 (CPython, arm64,
  macOS-14.5-arm64-arm-64bit-Mach-O).
- **Exact install mechanism used:** pip 25.2 (`pip install --upgrade
  pip==25.2` before installing this project).
- **Zero production runtime dependencies** — `[project].dependencies` is
  empty; the lock file covers only the dev/build toolchain, never shipped.
- No new package manager introduced — plain `pip` + PEP 621 `pyproject.toml`
  remains sufficient for a zero-runtime-dependency package.

Fresh clean-room reconstruction from committed state is verified to
reproduce byte-for-byte identical package versions (`pip check` clean, no
broken requirements) — see "Build / test locally" below for the exact
reconstruction commands.

## Build / test locally

```bash
cd python/structure-engine
python3.13 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip==25.2

# Exact reconstruction from committed lock state (no resolver involved):
pip install --no-deps -r requirements-dev.lock.txt
pip install -e . --no-deps
pip check   # -> "No broken requirements found."

ruff format .
ruff check .
mypy
pytest tests/ -v
```

(`pip install -e ".[dev]"` also works for day-to-day development — it lets
pip's resolver pick up the exact pins from `pyproject.toml` directly — but
the two-step `--no-deps` sequence above is the one that reproduces the
committed lock exactly, with no resolver freedom at all.)

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
