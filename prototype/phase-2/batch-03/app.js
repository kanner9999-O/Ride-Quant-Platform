/*
 * Ride — Phase 2 Prototype — Batch 03 (Backtest setup + run detail + run comparison).
 *
 * Illustrative, non-authoritative UI logic only. No real backend, no real
 * exchange integration, no real credentials, no authoritative financial
 * data, no simulation engine, no Decision/Risk engine, no domain event log.
 * Every displayed value below is mock/static/deterministic.
 *
 * This is a separate, self-contained page from Batch 01/02 — it does NOT
 * share live JS state with prototype/phase-2/batch-01/ or batch-02/.
 * "Strategy Instance already pinned" is represented as Batch-03-local
 * simulated incoming context (QA panel), per the same convention as Batch
 * 02 — VIEW-001 is NOT re-implemented as a new surface here.
 *
 * Backtest/Paper authority separation (critical, see traceability.md §6):
 * nothing here creates or reuses a PAPER Order/ExecutionResult/Fill/
 * Position, and no action here promotes/converts a Backtest Decision into
 * a Paper Decision. "Exposure change"/"position" below are simulated,
 * non-PAPER, illustrative labels only — not BacktestFill/BacktestPosition
 * entities (none are defined; none are invented here).
 *
 * Traceability for every element rendered here is pinned in
 * traceability.md — this file does not introduce any UC/PR/domain concept
 * that is not already Consolidated Stable in docs/product/ux-blueprint.md,
 * docs/product/use-case-workflow.md, or docs/domain/decision.md/risk.md.
 */

