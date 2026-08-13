/*
 * Ride — Phase 2 Prototype — Batch 02 (Replay reconstruction + optional parity).
 *
 * Illustrative, non-authoritative UI logic only. No real backend, no real
 * exchange integration, no real credentials, no authoritative financial
 * data, no domain event log, no replay/Decision/parity engine. Every
 * displayed value below is mock/static.
 *
 * This is a separate, self-contained page from Batch 01 — it does NOT share
 * live JS state with prototype/phase-2/batch-01/. "Arriving from Research"
 * (pinned Strategy Instance, Research verification outcome) is represented
 * as Batch-02-local simulated incoming context, per the QA panel — VIEW-001/
 * VIEW-002 are NOT re-implemented as new surfaces here.
 *
 * Traceability for every element rendered here is pinned in
 * traceability.md — this file does not introduce any UC/PR/domain concept
 * that is not already Consolidated Stable in docs/product/ux-blueprint.md
 * or docs/domain/decision.md §9a.
 */

(function () {
  "use strict";

  // ---- Mock data (illustrative only, not authoritative financial data) ----

  var MOCK_CURSORS = [
    { id: "C-001", label: "C-001 — 2026-08-01T09:00:00Z", available: true },
    { id: "C-002", label: "C-002 — 2026-08-01T10:15:00Z", available: true },
    { id: "C-003", label: "C-003 — 2026-08-01T11:30:00Z (reference unavailable)", available: false }
  ];

  // Decision -> Trade Intent -> RiskEvaluation -> Execution Intent -> Order -> ExecutionResult ->
  // Fill -> Position lineage AT the cursor (ux-blueprint.md §7.2 SCR-002 "Information displayed").
  // Only facts whose recorded_time <= C appear -- represented here as a static label per cursor,
  // not a real timestamp engine.
  var MOCK_REPLAY_STATE = {
    "C-001": {
      decision: "LONG",
      tradeIntent: "TradeIntentIssued (issued)",
      riskEvaluation: "APPROVED",
      executionIntent: "ExecutionIntentAccepted",
      order: "OrderSubmissionRequest acknowledged",
      executionResult: "EXECUTED",
      fill: "Fill recorded",
      position: "LONG"
    },
    "C-002": {
      decision: "NO_ACTION",
      tradeIntent: "— none (result = NO_ACTION never issues Trade Intent, decision.md §10)",
      riskEvaluation: "— not applicable (no Trade Intent)",
      executionIntent: "— not applicable",
      order: "— not applicable",
      executionResult: "— not applicable",
      fill: "— not applicable",
      position: "FLAT"
    }
  };

  // Canonical Decision Semantic Representation (decision.md §9a.1) -- illustrative subset of the
  // fixed field set, per cursor. Used as the "recorded side" for VIEW-003.
  var MOCK_REPRESENTATION = {
    "C-001": {
      result: "LONG",
      instrument_selection_ref: "{BTC-USDT, Binance, listing-01}",
      strategy_instance_id: "inst-a",
      strategy_definition_version_id: "sdv-v1.0",
      configuration_version_ref: "cfg-v3",
      decision_rule_ref: "rule-crossing-ma",
      rule_family: "moving-average-crossing",
      decision_context_cursor: "C-001",
      normalized_rule_parameters: "price_source=mark, crossing_policy=strict (illustrative subset)",
      input_evidence_refs: "price_fact#4821, reference_fact#4820 (illustrative)"
    },
    "C-002": {
      result: "NO_ACTION",
      instrument_selection_ref: "{BTC-USDT, Binance, listing-01}",
      strategy_instance_id: "inst-a",
      strategy_definition_version_id: "sdv-v1.0",
      configuration_version_ref: "cfg-v3",
      decision_rule_ref: "rule-crossing-ma",
      rule_family: "moving-average-crossing",
      decision_context_cursor: "C-002",
      normalized_rule_parameters: "price_source=mark, crossing_policy=strict (illustrative subset)",
      input_evidence_refs: "price_fact#4915, reference_fact#4914 (illustrative)"
    }
  };

  var REPRESENTATION_FIELD_ORDER = [
    ["result", "Result"],
    ["instrument_selection_ref", "Instrument selection ref"],
    ["strategy_instance_id", "Strategy Instance"],
    ["strategy_definition_version_id", "Strategy Definition Version"],
    ["configuration_version_ref", "Configuration Version"],
    ["decision_rule_ref", "Decision rule ref"],
    ["rule_family", "Rule family"],
    ["decision_context_cursor", "Decision-context cursor"],
    ["normalized_rule_parameters", "Normalized rule parameters"],
    ["input_evidence_refs", "Input evidence refs"]
  ];

  // Nine pinned axes (decision.md §9a.4) -- demo-only status per QA-selected outcome, never
  // computed. Order matches §9a.4/§9a.6 verbatim.
  var PINNED_AXES = [
    "Strategy Instance",
    "Strategy Definition Version",
    "Configuration Version",
    "Decision rule identity/version",
    "Decision implementation provenance (when established)",
    "Canonical Replay Cursor",
    "Input evidence reference",
    "Semantic-representation-definition version (DSR-001 v2)",
    "Digest-definition version (§9a.5b(3))"
  ];

  // Axis 9 (Digest-definition version) is always "not-applicable" in this batch's demo path --
  // structured Canonical Decision Semantic Representation comparison is the basis used, Digest
  // comparison is never invoked, so this axis is N/A rather than "resolved" or "unresolved"
  // (decision.md §9a.2). Closes P2-B02-B-MAJ-01: "ok"/"resolved, consistent" previously
  // overloaded this axis even though Digest was never used.
  var DIGEST_AXIS_INDEX = 8;

  function baseAxisStatuses() {
    var statuses = ["ok", "ok", "ok", "ok", "ok", "ok", "ok", "ok", "ok"];
    statuses[DIGEST_AXIS_INDEX] = "not-applicable";
    return statuses;
  }

  // ---- Demo/UI state (prototype-local only, not a domain/session/replay state) ----

  var state = {
    incomingContext: "incoming-ok", // "incoming-ok" | "incoming-no-instance" | "incoming-not-passed"
    selectedCursor: "C-001",
    qaOverride: null, // e.g. "scr002-loading"
    parityOutcome: "match" // "match" | "mismatch" | "indeterminate" -- demo-selected, never computed
  };

  // ---- Helpers ----

  function el(id) { return document.getElementById(id); }

  function cursorById(id) {
    var i;
    for (i = 0; i < MOCK_CURSORS.length; i++) {
      if (MOCK_CURSORS[i].id === id) return MOCK_CURSORS[i];
    }
    return null;
  }

  function showScreen(targetId, deferredStageName) {
    var screens = document.querySelectorAll(".screen");
    screens.forEach(function (s) { s.classList.add("screen-hidden"); });
    el(targetId).classList.remove("screen-hidden");

    var navButtons = document.querySelectorAll(".nav-btn");
    navButtons.forEach(function (b) { b.classList.remove("nav-btn-active"); });

    if (targetId === "screen-scr-002") {
      var navReplay = document.querySelector('[data-nav="NAV-002"]');
      if (navReplay) navReplay.classList.add("nav-btn-active");
    }
    if (targetId === "screen-deferred") {
      el("deferred-stage-name").textContent = deferredStageName || "This stage";
    }
  }

  function updateContextBar() {
    var strategyLabel;
    if (state.incomingContext === "incoming-no-instance") {
      strategyLabel = "— not pinned —";
    } else {
      strategyLabel = "Instance A — bound to Strategy Definition Version v1.0 (pinned, read-only)";
    }
    el("ctx-strategy-instance").textContent = strategyLabel;
  }

  // ---- SCR-002 rendering ----

  function renderScr002() {
    var body = el("scr-002-precondition-body");
    var override = state.qaOverride;

    // NAV-002-level gate: Strategy Instance missing (STATE-004's own catalogue "Applicable
    // screen/view" column names VIEW-001 only, NOT SCR-002 -- represented here as NAV-002's
    // prose-described blocked/prompt precondition for SCR-002 entry, faithfully kept distinct
    // from a claim that SCR-002 itself owns STATE-004, per ux-blueprint.md §5a NAV-002 vs §11
    // STATE-004 row).
    if (state.incomingContext === "incoming-no-instance") {
      body.innerHTML =
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">Blocked — Strategy Instance not pinned (NAV-002 precondition, STATE-004 cited at the NAV level)</div>' +
        "<div>NAV-002's Required Context: a Strategy Instance must be pinned (VIEW-001) before " +
        "Replay reconstruction may begin. This panel reflects NAV-002's own blocked/prompt " +
        "behavior (ux-blueprint.md §5a) -- the canonical STATE-004 catalogue entry's " +
        '"Applicable screen/view" column names VIEW-001, not SCR-002; this is NOT a claim that ' +
        "SCR-002 itself owns STATE-004.</div>" +
        "</div>";
      return;
    }

    // Read-only inspection: Research verification did not PASS -- authoritative reconstruction
    // blocked, blocked reason still disclosed (UX-P-5).
    if (state.incomingContext === "incoming-not-passed") {
      body.innerHTML =
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">Blocked — Research verification did not PASS</div>' +
        "<div>A Strategy Instance is pinned, but the Research verification result (VIEW-002) was " +
        "not PASSED. Per UX-P-5, read-only navigation to SCR-002 remains available to view this " +
        "blocked reason -- no historical reconstruction runs, and no authoritative progression " +
        "is permitted.</div>" +
        "</div>";
      return;
    }

    if (override === "scr002-loading") {
      body.innerHTML =
        '<div class="panel panel-loading">STATE-001 — loading market-analysis / reconstruction state…</div>';
      return;
    }

    // Cursor picker is always shown once the precondition is satisfied.
    var html = '<div class="field-row">' +
      '<label for="cursor-select">Canonical Replay Cursor</label>' +
      '<select id="cursor-select"></select>' +
      "</div>" +
      '<div id="scr-002-reconstruction-body"></div>';
    body.innerHTML = html;

    var select = el("cursor-select");
    MOCK_CURSORS.forEach(function (c) {
      var opt = document.createElement("option");
      opt.value = c.id;
      opt.textContent = c.label;
      select.appendChild(opt);
    });
    select.value = state.selectedCursor;
    select.addEventListener("change", function () {
      state.selectedCursor = select.value;
      state.qaOverride = null;
      renderReconstruction();
    });

    renderReconstruction();
  }

  function renderReconstruction() {
    var body = el("scr-002-reconstruction-body");
    if (!body) return;

    var cursor = cursorById(state.selectedCursor);

    if (!cursor || !cursor.available) {
      body.innerHTML =
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-006 — Replay reference unavailable</div>' +
        "<div>The selected cursor's Replay reference (Chapter 8 §8.5) does not resolve. No " +
        "historical reconstruction can be shown for <strong>" + (cursor ? cursor.label : state.selectedCursor) +
        "</strong>.</div>" +
        "</div>";
      return;
    }

    var lineage = MOCK_REPLAY_STATE[cursor.id];

    body.innerHTML =
      '<div class="panel">' +
      '<div class="label-row">' +
      '<span class="mode-label">Replay</span>' +
      '<span class="authority-label authority-label-authoritative">Authority class: Recorded fact (default reconstruction)</span>' +
      '<span class="prototype-datum-label">Prototype datum: Illustrative / non-authoritative</span>' +
      "</div>" +
      '<div class="hint">ReplayState(' + cursor.id + ') — only facts with recorded_time &le; ' + cursor.id + " are shown.</div>" +
      '<div class="lineage-list">' +
      lineageRow("Decision", lineage.decision) +
      lineageRow("Trade Intent", lineage.tradeIntent) +
      lineageRow("RiskEvaluation", lineage.riskEvaluation) +
      lineageRow("Execution Intent", lineage.executionIntent) +
      lineageRow("Order", lineage.order) +
      lineageRow("ExecutionResult", lineage.executionResult) +
      lineageRow("Fill", lineage.fill) +
      lineageRow("Position", lineage.position) +
      "</div>" +
      "</div>" +
      '<div class="exit-row">' +
      '<button class="btn btn-primary" id="btn-to-view-003">Invoke optional parity recomputation</button>' +
      '<p class="hint">Optional, non-automatic (VIEW-003) -- not invoked unless explicitly requested here.</p>' +
      "</div>";

    el("btn-to-view-003").addEventListener("click", function () {
      showScreen("screen-view-003");
      renderView003();
    });
  }

  function lineageRow(name, value) {
    return '<div class="lineage-step"><span class="lineage-step-name">' + name +
      '</span><span class="lineage-step-value">' + value + "</span></div>";
  }

  // ---- VIEW-003 rendering ----

  function renderView003() {
    var body = el("view-003-body");
    var cursor = cursorById(state.selectedCursor);
    var recorded = MOCK_REPRESENTATION[cursor.id];
    var outcome = state.parityOutcome; // "match" | "mismatch" | "indeterminate"

    var recomputed;
    // array of "ok" | "differs" | "unresolved" | "not-applicable", one per PINNED_AXES entry --
    // DIGEST_AXIS_INDEX is always "not-applicable" here (baseAxisStatuses()), never "ok", since
    // Digest comparison is never used in this batch's demo path (closes P2-B02-B-MAJ-01).
    var axisStatuses;
    if (outcome === "match") {
      recomputed = recorded;
      axisStatuses = baseAxisStatuses();
    } else if (outcome === "mismatch") {
      recomputed = Object.assign({}, recorded, {
        result: recorded.result === "LONG" ? "NO_ACTION" : "LONG"
      });
      axisStatuses = baseAxisStatuses();
    } else {
      recomputed = Object.assign({}, recorded);
      axisStatuses = baseAxisStatuses();
      axisStatuses[4] = "unresolved"; // Decision implementation provenance (axis 5)
    }

    var html = '<div class="label-row">' +
      '<span class="mode-label">Replay</span>' +
      '<span class="authority-label authority-label-recomputation">Authority class: Non-authoritative recomputation</span>' +
      '<span class="prototype-datum-label">Prototype datum: Illustrative / non-authoritative (demo-selected outcome)</span>' +
      "</div>";

    html += '<div class="digest-note">decision_semantic_digest_definition_id/version: <strong>CHƯA ESTABLISHED / unresolved</strong> ' +
      "(decision.md §9a.2/§9a.5b(3)). This prototype demonstrates structured Canonical Decision " +
      "Semantic Representation comparison — the only valid basis for MATCH while this axis " +
      "remains ungoverned. Because Digest comparison is NOT used here, the Digest-definition " +
      "axis below renders as <strong>not applicable</strong>, not \"unresolved\" — those are " +
      "different concepts: \"unresolved\" means a required axis failed to resolve (forcing " +
      "INDETERMINATE); \"not applicable\" means this axis is not part of the comparison basis " +
      "actually being used. A future comparison that DID use Digest would require this axis's " +
      "governing definition to resolve, per decision.md §9a.2/§9a.6, before Digest could " +
      "contribute to MATCH/MISMATCH — that governance gap is not resolved here.</div>";

    html += '<div class="representation-compare">' +
      representationPanel("Recorded Decision — Canonical Semantic Representation", recorded, "authoritative") +
      representationPanel("Recomputed — Canonical Semantic Representation", recomputed, "recomputation") +
      "</div>";

    html += '<div class="axis-list">';
    PINNED_AXES.forEach(function (axisName, i) {
      html += axisRow(axisName, axisStatuses[i]);
    });
    html += "</div>";

    if (outcome === "match") {
      html +=
        '<div class="panel panel-passed">' +
        '<div class="panel-title">STATE-007 — parity match</div>' +
        "<div>All applicable required axes are resolved and consistent; the Digest-definition " +
        "axis is not applicable — Digest is not used in this structured Representation " +
        "comparison (decision.md §9a.2). Canonical Decision Semantic Representation equal under " +
        "structured comparison. This confirms, but does not re-authorize, the already-recorded " +
        "Decision (decision.md §9a.7).</div>" +
        "</div>";
    } else if (outcome === "mismatch") {
      html +=
        '<div class="panel panel-fail">' +
        '<div class="panel-title">STATE-008 — parity mismatch</div>' +
        "<div>All applicable required axes are resolved and consistent (Digest-definition axis " +
        "not applicable — Digest is not used for this comparison), but the Canonical Decision " +
        "Semantic Representation differs between recorded and recomputed sides (illustrative: " +
        "result " + recorded.result + " vs " + recomputed.result + "). This does NOT " +
        "automatically invalidate the recorded Decision -- correction lineage (decision.md §11) " +
        "still requires its own explicit invalidate-then-replace transaction.</div>" +
        "</div>" +
        '<div class="exit-row">' +
        '<button class="btn" data-nav="NAV-005" data-target="screen-deferred" data-stage="Review">Continue to Review</button>' +
        '<p class="hint">Review (SCR-009) is not authored in Batch 02 -- deferred to a later batch.</p>' +
        "</div>";
    } else {
      html +=
        '<div class="panel panel-indeterminate">' +
        '<div class="panel-title">STATE-030 — parity indeterminate</div>' +
        "<div>Decision implementation provenance (axis 5) does not resolve/reproduce consistently " +
        "between recorded and recomputed sides -- per decision.md §9a.4/§9a.6, this must be " +
        "INDETERMINATE, never MATCH or MISMATCH, regardless of whether the Representation " +
        "otherwise appears equal.</div>" +
        "</div>";
    }

    body.innerHTML = html;
    wireGlobalNav(body);
  }

  function representationPanel(title, fields, kind) {
    var html = '<div class="representation-panel"><h3>' + title + "</h3>";
    REPRESENTATION_FIELD_ORDER.forEach(function (entry) {
      var key = entry[0], label = entry[1];
      html += '<div class="evidence-row"><span class="evidence-label">' + label +
        '</span><span class="evidence-value">' + fields[key] + "</span></div>";
    });
    return html + "</div>";
  }

  // Four distinct axis states (closes P2-B02-B-MAJ-01 -- "ok" previously overloaded both
  // "genuinely resolved/consistent" and "not part of this comparison basis"):
  //   ok              resolved, consistent
  //   differs          resolved, but Representation differs between sides
  //   unresolved       required for this comparison, but did not resolve (forces INDETERMINATE)
  //   not-applicable   axis is not part of the comparison basis actually used here (Digest, in
  //                    this batch's demo path)
  function axisRow(name, statusKey) {
    var statusText = statusKey === "ok" ? "resolved, consistent"
      : statusKey === "differs" ? "resolved, differs"
      : statusKey === "not-applicable" ? "not applicable — not used for this comparison"
      : "unresolved";
    var statusClass = statusKey === "ok" ? "axis-status-ok"
      : statusKey === "differs" ? "axis-status-differs"
      : statusKey === "not-applicable" ? "axis-status-not-applicable"
      : "axis-status-unresolved";
    return '<div class="axis-row"><span class="axis-name">' + name +
      '</span><span class="axis-status ' + statusClass + '">' + statusText + "</span></div>";
  }

  // ---- Navigation wiring ----

  function wireGlobalNav(scope) {
    var root = scope || document;
    var buttons = root.querySelectorAll("[data-nav][data-target]");
    buttons.forEach(function (b) {
      b.addEventListener("click", function () {
        var target = b.getAttribute("data-target");
        var stage = b.getAttribute("data-stage");
        showScreen(target, stage);
        if (target === "screen-scr-002") renderScr002();
      });
    });
  }

  function renderAll() {
    renderScr002();
  }

  // ---- QA panel wiring ----

  function wireQaPanel() {
    el("qa-toggle").addEventListener("click", function () {
      var body = el("qa-body");
      var expanded = !body.classList.contains("qa-hidden");
      body.classList.toggle("qa-hidden");
      el("qa-toggle").setAttribute("aria-expanded", String(!expanded));
    });

    var qaButtons = document.querySelectorAll("[data-qa]");
    qaButtons.forEach(function (b) {
      b.addEventListener("click", function () {
        var qa = b.getAttribute("data-qa");

        if (qa === "incoming-ok" || qa === "incoming-no-instance" || qa === "incoming-not-passed") {
          state.incomingContext = qa;
          state.qaOverride = null;
          updateContextBar();
          showScreen("screen-scr-002");
          renderScr002();
          return;
        }

        if (qa === "scr002-loading") {
          state.qaOverride = "scr002-loading";
          showScreen("screen-scr-002");
          renderScr002();
          return;
        }
        if (qa === "scr002-normal") {
          state.qaOverride = null;
          showScreen("screen-scr-002");
          renderScr002();
          return;
        }

        if (qa === "view003-match" || qa === "view003-mismatch" || qa === "view003-indeterminate") {
          state.parityOutcome = qa.replace("view003-", "");
          showScreen("screen-view-003");
          renderView003();
        }
      });
    });

    el("qa-reset").addEventListener("click", function () {
      state.incomingContext = "incoming-ok";
      state.selectedCursor = "C-001";
      state.qaOverride = null;
      state.parityOutcome = "match";
      updateContextBar();
      showScreen("screen-scr-002");
      renderAll();
    });
  }

  // ---- Init ----

  function init() {
    wireGlobalNav(document);
    wireQaPanel();
    updateContextBar();
    renderAll();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
