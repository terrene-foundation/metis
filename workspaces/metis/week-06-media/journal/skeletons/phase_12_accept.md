# Phase 12 — Solver Acceptance (first pass, BEFORE IMDA injection)

**Sprint:** 3 · **Time:** **_:_** · **Artefact:** `journal/phase_12_accept.md`

## LP solve output

- Endpoint: POST /queue/solve, then GET /queue/last_plan
- Feasibility: \_\_\_ (FEASIBLE / INFEASIBLE)
- Optimality gap: \_\_\_%
- Total expected $ cost / day: $\_\_\_

## Per-tier × per-queue plan

| Tier                   | Expedited | Standard | Bulk   | Total  |
| ---------------------- | --------- | -------- | ------ | ------ |
| auto-allow             | \_\_\_    | \_\_\_   | \_\_\_ | \_\_\_ |
| low-confidence-allow   | \_\_\_    | \_\_\_   | \_\_\_ | \_\_\_ |
| mid-confidence-review  | \_\_\_    | \_\_\_   | \_\_\_ | \_\_\_ |
| high-confidence-review | \_\_\_    | \_\_\_   | \_\_\_ | \_\_\_ |
| auto-remove            | \_\_\_    | \_\_\_   | \_\_\_ | \_\_\_ |

## Pathology checks

- Concentration: any queue handling >70% of posts? \_\_\_
- Empty queues: any queue allocated zero? \_\_\_
- SLA breach count at optimum: \_\_\_ posts/day breach 90min SLA
- Reviewer-minute total: within `reviewer_count × shift_hours × 60`? \_\_\_

## Shadow prices on binding constraints

| Constraint         | Shadow price ($/unit) | What it means                            |
| ------------------ | --------------------- | ---------------------------------------- |
| Reviewer headcount | \_\_\_                | Marginal $ saved per added reviewer-hour |
| 90-min SLA         | \_\_\_                | Cost per minute of SLA softening         |

## Decision

**ACCEPT** / **REVISE-AND-RESOLVE** / **REJECT-AND-REDESIGN** — \_\_\_

## What I sacrificed (D3)

<Quantify. "Accepted plan with 4% SLA breach because tighter SLA would require 2 more reviewers ($X/day) for a $Y/day breach cost.">

## Reversal condition (D5)

<When does the plan need re-solving? "Daily — when ingest volume exceeds reviewer capacity by more than 10%, re-run /queue/solve.">
