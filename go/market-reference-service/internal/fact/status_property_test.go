package fact_test

// I-13 property-based evidence (P3-MR-QG-A-MAJ-01 remediation, Chapter 13
// §13.6). Exercises the fold engine (internal/fact) against the three
// real, authoritative state machines it is applied to verbatim
// (instrument.md §1, venue.md §1, instrument.md §10) — never a
// re-implementation of their transition rules. External test package
// (fact_test) so it can import the sibling entity packages without an
// import cycle (they import fact; fact_test does not).

import (
	"fmt"
	"math/rand"
	"testing"
	"time"

	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/fact"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/instrument"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/listing"
	"github.com/kanner9999-O/Ride-Quant-Platform/go/market-reference-service/internal/venue"
)

var propertyBaseTime = time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)

func pt(offset int) time.Time { return propertyBaseTime.Add(time.Duration(offset) * time.Minute) }

func pref(id string) fact.Ref { return fact.Ref{StreamID: "prop", Sequence: 1, EventID: id} }

// stateMachine bundles one of the three real state machines this service
// implements, so every property below runs against all three identically.
type stateMachine struct {
	name    string
	initial string
	domain  []string
	valid   func(from, to string) bool
}

func stateMachines() []stateMachine {
	return []stateMachine{
		{
			name:    "instrument",
			initial: instrument.StatusRegistered,
			domain:  []string{instrument.StatusRegistered, instrument.StatusActive, instrument.StatusSuspended, instrument.StatusRetired},
			valid:   instrument.IsValidTransition,
		},
		{
			name:    "venue",
			initial: venue.StatusRegistered,
			domain:  []string{venue.StatusRegistered, venue.StatusActive, venue.StatusSuspended, venue.StatusRetired},
			valid:   venue.IsValidTransition,
		},
		{
			name:    "listing",
			initial: listing.StatusActive,
			domain:  []string{listing.StatusActive, listing.StatusSuspended, listing.StatusDelisted},
			valid:   listing.IsValidTransition,
		},
	}
}

// TestFoldStatusPropertySequentialOracleMatchesRealValidator: property —
// for any generated sequence of proposed statuses at strictly increasing
// effective times, FoldStatus must agree with sequentially applying the
// REAL IsValidTransition function step by step (stop at the first invalid
// step). This directly covers "illegal transitions never become valid":
// any generated sequence containing one is asserted to fail closed, not
// silently produce a resolved status.
func TestFoldStatusPropertySequentialOracleMatchesRealValidator(t *testing.T) {
	for _, m := range stateMachines() {
		m := m
		t.Run(m.name, func(t *testing.T) {
			rng := rand.New(rand.NewSource(1))
			for trial := 0; trial < 300; trial++ {
				n := 1 + rng.Intn(8)
				changes := make([]fact.StatusChange, n)
				current := m.initial
				oracleConflict := false
				for i := 0; i < n; i++ {
					proposed := m.domain[rng.Intn(len(m.domain))]
					changes[i] = fact.StatusChange{
						LineageFact:   fact.LineageFact{Ref: pref(fmt.Sprintf("%s-%d-%d", m.name, trial, i)), RecordedTime: pt(i)},
						EffectiveTime: pt(10 * (i + 1)),
						NewStatus:     proposed,
					}
					if oracleConflict {
						continue
					}
					if !m.valid(current, proposed) {
						oracleConflict = true
						continue
					}
					current = proposed
				}
				got := fact.FoldStatus(m.initial, changes, nil, pt(10*(n+1)), pt(n+1), m.valid)
				if oracleConflict {
					if !got.Conflict {
						t.Fatalf("trial %d: oracle found an invalid transition in %v (from %s), want Conflict=true, got %+v", trial, changes, m.initial, got)
					}
					continue
				}
				if got.Conflict {
					t.Fatalf("trial %d: oracle found only valid transitions in %v (from %s to %s), want Conflict=false, got Conflict=true", trial, changes, m.initial, current)
				}
				if got.CurrentStatus != current {
					t.Fatalf("trial %d: got CurrentStatus=%q, oracle wants %q (sequence %v)", trial, got.CurrentStatus, current, changes)
				}
			}
		})
	}
}

