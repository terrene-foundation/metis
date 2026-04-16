# Grading Rubric + Contract Grader

This spec is the authority on how student work is graded. Two layers, weighted 60/40:

- **Layer 1 — Decision Journal (60%)** — 5-dimension rubric applied to every journal entry.
- **Layer 2 — Product Shipped (40%)** — 5 endpoint contract checks enforced by `scripts/grade_product.py`.

The grader script is shipped in the scaffold and MUST be run publicly by the instructor on the projector at 03:20. No post-hoc regrading.

## 1. Journal rubric (60% of total)

Every journal entry is scored on five dimensions, 0 / 2 / 4 per dimension. The cohort-average target is ≥ 3.0 across all entries to pass.

| Dim # | Dimension               | 0 (absent)                   | 2 (partial)               | 4 (complete)                                     |
| ----- | ----------------------- | ---------------------------- | ------------------------- | ------------------------------------------------ |
| D1    | **Harm framing**        | No stakeholders named        | Names one cost            | Quantifies asymmetry in named units ($40 vs $12) |
| D2    | **Metric→cost linkage** | Metric chosen without reason | Reason named              | Reason is a dollar figure or equivalent          |
| D3    | **Trade-off honesty**   | Picks winner, ignores loser  | Names what was sacrificed | Quantifies the sacrifice (e.g. "lost 0.8% MAPE") |
| D4    | **Constraint classify** | Unclear hard/soft            | Labelled correctly        | Penalty + reasoning included                     |
| D5    | **Reversal condition**  | "If data changed"            | Names a signal            | Names signal + threshold + duration window       |

Every entry is scored on all five dimensions even if not every dimension applies equally — the pattern of low scores across entries is itself a signal to the instructor.

### 1.1 Anchored 4/4 example (Phase 6 — Metric + Threshold)

```
Phase 6 — Metric + Threshold
Metric: cost-weighted MAPE with under-forecast weight=40 and over-forecast weight=12,
        averaged over depot-days. Reason: stockouts cost $40/unit (customer goodwill
        + penalties) and overstocks cost $12/unit (wasted driver hours + fuel), so a
        symmetric metric systematically over-values over-forecasting.
Threshold/Interval: 80th-percentile prediction interval. At the 50th percentile
        expected stockout cost is $4,800/day (holdout). At the 80th it drops to
        $1,280 but overstock rises to $780 — net $2,060 below the 50th. At the
        95th overstock dominates at $2,600.
Expected business impact: ~$16,000/week reduction in total cost vs 50th-percentile.
Sensitivity flip point: if stockout cost drops below $15 (e.g. SLA renegotiation),
        the 50th percentile beats the 80th — re-tune.
```

Scores: D1 = 4 ($40/$12 quantified), D2 = 4 (dollar-grounded reasoning), D3 = 4 ($780 overstock sacrifice named), D4 = n/a (not a constraint phase), D5 = 4 (named signal + $15 threshold).

### 1.2 Anchored 1/4 example (Phase 6 — same phase, same student's first draft)

```
Phase 6 — Metric + Threshold
Metric: MAPE, because it's a percentage so it's easy to explain.
Threshold: 80th percentile seems fine.
Impact: it should be good.
Sensitivity: if data changes, I'd re-run.
```

Scores: D1 = 0 (no stakeholders), D2 = 0 (no cost reason), D3 = 0 (no sacrifice named), D4 = n/a, D5 = 0 ("if data changes"). Average 0/4.

The full set of worked 4/4 and 1/4 examples lives in `journal/_examples.md`. Students read them before writing their first entry, so the gap between 4/4 and 1/4 is visible before the rubric pressure hits.

### 1.3 Applicability matrix

Not every dimension applies with equal weight to every phase. The grader averages actual-scored dimensions only (denominator = number of applicable dimensions × 4).

| Phase | D1 Harm | D2 Metric→cost | D3 Trade-off | D4 Constraint | D5 Reversal |
| ----- | ------- | -------------- | ------------ | ------------- | ----------- |
| 1     | **X**   | **X**          | —            | —             | **X**       |
| 2     | —       | —              | **X**        | —             | **X**       |
| 5     | —       | **X**          | **X**        | —             | **X**       |
| 6     | **X**   | **X**          | **X**        | —             | **X**       |
| 7     | **X**   | —              | **X**        | —             | **X**       |
| 8     | —       | —              | —            | **X**         | **X**       |
| 9     | —       | —              | —            | —             | —           |
| 10    | **X**   | **X**          | **X**        | —             | —           |
| 11    | —       | —              | —            | **X**         | —           |
| 12    | —       | —              | **X**        | **X**         | **X**       |
| 13    | —       | —              | —            | —             | **X**       |

