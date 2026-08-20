package ingest

import (
	"context"
	"errors"
	"testing"
	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/candle"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/decimal"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/envelope"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/precedence"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/publish"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/reference"
)

func newTestService() (*Service, *publish.Memory) {
	pub := publish.NewMemory("market-data-ingestion", "v0.1.0-dev", "test-run")
	svc := NewService(reference.NewFake(), pub)
	return svc, pub
}

func ohlcv(close string) candle.OHLCV {
	return candle.OHLCV{
		Open:   decimal.MustFromString("100"),
		High:   decimal.MustFromString("110"),
		Low:    decimal.MustFromString("90"),
		Close:  decimal.MustFromString(close),
		Volume: decimal.MustFromString("5"),
	}
}

// brokenOHLCV returns an otherwise-well-formed OHLCV with exactly one
// required field left at the Go zero value (uninitialized decimal.Decimal{},
// distinct from a legitimately parsed zero) — the P3-MDI-DECIMAL-MAJ-01
// regression fixture.
func brokenOHLCV(missingField string) candle.OHLCV {
	o := ohlcv("101")
	switch missingField {
	case "open":
		o.Open = decimal.Decimal{}
	case "high":
		o.High = decimal.Decimal{}
	case "low":
		o.Low = decimal.Decimal{}
	case "close":
		o.Close = decimal.Decimal{}
	case "volume":
		o.Volume = decimal.Decimal{}
	default:
		panic("brokenOHLCV: unknown field " + missingField)
	}
	return o
}

var requiredOHLCVFields = []string{"open", "high", "low", "close", "volume"}

func rawClosed(t time.Time, close, sourceIdentityValue string) RawClosedFact {
	return RawClosedFact{
		RawFact: RawFact{
			EventID:             "evt-" + close,
			RawVenueID:          "binance-spot",
			RawInstrumentSymbol: "BTCUSDT",
			Timeframe:           "1m",
			Instant:             t,
			RecordedTime:        t,
			OHLCV:               ohlcv(close),
			NativeSourceIdentity: &envelope.SourceIdentity{
				VenueID:      "binance-spot",
				InstrumentID: "BTCUSDT",
				Type:         "kline_update_id",
				Value:        sourceIdentityValue,
			},
		},
		DataQuality: candle.DataQualityComplete,
	}
}

func TestObserveProvisionalPublishesObservedEvent(t *testing.T) {
	svc, pub := newTestService()
	ctx := context.Background()
	instant := time.Date(2026, 8, 19, 10, 0, 30, 0, time.UTC)

	raw := RawFact{
		EventID:             "evt-obs-1",
		RawVenueID:          "binance-spot",
		RawInstrumentSymbol: "BTCUSDT",
		Timeframe:           "1m",
		Instant:             instant,
		RecordedTime:        instant,
		OHLCV:               ohlcv("101"),
	}
	ref, err := svc.ObserveProvisional(ctx, raw)
	if err != nil {
		t.Fatalf("ObserveProvisional error: %v", err)
	}
	if ref.EventID != "evt-obs-1" {
		t.Fatalf("ref.EventID = %q, want evt-obs-1", ref.EventID)
	}

	records := pub.Records()
	if len(records) != 1 {
		t.Fatalf("len(Records()) = %d, want 1", len(records))
	}
	if records[0].Envelope.EventType != candle.EventTypeObserved {
		t.Errorf("EventType = %q, want %q", records[0].Envelope.EventType, candle.EventTypeObserved)
	}
	payload, ok := records[0].Payload.(candle.ObservedPayload)
	if !ok {
		t.Fatalf("Payload type = %T, want candle.ObservedPayload", records[0].Payload)
	}
	if !payload.Close.Equal(ohlcv("101").Close) {
		t.Errorf("payload.Close = %s, want 101", payload.Close.String())
	}
}

func TestObserveProvisionalUnknownVenueFailsClean(t *testing.T) {
	svc, _ := newTestService()
	ctx := context.Background()
	raw := RawFact{
		EventID:             "evt-x",
		RawVenueID:          "unknown-venue",
		RawInstrumentSymbol: "XXXX",
		Timeframe:           "1m",
		Instant:             time.Now(),
		OHLCV:               ohlcv("1"),
	}
	_, err := svc.ObserveProvisional(ctx, raw)
	if !errors.Is(err, reference.ErrUnknownReference) {
		t.Fatalf("got err=%v, want wrapping ErrUnknownReference", err)
	}
}

