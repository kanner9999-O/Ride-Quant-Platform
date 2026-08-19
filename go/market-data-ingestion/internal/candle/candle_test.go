package candle

import (
	"testing"
	"time"
)

func mkScope() Scope {
	return Scope{
		InstrumentID: "BTC-USDT",
		VenueID:      "binance-spot",
		Timeframe:    "1m",
		WindowStart:  time.Date(2026, 8, 19, 10, 0, 0, 0, time.UTC),
		WindowEnd:    time.Date(2026, 8, 19, 10, 1, 0, 0, time.UTC),
	}
}

func TestSubjectIDDeterministic(t *testing.T) {
	a := mkScope().SubjectID()
	b := mkScope().SubjectID()
	if a != b {
		t.Fatalf("SubjectID not deterministic: %q != %q", a, b)
	}
}

func TestSubjectIDStableAcrossTimezone(t *testing.T) {
	// Same instant, different location — must hash the same (I-2 parity
	// requires this to not depend on caller's local timezone).
	loc := time.FixedZone("UTC+7", 7*60*60)
	s1 := mkScope()
	s2 := s1
	s2.WindowStart = s1.WindowStart.In(loc)
	s2.WindowEnd = s1.WindowEnd.In(loc)
	if s1.SubjectID() != s2.SubjectID() {
		t.Fatalf("SubjectID changed across timezone representation of the same instant")
	}
}

func TestSubjectIDDiffersOnAnyFieldChange(t *testing.T) {
	base := mkScope()
	variants := []Scope{
		{InstrumentID: "ETH-USDT", VenueID: base.VenueID, Timeframe: base.Timeframe, WindowStart: base.WindowStart, WindowEnd: base.WindowEnd},
		{InstrumentID: base.InstrumentID, VenueID: "bybit-spot", Timeframe: base.Timeframe, WindowStart: base.WindowStart, WindowEnd: base.WindowEnd},
		{InstrumentID: base.InstrumentID, VenueID: base.VenueID, Timeframe: "5m", WindowStart: base.WindowStart, WindowEnd: base.WindowEnd},
		{InstrumentID: base.InstrumentID, VenueID: base.VenueID, Timeframe: base.Timeframe, WindowStart: base.WindowStart.Add(time.Minute), WindowEnd: base.WindowEnd},
		{InstrumentID: base.InstrumentID, VenueID: base.VenueID, Timeframe: base.Timeframe, WindowStart: base.WindowStart, WindowEnd: base.WindowEnd.Add(time.Minute)},
	}
	baseID := base.SubjectID()
	for i, v := range variants {
		if v.SubjectID() == baseID {
			t.Errorf("variant %d: expected different SubjectID when one scope field changes, got same %q", i, baseID)
		}
	}
}

func TestScopeEqual(t *testing.T) {
	a := mkScope()
	b := mkScope()
	if !a.Equal(b) {
		t.Fatalf("expected equal scopes to be Equal")
	}
	c := mkScope()
	c.Timeframe = "5m"
	if a.Equal(c) {
		t.Fatalf("expected different scopes to not be Equal")
	}
}

func TestCanTransition(t *testing.T) {
	allowed := map[[2]State]bool{
		{StateUnseen, StateProvisional}:      true,
		{StateUnseen, StateClosed}:           true, // historical/closed-only ingestion, candle.md §1
		{StateProvisional, StateProvisional}: true,
		{StateProvisional, StateClosed}:      true,
		{StateClosed, StateClosed}:           true, // correction self-transition, NOT terminal
	}
	states := []State{StateUnseen, StateProvisional, StateClosed}
	for _, from := range states {
		for _, to := range states {
			want := allowed[[2]State{from, to}]
			got := CanTransition(from, to)
			if got != want {
				t.Errorf("CanTransition(%s, %s) = %v, want %v", from, to, got, want)
			}
		}
	}
}

func TestCanTransitionRejectsClosedToProvisional(t *testing.T) {
	// terminal_states: [] does NOT mean CLOSED can go back to PROVISIONAL —
	// candle.md §1 is explicit that CLOSED never leaves CLOSED.
	if CanTransition(StateClosed, StateProvisional) {
		t.Fatalf("CLOSED -> PROVISIONAL must not be a valid transition")
	}
}

func TestStateString(t *testing.T) {
	cases := map[State]string{
		StateUnseen:      "UNSEEN",
		StateProvisional: "PROVISIONAL",
		StateClosed:      "CLOSED",
	}
	for state, want := range cases {
		if got := state.String(); got != want {
			t.Errorf("State(%d).String() = %q, want %q", state, got, want)
		}
	}
}
