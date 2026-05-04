<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Inherited Assumptions — LumenCircuit Industrial AI Suite

**Phase:** `/analyze` · **Author:** agent · **Date:** 2026-05-04
**Source:** read of `src/manufacturing/backend/{ml_context,startup,config,routes/*}.py` and `PRODUCT_BRIEF.md` §2.

Twelve assumptions the scaffold has already baked in. Each is cited to a source file. Every dollar figure is quoted verbatim from `PRODUCT_BRIEF.md §2` (the cost table) and re-affirmed by `specs/business-costs.md`. Every assumption you accept tonight is a decision by omission — the rubric will treat it as a decision you made unless you contest it in a journal.

---

## A1. Vision class taxonomy is frozen at four classes

**Cited to.** `src/manufacturing/backend/ml_context.py::VISION_CLASSES`.

```python
VISION_CLASSES: tuple[str, ...] = (
    "good",
    "minor_defect",
    "major_defect",
    "safety_critical_defect",
)
```

The 4-class structure is invariant — `startup.py` asserts the vision baseline ships fits across exactly these 4 classes; `routes/inspect_vision.py::set_threshold` refuses unknown class names with 422. Adding a fifth class (e.g. `cosmetic_only` separate from `minor_defect`, or splitting `major_defect` by defect-mode) is out of scope tonight. The defect-mode field on `boards_labelled.csv` (`solder-bridge / missing-component / tombstone / cold-joint / scratch / contamination / none`) is independent and not enforced by the route surface.

## A2. Safety-critical-defect is structurally HARD; floor is 0.40

**Cited to.** `ml_context.py::SAFETY_CRITICAL_HARD_FLOOR = 0.40` and the dual-gate enforcement at `routes/inspect_vision.py::set_threshold` (422 if `class_name == "safety_critical_defect" and threshold < 0.40`) and `::promote` (422 if persisted safety-critical threshold below floor at promote time).

The reason is regulatory, not statistical: `PRODUCT_BRIEF.md §2` lists "**WSH-notifiable incident (worker injury or fatality)** — **$1,000,000+** per incident — MOM fine + criminal liability + reputation" — quoted verbatim. The cost is high enough that no cost-balanced threshold can compete with the regulatory floor. IPC-A-610 Class 3 contractual flow-through (per `specs/compliance-floors.md`) is the second leg — recall liability is the manufacturer's. You inherit the value 0.40 — challenge it only if you have a defensible regulatory reading otherwise.

## A3. Vision embedding dimensionality is 32; embeddings are deterministic per `image_id`

**Cited to.** `ml_context.py::synthesise_image_embeddings` derives a per-(`image_id`, `arch`) seed and re-uses it on every call. The PNG dataset at `src/manufacturing/data/images_pcb/` ships 800 32×32 RGB procedural images (per `SCAFFOLD_MANIFEST.md §"Implementation deviations"` row 2) but the backend does NOT read pixel content at inference — it uses the synthesised per-class Gaussian-centroid embeddings.

The framing in `PRODUCT_BRIEF.md` says "frozen ResNet/EfficientNet/ViT backbones with fine-tuned classification heads". The scaffold's actual implementation (per `SCAFFOLD_MANIFEST.md §"Implementation deviations"` row 1) uses sklearn classifiers (LogisticRegression, RandomForestClassifier, HistGradientBoostingClassifier) on per-architecture embedding dimensionalities — real fits, real per-class metrics, but not real ResNet activations. The pedagogical contract is intact (3-arch leaderboard, per-class P/R/F1, $4,200/$85 cost-balanced threshold, 49:1 asymmetry). Asking Claude Code to "use real ResNet weights" raises a non-trivial change to startup time and is out of budget tonight.

## A4. Vision baseline is a 3-architecture head sweep across distinct embedding dimensionalities

**Cited to.** `ml_context.py::build_vision_baseline` constructs three architectures:

- `resnet50_lr_head` — `LogisticRegression` on a ResNet-50-shaped embedding
- `efficientnet_b0_rf_head` — `RandomForestClassifier` on an EfficientNet-B0-shaped embedding
- `vit_small_gbm_head` — `HistGradientBoostingClassifier` on a ViT-Small-shaped embedding

Per `SCAFFOLD_MANIFEST.md §"Family / architecture names diverge"` — the architecture **labels** preserve the brief's "ResNet-50 / EfficientNet-B0 / ViT-Small" leaderboard pattern even though the underlying classifiers are sklearn surrogates AND the embedding dimensionalities mimic the real-architecture differences. The chosen-by-macro-F1 default at startup is the F1.1 trap; `routes/inspect_vision.py::leaderboard` exposes the comparison. From-scratch CNN training is BLOCKED by the time budget; the brief's "transfer-learning is the practical default" framing owns the architecture choice.

## A5. Predictive-maintenance baseline is LightGBM + LSTM + Survival-Forest 3-family × 3-window leaderboard

**Cited to.** `ml_context.py::PREDMAINT_FAMILIES` and `::PREDMAINT_WINDOWS`:

