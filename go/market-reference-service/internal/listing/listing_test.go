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

// buildMetadataRevisedDraft mirrors query/service_test.go's
// buildListingMetadataDraft (kept package-local since it uses this
// package's own unexported EventType/ContractID/contractVersion).
func buildMetadataRevisedDraft(scope Scope, recordedTime, effectiveTime time.Time, eventID string) envelope.Draft {
	return envelope.Draft{
		EventID:   eventID,
		EventType: EventTypeMetadataRevised,
		EventContractRef: envelope.ContractRef{
			ContractID:      ContractIDMetadataRevised,
			ContractVersion: contractVersion,
		},
		SchemaVersion:    payloadSchemaVersion,
		RecordedTime:     recordedTime,
		SubjectRef:       subjectRef(scope),
		CausationRefs:    []envelope.EventRecordRef{},
		RelatedEventRefs: []envelope.EventRecordRef{},
		EffectiveTime:    effectiveTime,
	}
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

// setupListingForMetadataRevision creates one listing with well-formed
// initial precision fields, returning the Registry/store/scope/base-time
// so callers can append a further MetadataRevisedPayload and resolve.
func setupListingForMetadataRevision(t *testing.T) (*Registry, *store.Memory, Scope, time.Time) {
	t.Helper()
	ctx := context.Background()
	s := store.NewMemory("market-reference-service", "v0.1.0-dev", "test-run")
	reg := NewRegistry(s)
	scope := mkScope()
	t0 := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)

	if _, err := reg.CreateListing(ctx, CreateListingInput{
		Scope: scope, VenueSymbol: "BTCUSDT",
		PriceIncrement: decimal.MustFromString("0.01"), QuantityIncrement: decimal.MustFromString("0.0001"),
		SessionCalendarRef: "cal-crypto-247", ActivationRequestID: DeterministicActivationRequestID(scope),
		RecordedTime: t0, EffectiveTime: t0,
		RequestEventID: "evt-req", ReservedEventID: "evt-res", CreatedEventID: "evt-created",
	}); err != nil {
		t.Fatalf("CreateListing error: %v", err)
	}
	return reg, s, scope, t0
}

// TestResolveViewMalformedPriceIncrementFailsClosed is the
// P3-MR-DECIMAL-MAJ-01 regression test: a metadata revision that sets an
// unparseable price_increment must never panic and must never be reported
// as a resolved VALID view — it must fail closed into PENDING_CORRECTION/
// AwaitingSameSubjectReplacement (instrument.md §7/§19), the same
// representation already used for other same-subject pending states.
func TestResolveViewMalformedPriceIncrementFailsClosed(t *testing.T) {
	ctx := context.Background()
	reg, s, scope, t0 := setupListingForMetadataRevision(t)
	patchAt := t0.Add(time.Hour)

	if _, err := s.Append(ctx, buildMetadataRevisedDraft(scope, patchAt, patchAt, "evt-bad-price"), MetadataRevisedPayload{
		ListingID:     scope.ListingID,
		ChangedFields: map[string]string{"price_increment": "not-a-number"},
	}); err != nil {
		t.Fatalf("append malformed price_increment patch: %v", err)
	}

	view := reg.ResolveView(scope.ListingID, patchAt.Add(time.Minute), patchAt.Add(time.Minute)) // must not panic
	if view.ViewState != fact.ViewPendingCorrection {
		t.Fatalf("ViewState = %v, want ViewPendingCorrection for malformed price_increment", view.ViewState)
	}
	if view.PendingClass != fact.AwaitingSameSubjectReplacement {
		t.Fatalf("PendingClass = %v, want AwaitingSameSubjectReplacement", view.PendingClass)
	}
}

