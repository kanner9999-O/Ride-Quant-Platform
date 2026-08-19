// Package listing implements the TradableListing subordinate concept
// (instrument.md §10-§15 Bước 1-3): a Logical Instrument's venue-specific
// trading metadata (venue symbol, tick/lot increments, session reference,
// listing status).
//
// Scope descope (documented, not silent): instrument.md §16 additionally
// defines a full pair-scoped ActiveListingReservation arbitration protocol
// (ActiveListingActivationRequested/Reserved/Rejected/Released/
// FactInvalidated, idempotency, terminal request disposition) governing
// which listing wins contended activation across concurrent registration
// attempts. TradableListingCreated's own invariants (§11) make a minimal
// slice of that protocol structurally mandatory — a valid
// TradableListingCreated cannot exist without a matching
// ActiveListingReserved (reservation_grant_ref, activation_request_id).
// This package therefore implements exactly that mandatory happy path
// (CreateListing atomically appends ActiveListingActivationRequested +
// ActiveListingReserved + TradableListingCreated with correct causal
// linkage) and nothing else from §16: no rejection path, no release, no
// reservation correction lineage, no contested-request arbitration. This
// is a legitimate implementation-scope boundary, not an invented or
// altered domain semantic — every event this package emits matches
// instrument.md's schema exactly; the omitted paths are simply not
// exercised because nothing in this transaction's scope (a single,
// uncontested listing per pair) requires them. See README for the full
// note.
package listing

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/decimal"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/envelope"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/fact"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/store"
)

// Event types (instrument.md §2/§11/§16).
const (
	EventTypeActivationRequested = "ACTIVE_LISTING_ACTIVATION_REQUESTED"
	EventTypeReserved            = "ACTIVE_LISTING_RESERVED"
	EventTypeCreated             = "TRADABLE_LISTING_CREATED"
	EventTypeMetadataRevised     = "TRADABLE_LISTING_METADATA_REVISED"
	EventTypeStatusChanged       = "TRADABLE_LISTING_STATUS_CHANGED"
)

// Contract concept IDs (instrument.md §0).
const (
	ContractIDActivationRequested = "active-listing-activation-requested"
	ContractIDReserved            = "active-listing-reserved"
	ContractIDCreated             = "tradable-listing-created"
	ContractIDMetadataRevised     = "tradable-listing-metadata-revised"
	ContractIDStatusChanged       = "tradable-listing-status-changed"
)

const contractVersion = "0.6"
const payloadSchemaVersion = 1

// Status values (instrument.md §10 state_machine).
const (
	StatusActive    = "ACTIVE"
	StatusSuspended = "SUSPENDED"
	StatusDelisted  = "DELISTED"
)

// notionalInitialStatus feeds fact.FoldStatus's initialStatus — Listing has
// no UNSEEN/pre-ACTIVE status field of its own (TradableListingCreated
// itself sets ACTIVE, instrument.md §10 state_machine: UNSEEN -> ACTIVE
// caused_by TradableListingCreated), so folding starts from ACTIVE once
// the creation lineage head resolves; ResolveView never calls FoldStatus
// unless a creation head exists.
const notionalInitialStatus = StatusActive

// IsValidTransition implements instrument.md §10's state machine.
func IsValidTransition(from, to string) bool {
	allowed := map[[2]string]bool{
		{StatusActive, StatusSuspended}:   true,
		{StatusSuspended, StatusActive}:   true,
		{StatusActive, StatusDelisted}:    true,
		{StatusSuspended, StatusDelisted}: true,
	}
	return allowed[[2]string{from, to}]
}

// Scope is the TradableListing's immutable qualifying scope (instrument.md
// §10). ListingID is opaque and client-assigned (not derived) — a relist
// after delisting is a wholly new subject (§10 invariant).
type Scope struct {
	InstrumentID string
	VenueID      string
	ListingID    string
}

func toFactRef(r envelope.EventRecordRef) fact.Ref {
	return fact.Ref{StreamID: r.StreamID, Sequence: r.Sequence, EventID: r.EventID}
}

// CreatedPayload is TradableListingCreated's payload (instrument.md §11).
type CreatedPayload struct {
	Scope               Scope
	VenueSymbol         string
	PriceIncrement      decimal.Decimal
	QuantityIncrement   decimal.Decimal
	MinQuantity         *decimal.Decimal
	MinNotional         *decimal.Decimal
	SessionCalendarRef  string
	ActivationRequestID string
	ReservationGrantRef envelope.EventRecordRef
}

