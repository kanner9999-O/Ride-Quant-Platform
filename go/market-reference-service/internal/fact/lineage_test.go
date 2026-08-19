package fact

import (
	"testing"
	"time"
)

func t0(offset int) time.Time {
	return time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC).Add(time.Duration(offset) * time.Minute)
}

func ref(id string) Ref { return Ref{StreamID: "s", Sequence: 1, EventID: id} }

func TestResolveLineageHeadOriginalOnly(t *testing.T) {
	facts := []LineageFact{{Ref: ref("f1"), RecordedTime: t0(0)}}
	r := ResolveLineageHead(facts, nil, t0(10))
	if !r.Valid || r.Head != ref("f1") {
		t.Fatalf("got %+v, want valid head f1", r)
	}
}

func TestResolveLineageHeadNotYetVisible(t *testing.T) {
	facts := []LineageFact{{Ref: ref("f1"), RecordedTime: t0(10)}}
	r := ResolveLineageHead(facts, nil, t0(5)) // cursor before recorded_time
	if r.Valid {
		t.Fatalf("got %+v, want not visible yet", r)
	}
}

func TestResolveLineageHeadMetadataErrorReplacement(t *testing.T) {
	original := LineageFact{Ref: ref("f1"), RecordedTime: t0(0)}
	inv := Invalidation{Ref: ref("inv1"), RecordedTime: t0(5), InvalidatedRef: ref("f1"), CorrectionClass: CorrectionClassMetadataError}
	replacement := LineageFact{Ref: ref("f2"), RecordedTime: t0(6), SupersedesRef: ref("f1")}

	// Before invalidation: original still valid.
	r1 := ResolveLineageHead([]LineageFact{original}, nil, t0(3))
	if !r1.Valid || r1.Head != ref("f1") {
		t.Fatalf("before invalidation: got %+v, want valid f1", r1)
	}

	// After invalidation, before replacement visible: pending, awaiting same-subject replacement.
	r2 := ResolveLineageHead([]LineageFact{original}, []Invalidation{inv}, t0(5))
	if r2.Valid || r2.PendingClass != AwaitingSameSubjectReplacement {
		t.Fatalf("after invalidation: got %+v, want pending AwaitingSameSubjectReplacement", r2)
	}

	// After replacement visible: valid again, head is the replacement.
	r3 := ResolveLineageHead([]LineageFact{original, replacement}, []Invalidation{inv}, t0(6))
	if !r3.Valid || r3.Head != ref("f2") {
		t.Fatalf("after replacement: got %+v, want valid f2", r3)
	}
}

func TestResolveLineageHeadScopeErrorTerminal(t *testing.T) {
	original := LineageFact{Ref: ref("f1"), RecordedTime: t0(0)}
	inv := Invalidation{Ref: ref("inv1"), RecordedTime: t0(5), InvalidatedRef: ref("f1"), CorrectionClass: CorrectionClassScopeError}

	r := ResolveLineageHead([]LineageFact{original}, []Invalidation{inv}, t0(100))
	if r.Valid || r.PendingClass != TerminalScopeInvalidation {
		t.Fatalf("got %+v, want permanently TerminalScopeInvalidation", r)
	}
}

func TestResolveLineageHeadNoFactsYet(t *testing.T) {
	r := ResolveLineageHead(nil, nil, t0(100))
	if r.Valid || r.PendingClass != PendingCorrectionNone {
		t.Fatalf("got %+v, want zero result (no facts yet, not pending)", r)
	}
}

func TestResolveLineageHeadCorrectionRecordedLaterInvisibleToEarlierCursor(t *testing.T) {
	// ADR-032 look-ahead guard: a correction recorded later must not leak
	// into a query with an earlier knowledge cursor.
	original := LineageFact{Ref: ref("f1"), RecordedTime: t0(0)}
	inv := Invalidation{Ref: ref("inv1"), RecordedTime: t0(50), InvalidatedRef: ref("f1"), CorrectionClass: CorrectionClassMetadataError}
	replacement := LineageFact{Ref: ref("f2"), RecordedTime: t0(51), SupersedesRef: ref("f1")}

	// Query with knowledge cursor BEFORE the correction was recorded must
	// still see the original as valid.
	r := ResolveLineageHead([]LineageFact{original, replacement}, []Invalidation{inv}, t0(10))
	if !r.Valid || r.Head != ref("f1") {
		t.Fatalf("got %+v, want original f1 still valid at cursor before correction recorded_time", r)
	}
}
