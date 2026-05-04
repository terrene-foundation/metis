<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Decisions Still Open — LumenCircuit Industrial AI Suite

**Phase:** `/analyze` · **Author:** agent · **Date:** 2026-05-04
**Source:** intersection of `failure-points.md`, `assumptions.md`, the 14-phase Playbook, and the 5 ★ Trust-Plane decision moments named in `PRODUCT_BRIEF.md §5`.

What remains yours to decide tonight, organised by sprint and tagged to the Playbook phase that owns each decision. **No proposed values appear here** — the rubric demands you pre-register thresholds, weights, windows, and architectures in their owning phase journals BEFORE seeing the leaderboard or the simulate output. A value proposed here would corrupt the pre-registration.

The five Trust-Plane decision moments (`PRODUCT_BRIEF.md §5`) are flagged ★. They are non-negotiable.

---

## Cross-sprint (shared framing)

### D-01: Define what counts as "shippable" per defect class (Phase 1 · shared)

What's at stake: the auto-pass / human-review / hard-block mapping per of the 4 vision classes, plus the parallel mapping for the predmaint window, plus the same for RL setpoint adjustment, plus the same for safety-monitor alerts. Policy decision, not technical — but downstream Phase 6 (vision threshold), Phase 11 (RL constraints), and Phase 12 (agent autonomy ladder) all consume it. Endpoints committed: `POST /inspect/vision/threshold`, `POST /agent/policy`, `POST /optimize/rl/reward_function`.

### D-02: Population scope and exclusions (Phase 1 · shared)

What's at stake: which boards, machines, and reflow runs are in scope. Inclusions and explicit exclusions (BizSAFE re-certification cycles, Q4 ramp, scheduled re-calibrations, customer-specific lots that override the default per-class threshold). Frame writes this in plain language. Phase 13 seasonal-exclusion language draws from this. Endpoints committed: none — Phase 1 is journal-only.

### D-03: Horizon — auto-decision latency target stated in milliseconds (Phase 1 · shared)

What's at stake: the 80 ms/board edge-latency budget owned by the inspection cameras (Jetson-class hardware). Architecture choice (D-04) is partly an edge-deployment trade-off; ViT-Small is data-hungry AND compute-hungry. The throughput-recovery target on the RL side has a corresponding latency budget (action-selection at 1 board/sec ≈ 60 boards/min ceiling). Endpoints committed: none — Phase 1 framing.

### D-04: Cost-asymmetry framing — primary FN vs FP terms, plus WSH ceiling acknowledged separately (Phase 1 · shared)

What's at stake: cite `$4,200` major-defect-shipped, `$85` good-board-scrapped, `$1,000,000+` WSH ceiling, `$12,000` unplanned-stop, `$1,800` planned-stop, `$50,000` equipment damage, `$35/min` inspector verbatim from `PRODUCT_BRIEF.md §2`. The 49:1 vision asymmetry and the 6.7:1 predmaint asymmetry are the two anchors every later threshold cites. Endpoints committed: none — Phase 1 framing.

### D-05: Six-category data audit — label noise, leakage, class imbalance, OOD coverage, demographic skew, scaffold-coverage gaps (Phase 2 · shared)

What's at stake: a single audit covers the 800 vision images, the 432,000 sensor rows, the 10,000 RL episodes per policy, and the 200 safety images. Class imbalance on the safety_critical_defect class is the first finding (49:1 cost asymmetry × naturally low base-rate); the predmaint label imbalance (4 of 10 machines fail in 30 days = ~13% base rate) is the second. Endpoints committed: read-only — `GET /inspect/vision/leaderboard`, `GET /predict/maintenance/leaderboard`, `GET /optimize/rl/leaderboard`.

### D-06: Feature framing — declared vision features + augmentations, declared sensor features (sliding window stats), declared RL state features (zone temps + line speed + board class) (Phase 3 · shared)

What's at stake: declare the feature surface for each modality so Phase 4's candidate sweep is fitting on a known surface, not a black box. The PSI signal in Phase 13 is computed on these features — incoherent feature framing breaks the drift signal. Cite `ml_context.py::synthesise_image_embeddings` (32-dim per-architecture surrogates) and `::synthesise_sensor_window_features` (per-machine sliding window stats). Endpoints committed: none — declarative phase.

---

## Sprint 1 — Vision QC · Transfer Learning · See

### D-07: Vision architecture pick — ResNet-50 / EfficientNet-B0 / ViT-Small ★ (Phase 5 · Sprint 1)

