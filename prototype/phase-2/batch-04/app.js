/*
 * Ride — Phase 2 Prototype — Batch 04 (Paper initiation + execution evidence/detail).
 *
 * Illustrative, non-authoritative UI logic only. No real backend, no real
 * exchange integration, no real credentials, no signing/custody, no
 * authoritative financial computation, no production execution/simulation
 * engine. Every displayed value below is mock/static/deterministic.
 *
 * This is a separate, self-contained page from Batch 01/02/03 — it does
 * NOT share live JS state with any of them. "Paper-pinned Strategy
 * Instance" is represented as Batch-04-local simulated state (QA panel +
 * a bounded local fixture standing in for VIEW-001), NOT by
 * re-implementing VIEW-001 as a new surface.
 *
 * PAPER Decision separation (INV-1, critical): the PAPER-context Decision
 * below is a distinct, already-existing authoritative fixture. Nothing
 * here clones/carries-forward/promotes/reuses the Batch 03 Backtest
 * Decision or any Research Decision as this PAPER Decision, and nothing
 * defines the mechanism that created it (that remains a deferred
 * domain/workflow dependency, use-case-workflow.md UC-011).
 *
 * Traceability for every element rendered here is pinned in
 * traceability.md — this file does not introduce any UC/PR/domain concept
 * that is not already Consolidated Stable in docs/product/ux-blueprint.md,
 * docs/product/use-case-workflow.md, or docs/domain/*.md.
 */

