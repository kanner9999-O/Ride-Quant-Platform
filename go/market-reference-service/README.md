# market-reference-service

Phase 3 Data Layer completion. Governed by `module-registry.yaml`
(`market-reference-service`), **ADR-032 v0.2 (Approved)**, and the
Instrument/Venue Domain Contracts (`docs/domain/instrument.md` v0.6,
`docs/domain/venue.md` v0.3, both Draft).

## Scope of this transaction

Implemented: the domain core of `market-reference-service` — Instrument
(`instrument.md` §1-§9) and Venue (`venue.md` §1-§9, "áp dụng nguyên văn")
identity/registration/correction-lineage/metadata-revision/status-lifecycle,
TradableListing (`instrument.md` §10-§15 Bước 1-3) creation/metadata/status,
and a **generic bitemporal fold engine** (`internal/fact`) implementing
`instrument.md` §7/§18/§19/§20's registration-lineage-head resolution,
`EXPLICIT_PATCH_WITH_CLEAR_SET` metadata patch fold, and the 5-phase
`RECORDED_VISIBILITY_THEN_EFFECTIVE_ORDER` status fold — applied identically
to all three entities, exactly as the Domain Contract requires ("áp dụng
nguyên văn"). All with real, passing unit tests (`go test ./...`), including
an explicit look-ahead guard test at the query-service boundary.

The query boundary (`internal/query.Service`) implements **ADR-032 v0.2
§B.3's two-axis bitemporal contract exactly**: every query takes an
effective-applicability instant and a knowledge (recorded_time/Replay
Cursor) boundary as two separate, mandatory, independent parameters, and
resolves the deterministic intersection of the two — never one alone.

## ADR-032 compliance

- **Language: Go.** Per ADR-032 §B.1 (Approved) — capability-nature match
  (I/O + reliability), not module-name similarity.
- **Sole authoritative owner.** `market-reference-service` owns Instrument/
  Venue identity, precision/tick/lot, calendar/session (I-12) — nothing in
  `market-data-ingestion` duplicates this authority (see the alignment
  note below).
- **Two-axis query contract (ADR-032 §B.3, v0.2), all three lookups.**
  `query.Service.ResolveIdentity`/`ResolveWindow`/`ResolvePrecision` each
  take `(effectiveInstant, knowledgeCursor time.Time)` as two independent
  parameters — never a single ambiguous temporal parameter, and never a
  current/static mapping. **`ResolveIdentity` was corrected under
  `P3-DL-A-MAJ-01`**: it originally went through a static `bySymbol` map
  with neither axis. It now reverse-scans the already-modeled bitemporal
  fold: `resolveVenueID` matches a `VenueRegistered` fact's
  `venue_identity_ref` (visible/effective per the cursor pair), and
  `resolveListingByVenueSymbol` resolves each candidate
  `TradableListing`'s `venue_symbol` via `listing.ResolveView` at the exact
  same cursor pair — `venue_symbol` is already a forward-looking,
  bitemporally-revisable field (`instrument.md` §12's
  `EXPLICIT_PATCH_WITH_CLEAR_SET` whitelist), so no new Domain Contract
  semantics were needed to fix this, only correct implementation against
  what already existed. `effective_time` alone never controls visibility;
  a correction's visibility is governed solely by `knowledgeCursor`,
  matching `instrument.md` §20's own selection algorithm ("latest valid
  fact với `effective_time <= cursor` VÀ `recorded_time <= replay
  cursor"") — ADR-032's contract and `instrument.md`'s pre-existing Draft
  semantics agree exactly; this transaction did not need to invent
  anything new here, only implement what both already specified. Proven
  by `internal/query/service_test.go`'s `TestResolvePrecisionLookAheadGuard`
  and `TestResolveIdentityLookAheadGuard`: a correction recorded later is
  invisible to an earlier knowledge cursor, and the same effective instant
  resolves differently only once the knowledge cursor advances past the
  correction's `recorded_time`.
- **Deferred, unchanged by this transaction (ADR-032 §B.3 points 3-4):**
  transport/API serialization (this module exposes a Go interface, not a
  network API — no RPC/HTTP chosen) and the internal calendar/session/
  precision-computation *algorithm* (see `internal/calendar` below).

## Scope descope: `ActiveListingReservation` (`instrument.md` §16)

`instrument.md` §16 defines a full pair-scoped activation-arbitration
protocol (`ActiveListingActivationRequested`/`Reserved`/
`ActivationRejected`/`ReservationReleased`/`ReservationFactInvalidated`,
idempotency, terminal request disposition) governing which listing wins
*contended* activation. `TradableListingCreated`'s own invariants make a
minimal slice of this structurally mandatory (a valid `TradableListingCreated`
cannot exist without a matching `ActiveListingReserved`) — `listing.
CreateListing` implements exactly that mandatory happy path
(`Requested -> Reserved -> Created`, correctly causally linked, matching
`activation_request_id`) and nothing else from §16: no rejection path, no
release, no reservation correction lineage, no contested-request
arbitration. Every event this package emits matches `instrument.md`'s
schema exactly — this is a bounded **implementation-scope** decision (a
subset of already-fully-specified semantics), not an invented or altered
domain semantic, and not a `DOMAIN_CONTRACT_DECISION_REQUIRED` situation.
See `internal/listing/listing.go`'s package doc for the full reasoning.

Consequence: `TradableListingCurrentView`'s full 7-step fold (`instrument.md`
§15) is **not** implemented — only Steps 1-3 (this package's `ResolveView`).
Steps 4-5 (cross-subject Instrument/Venue-RETIRED eligibility) and Step 6
(reservation-state fold) are not exercised by `query.Service`'s three
methods, which only need Steps 1-3's resolved fields (venue_symbol,
price/quantity increment, session_calendar_ref, current_status) —
`market-data-ingestion` never asks for `eligibility_state`.

## `internal/calendar`: session/calendar resolution mechanism

`venue.md` §17 and `candle.md` §17 both explicitly defer the *concrete*
calendar/session-resolution algorithm to implementation ("calendar/timezone/
reference service, Phase 1"), and ADR-032 §B.3 point 3 assigns that decision
to this build transaction. ADR-007 forbids hardcoding a single universal
session model ("KHÔNG được giả định... 24/7... một session per day") — so
`calendar.Calendar` is an interface, resolved per-venue via an opaque
`session_calendar_ref` (`venue.md` §8), not a hardcoded global rule. Only one
concrete implementation exists in this transaction: `calendar.Continuous`
(24/7, UTC-aligned) — matching ADR-007's current actual deployment scope
("nội bộ/crypto trước") and the same assumption `market-data-ingestion`'s
Batch 01 `reference.Fake` already used. A traditional exchange-hours
calendar (open/close/holidays) is a natural future extension via the same
interface, requiring no architecture change — not built here because
nothing in this transaction's scope exercises it.

## Not built (needs its own scoped transaction, not silently added here)

- Real durable storage / a real `stream-registry.yaml`-backed event log —
  `internal/store.Memory` is an in-memory test double (same gap
  `market-data-ingestion`'s `internal/publish` documents, independently
  confirmed absent by Package 1.3-A §13's own open-gaps list).
- **Fixed under `P3-DL-A-MAJ-01`** (previously listed here as not built): a
  bitemporal symbol-to-listing resolution mechanism — `query.Service` no
  longer holds a static `bySymbol` map; `ResolveIdentity` now reverse-scans
  `VenueRegistered`/`TradableListingCreated` facts and resolves each
  candidate listing's `venue_symbol` through `listing.ResolveView` at the
  requested two-axis cursor pair (see "ADR-032 compliance" above). Still
  not built: an *indexed* (non-linear-scan) implementation — the current
  scan is O(n) over all registered venues/listings, acceptable for this
  transaction's scope (a handful of fixtures) but not a real deployment's
  performance characteristic; that is a separate, later optimization, not
  a correctness gap.
- The full `ActiveListingReservation` arbitration protocol (see above).
- A traditional exchange-hours `Calendar` implementation (see above).
- `InstrumentCurrentView`/`VenueCurrentView`/`TradableListingCurrentView` as
  independently queryable read-model projections — this transaction's
  `ResolveView` methods compute the same fold on demand, which is
  sufficient for `query.Service`'s needs; a materialized, independently
  queryable projection is a separate concern (Chapter 7 §7.4).

## Toolchain

Same as `market-data-ingestion`: Go minimum version verified directly
against <https://go.dev/doc/devel/release> (Go supports the two newest
major releases; `go.mod` pins `go 1.25`, built/tested with go1.26.6).
`gofmt`/`go vet` only, standard library `testing` only — no third-party
tooling chosen (none pinned anywhere in this repository).

## Running

```sh
cd go/market-reference-service
go build ./...
go vet ./...
go test ./...
go run ./cmd/marketreferenceservice   # demo wiring
```
