<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Failure Points — LumenCircuit Industrial AI Suite

**Phase:** `/analyze` · **Author:** agent · **Date:** 2026-05-04
**Source:** read of `src/manufacturing/backend/{ml_context,startup,routes/*}.py` and `SCAFFOLD_MANIFEST.md`.

Twelve failure points across the four modules — three per module — each cited to a specific file and function in the scaffold. Each failure maps to the Playbook phase that catches it. Citations name `<file>::<function>`; line numbers are deliberately omitted because they drift across edits.

---

## Module 1 · Vision QC Inspector (Sprint 1 · Transfer Learning · See)

### F1.1 — Chosen architecture wins on macro_f1, hides per-class safety-critical recall miss

**Where it lives.** `src/manufacturing/backend/ml_context.py::build_vision_baseline` ranks the 3-architecture leaderboard by `chosen = max(candidates, key=lambda k: candidates[k].macro_f1)`. The `chosen_arch` is the macro-F1 winner; per-class recall on `safety_critical_defect` is not a tie-breaker. The result surfaces at `src/manufacturing/backend/routes/inspect_vision.py::leaderboard` which exposes `chosen_arch` and the per-class metrics — students who read only the headline number inherit the trap.

**What goes wrong.** Macro-F1 averages across all 4 classes equally (good / minor_defect / major_defect / safety_critical_defect). The safety-critical-defect class — the one that costs $4,200 per missed major + $1,000,000 WSH ceiling per `PRODUCT_BRIEF.md §2` — has the smallest weight in the ranking. An architecture with macro_f1 = 0.88 that achieves 0.55 recall on `safety_critical_defect` ranks above an architecture with macro_f1 = 0.84 and 0.78 recall on `safety_critical_defect`. The wrong architecture ships and the WSH-affecting class is the one that is silently weakest.

**Caught by.** Phase 5 Implications (Vision) — re-rank on per-class metrics, not macro — and Phase 6 Metric+Threshold (per-class threshold defense). The `/inspect/vision/leaderboard` response surfaces per-class P/R/F1 and the WSH safety floor; the Phase 5 journal must read the per-class numbers, not the headline macro_f1.

### F1.2 — Embeddings are deterministic per `image_id`; "live training" doesn't see new data

**Where it lives.** `ml_context.py::synthesise_image_embeddings` derives a per-(`image_id`, `arch`) seed and re-uses it on every call. `routes/inspect_vision.py::score` re-synthesises the embedding to keep the score stable across requests; `routes/inspect_vision.py::retrain` re-fits the same 3-architecture sweep on the same per-class Gaussian-centroid embeddings.

**What goes wrong.** A student who runs `POST /inspect/vision/train` with a different seed expects to see a fresh data sweep on actual ResNet/EfficientNet/ViT activations. They will see the leaderboard re-fit on synthesised embeddings. The pedagogy survives (the leaderboard ranks differently because the train/test split rotates with the seed), but a student who claims "I trained on 800 fresh PCB images" is wrong — the dataset is fixed at startup and the embeddings are surrogates per `SCAFFOLD_MANIFEST.md §"Implementation deviations"` row 1.

**Caught by.** Phase 4 Candidates (Vision) — read the actual sweep output rather than trusting the prompt — and Phase 7 Red-team (Vision) — the OOD test surfaces this when adversarial pixel perturbation does not change the per-class probabilities the way it would for a real CNN.

### F1.3 — Promote refuses below safety-critical hard floor; threshold POST does too — but promote-then-lower bypass

**Where it lives.** `routes/inspect_vision.py::promote` checks `sc < SAFETY_CRITICAL_HARD_FLOOR` and returns 422. `routes/inspect_vision.py::set_threshold` checks the same floor on `POST /inspect/vision/threshold`. Both gates exist independently and the floor constant is `ml_context.py::SAFETY_CRITICAL_HARD_FLOOR = 0.40`.

