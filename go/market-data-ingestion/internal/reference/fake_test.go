package reference

import (
	"context"
	"errors"
	"testing"
	"time"
)

func TestFakeResolveIdentityKnown(t *testing.T) {
	f := NewFake()
	id, err := f.ResolveIdentity(context.Background(), "binance-spot", "BTCUSDT")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if id.InstrumentID != "BTC-USDT" || id.VenueID != "binance-spot" {
		t.Fatalf("got %+v, want BTC-USDT/binance-spot", id)
	}
}

func TestFakeResolveIdentityUnknown(t *testing.T) {
	f := NewFake()
	_, err := f.ResolveIdentity(context.Background(), "unknown-venue", "XXXX")
	if !errors.Is(err, ErrUnknownReference) {
		t.Fatalf("got err=%v, want ErrUnknownReference", err)
	}
}

func TestFakeWindowForAlignsToBucket(t *testing.T) {
	f := NewFake()
	t1 := time.Date(2026, 8, 19, 10, 0, 37, 0, time.UTC)
	w, err := f.WindowFor(context.Background(), "BTC-USDT", "binance-spot", "1m", t1)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	wantStart := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)
	wantEnd := time.Date(2026, 8, 19, 10, 1, 0, 0, time.UTC)
	if !w.Start.Equal(wantStart) || !w.End.Equal(wantEnd) {
		t.Fatalf("got [%v, %v), want [%v, %v)", w.Start, w.End, wantStart, wantEnd)
	}
}

func TestFakeWindowForUnknownTimeframe(t *testing.T) {
	f := NewFake()
	_, err := f.WindowFor(context.Background(), "BTC-USDT", "binance-spot", "3d", time.Now())
	if err == nil {
		t.Fatalf("expected error for unconfigured timeframe")
	}
}
