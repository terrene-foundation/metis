# Playbook Phases 1–9 — Supervised ML (Frame → Codify)

This spec is the detail authority for phases 1, 2, 4, 5, 6, 7, 8, 9 of the Universal ML Decision Playbook. Phases 10–12 live in `playbook-phases-prescribe.md`; phases 13–14 live in `playbook-phases-mlops.md`. The cross-index stays in `playbook-universal.md`.

Each phase specifies: (a) sprints that run it, (b) trust-plane question, (c) prompt template, (d) evaluation checklist, (e) journal schema, (f) common failure modes, (g) the artefact that MUST exist on disk to claim the phase complete.

Week 4 runs phases 1, 2, 4, 5, 6, 7, 8 in Sprint 1 and Phase 9 in the Close block. Phase 3 is folded into Phase 2 for Week 4.

Trust Plane / Execution Plane capitalisation follows `terrene-naming.md`. Library API references follow kailash-ml source (see `wiring-contracts.md`) — if SKILL.md disagrees with source, source wins.

---

## Phase 1 — Frame

- **Sprints**: Sprint 1 (first ~7 min).
- **Trust-plane question**: What is the target, the population, the horizon, the cost of being wrong?
- **Prompt template**:
  > _"Read the product brief. I need a clear problem statement for the forecasting module. Tell me: what exactly are we predicting, for which locations, how far ahead, and what it costs when we get it wrong in each direction. A missed delivery costs us $40; excess capacity costs $12. Don't assume anything — if the brief is vague on scope, ask me."_
- **Evaluation checklist**:
  - [ ] Target variable precise (not "demand" but "orders per depot-day").
  - [ ] Population scope explicit.
  - [ ] Horizon named in days.
  - [ ] Cost asymmetry quantified as dollar figures with units attached, not a bare ratio.
  - [ ] No silent assumptions.
- **Journal schema**:
  ```
  Phase 1 — Frame
  Target: ____
  Population: ____
  Horizon: ____
  Cost asymmetry: $__ per ____ (under) vs $__ per ____ (over) = __:1
  What I would change my mind on: ____
  ```
- **Common failure modes**:
  - Target drifts into fuzzy language ("forecast demand") — downstream phases lose grounding.
  - Horizon left implicit — optimiser operates on wrong window.
  - Cost asymmetry stated as "3:1" ratio without dollars — scores 2/4 on Harm framing rubric.
- **Artefact**: `journal/phase_1_frame.md`.

---

## Phase 2 — Data Audit (includes folded Phase 3: Feature Framing)

- **Sprints**: Sprint 1 (~10 min).
- **Trust-plane question**: Is this data trustworthy? Which features are available at prediction time, leaky, or ethically loaded?
- **Prompt template**:
  > _"Audit the Northwind demand dataset before we train anything. I need to know: is the data trustworthy? Check for label errors, time leakage, missing values, bias in which customers appear, and any features that look suspiciously perfect. Then list every feature and tell me which ones are safe to use, which ones leak future info, and which ones might be ethically loaded. Recommend a feature set — I'll make the final call."_
- **Evaluation checklist**:
  - [ ] All 6 audit categories addressed with specifics (row X, col Y).
  - [ ] Every candidate feature classified on all four axes (available / leaky / ethically-loaded / engineered).
  - [ ] Ethically-loaded features (segment, region) have a rationale, not a drive-by "OK".
  - [ ] Engineered features have a derivation explanation.
  - [ ] Recommendation offered but not auto-applied.
- **Journal schema**:
  ```
  Phase 2 — Data Audit
  Accepted? Yes / Conditional / No
  Conditions applied: ____
  Known risks I am accepting: ____
  Features IN: ____
  Features OUT (with reason): ____
  ```
- **Common failure modes**:
  - DataExplorer output accepted as-is; no call made on any of the six categories.
  - Ethically-loaded features classified "OK" with no rationale.
  - Engineered feature added without derivation — becomes a leakage vector.