What's at stake: ★ Decision moment 1 of 5. Three architectures pre-fit on the leaderboard at startup; chosen-by-macro-F1 default is the F1.1 trap. Tied to the 80 ms/board edge-deployment latency budget AND the per-class P/R/F1 leaderboard AND the 49:1 cost asymmetry. ResNet-50 is robust, well-understood, fast inference; EfficientNet-B0 is best accuracy/efficiency on Jetson; ViT-Small is highest accuracy on subtle defects but data-hungry at 800 images. Endpoints committed: `POST /inspect/vision/promote` (Phase 8, post-defense).

### D-08: Vision per-class evidence — Brier per class, per-class WSH-mandated recall on safety_critical_defect (Phase 5 · Sprint 1)

What's at stake: NOT macro-F1. The journal must name Brier per class for the chosen architecture, flag any class above a pre-registered Brier floor as a finding, and explicitly cite the safety-critical recall number. F1.1 is the trap. Endpoints committed: read-only — `GET /inspect/vision/leaderboard`.

### D-09: Vision auto-pass threshold per class × 4 ★ (Phase 6 · Sprint 1)

What's at stake: ★ Decision moment 2 of 5. Set the threshold for each of `good`, `minor_defect`, `major_defect`, `safety_critical_defect`. Three are cost-balanced under $4,200 FN / $85 FP (49:1 asymmetry); `safety_critical_defect` is structurally HARD at the WSH-mandated 0.40 floor (`SAFETY_CRITICAL_HARD_FLOOR`). The threshold POST refuses below floor; promote refuses below floor at promote time. Endpoints committed: `POST /inspect/vision/threshold` × 4.

### D-10: Vision per-class action declaration — auto_pass / human_review / hard_block per class (Phase 6 · Sprint 1)

What's at stake: don't conflate threshold with action — the route accepts any [0,1] for the threshold; action is encoded by which class+threshold combination triggers what dispatch. `safety_critical_defect` above 0.40 is a hard-block (no auto-pass at all is the WSH-defensible reading); `major_defect` above its threshold goes to human_review; `minor_defect` above its threshold goes to in-line rework dispatch. The mapping is the journal's deliverable. Endpoints committed: implicit via threshold + scoring path.

### D-11: Vision Phase 7 sweeps × 3 — adversarial pixel perturbation / OOD novel defect mode / IPC-A-610 Class-3-vs-Class-2 skew (Phase 7 · Sprint 1)

What's at stake: pre-registered acceptance criteria, executed via `POST /inspect/vision/score` against curated holdouts (image_ids from the 800 labelled). Severity (block / monitor / accept) per finding. Cold-start novel-defect-mode case ($620/misclass per `business-costs.md`) is one of the sweeps. Endpoints committed: `POST /inspect/vision/score` against curated holdouts.

### D-12: Sprint 1 deployment gate — PASS / FAIL on per-class evidence + threshold defense + WSH-floor compliance (Phase 8 · Sprint 1)

What's at stake: promote chosen architecture to `shadow` stage with rationale; both WSH-floor gates apply (threshold POST AND promote POST). On FAIL, name the specific deficit and the next action. Endpoints committed: `POST /inspect/vision/promote`, `GET /inspect/vision/registry`.

---

## Sprint 2 — Predictive Maintenance · Time-Series ML · Predict

Phases 1–3 are NOT re-run. Phase 4–8 are replayed against the predmaint module with `_predmaint` suffix on the journal files.

### D-13: Predmaint family pick — LightGBM / LSTM / Survival-Forest, defended on per-window F1 + Brier + degenerate-flag check (Phase 5 · Sprint 2)

What's at stake: F2.3 is the trap (`degenerate` field on the leaderboard rows when there are too few positive labels in a window). F2.1 is the second trap (family and window must be coherent). The 3-family leaderboard is at `/predict/maintenance/leaderboard` nested by window. Endpoints committed: `POST /predict/maintenance/family`.

### D-14: Predmaint prediction window pick — 3 / 7 / 14 days ★ (Phase 5 · Sprint 2)

What's at stake: ★ Decision moment 3 of 5. 3-day = faster recovery, more false positives; 7-day = ops sweet spot (gives ops time to schedule downtime); 14-day = lower FP rate but throughput already lost by the time you act. Defended in $ of unplanned-stop ($12,000) avoidance vs planned-maintenance ($1,800) overhead — 6.7:1 ratio. The pair (family, window) must be coherent (F2.1). Endpoints committed: `POST /predict/maintenance/window`.

### D-15: Predmaint cost-balanced threshold + held-out calibration check (Phase 6 · Sprint 2)

What's at stake: cost-balanced minimum threshold against the 6.7:1 unplanned-vs-planned asymmetry; held-out calibration check on the chosen (family, window) pair, NOT in-sample (F2.2 is the trap). The Brier registered at startup as the drift baseline is in-sample — call this out and request held-out evidence as a Phase 7 sweep input. Endpoints committed: `POST /predict/maintenance/threshold`.

