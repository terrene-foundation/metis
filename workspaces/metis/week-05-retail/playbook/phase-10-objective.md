<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 10 — Objective Function

> **What this phase does:** Define "good" for the LP allocator — which signals to maximise, in what combination, at what dollar weights — and show what each framing sacrifices before you pick one.
> **Why it exists:** Without a written objective, the solver optimises whatever it was last handed. The weights are a stakeholder decision, not a default.
> **You're here because:** Sprint 3 just booted (`workflow-05-sprint-3-opt-boot.md`). Phase 10 is the first decision of the optimisation sprint. Next is Phase 11 — Constraints.
> **Key concepts you'll see:** objective function, single-vs-multi-objective, shadow prices, Pareto frontier, coverage/diversity floors

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering Playbook Phase 10 — Objective Function. My decision
here is the OBJECTIVE WEIGHTS for this sprint's optimisation layer —
which signals to maximise, in what combination, and how to defend
each weight in dollars. I am NOT picking weight values yet; I am
choosing the shape and asking you to show me both framings.

Your job:

1. Name the 3–5 competing signals "good" means across this
   domain. For each signal, give the dollar rate from the
   project's cost source, verbatim. If you cannot find a rate,
   say so — do NOT invent numbers.

2. Draft BOTH framings side by side:
   (a) Single-objective: one weighted sum maximising the
       primary signal, with coverage and diversity moved to the
       constraint set (Phase 11). Show the formula in plain
       language before the math.
   (b) Multi-objective: separate scores on 2–3 signals with a
       Pareto frontier sketch. Name what the frontier means in
       terms a stakeholder can act on.

3. Compute the SHADOW PRICE for the two most important
   constraints. Shadow price = how much extra objective value
   per unit of constraint relaxation. Read it from a real solver
   run — do not estimate it by hand.

4. Recommend ONE framing with a reason. Name what the chosen
   framing sacrifices — there is no free lunch.

5. Do NOT set the weight values. Your job is the shape and the
   rationale; my job is the weight numbers.

6. Do NOT call any endpoint to POST new weights yet. Run the
   solver with current / default weights to expose the shadow
   prices, then stop.

Do NOT propose weight values (e.g. weight_revenue = 0.7).
Do NOT use "blocker" without naming the specific ship-action.

When framings, shadow prices, and sacrifices are drafted with
sourced dollar rates, stop and wait for my weight decision.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

