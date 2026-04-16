---
shard_id: 03a
slug: optimize-core
title: >
  Implement the STUDENT-COMMISSIONED /optimize/solve route handler wired to
  OR-Tools VRP (primary path only), writing route_plan.json and snapshot files,
  the 3-term objective DSL, hard/soft constraint classifier, the snapshot
  state machine, ExperimentTracker tagging, and the Tier-2 OR-Tools wiring test.
loc_estimate: 200
invariants:
  - feasibility-typed: response always contains feasibility:bool and optimality_gap:float>=0; never omits these fields even on infeasible result
  - hard-constraints-dict: hard_constraints_satisfied is a dict[str,bool] containing at least vehicle_capacity and driver_hours_max
  - snapshot-hygiene: route_plan_preunion.json and route_plan_postunion.json are written at scenario_tag boundaries; route_plan.json is never overwritten when scenario_tag is postunion
  - experiment-tagged: ExperimentTracker.log_run called with tag="phase=optimize" and scenario=<preunion|postunion> per scaffold-contract.md banner
  - solver-time-budget: time_budget_s default 30s enforced; 500 with error_category=timeout when exceeded
  - solver-choice-is-deterministic-guard: the import-guard check (try import ortools; except ImportError: use pulp) is a deterministic installer check, NOT an agent decision; if a future shard proposes "choose solver by problem shape", that introduces LLM-routing-in-agent-path and is BLOCKED per rules/agent-reasoning.md
call_graph_hops: 3
depends_on: [01]
blocks: [03b]
specs_consulted:
  - specs/canonical-values.md §8.4 (POST /optimize/solve contract)
  - specs/product-northwind.md §8.4 (full request/response schemas + error taxonomy)
  - specs/scaffold-contract.md §2 (banner text for routes/optimize.py, verbatim)
  - specs/wiring-contracts.md §9 (OR-Tools VRP wiring test — scaffold-contract.md §9 audit table)
  - specs/playbook-phases-prescribe.md (Phase 10-12: objective + constraints + solver acceptance)
  - specs/scenario-catalog.md §2 (union-cap snapshot contract: route_plan_preunion.json / _postunion.json)
acceptance_criteria:
  - src/backend/routes/optimize.py ships with TODO-STUDENT banner from scaffold-contract.md §2 (verbatim); 501-stub body for student replacement; route registration stays put
  - POST /optimize/solve reads forecast_path from request; returns 422 with actionable message if file missing
  - Solver primary path uses ortools.constraint_solver.pywrapcp VRP; objective DSL accepts variable-length terms array (3-term baseline: fuel + sla + overtime); objective_value reflects all terms present in the request
  - Response contains feasibility:bool, optimality_gap:float>=0, objective_value:float, hard_constraints_satisfied dict with at least vehicle_capacity and driver_hours_max, plan_path, solver string, wallclock_s per canonical-values.md §8.4
  - When feasibility:false, response includes violated_constraints list and suggestion string per product-northwind.md §8.4 error cases
  - When scenario_tag is "preunion": writes data/route_plan.json (current) and data/route_plan_preunion.json (snapshot) atomically; does NOT overwrite preunion snapshot if already exists
  - When scenario_tag is "postunion": writes data/route_plan_postunion.json; does not touch route_plan.json or _preunion.json
  - ExperimentTracker.log_run called with experiment tags ["phase=optimize", "scenario=<tag>"] per scaffold-contract banner
  - 500 with error_category in {timeout, internal} when solver exceeds time_budget_s or crashes
  - tests/integration/test_ortools_vrp_wiring.py passes: imports ortools through route call (real OR-Tools, no mocks — testing.md Tier-2 MUST rule); asserts feasibility:true and optimality_gap>=0 and plan_path file written
wiring_tests:
  - tests/integration/test_ortools_vrp_wiring.py (scaffold-contract.md §9 audit table; real OR-Tools required; testing.md Tier-2 NO mocking)
---

# Shard 03a — Optimize Core

## What

Implement the /optimize/solve route with the OR-Tools VRP primary path, the 3-term objective DSL accepting variable-arity terms arrays, the snapshot hygiene rules for the union-cap scenario, ExperimentTracker tagging, and the Tier-2 OR-Tools wiring test. This shard covers the "route works correctly in normal conditions" path.

## Why

The 501-stub registration plus the wiring test must ship with the scaffold so OR-Tools is never an orphaned component. The snapshot hygiene invariant (never overwrite \_preunion once written) is the key state-machine contract the union-cap scenario injection depends on; violating it loses the before/after comparison the RoutePanel.tsx renders. The variable-arity terms array is required now so shard 03b can add the carbon_levy 4th term without changing the route's acceptance schema.

## Implementation sketch

- `routes/optimize.py` — TODO-STUDENT banner (verbatim); 501-stub body; route registration stays; inline comments listing required call sites and forbidden patterns
- `src/backend/solvers/vrp_solver.py` — wraps OR-Tools VRP; accepts the canonical request body with `objective.terms` array (list of {name, weight, unit}); returns the canonical response dict; sums all terms into objective_value regardless of arity; hard/soft constraint classifier checks required keys (vehicle_capacity, driver_hours_max)
- Snapshot logic: check `scenario_tag`; if "preunion" and `route_plan_preunion.json` does not exist, copy current `route_plan.json` there first; write solved plan to `route_plan.json`; if "postunion" write only to `route_plan_postunion.json`
- Wiring test: test_ortools uses real OR-Tools on a minimal 3-depot 2-vehicle fixture with a 3-term objective; asserts all external effects (feasibility, file written, experiment tagged)

## Out of scope

- PuLP fallback (shard 03b)
- 4-term carbon_levy objective (shard 03b)
- /forecast/train (shard 02)
- /drift/check (shard 04)
- Viewer panel rendering of route plan (shard 05)
- scenario_inject.py CLI (shard 06)

## Acceptance

- [ ] src/backend/routes/optimize.py ships with TODO-STUDENT banner from scaffold-contract.md §2 (verbatim); 501-stub body for student replacement; route registration stays put
- [ ] POST /optimize/solve reads forecast_path from request; returns 422 with actionable message if file missing
- [ ] Solver primary path uses ortools.constraint_solver.pywrapcp VRP; objective DSL accepts variable-arity terms array
- [ ] Response contains feasibility:bool, optimality_gap:float>=0, objective_value:float, hard_constraints_satisfied dict with at least vehicle_capacity and driver_hours_max, plan_path, solver string, wallclock_s per canonical-values.md §8.4
- [ ] When feasibility:false, response includes violated_constraints list and suggestion string
- [ ] When scenario_tag is "preunion": writes route_plan.json + route_plan_preunion.json atomically; does NOT overwrite preunion snapshot if already exists
- [ ] When scenario_tag is "postunion": writes route_plan_postunion.json only
- [ ] ExperimentTracker.log_run called with ["phase=optimize", "scenario=<tag>"]
- [ ] 500 with error_category in {timeout, internal} when solver exceeds time_budget_s or crashes
- [ ] tests/integration/test_ortools_vrp_wiring.py passes with real OR-Tools (no mocks); asserts feasibility:true and optimality_gap>=0 and plan_path file written
