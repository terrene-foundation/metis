<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 12 — Solver Acceptance (RL leaderboard accept + LP solve)

## 1. What this phase decides

Solve the LP allocator + read the RL leaderboard with the Phase 10 objective + Phase 11 constraints. Accept or reject based on feasibility, optimality gap, and pathology checks. Re-run after MOM/WSH injection — this is the most common D3 zero of the night if skipped.

## 2. The Week 7 lens

**RL leaderboard accept (Sprint 3):**
With weights set in Phase 10 + hard floors set in Phase 11, the chosen policy must clear ALL of: zero hard-floor violations across 10K episodes, throughput ≥ 5% above random baseline, defect rate < ceiling, energy within budget. ACCEPT, REVISE-AND-RESOLVE, or REJECT-AND-REDESIGN.

**Inspector queue LP accept (Sprint 4):**
`POST /queue/solve` with constraints from Phase 11. Acceptance memo: feasibility, optimality gap, pathology checks (queue concentration, empty queues, SLA violations, inspector overload), total $ cost, shadow prices.

**Post-WSH re-acceptance:**
Re-run BOTH the RL leaderboard read AND the queue LP solve under the post-WSH envelope. Quantify the **compliance shadow price**: $/day delta = post-WSH expected throughput − pre-WSH expected throughput (both cost-equivalent). This delta IS the cost of the regulator's mandate. Save as `journal/phase_12_postwsh.md`.

## 3. Your levers

- **Feasibility check** — does a plan exist under the hard constraints?
- **Optimality gap** — how far is the plan from the LP lower bound?
- **Pathology check** — operationally bad plans that are technically feasible (queue concentration, inspector overload)
- **Compliance shadow price** — $/day cost of the MOM/WSH envelope

## 4. Paste-ready block for the journal

```
I'm in Playbook Phase 12 — Solver Acceptance.

For RL: read /optimize/rl/leaderboard with the chosen weights + hard
floors. Confirm the chosen policy clears:
1. Zero hard-floor violations across 10,000 cached episodes
2. Throughput ≥ 5% above random baseline
3. Defect rate < ceiling (cite Phase 5 RL pre-registration)
4. Energy within budget

For inspector queue LP: POST /queue/solve and read the result.

Produce an acceptance memo:
1. Feasibility: did the LP find a feasible plan? If INFEASIBLE, which
   hard constraint is over-tight?
2. Optimality gap: how far is the plan from the LP's lower bound?
3. Pathology checks:
   - Concentration: is one queue handling > 70% of boards?
   - Empty queues: is any queue allocated zero boards?
   - SLA violations: how many soft-SLA breaches at the optimum?
   - Inspector overload: are inspector-minute totals within headcount?
4. Total expected $ cost: sum of all four objective terms at the plan
5. Shadow prices on the binding constraints

Then: ACCEPT, REVISE-AND-RESOLVE, or REJECT-AND-REDESIGN.

Do NOT auto-accept — I sign.
Do NOT use "blocker" without specifics.

Endpoints:
- /optimize/rl/leaderboard (read)
- POST /queue/solve to run; GET /queue/last_plan to read result.

First pass (BEFORE MOM/WSH injection):
- Expected: feasible plan with cost-balanced setpoint_adjustment +
  safety_alert (agent may recommend), no expedited-queue overload, SLA
  breaches in soft-acceptable range.
- Total $ cost: state at the plan.
- Shadow prices: which constraint is binding? Inspector headcount or
  expedited-queue SLA?

Post-MOM/WSH injection (~4:30pm):
- Re-solve: read /optimize/rl/leaderboard AGAIN with the post-WSH
  ladder (setpoint_adjustment + safety_alert in shadow). The chosen
  policy's effective throughput drops because the agent can no longer
  auto-act on safety-affecting setpoints.
- Re-solve: POST /queue/solve again. The plan changes visibly:
  expedited queue load may shift; SLA shadow price likely shifts.
- Total $ cost should INCREASE (compliance cost is non-zero).
- Quantify the COMPLIANCE SHADOW PRICE: $/day delta =
  post-WSH expected $ - pre-WSH expected $. This IS the regulator-
  imposed cost in real dollars.
- Save second pass as journal/phase_12_postwsh.md.
- The first pass STAYS in journal/phase_12_acceptance.md — do NOT
  overwrite.

Pathology checks (specific):
- RL: any policy with non-zero hard-floor violations is auto-REJECT
- LP concentration: if expedited queue > 70% post-WSH, inspector
  headcount is undersized
- LP SLA breach count: at the optimum, how many boards breach 60-min
  expedited SLA?
- LP inspector minute total: must be ≤ inspector_count × shift_hours
  × 60.

Acceptance criteria:
- ACCEPT: RL clears hard-floor + throughput floor; LP feasible,
  optimality gap < 5%, no HIGH-severity pathology, total $ cost within
  team budget.
- REVISE-AND-RESOLVE: pathology found that suggests Phase 11 constraint
  tweak. Re-run.
- REJECT-AND-REDESIGN: infeasible AND no soft fix; back to Phase 10/11.

Journal files:
- First pass: journal/phase_12_acceptance.md
- Re-run: journal/phase_12_postwsh.md (with quantified compliance
  shadow price in $/day)

CRITICAL: missing the post-WSH re-solve OR missing the
compliance-shadow-price quantification both score 0 on D3
(trade-off honesty).
```

## 5. Cost anchor

From `specs/business-costs.md`:

- **RL throughput recovery:** 2-3% × 40,000 boards/day × $60 = $48K-$72K/day pre-WSH
- **Compliance shadow price target estimate:** post-WSH typically loses some fraction of that throughput recovery as the agent shifts to recommend-only on safety-affecting setpoints — quantifying the actual $/day delta IS the Phase 12 post-WSH deliverable
- **Inspector minute cost:** $35/min × shadow-price slack on the binding queue constraint

## 6. Hard-floor table

From `specs/compliance-floors.md`:

| Floor                      | Phase 12 enforcement                                                 |
| -------------------------- | -------------------------------------------------------------------- |
| RL hard floors             | Auto-REJECT any policy with non-zero violations                      |
| WSH-affecting categories   | Post-WSH plan MUST have shadow on setpoint_adjustment + safety_alert |
| MOM mandate window 90 days | All re-solves during window must respect shadow envelope             |

## 7. Reversal condition

A Phase 12 ACCEPT is reversed when:

- **Signal**: live shadow data shows actual $/day exceeds the planned $ cost by > 25%
- **Threshold**: 25% delta sustained
- **Duration**: 3 consecutive shifts

Then re-open Phase 12 — the LP modelled an objective that doesn't match production, and either Phase 10 weights or Phase 11 classifications are wrong.

## 8. Transfer to next project

The acceptance pattern (feasibility + optimality gap + pathology + shadow price + accept/revise/redesign) is universal to any solver-driven decision system. The compliance shadow price quantification — explicit $/day delta from regulator action — is the structural defense against vague "compliance costs us something" claims. Anywhere a regulator's mandate fires mid-product, the same shape applies: re-classify (Phase 11), re-solve (Phase 12), quantify the $/day delta in writing.

---

**Next file:** Sprint 4 boot: [`workflow-06-sprint-4-agent-mlops-boot.md`](./workflow-06-sprint-4-agent-mlops-boot.md)
