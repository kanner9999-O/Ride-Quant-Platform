package fact

import (
	"testing"
)

func instrumentTransitions(from, to string) bool {
	allowed := map[[2]string]bool{
		{"REGISTERED", "ACTIVE"}:  true,
		{"ACTIVE", "SUSPENDED"}:   true,
		{"SUSPENDED", "ACTIVE"}:   true,
		{"ACTIVE", "RETIRED"}:     true,
		{"SUSPENDED", "RETIRED"}:  true,
		{"REGISTERED", "RETIRED"}: true,
	}
	return allowed[[2]string{from, to}]
}

func TestFoldStatusSequentialTransitions(t *testing.T) {
	changes := []StatusChange{
		{LineageFact: LineageFact{Ref: ref("s1"), RecordedTime: t0(1)}, EffectiveTime: t0(10), NewStatus: "ACTIVE"},
		{LineageFact: LineageFact{Ref: ref("s2"), RecordedTime: t0(2)}, EffectiveTime: t0(20), NewStatus: "SUSPENDED"},
	}
	r := FoldStatus("REGISTERED", changes, nil, t0(30), t0(100), instrumentTransitions)
	if r.Conflict {
		t.Fatalf("unexpected conflict: %+v", r)
	}
	if r.CurrentStatus != "SUSPENDED" {
		t.Fatalf("got %q, want SUSPENDED", r.CurrentStatus)
	}
}

func TestFoldStatusEffectiveCursorLimitsVisibility(t *testing.T) {
	changes := []StatusChange{
		{LineageFact: LineageFact{Ref: ref("s1"), RecordedTime: t0(1)}, EffectiveTime: t0(10), NewStatus: "ACTIVE"},
	}
	r := FoldStatus("REGISTERED", changes, nil, t0(5), t0(100), instrumentTransitions) // effective cursor before the change
	if r.CurrentStatus != "REGISTERED" {
		t.Fatalf("got %q, want REGISTERED (status change not yet effective)", r.CurrentStatus)
	}
}

func TestFoldStatusFutureRecordedButNotYetEffectiveDoesNotLeak(t *testing.T) {
	// "Future-effective status event ĐÃ recorded (Phase 1 visible) nhưng
	// effective_time > cursor hiện tại (Phase 3 chưa eligible) KHÔNG ảnh
	// hưởng current_status tại cursor đó" — instrument.md §7 Bước 3.
	changes := []StatusChange{
		{LineageFact: LineageFact{Ref: ref("s1"), RecordedTime: t0(1)}, EffectiveTime: t0(10), NewStatus: "ACTIVE"},
		{LineageFact: LineageFact{Ref: ref("s2"), RecordedTime: t0(2)}, EffectiveTime: t0(9999), NewStatus: "RETIRED"}, // recorded already, effective far in the future
	}
	r := FoldStatus("REGISTERED", changes, nil, t0(50), t0(100), instrumentTransitions)
	if r.CurrentStatus != "ACTIVE" {
		t.Fatalf("got %q, want ACTIVE (future-effective RETIRED must not leak backward)", r.CurrentStatus)
	}
}

func TestFoldStatusKnowledgeCursorHidesUnrecordedChange(t *testing.T) {
	changes := []StatusChange{
		{LineageFact: LineageFact{Ref: ref("s1"), RecordedTime: t0(50)}, EffectiveTime: t0(10), NewStatus: "ACTIVE"},
	}
	r := FoldStatus("REGISTERED", changes, nil, t0(100), t0(20), instrumentTransitions) // knowledge cursor before recorded_time
	if r.CurrentStatus != "REGISTERED" {
		t.Fatalf("got %q, want REGISTERED (change not yet recorded/visible at knowledge cursor)", r.CurrentStatus)
	}
}

func TestFoldStatusSameEffectiveTimeConflict(t *testing.T) {
	changes := []StatusChange{
		{LineageFact: LineageFact{Ref: ref("s1"), RecordedTime: t0(1)}, EffectiveTime: t0(10), NewStatus: "ACTIVE"},
		{LineageFact: LineageFact{Ref: ref("s2"), RecordedTime: t0(2)}, EffectiveTime: t0(10), NewStatus: "RETIRED"}, // same effective_time, incompatible
	}
	r := FoldStatus("REGISTERED", changes, nil, t0(20), t0(100), instrumentTransitions)
	if !r.Conflict {
		t.Fatalf("got %+v, want Conflict=true for same-effective-time incompatible transitions", r)
	}
}

func TestFoldStatusCorrectionRecordedLaterInvisibleToEarlierReplay(t *testing.T) {
	// ADR-032 look-ahead guard applied to status.
	original := StatusChange{LineageFact: LineageFact{Ref: ref("s1"), RecordedTime: t0(1)}, EffectiveTime: t0(10), NewStatus: "ACTIVE"}
	inv := Invalidation{Ref: ref("inv1"), RecordedTime: t0(90), InvalidatedRef: ref("s1"), CorrectionClass: CorrectionClassNone}
	// REGISTERED -> RETIRED is a valid direct transition (unlike SUSPENDED,
	// which requires having been ACTIVE first) — chosen so this test
	// isolates look-ahead behavior, not state-machine validity.
	replacement := StatusChange{LineageFact: LineageFact{Ref: ref("s2"), RecordedTime: t0(91), SupersedesRef: ref("s1")}, EffectiveTime: t0(10), NewStatus: "RETIRED"}

	// Early replay (knowledge cursor before the correction) sees the
	// original transition.
	r := FoldStatus("REGISTERED", []StatusChange{original, replacement}, []Invalidation{inv}, t0(50), t0(50), instrumentTransitions)
	if r.CurrentStatus != "ACTIVE" {
		t.Fatalf("got %q, want ACTIVE (correction recorded later must not leak into earlier replay)", r.CurrentStatus)
	}

	// Later replay (knowledge cursor after the correction) sees the
	// corrected transition.
	r2 := FoldStatus("REGISTERED", []StatusChange{original, replacement}, []Invalidation{inv}, t0(50), t0(200), instrumentTransitions)
	if r2.CurrentStatus != "RETIRED" {
		t.Fatalf("got %q, want RETIRED (correction visible after its recorded_time)", r2.CurrentStatus)
	}
}
