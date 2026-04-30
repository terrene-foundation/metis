<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 12 — Solver Acceptance (LP plan acceptance)

> **What this phase does:** Solve the LP with the Phase 10 objective + Phase 11 constraints. Accept or reject the plan based on feasibility, optimality gap, and pathology checks. Re-run after IMDA injection.
> **Why it exists:** A solver returns a plan but doesn't tell you if it's a good plan. Phase 12 is the human acceptance gate — feasibility check, pathology check, sign-off. Skipping the post-IMDA re-solve scores 0 on D3.
> **You're here because:** Phases 10 and 11 set up the LP. Phase 12 runs it and decides accept/redo.
> **Key concepts you'll see:** feasibility, optimality gap, pathology, accept/redo, post-IMDA re-solve

---

## 1. Paste this into Claude Code

**Universal core:**

```
I'm in Playbook Phase 12 — Solver Acceptance. POST /queue/solve and read
the result. Produce an acceptance memo:

1. Feasibility: did the LP find a feasible plan? If INFEASIBLE, which
   hard constraint is over-tight?
2. Optimality gap: how far is the plan from the LP's lower bound?
3. Pathology checks:
   - Concentration: is one queue handling 95% of posts?
   - Empty queues: is any queue allocated zero posts?
   - SLA violations: how many soft-SLA breaches at the optimum?
   - Reviewer overload: are reviewer-minute totals within headcount?
4. Total expected $ cost: sum of all four objective terms at the plan
5. Shadow prices on the binding constraints

Then: ACCEPT, REVISE-AND-RESOLVE, or REJECT-AND-REDESIGN.

Do NOT auto-accept — I sign.
Do NOT use "blocker" without specifics.
```

**Tonight-specific additions** (Week 6 MosaicHub):

```
Endpoint:
- POST /queue/solve to run; GET /queue/last_plan to read result.

First pass (BEFORE IMDA injection):
- Expected: feasible plan with cost-balanced csam_adjacent, no expedited-
  queue overload, SLA breaches in soft-acceptable range.
- Total $ cost: state at the plan.
- Shadow prices: which constraint is binding? Reviewer headcount or SLA?

Post-IMDA injection (~4:30pm):
- Re-solve: POST /queue/solve again. The plan MUST change visibly:
  expedited queue load increases (csam_adjacent now hard-routed to it),
  SLA shadow price likely shifts.
- Total $ cost should INCREASE (compliance cost is non-zero).
- Quantify the compliance cost: $/day delta = post-IMDA cost - pre-IMDA cost.
  This IS the regulator-imposed cost in real dollars.
- Save second pass as journal/phase_12_postimda.md.
- The first pass STAYS in journal/phase_12_accept.md — do NOT overwrite.

Pathology checks (specific):
- Concentration: if expedited queue receives >70% of posts post-IMDA,
  that's a finding — reviewer headcount may be undersized for compliance.
- Empty queues: if standard queue receives <5% of posts, the tier
  classification may be off.
- SLA breach count: at the optimum, how many posts breach 90min SLA?
- Reviewer minute total: must be ≤ reviewer_count × shift_hours × 60.

Acceptance:
- ACCEPT: feasible, optimality gap < 5%, no HIGH-severity pathology,
  total $ cost within team budget.
- REVISE-AND-RESOLVE: pathology found that suggests Phase 11 constraint
  tweak. Re-run.
- REJECT-AND-REDESIGN: infeasible AND no soft fix; back to Phase 10/11.

Journal files:
- First pass: journal/phase_12_accept.md
- Re-run: journal/phase_12_postimda.md (with quantified compliance cost
  in $/day)

CRITICAL: missing the post-IMDA re-solve OR missing the compliance-cost
quantification both score 0 on D3 (trade-off honesty).
```

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ First-pass: feasible plan, optimality gap, pathology checks, total $ cost, shadow prices
- ✓ ACCEPT/REVISE/REJECT decision made
- ✓ Post-IMDA re-solve: plan visibly changes, total $ cost increases
- ✓ Compliance cost quantified ($/day delta)
- ✓ Both `phase_12_accept.md` and `phase_12_postimda.md` exist
- ✓ Stop signal pending session close