// MetadataRevisedPayload is TradableListingMetadataRevised's payload
// (instrument.md §12).
type MetadataRevisedPayload struct {
	ListingID     string
	ChangedFields map[string]string
	ClearFields   []string
}

// StatusChangedPayload is TradableListingStatusChanged's payload
// (instrument.md §13).
type StatusChangedPayload struct {
	ListingID string
	NewStatus string
}

// activationRequestedPayload is ActiveListingActivationRequested's payload
// (instrument.md §16) — unexported: not independently queryable in this
// package's scope (see package doc), only constructed internally by
// CreateListing.
type activationRequestedPayload struct {
	ActivationRequestID   string
	InstrumentID          string
	VenueID               string
	ListingID             string
	RequestedTargetStatus string
}

// reservedPayload is ActiveListingReserved's payload (instrument.md §16).
type reservedPayload struct {
	ActivationRequestID string
	InstrumentID        string
	VenueID             string
	ListingID           string
}

// View is the resolved Current View (instrument.md §15 Bước 1-3 only —
// Bước 4-7 cross-subject eligibility/reservation fold are handled by
// query.Service, not this package, since they need Instrument/Venue
// registries).
type View struct {
	ViewState          fact.ViewState
	PendingClass       fact.PendingCorrectionClass
	Scope              Scope
	VenueSymbol        string
	PriceIncrement     decimal.Decimal
	QuantityIncrement  decimal.Decimal
	MinQuantity        *decimal.Decimal
	MinNotional        *decimal.Decimal
	SessionCalendarRef string
	CurrentStatus      string
}

// Registry builds and queries TradableListing facts against a store.
type Registry struct {
	Store *store.Memory
}

// NewRegistry builds a Registry.
func NewRegistry(s *store.Memory) *Registry {
	return &Registry{Store: s}
}

func subjectRef(scope Scope) envelope.SubjectRef {
	return envelope.SubjectRef{
		ContextID:   "instrument-venue-reference",
		SubjectKind: "entity",
		SubjectType: "TradableListing",
		SubjectID:   scope.ListingID,
		Scope: map[string]string{
			"instrument_id": scope.InstrumentID,
			"venue_id":      scope.VenueID,
		},
	}
}

// CreateListingInput bundles CreateListing's parameters.
type CreateListingInput struct {
	Scope                                           Scope
	VenueSymbol                                     string
	PriceIncrement                                  decimal.Decimal
	QuantityIncrement                               decimal.Decimal
	MinQuantity                                     *decimal.Decimal
	MinNotional                                     *decimal.Decimal
	SessionCalendarRef                              string
	ActivationRequestID                             string                  // logical request identity (instrument.md §16 Part B) — caller-assigned, must be globally unique per real request
	InstrumentRegistered                            envelope.EventRecordRef // proves the Instrument subject exists (instrument.md §11 invariant)
	VenueRegistered                                 envelope.EventRecordRef // proves the Venue subject exists
	RecordedTime                                    time.Time
	EffectiveTime                                   time.Time
	RequestEventID, ReservedEventID, CreatedEventID string
}

