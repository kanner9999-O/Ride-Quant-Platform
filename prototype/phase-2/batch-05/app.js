/*
 * Ride — Phase 2 Prototype — Batch 05 (Review / causation / historical comparison / correction
 * inspection).
 *
 * Illustrative, non-authoritative UI logic only. No real backend, no real exchange integration,
 * no real credentials, no signing/custody, no authoritative financial computation. Every
 * displayed value below is mock/static/deterministic. This is a separate, self-contained page
 * from Batch 01/02/03/04 — it does NOT share live JS state with any of them.
 *
 * INV-1 (read-only, critical): NAV-005/SCR-008/SCR-009/VIEW-004 are read-only inspection only.
 * There is no create/overwrite/correct/invalidate/promote/"apply correction"/"accept
 * replacement"/"save reconstructed state" action anywhere in this file — verify directly: no
 * function below mutates any MOCK_* fixture, only `state.*` (prototype-local UI selection state).
 *
 * Correction-lineage scope (explicit, per task boundary — "do not invent a generic universal
 * correction schema"): the ONE interactive correction fixture in this batch
 * (MOCK_DECISION_CORRECTION) uses Decision's own exact vocabulary (decision.md §6
 * DecisionFactInvalidated: invalidated_fact_ref/invalidation_reason; DecisionRecorded's own
 * supersedes_fact_ref, direct-predecessor-fact-targeting). RiskEvaluation and Fill share this
 * same direct pattern (risk.md, fill.md) but are not separately fixtured here. ExecutionResult's
 * correction lineage is materially different/more complex (execution-result.md §2 —
 * ExecutionResultComputation with computation_purpose=CORRECTION + predecessor_execution_result_
 * ref + correction_authorization_ref, THEN a new ExecutionResultRecorded) and is NOT modeled
 * interactively here — see the hint text on VIEW-004. PaperExecutionObservation and Position have
 * no correction lineage of their own (execution-result.md §11, position.md §1) and none is
 * invented.
 *
 * Traceability for every element rendered here is pinned in traceability.md — this file does not
 * introduce any UC/PR/domain concept that is not already Consolidated Stable in
 * docs/product/ux-blueprint.md, docs/product/use-case-workflow.md, or docs/domain/*.md.
 */

