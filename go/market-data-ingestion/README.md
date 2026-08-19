# market-data-ingestion

Phase 3 Data Layer Batch 01 implementation. Governed by `module-registry.yaml`
(`market-data-ingestion`), Package 1.3-A
(`docs/architecture/engine/structure-regime-architecture.md` §2.2), and the
Candle Domain Contract (`docs/domain/candle.md`, v0.4, Draft).

## Scope of this transaction

Implemented: the domain core of `market-data-ingestion` — Candle identity/
state machine, the Chapter 8 §8.2 event envelope, the candle.md §11 5-step
duplicate/correction/fail-closed precedence algorithm, candle.md §12
missing-data handling (the `complete_zero_volume` 5-condition gate and
`CandleDataGapObserved` reason mapping), and an orchestration service tying
these together — all with real, passing unit tests (`go test ./...`).

Explicitly **not** implemented, by task instruction: Structure Engine, Raw
Regime Engine, LIVE exchange connectivity/credentials/order execution, any
change to the module dependency graph, any change to architecture docs, any
Phase 3 Definition of Done, any module/package approval.

## Ports instead of infrastructure

Two dependencies this module needs do not exist yet anywhere in the
repository, and inventing them would mean silently making an architecture
decision this transaction is not authorized to make. Both are represented
as narrow Go interfaces (ports) with only test-double implementations:

- **`internal/reference.Provider`** — market-reference-service
  (venue/instrument identity resolution + calendar/session window
  resolution). `internal/reference.Fake` is a 24/7, UTC-aligned test
  double — explicitly not a real trading-calendar implementation.
- **`internal/publish.EventPublisher`** — the append boundary that would
  resolve `stream-registry.yaml` and allocate `sequence`/`producer_ref`
  atomically with append (Chapter 8 §8.3.2).
  `internal/publish.Memory` is a single-process in-memory test double.

Both gaps are pre-existing and independently confirmed by
`docs/architecture/engine/structure-regime-architecture.md` §13 ("Open
Domain và architecture gaps"): `stream-registry.yaml` is explicitly
un-authored there too, for the same reason (Phase 1/implementation
concern, not architecture-level).

No real venue adapter exists either — `internal/ingest.Service` accepts
already venue-adapter-normalized `RawFact` values; nothing in this module
talks to a real exchange.

## Deferred: market-reference-service itself

`market-reference-service` (the other module in this batch,
`depends_on: []`) is **not implemented** in this transaction. Two
independent, pre-existing blockers, neither invented here:

1. **Language assignment does not resolve.** ADR-008 pins Python to
   {Feature Engineering, Strategy, Decision logic, Backtest Engine} and Go
   to {Market Data Ingestion, Risk Gateway, Execution Engine} — by
   capability nature, not by name (`docs/engineering/monorepo.md` §4).
   `market-reference-service`'s responsibility (authoritative
   Instrument/Venue identity, precision/tick/lot metadata, trading
   calendar/session — reference/master-data ownership) does not fit either
   layer's stated rationale. This needs either a governed layer-application
   decision or a new ADR — not a silent choice made in code.
2. **Its own Domain Contracts are unresolved.** `docs/domain/instrument.md`
   (v0.6, Draft, six correction rounds) and `docs/domain/venue.md` both
   explicitly defer the concrete calendar/session/precision-resolution
   mechanism to implementation time ("Phase 1, chưa author" — venue.md
   §8/§17). Building `market-reference-service` now would mean inventing
   that mechanism silently.

**Escalation:** both points require a governance decision (ADR or a
build-time ADR-008 layer-application ruling, plus resolution of the
instrument/venue calendar/session/precision design) before
`market-reference-service` can be built. `market-data-ingestion` depends on
it only through `internal/reference.Provider`, so this deferral does not
block `market-data-ingestion`'s own implementation.

## Implementation-level decisions made at this build transaction

candle.md §17 explicitly defers these to implementation; the choices below
apply here and are not architecture decisions:

- `candle_subject_id`: SHA-256 content hash of the five-field scope,
  canonicalized to UTC RFC3339Nano before hashing
  (`internal/candle.Scope.SubjectID`). Domain logic never parses it
  (Chapter 6 §6.8).
- `event_contract_ref.contract_version`: pinned to candle.md's own document
  version ("0.4") per event concept, since candle.md does not yet version
  each event concept independently. Revisit if candle.md is Approved with
  per-event contract versioning.
- `delayed_beyond_threshold`: modeled as an externally-configured
  `time.Duration` (`internal/gap.DelayEvaluator`), never hardcoded.
- Precedence algorithm's "first-ever fact for a subject" case: candle.md
  §11 Steps 3-5 all presuppose a prior processed fact to compare against;
  the case where none exists is treated as the subject's first
  authoritative close. See `internal/precedence` package doc for the full
  reasoning.
- Financial values (OHLCV) use `internal/decimal`, a minimal
  arbitrary-precision decimal type backed by `math/big`, parsed directly
  from strings — never round-tripped through `float64` at any step
  (Constitution I-9).

## Not built (needs its own scoped transaction, not silently added here)

- A real venue adapter (WS/REST) for any specific exchange.
- A real `market-reference-service` client / implementation.
- Real event-log/broker wiring (`stream-registry.yaml` + a real
  `EventPublisher`).
- `CandleCurrentView` read-model projection (candle.md §7) — not required
  by this batch's two modules; the authoritative event stream is what
  downstream consumers (Structure/Regime Engine) read from per
  `structure-regime-architecture.md` §3.
- Venue/session-closed handling (candle.md §12 case one) beyond the port
  shape (`reference.ErrSessionClosed`) — resolving it fully needs the
  `instrument-venue-reference` Domain Contract, which does not exist yet.

## Toolchain

Go minimum version verified directly against <https://go.dev/doc/devel/release>
at this build transaction (2026-08-19): Go supports the two newest major
releases (currently 1.26 and 1.25). `go.mod` pins `go 1.25` (the oldest
still-supported major release) as the minimum; built and tested locally
with go1.26.6. Formatting/linting: `gofmt` and `go vet`, both bundled with
the toolchain (`docs/engineering/coding-standard.md` §1/§2) — no
third-party linter chosen. Testing: standard library `testing` only, table-
driven where useful (`docs/engineering/testing.md` §10) — no third-party
test framework chosen (none is pinned anywhere in this repository yet).

## Running

```sh
cd go/market-data-ingestion
go build ./...
go vet ./...
go test ./...
go run ./cmd/marketdataingestion   # demo wiring, fakes only
```
