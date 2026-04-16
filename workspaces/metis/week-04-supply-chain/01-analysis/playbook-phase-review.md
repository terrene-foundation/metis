# Playbook Phase Review — 14-Phase Universal ML Decision Playbook

**Purpose**: for each of the 14 phases, specify which sprint runs it, minimum evaluation criteria, common failure modes, and the artifact that MUST exist to claim the phase complete. This document is the basis for `PLAYBOOK.md`.

**Scope in Week 4**: phases 1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 13, 9 (9 moved to close). Phase 3 folded into Phase 2. Phase 14 deferred to Week 7.

---

## Phase 1 — Frame

**Sprint**: Sprint 1 (Forecast), first ~7 min.

**Trust-plane question**: What is the target, the population, the horizon, the cost of being wrong?

**Minimum evaluation criteria**:

- Target variable named precisely (not "demand" but "orders per depot-day").
- Population scope explicit (all depots? active customers only? peak season?).
- Horizon named in days.
- Cost asymmetry quantified in dollars using the `specs/business-costs.md` numbers.
- No silent assumptions ("I'll decide this later" is not acceptable).

**Common failure modes**:

- Target drifts into fuzzy language ("forecast demand"). Grader can't score downstream decisions.
- Horizon left implicit, so the optimizer downstream operates on the wrong time window.
- Cost asymmetry stated as a ratio but not a dollar figure ("3:1" is 2/4 per rubric; "$40 vs $12" is 4/4).

**Artifact**: `journal/phase_1_frame.md` — 5-line entry with target, population, horizon, cost asymmetry, reversal condition.

---

## Phase 2 — Data Audit (includes folded Phase 3 — Feature Framing)

**Sprint**: Sprint 1, ~10 min.

**Trust-plane question**: Is this data trustworthy? Which features are available at prediction time, leaky, or ethically loaded?

**Minimum evaluation criteria**:

- All 6 audit categories addressed with specifics (label quality, temporal leakage, survivorship bias, distribution shift, missingness, proxy variables).
- Each flagged issue has a concrete example (row X, column Y).
- Every candidate feature classified: (a) available at prediction time, (b) leaky with evidence, (c) ethically loaded, (d) engineered or raw.
- Recommendation offered but not auto-applied — the student's journal records the accept/reject decision.

**Common failure modes**:

- DataExplorer output accepted as-is; student doesn't make a call on any of the six categories.
- Ethically-loaded features (customer segment, region) classified as "OK" without a rationale.
- Engineered feature added without a derivation explanation.

**Artifact**: `journal/phase_2_data_audit.md` — accepted / conditional / no, conditions applied, risks accepted, features in / out.

---

## Phase 3 — Feature Framing (FOLDED INTO PHASE 2 in Week 4)

Retained in the 14-phase Playbook for generality (other weeks may split). In Week 4, the Phase 2 artifact includes the feature list.

---

## Phase 4 — Model Candidates

**Sprint**: Sprint 1, ~12 min. AutoML live-run uses `search_n_trials=5, families=3, search_strategy="random"` to stay under 90s wall-clock.

**Trust-plane question**: Which 3-5 models are reasonable candidates?

**Minimum evaluation criteria**:

- Candidates span a complexity range (not 5 variants of XGBoost).
- Each candidate has a distinct reason for inclusion and a risk.
- A naive baseline is included ("predict last week").
- All candidates train on the SAME schema and SAME splits (else comparison is invalid).

**Common failure modes**:

- AutoML run triggers with the old `search_n_trials=30` number and blows the sprint budget (F1).
- `[xgb]` extra missing; XGBoost candidate fails (F4); AutoML crashes.
- FeatureStore ingest skipped; TrainingPipeline errors (F10).
- Candidates trained on different fold definitions; leaderboard misleading.

**Artifact**: `data/leaderboard.json` (live run) + scaffolded `data/leaderboard_prebaked.json` (30-trial critique target). No journal entry — Phase 5 journals the decision.

---

## Phase 5 — Model Implications