### D-16: Predmaint Phase 7 sweeps × 3 — sensor-noise robustness / novel failure mode (cold-start) / cross-machine generalisation (Phase 7 · Sprint 2)

What's at stake: pre-registered acceptance criteria; cross-machine generalisation is the key one because 4 of 10 machines have failure events — leakage between train/test machine splits is a real risk. Cold-start ($620/misclass per `business-costs.md`) is one of the sweeps. Endpoints committed: `POST /predict/maintenance/score` against held-out machine-windows.

### D-17: Sprint 2 deployment gate — PASS / FAIL + promotion (Phase 8 · Sprint 2)

What's at stake: no WSH-floor gate on this endpoint; calibration confirmation + degenerate-flag check are the substitutes. Endpoints committed: `POST /predict/maintenance/promote`.

---

## Sprint 3 — Process Optimization (RL) + Inspector Queue · Reinforcement Learning + LP · Optimize

### D-18: RL policy pick — PPO / DQN / Random baseline (Phase 5 · Sprint 3)

What's at stake: re-scoring under student-set weights uses cached transitions (F3.1 is the trap — students who say "I trained PPO" are wrong; they re-RANKED). Defended on per-policy throughput / defect_rate / energy / safety_violation under the chosen reward weights. The 2-3% throughput-recovery target ($48,000-$72,000/day per `business-costs.md`) is the dollar framing. Endpoints committed: `POST /optimize/rl/promote` (Phase 8).

### D-19: RL reward function weights × 4 — throughput / defect_cost / energy_cost / safety_penalty ★ (Phase 7 · Sprint 3)

What's at stake: ★ Decision moment 4 of 5. Set the four reward weights; `safety_penalty` MUST be ≥ `RL_HARD_FLOOR_SAFETY_PENALTY` (route refuses below). Goodhart's Law check: "Maximize throughput" with safety_penalty=floor → agent runs line at >60 boards/min, defect rate triples, equipment crashes within 48 hours of cached rollouts. The leaderboard MUST show your chosen weights produce defect rate below ceiling AND throughput at least 5% above the random baseline AND zero hard-floor violations across the 10,000-episode bench (NOT the 500-episode promote bench — F3.2 is the trap). Endpoints committed: `POST /optimize/rl/reward_function`, `POST /optimize/rl/simulate`.

### D-20: Inspector queue allocator LP objective — minimise expected catch-value loss vs minimise inspector cost (Phase 10 · Sprint 3)

What's at stake: the objective is fixed in `routes/queue.py::solve` (maximise catch-value subject to inspector-minute budget); the student's decision is the queue depth and inspector-minutes-available inputs. Defended in $ of FN cost ($4,200 critical / $1,800 major / $180 minor) vs inspector cost ($35/min × 2,880 minutes/shift = $100,800/shift maximum). Endpoints committed: `POST /queue/solve` with a chosen `queue_depth` and `inspector_minutes_available`.

### D-21: Inspector queue first-pass constraints — hard set (inspector-minute budget) and soft set (per-tier SLA penalties) (Phase 11 · Sprint 3, first pass)

What's at stake: classify constraints as hard vs soft. Inspector-minute budget is HARD (physics — 6 inspectors × 8-hour shift). Per-tier SLA bounds (30 / 60 / 120 minutes for critical / major / minor) are SOFT. The post-WSH re-run flips part of this. Endpoints committed: `POST /queue/solve` (writes `queue_last_plan.json`).

### D-22: Inspector queue first-pass acceptance — feasibility + pathology check + disposition (Phase 12 · Sprint 3, first pass)

What's at stake: verify `feasibility: true` on the response body directly — don't trust the viewer card alone. Disposition: ACCEPT / RE-TUNE / FALL BACK / REDESIGN. Endpoints committed: `POST /queue/solve`, `GET /queue/last_plan`.

### D-23: Agent autonomy ladder + WSH shadow-mode override ★ (Phase 11 + 12 · Sprint 3, post-WSH)

What's at stake: ★ Decision moment 5 of 5. Three autonomy modes (shadow / recommend / act) per task class (vision_triage / maintenance_scheduling / setpoint_adjustment / safety_alert). The WSH-affecting categories (`setpoint_adjustment`, `safety_alert`) are STRUCTURALLY hard-shadowed when the MOM mandate fires (mid-Sprint-3 injection at ~4:30 pm via `scripts/scenario_inject.py mom_wsh_shadow_mandate`). Re-solve the agent autonomy table under the post-WSH envelope AND quantify the optimization shadow price (compliance cost in $/day of lost RL throughput gains). Re-run RL simulate under the post-MOM line-speed (≤60 boards/min) and zone-temp (≤250 °C) ceilings — F3.3 is the trap (the MOM mandate touches three endpoints, not one). Endpoints committed: `POST /agent/policy` (refused 422 if WSH-affecting class is non-shadow during mandate), `POST /optimize/rl/simulate` re-run, `POST /queue/solve` re-run if backlog shifts.

