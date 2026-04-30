<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 10 — Objective Function (queue allocator)

> **What this phase does:** Set the objective function for the reviewer queue allocator's linear program. Decision variables: how many posts of each tier route to which queue. Objective: minimise expected $ cost (FN + FP + reviewer-time + GPU).
> **Why it exists:** The LP doesn't pick its own objective. Phase 10 is where the moderation product becomes a business decision under constraints.
> **You're here because:** Sprint 3 booted. Phase 10 sets the LP objective; Phases 11 and 12 set constraints and acceptance.
> **Key concepts you'll see:** linear program, decision variables, multi-term objective, weight defense, shadow price

---

## 1. Paste this into Claude Code

**Universal core:**

```
I'm in Playbook Phase 10 — Objective Function. The reviewer queue
allocator solves a linear program. The objective minimises expected
cost across:

1. False-negative cost: FN_count × $FN_cost
2. False-positive cost: FP_count × $FP_cost
3. Reviewer-minute cost: reviewer_minutes × $reviewer_rate
4. GPU inference cost: inference_count × $GPU_rate

Decision variables: x[tier, queue] = number of posts in each (tier,
queue) pair.

Propose:
- The objective formula with all four terms and their weights/units
- The decision variable space (what tiers, what queues)
- A defense per term: "this term in the objective because <business
  rationale>"

Do NOT propose hard or soft constraints — those are Phase 11.
Do NOT use "blocker" without specifics.
```

**Tonight-specific additions** (Week 6 MosaicHub):

```
Cost source: PRODUCT_BRIEF.md §2.
- $FN_cost = $320/piece
- $FP_cost = $15/piece
- $reviewer_rate = $22/minute
- $GPU_rate = $0.03 per 1,000 image classifications

Decision variable space:
- Tiers (5): auto-allow, low-confidence-allow, mid-confidence-review,
  high-confidence-review, auto-remove
- Queues (3): expedited (60s SLA, for IMDA-mandate items),
  standard (90min SLA, for cost-balanced items),
  bulk (24hr SLA, for low-confidence repeat-violation patterns)

Objective formula draft (you propose, I edit):
  minimise: sum over (tier, queue) [
    expected_FN_at(tier) × $320
    + expected_FP_at(tier) × $15
    + expected_reviewer_minutes_at(queue) × $22
    + expected_GPU_inferences × $0.03/1000
  ]

Defenses per term:
- FN cost: catches harm that escaped auto-decision; cite $320
- FP cost: legitimate content auto-removed; cite $15
- Reviewer-minute: queue allocation under reviewer headcount; cite $22
- GPU inference: at 3M items/day across image+text+fusion, the cost is
  non-negligible; cite $0.03/1k

Defendable trade-offs:
- Pure FN-minimisation drives everything to expedited queue → reviewer
  cost explodes → SLA breaks
- Pure cost-minimisation under-staffs queues → FN escapes regulator
- The objective balances; Phase 11 hard constraints make IMDA non-
  negotiable so the LP can't trade compliance for cost.

Endpoint to call:
- POST /queue/objective with the weighted objective formula

Journal file: copy journal/skeletons/phase_10_objective.md.
```

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ Objective formula with 4 terms (FN / FP / reviewer / GPU)
- ✓ All weights cited from `PRODUCT_BRIEF.md §2`
- ✓ Decision variable space named (5 tiers × 3 queues)
- ✓ Per-term defenses written
- ✓ Trade-off discussion (pure-FN vs pure-cost extremes)
- ✓ POST to /queue/objective
- ✓ Stop signal pending Phase 11

**Signals of drift — push back if you see:**

- ✗ Weights without quoted brief lines — ask for citations
- ✗ Constraint hints in the objective (e.g. "subject to SLA ≤ 90min") — ask "isn't that Phase 11?"
- ✗ Missing GPU term at our 3M/day volume — ask for the inference-cost line
- ✗ Pure FN minimisation proposed without trade-off acknowledgment

---

## 3. Things you might not understand in this phase

- **Linear program** — a math problem with linear objective and linear constraints, solvable in milliseconds at our size
- **Decision variables** — the unknowns the solver picks (post-tier-queue counts)
- **Multi-term objective** — adding several cost terms with explicit weights
- **Weight defense** — why each term's coefficient is what it is, in business language
- **Shadow price** — the marginal $ cost of tightening a constraint by one unit (Phase 11/12 reads these)

---

## 4. Quick reference (30 sec, generic)

### Linear program

A math problem: minimise (or maximise) a linear function of decision variables, subject to linear equality and inequality constraints. The queue allocator's LP solves in milliseconds at our size (a few thousand decision variables). The LP is honest — it gives exactly what you asked for. Which is why getting Phase 10 (objective) and Phase 11 (constraints) right is everything.

> **Deeper treatment:** [appendix/03-modeling/recommender-families.md](./appendix/03-modeling/recommender-families.md)

### Decision variables

The unknowns the solver picks. Tonight: x[tier, queue] = how many posts of this confidence tier go to this queue. The solver picks values that minimise objective subject to constraints. The choice of decision-variable space matters — too coarse and you can't express the right plan; too fine and the LP doesn't solve in time.

> **Deeper treatment:** [appendix/03-modeling/recommender-families.md](./appendix/03-modeling/recommender-families.md)

### Multi-term objective

Adding several cost terms with explicit weights produces a single number to minimise. Each term has units in $; the weights are absolute (not normalised) so the LP optimises real dollars, not abstract scores. Adding a term shifts the optimal plan; removing a term hides cost. Tonight's four terms cover all real costs the platform incurs.

> **Deeper treatment:** [appendix/03-modeling/recommender-families.md](./appendix/03-modeling/recommender-families.md)

### Weight defense

Each weight is justified in business language. "$320 per FN because regulator complaint risk + lawsuit defense per PRODUCT_BRIEF.md §2." "$22 per reviewer-minute because that's the loaded cost from finance." Defending in business language means the rubric (and Legal) can verify the weight against an audit-trail document, not the agent's pattern-matching.

> **Deeper treatment:** [appendix/01-framing/cost-asymmetry.md](./appendix/01-framing/cost-asymmetry.md)

### Shadow price

The marginal $ cost of tightening a constraint by one unit. If reviewer headcount is the binding constraint, the shadow price is "$X per additional reviewer." Phase 12 reads shadow prices to quantify compliance cost (e.g. "the IMDA hard-line raised expected $/day by $Y because the reviewer queue tightened"). Shadow prices are the LP's way of explaining itself.

> **Deeper treatment:** [appendix/07-governance/shadow-prices.md](./appendix/07-governance/shadow-prices.md)

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 6 Phase 10.

Read the phase file and `workspaces/metis/week-06-media/journal/phase_10_objective.md`.

Explain "<<< FILL IN: concept name >>>" — plain language, MosaicHub-grounded,
implications for Phase 10 objective, what to push back on. Under 400 words.
```

---

## 6. Gate / next

- [ ] Objective formula has 4 cited terms
- [ ] Decision variable space named
- [ ] Per-term defenses written
- [ ] POST /queue/objective fired
- [ ] Stop signal pending Phase 11

**Next file:** [`phase-11-constraints.md`](./phase-11-constraints.md)
