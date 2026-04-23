<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 12 — Solver Acceptance

> **What this phase does:** Run the solver, check that the plan is feasible AND pathology-free, and make one of four dispositions: accept, re-tune, fall back, or redesign. Run this twice if the PDPA injection has fired.
> **Why it exists:** A feasible plan is not the same as a shippable plan. Concentration, dead campaigns, and boundary solutions are plan failures the solver won't flag on its own.
> **You're here because:** Phase 11 set the constraints (`phase-11-constraints.md`). The solver can now run. If the PDPA injection fired, Phase 12 runs again after `phase_11_postpdpa.md` is written.
> **Key concepts you'll see:** feasibility vs optimality, optimality gap, solver pathologies (concentration, dead campaigns), accept/retune/fall-back/redesign, PDPA re-solve discipline

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering Playbook Phase 12 — Solver Acceptance. My decision
here is ACCEPT / RE-TUNE / FALL-BACK / REDESIGN on the solved
plan. I check feasibility first, then pathologies, then make a
disposition. I am NOT deciding in advance — I wait for the data.

Your job:

1. Run the solver with the current Phase 10 objective and Phase 11
   constraints. Save the response to the plan persistence file.
   Cite the solver function.

2. Report FEASIBILITY per hard constraint — name each hard
   constraint and report whether the solved plan satisfies it
   (e.g. "touch budget used: X of Y", "inventory: no SKU over
   availability"). If any hard constraint is violated, the plan
   is infeasible — my disposition is REDESIGN or FALL-BACK.

3. Report the OPTIMALITY GAP — the distance from the LP optimum.
   If > 5%, name it as a finding. Quote the solver's reported gap,
   not an estimate.

4. Check four PATHOLOGIES:
   (a) Concentration — report the percentage of the plan going
       to the top segment or output. I set the threshold; you
       report the measured value.
   (b) Dead variables — any campaign, SKU, or route with zero
       allocation across all outputs.
   (c) Boundary — any decision at 100% of a budget when 80% was
       expected.
   (d) Sensitivity — perturb the objective weights by ±10% and
       re-solve. Does the top-concentration output flip? Does a
       dead variable come alive? Report the change.

5. Compute a prior-plan comparison — if a prior plan exists in
   the persistence file, what is the expected-revenue delta in
   dollars? Use only sourced dollar rates for the calculation.

6. Recommend ACCEPT / RE-TUNE / FALL-BACK / REDESIGN with a
   rationale. Do NOT decide on my behalf — recommend only.

Do NOT propose pathology thresholds. The concentration cutoff,
gap cutoff, and sensitivity band are mine to set. You report
the measured values; I compare to my pre-registered floors.

Do NOT use "blocker" without naming the specific ship-action.

Post-injection re-run (when the regulatory event has fired):

After the post-injection Phase 11 journal file is written, run
the solver AGAIN with the new hard constraint applied. Save the
new plan to the persistence file. The plan MUST be different from
the first-pass plan — if the file is byte-identical, the solver
did not pick up the new constraint.

Copy the acceptance skeleton into a new post-injection journal
file (e.g. phase_12_postpdpa.md). Run the same four-pathology
check. Compute the SHADOW PRICE of the new hard constraint in
dollars per unit of relaxation.

Do NOT overwrite the first-pass journal file — both must exist.

When feasibility, gap, pathology report, and sensitivity are in
the journal, stop and wait for my disposition. When the injection
fires, re-run and stop again.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

_First pass (pre-injection):_

```
Journal file: copy journal/skeletons/phase_12_accept.md into
  workspaces/metis/week-05-retail/journal/phase_12_accept.md.
Solver endpoint: POST /allocate/solve per
  src/retail/backend/routes/allocate.py.
Plan persistence: data/allocator_last_plan.json (the endpoint
  writes this automatically — cite the function).

Dollar rates for prior-plan comparison — quote verbatim from
PRODUCT_BRIEF.md §2:
  - $18 basket lift per converted click
  - $14 wasted impression per session

Four pathologies for tonight's allocator:
  (a) Concentration: report % of plan going to top segment.
  (b) Dead campaigns: any campaign with 0 allocation across
      all segments.
  (c) Boundary: any decision at 100% of touch budget or
      inventory cap.
  (d) Sensitivity: perturb objective weights ±10%, re-solve,
      report which segment changes concentration most.

Do NOT propose thresholds (e.g. "concentration limit = 10%").
I set those in my journal. You report measured values.

Do NOT decide ACCEPT / RE-TUNE / FALL-BACK / REDESIGN on my
behalf. You recommend; I sign.
```

_Post-injection re-run (when PDPA fires):_

```
When phase_11_postpdpa.md is written:
  - POST /allocate/solve AGAIN with the new hard PDPA constraint.
  - The file data/allocator_last_plan.json MUST be different from
    the first-pass plan. If byte-identical, the solver did not
    pick up the new constraint — do NOT proceed; flag this.
  - Copy skeleton into:
    workspaces/metis/week-05-retail/journal/phase_12_postpdpa.md
    Do NOT overwrite phase_12_accept.md — both must exist.
  - Run the same four-pathology check on the new plan.
  - Compute the SHADOW PRICE of the PDPA hard constraint:
    "dollar revenue lost to compliance." Quote the $220 per
    under-18 record from PRODUCT_BRIEF.md §2 verbatim to anchor
    the shadow price in per-record terms.
  - The single most common D3 rubric failure tonight is writing
    phase_11_postpdpa.md but NOT re-solving here. Writing
    phase_12_postpdpa.md with a byte-identical plan is the same
    failure. Both journal files on disk + a different plan file
    = the rubric check passes.
```

**How to paste:** Use the universal core plus the first-pass block now. Keep the post-injection block ready for when the PDPA injection fires.

---

## 2. Signals the output is on track

**Signals of success (first pass):**

- ✓ `journal/phase_12_accept.md` exists with feasibility confirmed per hard constraint, optimality gap quoted from solver output, and all four pathologies checked
- ✓ Concentration, dead campaigns, boundary, and sensitivity all reported as measured values — not thresholds, not estimates
- ✓ Sensitivity: solver actually re-ran with ±10% perturbed weights; results show whether plan is stable or fragile
- ✓ Prior-plan revenue delta computed with §2-quoted dollar rates ($18 basket lift, $14 wasted impression)
- ✓ A disposition RECOMMENDATION with rationale — not a decision signed on your behalf
- ✓ Stop signal waiting for your ACCEPT / RE-TUNE / FALL-BACK / REDESIGN call
- ✓ Viewer (http://localhost:3000) shows: allocator plan panel with feasibility status, solved plan (campaigns × segments grid), and pathology warnings if any

**Signals of success (post-injection):**

- ✓ `journal/phase_12_postpdpa.md` exists alongside `journal/phase_12_accept.md` — both present
- ✓ `data/allocator_last_plan.json` is visibly different from the first-pass plan (different allocations, confirmed by the solver re-run)
- ✓ PDPA shadow price computed in dollars per unit of relaxation, anchored to the $220 §2 quote
- ✓ Same four-pathology check run on the post-injection plan
- ✓ Viewer (http://localhost:3000) shows: the allocator plan panel VISIBLY CHANGED vs the first-pass view — different segment concentrations, the shadow price of PDPA constraint shown in dollars

**Signals of drift — push back if you see:**

- ✗ A proposed pathology threshold ("concentration limit = 10%") — "please remove; I set pathology floors, you report measured values"
- ✗ `phase_12_postpdpa.md` written but `data/allocator_last_plan.json` byte-identical to the first pass — "the solver didn't re-run under the new hard constraint; please re-POST /allocate/solve and confirm the plan file changed"
- ✗ A "feasible plan" claim without the four-pathology check — "did you check concentration, dead campaigns, boundary, and sensitivity? feasible alone is not enough"
- ✗ Shadow price quoted without a dollar unit — "shadow price of what, in dollars per what unit?"
- ✗ Disposition decided on your behalf ("accepting the plan") — "please state this as a recommendation only; the disposition signature is mine"
- ✗ Viewer plan panel unchanged after the PDPA re-solve — the most critical viewer check: if the panel didn't change, the solver didn't re-run. Re-prompt: "show me the plan panel before and after the PDPA re-solve; are they different?"

---

## 3. Things you might not understand in this phase

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **Feasibility vs optimality** — two separate checks: feasibility means no hard constraint is violated; optimality means how close to the best possible plan given the constraints
- **Optimality gap** — the distance between the solver's solution and the theoretical LP optimum; if this is large, either the solver needs more time or the problem is harder than expected
- **Solver pathologies (concentration, dead campaigns)** — plan failures that are feasible but unusable: all budget goes to one output, or some outputs get nothing despite being in the campaign list
- **Accept/retune/fall-back/redesign** — the four dispositions; only one means the plan ships as-is; the others trigger changes before the plan is used
- **PDPA re-solve discipline** — the requirement that Phase 12 re-run after Phase 11 PDPA re-classification, producing a different plan; without this, the constraint change is documented but not enforced

---

## 4. Quick reference (30 sec, generic)

### Feasibility vs optimality

Feasibility: the solver found a plan where every hard constraint is satisfied. Optimality: the plan is as good as it can be given those constraints (or close to it). You need both. An infeasible solver returns nothing. A feasible-but-suboptimal solver returns a plan that works but wastes budget. Tonight's check order: feasibility first (hard constraints satisfied?), then optimality gap (how much better could the plan be?), then pathologies (is the plan concentrating on one segment?).

> **Deeper treatment:** [appendix/03-modeling/optimization-families.md](./appendix/03-modeling/optimization-families.md)

### Optimality gap

The percentage difference between the solver's solution and the LP relaxation upper bound. A 2% gap means the solver's plan is within 2% of the best possible outcome — acceptable. A 15% gap means the solver gave up early or the problem is hard — dig into why. The solver reports this number; you don't compute it by hand. If the gap is large, the options are: give the solver more time, relax a constraint, or accept the sub-optimality with a written reason.

> **Deeper treatment:** [appendix/03-modeling/optimization-families.md](./appendix/03-modeling/optimization-families.md)

### Solver pathologies (concentration, dead campaigns)

Concentration: one segment gets a disproportionate share of the plan. If segment A gets 85% of all campaign touches, the other segments are effectively invisible — that's a product failure even if the plan is feasible. Dead campaigns: some campaigns have zero allocation across all segments — they are in the list but the solver chose not to use them. Boundary: a decision is at 100% of a budget when you expected the solver to use 70–80% — usually means a binding constraint is hiding an assumption. Sensitivity: perturb the weights slightly and see if the plan changes dramatically — if it does, the plan is on a knife edge.

> **Deeper treatment:** [appendix/03-modeling/optimization-families.md](./appendix/03-modeling/optimization-families.md)

### Accept/retune/fall-back/redesign

Four dispositions. Accept: feasible, no pathologies, sensitivity stable — ship it. Re-tune: feasible but pathological or knife-edge — adjust objective weights or soft-constraint penalties and re-solve (stay in Phase 12). Fall back: infeasible under current hard constraints — demote one hard constraint to soft (back to Phase 11, then re-run Phase 12). Redesign: the problem as framed has no workable solution — return to Phase 10 and reframe the objective. Each disposition has a different next action; the disposition is yours to sign, not the agent's.

> **Deeper treatment:** [appendix/05-deployment/deployment-gate.md](./appendix/05-deployment/deployment-gate.md)

### PDPA re-solve discipline

When Phase 11 reclassifies the under-18 PDPA rule from soft to hard, Phase 12 must re-run the solver under the new constraint. The plan file must change — the PDPA hard constraint removes some campaigns or allocations that were previously allowed. The post-injection journal (`phase_12_postpdpa.md`) is the audit record; the changed plan file is the proof. If the plan file is byte-identical after the re-solve, the new constraint was not passed to the solver — the compliance change is documented but not enforced. This is the single most common D3 rubric failure tonight.

> **Deeper treatment:** [appendix/07-governance/pdpa-basics.md](./appendix/07-governance/pdpa-basics.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in Playbook
Phase 12 — Solver Acceptance.

Read `workspaces/metis/week-05-retail/playbook/phase-12-acceptance.md` for
what this phase does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. PDPA re-solve discipline >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in Phase 12
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] `journal/phase_12_accept.md` exists: feasibility per hard constraint, optimality gap, all four pathologies, sensitivity result, and a disposition recommendation
- [ ] Dollar rates quoted from `PRODUCT_BRIEF.md §2` for the prior-plan revenue comparison
- [ ] You signed your ACCEPT / RE-TUNE / FALL-BACK / REDESIGN disposition — not the agent's
- [ ] If PDPA injection has fired: `journal/phase_12_postpdpa.md` also exists, `data/allocator_last_plan.json` is confirmed different from first-pass plan, and PDPA shadow price is quoted in dollars
- [ ] Viewer plan panel changed between first-pass and PDPA re-run (if injection fired)

**Next file:** [`workflow-06-sprint-4-mlops-boot.md`](./workflow-06-sprint-4-mlops-boot.md)

Sprint 3 is complete. Sprint 4 (MLOps — drift monitoring) boots next. If PDPA injection fired and Phase 12 post-injection is not yet done, complete it before moving to the workflow.