// CreateListing atomically appends the minimal ActiveListingActivation
// happy path (Requested -> Reserved) plus TradableListingCreated, with
// correct causal linkage and matching activation_request_id — the
// structurally mandatory subset of instrument.md §16 (see package doc).
func (r *Registry) CreateListing(ctx context.Context, in CreateListingInput) (envelope.EventRecordRef, error) {
	reqSubject := subjectRef(in.Scope)

	requestDraft := envelope.Draft{
		EventID:   in.RequestEventID,
		EventType: EventTypeActivationRequested,
		EventContractRef: envelope.ContractRef{
			ContractID:      ContractIDActivationRequested,
			ContractVersion: contractVersion,
		},
		SchemaVersion:    payloadSchemaVersion,
		RecordedTime:     in.RecordedTime,
		SubjectRef:       reqSubject,
		CausationRefs:    []envelope.EventRecordRef{},
		RelatedEventRefs: []envelope.EventRecordRef{},
		EffectiveTime:    in.EffectiveTime,
	}
	requestRef, err := r.Store.Append(ctx, requestDraft, activationRequestedPayload{
		ActivationRequestID: in.ActivationRequestID, InstrumentID: in.Scope.InstrumentID, VenueID: in.Scope.VenueID,
		ListingID: in.Scope.ListingID, RequestedTargetStatus: StatusActive,
	})
	if err != nil {
		return envelope.EventRecordRef{}, err
	}

	reservedDraft := envelope.Draft{
		EventID:   in.ReservedEventID,
		EventType: EventTypeReserved,
		EventContractRef: envelope.ContractRef{
			ContractID:      ContractIDReserved,
			ContractVersion: contractVersion,
		},
		SchemaVersion:    payloadSchemaVersion,
		RecordedTime:     in.RecordedTime,
		SubjectRef:       reqSubject,
		CausationRefs:    []envelope.EventRecordRef{requestRef}, // causal to the REQUEST, not the activation event (instrument.md §16 v0.4, avoids the causal cycle IRB-C1-V03-MAJ-01 closed)
		RelatedEventRefs: []envelope.EventRecordRef{},
		EffectiveTime:    in.EffectiveTime,
	}
	reservedRef, err := r.Store.Append(ctx, reservedDraft, reservedPayload{
		ActivationRequestID: in.ActivationRequestID, InstrumentID: in.Scope.InstrumentID, VenueID: in.Scope.VenueID, ListingID: in.Scope.ListingID,
	})
	if err != nil {
		return envelope.EventRecordRef{}, err
	}

	createdDraft := envelope.Draft{
		EventID:   in.CreatedEventID,
		EventType: EventTypeCreated,
		EventContractRef: envelope.ContractRef{
			ContractID:      ContractIDCreated,
			ContractVersion: contractVersion,
		},
		SchemaVersion: payloadSchemaVersion,
		RecordedTime:  in.RecordedTime,
		SubjectRef:    reqSubject,
		CausationRefs: []envelope.EventRecordRef{
			in.InstrumentRegistered, in.VenueRegistered, reservedRef,
		},
		RelatedEventRefs: []envelope.EventRecordRef{},
		EffectiveTime:    in.EffectiveTime,
	}
	payload := CreatedPayload{
		Scope: in.Scope, VenueSymbol: in.VenueSymbol, PriceIncrement: in.PriceIncrement, QuantityIncrement: in.QuantityIncrement,
		MinQuantity: in.MinQuantity, MinNotional: in.MinNotional, SessionCalendarRef: in.SessionCalendarRef,
		ActivationRequestID: in.ActivationRequestID, ReservationGrantRef: reservedRef,
	}
	return r.Store.Append(ctx, createdDraft, payload)
}

// ChangeStatus appends TradableListingStatusChanged for a SUSPENDED/
// DELISTED transition (instrument.md §13). Reactivating from SUSPENDED
// back to ACTIVE is out of this package's scope (would require a fresh
// reservation grant, §13 invariants) — not exercised by this transaction.
func (r *Registry) ChangeStatus(ctx context.Context, eventID string, scope Scope, newStatus string, recordedTime, effectiveTime time.Time) (envelope.EventRecordRef, error) {
	draft := envelope.Draft{
		EventID:   eventID,
		EventType: EventTypeStatusChanged,
		EventContractRef: envelope.ContractRef{
			ContractID:      ContractIDStatusChanged,
			ContractVersion: contractVersion,
		},
		SchemaVersion:    payloadSchemaVersion,
		RecordedTime:     recordedTime,
		SubjectRef:       subjectRef(scope),
		CausationRefs:    []envelope.EventRecordRef{},
		RelatedEventRefs: []envelope.EventRecordRef{},
		EffectiveTime:    effectiveTime,
	}
	return r.Store.Append(ctx, draft, StatusChangedPayload{ListingID: scope.ListingID, NewStatus: newStatus})
}

func decimalFieldString(d decimal.Decimal) string { return d.String() }