(function () {
  "use strict";

  // ---- Mock data (illustrative only, not authoritative financial data) ----

  // Pinned Strategy Instance context used to bind any newly-started run (SCR-003 "Required
  // context for STARTING a run"). Same illustrative identifiers as Batch 02's fixtures, for
  // cross-batch readability only — not a shared/coupled data source.
  var MOCK_STRATEGY_CONTEXT = {
    instanceId: "inst-a",
    instanceLabel: "Instance A",
    strategyDefinitionVersion: "sdv-v1.0",
    configurationVersion: "cfg-v3"
  };

  var MOCK_INTERVALS = [
    { id: "INT-A", label: "2026-06-01 → 2026-06-30", available: true },
    { id: "INT-B", label: "2026-07-01 → 2026-07-31", available: true },
    { id: "INT-C", label: "2025-01-01 → 2025-01-31 (no historical evidence)", available: false }
  ];

  function intervalById(id) {
    var i;
    for (i = 0; i < MOCK_INTERVALS.length; i++) {
      if (MOCK_INTERVALS[i].id === id) return MOCK_INTERVALS[i];
    }
    return null;
  }

  // Decision shape: outcome (A) + upstream explainability (B) + downstream lineage (C, only
  // when it exists). RiskEvaluation always lives in downstream (C), never upstream (B) —
  // risk.md §1: RiskEvaluation evaluates a Trade Intent, which only exists AFTER a LONG/SHORT
  // Decision (decision.md §10) — closes the same causal-direction requirement already
  // established at use-case-workflow.md UC-007 v0.6.
  function decision(id, outcome, evaluationEvidence, downstream, exposureChange) {
    return {
      id: id,
      outcome: outcome, // "LONG" | "SHORT" | "NO_ACTION"
      upstream: {
        strategyInstance: MOCK_STRATEGY_CONTEXT.instanceLabel + " (" + MOCK_STRATEGY_CONTEXT.instanceId + ")",
        strategyDefinitionVersion: MOCK_STRATEGY_CONTEXT.strategyDefinitionVersion,
        configurationContext: MOCK_STRATEGY_CONTEXT.configurationVersion,
        inputSnapshot: "price_fact#" + (4800 + id.length + outcome.length) + ", reference_fact#" + (4799 + id.length) + " (illustrative)",
        evaluationEvidence: evaluationEvidence
      },
      downstream: downstream, // null, or { tradeIntent, riskEvaluation, executionIntent }
      exposureChange: exposureChange || null // e.g. "FLAT -> LONG" — only set when downstream APPROVED
    };
  }

  var EMA_RULE_LONG = "current candle closed strictly above EMA(20); previous candle ≤ previous EMA(20) (crossing_policy=strict)";
  var EMA_RULE_SHORT = "current candle closed strictly below EMA(20); previous candle ≥ previous EMA(20) (crossing_policy=strict)";
  var EMA_RULE_NONE = "no crossing condition met at this candle (crossing_policy=strict)";

  function seedRuns() {
    return [
      {
        id: "BT-001",
        interval: "2026-06-01 → 2026-06-30",
        strategyInstance: MOCK_STRATEGY_CONTEXT.instanceLabel + " (" + MOCK_STRATEGY_CONTEXT.instanceId + ")",
        strategyDefinitionVersion: "sdv-v1.0",
        configurationVersion: "cfg-v3",
        status: "completed",
        decisions: [
          decision("D1", "LONG", EMA_RULE_LONG,
            { tradeIntent: "TradeIntentIssued (issued)", riskEvaluation: "APPROVED", executionIntent: "ExecutionIntentAccepted" },
            "FLAT → LONG"),
          decision("D2", "NO_ACTION", EMA_RULE_NONE, null, null),
          decision("D3", "SHORT", EMA_RULE_SHORT,
            { tradeIntent: "TradeIntentIssued (issued)", riskEvaluation: "REJECTED (reason: exceeds simulated risk budget, illustrative)", executionIntent: "— not applicable (RiskEvaluation REJECTED)" },
            null),
          decision("D4", "SHORT", EMA_RULE_SHORT,
            { tradeIntent: "TradeIntentIssued (issued)", riskEvaluation: "APPROVED", executionIntent: "ExecutionIntentAccepted" },
            "LONG → FLAT")
        ]
      },
      {
        id: "BT-002",
        interval: "2026-07-01 → 2026-07-31",
        strategyInstance: MOCK_STRATEGY_CONTEXT.instanceLabel + " (" + MOCK_STRATEGY_CONTEXT.instanceId + ")",
        strategyDefinitionVersion: "sdv-v1.1",
        configurationVersion: "cfg-v4",
        status: "completed",
        decisions: [
          decision("D1", "LONG", EMA_RULE_LONG,
            { tradeIntent: "TradeIntentIssued (issued)", riskEvaluation: "APPROVED", executionIntent: "ExecutionIntentAccepted" },
            "FLAT → LONG"),
          decision("D2", "SHORT", EMA_RULE_SHORT,
            { tradeIntent: "TradeIntentIssued (issued)", riskEvaluation: "APPROVED", executionIntent: "ExecutionIntentAccepted" },
            "LONG → FLAT")
        ]
      },
      {
        id: "BT-003",
        interval: "2026-05-01 → 2026-05-31",
        strategyInstance: MOCK_STRATEGY_CONTEXT.instanceLabel + " (" + MOCK_STRATEGY_CONTEXT.instanceId + ")",
        strategyDefinitionVersion: "sdv-v1.0",
        configurationVersion: "cfg-v3",
        status: "completed",
        decisions: [
          decision("D1", "NO_ACTION", EMA_RULE_NONE, null, null),
          decision("D2", "NO_ACTION", EMA_RULE_NONE, null, null)
        ]
      }
    ];
  }

  var runIdCounter = 4; // next new run is BT-004

  function exposureChangingDecisions(run) {
    return run.decisions.filter(function (d) { return d.exposureChange; });
  }

  // UC-008/UC-009 alternate/failure: a run with zero exposure-changing Decisions has
  // insufficient evaluable evidence — STATE-009, distinct from STATE-002 (no run at all) and
  // STATE-010 (run identity unresolved). Represented at the run level, not collapsed into one
  // generic error (Batch 03 validation requirement).
  function hasInsufficientEvidence(run) {
    return exposureChangingDecisions(run).length === 0;
  }

  function finalPosition(run) {
    var changing = exposureChangingDecisions(run);
    if (changing.length === 0) return null;
    var last = changing[changing.length - 1].exposureChange;
    return last.split("→")[1].trim();
  }

  // Ordered exposure/position progression across the run interval (UC-008 Main flow step 2,
  // distinct from step 1's "per-Decision exposure change" list, closes P2-B03-A-MAJ-01).
  // Derived deterministically from the run's OWN decisions array (already part of the run
  // fixture) — not a separate invented dataset, and naturally differs per run since each run's
  // decisions differ. One ordered point per Decision (not only the exposure-changing ones), so
  // the timeline is continuous across the whole interval, not just the change events.
  function positionProgression(run) {
    var current = "FLAT";
    return run.decisions.map(function (d, idx) {
      var before = current;
      var changed = !!d.exposureChange;
      if (changed) current = d.exposureChange.split("→")[1].trim();
      return {
        seq: idx + 1,
        decisionId: d.id,
        before: before,
        change: changed ? d.exposureChange : "no change",
        after: current
      };
    });
  }

  // ---- Demo/UI state (prototype-local only, not a domain/session/replay state) ----

  var state = {
    incomingContext: "incoming-ok", // "incoming-ok" | "incoming-no-instance"
    qaOverride: null, // e.g. "scr003-loading"
    selectedInterval: "INT-A",
    runs: seedRuns(),
    lastCreatedRunId: null,
    selectedRunId: "BT-001",
    forceUnresolvedRun: false, // STATE-010 demo
    compareA: "BT-001",
    compareB: "BT-002",
    scr004Tab: "trace" // "trace" | "economic" | "result"
  };

  // ---- Helpers ----

  function el(id) { return document.getElementById(id); }

  function runById(id) {
    var i;
    for (i = 0; i < state.runs.length; i++) {
      if (state.runs[i].id === id) return state.runs[i];
    }
    return null;
  }

  function completedRuns() {
    return state.runs;
  }

  function showScreen(targetId, deferredStageName) {
    var screens = document.querySelectorAll(".screen");
    screens.forEach(function (s) { s.classList.add("screen-hidden"); });
    el(targetId).classList.remove("screen-hidden");

    var navButtons = document.querySelectorAll(".nav-btn");
    navButtons.forEach(function (b) { b.classList.remove("nav-btn-active"); });

    if (targetId === "screen-scr-003" || targetId === "screen-scr-004" || targetId === "screen-scr-005") {
      var navBacktest = document.querySelector('[data-nav="NAV-003"]');
      if (navBacktest) navBacktest.classList.add("nav-btn-active");
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
      strategyLabel = MOCK_STRATEGY_CONTEXT.instanceLabel + " — bound to Strategy Definition Version " +
        MOCK_STRATEGY_CONTEXT.strategyDefinitionVersion + " (pinned, read-only)";
    }
    el("ctx-strategy-instance").textContent = strategyLabel;
  }

  // ---- SCR-003 rendering (Backtest Run Setup + read-only existing-run list) ----

  function renderScr003() {
    renderRunListSection();
    renderStartFormSection();
  }

  // Read-only inspection of existing runs remains available even when the current Strategy
  // Instance differs from the one that created a given run (NAV-003 "Read-only inspection
  // behavior") or when no Strategy Instance is pinned at all — only STARTING a new run is
  // gated.
  function renderRunListSection() {
    var body = el("scr-003-run-list-body");
    if (state.runs.length === 0) {
      body.innerHTML = '<div class="panel"><div class="hint">No Backtest run exists yet.</div></div>';
      return;
    }
    var html = '<div class="instance-list">';
    state.runs.forEach(function (run) {
      var insufficient = hasInsufficientEvidence(run);
      html += '<div class="instance-row" data-run-open="' + run.id + '">' +
        '<div><strong>' + run.id + '</strong> — ' + run.interval +
        '<div class="instance-row-meta">' + run.strategyInstance + ' · ' + run.strategyDefinitionVersion +
        ' · ' + run.configurationVersion + '</div></div>' +
        '<div class="instance-row-meta">' + (insufficient ? "insufficient evaluable evidence" : "completed") + '</div>' +
        '</div>';
    });
    html += "</div>";
    body.innerHTML = html;

    body.querySelectorAll("[data-run-open]").forEach(function (rowEl) {
      rowEl.addEventListener("click", function () {
        state.selectedRunId = rowEl.getAttribute("data-run-open");
        state.forceUnresolvedRun = false;
        state.scr004Tab = "trace";
        showScreen("screen-scr-004");
        renderScr004();
      });
    });
  }

  function renderStartFormSection() {
    var body = el("scr-003-start-form-body");
    var override = state.qaOverride;

    // NAV-003-level gate: Strategy Instance missing — mirrors NAV-002's own precondition
    // pattern (batch-02, "cited at the NAV level" disclaimer): STATE-004's canonical catalogue
    // "Applicable screen/view" column names VIEW-001, not SCR-003; this is NOT a claim that
    // SCR-003 itself owns STATE-004.
    if (state.incomingContext === "incoming-no-instance") {
      body.innerHTML =
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">Blocked — Strategy Instance not pinned (NAV-003 precondition, STATE-004 cited at the NAV level)</div>' +
        "<div>NAV-003's Required Context: a Strategy Instance must be pinned (VIEW-001) before a new " +
        "Backtest run may be started. This panel reflects NAV-003's own blocked/prompt behavior " +
        "(ux-blueprint.md §5a) — the canonical STATE-004 catalogue entry's \"Applicable " +
        "screen/view\" column names VIEW-001, not SCR-003. Existing runs above remain viewable " +
        "read-only.</div>" +
        "</div>";
      return;
    }

    if (override === "scr003-loading") {
      body.innerHTML = '<div class="panel panel-loading">STATE-001 — loading Backtest run setup state…</div>';
      return;
    }

    var html = '<div class="field-row">' +
      '<label for="interval-select">Historical interval (bounded start/end)</label>' +
      '<select id="interval-select"></select>' +
      "</div>" +
      '<div class="evidence-row"><span class="evidence-label">Strategy Instance</span><span class="evidence-value">' +
      MOCK_STRATEGY_CONTEXT.instanceLabel + " (" + MOCK_STRATEGY_CONTEXT.instanceId + ")</span></div>" +
      '<div class="evidence-row"><span class="evidence-label">Strategy Definition Version</span><span class="evidence-value">' +
      MOCK_STRATEGY_CONTEXT.strategyDefinitionVersion + "</span></div>" +
      '<div class="evidence-row"><span class="evidence-label">Configuration / policy version</span><span class="evidence-value">' +
      MOCK_STRATEGY_CONTEXT.configurationVersion + "</span></div>" +
      '<div class="evidence-row"><span class="evidence-label">Mode</span><span class="evidence-value">Backtest</span></div>' +
      '<div class="label-row" style="margin-top:10px;">' +
      '<span class="mode-label">Backtest</span>' +
      '<span class="authority-label authority-label-recomputation">Authority class: Backtest / non-PAPER simulated</span>' +
      '<span class="prototype-datum-label">Prototype datum: Illustrative / non-authoritative</span>' +
      "</div>" +
      '<div class="hint">Starting a run does not route to any real exchange endpoint, does not create a ' +
      "PAPER Order/ExecutionResult/Fill/Position, and does not implement a simulation engine — " +
      "static illustrative fixtures only.</div>" +
      '<div id="scr-003-start-result"></div>' +
      '<div class="exit-row"><button class="btn btn-primary" id="btn-start-run">Start Backtest run</button></div>';
    body.innerHTML = html;

    var select = el("interval-select");
    MOCK_INTERVALS.forEach(function (iv) {
      var opt = document.createElement("option");
      opt.value = iv.id;
      opt.textContent = iv.label;
      select.appendChild(opt);
    });
    select.value = state.selectedInterval;
    select.addEventListener("change", function () {
      state.selectedInterval = select.value;
      el("scr-003-start-result").innerHTML = "";
    });

    el("btn-start-run").addEventListener("click", function () {
      startBacktestRun(state.selectedInterval);
    });
  }

  function startBacktestRun(intervalId) {
    var iv = intervalById(intervalId);
    var resultBox = el("scr-003-start-result");
    if (!resultBox) return;

    // STATE-005: a run must not appear successfully started if the selected interval is in the
    // missing-evidence demo state.
    if (!iv || !iv.available) {
      resultBox.innerHTML =
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-005 — missing historical evidence</div>' +
        "<div>No historical data is available for <strong>" + (iv ? iv.label : intervalId) +
        "</strong>. No Backtest run identity was assigned — no run created.</div>" +
        "</div>";
      return;
    }

    var newId = "BT-" + String(runIdCounter).padStart(3, "0");
    runIdCounter += 1;
    // The new run identity visibly binds interval + Strategy Instance + Strategy Definition
    // Version + configuration/policy version, and actually participates in later
    // prototype-local state (appears in the run list, viewable at SCR-004, selectable at
    // SCR-005) — not an inert "Start run" control.
    var newRun = {
      id: newId,
      interval: iv.label,
      strategyInstance: MOCK_STRATEGY_CONTEXT.instanceLabel + " (" + MOCK_STRATEGY_CONTEXT.instanceId + ")",
      strategyDefinitionVersion: MOCK_STRATEGY_CONTEXT.strategyDefinitionVersion,
      configurationVersion: MOCK_STRATEGY_CONTEXT.configurationVersion,
      status: "completed",
      decisions: [
        decision("D1", "LONG", EMA_RULE_LONG,
          { tradeIntent: "TradeIntentIssued (issued)", riskEvaluation: "APPROVED", executionIntent: "ExecutionIntentAccepted" },
          "FLAT → LONG"),
        decision("D2", "NO_ACTION", EMA_RULE_NONE, null, null),
        decision("D3", "SHORT", EMA_RULE_SHORT,
          { tradeIntent: "TradeIntentIssued (issued)", riskEvaluation: "APPROVED", executionIntent: "ExecutionIntentAccepted" },
          "LONG → FLAT")
      ]
    };
    state.runs.push(newRun);
    state.lastCreatedRunId = newId;

    resultBox.innerHTML =
      '<div class="panel panel-passed">' +
      '<div class="panel-title">Backtest run identity created — ' + newId + '</div>' +
      "<div>Bound to " + iv.label + " · " + MOCK_STRATEGY_CONTEXT.instanceLabel + " · " +
      MOCK_STRATEGY_CONTEXT.strategyDefinitionVersion + " · " + MOCK_STRATEGY_CONTEXT.configurationVersion + "</div>" +
      '<button class="btn" id="btn-view-new-run" style="margin-top:8px;">View run detail →</button>' +
      "</div>";
    renderRunListSection();
    el("btn-view-new-run").addEventListener("click", function () {
      state.selectedRunId = newId;
      state.forceUnresolvedRun = false;
      state.scr004Tab = "trace";
      showScreen("screen-scr-004");
      renderScr004();
    });
  }

  // ---- SCR-004 rendering (Backtest Run Detail) ----

  function renderScr004() {
    var body = el("scr-004-body");

    // STATE-002: run list empty, nothing to show.
    if (state.runs.length === 0) {
      body.innerHTML =
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-002 — empty</div>' +
        "<div>No Backtest run exists yet. Start one from Backtest Run Setup.</div>" +
        "</div>";
      return;
    }

    // STATE-010: Backtest run identity does not resolve (QA-forced demo, or a stale
    // selectedRunId). Run identity itself, if known, remains observable; reason disclosed; no
    // downstream authoritative action; no run-deletion/state-machine/archival lifecycle implied
    // (use-case-workflow.md UC-007 alternate/failure, v0.2).
    var run = state.forceUnresolvedRun ? null : runById(state.selectedRunId);
    if (!run) {
      body.innerHTML =
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-010 — Backtest run identity unresolved</div>' +
        "<div>Run identity <strong>" + (state.forceUnresolvedRun ? "BT-999" : state.selectedRunId) +
        "</strong> does not resolve, or its evidence is currently unavailable. No downstream " +
        "action is available for this identity. This does not imply a run deletion event, state " +
        "machine, or archival lifecycle.</div>" +
        '<div class="exit-row"><button class="btn" id="btn-back-to-setup">Back to Backtest Run Setup</button></div>' +
        "</div>";
      el("btn-back-to-setup").addEventListener("click", function () {
        showScreen("screen-scr-003");
        renderScr003();
      });
      return;
    }

    var html = '<div class="label-row">' +
      '<span class="mode-label">Backtest</span>' +
      '<span class="authority-label authority-label-recomputation">Authority class: Backtest / non-PAPER simulated</span>' +
      '<span class="prototype-datum-label">Prototype datum: Illustrative / non-authoritative</span>' +
      "</div>" +
      '<div class="evidence-row"><span class="evidence-label">Run identity</span><span class="evidence-value">' + run.id + "</span></div>" +
      '<div class="evidence-row"><span class="evidence-label">Interval</span><span class="evidence-value">' + run.interval + "</span></div>" +
      '<div class="evidence-row"><span class="evidence-label">Strategy Instance</span><span class="evidence-value">' + run.strategyInstance + "</span></div>" +
      '<div class="evidence-row"><span class="evidence-label">Strategy Definition Version</span><span class="evidence-value">' + run.strategyDefinitionVersion + "</span></div>" +
      '<div class="evidence-row"><span class="evidence-label">Configuration / policy version</span><span class="evidence-value">' + run.configurationVersion + "</span></div>" +
      '<div class="subtab-row">' +
      '<button class="subtab-btn" data-tab="trace">Decision / RiskEvaluation trace</button>' +
      '<button class="subtab-btn" data-tab="economic">Simulated economic evidence</button>' +
      '<button class="subtab-btn" data-tab="result">Strategy-level evaluable result</button>' +
      "</div>" +
      '<div id="scr-004-tab-body"></div>' +
      '<div class="exit-row">' +
      '<button class="btn btn-primary" id="btn-to-scr-005">Compare with another run →</button>' +
      '<p class="hint">Backtest evidence remains non-PAPER and simulated throughout — see README for the Backtest/Paper authority separation this batch preserves.</p>' +
      "</div>";
    body.innerHTML = html;

    body.querySelectorAll("[data-tab]").forEach(function (btn) {
      btn.classList.toggle("subtab-btn-active", btn.getAttribute("data-tab") === state.scr004Tab);
      btn.addEventListener("click", function () {
        state.scr004Tab = btn.getAttribute("data-tab");
        renderScr004();
      });
    });

    renderScr004Tab(run);

    el("btn-to-scr-005").addEventListener("click", function () {
      state.compareA = run.id;
      showScreen("screen-scr-005");
      renderScr005();
    });
  }

  function renderScr004Tab(run) {
    var body = el("scr-004-tab-body");
    if (state.scr004Tab === "trace") {
      body.innerHTML = renderDecisionTrace(run);
    } else if (state.scr004Tab === "economic") {
      body.innerHTML = renderEconomicEvidence(run);
    } else {
      body.innerHTML = renderEvaluableResult(run);
    }
  }

  // Panel A: for each Decision, three explicitly separate groups — (A) outcome, (B) upstream
  // explainability (evidence used to CREATE the Decision), (C) downstream lineage (fact
  // causally derived from/related to the Decision, NEVER presented as evidence used to create
  // it). RiskEvaluation always renders inside group C.
  function renderDecisionTrace(run) {
    var html = "";
    run.decisions.forEach(function (d) {
      var outcomeClass = d.outcome === "LONG" ? "outcome-long" : d.outcome === "SHORT" ? "outcome-short" : "outcome-no-action";
      html += '<div class="decision-card">' +
        '<div class="decision-header"><span class="decision-id">' + d.id + '</span>' +
        '<span class="outcome-badge ' + outcomeClass + '">A — ' + d.outcome + "</span></div>" +
        '<div class="evidence-group evidence-group-upstream">' +
        '<div class="evidence-group-label">B — Upstream Decision origin / explainability (used to CREATE this Decision)</div>' +
        '<div class="evidence-row"><span class="evidence-label">Strategy Instance</span><span class="evidence-value">' + d.upstream.strategyInstance + "</span></div>" +
        '<div class="evidence-row"><span class="evidence-label">Strategy Definition Version</span><span class="evidence-value">' + d.upstream.strategyDefinitionVersion + "</span></div>" +
        '<div class="evidence-row"><span class="evidence-label">Configuration context</span><span class="evidence-value">' + d.upstream.configurationContext + "</span></div>" +
        '<div class="evidence-row"><span class="evidence-label">Recorded input snapshot</span><span class="evidence-value">' + d.upstream.inputSnapshot + "</span></div>" +
        '<div class="evidence-row"><span class="evidence-label">Recorded evaluation evidence</span><span class="evidence-value">' + d.upstream.evaluationEvidence + "</span></div>" +
        "</div>";
      if (d.downstream) {
        html += '<div class="evidence-group evidence-group-downstream">' +
          '<div class="evidence-group-label">C — Downstream lineage (causally derived from/related to this Decision — NOT evidence used to create it)</div>' +
          '<div class="evidence-row"><span class="evidence-label">Trade Intent</span><span class="evidence-value">' + d.downstream.tradeIntent + "</span></div>" +
          '<div class="evidence-row"><span class="evidence-label">RiskEvaluation</span><span class="evidence-value">' + d.downstream.riskEvaluation + "</span></div>" +
          '<div class="evidence-row"><span class="evidence-label">Execution Intent</span><span class="evidence-value">' + d.downstream.executionIntent + "</span></div>" +
          "</div>";
      } else {
        html += '<div class="evidence-group evidence-group-none">' +
          "C — Downstream lineage: none (result = NO_ACTION never issues a Trade Intent, decision.md §10)." +
          "</div>";
      }
      html += "</div>";
    });
    return html;
  }

  // Panel B: simulated economic evidence + exposure/position progression — non-PAPER,
  // illustrative only. STATE-009 when the run has zero exposure-changing Decisions.
  function renderEconomicEvidence(run) {
    if (hasInsufficientEvidence(run)) {
      return '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-009 — Backtest evidence insufficient</div>' +
        "<div>No Decision in this run produced a simulated exposure change (\"no simulated exposure " +
        "change produced\"). The run identity remains observable; no strategy-level evaluable result " +
        "can be shown as evaluable for this run.</div>" +
        "</div>";
    }
    var html = '<div class="label-row">' +
      '<span class="mode-label">Backtest</span>' +
      '<span class="authority-label authority-label-recomputation">Authority class: Backtest / non-PAPER simulated</span>' +
      '<span class="prototype-datum-label">Prototype datum: Illustrative / non-authoritative</span>' +
      "</div>" +
      '<div class="hint">Simulated exposure change per Decision — NOT PAPER ExecutionResult/Fill/Position; no BacktestFill/BacktestPosition entity exists or is invented here.</div>' +
      '<div class="lineage-list">';
    run.decisions.forEach(function (d) {
      if (d.exposureChange) {
        html += lineageRow(d.id + " (" + d.outcome + ") simulated exposure change", d.exposureChange);
      }
    });
    html += "</div>";

    // UC-008 Main flow step 2 — exposure/position progression theo thời gian xuyên suốt khoảng
    // interval của run (ux-blueprint.md §7.3 SCR-004 Panel (b)), distinct from step 1's
    // per-Decision change list above. One ordered row per Decision (including no-change points)
    // so the timeline is continuous across the whole interval, not just the change events.
    html += '<h3 style="font-size:13px;margin:16px 0 8px;color:#33455e;">Simulated exposure/position progression (ordered across the run interval)</h3>' +
      '<table class="progression-table"><thead><tr>' +
      "<th>#</th><th>Decision</th><th>Position before</th><th>Simulated change</th><th>Position after</th>" +
      "</tr></thead><tbody>";
    positionProgression(run).forEach(function (p) {
      html += "<tr><td>" + p.seq + "</td><td>" + p.decisionId + "</td><td>" + p.before +
        "</td><td>" + p.change + "</td><td>" + p.after + "</td></tr>";
    });
    html += "</tbody></table>";

    html += '<div class="evidence-row" style="margin-top:8px;"><span class="evidence-label">Final simulated position (illustrative)</span><span class="evidence-value">' + finalPosition(run) + "</span></div>";
    return html;
  }

  // Panel C: strategy-level evaluable result bound to the exact run/version tuple —
  // threshold-neutral, no KPI/pass-fail/score/Sharpe/win-rate/profitability criterion defined
  // or implied (OQ-003 unresolved). STATE-009 when insufficient (same condition as economic
  // evidence, per use-case-workflow.md UC-009 alternate/failure).
  function renderEvaluableResult(run) {
    if (hasInsufficientEvidence(run)) {
      return '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-009 — Backtest evidence insufficient</div>' +
        "<div>This run has no simulated exposure change to derive a strategy-level evaluable result " +
        "from. Run identity remains observable; reason disclosed.</div>" +
        "</div>";
    }
    var changing = exposureChangingDecisions(run);
    return '<div class="label-row">' +
      '<span class="mode-label">Backtest</span>' +
      '<span class="authority-label authority-label-recomputation">Authority class: Backtest / non-PAPER simulated</span>' +
      '<span class="prototype-datum-label">Prototype datum: Illustrative / non-authoritative (no KPI threshold defined — OQ-003 unresolved)</span>' +
      "</div>" +
      '<div class="evidence-row"><span class="evidence-label">Run / version tuple</span><span class="evidence-value">' +
      run.id + " · " + run.strategyDefinitionVersion + " · " + run.configurationVersion + "</span></div>" +
      '<div class="evidence-row"><span class="evidence-label">Simulated exposure-changing Decisions</span><span class="evidence-value">' +
      changing.length + " of " + run.decisions.length + "</span></div>" +
      '<div class="evidence-row"><span class="evidence-label">Final simulated position (illustrative)</span><span class="evidence-value">' +
      finalPosition(run) + "</span></div>" +
      '<div class="hint">No pass/fail target, aggregate score, Sharpe target, win-rate threshold, or profitability criterion is defined or implied — OQ-003 remains unresolved (use-case-workflow.md UC-009 Out-of-scope boundary).</div>';
  }

  function lineageRow(name, value) {
    return '<div class="lineage-step"><span class="lineage-step-name">' + name +
      '</span><span class="lineage-step-value">' + value + "</span></div>";
  }

  // ---- SCR-005 rendering (Backtest Run Comparison) ----

  function renderScr005() {
    var body = el("scr-005-body");
    var runs = completedRuns();

    // STATE-002: fewer than two completed runs available.
    if (runs.length < 2) {
      body.innerHTML =
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-002 — empty</div>' +
        "<div>Fewer than two Backtest runs are available to compare. Start additional runs from " +
        "Backtest Run Setup.</div>" +
        "</div>";
      return;
    }

    if (runs.indexOf(runById(state.compareA)) === -1 || !runById(state.compareA)) state.compareA = runs[0].id;
    if (state.compareB === state.compareA || !runById(state.compareB)) {
      state.compareB = runs.filter(function (r) { return r.id !== state.compareA; })[0].id;
    }

    var html = '<div class="run-select-row">' +
      selectField("compare-a-select", "Run A", runs, state.compareA) +
      selectField("compare-b-select", "Run B", runs, state.compareB) +
      "</div>" +
      '<div class="representation-compare">' +
      comparisonColumn(runById(state.compareA)) +
      comparisonColumn(runById(state.compareB)) +
      "</div>" +
      '<div class="hint">Each column retains its own run identity, interval, Strategy Instance, Strategy Definition Version, and configuration/version context — results are shown side by side, never aggregated into one opaque overall score.</div>' +
      '<div class="exit-row">' +
      '<button class="btn" data-nav="NAV-006" data-target="screen-deferred" data-stage="Improve">Continue to Improve (Strategy Definition Version comparison)</button>' +
      '<p class="hint">SCR-011 (Strategy Definition Version Comparison) is not authored in Batch 03 — this is a deferred handoff only.</p>' +
      "</div>";
    body.innerHTML = html;

    el("compare-a-select").addEventListener("change", function () {
      state.compareA = el("compare-a-select").value;
      renderScr005();
    });
    el("compare-b-select").addEventListener("change", function () {
      state.compareB = el("compare-b-select").value;
      renderScr005();
    });

    wireGlobalNav(body);
  }

  function selectField(id, label, runs, selectedId) {
    var html = '<div class="field-row"><label for="' + id + '">' + label + "</label><select id=\"" + id + "\">";
    runs.forEach(function (r) {
      html += '<option value="' + r.id + '"' + (r.id === selectedId ? " selected" : "") + ">" + r.id + " — " + r.interval + "</option>";
    });
    html += "</select></div>";
    return html;
  }

  function comparisonColumn(run) {
    if (!run) return '<div class="representation-panel"><h3>—</h3></div>';
    var html = '<div class="representation-panel"><h3>' + run.id + "</h3>";
    if (hasInsufficientEvidence(run)) {
      html += '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-009 — Backtest evidence insufficient</div>' +
        "<div>This run lacks sufficient evaluable evidence; other selected run evidence remains " +
        "visible.</div></div>";
      return html + "</div>";
    }
    var changing = exposureChangingDecisions(run);
    html += '<div class="evidence-row"><span class="evidence-label">Interval</span><span class="evidence-value">' + run.interval + "</span></div>" +
      '<div class="evidence-row"><span class="evidence-label">Strategy Instance</span><span class="evidence-value">' + run.strategyInstance + "</span></div>" +
      '<div class="evidence-row"><span class="evidence-label">Strategy Definition Version</span><span class="evidence-value">' + run.strategyDefinitionVersion + "</span></div>" +
      '<div class="evidence-row"><span class="evidence-label">Configuration / policy version</span><span class="evidence-value">' + run.configurationVersion + "</span></div>" +
      '<div class="evidence-row"><span class="evidence-label">Simulated exposure-changing Decisions</span><span class="evidence-value">' + changing.length + " of " + run.decisions.length + "</span></div>" +
      '<div class="evidence-row"><span class="evidence-label">Final simulated position</span><span class="evidence-value">' + finalPosition(run) + "</span></div>";
    return html + "</div>";
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
        if (target === "screen-scr-003") renderScr003();
      });
    });
  }

  function renderAll() {
    renderScr003();
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

        if (qa === "incoming-ok" || qa === "incoming-no-instance") {
          state.incomingContext = qa;
          state.qaOverride = null;
          updateContextBar();
          showScreen("screen-scr-003");
          renderScr003();
          return;
        }

        if (qa === "scr003-loading") {
          state.qaOverride = "scr003-loading";
          showScreen("screen-scr-003");
          renderScr003();
          return;
        }
        if (qa === "scr003-normal") {
          state.qaOverride = null;
          showScreen("screen-scr-003");
          renderScr003();
          return;
        }

        if (qa === "scr004-unresolved") {
          state.forceUnresolvedRun = true;
          showScreen("screen-scr-004");
          renderScr004();
          return;
        }
        if (qa === "scr004-clear-runs") {
          state.runs = [];
          showScreen("screen-scr-004");
          renderScr004();
          renderRunListSection();
          return;
        }
      });
    });

    el("qa-reset").addEventListener("click", function () {
      state.incomingContext = "incoming-ok";
      state.qaOverride = null;
      state.selectedInterval = "INT-A";
      state.runs = seedRuns();
      runIdCounter = 4;
      state.lastCreatedRunId = null;
      state.selectedRunId = "BT-001";
      state.forceUnresolvedRun = false;
      state.compareA = "BT-001";
      state.compareB = "BT-002";
      state.scr004Tab = "trace";
      updateContextBar();
      showScreen("screen-scr-003");
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
