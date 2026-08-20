package query

import (
	"context"
	"testing"
	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/calendar"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/decimal"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/envelope"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/instrument"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/listing"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/store"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/venue"
)

func buildListingMetadataDraft(scope listing.Scope, recordedTime, effectiveTime time.Time) envelope.Draft {
	return envelope.Draft{
		EventID:   "evt-correction-" + recordedTime.String(),
		EventType: listing.EventTypeMetadataRevised,
		EventContractRef: envelope.ContractRef{
			ContractID:      listing.ContractIDMetadataRevised,
			ContractVersion: "0.6",
		},
		SchemaVersion: 1,
		RecordedTime:  recordedTime,
		SubjectRef: envelope.SubjectRef{
			ContextID:   "instrument-venue-reference",
			SubjectKind: "entity",
			SubjectType: "TradableListing",
			SubjectID:   scope.ListingID,
		},
		CausationRefs:    []envelope.EventRecordRef{},
		RelatedEventRefs: []envelope.EventRecordRef{},
		EffectiveTime:    effectiveTime,
	}
}

const rawVenueID = "binance-spot"

type fixture struct {
	svc          *Service
	instrumentID string
	venueID      string
	listingScope listing.Scope
}

func setup(t *testing.T) fixture {
	t.Helper()
	ctx := context.Background()
	s := store.NewMemory("market-reference-service", "v0.1.0-dev", "test-run")
	instruments := instrument.NewRegistry(s)
	venues := venue.NewRegistry(s)
	listings := listing.NewRegistry(s)
	calendars := calendar.NewResolver(map[string]calendar.Calendar{"cal-crypto-247": calendar.NewContinuous()})
	svc := NewService(instruments, venues, listings, calendars)

	t0 := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)
	insScope := instrument.Scope{InstrumentIdentityRef: "btc-usdt", BaseAssetRef: "BTC", QuoteAssetRef: "USDT", InstrumentType: "SPOT"}
	insRef, err := instruments.Register(ctx, "ins-reg", insScope, "BTC/USDT", t0, t0)
	if err != nil {
		t.Fatalf("Register instrument: %v", err)
	}
	// VenueIdentityRef intentionally matches rawVenueID — ResolveIdentity
	// treats the raw venue reference as the Venue's venue_identity_ref
	// (venue.md §1's opaque external reference, see query package doc).
	venScope := venue.Scope{VenueIdentityRef: rawVenueID, VenueType: "CENTRALIZED_EXCHANGE"}
	venRef, err := venues.Register(ctx, "ven-reg", venScope, "Binance", "UTC", "cal-crypto-247", "prec-default", t0, t0)
	if err != nil {
		t.Fatalf("Register venue: %v", err)
	}

	lstScope := listing.Scope{InstrumentID: insScope.InstrumentID(), VenueID: venScope.VenueID(), ListingID: "lst_1"}
	_, err = listings.CreateListing(ctx, listing.CreateListingInput{
		Scope: lstScope, VenueSymbol: "BTCUSDT",
		PriceIncrement: decimal.MustFromString("0.01"), QuantityIncrement: decimal.MustFromString("0.0001"),
		SessionCalendarRef: "cal-crypto-247", ActivationRequestID: listing.DeterministicActivationRequestID(lstScope),
		InstrumentRegistered: insRef, VenueRegistered: venRef,
		RecordedTime: t0, EffectiveTime: t0,
		RequestEventID: "evt-req", ReservedEventID: "evt-res", CreatedEventID: "evt-created",
	})
	if err != nil {
		t.Fatalf("CreateListing: %v", err)
	}

	return fixture{svc: svc, instrumentID: insScope.InstrumentID(), venueID: venScope.VenueID(), listingScope: lstScope}
}

func TestResolveIdentityKnown(t *testing.T) {
	f := setup(t)
	instant := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)
	id, err := f.svc.ResolveIdentity(rawVenueID, "BTCUSDT", instant, instant.Add(time.Hour))
	if err != nil {
		t.Fatalf("ResolveIdentity error: %v", err)
	}
	if id.InstrumentID != f.instrumentID || id.VenueID != f.venueID {
		t.Fatalf("got %+v, want {%s %s}", id, f.instrumentID, f.venueID)
	}
}

