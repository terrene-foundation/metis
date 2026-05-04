<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 6 — Sprint 4 Agent + MLOps Boot (Coordination agent + drift × 3)

> **What this step does:** Boot Sprint 4 by copying the Phase 13 skeleton, confirming drift endpoints are live for all three model IDs, and orienting on why the three retrain rules sit at three different cadences.
> **Why it exists:** Most students try to write one universal retrain rule that fires across all three models. That fails the rubric. Booting cleanly forces you to confront the three-cadence reality before you write the rule. Sprint 4 also closes the chain by exercising the LLM agent's `/agent/decide` endpoint on real test contexts.
> **You're here because:** Sprint 3 wrapped (Phase 12 post-WSH accepted) and Sprint 4 closes the chain.
> **Key concepts you'll see:** drift × 3 cadences (vision weekly / sensor daily / RL per-deployment), PSI, calibration decay, agent autonomy ladder under WSH, HITL on first trigger

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering Sprint 4 — coordination agent + MLOps drift monitoring. Three
drift rules, three cadences, three signals. Phase 13 fires once but covers
all three models. The agent's autonomy ladder (set in Phase 11) is now
active; /agent/decide must return real decisions on test contexts.

Before I start Phase 13, I need you to:

1. Copy the Phase 13 skeleton from journal/skeletons/phase_13_retrain.md
   into journal/.

2. Confirm /drift/status/{model_id} returns reference_set: true for all
   three IDs (vision, predmaint, rl).

3. Confirm /agent/policy is at the post-WSH state (WSH-affecting categories
   in shadow if the MOM mandate window is active).

4. State, in writing: why the three models drift at three different
   cadences and what signals are appropriate for each. Do NOT propose
   threshold values; those are my pre-registration call in
   phase_13_retrain.md.

5. Name the seasonal exclusions explicitly. Q4 ramp + scheduled
   re-calibrations spike both sensor and vision distributions; auto-
   retraining on those windows bakes the spike into the model. Cite from
   PRODUCT_BRIEF.md.

6. Do NOT use the word "blocker" without naming a specific action.

Once skeleton is copied and endpoints confirmed live, summarise: the three
cadences (vision weekly / sensor daily / RL per-deployment), the signal per
cadence, the role of HITL on first trigger, and the seasonal exclusions.

Then stop and wait for my Phase 13 prompt.
```

**Tonight-specific additions** (Week 7 LumenCircuit Sprint 4):

```
Sprint: Sprint 4 Agent + MLOps — coordination agent + drift × 3 models.
Phases covered: Playbook phase 13 (one entry covers all three models),
plus an agent-decision exercise to demonstrate the ladder is live.

Skeleton copy: copy phase_13_retrain.md from journal/skeletons/ into journal/.

Endpoint checks (GET only):
- /drift/status/vision → reference_set: true
- /drift/status/predmaint → reference_set: true
- /drift/status/rl → reference_set: true
- /agent/policy → returns the autonomy ladder you set in Phase 11
  (post-WSH if the MOM mandate fired)
If any returns reference_set: false, STOP and raise a hand — do not re-seed.

Why three cadences (NAME, do NOT pick threshold values):
- VISION model: equipment + supplier drift moves on weekly cycles
  (component lots change, line operators rotate); per-class score
  distribution PSI + per-feature embedding PSI; cadence WEEKLY.
- PREDMAINT (sensor) model: temperature, calibration, and ambient drift
  move on daily cycles (Singapore humidity, shift changes); rolling
  window feature PSI + per-class calibration decay; cadence DAILY.
- RL model: every policy update IS a new model — drift is per-deployment.
  Reward-distribution variance vs cached baseline + safety-violation
  count; cadence PER-DEPLOYMENT (any new policy version triggers a check
  before promote-to-shadow).

Signals per cadence (NAME, do NOT propose thresholds):
- VISION: per-class score-distribution PSI (mean + 3σ over 4 weeks
  baseline); per-feature embedding PSI on a representative pixel-feature.
- PREDMAINT: per-feature PSI (vibration RMS, motor current p95, head-temp
  rolling mean); calibration decay (Brier delta vs registered baseline);
  per-machine cohort PSI (ten machines tracked separately).
- RL: reward-component variance vs cached baseline (throughput / defect /
  energy / safety); safety_violation count delta vs floor; novel-state
  fraction.

Seasonal exclusions (cite from PRODUCT_BRIEF.md §2 + business-costs.md
"Seasonality"): Q4 automotive ramp + medical certification cycles +
scheduled equipment re-calibrations. Auto-retraining during these windows
bakes the seasonal spike into the model and lowers recall on harm
permanently for the next quarter.

HITL on first trigger: every retrain rule fires HITL on first trigger.
After the first trigger AND a successful re-train AND a 30-day stable
window, the rule may auto-fire on subsequent triggers. The HITL human is
named per task class:
- vision retrain → Head of Quality (per Persona table)
- predmaint retrain → Head of Operations
- RL retrain → Head of Operations + Head of EHS jointly (because RL
  retrain touches the safety envelope)

Agent decision exercise (after Phase 13 journal is drafted, before
/redteam): POST /agent/decide on at least three test contexts:
1. A board with vision_score=0.31 on safety_critical_defect (just under
   the WSH 0.40 floor — confirm the agent escalates to manual review)
2. A machine with predmaint score 0.78 over 7-day window (confirm the
   agent suggests planned-maintenance scheduling)
3. A reflow setpoint suggestion that pushes line speed to 65 boards/min
   (confirm the agent's setpoint_adjustment task class is in shadow per
   the post-WSH ladder, agent recommends but does NOT act)
Save the three audit_id values to journal/phase_13_retrain.md as
demonstration that the ladder is live.

