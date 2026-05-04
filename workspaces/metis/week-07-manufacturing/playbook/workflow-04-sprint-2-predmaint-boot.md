<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 4 — Sprint 2 Predictive Maintenance Boot (Time-series classifier)

> **What this step does:** Boot Sprint 2 by copying the predmaint skeletons, confirming the time-series endpoints are live, and getting a written orientation — before any Phase 4 SML prompt fires.
> **Why it exists:** Sprint 2 replays Phases 4–8 for the predictive-maintenance classifier. Booting cleanly means the SML phase pattern fires fast — without re-discovering scaffold details Sprint 1 already established.
> **You're here because:** Sprint 1 Vision wrapped (Phase 8 gate signed) and Sprint 2 is the time-series replay.
> **Key concepts you'll see:** SML replay, time-series families, calibration, prediction window, three-family leaderboard

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering Sprint 2 — the SML replay for the predictive-maintenance
classifier. Same five-phase pattern as Sprint 1 (Phase 4 candidates →
Phase 5 implications → Phase 6 metric+threshold → Phase 7 red-team →
Phase 8 deployment gate), but applied to a different model class
(time-series).

Before I start the phase walk, I need you to:

1. Copy the SML replay skeletons from journal/skeletons/ into journal/.
   These have the _predmaint suffix to distinguish them from the _vision pass.

2. Confirm the predmaint endpoints are live by making GET requests.
   If any is not live, STOP and raise a hand.

3. Re-state — for THIS sprint's model class — the dollar asymmetry that
   drives Phase 6 thresholds. Quote the exact lines from the cost source.

4. Name the three-family leaderboard the scaffold ships. For each family,
   cite the file and function. Do NOT invent families that aren't in the
   scaffold.

5. Do NOT propose the prediction window or the threshold. Those are my
   pre-registration in phase_5_predmaint.md and phase_6_predmaint.md
   before I see the leaderboard.

6. Do NOT use the word "blocker" without naming a specific action.

Once skeletons are copied and endpoints confirmed live, summarise: the five
SML phases for this sprint, the prediction-window decision shape (3 / 7 /
14 days), the calibration check (Brier + reliability diagram) that Phase 6
adds on top of the threshold decision, and the Phase 7 sweeps specific to
this sprint's model class.

Then stop and wait for my Phase 4 prompt.
```

**Tonight-specific additions** (Week 7 LumenCircuit Sprint 2):

```
Sprint: Sprint 2 Predictive Maintenance — time-series classifier scoring
each of 10 SMT machines per day for failure within the next N days
(N ∈ {3, 7, 14}, your Phase 5 call).

Phases covered: Playbook phases 4, 5, 6, 7, 8 (replay). Phases 1, 2, 3
were framed in Sprint 1 — do NOT re-run them.

Skeleton copy: copy phase_{4..8}_predmaint.md skeletons from
journal/skeletons/ into workspaces/metis/week-07-manufacturing/journal/.

Endpoint checks (GET only):
- /predict/maintenance/leaderboard → 3 families × 3 windows of P/R/F1 + Brier
- /predict/maintenance/registry → registry state
- /drift/status/predmaint → reference_set: true
If any is not live, STOP and raise a hand.

Three-family leaderboard cite (cite, do not pick):
- lightgbm_features — gradient-boosted on hand-engineered window features
  (rolling mean / std / RMS / spectral)
- lstm_sequence — LSTM-shaped numpy approximation on raw sensor sequence
- survival_forest_tte — RandomSurvivalForest-shaped scipy approximation
  on time-to-event labels
Cite each in src/manufacturing/backend/ml_context.py — e.g.
"lightgbm_features, per fit_predmaint_lightgbm in
src/manufacturing/backend/ml_context.py."

Dollar asymmetry restatement:
- $12,000 unplanned line-stop (FN — missed maintenance signal)
- $1,800 planned-maintenance window (FP — too-early alarm at off-shift)
- Ratio 6.7:1 in favour of catching failures (specs/business-costs.md)
The WSH $1M ceiling does NOT apply to predmaint — wrong machine going
down is operational cost, not safety liability. Confirm this distinction.

Prediction-window trade-off (NAME, do NOT pick — Phase 5 owns):
- 3 days: faster recovery, more false positives (planned-maintenance overhead)
- 7 days: operations sweet spot — gives ops time to schedule downtime
- 14 days: lower FP rate but you've already lost throughput by the time you act

Calibration: Phase 6 SML adds calibration on top of threshold. The scaffold
exposes /predict/maintenance/calibrate with platt and isotonic methods.
Brier score and reliability diagram both render in the viewer. Calibration
matters because the maintenance scheduler consumes probabilities directly,
not just labels.