func TestResolveIdentityUnknown(t *testing.T) {
	f := setup(t)
	instant := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)
	_, err := f.svc.ResolveIdentity("unknown-venue", "XXXX", instant, instant.Add(time.Hour))
	if err != ErrUnknownReference {
		t.Fatalf("got %v, want ErrUnknownReference", err)
	}
}

// TestResolveIdentityNotYetVisibleAtKnowledgeCursor proves the identity
// registration itself is subject to the knowledge axis: a query with a
// knowledge cursor before the listing/venue/instrument were even recorded
// must not resolve them (P3-DL-A-MAJ-01).
func TestResolveIdentityNotYetVisibleAtKnowledgeCursor(t *testing.T) {
	f := setup(t)
	instant := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)
	_, err := f.svc.ResolveIdentity(rawVenueID, "BTCUSDT", instant, instant.Add(-time.Hour)) // knowledge cursor before registration was recorded
	if err != ErrUnknownReference {
		t.Fatalf("got %v, want ErrUnknownReference (registration not yet visible)", err)
	}
}

func TestResolveWindow(t *testing.T) {
	f := setup(t)
	instant := time.Date(2026, 8, 19, 10, 0, 37, 0, time.UTC)
	w, err := f.svc.ResolveWindow(f.instrumentID, f.venueID, "1m", instant, instant.Add(time.Hour))
	if err != nil {
		t.Fatalf("ResolveWindow error: %v", err)
	}
	wantStart := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)
	if !w.Start.Equal(wantStart) {
		t.Fatalf("got Start=%v, want %v", w.Start, wantStart)
	}
}

func TestResolvePrecision(t *testing.T) {
	f := setup(t)
	instant := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)
	p, err := f.svc.ResolvePrecision(f.instrumentID, f.venueID, instant, instant.Add(time.Hour))
	if err != nil {
		t.Fatalf("ResolvePrecision error: %v", err)
	}
	if !p.PriceIncrement.Equal(decimal.MustFromString("0.01")) {
		t.Fatalf("PriceIncrement = %s, want 0.01", p.PriceIncrement.String())
	}
}

// TestResolvePrecisionLookAheadGuard is the core ADR-032 §B.3 acceptance
// test at the query.Service boundary: a correction recorded later must not
// leak into an earlier knowledge-cursor query, and effective_time alone
// must not control visibility.
func TestResolvePrecisionLookAheadGuard(t *testing.T) {
	ctx := context.Background()
	f := setup(t)
	instant := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)

	// Baseline: original precision resolves.
	before, err := f.svc.ResolvePrecision(f.instrumentID, f.venueID, instant, instant.Add(time.Minute))
	if err != nil {
		t.Fatalf("ResolvePrecision (before correction) error: %v", err)
	}
	if !before.PriceIncrement.Equal(decimal.MustFromString("0.01")) {
		t.Fatalf("before correction: PriceIncrement = %s, want 0.01", before.PriceIncrement.String())
	}

	// A correction is recorded later, changing price_increment, effective
	// retroactively at the SAME effective instant window (forward-looking
	// metadata patch effective at instant.Add(-time.Hour), well before our
	// query instant, so it applies going forward through `instant`).
	correctionRecordedAt := instant.Add(time.Hour)
	if _, err := f.svc.Listings.Store.Append(ctx, buildListingMetadataDraft(f.listingScope, correctionRecordedAt, instant.Add(-time.Hour)), listing.MetadataRevisedPayload{
		ListingID:     f.listingScope.ListingID,
		ChangedFields: map[string]string{"price_increment": "0.001"},
	}); err != nil {
		t.Fatalf("append correction: %v", err)
	}

	// A query with a knowledge cursor BEFORE the correction was recorded
	// must still see the original value — the correction must not leak
	// backward.
	stillOld, err := f.svc.ResolvePrecision(f.instrumentID, f.venueID, instant, correctionRecordedAt.Add(-time.Minute))
	if err != nil {
		t.Fatalf("ResolvePrecision (knowledge cursor before correction) error: %v", err)
	}
	if !stillOld.PriceIncrement.Equal(decimal.MustFromString("0.01")) {
		t.Fatalf("got PriceIncrement=%s at a knowledge cursor BEFORE the correction was recorded, want unchanged 0.01 (look-ahead leak)", stillOld.PriceIncrement.String())
	}

	// A query with a knowledge cursor AFTER the correction was recorded
	// sees the corrected value, for the SAME effective instant — proving
	// effective_time alone does not control visibility; the knowledge
	// cursor does.
	afterCorrection, err := f.svc.ResolvePrecision(f.instrumentID, f.venueID, instant, correctionRecordedAt.Add(time.Minute))
	if err != nil {
		t.Fatalf("ResolvePrecision (knowledge cursor after correction) error: %v", err)
	}
	if !afterCorrection.PriceIncrement.Equal(decimal.MustFromString("0.001")) {
		t.Fatalf("got PriceIncrement=%s at a knowledge cursor AFTER the correction was recorded, want corrected 0.001", afterCorrection.PriceIncrement.String())
	}

	// Current wall clock is irrelevant: querying with an explicit knowledge
	// cursor from the past never depends on time.Now().
	_ = time.Now() // documents the assertion above already proves this: no call in this test path reads wall-clock time.
}

