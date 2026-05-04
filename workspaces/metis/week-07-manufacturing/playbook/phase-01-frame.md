<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 1 — Frame

## 1. What this phase decides

Pin down exactly what gets classified, over what window, how many auto-decisions per minute the line can sustain, and what it costs when the answer is wrong — in writing, before any code runs.

## 2. The Week 7 lens

**Vision QC (Sprint 1):**
The frame names the per-board score (good / minor / major / safety_critical), the per-board horizon (≤ 80 ms edge inference), the throughput ceiling (12,000 inspection events/day across 3 lines), and the 49:1 cost asymmetry between major-defect-shipped ($4,200) and false-scrap ($85). The WSH $1M+ ceiling on safety_critical is acknowledged here as a SEPARATE structural floor, not folded into cost-balanced math.

**Predictive Maintenance (Sprint 2):**
Frame names the per-machine-per-day score, the prediction window (3/7/14 days — your Phase 5 call), the throughput ceiling (10 machines × daily check), and the 6.7:1 asymmetry between $12,000 unplanned and $1,800 planned. No regulatory floor on predmaint — operational cost only.

**RL controller (Sprint 3):**
Frame names the per-step state-action pair (zone temps + line speed × ±5 °C / ±10 boards-per-min), the horizon (per-episode reward over a shift), the throughput ceiling (2-3% throughput recovery target = $48-72K/day upside), and the THREE asymmetries that bind: defect cost in the reward, $50K equipment-damage hard floor, and WSH $1M+ ceiling.

**Coordination Agent (Sprint 4):**
Frame names the per-board+per-machine context the agent decides on, the four task classes, and the autonomy modes the ladder permits. The agent is decoupled from a single $-asymmetry — it inherits the per-task-class costs from the upstream models.

## 3. Your levers

- **Target unit and granularity** — per-board / per-machine-per-day / per-step state-action / per-context decision
- **Population inclusions and exclusions** — IPC-A-610 Class 3 vs Class 2 boards; which machines / lines / shifts are in scope
- **Horizon in seconds or hours** — never "fast"
- **Throughput ceiling** — named with a role owner (Head of Quality / Head of Operations / Head of EHS)
- **Cost asymmetry** — quoted from `specs/business-costs.md`, never invented

## 4. Paste-ready block for the journal

```
I'm entering Playbook Phase 1 — Frame. My decision here is the written
frame for this sprint's model — target, population, horizon, throughput
ceiling, and the cost asymmetry in dollars that every later phase will
anchor to.

Draft the frame for me to edit. Produce these pieces, in order:

1. Target — one sentence naming WHAT is predicted/classified, the unit
   (per board, per machine-day, per step, per agent-context), and the
   window in milliseconds, hours, or days.
2. Population — inclusions AND explicit exclusions (IPC-A-610 Class 2
   vs Class 3; specific machines/lines in scope; shifts in scope).
3. Horizon — named in seconds, hours, or days. Sprint 1 vision: 80 ms
   edge latency. Sprint 2 predmaint: per-machine-per-day. Sprint 3 RL:
   per-step in real-time. Sprint 4 agent: per-context.
4. Primary cost term AND secondary cost term. Quote both from
   specs/business-costs.md verbatim; do not invent numbers.
5. Throughput ceiling — how many decisions per minute the auto-layer can
   handle before the queue overflows, and WHO owns the ceiling (a role,
   not "the team").

Then show the dollar exposure per day at a plausible mis-classification
rate, using only sourced numbers.

Tonight-specific:
- Sprint 1 cost terms: $4,200 (major-defect FN) + $85 (false-scrap FP).
  Asymmetry = 49:1. Quote BOTH lines verbatim from
  specs/business-costs.md.
- Sprint 2 cost terms: $12,000 (unplanned line-stop FN) + $1,800
  (planned-maintenance window FP). Asymmetry = 6.7:1.
- Sprint 3 cost terms: defect cost (per-board contribution to reward)
  + $50,000 equipment-damage hard floor + WSH $1,000,000+ ceiling.
- Sprint 4: inherits from upstream; frame names the four task classes.
- Throughput: 12,000 inspection events/day; 10 machines × daily;
  ~30-min reflow re-balance cycle today.
- The WSH $1M ceiling on safety_critical_defect (Sprint 1) and on
  WSH-affecting RL/agent categories (Sprint 3) is a SEPARATE structural
  cost, not folded into the cost-balanced math. Acknowledge it as a
  hard floor here, but don't fold it in.

Do NOT propose values for thresholds, architectures, RL weights, or
autonomy slots — those are my calls in later phases.
Do NOT use "blocker" without naming a specific next step.

Journal file: copy journal/skeletons/phase_1_frame.md into
workspaces/metis/week-07-manufacturing/journal/phase_1_frame.md and fill
in as we go.

When the journal file has the five items drafted and the arithmetic
shown, stop and wait for my review.
```

## 5. Cost anchor

From `specs/business-costs.md` "Direct costs":

- **Major defect shipped:** $4,200 / board (Sprint 1 FN)
- **Good board scrapped:** $85 / board (Sprint 1 FP)
- **Unplanned line-stop:** $12,000 / stop (Sprint 2 FN)
- **Planned-maintenance window:** $1,800 / stop (Sprint 2 FP)

Asymmetry call-outs: **49:1** (Sprint 1 FN/FP), **6.7:1** (Sprint 2 FN/FP).

## 6. Hard-floor table (acknowledge here, don't fold in)

From `specs/compliance-floors.md`:

| Floor                                       | Source          | Threshold | Where enforced                       |
| ------------------------------------------- | --------------- | --------- | ------------------------------------ |
| Safety-critical-defect auto-pass confidence | IPC-A-610 Cl. 3 | ≥ 0.40    | `POST /inspect/vision/threshold`     |
| WSH-notifiable incident                     | WSH Act 2006    | 0/year    | `POST /agent/policy` (forces shadow) |

Phase 1 acknowledges these floors exist; Phase 6 (vision) and Phase 11 (autonomy) enforce them.

## 7. Reversal condition

A Phase 1 frame is reversed when:

- **Signal**: a sprint's actual auto-decision daily volume diverges from the framed throughput ceiling
- **Threshold**: > 25% (sustained)
- **Duration**: 3 consecutive shifts

Then re-open the frame: ceiling assumption is wrong, and downstream phases (especially Phase 10 / 11) need re-anchoring.

## 8. Transfer to next project

The frame is the most transferable artefact in the Playbook. In any new ML domain (Week 8 capstone, your next job), the same five items — target/population/horizon/cost-asymmetry/throughput-ceiling — anchor every later decision. The two pitfalls that show up everywhere: (a) horizon stated as "fast" or "real-time" instead of milliseconds; (b) cost asymmetry invented at the agent's pattern-matching default of 1:1 instead of read from the finance pack.

---

**Next file:** [`phase-02-data-audit.md`](./phase-02-data-audit.md)