// TestResolveViewMalformedQuantityIncrementFailsClosed mirrors the
// price_increment case for quantity_increment (also REQUIRED, §11).
func TestResolveViewMalformedQuantityIncrementFailsClosed(t *testing.T) {
	ctx := context.Background()
	reg, s, scope, t0 := setupListingForMetadataRevision(t)
	patchAt := t0.Add(time.Hour)

	if _, err := s.Append(ctx, buildMetadataRevisedDraft(scope, patchAt, patchAt, "evt-bad-qty"), MetadataRevisedPayload{
		ListingID:     scope.ListingID,
		ChangedFields: map[string]string{"quantity_increment": "12a.3"},
	}); err != nil {
		t.Fatalf("append malformed quantity_increment patch: %v", err)
	}

	view := reg.ResolveView(scope.ListingID, patchAt.Add(time.Minute), patchAt.Add(time.Minute)) // must not panic
	if view.ViewState != fact.ViewPendingCorrection {
		t.Fatalf("ViewState = %v, want ViewPendingCorrection for malformed quantity_increment", view.ViewState)
	}
	if view.PendingClass != fact.AwaitingSameSubjectReplacement {
		t.Fatalf("PendingClass = %v, want AwaitingSameSubjectReplacement", view.PendingClass)
	}
}

// TestResolveViewMalformedMinQuantityFailsClosed covers the OPTIONAL,
// clearable min_quantity field (§11) — presence with unparseable content
// must fail closed exactly like a malformed REQUIRED field, never be
// silently dropped/ignored (distinct from legitimate absence, see
// TestResolveViewValidOptionalFieldsUnaffected below).
func TestResolveViewMalformedMinQuantityFailsClosed(t *testing.T) {
	ctx := context.Background()
	reg, s, scope, t0 := setupListingForMetadataRevision(t)
	patchAt := t0.Add(time.Hour)

	if _, err := s.Append(ctx, buildMetadataRevisedDraft(scope, patchAt, patchAt, "evt-bad-minqty"), MetadataRevisedPayload{
		ListingID:     scope.ListingID,
		ChangedFields: map[string]string{"min_quantity": "garbage"},
	}); err != nil {
		t.Fatalf("append malformed min_quantity patch: %v", err)
	}

	view := reg.ResolveView(scope.ListingID, patchAt.Add(time.Minute), patchAt.Add(time.Minute)) // must not panic
	if view.ViewState != fact.ViewPendingCorrection {
		t.Fatalf("ViewState = %v, want ViewPendingCorrection for malformed min_quantity", view.ViewState)
	}
	if view.PendingClass != fact.AwaitingSameSubjectReplacement {
		t.Fatalf("PendingClass = %v, want AwaitingSameSubjectReplacement", view.PendingClass)
	}
}

// TestResolveViewMalformedMinNotionalFailsClosed mirrors the min_quantity
// case for the other optional, clearable field, min_notional (§11).
func TestResolveViewMalformedMinNotionalFailsClosed(t *testing.T) {
	ctx := context.Background()
	reg, s, scope, t0 := setupListingForMetadataRevision(t)
	patchAt := t0.Add(time.Hour)

	if _, err := s.Append(ctx, buildMetadataRevisedDraft(scope, patchAt, patchAt, "evt-bad-minnotional"), MetadataRevisedPayload{
		ListingID:     scope.ListingID,
		ChangedFields: map[string]string{"min_notional": "$100"},
	}); err != nil {
		t.Fatalf("append malformed min_notional patch: %v", err)
	}

	view := reg.ResolveView(scope.ListingID, patchAt.Add(time.Minute), patchAt.Add(time.Minute)) // must not panic
	if view.ViewState != fact.ViewPendingCorrection {
		t.Fatalf("ViewState = %v, want ViewPendingCorrection for malformed min_notional", view.ViewState)
	}
	if view.PendingClass != fact.AwaitingSameSubjectReplacement {
		t.Fatalf("PendingClass = %v, want AwaitingSameSubjectReplacement", view.PendingClass)
	}
}

