package publish

import (
	"context"
	"testing"
	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/envelope"
)

func draft(eventID string) envelope.Draft {
	return envelope.Draft{
		EventID:       eventID,
		EventType:     "CANDLE_CLOSED",
		CausationRefs: []envelope.EventRecordRef{},
		RecordedTime:  time.Now().UTC(),
	}
}

func TestPublishAssignsContiguousSequence(t *testing.T) {
	m := NewMemory("market-data-ingestion", "v0.1.0-dev", "run-1")
	ctx := context.Background()

	ref1, err := m.Publish(ctx, draft("evt-1"), nil)
	if err != nil {
		t.Fatalf("Publish error: %v", err)
	}
	ref2, err := m.Publish(ctx, draft("evt-2"), nil)
	if err != nil {
		t.Fatalf("Publish error: %v", err)
	}

	if ref1.Sequence != 1 || ref2.Sequence != 2 {
		t.Fatalf("sequences = %d, %d, want 1, 2 (contiguous, Chapter 8 §8.3.2)", ref1.Sequence, ref2.Sequence)
	}
	if ref1.StreamID != ref2.StreamID {
		t.Fatalf("expected same stream for both records, got %q and %q", ref1.StreamID, ref2.StreamID)
	}
}

func TestPublishStampsProducerRef(t *testing.T) {
	m := NewMemory("market-data-ingestion", "v0.1.0-dev", "run-42")
	ctx := context.Background()

	if _, err := m.Publish(ctx, draft("evt-1"), nil); err != nil {
		t.Fatalf("Publish error: %v", err)
	}

	records := m.Records()
	if len(records) != 1 {
		t.Fatalf("len(Records()) = %d, want 1", len(records))
	}
	got := records[0].Envelope.ProducerRef
	want := envelope.ProducerRef{ModuleID: "market-data-ingestion", ImplementationVersion: "v0.1.0-dev", RunID: "run-42"}
	if got != want {
		t.Fatalf("ProducerRef = %+v, want %+v", got, want)
	}
}

func TestPublishCarriesPayload(t *testing.T) {
	m := NewMemory("market-data-ingestion", "v0.1.0-dev", "run-1")
	ctx := context.Background()
	type samplePayload struct{ X int }
	if _, err := m.Publish(ctx, draft("evt-1"), samplePayload{X: 7}); err != nil {
		t.Fatalf("Publish error: %v", err)
	}
	records := m.Records()
	got, ok := records[0].Payload.(samplePayload)
	if !ok || got.X != 7 {
		t.Fatalf("Payload = %#v, want samplePayload{X: 7}", records[0].Payload)
	}
}

func TestRecordsReturnsCopy(t *testing.T) {
	m := NewMemory("market-data-ingestion", "v0.1.0-dev", "run-1")
	ctx := context.Background()
	if _, err := m.Publish(ctx, draft("evt-1"), nil); err != nil {
		t.Fatalf("Publish error: %v", err)
	}
	records := m.Records()
	records[0].Envelope.EventID = "mutated"
	if m.Records()[0].Envelope.EventID == "mutated" {
		t.Fatalf("Records() leaked internal slice — caller mutation affected publisher state")
	}
}