After the summary, stop and wait for my Phase 13 prompt.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ Skeleton copied: `journal/phase_13_retrain.md`
- ✓ All three `/drift/status/{model_id}` endpoints returned `reference_set: true`
- ✓ `/agent/policy` returned the post-WSH autonomy ladder (if MOM mandate fired)
- ✓ Summary names the three cadences (weekly / daily / per-deployment) with rationale per cadence
- ✓ Summary names the signals per cadence (PSI variants, calibration decay, reward-component variance)
- ✓ Seasonal exclusions cited from `PRODUCT_BRIEF.md §2` (Q4 ramp + medical certification + scheduled re-calibrations)
- ✓ HITL-on-first-trigger named per model with the specific persona who approves
- ✓ Three `/agent/decide` test contexts identified (NOT yet run; that comes after Phase 13 journal)
- ✓ Stop signal pending Phase 13
- ✓ Viewer Sprint 4 tile activates

**Signals of drift — push back if you see:**

- ✗ A single universal cadence proposed (e.g. "weekly across all three") — ask "what's the rationale per model? sensor data drifts faster than equipment-induced vision drift."
- ✗ Threshold values proposed (e.g. "PSI > 0.25") — ask to remove
- ✗ "Auto-retrain immediately on trigger" — ask "where's HITL on first trigger? PRODUCT_BRIEF says first-trigger is HITL."
- ✗ Seasonal exclusions described only as "Nov–Dec" — ask "isn't tonight's seasonal exclusion Q4 automotive ramp + medical certification + scheduled re-calibrations?"
- ✗ A `reference_set: false` ignored — ask "the reference is missing for this model; isn't that a scaffold bug?"
- ✗ Agent decision exercise skipped — ask "the autonomy ladder is the Sprint 3 deliverable; doesn't Sprint 4 demonstrate it via /agent/decide?"

---

## 3. Things you might not understand in this step

- **Drift cadence stratification** — different models drift at different speeds; one universal retrain rule fails
- **PSI (Population Stability Index)** — measures how much a distribution has shifted from a registered baseline
- **Calibration decay** — even if accuracy holds, the probabilities can become miscalibrated as the world drifts
- **HITL on first trigger** — first time a retrain rule fires, a human approves before retraining auto-runs
- **Seasonal exclusion** — windows of expected operational spike (Q4 ramp, planned re-calibrations) where auto-retraining bakes the spike into the model

---

## 4. Quick reference (30 sec, generic)

### Drift cadence stratification

The three models drift at three speeds. Equipment + supplier-lot drift on the vision side moves weekly — component lots change, line operators rotate. Sensor calibration + ambient drift on the predmaint side moves daily — Singapore humidity swings, shift changes shift baseline temps. RL drift is per-deployment because every policy update IS a new model — there is no continuous-drift baseline to track. A universal retrain rule (e.g. "weekly across all three") under-reacts on sensors and over-reacts on RL.

### PSI (Population Stability Index)

A simple statistic that measures how much a distribution has shifted: sum over bins of `(p_now - p_ref) × ln(p_now / p_ref)`. PSI < 0.1 = no meaningful shift; PSI 0.1–0.25 = moderate; PSI > 0.25 = significant. Used tonight for per-class score distributions (vision), per-feature sensor windows (predmaint), and per-component reward distributions (RL). The thresholds you set in Phase 13 are PSI-floor values per signal — variance-grounded against the registered baseline.

### Calibration decay

Brier score or reliability-diagram drift over time. Even if F1 holds, the model's P=0.7 may now correspond to actual frequency P=0.55 — the labels still come out right but the probabilities lie. Calibration decay matters tonight because the maintenance scheduler (Phase 6 PredMaint) consumes probabilities directly. A miscalibrated predmaint classifier silently corrupts the planned-maintenance scheduling decisions, wasting $1,800 windows on machines that wouldn't have failed.

### HITL on first trigger

The first time a retrain rule fires (signal exceeds threshold over the duration window), a named human approves before the retrain auto-runs. After the first successful retrain AND a 30-day stable window, the rule may auto-fire on subsequent triggers. Tonight the HITL human is per-model: Head of Quality for vision, Head of Operations for predmaint, Head of Operations + Head of EHS jointly for RL (because RL retrain touches the safety envelope).

### Seasonal exclusion

A window of expected operational spike (Q4 automotive ramp, medical certification cycles, scheduled equipment re-calibrations) during which auto-retraining is suspended. The reason: an auto-retrain on a Q4 spike bakes the ramp pattern into the model — the predmaint classifier learns that the ramp is "normal," then the ramp ends and the classifier under-fires on real failure precursors for the next quarter. Seasonal exclusion is a hard constraint on retrain-rule firing.

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 7 Sprint 4 (agent
+ drift), where I am building an industrial AI suite for LumenCircuit.

Read `workspaces/metis/week-07-manufacturing/playbook/workflow-06-sprint-4-agent-mlops-boot.md`
for what this step does, and read `workspaces/metis/week-07-manufacturing/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. drift cadence stratification >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current LumenCircuit state
3. Implications for the decision I'm about to make (or just made) in Sprint 4
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

- [ ] Skeleton copied (`phase_13_retrain.md`)
- [ ] All three `/drift/status/{model_id}` returned `reference_set: true`
- [ ] `/agent/policy` confirmed at post-WSH state
- [ ] Summary names three cadences with rationale, three signals, seasonal exclusions, HITL-on-first-trigger persona-by-persona
- [ ] Three `/agent/decide` test contexts identified for the post-Phase-13 demonstration
- [ ] Claude Code stopped, waiting for Phase 13 prompt

**Next file:** [`phase-13-drift.md`](./phase-13-drift.md)
