<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 13 — Drift × 3 cadences (retrain rules)

## 1. What this phase decides

Write three retrain rules — one per model — at three cadences (vision weekly / sensor daily / RL per-deployment). Each rule has signal + threshold (variance-grounded) + duration window + HITL disposition + seasonal exclusion.

## 2. The Week 7 lens

**Vision retrain rule (`model_id: vision`) — WEEKLY:**
Equipment + supplier-lot drift moves on weekly cycles (component lots change, line operators rotate). Signals: per-class score-distribution PSI; per-feature embedding PSI on representative pixel-feature. Threshold: variance-grounded (mean PSI + 3σ over 4-week stable baseline). Duration: signal exceeds threshold for 2 consecutive weekly checks. HITL: yes (Head of Quality approves first trigger). Seasonal exclusion: Q4 automotive ramp + medical certification cycles.

**PredMaint retrain rule (`model_id: predmaint`) — DAILY:**
Sensor calibration + ambient drift moves on daily cycles (Singapore humidity, shift changes, scheduled re-calibrations). Signals: per-feature PSI (vibration RMS, motor current p95, head temp rolling); calibration decay (Brier delta vs registered baseline); per-machine cohort PSI. Threshold: variance-grounded. Duration: 5 consecutive daily checks (1 week sustained). HITL: yes (Head of Operations approves first trigger). Seasonal exclusion: Q4 ramp + scheduled re-calibrations.

**RL retrain rule (`model_id: rl`) — PER-DEPLOYMENT:**
Every policy update IS a new model — drift is per-deployment. Signals: reward-component variance vs cached baseline (throughput / defect / energy / safety); safety_violation count delta; novel-state fraction. Threshold: any safety_violation OR throughput drop > 5% OR defect rate increase > 2%. Duration: per-deployment (any new policy version checks before promote-to-shadow). HITL: yes (Head of Operations + Head of EHS jointly — RL retrain touches the safety envelope). Seasonal exclusion: any active MOM mandate window suspends auto-retrain.

## 3. Your levers

- **Cadence per model** — weekly / daily / per-deployment, NEVER universal
- **Signal selection** — PSI, calibration decay, reward-component variance
- **Variance-grounded threshold** — mean + N σ over a stable historical window; cite the baseline mean and σ
- **Duration window** — N consecutive checks before firing
- **HITL disposition per model** — named persona (Head of Quality / Operations / EHS)
- **Seasonal exclusion** — Q4 ramp + medical certification + planned re-calibrations + active MOM mandate

## 4. Paste-ready block for the journal

