# Phase 11 — Constraints (first pass, pre-injection)

**Sprint:** 3 · **Time:** **_:_** · _(Prior version preserved; do NOT overwrite after PDPA injection — write `phase_11_postpdpa.md` instead.)_

## Hard constraints

| Rule                   | Regime / reason                    | Rationale                         |
| ---------------------- | ---------------------------------- | --------------------------------- |
| touch_budget_total     | contract: marketing ops ceiling    | $**_ per touch × _** max = budget |
| inventory_availability | physical: cannot ship out-of-stock | N/A (physical)                    |
| \_\_\_                 | \_\_\_                             | \_\_\_                            |

## Soft constraints (with $ penalty)

| Rule                    | Penalty per violation | Reason                 |
| ----------------------- | --------------------- | ---------------------- |
| max_touches_per_segment | $\_\_\_ per excess    | avoid customer fatigue |
| \_\_\_                  | \_\_\_                | \_\_\_                 |

## Classifications I'm unsure about

<List them. Ask instructor if needed.>

## Reversal condition (D5)

<What event would demote a hard to soft, or promote a soft to hard? "If Legal classifies the X rule, move to hard.">