- **Artefact**: `journal/phase_2_data_audit.md`.

---

## Phase 3 — Feature Framing (FOLDED INTO PHASE 2 for Week 4)

Retained in the universal Playbook for generality — Weeks 5–8 may split it out if the domain justifies a dedicated pass. In Week 4, the Phase 2 artefact captures the feature in/out decisions.

- **Sprints**: none in Week 4.
- **Artefact**: embedded in `phase_2_data_audit.md`.

---

## Phase 4 — Model Candidates

- **Sprints**: Sprint 1 (~12 min). AutoML live-run uses `search_n_trials=5`, a `candidate_families` list of size 3, `search_strategy="random"` to stay under 90 s wall-clock. If `KAILASH_ML_AUTOML_QUICK=1` is set, the cap is defence-in-depth.
- **Trust-plane question**: Which 3–5 models are reasonable candidates for this problem?
- **Prompt template**:
  > _"Train 3 to 5 different forecasting models on the Northwind demand data using kailash-ml. I want a range of complexity — something simple and interpretable, something mid-range, and something powerful. Use time-series cross-validation so the comparison is fair. Keep it quick — 5 trials max. Show me a leaderboard comparing them all on the same metrics. Also compare against the pre-baked leaderboard in the data folder so I can see if my live run is in the right ballpark."_
- **Evaluation checklist**:
  - [ ] Candidates span a complexity range (Ridge + RandomForest + GradientBoosting; optionally XGBoost if preflight-verified).
  - [ ] Each candidate has a distinct reason for inclusion + a stated risk.
  - [ ] A naive baseline is cited from `AutoMLResult.baseline_recommendation` (kailash-ml computes this automatically).
  - [ ] All candidates trained on the SAME schema + SAME `EvalSpec` so the leaderboard is comparable.
- **Journal schema**: _(no journal entry — decision happens in Phase 5)_
- **Common failure modes**:
  - AutoML run triggered with `search_n_trials=30` — blows Sprint 1 budget (F1). `KAILASH_ML_AUTOML_QUICK=1` caps at 20; Sprint 1's default 5 stays well under.
  - `[xgb]` extra missing — if `XGBoostRegressor` is in `candidate_families`, kailash-ml logs a WARN and skips the candidate (the per-candidate try/except is in `AutoMLEngine.run`). Leaderboard will have one fewer row. Preflight is the forcing function; do NOT paper over with a silent substitute.
  - FeatureStore not populated — the handler calls `register_features` + `store` itself (idempotent after `fs_preload.py`).
  - Candidates trained on different fold definitions — impossible with a single shared `EvalSpec`.
  - Constructor fabricated as `AutoMLEngine(feature_store=..., model_registry=..., config=...)` — the #1 red-team finding; the constructor is positional `(pipeline, search, *, registry)` and the config goes to `.run()`, not `__init__`.
- **Artefact**: `data/leaderboard.json` (live run) + the pre-built `data/leaderboard_prebaked.json` (30-trial critique target).

---

## Phase 5 — Model Implications

- **Sprints**: Sprint 1 (~10 min). Also re-run in Sprint 3 on post-drift data.
- **Trust-plane question**: Given the leaderboard, which model do I stake my career on and why?
- **Prompt template**:
  > _"Compare the models on the leaderboard. For each one, tell me: how accurate is it, how stable is it across different time periods, how complex is it, and how long did it take to train. Then recommend one — but explain the trade-offs as if you're briefing someone who doesn't know what a random forest is. I'll make the final pick."_
- **Evaluation checklist**:
  - [ ] All candidates compared on identical metrics.
  - [ ] Headline advantage assessed as meaningful (multiple percent) vs noise (< 1%).
  - [ ] Fold-to-fold variance examined (tight vs fragile).
  - [ ] Complexity matches problem complexity (a 500-tree XGBoost beating LinReg by 0.3% is likely overfit).
  - [ ] Recommendation defensible in 30 seconds to a non-technical executive.
