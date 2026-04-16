<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Northwind Control Tower — Product Brief

Workshop product: a supply-chain **Control Tower** for Northwind Logistics. By the end of the 210-minute workshop you will have shipped three working modules (Demand Forecaster, Route Optimizer, Drift Monitor) against a real backend, and defended a page of written decisions that explain why you shipped them that way.

Read this before writing your first prompt. Every dollar figure here is cited by the rubric and the contract grader; making them up in a journal entry scores zero.

## 1. Business context

Northwind Logistics runs 3 Singapore depots, 500 regular customers, a fleet of 20 vehicles, and delivers roughly 12,000 orders per day. Two years of daily demand history sit in `data/northwind_demand.csv`. The team has been forecasting by spreadsheet and is asking whether a data-driven Control Tower would cut cost, raise reliability, and tell them when to stop trusting the model. Your job during the workshop is to commission Claude Code to build the product, make the calls the tool cannot make for you, and write the journal that proves you made them.

Two planes run in parallel: the **Trust Plane** is where you decide (which model, what threshold, when to reverse course); the **Execution Plane** is Claude Code writing the code. If a question is _what_ or _how_, route it to the Execution Plane. If it is _which_, _whether_, _who wins_, or _is it good enough to ship_, it stays with you.

## 2. Cost table (ground truth — use these exact numbers)

These numbers come from `specs/canonical-values.md` §6. Every journal entry that names dollar asymmetry must cite from this table. The stockout-to-overstock ratio is fixed at **$40 / $12 = 3.3 : 1**.

| Cost term                   | Value        | Unit                        | Where it shows up                            |
| --------------------------- | ------------ | --------------------------- | -------------------------------------------- |
| Stockout cost               | $40          | per unit short of demand    | Phase 6 metric weighting; Phase 10 objective |
| Overstock cost              | $12          | per unit of excess capacity | Phase 6 metric weighting; Phase 10 objective |
| Late-delivery SLA violation | $220         | per violation               | Phase 7 Safety red-team; Phase 10 objective  |
| Driver overtime             | $45          | per hour                    | Phase 10 objective; `union-cap` scenario     |
| Fuel                        | $0.35        | per km                      | Phase 10 objective                           |
| Carbon                      | $8           | per kg CO2                  | Phase 10 ESG objective; `lta-carbon-levy`    |
| Peak season                 | Q4 (Oct–Dec) | seasonal window             | Phase 1 framing; Phase 13 drift context      |

## 3. Personas (who you are serving)

From `specs/product-northwind.md` §3. You play the Student role and commission the Execution Plane on behalf of the three Trust Plane personas below.

| Persona        | Plane           | What they do                                                                         | What they read                         |
| -------------- | --------------- | ------------------------------------------------------------------------------------ | -------------------------------------- |
| Ops Manager    | Trust Plane     | Approves tomorrow's plan; decides go / no-go on deploy                               | Dashboard, journal, daily digest       |
| Demand Planner | Trust Plane     | Tracks forecast accuracy; owns model health                                          | Leaderboard, drift chart               |
| Dispatcher     | Trust Plane     | Reads routes; adjusts for real-world events                                          | Route map, time-window violations      |
| ML Engineer    | Execution Plane | Ships training pipeline, registry, drift monitor (= Claude Code during the workshop) | Logs, ExperimentTracker, ModelRegistry |
| Student (you)  | Trust Plane     | Commissions every piece; graded on journal + contract grader                         | Viewer Pane, terminal, `PLAYBOOK.md`   |

## 4. 3:30 pm success definition

By the close of the workshop (15:30 wall-clock), a passing run looks like this. Every item is grader-verifiable or rubric-verifiable.

- [ ] All five product endpoints answer the contract grader with real data (not `{"status":"ok"}` stubs): `/forecast/train`, `/forecast/compare`, `/forecast/predict`, `/optimize/solve`, `/drift/check`.
- [ ] At least 11 journal entries exist at `journal/phase_<N>_<slug>.md`. Each one names its signal, threshold, and duration window under `## Reversal condition` — never the phrase "if data changes".
- [ ] The `union-cap` scenario injection at 02:05 produced both `data/route_plan_preunion.json` and `data/route_plan_postunion.json`; the Phase 11 re-run journal classifies overtime as a **hard** constraint with a penalty named in dollars.
- [ ] The `drift-week-78` scenario at 02:40 produced a Phase 13 journal entry that names a signal (e.g. PSI on the top-3 features), a numeric threshold (grounded in the training-window p95), and a duration window (e.g. "sustained for 3 consecutive days").
- [ ] `metis journal export --output journal.pdf` renders without silent degradation. If `pandoc` or LaTeX is missing, the fallback HTML + Markdown export is annotated with the reason.

Combined score target: ≥ 0.60 (60% journal rubric mean + 40% contract grader).

## 5. Where to go next

- `START_HERE.md` — student manual with the opening prompt and the Phase 1 entrypoint.
- `PLAYBOOK.md` — 12-phase-in-Week-4 procedure, prompts, and per-phase journal schemas.
- `specs/business-costs.md` — the canonical cost table above, as a short reference.
- `specs/rubric.md` — what 4/4 looks like on each of the five rubric dimensions.
- `journal/_examples.md` — worked 4/4 and 1/4 entries per rubric dimension, using the $40 / $12 / $220 / $45 numbers from the table above.