Total scoring opportunities across Week 4's 11–13 journal entries: ~65 (approach.md calculation).

## 2. Product grade — 5 endpoint contracts (40% of total)

Each endpoint gets 8% of the total grade. The grader runs `scripts/grade_product.py` against the live backend and asserts non-trivial contracts — not HTTP 200. A student who ships `{"status": "ok"}` scores 0% on every endpoint because none of the assertions below reduce to a status-code check.

| #   | Endpoint            | Contract asserted by grader                                                                                                                                                                                                                                                                           | Weight |
| --- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| 1   | `/forecast/train`   | Response contains `experiment_run_id`; `ExperimentTracker.get_run(id)` returns params AND ≥ 2 metrics AND a non-null training timestamp                                                                                                                                                               | 8%     |
| 2   | `/forecast/compare` | Response is a list of ≥ 3 runs; each run has distinct `params_hash`; metric column is present and numeric                                                                                                                                                                                             | 8%     |
| 3   | `/forecast/predict` | Response contains `model_version_id` (derived string of form `{name}_v{version}`); handler parses to `(name, version)` and `ModelRegistry.get_model(name, version=version).stage ∈ {"staging", "shadow", "production"}`; `predictions` is a non-empty list of objects with numeric `predicted_orders` | 8%     |
| 4   | `/optimize/solve`   | Response contains `feasibility: true`, `optimality_gap` as float ≥ 0, `hard_constraints_satisfied` as dict containing AT LEAST keys `vehicle_capacity` and `driver_hours_max` where every value is `true`                                                                                             | 8%     |
| 5   | `/drift/check`      | Response contains ≥ 1 test with `name ∈ {"ks", "psi"}` (the two tests kailash-ml emits — no `chi2`, no `js`) and a numeric `statistic`; top-level `overall_severity ∈ {"none", "moderate", "severe"}` (3-value enum; the library never emits `"low"`)                                                 | 8%     |

### 2.1 Why this resists rubric gaming

A student returning `{"status": "ok"}` from `/forecast/train` scores 0% because no `experiment_run_id` is present. A student hardcoding a fake run ID scores 0% because `ExperimentTracker.get_run(id)` fails. A student returning a fake `model_version_id` scores 0% because `ModelRegistry.get(id)` fails. Gaming the grader would require re-implementing `ExperimentTracker` and `ModelRegistry` to fake-accept the grader's queries — more work than the honest path and with no ML decisions to show for it.

### 2.2 Partial credit policy

Each of the 5 endpoints is binary within itself — all of that endpoint's sub-assertions must pass for the 8%. An endpoint with N of N sub-assertions passing = 8%; anything less = 0%. The exact sub-assertion count per endpoint appears in the §3.3 report JSON (e.g. `/forecast/train` has 4 sub-assertions: `experiment_run_id_present`, `tracker_get_run_succeeds`, `metrics_count_ge_2`, `training_timestamp_nonnull`). No partial credit within an endpoint. This is deliberate: partial-credit rubrics invite stub-shaped responses that pass the easy assertion and fail the hard one.

## 3. `scripts/grade_product.py` contract

### 3.1 Inputs

- `--base-url` (default `http://localhost:8000`) — the Nexus API to grade.
- `--student-id` (optional) — tags the output report.
- `--output` (default `grade_report.json`) — where to write the machine-readable report.
- Reads `specs/success-criteria.md` for the assertion thresholds so the contract is edit-one-place.

### 3.2 Execution order

