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
