<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Optimization Families

> **One-line hook:** Four approaches for making the best decisions under constraints — and why linear programming is the right tool for Arcadia's campaign allocator.

## The gist

Optimization is the third layer of the ML value chain: after you've discovered segments (USML) and predicted responses (SML), you need to decide what to do — which customers get which campaigns, given a fixed budget and legal constraints. That's an optimization problem.

**Linear programming (LP)**: Maximise or minimise a linear objective (e.g., total expected revenue) subject to linear constraints (e.g., total spend ≤ budget, each customer contacted at most once). Solved exactly and efficiently by scipy or PuLP. The Arcadia allocator is an LP: maximise `Σ x × (P(convert) × $18 revenue − $3 touch cost)` subject to budget cap, PDPA exclusions, and inventory limits. You specify the objective and the constraints; the solver finds the optimal allocation plan.

**Mixed-integer programming (MIP)**: An extension of LP where some decisions must be integers (0 or 1 — yes/no decisions like "does this customer get contacted?"). MIP problems are much harder to solve and may require heuristics or approximate solvers. Use when LP produces fractional decisions you cannot round safely.

**Constraint satisfaction**: Find any feasible solution (one that satisfies all constraints), without optimising for an objective. Useful when feasibility is the primary concern and there's no clear objective to maximise. Rarer in marketing; more common in scheduling.

**Greedy heuristics**: Allocate budget greedily — assign the highest-expected-revenue customer first, then the next, until budget is gone. Simple, fast, and often within 10–30% of the LP optimum. A good fallback if the LP is too slow or infeasible.

For Arcadia Sprint 3: you use LP. The solver (scipy's `linprog` or similar) is pre-wired at `/allocate/solve`. Your Phases 10–12 decisions are the objective weights, the constraint classifications (hard vs soft), and whether the resulting plan is acceptable.

## Why it matters for ML orchestrators

The shadow price — the dollar value of relaxing a constraint by one unit — is an LP concept that makes constraints legible to business stakeholders. When the PDPA hard constraint costs $50,000/month in shadow price, that's the dollar cost of compliance made visible. That number belongs in your journal and in your conversation with the CMO.

## Common confusions

- **"LP assumes linearity, which is unrealistic"** — For campaign allocation, linear is usually fine: expected revenue scales with allocation, costs are proportional to contacts. If you had interaction effects (e.g., showing two ads to the same customer produces less-than-doubled effect), you'd need a non-linear formulation, which is much harder.
- **"Feasible plan = good plan"** — Feasibility means the plan satisfies all hard constraints. It doesn't mean the plan is sensible: a feasible plan might allocate 90% of the budget to one segment (a pathology you check in Phase 12).

## When you'll hit it

Used in: Phase 10 (Objective — LP objective design), Phase 11 (Constraints — hard/soft classification, PDPA), Phase 12 (Solver Acceptance — feasibility, pathology detection), workflow-05 (Sprint 3 Opt boot)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Hillier & Lieberman, "Introduction to Operations Research" — foundational LP text
- Hart et al., "Pyomo — Optimization Modeling in Python" — practical LP/MIP in Python