// TestResolveIdentityLookAheadGuard is the P3-DL-A-MAJ-01 acceptance test:
// identity resolution (venue_symbol -> canonical instrument/venue ID) must
// obey the same two-axis bitemporal contract as window/precision
// resolution. A rebrand (TradableListingMetadataRevised changing
// venue_symbol, instrument.md §12) recorded later must not leak into an
// earlier knowledge-cursor identity query, and the OLD raw symbol must
// keep resolving at cursors before the rebrand was recorded — proving
// effective_time alone does not control visibility.
func TestResolveIdentityLookAheadGuard(t *testing.T) {
	ctx := context.Background()
	f := setup(t)
	effectiveInstant := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)

	// 1. Identity mapping A ("BTCUSDT") is effective at effectiveInstant —
	// baseline resolution.
	before, err := f.svc.ResolveIdentity(rawVenueID, "BTCUSDT", effectiveInstant, effectiveInstant.Add(time.Minute))
	if err != nil {
		t.Fatalf("ResolveIdentity (before rebrand) error: %v", err)
	}
	if before.InstrumentID != f.instrumentID || before.VenueID != f.venueID {
		t.Fatalf("got %+v, want {%s %s}", before, f.instrumentID, f.venueID)
	}

	// 2. A corrected/revised mapping B ("XBTUSDT", a venue-side rebrand) is
	// recorded later — instrument.md §12 explicitly authorizes venue_symbol
	// as a forward-looking, whitelist-patchable field via
	// TradableListingMetadataRevised, so this correction is within existing
	// Domain Contract semantics, not an invented rule.
	rebrandRecordedAt := effectiveInstant.Add(time.Hour)
	rebrandEffectiveAt := effectiveInstant.Add(-30 * time.Minute) // forward-looking from a point before our query instant, so it applies going forward through effectiveInstant once visible
	if _, err := f.svc.Listings.Store.Append(ctx, buildListingMetadataDraft(f.listingScope, rebrandRecordedAt, rebrandEffectiveAt), listing.MetadataRevisedPayload{
		ListingID:     f.listingScope.ListingID,
		ChangedFields: map[string]string{"venue_symbol": "XBTUSDT"},
	}); err != nil {
		t.Fatalf("append rebrand: %v", err)
	}

	// 3. Query at effective_instant + an EARLIER knowledge cursor (before
	// the rebrand was recorded) must still resolve the OLD symbol
	// ("BTCUSDT") to the same identity — the rebrand must not leak
	// backward.
	stillOld, err := f.svc.ResolveIdentity(rawVenueID, "BTCUSDT", effectiveInstant, rebrandRecordedAt.Add(-time.Minute))
	if err != nil {
		t.Fatalf("ResolveIdentity (knowledge cursor before rebrand, old symbol) error: %v", err)
	}
	if stillOld.InstrumentID != f.instrumentID || stillOld.VenueID != f.venueID {
		t.Fatalf("got %+v at knowledge cursor before rebrand, want unchanged {%s %s} (look-ahead leak)", stillOld, f.instrumentID, f.venueID)
	}
	// The NEW symbol must NOT resolve yet at this earlier knowledge cursor.
	if _, err := f.svc.ResolveIdentity(rawVenueID, "XBTUSDT", effectiveInstant, rebrandRecordedAt.Add(-time.Minute)); err != ErrUnknownReference {
		t.Fatalf("got err=%v for new symbol at knowledge cursor before rebrand, want ErrUnknownReference", err)
	}

	// 4. SAME effective_instant, knowledge cursor AFTER the rebrand was
	// recorded: the NEW symbol ("XBTUSDT") now resolves to the same
	// canonical identity — the Domain Contract semantics (forward-looking
	// metadata revision) authorize this.
	afterRebrand, err := f.svc.ResolveIdentity(rawVenueID, "XBTUSDT", effectiveInstant, rebrandRecordedAt.Add(time.Minute))
	if err != nil {
		t.Fatalf("ResolveIdentity (knowledge cursor after rebrand, new symbol) error: %v", err)
	}
	if afterRebrand.InstrumentID != f.instrumentID || afterRebrand.VenueID != f.venueID {
		t.Fatalf("got %+v, want {%s %s}", afterRebrand, f.instrumentID, f.venueID)
	}
	// The OLD symbol must no longer resolve at this later knowledge cursor
	// (venue_symbol is a single-valued field — the patch supersedes it).
	if _, err := f.svc.ResolveIdentity(rawVenueID, "BTCUSDT", effectiveInstant, rebrandRecordedAt.Add(time.Minute)); err != ErrUnknownReference {
		t.Fatalf("got err=%v for old symbol at knowledge cursor after rebrand, want ErrUnknownReference (old symbol superseded)", err)
	}

	// 5. Determinism: identical cursor pairs resolve identically.
	repeat, err := f.svc.ResolveIdentity(rawVenueID, "XBTUSDT", effectiveInstant, rebrandRecordedAt.Add(time.Minute))
	if err != nil {
		t.Fatalf("ResolveIdentity (repeat) error: %v", err)
	}
	if repeat != afterRebrand {
		t.Fatalf("got %+v on repeat query with identical cursor pair, want %+v (deterministic resolution)", repeat, afterRebrand)
	}
}

