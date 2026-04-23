<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 5 — Sprint 3 Optimization Boot (LP allocator + PDPA injection)

> **What this step does:** Boot Sprint 3 by copying five skeleton files (including two held in reserve for the PDPA injection), confirming the allocator endpoint live, and orienting Claude Code on both the LP paradigm and the mandatory mid-sprint re-run sequence.
> **Why it exists:** Sprint 3 has a built-in surprise — the PDPA injection fires mid-sprint and requires two re-runs, not one. A boot that doesn't name this produces a student who completes the Phase 11 journal and ships without re-solving the LP, which is the top-scoring rubric failure of the night.
> **You're here because:** Phase 8 (Sprint 2 deployment gate) was signed. Sprint 2 SML is complete.
> **Key concepts you'll see:** LP allocator, hard vs soft constraint, PDPA injection sequence, pathology detection, shadow price

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering an optimization sprint. The scaffold pre-wires a solver that
consumes prior sprint outputs (segments and classifier probabilities) and
returns a plan. Someone committed to the objective shape on my behalf. My
job this sprint is to set the objective weights, classify every constraint
as hard or soft, then sign or reject the solved plan.

This sprint replaces several Playbook phases with optimization equivalents:
- Objective phase (single vs multi objective, shadow prices)
- Constraints phase (hard / soft + dollar penalties)
- Solver Acceptance phase (feasibility, optimality gap, pathology detection)
The acceptance question in an optimization sprint is not "is accuracy high"
but "is the plan feasible and pathology-free".

Before I start the phase walk:

1. Copy the sprint skeletons from journal/skeletons/ into journal/ —
   including files held in reserve for any regulatory re-run sequence.
   Leave blanks blank; I fill them when the relevant event fires.

2. Confirm the sprint endpoint is live. If not live, STOP and raise a hand.

3. For every objective term, constraint, or solver concept you name
   (shadow price, slack variable, feasibility), cite the file and function
   in the codebase that implements it. If you cannot cite, say so.

4. For every dollar figure, quote the exact line from the project's cost source.

5. Do NOT propose objective weights, penalty values, or the hard/soft
   classification for any constraint. Those are my calls in the phase
   journals.

6. Do NOT use the word "blocker" without naming a specific action.

Once skeletons are copied and endpoints confirmed, summarise: (a) the
phases of this sprint and the single Trust Plane decision each owns,
(b) the pathologies the acceptance phase detects, (c) the exact sequence
for any regulatory injection that may fire mid-sprint.

Then stop and wait for my first optimization phase prompt.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

```
Sprint: Sprint 3 Opt — LP allocator.
Phases covered: Phase 10 (Objective), Phase 11 (Constraints), Phase 12
(Solver Acceptance). Plus the PDPA re-runs of Phase 11 and Phase 12.

Skeleton copy — FIVE files:
- phase_10_objective.md
- phase_11_constraints.md
- phase_11_postpdpa.md  ← held in reserve; fill when injection fires
- phase_12_accept.md
- phase_12_postpdpa.md  ← held in reserve; fill when injection fires
Source: journal/skeletons/. See journal/skeletons/README.md.
The two postpdpa files exist from the start; they are NOT optional.

Endpoint check (GET only):
- /allocate/campaigns → should return 5 campaigns
If not live, STOP and raise a hand.

For every objective term, constraint, or solver concept named (shadow price,
slack variable, Pareto frontier, feasibility), cite the file and function
in src/retail/backend/. If you cannot cite, say so.

Dollar figures for Sprint 3 — all from PRODUCT_BRIEF.md §2. Quote the line:
$18 basket lift per converted click, $14 per wasted impression, $45 per
wrong-segment customer, $3 per touch, $220 per under-18 PDPA exposure,
$8 per cold-start session.

Do NOT propose objective weights, penalty values, or the hard/soft
classification for any constraint.

PDPA injection — CRITICAL:
At roughly 4:30 tonight (~T+02:30), the instructor fires a PDPA injection.
Legal classifies under-18 browsing history as a PDPA §13 hard exclusion.
When this fires, the mandatory sequence is:
  1. Re-classify in Phase 11 → write phase_11_postpdpa.md
     (quote the $220/record line from PRODUCT_BRIEF.md §2)
  2. Re-solve the LP → write phase_12_postpdpa.md
     (the shadow price is the dollar cost of compliance)
  3. Confirm data/allocator_last_plan.json has changed on disk

Writing only phase_11_postpdpa.md without re-solving the LP is the single
most common D3 rubric failure tonight. Do NOT let me ship without step 2.

Summary must name: (a) three phases and their Trust Plane decisions,
(b) four pathologies Phase 12 detects (concentration, dead campaigns,
boundary cases, sensitivity flip), (c) the exact PDPA sequence above.

Then stop and wait for my Phase 10 prompt.
```

