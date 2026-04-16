<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Worked Journal Examples — 4/4 vs 1/4 per Rubric Dimension

Read this file before writing your first journal entry. Every rubric dimension below is anchored by a 4/4 example and a 1/4 example using the same Northwind numbers you will work with in the workshop ($40 stockout, $12 overstock, $220 SLA, $45/hr overtime, $0.35/km fuel, $0.18/km LTA carbon levy). Anti-patterns are lifted from `specs/rubric-grader.md` §1.2 and §5.

Rubric anchors cited below come from `specs/canonical-values.md` §9 (D1–D5 at 0 / 2 / 4).

---

## D1 — Harm framing

> Anchor 4 (`canonical-values.md` §9): Quantifies asymmetry in named dollars ($40 vs $12 = 3.3:1).
> Anchor 0: No stakeholders named.

### 4 / 4 — Phase 1 (Frame)

> Under-forecasting a depot-day costs Ops $40 per unit short: customer goodwill plus SLA exposure on the $220 violation fee when missed deliveries roll into next-day. Over-forecasting costs $12 per unit of excess capacity — wasted driver hours plus fuel at $0.35/km. The asymmetry is 3.3 : 1, so a symmetric metric (plain MAPE) systematically under-values the Ops Manager's actual cost. Stakeholder: Ops Manager (decides tomorrow's plan); impacted secondaries: Dispatcher (handles missed-delivery calls), Demand Planner (owns model health).

### 1 / 4 — Phase 1 (Frame)

> Forecasting demand so Northwind can run better. Bad forecasts cost money and should be avoided.

Why 1/4: no stakeholder named, no cost term named, no asymmetry. Anti-pattern from `rubric-grader.md` §1.2 — "costs more" without a ratio.

---

## D2 — Metric → cost linkage

> Anchor 4: Reason is a dollar figure or dollar-equivalent.
> Anchor 0: Metric chosen without reason.

### 4 / 4 — Phase 6 (Metric + Threshold)

> Metric: cost-weighted MAPE with under-forecast weight 40 and over-forecast weight 12, averaged over depot-days. The weights are the Northwind stockout and overstock costs. A 1-point drop in weighted MAPE on the 30-day holdout translates to approximately $4,200 of avoided cost per week at the current 12,000-order/day volume; we quantified this by multiplying the per-unit asymmetry by the observed 10-day rolling error distribution. Plain MAPE would have picked a model that drifts 0.8 percentage points higher on under-forecast error — roughly $3,400/week of hidden stockout cost.

### 1 / 4 — Phase 6 (same student's first draft)

> MAPE, because it's standard and easy to explain.

Why 1/4: no dollar reasoning, no cost linkage. Anti-pattern from `rubric-grader.md` §5 — "MAPE because it's standard".

---

## D3 — Trade-off honesty

> Anchor 4: Quantifies the sacrifice (e.g. "lost 0.8% MAPE").
> Anchor 0: Picks winner, ignores loser.

### 4 / 4 — Phase 5 (Model Selection)

> Chose `sklearn.ensemble.GradientBoostingRegressor` (ExperimentTracker run `a1b2c3d4-...`) with weighted MAPE 6.4% vs the pre-baked XGBRegressor at 5.9%. Sacrificed 0.5 percentage points of accuracy to stay inside the workshop's no-XGB-fallback path (Phase 7 redteam preserves Transparency: Gradient Boosting has a well-understood explainer path via `permutation_importance`). In dollars, the sacrifice is ~$0.53 per km of route wasted on extra driver time when the forecast under-predicts one depot, holding fuel constant at $0.35/km — about $2,100/week across the 3-depot network. I accepted the trade because the Ops Manager cannot debug XGB if it breaks mid-week and we have no XGBoost installed on half the fleet laptops.

### 1 / 4 — Phase 5 (same student's first draft)

> Picked Gradient Boosting because it was at the top of the leaderboard.

Why 1/4: no sacrifice named, no cost quantified, no reason beyond rank. Anti-pattern from `rubric-grader.md` §5 — "Solver said feasible, accept".

---

## D4 — Constraint classification

> Anchor 4: Penalty (in dollars) + reasoning included.
> Anchor 0: Unclear hard/soft.

### 4 / 4 — Phase 11 (post `union-cap` injection)

> Re-classified `driver_overtime_hours_max` from **soft** (penalty $45/hour) to **hard** (5 h/week cap, no penalty accepted). Reason: the MOM Employment Act framing in the `union-cap` injection makes this contractual, not financial — a violation is not something you pay $45/hour to undo, it is something that triggers a compliance incident with an estimated exposure >$10,000 per driver per week (legal fees + remediation), dwarfing the overtime savings. The previous plan's $450/week overtime spend across 10 drivers becomes zero; SLA violations at $220 each rise by an estimated 3 per week, net weekly impact +$660 but with compliance risk retired. Soft constraint retained: `delivery_before_5pm` at $15/hr-late — still a dollar trade.

### 1 / 4 — Phase 11 (post `union-cap`, anti-pattern)

> Kept overtime as a soft constraint but raised the penalty from $45 to $200/hour so the solver would respect it.

Why 1/4: contractual constraints are not price-able. Anti-pattern from `rubric-grader.md` §5 — "Union-cap is still soft".

---

## D5 — Reversal condition

> Anchor 4: Names signal + threshold + duration window (no bare rules).
> Anchor 0: "If data changed".

### 4 / 4 — Phase 13 (post `drift-week-78`)

> Signal: PSI on the top three features (`day_of_week`, `customer_segment_mix`, `depot_region_share`) as surfaced by `/drift/check`. Threshold: PSI ≥ 0.25 (the `severe` anchor from `canonical-values.md` §1; matches the training-window p95 for these features). Duration window: sustained across 3 consecutive daily checks. Human-in-the-loop: yes — the Demand Planner reviews the drift report in the Viewer's Drift panel and either opens a retraining ticket or signs off. We are NOT auto-retraining; the $40/$12 asymmetry means a bad retrain is worse than waiting a day.

### 1 / 4 — Phase 13

> If data changes or MAPE goes above 15%, retrain automatically.

Why 1/4: "if data changes" is the canonical 0 anchor from `rubric-grader.md` §1.2; auto-retraining is a `rules/agent-reasoning.md` violation ("Auto-retrain when MAPE > 15%" from `rubric-grader.md` §5).

---

## How to use these examples

1. Before you write any journal entry, read the 4/4 example for each dimension the phase applies to (see `specs/rubric.md` §1.3 applicability matrix).
2. Write your entry. Then read the matching 1/4 example and check you did not accidentally match any of its anti-patterns.
3. If the grader scores you low on a dimension, return to this file: the worked 4/4 is the appeal-proof target.
