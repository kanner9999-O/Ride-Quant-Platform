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

func buildMetadataDraft(scope listing.Scope, recordedTime, effectiveTime time.Time) envelope.Draft {
	return envelope.Draft{
		EventID:   "evt-correction",
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
	venScope := venue.Scope{VenueIdentityRef: "binance-global", VenueType: "CENTRALIZED_EXCHANGE"}
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

	svc.RegisterSymbolBinding("binance-spot", "BTCUSDT", lstScope)

	return fixture{svc: svc, instrumentID: insScope.InstrumentID(), venueID: venScope.VenueID(), listingScope: lstScope}
}

func TestResolveIdentityKnown(t *testing.T) {
	f := setup(t)
	id, err := f.svc.ResolveIdentity("binance-spot", "BTCUSDT")
	if err != nil {
		t.Fatalf("ResolveIdentity error: %v", err)
	}
	if id.InstrumentID != f.instrumentID || id.VenueID != f.venueID {
		t.Fatalf("got %+v, want {%s %s}", id, f.instrumentID, f.venueID)
	}
}

func TestResolveIdentityUnknown(t *testing.T) {
	f := setup(t)
	_, err := f.svc.ResolveIdentity("unknown-venue", "XXXX")
	if err != ErrUnknownReference {
		t.Fatalf("got %v, want ErrUnknownReference", err)
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
	if _, err := f.svc.Listings.Store.Append(ctx, buildMetadataDraft(f.listingScope, correctionRecordedAt, instant.Add(-time.Hour)), listing.MetadataRevisedPayload{
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
