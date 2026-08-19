package venue

import (
	"context"
	"testing"
	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/fact"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/store"
)

func mkScope() Scope {
	return Scope{VenueIdentityRef: "binance-global", VenueType: "CENTRALIZED_EXCHANGE"}
}

func TestVenueIDDeterministic(t *testing.T) {
	if mkScope().VenueID() != mkScope().VenueID() {
		t.Fatalf("VenueID not deterministic")
	}
}

func TestRegisterThenResolveView(t *testing.T) {
	ctx := context.Background()
	reg := NewRegistry(store.NewMemory("market-reference-service", "v0.1.0-dev", "test-run"))
	scope := mkScope()
	venueID := scope.VenueID()
	t0 := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)

	if _, err := reg.Register(ctx, "evt-1", scope, "Binance", "UTC", "cal-crypto-247", "prec-default", t0, t0); err != nil {
		t.Fatalf("Register error: %v", err)
	}

	view := reg.ResolveView(venueID, t0.Add(time.Hour), t0.Add(time.Hour))
	if view.ViewState != fact.ViewValid {
		t.Fatalf("ViewState = %v, want VALID", view.ViewState)
	}
	if view.DefaultSessionCalendarRef != "cal-crypto-247" {
		t.Fatalf("DefaultSessionCalendarRef = %q, want cal-crypto-247", view.DefaultSessionCalendarRef)
	}
	if view.CurrentStatus != StatusRegistered {
		t.Fatalf("CurrentStatus = %q, want REGISTERED", view.CurrentStatus)
	}
}

func TestVenueRetiredBlocksListingEligibility(t *testing.T) {
	ctx := context.Background()
	reg := NewRegistry(store.NewMemory("market-reference-service", "v0.1.0-dev", "test-run"))
	scope := mkScope()
	venueID := scope.VenueID()
	t0 := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)

	if _, err := reg.Register(ctx, "evt-1", scope, "Binance", "UTC", "cal", "prec", t0, t0); err != nil {
		t.Fatalf("Register error: %v", err)
	}
	if _, err := reg.ChangeStatus(ctx, "evt-2", venueID, scope, StatusActive, t0, t0); err != nil {
		t.Fatalf("ChangeStatus ACTIVE error: %v", err)
	}
	retiredAt := t0.Add(time.Hour)
	if _, err := reg.ChangeStatus(ctx, "evt-3", venueID, scope, StatusRetired, retiredAt, retiredAt); err != nil {
		t.Fatalf("ChangeStatus RETIRED error: %v", err)
	}

	view := reg.ResolveView(venueID, retiredAt.Add(time.Minute), retiredAt.Add(time.Minute))
	if view.CurrentStatus != StatusRetired {
		t.Fatalf("CurrentStatus = %q, want RETIRED", view.CurrentStatus)
	}
}
