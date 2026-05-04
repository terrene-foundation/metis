<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 8 — Deployment Gate (promote to shadow)

## 1. What this phase decides

PASS/FAIL the chosen model against pre-registered floors and Phase 7 findings. If PASS, promote to shadow stage. If FAIL, name the blocker and the rerun plan.

## 2. The Week 7 lens

**Vision (Sprint 1):**
Per-class threshold floors (cost-balanced for 3 classes + WSH 0.40 for safety_critical_defect), edge-latency floor (80 ms/board on Jetson), Brier ceiling per class, inference-cost ceiling. Promote via `POST /inspect/vision/promote { version, to_stage: "shadow" }`. The endpoint returns 409 if persisted threshold is below the 0.40 WSH floor at promote time.

**PredMaint (Sprint 2):**
Threshold floor on chosen window, calibration floor (Brier ≤ 0.20), per-machine cohort floor (no machine with > 5 pp recall delta). Promote via `POST /predict/maintenance/promote`.

**RL (Sprint 3):**
Reward-weight floors (clears the hard-floor table — zero hard-floor violations across 10,000 cached episodes), throughput floor (≥ 5% above random), defect-rate ceiling (cited from Phase 5 pre-registration). Promote via `POST /optimize/rl/promote`.

**Agent (Sprint 4) — collapsed:**
The agent gate is the autonomy ladder + the WSH shadow-mode mandate at Phase 11. Phase 8 Agent is the implicit gate that the post-WSH ladder is in shadow on safety-affecting categories.

## 3. Your levers

- **Per-floor PASS/FAIL** with measured value
- **HIGH-severity Phase 7 disposition** — RESOLVED or ACCEPTED-WITH-MITIGATION
- **Promotion stage** — staging → shadow (default Phase 8 target) → production
- **Rollback signal** — NAMED, not described

## 4. Paste-ready block for the journal

```
I'm in Playbook Phase 8 — Deployment Gate. The decision is PASS / FAIL
against pre-registered floors and Phase 7 findings.

Produce the gate document with these sections:

1. Pre-registered floors recap (from Phase 6 / 7 journals)
2. Per-floor PASS/FAIL with the actual measured value
3. HIGH-severity Phase 7 findings — RESOLVED or ACCEPTED-WITH-MITIGATION?
4. Inference-cost feasibility (Phase 5's $/day check)
5. Overall: PASS or FAIL
6. If PASS: promote to which stage (staging / shadow / production)?
   And what's the rollback signal?
7. If FAIL: which floor failed, what's the rerun plan?

Do NOT auto-promote — I sign the gate.
Do NOT use "blocker" without specifics.

Sprint detection:
- Sprint 1 (Vision): gate vision QC. POST /inspect/vision/promote
  { version, to_stage } — returns 409 if safety_critical_defect
  threshold persisted below 0.40 WSH floor.
- Sprint 2 (PredMaint): gate predmaint. POST /predict/maintenance/promote.
- Sprint 3 (RL): gate RL policy. POST /optimize/rl/promote — returns
  422 if safety_penalty weight below floor.

Pre-registered floors (Sprint-specific, recap from Phase 6 / 7):

Sprint 1:
- Per-class precision floor (named in Phase 6 journal)
- Per-class recall floor
- safety_critical_defect WSH hard-floor 0.40 honoured
- Brier ceiling per class (calibration)
- 80 ms/board edge-latency ceiling on Jetson
- $/day inference cost ceiling

Sprint 2:
- Cost-balanced threshold floor on chosen window
- Brier ≤ 0.20
- Per-machine cohort floor (no machine > 5 pp delta)

Sprint 3:
- Zero hard-floor violations across 10,000 cached episodes
- Throughput ≥ 5% above random baseline
- Defect-rate < ceiling
- Energy cost within budget

HIGH-severity Phase 7 findings to address:
- Vision: did any per-line cohort show recall delta > 5 pp?
- PredMaint: did Q4-ramp OOD trigger > 10% FN spike?
- RL: any non-zero hard-floor violation count?

Promotion stages:
- staging → shadow: model runs alongside production, scores logged but
  not auto-acted. Default Phase 8 PASS target.
- shadow → production: requires 7 days of shadow data + cross-sprint
  redteam pass. NOT a Phase 8 tonight decision unless instructor
  approves accelerated promotion.

Rollback signal (must be NAMED, not described):
- Sprint 1: per-class P/R drops below floor for 3 consecutive shifts;
  OR safety_critical_defect FN rate > 0 in any single shift
- Sprint 2: per-machine Brier exceeds 0.20 for 24 hours
- Sprint 3: any safety_violation in 100 deployment episodes; OR
  throughput drops below random baseline for 3 consecutive shifts

Endpoint:
- POST /inspect/{vision,predict,optimize}/promote with { version, to_stage }

Journal file: copy journal/skeletons/phase_8_gate.md (suffix
_vision / _predmaint / _rl).
```

## 5. Cost anchor

From `specs/business-costs.md`:

- A Phase 8 PASS that ships with safety_critical_defect threshold below 0.40 WSH floor blast radius: the regulator catches it, $1M+ WSH-notifiable exposure plus criminal liability for directors under WSH Act 2006
- A Phase 8 PASS that ignores a HIGH-severity Phase 7 cohort finding propagates the cohort skew into shadow data, corrupting the Phase 13 drift signal calibration

## 6. Hard-floor table

From `specs/compliance-floors.md`:

| Floor                         | Phase 8 enforcement                                                           |
| ----------------------------- | ----------------------------------------------------------------------------- |
| Safety-critical-defect ≥ 0.40 | `POST /inspect/vision/promote` returns 409 if persisted threshold below floor |
| RL safety_penalty ≥ floor     | `POST /optimize/rl/promote` returns 422 if weight below floor                 |
| Both gates are server-side    | A forgetful student CANNOT ship below floor                                   |

## 7. Reversal condition

A Phase 8 PASS is reversed when:

- **Signal**: any rollback-signal triggers in shadow data
- **Threshold**: as named in the rollback signal field
- **Duration**: as named in the rollback signal field

The rollback signal IS the reversal condition — that's the structural design.

## 8. Transfer to next project

The Phase 8 gate pattern is universal: pre-registered floors + measured values + named rollback signal + human sign-off. The rollback signal must be a (signal + threshold + duration) triple, never a vague "monitor metrics." The server-side enforcement at the promote endpoint (returning 409/422 below floor) is the structural defense against silent floor-violations — applies anywhere the regulator owns a class.

---

**Next file:** Sprint 1 → [`workflow-04-sprint-2-predmaint-boot.md`](./workflow-04-sprint-2-predmaint-boot.md). Sprint 2 → [`workflow-05-sprint-3-rl-boot.md`](./workflow-05-sprint-3-rl-boot.md). Sprint 3 → [`workflow-06-sprint-4-agent-mlops-boot.md`](./workflow-06-sprint-4-agent-mlops-boot.md).
