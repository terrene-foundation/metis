<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

_[← Playbook index (README)](./README.md)_

## Phase 10 — Objective Function

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ USML ✓ ▸ SML ✓ ▸ **Opt ◉** ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 3 · Phase 10 of 12 — Objective
 LEVERS:        single-vs-multi · weight assignment · proxy metrics · coverage floors
──────────────────────────────────────────────────────────────────
```

### Concept

Defining "good" for a product that has a secondary optimization layer. "Good" is almost never one number — it's 3–5 competing signals (revenue, reach, diversity, touches, cost, fairness). You present both a single-objective framing (weighted sum) and a multi-objective framing (separate scores with a Pareto frontier). Recommend one; defend weights; name honestly what each framing sacrifices.

### Why it matters (SML + Optimization lens — the DEPTH Week 4 skipped)

- **Loss functions in SML ARE objective functions.** Cross-entropy (classification), MSE (regression), hinge (SVM). The choice shapes what the model optimizes.
- **Linear programming objective.** `minimise c^T x` where `c` is the cost vector, `x` is the decision. Every LP has an objective; choosing it IS the job.
- **Dual variables and shadow prices.** When an LP solves, each constraint has a **shadow price** = the marginal improvement in the objective if the constraint were relaxed by one unit. "What's it worth to add one more touch to the budget?" = shadow price of the touch-budget constraint.
- **Pareto frontier.** For multi-objective problems, a Pareto-optimal point is one where you can't improve one objective without worsening another. The frontier is the set of all Pareto-optimal points. You pick on it by declaring weights.
- **Coverage / fairness floors as constraints, not as objectives.** If you optimize revenue and _hope_ for diverse coverage, you'll get a monoculture. Coverage belongs in the constraint set (Phase 11), not in the objective (Phase 10). The objective is what you _maximise_; the constraint is what you _respect_.

### Your levers this phase

- **Lever 1 (the big one): single vs multi-objective.** Single-objective = everything in one weighted sum → simpler, may hide trade-offs. Multi-objective = separate scores → honest, harder to action. Default to single WITH coverage/fairness in constraints; go multi when stakeholders explicitly disagree on trade-offs.
- **Lever 2 (the weight-assignment): defend in dollars.** Each term in the objective has a dollar interpretation: revenue is $, reach is $/customer, diversity is $/category-covered (via long-tail protection). Weights come from stakeholder conversation + dollar math.
- **Lever 3 (the proxy-metrics rule):** some signals (serendipity, customer-happiness) are proxies for long-term revenue. Name them as proxies; don't pretend they're direct.
- **Lever 4 (the skip):** coverage/fairness/diversity BELONGS in Phase 11 constraints, not Phase 10 objective.

### Trust-plane question

Single-objective (revenue only, with coverage as constraint) or multi-objective (revenue AND reach AND diversity with weights)? What are the weights, and what does each framing sacrifice?

### Paste this

```
I'm entering Playbook Phase 10 — Objective Function. The scaffold
pre-committed to the LP allocator shape and the endpoints
(/allocate/objective GET + POST, /allocate/campaigns,
/allocate/solve per src/retail/backend/routes/allocate.py); my
decision here is the OBJECTIVE WEIGHTS — single vs multi-objective,
and the specific weight per term — defended in dollars.

Copy journal/skeletons/phase_10_objective.md into
workspaces/metis/week-05-retail/journal/phase_10_objective.md.

Your job:

1. Name the 3–5 competing signals the objective needs to reason
   across. For Arcadia's allocator these are: expected revenue,
   reach (customers touched), diversity (cross-segment coverage),
   touch spend. If you add a fifth (fairness, serendipity), name
   it as a PROXY for long-term revenue, not a direct term.

2. For each term, quote the dollar rate VERBATIM from
   PRODUCT_BRIEF.md §2:
   - Expected revenue per converted click — $18 (row: basket lift)
   - Wasted impression — $14 per session
   - Per-customer touch cost — $3 per contact
   - Cold-start session fallback — $8 per new-user session
   If you cannot find a row, say so; do NOT invent rates.

3. Draft BOTH framings side by side:
   (a) Single-objective: expected revenue maximisation, with
       diversity / reach as constraint floors (those go in Phase
       11). Formula:
       max Σ x × (P(convert) × $18 − $14 × wasted − $3 × touches)
   (b) Multi-objective: separate scores on revenue, reach,
       diversity, each scaled. Pareto frontier sketch.

4. Compute the SHADOW PRICE for the two most important constraints
   (touch budget and the PDPA under-18 exclusion). Shadow price =
   "how much extra revenue per unit of constraint relaxation". Run
   /allocate/solve once and read the solver output. Cite the
   solver function in src/retail/backend/routes/allocate.py.

