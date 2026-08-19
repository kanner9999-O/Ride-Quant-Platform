// Package fact implements the bitemporal fold algorithms instrument.md
// pins once and applies verbatim to Instrument (§1-§9), Venue (venue.md
// §1-§9, "áp dụng nguyên văn theo instrument.md"), and TradableListing
// (§10-§15 Bước 1-3): registration/creation lineage-head resolution
// (§7 Bước 1 / §18), the EXPLICIT_PATCH_WITH_CLEAR_SET metadata patch fold
// (§7 Bước 2 / §17), and the RECORDED_VISIBILITY_THEN_EFFECTIVE_ORDER
// 5-phase status fold (§7 Bước 3 / §17).
//
// Every query into this engine takes the two independent bitemporal axes
// ADR-032 §B.3 requires: an effective-applicability instant and a
// knowledge-visibility (recorded_time) cursor. Corrections recorded after
// the supplied knowledge cursor are invisible to that query, regardless of
// their effective_time (instrument.md §20 — "Historical Replay PHẢI dùng
// đúng metadata có hiệu lực TẠI computation cursor... Selection algorithm:
// latest valid fact với effective_time <= cursor VÀ recorded_time <=
// replay cursor").
package fact

import (
	"sort"
	"time"
)

// Ref is the canonical event-record reference (Chapter 8 §8.2.3), kept
// independent of the envelope package's domain-specific fields so this
// engine has no dependency beyond the standard library.
type Ref struct {
	StreamID string
	Sequence int64
	EventID  string
}

// IsZero reports whether r is the zero value (no reference).
func (r Ref) IsZero() bool {
	return r == Ref{}
}

// CorrectionClass mirrors instrument.md §19's initial_fact_correction_class
// — only meaningful when an invalidation targets a registration/creation
// fact (the lineage's original/replacement chain), never a metadata-patch
// or status-change fact (§19: those are always same-subject, i.e.
// AwaitingSameSubjectReplacement).
type CorrectionClass int

const (
	// CorrectionClassNone: the invalidation does not carry a class (valid
	// only when targeting a metadata-patch or status-change fact).
	CorrectionClassNone CorrectionClass = iota
	// CorrectionClassMetadataError: same-scope error — a replacement under
	// the same subject is expected (instrument.md §19).
	CorrectionClassMetadataError
	// CorrectionClassScopeError: scope/identity error — no replacement is
	// permitted under the old subject; a new subject must be registered
	// (instrument.md §19).
	CorrectionClassScopeError
)

// PendingCorrectionClass mirrors instrument.md §19's pending_correction_class
// — the Current-View-facing discriminator derived from CorrectionClass.
type PendingCorrectionClass int

const (
	PendingCorrectionNone PendingCorrectionClass = iota
	// AwaitingSameSubjectReplacement: temporary — a future cursor (once the
	// replacement becomes visible) resolves back to VALID.
	AwaitingSameSubjectReplacement
	// TerminalScopeInvalidation: permanent — no cursor ever resolves this
	// subject back to VALID (instrument.md §19).
	TerminalScopeInvalidation
)

// LineageFact is any fact that can participate in the append-only
// correction-lineage pattern (instrument.md §18): an original fact
// (SupersedesRef zero) or a replacement (SupersedesRef pointing at the
// fact it replaces, always the current lineage head at append time,
// instrument.md §18 invariants 3-5).
type LineageFact struct {
	Ref           Ref
	RecordedTime  time.Time
	SupersedesRef Ref // zero value = original fact, no supersedes
}

// Invalidation is a *FactInvalidated event targeting some fact in this
// lineage (instrument.md §6/§18).
type Invalidation struct {
	Ref             Ref
	RecordedTime    time.Time
	InvalidatedRef  Ref
	CorrectionClass CorrectionClass // meaningful only when InvalidatedRef is a registration/creation fact
}

// LineageResult is the outcome of resolving a lineage head at a knowledge
// (recorded_time) cursor.
type LineageResult struct {
	// Head is the resolved lineage-head fact's reference. Zero when no
	// fact is visible yet, or when PendingClass == TerminalScopeInvalidation
	// (no valid head — instrument.md §19: "subject cũ KHÔNG được tiếp tục
	// authoritative").
	Head Ref
	// Valid reports whether Head resolves to a usable, non-pending fact.
	Valid bool
	// PendingClass is set when the lineage head is currently invalidated
	// with no visible replacement (instrument.md §19).
	PendingClass PendingCorrectionClass
}