(function () {
  "use strict";

  // ---- Mock data (illustrative only, not authoritative financial data) ----

  var MOCK_ACCOUNT_CONTEXT = {
    account: "Ride Internal Account",
    instrument: "BTC/USDT",
    venue: "Binance"
  };

  var MOCK_STRATEGY_CONTEXT = {
    instanceId: "inst-a",
    instanceLabel: "Instance A",
    strategyDefinitionVersion: "sdv-v1.0",
    configurationVersion: "cfg-v3"
  };

  // ---- SCR-008 lineage fixtures (UC-016) ----
  //
  // UC-016's Main flow names an EXACT causation chain: Fill -> ExecutionResult -> Order ->
  // Execution Intent -> RiskEvaluation -> Trade Intent -> Decision gốc. This batch renders
  // exactly those seven links (no OrderSubmissionRequest/ExecutionResultComputation/
  // PaperExecutionObservation nodes are added here — that would be scope beyond what UC-016
  // itself enumerates; those entities are Batch 04's concern, not re-litigated here). Two
  // genuinely distinct, already-existing, already-recorded lineages (LONG and SHORT) are
  // selectable so the trace is materially inspectable in both directions, not just a label.
  var LINEAGE_FILLS = {
    "FILL-RV-A-001": {
      fill: { id: "FILL-RV-A-001", direction: "LONG", quantity: "0.50", quantityUnit: "BTC", price: "65000.00", priceCurrency: "USDT" },
      executionResult: { id: "ER-RV-A-001", resultType: "EXECUTED" },
      order: { id: "ORD-RV-A-001", environment: "PAPER" },
      executionIntent: { id: "EI-RV-A-001", status: "ISSUED" },
      riskEvaluation: { id: "RE-RV-A-001", result: "APPROVED" },
      tradeIntent: { id: "TI-RV-A-001" },
      decision: {
        id: "PD-RV-A-001",
        outcome: "LONG",
        strategyInstance: MOCK_STRATEGY_CONTEXT.instanceLabel + " (" + MOCK_STRATEGY_CONTEXT.instanceId + ")",
        strategyDefinitionVersion: MOCK_STRATEGY_CONTEXT.strategyDefinitionVersion,
        configurationVersion: MOCK_STRATEGY_CONTEXT.configurationVersion,
        inputSnapshot: "price_fact#7710, reference_fact#7709 (illustrative)",
        evaluationEvidence: "current candle closed strictly above EMA(20); previous candle ≤ previous EMA(20) (crossing_policy=strict)"
      }
    },
    "FILL-RV-B-001": {
      fill: { id: "FILL-RV-B-001", direction: "SHORT", quantity: "0.35", quantityUnit: "BTC", price: "64200.00", priceCurrency: "USDT" },
      executionResult: { id: "ER-RV-B-001", resultType: "EXECUTED" },
      order: { id: "ORD-RV-B-001", environment: "PAPER" },
      executionIntent: { id: "EI-RV-B-001", status: "ISSUED" },
      riskEvaluation: { id: "RE-RV-B-001", result: "APPROVED" },
      tradeIntent: { id: "TI-RV-B-001" },
      decision: {
        id: "PD-RV-B-001",
        outcome: "SHORT",
        strategyInstance: MOCK_STRATEGY_CONTEXT.instanceLabel + " (" + MOCK_STRATEGY_CONTEXT.instanceId + ")",
        strategyDefinitionVersion: MOCK_STRATEGY_CONTEXT.strategyDefinitionVersion,
        configurationVersion: MOCK_STRATEGY_CONTEXT.configurationVersion,
        inputSnapshot: "price_fact#8210, reference_fact#8209 (illustrative)",
        evaluationEvidence: "current candle closed strictly below EMA(20); previous candle ≥ previous EMA(20) (crossing_policy=strict)"
      }
    }
  };

  // ---- SCR-009 / VIEW-004 correction fixture (UC-017, UC-018) ----
  //
  // The ONE bounded correction lineage shared, by literal identity, between SCR-009's
  // "correction visible after historical cursor" scenario and VIEW-004 — same decision_id
  // strings, same objects, never a look-alike re-fixture. decision.md §6: replacement
  // DecisionRecorded carries a NEW decision_id + supersedes_fact_ref pointing DIRECTLY at the
  // original DecisionRecorded (direct-predecessor-fact-targeting, same convention as
  // order.md/risk.md/fill.md/execution-result.md) — NOT at the DecisionFactInvalidated event.
  // Both original and replacement share the SAME decision_context_cursor ("C-100"), matching
  // §6's "CÙNG logical computation key."
  var MOCK_DECISION_CORRECTION = {
    original: {
      id: "PD-100",
      outcome: "NO_ACTION",
      decisionContextCursor: "C-100",
      strategyInstance: MOCK_STRATEGY_CONTEXT.instanceLabel + " (" + MOCK_STRATEGY_CONTEXT.instanceId + ")",
      strategyDefinitionVersion: MOCK_STRATEGY_CONTEXT.strategyDefinitionVersion,
      configurationVersion: MOCK_STRATEGY_CONTEXT.configurationVersion,
      inputSnapshot: "price_fact#9001 (illustrative)",
      recordedTime: "2026-08-01T09:00:00Z"
    },
    invalidation: {
      invalidatedFactRef: "PD-100",
      invalidationReason: "Input evidence correction — the underlying price_fact#9001 was itself corrected upstream (illustrative)",
      recordedTime: "2026-08-05T14:00:00Z"
    },
    replacement: {
      id: "PD-101",
      outcome: "LONG",
      decisionContextCursor: "C-100",
      supersedesFactRef: "PD-100",
      strategyInstance: MOCK_STRATEGY_CONTEXT.instanceLabel + " (" + MOCK_STRATEGY_CONTEXT.instanceId + ")",
      strategyDefinitionVersion: MOCK_STRATEGY_CONTEXT.strategyDefinitionVersion,
      configurationVersion: MOCK_STRATEGY_CONTEXT.configurationVersion,
      inputSnapshot: "price_fact#9001-corrected (illustrative)",
      recordedTime: "2026-08-05T14:05:00Z"
    }
  };

  // Two illustrative Replay Cursors already run at SCR-002 (NAV-005 "Required context" for
  // SCR-009: "một Replay Cursor đã chạy tại SCR-002 ... phải tồn tại"). C-200 demonstrates "No
  // conflict"; C-100 demonstrates "correction visible after historical cursor," reusing the SAME
  // PD-100 identity as MOCK_DECISION_CORRECTION.original (no-look-ahead: at cursor C-100 itself,
  // ReplayState(C-100) shows PD-100/NO_ACTION — the later correction, recorded AFTER C-100's own
  // boundary, is disclosed separately, never repainted into the cursor's own reconstructed value,
  // per replay-event.md §2 "No-look-ahead xuyên suốt").
  var REPLAY_CURSORS = {
    "C-200": {
      cursor: "C-200",
      decision: {
        id: "PD-200",
        outcome: "SHORT",
        decisionContextCursor: "C-200",
        strategyInstance: MOCK_STRATEGY_CONTEXT.instanceLabel + " (" + MOCK_STRATEGY_CONTEXT.instanceId + ")",
        strategyDefinitionVersion: MOCK_STRATEGY_CONTEXT.strategyDefinitionVersion,
        configurationVersion: MOCK_STRATEGY_CONTEXT.configurationVersion,
        inputSnapshot: "price_fact#8410 (illustrative)",
        recordedTime: "2026-08-06T10:00:00Z"
      },
      hasCorrectionAfterCursor: false
    },
    "C-100": {
      cursor: "C-100",
      decision: MOCK_DECISION_CORRECTION.original,
      hasCorrectionAfterCursor: true
    }
  };

  // ---- Demo/UI state (prototype-local only, not a domain/session/replay state) ----

  var state = {
    activeScreen: "scr-008", // "scr-008" | "scr-009" | "view-004"
    scr008Selection: null, // null | "FILL-RV-A-001" | "FILL-RV-B-001"
    scr009Selection: null, // null | "C-100" | "C-200"
    // Family D — NAV-005 "Required context": whether a genuine Fill/Position contribution (SCR-008)
    // or a Replay Cursor already run at SCR-002 (SCR-009) currently exists at all. Independent
    // from whether the user has made a selection yet (state.scr008Selection/scr009Selection).
    reviewEvidence: {
      fillContributionExists: true,
      replayCursorRunExists: true
    }
  };

  // ---- Helpers ----

  function el(id) { return document.getElementById(id); }

  function el5(name, value) {
    return '<div class="evidence-row"><span class="evidence-label">' + name + '</span><span class="evidence-value">' + value + "</span></div>";
  }

  function chainStep(name, value, stopped) {
    return '<div class="chain-step">' +
      '<span class="chain-step-name">' + name + '</span>' +
      '<span class="chain-step-value' + (stopped ? " chain-step-stopped" : "") + '">' + value + '</span>' +
      "</div>";
  }

  function showScreen(targetId) {
    var screens = document.querySelectorAll(".screen");
    screens.forEach(function (s) { s.classList.add("screen-hidden"); });
    el(targetId).classList.remove("screen-hidden");

    var navButtons = document.querySelectorAll(".nav-btn");
    navButtons.forEach(function (b) { b.classList.remove("nav-btn-active"); });
    var navReview = document.querySelector('[data-nav="NAV-005"]');
    if (navReview && targetId === "screen-review") navReview.classList.add("nav-btn-active");

    if (targetId === "screen-deferred") {
      // no-op placeholder hookup handled by caller for deferred-stage-name
    }
  }

  // ---- Review section rendering (NAV-005 destination: SCR-008 + SCR-009 + VIEW-004) ----

  function renderReviewSection() {
    document.querySelectorAll("#review-subtabs [data-subtab]").forEach(function (btn) {
      btn.classList.toggle("subtab-btn-active", btn.getAttribute("data-subtab") === state.activeScreen);
    });
    el("scr-008-body").classList.toggle("screen-hidden", state.activeScreen !== "scr-008");
    el("scr-009-body").classList.toggle("screen-hidden", state.activeScreen !== "scr-009");
    el("view-004-body").classList.toggle("screen-hidden", state.activeScreen !== "view-004");

    if (state.activeScreen === "scr-008") renderScr008();
    else if (state.activeScreen === "scr-009") renderScr009();
    else renderView004();
  }

  function goToReviewTab(tab) {
    state.activeScreen = tab;
    showScreen("screen-review");
    renderReviewSection();
  }

  // ---- SCR-008 — Decision -> Position Lineage Trace (UC-016) ----

  function renderScr008() {
    var body = el("scr-008-body");

    // NAV-005 "Required context": a Fill/Position contribution must exist. When missing, no
    // evidence is fabricated to fill the gap. Labelled per NAV-005's own text as "STATE-002
    // (empty)" at this destination-selection level — see traceability.md §3 for the explicit
    // disclaimer that this is distinct from STATE-002's own narrower canonical catalogue row
    // (ux-blueprint.md §11, which lists only SCR-004/SCR-005/SCR-007/SCR-011).
    if (!state.reviewEvidence.fillContributionExists) {
      body.innerHTML =
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-002 — empty (NAV-005 destination-selection level)</div>' +
        "<div>No Fill/Position contribution exists to trace. Read-only navigation to this " +
        "destination remains available (UX-P-5); no review evidence is invented to fill the gap.</div>" +
        "</div>";
      return;
    }

    var html = '<div class="label-row">' +
      '<span class="mode-label">Review</span>' +
      '<span class="authority-label authority-label-authoritative">Authority class: authoritative (every fact in the chain)</span>' +
      '<span class="prototype-datum-label">Prototype datum: Illustrative / non-authoritative</span>' +
      "</div>" +
      '<div class="field-row">' +
      '<label>Select a Fill contributing to Position to trace (UC-016 step 1)</label>' +
      '<div class="chip-row" id="scr-008-fill-selector">' +
      '<button class="btn subtab-btn" data-fill-select="FILL-RV-A-001">FILL-RV-A-001 (LONG)</button>' +
      '<button class="btn subtab-btn" data-fill-select="FILL-RV-B-001">FILL-RV-B-001 (SHORT)</button>' +
      "</div></div>" +
      '<div id="scr-008-trace"></div>';
    body.innerHTML = html;

    body.querySelectorAll("[data-fill-select]").forEach(function (btn) {
      btn.classList.toggle("subtab-btn-active", btn.getAttribute("data-fill-select") === state.scr008Selection);
      btn.addEventListener("click", function () {
        state.scr008Selection = btn.getAttribute("data-fill-select");
        renderScr008();
      });
    });

    renderScr008Trace();
  }

  function renderScr008Trace() {
    var box = el("scr-008-trace");
    if (!box) return;
    if (!state.scr008Selection) {
      box.innerHTML = '<div class="hint">No Fill selected yet — choose one above to view its lineage trace.</div>';
      return;
    }
    var lin = LINEAGE_FILLS[state.scr008Selection];
    var html =
      // Downstream causation trace — INV-2, TÁCH BIỆT visually from the Decision explainability
      // group below (reuses the purple "downstream" border convention from Batch 04).
      '<div class="evidence-group evidence-group-downstream">' +
      '<div class="evidence-group-label">Causation trace (Fill → Decision, no mắt xích thiếu)</div>' +
      '<div class="chain-list">' +
      chainStep("Fill", lin.fill.id + " (direction " + lin.fill.direction + ", " + lin.fill.quantity + " " + lin.fill.quantityUnit + " @ " + lin.fill.price + " " + lin.fill.priceCurrency + ")") +
      chainStep("ExecutionResult", lin.executionResult.id + " (" + lin.executionResult.resultType + ")") +
      chainStep("Order", lin.order.id + " (environment " + lin.order.environment + ")") +
      chainStep("Execution Intent", lin.executionIntent.id + " (" + lin.executionIntent.status + ")") +
      chainStep("RiskEvaluation", lin.riskEvaluation.id + " (" + lin.riskEvaluation.result + ")") +
      chainStep("Trade Intent", lin.tradeIntent.id) +
      chainStep("Decision (gốc)", lin.decision.id + " (" + lin.decision.outcome + ")") +
      "</div></div>" +
      // Decision explainability — separate group, resolved DIRECTLY from the recorded fact, no
      // re-derivation/recomputation after the fact (INV-2).
      '<div class="evidence-group evidence-group-upstream">' +
      '<div class="evidence-group-label">Decision explainability evidence (tách biệt khỏi causation trace above — resolved directly from recorded fact)</div>' +
      '<div style="margin-bottom:6px;"><span class="outcome-badge ' + (lin.decision.outcome === "LONG" ? "outcome-long" : "outcome-short") + '">' + lin.decision.outcome + "</span></div>" +
      el5("Decision identity", lin.decision.id) +
      el5("Strategy Instance", lin.decision.strategyInstance) +
      el5("Strategy Definition Version", lin.decision.strategyDefinitionVersion) +
      el5("Configuration", lin.decision.configurationVersion) +
      el5("Recorded input snapshot", lin.decision.inputSnapshot) +
      el5("Recorded evaluation evidence", lin.decision.evaluationEvidence) +
      "</div>" +
      '<div class="exit-row">' +
      // v1.1 (closes P2-B05-A-MIN-01): renamed from "Compare this trace's cursor..." — neither
      // lineage above carries a mapped Replay Cursor, so the old wording overstated a handoff
      // that never actually carried this trace's cursor into SCR-009. SCR-009's own cursor
      // selection is genuinely independent of whatever was selected here.
      '<button class="btn" id="btn-scr008-to-scr009">Open Historical State Comparison (SCR-009) →</button>' +
      '<p class="hint">Neither lineage above has a correction recorded against it, so there is no "correction detected" hand-off to VIEW-004 from this screen in this bounded fixture set — see SCR-009 for the correction-inspection hand-off (UC-018). The historical comparison target (Replay Cursor) is selected independently on SCR-009 — this button does not carry the trace above’s own cursor forward.</p>' +
      "</div>";
    box.innerHTML = html;
    el("btn-scr008-to-scr009").addEventListener("click", function () { goToReviewTab("scr-009"); });
  }

  // ---- SCR-009 — Historical State Comparison (UC-017) ----

  function renderScr009() {
    var body = el("scr-009-body");

    // NAV-005 "Required context": a Replay Cursor already run at SCR-002 must exist.
    if (!state.reviewEvidence.replayCursorRunExists) {
      body.innerHTML =
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-002 — empty (NAV-005 destination-selection level)</div>' +
        "<div>No Replay Cursor has been run at SCR-002 yet. Read-only navigation to this " +
        "destination remains available; no comparison is invented to fill the gap.</div>" +
        "</div>";
      return;
    }

    var html = '<div class="label-row">' +
      '<span class="mode-label">Review</span>' +
      '<span class="authority-label authority-label-authoritative">Authority class: authoritative recorded fact</span>' +
      '<span class="authority-label authority-label-recomputation">Authority class: non-authoritative comparison result</span>' +
      '<span class="prototype-datum-label">Prototype datum: Illustrative / non-authoritative</span>' +
      "</div>" +
      '<div class="field-row">' +
      '<label>Select a Replay Cursor already run at SCR-002 to compare</label>' +
      '<div class="chip-row" id="scr-009-cursor-selector">' +
      '<button class="btn subtab-btn" data-cursor-select="C-200">C-200 (no correction affecting this cursor)</button>' +
      '<button class="btn subtab-btn" data-cursor-select="C-100">C-100 (correction recorded after this cursor)</button>' +
      "</div></div>" +
      '<div id="scr-009-comparison"></div>';
    body.innerHTML = html;

    body.querySelectorAll("[data-cursor-select]").forEach(function (btn) {
      btn.classList.toggle("subtab-btn-active", btn.getAttribute("data-cursor-select") === state.scr009Selection);
      btn.addEventListener("click", function () {
        state.scr009Selection = btn.getAttribute("data-cursor-select");
        body.querySelectorAll("[data-cursor-select]").forEach(function (b2) {
          b2.classList.toggle("subtab-btn-active", b2 === btn);
        });
        renderScr009Comparison();
      });
    });

    renderScr009Comparison();
  }

  function renderScr009Comparison() {
    var box = el("scr-009-comparison");
    if (!box) return;
    if (!state.scr009Selection) {
      box.innerHTML = '<div class="hint">No cursor selected yet — choose one above to compare reconstructed vs. recorded state.</div>';
      return;
    }
    var c = REPLAY_CURSORS[state.scr009Selection];
    var d = c.decision;

    // Both panels below resolve to the SAME object on purpose (INV-3 / replay-event.md's
    // determinism guarantee) — ReplayState(C) and "state originally recorded at C" are not
    // two independently-computed values that happen to agree; they are structurally the same
    // fold at the same no-look-ahead cursor, so there is nothing to silently drift.
    var html =
      '<div class="panel">' +
      '<div class="panel-title">ReplayState(' + c.cursor + ') — reconstructed now</div>' +
      el5("Decision identity", d.id) +
      el5("outcome", d.outcome) +
      el5("decision_context_cursor", d.decisionContextCursor) +
      el5("recorded_time", d.recordedTime) +
      "</div>" +
      '<div class="panel">' +
      '<div class="panel-title">State recorded / originally displayed at cursor ' + c.cursor + '</div>' +
      "<div>Identical to the reconstructed panel above — deterministic, no-look-ahead replay at " +
      "the SAME cursor cannot diverge from what was recorded at that cursor (replay-event.md §2).</div>" +
      "</div>";

    if (!c.hasCorrectionAfterCursor) {
      html += '<div class="panel panel-passed">' +
        '<div class="panel-title">No conflict</div>' +
        '<span class="authority-label authority-label-recomputation">Non-authoritative comparison result</span>' +
        "<div>No correction exists between the recorded time and now for this Decision.</div>" +
        "</div>";
    } else {
      // v1.1 (closes P2-B05-A-MAJ-01): the panel below previously only disclosed that an
      // invalidation occurred — it never showed the later replacement value or the explicit
      // old→new difference, so UC-017 was not satisfied without a further trip to VIEW-004. The
      // historical panels above remain byte-for-byte unchanged (no repaint) — this panel is
      // purely additive, reusing the SAME MOCK_DECISION_CORRECTION object VIEW-004 reads (no
      // duplicate/look-alike fixture).
      var orig = MOCK_DECISION_CORRECTION.original;
      var inv = MOCK_DECISION_CORRECTION.invalidation;
      var repl = MOCK_DECISION_CORRECTION.replacement;
      html += '<div class="panel panel-indeterminate">' +
        '<div class="panel-title">Correction visible after historical cursor</div>' +
        "<div>The historical value shown above is UNCHANGED — it still correctly reflects " + d.id +
        " at cursor " + c.cursor + " (no repaint). A correction was recorded AFTER this cursor " +
        "(recorded_time " + inv.recordedTime + " > this cursor’s own recorded_time " + d.recordedTime + "):</div>" +
        "</div>" +
        '<div class="panel panel-indeterminate">' +
        '<div class="panel-title">Later-correction comparison (UC-017 explicit difference)</div>' +
        '<span class="authority-label authority-label-authoritative">Authority class: authoritative recorded evidence (original / invalidation / replacement)</span>' +
        '<span class="authority-label authority-label-recomputation">Authority class: non-authoritative comparison result</span>' +
        el5("Historical cursor", c.cursor) +
        el5("Original historical fact (unchanged above)", orig.id + " — " + orig.outcome) +
        el5("Invalidation — invalidated_fact_ref", inv.invalidatedFactRef) +
        el5("Invalidation — invalidation_reason", inv.invalidationReason) +
        el5("Invalidation — recorded_time", inv.recordedTime) +
        el5("Later replacement", repl.id + " — " + repl.outcome) +
        el5("Later replacement — supersedes_fact_ref", repl.supersedesFactRef) +
        el5("Later replacement — recorded_time", repl.recordedTime) +
        '<div class="panel-title" style="margin-top:10px;">Comparison result (non-authoritative)</div>' +
        "<div><strong>" + orig.outcome + " → " + repl.outcome + "</strong> — this difference is a derived comparison, not itself a fact; the authoritative facts remain the original/invalidation/replacement rows above.</div>" +
        '<div class="exit-row"><button class="btn btn-primary" id="btn-scr009-to-view004">Inspect correction (VIEW-004) →</button></div>' +
        "</div>";
    }
    box.innerHTML = html;
    var btn = el("btn-scr009-to-view004");
    if (btn) btn.addEventListener("click", function () { goToReviewTab("view-004"); });
  }

  // ---- VIEW-004 — Correction Inspection (UC-018) ----

  function renderView004() {
    var body = el("view-004-body");
    var c = MOCK_DECISION_CORRECTION;

    // VIEW-004 has no empty/blocked state of its own (ux-blueprint.md §7.4 VIEW-004: "KHÔNG áp
    // dụng — hiển thị luôn cả hai trạng thái là hành vi bắt buộc") — showing both the
    // original fact and the replacement fact is mandatory behavior, never a branch. This bounded
    // prototype has exactly one correction fixture, shown directly.
    var html = '<div class="label-row">' +
      '<span class="mode-label">Review</span>' +
      '<span class="authority-label authority-label-authoritative">Authority class: authoritative (both the original fact and the replacement fact)</span>' +
      '<span class="prototype-datum-label">Prototype datum: Illustrative / non-authoritative</span>' +
      "</div>" +
      '<div class="evidence-group evidence-group-upstream">' +
      '<div class="evidence-group-label">Original fact (still resolvable, append-only — never deleted/overwritten)</div>' +
      el5("Decision identity", c.original.id) +
      el5("outcome", c.original.outcome) +
      el5("decision_context_cursor", c.original.decisionContextCursor) +
      el5("Strategy Instance", c.original.strategyInstance) +
      el5("Recorded input snapshot", c.original.inputSnapshot) +
      el5("recorded_time", c.original.recordedTime) +
      "</div>" +
      '<div class="evidence-group evidence-group-downstream">' +
      '<div class="evidence-group-label">Invalidation + replacement fact</div>' +
      '<div class="chain-step-name" style="margin-bottom:4px;">DecisionFactInvalidated</div>' +
      el5("invalidated_fact_ref", c.invalidation.invalidatedFactRef) +
      el5("invalidation_reason", c.invalidation.invalidationReason) +
      el5("recorded_time", c.invalidation.recordedTime) +
      '<div class="chain-step-name" style="margin:10px 0 4px;">Replacement DecisionRecorded</div>' +
      el5("Decision identity", c.replacement.id) +
      el5("outcome", c.replacement.outcome) +
      el5("decision_context_cursor (same logical computation key as original)", c.replacement.decisionContextCursor) +
      el5("Recorded input snapshot", c.replacement.inputSnapshot) +
      el5("recorded_time", c.replacement.recordedTime) +
      '<div class="hint"><strong>supersedes_fact_ref: ' + c.replacement.supersedesFactRef +
      "</strong> — explicit link from replacement " + c.replacement.id + " directly to original " +
      c.original.id + " (direct-predecessor-fact-targeting, decision.md §6 §11).</div>" +
      "</div>" +
      '<div class="hint">Scope note: this prototype demonstrates Decision’s correction lineage. ' +
      "RiskEvaluation and Fill follow the SAME direct supersedes_fact_ref + *FactInvalidated pattern " +
      "(risk.md, fill.md) but are not separately fixtured here. ExecutionResult’s correction lineage " +
      "is materially more complex (execution-result.md §2 — a new ExecutionResultComputation with " +
      "computation_purpose=CORRECTION + predecessor_execution_result_ref + correction_authorization_ref, " +
      "THEN a new ExecutionResultRecorded) and is not modeled interactively here. PaperExecutionObservation " +
      "and Position have no correction lineage of their own (execution-result.md §11, position.md §1) " +
      "— none of these variants is collapsed into one invented uniform schema.</div>" +
      '<div class="exit-row">' +
      '<button class="btn" id="btn-view004-to-scr009">← Back to Historical Comparison (SCR-009)</button>' +
      '<button class="btn" id="btn-view004-to-scr008">← Back to Lineage Trace (SCR-008)</button>' +
      "</div>";
    body.innerHTML = html;
    el("btn-view004-to-scr009").addEventListener("click", function () { goToReviewTab("scr-009"); });
    el("btn-view004-to-scr008").addEventListener("click", function () { goToReviewTab("scr-008"); });
  }

  // ---- Navigation wiring ----

  function wireGlobalNav(scope) {
    var root = scope || document;
    var buttons = root.querySelectorAll("[data-nav][data-target]");
    buttons.forEach(function (b) {
      b.addEventListener("click", function () {
        var target = b.getAttribute("data-target");
        var stage = b.getAttribute("data-stage");
        showScreen(target);
        if (stage) el("deferred-stage-name").textContent = stage;
        if (target === "screen-review") renderReviewSection();
      });
    });
  }

  function wireReviewSubtabs() {
    document.querySelectorAll("#review-subtabs [data-subtab]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        state.activeScreen = btn.getAttribute("data-subtab");
        renderReviewSection();
      });
    });
  }

  // ---- QA panel wiring (prototype tooling only — Family D empty-context simulation) ----

  function refreshQaActiveStates() {
    var map = {
      "scr008-evidence-exists": state.reviewEvidence.fillContributionExists === true,
      "scr008-evidence-missing": state.reviewEvidence.fillContributionExists === false,
      "scr009-cursor-exists": state.reviewEvidence.replayCursorRunExists === true,
      "scr009-cursor-missing": state.reviewEvidence.replayCursorRunExists === false
    };
    document.querySelectorAll("[data-qa]").forEach(function (b) {
      var key = b.getAttribute("data-qa");
      if (map.hasOwnProperty(key)) b.classList.toggle("qa-btn-active", map[key]);
    });
  }

  function wireQaPanel() {
    el("qa-toggle").addEventListener("click", function () {
      var body = el("qa-body");
      var expanded = !body.classList.contains("qa-hidden");
      body.classList.toggle("qa-hidden");
      el("qa-toggle").setAttribute("aria-expanded", String(!expanded));
    });

    document.querySelectorAll("[data-qa]").forEach(function (b) {
      b.addEventListener("click", function () {
        var qa = b.getAttribute("data-qa");
        if (qa === "scr008-evidence-exists") state.reviewEvidence.fillContributionExists = true;
        else if (qa === "scr008-evidence-missing") state.reviewEvidence.fillContributionExists = false;
        else if (qa === "scr009-cursor-exists") state.reviewEvidence.replayCursorRunExists = true;
        else if (qa === "scr009-cursor-missing") state.reviewEvidence.replayCursorRunExists = false;

        refreshQaActiveStates();
        showScreen("screen-review");
        renderReviewSection();
      });
    });

    el("qa-reset").addEventListener("click", function () {
      state.reviewEvidence.fillContributionExists = true;
      state.reviewEvidence.replayCursorRunExists = true;
      state.scr008Selection = null;
      state.scr009Selection = null;
      state.activeScreen = "scr-008";
      refreshQaActiveStates();
      showScreen("screen-review");
      renderReviewSection();
    });
  }

  // ---- Init ----

  function init() {
    wireGlobalNav(document);
    wireReviewSubtabs();
    wireQaPanel();
    refreshQaActiveStates();
    renderReviewSection();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
