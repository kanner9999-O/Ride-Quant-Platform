# raw-regime-engine

Authoritative Raw Regime Engine: `volatility` / `directional_persistence`
regime classification directly over canonical Candle facts
(`docs/domain/regime.md`). `module_id: raw-regime-engine` per
`docs/architecture/module-registry.yaml`. Implementation language (Python)
resolved by [ADR-033](../../docs/adr/ADR-033.md) (Approved). Structurally
independent from Structure Engine — [ADR-014](../../docs/adr/ADR-014.md) /
`forbidden_dependencies: [structure-engine]` on this module's own registry
entry.

This is the **analytical core only** — no broker, no RPC/HTTP, no
Go↔Python transport, no deployment/process topology, no real event log, no
venue connectivity, and **no concrete production formula/threshold values**
(see "The formula boundary" below). Those are all separate, future governed
decisions.

## What this module owns

- `RegimeClassified` / `RegimeFactInvalidated` facts for exactly two
  dimensions: `volatility` and `directional_persistence` (`regime.md`).
- The non-authoritative `RegimeCurrentView` projection (`regime.md` §11).

## What this module never does

- Consume Structure, Swing, Feature, Context, Strategy, Account, or Risk —
  `regime.md` §13's input contract is exactly candle-closed/candle-corrected,
  nothing else. This package has no import of, and no dependency on, any
  `structure_engine` module (`test_no_structure_engine_import` enforces this
  directly on the committed source tree).
- Invent a canonical ATR/ADX/efficiency-ratio/realized-volatility/
  trend-score/moving-average formula, or a production threshold value —
  `regime.md` §19 deliberately defers both to configuration. Only
  clearly-labeled `test-*` formulas exist in this repository.
- Add Activity/Liquidity/Structure-aware regime — `module-registry.yaml`'s
  own "DEFERRED COVERAGE" note blocks that responsibility on a Domain
  Context/Capability registration decision that has not happened yet; out of
  this module's scope.
- Assign its own Quality Tier or claim a formal Chapter 13 Quality Gate
  result — both are separate governed prerequisites.

## The formula boundary

`regime.md` intentionally does not select a concrete metric formula. This
engine is generic over an injected `MetricFormula` (a `formula_id` +
`compute(evidence) -> Decimal`) and an explicit, immutable
`RegimeDefinition`/`RegimeDimensionDefinition` supplying per-dimension
`window_candle_count`, `class_thresholds` (caller-supplied `Decimal`
boundaries — never hardcoded), `threshold_comparison_policy`
(`strict`/`inclusive`), `warm_up_policy`, `gap_policy`, and a
`decimal_precision_policy` (stdlib `decimal` rounding mode only). The engine
fails closed (`FormulaMismatchError`) if the supplied formula's own
`formula_id` does not match the definition's pinned `metric_formula_id` —
there is no global formula registry to fall back on. `class_thresholds`
labels are still validated against `regime.md`'s own closed vocabulary per
dimension (`volatility`: `LOW|NORMAL|HIGH|EXTREME`; `directional_persistence`:
`NON_DIRECTIONAL|DIRECTIONAL|TRANSITIONAL`) — a domain fact, not a threshold
value, so this validation does not reintroduce a canonical formula.

## Package layout

```
src/raw_regime_engine/
  identity.py    deterministic opaque subject-id derivation (module-local — regime.md
                 §19 leaves the concrete algorithm unspecified). Duplicated, not
                 imported, from structure-engine's own identity.py (see below).
  envelope.py    Chapter 8 §8.2 event-record identity shapes (EventRecordRef/StreamRef/ProducerRef)
  publish.py     in-process, per-stream contiguous sequence allocation (ADR-009) — a
                 bounded stand-in for the stream-registry.yaml infrastructure that does
                 not exist yet (Phase 1)
  candle.py      authoritative Candle input (CandleScope/OHLCV/CandleFact)
  regime.py      RegimeDefinition/RegimeDimensionDefinition/ThresholdBand/
                 DecimalPrecisionPolicy/MetricFormula/RegimeScope/
                 RegimeClassified/RegimeFactInvalidated/RegimeEngine/
                 RegimeCurrentView/RegimeViewResult
  errors.py      explicit technical failure modes (Error Handling Convention §7),
                 plus FormulaMismatchError/RegimeLineageError specific to Raw Regime
tests/
  conftest.py     candle/definition/formula test fixtures (TEST-ONLY MetricFormula
                  implementations, clearly labeled — never production-canonical)
  test_regime.py  warm-up/every-window-emits, both dimensions, threshold boundary
                  (strict/inclusive), decimal precision, formula-id mismatch,
                  evidence normalization (order-independence), duplicate-computation
                  idempotency, correction invalidate+replace (incl. unchanged-class
                  and multi-window-overlap cases), RegimeCurrentView lineage
                  invariants/pending-correction/no-fallback, historical cadence,
                  per-scope ordering/foreign-scope, deterministic replay, no
                  Structure import
```

