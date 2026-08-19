package store

import (
	"context"
	"testing"
	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/envelope"
)

func draft(eventID, subjectID string) envelope.Draft {
	return envelope.Draft{
		EventID:          eventID,
		EventType:        "SOMETHING_HAPPENED",
		CausationRefs:    []envelope.EventRecordRef{},
		RelatedEventRefs: []envelope.EventRecordRef{},
		RecordedTime:     time.Now().UTC(),
		SubjectRef:       envelope.SubjectRef{SubjectID: subjectID},
	}
}

func TestAppendAssignsContiguousSequenceAndProducerRef(t *testing.T) {
	m := NewMemory("market-reference-service", "v0.1.0-dev", "run-1")
	ctx := context.Background()

	ref1, err := m.Append(ctx, draft("evt-1", "subj-a"), nil)
	if err != nil {
		t.Fatalf("Append error: %v", err)
	}
	ref2, err := m.Append(ctx, draft("evt-2", "subj-a"), nil)
	if err != nil {
		t.Fatalf("Append error: %v", err)
	}
	if ref1.Sequence != 1 || ref2.Sequence != 2 {
		t.Fatalf("sequences = %d, %d, want 1, 2", ref1.Sequence, ref2.Sequence)
	}

	records := m.AllRecords()
	if records[0].Envelope.ProducerRef.ModuleID != "market-reference-service" {
		t.Fatalf("ProducerRef.ModuleID = %q, want market-reference-service", records[0].Envelope.ProducerRef.ModuleID)
	}
}

func TestRecordsForSubjectFiltersBySubjectID(t *testing.T) {
	m := NewMemory("market-reference-service", "v0.1.0-dev", "run-1")
	ctx := context.Background()

	if _, err := m.Append(ctx, draft("evt-1", "subj-a"), "payload-a"); err != nil {
		t.Fatalf("Append error: %v", err)
	}
	if _, err := m.Append(ctx, draft("evt-2", "subj-b"), "payload-b"); err != nil {
		t.Fatalf("Append error: %v", err)
	}
	if _, err := m.Append(ctx, draft("evt-3", "subj-a"), "payload-a2"); err != nil {
		t.Fatalf("Append error: %v", err)
	}

	got := m.RecordsForSubject("subj-a")
	if len(got) != 2 {
		t.Fatalf("len(RecordsForSubject) = %d, want 2", len(got))
	}
	if got[0].Payload != "payload-a" || got[1].Payload != "payload-a2" {
		t.Fatalf("unexpected payloads/order: %+v", got)
	}
}

func TestAllRecordsReturnsCopy(t *testing.T) {
	m := NewMemory("market-reference-service", "v0.1.0-dev", "run-1")
	ctx := context.Background()
	if _, err := m.Append(ctx, draft("evt-1", "subj-a"), nil); err != nil {
		t.Fatalf("Append error: %v", err)
	}
	records := m.AllRecords()
	records[0].Envelope.EventID = "mutated"
	if m.AllRecords()[0].Envelope.EventID == "mutated" {
		t.Fatalf("AllRecords() leaked internal slice")
	}
}
