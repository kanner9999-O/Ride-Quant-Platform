package fact

import "time"

// ViewState mirrors instrument.md §7's two-value view_state.
type ViewState int

const (
	ViewValid ViewState = iota
	ViewPendingCorrection
)

// ResolveInput bundles one subject's complete fact family for the
// three-step Current View fold shared verbatim by Instrument (§7),
// Venue (venue.md §7, "áp dụng nguyên văn"), and TradableListing
// (§15 Bước 1-3).
type ResolveInput struct {
	RegistrationFacts         []LineageFact
	RegistrationInvalidations []Invalidation

	MetadataBase          map[string]string
	MetadataPatches       []MetadataPatch
	MetadataInvalidations []Invalidation

	StatusChanges       []StatusChange
	StatusInvalidations []Invalidation
	InitialStatus       string
	IsValidTransition   func(from, to string) bool

	EffectiveCursor time.Time
	KnowledgeCursor time.Time
}

// ResolveOutput is the resolved Current View state.
type ResolveOutput struct {
	ViewState        ViewState
	PendingClass     PendingCorrectionClass
	RegistrationHead Ref
	Fields           map[string]string
	CurrentStatus    string
}

// Resolve implements instrument.md §7 Bước 1-3 (registration lineage head
// -> metadata patch fold -> status fold), applied identically to
// Instrument, Venue, and TradableListing's own three-step prefix (§15).
func Resolve(in ResolveInput) ResolveOutput {
	reg := ResolveLineageHead(in.RegistrationFacts, in.RegistrationInvalidations, in.KnowledgeCursor)
	if !reg.Valid {
		return ResolveOutput{ViewState: ViewPendingCorrection, PendingClass: reg.PendingClass}
	}

	meta := FoldMetadataPatches(in.MetadataBase, in.MetadataPatches, in.MetadataInvalidations, in.EffectiveCursor, in.KnowledgeCursor)
	if meta.PendingClass != PendingCorrectionNone {
		// instrument.md §7 Bước 2: the most-recent-by-effective_time patch
		// being pending makes the overall view PENDING_CORRECTION, same as
		// a registration-lineage pending state.
		return ResolveOutput{ViewState: ViewPendingCorrection, PendingClass: meta.PendingClass, RegistrationHead: reg.Head, Fields: meta.Fields}
	}

	status := FoldStatus(in.InitialStatus, in.StatusChanges, in.StatusInvalidations, in.EffectiveCursor, in.KnowledgeCursor, in.IsValidTransition)
	if status.Conflict {
		// instrument.md §7 Bước 3 Phase 5: same-effective-time incompatible
		// transitions are AwaitingSameSubjectReplacement (never terminal —
		// a corrected/disambiguating status fact can still resolve it).
		return ResolveOutput{ViewState: ViewPendingCorrection, PendingClass: AwaitingSameSubjectReplacement, RegistrationHead: reg.Head, Fields: meta.Fields}
	}

	return ResolveOutput{
		ViewState:        ViewValid,
		RegistrationHead: reg.Head,
		Fields:           meta.Fields,
		CurrentStatus:    status.CurrentStatus,
	}
}
