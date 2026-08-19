package reference

import (
	"context"
	"errors"
	"testing"
	"time"
)

func TestFakeResolveIdentityKnown(t *testing.T) {
	f := NewFake()
	now := time.Now()
	id, err := f.ResolveIdentity(context.Background(), "binance-spot", "BTCUSDT", now, now)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if id.InstrumentID != "BTC-USDT" || id.VenueID != "binance-spot" {
		t.Fatalf("got %+v, want BTC-USDT/binance-spot", id)
	}
}

func TestFakeResolveIdentityUnknown(t *testing.T) {
	f := NewFake()
	now := time.Now()
	_, err := f.ResolveIdentity(context.Background(), "unknown-venue", "XXXX", now, now)
	if !errors.Is(err, ErrUnknownReference) {
		t.Fatalf("got err=%v, want ErrUnknownReference", err)
	}
}

func TestFakeWindowForAlignsToBucket(t *testing.T) {
	f := NewFake()
	t1 := time.Date(2026, 8, 19, 10, 0, 37, 0, time.UTC)
	w, err := f.WindowFor(context.Background(), "BTC-USDT", "binance-spot", "1m", t1, t1)
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
	now := time.Now()
	_, err := f.WindowFor(context.Background(), "BTC-USDT", "binance-spot", "3d", now, now)
	if err == nil {
		t.Fatalf("expected error for unconfigured timeframe")
	}
}

// TestFakeWindowForLookAheadGuard exercises the ADR-032 §B.3 two-axis
// contract directly against the Fake: a duration correction recorded later
// must not leak into a query with an earlier knowledge cursor, and the
// same effective instant resolves differently only once the knowledge
// cursor advances past the correction's recorded_time.
func TestFakeWindowForLookAheadGuard(t *testing.T) {
	f := NewFake()
	effectiveInstant := time.Date(2026, 8, 19, 10, 0, 37, 0, time.UTC)
	correctionRecordedAt := time.Date(2026, 8, 19, 12, 0, 0, 0, time.UTC)

	// Correct "1m" to actually mean 5m windows, recorded at
	// correctionRecordedAt.
	f.ReviseDuration("1m", 5*time.Minute, correctionRecordedAt)

	// Knowledge cursor BEFORE the correction was recorded: still sees the
	// original 1-minute bucket for the same effective instant.
	before, err := f.WindowFor(context.Background(), "BTC-USDT", "binance-spot", "1m", effectiveInstant, correctionRecordedAt.Add(-time.Minute))
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	wantBeforeEnd := time.Date(2026, 8, 19, 10, 1, 0, 0, time.UTC)
	if !before.End.Equal(wantBeforeEnd) {
		t.Fatalf("got End=%v at knowledge cursor before correction, want %v (correction must not leak backward)", before.End, wantBeforeEnd)
	}

	// Knowledge cursor AFTER the correction was recorded, SAME effective
	// instant: sees the corrected 5-minute bucket.
	after, err := f.WindowFor(context.Background(), "BTC-USDT", "binance-spot", "1m", effectiveInstant, correctionRecordedAt.Add(time.Minute))
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	wantAfterEnd := time.Date(2026, 8, 19, 10, 5, 0, 0, time.UTC)
	if !after.End.Equal(wantAfterEnd) {
		t.Fatalf("got End=%v at knowledge cursor after correction, want %v (effective_time alone must not control visibility)", after.End, wantAfterEnd)
	}
}

// TestFakeResolveIdentityLookAheadGuard is the P3-DL-A-MAJ-01 acceptance
// test at the Fake boundary: identity resolution must obey the same
// two-axis bitemporal contract as WindowFor. A revised/corrected identity
// mapping recorded later must not leak backward into an earlier
// knowledge-cursor query at the same effective instant, and identical
// cursor pairs must resolve deterministically.
func TestFakeResolveIdentityLookAheadGuard(t *testing.T) {
	f := NewFake()
	effectiveInstant := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)
	revisionEffectiveAt := effectiveInstant.Add(-time.Hour) // forward-looking from before our query instant
	revisionRecordedAt := effectiveInstant.Add(2 * time.Hour)

	// 1. Identity mapping A (the Fake's base mapping) is effective at T.
	before, err := f.ResolveIdentity(context.Background(), "binance-spot", "BTCUSDT", effectiveInstant, revisionRecordedAt.Add(-time.Minute))
	if err != nil {
		t.Fatalf("ResolveIdentity (before revision) error: %v", err)
	}
	if before.InstrumentID != "BTC-USDT" {
		t.Fatalf("got %+v, want InstrumentID=BTC-USDT", before)
	}

	// 2. A corrected/revised mapping B is recorded later.
	revised := Identity{InstrumentID: "BTC-USDT-REVISED", VenueID: "binance-spot"}
	f.ReviseIdentity("binance-spot", "BTCUSDT", revised, revisionEffectiveAt, revisionRecordedAt)

	// 3. Query at effective T + an EARLIER knowledge cursor still resolves
	// A — the revision must not leak backward.
	stillOld, err := f.ResolveIdentity(context.Background(), "binance-spot", "BTCUSDT", effectiveInstant, revisionRecordedAt.Add(-time.Minute))
	if err != nil {
		t.Fatalf("ResolveIdentity (knowledge cursor before revision) error: %v", err)
	}
	if stillOld.InstrumentID != "BTC-USDT" {
		t.Fatalf("got %+v at knowledge cursor before revision, want unchanged InstrumentID=BTC-USDT (look-ahead leak)", stillOld)
	}

	// 4. SAME effective T + a LATER knowledge cursor resolves B.
	after, err := f.ResolveIdentity(context.Background(), "binance-spot", "BTCUSDT", effectiveInstant, revisionRecordedAt.Add(time.Minute))
	if err != nil {
		t.Fatalf("ResolveIdentity (knowledge cursor after revision) error: %v", err)
	}
	if after.InstrumentID != "BTC-USDT-REVISED" {
		t.Fatalf("got %+v at knowledge cursor after revision, want InstrumentID=BTC-USDT-REVISED (effective_time alone must not control visibility)", after)
	}

	// 5. Determinism: identical cursor pairs resolve identically.
	repeat, err := f.ResolveIdentity(context.Background(), "binance-spot", "BTCUSDT", effectiveInstant, revisionRecordedAt.Add(time.Minute))
	if err != nil {
		t.Fatalf("ResolveIdentity (repeat) error: %v", err)
	}
	if repeat != after {
		t.Fatalf("got %+v on repeat query with identical cursor pair, want %+v (deterministic resolution)", repeat, after)
	}
}