(function () {
  "use strict";

  // ---- Mock data (illustrative only, not authoritative financial data) ----

  var MOCK_ACCOUNT_CONTEXT = {
    account: "Ride Internal Account",
    instrument: "BTC/USDT",
    venue: "Binance"
  };

  // Paper-specific pin — independent from any Replay/Backtest pin (NAV-004 "Required context").
  var MOCK_STRATEGY_CONTEXT = {
    instanceId: "inst-a",
    instanceLabel: "Instance A",
    strategyDefinitionVersion: "sdv-v1.0",
    configurationVersion: "cfg-v3"
  };

  // The PAPER-context authoritative Decision lineage — a distinct fact, NOT a Backtest/Research
  // Decision carried forward (INV-1). Its creation mechanism is intentionally NOT modeled here
  // (use-case-workflow.md UC-011: "deferred domain/workflow dependency, §9d").
  var MOCK_PAPER_DECISION = {
    id: "PD-001",
    outcome: "LONG",
    strategyInstance: MOCK_STRATEGY_CONTEXT.instanceLabel + " (" + MOCK_STRATEGY_CONTEXT.instanceId + ")",
    strategyDefinitionVersion: MOCK_STRATEGY_CONTEXT.strategyDefinitionVersion,
    configurationVersion: MOCK_STRATEGY_CONTEXT.configurationVersion,
    inputSnapshot: "price_fact#7710, reference_fact#7709 (illustrative)",
    evaluationEvidence: "current candle closed strictly above EMA(20); previous candle ≤ previous EMA(20) (crossing_policy=strict)"
  };

  // ---- Deterministic downstream chain builder (INV-4: exact branch truncation) ----

  // Builds the PAPER C7 chain from the current QA-selected risk/execution outcome. This is the
  // ONLY place a chain object is produced — SCR-006's inline summary and SCR-007's full detail
  // both render from the SAME state.execution object (INV-5 identity continuity / no disconnected
  // fixtures between screens).
  //
  // v1.1 (closes P2-B04-A-MAJ-01): the chain now represents ExecutionResultComputation
  // (execution-result.md §2 — authorized computation identity/binding fact, computation_purpose/
  // order_id/submission_request_id/computation_cursor) and PaperExecutionObservation
  // (execution-result.md §1 — execution_result_computation_id/simulation evidence four-axis/
  // result_type/economics) as two DISTINCT nodes between OrderSubmissionRequest and
  // ExecutionResult — previously collapsed into a bare `observationId` string on ExecutionResult
  // and `executionObservationId` on Fill, with no PaperExecutionObservation entity of its own.
  // Fill's economics (quantity/price/currency) are now literally copied from
  // paperExecutionObservation's own executedQuantity/executionPrice/priceCurrency fields (not a
  // second independent literal), matching fill.md v0.2's "PHẢI BẰNG HỆT Observation" invariant at
  // the code level.
  function buildExecutionChain(riskOutcome, executionOutcome) {
    var chain = {
      decisionId: MOCK_PAPER_DECISION.id,
      tradeIntentId: "TI-001",
      riskEvaluation: { id: "RE-001", result: riskOutcome, reasonCode: null },
      executionIntent: null,
      order: null,
      submissionRequest: null,
      executionResultComputation: null,
      paperExecutionObservation: null,
      executionResult: null,
      fill: null
    };

    if (riskOutcome === "REJECTED") {
      chain.riskEvaluation.reasonCode = "INVALID_SIZING_INPUT";
      return chain; // STATE-013: stop at RiskEvaluation — no Execution Intent/Order/Computation/Observation/ExecutionResult/Fill.
    }
    if (riskOutcome === "NON_EVALUABLE") {
      chain.riskEvaluation.reasonCode = "REQUIRED_EVIDENCE_UNAVAILABLE";
      return chain; // STATE-014: same stop boundary as REJECTED.
    }

    // riskOutcome === "APPROVED" — may continue downstream.
    chain.executionIntent = { id: "EI-001", status: "ISSUED" };
    chain.order = { id: "ORD-001", environment: "PAPER" };
    chain.submissionRequest = { id: "OSR-001" };

    // ExecutionResultComputation (execution-result.md §2) — authorized computation identity,
    // bound to this Order/OrderSubmissionRequest. Illustrative only, no computation logic run.
    chain.executionResultComputation = {
      id: "ERC-001",
      computationPurpose: "INITIAL",
      orderId: chain.order.id,
      submissionRequestId: chain.submissionRequest.id,
      computationCursor: "C-ERC-001"
    };

    // PaperExecutionObservation (execution-result.md §1) — bound to the ExecutionResultComputation
    // above via execution_result_computation_id, carries the four simulation-evidence axes and
    // (when EXECUTED) the economics that ExecutionResult/Fill copy from — never independently
    // computed here.
    chain.paperExecutionObservation = {
      id: "OBS-001",
      executionResultComputationId: chain.executionResultComputation.id,
      orderId: chain.order.id,
      submissionRequestId: chain.submissionRequest.id,
      observationCursor: chain.executionResultComputation.computationCursor,
      simulationPolicyRef: "sim-policy-v1",
      simulationConfigurationRef: "sim-config-v1",
      simulationBuildRef: "sim-build-v1",
      deterministicInputRef: "det-input-abc123",
      resultType: executionOutcome
    };

    if (executionOutcome === "NOT_EXECUTED") {
      // STATE-016: Computation + Observation both exist (result_type = NOT_EXECUTED, economics
      // fields absent per execution-result.md §1 invariant), ExecutionResult copies that
      // result_type, zero Fill.
      chain.executionResult = {
        id: "ER-001",
        resultType: "NOT_EXECUTED",
        executionObservationId: chain.paperExecutionObservation.id
      };
      return chain;
    }

    // executionOutcome === "EXECUTED" — STATE-015, exactly one Fill. Economics live on the
    // Observation first; ExecutionResult/Fill reference it, Fill copies its economics exactly.
    chain.paperExecutionObservation.executedQuantity = "0.50";
    chain.paperExecutionObservation.executionPrice = "65000.00";
    chain.paperExecutionObservation.priceCurrency = "USDT";
    chain.paperExecutionObservation.quantityUnit = "BTC";

    chain.executionResult = {
      id: "ER-001",
      resultType: "EXECUTED",
      executionObservationId: chain.paperExecutionObservation.id
    };
    chain.fill = {
      id: "FILL-001",
      executionObservationId: chain.paperExecutionObservation.id,
      quantity: chain.paperExecutionObservation.executedQuantity,
      quantityUnit: chain.paperExecutionObservation.quantityUnit,
      price: chain.paperExecutionObservation.executionPrice,
      priceCurrency: chain.paperExecutionObservation.priceCurrency
    };
    return chain;
  }

  // An illustrative PRIOR eligible Fill for the SAME Account/Instrument, from an earlier Paper
  // session not otherwise represented in this batch — exists ONLY to give the NON_EVALUABLE demo
  // below (closes P2-B04-A-MAJ-02) a coherent, explicitly-disclosed second Fill lineage, rather
  // than fabricating an unexplained FILL-002.
  var MOCK_PRIOR_FILL_LABEL = "FILL-000 (illustrative prior eligible Fill, same Account/Instrument, earlier Paper session — not otherwise shown in this batch, represented only for this demo)";

  function derivePositionNatural(execution) {
    if (!execution || !execution.fill) {
      return { status: "EVALUABLE", direction: null, netQuantity: "0" };
    }
    return {
      status: "EVALUABLE",
      direction: MOCK_PAPER_DECISION.outcome, // LONG/SHORT — this prototype's single Fill lineage direction follows the Decision outcome.
      netQuantity: execution.fill.quantity,
      quantityUnit: execution.fill.quantityUnit,
      averageEntryPrice: execution.fill.price,
      priceCurrency: execution.fill.priceCurrency
    };
  }

  // Position (UC-014) is a derived projection (position.md §1 — read_model, Type 2 Projection,
  // NOT an authoritative fact). Derived from eligible Fill count for this Account/Instrument —
  // zero eligible Fill -> FLAT (independent of WHY there's no Fill); exactly one -> LONG/SHORT;
  // >1 conflicting eligible Fill lineage -> NON_EVALUABLE.
  //
  // v1.1 (closes P2-B04-A-MAJ-02): the NON_EVALUABLE demo previously fabricated a second Fill
  // (FILL-002) with no evidence basis, and could render even when the CURRENT selected execution
  // was NOT_EXECUTED (zero Fill) — a direct contradiction with the Fill/ExecutionResult tabs.
  // NON_EVALUABLE now renders ONLY when the current execution actually produced a Fill (EXECUTED)
  // — its contributing_fill_refs then pair that REAL current Fill with one explicitly-labelled
  // illustrative PRIOR Fill (MOCK_PRIOR_FILL_LABEL), never an unexplained second current Fill. If
  // the override is selected but the current execution has no Fill, the override does not apply
  // — the TRUE current Position state is returned instead (never silently forced to FLAT; it is
  // whatever derivePositionNatural() actually resolves, which happens to be FLAT only when that
  // is itself the true zero-Fill state), with an explicit note explaining why.
  function derivePosition(execution, positionDemoOverride) {
    if (positionDemoOverride === "non-evaluable") {
      if (execution && execution.fill) {
        return {
          status: "NON_EVALUABLE",
          contributingFillRefs: [MOCK_PRIOR_FILL_LABEL, execution.fill.id + " (current execution's Fill)"]
        };
      }
      var natural = derivePositionNatural(execution);
      natural.demoNote = "NON_EVALUABLE demo requires the current execution to have produced a Fill (EXECUTED) to pair with the illustrative prior Fill — the current execution has none, so the override does not apply here; the actual Position state is shown instead.";
      return natural;
    }
    return derivePositionNatural(execution);
  }

  // ---- Demo/UI state (prototype-local only, not a domain/session/replay state) ----

  var state = {
    accountValid: true, // STATE-003 when false
    paperPin: "pinned", // "none" (STATE-028) | "selected" (STATE-029) | "pinned"
    decisionAvailable: true, // STATE-011 when pinned but false
    riskOutcome: "APPROVED", // QA-selected scenario for the NEXT initiation
    executionOutcome: "EXECUTED",
    execution: null, // null until user clicks "Initiate PAPER execution" (STATE-002 on SCR-007 until then)
    positionDemoOverride: null, // null | "non-evaluable"
    activeScreen: "scr-006" // "scr-006" | "scr-007"
  };

  // ---- Helpers ----

  function el(id) { return document.getElementById(id); }

  function showScreen(targetId, deferredStageName) {
    var screens = document.querySelectorAll(".screen");
    screens.forEach(function (s) { s.classList.add("screen-hidden"); });
    el(targetId).classList.remove("screen-hidden");

    var navButtons = document.querySelectorAll(".nav-btn");
    navButtons.forEach(function (b) { b.classList.remove("nav-btn-active"); });

    if (targetId === "screen-paper") {
      var navPaper = document.querySelector('[data-nav="NAV-004"]');
      if (navPaper) navPaper.classList.add("nav-btn-active");
    }
    if (targetId === "screen-deferred") {
      el("deferred-stage-name").textContent = deferredStageName || "This stage";
    }
  }

  function updateContextBar() {
    var strategyLabel;
    if (state.paperPin === "none") {
      strategyLabel = "— not pinned for Paper —";
    } else if (state.paperPin === "selected") {
      strategyLabel = MOCK_STRATEGY_CONTEXT.instanceLabel + " — selected, not yet pinned for Paper";
    } else {
      strategyLabel = MOCK_STRATEGY_CONTEXT.instanceLabel + " — pinned for Paper (Strategy Definition Version " +
        MOCK_STRATEGY_CONTEXT.strategyDefinitionVersion + ")";
    }
    el("ctx-strategy-instance").textContent = strategyLabel;
  }

  function el5(name, value) {
    return '<div class="evidence-row"><span class="evidence-label">' + name + '</span><span class="evidence-value">' + value + "</span></div>";
  }

  // ---- Paper section rendering (NAV-004 destination: SCR-006 + SCR-007) ----

  function renderPaperSection() {
    document.querySelectorAll("#paper-subtabs [data-subtab]").forEach(function (btn) {
      btn.classList.toggle("subtab-btn-active", btn.getAttribute("data-subtab") === state.activeScreen);
    });
    if (state.activeScreen === "scr-006") {
      el("scr-006-body").classList.remove("screen-hidden");
      el("scr-007-body").classList.add("screen-hidden");
      renderScr006();
    } else {
      el("scr-006-body").classList.add("screen-hidden");
      el("scr-007-body").classList.remove("screen-hidden");
      renderScr007();
    }
  }

  // ---- SCR-006 — Paper Execution Initiation ----

  function renderScr006() {
    var body = el("scr-006-body");

    // NAV-004 "Required context," checked in order: (1) Account/Instrument/Venue validity,
    // (2) Strategy Instance selected+pinned for Paper, (3) eligible PAPER-context Decision
    // lineage. Each cause disclosed distinctly — never collapsed into one generic message.
    if (!state.accountValid) {
      body.innerHTML =
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-003 — invalid Account/Instrument/Venue</div>' +
        "<div>The current Account/Instrument/Venue context is not valid for initiating PAPER " +
        "execution. Read-only navigation to this destination remains available; initiation is " +
        "blocked until a valid context resolves.</div>" +
        "</div>";
      return;
    }
    if (state.paperPin === "none") {
      body.innerHTML =
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-028 — Paper Strategy Instance not selected</div>' +
        "<div>No Strategy Instance has been selected for this Paper interaction. This pin is " +
        "independent from any Replay/Backtest pin — it is never silently carried over.</div>" +
        '<div class="exit-row"><button class="btn btn-primary" id="btn-select-pin">Select + pin Strategy Instance for Paper (via VIEW-001)</button></div>' +
        "</div>";
      el("btn-select-pin").addEventListener("click", function () {
        state.paperPin = "pinned";
        updateContextBar();
        renderScr006();
      });
      return;
    }
    if (state.paperPin === "selected") {
      body.innerHTML =
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-029 — Paper Strategy Instance selected but not pinned</div>' +
        "<div>" + MOCK_STRATEGY_CONTEXT.instanceLabel + " has been selected but is not yet pinned " +
        "for this Paper interaction.</div>" +
        '<div class="exit-row"><button class="btn btn-primary" id="btn-select-pin">Pin ' + MOCK_STRATEGY_CONTEXT.instanceLabel + ' for Paper</button></div>' +
        "</div>";
      el("btn-select-pin").addEventListener("click", function () {
        state.paperPin = "pinned";
        updateContextBar();
        renderScr006();
      });
      return;
    }
    if (!state.decisionAvailable) {
      body.innerHTML =
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-011 — PAPER Decision lineage unavailable</div>' +
        "<div>" + MOCK_STRATEGY_CONTEXT.instanceLabel + " is pinned for Paper, but no eligible " +
        "PAPER-context authoritative Decision lineage resolves for it. Workflow stops before " +
        "PAPER execution — no Trade Intent/RiskEvaluation/Execution Intent/Order is created. " +
        "Research/Replay/Backtest evidence, if viewed, informs judgment only and is never " +
        "authoritative input here.</div>" +
        "</div>";
      return;
    }

    // Eligible: show upstream Decision evidence (INV-3), visually separate from downstream
    // causation, then the initiation control.
    var html = '<div class="label-row">' +
      '<span class="mode-label">Paper</span>' +
      '<span class="authority-label authority-label-authoritative">Authority class: authoritative PAPER</span>' +
      '<span class="prototype-datum-label">Prototype datum: Illustrative / non-authoritative</span>' +
      "</div>" +
      el5("Account", MOCK_ACCOUNT_CONTEXT.account) +
      el5("Instrument", MOCK_ACCOUNT_CONTEXT.instrument) +
      el5("Venue", MOCK_ACCOUNT_CONTEXT.venue) +
      el5("Strategy Instance (pinned for Paper)", MOCK_STRATEGY_CONTEXT.instanceLabel + " (" + MOCK_STRATEGY_CONTEXT.instanceId + ")") +
      el5("Strategy Definition Version", MOCK_STRATEGY_CONTEXT.strategyDefinitionVersion) +
      el5("Configuration", MOCK_STRATEGY_CONTEXT.configurationVersion) +
      '<div class="evidence-group evidence-group-upstream">' +
      '<div class="evidence-group-label">Upstream PAPER Decision evidence (shown BEFORE initiation — resolved directly from recorded fact, NOT this Batch\'s Backtest Decision, NOT re-derived)</div>' +
      '<div style="margin-bottom:6px;"><span class="outcome-badge ' + (MOCK_PAPER_DECISION.outcome === "LONG" ? "outcome-long" : "outcome-short") + '">' + MOCK_PAPER_DECISION.outcome + "</span></div>" +
      el5("Decision identity", MOCK_PAPER_DECISION.id) +
      el5("Strategy Instance (origin)", MOCK_PAPER_DECISION.strategyInstance) +
      el5("Strategy Definition Version (origin)", MOCK_PAPER_DECISION.strategyDefinitionVersion) +
      el5("Recorded input snapshot", MOCK_PAPER_DECISION.inputSnapshot) +
      el5("Recorded evaluation evidence", MOCK_PAPER_DECISION.evaluationEvidence) +
      "</div>" +
      '<div class="hint">Initiating supplies intent only — no quantity/order type/sizing/fee/slippage/execution-model input is collected here; the system owns the entire downstream chain.</div>' +
      '<div id="scr-006-initiation-result"></div>' +
      '<div class="exit-row"><button class="btn btn-primary" id="btn-initiate">Initiate PAPER execution</button></div>';
    body.innerHTML = html;

    el("btn-initiate").addEventListener("click", function () {
      state.execution = buildExecutionChain(state.riskOutcome, state.executionOutcome);
      renderInitiationResult();
    });

    renderInitiationResult();
  }

  function renderInitiationResult() {
    var box = el("scr-006-initiation-result");
    if (!box) return;
    if (!state.execution) { box.innerHTML = ""; return; }

    var ex = state.execution;
    var html = "";
    if (ex.riskEvaluation.result === "REJECTED") {
      html = '<div class="panel panel-fail">' +
        '<div class="panel-title">STATE-013 — Risk REJECTED</div>' +
        "<div>RiskEvaluation " + ex.riskEvaluation.id + ": REJECTED (reason: " + ex.riskEvaluation.reasonCode +
        "). Chain stops here — no Execution Intent, Order, OrderSubmissionRequest, " +
        "ExecutionResultComputation, PaperExecutionObservation, ExecutionResult, or Fill created.</div>" +
        "</div>";
    } else if (ex.riskEvaluation.result === "NON_EVALUABLE") {
      html = '<div class="panel panel-indeterminate">' +
        '<div class="panel-title">STATE-014 — Risk NON_EVALUABLE</div>' +
        "<div>RiskEvaluation " + ex.riskEvaluation.id + ": NON_EVALUABLE (reason: " + ex.riskEvaluation.reasonCode +
        "). Same stop boundary as REJECTED — no Execution Intent, Order, OrderSubmissionRequest, " +
        "ExecutionResultComputation, PaperExecutionObservation, ExecutionResult, or Fill created.</div>" +
        "</div>";
    } else if (ex.executionResult.resultType === "NOT_EXECUTED") {
      html = '<div class="panel panel-blocked">' +
        '<div class="panel-title">RiskEvaluation APPROVED → STATE-016 ExecutionResult NOT_EXECUTED</div>' +
        "<div>Order " + ex.order.id + " submitted (" + ex.submissionRequest.id + "); " +
        "ExecutionResultComputation " + ex.executionResultComputation.id + " authorized; " +
        "PaperExecutionObservation " + ex.paperExecutionObservation.id + " recorded (result_type NOT_EXECUTED); " +
        "ExecutionResult " + ex.executionResult.id + ": NOT_EXECUTED. Zero Fill.</div>" +
        '<button class="btn" id="btn-view-detail" style="margin-top:8px;">View full detail →</button>' +
        "</div>";
    } else {
      html = '<div class="panel panel-passed">' +
        '<div class="panel-title">RiskEvaluation APPROVED → STATE-015 ExecutionResult EXECUTED</div>' +
        "<div>Order " + ex.order.id + " submitted (" + ex.submissionRequest.id + "); " +
        "ExecutionResultComputation " + ex.executionResultComputation.id + " authorized; " +
        "PaperExecutionObservation " + ex.paperExecutionObservation.id + " recorded (result_type EXECUTED); " +
        "ExecutionResult " + ex.executionResult.id + ": EXECUTED; exactly one Fill (" + ex.fill.id + ") recorded.</div>" +
        '<button class="btn" id="btn-view-detail" style="margin-top:8px;">View full detail →</button>' +
        "</div>";
    }
    box.innerHTML = html;
    var btn = el("btn-view-detail");
    if (btn) {
      btn.addEventListener("click", function () {
        state.activeScreen = "scr-007";
        renderPaperSection();
      });
    }
  }

  // ---- SCR-007 — Paper Order/Execution Detail ----

  function renderScr007() {
    var body = el("scr-007-body");

    // STATE-002 applies whenever no Order/Fill exists yet (ux-blueprint.md §11 STATE-002 row:
    // "chưa Order/Fill nào tồn tại") — this covers BOTH "nothing initiated yet" AND "initiated,
    // but RiskEvaluation REJECTED/NON_EVALUABLE truncated the chain before Order was ever
    // created" (INV-4: Order never exists in either truncation branch). The RiskEvaluation
    // outcome itself remains fully visible on SCR-006's own initiation-result panel.
    if (!state.execution || !state.execution.order) {
      var reasonNote = state.execution
        ? " A PAPER execution was initiated, but RiskEvaluation " + state.execution.riskEvaluation.id +
          " resulted in " + state.execution.riskEvaluation.result + " (reason: " +
          state.execution.riskEvaluation.reasonCode + ") — the chain stopped before an Order was " +
          "created, so there is still nothing here to inspect. See the Initiation tab for the " +
          "RiskEvaluation evidence."
        : " Initiate a PAPER execution from the Initiation tab first.";
      body.innerHTML =
        '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-002 — empty</div>' +
        "<div>No Order/Fill exists yet for this Paper interaction." + reasonNote + "</div>" +
        "</div>";
      return;
    }

    var html = '<div class="label-row">' +
      '<span class="mode-label">Paper</span>' +
      '<span class="authority-label authority-label-authoritative">Authority class: authoritative PAPER</span>' +
      '<span class="prototype-datum-label">Prototype datum: Illustrative / non-authoritative</span>' +
      "</div>" +
      el5("Strategy Instance (pinned, continuous from SCR-006)", MOCK_STRATEGY_CONTEXT.instanceLabel + " (" + MOCK_STRATEGY_CONTEXT.instanceId + ")") +
      el5("Strategy Definition Version", MOCK_STRATEGY_CONTEXT.strategyDefinitionVersion) +
      el5("Account", MOCK_ACCOUNT_CONTEXT.account) +
      el5("Instrument", MOCK_ACCOUNT_CONTEXT.instrument) +
      el5("Venue", MOCK_ACCOUNT_CONTEXT.venue) +
      el5("Decision lineage", MOCK_PAPER_DECISION.id + " (" + MOCK_PAPER_DECISION.outcome + ")") +
      '<div class="subtab-row" id="scr-007-tabs">' +
      '<button class="subtab-btn" data-tab="result">ExecutionResult</button>' +
      '<button class="subtab-btn" data-tab="fill">Fill evidence</button>' +
      '<button class="subtab-btn" data-tab="position">Position</button>' +
      '<button class="subtab-btn" data-tab="safety">No-real-exchange</button>' +
      "</div>" +
      '<div id="scr-007-tab-body"></div>' +
      '<div class="exit-row">' +
      '<button class="btn" data-nav="NAV-005" data-target="screen-deferred" data-stage="Review">Continue to Review</button>' +
      '<p class="hint">SCR-008 (Decision → Position Lineage Trace) is not authored in Batch 04 — this is a deferred handoff only.</p>' +
      "</div>";
    body.innerHTML = html;

    if (!state.scr007Tab) state.scr007Tab = "result";
    body.querySelectorAll("[data-tab]").forEach(function (btn) {
      btn.classList.toggle("subtab-btn-active", btn.getAttribute("data-tab") === state.scr007Tab);
      btn.addEventListener("click", function () {
        state.scr007Tab = btn.getAttribute("data-tab");
        renderScr007Tab();
      });
    });
    renderScr007Tab();
    wireGlobalNav(body);
  }

  function renderScr007Tab() {
    var body = el("scr-007-tab-body");
    if (state.scr007Tab === "result") body.innerHTML = renderExecutionResultTab();
    else if (state.scr007Tab === "fill") body.innerHTML = renderFillTab();
    else if (state.scr007Tab === "position") body.innerHTML = renderPositionTab();
    else body.innerHTML = renderSafetyTab();
  }

  // UC-012 — ExecutionResult: STATE-015 EXECUTED / STATE-016 NOT_EXECUTED (zero Fill explicit).
  // Reached only when state.execution.order exists (renderScr007's STATE-002 gate) — by
  // buildExecutionChain's construction, order only exists when riskEvaluation.result ===
  // "APPROVED", so that branch is not re-checked here. ExecutionResultComputation/
  // PaperExecutionObservation identities exposed as supporting evidence (closes
  // P2-B04-A-MAJ-01) — kept to identity rows only, not a computation-debugging surface.
  function renderExecutionResultTab() {
    var ex = state.execution;
    if (ex.executionResult.resultType === "NOT_EXECUTED") {
      return '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-016 — ExecutionResult NOT_EXECUTED</div>' +
        el5("ExecutionResult identity", ex.executionResult.id) +
        el5("Order", ex.order.id) +
        el5("OrderSubmissionRequest", ex.submissionRequest.id) +
        el5("Execution Result Computation", ex.executionResultComputation.id + " (INITIAL)") +
        el5("PaperExecutionObservation", ex.paperExecutionObservation.id + " (result_type NOT_EXECUTED)") +
        el5("environment", "PAPER") +
        el5("Fill", "zero — none created") +
        "</div>";
    }
    return '<div class="panel panel-passed">' +
      '<div class="panel-title">STATE-015 — ExecutionResult EXECUTED</div>' +
      el5("ExecutionResult identity", ex.executionResult.id) +
      el5("Order", ex.order.id) +
      el5("OrderSubmissionRequest", ex.submissionRequest.id) +
      el5("Execution Result Computation", ex.executionResultComputation.id + " (INITIAL)") +
      el5("PaperExecutionObservation", ex.paperExecutionObservation.id + " (result_type EXECUTED)") +
      el5("environment", "PAPER") +
      el5("Fill", "exactly one — " + ex.fill.id) +
      "</div>";
  }

  // UC-013 — Fill simulation evidence + economics, matching the SAME PaperExecutionObservation
  // as the ExecutionResult above (execution_observation_id equality, fill.md v0.2). Simulation
  // evidence axes now read from ex.paperExecutionObservation (their actual owner per
  // execution-result.md §1), not from the Fill object itself — Fill only owns economics, copied
  // exactly from the Observation (see buildExecutionChain()).
  function renderFillTab() {
    var ex = state.execution;
    if (ex.executionResult.resultType === "NOT_EXECUTED") {
      return '<div class="panel panel-blocked">' +
        '<div class="panel-title">STATE-017 — Fill absent</div>' +
        "<div>ExecutionResult " + ex.executionResult.id + " is NOT_EXECUTED (PaperExecutionObservation " +
        ex.paperExecutionObservation.id + " recorded a NOT_EXECUTED result) — no Fill exists to inspect.</div>" +
        "</div>";
    }
    var f = ex.fill;
    var obs = ex.paperExecutionObservation;
    return '<div class="panel panel-passed">' +
      '<div class="panel-title">Fill ' + f.id + ' — economics (copied from PaperExecutionObservation ' + f.executionObservationId + ")</div>" +
      el5("Fill quantity", f.quantity + " " + f.quantityUnit) +
      el5("Fill price", f.price + " " + f.priceCurrency) +
      el5("Price currency", f.priceCurrency) +
      "</div>" +
      '<table class="simulation-table"><thead><tr><th>Axis</th><th>Reference</th></tr></thead><tbody>' +
      "<tr><td>Simulation policy</td><td>" + obs.simulationPolicyRef + "</td></tr>" +
      "<tr><td>Simulation configuration</td><td>" + obs.simulationConfigurationRef + "</td></tr>" +
      "<tr><td>Simulation build</td><td>" + obs.simulationBuildRef + "</td></tr>" +
      "<tr><td>Deterministic-input reference</td><td>" + obs.deterministicInputRef + "</td></tr>" +
      "</tbody></table>" +
      '<div class="hint">Economics and simulation evidence both come from PaperExecutionObservation ' + obs.id + ' — the same Observation referenced by the ExecutionResult tab — not independently recalculated.</div>';
  }

  // UC-014 — Position: FLAT/LONG/SHORT/NON_EVALUABLE, explicit, never guessed/collapsed/aggregated.
  // v1.1 (closes P2-B04-A-MAJ-02): NON_EVALUABLE now only ever renders with an explicit,
  // coherent evidence basis (see derivePosition()). When the override was requested but doesn't
  // apply (no current Fill to pair with the illustrative prior one), the TRUE state is shown
  // with a `demoNote` explaining why — surfaced on whichever branch (FLAT/LONG/SHORT) is
  // actually true, never silently dropped.
  function renderPositionTab() {
    var pos = derivePosition(state.execution, state.positionDemoOverride);
    var demoNoteHtml = pos.demoNote ? '<div class="hint">' + pos.demoNote + "</div>" : "";
    if (pos.status === "NON_EVALUABLE") {
      return '<div class="panel panel-indeterminate">' +
        '<div class="panel-title">STATE-021 — Position NON_EVALUABLE</div>' +
        "<div>More than one eligible Fill lineage contributes to this Account/Instrument position — " +
        "no single value is reported.</div>" +
        el5("contributing_fill_refs", pos.contributingFillRefs.join("; ")) +
        '<div class="hint">QA demonstration: one of the two contributing Fills is the current execution\'s real Fill; the other is an explicitly-labelled illustrative prior Fill (this prototype\'s single-initiation flow cannot itself naturally produce a second current Fill — see README).</div>' +
        "</div>";
    }
    if (!pos.direction) {
      return '<div class="panel">' +
        '<div class="panel-title">STATE-018 — Position FLAT</div>' +
        el5("net_quantity", "0") +
        "<div class=\"hint\">Zero eligible Fill for this Account/Instrument (Position is a derived projection, not an authoritative fact — position.md §1).</div>" +
        demoNoteHtml +
        "</div>";
    }
    var stateLabel = pos.direction === "LONG" ? "STATE-019 — Position LONG" : "STATE-020 — Position SHORT";
    return '<div class="panel panel-passed">' +
      '<div class="panel-title">' + stateLabel + "</div>" +
      el5("net_quantity", pos.netQuantity + " " + pos.quantityUnit) +
      el5("average_entry_price", pos.averageEntryPrice + " " + pos.priceCurrency) +
      "<div class=\"hint\">Position is a derived projection (position.md §1) — not an authoritative fact of its own.</div>" +
      demoNoteHtml +
      "</div>";
  }

  // UC-015 — no real exchange order. Always available regardless of chain state.
  function renderSafetyTab() {
    return '<div class="panel panel-passed">' +
      '<div class="panel-title">PAPER safety confirmation</div>' +
      el5("environment", "PAPER (every Order/ExecutionResult in this session)") +
      el5("Real exchange order placed", "No") +
      el5("Real exchange network route in this prototype", "None — no fetch/XHR/WebSocket exists in this file") +
      "<div class=\"hint\">This is a static representation of the environment=PAPER field, not a claim that a technical network audit was performed (out of scope, Phase 1).</div>" +
      "</div>";
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
        if (target === "screen-paper") renderPaperSection();
      });
    });
  }

  function wirePaperSubtabs() {
    document.querySelectorAll("#paper-subtabs [data-subtab]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        state.activeScreen = btn.getAttribute("data-subtab");
        renderPaperSection();
      });
    });
  }

  // ---- QA panel wiring ----

  function refreshQaActiveStates() {
    var map = {
      "acct-valid": state.accountValid === true,
      "acct-invalid": state.accountValid === false,
      "pin-none": state.paperPin === "none",
      "pin-selected": state.paperPin === "selected",
      "pin-pinned": state.paperPin === "pinned",
      "decision-available": state.decisionAvailable === true,
      "decision-unavailable": state.decisionAvailable === false,
      "risk-approved": state.riskOutcome === "APPROVED",
      "risk-rejected": state.riskOutcome === "REJECTED",
      "risk-non-evaluable": state.riskOutcome === "NON_EVALUABLE",
      "exec-executed": state.executionOutcome === "EXECUTED",
      "exec-not-executed": state.executionOutcome === "NOT_EXECUTED",
      "position-natural": !state.positionDemoOverride,
      "position-non-evaluable": state.positionDemoOverride === "non-evaluable"
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
        if (qa === "acct-valid") state.accountValid = true;
        else if (qa === "acct-invalid") state.accountValid = false;
        else if (qa === "pin-none") state.paperPin = "none";
        else if (qa === "pin-selected") state.paperPin = "selected";
        else if (qa === "pin-pinned") state.paperPin = "pinned";
        else if (qa === "decision-available") state.decisionAvailable = true;
        else if (qa === "decision-unavailable") state.decisionAvailable = false;
        else if (qa === "risk-approved") state.riskOutcome = "APPROVED";
        else if (qa === "risk-rejected") state.riskOutcome = "REJECTED";
        else if (qa === "risk-non-evaluable") state.riskOutcome = "NON_EVALUABLE";
        else if (qa === "exec-executed") state.executionOutcome = "EXECUTED";
        else if (qa === "exec-not-executed") state.executionOutcome = "NOT_EXECUTED";
        else if (qa === "position-natural") state.positionDemoOverride = null;
        else if (qa === "position-non-evaluable") state.positionDemoOverride = "non-evaluable";

        updateContextBar();
        refreshQaActiveStates();
        showScreen("screen-paper");
        renderPaperSection();
      });
    });

    el("qa-reset").addEventListener("click", function () {
      state.accountValid = true;
      state.paperPin = "pinned";
      state.decisionAvailable = true;
      state.riskOutcome = "APPROVED";
      state.executionOutcome = "EXECUTED";
      state.execution = null;
      state.positionDemoOverride = null;
      state.activeScreen = "scr-006";
      updateContextBar();
      refreshQaActiveStates();
      showScreen("screen-paper");
      renderPaperSection();
    });
  }

  // ---- Init ----

  function init() {
    wireGlobalNav(document);
    wirePaperSubtabs();
    wireQaPanel();
    updateContextBar();
    refreshQaActiveStates();
    renderPaperSection();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