**What goes wrong.** The two checks are belt-and-suspenders defense for an honest student. The fail mode is procedural: a student promotes the chosen architecture at threshold = 0.5 (passes both gates), then later sets `safety_critical_defect` threshold = 0.35 (refused — 422) — but if they instead promote at 0.5 and never set the safety-critical-class threshold explicitly, the workspace `vision_thresholds.json` retains the default 0.40 floor; they can claim "I hit the WSH floor" without having reasoned about it. The floor is met by accident, not by design — the rubric's D5 (constraint honesty) reads this as a zero.

**Caught by.** Phase 6 Metric+Threshold (Vision) journal (must write the WSH-floor justification, not just hit it) and Phase 8 Gate (Vision) instructor review of threshold rationale.

---

## Module 2 · Predictive Maintenance Classifier (Sprint 2 · Time-Series ML · Predict)

### F2.1 — Window pick is silently independent of the family pick; cost asymmetry math runs twice

**Where it lives.** `routes/predict_maintenance.py::set_window` and `::set_family` are independent endpoints. `ml_context.py::build_predmaint_baseline` builds a leaderboard nested by window (3 / 7 / 14 days) AND family (`lightgbm_features` / `lstm_sequence` / `survival_forest_tte`); `chosen_window` and `chosen_family` are set independently at startup and are independently mutable via the two POST endpoints.

**What goes wrong.** A student picks the family on macro-F1 at the 7-day window (because the leaderboard happened to be sorted that way) and the window on FN/FP cost asymmetry separately — without ever checking that the chosen FAMILY is best at the chosen WINDOW. A family that wins at 14 days might place last at 3 days; the route does not enforce coherence. The $12,000 unplanned-stop vs $1,800 planned-stop ratio (6.7:1 per `business-costs.md`) is the right framing, but it gets applied to a leaderboard slice that does not match the chosen family's strength.

**Caught by.** Phase 5 Implications (PredMaint) — the journal must defend the (family, window) PAIR jointly, not the two halves separately — and Phase 8 Gate (PredMaint) instructor cross-check.

### F2.2 — Calibration check is computed at startup on the same data the family was fit on

**Where it lives.** `ml_context.py::_train_predmaint_family` computes the per-family `brier` at fit time on the held-out test split inside the same function; the value is then used at runtime via `routes/predict_maintenance.py::leaderboard` (read) and at startup in `startup.py` to register the predmaint drift baseline (`brier` field on the registered drift reference). There is no held-out-after-the-fact calibration check exposed via the route surface.

**What goes wrong.** A student looks at a low Brier across all three families and concludes "my predmaint classifier is well-calibrated tonight". The baseline was calibrated on the data it was fit on; the in-fit Brier is overoptimistic. Out-of-sample Brier — the metric that survives the next month of sensor stream — is bigger. The Phase 5 SML calibration check is weaker than the journal will claim, and the Phase 13 drift signal (`per_class_calibration_decay` from `routes/drift.py::check`) will be muted until the q4_demand_drift scenario fires.

**Caught by.** Phase 5 Implications (PredMaint) calibration check (push back if the Brier is suspiciously low across all three families and all three windows) and Phase 13 Drift (PredMaint) — the cadence-daily rule body must explicitly cite the in-sample-calibration caveat as the reason daily is the right cadence, not weekly.

### F2.3 — Score endpoint returns "model degenerate" warning silently if the chosen window has too few positive labels

**Where it lives.** `routes/predict_maintenance.py::score` checks `if entry.degenerate` and returns a payload with a `"warning": "model degenerate (too few positive labels in window)"` field, but the response status code is still 200 and there is no on-disk persistence of the degeneracy event.