// TestResolvePrecisionMalformedMetadataFailsClosedNoPanic is the
// P3-MR-DECIMAL-MAJ-01 regression test at the PUBLIC query boundary:
// malformed authoritative numeric metadata (a corrupted price_increment
// patch) must never panic through ResolvePrecision, and must resolve to
// ErrUnknownReference — the existing view.ViewState != fact.ViewValid
// check in ResolvePrecision already routes there once listing.ResolveView
// correctly reports the malformed field as PENDING_CORRECTION, requiring
// no change to this package at all.
func TestResolvePrecisionMalformedMetadataFailsClosedNoPanic(t *testing.T) {
	ctx := context.Background()
	f := setup(t)
	instant := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)

	// Effective BEFORE the query instant (so it is always eligible once
	// visible) but RECORDED later — isolates the knowledge axis exactly
	// like TestResolvePrecisionLookAheadGuard above.
	patchEffectiveAt := instant.Add(-time.Hour)
	patchRecordedAt := instant.Add(time.Hour)
	if _, err := f.svc.Listings.Store.Append(ctx, buildListingMetadataDraft(f.listingScope, patchRecordedAt, patchEffectiveAt), listing.MetadataRevisedPayload{
		ListingID:     f.listingScope.ListingID,
		ChangedFields: map[string]string{"price_increment": "not-a-number"},
	}); err != nil {
		t.Fatalf("append malformed price_increment patch: %v", err)
	}

	// Knowledge cursor AFTER the malformed patch was recorded: it is now
	// visible and effective — must not panic, must fail closed.
	_, err := f.svc.ResolvePrecision(f.instrumentID, f.venueID, instant, patchRecordedAt.Add(time.Minute)) // must not panic
	if err != ErrUnknownReference {
		t.Fatalf("ResolvePrecision with malformed price_increment: got err=%v, want ErrUnknownReference", err)
	}

	// A query at a knowledge cursor BEFORE the malformed patch was recorded
	// must still resolve the original, well-formed value — the malformed
	// patch must not leak backward, exactly like any other correction
	// (ADR-032 §B.3 look-ahead guard, unaffected by this fix).
	before, err := f.svc.ResolvePrecision(f.instrumentID, f.venueID, instant, patchRecordedAt.Add(-time.Minute))
	if err != nil {
		t.Fatalf("ResolvePrecision before malformed patch was recorded: unexpected error %v", err)
	}
	if !before.PriceIncrement.Equal(decimal.MustFromString("0.01")) {
		t.Fatalf("PriceIncrement before malformed patch = %s, want unchanged 0.01", before.PriceIncrement.String())
	}
}

