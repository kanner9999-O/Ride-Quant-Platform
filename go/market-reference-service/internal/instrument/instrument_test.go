package instrument

import (
	"context"
	"testing"
	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/envelope"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/fact"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/store"
)

func mkScope() Scope {
	return Scope{
		InstrumentIdentityRef: "binance-btc-usdt-spot",
		BaseAssetRef:          "BTC",
		QuoteAssetRef:         "USDT",
		InstrumentType:        "SPOT",
	}
}

func TestInstrumentIDDeterministic(t *testing.T) {
	if mkScope().InstrumentID() != mkScope().InstrumentID() {
		t.Fatalf("InstrumentID not deterministic")
	}
}

func TestInstrumentIDDiffersOnScopeChange(t *testing.T) {
	a := mkScope()
	b := mkScope()
	b.QuoteAssetRef = "USDC"
	if a.InstrumentID() == b.InstrumentID() {
		t.Fatalf("expected different InstrumentID for different scope")
	}
}

func TestRegisterThenResolveView(t *testing.T) {
	ctx := context.Background()
	reg := NewRegistry(store.NewMemory("market-reference-service", "v0.1.0-dev", "test-run"))
	scope := mkScope()
	instrumentID := scope.InstrumentID()

	t0 := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)
	if _, err := reg.Register(ctx, "evt-1", scope, "BTC/USDT Spot", t0, t0); err != nil {
		t.Fatalf("Register error: %v", err)
	}

	view := reg.ResolveView(instrumentID, t0.Add(time.Hour), t0.Add(time.Hour))
	if view.ViewState != fact.ViewValid {
		t.Fatalf("ViewState = %v, want VALID", view.ViewState)
	}
	if view.CurrentStatus != StatusRegistered {
		t.Fatalf("CurrentStatus = %q, want REGISTERED (notional initial status)", view.CurrentStatus)
	}
	if view.DisplayName != "BTC/USDT Spot" {
		t.Fatalf("DisplayName = %q, want BTC/USDT Spot", view.DisplayName)
	}
}

func TestChangeStatusActivatesInstrument(t *testing.T) {
	ctx := context.Background()
	reg := NewRegistry(store.NewMemory("market-reference-service", "v0.1.0-dev", "test-run"))
	scope := mkScope()
	instrumentID := scope.InstrumentID()
	t0 := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)

	if _, err := reg.Register(ctx, "evt-1", scope, "BTC/USDT Spot", t0, t0); err != nil {
		t.Fatalf("Register error: %v", err)
	}
	activateAt := t0.Add(time.Hour)
	if _, err := reg.ChangeStatus(ctx, "evt-2", instrumentID, scope, StatusActive, activateAt, activateAt); err != nil {
		t.Fatalf("ChangeStatus error: %v", err)
	}

	before := reg.ResolveView(instrumentID, t0.Add(30*time.Minute), t0.Add(2*time.Hour))
	if before.CurrentStatus != StatusRegistered {
		t.Fatalf("before activation effective_time: CurrentStatus = %q, want REGISTERED", before.CurrentStatus)
	}

	after := reg.ResolveView(instrumentID, t0.Add(2*time.Hour), t0.Add(2*time.Hour))
	if after.CurrentStatus != StatusActive {
		t.Fatalf("after activation effective_time: CurrentStatus = %q, want ACTIVE", after.CurrentStatus)
	}
}

func TestResolveViewNotYetRegistered(t *testing.T) {
	reg := NewRegistry(store.NewMemory("market-reference-service", "v0.1.0-dev", "test-run"))
	view := reg.ResolveView("ins_nonexistent", time.Now(), time.Now())
	if view.ViewState == fact.ViewValid {
		t.Fatalf("expected PENDING_CORRECTION/absent for unregistered subject, got VALID")
	}
}

// TestResolveViewAppliesMetadataRevision proves ResolveView folds a
// forward-looking InstrumentMetadataRevised patch (instrument.md §4) into
// display_name — previously untested end-to-end (gobco -branch confirmed
// the MetadataRevisedPayload type-switch case had never matched in this
// package's own test run).
func TestResolveViewAppliesMetadataRevision(t *testing.T) {
	ctx := context.Background()
	s := store.NewMemory("market-reference-service", "v0.1.0-dev", "test-run")
	reg := NewRegistry(s)
	scope := mkScope()
	instrumentID := scope.InstrumentID()
	t0 := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)

	if _, err := reg.Register(ctx, "evt-1", scope, "BTC/USDT Spot", t0, t0); err != nil {
		t.Fatalf("Register error: %v", err)
	}

	revisedAt := t0.Add(time.Hour)
	if _, err := s.Append(ctx, envelope.Draft{
		EventID:          "evt-revise",
		EventType:        EventTypeMetadataRevised,
		EventContractRef: envelope.ContractRef{ContractID: ContractIDMetadataRevised, ContractVersion: contractVersion},
		SchemaVersion:    payloadSchemaVersion,
		RecordedTime:     revisedAt,
		SubjectRef:       subjectRef(instrumentID, scope),
		CausationRefs:    []envelope.EventRecordRef{},
		RelatedEventRefs: []envelope.EventRecordRef{},
		EffectiveTime:    revisedAt,
	}, MetadataRevisedPayload{
		InstrumentID:  instrumentID,
		ChangedFields: map[string]string{"display_name": "Bitcoin / Tether Spot"},
	}); err != nil {
		t.Fatalf("append metadata revision: %v", err)
	}

	view := reg.ResolveView(instrumentID, revisedAt.Add(time.Minute), revisedAt.Add(time.Minute))
	if view.ViewState != fact.ViewValid {
		t.Fatalf("ViewState = %v, want VALID for a well-formed revision", view.ViewState)
	}
	if view.DisplayName != "Bitcoin / Tether Spot" {
		t.Fatalf("DisplayName = %q, want revised value", view.DisplayName)
	}

	// A knowledge cursor before the revision was recorded must still see
	// the original display_name — the revision must not leak backward.
	before := reg.ResolveView(instrumentID, revisedAt.Add(time.Minute), revisedAt.Add(-time.Minute))
	if before.DisplayName != "BTC/USDT Spot" {
		t.Fatalf("DisplayName before revision recorded = %q, want original BTC/USDT Spot (look-ahead leak)", before.DisplayName)
	}
}
