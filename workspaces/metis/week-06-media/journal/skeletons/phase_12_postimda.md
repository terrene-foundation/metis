# Phase 12 — Solver Acceptance (POST-IMDA RE-SOLVE)

**Sprint:** 3 · **Time:** **_:_** (injection fired at **_:_**) · **Do NOT overwrite `phase_12_accept.md`**

> Skipping this re-solve OR skipping the compliance-cost quantification = 0 on rubric D3.

## Re-solve output

- Endpoint: POST /queue/solve (with hardened constraint set from `phase_11_postimda.md`), then GET /queue/last_plan
- Feasibility: \_\_\_
- Optimality gap: \_\_\_%
- Total expected $ cost / day: $\_\_\_

## Compliance cost (D1, D3 — required)

- Pre-IMDA total cost: $\_\_\_/day (from `phase_12_accept.md`)
- Post-IMDA total cost: $\_\_\_/day (this run)
- **Compliance cost = post − pre = $\_\_\_/day** ← THIS IS THE QUANTIFIED DOLLAR COST OF REGULATOR ACTION
- Annualised compliance cost: $\_\_\_/year

## What changed in the plan (visible delta)

- Expedited queue load: pre-IMDA \_\_\_ posts/day → post-IMDA \_\_\_ posts/day (Δ = \_\_\_)
- Standard queue load: pre-IMDA \_\_\_ → post-IMDA \_\_\_ (Δ = \_\_\_)
- SLA breach count: pre-IMDA \_\_\_ → post-IMDA \_\_\_

## Pathology checks (post-IMDA)

- Expedited queue concentration: any over-load? \_\_\_
- Reviewer-minute total: still within headcount? \_\_\_ (if not — INFEASIBLE; need expansion)
- Cold-start handling under new csam_adjacent ≤ 0.40 floor: \_\_\_

## Shadow price on the IMDA hard constraint

- Marginal $ cost per additional unit of csam_adjacent floor tightening: $\_\_\_

## Decision

**ACCEPT** / **REVISE-AND-RESOLVE** / **REJECT-AND-REDESIGN** — \_\_\_

## What I sacrificed (D3 — compliance is the sacrifice; quantify it)

<"Accepted post-IMDA plan with $X/day compliance cost ($Y/year) because the regulator alternative ($1M per incident) is structurally larger by orders of magnitude.">

## Reversal condition (D5)

<When does the post-IMDA plan need revising? "If reviewer headcount drops below N during a peak event, re-run with an expanded expedited capacity request to Reviewer Ops Lead.">
