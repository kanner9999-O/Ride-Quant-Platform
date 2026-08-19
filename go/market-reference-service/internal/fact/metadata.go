package fact

import (
	"sort"
	"time"
)

// MetadataPatch is a single *MetadataRevised fact (Instrument/Venue/
// TradableListing all share this shape). It embeds LineageFact because an
// individual patch can itself be corrected via invalidate+replacement,
// forming its own mini-lineage scoped to its EffectiveTime (instrument.md
// §18: "Correction lineage scoped chính xác theo (subject_id,
// effective_time) — mỗi effective_time-slice có chuỗi lineage RIÊNG").
type MetadataPatch struct {
	LineageFact
	EffectiveTime time.Time
	ChangedFields map[string]string
	ClearFields   []string
}

// FoldMetadataResult is the outcome of folding a base field set through a
// sequence of patches.
type FoldMetadataResult struct {
	Fields       map[string]string
	PendingClass PendingCorrectionClass // set only if the chronologically-last effective_time group is itself pending correction (instrument.md §7 Bước 2)
}

// FoldMetadataPatches implements instrument.md §7 Bước 2
// (EXPLICIT_PATCH_WITH_CLEAR_SET, §17): fold base through patches ordered
// by effective_time, applying only patches visible at knowledgeCursor and
// eligible at effectiveCursor. base is not mutated.
func FoldMetadataPatches(base map[string]string, patches []MetadataPatch, invalidations []Invalidation, effectiveCursor, knowledgeCursor time.Time) FoldMetadataResult {
	type group struct {
		effectiveTime time.Time
		facts         []LineageFact
	}
	groupIndex := make(map[time.Time]int)
	var groups []group

	for _, p := range patches {
		if p.EffectiveTime.After(effectiveCursor) {
			continue
		}
		idx, ok := groupIndex[p.EffectiveTime]
		if !ok {
			idx = len(groups)
			groupIndex[p.EffectiveTime] = idx
			groups = append(groups, group{effectiveTime: p.EffectiveTime})
		}
		groups[idx].facts = append(groups[idx].facts, p.LineageFact)
	}
	sort.Slice(groups, func(i, j int) bool { return groups[i].effectiveTime.Before(groups[j].effectiveTime) })

	patchByRef := make(map[Ref]MetadataPatch, len(patches))
	for _, p := range patches {
		patchByRef[p.Ref] = p
	}

	fields := make(map[string]string, len(base))
	for k, v := range base {
		fields[k] = v
	}

	var lastPending PendingCorrectionClass
	for _, g := range groups {
		r := ResolveLineageHead(g.facts, invalidations, knowledgeCursor)
		if !r.Valid {
			lastPending = r.PendingClass // only matters if this is the last group overall
			continue
		}
		lastPending = PendingCorrectionNone
		patch := patchByRef[r.Head]
		for k, v := range patch.ChangedFields {
			fields[k] = v
		}
		for _, k := range patch.ClearFields {
			delete(fields, k)
		}
	}

	return FoldMetadataResult{Fields: fields, PendingClass: lastPending}
}