```
I'm in Playbook Phase 13 — Drift Retrain Rules. Write three retrain
rules, one per model. For each:

1. Cadence: how often the rule is checked (weekly / daily / per-deployment)
2. Signal(s): what is monitored (PSI, calibration decay, reward-component
   variance)
3. Threshold per signal: variance-grounded (mean + N std-devs over a
   stable historical window)
4. Duration window: must persist for X consecutive checks before firing
5. HITL disposition on first trigger: named persona who approves
6. Seasonal exclusion: windows when the rule does NOT auto-fire

Do NOT propose universal cadence. Three models = three cadences.
Do NOT use "blocker" without specifics.

Three models, three cadences (cite from PRODUCT_BRIEF.md §4.4):

1. Vision (model_id: vision) — WEEKLY
   - Signals: per-class score-distribution PSI; per-feature embedding
     PSI on representative pixel-feature.
   - Threshold: PSI > N where N is variance-grounded (mean PSI + 3σ
     over a stable 4-week baseline). State the historical mean and σ
     used; do NOT guess a value.
   - Duration: signal exceeds threshold for 2 consecutive weekly checks.
   - HITL: yes — Head of Quality approves first trigger (per persona
     table in PRODUCT_BRIEF.md §3).
   - Seasonal exclusion: Q4 automotive ramp + medical certification
     cycles (per specs/business-costs.md "Seasonality").

2. PredMaint (model_id: predmaint) — DAILY
   - Signals: per-feature PSI (vibration RMS, motor current p95,
     head_temp rolling); calibration decay (Brier delta vs registered
     baseline); per-machine cohort PSI (10 machines tracked separately).
   - Threshold: variance-grounded (state historical mean and σ).
   - Duration: signal exceeds threshold for 5 consecutive daily checks
     (1 week of sustained drift).
   - HITL: yes — Head of Operations approves first trigger.
   - Seasonal exclusion: Q4 ramp + scheduled equipment re-calibrations
     (the planned re-calibrations cause baseline shifts that should NOT
     auto-trigger retrain).

3. RL (model_id: rl) — PER-DEPLOYMENT
   - Signals: reward-component variance vs cached baseline (throughput /
     defect / energy / safety); safety_violation count delta vs floor;
     novel-state fraction.
   - Threshold: ANY safety_violation OR throughput drop > 5% OR defect
     rate increase > 2 pp on the next-deployment check.
   - Duration: per-deployment (any new policy version triggers a check
     before promote-to-shadow).
   - HITL: yes — Head of Operations + Head of EHS jointly (RL retrain
     touches the safety envelope; both signatures required).
   - Seasonal exclusion: any active MOM mandate window suspends
     auto-retrain — explicit gate.

Variance-grounding: every threshold MUST be backed by historical
variance data. The scaffold's drift_baseline.json has the per-model
reference. Use mean + 3σ as the default threshold formula; state the
actual values read from the baseline file in the journal.

HITL on first trigger: explained in the autonomy ladder set in
Phase 11. First time the rule fires, the named persona approves. After
30 days of stable post-retrain operation, the rule may auto-fire on
subsequent triggers (except RL, which always requires joint HITL).

Seasonal exclusions cited from specs/business-costs.md "Seasonality":
Q4 automotive ramp + medical device certification cycles + scheduled
equipment re-calibrations.

Endpoint per model:
- POST /drift/retrain_rule with { model_id, signals, thresholds,
  duration_window, hitl, seasonal_exclusions }
- Call once per model_id (3 calls total).

Journal file: journal/phase_13_retrain.md (single file, three rules
inside).
```

## 5. Cost anchor

From `specs/business-costs.md`:

- **Cold-start misclassification ($620/novel mode):** the cost the drift signal exists to bound — without a retrain rule, novel defect modes accumulate at $620 each
- **Cloud RL training ($0.40/hr):** retrain compute is negligible vs the cost of NOT retraining
- **Q4 ramp seasonality:** the explicit window where auto-retrain bakes the spike into the model

## 6. Hard-floor table

Not a Phase 13 floor table per se, but the RL retrain rule has a hard requirement: **any active MOM mandate window suspends auto-retrain on RL**. This is the structural defense against retraining a policy under a regulator mandate where the underlying envelope is itself in flux.

## 7. Reversal condition

A Phase 13 retrain rule is reversed when:

- **Signal**: rule fires repeatedly (3+ times in 30 days) without finding actual drift
- **Threshold**: 3+ false-positive triggers
- **Duration**: 30-day rolling window

Then the threshold was set tighter than the natural variance — re-derive the variance-grounded threshold against a longer baseline.

## 8. Transfer to next project

Stratified drift cadence by data-generating process is universal. The pattern: (a) one rule per model_id; (b) cadence chosen by the data-generating process (slow-moving = weekly, fast-moving = daily, per-update for RL); (c) variance-grounded thresholds, never textbook-borrowed values; (d) HITL on first trigger with named persona authority; (e) seasonal exclusion as a hard gate on auto-firing. Anywhere the system spans modalities or update cadences, the same three-rules-three-cadences pattern is the only honest answer.

---

**Next file:** [`workflow-07-redteam.md`](./workflow-07-redteam.md)
