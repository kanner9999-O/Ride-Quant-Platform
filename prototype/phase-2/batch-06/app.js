/*
 * Ride — Phase 2 Prototype — Batch 06 (Improve / new strategy version / instance registration /
 * version comparison / old-version evidence access).
 *
 * Illustrative, non-authoritative UI logic only. No real backend, no real persistent storage, no
 * network calls, no credentials. Every displayed value below is mock/static/deterministic OR a
 * bounded prototype-local record created by clicking a control in this page — never a claim of
 * production authoritative persistence. This is a separate, self-contained page from Batch
 * 01/02/03/04/05 — it does NOT share live JS state with any of them.
 *
 * INV-1 (new version = new immutable identity): buildNewVersion() below NEVER mutates
 * VERSION_FIXTURES in place — it always creates a new object with a new id, pushed into
 * state.createdVersions. The old version stays exactly as it was, independently resolvable.
 *
 * INV-2 (no invented Strategy Definition schema): every field on a version object below is one
 * of exactly the eight current strategy.md §1 StrategyDefinitionVersionRegistered payload fields
 * (strategy_definition_version_id, strategy_definition_id, thesis, supported_scope,
 * required_input_contracts, decision_rule_ref, explanation_contract_ref,
 * downstream_output_capability) — no DSL, compiler, validation taxonomy, version graph, or
 * approval workflow is modeled.
 *
 * INV-3 (VIEW-006 is not VIEW-001): registerInstance() below only creates a
 * StrategyInstanceRegistered-shaped record (strategy.md §5/§6) — it never sets a "pinned for
 * Replay/Backtest/Paper" flag anywhere. That remains VIEW-001's exclusive responsibility
 * (represented here only as a real link to ../batch-01/, never re-authored).
 *
 * INV-4 (comparison keeps evidence families separate): renderComparisonSide() below never merges
 * a Backtest evidence object with a PAPER evidence object into one structure — each side resolves
 * independently from EVIDENCE[instanceId].backtest or EVIDENCE[instanceId].paper, rendered into
 * its own panel with its own mode/authority labels. No score/ranking function exists anywhere in
 * this file.
 *
 * INV-5 (old-version evidence stays accessible): VIEW-005 below always renders the old version's
 * identity first, then resolves each family independently — an unavailable family never blanks
 * out the version identity or the other family.
 *
 * INV-6 (registration vs inspection): only buildNewVersion()/registerInstance() create new
 * prototype-local records; every SCR-011/VIEW-005 render function is read-only — it only reads
 * VERSION_FIXTURES/INSTANCE_FIXTURES/EVIDENCE and state.*, never writes a new version/instance.
 *
 * Traceability for every element rendered here is pinned in traceability.md — this file does not
 * introduce any UC/PR/domain concept that is not already Consolidated Stable in
 * docs/product/ux-blueprint.md, docs/product/use-case-workflow.md, or docs/domain/strategy.md.
 */

