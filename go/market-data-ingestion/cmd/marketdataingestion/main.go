// Command marketdataingestion is a demonstration wiring of the
// market-data-ingestion pipeline: fake reference-data provider, in-memory
// event publisher, no real venue connectivity. It exists to show the
// pieces compose into a working pipeline end-to-end — it is not a
// deployable service. Real venue adapters, a real market-reference-service
// client, and real event-log publishing are out of scope for this
// transaction (see ../../README.md).
package main

import (
	"context"
	"fmt"
	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/candle"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/decimal"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/envelope"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/ingest"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/publish"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-data-ingestion/internal/reference"
)

func main() {
	ctx := context.Background()

	ref := reference.NewFake()
	pub := publish.NewMemory("market-data-ingestion", "v0.1.0-dev", "demo-run")
	svc := ingest.NewService(ref, pub)

	windowStart := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)

	ohlcv := func(close string) candle.OHLCV {
		return candle.OHLCV{
			Open:   decimal.MustFromString("65000"),
			High:   decimal.MustFromString("65100"),
			Low:    decimal.MustFromString("64950"),
			Close:  decimal.MustFromString(close),
			Volume: decimal.MustFromString("12.5"),
		}
	}

	// 1. A provisional observation while the candle is still forming.
	_, err := svc.ObserveProvisional(ctx, ingest.RawFact{
		EventID:             "demo-evt-observed-1",
		RawVenueID:          "binance-spot",
		RawInstrumentSymbol: "BTCUSDT",
		Timeframe:           "1m",
		Instant:             windowStart.Add(30 * time.Second),
		RecordedTime:        windowStart.Add(30 * time.Second),
		OHLCV:               ohlcv("65050"),
	})
	must(err)

	// 2. The window closes — first authoritative CandleClosed.
	closedResult, err := svc.IngestClosedFact(ctx, ingest.RawClosedFact{
		RawFact: ingest.RawFact{
			EventID:             "demo-evt-closed-1",
			RawVenueID:          "binance-spot",
			RawInstrumentSymbol: "BTCUSDT",
			Timeframe:           "1m",
			Instant:             windowStart.Add(59 * time.Second),
			RecordedTime:        windowStart.Add(60 * time.Second),
			OHLCV:               ohlcv("65080"),
			NativeSourceIdentity: &envelope.SourceIdentity{
				VenueID:      "binance-spot",
				InstrumentID: "BTCUSDT",
				Type:         "kline_update_id",
				Value:        "kline-1000",
			},
		},
		DataQuality: candle.DataQualityComplete,
	})
	must(err)
	fmt.Printf("first close outcome: %v, ref: %+v\n", closedResult.Outcome, closedResult.Ref)

	// 3. A late venue correction arrives (candle.md §11 Step 4).
	correctedResult, err := svc.IngestClosedFact(ctx, ingest.RawClosedFact{
		RawFact: ingest.RawFact{
			EventID:             "demo-evt-corrected-1",
			RawVenueID:          "binance-spot",
			RawInstrumentSymbol: "BTCUSDT",
			Timeframe:           "1m",
			Instant:             windowStart.Add(59 * time.Second),
			RecordedTime:        windowStart.Add(7 * time.Minute),
			OHLCV:               ohlcv("65095"), // authoritative value changed
			NativeSourceIdentity: &envelope.SourceIdentity{
				VenueID:      "binance-spot",
				InstrumentID: "BTCUSDT",
				Type:         "kline_update_id",
				Value:        "kline-1000-correction",
			},
		},
		DataQuality: candle.DataQualityComplete,
	})
	must(err)
	fmt.Printf("correction outcome: %v, ref: %+v, causation target: %+v\n", correctedResult.Outcome, correctedResult.Ref, closedResult.Ref)

	fmt.Println()
	fmt.Println("published records:")
	for _, r := range pub.Records() {
		fmt.Printf("  seq=%d type=%s event_id=%s causation_refs=%v\n",
			r.Envelope.Sequence, r.Envelope.EventType, r.Envelope.EventID, r.Envelope.CausationRefs)
	}
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}