**Signals of drift — push back if you see:**

- ✗ Auto-accept without my sign-off
- ✗ Post-IMDA re-solve skipped — ask "didn't IMDA fire? where's the re-solve?"
- ✗ Compliance cost not quantified — ask "$/day delta from regulator action?"
- ✗ Post-IMDA file overwriting first-pass — ask for both
- ✗ Pathologies waved away as "minor" without quantification

---

## 3. Things you might not understand in this phase

- **Feasibility** — does a plan exist that satisfies all hard constraints?
- **Optimality gap** — how far is the returned plan from the proven minimum?
- **Pathology** — operationally bad plans that are technically feasible
- **Accept / revise / redesign** — the three outcome levels
- **Post-IMDA re-solve** — running the LP again with the hardened constraint, quantifying compliance cost

---

## 4. Quick reference (30 sec, generic)

### Feasibility

A plan exists that satisfies all hard constraints. INFEASIBLE means: no plan exists. Recovery: identify the over-tight hard constraint and either soften it (Phase 11 revision) or add resources (more reviewers). Most workshop infeasibility comes from over-classifying hard.

> **Deeper treatment:** [appendix/03-modeling/recommender-families.md](./appendix/03-modeling/recommender-families.md)

### Optimality gap

(plan_cost − LP_lower_bound) / LP_lower_bound. Gap < 5% = good plan. Gap > 20% = the solver gave up early or the LP is poorly conditioned. The solver reports gap; if it doesn't, ask why.

> **Deeper treatment:** [appendix/03-modeling/recommender-families.md](./appendix/03-modeling/recommender-families.md)

### Pathology

Operationally bad plans that are technically feasible. Concentration (one queue gets 95%), empty queues, reviewer overload, geographic absurdity. Pathologies signal that the objective + constraints don't fully capture business intent. Tonight's most likely pathology: post-IMDA expedited queue overload.

> **Deeper treatment:** [appendix/03-modeling/recommender-families.md](./appendix/03-modeling/recommender-families.md)

### Accept / revise / redesign

ACCEPT: ship the plan. REVISE-AND-RESOLVE: tweak Phase 11 constraints (e.g. soften an over-tight one) and re-solve. REJECT-AND-REDESIGN: the LP shape is wrong; back to Phase 10. Most Phase 12 outcomes are ACCEPT (with pathology notes) or REVISE; REDESIGN is rare.

> **Deeper treatment:** [appendix/05-deployment/deployment-gate.md](./appendix/05-deployment/deployment-gate.md)

### Post-IMDA re-solve

After the IMDA injection, the constraint set tightens (csam_adjacent → hard, 60s SLA → hard on expedited queue). Re-running /queue/solve produces a new plan; total $ cost increases (this is the compliance cost). Quantifying $/day delta is the rubric D3 deliverable. Skipping the re-solve is the most common D3 zero of Sprint 3.

> **Deeper treatment:** [appendix/07-governance/shadow-prices.md](./appendix/07-governance/shadow-prices.md)

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 6 Phase 12.

Read the phase file and `workspaces/metis/week-06-media/journal/phase_12_*.md`.

Explain "<<< FILL IN: concept name >>>" — plain language, MosaicHub-grounded,
implications for Phase 12 acceptance, what to push back on. Under 400 words.
```

---

## 6. Gate / next

- [ ] First-pass: feasibility, optimality gap, pathology checks, $ cost, shadow prices
- [ ] ACCEPT/REVISE/REJECT decision
- [ ] Post-IMDA re-solve produced visible plan change
- [ ] Compliance cost quantified ($/day delta)
- [ ] Both `phase_12_accept.md` and `phase_12_postimda.md` exist

**Next file:** Sprint 4 boot: [`workflow-06-sprint-4-mlops-boot.md`](./workflow-06-sprint-4-mlops-boot.md)