**Sprint**: Sprint 1, ~10 min. Also re-run in Sprint 3 on post-drift data.

**Trust-plane question**: Given the leaderboard, which model do I stake my career on and why?

**Minimum evaluation criteria**:

- All candidates compared on identical metrics.
- Headline advantage assessed as meaningful (multiple percent) vs noise (<1%).
- Fold-to-fold variance examined (tight vs fragile).
- Complexity vs problem-complexity assessed (500-tree XGBoost beating LinReg by 0.3% is likely overfit).
- Recommendation defensible in 30 seconds to a non-technical executive.

**Common failure modes**:

- Student picks the top of the leaderboard without checking fold variance; journal entry scores 2/4 on trade-off honesty.
- Student accepts Claude Code's recommendation verbatim; no trust-plane decision happened.
- Prebaked leaderboard vs live leaderboard confusion — student cites the wrong run ID.

**Artifact**: `journal/phase_5_model_selection.md` — chosen model + ExperimentTracker run ID, rejected alternatives, why-not-top-of-leaderboard, what-I-would-retrain-with.

---

## Phase 6 — Metric + Threshold

**Sprint**: Sprint 1, ~10 min. Also re-run in Sprint 3 on post-drift data.

**Trust-plane question**: Which metric, which threshold, tied to what costs?

**Minimum evaluation criteria**:

- Metric choice tied to dollars (MAPE vs RMSE resolved with cost logic, not aesthetics).
- Prediction interval / threshold presented as a curve, not a single number.
- Sensitivity analysis included ("at peak season costs shift; re-tune weekly").
- Expected business impact named in dollars.

**Common failure modes**:

- Student picks MAPE because "it's a percentage" without tying it to the $40/$12 asymmetry.
- Interval width chosen without a cost curve.
- Reversal condition stated as "if data changes" — 0/4 per rubric.

**Artifact**: `journal/phase_6_metric_threshold.md` — metric, threshold/interval, expected business impact, sensitivity flip point.

---

## Phase 7 — Red-Team (expanded to cover AI Verify: Transparency, Robustness, Safety)

**Sprint**: Sprint 1, ~10 min. Partially re-run in Sprint 3 (adversarial drift test).

**Trust-plane question**: How does this model fail? What breaks it?

**Minimum evaluation criteria** (3-dimension AI Verify structure):

- **Transparency**: top feature by importance named; feature-ablation impact in MAPE; one-sentence plain-language explanation of a single prediction.
- **Robustness**: 3 worst customer segments named with MAPE; 3 worst calendar weeks; behavior on week-78 drift event quantified.
- **Safety**: cost of worst 1% of predictions in dollars; behavior on degenerate inputs (zero demand, missing features); blast-radius memo naming who is harmed.
- Fairness row ends with "deferred to Week 7" pointer — explicit deferral, not silent drop.

**Common failure modes**:

- Red-team stops at "the model sometimes over-predicts" — no specifics.
- ModelExplainer run but output not surfaced as a Transparency finding.
- Safety dimension skipped because the term "safety" feels abstract; grounding in the $220 SLA cost forces it concrete.

**Artifact**: `journal/phase_7_red_team.md` — per-dimension findings, blockers, accepted risks, mitigations to ship with.

---

## Phase 8 — Deployment Gate

**Sprint**: Sprint 1, ~8 min. Re-run in Sprint 2 after scenario injection changes the plan.

**Trust-plane question**: Ship or don't ship, and on what monitoring?

**Minimum evaluation criteria**:

- Go / no-go criteria are measurable (named metric thresholds, not "looks good").
- Monitoring plan names specific metrics and alert thresholds.
- Rollback trigger is automatable (a specific signal, not "if things look bad").
- ModelRegistry stage transition executed (staging -> shadow at minimum).

**Common failure modes**:

- Illegal stage transition attempted (F9) — e.g. `production -> staging`. Grader catches and prints the transition table.
- "Monitoring plan" written as prose, no metric names — grader cannot verify downstream.
- Rollback trigger tied to a non-existent signal.

