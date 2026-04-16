<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# AI Verify — Governance Review Checklist

Three-dimension AI governance review used at Phase 7 (red-team during Sprint 1) and Phase 9 / Phase 13 (codify step). Fairness is deliberately deferred to Week 7 — the Week 4 cohort is not yet equipped to reason about protected subgroups on logistics data without oversimplifying.

Each dimension has 3–5 concrete checks. Treat the checks as prompts for yourself; the grader does not score this file directly but Phase 7 journal entries reference it and Phase 9 codify lessons cite the dimensions by name.

## 1. Transparency

The ML Engineer and the Ops Manager must be able to explain, in plain English, why the chosen model produced a given prediction.

- [ ] Model family is documented in the Phase 5 journal entry with a one-sentence explanation of how it makes a prediction (e.g. "gradient-boosted decision trees average many small shallow trees; each tree splits on feature thresholds").
- [ ] At least one feature-importance view is produced by `ModelExplainer` or `permutation_importance` and attached to the Phase 7 journal entry.
- [ ] The top-3 features by importance are named in the journal with a Northwind-grounded sentence each (e.g. "day_of_week: Q4 peak drives ~20% of variance").
- [ ] If the model is an ensemble, the Phase 7 entry names which family dominates the prediction on the 3 depot-day segments most sensitive to forecast error.

## 2. Robustness

The model must degrade gracefully on data it was not trained on — the holdout window and post-drift periods are the main tests.

- [ ] Walk-forward validation (`split_strategy="walk_forward"`) was used in `/forecast/train` — time-series causality preserved.
- [ ] Metric-on-holdout is within a named delta of metric-on-training (e.g. "holdout MAPE 6.8% vs training 6.2% = +0.6 pp — acceptable because <1 pp"). Name the delta AND the acceptability threshold.
- [ ] The Phase 7 journal entry cites at least one out-of-distribution (OOD) risk the model will encounter in production (e.g. "Chinese New Year week is absent from the training window — forecasts there are extrapolation, not interpolation").
- [ ] DriftMonitor reference data is set by `drift_wiring.wire` after training; `.preflight.json.drift_wiring == true` confirms this (do not trust the flag without also running `GET /drift/status/<model_id>`).

## 3. Safety

Bad predictions must fail soft, not silently propagate into operations.

- [ ] Worst-1% predictions are bounded (e.g. "predicted_orders clamped to [0, 2 × historical depot-day max]" or "flagged for dispatcher review when > 99th percentile training value").
- [ ] Phase 8 deployment gate names the reversal condition explicitly — what signal, what threshold, what duration window would trigger a rollback from `shadow` to `staging`.
- [ ] The $220 SLA violation cost is surfaced in the Phase 7 red-team entry as the worst-case dollar exposure of a bad worst-1% prediction (e.g. "if the worst-1% predicts 50 orders short of reality, SLA hits could add $11,000/week").
- [ ] Human-in-the-loop is named for every reversible action (retrain, promote, rollback). No auto-retraining; no auto-promotion. See `rules/agent-reasoning.md`.

## 4. Fairness — deferred to Week 7

Week 4 does not score Fairness. The rationale: Northwind is a logistics domain with customer-segment features but no protected attributes in the traditional civil-rights sense. Teaching protected-subgroup analysis here invites oversimplification. Week 7 introduces a HR / people-ops dataset where the framing is appropriate.

Do note in your Phase 7 entry that Fairness was deferred (one sentence), so the codify step in Phase 9 can cite the deferral as a known gap.

## Related specs

- `rubric-grader.md` §1.1 — Phase 7 rubric applicability (D1 Harm, D3 Trade-off, D5 Reversal).
- `canonical-values.md` §1 — drift severity enum Transparency + Robustness cite.
- `product-northwind.md` §4.2 — Phase 7 in the Sprint 1 flow.
