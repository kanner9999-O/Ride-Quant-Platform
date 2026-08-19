// Command marketreferenceservice is a demonstration wiring of
// market-reference-service: register an Instrument, a Venue, and a
// TradableListing, then resolve identity/window/precision through
// query.Service — showing the pieces compose end-to-end. It is not a
// deployable service; there is no real storage/transport here (see
// ../../README.md).
package main

import (
	"context"
	"fmt"
	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/calendar"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/decimal"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/instrument"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/listing"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/query"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/store"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/venue"
)

func main() {
	ctx := context.Background()
	s := store.NewMemory("market-reference-service", "v0.1.0-dev", "demo-run")
	instruments := instrument.NewRegistry(s)
	venues := venue.NewRegistry(s)
	listings := listing.NewRegistry(s)
	calendars := calendar.NewResolver(map[string]calendar.Calendar{"cal-crypto-247": calendar.NewContinuous()})
	svc := query.NewService(instruments, venues, listings, calendars)

	t0 := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)

	insScope := instrument.Scope{InstrumentIdentityRef: "btc-usdt", BaseAssetRef: "BTC", QuoteAssetRef: "USDT", InstrumentType: "SPOT"}
	insRef, err := instruments.Register(ctx, "ins-reg-1", insScope, "BTC/USDT Spot", t0, t0)
	must(err)

	venScope := venue.Scope{VenueIdentityRef: "binance-spot", VenueType: "CENTRALIZED_EXCHANGE"}
	venRef, err := venues.Register(ctx, "ven-reg-1", venScope, "Binance", "UTC", "cal-crypto-247", "prec-default", t0, t0)
	must(err)

	lstScope := listing.Scope{InstrumentID: insScope.InstrumentID(), VenueID: venScope.VenueID(), ListingID: "lst-btcusdt-binance-1"}
	_, err = listings.CreateListing(ctx, listing.CreateListingInput{
		Scope: lstScope, VenueSymbol: "BTCUSDT",
		PriceIncrement: decimal.MustFromString("0.01"), QuantityIncrement: decimal.MustFromString("0.0001"),
		SessionCalendarRef: "cal-crypto-247", ActivationRequestID: listing.DeterministicActivationRequestID(lstScope),
		InstrumentRegistered: insRef, VenueRegistered: venRef,
		RecordedTime: t0, EffectiveTime: t0,
		RequestEventID: "req-1", ReservedEventID: "res-1", CreatedEventID: "created-1",
	})
	must(err)

	instant := time.Date(2026, 8, 19, 10, 0, 37, 0, time.UTC)
	knowledgeCursor := instant.Add(time.Minute)

	id, err := svc.ResolveIdentity("binance-spot", "BTCUSDT", instant, knowledgeCursor)
	must(err)
	fmt.Printf("identity: %+v\n", id)

	window, err := svc.ResolveWindow(id.InstrumentID, id.VenueID, "1m", instant, knowledgeCursor)
	must(err)
	fmt.Printf("window: [%v, %v)\n", window.Start, window.End)

	precision, err := svc.ResolvePrecision(id.InstrumentID, id.VenueID, instant, knowledgeCursor)
	must(err)
	fmt.Printf("precision: price_increment=%s quantity_increment=%s\n", precision.PriceIncrement.String(), precision.QuantityIncrement.String())
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}
