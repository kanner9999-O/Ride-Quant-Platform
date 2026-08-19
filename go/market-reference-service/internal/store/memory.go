// Package store implements the append-only event store market-reference-
// service's domain packages (instrument/venue/listing) build on. It is an
// in-memory test double, not a real durable event log — stream-
// registry.yaml and a real EventPublisher do not exist yet anywhere in
// this repository (see go/market-data-ingestion/README.md and Package
// 1.3-A §13's own open-gaps list, which independently confirms this).
package store

import (
	"context"
	"sync"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/envelope"
)

const fakeStreamID = "market-reference-fake"

// Record pairs a published envelope with its domain payload.
type Record struct {
	Envelope envelope.Envelope
	Payload  any
}

// Memory is a single-process, in-memory append-only event store —
// contiguous per-stream sequence (Chapter 8 §8.3.2), atomic sequence
// allocation with append, producer_ref stamping.
type Memory struct {
	mu          sync.Mutex
	nextSeq     int64
	records     []Record
	moduleID    string
	implVersion string
	runID       string
}

// NewMemory builds a Memory store. moduleID/implVersion/runID populate
// every appended event's producer_ref (Chapter 8 §8.2.4).
func NewMemory(moduleID, implVersion, runID string) *Memory {
	return &Memory{moduleID: moduleID, implVersion: implVersion, runID: runID}
}

// Append appends draft+payload atomically, assigning StreamRef, Sequence,
// and ProducerRef, and returns the resulting event record's canonical
// locator.
func (m *Memory) Append(_ context.Context, draft envelope.Draft, payload any) (envelope.EventRecordRef, error) {
	m.mu.Lock()
	defer m.mu.Unlock()

	m.nextSeq++
	seq := m.nextSeq

	env := envelope.Envelope{
		Draft: draft,
		StreamRef: envelope.StreamRef{
			StreamID:        fakeStreamID,
			RegistryVersion: "fake-v0",
		},
		Sequence: seq,
		ProducerRef: envelope.ProducerRef{
			ModuleID:              m.moduleID,
			ImplementationVersion: m.implVersion,
			RunID:                 m.runID,
		},
	}
	m.records = append(m.records, Record{Envelope: env, Payload: payload})

	return envelope.EventRecordRef{StreamID: fakeStreamID, Sequence: seq, EventID: draft.EventID}, nil
}

// RecordsForSubject returns every record whose subject_id matches, in
// append order — for domain packages to build fact.LineageFact/
// MetadataPatch/StatusChange/Invalidation slices from.
func (m *Memory) RecordsForSubject(subjectID string) []Record {
	m.mu.Lock()
	defer m.mu.Unlock()
	var out []Record
	for _, r := range m.records {
		if r.Envelope.SubjectRef.SubjectID == subjectID {
			out = append(out, r)
		}
	}
	return out
}

// AllRecords returns every event appended so far, in append order — for
// test assertions and demo wiring only.
func (m *Memory) AllRecords() []Record {
	m.mu.Lock()
	defer m.mu.Unlock()
	out := make([]Record, len(m.records))
	copy(out, m.records)
	return out
}
