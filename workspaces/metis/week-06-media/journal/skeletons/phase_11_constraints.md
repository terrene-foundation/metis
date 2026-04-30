# Phase 11 — Constraints (first pass, BEFORE IMDA injection)

**Sprint:** 3 · **Time:** **_:_** · **Artefact:** `journal/phase_11_constraints.md` (DO NOT overwrite when post-IMDA fires — that's a separate file)

## Hard constraints

| Rule                           | Reason (regime)     | Penalty                   |
| ------------------------------ | ------------------- | ------------------------- |
| Reviewer headcount cap         | physics             | LP infeasible if violated |
| Per-reviewer max-shift 8hr     | labour law          | LP infeasible if violated |
| Auto-remove decision auditable | legal (audit trail) | LP infeasible if violated |
| \_\_\_                         | \_\_\_              | \_\_\_                    |

## Soft constraints

| Rule                            | $ penalty per unit violated | Justification (D4)                   |
| ------------------------------- | --------------------------- | ------------------------------------ |
| 90-min SLA on standard queue    | $\_\_\_/min late            | Creator-trust + appeal-handling cost |
| Per-tier balance (fairness)     | $\_\_\_/imbalance unit      | Reviewer fatigue / morale            |
| Cold-start default to expedited | $\_\_\_/cold-start case     | Operational pref                     |
| \_\_\_                          | \_\_\_                      | \_\_\_                               |

## PENDING — re-classified post-IMDA

- `csam_adjacent` threshold: currently SOFT cost-balanced (e.g. 0.85). After IMDA fires, becomes HARD with regulator-mandated 0.40 + 60s human-review SLA.

## Endpoint call

- POST /queue/constraints with the classified set above

## Reversal condition per soft constraint (D5)

<For each soft constraint: signal + threshold + duration that would re-classify it as hard or change its penalty. "If creator-appeal volume exceeds N appeals/week for 4 consecutive weeks, raise SLA penalty from $X to $Y/min.">