(function () {
  "use strict";

  // ---- Mock data (illustrative only, not authoritative financial data) ----

  var MOCK_ACCOUNT_CONTEXT = {
    account: "Ride Internal Account",
    instrument: "BTC/USDT",
    venue: "Binance"
  };

  var STRATEGY_DEFINITION_ID = "sd-fam-001";

  // ---- Strategy Definition Version fixtures (strategy.md §1) ----
  //
  // VERSION_FIXTURES is never mutated in place (INV-1) — SCR-010's creation action only ever
  // pushes a brand-new object into state.createdVersions (see buildNewVersion()). Both fixtures
  // below pre-exist this batch's own session and are immutable for the lifetime of the page.
  var VERSION_FIXTURES = {
    // "Old / no-longer-current" version for this batch's UC-020/UC-021 demo — the Instance bound
    // to it (INSTANCE_FIXTURES["inst-old-001"]) is illustratively RETIRED (a genuine
    // strategy.md §5 Strategy Instance lifecycle value) — the Version itself is NOT invalidated
    // (versions are never invalidated merely for being superseded, strategy.md §1); "no longer
    // active" here is product-level description of the RETIRED Instance using it, not a fake
    // "active" field bolted onto the Version.
    "sdv-v0.9": {
      strategyDefinitionVersionId: "sdv-v0.9",
      strategyDefinitionId: STRATEGY_DEFINITION_ID,
      thesis: "Mean-reversion trên BTC/USDT khi RSI(14) dưới 30 (illustrative, phiên bản đầu)",
      supportedScope: "mean-reversion trên crypto major liquid pairs",
      requiredInputContracts: ["candle-context-v1"],
      decisionRuleRef: "rule-rsi-meanrev-v1",
      explanationContractRef: "expl-v1",
      downstreamOutputCapability: "trade-intent-capable"
    },
    // Current baseline version — pre-existing before this batch's own SCR-010 creation flow.
    "sdv-v1.0": {
      strategyDefinitionVersionId: "sdv-v1.0",
      strategyDefinitionId: STRATEGY_DEFINITION_ID,
      thesis: "Trend-following trên BTC/USDT khi candle đóng cửa vượt EMA(20) (illustrative)",
      supportedScope: "trend-following trên crypto major liquid pairs",
      requiredInputContracts: ["candle-context-v1", "reference-context-v1"],
      decisionRuleRef: "rule-ema-cross-v1",
      explanationContractRef: "expl-v1",
      downstreamOutputCapability: "trade-intent-capable"
    }
  };

  // ---- Strategy Instance fixtures (strategy.md §5/§6) ----
  var INSTANCE_FIXTURES = {
    "inst-old-001": {
      strategyInstanceId: "inst-old-001",
      strategyDefinitionVersionRef: "sdv-v0.9",
      pluginVersionRef: "plugin-v1",
      configurationVersionRef: "cfg-v1",
      packageBuildArtifactRef: "build-9f21ac0",
      accountId: "acct-001",
      instrumentSelectionRef: { instrument_id: "BTC", venue_id: "binance", listing_id: "BTC-USDT-BINANCE" },
      displayName: "Instance OLD (RSI mean-reversion)",
      status: "RETIRED"
    },
    "inst-a": {
      strategyInstanceId: "inst-a",
      strategyDefinitionVersionRef: "sdv-v1.0",
      pluginVersionRef: "plugin-v1",
      configurationVersionRef: "cfg-v3",
      packageBuildArtifactRef: "build-65000ab",
      accountId: "acct-001",
      instrumentSelectionRef: { instrument_id: "BTC", venue_id: "binance", listing_id: "BTC-USDT-BINANCE" },
      displayName: "Instance A (current, EMA trend-following)",
      status: "ACTIVE"
    }
  };

  // ---- Evidence fixtures — two families, always kept as separate objects (INV-4) ----
  //
  // "inst-old-001" carries BOTH families on purpose (a single coherent fixture, per task
  // guidance) so VIEW-005's "both families" (C) and STATE-025/026 toggle have a real basis — its
  // PAPER family's Fill/Position resolvability is controlled by state.oldVersionPaperFillAvailable
  // (STATE-026 QA toggle) so SCR-011 and VIEW-005 always agree (same underlying flag, never two
  // independent copies).
  var EVIDENCE = {
    "inst-old-001": {
      backtest: {
        runId: "BT-OLD-001",
        versionId: "sdv-v0.9",
        decision: { id: "PD-BT-OLD-001", outcome: "LONG" },
        riskEvaluation: { id: "RE-BT-OLD-001", result: "APPROVED" },
        economicEvidence: { simulatedPnl: "+1.40%", simulatedTrades: 9 },
        exposureProgression: "FLAT → LONG → FLAT (illustrative path)",
        evaluableResult: "EVALUABLE"
      },
      paper: {
        decision: { id: "PD-PP-OLD-001", outcome: "LONG" },
        tradeIntent: { id: "TI-PP-OLD-001" },
        riskEvaluation: { id: "RE-PP-OLD-001", result: "APPROVED" },
        executionIntent: { id: "EI-PP-OLD-001", status: "ISSUED" },
        order: { id: "ORD-PP-OLD-001", environment: "PAPER" },
        executionResult: { id: "ER-PP-OLD-001", resultType: "EXECUTED" }
        // fill/position deliberately absent here — resolved conditionally at render time from
        // state.oldVersionPaperFillAvailable, never fabricated when unavailable.
      }
    },
    "inst-a": {
      backtest: {
        runId: "BT-A-001",
        versionId: "sdv-v1.0",
        decision: { id: "PD-BT-A-001", outcome: "LONG" },
        riskEvaluation: { id: "RE-BT-A-001", result: "APPROVED" },
        economicEvidence: { simulatedPnl: "+3.20%", simulatedTrades: 14 },
        exposureProgression: "FLAT → LONG → FLAT → LONG (illustrative path)",
        evaluableResult: "EVALUABLE"
      },
      paper: {
        decision: { id: "PD-PP-A-001", outcome: "LONG" },
        tradeIntent: { id: "TI-PP-A-001" },
        riskEvaluation: { id: "RE-PP-A-001", result: "APPROVED" },
        executionIntent: { id: "EI-PP-A-001", status: "ISSUED" },
        order: { id: "ORD-PP-A-001", environment: "PAPER" },
        executionResult: { id: "ER-PP-A-001", resultType: "EXECUTED" },
        fill: { id: "FILL-PP-A-001", direction: "LONG", quantity: "0.50", quantityUnit: "BTC", price: "65000.00", priceCurrency: "USDT" },
        position: { status: "EVALUABLE", direction: "LONG", netQuantity: "0.50", quantityUnit: "BTC" }
      }
    }
    // newly registered instances (state.registeredInstances) intentionally have NO key here —
    // renderEvidenceSide() treats a missing entry as "no outcome yet," never an error.
  };

  // ---- Demo/UI state (prototype-local only, not a domain/session/replay state) ----

  var state = {
    activeScreen: "scr-010", // "scr-010" | "view-006" | "scr-011" | "view-005"
    // SCR-010 — editable illustrative content for the NEXT version to create.
    formThesis: "Trend-following trên BTC/USDT khi candle đóng cửa vượt EMA(20), thắt chặt lọc theo volatility (illustrative v1.1 draft)",
    formSupportedScope: "trend-following trên crypto major liquid pairs (volatility-filtered)",
    createdVersions: [], // array of version objects created this session (append-only, INV-1)
    versionCounter: 1, // next created version suffix (sdv-v1.1, v1.2, ...)
    // VIEW-006 — per-created-version registration state.
    registrationByVersionId: {}, // versionId -> instance object once registered
    instanceCounter: 1, // next registered instance suffix (inst-b-1, inst-b-2, ...)
    // SCR-011 — comparison side selections.
    sideA: { instanceId: null, mode: null },
    sideB: { instanceId: null, mode: null },
    // VIEW-005 — mode selector + entry context.
    view005Mode: null, // null | "backtest" | "paper" | "both"
    view005EntryNote: null,
    // QA/demo-only toggles.
    oldVersionPaperFillAvailable: true, // STATE-025 (true) / STATE-026 (false) for inst-old-001's PAPER family
    scr011EvidenceExists: true // NAV-006 required-context toggle for SCR-011 (Family D)
  };

  function allInstances() {
    var map = {};
    Object.keys(INSTANCE_FIXTURES).forEach(function (id) { map[id] = INSTANCE_FIXTURES[id]; });
    Object.keys(state.registrationByVersionId).forEach(function (vId) {
      var inst = state.registrationByVersionId[vId];
      map[inst.strategyInstanceId] = inst;
    });
    return map;
  }

  function latestCreatedVersion() {
    if (state.createdVersions.length === 0) return null;
    return state.createdVersions[state.createdVersions.length - 1];
  }

  // ---- Helpers ----

  function el(id) { return document.getElementById(id); }

  function el5(name, value) {
    return '<div class="evidence-row"><span class="evidence-label">' + name + '</span><span class="evidence-value">' + value + "</span></div>";
  }

  function showScreen(targetId) {
    var screens = document.querySelectorAll(".screen");
    screens.forEach(function (s) { s.classList.add("screen-hidden"); });
    el(targetId).classList.remove("screen-hidden");

    var navButtons = document.querySelectorAll(".nav-btn");
    navButtons.forEach(function (b) { b.classList.remove("nav-btn-active"); });
    var navImprove = document.querySelector('[data-nav="NAV-006"]');
    if (navImprove && targetId === "screen-improve") navImprove.classList.add("nav-btn-active");
  }

  // ---- Improve section rendering (NAV-006 destination: SCR-010 + VIEW-006 + SCR-011 + VIEW-005) ----

  function renderImproveSection() {
    document.querySelectorAll("#improve-subtabs [data-subtab]").forEach(function (btn) {
      btn.classList.toggle("subtab-btn-active", btn.getAttribute("data-subtab") === state.activeScreen);
    });
    el("scr-010-body").classList.toggle("screen-hidden", state.activeScreen !== "scr-010");
    el("view-006-body").classList.toggle("screen-hidden", state.activeScreen !== "view-006");
    el("scr-011-body").classList.toggle("screen-hidden", state.activeScreen !== "scr-011");
    el("view-005-body").classList.toggle("screen-hidden", state.activeScreen !== "view-005");

    if (state.activeScreen === "scr-010") renderScr010();
    else if (state.activeScreen === "view-006") renderView006();
    else if (state.activeScreen === "scr-011") renderScr011();
    else renderView005();
  }

  function goToImproveTab(tab) {
    state.activeScreen = tab;
    showScreen("screen-improve");
    renderImproveSection();
  }

  // ---- SCR-010 — Strategy Definition Version Creation (UC-019) ----

  function renderScr010() {
    var body = el("scr-010-body");
    var oldVersion = VERSION_FIXTURES["sdv-v1.0"];

    var html = '<div class="label-row">' +
      '<span class="mode-label">Improve</span>' +
      '<span class="authority-label authority-label-authoritative">Represented authority class: authoritative Strategy registration</span>' +
      '<span class="prototype-datum-label">Prototype datum: Illustrative / non-authoritative</span>' +
      "</div>" +
      '<div class="evidence-group evidence-group-upstream">' +
      '<div class="evidence-group-label">Existing Strategy Definition + current version (required context)</div>' +
      el5("strategy_definition_id (family)", STRATEGY_DEFINITION_ID) +
      el5("Existing strategy_definition_version_id", oldVersion.strategyDefinitionVersionId) +
      el5("thesis", oldVersion.thesis) +
      el5("supported_scope", oldVersion.supportedScope) +
      el5("required_input_contracts", oldVersion.requiredInputContracts.join(", ")) +
      el5("decision_rule_ref", oldVersion.decisionRuleRef) +
      el5("explanation_contract_ref", oldVersion.explanationContractRef) +
      el5("downstream_output_capability", oldVersion.downstreamOutputCapability) +
      "</div>" +
      '<div class="field-row">' +
      '<label>thesis (new version — editable, illustrative)</label>' +
      '<textarea class="ta" id="scr010-thesis" rows="2">' + state.formThesis + "</textarea>" +
      "</div>" +
      '<div class="field-row">' +
      '<label>supported_scope (new version — editable, illustrative)</label>' +
      '<input class="ta" id="scr010-scope" type="text" value="' + state.formSupportedScope + '">' +
      "</div>" +
      '<div class="hint">required_input_contracts/decision_rule_ref/explanation_contract_ref/downstream_output_capability for the new version use fixed illustrative values below — only thesis/supported_scope are user-editable in this bounded prototype. No Strategy Definition field beyond these eight (the exact current strategy.md §1 StrategyDefinitionVersionRegistered payload fields) exists anywhere in this file.</div>' +
      '<div class="exit-row"><button class="btn btn-primary" id="btn-create-version">Create Strategy Definition Version</button></div>' +
      '<div id="scr010-result"></div>';
    body.innerHTML = html;

    el("scr010-thesis").addEventListener("input", function (e) { state.formThesis = e.target.value; });
    el("scr010-scope").addEventListener("input", function (e) { state.formSupportedScope = e.target.value; });
    el("btn-create-version").addEventListener("click", function () {
      buildNewVersion();
      renderScr010Result();
    });

    renderScr010Result();
  }

  // System-owned action (UC-019 step 2): assigns a NEW immutable version identity, distinct from
  // sdv-v1.0 and from every previously created version — NEVER edits VERSION_FIXTURES or any
  // element of state.createdVersions already pushed (INV-1, append-only).
  function buildNewVersion() {
    var newId = "sdv-v1." + state.versionCounter;
    state.versionCounter += 1;
    var v = {
      strategyDefinitionVersionId: newId,
      strategyDefinitionId: STRATEGY_DEFINITION_ID,
      thesis: state.formThesis,
      supportedScope: state.formSupportedScope,
      requiredInputContracts: ["candle-context-v1", "reference-context-v1", "volatility-context-v1"],
      decisionRuleRef: "rule-ema-cross-v2",
      explanationContractRef: "expl-v1",
      downstreamOutputCapability: "trade-intent-capable"
    };
    state.createdVersions.push(v);
  }

  function renderScr010Result() {
    var box = el("scr010-result");
    if (!box) return;
    var v = latestCreatedVersion();
    if (!v) { box.innerHTML = ""; return; }
    var oldVersion = VERSION_FIXTURES["sdv-v1.0"];
    box.innerHTML = '<div class="panel panel-passed">' +
      '<div class="panel-title">New Strategy Definition Version created — distinct, independent identity</div>' +
      el5("New strategy_definition_version_id", v.strategyDefinitionVersionId) +
      el5("strategy_definition_id (same family)", v.strategyDefinitionId) +
      el5("thesis", v.thesis) +
      el5("supported_scope", v.supportedScope) +
      '<div class="hint">Old version ' + oldVersion.strategyDefinitionVersionId + ' is UNCHANGED and still independently resolvable — see the "Existing Strategy Definition + current version" panel above, which reads directly from the same unmutated fixture object.</div>' +
      '<div class="exit-row">' +
      '<button class="btn btn-primary" id="btn-scr010-to-view006">Register a Strategy Instance for this new version (VIEW-006) →</button>' +
      '<button class="btn" id="btn-scr010-to-scr011">Compare with older versions (SCR-011) →</button>' +
      '<a class="btn" href="../batch-01/index.html">Open Research (SCR-001) read-only, optional →</a>' +
      '<p class="hint">The exact version above is the one handed to VIEW-006 — no unrelated fixture is generated there.</p>' +
      "</div></div>";
    el("btn-scr010-to-view006").addEventListener("click", function () { goToImproveTab("view-006"); });
    el("btn-scr010-to-scr011").addEventListener("click", function () { goToImproveTab("scr-011"); });
  }

  // ---- VIEW-006 — Strategy Instance Creation/Binding (UC-019 handoff, UC-002 downstream) ----

  function renderView006() {
    var body = el("view-006-body");
    var target = latestCreatedVersion();

    // Required context: a new Strategy Definition Version created through SCR-010 must exist.
    // "registration unavailable" — four-part fallback (stop, disclose reason, preserve available
    // identity, no authoritative action) — no new STATE-XXX invented, per instruction.
    if (!target) {
      body.innerHTML = '<div class="label-row">' +
        '<span class="mode-label">Improve</span>' +
        '<span class="prototype-datum-label">Prototype datum: Illustrative / non-authoritative</span>' +
        "</div>" +
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">Registration unavailable</div>' +
        "<div>No Strategy Definition Version created through SCR-010 exists yet in this session — " +
        "the required context for Instance registration is absent. Workflow stops here; no Strategy " +
        "Instance is created. Existing Strategy Definition identity: " + STRATEGY_DEFINITION_ID + " — " +
        "this is the only identity available right now.</div>" +
        '<div class="exit-row"><button class="btn" id="btn-view006-to-scr010">Go to Strategy Definition Version Creation (SCR-010) →</button></div>' +
        "</div>";
      el("btn-view006-to-scr010").addEventListener("click", function () { goToImproveTab("scr-010"); });
      return;
    }

    var existingInstance = state.registrationByVersionId[target.strategyDefinitionVersionId];
    var html = '<div class="label-row">' +
      '<span class="mode-label">Improve</span>' +
      '<span class="authority-label authority-label-authoritative">Represented authority class: authoritative Strategy registration</span>' +
      '<span class="prototype-datum-label">Prototype datum: Illustrative / non-authoritative</span>' +
      "</div>" +
      el5("Strategy Definition identity", STRATEGY_DEFINITION_ID) +
      el5("New Strategy Definition Version", target.strategyDefinitionVersionId) +
      '<div class="hint">A SEPARATE new Strategy Instance will be registered, bound to EXACTLY this version — not a selection/pin for Replay/Backtest/Paper, and not a reuse of any existing Instance identity.</div>';

    if (existingInstance) {
      html += '<div class="panel panel-passed">' +
        '<div class="panel-title">Registration completed</div>' +
        el5("New Strategy Instance identity", existingInstance.strategyInstanceId) +
        el5("Bound Strategy Definition Version (explicit binding)", existingInstance.strategyInstanceId + " → " + existingInstance.strategyDefinitionVersionRef) +
        el5("account_id", existingInstance.accountId) +
        el5("instrument_selection_ref", existingInstance.instrumentSelectionRef.instrument_id + " / " + existingInstance.instrumentSelectionRef.venue_id + " / " + existingInstance.instrumentSelectionRef.listing_id) +
        '<div class="hint">Distinct from the pre-existing Instance ' + INSTANCE_FIXTURES["inst-a"].strategyInstanceId + ' — old and new Strategy Instance identities are never merged or reused.</div>' +
        '<div class="exit-row">' +
        '<a class="btn btn-primary" href="../batch-01/index.html">Instance is now available to select/pin through VIEW-001 →</a>' +
        '<p class="hint">This is NOT a claim that the Instance is now pinned — no Replay pin, Backtest pin, or Paper pin is created here. VIEW-001 owns that separate, bounded interaction.</p>' +
        "</div></div>";
    } else {
      html += '<div class="exit-row"><button class="btn btn-primary" id="btn-register-instance">Register Strategy Instance for this Version</button></div>';
    }
    body.innerHTML = html;

    var btn = el("btn-register-instance");
    if (btn) {
      btn.addEventListener("click", function () {
        registerInstance(target);
        renderView006();
      });
    }
  }

  // System-owned action (VIEW-006): registers a brand-new Strategy Instance identity, distinct
  // from every existing Instance, bound to exactly the target version. Never mutates
  // INSTANCE_FIXTURES; never sets a Replay/Backtest/Paper pin flag anywhere (INV-3).
  function registerInstance(targetVersion) {
    var newId = "inst-b-" + state.instanceCounter;
    state.instanceCounter += 1;
    var inst = {
      strategyInstanceId: newId,
      strategyDefinitionVersionRef: targetVersion.strategyDefinitionVersionId,
      pluginVersionRef: "plugin-v1",
      configurationVersionRef: "cfg-v3",
      packageBuildArtifactRef: "build-65000ab",
      accountId: "acct-001",
      instrumentSelectionRef: { instrument_id: "BTC", venue_id: "binance", listing_id: "BTC-USDT-BINANCE" },
      displayName: "Instance " + newId + " (newly registered)",
      status: "ACTIVE"
    };
    state.registrationByVersionId[targetVersion.strategyDefinitionVersionId] = inst;
  }

  // ---- SCR-011 — Strategy Version Comparison (UC-020) ----

  function renderScr011() {
    var body = el("scr-011-body");

    // STATE-002 (canonical row, ux-blueprint.md §11 explicitly lists SCR-011 — "dưới hai
    // Strategy Instance đã đăng ký để so sánh") — required context: at least two Strategy
    // Instances bound to different Strategy Definition Versions.
    var instances = allInstances();
    var count = Object.keys(instances).length;
    if (!state.scr011EvidenceExists || count < 2) {
      body.innerHTML = '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-002 — empty</div>' +
        "<div>Fewer than two Strategy Instances bound to different Strategy Definition Versions " +
        "are available to compare. No comparison is invented to fill the gap.</div>" +
        "</div>";
      return;
    }

    var html = '<div class="label-row">' +
      '<span class="mode-label">Improve</span>' +
      '<span class="authority-label authority-label-recomputation">Read-only / non-authoritative comparison presentation</span>' +
      '<span class="prototype-datum-label">Prototype datum: Illustrative / non-authoritative</span>' +
      "</div>" +
      "<div class=\"hint\">Choose a Strategy Instance + mode independently for each side. Same mode on both sides = Backtest-vs-Backtest or PAPER-vs-PAPER; different modes = cross-mode side-by-side. Evidence families are never merged, normalized, or scored together.</div>" +
      '<div class="compare-grid">' +
      renderSideSelector("A", instances) +
      renderSideSelector("B", instances) +
      "</div>" +
      '<div id="scr011-pair-status"></div>' +
      '<div class="compare-grid" id="scr011-panels">' +
      '<div id="scr011-side-a"></div>' +
      '<div id="scr011-side-b"></div>' +
      "</div>";
    body.innerHTML = html;

    wireSideSelector("A", instances);
    wireSideSelector("B", instances);
    renderScr011Panels();
  }

  // v1.1 (closes P2-B06-A-MAJ-02): UC-020 requires the two compared Strategy Instances to be
  // bound to two DIFFERENT Strategy Definition Versions — same Instance selected twice, or two
  // different Instances that happen to bind the SAME version, must never render as a valid
  // comparison. Mode difference does NOT waive this requirement (it is evaluated before mode is
  // even considered). Returns {ready:false} while either side is still missing a selection;
  // {ready:true, valid:false, reason} when both sides are selected but the pair is ineligible;
  // {ready:true, valid:true} when the pair is a genuine two-different-version comparison.
  function comparisonPairValidity() {
    if (!state.sideA.instanceId || !state.sideA.mode || !state.sideB.instanceId || !state.sideB.mode) {
      return { ready: false };
    }
    var instances = allInstances();
    var instA = instances[state.sideA.instanceId];
    var instB = instances[state.sideB.instanceId];
    if (state.sideA.instanceId === state.sideB.instanceId) {
      return {
        ready: true, valid: false,
        reason: "Both sides select the same Strategy Instance (" + instA.strategyInstanceId + ")."
      };
    }
    if (instA.strategyDefinitionVersionRef === instB.strategyDefinitionVersionRef) {
      return {
        ready: true, valid: false,
        reason: "Both selected Strategy Instances are bound to the same Strategy Definition Version (" + instA.strategyDefinitionVersionRef + ")."
      };
    }
    return { ready: true, valid: true };
  }

  // v1.1 (MỚI, closes P2-B06-A-MAJ-02): single entry point that re-evaluates pair validity
  // fresh, THEN renders the shared pair-status panel and both sides together — called on every
  // side/mode selection change so no stale panel from a previously-valid pair can persist.
  function renderScr011Panels() {
    renderPairStatus();
    renderComparisonSide("A");
    renderComparisonSide("B");
  }

  function renderPairStatus() {
    var box = el("scr011-pair-status");
    if (!box) return;
    var v = comparisonPairValidity();
    if (!v.ready || v.valid) { box.innerHTML = ""; return; }
    box.innerHTML = '<div class="panel panel-blocked">' +
      '<div class="panel-title">Not a valid comparison pair</div>' +
      "<div>" + v.reason + " Strategy Version Comparison requires two different Strategy " +
      "Definition Versions. Selected identities/context are shown below for reference — no " +
      "comparison evidence is rendered until the selection changes.</div></div>";
  }

  function renderSideSelector(side, instances) {
    var instOptions = Object.keys(instances).map(function (id) {
      return '<option value="' + id + '">' + instances[id].displayName + " (" + id + ")</option>";
    }).join("");
    return '<div class="compare-column">' +
      '<div class="evidence-group-label">Side ' + side + '</div>' +
      '<div class="field-row"><label>Strategy Instance</label><select class="sel" id="scr011-inst-' + side + '"><option value="">— choose —</option>' + instOptions + "</select></div>" +
      '<div class="field-row"><label>Mode</label><select class="sel" id="scr011-mode-' + side + '">' +
      '<option value="">— choose —</option>' +
      '<option value="backtest">Backtest (non-PAPER simulated)</option>' +
      '<option value="paper">PAPER (authoritative where source facts are authoritative)</option>' +
      "</select></div>" +
      "</div>";
  }

  function wireSideSelector(side, instances) {
    var stateSide = side === "A" ? state.sideA : state.sideB;
    el("scr011-inst-" + side).value = stateSide.instanceId || "";
    el("scr011-mode-" + side).value = stateSide.mode || "";
    el("scr011-inst-" + side).addEventListener("change", function (e) {
      stateSide.instanceId = e.target.value || null;
      renderScr011Panels();
    });
    el("scr011-mode-" + side).addEventListener("change", function (e) {
      stateSide.mode = e.target.value || null;
      renderScr011Panels();
    });
  }

  function renderComparisonSide(side) {
    var box = el("scr011-side-" + side);
    if (!box) return;
    var stateSide = side === "A" ? state.sideA : state.sideB;
    if (!stateSide.instanceId || !stateSide.mode) {
      box.innerHTML = '<div class="hint">Select an Instance and a mode for Side ' + side + ".</div>";
      return;
    }
    var instances = allInstances();
    var inst = instances[stateSide.instanceId];
    var famData = EVIDENCE[stateSide.instanceId];

    var header = '<div class="label-row">' +
      '<span class="mode-label">' + (stateSide.mode === "backtest" ? "Backtest" : "PAPER") + "</span>" +
      '<span class="authority-label ' + (stateSide.mode === "backtest" ? "authority-label-recomputation" : "authority-label-authoritative") + '">' +
      (stateSide.mode === "backtest" ? "Authority: non-PAPER simulated" : "Authority: authoritative PAPER") + "</span>" +
      "</div>" +
      el5("Strategy Instance", inst.displayName + " (" + inst.strategyInstanceId + ")") +
      el5("Strategy Definition Version", inst.strategyDefinitionVersionRef);

    // v1.1 (closes P2-B06-A-MAJ-02): identity/context above is ALWAYS shown, but comparison
    // evidence is withheld entirely when the pair is not eligible (same Instance both sides, or
    // two Instances bound to the same Version) — the shared #scr011-pair-status panel discloses
    // why. This never invents a new STATE-XXX; it is a plain guard before rendering evidence.
    var pairValidity = comparisonPairValidity();
    if (pairValidity.ready && !pairValidity.valid) {
      box.innerHTML = header + '<div class="hint">Comparison evidence is not shown for this side until both sides are bound to two different Strategy Definition Versions.</div>';
      return;
    }

    var oldVersionNote = "";
    if (inst.status === "RETIRED") {
      oldVersionNote = '<div class="exit-row"><button class="btn" id="btn-scr011-to-view005-' + side + '">This Instance’s version (' + inst.strategyDefinitionVersionRef + ') is not active (Instance RETIRED) — inspect full old-version evidence in VIEW-005 →</button></div>';
    }

    var famObj = famData ? famData[stateSide.mode] : null;
    var body;
    if (!famObj) {
      body = '<div class="panel panel-blocked"><div class="panel-title">No outcome yet</div>' +
        "<div>" + inst.displayName + " has no " + (stateSide.mode === "backtest" ? "Backtest" : "PAPER") +
        " outcome recorded — empty for this Instance only, the other side is unaffected.</div></div>";
    } else if (stateSide.mode === "backtest") {
      body = renderBacktestFamilyHtml(famObj);
    } else {
      body = renderPaperFamilyHtml(famObj, stateSide.instanceId === "inst-old-001" ? state.oldVersionPaperFillAvailable : true);
    }
    box.innerHTML = header + body + oldVersionNote;
    var v5btn = el("btn-scr011-to-view005-" + side);
    if (v5btn) {
      v5btn.addEventListener("click", function () {
        state.view005EntryNote = "Opened from SCR-011, Side " + side + " (" + inst.strategyInstanceId + ")";
        goToImproveTab("view-005");
      });
    }
  }

  function renderBacktestFamilyHtml(bt) {
    return '<div class="panel">' +
      el5("Run identity", bt.runId) +
      el5("Decision / RiskEvaluation trace", bt.decision.id + " (" + bt.decision.outcome + ") / " + bt.riskEvaluation.id + " (" + bt.riskEvaluation.result + ")") +
      el5("Simulated economic evidence", bt.economicEvidence.simulatedPnl + " over " + bt.economicEvidence.simulatedTrades + " simulated trades") +
      el5("Exposure/position progression", bt.exposureProgression) +
      el5("Strategy-level evaluable result", bt.evaluableResult) +
      '<div class="hint">Non-PAPER simulated — never labelled authoritative ExecutionResult/Fill/Position.</div>' +
      "</div>";
  }

  function renderPaperFamilyHtml(pp, fillAvailable) {
    var html = '<div class="panel">' +
      el5("Decision / Trade Intent / RiskEvaluation", pp.decision.id + " (" + pp.decision.outcome + ") / " + pp.tradeIntent.id + " / " + pp.riskEvaluation.id + " (" + pp.riskEvaluation.result + ")") +
      el5("Execution Intent / Order", pp.executionIntent.id + " (" + pp.executionIntent.status + ") / " + pp.order.id + " (" + pp.order.environment + ")") +
      el5("ExecutionResult", pp.executionResult.id + " (" + pp.executionResult.resultType + ")");
    if (fillAvailable && pp.fill) {
      html += el5("Fill", pp.fill.id + " (" + pp.fill.direction + ", " + pp.fill.quantity + " " + pp.fill.quantityUnit + " @ " + pp.fill.price + " " + pp.fill.priceCurrency + ")") +
        el5("Position", pp.position.status + " " + (pp.position.direction || "") + " " + (pp.position.netQuantity || "") + " " + (pp.position.quantityUnit || ""));
    } else {
      html += '<div class="panel panel-blocked" style="margin-top:8px;">' +
        '<div class="panel-title">Fill / Position — incomplete</div>' +
        "<div>Fill and Position evidence for this ExecutionResult are not resolvable in this bounded " +
        "prototype (illustrative unavailability, not a claim about real retention). Reason: simulated " +
        "STATE-026 old-version evidence gap. Everything else above remains visible.</div></div>";
    }
    html += "</div>";
    return html;
  }

  // ---- VIEW-005 — Old-Version Evidence Access (UC-021) ----

  function renderView005() {
    var body = el("view-005-body");
    var oldInstance = INSTANCE_FIXTURES["inst-old-001"];
    var oldVersion = VERSION_FIXTURES[oldInstance.strategyDefinitionVersionRef];
    var famData = EVIDENCE[oldInstance.strategyInstanceId];

    var html = '<div class="label-row">' +
      '<span class="mode-label">Improve</span>' +
      '<span class="prototype-datum-label">Prototype datum: Illustrative / non-authoritative</span>' +
      "</div>" +
      (state.view005EntryNote ? '<div class="hint">' + state.view005EntryNote + " — same Strategy Definition Version identity preserved.</div>" : "") +
      el5("Strategy Definition Version identity (always visible)", oldVersion.strategyDefinitionVersionId) +
      el5("strategy_definition_id (family)", oldVersion.strategyDefinitionId) +
      el5("Bound Instance status", oldInstance.strategyInstanceId + " — " + oldInstance.status + " (no longer active)") +
      '<div class="field-row"><label>Mode to resolve</label><div class="chip-row" id="view005-mode-selector">' +
      '<button class="btn subtab-btn" data-mode="backtest">Backtest only</button>' +
      '<button class="btn subtab-btn" data-mode="paper">PAPER only</button>' +
      '<button class="btn subtab-btn" data-mode="both">Both</button>' +
      "</div></div>" +
      '<div id="view005-families"></div>' +
      '<div class="exit-row"><button class="btn" id="btn-view005-to-scr011">← Return to Version Comparison (SCR-011)</button></div>';
    body.innerHTML = html;

    body.querySelectorAll("[data-mode]").forEach(function (btn) {
      btn.classList.toggle("subtab-btn-active", btn.getAttribute("data-mode") === state.view005Mode);
      btn.addEventListener("click", function () {
        state.view005Mode = btn.getAttribute("data-mode");
        body.querySelectorAll("[data-mode]").forEach(function (b2) {
          b2.classList.toggle("subtab-btn-active", b2 === btn);
        });
        renderView005Families(famData);
      });
    });
    el("btn-view005-to-scr011").addEventListener("click", function () {
      state.view005EntryNote = null;
      goToImproveTab("scr-011");
    });

    renderView005Families(famData);
  }

  // v1.1 (closes P2-B06-A-MAJ-01): completeness is derived from the REQUESTED mode plus the
  // availability of evidence that mode actually needs — NOT from a single global boolean read
  // regardless of what was requested. Backtest evidence for inst-old-001 is always fully
  // resolvable in this bounded prototype; only the PAPER family's Fill/Position is ever toggled
  // unavailable (state.oldVersionPaperFillAvailable). So "Backtest only" is complete even when
  // PAPER Fill/Position is unavailable, "PAPER only"/"Both" are complete only when it is
  // available. STATE-026 is therefore never synonymous with "PAPER Fill missing" in the
  // abstract — it only applies when the missing evidence actually falls within what was asked
  // for.
  function oldVersionEvidenceComplete(mode) {
    if (mode === "backtest") return true;
    return state.oldVersionPaperFillAvailable; // "paper" or "both" — both need the PAPER family
  }

  function renderView005Families(famData) {
    var box = el("view005-families");
    if (!box) return;
    if (!state.view005Mode) {
      box.innerHTML = '<div class="hint">Choose a mode above to resolve evidence.</div>';
      return;
    }
    var mode = state.view005Mode;
    var html = "";
    if (mode === "backtest" || mode === "both") {
      html += '<div class="evidence-group evidence-group-downstream">' +
        '<div class="evidence-group-label">Backtest evidence family (non-PAPER)</div>' +
        renderBacktestFamilyHtml(famData.backtest) +
        "</div>";
    }
    if (mode === "paper" || mode === "both") {
      html += '<div class="evidence-group evidence-group-upstream">' +
        '<div class="evidence-group-label">PAPER evidence family (authoritative)</div>' +
        renderPaperFamilyHtml(famData.paper, state.oldVersionPaperFillAvailable) +
        "</div>";
    }
    var complete = oldVersionEvidenceComplete(mode);
    var overallState;
    if (complete) {
      overallState = '<div class="panel panel-passed"><div class="panel-title">STATE-025 — old-version evidence complete</div><div>Every requested evidence family/type above resolved fully' +
        (mode === "backtest" ? " (PAPER evidence was not requested in this mode, so its availability does not affect this result)." : ".") +
        "</div></div>";
    } else {
      overallState = '<div class="panel panel-indeterminate"><div class="panel-title">STATE-026 — old-version evidence partially unavailable</div><div>' +
        (mode === "both" ? "Backtest evidence is fully available; " : "") +
        'PAPER Fill/Position evidence is unavailable for this old version within the requested mode (see the "incomplete" panel above) — the version identity, mode, authority, and all other requested evidence remain visible. This does NOT mean the entire old-version history is unavailable.</div></div>';
    }
    html += overallState;
    box.innerHTML = html;
  }

  // ---- Navigation wiring ----

  function wireGlobalNav(scope) {
    var root = scope || document;
    var buttons = root.querySelectorAll("[data-nav][data-target]");
    buttons.forEach(function (b) {
      b.addEventListener("click", function () {
        var target = b.getAttribute("data-target");
        showScreen(target);
        if (target === "screen-improve") renderImproveSection();
      });
    });
  }

  function wireImproveSubtabs() {
    document.querySelectorAll("#improve-subtabs [data-subtab]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        state.activeScreen = btn.getAttribute("data-subtab");
        renderImproveSection();
      });
    });
  }

  // ---- QA panel wiring (prototype tooling only) ----

  function refreshQaActiveStates() {
    var map = {
      "state025-complete": state.oldVersionPaperFillAvailable === true,
      "state026-partial": state.oldVersionPaperFillAvailable === false,
      "scr011-evidence-exists": state.scr011EvidenceExists === true,
      "scr011-evidence-missing": state.scr011EvidenceExists === false
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
        if (qa === "state025-complete") state.oldVersionPaperFillAvailable = true;
        else if (qa === "state026-partial") state.oldVersionPaperFillAvailable = false;
        else if (qa === "scr011-evidence-exists") state.scr011EvidenceExists = true;
        else if (qa === "scr011-evidence-missing") state.scr011EvidenceExists = false;

        refreshQaActiveStates();
        showScreen("screen-improve");
        renderImproveSection();
      });
    });

    el("qa-reset").addEventListener("click", function () {
      state.activeScreen = "scr-010";
      state.formThesis = "Trend-following trên BTC/USDT khi candle đóng cửa vượt EMA(20), thắt chặt lọc theo volatility (illustrative v1.1 draft)";
      state.formSupportedScope = "trend-following trên crypto major liquid pairs (volatility-filtered)";
      state.createdVersions = [];
      state.versionCounter = 1;
      state.registrationByVersionId = {};
      state.instanceCounter = 1;
      state.sideA = { instanceId: null, mode: null };
      state.sideB = { instanceId: null, mode: null };
      state.view005Mode = null;
      state.view005EntryNote = null;
      state.oldVersionPaperFillAvailable = true;
      state.scr011EvidenceExists = true;
      refreshQaActiveStates();
      showScreen("screen-improve");
      renderImproveSection();
    });
  }

  // ---- Init ----

  function init() {
    wireGlobalNav(document);
    wireImproveSubtabs();
    wireQaPanel();
    refreshQaActiveStates();
    renderImproveSection();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
