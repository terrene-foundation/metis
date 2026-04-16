<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Success Criteria — Endpoint Contract Assertions

This spec defines the five endpoint contracts the contract grader enforces (`scripts/grade_product.py`, weighted 40% of the workshop grade). Each endpoint is binary: all sub-assertions pass = 8%; anything less = 0% (see `rubric-grader.md` §2.2 no-partial-credit policy).

The grader imports the `ENDPOINT_CONTRACTS` dict from the Python module below. Keep the Python literal and the prose description in lock-step — a change to either MUST change both.

## Source of truth

Every assertion cites `canonical-values.md` §8 (endpoint contracts), §1 (drift severity enum), §2 (AutoML strategies), §3 (split strategies), §4 (ModelRegistry states), and `rubric-grader.md` §2 (contract table).

## `ENDPOINT_CONTRACTS` — importable Python dict

```python
# Imported by scripts/grade_product.py.
# Keys: endpoint path. Values: list of sub-assertion specs.
# Each sub-assertion carries a short name, a predicate description, and the
# actionable fix message printed on failure (sourced from scripts/grade_fix_messages.json).

ENDPOINT_CONTRACTS = {
    "POST /forecast/train": [
        {
            "name": "experiment_run_id_present",
            "assert": "response JSON contains key 'experiment_run_id' (non-empty string)",
            "fix": "re-prompt Claude Code: commission /forecast/train to call "
                   "TrainingPipeline.train and return the ExperimentTracker run ID.",
        },
        {
            "name": "tracker_get_run_succeeds",
            "assert": "ExperimentTracker.get_run(experiment_run_id) returns a run record",
            "fix": "the returned run ID does not resolve in the tracker; check that "
                   "TrainingPipeline was constructed with tracker=get_ml_context().tracker.",
        },
        {
            "name": "metrics_count_ge_2",
            "assert": "run.metrics has length >= 2",
            "fix": "log at least two metrics (e.g. mape AND rmse) per run.",
        },
        {
            "name": "training_timestamp_nonnull",
            "assert": "run.training_timestamp is not None",
            "fix": "TrainingPipeline.train must record training_timestamp on the run.",
        },
    ],
    "GET /forecast/compare": [
        {
            "name": "runs_count_ge_3",
            "assert": "response.runs is a list with length >= 3",
            "fix": "re-run /forecast/train with search_n_trials>=3 OR fall back to "
                   "data/leaderboard_prebaked.json.",
        },
        {
            "name": "distinct_params_hash",
            "assert": "every run in response.runs has a distinct params_hash",
            "fix": "AutoML search produced duplicate configs; raise n_trials or "
                   "diversify candidate_families.",
        },
        {
            "name": "metric_column_numeric",
            "assert": "each run's metric field is present and numeric",
            "fix": "ExperimentTracker.log_run must record a numeric metric value "
                   "(not None, not a string).",
        },
    ],
    "POST /forecast/predict": [
        {
            "name": "model_version_id_derived_shape",
            "assert": "response.model_version_id matches r'^.+_v\\d+$' "
                      "(format {name}_v{version}, see canonical-values §5)",
            "fix": "use ml_context.derive_model_version_id(name, version) to build "
                   "the response id; do NOT return opaque strings like 'mv_007'.",
        },
        {
            "name": "model_stage_is_serving",
            "assert": "ModelRegistry.get_model(name, version).stage in "
                      "{'staging', 'shadow', 'production'}",
            "fix": "model is archived; promote back to staging via "
                   "ModelRegistry.promote_model first (see canonical-values §4 transitions).",
        },
        {
            "name": "predictions_nonempty_numeric",
            "assert": "response.predictions is a non-empty list; every entry has "
                      "numeric predicted_orders",
            "fix": "InferenceServer.predict must emit at least one row with a "
                   "numeric predicted_orders value.",
        },
    ],
    "POST /optimize/solve": [
        {
            "name": "feasibility_true",
            "assert": "response.feasibility is True",
            "fix": "infeasible — re-classify one hard constraint as soft; see "
                   "Phase 11 fallback.",
        },
        {
            "name": "optimality_gap_float_ge_0",
            "assert": "response.optimality_gap is a float >= 0",
            "fix": "solver did not surface optimality_gap; check solver wrapper in "
                   "solvers/vrp_solver.py.",
        },
        {
            "name": "hard_constraints_keys_present",
            "assert": "response.hard_constraints_satisfied contains at least "
                      "{'vehicle_capacity', 'driver_hours_max'}",
            "fix": "hard_constraints_satisfied is missing required keys; the solver "
                   "must surface per-constraint booleans (additional keys welcome).",
        },
        {
            "name": "hard_constraints_all_true",
            "assert": "every value in response.hard_constraints_satisfied is True",
            "fix": "a hard constraint is violated; the solver returned a plan that "
                   "should have been rejected — check feasibility logic.",
        },
    ],
    "POST /drift/check": [
        {
            "name": "tests_list_has_ks_or_psi",
            "assert": "response.tests is a list with >=1 entry whose name in {'ks', 'psi'}",
            "fix": "DriftMonitor only emits KS (continuous) and PSI (population "
                   "stability); check your /drift/check response serializer.",
        },
        {
            "name": "test_statistic_numeric",
            "assert": "every test entry has a numeric statistic field",
            "fix": "the DriftReport must include statistic: float per test; do not "
                   "stringify.",
        },
        {
            "name": "overall_severity_enum",
            "assert": "response.overall_severity in {'none', 'moderate', 'severe'} "
                      "(canonical-values §1; library never emits 'low')",
            "fix": "severity emitted is not in the 3-value enum; do not invent 'low'.",
        },
    ],
}
```

## Assertion-count summary

| Endpoint            | Sub-assertions | Weight |
| ------------------- | -------------- | ------ |
| `/forecast/train`   | 4              | 8%     |
| `/forecast/compare` | 3              | 8%     |
| `/forecast/predict` | 3              | 8%     |
| `/optimize/solve`   | 4              | 8%     |
| `/drift/check`      | 3              | 8%     |

Total: 5 endpoints × 8% = 40% of total grade. See `rubric-grader.md` §3.3 for the `grade_report.json` shape and `§3.5` for behaviour on stub responses (treated as 0%).

## Behaviour when an endpoint returns `"placeholder": true`

If a response contains the scaffold-banner key `placeholder: true` (see `scaffold-contract.md` §4 JSON banner), the grader treats all sub-assertions as failed with fix message "this endpoint is still a scaffold placeholder; your commissioning prompt did not replace it."
