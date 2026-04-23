<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

_[← Playbook index (README)](./README.md)_

## Phase 12 — Solver Acceptance (REPLACED for Optimization)

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ USML ✓ ▸ SML ✓ ▸ **Opt ◉** ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 3 · Phase 12 of 12 — Solver Acceptance
 LEVERS:        held-out choice · pathology detection · accept/retune/redesign · rollback readiness
──────────────────────────────────────────────────────────────────
```

### Concept

The solver runs. It returns a plan. You check: feasibility (every hard constraint satisfied), optimality (how close to the LP optimum), pathologies (one segment getting 90% of the plan, dead campaigns with zero allocation). Decide: accept, re-tune (change weights or penalties), fall back (demote a hard constraint), or redesign (the problem is ill-posed).

### Why it matters (Optimization lens — the DEPTH Week 4 skipped)

- **Feasibility first, optimality second.** An infeasible LP returns no plan. A feasible-but-pathological plan returns an unusable one. Both are failures; the diagnosis differs.
- **Optimality gap.** Distance from the LP optimum (or the LP relaxation upper bound for MIP). Gap > 5% → either tighten the solver or accept the sub-optimality with a reason.
- **Pathology detection.** Feasible plans can still be wrong: concentration (one output gets the whole plan), dead variables (unused campaigns / SKUs / routes), boundary cases (the solver chose an extreme corner of the polytope).
- **Sensitivity analysis.** How robust is the plan to small changes in the objective weights or constraint values? If weight_revenue = 0.95 gives plan A but weight_revenue = 0.93 gives plan B, your plan is fragile.

### Your levers this phase

- **Lever 1 (the big one): pathology detection.** Concentration (one segment > 60%), dead campaigns (0 allocation), boundary solutions (activity at 100% of budget when you expected 80%).
- **Lever 2 (the decision):** accept, re-tune, fall back, redesign. Don't default to accept; the solver being feasible is not the same as the plan being shippable.
- **Lever 3 (the rollback readiness):** the prior plan. Is the current plan better than the prior plan by the dollar lift you expected? If not, stay with the prior.
- **Lever 4 (the sensitivity):** perturb the weights by ±10% and re-solve. If the plan is stable, ship. If it flips, your decision is on a knife edge.

### Trust-plane question

Is the solution feasible, optimal, edge-case safe, and pathology-free?

### Paste this

```
I'm entering Playbook Phase 12 — Solver Acceptance. The scaffold
pre-committed to the LP solver behind /allocate/solve and the
last-plan persistence at data/allocator_last_plan.json per
src/retail/backend/routes/allocate.py; my decision here is
ACCEPT / RE-TUNE / FALL-BACK / REDESIGN on the solved plan,
checked for feasibility AND pathologies. I run this twice — once
with the first-pass constraints, once after the PDPA injection.

Copy journal/skeletons/phase_12_accept.md into
workspaces/metis/week-05-retail/journal/phase_12_accept.md.

Your job, first pass:

1. POST to /allocate/solve with the current Phase 10 objective
   and Phase 11 constraints. Save the response to
   data/allocator_last_plan.json (the endpoint does this
   automatically per allocate.py). Cite the solver function.