func TestIngestClosedFactFirstCloseThenDuplicateThenCorrection(t *testing.T) {
	svc, pub := newTestService()
	ctx := context.Background()
	t1 := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)

	// First close for this subject.
	res1, err := svc.IngestClosedFact(ctx, rawClosed(t1, "105", "sid-1"))
	if err != nil {
		t.Fatalf("IngestClosedFact (first) error: %v", err)
	}
	if res1.Outcome != precedence.OutcomeEmitFirstClosed {
		t.Fatalf("outcome = %v, want OutcomeEmitFirstClosed", res1.Outcome)
	}

	// Exact duplicate delivery (same identity, same payload) -> zero effect.
	res2, err := svc.IngestClosedFact(ctx, rawClosed(t1, "105", "sid-1"))
	if err != nil {
		t.Fatalf("IngestClosedFact (duplicate) error: %v", err)
	}
	if res2.Outcome != precedence.OutcomeDuplicateZeroEffect {
		t.Fatalf("outcome = %v, want OutcomeDuplicateZeroEffect", res2.Outcome)
	}

	// New identity, changed payload -> correction, causation_refs must
	// point at the first CandleClosed.
	res3, err := svc.IngestClosedFact(ctx, rawClosed(t1, "106", "sid-2"))
	if err != nil {
		t.Fatalf("IngestClosedFact (correction) error: %v", err)
	}
	if res3.Outcome != precedence.OutcomeEmitCorrected {
		t.Fatalf("outcome = %v, want OutcomeEmitCorrected", res3.Outcome)
	}

	records := pub.Records()
	if len(records) != 2 { // duplicate must NOT have published anything
		t.Fatalf("len(Records()) = %d, want 2 (first close + correction only)", len(records))
	}
	closedRef := envelope.EventRecordRef{StreamID: records[0].Envelope.StreamRef.StreamID, Sequence: records[0].Envelope.Sequence, EventID: records[0].Envelope.EventID}
	correctedCausation := records[1].Envelope.CausationRefs
	if len(correctedCausation) != 1 || correctedCausation[0] != closedRef {
		t.Fatalf("CandleCorrected causation_refs = %v, want [%v]", correctedCausation, closedRef)
	}
	if records[1].Envelope.EventType != candle.EventTypeCorrected {
		t.Fatalf("EventType = %q, want %q", records[1].Envelope.EventType, candle.EventTypeCorrected)
	}
}

func TestIngestClosedFactUnresolvedIdentityFailsClosedAndPublishesNothing(t *testing.T) {
	svc, pub := newTestService()
	ctx := context.Background()
	t1 := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)

	raw := rawClosed(t1, "105", "")
	raw.NativeSourceIdentity = nil // no native identity, no fallback declared

	res, err := svc.IngestClosedFact(ctx, raw)
	if err != nil {
		t.Fatalf("IngestClosedFact error: %v", err)
	}
	if res.Outcome != precedence.OutcomeFailClosed {
		t.Fatalf("outcome = %v, want OutcomeFailClosed", res.Outcome)
	}
	if len(pub.Records()) != 0 {
		t.Fatalf("expected nothing published on fail-closed, got %d records", len(pub.Records()))
	}
}

func TestIngestClosedFactProvenanceIntegrityViolation(t *testing.T) {
	svc, pub := newTestService()
	ctx := context.Background()
	t1 := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)

	if _, err := svc.IngestClosedFact(ctx, rawClosed(t1, "105", "sid-1")); err != nil {
		t.Fatalf("IngestClosedFact (first) error: %v", err)
	}
	// Same identity, different payload -> integrity violation, fail closed.
	res, err := svc.IngestClosedFact(ctx, rawClosed(t1, "999", "sid-1"))
	if err != nil {
		t.Fatalf("IngestClosedFact (conflicting) error: %v", err)
	}
	if res.Outcome != precedence.OutcomeFailClosed {
		t.Fatalf("outcome = %v, want OutcomeFailClosed", res.Outcome)
	}
	if len(pub.Records()) != 1 { // only the original first-close was published
		t.Fatalf("len(Records()) = %d, want 1", len(pub.Records()))
	}
}

