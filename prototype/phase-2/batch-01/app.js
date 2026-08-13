/*
 * Ride — Phase 2 Prototype — Batch 01.
 *
 * Illustrative, non-authoritative UI logic only. No real backend, no real
 * exchange integration, no real credentials, no authoritative financial
 * data, no domain event log. Every displayed value below is mock/static.
 *
 * Traceability for every element rendered here is pinned in
 * TRACEABILITY.md — this file does not introduce any UC/PR/domain
 * concept that is not already Consolidated Stable in
 * docs/product/ux-blueprint.md.
 */

(function () {
  "use strict";

  // ---- Mock data (illustrative only, not authoritative financial data) ----

  var MOCK_INSTRUMENTS = [
    { id: "BTC-USDT@BINANCE", label: "BTC/USDT — Binance", hasHistoricalEvidence: true },
    { id: "ETH-USDT@BINANCE", label: "ETH/USDT — Binance", hasHistoricalEvidence: true },
    { id: "SOL-USDT@COINBASE", label: "SOL/USDT — Coinbase", hasHistoricalEvidence: false }
  ];

  var MOCK_STRATEGY_INSTANCES = [
    { id: "inst-a", label: "Instance A — bound to Strategy Definition Version v1.0" },
    { id: "inst-b", label: "Instance B — bound to Strategy Definition Version v2.0" }
  ];

  // ---- Demo/UI state (prototype-local only, not a domain/session state) ----

  var state = {
    selectedInstrumentId: null,
    pinnedStrategyInstanceId: null,
    // QA overrides let every STATE-XXX be inspected on demand without
    // pretending this static prototype computes real verification logic.
    qaOverride: null // e.g. "scr001-loading" | "scr001-invalid" | ...
  };

  // ---- Helpers ----

  function el(id) { return document.getElementById(id); }

  function instrumentById(id) {
    var i;
    for (i = 0; i < MOCK_INSTRUMENTS.length; i++) {
      if (MOCK_INSTRUMENTS[i].id === id) return MOCK_INSTRUMENTS[i];
    }
    return null;
  }

  function instanceById(id) {
    var i;
    for (i = 0; i < MOCK_STRATEGY_INSTANCES.length; i++) {
      if (MOCK_STRATEGY_INSTANCES[i].id === id) return MOCK_STRATEGY_INSTANCES[i];
    }
    return null;
  }

  function showScreen(targetId, deferredStageName) {
    var screens = document.querySelectorAll(".screen");
    screens.forEach(function (s) { s.classList.add("screen-hidden"); });
    el(targetId).classList.remove("screen-hidden");

    var navButtons = document.querySelectorAll(".nav-btn");
    navButtons.forEach(function (b) { b.classList.remove("nav-btn-active"); });

    if (targetId === "screen-scr-001") {
      document.querySelector('[data-nav="NAV-001"]').classList.add("nav-btn-active");
    }
    if (targetId === "screen-deferred") {
      el("deferred-stage-name").textContent = deferredStageName || "This stage";
    }
  }

  function updateContextBar() {
    var instrument = instrumentById(state.selectedInstrumentId);
    el("ctx-instrument").textContent = instrument ? instrument.label : "— none selected —";

    var instance = instanceById(state.pinnedStrategyInstanceId);
    el("ctx-strategy-instance").textContent = instance
      ? instance.label + " (pinned, read-only)"
      : "— not pinned —";
  }

  // ---- SCR-001 rendering ----

  function renderScr001() {
    var body = el("scr-001-body");
    var override = state.qaOverride;
    var instrument = instrumentById(state.selectedInstrumentId);

    if (override === "scr001-loading") {
      body.innerHTML =
        '<div class="panel panel-loading">STATE-001 — loading market-analysis state…</div>';
      return;
    }

    if (override === "scr001-invalid" || !instrument) {
      body.innerHTML =
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-003 — invalid Instrument/Venue</div>' +
        "<div>Select an Instrument/Venue from the registered TradableListing set above " +
        "before market-analysis state can be observed.</div>" +
        "</div>";
      el("btn-to-view-001").disabled = true;
      return;
    }

    if (override === "scr001-missing" || !instrument.hasHistoricalEvidence) {
      body.innerHTML =
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-005 — missing historical evidence</div>' +
        "<div>No historical Candle/Swing/Structure/Regime/Feature/Market Context evidence is " +
        "available yet for <strong>" + instrument.label + "</strong> at the selected range.</div>" +
        "</div>";
      el("btn-to-view-001").disabled = true;
      return;
    }

    // Normal content — illustrative snapshot only, not a real chart/indicator.
    body.innerHTML =
      '<div class="panel">' +
      '<div class="label-row">' +
      '<span class="mode-label">Research</span>' +
      '<span class="authority-label authority-label-authoritative">authoritative (recorded fact, read-only)</span>' +
      "</div>" +
      '<div class="evidence-row"><span class="evidence-label">Candle (latest)</span><span class="evidence-value">O 61,200 · H 61,540 · L 61,050 · C 61,410 (illustrative)</span></div>' +
      '<div class="evidence-row"><span class="evidence-label">Swing</span><span class="evidence-value">Recent swing high at 61,540 (illustrative)</span></div>' +
      '<div class="evidence-row"><span class="evidence-label">Structure</span><span class="evidence-value">Higher-high / higher-low sequence (illustrative)</span></div>' +
      '<div class="evidence-row"><span class="evidence-label">Regime</span><span class="evidence-value">Trending (illustrative)</span></div>' +
      '<div class="evidence-row"><span class="evidence-label">Feature</span><span class="evidence-value">Illustrative feature snapshot, no real indicator computed</span></div>' +
      '<div class="evidence-row"><span class="evidence-label">Market Context</span><span class="evidence-value">Illustrative snapshot for ' + instrument.label + "</span></div>" +
      "</div>";
    el("btn-to-view-001").disabled = false;
  }

  // ---- VIEW-001 rendering ----

  function renderView001() {
    var body = el("view-001-body");
    var override = state.qaOverride;

    var list = MOCK_STRATEGY_INSTANCES;
    if (override === "view001-empty") list = [];

    if (list.length === 0) {
      body.innerHTML =
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-004 — missing Strategy Instance</div>' +
        "<div>No Strategy Instance is registered yet. Registration happens elsewhere " +
        "(VIEW-006, Improve — out of Batch 01 scope).</div>" +
        "</div>";
      return;
    }

    var html = '<div class="label-row">' +
      '<span class="mode-label">Research</span>' +
      '<span class="authority-label authority-label-registration">authoritative (registration record)</span>' +
      "</div>" +
      '<div class="instance-list">';
    list.forEach(function (inst) {
      var pinned = state.pinnedStrategyInstanceId === inst.id;
      html +=
        '<div class="instance-row' + (pinned ? " instance-row-pinned" : "") + '">' +
        "<span>" + inst.label + (pinned ? " — pinned (read-only)" : "") + "</span>" +
        (pinned
          ? "<span>&#10003; pinned</span>"
          : '<button class="btn" data-select-instance="' + inst.id + '">Select &amp; pin</button>') +
        "</div>";
    });
    html += "</div>";
    body.innerHTML = html;

    var buttons = body.querySelectorAll("[data-select-instance]");
    buttons.forEach(function (b) {
      b.addEventListener("click", function () {
        state.pinnedStrategyInstanceId = b.getAttribute("data-select-instance");
        updateContextBar();
        showScreen("screen-view-002");
        renderView002();
      });
    });
  }

  // ---- VIEW-002 rendering ----

  function renderView002() {
    var body = el("view-002-body");
    var override = state.qaOverride;
    var outcome = override === "view002-passed" ? "PASSED"
      : override === "view002-failed" ? "FAILED"
      : override === "view002-indeterminate" ? "INDETERMINATE"
      : "PASSED"; // default demo path once a Strategy Instance is pinned

    var html = '<div class="label-row">' +
      '<span class="mode-label">Research</span>' +
      '<span class="authority-label authority-label-workflow">workflow-visible verification result</span>' +
      "</div>";

    if (outcome === "PASSED") {
      html +=
        '<div class="panel panel-passed">' +
        '<div class="panel-title">STATE-022 — Research verification PASSED</div>' +
        "<div>No prohibited authoritative fact was created during this Research session.</div>" +
        "</div>" +
        '<div class="exit-row">' +
        '<button class="btn btn-primary" data-nav="NAV-002" data-target="screen-deferred" data-stage="Replay">Continue to Replay</button> ' +
        '<button class="btn" data-nav="NAV-003" data-target="screen-deferred" data-stage="Backtest">Continue to Backtest</button>' +
        "<p class=\"hint\">Replay and Backtest are separate Phase 2 batches — not authored here.</p>" +
        "</div>";
    } else if (outcome === "FAILED") {
      html +=
        '<div class="panel panel-fail">' +
        '<div class="panel-title">STATE-023 — Research verification FAILED</div>' +
        "<div>Reason (illustrative): a prohibited authoritative fact was detected during the " +
        "session window. Affected fact (illustrative): Decision record dated within the session " +
        "window.</div>" +
        "<div>Authoritative progression to Replay/Backtest is blocked. Read-only navigation to " +
        "other stages remains available via the nav bar.</div>" +
        "</div>";
    } else {
      html +=
        '<div class="panel panel-indeterminate">' +
        '<div class="panel-title">STATE-024 — Research verification INDETERMINATE</div>' +
        "<div>Reason (illustrative): evidence needed to confirm the session window is incomplete " +
        "or not yet resolved.</div>" +
        "<div>Authoritative progression to Replay/Backtest is blocked, same as FAILED. Read-only " +
        "navigation to other stages remains available via the nav bar.</div>" +
        "</div>";
    }

    body.innerHTML = html;
    wireGlobalNav(body);
  }

  // ---- Navigation wiring ----

  function wireGlobalNav(scope) {
    var root = scope || document;
    var buttons = root.querySelectorAll("[data-nav]");
    buttons.forEach(function (b) {
      b.addEventListener("click", function () {
        var target = b.getAttribute("data-target");
        var stage = b.getAttribute("data-stage");
        showScreen(target, stage);
      });
    });
  }

  function renderAll() {
    renderScr001();
    renderView001();
    renderView002();
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
        state.qaOverride = qa;

        if (qa.indexOf("scr001") === 0) {
          if (qa === "scr001-content" && !state.selectedInstrumentId) {
            state.selectedInstrumentId = MOCK_INSTRUMENTS[0].id;
            el("instrument-select").value = state.selectedInstrumentId;
            updateContextBar();
          }
          showScreen("screen-scr-001");
        } else if (qa.indexOf("view001") === 0) {
          showScreen("screen-view-001");
        } else if (qa.indexOf("view002") === 0) {
          showScreen("screen-view-002");
        }
        renderAll();
      });
    });

    el("qa-reset").addEventListener("click", function () {
      state.selectedInstrumentId = null;
      state.pinnedStrategyInstanceId = null;
      state.qaOverride = null;
      el("instrument-select").value = "";
      updateContextBar();
      showScreen("screen-scr-001");
      renderAll();
    });
  }

  // ---- Init ----

  function init() {
    var select = el("instrument-select");
    var placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "— select Instrument/Venue —";
    select.appendChild(placeholder);

    MOCK_INSTRUMENTS.forEach(function (inst) {
      var opt = document.createElement("option");
      opt.value = inst.id;
      opt.textContent = inst.label;
      select.appendChild(opt);
    });

    select.addEventListener("change", function () {
      state.selectedInstrumentId = select.value || null;
      state.qaOverride = null;
      updateContextBar();
      renderScr001();
    });

    el("btn-to-view-001").addEventListener("click", function () {
      state.qaOverride = null;
      showScreen("screen-view-001");
      renderView001();
    });

    wireGlobalNav(document);
    wireQaPanel();
    updateContextBar();
    renderAll();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