// TestResolveIdentityBeforeVenueEffectiveTime proves a query at an
// effective instant BEFORE the venue's own registration effective_time
// does not resolve — the registration itself is not yet effective, a
// distinct temporal question from whether it is yet VISIBLE (already
// covered by TestResolveIdentityNotYetVisibleAtKnowledgeCursor).
func TestResolveIdentityBeforeVenueEffectiveTime(t *testing.T) {
	f := setup(t)
	t0 := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC) // venue's own RecordedTime/EffectiveTime, per setup()
	beforeVenueEffective := t0.Add(-time.Hour)
	afterVenueRecorded := t0.Add(time.Hour) // knowledge cursor AFTER recording — isolates the effective-time axis specifically, distinct from TestResolveIdentityNotYetVisibleAtKnowledgeCursor's knowledge-axis test
	_, err := f.svc.ResolveIdentity(rawVenueID, "BTCUSDT", beforeVenueEffective, afterVenueRecorded)
	if err != ErrUnknownReference {
		t.Fatalf("got err=%v querying before the venue's own effective_time (but after it was recorded), want ErrUnknownReference", err)
	}
}

// TestResolveIdentityScopedToCorrectVenue proves resolveListingByVenueSymbol
// does not leak a symbol match across venues: a second venue+listing using
// the SAME venue_symbol under a DIFFERENT venue must not be returned when
// querying the first venue.
func TestResolveIdentityScopedToCorrectVenue(t *testing.T) {
	ctx := context.Background()
	f := setup(t)
	t0 := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)

	otherVenScope := venue.Scope{VenueIdentityRef: "kraken-spot", VenueType: "CENTRALIZED_EXCHANGE"}
	otherVenRef, err := f.svc.Venues.Register(ctx, "ven-reg-2", otherVenScope, "Kraken", "UTC", "cal-crypto-247", "prec-default", t0, t0)
	if err != nil {
		t.Fatalf("Register second venue: %v", err)
	}
	otherInsScope := instrument.Scope{InstrumentIdentityRef: "eth-usdt", BaseAssetRef: "ETH", QuoteAssetRef: "USDT", InstrumentType: "SPOT"}
	otherInsRef, err := f.svc.Instruments.Register(ctx, "ins-reg-2", otherInsScope, "ETH/USDT", t0, t0)
	if err != nil {
		t.Fatalf("Register second instrument: %v", err)
	}
	otherLstScope := listing.Scope{InstrumentID: otherInsScope.InstrumentID(), VenueID: otherVenScope.VenueID(), ListingID: "lst_2"}
	if _, err := f.svc.Listings.CreateListing(ctx, listing.CreateListingInput{
		Scope: otherLstScope, VenueSymbol: "BTCUSDT", // same raw symbol as fixture's listing, DIFFERENT venue
		PriceIncrement: decimal.MustFromString("0.5"), QuantityIncrement: decimal.MustFromString("0.001"),
		SessionCalendarRef: "cal-crypto-247", ActivationRequestID: listing.DeterministicActivationRequestID(otherLstScope),
		InstrumentRegistered: otherInsRef, VenueRegistered: otherVenRef,
		RecordedTime: t0, EffectiveTime: t0,
		RequestEventID: "evt-req-2", ReservedEventID: "evt-res-2", CreatedEventID: "evt-created-2",
	}); err != nil {
		t.Fatalf("CreateListing (second venue): %v", err)
	}

	instant := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)
	id, err := f.svc.ResolveIdentity(rawVenueID, "BTCUSDT", instant, instant.Add(time.Hour))
	if err != nil {
		t.Fatalf("ResolveIdentity error: %v", err)
	}
	if id.InstrumentID != f.instrumentID || id.VenueID != f.venueID {
		t.Fatalf("got %+v, want original venue's identity {%s %s} — a same-symbol listing under a DIFFERENT venue must not match", id, f.instrumentID, f.venueID)
	}

	// The reverse direction: querying the SECOND venue's own raw identity
	// must skip past the FIRST (non-matching-venue) listing — which is
	// encountered first in append order — and correctly resolve the
	// second listing instead, proving the scoping guard, not iteration
	// order, decides the match.
	id2, err := f.svc.ResolveIdentity("kraken-spot", "BTCUSDT", instant, instant.Add(time.Hour))
	if err != nil {
		t.Fatalf("ResolveIdentity (second venue) error: %v", err)
	}
	if id2.InstrumentID != otherInsScope.InstrumentID() || id2.VenueID != otherVenScope.VenueID() {
		t.Fatalf("got %+v, want second venue's identity {%s %s}", id2, otherInsScope.InstrumentID(), otherVenScope.VenueID())
	}
}

