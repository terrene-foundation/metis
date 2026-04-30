# Phase 11 — Constraints (POST-IMDA RE-RUN)

**Sprint:** 3 · **Time:** **_:_** (injection fired at **_:_**) · **Do NOT overwrite `phase_11_constraints.md`**

## What changed

<Named rule: e.g. "csam_adjacent threshold: reclassified from soft (cost-balanced 0.85) to HARD (regulator-mandated 0.40 + 60s human-review SLA on the expedited queue).">

## New hard constraints

| Rule                                       | Regime / reason         | Reason (specific clause)                          |
| ------------------------------------------ | ----------------------- | ------------------------------------------------- |
| csam_adjacent ≤ 0.40 auto-remove threshold | IMDA Online Safety Code | Mandatory floor; $1M per incident regulator fine  |
| 60s mandatory-human-review on expedited    | IMDA mandate            | Mandatory routing window for csam_adjacent > 0.40 |
| \_\_\_                                     | \_\_\_                  | \_\_\_                                            |

## Soft constraints removed or modified

<If any. The cost-balanced csam_adjacent threshold no longer fires — the HARD floor governs.>

## Shadow price of the new hard constraint (D1)

<Cost of compliance in dollars, computed in Phase 12 re-solve. "IMDA hard adds $\_\_\_/day in expected cost vs pre-injection plan, mostly through expedited queue load shift and reviewer-minute increase.">

## Re-justification (D4)

<Why the new classification is correct. Cite the regime. "IMDA Online Safety Code §X imposes a $1M per-incident penalty on non-takedown of CSAM-adjacent content. Even at a 0.001% violation rate, this exceeds the entire cost-balanced soft-constraint budget by orders of magnitude. The regulator wins; the LP must respect it as hard.">

## Reversal condition (D5)

<When would this re-classify back? "Not without an amendment to the IMDA Online Safety Code. Even then, the regulator's clarification would have to revise the 0.40 floor explicitly.">
