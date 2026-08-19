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