```python
PREDMAINT_WINDOWS: tuple[int, ...] = (3, 7, 14)
PREDMAINT_FAMILIES: tuple[str, ...] = ("lightgbm_features", "lstm_sequence", "survival_forest_tte")
```

`build_predmaint_baseline` fits each (family, window) pair against per-machine sliding-window features synthesised from the 432,000-row sensor stream. 4 of 10 machines have a labelled failure event in the 30-day window per `PRODUCT_BRIEF.md §2` and `specs/business-costs.md`. Per `SCAFFOLD_MANIFEST.md §"Implementation deviations"`, the underlying classifiers are sklearn / scipy surrogates (LightGBM is real; LSTM is a numpy approximation; Survival Forest is a scipy-based time-to-event approximation). The 3-family pattern matches the brief's "LightGBM + LSTM + Survival Forest" leaderboard.

## A6. RL ships three policies as cached transition tables; "training" is re-scoring, not re-training

**Cited to.** `ml_context.py::RL_POLICIES = ("ppo_continuous", "dqn_discrete", "random_baseline")`. `build_rl_baseline` reads `src/manufacturing/data/rl_episodes.json` (10,000 cached transitions per policy per `SCAFFOLD_MANIFEST.md`) and computes per-policy throughput / defect_rate / energy / safety_violation summaries. `routes/optimize_rl.py::leaderboard` calls `_re_score_under_weights` which iterates the cached transitions under the current `RewardFunction` to produce the leaderboard ranking.

Per `SCAFFOLD_MANIFEST.md §"Implementation deviations"` row 3: "The RL 'environment' is a cached transition table, not a live simulator." This is the F3.1 trap — students who say "I trained PPO with my new reward weights" are wrong; they re-RANKED cached rollouts under the new weights. The pedagogical contract (defending reward weights against a leaderboard, hitting the hard-floor table on the simulate bench) is intact. The dollar framing — 2-3% throughput recovery × 40,000 boards/day × ~$60 contribution margin = $48,000-$72,000/day per `business-costs.md` — owns the Phase 10 deliverable.

## A7. RL safety_penalty has a HARD floor; equipment-damage + WSH ceilings are reward-side hard constraints

**Cited to.** `ml_context.py::RL_HARD_FLOOR_SAFETY_PENALTY = 0.50`. `routes/optimize_rl.py::set_reward_function` refuses (422) any `safety_penalty < RL_HARD_FLOOR_SAFETY_PENALTY`. `RewardFunction.hard_floors` carries the `equipment_damage_dollar_per_incident: $50,000` and `wsh_dollar_per_incident: $1,000,000` constants. `routes/optimize_rl.py::promote` calls `simulate(SimulateRequest(policy=req.policy, n_episodes=500, seed=42))` and refuses promotion if `hard_floor_active` (any safety_violation, line_speed_violation, or temp_violation in the 500-episode bench).

The values come from `PRODUCT_BRIEF.md §2`: "Equipment damage from RL action outside safe envelope — $50,000 per incident" and the WSH ceiling above. The route's hard-floor refusal at the reward_function POST is a structural defense; the simulate-bench refusal at promote time is belt-and-suspenders (F3.2 is the trap on the bench-size limit).

## A8. Agent task-class taxonomy is fixed at four; autonomy modes are fixed at three; default is shadow across the board

**Cited to.** `ml_context.py::AGENT_TASK_CLASSES` and `::AGENT_AUTONOMY_MODES`:

```python
AGENT_TASK_CLASSES: tuple[str, ...] = (
    "vision_triage",
    "maintenance_scheduling",
    "setpoint_adjustment",
    "safety_alert",
)
AGENT_AUTONOMY_MODES: tuple[str, ...] = ("shadow", "recommend", "act")
```

`AgentPolicy.autonomy` defaults to `{vision_triage: shadow, maintenance_scheduling: shadow, setpoint_adjustment: shadow, safety_alert: shadow}`. `WSH_AFFECTING_TASK_CLASSES` is a subset (`setpoint_adjustment`, `safety_alert`); during the MOM mandate window, `routes/agent.py::set_policy` refuses (422) any non-shadow autonomy for these classes. The agent harness is deterministic (no real LLM) per `routes/agent.py::_decide_task_class`; the pedagogical contract is "defend the autonomy ladder, not the LLM prompt".

## A9. Drift baselines are registered for exactly three model IDs; cadence is hardcoded per modality

**Cited to.** `startup.py` builds `drift_baselines = {"vision": ..., "predmaint": ..., "rl": ...}` with `cadence="weekly"` for vision, `cadence="daily"` for predmaint, `cadence="per_deployment"` for rl. The hard invariant at the bottom of `startup.py` raises `RuntimeError` if `ctx.drift_baselines_registered != 3`.

