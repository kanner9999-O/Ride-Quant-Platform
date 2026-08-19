// Package envelope implements the Chapter 8 §8.2 event envelope (metadata)
// shared by every Candle event (candle.md §2). Chapter 8 owns envelope
// semantics; this package applies it, it does not redefine it.
//
// StreamRef, Sequence, and ProducerRef are deliberately split out of Draft
// into the publisher-assigned Envelope: Chapter 8 §8.3.2 requires sequence
// allocation to happen atomically with append, which is the
// publish.EventPublisher's responsibility, not domain/ingestion logic's.
package envelope

import "time"

// EventRecordRef is the canonical event-record reference shape (Chapter 8
// §8.2.3): a qualified locator (stream_id, sequence) plus a verification
// field (event_id).
type EventRecordRef struct {
	StreamID string
	Sequence int64
	EventID  string
}

// ContractRef pins an immutable Event Contract snapshot (Chapter 8 §8.2.5):
// {contract_id, contract_version}, kept separate from SchemaVersion because
// the two evolve independently.
type ContractRef struct {
	ContractID      string
	ContractVersion string
}

// SubjectRef is the polymorphic, qualified subject reference (Chapter 8
// §8.2.2). Scope holds only the fields the Event Contract declares as
// needed — for Candle, exactly the five-field scope (candle.md §1).
type SubjectRef struct {
	ContextID   string
	SubjectKind string
	SubjectType string
	SubjectID   string
	Scope       map[string]string
}

// EffectiveTime represents Chapter 8 §8.2.1's "instant hoặc interval" shape.
// For Candle, it is always the interval [WindowStart, WindowEnd) — see
// candle.md §8.
type EffectiveTime struct {
	WindowStart time.Time
	WindowEnd   time.Time
}

// SourceIdentity is the venue-neutral idempotency-identity schema (Chapter
// 6 §6.6, candle.md §13). Present only when the source can retry/redeliver.
type SourceIdentity struct {
	VenueID      string
	InstrumentID string
	Type         string
	Value        string
}

// StreamRef pins the stream definition snapshot applied at append
// (Chapter 8 §8.3.1): {stream_id, registry_version}. registry_version is
// NOT part of the canonical locator (stream_id, sequence).
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

// Draft is the portion of the Chapter 8 §8.2 envelope that domain/ingestion
// logic is authoritative for and constructs before append.
type Draft struct {
	EventID          string
	EventType        string
	EventContractRef ContractRef
	SchemaVersion    int
	RecordedTime     time.Time
	SubjectRef       SubjectRef
	CorrelationID    string // optional for root/independent Candle observations (candle.md §2)
	CausationRefs    []EventRecordRef
	RelatedEventRefs []EventRecordRef
	EffectiveTime    *EffectiveTime // required for Candle (candle.md §2)
	MarketTime       *time.Time     // conditional — set when venue provides it
	SourceIdentity   *SourceIdentity
}

// Envelope is the full Chapter 8 §8.2 envelope after append: Draft plus the
// fields the EventPublisher assigns atomically at append time
// (Chapter 8 §8.3.2).
type Envelope struct {
	Draft
	StreamRef   StreamRef
	Sequence    int64
	ProducerRef ProducerRef
}
