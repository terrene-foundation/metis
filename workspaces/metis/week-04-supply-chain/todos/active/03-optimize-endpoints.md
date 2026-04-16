---
shard_id: 03
status: SUPERSEDED
superseded_by: [03a, 03b]
reason: >
  Split per H1/H2 invariant-budget finding (red-team convergence report).
  Original shard had 9-10 invariants and 550-700 realistic LOC — over the
  autonomous-execution.md budget. 03a owns OR-Tools primary path + 3-term
  objective DSL. 03b owns PuLP fallback + 4-term carbon_levy objective +
  snapshot regression. See 03a-optimize-core.md and 03b-optimize-multi-objective.md.
---

# Shard 03 — SUPERSEDED

This shard has been split into:

- **03a-optimize-core.md** — OR-Tools VRP primary path, 3-term objective DSL, snapshot state machine, ExperimentTracker tagging, Tier-2 OR-Tools wiring test
- **03b-optimize-multi-objective.md** — PuLP fallback (env-var trigger, no mocks), 4-term carbon_levy objective (lta-carbon-levy scenario C1 fix), union-cap snapshot regression test

Do not implement from this file.
