package fact

import (
	"testing"
)

func TestFoldMetadataPatchesAppliesInEffectiveOrder(t *testing.T) {
	base := map[string]string{"display_name": "Original"}
	patches := []MetadataPatch{
		{LineageFact: LineageFact{Ref: ref("p1"), RecordedTime: t0(1)}, EffectiveTime: t0(10), ChangedFields: map[string]string{"display_name": "Renamed"}},
		{LineageFact: LineageFact{Ref: ref("p2"), RecordedTime: t0(2)}, EffectiveTime: t0(20), ChangedFields: map[string]string{"display_name": "Renamed Again"}},
	}

	// Cursor before any patch is effective: base value.
	r0 := FoldMetadataPatches(base, patches, nil, t0(5), t0(100))
	if r0.Fields["display_name"] != "Original" {
		t.Fatalf("got %q, want Original", r0.Fields["display_name"])
	}

	// Cursor after first patch only.
	r1 := FoldMetadataPatches(base, patches, nil, t0(15), t0(100))
	if r1.Fields["display_name"] != "Renamed" {
		t.Fatalf("got %q, want Renamed", r1.Fields["display_name"])
	}

	// Cursor after both patches.
	r2 := FoldMetadataPatches(base, patches, nil, t0(25), t0(100))
	if r2.Fields["display_name"] != "Renamed Again" {
		t.Fatalf("got %q, want Renamed Again", r2.Fields["display_name"])
	}
}

func TestFoldMetadataPatchesClearField(t *testing.T) {
	base := map[string]string{"display_name": "X"}
	patches := []MetadataPatch{
		{LineageFact: LineageFact{Ref: ref("p1"), RecordedTime: t0(1)}, EffectiveTime: t0(10), ClearFields: []string{"display_name"}},
	}
	r := FoldMetadataPatches(base, patches, nil, t0(20), t0(100))
	if _, present := r.Fields["display_name"]; present {
		t.Fatalf("expected display_name cleared, got %q", r.Fields["display_name"])
	}
}

func TestFoldMetadataPatchesHistoricalReplayUsesEffectiveValueNotCurrent(t *testing.T) {
	// instrument.md §20: historical replay must use the value effective AT
	// the cursor, not the latest value.
	base := map[string]string{"price_increment": "0.01"}
	patches := []MetadataPatch{
		{LineageFact: LineageFact{Ref: ref("p1"), RecordedTime: t0(1)}, EffectiveTime: t0(10), ChangedFields: map[string]string{"price_increment": "0.001"}},
	}
	r := FoldMetadataPatches(base, patches, nil, t0(5), t0(100)) // effective cursor BEFORE the patch's effective_time
	if r.Fields["price_increment"] != "0.01" {
		t.Fatalf("got %q, want historical value 0.01 (patch not yet effective at cursor)", r.Fields["price_increment"])
	}
}

func TestFoldMetadataPatchesPendingCorrectionOnlyWhenMostRecent(t *testing.T) {
	base := map[string]string{"x": "base"}
	pendingInv := Invalidation{Ref: ref("inv1"), RecordedTime: t0(15), InvalidatedRef: ref("p1"), CorrectionClass: CorrectionClassMetadataError}
	patches := []MetadataPatch{
		{LineageFact: LineageFact{Ref: ref("p1"), RecordedTime: t0(1)}, EffectiveTime: t0(10), ChangedFields: map[string]string{"x": "v10"}},
	}
	// The only patch is now pending (invalidated, no replacement) and IS
	// the most recent -> PendingClass should be set.
	r := FoldMetadataPatches(base, patches, []Invalidation{pendingInv}, t0(50), t0(20))
	if r.PendingClass != AwaitingSameSubjectReplacement {
		t.Fatalf("got PendingClass=%v, want AwaitingSameSubjectReplacement", r.PendingClass)
	}
	if r.Fields["x"] != "base" {
		t.Fatalf("got x=%q, want base value retained (pending patch not applied)", r.Fields["x"])
	}
}

func TestFoldMetadataPatchesPendingNotMostRecentDoesNotSetPendingClass(t *testing.T) {
	base := map[string]string{"x": "base"}
	pendingInv := Invalidation{Ref: ref("inv1"), RecordedTime: t0(15), InvalidatedRef: ref("p1"), CorrectionClass: CorrectionClassMetadataError}
	patches := []MetadataPatch{
		{LineageFact: LineageFact{Ref: ref("p1"), RecordedTime: t0(1)}, EffectiveTime: t0(10), ChangedFields: map[string]string{"x": "v10"}},
		{LineageFact: LineageFact{Ref: ref("p2"), RecordedTime: t0(2)}, EffectiveTime: t0(30), ChangedFields: map[string]string{"x": "v30"}},
	}
	r := FoldMetadataPatches(base, patches, []Invalidation{pendingInv}, t0(50), t0(20))
	if r.PendingClass != PendingCorrectionNone {
		t.Fatalf("got PendingClass=%v, want None (a later valid patch exists)", r.PendingClass)
	}
	if r.Fields["x"] != "v30" {
		t.Fatalf("got x=%q, want v30 (later valid patch applied)", r.Fields["x"])
	}
}