// TestFoldStatusPropertyOrderIndependence: property — FoldStatus's own doc
// contract says facts may be supplied "in any order"; shuffling the input
// slice must never change the result for the same cursors (same
// input/history + same cursor -> deterministic state).
func TestFoldStatusPropertyOrderIndependence(t *testing.T) {
	for _, m := range stateMachines() {
		m := m
		t.Run(m.name, func(t *testing.T) {
			rng := rand.New(rand.NewSource(2))
			for trial := 0; trial < 200; trial++ {
				n := 1 + rng.Intn(6)
				changes := make([]fact.StatusChange, n)
				for i := 0; i < n; i++ {
					changes[i] = fact.StatusChange{
						LineageFact:   fact.LineageFact{Ref: pref(fmt.Sprintf("oi-%s-%d-%d", m.name, trial, i)), RecordedTime: pt(i)},
						EffectiveTime: pt(10 * (i + 1)),
						NewStatus:     m.domain[rng.Intn(len(m.domain))],
					}
				}
				effectiveCursor, knowledgeCursor := pt(10*(n+1)), pt(n+1)
				want := fact.FoldStatus(m.initial, changes, nil, effectiveCursor, knowledgeCursor, m.valid)

				shuffled := append([]fact.StatusChange(nil), changes...)
				rng.Shuffle(len(shuffled), func(i, j int) { shuffled[i], shuffled[j] = shuffled[j], shuffled[i] })
				got := fact.FoldStatus(m.initial, shuffled, nil, effectiveCursor, knowledgeCursor, m.valid)

				if got != want {
					t.Fatalf("trial %d: input order changed the result — original %+v, shuffled %+v (input %v)", trial, want, got, changes)
				}
			}
		})
	}
}

// TestFoldStatusPropertyTerminalStatesHaveNoOutgoingTransition: property —
// terminal states cannot transition where prohibited. Checked against the
// real IsValidTransition, including malformed/unknown "to" values.
func TestFoldStatusPropertyTerminalStatesHaveNoOutgoingTransition(t *testing.T) {
	terminals := map[string]string{
		"instrument": instrument.StatusRetired,
		"venue":      venue.StatusRetired,
		"listing":    listing.StatusDelisted,
	}
	for _, m := range stateMachines() {
		m := m
		term := terminals[m.name]
		t.Run(m.name, func(t *testing.T) {
			candidates := append([]string{}, m.domain...)
			candidates = append(candidates, "", "UNKNOWN_STATUS", term+term)
			for _, to := range candidates {
				if m.valid(term, to) {
					t.Fatalf("terminal state %q must have no valid outgoing transition, but IsValidTransition(%q, %q) = true", term, term, to)
				}
			}
		})
	}
}

// TestFoldStatusPropertyFutureRecordedFactsNeverChangeEarlierReplay:
// property — correction/replay ordering preserves valid transition
// semantics. Generalizes the existing look-ahead example tests: adding
// ANY randomly generated fact recorded strictly after a knowledge cursor
// must never change that cursor's resolved result, regardless of the
// added fact's effective_time or proposed status.
func TestFoldStatusPropertyFutureRecordedFactsNeverChangeEarlierReplay(t *testing.T) {
	for _, m := range stateMachines() {
		m := m
		t.Run(m.name, func(t *testing.T) {
			rng := rand.New(rand.NewSource(3))
			for trial := 0; trial < 150; trial++ {
				n := 1 + rng.Intn(5)
				var base []fact.StatusChange
				for i := 0; i < n; i++ {
					base = append(base, fact.StatusChange{
						LineageFact:   fact.LineageFact{Ref: pref(fmt.Sprintf("la-%s-%d-%d", m.name, trial, i)), RecordedTime: pt(i)},
						EffectiveTime: pt(10 * (i + 1)),
						NewStatus:     m.domain[rng.Intn(len(m.domain))],
					})
				}
				knowledgeCursor := pt(n)
				effectiveCursor := pt(10 * (n + 5))
				before := fact.FoldStatus(m.initial, base, nil, effectiveCursor, knowledgeCursor, m.valid)

				extraCount := 1 + rng.Intn(3)
				withExtra := append([]fact.StatusChange(nil), base...)
				for j := 0; j < extraCount; j++ {
					withExtra = append(withExtra, fact.StatusChange{
						LineageFact:   fact.LineageFact{Ref: pref(fmt.Sprintf("la-extra-%s-%d-%d", m.name, trial, j)), RecordedTime: pt(n + 1 + j)},
						EffectiveTime: pt(rng.Intn(10 * (n + 10))),
						NewStatus:     m.domain[rng.Intn(len(m.domain))],
					})
				}
				after := fact.FoldStatus(m.initial, withExtra, nil, effectiveCursor, knowledgeCursor, m.valid)
				if after != before {
					t.Fatalf("trial %d: a fact recorded after the knowledge cursor leaked into an earlier replay — before=%+v after=%+v", trial, before, after)
				}
			}
		})
	}
}