**Why this package duplicates `identity.py`/`envelope.py`/`publish.py`/
`candle.py` instead of importing structure-engine's:** ADR-014's Structure/
Regime independence is structural, and each Python module is independently
built/deployed (Chapter 3 §3.1). Duplicating these small, self-contained
building blocks (rather than sharing them across a forbidden-dependency
boundary) mirrors the existing, already-governed precedent of
`market-reference-service` holding its own independent copy of a Go decimal
package originally duplicated from `market-data-ingestion`.

The engine (`RegimeEngine`) is pure, deterministic, in-process, and holds no
network dependency — a caller drives it by calling `on_candle` in cursor
order. Unlike Swing (which has a provisional Candidate stage to suppress in
historical mode), Raw Regime has no historical/streaming split at all:
`regime.md` §9 requires every completed window to emit a fact regardless of
mode, so there is exactly one algorithm, used identically for
Replay/Backtest/Paper/Live (Chapter 3 §3.1).

## First-Python-build toolchain reused (this module reuses, not re-derives, structure-engine's baseline)

Per the governing task's own instruction, this module reuses
`structure-engine`'s already-verified first-Python-build baseline rather than
re-deriving it from scratch, with its **own independent reproducible
environment evidence** (not shared files):

**Python >= 3.13** — same validated *compatibility floor* rationale as
`structure-engine` (see that module's README for the full corrected
rationale; not a "longest support runway" claim). Interpreter used to build
and verify this module: Python 3.13.6 (CPython, arm64, macOS-14.5-arm64-
arm-64bit-Mach-O) — identical to structure-engine's own build machine, not
independently re-verified against a different machine.

| Concern | Tool | Pinned version | Why |
|---|---|---|---|
| Formatter | `ruff format` | `0.16.4` | Re-verified as still the current release on PyPI at this module's build time; reused unchanged (no cosmetic bump). |
| Lint / static analysis | `ruff check` | `0.16.4` | Same reasoning. |
| Type checking | `mypy --strict` | `2.3.1` | Re-verified current on PyPI; reused unchanged. |
| Test framework | `pytest` | `9.1.1` | Re-verified current on PyPI; reused unchanged. |

No numerical/data-science stack is used — **zero runtime dependencies**;
`decimal.Decimal` (stdlib) provides lossless arbitrary-precision arithmetic
for every authoritative numerical value (`computed_metric`, OHLCV fields,
threshold boundaries) — never binary float.

### Reproducible build/dev environment

- **Build backend:** `[build-system].requires` pins `setuptools==84.0.0` exactly.
- **Full transitive dev/build dependency state:**
  [`requirements-dev.lock.txt`](./requirements-dev.lock.txt) — generated via
  `pip freeze --exclude-editable` from a **fresh venv built specifically for
  this module** (not copied from structure-engine's own lock file, even
  though both currently resolve to identical versions on this machine).
- **Exact interpreter/install mechanism used:** Python 3.13.6; pip 25.2
  (`pip install --upgrade pip==25.2` before installing this project).
- **Zero production runtime dependencies** — `[project].dependencies` is empty.

Fresh clean-room reconstruction from committed state is verified to
reproduce a working, `pip check`-clean environment — see "Build / test
locally" below for the exact reconstruction commands.

## Build / test locally

```bash
cd python/raw-regime-engine
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

Coverage may be collected for local diagnostics (`coverage run -m pytest &&
coverage report`) but is **NON-FORMAL / INFORMATIONAL ONLY** (97% at build
time) — this module's Quality Tier is unresolved, so no formal Chapter 13
Quality Gate result can be claimed for it yet.

## ADR Scope Rule

`ADR_NOT_REQUIRED` — this is a module-local implementation of already-
governed authority (ADR-033's language decision, `regime.md`'s existing
Domain Contract semantics, Chapter 3 §3.1's authoritative-implementation
rule). No new/changed Event or Domain Contract semantic, no dependency graph
change, no authority transfer, no cross-module semantic contract, no runtime-
topology decision, no security/custody boundary, and — critically — **no
concrete production formula or threshold value was selected**: every design
choice made while building this module stayed within regime.md's own
generic engine boundary. Where regime.md explicitly defers a concrete
mechanism (subject-id derivation, the ascending-threshold-band classification
scan, the rolling-window cadence model), this module pins one bounded,
documented interpretation in code, not a governance decision.

## Current state (as of this build)

- Raw Regime Engine: implemented (engine semantics only) — no production
  `RegimeDefinition`/`MetricFormula` instance exists or is claimed; those
  remain externally unresolved configuration.
- Raw Regime Quality Tier: **UNRESOLVED** — not assigned in this transaction.
- Structure Engine: unchanged by this transaction — remains implemented, not
  Product-Owner-approved, Quality Tier unresolved.
- No formal Chapter 13 Quality Gate claimed for either module.
- No module-level, Data-Layer-level, or Phase-3-level approval implied.
- LIVE: **NOT_AUTHORIZED**.
