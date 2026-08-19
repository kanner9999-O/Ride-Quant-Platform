package ingest

import (
	"context"
	"testing"
	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/envelope"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/publish"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/reference"
)

// TestIngestionReferenceResolutionIsDeterministicAndBitemporallyCorrect is
// the Phase-3 Data-Layer-completion cross-module acceptance test: it
// exercises the full market-data-ingestion pipeline (ingest.Service ->
// reference.Provider) against a reference.Fake that honors ADR-032 v0.2
// §B.3's two-axis bitemporal contract exactly the way
// go/market-reference-service/internal/query's own
// TestResolvePrecisionLookAheadGuard proves the real implementation does —
// same scenario, same assertions, independently verified on both sides of
// the module boundary. A literal single-process Go-level integration test
// importing both modules' internal packages is not possible without
// exporting either module's internal API (Go's internal/ visibility rules
// scope importability to each module's own tree) — doing so would itself
// be an unauthorized module-boundary/API-surface change this transaction
// does not make. This test is therefore the strongest verification
// achievable within scope: it proves market-data-ingestion's SIDE of the
// contract (it calls the two-axis Provider interface correctly and
// propagates the result deterministically) using the same fixture pattern
// query.Service's own test proves market-reference-service's SIDE with.
func TestIngestionReferenceResolutionIsDeterministicAndBitemporallyCorrect(t *testing.T) {
	ctx := context.Background()
	fake := reference.NewFake()
	pub := publish.NewMemory("market-data-ingestion", "v0.1.0-dev", "test-run")
	svc := NewService(fake, pub)

	effectiveInstant := time.Date(2026, 8, 19, 10, 0, 37, 0, time.UTC)
	correctionRecordedAt := time.Date(2026, 8, 19, 12, 0, 0, 0, time.UTC)

	// Baseline: ingest a provisional observation whose RecordedTime is
	// BEFORE the correction will be recorded — resolves the original
	// 1-minute window.
	beforeRaw := RawFact{
		EventID:             "evt-obs-before",
		RawVenueID:          "binance-spot",
		RawInstrumentSymbol: "BTCUSDT",
		Timeframe:           "1m",
		Instant:             effectiveInstant,
		RecordedTime:        correctionRecordedAt.Add(-time.Minute), // knowledge cursor BEFORE the correction
		OHLCV:               ohlcv("101"),
	}
	beforeRef, err := svc.ObserveProvisional(ctx, beforeRaw)
	if err != nil {
		t.Fatalf("ObserveProvisional (before correction) error: %v", err)
	}

	// A reference-data correction is now recorded: "1m" windows are
	// actually 5m, recorded at correctionRecordedAt — matching the
	// scenario go/market-reference-service/internal/query's
	// TestResolvePrecisionLookAheadGuard proves against the real
	// implementation.
	fake.ReviseDuration("1m", 5*time.Minute, correctionRecordedAt)

	// A second observation, SAME effective instant, but with RecordedTime
	// (knowledge cursor) BEFORE the correction was recorded — must resolve
	// to the SAME window as the baseline (deterministic; stale/future
	// reference facts must not leak backward).
	stillOldRaw := beforeRaw
	stillOldRaw.EventID = "evt-obs-still-old"
	stillOldRaw.RecordedTime = correctionRecordedAt.Add(-30 * time.Second)
	stillOldRef, err := svc.ObserveProvisional(ctx, stillOldRaw)
	if err != nil {
		t.Fatalf("ObserveProvisional (still before correction) error: %v", err)
	}

	// A third observation, SAME effective instant, with RecordedTime AFTER
	// the correction — must resolve to the CORRECTED (wider) window.
	afterRaw := beforeRaw
	afterRaw.EventID = "evt-obs-after"
	afterRaw.RecordedTime = correctionRecordedAt.Add(time.Minute)
	afterRef, err := svc.ObserveProvisional(ctx, afterRaw)
	if err != nil {
		t.Fatalf("ObserveProvisional (after correction) error: %v", err)
	}

	windowEnd := func(ref envelope.EventRecordRef) time.Time {
		for _, r := range pub.Records() {
			if r.Envelope.EventID == ref.EventID {
				return r.Envelope.EffectiveTime.WindowEnd
			}
		}
		t.Fatalf("record for %v not found", ref)
		return time.Time{}
	}

	wantBefore := time.Date(2026, 8, 19, 10, 1, 0, 0, time.UTC) // 1m bucket
	wantAfter := time.Date(2026, 8, 19, 10, 5, 0, 0, time.UTC)  // corrected 5m bucket

	if got := windowEnd(beforeRef); !got.Equal(wantBefore) {
		t.Fatalf("baseline window end = %v, want %v", got, wantBefore)
	}
	if got := windowEnd(stillOldRef); !got.Equal(wantBefore) {
		t.Fatalf("knowledge cursor still before correction: window end = %v, want %v (stale/future reference facts must not leak backward)", got, wantBefore)
	}
	if got := windowEnd(afterRef); !got.Equal(wantAfter) {
		t.Fatalf("knowledge cursor after correction: window end = %v, want %v (effective_time alone must not control visibility)", got, wantAfter)
	}

	// Determinism: resolving the exact same (effectiveInstant,
	// knowledgeCursor) pair twice must yield the exact same result —
	// re-run the "before" case and confirm it's unchanged.
	repeatRaw := beforeRaw
	repeatRaw.EventID = "evt-obs-repeat"
	repeatRef, err := svc.ObserveProvisional(ctx, repeatRaw)
	if err != nil {
		t.Fatalf("ObserveProvisional (repeat) error: %v", err)
	}
	if got := windowEnd(repeatRef); !got.Equal(wantBefore) {
		t.Fatalf("repeat query with identical cursor pair = %v, want %v (deterministic resolution)", got, wantBefore)
	}
}

