// Package instrument implements the Logical Instrument subject
// (instrument.md §1-§9): identity, registration/correction lineage,
// forward-looking metadata revision, and status lifecycle — built on the
// generic bitemporal fold engine in internal/fact.
package instrument

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

// Event types (instrument.md §2 event_types — PAST_TENSE_UPPER_SNAKE per
// Chapter 3 §3.2).
const (
	EventTypeRegistered      = "INSTRUMENT_REGISTERED"
	EventTypeMetadataRevised = "INSTRUMENT_METADATA_REVISED"
	EventTypeStatusChanged   = "INSTRUMENT_STATUS_CHANGED"
	EventTypeFactInvalidated = "INSTRUMENT_FACT_INVALIDATED"
)

// Contract concept IDs (instrument.md §0).
const (
	ContractIDRegistered      = "instrument-registered"
	ContractIDMetadataRevised = "instrument-metadata-revised"
	ContractIDStatusChanged   = "instrument-status-changed"
	ContractIDFactInvalidated = "instrument-fact-invalidated"
)

const contractVersion = "0.6" // pins instrument.md's document version, see market-data-ingestion's analogous note in candle/events.go
const payloadSchemaVersion = 1

// Status values (instrument.md §1 state_machine).
const (
	StatusRegistered = "REGISTERED"
	StatusActive     = "ACTIVE"
	StatusSuspended  = "SUSPENDED"
	StatusRetired    = "RETIRED"
)

// IsValidTransition implements instrument.md §1's state machine.
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

// Scope is the Logical Instrument's immutable qualifying scope
// (instrument.md §1).
type Scope struct {
	InstrumentIdentityRef string
	BaseAssetRef          string
	QuoteAssetRef         string
	InstrumentType        string // SPOT | PERPETUAL | FUTURE
	ContractExpiryRef     string // required iff FUTURE
	SettlementType        string // required iff FUTURE or PERPETUAL
}

// InstrumentID computes the opaque, stable instrument_id deterministically
// from the full scope (instrument.md §1 invariants; §23 defers the
// concrete algorithm to implementation, same pattern as candle.md §17 /
// market-data-ingestion's candle.Scope.SubjectID).
func (s Scope) InstrumentID() string {
	canonical := fmt.Sprintf("%s\x1f%s\x1f%s\x1f%s\x1f%s\x1f%s",
		s.InstrumentIdentityRef, s.BaseAssetRef, s.QuoteAssetRef, s.InstrumentType, s.ContractExpiryRef, s.SettlementType)
	sum := sha256.Sum256([]byte(canonical))
	return "ins_" + hex.EncodeToString(sum[:])
}

func toFactRef(r envelope.EventRecordRef) fact.Ref {
	return fact.Ref{StreamID: r.StreamID, Sequence: r.Sequence, EventID: r.EventID}
}

// RegisteredPayload is InstrumentRegistered's payload (instrument.md §3,
// scope + initial metadata fields only — this transaction does not model
// same-scope correction replacement, see README known-gaps).
type RegisteredPayload struct {
	InstrumentID string
	Scope        Scope
	DisplayName  string
}

// MetadataRevisedPayload is InstrumentMetadataRevised's payload
// (instrument.md §4).
type MetadataRevisedPayload struct {
	InstrumentID  string
	ChangedFields map[string]string
	ClearFields   []string
}

// StatusChangedPayload is InstrumentStatusChanged's payload
// (instrument.md §5... actually §1 state machine, event at §? — see
// instrument.md, InstrumentStatusChanged event).
type StatusChangedPayload struct {
	InstrumentID string
	NewStatus    string
}

// View is the resolved Current View (instrument.md §7) at a given
// two-axis bitemporal cursor pair.
type View struct {
	ViewState        fact.ViewState
	PendingClass     fact.PendingCorrectionClass
	Scope            Scope
	DisplayName      string
	CurrentStatus    string
	RegistrationHead envelope.EventRecordRef
}

// Registry builds and queries Instrument facts against a store.
type Registry struct {
	Store *store.Memory
}

// NewRegistry builds a Registry.
func NewRegistry(s *store.Memory) *Registry {
	return &Registry{Store: s}
}

func subjectRef(instrumentID string, scope Scope) envelope.SubjectRef {
	return envelope.SubjectRef{
		ContextID:   "instrument-venue-reference",
		SubjectKind: "entity",
		SubjectType: "Instrument",
		SubjectID:   instrumentID,
		Scope: map[string]string{
			"instrument_identity_ref": scope.InstrumentIdentityRef,
			"base_asset_ref":          scope.BaseAssetRef,
			"quote_asset_ref":         scope.QuoteAssetRef,
			"instrument_type":         scope.InstrumentType,
			"contract_expiry_ref":     scope.ContractExpiryRef,
			"settlement_type":         scope.SettlementType,
		},
	}
}