---

## Sprint 4 — Coordination Agent + Drift × 3 · Agent + MLOps · Coordinate

One phase, three rules; nothing else.

### D-24: Vision retrain rule — signal, threshold, duration window, HITL disposition, seasonal exclusions (Phase 13 · Sprint 4)

What's at stake: cadence is **weekly** (A9). Signal choice: PSI on the chosen-arch embedding distribution OR per-class calibration_decay against the registered baseline. The variance-grounded threshold cites the calm-state `recent_30d` PSI (F4.1 is the trap — `recent_30d` is a uniform sub-sample by construction). HITL=true on first trigger. Seasonal exclusions cite Q4 ramp + medical certification cycles per `business-costs.md §"Seasonality"`. Endpoints committed: `POST /drift/retrain_rule` for `model_id=vision`.

### D-25: Predmaint retrain rule — signal, threshold, duration window, HITL disposition, seasonal exclusions (Phase 13 · Sprint 4)

What's at stake: cadence is **daily** (A9) — sensor stream drifts on temperature, calibration, supplier lots. Signal choice: PSI OR calibration_decay; the brier-baseline-anchoring trap (F4.2) means calibration_decay is muted on `recent_30d` and shifted on `q4_demand_drift`. The duration window must be longer than a single shift to avoid alarm-fatigue (~3-7 days is the rubric-defensible band, but pre-register your exact value). Endpoints committed: `POST /drift/retrain_rule` for `model_id=predmaint`.

### D-26: RL retrain rule — signal, threshold, duration window, HITL disposition, seasonal exclusions (Phase 13 · Sprint 4)

What's at stake: cadence is **per-deployment** (A9). The brier-N/A caveat (F4.2) means the RL drift signal is structurally PSI-only; the rule body MUST cite this. Per-deployment cadence means the rule fires on every `POST /optimize/rl/promote` — the seasonal exclusion is "do not auto-retrain during the MOM mandate window". HITL=true on first trigger. Endpoints committed: `POST /drift/retrain_rule` for `model_id=rl`.

### D-27: Calibration-decay validity disposition (Phase 13 · Sprint 4)

What's at stake: when the calibration_decay signal is muted on `recent_30d` (F4.1 + F4.2) and noise-shifted on `q4_demand_drift`, which window is the canonical retrain trigger per cadence? The drift-route does not enforce this; rule body must. Endpoints committed: implicit via `POST /drift/retrain_rule` rule bodies.

---

## Close

### D-28: Cross-sprint red-team findings — severity-ranked, blast-radius in $, detection cadence, mitigation (`/redteam`)

What's at stake: ≥ 8 findings minimum (rubric floor). Output: `04-validate/redteam.md`. Cross-sprint cascade (vision → predmaint → RL → agent) is the rubric's pressure point — F1.1 + F2.2 + F3.1 + F4.2 chain together silently if the journal entries don't catch them.

### D-29: Phase 9 codify lessons — 3 transferable + 2 domain-specific (`/codify`)

What's at stake: anti-platitude check; each lesson must name a Week 7 scenario. Transferable: macro-F1 trap, in-sample calibration trap, Goodhart's Law on RL reward. Domain-specific: WSH hard floor as structural override of cost-balanced threshold, MOM mandate as multi-endpoint hard-shadow.

---

## Summary

- **23+ open decisions** organized as 6 cross-sprint framing decisions (D-01 through D-06), 6 Sprint-1 decisions (D-07 through D-12), 5 Sprint-2 decisions (D-13 through D-17), 6 Sprint-3 decisions (D-18 through D-23), 4 Sprint-4 decisions (D-24 through D-27), and 2 close decisions (D-28 + D-29). Of these, ~15 require values you pre-register in a journal; 6 are framing decisions (Phases 1–3); 4 are gate decisions (Phase 8 × 3, Phase 12 × 1 first-pass).
- **5 ★ decision moments**: D-07 (vision architecture), D-09 (vision per-class thresholds), D-14 (predmaint window), D-19 (RL reward weights), D-23 (agent autonomy + MOM hard-shadow). All non-negotiable; rubric scores zero on D3 (trade-off honesty) if any are skipped.
- **Replay phases.** Phase 4–8 run THREE times (Vision then PredMaint then RL); Phase 11–12 run twice (first-pass then post-WSH). Total 14 + 5×2 + 2 = ~26 phase passes excluding `/redteam` + `/codify` + `/wrapup`.

Stopping for `/todos`.