**How to paste:** Combine both blocks into a single paste into your `claude` session.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ Five skeleton files copied: `phase_10_objective.md`, `phase_11_constraints.md`, `phase_11_postpdpa.md`, `phase_12_accept.md`, `phase_12_postpdpa.md`
- ✓ A live GET against `/allocate/campaigns` returning 5 campaigns
- ✓ Summary names: three phases and Trust Plane decisions, four pathologies, the exact PDPA sequence (re-classify → re-solve → confirm JSON changed)
- ✓ No proposed objective weights or constraint classifications
- ✓ Stop signal pending the Phase 10 prompt
- ✓ Viewer (http://localhost:3000) refreshes and shows: Sprint 3 tile activates; allocator-plan region shows "awaiting Phase 12"

**Signals of drift — push back if you see:**

- ✗ A proposed objective weight or penalty value — ask "please remove; I own these values in `phase_10_objective.md` / `phase_11_constraints.md`."
- ✗ Missing `phase_11_postpdpa.md` or `phase_12_postpdpa.md` in the skeleton copy — ask "where are the PDPA re-run files? They are not optional."
- ✗ PDPA sequence described as "re-classify only" — ask "where is the LP re-solve step? The plan file must also change."
- ✗ $220 not quoted from `PRODUCT_BRIEF.md §2` — ask "please quote the $220 line from §2."
- ✗ Viewer Sprint 3 tile does not activate — confirm `/allocate/campaigns` GET ran and returned 5 campaigns.

---

## 3. Things you might not understand in this step

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **LP allocator** — a linear program that maximises expected revenue by distributing campaign budget across customer segments
- **Hard vs soft constraint** — hard constraints cannot be violated (legal, physical); soft constraints can be violated for a dollar penalty
- **PDPA injection sequence** — the mandatory two-step re-run when a regulatory rule fires mid-sprint
- **Pathology detection** — checking for four structural problems in the solved plan before accepting it
- **Shadow price** — the dollar cost of adding one more unit of a hard constraint (how much compliance costs in revenue terms)

---

## 4. Quick reference (30 sec, generic)

### LP allocator

A linear program (LP) is an optimisation model that maximises or minimises an objective (e.g. expected revenue) subject to constraints (e.g. budget caps, minimum campaign sizes). Tonight's LP takes Sprint 1 segment memberships and Sprint 2 conversion probabilities as inputs and returns a campaign plan — how many customers from each segment to target with which campaign type and how much to spend. "Linear" means every term in the objective and constraints is a simple multiple of a decision variable (no squared terms, no if-then logic).

> **Deeper treatment:** [appendix/03-modeling/optimization-families.md](./appendix/03-modeling/optimization-families.md)

### Hard vs soft constraint

Hard constraints are lines the plan must not cross, regardless of cost — a legal restriction or a physical impossibility. Soft constraints are preferences: the plan prefers to stay within them, but can violate them for a dollar penalty. Tonight, the under-18 PDPA exclusion starts as a data-governance note and becomes a hard constraint when the injection fires. Misclassifying a hard constraint as soft means the LP can buy its way past a legal line. The classification decision is yours in Phase 11.

> **Deeper treatment:** [appendix/07-governance/hard-vs-soft-constraints.md](./appendix/07-governance/hard-vs-soft-constraints.md)

### PDPA injection sequence

When the instructor fires the PDPA injection at ~4:30, the mandatory sequence is: (1) re-classify under-18 browsing history as a hard constraint in Phase 11, quoting the $220/record penalty from `PRODUCT_BRIEF.md §2`; (2) re-solve the LP in Phase 12 with the new hard constraint; (3) confirm `data/allocator_last_plan.json` has changed on disk. Writing only step 1 is the top D3 rubric failure: your journal says you handled PDPA, but the plan file shows a pre-PDPA allocation.

> **Deeper treatment:** [appendix/07-governance/pdpa-basics.md](./appendix/07-governance/pdpa-basics.md)

### Pathology detection

Phase 12 checks for four structural problems in the solved plan before you accept it: (1) concentration — does one segment get all the budget? (2) dead campaigns — any campaign assigned zero spend? (3) boundary cases — is any decision variable at exactly its upper or lower bound (a sign the model is pushing against a constraint)? (4) sensitivity flip — does a small change in inputs flip which segment gets allocated? A plan that's "feasible" but has these pathologies will fail in production.

> **Deeper treatment:** [appendix/07-governance/hard-vs-soft-constraints.md](./appendix/07-governance/hard-vs-soft-constraints.md)

### Shadow price

The shadow price of a constraint is the amount the objective (expected revenue) improves if you relax that constraint by one unit. In PDPA terms: the shadow price of the hard under-18 exclusion is the revenue you give up to comply. If excluding under-18 browsing history costs $12,000/month in foregone revenue, the shadow price is $12,000. Reporting the shadow price in Phase 12 postpdpa turns a legal compliance step into a business conversation — "this constraint costs us this much, and here is why we accept it."

> **Deeper treatment:** [appendix/07-governance/shadow-prices.md](./appendix/07-governance/shadow-prices.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in the Sprint 3
Optimization boot step.

Read `workspaces/metis/week-05-retail/playbook/workflow-05-sprint-3-opt-boot.md`
for what this step does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. PDPA injection sequence >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in the Sprint 3 boot
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] Five skeleton files copied: including both `phase_11_postpdpa.md` and `phase_12_postpdpa.md`
- [ ] `/allocate/campaigns` returned 5 campaigns
- [ ] Summary names three phases, four pathologies, and the full PDPA re-run sequence
- [ ] No proposed weights or constraint classifications
- [ ] Claude Code has stopped and is waiting for the Phase 10 prompt

**Next file:** [`phase-10-objective.md`](./phase-10-objective.md)
