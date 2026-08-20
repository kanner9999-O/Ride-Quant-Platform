package listing

import "testing"

// FuzzIsValidTransitionNeverPanicsAndRespectsTerminal is Go-native fuzz/
// property-style evidence (I-13, Chapter 13 §13.6) for instrument.md
// §10's TradableListing state machine: DELISTED is terminal (no outgoing
// transition), and no status validly transitions to itself. Exercises the
// real IsValidTransition directly, never a re-implementation of its
// rules.
func FuzzIsValidTransitionNeverPanicsAndRespectsTerminal(f *testing.F) {
	seeds := []string{StatusActive, StatusSuspended, StatusDelisted, "", "UNKNOWN"}
	for _, from := range seeds {
		for _, to := range seeds {
			f.Add(from, to)
		}
	}
	f.Fuzz(func(t *testing.T, from, to string) {
		got := IsValidTransition(from, to) // must not panic on any input
		if from == StatusDelisted && got {
			t.Fatalf("DELISTED must be terminal: IsValidTransition(DELISTED, %q) = true", to)
		}
		if from == to && got {
			t.Fatalf("self-transition must never be valid: IsValidTransition(%q, %q) = true", from, from)
		}
	})
}