// TestFoldStatusPropertySameEffectiveTimeConflictAlwaysFailsClosed:
// property — malformed/conflicting histories fail closed. Any two
// incompatible status proposals sharing an effective_time must always
// produce Conflict=true, never an arbitrary pick, across many random
// status-pair combinations.
func TestFoldStatusPropertySameEffectiveTimeConflictAlwaysFailsClosed(t *testing.T) {
	for _, m := range stateMachines() {
		m := m
		t.Run(m.name, func(t *testing.T) {
			rng := rand.New(rand.NewSource(4))
			for trial := 0; trial < 150; trial++ {
				et := pt(10)
				s1 := m.domain[rng.Intn(len(m.domain))]
				s2 := m.domain[rng.Intn(len(m.domain))]
				for s2 == s1 {
					s2 = m.domain[rng.Intn(len(m.domain))]
				}
				changes := []fact.StatusChange{
					{LineageFact: fact.LineageFact{Ref: pref(fmt.Sprintf("sc-%s-%d-a", m.name, trial)), RecordedTime: pt(1)}, EffectiveTime: et, NewStatus: s1},
					{LineageFact: fact.LineageFact{Ref: pref(fmt.Sprintf("sc-%s-%d-b", m.name, trial)), RecordedTime: pt(2)}, EffectiveTime: et, NewStatus: s2},
				}
				got := fact.FoldStatus(m.initial, changes, nil, pt(20), pt(100), m.valid)
				if !got.Conflict {
					t.Fatalf("trial %d: same-effective-time incompatible statuses (%q vs %q) must fail closed, got %+v", trial, s1, s2, got)
				}
			}
		})
	}
}

// TestResolveLineageHeadPropertyForkNeverSilentlyResolved: property —
// invariants hold across generated histories at the registration-lineage
// boundary (instrument.md §18 invariant 6). Any set of 2+ independent
// original facts (a genuine fork) must never resolve to a single silently
// chosen head.
func TestResolveLineageHeadPropertyForkNeverSilentlyResolved(t *testing.T) {
	rng := rand.New(rand.NewSource(5))
	for trial := 0; trial < 150; trial++ {
		n := 2 + rng.Intn(3)
		var facts []fact.LineageFact
		for i := 0; i < n; i++ {
			facts = append(facts, fact.LineageFact{Ref: pref(fmt.Sprintf("fork-%d-%d", trial, i)), RecordedTime: pt(i)})
		}
		got := fact.ResolveLineageHead(facts, nil, pt(100))
		if got.Valid {
			t.Fatalf("trial %d: %d independent original facts is a fork, must never resolve Valid=true (got %+v)", trial, n, got)
		}
		if got.PendingClass != fact.AwaitingSameSubjectReplacement {
			t.Fatalf("trial %d: fork must classify as AwaitingSameSubjectReplacement, got %+v", trial, got)
		}
	}
}

// TestResolveLineageHeadPropertySingleChainAlwaysResolvesToActualTerminus:
// property — a well-formed correction chain of any generated length must
// always resolve to its actual terminus (the one fact nothing else
// supersedes), never a fork classification and never any other fact.
func TestResolveLineageHeadPropertySingleChainAlwaysResolvesToActualTerminus(t *testing.T) {
	rng := rand.New(rand.NewSource(6))
	for trial := 0; trial < 150; trial++ {
		n := 1 + rng.Intn(4)
		var facts []fact.LineageFact
		var prev, terminus fact.Ref
		for i := 0; i < n; i++ {
			r := pref(fmt.Sprintf("chain-%d-%d", trial, i))
			facts = append(facts, fact.LineageFact{Ref: r, RecordedTime: pt(i), SupersedesRef: prev})
			prev, terminus = r, r
		}
		got := fact.ResolveLineageHead(facts, nil, pt(100))
		if !got.Valid || got.Head != terminus {
			t.Fatalf("trial %d: %d-link correction chain must resolve to its actual terminus %v, got %+v", trial, n, terminus, got)
		}
	}
}