**Artifact**: `journal/phase_8_gate.md` — go/no-go, monitoring plan (metrics + thresholds), rollback trigger. Plus a ModelRegistry record in the shipped registry DB.

---

## Phase 9 — Codify

**Sprint**: Close block (last ~8 min of class).

**Trust-plane question**: What transfers to the next domain?

**Minimum evaluation criteria**:

- 3 lessons that transfer to any ML product (domain-agnostic).
- 2 lessons specific to demand forecasting (domain-specific).
- Playbook delta appended to `PLAYBOOK.md` under a `Week 4 delta` section.

**Common failure modes**:

- Codify skipped because time ran out — systemic knowledge capture lost.
- Lessons written as generic platitudes ("data quality matters") — not actionable in Week 5.
- No distinction between transferable and domain-specific.

**Artifact**: `journal/phase_9_codify.md` + the `Week 4 delta` section in `PLAYBOOK.md`.

---

## Phase 10 — Objective Function

**Sprint**: Sprint 2, ~12 min.

**Trust-plane question**: Single or multi-objective? What are the weights?

**Minimum evaluation criteria**:

- Every term in the objective has a cost in real money or justified proxy.
- Single-objective version AND multi-objective version both presented.
- Weights in the multi-objective are defended with business reasoning.
- Recommendation discusses trade-off honestly ("carbon weight of $8/kg is below social cost of carbon; revise next year").

**Common failure modes**:

- Objective written in math-y language without business grounding.
- Carbon term dropped because "client didn't ask" — yet the deck emphasizes ESG; student loses a journal dimension.
- Weights pulled from thin air with no defense — 0/4 on trade-off honesty.

**Artifact**: `journal/phase_10_objective.md` — chosen function, weights, business justification.

---

## Phase 11 — Constraint Classification

**Sprint**: Sprint 2, ~10 min. Re-run after union-cap injection.

**Trust-plane question**: Hard or soft for each rule? Penalty for soft?

**Minimum evaluation criteria**:

- Every constraint classified with explicit rationale (law, physics, contract, preference).
- Soft constraints have defensible penalty values.
- No constraint left as "probably hard" without reason.
- Re-classification after injection: the union-cap becomes hard (labor law / contract). Student must recognize this.

**Common failure modes**:

- Union-cap mis-classified as soft after injection (the injection exists precisely to test this).
- Hard-constraint set too tight; solver infeasible; student panics. Recovery: re-classify one as soft.
- Penalty values unspecified ("some penalty") — 1/4 on classification rubric.

**Artifact**: `journal/phase_11_constraints.md` + `journal/phase_11_postunion.md` (after injection). Explicit before/after required per F6 mitigation.

---

## Phase 12 — Solver Acceptance

**Sprint**: Sprint 2, ~10 min. Re-run after union-cap injection.

**Trust-plane question**: Is the solution feasible, optimal, edge-case safe?

**Minimum evaluation criteria**:

- Every hard constraint confirmed satisfied (explicit yes/no table).
- Optimality gap reported numerically.
- Pathologies named (driver imbalance, zigzags, underutilization).
- Accept / re-solve / re-design decision defended.

**Common failure modes**:

