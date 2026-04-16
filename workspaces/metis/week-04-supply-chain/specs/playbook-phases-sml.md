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
  > _"Read `PRODUCT_BRIEF.md` and produce a one-paragraph ML problem statement for the Forecast module. Include: target variable (precise name + unit), unit of prediction (per what, per when), population scope (all depots? active customers only? peak season?), prediction horizon in days, and cost asymmetry in dollars with units attached (e.g. `$40 per unit short of demand` vs `$12 per unit of excess capacity deployed`) using the numbers in `specs/business-costs.md`. No silent assumptions — if anything is ambiguous, ask me."_
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
  > _"Audit `data/northwind_demand.csv` with `kailash_ml.DataExplorer`. For each of six categories — label quality, temporal leakage, survivorship bias, distribution shift, missingness pattern, proxy variables — report specific findings with row indexes and column names. Then list every candidate feature and classify each as: (a) available at prediction time, (b) leaky with evidence, (c) ethically loaded, (d) engineered or raw. Recommend an initial feature set; I will decide."_
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
  > _"Load `data/northwind_demand.csv` into a Polars DataFrame. Build the `FeatureSchema` imported from `specs/schemas/demand.py`. Populate the FeatureStore exactly once (idempotent; `fs_preload.py` runs the same calls on Nexus startup) by awaiting `fs.register_features(schema)` followed by `fs.store(schema, df)` — NOT a non-existent `fs.ingest()`. Construct `TrainingPipeline(feature_store=fs, registry=registry)` and `HyperparameterSearch(pipeline=pipeline, registry=registry)`. Build `AutoMLConfig(task_type='regression', metric_to_optimize='mape', candidate_families=['sklearn.linear_model.Ridge', 'sklearn.ensemble.RandomForestRegressor', 'sklearn.ensemble.GradientBoostingRegressor'], search_strategy='random', search_n_trials=5, auto_approve=False)` — note the field name is `candidate_families`, NOT `families`. Build `EvalSpec(metrics=['mape','rmse'], split_strategy='walk_forward', test_size=0.2)` — `split_strategy='walk_forward'` is the library's supported name for time-series rolling-origin evaluation; `cv_strategy='rolling_origin'` is NOT a valid EvalSpec value. Instantiate `AutoMLEngine(pipeline, search, registry=registry)` — positional `pipeline` + `search`, keyword-only `registry`; `feature_store`/`model_registry`/`config` are NOT constructor kwargs. Call `result = await engine.run(data=df, schema=schema, config=config, eval_spec=eval_spec, experiment_name='forecast_sprint1', tracker=tracker)`. Only add `XGBoostRegressor` to `candidate_families` if `preflight.json.xgb_available` is true; otherwise omit it (do NOT silently substitute). Write the resulting per-family leaderboard to `data/leaderboard.json` and render in the Viewer."_
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
  > _"Compare the leaderboard in `data/leaderboard.json` against the pre-baked leaderboard in `data/leaderboard_prebaked.json`. For each candidate, surface: headline MAPE, fold-to-fold variance, complexity class, training time, and `ExperimentTracker` run ID. Then recommend one model as the deployment candidate. Frame the trade-offs as if briefing a non-technical executive in 90 seconds of speech."_
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
  > _"For Northwind demand forecasting, propose an evaluation metric grounded in the business costs in `specs/business-costs.md` (stockout $40 per unit short of demand, overstock $12 per unit of excess capacity deployed). Then propose a prediction interval (50th / 80th / 95th percentile) and compute expected stockout + overstock cost at each width across the holdout. Include a sensitivity analysis ('at peak season costs shift; recommend re-tune weekly'). I will decide."_
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
  > _"Red-team the chosen forecast model across three AI Verify dimensions. (1) **Transparency**: run `ModelExplainer` — which feature does the model rely on most? If that feature were removed, how does headline MAPE change? Explain to the Ops Manager in one sentence why the model predicted last Tuesday's orders. If `ModelExplainer` raises `ImportError` because the `[explain]` extra (SHAP) is not installed, fall back to sklearn's `permutation_importance` via `kailash_ml.engines.model_visualizer` (no SHAP dependency) AND record the fallback explicitly in the journal entry as a cited limitation; preflight should have caught this pre-class, so treat the fallback as a recovery path, not a silent substitute. (2) **Robustness**: name the 3 worst customer segments by MAPE and the 3 worst calendar weeks; quantify behaviour on the week-78 drift event. (3) **Safety**: cost of the worst 1% of predictions in dollars; behaviour on zero-demand days and on days missing upstream features; who is harmed if this model silently fails for a week. Rank every finding by severity. Note: Fairness (AI Verify's 4th dimension) is deferred to Week 7 per the Playbook."_
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
  > _"Write the go/no-go gate for model `<model_name>` version `<N>` (the `{model_name}_v{N}` derivation is the surface form used by `/forecast/predict`; internally it resolves to `ModelRegistry.get_model(name, version=N)` — see `wiring-contracts.md`). Include: (1) go criteria — named metric thresholds from Phase 6 + no open HIGH red-team finding, (2) monitoring plan — specific metrics with alert thresholds, (3) rollback trigger — an automatable signal, not 'if things look bad'. Then call `await registry.promote_model(name, version, to_stage='shadow', reason='Phase 8 gate passed')` to transition from `staging → shadow`. Only the transitions in the table below are legal."_
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
  > _"`/codify` — For today's Forecast + Optimize + Monitor sprints, what 3 lessons transfer to any ML-powered product? What 2 lessons are specific to demand forecasting + VRP? Append a `Week 4 delta` section to `PLAYBOOK.md` and produce `journal/phase_9_codify.md`."_
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
