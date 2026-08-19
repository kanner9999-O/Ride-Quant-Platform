package fact

import (
	"sort"
	"time"
)

// StatusChange is a single *StatusChanged fact (Instrument/Venue/
// TradableListing all share this shape). Like MetadataPatch, it embeds
// LineageFact because an individual status-change fact can itself be
// corrected via invalidate+replacement at the same effective_time
// (instrument.md §18).
type StatusChange struct {
	LineageFact
	EffectiveTime time.Time
	NewStatus     string
}

// FoldStatusResult is the outcome of the 5-phase status fold.
type FoldStatusResult struct {
	// CurrentStatus is the resolved status after folding all valid,
	// eligible, non-conflicting transitions. Empty if no transition
	// resolved (caller should use the entity's own initial status).
	CurrentStatus string
	// Conflict reports a same-effective-time incompatible-transition
	// conflict (instrument.md §7 Bước 3 Phase 5) — when true, CurrentStatus
	// is not meaningful and the caller must treat this as
	// PENDING_CORRECTION / AwaitingSameSubjectReplacement.
	Conflict bool
}

// FoldStatus implements instrument.md §7 Bước 3, `status_fold_order_policy:
// RECORDED_VISIBILITY_THEN_EFFECTIVE_ORDER` (§17) — applied identically to
// Instrument/Venue/TradableListing status. initialStatus is the entity's
// notional starting status (before any StatusChanged event — e.g.
// REGISTERED for Instrument, immediately after registration).
// isValidTransition implements the entity's own state machine (§1/§10).
func FoldStatus(initialStatus string, changes []StatusChange, invalidations []Invalidation, effectiveCursor, knowledgeCursor time.Time, isValidTransition func(from, to string) bool) FoldStatusResult {
	// Phase 1 (recorded visibility) is implicit: ResolveLineageHead only
	// considers facts/invalidations with RecordedTime <= knowledgeCursor.

	// Group raw status facts by effective_time — each effective_time slot
	// is its own correction lineage (instrument.md §18), exactly as for
	// metadata patches.
	type group struct {
		effectiveTime time.Time
		facts         []LineageFact
	}
	groupIndex := make(map[time.Time]int)
	var groups []group
	for _, c := range changes {
		idx, ok := groupIndex[c.EffectiveTime]
		if !ok {
			idx = len(groups)
			groupIndex[c.EffectiveTime] = idx
			groups = append(groups, group{effectiveTime: c.EffectiveTime})
		}
		groups[idx].facts = append(groups[idx].facts, c.LineageFact)
	}

	changeByRef := make(map[Ref]StatusChange, len(changes))
	for _, c := range changes {
		changeByRef[c.Ref] = c
	}

	// Phase 2 (lineage validity) + Phase 3 (effective eligibility): resolve
	// each group's valid head, keep only those eligible at effectiveCursor.
	type eligible struct {
		change StatusChange
	}
	var eligibleChanges []eligible
	for _, g := range groups {
		if g.effectiveTime.After(effectiveCursor) {
			continue // Phase 3: not yet eligible — future-effective, no look-ahead
		}
		// Use resolveLiveHeads (not ResolveLineageHead) deliberately: two
		// independent, non-superseding status facts sharing the same
		// effective_time are a valid Phase 5 same-effective-time conflict
		// scenario (instrument.md §7 Bước 3 Phase 5), not a lineage fork —
		// both must survive into the candidate pool below so the conflict
		// check can see them.
		for _, h := range resolveLiveHeads(g.facts, invalidations, knowledgeCursor) {
			if h.pending {
				continue // pending correction at this slot — excluded from fold, same as instrument.md §7 Bước 2 treatment
			}
			eligibleChanges = append(eligibleChanges, eligible{change: changeByRef[h.ref]})
		}
	}

	// Phase 4: total deterministic ordering — effective_time ASC,
	// recorded_time ASC, event_id ASC (never raw cross-stream sequence).
	sort.Slice(eligibleChanges, func(i, j int) bool {
		a, b := eligibleChanges[i].change, eligibleChanges[j].change
		if !a.EffectiveTime.Equal(b.EffectiveTime) {
			return a.EffectiveTime.Before(b.EffectiveTime)
		}
		if !a.RecordedTime.Equal(b.RecordedTime) {
			return a.RecordedTime.Before(b.RecordedTime)
		}
		return a.Ref.EventID < b.Ref.EventID
	})

	// Phase 5: transition validation, with same-effective-time incompatible
	// transition detection.
	current := initialStatus
	for i := 0; i < len(eligibleChanges); i++ {
		c := eligibleChanges[i].change
		// Detect a same-effective-time conflict: another eligible change at
		// the exact same effective_time proposing a different new_status.
		for j := i + 1; j < len(eligibleChanges) && eligibleChanges[j].change.EffectiveTime.Equal(c.EffectiveTime); j++ {
			if eligibleChanges[j].change.NewStatus != c.NewStatus {
				return FoldStatusResult{Conflict: true}
			}
		}
		if !isValidTransition(current, c.NewStatus) {
			// An invalid transition in an otherwise well-formed history is
			// itself an integrity condition this engine surfaces as a
			// conflict rather than silently ignoring or crashing.
			return FoldStatusResult{Conflict: true}
		}
		current = c.NewStatus
	}

	return FoldStatusResult{CurrentStatus: current}
}