- Solver returns feasible but pathological plan (one driver 95% of work). Student accepts because "solver said feasible" — 1/4 on trade-off honesty.
- Optimality gap not reported (OR-Tools reports it; student doesn't surface it).
- Scenario injection state corruption (F6): `route_plan.json` overwritten without `_preunion` snapshot; before/after comparison impossible.

**Artifact**: `data/route_plan_preunion.json` + `data/route_plan_postunion.json` + `journal/phase_12_solver.md` (before) + `journal/phase_12_postunion.md` (after).

---

## Phase 13 — Drift Triggers

**Sprint**: Sprint 3, ~15 min.

**Trust-plane question**: When do we retrain? What is the rule?

**Minimum evaluation criteria**:

- `DriftMonitor.set_reference_data` called (auto-wired by `drift_wiring.py`, but student must confirm).
- `check_drift` output surfaced (statistical test names + statistics + severity + recommendations).
- Each proposed signal has a threshold grounded in historical variance, not a guess.
- Duration window prevents retrain-on-spike (e.g. "sustained 7 days", not "one spike").
- Retrain decision stays in trust plane — human-in-the-loop reasoning defended. No `if X > Y then retrain` encoded as agent logic (violates `agent-reasoning.md`).

**Common failure modes**:

- Set-reference-data step skipped (F8) — mitigated by scaffold but student must still cite it.
- Threshold guessed ("15% feels right") with no variance grounding — 1/4 on reversal condition.
- Agent-reasoning violation: student asks Claude Code to "auto-retrain when MAPE > 15%" — prompt must be reframed as "signals and thresholds for operator monitoring, with human deciding."

**Artifact**: `data/drift_report.json` + `journal/phase_13_retrain.md` — signals, thresholds, duration, human-in-the-loop justification.

---

## Phase 14 — Fairness Audit (DEFERRED TO WEEK 7)

Not run in Week 4. Phase 7 journal entries include a one-line "Fairness audit deferred to Week 7 per Playbook" so the deferral is explicit, not silent. Week 7 (healthcare + credit) is the natural home — protected classes and disparate-impact testing get a full treatment there.

---

## Summary table

| #   | Phase                | Sprint  | Artifact                                                                  | Rubric dimensions pressured       |
| --- | -------------------- | ------- | ------------------------------------------------------------------------- | --------------------------------- |
| 1   | Frame                | S1      | `journal/phase_1_frame.md`                                                | Harm framing, metric-cost linkage |
| 2   | Data audit + feat    | S1      | `journal/phase_2_data_audit.md`                                           | Trade-off honesty                 |
| 3   | (folded)             | —       | (folded into phase 2)                                                     | —                                 |
| 4   | Candidates           | S1      | `data/leaderboard.json` + `data/leaderboard_prebaked.json`                | (no journal — decision in 5)      |
| 5   | Implications         | S1 + S3 | `journal/phase_5_model_selection.md`                                      | Trade-off honesty, reversal       |
| 6   | Metric + threshold   | S1 + S3 | `journal/phase_6_metric_threshold.md`                                     | Metric-cost linkage, reversal     |
| 7   | Red-team (AI Verify) | S1 + S3 | `journal/phase_7_red_team.md`                                             | All 5 dimensions                  |
| 8   | Deployment gate      | S1 + S2 | `journal/phase_8_gate.md` + ModelRegistry record                          | Reversal, constraint              |
| 9   | Codify               | Close   | `journal/phase_9_codify.md` + `PLAYBOOK.md` delta                         | (meta — not scored on rubric)     |
| 10  | Objective            | S2      | `journal/phase_10_objective.md`                                           | Metric-cost linkage, trade-off    |
| 11  | Constraints          | S2 × 2  | `journal/phase_11_constraints.md` + `journal/phase_11_postunion.md`       | Constraint classification         |
| 12  | Solver acceptance    | S2 × 2  | `data/route_plan_*.json` + `journal/phase_12_solver.md` + `_postunion.md` | Trade-off honesty, constraint     |
| 13  | Drift triggers       | S3      | `data/drift_report.json` + `journal/phase_13_retrain.md`                  | Reversal condition                |
| 14  | Fairness             | Week 7  | (deferred)                                                                | —                                 |

Total journal entries in Week 4: **11** (phases 1, 2, 5, 6, 7, 8, 9, 10, 11 × 2, 12 × 2, 13) = 13 journal entries if both pre/post-injection counted. At 5 dimensions × 0-4 per entry, the cohort has 65 scoring opportunities — enough variance to produce a meaningful grade distribution.

## Orphan-detection audit

Every phase names an artifact that lands on disk. Grader script `scripts/grade_product.py` iterates the phase list and confirms the artifact exists. No orphaned phases.