**What goes wrong.** The 30-day × 10-machine sensor stream has 4 labelled failures total. At the 3-day window, only 4 of 30 days × 10 machines = ~40 (machine, day) pairs can possibly be positive — the rest are forced negatives. At the 14-day window the positive-label density is even higher per window but the absolute count is the same 4. A student picks the 3-day window for "fast recovery" (per the brief's "3-day = faster recovery, more false positives") and never sees that the family is in degenerate territory because the warning is buried in the JSON body and no test assertion fires on it.

**Caught by.** Phase 4 Candidates (PredMaint) — read the `degenerate` field on the leaderboard rows, not just `f1` — and Phase 7 Red-team (PredMaint) — at least one sweep MUST inject `/predict/maintenance/score` against a machine the chosen family classifies degenerate, and the journal must capture the disposition.

---

## Module 3 · Process-Optimization Controller + Reward Function (Sprint 3 · Reinforcement Learning · Optimize)

### F3.1 — Re-scoring under student-set weights uses CACHED transitions; new weights cannot un-make a reward-hacked policy

**Where it lives.** `routes/optimize_rl.py::leaderboard` calls `_re_score_under_weights(ctx.rl_episodes, rl.reward_function)` which iterates the cached episode transitions and re-computes returns under the current `RewardFunction(throughput, defect_cost, energy_cost, safety_penalty)`. The policies themselves (PPO / DQN / Random) are NOT re-trained — the scaffold ships 10,000 cached rollouts per policy and only the SCORING under new weights changes.

**What goes wrong.** A student sets `safety_penalty = RL_HARD_FLOOR_SAFETY_PENALTY` (the minimum) and watches PPO climb the leaderboard. They believe they are "training" a safer policy when in fact they are re-RANKING the same three cached rollouts under different reward weights. A policy that reward-hacked throughput in its CACHED rollouts continues to reward-hack — it just looks worse on the new weights. The Goodhart's Law trap (`PRODUCT_BRIEF.md §4.3`) is INVISIBLE in the cached scoring because the offending behaviour is already baked into the `safety_violation` count for each cached transition.

**Caught by.** Phase 5 Implications (RL) — the journal must explicitly state that the scaffold re-scores cached transitions, not re-trains the policy — and Phase 7 Red-team (RL) — the reward-function sweep must include a "set safety_penalty to floor and observe whether throughput jumps; if yes, the cached PPO rollouts already contained the violation, fix the weights upward".

### F3.2 — `simulate` looks up cached transitions by policy + seed; "rolling 500 episodes" can replay the same 500 every time

**Where it lives.** `routes/optimize_rl.py::simulate` accepts a `n_episodes` and `seed`; the implementation iterates `ctx.rl_episodes[req.policy]` in deterministic order and slices the first `n_episodes` (modulated by seed). The defensive promotion gate in `routes/optimize_rl.py::promote` calls `simulate(SimulateRequest(policy=req.policy, n_episodes=500, seed=42))` — every promotion check uses the same 500 cached transitions.

**What goes wrong.** A student tunes the reward weights so the FIRST 500 cached rollouts of PPO have zero `safety_violation` events, promotes, and ships. The remaining 9,500 rollouts (which the leaderboard re-score under the same weights) might have hundreds of violations — but the promotion-time gate never sees them because it is hardcoded to seed=42, n=500. The defensive WSH gate at promotion is real (`hard_floor_active` returns True when violations + line_speed_violations + temp_violations > 0) but only against the 500-episode slice.

**Caught by.** Phase 7 Red-team (RL) — the reward-function sweep MUST include a full 10,000-episode simulate at the promotion-time weights, not the 500 the gate uses — and Phase 8 Gate (RL) instructor cross-check.

### F3.3 — MOM mandate enforcement is at `POST /agent/policy`, not at `POST /optimize/rl/simulate`

**Where it lives.** `routes/agent.py::set_policy` checks `ctx.agent_policy.mom_mandate_active` and refuses any non-shadow autonomy mode for WSH-affecting task classes. `routes/optimize_rl.py::simulate` checks the simulated rollout's `line_speed_violations` and `temp_violations` against the post-MOM ceilings (60 boards/min, 250 °C) — but ONLY at the simulate boundary, not at the reward_function POST. A student can `POST /optimize/rl/reward_function` with `safety_penalty < RL_HARD_FLOOR_SAFETY_PENALTY` (refused — 422) but can also `POST` with weights that DO satisfy the floor yet produce a policy that, when simulated under the post-MOM envelope, exceeds the line-speed ceiling.

**What goes wrong.** A student reads "the WSH mandate is honoured by the agent autonomy gate" and assumes the RL surface is also locked down. They never re-run `POST /optimize/rl/simulate` after the MOM mandate fires, and the cached PPO rollouts that exceeded 60 boards/min before the mandate are still in the leaderboard, still chosen, still promoted. The `phase_12_postwsh.md` journal entry quantifies the AGENT compliance shadow price but the RL side of the mandate gets no entry — the rubric reads this as one decision moment half-shipped.

**Caught by.** Phase 11 Constraints (post-WSH) — must enumerate every endpoint the MOM mandate touches: agent policy, RL simulate envelope, RL reward function — and Phase 12 Acceptance (post-WSH) — must re-run simulate under the mandate AND re-run the agent autonomy ladder, both quantified separately.

---

## Module 4 · Coordination Agent + Drift Monitor × 3 (Sprint 4 · Agent + MLOps · Coordinate)

### F4.1 — `recent_30d` drift sample is a uniform sub-sample of the reference — PSI is near zero by construction

**Where it lives.** `routes/drift.py::check` for `req.window == "recent_30d"` calls `rng.choice(n, size=min(2000, n), replace=False)` and returns a slice of the reference embeddings. PSI is computed via `_compute_psi(ref_means, ref_stds, sample)` against the same reference distribution.

**What goes wrong.** The "30-day window" never exhibits drift. A student running `POST /drift/check` with `window=recent_30d` for any of the three model_ids will see PSI < 0.10 across every feature and conclude "no drift in production". The window is by construction a sub-sample of the reference; PSI cannot be high. The defensible interpretation is "the simulator is calm-state" — but the journal won't say that unless Phase 13 surfaces it. The signal lights up only on the synthetic `q4_demand_drift` window because that path adds elevated variance + mean shift.

**Caught by.** Phase 13 Drift signal-validity check (every drift signal must include a calm-state reference and an injected-state reference; otherwise the threshold is unfalsifiable) — the rule body must distinguish what `recent_30d` is FOR vs what `q4_demand_drift` is FOR per model.

### F4.2 — Calibration decay is anchored on baseline brier; multiplicative noise is window-dependent, not data-dependent

**Where it lives.** `routes/drift.py::check` builds `decay` from `cal["brier"]` plus a multiplicative bump that depends only on `req.window` (`+0.04` for `q4_demand_drift`, `+0.0` for everything else). `ref_calib` (`drift_baselines[model_id].per_class_calibration`) was computed at startup from the baseline `per_class.brier` for vision and predmaint; for RL, brier is N/A and the registered baseline brier is 0.0 (`startup.py` line 164).

**What goes wrong.** Reference and live brier are both anchored on the startup-time test-split — so `calibration_decay = sample_brier - ref_brier` is identically the multiplicative-noise bump on `recent_30d` and the same bump shifted on `q4_demand_drift`. A real production drift (degraded sensors, board-class distribution shift on incoming images, novel defect mode) would not be caught by this signal in tonight's scaffold. Worse: for RL, `ref_brier = 0.0` and `sample_brier = 0.0` means the calibration-decay number is identically zero on every window — the RL drift signal carries no information.

**Caught by.** Phase 13 Drift (RL) — the per-deployment cadence rule body MUST cite the brier=0 caveat as the reason the RL drift signal is structurally PSI-only, not calibration-decay — and `/redteam` cross-sprint (the test that swaps the predmaint rule onto RL and checks whether the system flags it).

### F4.3 — Universal "auto-retrain when X" is BLOCKED by route — but only via signal-set gate, not signal validity

**Where it lives.** `routes/drift.py::set_retrain_rule` accepts `signal in ("psi", "calibration_decay", "combined")` and any `threshold` / `duration` / `hitl` / `seasonal_exclusions`. The route's COMPLETE gate is "rule registered for all three model_ids"; it does not check whether the rule's signal makes sense per cadence (vision weekly, predmaint daily, RL per-deployment per `startup.py` lines 185–235).

**What goes wrong.** A student sets the same rule (signal=`psi`, threshold=`0.25`, duration=7d, hitl=true) for all three model IDs. The route happily accepts; `complete=true` flips green; viewer Sprint 4 lights up. The Phase 13 rubric demand — three cadences, three signals (calibration_decay invalid for RL per F4.2), three durations — is enforced by the rubric but not by the route. Universal `psi >= 0.25` triggers retraining of the RL policy 7 days after the seasonal Q4 ramp begins, when the brief's `Peak season` row says drift in that window is expected.

**Caught by.** Phase 13 Drift journal (the rule body must distinguish vision-weekly / predmaint-daily / rl-per-deployment with a SIGNAL choice that is valid for that cadence — not the same rule three times) and `/redteam` cross-sprint (the test that posts the same rule body to all three model_ids and checks whether any of them rejects).

---

## Cascade summary

The four-layer cascade — vision quality → predictive-maintenance precision → RL safety envelope → agent autonomy bound — propagates errors. F1.1 (vision picks wrong arch on macro-F1) feeds F2.2 (the predmaint baseline registers brier from a calibration that was already overstated) and F4.2 (the drift baseline anchors on the same brier). F3.1 (RL re-scoring uses cached transitions) corrupts every Phase 7 reward-function sweep that does not also call simulate at full-fleet scale. F3.3 (MOM mandate touches three independent endpoints) corrupts the Phase 12 compliance-cost number if any one is missed. The `/redteam` cross-sprint sweep is the only place every link is checked end-to-end.

## Five Trust-Plane decision moments — gap status

| #   | Decision moment                                                                                      | Owning phase             | Status as of pre-run                                                                                                                                                                                            |
| --- | ---------------------------------------------------------------------------------------------------- | ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Choose the vision QC base architecture (ResNet-50 / EfficientNet-B0 / ViT-Small)                     | Phase 5 (Vision)         | Open. Three architectures pre-fit at startup; `chosen_arch` defaulted to macro-F1 winner (F1.1 trap). Student picks final on Phase 5 against per-class evidence + 80 ms/board edge latency budget.              |
| 2   | Set the auto-pass confidence threshold per class × 4 (good / minor / major / safety_critical_defect) | Phase 6 (Vision)         | Open for 3 of 4 classes. `safety_critical_defect` has a structural hard floor at 0.40 already in place (`ml_context.py::SAFETY_CRITICAL_HARD_FLOOR`); the 49:1 asymmetry math owns the other three.             |
| 3   | Choose the predictive-maintenance prediction window (3 / 7 / 14 days)                                | Phase 5 (PredMaint)      | Open. Three windows pre-fit per family at startup. F2.1 is the trap (window and family chosen independently). $12,000 vs $1,800 unplanned-vs-planned math owns the decision.                                    |
| 4   | Design the RL reward function weights (throughput / defect_cost / energy_cost / safety_penalty)      | Phase 7 (RL)             | Open. `safety_penalty` has a hard floor at `RL_HARD_FLOOR_SAFETY_PENALTY` (route refuses below); the other three are student-set. Goodhart's Law check (F3.1) is the rubric's pressure point.                   |
| 5   | Set the agent autonomy ladder + MOM/WSH shadow-mode override                                         | Phase 11 + 12 (post-WSH) | Open. Default autonomy `{vision_triage: shadow, maintenance_scheduling: shadow, setpoint_adjustment: shadow, safety_alert: shadow}`. `mom_mandate_active=False` until injection script fires; F3.3 is the trap. |

Stopping for `/todos`.
