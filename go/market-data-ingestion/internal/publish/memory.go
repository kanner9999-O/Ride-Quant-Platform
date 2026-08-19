package publish

import (
	"context"
	"sync"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/envelope"
)

// fakeStreamID is a placeholder single-stream topology for the in-memory
// test double. Real stream topology (how many streams, keyed by what —
// per venue, per instrument, per event family) is a stream-registry.yaml
// decision (Chapter 8 §8.3.1) that does not exist yet; this constant makes
// no claim about what the real topology should be.
const fakeStreamID = "candle-events-fake"

// Memory is a single-process, in-memory EventPublisher test double. It
// preserves the invariants this module's domain logic depends on —
// per-stream contiguous sequence (Chapter 8 §8.3.2) and atomic
// sequence-allocation-with-append — but is not a stream-registry/broker
// implementation (see package doc).
// Record pairs a published envelope with its domain payload — for test
// assertions only.
type Record struct {
	Envelope envelope.Envelope
	Payload  any
}

type Memory struct {
	mu          sync.Mutex
	nextSeq     int64
	records     []Record
	moduleID    string
	implVersion string
	runID       string
}

// NewMemory builds a Memory publisher. moduleID/implVersion/runID populate
// every appended event's producer_ref (Chapter 8 §8.2.4).
func NewMemory(moduleID, implVersion, runID string) *Memory {
	return &Memory{moduleID: moduleID, implVersion: implVersion, runID: runID}
}

// Publish implements EventPublisher.
func (m *Memory) Publish(_ context.Context, draft envelope.Draft, payload any) (envelope.EventRecordRef, error) {
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

// Records returns every event appended so far, in append order — for test
// assertions only.
func (m *Memory) Records() []Record {
	m.mu.Lock()
	defer m.mu.Unlock()
	out := make([]Record, len(m.records))
	copy(out, m.records)
	return out
}