- **Journal schema**:
  ```
  Phase 5 — Model Selection
  Picked: ____ (ExperimentTracker run ID: ____)
  Rejected alternatives: ____
  Why not the top of the leaderboard, if applicable: ____
  What I would retrain with: ____
  ```
- **Common failure modes**:
  - Student picks top of leaderboard without checking fold variance — scores 2/4 on trade-off honesty.
  - Student accepts Claude Code's recommendation verbatim — no Trust Plane decision happened.
  - Prebaked vs live leaderboard confusion — student cites wrong run ID (grader catches it).
- **Artefact**: `journal/phase_5_model_selection.md` (and `journal/phase_5_postdrift.md` on Sprint 3 re-run).

---

## Phase 6 — Metric + Threshold

- **Sprints**: Sprint 1 (~10 min). Re-run in Sprint 3 on post-drift data.
- **Trust-plane question**: Which metric, which threshold, tied to what costs?
- **Prompt template**:
  > _"Given that a missed delivery costs us $40 and excess capacity costs $12, which accuracy metric should we optimise for? Show me three different confidence levels for the forecast — conservative, moderate, aggressive — and compute the expected cost of each in dollars. If peak season changes these economics, flag that. I will pick the level."_
- **Evaluation checklist**:
  - [ ] Metric choice tied to dollars, not aesthetics (MAPE vs RMSE resolved with cost logic).
  - [ ] Threshold/interval presented as a cost curve, not a single number.
  - [ ] Sensitivity analysis included (what flips the decision).
  - [ ] Expected business impact named in dollars.
- **Journal schema**:
  ```
  Phase 6 — Metric + Threshold
  Metric: ____ (reason: ____)
  Threshold/Interval: ____
  Expected business impact: $____
  Sensitivity flip point: ____
  ```
- **Common failure modes**:
  - Metric picked because "it's a percentage" without tying to $40/$12 asymmetry.
  - Interval width chosen without a cost curve.
  - Reversal condition stated as "if data changes" — 0/4 on rubric.
- **Artefact**: `journal/phase_6_metric_threshold.md` (and `journal/phase_6_postdrift.md` on Sprint 3 re-run).

---

## Phase 7 — Red-Team (AI Verify dimensions: Transparency, Robustness, Safety)

- **Sprints**: Sprint 1 (~10 min). Partially re-run in Sprint 3 (adversarial drift test).
- **Trust-plane question**: How does this model fail? What breaks it?
- **Prompt template**:
  > _"Try to break this model. I want to know three things: (1) Transparency — what is the model relying on most heavily? Could you explain to a non-technical ops manager why it made a specific prediction? (2) Robustness — where does it fail worst? Which customer segments, which weeks, which conditions? What happens when the data drifts? (3) Safety — if this model silently went wrong for a week, what's the dollar damage and who gets hurt? Rank every finding by severity. Fairness will be covered in Week 7."_
- **Evaluation checklist**:
  - [ ] **Transparency**: top feature named; ablation impact in MAPE; one-sentence plain-language explanation of a single prediction; if SHAP unavailable, `permutation_importance` fallback cited as a limitation.
  - [ ] **Robustness**: 3 worst segments with MAPE; 3 worst weeks; week-78 drift quantified.
  - [ ] **Safety**: tail-risk in dollars; degenerate-input behaviour; blast-radius memo naming who is harmed.
  - [ ] Fairness row ends with "deferred to Week 7 per Playbook" — explicit, not silent.
- **Journal schema**:
  ```
  Phase 7 — Red-Team (AI Verify)
  Transparency: top feature ____; ablation MAPE delta ____; one-sentence explanation ____
  Robustness: worst segments ____; worst weeks ____; week-78 behaviour ____
  Safety: worst-1% cost $____; degenerate behaviour ____; blast radius ____
  Fairness: deferred to Week 7 per Playbook
  Blockers: ____
  Accepted risks: ____
  Mitigations to ship with: ____
  ```