// ResolveLineageHead implements instrument.md §7 Bước 1 (registration
// lineage) and, by the same construction, §18's general lineage-head rule
// — applied identically to Instrument registration, Venue registration,
// and TradableListing creation.
//
// facts and invalidations are the fact family's complete history (any
// order); knowledgeCursor is the recorded_time visibility boundary (ADR-032
// §B.3.b). Only facts/invalidations with RecordedTime <= knowledgeCursor
// participate — this is the sole mechanism that prevents a correction
// recorded after the cursor from leaking backward into an earlier query
// (ADR-032 §B.3: "corrections recorded later MUST NOT leak into earlier
// Replay").
func ResolveLineageHead(facts []LineageFact, invalidations []Invalidation, knowledgeCursor time.Time) LineageResult {
	heads := resolveLiveHeads(facts, invalidations, knowledgeCursor)
	switch len(heads) {
	case 0:
		return LineageResult{}
	case 1:
		return headResult(heads[0])
	default:
		// instrument.md §18 invariant 6 violated (fork) — fail closed
		// (Constitution I-6) rather than silently pick one. Status folding
		// (status.go) intentionally does NOT go through this function for
		// exactly this reason: independent same-effective-time status
		// facts are a valid Phase 5 conflict scenario, not a lineage fork.
		return LineageResult{PendingClass: AwaitingSameSubjectReplacement}
	}
}

// liveHead is a resolved, currently-live chain terminus within a single
// correction lineage — either a usable fact or a pending (invalidated,
// not-yet-replaced) one.
type liveHead struct {
	ref          Ref
	pending      bool
	pendingClass PendingCorrectionClass
}

func headResult(h liveHead) LineageResult {
	if h.pending {
		return LineageResult{PendingClass: h.pendingClass}
	}
	return LineageResult{Head: h.ref, Valid: true}
}

// resolveLiveHeads finds every visible fact that nothing else visible
// supersedes (i.e. every independent chain terminus), resolving each
// terminus's own pending/invalidated state. In a single well-formed
// lineage this returns at most one entry; status folding calls this
// directly to detect the multi-head case itself (Phase 5 same-effective-
// time conflict) rather than having it collapsed here.
func resolveLiveHeads(facts []LineageFact, invalidations []Invalidation, knowledgeCursor time.Time) []liveHead {
	visibleFacts := make(map[Ref]LineageFact)
	for _, f := range facts {
		if !f.RecordedTime.After(knowledgeCursor) {
			visibleFacts[f.Ref] = f
		}
	}
	if len(visibleFacts) == 0 {
		return nil
	}

	invalidatedBy := make(map[Ref]Invalidation) // invalidated fact ref -> its invalidation
	replacementOf := make(map[Ref]Ref)          // superseded ref -> replacement ref
	for _, inv := range invalidations {
		if inv.RecordedTime.After(knowledgeCursor) {
			continue
		}
		invalidatedBy[inv.InvalidatedRef] = inv
	}
	for ref, f := range visibleFacts {
		if !f.SupersedesRef.IsZero() {
			replacementOf[f.SupersedesRef] = ref
		}
	}

	// Iterate refs in a deterministic order (map iteration order is not) so
	// results are stable across runs.
	refs := make([]Ref, 0, len(visibleFacts))
	for ref := range visibleFacts {
		refs = append(refs, ref)
	}
	sort.Slice(refs, func(i, j int) bool {
		if refs[i].StreamID != refs[j].StreamID {
			return refs[i].StreamID < refs[j].StreamID
		}
		return refs[i].Sequence < refs[j].Sequence
	})

	var heads []liveHead
	for _, ref := range refs {
		if _, superseded := replacementOf[ref]; superseded {
			continue
		}
		inv, isInvalidated := invalidatedBy[ref]
		if !isInvalidated {
			heads = append(heads, liveHead{ref: ref})
			continue
		}
		class := AwaitingSameSubjectReplacement
		if inv.CorrectionClass == CorrectionClassScopeError {
			class = TerminalScopeInvalidation
		}
		heads = append(heads, liveHead{ref: ref, pending: true, pendingClass: class})
	}
	return heads
}
