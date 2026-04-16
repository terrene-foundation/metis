<!--
GENERATED — do not edit directly.
Source specs (edit these, then re-run scripts/build_playbook.py):
  - specs/playbook-universal.md      (summary table)
  - specs/playbook-phases-sml.md     (Phases 1–9)
  - specs/playbook-phases-prescribe.md (Phases 10–12)
  - specs/playbook-phases-mlops.md   (Phases 13–14)
-->

<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# The ML Decision Playbook — 14 Phases

**Version:** 2026-04-16 · **Generated:** 2026-04-16 from three source specs · **License:** CC BY 4.0

## How to use this Playbook

This is the student-facing procedure for every ML-powered product you commission — Week 4 and every week after. Read it once end-to-end before class so the shape is familiar. During class, keep it open; jump to the phase you are running.

Every phase follows the same shape:

- **Trust-plane question** — the single decision you own for this phase.
- **Prompt template** — what you type to Claude Code to execute the phase.
- **Evaluation checklist** — how you judge whether the output is good.
- **Journal schema** — what you record when you decide.
- **Common failure modes** — the 2–3 ways this phase usually goes wrong.
- **Artefact** — the file on disk that proves the phase happened.

Two planes are at work. The **Trust Plane** is you: framing, judging, approving. The **Execution Plane** is Claude Code plus the kailash frameworks: code, trained models, solver runs, dashboards. If the answer is "what" or "how", Execution owns it. If the answer is "which", "whether", "who wins and who loses", or "is it good enough to ship" — Trust owns it, which means you own it.

## How to prompt — the delegation skill

This is the single most important skill the course teaches. You are a **commissioner**, not a coder. Your prompts should sound like a founder briefing a team — not like a developer dictating implementation.

**Every prompt you write should contain these 5 elements:**

1. **Objective** — what business outcome you want, in plain language. _"I need a forecast that tells us how many orders each depot will get tomorrow."_
2. **Boundaries** — what matters, what doesn't, what costs what. _"A missed delivery costs $40; excess capacity costs $12. Stability across time periods matters more than squeezing an extra 0.5% accuracy."_
3. **Expected output** — what deliverable you want back. _"Show me a comparison table. Recommend one. I decide."_
4. **Checks** — what could go wrong, what would make you change your mind. _"Flag anything that looks like it's relying too heavily on one feature — that could be data leakage."_
5. **Decision authority** — make clear what YOU will decide vs. what CC executes. _"You train and compare. I pick the model and set the threshold."_

**What your prompt should NEVER contain:**