1. **Preflight check** — `GET /health`; fail-fast with actionable error if DB unreachable, FeatureStore empty, or drift wiring not active.
2. **Feature store populated** — `GET /forecast/compare?top_n=0`; if it returns `409 feature store empty`, print "run `scripts/preflight.py` and confirm `fs_preload.py` ran" and abort.
3. **Run each of the 5 endpoint assertions in sequence**, capturing response + latency.
4. **Actionable-message mapping** — each failure carries a specific fix instruction (not a stack trace). Every 4xx/5xx documented in `product-northwind.md` §8 has a matching fix message; all mappings live in `scripts/grade_fix_messages.json`:
   - `/forecast/train` 400 unknown `feature_schema` → "schema 'X' not registered in FeatureStore; check `fs_preload.py` ran (`.preflight.json.feature_store_populated: true`)."
   - `/forecast/train` 400 unsupported `split_strategy` → "replace 'rolling_origin' with 'walk_forward' — see `playbook-phases-sml.md` Phase 4."
   - `/forecast/train` 409 FeatureStore empty → "restart Nexus so `fs_preload.py` runs `register_features` + `store` on startup."
   - `/forecast/train` 422 AUTOML_QUICK cap → "reduce `search_n_trials` to ≤20, or unset `KAILASH_ML_AUTOML_QUICK` before retry."
   - `/forecast/train` 500 `error_category: xgb_missing` → "XGBoost extra not installed; preflight should have caught this. Omit XGBoostRegressor from `candidate_families` or `pip install kailash-ml[xgb]`."
   - `/forecast/train` no `experiment_run_id` → "re-prompt Claude Code: commission `/forecast/train` to call `TrainingPipeline.train` and return the ExperimentTracker run ID."
   - `/forecast/predict` 400 malformed `model_version_id` → "use the format `{name}_v{version}`, e.g. `forecast_sprint1_v3`."
   - `/forecast/predict` 404 model not found → "run Phase 4 AutoML + Phase 8 to register and promote a model."
   - `/forecast/predict` 409 archived model → "promote from archived → staging first via `ModelRegistry.promote_model`."
   - `/forecast/predict` 422 feature validation → "check that all features in the schema are present and numeric in the request `inputs`."
   - `/optimize/solve` no `optimality_gap` field → "re-prompt: the solver's `optimality_gap` must be surfaced in the response."
   - `/optimize/solve` 409 infeasible → "re-classify a hard constraint as soft; see Phase 11 fallback."
   - `/drift/check` 409 `reference data not set` → "GET /drift/status/<model_id> to confirm; if `reference_set: false`, re-run /forecast/train (which calls drift_wiring.wire synchronously)."
   - `/drift/check` 404 model not found → "check /forecast/compare for available model_version_ids."
   - Illegal `ModelRegistry` stage transition → print the transition table from `playbook-phases-sml.md` Phase 8.
5. **Emit pass/fail table** per endpoint with 8% / 0% scoring.
6. **Emit total product grade** as sum of passed endpoints.
7. **Return exit code 0** if all pass, non-zero otherwise.

### 3.3 Report format

`grade_report.json`:

```json
{
  "student_id": "<optional>",
  "graded_at": "2026-04-16T15:20:00Z",
  "base_url": "http://localhost:8000",
  "endpoints": [
    {
      "name": "/forecast/train",
      "weight": 0.08,
      "passed": true,
      "assertions": [
        { "name": "experiment_run_id_present", "passed": true },
        { "name": "tracker_get_run_succeeds", "passed": true },
        { "name": "metrics_count_ge_2", "passed": true, "observed": 3 },
        { "name": "training_timestamp_nonnull", "passed": true }
      ],
      "latency_ms": 87412,
      "message": null
    }
    // ... 4 more
  ],
  "product_grade": 0.4,
  "product_grade_max": 0.4
}
```

Console output mirrors the JSON in a colour-coded table so the projector audience sees it live.

### 3.4 Behaviour when endpoints are unreachable

If an endpoint returns 5xx or times out, the grader prints the specific fix instruction and scores that endpoint 0%. It does NOT retry — this is a live grade at 03:20, not a CI run. HTTP timeout is 120 seconds per request (configured via `httpx.Client(timeout=120)`), giving the 90-second `/forecast/train` contract 30s headroom.

### 3.5 Behaviour on stub responses

If a response is JSON but contains `"placeholder": true` (the JSON banner marker), the grader treats it as if the endpoint returned an empty body: 0% + "this endpoint is still a scaffold placeholder; the student's commissioning prompt did not replace it."

## 4. Combined score

```
total = 0.60 × journal_score + 0.40 × product_score
```

Where `journal_score` is the mean of per-entry mean-across-applicable-dimensions scores scaled to [0, 1], and `product_score` is the sum of passed endpoint weights scaled to [0, 1].

A student needs total ≥ 0.60 to pass the workshop. The best-case scenario (approach.md §Scenario 1) projects 85% of students passing.

## 5. Anti-patterns the rubric catches

- **"If data changed"** — scores 0/4 on D5 every time. The reversal-condition rubric is the primary learning outcome.
- **"MAPE because it's standard"** — scores 0/4 on D2. The metric must be tied to dollars.
- **"Solver said feasible, accept"** — scores 1/4 on D3 when a pathological plan ships. Must name the sacrifice.
- **"Union-cap is still soft"** (post-injection) — scores 1/4 on D4. The entire scenario injection exists to test this.
- **"Auto-retrain when MAPE > 15%"** — violates `agent-reasoning.md`. The Phase 13 prompt template refuses to accept it; the rubric's D5 rewards human-in-the-loop justification instead. See `journal/_examples.md` for a 4/4 example (signals + thresholds memo with human decision) vs a 1/4 example (if-else agent workflow) on this exact prompt.

## Open questions

None — the approach.md, failure-points, and risk-assessment artefacts agree on weights, assertions, and public-run timing.