// TestIngestionCannotSeeFutureIdentityCorrections is the P3-DL-A-MAJ-01
// acceptance test at the full ingest.Service pipeline level: a venue-side
// identity revision (e.g. a rebrand) recorded after a fact's knowledge
// cursor must not affect which canonical instrument_id/venue_id that fact
// resolves to and publishes under, even though the revision is already
// recorded in the reference store by the time this test asserts on it.
func TestIngestionCannotSeeFutureIdentityCorrections(t *testing.T) {
	ctx := context.Background()
	fake := reference.NewFake()
	pub := publish.NewMemory("market-data-ingestion", "v0.1.0-dev", "test-run")
	svc := NewService(fake, pub)

	effectiveInstant := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)
	revisionRecordedAt := effectiveInstant.Add(2 * time.Hour)

	// Ingest a fact whose RecordedTime (knowledge cursor) is BEFORE the
	// identity revision will be recorded.
	raw := RawFact{
		EventID:             "evt-obs-1",
		RawVenueID:          "binance-spot",
		RawInstrumentSymbol: "BTCUSDT",
		Timeframe:           "1m",
		Instant:             effectiveInstant,
		RecordedTime:        revisionRecordedAt.Add(-time.Minute),
		OHLCV:               ohlcv("101"),
	}
	ref, err := svc.ObserveProvisional(ctx, raw)
	if err != nil {
		t.Fatalf("ObserveProvisional error: %v", err)
	}

	// Now register a revised identity, effective retroactively but
	// recorded AFTER the fact above was already ingested.
	fake.ReviseIdentity("binance-spot", "BTCUSDT",
		reference.Identity{InstrumentID: "BTC-USDT-REBRANDED", VenueID: "binance-spot"},
		effectiveInstant.Add(-time.Hour), revisionRecordedAt)

	var subjectID string
	for _, r := range pub.Records() {
		if r.Envelope.EventID == ref.EventID {
			subjectID = r.Envelope.SubjectRef.SubjectID
		}
	}
	if subjectID == "" {
		t.Fatalf("published record for %v not found", ref)
	}

	// The already-published event's subject identity must remain resolved
	// against the ORIGINAL (BTC-USDT) instrument — the later-recorded
	// rebrand must not retroactively change a fact already ingested at an
	// earlier knowledge cursor (candle_subject_id is derived from
	// InstrumentID/VenueID at resolution time, so a different resolved
	// InstrumentID would have produced a different subject_id entirely).
	rawBefore := raw
	rawBefore.EventID = "evt-obs-repeat-before-cursor"
	repeatRef, err := svc.ObserveProvisional(ctx, rawBefore)
	if err != nil {
		t.Fatalf("ObserveProvisional (repeat, same knowledge cursor) error: %v", err)
	}
	var repeatSubjectID string
	for _, r := range pub.Records() {
		if r.Envelope.EventID == repeatRef.EventID {
			repeatSubjectID = r.Envelope.SubjectRef.SubjectID
		}
	}
	if repeatSubjectID != subjectID {
		t.Fatalf("got subject_id=%q for a fact re-ingested at the same knowledge cursor after the rebrand was recorded, want unchanged %q (future identity correction leaked backward)", repeatSubjectID, subjectID)
	}

	// A NEW fact, ingested with a knowledge cursor AFTER the rebrand was
	// recorded, resolves to a DIFFERENT subject (the rebranded instrument)
	// — proving the pipeline does track the correction once it is actually
	// visible, not that identity resolution is frozen forever.
	rawAfter := raw
	rawAfter.EventID = "evt-obs-after-cursor"
	rawAfter.RecordedTime = revisionRecordedAt.Add(time.Minute)
	afterRef, err := svc.ObserveProvisional(ctx, rawAfter)
	if err != nil {
		t.Fatalf("ObserveProvisional (after revision recorded) error: %v", err)
	}
	var afterSubjectID string
	for _, r := range pub.Records() {
		if r.Envelope.EventID == afterRef.EventID {
			afterSubjectID = r.Envelope.SubjectRef.SubjectID
		}
	}
	if afterSubjectID == subjectID {
		t.Fatalf("got same subject_id=%q for a fact ingested AFTER the rebrand was recorded, want a different subject_id (rebranded instrument)", afterSubjectID)
	}
}