// TestResolveViewValidOptionalFieldsUnaffected proves the fix does not
// regress the legitimate path: well-formed min_quantity/min_notional
// (present, parseable) resolve normally into a VALID view, and legitimate
// absence (never set) remains nil — never confused with malformed presence.
func TestResolveViewValidOptionalFieldsUnaffected(t *testing.T) {
	ctx := context.Background()
	s := store.NewMemory("market-reference-service", "v0.1.0-dev", "test-run")
	reg := NewRegistry(s)
	scope := mkScope()
	t0 := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)
	minQty := decimal.MustFromString("0.001")
	minNotional := decimal.MustFromString("10")

	if _, err := reg.CreateListing(ctx, CreateListingInput{
		Scope: scope, VenueSymbol: "BTCUSDT",
		PriceIncrement: decimal.MustFromString("0.01"), QuantityIncrement: decimal.MustFromString("0.0001"),
		MinQuantity: &minQty, MinNotional: &minNotional,
		SessionCalendarRef: "cal-crypto-247", ActivationRequestID: DeterministicActivationRequestID(scope),
		RecordedTime: t0, EffectiveTime: t0,
		RequestEventID: "evt-req", ReservedEventID: "evt-res", CreatedEventID: "evt-created",
	}); err != nil {
		t.Fatalf("CreateListing error: %v", err)
	}

	view := reg.ResolveView(scope.ListingID, t0.Add(time.Hour), t0.Add(time.Hour))
	if view.ViewState != fact.ViewValid {
		t.Fatalf("ViewState = %v, want VALID for well-formed optional fields", view.ViewState)
	}
	if view.MinQuantity == nil || !view.MinQuantity.Equal(minQty) {
		t.Fatalf("MinQuantity = %v, want %s", view.MinQuantity, minQty.String())
	}
	if view.MinNotional == nil || !view.MinNotional.Equal(minNotional) {
		t.Fatalf("MinNotional = %v, want %s", view.MinNotional, minNotional.String())
	}
	if !view.PriceIncrement.Equal(decimal.MustFromString("0.01")) {
		t.Fatalf("PriceIncrement = %s, want 0.01 (valid metadata must be unaffected)", view.PriceIncrement.String())
	}

	// A SEPARATE listing that never sets these optional fields must resolve
	// with them nil — legitimate absence, not confused with malformed
	// presence (the case covered above).
	reg2, _, scope2, t02 := setupListingForMetadataRevision(t)
	view2 := reg2.ResolveView(scope2.ListingID, t02.Add(time.Hour), t02.Add(time.Hour))
	if view2.ViewState != fact.ViewValid {
		t.Fatalf("ViewState = %v, want VALID", view2.ViewState)
	}
	if view2.MinQuantity != nil || view2.MinNotional != nil {
		t.Fatalf("MinQuantity/MinNotional = %v/%v, want both nil (never set)", view2.MinQuantity, view2.MinNotional)
	}
}

// TestResolveViewMetadataRevisionAppliesToVenueSymbol proves the fold
// itself still applies well-formed metadata revisions correctly after the
// fix (venue_symbol is not decimal-typed, so it is not covered by the
// price/quantity/min-field validation above, but it flows through the
// same out.Fields map and must be unaffected).
func TestResolveViewMetadataRevisionAppliesToVenueSymbol(t *testing.T) {
	ctx := context.Background()
	reg, s, scope, t0 := setupListingForMetadataRevision(t)
	rebrandAt := t0.Add(time.Hour)

	if _, err := s.Append(ctx, buildMetadataRevisedDraft(scope, rebrandAt, rebrandAt, "evt-rebrand"), MetadataRevisedPayload{
		ListingID:     scope.ListingID,
		ChangedFields: map[string]string{"venue_symbol": "XBTUSDT"},
	}); err != nil {
		t.Fatalf("append rebrand: %v", err)
	}

	view := reg.ResolveView(scope.ListingID, rebrandAt.Add(time.Minute), rebrandAt.Add(time.Minute))
	if view.ViewState != fact.ViewValid {
		t.Fatalf("ViewState = %v, want VALID for a well-formed revision", view.ViewState)
	}
	if view.VenueSymbol != "XBTUSDT" {
		t.Fatalf("VenueSymbol = %q, want XBTUSDT", view.VenueSymbol)
	}
	if !view.PriceIncrement.Equal(decimal.MustFromString("0.01")) {
		t.Fatalf("PriceIncrement = %s, want unchanged 0.01", view.PriceIncrement.String())
	}
}

// TestResolveViewUnknownListingIDIsPendingCorrection proves an unknown/
// never-created listing_id fails closed (no panic, no fabricated view)
// rather than resolving to a misleading zero-valued VALID view.
func TestResolveViewUnknownListingIDIsPendingCorrection(t *testing.T) {
	reg := NewRegistry(store.NewMemory("market-reference-service", "v0.1.0-dev", "test-run"))
	t0 := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)

	view := reg.ResolveView("never-created-listing-id", t0, t0) // must not panic
	if view.ViewState != fact.ViewPendingCorrection {
		t.Fatalf("ViewState = %v, want ViewPendingCorrection for an unknown listing_id", view.ViewState)
	}
}
