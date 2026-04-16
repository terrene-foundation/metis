# Playbook Phases 10–12 — Prescriptive / Optimization

This spec is the detail authority for phases 10, 11, 12 of the Universal ML Decision Playbook — Sprint 2's Optimize block. Phases 1–9 live in `playbook-phases-sml.md`; phases 13–14 live in `playbook-phases-mlops.md`. Cross-index is `playbook-universal.md`.

Each phase specifies: (a) sprints that run it, (b) trust-plane question, (c) prompt template, (d) evaluation checklist, (e) journal schema, (f) common failure modes, (g) the artefact that MUST exist on disk to claim the phase complete.

Trust Plane / Execution Plane capitalisation follows `terrene-naming.md`.

---

## Phase 10 — Objective Function

- **Sprints**: Sprint 2 (~12 min).
- **Trust-plane question**: Single or multi-objective? What are the weights?
- **Prompt template**:
  > _"Propose an objective function for the Northwind route optimiser using the business costs in `specs/business-costs.md` (fuel $0.35/km, late delivery $220, overtime $45/hr, carbon $8/kg CO₂). Show a single-objective version (sum of costs) AND a multi-objective version (cost, SLA, carbon with defended weights). Recommend one. Discuss the trade-off honestly — e.g. 'carbon weight of $8/kg is below social cost of carbon; revise next year.'"_
- **Evaluation checklist**:
  - [ ] Every term has a cost in real money or a justified proxy.
  - [ ] Single-objective AND multi-objective both presented.
  - [ ] Weights defended with business reasoning.
  - [ ] Trade-off discussed honestly.
- **Journal schema**:
  ```
  Phase 10 — Objective
  Chosen: single / multi
  Terms + weights: ____
  Business justification: ____
  Known limitation: ____
  ```
- **Common failure modes**:
  - Objective written in math-y language without business grounding.
  - Carbon term dropped because "client didn't ask" — but the deck emphasises ESG; loses a dimension.
  - Weights pulled from thin air — 0/4 on trade-off honesty.
- **Artefact**: `journal/phase_10_objective.md`.

---

## Phase 11 — Constraint Classification

- **Sprints**: Sprint 2 (~10 min). Re-run after union-cap injection.
- **Trust-plane question**: Hard or soft for each rule? Penalty for soft?
- **Prompt template (first pass)**:
  > _"List every constraint the optimiser will face (vehicle capacity, driver hours, time windows, carbon targets, service levels). For each: (a) hard or soft, (b) if soft, penalty per unit violated, (c) justification grounded in the business rule it encodes (law, physics, contract, preference)."_
- **Prompt template (post-injection re-run)**:
  > _"The instructor fired the union-cap scenario: driver overtime is now capped at 5 h/week. Re-classify the relevant constraint. The prior classification is already saved as `journal/phase_11_constraints.md`; write the new one as `journal/phase_11_postunion.md`. Be explicit about which constraint changed from soft to hard and why."_
- **Evaluation checklist**:
  - [ ] Every constraint classified with explicit rationale (law / physics / contract / preference).
  - [ ] Soft constraints have defensible penalty values.
  - [ ] No constraint labelled "probably hard" without reason.
  - [ ] Post-injection: union-cap correctly re-classified as hard (labour law / contract).
- **Journal schema** (both passes):
  ```
  Phase 11 — Constraints
  Hard: ____ (reason each)
  Soft: ____ (penalty each)
  What changed from prior pass (post-injection only): ____
  ```
- **Common failure modes**:
  - Union-cap mis-classified as soft after injection (the injection exists precisely to test this).
  - Hard-constraint set too tight → solver infeasible → student panics. Recovery: re-classify one as soft.
  - Penalty values unspecified ("some penalty") — 1/4 on classification rubric.
- **Artefact**: `journal/phase_11_constraints.md` + `journal/phase_11_postunion.md`.

---

## Phase 12 — Solver Acceptance

- **Sprints**: Sprint 2 (~10 min). Re-run after union-cap injection.
- **Trust-plane question**: Is the solution feasible, optimal, edge-case safe?
- **Prompt template**:
  > _"Run the OR-Tools VRP solver on `data/forecast_output.json` with the objective from Phase 10 and constraints from Phase 11. Time budget 30 s. Report: (a) every hard constraint satisfied — yes/no table (at minimum `vehicle_capacity` and `driver_hours_max`), (b) objective value + optimality gap, (c) top 3 pathological patterns (driver imbalance, geographic zigzags, underutilised vehicles). Recommend accept / re-solve / re-design. Save plan to `data/route_plan.json`. After the scenario injection, save pre-injection plan as `data/route_plan_preunion.json` and post-injection plan as `data/route_plan_postunion.json`."_
- **Evaluation checklist**:
  - [ ] Every hard constraint confirmed satisfied — `hard_constraints_satisfied` response dict contains at least `vehicle_capacity` and `driver_hours_max` with value `true`.
  - [ ] Optimality gap reported numerically (OR-Tools produces this).
  - [ ] Pathologies named (driver imbalance, zigzags, underutilisation).
  - [ ] Accept / re-solve / re-design decision defended.
  - [ ] Post-injection: `_preunion` and `_postunion` both on disk, neither overwritten.
- **Journal schema**:
  ```
  Phase 12 — Solver Acceptance
  Feasibility: yes/no (per hard constraint)
  Optimality gap: ____
  Pathologies: ____
  Decision: Accept / Re-solve / Re-design
  What would make me re-design: ____
  ```
- **Common failure modes**:
  - Solver returns feasible but pathological plan (one driver 95% of work). Student accepts because "solver said feasible" — 1/4 on trade-off honesty.
  - Optimality gap not surfaced (OR-Tools reports it; student doesn't read it out).
  - Scenario-injection state corruption (F6): `route_plan.json` overwritten without `_preunion` snapshot. Recovery via `scripts/seed_route_plan.py` (see `scaffold-contract.md` §6).
- **Artefact**: `data/route_plan_preunion.json` + `data/route_plan_postunion.json` + `journal/phase_12_solver.md` + `journal/phase_12_postunion.md`.