The cadence labels are metadata only — they live on the `DriftReference` dataclass. The scaffold does not enforce that the student's Phase 13 `retrain_rule` matches the registered cadence; that match is a rubric concern. Per F4.2, the RL drift baseline ships with `brier=0.0` because "RL reward is not a probability; brier is N/A" (`startup.py` line 164) — the calibration_decay signal is structurally PSI-only for RL.

## A10. Inspector queue allocator is a 3-tier LP; capacity = 6 inspectors × 8-hour shift

**Cited to.** `routes/queue.py::TIER_CONFIG` (3 tiers — `critical` / `major` / `minor` with per-board mean review minutes 6.0 / 3.0 / 1.5 and SLA bounds 30 / 60 / 120 minutes), `::QueueState` (default queue depth `{critical: 120, major: 480, minor: 800}`), and `::INSPECTOR_HOURLY_DOLLAR = 35.0 * 60.0` ($35/min × 60 = $2,100/hr).

Total inspector-minutes/shift = 6 × 8 × 60 = 2,880 minutes. The `critical` tier carries `fn_dollar_per_board: 4200.0` (the major-defect-shipped cost from `business-costs.md`); the `major` tier carries `fn_dollar_per_board: 1800.0` (the planned-stop scaffold-default proxy); the `minor` tier carries `fn_dollar_per_board: 180.0` (the minor-defect-shipped cost). The $35/min inspector-time cost is verbatim from `PRODUCT_BRIEF.md §2` ("Qualified inspector time (IPC-A-610 Class 3 certified) — $35 per minute on the manual-review queue").

## A11. Cost asymmetry $4,200 FN / $85 FP / $1M WSH / $50K equipment / $35 inspector min — verbatim from brief

**Cited to.** `PRODUCT_BRIEF.md §2`. Quoted verbatim:

- "Major defect shipped (recall / field return) — $4,200 per board (warranty + replacement + customer-confidence)"
- "Minor defect shipped (rework downstream) — $180 per board (in-line rework + repackage)"
- "Good board scrapped (false-positive auto-fail) — $85 per board (component + labour cost of a scrapped BOM)"
- "Unplanned line-stop from missed maintenance signal — $12,000 per stop"
- "Equipment damage from RL action outside safe envelope — $50,000 per incident"
- "**WSH-notifiable incident (worker injury or fatality)** — **$1,000,000+** per incident — MOM fine + criminal liability + reputation"
- "Qualified inspector time (IPC-A-610 Class 3 certified) — $35 per minute on the manual-review queue"
- "Cold-start cost (novel defect type, zero-shot misclass) — $620 per misclassified novel defect mode"
- "Edge inference (on-line camera, Jetson-class) — $0.001 per board classification served at the edge"
- "Cloud RL training (A10G class) — $0.40 per training hour"
- Planned-maintenance window — $1,800 per stop (off-shift; component + labour only) — re-affirmed in `specs/business-costs.md` row 5.

The 49:1 ratio ($4,200 / $85) is stated in the brief and re-affirmed in `business-costs.md §"Decision anchors"`. The 6.7:1 ratio ($12,000 / $1,800) on the predmaint side is the second-order asymmetry. These are the only numbers tonight's journal entries may cite without separate justification.

## A12. CORS is permissive; backend binds 127.0.0.1; workspace JSON files are the persistence layer

**Cited to.** `src/manufacturing/backend/app.py` registers `CORSMiddleware(allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])`. `src/manufacturing/backend/config.py::load_settings` defaults `api_host` to `"127.0.0.1"`. `routes/state.py::_PHASE_FILE_RE` and `_SKELETON_BYTES_THRESHOLD = 500` (mirrored from the Week 6 scaffold) — state auto-detection scans `workspace_root/journal/phase_*.md`; any file matching `phase_(\d+)_<slug>.md` larger than 500 bytes is treated as an authored phase entry.

`routes/inspect_vision.py`, `routes/predict_maintenance.py`, `routes/optimize_rl.py`, `routes/agent.py`, and `routes/drift.py` persist state via JSON files in `workspace_root` (`vision_thresholds.json`, `predmaint_state.json`, `rl_reward_function.json`, `agent_policy.json`, `retrain_rules.json`). The state survives backend restart. Files written via the MOM injection script (`scripts/scenario_inject.py mom_wsh_shadow_mandate`) flip `ctx.agent_policy.mom_mandate_active` to True — that's the mechanism behind the ~4:30 pm Sprint 3 trigger.

The CORS wildcard is acceptable HERE because the backend binds to 127.0.0.1 by default and the dataset contains no real PII — explicit teaching-scaffold concession. Do not copy this CORS configuration into a production journal entry. Flagging this in `phase_7_red_team` is the rubric-recognised disposition.

---

## Closing note

The dollar table (A11), the 4-class vision taxonomy (A1), the WSH hard floor (A2), the RL safety_penalty floor (A7), and the three drift cadences (A9) are the load-bearing assumptions tonight. Everything else is a scaffold-set default that you can override or contest in a journal — and if you don't contest it, the rubric scores you as having accepted it.

Stopping for `/todos`.