2. Report FEASIBILITY per hard constraint — which constraints are
   satisfied (e.g. "touch budget used: X of Y", "inventory: no
   SKU allocated beyond availability"). If any hard constraint
   is violated, the plan is infeasible and my disposition is
   REDESIGN or FALL-BACK.

3. Report the OPTIMALITY GAP — the distance from the LP optimum.
   If >5%, name it as a finding.

4. Check four PATHOLOGIES:
   (a) Concentration — is any segment getting >10% of the
       plan disproportionately? I set the threshold; you report
       the concentration percentage per segment.
   (b) Dead campaigns — any campaign with 0 allocation across
       all segments.
   (c) Boundary — any decision at 100% of a budget when I
       expected 80%.
   (d) Sensitivity — perturb weights by ±10% and re-solve.
       Does the top-concentration segment flip? Does a dead
       campaign come alive? Report the change in allocations.

5. Compute prior-plan comparison — if a prior /allocate/last_plan
   exists, what's the expected-revenue delta in dollars?
   Quote the $18 basket-lift and $14 wasted-impression rates
   from PRODUCT_BRIEF.md §2 verbatim for the calculation.

Do NOT propose pathology THRESHOLDS. The 10% concentration, the
5% optimality gap, the ±10% sensitivity band — I set those. Your
job is to report the measured values; I compare to my floors.
The point is pre-registered pathology floors, not post-hoc ones.

Do NOT decide ACCEPT / RE-TUNE / FALL-BACK / REDESIGN. That is my
call per pass. You recommend with rationale; I sign.

Post-injection re-run (when PDPA fires):

After phase_11_postpdpa.md is written, POST /allocate/solve AGAIN
with the new hard PDPA constraint. Save the new plan — the file
at data/allocator_last_plan.json MUST BE DIFFERENT from the
first-pass plan. If the file is byte-identical, the solver did
not pick up the new constraint and something is wrong.

Copy the skeleton into phase_12_postpdpa.md (do not overwrite
phase_12_accept.md). Report the same four pathologies. Compute
the SHADOW PRICE of the new hard PDPA constraint — "the dollar
revenue lost to compliance". Quote the $220 line from
PRODUCT_BRIEF.md §2 to anchor the shadow price in per-record
terms.

For every claim, cite the file and function. For every dollar
figure, quote §2. Do NOT invent.

Do NOT use "blocker" without the specific blocked ship-action.

When feasibility, gap, pathology report, and sensitivity are in
the journal, stop and wait for my disposition. When PDPA fires,
re-run and stop again.
```

### Why this prompt is written this way

- Inheritance-framed opening names the scaffold's solver and plan-persistence commitments and keeps the disposition with me — "feasible" is not the same as "shippable" and only I say so.
- Four pathologies are enumerated because Phase 12 checklist says all four must be checked; missing one is a 2/4 on D3.
- Forbidding pathology THRESHOLD proposals is the anti-post-hoc guard — the agent reporting "concentration 12% which is below the 15% threshold" post-hoc is exactly the failure Phase 6 pre-registration was supposed to prevent.
- The byte-identical-plan check is the disk-level proof that the PDPA re-solve actually fired — the #1 rubric trap of the night is writing `phase_12_postpdpa.md` while the solver never re-ran.
- Show-the-brief on $18 / $14 / $220 is required so expected-revenue delta and shadow-price claims are audit-traceable.

### What to expect back

- `journal/phase_12_accept.md` with feasibility per hard constraint + optimality gap + four-pathology report + ±10% sensitivity.
- Later: `journal/phase_12_postpdpa.md` after the injection, with a DIFFERENT `data/allocator_last_plan.json` and a quoted shadow price.
- Expected-revenue delta vs prior plan in dollars, sourced from §2 rates.
- A disposition RECOMMENDATION with rationale — not a decision.
- A stop signal pending my ACCEPT / RE-TUNE / FALL-BACK / REDESIGN call.

### Push back if you see

- A proposed pathology threshold ("concentration limit = 10%") — "please remove; I set pathology floors in my journal, not you."
- `phase_12_postpdpa.md` written but `data/allocator_last_plan.json` byte-identical to the first pass — "the solver didn't re-run; please re-POST `/allocate/solve` and confirm the plan file changed."
- A "feasible plan" claim without the four-pathology check — "did you check concentration, dead campaigns, boundary, and sensitivity? feasible alone is 1/4 on D3."
- Shadow price quoted without a $ unit — "shadow price of what, in dollars per what unit?"
- Disposition decided on my behalf ("I recommend accept, accepting the plan") — "please state disposition as a recommendation only; the sign is mine."

### Adapt for your next domain

- Change `/allocate/solve` and `data/allocator_last_plan.json` to your optimization endpoints and plan persistence.
- Change the four pathologies (concentration / dead / boundary / sensitivity) to your domain's pathology taxonomy.
- Change `$18 / $14 / $220` to your domain's §2-equivalent rates.
- Change `PDPA injection` to your domain's mid-sprint regulatory event.
- Keep the byte-identical-plan check as-is — it's domain-independent structural proof.

### Evaluation checklist

- [ ] Every hard constraint confirmed satisfied.
- [ ] Optimality gap reported numerically.
- [ ] Pathologies named (concentration, dead variables, boundary cases).
- [ ] Sensitivity checked (perturb ± 10%).
- [ ] Accept / re-tune / fall back / redesign decision defended.
- [ ] Post-injection re-run: `phase_12_postpdpa.md` on disk alongside `phase_12_accept.md`.

### Journal schema — universal

```
Phase 12 — Solver Acceptance
Feasibility per hard constraint: ____
Optimality gap: ____
Pathologies: ____
Sensitivity (± 10%): plan stable? ____
Decision: Accept / Re-tune / Fall back / Redesign
Reason: ____
Prior-plan comparison: expected lift = ____; actual lift = ____
What would make me re-design: ____
```

### Common failure modes

- Solver returns feasible but pathological plan (one segment 90%). Student accepts because "feasible" — 1/4 on D3.
- Optimality gap not surfaced (solver reports it; student doesn't read it).
- Sensitivity skipped — plan ships on a knife edge.
- Post-injection plan overwrites pre-injection (state corruption).

### Artefact

`POST /allocate/solve` response saved to `data/allocator_last_plan.json` + `journal/phase_12_accept.md` + `journal/phase_12_postpdpa.md`.

### Instructor pause point

- Show the 3-segment concentration plot. Ask: 70% of the plan in one segment — is this shippable?
- Demonstrate: perturb weight_revenue by 10%. Plan changes? By how much?
- Ask: PDPA re-solve shows $50K of shadow-price cost. Do we accept? What's the business defence?

### Transfer to your next project

1. Does my solver return **feasible** AND **pathology-free**? Did I check for concentration, dead variables, boundary solutions?
2. What is the optimality gap, and is it tight enough for the decision's dollar stakes?
3. Is my plan stable under ± 10% perturbation of the weights, or is it on a knife edge?

---

# SPRINT 4 — MLOPS · Monitor · Phase 13

---