// TestResolveIdentityIgnoresListingWithPendingCorrectionView proves
// resolveListingByVenueSymbol correctly SKIPS a candidate listing whose
// Current View is not VALID (here: malformed metadata content, fail-closed
// per P3-MR-DECIMAL-MAJ-01) rather than misresolving or panicking.
func TestResolveIdentityIgnoresListingWithPendingCorrectionView(t *testing.T) {
	ctx := context.Background()
	f := setup(t)
	instant := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)

	patchEffectiveAt := instant.Add(-time.Hour)
	patchRecordedAt := instant.Add(-30 * time.Minute)
	if _, err := f.svc.Listings.Store.Append(ctx, buildListingMetadataDraft(f.listingScope, patchRecordedAt, patchEffectiveAt), listing.MetadataRevisedPayload{
		ListingID:     f.listingScope.ListingID,
		ChangedFields: map[string]string{"price_increment": "not-a-number"},
	}); err != nil {
		t.Fatalf("append malformed price_increment patch: %v", err)
	}

	_, err := f.svc.ResolveIdentity(rawVenueID, "BTCUSDT", instant, instant.Add(time.Hour)) // must not panic
	if err != ErrUnknownReference {
		t.Fatalf("got err=%v for a listing with a PENDING_CORRECTION view, want ErrUnknownReference (correctly skipped, not misresolved)", err)
	}
}

// TestResolveWindowUnknownReference proves ResolveWindow's own
// findListingScope-not-found path (distinct from ResolvePrecision's).
func TestResolveWindowUnknownReference(t *testing.T) {
	f := setup(t)
	instant := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)
	_, err := f.svc.ResolveWindow("ins_nonexistent", "ven_nonexistent", "1m", instant, instant.Add(time.Hour))
	if err != ErrUnknownReference {
		t.Fatalf("got err=%v for an unknown (instrumentID, venueID) pair, want ErrUnknownReference", err)
	}
}

// TestResolvePrecisionUnknownReference mirrors the above for
// ResolvePrecision's own findListingScope-not-found path.
func TestResolvePrecisionUnknownReference(t *testing.T) {
	f := setup(t)
	instant := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)
	_, err := f.svc.ResolvePrecision("ins_nonexistent", "ven_nonexistent", instant, instant.Add(time.Hour))
	if err != ErrUnknownReference {
		t.Fatalf("got err=%v for an unknown (instrumentID, venueID) pair, want ErrUnknownReference", err)
	}
}

// TestResolveWindowEmptySessionCalendarRef proves a listing with an
// absent/empty session_calendar_ref fails closed with ErrUnknownReference
// rather than attempting to resolve an empty calendar reference.
func TestResolveWindowEmptySessionCalendarRef(t *testing.T) {
	ctx := context.Background()
	f := setup(t)
	t0 := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)

	insScope := instrument.Scope{InstrumentIdentityRef: "sol-usdt", BaseAssetRef: "SOL", QuoteAssetRef: "USDT", InstrumentType: "SPOT"}
	insRef, err := f.svc.Instruments.Register(ctx, "ins-reg-3", insScope, "SOL/USDT", t0, t0)
	if err != nil {
		t.Fatalf("Register instrument: %v", err)
	}
	venScope := venue.Scope{VenueIdentityRef: "okx-spot", VenueType: "CENTRALIZED_EXCHANGE"}
	venRef, err := f.svc.Venues.Register(ctx, "ven-reg-3", venScope, "OKX", "UTC", "cal-crypto-247", "prec-default", t0, t0)
	if err != nil {
		t.Fatalf("Register venue: %v", err)
	}
	lstScope := listing.Scope{InstrumentID: insScope.InstrumentID(), VenueID: venScope.VenueID(), ListingID: "lst_no_calendar"}
	if _, err := f.svc.Listings.CreateListing(ctx, listing.CreateListingInput{
		Scope: lstScope, VenueSymbol: "SOLUSDT",
		PriceIncrement: decimal.MustFromString("0.01"), QuantityIncrement: decimal.MustFromString("0.1"),
		SessionCalendarRef:   "", // deliberately absent
		ActivationRequestID:  listing.DeterministicActivationRequestID(lstScope),
		InstrumentRegistered: insRef, VenueRegistered: venRef,
		RecordedTime: t0, EffectiveTime: t0,
		RequestEventID: "evt-req-3", ReservedEventID: "evt-res-3", CreatedEventID: "evt-created-3",
	}); err != nil {
		t.Fatalf("CreateListing: %v", err)
	}

	_, err = f.svc.ResolveWindow(insScope.InstrumentID(), venScope.VenueID(), "1m", t0.Add(time.Hour), t0.Add(time.Hour))
	if err != ErrUnknownReference {
		t.Fatalf("got err=%v for empty session_calendar_ref, want ErrUnknownReference", err)
	}
}

