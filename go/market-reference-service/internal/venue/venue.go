// Package venue implements the Logical Venue subject (venue.md §1-§9,
// "áp dụng nguyên văn theo instrument.md" for envelope/lineage/patch/status
// semantics) — built on the same generic bitemporal fold engine as
// internal/instrument.
package venue

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/envelope"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/fact"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/store"
)

// Event types (venue.md §2).
const (
	EventTypeRegistered      = "VENUE_REGISTERED"
	EventTypeMetadataRevised = "VENUE_METADATA_REVISED"
	EventTypeStatusChanged   = "VENUE_OPERATIONAL_STATUS_CHANGED"
	EventTypeFactInvalidated = "VENUE_FACT_INVALIDATED"
)

// Contract concept IDs (venue.md §0).
const (
	ContractIDRegistered      = "venue-registered"
	ContractIDMetadataRevised = "venue-metadata-revised"
	ContractIDStatusChanged   = "venue-operational-status-changed"
	ContractIDFactInvalidated = "venue-fact-invalidated"
)

const contractVersion = "0.3" // pins venue.md's document version
const payloadSchemaVersion = 1

// Status values (venue.md §1 state_machine).
const (
	StatusRegistered = "REGISTERED"
	StatusActive     = "ACTIVE"
	StatusSuspended  = "SUSPENDED"
	StatusRetired    = "RETIRED"
)

// IsValidTransition implements venue.md §1's state machine (identical
// shape to instrument.md §1).
func IsValidTransition(from, to string) bool {
	allowed := map[[2]string]bool{
		{StatusRegistered, StatusActive}:  true,
		{StatusActive, StatusSuspended}:   true,
		{StatusSuspended, StatusActive}:   true,
		{StatusActive, StatusRetired}:     true,
		{StatusSuspended, StatusRetired}:  true,
		{StatusRegistered, StatusRetired}: true,
	}
	return allowed[[2]string{from, to}]
}

// Scope is the Logical Venue's immutable qualifying scope (venue.md §1).
type Scope struct {
	VenueIdentityRef string
	VenueType        string // CENTRALIZED_EXCHANGE | DECENTRALIZED_EXCHANGE | BROKER
	JurisdictionRef  string // optional
}

// VenueID computes the opaque, stable venue_id deterministically from the
// full scope (venue.md §1 invariants; §17 defers the concrete algorithm to
// implementation).
func (s Scope) VenueID() string {
	canonical := fmt.Sprintf("%s\x1f%s\x1f%s", s.VenueIdentityRef, s.VenueType, s.JurisdictionRef)
	sum := sha256.Sum256([]byte(canonical))
	return "ven_" + hex.EncodeToString(sum[:])
}

func toFactRef(r envelope.EventRecordRef) fact.Ref {
	return fact.Ref{StreamID: r.StreamID, Sequence: r.Sequence, EventID: r.EventID}
}

// RegisteredPayload is VenueRegistered's payload (venue.md §3).
type RegisteredPayload struct {
	VenueID                   string
	Scope                     Scope
	DisplayName               string
	TimezoneRef               string
	DefaultSessionCalendarRef string
	DefaultPrecisionPolicyRef string
}

// MetadataRevisedPayload is VenueMetadataRevised's payload (venue.md §4).
type MetadataRevisedPayload struct {
	VenueID       string
	ChangedFields map[string]string
	ClearFields   []string
}

// StatusChangedPayload is VenueOperationalStatusChanged's payload
// (venue.md §5).
type StatusChangedPayload struct {
	VenueID   string
	NewStatus string
}

// View is the resolved Current View (venue.md §7) at a given two-axis
// bitemporal cursor pair.
type View struct {
	ViewState                 fact.ViewState
	PendingClass              fact.PendingCorrectionClass
	Scope                     Scope
	DisplayName               string
	TimezoneRef               string
	DefaultSessionCalendarRef string
	DefaultPrecisionPolicyRef string
	CurrentStatus             string
	RegistrationHead          envelope.EventRecordRef
}

// Registry builds and queries Venue facts against a store.
type Registry struct {
	Store *store.Memory
}

// NewRegistry builds a Registry.
func NewRegistry(s *store.Memory) *Registry {
	return &Registry{Store: s}
}

func subjectRef(venueID string, scope Scope) envelope.SubjectRef {
	return envelope.SubjectRef{
		ContextID:   "instrument-venue-reference",
		SubjectKind: "entity",
		SubjectType: "Venue",
		SubjectID:   venueID,
		Scope: map[string]string{
			"venue_identity_ref": scope.VenueIdentityRef,
			"venue_type":         scope.VenueType,
			"jurisdiction_ref":   scope.JurisdictionRef,
		},
	}
}

