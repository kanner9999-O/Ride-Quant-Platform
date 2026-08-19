package calendar

import (
	"testing"
	"time"
)

func TestContinuousWindowForAlignsToBucket(t *testing.T) {
	c := NewContinuous()
	instant := time.Date(2026, 8, 19, 10, 0, 37, 0, time.UTC)
	w, ok := c.WindowFor(instant, "1m")
	if !ok {
		t.Fatalf("expected ok=true")
	}
	wantStart := time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC)
	wantEnd := time.Date(2026, 8, 19, 10, 1, 0, 0, time.UTC)
	if !w.Start.Equal(wantStart) || !w.End.Equal(wantEnd) {
		t.Fatalf("got [%v, %v), want [%v, %v)", w.Start, w.End, wantStart, wantEnd)
	}
}

func TestContinuousUnknownTimeframe(t *testing.T) {
	c := NewContinuous()
	_, ok := c.WindowFor(time.Now(), "3d")
	if ok {
		t.Fatalf("expected ok=false for unconfigured timeframe")
	}
}

func TestResolverResolvesRegisteredRef(t *testing.T) {
	r := NewResolver(map[string]Calendar{"cal-crypto-247": NewContinuous()})
	c, ok := r.Resolve("cal-crypto-247")
	if !ok {
		t.Fatalf("expected ok=true for registered ref")
	}
	if _, windowOK := c.WindowFor(time.Now(), "1m"); !windowOK {
		t.Fatalf("expected resolved calendar to answer WindowFor")
	}
}

func TestResolverUnknownRef(t *testing.T) {
	r := NewResolver(map[string]Calendar{})
	_, ok := r.Resolve("unknown-ref")
	if ok {
		t.Fatalf("expected ok=false for unknown ref")
	}
}
