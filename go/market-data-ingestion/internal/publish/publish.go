// Package publish defines market-data-ingestion's append boundary — the
// port through which domain-constructed envelope.Draft events become
// authoritative event records.
//
// A real implementation would resolve stream-registry.yaml, allocate
// `sequence` atomically with append (Chapter 8 §8.3.2: "Sequence
// allocation và append phải nằm trong cùng một atomic operation"), and
// stamp producer_ref from module-registry.yaml. Neither stream-
// registry.yaml nor that wiring exists yet in this repository — Package
// 1.3-A §13 explicitly carries this forward as a Phase 1 (implementation)
// concern, not an architecture-level decision to make here. This module
// therefore depends only on this interface; internal/publish/memory.go is
// a single-process test double, not infrastructure.
package publish

import (
	"context"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/envelope"
)

// EventPublisher appends an envelope.Draft plus its domain payload as an
// authoritative event record, assigning StreamRef, Sequence, and
// ProducerRef atomically with the append (Chapter 8 §8.3.2) — domain/
// ingestion logic never assigns these fields itself.
//
// payload is one of candle.ObservedPayload / candle.ClosedPayload /
// candle.CorrectedPayload / candle.DataGapPayload, matching draft.EventType
// — Chapter 8 owns envelope (metadata), the domain contract owns payload
// (Chapter 8 §8.2), so the two travel together but are typed separately.
type EventPublisher interface {
	// Publish appends draft+payload and returns the resulting event
	// record's canonical locator (Chapter 8 §8.2.3), for use as a later
	// correction's causation_refs target.
	Publish(ctx context.Context, draft envelope.Draft, payload any) (envelope.EventRecordRef, error)
}