func TestReportDataGapPublishesNoOHLCPayload(t *testing.T) {
	svc, pub := newTestService()
	ctx := context.Background()
	scope := candle.Scope{
		InstrumentID: "BTC-USDT",
		VenueID:      "binance-spot",
		Timeframe:    "1m",
		WindowStart:  time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC),
		WindowEnd:    time.Date(2026, 8, 19, 10, 1, 0, 0, time.UTC),
	}
	ref, err := svc.ReportDataGap(ctx, "evt-gap-1", scope, time.Now().UTC(), candle.GapReasonSourceUnavailable)
	if err != nil {
		t.Fatalf("ReportDataGap error: %v", err)
	}
	if ref.EventID != "evt-gap-1" {
		t.Fatalf("ref.EventID = %q, want evt-gap-1", ref.EventID)
	}
	records := pub.Records()
	payload, ok := records[0].Payload.(candle.DataGapPayload)
	if !ok {
		t.Fatalf("Payload type = %T, want candle.DataGapPayload", records[0].Payload)
	}
	if payload.Reason != candle.GapReasonSourceUnavailable {
		t.Errorf("Reason = %q, want %q", payload.Reason, candle.GapReasonSourceUnavailable)
	}
	if len(records[0].Envelope.CausationRefs) != 0 {
		t.Errorf("CausationRefs = %v, want empty (root event)", records[0].Envelope.CausationRefs)
	}
}

// TestObserveProvisionalRejectsUninitializedRequiredFields is a
// P3-MDI-DECIMAL-MAJ-01 regression test: an uninitialized required OHLCV
// field must fail closed with ErrInvalidOHLCV, publish nothing, and never
// panic — for each of the five required fields independently.
func TestObserveProvisionalRejectsUninitializedRequiredFields(t *testing.T) {
	for _, field := range requiredOHLCVFields {
		t.Run(field, func(t *testing.T) {
			svc, pub := newTestService()
			ctx := context.Background()
			raw := RawFact{
				EventID:             "evt-invalid-" + field,
				RawVenueID:          "binance-spot",
				RawInstrumentSymbol: "BTCUSDT",
				Timeframe:           "1m",
				Instant:             time.Date(2026, 8, 19, 10, 0, 30, 0, time.UTC),
				RecordedTime:        time.Date(2026, 8, 19, 10, 0, 30, 0, time.UTC),
				OHLCV:               brokenOHLCV(field),
			}
			_, err := svc.ObserveProvisional(ctx, raw)
			if !errors.Is(err, ErrInvalidOHLCV) {
				t.Fatalf("ObserveProvisional(%s unset) err = %v, want wrapping ErrInvalidOHLCV", field, err)
			}
			if len(pub.Records()) != 0 {
				t.Fatalf("ObserveProvisional(%s unset) published %d records, want 0", field, len(pub.Records()))
			}
		})
	}
}

// TestObserveProvisionalAcceptsLegitimateZeroValue proves the fix does not
// reject a legitimately parsed numeric zero (e.g. zero-volume bars) —
// IsInitialized is a presence check, not a value check.
func TestObserveProvisionalAcceptsLegitimateZeroValue(t *testing.T) {
	svc, pub := newTestService()
	ctx := context.Background()
	o := ohlcv("101")
	o.Volume = decimal.MustFromString("0")
	raw := RawFact{
		EventID:             "evt-zero-vol",
		RawVenueID:          "binance-spot",
		RawInstrumentSymbol: "BTCUSDT",
		Timeframe:           "1m",
		Instant:             time.Date(2026, 8, 19, 10, 0, 30, 0, time.UTC),
		RecordedTime:        time.Date(2026, 8, 19, 10, 0, 30, 0, time.UTC),
		OHLCV:               o,
	}
	if _, err := svc.ObserveProvisional(ctx, raw); err != nil {
		t.Fatalf("ObserveProvisional with legitimate zero volume: unexpected error: %v", err)
	}
	if len(pub.Records()) != 1 {
		t.Fatalf("len(Records()) = %d, want 1", len(pub.Records()))
	}
}

