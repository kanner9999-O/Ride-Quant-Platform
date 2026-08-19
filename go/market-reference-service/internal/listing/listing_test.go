package listing

import (
	"context"
	"testing"
	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/decimal"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/envelope"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/fact"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/store"
)

func mkScope() Scope {
	return Scope{InstrumentID: "ins_x", VenueID: "ven_x", ListingID: "lst_1"}
}

func TestCreateListingThenResolveView(t *testing.T) {
	ctx := context.Background()
	reg := NewRegistry(store.NewMemory("market-reference-service", "v0.1.0-dev", "test-run"))
	scope := mkScope()
	t0 := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)

	_, err := reg.CreateListing(ctx, CreateListingInput{
		Scope:                scope,
		VenueSymbol:          "BTCUSDT",
		PriceIncrement:       decimal.MustFromString("0.01"),
		QuantityIncrement:    decimal.MustFromString("0.0001"),
		SessionCalendarRef:   "cal-crypto-247",
		ActivationRequestID:  DeterministicActivationRequestID(scope),
		InstrumentRegistered: envelope.EventRecordRef{StreamID: "s", Sequence: 1, EventID: "ins-reg"},
		VenueRegistered:      envelope.EventRecordRef{StreamID: "s", Sequence: 1, EventID: "ven-reg"},
		RecordedTime:         t0,
		EffectiveTime:        t0,
		RequestEventID:       "evt-req",
		ReservedEventID:      "evt-res",
		CreatedEventID:       "evt-created",
	})
	if err != nil {
		t.Fatalf("CreateListing error: %v", err)
	}

	view := reg.ResolveView(scope.ListingID, t0.Add(time.Hour), t0.Add(time.Hour))
	if view.ViewState != fact.ViewValid {
		t.Fatalf("ViewState = %v, want VALID", view.ViewState)
	}
	if view.CurrentStatus != StatusActive {
		t.Fatalf("CurrentStatus = %q, want ACTIVE", view.CurrentStatus)
	}
	if view.VenueSymbol != "BTCUSDT" {
		t.Fatalf("VenueSymbol = %q, want BTCUSDT", view.VenueSymbol)
	}
	if !view.PriceIncrement.Equal(decimal.MustFromString("0.01")) {
		t.Fatalf("PriceIncrement = %s, want 0.01", view.PriceIncrement.String())
	}
	if view.SessionCalendarRef != "cal-crypto-247" {
		t.Fatalf("SessionCalendarRef = %q, want cal-crypto-247", view.SessionCalendarRef)
	}
}

func TestCreateListingCausationLinksReservationAndParents(t *testing.T) {
	ctx := context.Background()
	s := store.NewMemory("market-reference-service", "v0.1.0-dev", "test-run")
	reg := NewRegistry(s)
	scope := mkScope()
	t0 := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)
	insRef := envelope.EventRecordRef{StreamID: "s", Sequence: 1, EventID: "ins-reg"}
	venRef := envelope.EventRecordRef{StreamID: "s", Sequence: 1, EventID: "ven-reg"}

	createdRef, err := reg.CreateListing(ctx, CreateListingInput{
		Scope: scope, VenueSymbol: "BTCUSDT", PriceIncrement: decimal.MustFromString("0.01"), QuantityIncrement: decimal.MustFromString("0.0001"),
		SessionCalendarRef: "cal", ActivationRequestID: DeterministicActivationRequestID(scope),
		InstrumentRegistered: insRef, VenueRegistered: venRef,
		RecordedTime: t0, EffectiveTime: t0,
		RequestEventID: "evt-req", ReservedEventID: "evt-res", CreatedEventID: "evt-created",
	})
	if err != nil {
		t.Fatalf("CreateListing error: %v", err)
	}

	var createdEnv envelope.Envelope
	for _, rec := range s.AllRecords() {
		if rec.Envelope.EventID == createdRef.EventID {
			createdEnv = rec.Envelope
		}
	}
	found := map[string]bool{}
	for _, c := range createdEnv.CausationRefs {
		found[c.EventID] = true
	}
	if !found["ins-reg"] || !found["ven-reg"] || !found["evt-res"] {
		t.Fatalf("CausationRefs = %v, want to include ins-reg, ven-reg, evt-res (instrument.md §11 invariants)", createdEnv.CausationRefs)
	}

	// The ActiveListingReserved event must be causal to the REQUEST, never
	// to the activation event (instrument.md §16 v0.4, avoids the causal
	// cycle IRB-C1-V03-MAJ-01 closed).
	var reservedEnv envelope.Envelope
	for _, rec := range s.AllRecords() {
		if rec.Envelope.EventID == "evt-res" {
			reservedEnv = rec.Envelope
		}
	}
	if len(reservedEnv.CausationRefs) != 1 || reservedEnv.CausationRefs[0].EventID != "evt-req" {
		t.Fatalf("ActiveListingReserved CausationRefs = %v, want [evt-req]", reservedEnv.CausationRefs)
	}
}

func TestChangeStatusSuspendThenDelist(t *testing.T) {
	ctx := context.Background()
	reg := NewRegistry(store.NewMemory("market-reference-service", "v0.1.0-dev", "test-run"))
	scope := mkScope()
	t0 := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)

	if _, err := reg.CreateListing(ctx, CreateListingInput{
		Scope: scope, VenueSymbol: "BTCUSDT", PriceIncrement: decimal.MustFromString("0.01"), QuantityIncrement: decimal.MustFromString("0.0001"),
		SessionCalendarRef: "cal", ActivationRequestID: DeterministicActivationRequestID(scope),
		RecordedTime: t0, EffectiveTime: t0, RequestEventID: "evt-req", ReservedEventID: "evt-res", CreatedEventID: "evt-created",
	}); err != nil {
		t.Fatalf("CreateListing error: %v", err)
	}

	suspendAt := t0.Add(time.Hour)
	if _, err := reg.ChangeStatus(ctx, "evt-suspend", scope, StatusSuspended, suspendAt, suspendAt); err != nil {
		t.Fatalf("ChangeStatus SUSPENDED error: %v", err)
	}
	view := reg.ResolveView(scope.ListingID, suspendAt.Add(time.Minute), suspendAt.Add(time.Minute))
	if view.CurrentStatus != StatusSuspended {
		t.Fatalf("CurrentStatus = %q, want SUSPENDED", view.CurrentStatus)
	}

	delistAt := suspendAt.Add(time.Hour)
	if _, err := reg.ChangeStatus(ctx, "evt-delist", scope, StatusDelisted, delistAt, delistAt); err != nil {
		t.Fatalf("ChangeStatus DELISTED error: %v", err)
	}
	view2 := reg.ResolveView(scope.ListingID, delistAt.Add(time.Minute), delistAt.Add(time.Minute))
	if view2.CurrentStatus != StatusDelisted {
		t.Fatalf("CurrentStatus = %q, want DELISTED", view2.CurrentStatus)
	}
}