// ResolveView implements instrument.md §15 Bước 1-3 (creation lineage
// head, metadata patch fold, status fold) for one listing_id at the
// supplied two-axis bitemporal cursor pair. Bước 4-7 (cross-subject
// Instrument/Venue eligibility, reservation fold, derived
// eligibility_state) are the caller's responsibility (query.Service) —
// this package only resolves the listing's own three-step fold.
func (r *Registry) ResolveView(listingID string, effectiveCursor, knowledgeCursor time.Time) View {
	records := r.Store.RecordsForSubject(listingID)

	var creationFacts []fact.LineageFact
	var patches []fact.MetadataPatch
	var statusChanges []fact.StatusChange
	scopeByRef := make(map[fact.Ref]Scope)
	baseFieldsByRef := make(map[fact.Ref]map[string]string)
	createdByRef := make(map[fact.Ref]CreatedPayload)

	for _, rec := range records {
		ref := envelope.EventRecordRef{StreamID: rec.Envelope.StreamRef.StreamID, Sequence: rec.Envelope.Sequence, EventID: rec.Envelope.EventID}
		fref := toFactRef(ref)
		switch p := rec.Payload.(type) {
		case CreatedPayload:
			creationFacts = append(creationFacts, fact.LineageFact{Ref: fref, RecordedTime: rec.Envelope.RecordedTime})
			scopeByRef[fref] = p.Scope
			createdByRef[fref] = p
			baseFieldsByRef[fref] = map[string]string{
				"venue_symbol":         p.VenueSymbol,
				"price_increment":      decimalFieldString(p.PriceIncrement),
				"quantity_increment":   decimalFieldString(p.QuantityIncrement),
				"session_calendar_ref": p.SessionCalendarRef,
			}
			if p.MinQuantity != nil {
				baseFieldsByRef[fref]["min_quantity"] = decimalFieldString(*p.MinQuantity)
			}
			if p.MinNotional != nil {
				baseFieldsByRef[fref]["min_notional"] = decimalFieldString(*p.MinNotional)
			}
		case MetadataRevisedPayload:
			patches = append(patches, fact.MetadataPatch{
				LineageFact:   fact.LineageFact{Ref: fref, RecordedTime: rec.Envelope.RecordedTime},
				EffectiveTime: rec.Envelope.EffectiveTime,
				ChangedFields: p.ChangedFields,
				ClearFields:   p.ClearFields,
			})
		case StatusChangedPayload:
			statusChanges = append(statusChanges, fact.StatusChange{
				LineageFact:   fact.LineageFact{Ref: fref, RecordedTime: rec.Envelope.RecordedTime},
				EffectiveTime: rec.Envelope.EffectiveTime,
				NewStatus:     p.NewStatus,
			})
		}
	}

	regResult := fact.ResolveLineageHead(creationFacts, nil, knowledgeCursor)
	if !regResult.Valid {
		return View{ViewState: fact.ViewPendingCorrection, PendingClass: regResult.PendingClass}
	}

	out := fact.Resolve(fact.ResolveInput{
		RegistrationFacts: creationFacts,
		MetadataBase:      baseFieldsByRef[regResult.Head],
		MetadataPatches:   patches,
		StatusChanges:     statusChanges, InitialStatus: notionalInitialStatus, IsValidTransition: IsValidTransition,
		EffectiveCursor: effectiveCursor, KnowledgeCursor: knowledgeCursor,
	})

	view := View{
		ViewState:     out.ViewState,
		PendingClass:  out.PendingClass,
		Scope:         scopeByRef[regResult.Head],
		CurrentStatus: out.CurrentStatus,
	}
	if out.Fields != nil {
		view.VenueSymbol = out.Fields["venue_symbol"]
		view.SessionCalendarRef = out.Fields["session_calendar_ref"]
		if v, err := decimal.NewFromString(out.Fields["price_increment"]); err == nil {
			view.PriceIncrement = v
		}
		if v, err := decimal.NewFromString(out.Fields["quantity_increment"]); err == nil {
			view.QuantityIncrement = v
		}
		if s, ok := out.Fields["min_quantity"]; ok {
			if v, err := decimal.NewFromString(s); err == nil {
				view.MinQuantity = &v
			}
		}
		if s, ok := out.Fields["min_notional"]; ok {
			if v, err := decimal.NewFromString(s); err == nil {
				view.MinNotional = &v
			}
		}
	}
	return view
}

// DeterministicActivationRequestID derives a stable activation_request_id
// from the listing scope for tests/demo wiring where a real upstream
// request-generation workflow does not exist yet (instrument.md §23 defers
// the registration mechanism to Phase 1 either way — this is not a domain
// decision, just a convenience for constructing one).
func DeterministicActivationRequestID(scope Scope) string {
	sum := sha256.Sum256([]byte(fmt.Sprintf("%s\x1f%s\x1f%s", scope.InstrumentID, scope.VenueID, scope.ListingID)))
	return "req_" + hex.EncodeToString(sum[:8])
}
