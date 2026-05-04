<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 10 — Objective Function (RL reward function shape)

## 1. What this phase decides

Set the RL reward function for the reflow-oven controller. Four terms: throughput / defect_cost / energy_cost / safety_penalty. Decide the SHAPE here (which terms, what units, which direction); pre-register the WEIGHTS before reading the Phase 7 RL leaderboard.

## 2. The Week 7 lens

**RL (Sprint 3) — primary deliverable:**
The reward function is the load-bearing decision in any RL system. Tonight's four terms:

```
reward = w_throughput × throughput
       - w_defect    × defect_count × per_class_cost
       - w_energy    × kwh × $0.08
       - w_safety    × safety_violations  ← MUST clear hard floor
```

Where:

- `throughput` = boards completed per shift
- `defect_count × per_class_cost` cites $4,200 (major) / $180 (minor) from `specs/business-costs.md`
- `kwh × $0.08` is energy (operational cost)
- `safety_violations` is the count of envelope violations per episode; HARD-floored — `safety_penalty` weight MUST be ≥ floor that yields zero hard-floor violations across 10K episodes

**Inspector queue allocator (Sprint 4 — secondary deliverable):**
A separate LP for the inspector queue allocator runs at `/queue/solve`. Its objective minimises (FN cost × FN at tier + FP cost × FP at tier + inspector_minutes × $35 + edge_inference × $0.001/board). This LP and the RL reward function are SEPARATE objectives; do not conflate.

**Vision / PredMaint / Agent — N/A:**
No phase-10 objective decision; thresholds (Phase 6) and autonomy (Phase 11) cover their decision surfaces.

## 3. Your levers

- **Reward term selection** — which dimensions enter the function
- **Weight units** — keep all four in $-equivalent so the LP is honest
- **Defect cost differentiation** — major ($4,200) vs minor ($180); is the reward weighted by class?
- **Energy term inclusion** — ops cost vs noise; including it forces the agent to learn energy-efficient setpoints
- **Safety term inclusion** — must be present, must hit the hard floor

## 4. Paste-ready block for the journal

```
I'm in Playbook Phase 10 — Objective Function (RL reward + inspector
queue LP).

For the RL reward function:
1. Show the four-term shape:
   reward = w_throughput × throughput
          - w_defect × defect_count × per_class_cost
          - w_energy × kwh × $0.08
          - w_safety × safety_violations
2. Cite each cost from specs/business-costs.md
3. Pre-register the weight SHAPE (e.g. "w_safety dominates;
   w_throughput second; w_defect third; w_energy smallest"). Do NOT
   pre-register exact numerical weights — those are read from the
   leaderboard in Phase 7 RL after I see how the policies perform.
4. State the hard-floor relationship: w_safety MUST be ≥ floor that
   yields ZERO hard-floor violations across 10,000 cached episodes
   (cite specs/compliance-floors.md).

For the inspector queue allocator LP:
1. Decision variables: x[tier, queue] = number of boards at this
   confidence tier routed to this queue
2. Objective: minimise sum over (tier, queue) [
     expected_FN_at(tier) × $4,200 (major) or $180 (minor)
     + expected_FP_at(tier) × $85
     + expected_inspector_minutes_at(queue) × $35
     + expected_edge_inferences × $0.001/board
   ]
3. Decision variable space:
   - Tiers (4): auto_pass, manual_review, expedited_review, auto_fail
   - Queues (3): expedited (60-min SLA), standard (4-hour SLA),
     bulk (24-hour for low-confidence batches)

Defenses per term:
- RL throughput: 2-3% recovery target = $48K-$72K/day upside
  (specs/business-costs.md "Decision anchors")
- RL defect cost: $4,200/major board × per-class rate
- RL energy: $0.08/kWh × kWh; small term but binds the agent against
  flat-out heating
- RL safety: HARD-floored (specs/compliance-floors.md)
- Queue inspector: $35/min × ~3-min mean review × ~1,400 queue start =
  $147K/day inspector cost

Do NOT propose hard or soft constraints — those are Phase 11.
Do NOT use "blocker" without specifics.

Endpoints:
- POST /optimize/rl/reward_function with { throughput, defect_cost,
  energy_cost, safety_penalty } weights — returns 422 if safety_penalty
  below the hard-floor that yields zero violations
- POST /queue/solve to run the inspector queue LP

Journal file: copy journal/skeletons/phase_10_objective.md.
```

## 5. Cost anchor

From `specs/business-costs.md`:

- **RL throughput recovery:** 2-3% × 40,000 boards/day × ~$60 contribution margin = $48,000–$72,000/day (the upside that justifies RL at all)
- **RL defect cost:** $4,200 (major) or $180 (minor) per board
- **RL energy:** $0.08/kWh × ~kWh per shift (small term, binds against extremes)
- **Inspector queue:** $35/min × ~3-min × 1,400 queue start = ~$147,000/day inspector cost

## 6. Hard-floor table

From `specs/compliance-floors.md`:

| Floor                     | Source       | Phase 10 enforcement                                           |
| ------------------------- | ------------ | -------------------------------------------------------------- |
| RL safety_penalty weight  | WSH Act 2006 | `POST /optimize/rl/reward_function` returns 422 below floor    |
| Equipment damage envelope | Insurance    | $50,000/incident, 0/year — surfaces in Phase 11 hard table     |
| WSH-notifiable            | WSH Act 2006 | 0/year — surfaces in Phase 11 hard table + Phase 12 acceptance |

The reward function CANNOT be cost-balanced for the safety term — it sits ABOVE the cost-balanced math.

## 7. Reversal condition

A Phase 10 reward function is reversed when:

- **Signal**: Phase 7 RL leaderboard shows reward-hacking (chosen weights produce throughput up AND defect rate up AND/OR safety_violations > 0)
- **Threshold**: any non-zero hard-floor violation OR defect rate above pre-registered ceiling
- **Duration**: any single Phase 7 leaderboard read

Then re-pre-register the weight shape and re-run Phase 7 — Goodhart caught you.

## 8. Transfer to next project

The four-term reward function generalises to any RL system. The pattern: (a) one term per real-world cost dimension; (b) all terms in $-equivalent units so the function is honest; (c) the safety term sits ABOVE the cost-balanced math via a hard floor enforced server-side at the API boundary; (d) pre-register weight SHAPE, not values, so post-hoc rationalisation against the leaderboard is structurally blocked. Anywhere the model has multiple competing axes (throughput, latency, cost, safety, fairness), the same shape applies.

---

**Next file:** [`phase-11-constraints.md`](./phase-11-constraints.md)
