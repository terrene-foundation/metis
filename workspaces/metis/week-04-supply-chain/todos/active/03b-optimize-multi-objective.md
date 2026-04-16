---
shard_id: 03b
slug: optimize-multi-objective
title: >
  Extend /optimize/solve to support the 4-term carbon_levy objective (lta-carbon-levy
  scenario), add PuLP LP-decomposition fallback on ortools ImportError using an
  env-var guard (OR_TOOLS_DISABLED=1) instead of mocking, and add the
  union-cap re-solve snapshot regression test.
loc_estimate: 180
invariants:
  - carbon-levy-term: when scenario_tag=="post_carbon_levy", objective.terms array MUST include a {name:"carbon_levy", weight:0.18, unit:"per_km"} entry; objective_value reflects all four terms (fuel + sla + overtime + carbon_levy); solver does NOT reject or silently ignore the 4th term
  - pulp-fallback-real: PuLP fallback is triggered by OR_TOOLS_DISABLED=1 env var (real runtime code path); the test uses subprocess with OR_TOOLS_DISABLED=1 set; no @patch or MagicMock — testing.md Tier-2 MUST rule applies
  - lta-scenario-response: response for post_carbon_levy includes objective_value > fuel-only baseline; scenario_tag "post_carbon_levy" is accepted as a valid snapshot tag (does not write snapshot files — only preunion/postunion tags trigger snapshots)
  - carbon-levy-wiring-asserted: test_carbon_levy_objective.py POSTs a 4-term body and asserts objective_value > baseline 3-term solve on same fixture; proves D3 learning objective can score 4/4
  - union-cap-snapshot-regression: test_union_cap_snapshot_sequence.py proves preunion snapshot is never overwritten on a second "preunion" solve; proves postunion does not touch preunion
call_graph_hops: 3
depends_on: [03a]
blocks: []
specs_consulted:
  - specs/scenario-catalog.md §4 (lta-carbon-levy: scenario_tag="post_carbon_levy", 4-term objective, weight 0.18 per_km, Deployable tomorrow: YES)
  - specs/canonical-values.md §8.4 (POST /optimize/solve variable-arity terms contract)
  - specs/wiring-contracts.md §10 (PuLP wiring test — scaffold-contract.md §9 audit table)
  - specs/playbook-phases-prescribe.md (Phase 10 D3 cost-quantification learning objective: $0.53/km total cost delta)
acceptance_criteria:
  - POST /optimize/solve accepts a 4-term objective.terms array; when scenario_tag=="post_carbon_levy", the 4-term body {fuel, sla, overtime, carbon_levy} is processed and objective_value reflects all four terms; scenario-catalog.md §4 "Deployable tomorrow YES" contract satisfied
  - PuLP fallback path triggered by OR_TOOLS_DISABLED=1 environment variable on the vrp_solver import path; fallback produces a response with the same schema as the OR-Tools path; no @patch on ortools anywhere in test suite (testing.md Tier-2 NO mocking rule)
  - tests/integration/test_carbon_levy_objective.py passes: POSTs a 4-term body (fuel+sla+overtime+carbon_levy with weight 0.18 per_km) and asserts objective_value > the 3-term baseline on the same fixture; proves D3 cost delta is non-zero
  - tests/integration/test_pulp_wiring.py passes: sets OR_TOOLS_DISABLED=1 in subprocess env, calls POST /optimize/solve via Nexus TestClient, asserts PuLP path produces valid plan with same response schema (feasibility:bool, optimality_gap:float>=0, plan_path present); real PuLP, no mocks
  - tests/integration/test_union_cap_snapshot_sequence.py passes: calls solve with scenario_tag="preunion" twice; asserts route_plan_preunion.json is identical after second call (idempotent); then calls with scenario_tag="postunion"; asserts route_plan_preunion.json still unchanged
wiring_tests:
  - tests/integration/test_carbon_levy_objective.py (scenario-catalog.md §4 — 4-term objective accepted; D3 objective_value delta non-zero)
  - tests/integration/test_pulp_wiring.py (scaffold-contract.md §9 audit table; real PuLP, no mocks; OR_TOOLS_DISABLED=1 env trigger)
  - tests/integration/test_union_cap_snapshot_sequence.py (snapshot idempotency regression)
---

# Shard 03b — Optimize Multi-Objective

## What

Extend the /optimize/solve route (built in shard 03a) to support the lta-carbon-levy 4-term objective, add the PuLP fallback using a real env-var-triggered code path instead of a mock, and add the snapshot sequence regression test. This shard closes the CRITICAL C1 finding (4-term carbon_levy endpoint not implemented) and the HIGH finding on Tier-2 test mock violation.

## Why

The lta-carbon-levy scenario fires at minute 35 of Sprint 2. The instructor fires it; students POST a 4-term objective body per scenario-catalog.md §4. If the route silently ignores the carbon_levy term, objective_value does not change, students cannot observe the $0.53/km cost delta, and D3 "cost-quantification" scores 0/4 for every student. The scenario is marked "Deployable tomorrow: YES" — this is not a hypothetical.

The PuLP fallback mock was a testing.md Tier-2 violation. The fix is an env-var gate (OR_TOOLS_DISABLED=1) that the real runtime code checks, so the test exercises the real import-guard logic path without mocking.

## Implementation sketch

- `src/backend/solvers/vrp_solver.py` — extend import guard: `if os.environ.get("OR_TOOLS_DISABLED") == "1": raise ImportError("OR_TOOLS_DISABLED")` at module level so the real fallback fires in tests without patching
- `src/backend/solvers/lp_solver.py` — wraps PuLP LP decomposition; accepts the same canonical request dict from shard 03a; returns the same canonical response shape
- Route handler in optimize.py already accepts variable-arity terms (shard 03a); no schema change required for the 4th term — the terms array is already iterable and summed
- test_carbon_levy_objective.py: constructs a minimal northwind fixture, POSTs 3-term solve to record baseline objective_value, then POSTs 4-term solve with carbon_levy, asserts new objective_value > baseline
- test_pulp_wiring.py: sets `OR_TOOLS_DISABLED=1` in the test process env before importing the solver module (or via monkeypatch.setenv), calls the route, checks PuLP is used via the solver field in the response ("pulp"), asserts same response schema
- test_union_cap_snapshot_sequence.py: calls solve twice with scenario_tag="preunion", reads the bytes of route_plan_preunion.json both times, asserts md5 identical; then calls with "postunion", asserts preunion unchanged

## Out of scope

- Initial route scaffold and OR-Tools primary path (shard 03a)
- /forecast/train (shard 02)
- /drift/check (shard 04)
- scenario_inject.py lta-carbon-levy firing (shard 06 — injects the scenario; this shard provides the endpoint that accepts it)

## Acceptance

- [ ] POST /optimize/solve accepts a 4-term objective.terms array; scenario_tag=="post_carbon_levy" processed with all four terms; objective_value reflects carbon_levy contribution
- [ ] OR_TOOLS_DISABLED=1 env var triggers PuLP fallback in real code path; no @patch anywhere in tests for this path
- [ ] tests/integration/test_carbon_levy_objective.py passes: 4-term objective_value > 3-term baseline on same fixture
- [ ] tests/integration/test_pulp_wiring.py passes: real PuLP, OR_TOOLS_DISABLED=1 env trigger, same response schema
- [ ] tests/integration/test_union_cap_snapshot_sequence.py passes: preunion idempotency + postunion isolation