// TestResolveWindowUnregisteredCalendarBinding proves a listing whose
// session_calendar_ref points to a calendar NOT registered in the
// Resolver's bindings fails closed with ErrNoCalendarBinding.
func TestResolveWindowUnregisteredCalendarBinding(t *testing.T) {
	ctx := context.Background()
	f := setup(t)
	t0 := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)

	insScope := instrument.Scope{InstrumentIdentityRef: "ada-usdt", BaseAssetRef: "ADA", QuoteAssetRef: "USDT", InstrumentType: "SPOT"}
	insRef, err := f.svc.Instruments.Register(ctx, "ins-reg-4", insScope, "ADA/USDT", t0, t0)
	if err != nil {
		t.Fatalf("Register instrument: %v", err)
	}
	venScope := venue.Scope{VenueIdentityRef: "bybit-spot", VenueType: "CENTRALIZED_EXCHANGE"}
	venRef, err := f.svc.Venues.Register(ctx, "ven-reg-4", venScope, "Bybit", "UTC", "cal-unregistered", "prec-default", t0, t0)
	if err != nil {
		t.Fatalf("Register venue: %v", err)
	}
	lstScope := listing.Scope{InstrumentID: insScope.InstrumentID(), VenueID: venScope.VenueID(), ListingID: "lst_bad_calendar"}
	if _, err := f.svc.Listings.CreateListing(ctx, listing.CreateListingInput{
		Scope: lstScope, VenueSymbol: "ADAUSDT",
		PriceIncrement: decimal.MustFromString("0.0001"), QuantityIncrement: decimal.MustFromString("1"),
		SessionCalendarRef:   "cal-unregistered", // not in this test's Resolver bindings (only cal-crypto-247 is)
		ActivationRequestID:  listing.DeterministicActivationRequestID(lstScope),
		InstrumentRegistered: insRef, VenueRegistered: venRef,
		RecordedTime: t0, EffectiveTime: t0,
		RequestEventID: "evt-req-4", ReservedEventID: "evt-res-4", CreatedEventID: "evt-created-4",
	}); err != nil {
		t.Fatalf("CreateListing: %v", err)
	}

	_, err = f.svc.ResolveWindow(insScope.InstrumentID(), venScope.VenueID(), "1m", t0.Add(time.Hour), t0.Add(time.Hour))
	if err != ErrNoCalendarBinding {
		t.Fatalf("got err=%v for an unregistered session_calendar_ref, want ErrNoCalendarBinding", err)
	}
}

// TestResolveWindowUnsupportedTimeframe proves an unsupported timeframe
// string fails closed with ErrWindowNotResolved (calendar.Continuous's
// TimeframeDurations only defines 1m/5m/1h).
func TestResolveWindowUnsupportedTimeframe(t *testing.T) {
	f := setup(t)
	instant := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)
	_, err := f.svc.ResolveWindow(f.instrumentID, f.venueID, "1d", instant, instant.Add(time.Hour))
	if err != ErrWindowNotResolved {
		t.Fatalf("got err=%v for an unsupported timeframe, want ErrWindowNotResolved", err)
	}
}