// Register appends InstrumentRegistered (instrument.md §3). effectiveTime
// is when this registration has effect as reference data.
func (r *Registry) Register(ctx context.Context, eventID string, scope Scope, displayName string, recordedTime, effectiveTime time.Time) (envelope.EventRecordRef, error) {
	instrumentID := scope.InstrumentID()
	draft := envelope.Draft{
		EventID:   eventID,
		EventType: EventTypeRegistered,
		EventContractRef: envelope.ContractRef{
			ContractID:      ContractIDRegistered,
			ContractVersion: contractVersion,
		},
		SchemaVersion:    payloadSchemaVersion,
		RecordedTime:     recordedTime,
		SubjectRef:       subjectRef(instrumentID, scope),
		CausationRefs:    []envelope.EventRecordRef{}, // root event, no supersedes_fact_ref (original registration)
		RelatedEventRefs: []envelope.EventRecordRef{},
		EffectiveTime:    effectiveTime,
	}
	payload := RegisteredPayload{InstrumentID: instrumentID, Scope: scope, DisplayName: displayName}
	return r.Store.Append(ctx, draft, payload)
}

// ChangeStatus appends InstrumentStatusChanged (instrument.md state
// machine event). Does not itself validate the transition against current
// state — callers wanting pre-append validation should call ResolveView
// first and check IsValidTransition; the fold engine (fact.FoldStatus)
// treats an invalid transition in the resulting history as a Conflict at
// query time regardless.
func (r *Registry) ChangeStatus(ctx context.Context, eventID, instrumentID string, scope Scope, newStatus string, recordedTime, effectiveTime time.Time) (envelope.EventRecordRef, error) {
	draft := envelope.Draft{
		EventID:   eventID,
		EventType: EventTypeStatusChanged,
		EventContractRef: envelope.ContractRef{
			ContractID:      ContractIDStatusChanged,
			ContractVersion: contractVersion,
		},
		SchemaVersion:    payloadSchemaVersion,
		RecordedTime:     recordedTime,
		SubjectRef:       subjectRef(instrumentID, scope),
		CausationRefs:    []envelope.EventRecordRef{},
		RelatedEventRefs: []envelope.EventRecordRef{},
		EffectiveTime:    effectiveTime,
	}
	payload := StatusChangedPayload{InstrumentID: instrumentID, NewStatus: newStatus}
	return r.Store.Append(ctx, draft, payload)
}

// ResolveView implements instrument.md §7 (Bước 1-3) for one instrument_id
// at the supplied two-axis bitemporal cursor pair (ADR-032 §B.3).
func (r *Registry) ResolveView(instrumentID string, effectiveCursor, knowledgeCursor time.Time) View {
	records := r.Store.RecordsForSubject(instrumentID)

	var regFacts []fact.LineageFact
	var regInvalidations []fact.Invalidation
	var patches []fact.MetadataPatch
	var statusChanges []fact.StatusChange
	scopeByRef := make(map[fact.Ref]Scope)
	displayNameByRef := make(map[fact.Ref]string)

	for _, rec := range records {
		ref := recordRef(rec)
		switch p := rec.Payload.(type) {
		case RegisteredPayload:
			regFacts = append(regFacts, fact.LineageFact{Ref: toFactRef(ref), RecordedTime: rec.Envelope.RecordedTime})
			scopeByRef[toFactRef(ref)] = p.Scope
			displayNameByRef[toFactRef(ref)] = p.DisplayName
		case MetadataRevisedPayload:
			patches = append(patches, fact.MetadataPatch{
				LineageFact:   fact.LineageFact{Ref: toFactRef(ref), RecordedTime: rec.Envelope.RecordedTime},
				EffectiveTime: rec.Envelope.EffectiveTime,
				ChangedFields: p.ChangedFields,
				ClearFields:   p.ClearFields,
			})
		case StatusChangedPayload:
			statusChanges = append(statusChanges, fact.StatusChange{
				LineageFact:   fact.LineageFact{Ref: toFactRef(ref), RecordedTime: rec.Envelope.RecordedTime},
				EffectiveTime: rec.Envelope.EffectiveTime,
				NewStatus:     p.NewStatus,
			})
		}
	}

	regResult := fact.ResolveLineageHead(regFacts, regInvalidations, knowledgeCursor)
	if !regResult.Valid {
		return View{ViewState: fact.ViewPendingCorrection, PendingClass: regResult.PendingClass}
	}
	scope := scopeByRef[regResult.Head]
	base := map[string]string{"display_name": displayNameByRef[regResult.Head]}

	out := fact.Resolve(fact.ResolveInput{
		RegistrationFacts: regFacts, RegistrationInvalidations: regInvalidations,
		MetadataBase: base, MetadataPatches: patches,
		StatusChanges: statusChanges, InitialStatus: StatusRegistered, IsValidTransition: IsValidTransition,
		EffectiveCursor: effectiveCursor, KnowledgeCursor: knowledgeCursor,
	})

	view := View{
		ViewState:        out.ViewState,
		PendingClass:     out.PendingClass,
		Scope:            scope,
		CurrentStatus:    out.CurrentStatus,
		RegistrationHead: envelope.EventRecordRef{StreamID: out.RegistrationHead.StreamID, Sequence: out.RegistrationHead.Sequence, EventID: out.RegistrationHead.EventID},
	}
	if out.Fields != nil {
		view.DisplayName = out.Fields["display_name"]
	}
	return view
}

func recordRef(rec store.Record) envelope.EventRecordRef {
	return envelope.EventRecordRef{StreamID: rec.Envelope.StreamRef.StreamID, Sequence: rec.Envelope.Sequence, EventID: rec.Envelope.EventID}
}
