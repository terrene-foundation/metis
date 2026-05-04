<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 7 — Red-Team (per-sprint sweeps)

## 1. What this phase decides

Stress-test the chosen model on three sweeps: adversarial perturbation, out-of-distribution input, cohort skew (manufacturing analog to demographic skew). For RL: defend the four-term reward against Goodhart's Law via the leaderboard. Find failure modes before deployment.

## 2. The Week 7 lens

**Vision (Sprint 1):**
Adversarial = pixel noise, JPEG compression at the inspection-camera level. OOD = aspect-ratio variation, low-light synthetic dimming, novel defect mode (a defect type the 800-image scaffold under-represents). Cohort skew = per-line × per-shift × per-supplier-lot recall stratification (the manufacturing analog to demographic skew).

**PredMaint (Sprint 2):**
Adversarial = sensor-channel noise injection (vibration / current / temperature). OOD = Q4 ramp pattern that wasn't in the 30-day training window (`scenarios/q4_demand_drift.json` is the scaffold's mid-injection payload). Cohort skew = per-machine × per-line cohort recall (do all 10 machines fail at predicted rates? does Line 1 vs Line 3 vary?).

**RL (Sprint 3) — Goodhart defense:**
This is the heaviest Phase 7 of the night. The four reward weights interact non-monotonically. The leaderboard MUST show: chosen weights produce defect rate < ceiling AND throughput ≥ 5% above random baseline AND zero hard-floor violations across 10,000 cached episodes. Any reward-hacking (throughput up, defect up too) is a finding.

**Agent (Sprint 4) — collapsed into Sprint 3:**
The agent inherits Sprint 1/2/3 robustness findings. The cross-sprint cascade red-team in `workflow-07-redteam.md` is where the agent's autonomy ladder gets stress-tested.

## 3. Your levers

- **Adversarial perturbation set** — pixel/sensor noise, compression, channel-specific corruption
- **OOD scenario set** — aspect-ratio, lighting, Q4 ramp, novel defect mode
- **Cohort split set** — line × shift × supplier-lot for vision; machine × line for predmaint
- **RL leaderboard read** — defect rate, throughput, energy, safety_violations across all 3 policies
- **Severity ranking** — (probability × blast radius), not "scary-sounding"
- **Fairness deferral disclosure** — explicit deferral line; silent deferral scores 0 on D4

## 4. Paste-ready block for the journal

```
I'm in Playbook Phase 7 — Red-Team. Run three sweeps on the chosen
model:

1. Adversarial perturbation: how does the per-class score change under
   small input perturbations?
2. Out-of-distribution: how does the model perform on inputs unlike
   the training distribution?
3. Cohort-skew calibration: does P/R/F1 vary across natural cohorts?
   (Manufacturing analog to demographic skew.)

For each finding, name:
- The slice / perturbation that triggered the failure
- The per-class P/R/F1 delta vs holdout
- The blast radius in $ at production volume
- Severity (low / medium / high)

Surface "fairness deferred to Week 8 capstone" explicitly in the
journal — silent deferral is BLOCKED.

Do NOT propose mitigations beyond "monitor / re-train with augmentation
/ cap-the-class-confidence". Big-architecture fixes are not in
tonight's budget.
Do NOT use "blocker" without specifics.

Sprint detection (sweeps differ by modality):

Sprint 1 (Vision):
- Adversarial: random pixel noise (σ ∈ {0.01, 0.05, 0.10}), JPEG
  compression (Q ∈ {30, 50, 80}). Use scaffold's perturbation utility.
- OOD: aspect-ratio sweep, low-light synthetic dimming, novel defect
  mode (a defect_mode value under-represented in the 800-image set).
- Cohort: per-class recall stratified by line_id × shift × supplier_lot_id.

Sprint 2 (PredMaint):
- Adversarial: sensor-channel noise (vibration σ, current σ, temperature σ).
- OOD: Q4 ramp pattern via scenario_inject.py q4_demand_drift.
- Cohort: per-machine × per-line P/R/F1 (10 machines × 3 lines).

Sprint 3 (RL — Goodhart defense):
- Read /optimize/rl/leaderboard for all 3 policies (PPO, DQN, Random).
- Confirm chosen weights produce:
  (a) defect_rate < ceiling (cite ceiling from Phase 5 RL pre-registration)
  (b) throughput ≥ 5% above random baseline
  (c) ZERO hard-floor violations across 10,000 episodes
- If any of (a)/(b)/(c) fails, that's a Goodhart finding — re-pick weights.
- Adversarial: re-roll the policy with a perturbed initial state via
  /optimize/rl/simulate (e.g. start at the upper bound of safe
  temp range). Does the policy push back into safe envelope?
- OOD: simulate with a board_class distribution shifted toward
  Class 3 only — does throughput hold?

Severity ranking:
- HIGH: blast radius > $1M/year OR regulator visibility (WSH $1M
  ceiling triggered, MOM Inspectorate audit signal).
- MEDIUM: blast radius $10k–$1M/year.
- LOW: blast radius < $10k/year.

Fairness disclosure: every Phase 7 journal includes the line
"Fairness audit (full disparate-impact across protected classes) deferred
to Week 8 capstone per Playbook." This is mandatory — silent deferral
scores 0 on rubric D4.

Journal file: copy journal/skeletons/phase_7_red_team.md (suffix
_vision / _predmaint / _rl).
```

## 5. Cost anchor

From `specs/business-costs.md`:

- A Phase 7 vision finding showing per-line recall delta of 5 pp on `major_defect` blast radius: 12,000 boards/day × per-line fraction × 5% × $4,200 ≈ hundreds of thousands per day on the affected line
- A Phase 7 RL Goodhart finding (chosen weights produce defect-rate above ceiling) blast radius: at 40,000 boards/day × +1% defect rate × $180 (minor) or $4,200 (major) = $72K–$1.7M/day
- A Phase 7 predmaint OOD finding (Q4 ramp under-fires) blast radius: each missed unplanned stop × $12,000 / stop

## 6. Hard-floor table

From `specs/compliance-floors.md`, RL-specific:

| Floor                     | Source       | Where the Phase 7 leaderboard enforces                            |
| ------------------------- | ------------ | ----------------------------------------------------------------- |
| RL safety_penalty weight  | WSH Act 2006 | Leaderboard MUST show 0 hard-floor violations across 10K episodes |
| Equipment-damage envelope | Insurance    | Leaderboard MUST show 0 incidents at chosen weights               |
| WSH-notifiable            | WSH Act 2006 | Cross-checked at agent autonomy ladder (Phase 11)                 |

## 7. Reversal condition

A Phase 7 sweep is reversed when:

- **Signal**: a finding that was severity-ranked LOW shows up in /redteam cross-sprint review with cascade-amplified blast radius
- **Threshold**: cascade amplification factor > 5×
- **Duration**: any single /redteam read

## 8. Transfer to next project

The three sweeps (adversarial / OOD / cohort) generalise to every supervised model. RL adds a fourth: Goodhart defense via leaderboard verification of all reward dimensions, not just the optimised one. The fairness deferral disclosure is the structural defense against silent fairness gaps in the audit trail — applies in every regulated domain.

---

**Next file:** [`phase-08-gate.md`](./phase-08-gate.md)