- **Common failure modes**:
  - Red-team stops at "the model sometimes over-predicts" — no specifics.
  - `ModelExplainer` run but output not surfaced as a Transparency finding (orphaned call).
  - Safety dimension skipped because the term feels abstract — grounding in the $220 SLA forces it concrete.
- **Artefact**: `journal/phase_7_red_team.md`.

---

## Phase 8 — Deployment Gate

- **Sprints**: Sprint 1 (~8 min). Re-run in Sprint 2 after the union-cap injection changes the plan.
- **Trust-plane question**: Ship or don't ship, and on what monitoring?
- **Prompt template**:
  > _"Write the go/no-go gate for deploying this model. Include: (1) what metric thresholds must hold for it to ship — tie them to the numbers from Phase 6, (2) what we monitor on day one — name the specific signals and when they should fire an alert, (3) what triggers an automatic rollback — a specific measurable signal, not 'if things look bad'. Then promote the model from staging to shadow in the registry so it's ready for production."_
- **Evaluation checklist**:
  - [ ] Go / no-go criteria are measurable (named metric thresholds).
  - [ ] Monitoring plan names specific metrics and alert thresholds.
  - [ ] Rollback trigger is automatable (a specific signal).
  - [ ] ModelRegistry stage transition executed (`staging → shadow` minimum) via `registry.promote_model`.
- **Journal schema**:
  ```
  Phase 8 — Deployment Gate
  Go / No-Go: ____
  Monitoring (metric + threshold): ____
  Rollback trigger (signal): ____
  ModelRegistry transition: staging → ____
  ```
- **Common failure modes**:
  - Illegal stage transition attempted (e.g. `production → staging`) — `ModelRegistry.promote_model` raises `ValueError` with the current stage and the legal set; grader's actionable message prints the transition table instead of a stack trace (F9).
  - Monitoring plan written as prose, no metric names — grader cannot verify.
  - Rollback trigger tied to a non-existent signal.
- **Artefact**: `journal/phase_8_gate.md` + a `ModelRegistry` record at stage `shadow` or higher. Post-union Sprint 2 re-run: `journal/phase_8_postunion.md` on the new plan's gate decision.

### ModelRegistry state machine (reference — source: `kailash_ml.engines.model_registry.VALID_TRANSITIONS`)

```
staging ──→ {shadow, production, archived}
shadow  ──→ {production, archived, staging}
production ──→ {archived, shadow}    # shadow is the rollback channel
archived ──→ {staging}
```

`promote_model(name, version, to_stage, reason=None)` is the only legal mutation. Transitions outside the table raise `ValueError`. The `_kml_model_transitions` audit table persists every attempt (from_stage, to_stage, reason, transitioned_at). Promotion to `production` automatically archives any existing `production` version for the same `name`.

---

## Phase 9 — Codify

- **Sprints**: Close block (last ~8 min of class).
- **Trust-plane question**: What transfers to the next domain?
- **Prompt template**:
  > _"Looking back at today's three sprints — what did we learn that applies to ANY ML product we build next week? Give me 3 transferable lessons. And what 2 things were specific to demand forecasting and route optimization that won't transfer? Add a 'Week 4 lessons' section to the Playbook."_
- **Evaluation checklist**:
  - [ ] 3 transferable lessons (domain-agnostic).
  - [ ] 2 domain-specific lessons (demand forecasting + VRP).
  - [ ] Lessons are actionable in Week 5 (not platitudes like "data quality matters").
  - [ ] Playbook delta appended to `PLAYBOOK.md`.
- **Journal schema**:
  ```
  Phase 9 — Codify
  Transferable:
  1. ____
  2. ____
  3. ____
  Domain-specific:
  1. ____
  2. ____
  ```
- **Common failure modes**:
  - Codify skipped because time ran out — systemic knowledge capture lost.
  - Lessons written as generic platitudes.
  - No distinction between transferable and domain-specific.
- **Artefact**: `journal/phase_9_codify.md` + `Week 4 delta` section in `PLAYBOOK.md`.