// TestIngestClosedFactRejectsUninitializedRequiredFieldsFirstFact is a
// P3-MDI-DECIMAL-MAJ-01 regression test for the "no prior fact" path: an
// uninitialized required field must fail closed before resolveScope /
// precedence.Resolve ever run, for each required field independently.
func TestIngestClosedFactRejectsUninitializedRequiredFieldsFirstFact(t *testing.T) {
	for _, field := range requiredOHLCVFields {
		t.Run(field, func(t *testing.T) {
			svc, pub := newTestService()
			ctx := context.Background()
			t1 := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)

			raw := rawClosed(t1, "105", "sid-"+field)
			raw.OHLCV = brokenOHLCV(field)

			_, err := svc.IngestClosedFact(ctx, raw)
			if !errors.Is(err, ErrInvalidOHLCV) {
				t.Fatalf("IngestClosedFact(%s unset, first fact) err = %v, want wrapping ErrInvalidOHLCV", field, err)
			}
			if len(pub.Records()) != 0 {
				t.Fatalf("IngestClosedFact(%s unset, first fact) published %d records, want 0", field, len(pub.Records()))
			}
			svc.mu.Lock()
			n := len(svc.lastFact)
			svc.mu.Unlock()
			if n != 0 {
				t.Fatalf("IngestClosedFact(%s unset, first fact) left %d lastFact entries, want 0", field, n)
			}
		})
	}
}

// TestIngestClosedFactRejectsUninitializedRequiredFieldsExistingFact is the
// P3-MDI-DECIMAL-MAJ-01 core regression test: it reproduces the exact
// Formal QG panic path (a second closed fact for a subject that already has
// an accepted authoritative fact, which precedence.Resolve compares via
// payloadEqual's .Equal() calls) and proves it now fails closed with
// ErrInvalidOHLCV — before precedence.Resolve/payloadEqual are ever
// reached — instead of nil-pointer-panicking, and that the existing
// authoritative fact/publication record is left untouched.
func TestIngestClosedFactRejectsUninitializedRequiredFieldsExistingFact(t *testing.T) {
	for _, field := range requiredOHLCVFields {
		t.Run(field, func(t *testing.T) {
			svc, pub := newTestService()
			ctx := context.Background()
			t1 := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)

			// Seed an existing accepted authoritative fact for this subject.
			seedRaw := rawClosed(t1, "105", "sid-first-"+field)
			seed, err := svc.IngestClosedFact(ctx, seedRaw)
			if err != nil {
				t.Fatalf("IngestClosedFact (seed) error: %v", err)
			}
			if seed.Outcome != precedence.OutcomeEmitFirstClosed {
				t.Fatalf("seed outcome = %v, want OutcomeEmitFirstClosed", seed.Outcome)
			}
			if len(pub.Records()) != 1 {
				t.Fatalf("after seeding, len(Records()) = %d, want 1", len(pub.Records()))
			}

			// Second fact, same subject, one required field left
			// uninitialized: before the fix this reached payloadEqual and
			// nil-pointer-panicked comparing against the seeded fact.
			raw := rawClosed(t1, "106", "sid-second-"+field)
			raw.OHLCV = brokenOHLCV(field)
			_, err = svc.IngestClosedFact(ctx, raw)
			if !errors.Is(err, ErrInvalidOHLCV) {
				t.Fatalf("IngestClosedFact(%s unset, existing fact) err = %v, want wrapping ErrInvalidOHLCV", field, err)
			}
			// No CandleCorrected (or any other event) published: still only
			// the seeded first-close record.
			if len(pub.Records()) != 1 {
				t.Fatalf("IngestClosedFact(%s unset, existing fact) len(Records()) = %d, want still 1", field, len(pub.Records()))
			}
			if records := pub.Records(); records[0].Envelope.EventType != candle.EventTypeClosed {
				t.Fatalf("only published record EventType = %q, want %q (the seed, unchanged)", records[0].Envelope.EventType, candle.EventTypeClosed)
			}
		})
	}
}

// TestIngestClosedFactAcceptsLegitimateZeroValue proves the fix does not
// reject a legitimately parsed numeric zero on the closed-fact path either.
func TestIngestClosedFactAcceptsLegitimateZeroValue(t *testing.T) {
	svc, pub := newTestService()
	ctx := context.Background()
	t1 := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)

	raw := rawClosed(t1, "105", "sid-zero-vol")
	raw.OHLCV.Volume = decimal.MustFromString("0")

	res, err := svc.IngestClosedFact(ctx, raw)
	if err != nil {
		t.Fatalf("IngestClosedFact with legitimate zero volume: unexpected error: %v", err)
	}
	if res.Outcome != precedence.OutcomeEmitFirstClosed {
		t.Fatalf("outcome = %v, want OutcomeEmitFirstClosed", res.Outcome)
	}
	if len(pub.Records()) != 1 {
		t.Fatalf("len(Records()) = %d, want 1", len(pub.Records()))
	}
}