// Register appends VenueRegistered (venue.md §3).
func (r *Registry) Register(ctx context.Context, eventID string, scope Scope, displayName, timezoneRef, sessionCalendarRef, precisionPolicyRef string, recordedTime, effectiveTime time.Time) (envelope.EventRecordRef, error) {
	venueID := scope.VenueID()
	draft := envelope.Draft{
		EventID:   eventID,
		EventType: EventTypeRegistered,
		EventContractRef: envelope.ContractRef{
			ContractID:      ContractIDRegistered,
			ContractVersion: contractVersion,
		},
		SchemaVersion:    payloadSchemaVersion,
		RecordedTime:     recordedTime,
		SubjectRef:       subjectRef(venueID, scope),
		CausationRefs:    []envelope.EventRecordRef{},
		RelatedEventRefs: []envelope.EventRecordRef{},
		EffectiveTime:    effectiveTime,
	}
	payload := RegisteredPayload{
		VenueID: venueID, Scope: scope, DisplayName: displayName,
		TimezoneRef: timezoneRef, DefaultSessionCalendarRef: sessionCalendarRef, DefaultPrecisionPolicyRef: precisionPolicyRef,
	}
	return r.Store.Append(ctx, draft, payload)
}

// ChangeStatus appends VenueOperationalStatusChanged (venue.md §5).
func (r *Registry) ChangeStatus(ctx context.Context, eventID, venueID string, scope Scope, newStatus string, recordedTime, effectiveTime time.Time) (envelope.EventRecordRef, error) {
	draft := envelope.Draft{
		EventID:   eventID,
		EventType: EventTypeStatusChanged,
		EventContractRef: envelope.ContractRef{
			ContractID:      ContractIDStatusChanged,
			ContractVersion: contractVersion,
		},
		SchemaVersion:    payloadSchemaVersion,
		RecordedTime:     recordedTime,
		SubjectRef:       subjectRef(venueID, scope),
		CausationRefs:    []envelope.EventRecordRef{},
		RelatedEventRefs: []envelope.EventRecordRef{},
		EffectiveTime:    effectiveTime,
	}
	payload := StatusChangedPayload{VenueID: venueID, NewStatus: newStatus}
	return r.Store.Append(ctx, draft, payload)
}

// ResolveView implements venue.md §7 (Bước 1-3, applied verbatim from
// instrument.md §7) for one venue_id at the supplied two-axis bitemporal
// cursor pair (ADR-032 §B.3).
func (r *Registry) ResolveView(venueID string, effectiveCursor, knowledgeCursor time.Time) View {
	records := r.Store.RecordsForSubject(venueID)

	var regFacts []fact.LineageFact
	var patches []fact.MetadataPatch
	var statusChanges []fact.StatusChange
	scopeByRef := make(map[fact.Ref]Scope)
	baseFieldsByRef := make(map[fact.Ref]map[string]string)

	for _, rec := range records {
		ref := envelope.EventRecordRef{StreamID: rec.Envelope.StreamRef.StreamID, Sequence: rec.Envelope.Sequence, EventID: rec.Envelope.EventID}
		fref := toFactRef(ref)
		switch p := rec.Payload.(type) {
		case RegisteredPayload:
			regFacts = append(regFacts, fact.LineageFact{Ref: fref, RecordedTime: rec.Envelope.RecordedTime})
			scopeByRef[fref] = p.Scope
			baseFieldsByRef[fref] = map[string]string{
				"display_name":                 p.DisplayName,
				"timezone_ref":                 p.TimezoneRef,
				"default_session_calendar_ref": p.DefaultSessionCalendarRef,
				"default_precision_policy_ref": p.DefaultPrecisionPolicyRef,
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

	regResult := fact.ResolveLineageHead(regFacts, nil, knowledgeCursor)
	if !regResult.Valid {
		return View{ViewState: fact.ViewPendingCorrection, PendingClass: regResult.PendingClass}
	}

	out := fact.Resolve(fact.ResolveInput{
		RegistrationFacts: regFacts,
		MetadataBase:      baseFieldsByRef[regResult.Head],
		MetadataPatches:   patches,
		StatusChanges:     statusChanges, InitialStatus: StatusRegistered, IsValidTransition: IsValidTransition,
		EffectiveCursor: effectiveCursor, KnowledgeCursor: knowledgeCursor,
	})

	view := View{
		ViewState:        out.ViewState,
		PendingClass:     out.PendingClass,
		Scope:            scopeByRef[regResult.Head],
		CurrentStatus:    out.CurrentStatus,
		RegistrationHead: envelope.EventRecordRef{StreamID: out.RegistrationHead.StreamID, Sequence: out.RegistrationHead.Sequence, EventID: out.RegistrationHead.EventID},
	}
	if out.Fields != nil {
		view.DisplayName = out.Fields["display_name"]
		view.TimezoneRef = out.Fields["timezone_ref"]
		view.DefaultSessionCalendarRef = out.Fields["default_session_calendar_ref"]
		view.DefaultPrecisionPolicyRef = out.Fields["default_precision_policy_ref"]
	}
	return view
}