- Library names, class names, function signatures, import paths
- Python code or code snippets
- API parameter names or configuration objects
- File paths to source code (data file paths are fine — that's context, not implementation)

Claude Code has the specs, the skills, and the framework documentation. It knows which libraries to use and how to call them. **If you tell it how, you're doing its job. If you tell it what and why, you're doing yours.**

**Bad prompt** (doing CC's job):

> _"Using kailash_ml.AutoMLEngine with AutoMLConfig(candidate_families=['sklearn.ensemble.GradientBoostingRegressor'...], search_strategy='random')..."_

**Good prompt** (doing YOUR job):

> _"Train 3-5 forecasting models ranging from simple to complex. Compare them fairly using time-series validation. Show me which one wins and why — in business terms, not algorithm terms. I'll pick."_

The prompt templates below model this style. Adapt them to your own words — the templates are starting points, not scripts.

## Phase summary

| #   | Phase                | Sprint  | Artefact                                                                  | Rubric dimensions pressured       |
| --- | -------------------- | ------- | ------------------------------------------------------------------------- | --------------------------------- |
| 1   | Frame                | S1      | `journal/phase_1_frame.md`                                                | Harm framing, metric-cost linkage |
| 2   | Data audit + feat    | S1      | `journal/phase_2_data_audit.md`                                           | Trade-off honesty                 |
| 3   | (folded into 2)      | —       | (in phase 2)                                                              | —                                 |
| 4   | Candidates           | S1      | `data/leaderboard.json` + `data/leaderboard_prebaked.json`                | (no journal — decision in 5)      |
| 5   | Implications         | S1 + S3 | `journal/phase_5_model_selection.md` + `phase_5_postdrift.md`             | Trade-off honesty, reversal       |
| 6   | Metric + threshold   | S1 + S3 | `journal/phase_6_metric_threshold.md` + `phase_6_postdrift.md`            | Metric-cost linkage, reversal     |
| 7   | Red-team (AI Verify) | S1 + S3 | `journal/phase_7_red_team.md`                                             | All 5 dimensions                  |
| 8   | Deployment gate      | S1 + S2 | `journal/phase_8_gate.md` + `phase_8_postunion.md` + ModelRegistry record | Reversal, constraint              |
| 9   | Codify               | Close   | `journal/phase_9_codify.md` + `PLAYBOOK.md` delta                         | (meta — not scored on rubric)     |
| 10  | Objective            | S2      | `journal/phase_10_objective.md`                                           | Metric-cost linkage, trade-off    |
| 11  | Constraints          | S2 × 2  | `journal/phase_11_constraints.md` + `phase_11_postunion.md`               | Constraint classification         |
| 12  | Solver acceptance    | S2 × 2  | `data/route_plan_*.json` + `journal/phase_12_solver.md` + `_postunion.md` | Trade-off honesty, constraint     |
| 13  | Drift triggers       | S3      | `data/drift_report.json` + `journal/phase_13_retrain.md`                  | Reversal condition                |
| 14  | Fairness             | Week 7  | (deferred)                                                                | —                                 |

Week 4 runs phases **1, 2, 4, 5, 6, 7, 8** in Sprint 1, **10, 11, 12** in Sprint 2, **13** in Sprint 3, and **9** in the Close block. Phase 3 is folded into Phase 2. Phase 14 (Fairness) is deferred to Week 7.

---

# Sprint 1 — Supervised ML (Phases 1–9)

_Source: `specs/playbook-phases-sml.md`._

This is the detail authority for phases 1, 2, 4, 5, 6, 7, 8, 9 of the Universal ML Decision Playbook. Trust Plane / Execution Plane capitalisation follows `terrene-naming.md`. Library API references follow kailash-ml source (see `specs/wiring-contracts.md`) — if a skill file disagrees with source, source wins.

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

---

# Sprint 2 — Prescribe (Phases 10–12)

_Source: `specs/playbook-phases-prescribe.md`._

This is the detail authority for phases 10, 11, 12 of the Universal ML Decision Playbook — Sprint 2's Optimize block. Trust Plane / Execution Plane capitalisation follows `terrene-naming.md`.

---

## Phase 10 — Objective Function

- **Sprints**: Sprint 2 (~12 min).
- **Trust-plane question**: Single or multi-objective? What are the weights?
- **Prompt template**:
  > _"Design the objective for tomorrow's route plan. The costs are: fuel $0.35 per km, late delivery $220 per violation, overtime $45 per hour, carbon $8 per kg CO2. Show me two versions — one that lumps everything into a single cost, and one that treats cost, service level, and carbon as separate goals with weights. Recommend one and tell me honestly what each version sacrifices."_
- **Evaluation checklist**:
  - [ ] Every term has a cost in real money or a justified proxy.
  - [ ] Single-objective AND multi-objective both presented.
  - [ ] Weights defended with business reasoning.
  - [ ] Trade-off discussed honestly.
- **Journal schema**:
  ```
  Phase 10 — Objective
  Chosen: single / multi
  Terms + weights: ____
  Business justification: ____
  Known limitation: ____
  ```
- **Common failure modes**:
  - Objective written in math-y language without business grounding.
  - Carbon term dropped because "client didn't ask" — but the deck emphasises ESG; loses a dimension.
  - Weights pulled from thin air — 0/4 on trade-off honesty.
- **Artefact**: `journal/phase_10_objective.md`.

---

## Phase 11 — Constraint Classification

- **Sprints**: Sprint 2 (~10 min). Re-run after union-cap injection.
- **Trust-plane question**: Hard or soft for each rule? Penalty for soft?
- **Prompt template (first pass)**:
  > _"List every rule the route optimizer must respect — vehicle capacity, driver working hours, delivery time windows, anything else from the business brief. For each one, tell me: is it a hard line that can never be crossed (law or physics), or a preference we'd rather not violate but will if the cost is right? For preferences, propose a penalty in dollars. Justify each classification."_
- **Prompt template (post-injection re-run)**:
  > _"MOM just capped driver overtime at 5 hours per week — this is now law, not a preference. Update the constraint classification: which one changed from soft to hard? Re-justify it. Save this as a separate journal entry so we can compare before and after."_
- **Evaluation checklist**:
  - [ ] Every constraint classified with explicit rationale (law / physics / contract / preference).
  - [ ] Soft constraints have defensible penalty values.
  - [ ] No constraint labelled "probably hard" without reason.
  - [ ] Post-injection: union-cap correctly re-classified as hard (labour law / contract).
- **Journal schema** (both passes):
  ```
  Phase 11 — Constraints
  Hard: ____ (reason each)
  Soft: ____ (penalty each)
  What changed from prior pass (post-injection only): ____
  ```
- **Common failure modes**:
  - Union-cap mis-classified as soft after injection (the injection exists precisely to test this).
  - Hard-constraint set too tight → solver infeasible → student panics. Recovery: re-classify one as soft.
  - Penalty values unspecified ("some penalty") — 1/4 on classification rubric.
- **Artefact**: `journal/phase_11_constraints.md` + `journal/phase_11_postunion.md`.

---

## Phase 12 — Solver Acceptance

- **Sprints**: Sprint 2 (~10 min). Re-run after union-cap injection.
- **Trust-plane question**: Is the solution feasible, optimal, edge-case safe?
- **Prompt template**:
  > _"Run the route optimizer with the objective and constraints from the previous phases. Show me: did every hard constraint hold? How close to optimal is the plan? Are there any weird patterns — one truck doing all the work, routes that zigzag, vehicles sitting idle? Recommend whether I should accept this plan, re-solve with different settings, or redesign the problem. Save the plan so the dashboard can show it."_
- **Evaluation checklist**:
  - [ ] Every hard constraint confirmed satisfied — `hard_constraints_satisfied` response dict contains at least `vehicle_capacity` and `driver_hours_max` with value `true`.
  - [ ] Optimality gap reported numerically (OR-Tools produces this).
  - [ ] Pathologies named (driver imbalance, zigzags, underutilisation).
  - [ ] Accept / re-solve / re-design decision defended.
  - [ ] Post-injection: `_preunion` and `_postunion` both on disk, neither overwritten.
- **Journal schema**:
  ```
  Phase 12 — Solver Acceptance
  Feasibility: yes/no (per hard constraint)
  Optimality gap: ____
  Pathologies: ____
  Decision: Accept / Re-solve / Re-design
  What would make me re-design: ____
  ```
- **Common failure modes**:
  - Solver returns feasible but pathological plan (one driver 95% of work). Student accepts because "solver said feasible" — 1/4 on trade-off honesty.
  - Optimality gap not surfaced (OR-Tools reports it; student doesn't read it out).
  - Scenario-injection state corruption (F6): `route_plan.json` overwritten without `_preunion` snapshot. Recovery via `scripts/seed_route_plan.py` (see `scaffold-contract.md` §6).
- **Artefact**: `data/route_plan_preunion.json` + `data/route_plan_postunion.json` + `journal/phase_12_solver.md` + `journal/phase_12_postunion.md`.

---

# Sprint 3 — MLOps (Phases 13–14)

_Source: `specs/playbook-phases-mlops.md`._

This is the detail authority for phases 13 and 14 of the Universal ML Decision Playbook — Sprint 3's Monitor block, plus the deferred fairness audit. Trust Plane / Execution Plane capitalisation follows `terrene-naming.md`. Library API references follow kailash-ml source.

---

## Phase 13 — Drift Triggers

- **Sprints**: Sprint 3 (~15 min).
- **Trust-plane question**: When do we retrain? What is the rule?
- **Prompt template**:
  > _"Set up drift monitoring for the forecast model. First make sure the training data is registered as the baseline. Then run a drift check against the post-CNY data that just landed and show me: overall severity, which features shifted most, and what the system recommends. Based on the results, propose the signals and thresholds I should monitor going forward — how much drift before we retrain? Should that be an automatic trigger or should a human review first? Ground the thresholds in the data's actual historical variance, not round numbers."_
- **Evaluation checklist**:
  - [ ] `set_reference_data` confirmed active via `GET /drift/status/<model_id>` returning `reference_set: true` (or `.preflight.json.drift_wiring: true`); student must cite the verification in the journal.
  - [ ] `check_drift` output surfaced — per-feature `ks` and `psi` statistics (the two tests kailash-ml emits) + `overall_severity` (3-value enum) + recommendations.
  - [ ] Each proposed signal has a threshold grounded in historical variance, not a guess.
  - [ ] Duration window prevents retrain-on-spike (e.g. "sustained 7 days", not "one spike").
  - [ ] Retrain decision stays in Trust Plane — no `if X > Y` encoded as agent logic (see `agent-reasoning.md`).
- **Journal schema**:
  ```
  Phase 13 — Retrain Rule
  Signal(s): ____
  Threshold(s): ____ (historical variance grounding: ____)
  Duration window: ____
  Human-in-the-loop: yes / no (justification: ____)
  ```
- **Common failure modes**:
  - `set_reference_data` not called (F8) — should be prevented by `drift_wiring.wire()` fired synchronously by `/forecast/train`; `/drift/status` is the debug probe. If status shows `reference_set: false`, re-run `/forecast/train` or call `drift_wiring.wire()` manually.
  - Threshold guessed ("15% feels right") with no variance grounding — 1/4 on reversal condition.
  - Agent-reasoning violation: student asks Claude Code to "auto-retrain when MAPE > 15%". The prompt MUST be reframed as "signals and thresholds for operator monitoring". The 4/4 and 1/4 examples in `journal/_examples.md` make the difference concrete.
- **Artefact**: `data/drift_report.json` + `journal/phase_13_retrain.md`.

### DriftMonitor state machine (reference)

```
(no reference)
   │
   │  set_reference_data(model_name, reference_data, feature_columns)
   ▼
(reference_set, window_size=N)
   │
   ├── check_drift(model_name, current_data) → DriftReport (overall_severity ∈ {none, moderate, severe})
   │
   ├── schedule_monitoring(model_name, data_source_fn, interval_seconds)
   │       → background task running check_drift periodically
   │
   └── cancel_monitoring(model_name)
         → stops the background task

set_reference_data(same model_name, new data) updates the stored reference (UPDATE, not
INSERT); the in-memory cache is bounded to 100 references and evicts oldest.
```

---

## Phase 14 — Fairness Audit (DEFERRED TO WEEK 7)

Not run in Week 4. Phase 7 journal entries include a one-line "Fairness audit deferred to Week 7 per Playbook" so the deferral is explicit, not silent. Week 7 (healthcare + credit) is the natural home — protected classes and disparate-impact testing get a full treatment there.

- **Sprints**: none in Week 4.
- **Artefact**: deferred.