5. Recommend ONE framing with defensible weights — but do NOT
   set the weight values. Your job is the shape and the rationale
   ("single-objective because stakeholders agree revenue is the
   headline"); my job is the weight numbers I paste into
   /allocate/objective.

6. Name what each framing SACRIFICES. Single-objective sacrifices
   explicit reach / diversity visibility; multi-objective
   sacrifices a single go/no-go number. No free lunch — state it.

Do NOT call /allocate/objective to POST new weights yet. That is
my action. You run /allocate/solve with the current / default
weights to expose the shadow prices, then stop.

Do NOT propose weight VALUES (0.7 revenue, 0.2 reach, 0.1 diversity).
Your job is the framing and the dollar rates; I pick the weights.

Do NOT use "blocker" without naming the specific ship-action.

When framings, shadow prices, and sacrifices are drafted with §2
quotes, stop and wait for my weight decision.
```

### Why this prompt is written this way

- Inheritance-framed opening names the scaffold's LP shape and endpoints and keeps the WEIGHTS with me — the objective is where the CMO's preferences live, so the agent drafts and I number.
- Show-the-brief is mandatory on the four rates because an invented $19 or $15 corrupts the objective and scores 0/4 on D1.
- Single- AND multi-objective framings both required because Phase 10 checklist says both must be presented — skipping multi is a 2/4 on D3 (hidden trade-off).
- Shadow price on touch budget and PDPA is required up front so the "cost of compliance" conversation starts before the injection, not after.
- Forbidding the POST to `/allocate/objective` is the structural guard against auto-picking weights — the agent cannot set the objective by side effect.

### What to expect back

- `journal/phase_10_objective.md` with the 3–5 signals named, each with a §2 quote.
- Both single- and multi-objective framings drafted side by side.
- Shadow prices for touch-budget and PDPA constraints, read from a real `/allocate/solve` run.
- A recommended framing with sacrifice stated, NO weight values.
- A stop signal pending my weight decision.

### Push back if you see

- A weight value proposed ("weight_revenue = 0.7") — "please remove; I own weights, you own framing."
- A dollar rate not quoted from §2 — "please quote the §2 row for this rate."
- Only one framing (single OR multi, not both) — "please draft both; I need to see what each sacrifices."
- Shadow price stated without running the solver — "please run `/allocate/solve` first; shadow prices come from the solver output."
- A POST to `/allocate/objective` already made — "please revert; I set the weights, not you."

### Adapt for your next domain

- Change `expected revenue / reach / diversity / touches` to your domain's objective terms.
- Change the four §2 dollar rates to your domain's cost table rows.
- Change `/allocate/objective`, `/allocate/solve` to your optimization endpoints.
- Change `touch budget + PDPA` shadow-price pair to your domain's binding-constraint pair.
- Keep the "draft both framings, sacrifice named" mechanic — it's domain-independent.

### Evaluation checklist

- [ ] Every term has a dollar value or a named proxy.
- [ ] Single-objective AND multi-objective both presented.
- [ ] Weights defended with stakeholder reasoning (not "they feel right").
- [ ] Shadow prices shown for main constraints (touch budget, PDPA).
- [ ] Trade-off discussed honestly ("X weighting sacrifices Y").

### Journal schema — universal

```
Phase 10 — Objective
Mode: single | multi
Terms + weights: ____
Business justification: ____
Shadow price of key constraint: ____
Known limitation (what this framing sacrifices): ____
Reversal: if ____ changes, switch to ____
```

### Common failure modes

- Objective written in math-y language with no business grounding.
- Coverage / diversity in objective, not constraints → monoculture output.
- Weights pulled from thin air — 0/4 on D3.
- Shadow prices not surfaced — student doesn't learn what relaxing each constraint is worth.

### Artefact

`POST /allocate/objective` with justification + `journal/phase_10_objective.md`.

### Instructor pause point

- Whiteboard a 2×2: revenue high/low × reach high/low. Where does "hero SKU to everyone" land? Where's "long-tail showcase"? Where's Arcadia's target?
- Have students write weights silently on sticky notes. Compare. 2× differences = class disagrees on "good."
- Ask: the allocator's shadow price on the touch budget is $12 per extra touch. Do we raise the budget? How much?

### Transfer to your next project

1. What are the 3–5 competing signals "good" actually means in MY domain — and am I pretending one doesn't exist because it's hard to measure?
2. Does each signal have a dollar value or a named proxy? Am I willing to defend the weights in front of a sceptical executive?
3. Is coverage / fairness / diversity in my objective (where it will get sacrificed) or in my constraints (where it will be enforced)?

---