```
Sprint 3 optimisation — LP allocator.
Journal file: copy journal/skeletons/phase_10_objective.md into
  workspaces/metis/week-05-retail/journal/phase_10_objective.md.
Scaffold endpoints: /allocate/objective (GET + POST),
  /allocate/campaigns, /allocate/solve per
  src/retail/backend/routes/allocate.py.

The four dollar rates to quote from PRODUCT_BRIEF.md §2 verbatim:
  - Expected revenue per converted click: $18 (basket lift row)
  - Wasted impression: $14 per session
  - Per-customer touch cost: $3 per contact
  - Cold-start session fallback: $8 per new-user session
If any rate is not in §2, say so; do NOT invent.

Competing signals for tonight's allocator:
  expected revenue, reach (customers touched), diversity
  (cross-segment coverage), touch spend. If you add a fifth
  (e.g. serendipity), name it as a PROXY for long-term revenue,
  not a direct objective term.

Single-objective formula tonight:
  max Σ x × (P(convert) × $18 − $14 × wasted − $3 × touches)
Show this in plain language before the math.

Shadow prices: compute for touch-budget constraint AND the PDPA
  under-18 constraint. Run /allocate/solve once, read the solver
  output, cite the function in src/retail/backend/routes/allocate.py.

Coverage and diversity belong in Phase 11 constraints, NOT in
  the objective. If you put them in the objective, they get
  sacrificed during optimisation — move them to Phase 11.

Do NOT POST to /allocate/objective until I give you the weight
  values. Running /allocate/solve with current defaults is fine.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ `journal/phase_10_objective.md` exists with 3–5 competing signals, each with a verbatim §2 dollar quote or an explicit "not in §2" note
- ✓ Both single-objective AND multi-objective framings drafted side by side — not just one
- ✓ Shadow prices for touch-budget and PDPA constraints, read from a real `/allocate/solve` run (not estimated)
- ✓ A recommended framing with the sacrifice explicitly named ("single-objective sacrifices explicit reach/diversity visibility")
- ✓ No weight values proposed — framing and rationale only
- ✓ Stop signal waiting for your weight decision
- ✓ Viewer (http://localhost:3000) shows: allocator objective panel with selected framing, dollar rates per term, and Pareto frontier sketch if multi-objective was chosen

**Signals of drift — push back if you see:**

- ✗ Viewer shows nothing new after CC reports the phase complete — CC may have described the objective without running the solver. Re-prompt: "show me the objective panel in the viewer; what does it display?"

- ✗ A weight value proposed ("weight_revenue = 0.7") — "please remove; I own the weight numbers, you own the framing"
- ✗ A dollar rate not quoted from §2 — "please quote the §2 row, or state it's not in §2"
- ✗ Only one framing (single OR multi, not both) — "please draft both; I need to see what each sacrifices"
- ✗ Shadow price stated without running the solver — "please run /allocate/solve first; shadow prices come from solver output"
- ✗ Coverage or diversity inside the objective formula — "coverage belongs in Phase 11 constraints, not Phase 10 objective; move it"
- ✗ A POST to /allocate/objective already made — "please revert; I set the weights"

---

## 3. Things you might not understand in this phase

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **Objective function** — the single formula the solver is trying to maximise (or minimise), which encodes what "good" means in numbers
- **Single-vs-multi-objective** — whether you combine all goals into one weighted sum or track them as separate scores with trade-offs between them
- **Shadow prices** — the dollar value of relaxing one constraint by one unit; the solver produces this automatically and it tells you what compliance costs
- **Pareto frontier** — the set of plans where you cannot improve one goal without worsening another; it's the honest picture of trade-offs for multi-objective problems
- **Coverage/diversity floors** — minimums on reach and variety that belong in the constraint set (Phase 11), NOT in the objective, because objectives get sacrificed during optimisation

---

## 4. Quick reference (30 sec, generic)

### Objective function

The formula the solver maximises. It has terms (revenue, reach, diversity) and weights (how much each term matters relative to the others). The weights are a business decision. The solver finds the plan that scores highest on the formula. If the formula is wrong — if it ignores reach, or sets a wrong weight — the solver will find the best possible bad plan with great confidence.

> **Deeper treatment:** [appendix/03-modeling/optimization-families.md](./appendix/03-modeling/optimization-families.md)

### Single-vs-multi-objective

Single-objective: one weighted sum, one score, one go/no-go number. Simpler to action but hides trade-offs inside the weights. Multi-objective: separate scores for each goal, a Pareto frontier showing where improving one requires worsening another. More honest, harder to action because you need to pick a point on the frontier. Tonight: default to single-objective with coverage/diversity as constraints unless stakeholders explicitly disagree on which goal matters most.

> **Deeper treatment:** [appendix/03-modeling/optimization-families.md](./appendix/03-modeling/optimization-families.md)

### Shadow prices

When the solver solves an LP, each constraint gets a shadow price: the improvement in the objective if that constraint were relaxed by one unit. If the touch-budget constraint has shadow price $12, adding one more touch to the budget would gain $12 of expected revenue. Shadow prices are free output from the solver — you don't estimate them, you read them. They are the honest answer to "what does compliance cost?" before the regulator injects a new constraint.

> **Deeper treatment:** [appendix/07-governance/shadow-prices.md](./appendix/07-governance/shadow-prices.md)

### Pareto frontier

The set of plans where you cannot improve one objective without worsening another. Every point on the frontier is "optimal" for some weighting of goals. Points inside the frontier are dominated — there is a better plan available. Presenting the frontier to a stakeholder is honest: "here are all the ways to be optimal; which point do you want?" Picking weights is equivalent to picking a point on the frontier — so the weight decision IS the business decision.

> **Deeper treatment:** [appendix/03-modeling/optimization-families.md](./appendix/03-modeling/optimization-families.md)

### Coverage/diversity floors

Minimum thresholds on how many customers are reached (coverage) and how many distinct segments or categories appear in the plan (diversity). These belong in the CONSTRAINT set, not the objective. If you put them in the objective, the solver treats them as trade-offs — it will sacrifice reach whenever revenue gains are larger. As constraints, they are floors the solver must always satisfy. Tonight: put coverage/diversity in Phase 11.

> **Deeper treatment:** [appendix/04-evaluation/coverage-and-diversity.md](./appendix/04-evaluation/coverage-and-diversity.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in Playbook
Phase 10 — Objective Function.

Read `workspaces/metis/week-05-retail/playbook/phase-10-objective.md` for
what this phase does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. shadow prices >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in Phase 10
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] `journal/phase_10_objective.md` exists with 3–5 competing signals, each §2-quoted or explicitly "not in §2"
- [ ] Both single-objective AND multi-objective framings present
- [ ] Shadow prices for touch-budget and PDPA constraints, from a real solver run
- [ ] Recommended framing named with sacrifice stated
- [ ] No weight values proposed — framing only
- [ ] No POST to /allocate/objective yet

**Next file:** [`phase-11-constraints.md`](./phase-11-constraints.md)

Phase 11 classifies each constraint as hard or soft and sets the penalty structure — including the PDPA rule that will be re-classified mid-sprint.