Phase 7 sweeps to name (NOT execute): adversarial sensor perturbation
(noise injection on vibration / current channels), out-of-distribution
(Q4 ramp pattern that isn't in the 30-day training window), per-machine
cohort skew (do machines on Line 1 perform differently from Line 3?).

After the summary, stop and wait for my Phase 4 SML prompt.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ Five skeleton files copied: `journal/phase_{4..8}_predmaint.md` exist
- ✓ `/predict/maintenance/leaderboard` returned 3 families × 3 windows
- ✓ `/predict/maintenance/registry` returned registry state
- ✓ `/drift/status/predmaint` returned `reference_set: true`
- ✓ Summary names the five SML phases, the prediction-window shape (3/7/14), and the calibration check
- ✓ Three Phase 7 sweeps named (sensor noise / Q4 ramp / per-machine cohort)
- ✓ Stop signal pending Phase 4 SML
- ✓ Viewer Sprint 2 tile activates

**Signals of drift — push back if you see:**

- ✗ A proposed window value (e.g. "7 days") — ask to remove
- ✗ A 4th family invented (e.g. "Prophet") — ask "which file in `src/manufacturing/backend/` defines this?"
- ✗ The WSH $1M ceiling claimed for predmaint — ask "isn't that the vision safety-critical class?"
- ✗ Calibration described as optional — ask "the maintenance scheduler consumes probabilities; isn't calibration load-bearing?"
- ✗ Per-machine cohort sweep missed — ask "the 10 machines split across 3 lines; isn't that the cohort surface?"

---

## 3. Things you might not understand in this step

- **SML replay** — Phases 4–8 run twice tonight, once per supervised modality (transfer-learned vision in Sprint 1, time-series in Sprint 2)
- **Time-series families** — LightGBM (engineered windows) vs LSTM (raw sequence) vs Survival Forest (time-to-event); different inductive biases on the same sensor stream
- **Calibration** — does "P=0.7 of failure in 7 days" actually mean the model is right 70% of the time? Brier + reliability diagram answer this
- **Prediction-window trade-off** — shorter windows catch failures sooner but produce more false alarms; longer windows reduce FP but you've already lost throughput
- **Three-family leaderboard** — three families on the same labels for direct comparison

---

## 4. Quick reference (30 sec, generic)

### SML replay

Phases 4–8 are run twice tonight: once for the vision QC inspector (Sprint 1, transfer-learning families), once for the predictive-maintenance classifier (Sprint 2, time-series families). Replay is a teaching tool — the same five-phase pattern fires on a different model class so the pattern itself becomes muscle memory. The journals carry suffixes (`_vision`, `_predmaint`) so they don't overwrite each other. Skipping the replay is BLOCKED — the rubric counts both passes.

### Time-series families

LightGBM with engineered window features (rolling mean / std / RMS / spectral peaks) is the practical baseline — fast, interpretable, robust on small data. LSTM on raw sequence captures temporal patterns the engineered features miss but is data-hungry. Survival Forest models time-to-event directly (the "censored" failure-time framing) and naturally produces the per-day failure probability shape. Phase 5 picks among these on cost-asymmetry × per-class P/R + calibration + inference cost.

### Calibration

A model's P=0.7 is calibrated if, across many P=0.7 predictions, the model is right 70% of the time. Brier score measures squared error vs the true label; reliability diagrams plot predicted vs observed frequency. Calibration matters tonight because the maintenance scheduler uses the failure probability to decide when to insert planned downtime — a miscalibrated classifier scoring P=0.95 when truth is P=0.6 produces wrong scheduling decisions and wastes planned-maintenance windows.

### Prediction-window trade-off

A 3-day window catches failures fast but produces 3× the false alarms of a 14-day window (because the smaller window has less time-to-event signal). A 14-day window has the cleanest calibration but you've lost a week of throughput by the time the alarm justifies action. The 7-day window is the operations sweet spot for SMT lines — long enough for clean calibration, short enough that ops can schedule downtime in the next maintenance window.

### Three-family leaderboard

LightGBM + LSTM + Survival Forest all evaluated on the same machines on the same holdout windows. The leaderboard shows P/R/F1 + Brier per family per window. The decision in Phase 5 is which family to ship — and the decision is rarely "the highest F1." A higher-F1 family that's miscalibrated may lose to a lower-F1 family with better reliability for the maintenance scheduler.

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 7 Sprint 2
(predictive maintenance), where I am building an industrial AI suite for
LumenCircuit.

Read `workspaces/metis/week-07-manufacturing/playbook/workflow-04-sprint-2-predmaint-boot.md`
for what this step does, and read `workspaces/metis/week-07-manufacturing/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. calibration >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current LumenCircuit state
3. Implications for the decision I'm about to make (or just made) in Sprint 2
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

- [ ] Five skeleton files exist (`journal/phase_{4..8}_predmaint.md`)
- [ ] `/predict/maintenance/leaderboard` returned 3 families × 3 windows
- [ ] `/predict/maintenance/registry` returned registry state
- [ ] `/drift/status/predmaint` returned `reference_set: true`
- [ ] Summary written: 5 SML phases, prediction-window shape, calibration check, 3 Phase 7 sweeps, $12K vs $1.8K asymmetry quoted
- [ ] Claude Code stopped, waiting for Phase 4 SML prompt

**Next file:** [`phase-04-candidates.md`](./phase-04-candidates.md) (PredMaint pass)
