<!-- Copyright (c) 2026 Terrene Foundation (Singapore CLG) — CC BY 4.0 -->

# Phase 11 — Constraint Classification (pre-WSH)

**Decision moment:** Which constraints are HARD, which SOFT, with the dollar penalty named?
**Sprint:** 3 (Queue + RL + Agent)
**Time:** 18:45
**Artefact produced:** `journal/phase_11_constraints.md`

## Five dimensions

- **D1 Harm framing** — misclassifying a hard constraint as soft = WSH breach + criminal liability. Penalty $1M+/incident.
- **D2 Metric → cost linkage** — hard constraint penalty = $1M+ (WSH); $50K (equipment); $4,200/board (FN). Soft constraint penalties are the LP optimisation objective, not floors.
- **D3 Trade-off honesty** — soft constraints (queue depth, throughput) trade off inside the LP. Hard constraints are non-optimisable.
- **D4 Constraint classification** — see specs/compliance-floors.md for the canonical table.
- **D5 Reversal condition** — regulator update → re-classify (about to fire mid-sprint, see post-WSH journal).

## Constraint table (pre-MOM mandate)

| Constraint                                                  | Class | Penalty                            | Source                  | Where enforced                         |
| ----------------------------------------------------------- | ----- | ---------------------------------- | ----------------------- | -------------------------------------- |
| Safety-critical-defect threshold ≥ 0.40                     | HARD  | $1M WSH ceiling                    | IPC-A-610 Cl. 3 + WSH   | `POST /inspect/vision/threshold`, `…/promote` |
| RL safety_penalty ≥ 0.50                                    | HARD  | floor that yields 0 violations     | empirical (cached)      | `POST /optimize/rl/reward_function`    |
| WSH-notifiable incident                                     | HARD  | $1,000,000+                        | WSH Act 2006            | `POST /agent/decide` (envelope check)  |
| Equipment damage envelope                                   | HARD  | $50,000/incident, 0/year           | Insurance policy        | RL hard floor                          |
| Restricted-zone access during operation                     | HARD  | 0 incursions                       | WSH Act 2006            | `POST /agent/decide`                   |
| RL line-speed ceiling 60 boards/min                         | SOFT (pre-MOM) | (becomes HARD post-MOM)   | MOM directive (pending) | `POST /optimize/rl/simulate` envelope  |
| RL reflow-zone temp ≤ 250 °C                                | SOFT (pre-MOM) | (becomes HARD post-MOM)   | MOM directive (pending) | `POST /optimize/rl/simulate` envelope  |
| Inspector head-count                                        | SOFT  | LP shadow price (~$120/min)        | operations              | `POST /queue/solve`                    |
| Tier mean review time                                       | SOFT  | LP weight                          | operations              | `POST /queue/solve`                    |
| Throughput target                                           | SOFT  | $48k-$72k/day recovery             | operations              | RL reward function                     |

## What I decided

Documented all 10 constraints with class + penalty + enforcement site. The two MOM-pending soft constraints (line-speed 60 / reflow-temp 250) are flagged as "soft pre-MOM, becomes HARD post-MOM" — the Phase 11 post-WSH re-run will reclassify them when the mandate fires.

## Why

Hard constraints have non-optimisable penalty; soft constraints trade off inside the optimiser. The LP at Phase 10 only optimises the soft constraints; the hard floors are rejection gates at the API boundary (verified at /redteam: threshold POST below floor → 409, RL safety_penalty below floor → 422, agent policy on WSH-affecting class non-shadow during MOM → 422).

## What I rejected

"Treat $50K equipment as a soft penalty" — would let the optimiser trade equipment damage against throughput, structurally unsafe. "Treat WSH as a fineable cost term" — treating a $1M ceiling as marginal cost ignores criminal liability for directors.

## Reversal condition

MOM/WSH directive change → re-classify (this fires next; see `journal/phase_11_postwsh.md`).

## Risks I am accepting

Some soft constraints may need to harden as the line scales (e.g. inspector head-count becomes hard if hiring freezes). Q4 ramp may temporarily relax the mean-review-time soft constraint (operations team takes longer); revisit at Phase 13.
