// Package envelope implements the Chapter 8 §8.2 event envelope (metadata)
// shared by every Instrument/Venue/TradableListing event
// (instrument.md §2, applied verbatim by venue.md §2). Chapter 8 owns
// envelope semantics; this package applies it, it does not redefine it.
//
// StreamRef, Sequence, and ProducerRef are split out of Draft into the
// publisher-assigned Envelope for the same reason as market-data-
// ingestion's envelope package: Chapter 8 §8.3.2 requires sequence
// allocation atomic with append, which is the store's responsibility, not
// domain logic's.
package envelope

import "time"

// EventRecordRef is the canonical event-record reference shape (Chapter 8
// §8.2.3).
type EventRecordRef struct {
	StreamID string
	Sequence int64
	EventID  string
}

// IsZero reports whether ref is the zero value (no reference).
func (r EventRecordRef) IsZero() bool {
	return r == EventRecordRef{}
}

// SubjectRef is the polymorphic, qualified subject reference (Chapter 8
// §8.2.2).
type SubjectRef struct {
	ContextID   string
	SubjectKind string
	SubjectType string
	SubjectID   string
	Scope       map[string]string
}

// StreamRef pins the stream definition snapshot applied at append
// (Chapter 8 §8.3.1).
type StreamRef struct {
	StreamID        string
	RegistryVersion string
}

// ProducerRef traces the authoritative implementation that produced the
// event (Chapter 8 §8.2.4).
type ProducerRef struct {
	ModuleID              string
	ImplementationVersion string
	RunID                 string
}

// Draft is the domain-owned portion of the Chapter 8 §8.2 envelope.
// instrument.md §2/§20: effective_time is a point in time (when the fact
// has effect as reference data — forward-looking for revisions, historical
// for corrections), not an interval; market_time is PROHIBITED for this
// domain (instrument.md §2, §20).
type Draft struct {
	EventID          string
	EventType        string
	EventContractRef ContractRef
	SchemaVersion    int
	RecordedTime     time.Time
	SubjectRef       SubjectRef
	CorrelationID    string
	CausationRefs    []EventRecordRef
	RelatedEventRefs []EventRecordRef
	EffectiveTime    time.Time
	SourceIdentity   *SourceIdentity
}

// ContractRef pins an immutable Event Contract snapshot (Chapter 8 §8.2.5).
type ContractRef struct {
	ContractID      string
	ContractVersion string
}

// SourceIdentity is the venue-neutral idempotency-identity schema (Chapter
// 6 §6.6) — present only when the source can retry/redeliver. Reference
// data registration in this module is operator/Product-Owner-driven
// (instrument.md §23: registration mechanism deferred, either manual or
// automated), so most events in this module carry no SourceIdentity.
type SourceIdentity struct {
	Type  string
	Value string
}

// Envelope is the full Chapter 8 §8.2 envelope after append: Draft plus
// the fields the store assigns atomically at append time.
type Envelope struct {
	Draft
	StreamRef   StreamRef
	Sequence    int64
	ProducerRef ProducerRef
}
