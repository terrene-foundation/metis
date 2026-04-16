<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# START HERE — Week 4: Supply Chain Control Tower

**Version:** 2026-04-16 · **License:** CC BY 4.0

> A 3.5-hour workshop where **you commission and ship a full ML-powered product** — forecasting, optimization, and drift monitoring — **without writing a single line of code**. Claude Code builds. You direct, evaluate, decide, and defend.

This document is your manual for today. Read sections 0–3 before class. Keep this open in a tab throughout the session and refer back when stuck.

---

## 0. Five-Minute Orientation

### What you will walk away with today

1. **A deployed product.** A working Northwind Logistics Control Tower (dashboard + API + ML services) running at a URL you can share.
2. **A decision journal PDF.** A signed record of every ML judgment call you made today, scored on our 5-dimension rubric.
3. **A reusable ML Decision Playbook** — a 14-phase procedure you will apply to every product you build in Weeks 5, 6, 7, and 8, and to every ML-powered thing you commission in your career.
4. **Consolidation** of the supervised ML content from Weeks 2–3 and the new optimization + MLOps content for Week 4.

### What you will NOT do today

- Write Python, JavaScript, SQL, or any other code.
- Install libraries, configure environments, debug stack traces.
- Memorize "what is XGBoost" or "how does gradient boosting work."

### What you **will** do

- **Prompt** Claude Code through your terminal.
- **Read** the Viewer Pane as outputs arrive.
- **Evaluate** what Claude Code produced — was it good work? honest work? complete work?
- **Decide** the judgment calls that only a human can own (metric, threshold, constraints, deployment gate, retrain trigger).
- **Journal** every decision with a short memo justifying it.

### The bargain this course offers

We are not teaching you to build. We are teaching you to **commission, judge, and ship ML products as a one-person team.** Claude Code is your engineer, your data scientist, your DevOps. You are the founder. Your differentiating skill is knowing **what to ask, how to read the answer, and when to say "ship it" or "do it again."**

---

## 1. The Two Planes You Operate Across

Everything today (and every week onward) splits into two planes:

| Plane               | Who does it              | What they produce                                   | Examples                                                                                                                                                                                    |
| ------------------- | ------------------------ | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Trust plane**     | You — the human          | Judgment, framing, evaluation, approval             | "Optimize recall, not accuracy, because a missed stockout costs 7× a false alarm." "Driver hours is a hard constraint; delivery speed is soft." "Retrain when MAPE drifts >15% for 3 days." |
| **Execution plane** | Claude Code + frameworks | Code, trained models, APIs, dashboards, deployments | Nexus endpoints, kailash-ml pipelines (TrainingPipeline, AutoMLEngine, DriftMonitor), OR-Tools route solver runs, ExperimentTracker runs, Next.js dashboards                                |

### Why this split matters

In the old world, a manager asked a data scientist for a model, waited weeks, got a slide deck, and could not tell if the model was any good. In the AI-native world, **the slide deck is ten prompts away and the model is twenty prompts away** — which means the bottleneck moves to **asking the right questions and evaluating the answers**. That is the trust plane. That is your job.

If you cannot frame the problem, pick the metric, defend the threshold, classify the constraints, or approve the deployment — the AI is driving, not you. That is the failure mode. Today we train you out of it.

### The rule of thumb for today

> If the question is **what** or **how**, let Claude Code answer it.
> If the question is **which**, **whether**, **who wins and who loses**, or **is it good enough to ship** — that is yours.

---

## 2. The Product You Are Shipping: Northwind Logistics Control Tower

### What it is

A last-mile delivery operator's control dashboard. Three modules on one screen:

1. **Demand Forecaster** — predicts order volume by region for the next 7 days. Feeds the optimizer.
2. **Route Optimizer** — plans tomorrow's deliveries. Takes the forecast + vehicle/driver constraints → produces an optimal route plan.
3. **Drift Monitor** — watches whether the forecast model is still accurate in production, and tells you when to retrain.

### Who uses it

- **Ops Manager**: approves tomorrow's plan, overrides when needed
- **Demand Planner**: tracks forecast accuracy, owns model health
- **Dispatcher**: reads routes, adjusts for real-world events

### What "shipped" looks like at 3:30 pm

- A running dashboard at `http://localhost:3000` (or your sandbox URL)
- A running API at `http://localhost:8000` with `/forecast/*`, `/optimize/*`, `/drift/*` endpoints
- A `journal.pdf` in your workspace with all of today's decision memos

### The business context (for framing decisions)

- Northwind handles ~12,000 orders/day across 3 depots, 500 regular customers, 20 vehicles
- Each **stockout** (late order because we under-forecasted) costs **$40** in penalties + customer goodwill
- Each **overstock** (excess vehicle capacity deployed) costs **$12** in wasted driver hours
- Each **late delivery** (violated time window) costs **$220** (SLA penalty + re-delivery)
- Each **driver overtime hour** costs **$45** + union risk
- Peak season is Q4; drift has historically hit around week 40 every year

These numbers drive your decisions in phases 6 (metric + threshold), 10 (objective function), and 13 (retrain trigger). Keep this section open in a tab — every prompt template below that reads "use the numbers in `specs/business-costs.md`" is citing these exact figures.

---

## 3. Your Toolset — Each Explained

For every tool below, you get six answers:

- **What is it** (1–2 sentences, plain language)
- **Why do we need it** (what problem does it solve)
- **Implications** (what it means for your product)
- **How to use it** (what you actually type)
- **How to evaluate it** (how you judge whether it did good work)
- **How to improve it** (what to ask next when it falls short)

### 3.1 Claude Code (your terminal agent)

**What is it.** An AI coding agent running in your terminal. You type natural-language requests; it reads files, writes code, runs commands, and reports back. It has access to every tool your laptop has (file system, Python, Node, Git, Docker, databases).

**Why do we need it.** It is your engineering team. Without it, you could not ship a product in 3.5 hours. With it, you can. It turns "I need a forecast API" into a running forecast API in minutes.

**Implications.** Because Claude Code will do _whatever you ask_, the quality of your product equals the quality of your prompts plus the quality of your evaluation. A vague prompt produces a plausible-looking but shallow answer. A precise prompt with evaluation criteria produces defensible work. You are the bottleneck — not the AI.

**How to use it.**

- Open a terminal. Type `claude` to start a session in your workspace.
- Give it instructions in plain language: _"Train five candidate forecast models for Northwind demand using `kailash_ml.AutoMLEngine`, auto-logging to `ExperimentTracker`, and summarize the trade-offs for a non-technical executive."_
- Use slash commands to step through the COC workflow: `/analyze`, `/todos`, `/implement`, `/redteam`, `/codify`.
- **Reference files with the `@` prefix** — typing `@PLAYBOOK.md` in your message to Claude Code pulls that file's contents into the conversation so Claude can read it. This is Claude Code syntax, not shell syntax — it works inside the `claude` session only. Example: `Read @PRODUCT_BRIEF.md and summarise the cost table.`

**How to evaluate it.** After every response, ask yourself:

1. Did it actually do the work, or did it describe doing the work? (If the latter: push back.)
2. Did it cite specific files, numbers, rows, runs — or did it wave at generalities? (Specifics = real work; generalities = hand-waving.)
3. Did it acknowledge uncertainty where there is any? (A response with zero uncertainty is a response you cannot trust.)
4. Did it ask for clarification where your brief was genuinely ambiguous? (Silent assumption is a red flag.)

**How to improve it.** When the answer is thin:

- Ask _"show me the numbers, not the summary."_
- Ask _"what are three ways this could be wrong?"_
- Ask _"what assumptions did you make that I should approve or overrule?"_
- Paste in the relevant business numbers and ask it to re-reason with them.

### 3.2 The Viewer Pane (your dashboard)

**What is it.** A read-only web dashboard running on your laptop. It watches your workspace and renders the current state of your product: trained models, forecast charts, route maps, drift alerts, decision journal.

**Why do we need it.** Terminal output is text. Decisions about models, routes, and drift need to be read visually — a confusion matrix, a PR curve, a route map. The Viewer Pane is your cockpit.

**Implications.** The Viewer Pane is **part of the product you are shipping** — it is the dashboard a real Ops Manager would use. But _you_ also use it live to evaluate Claude Code's output. It has a dual role: product artifact + your evaluation instrument.

**How to use it.** Open `http://localhost:3000` in a browser tab next to your terminal. As Claude Code writes files to the workspace, the Viewer auto-refreshes. You do not click anything in it today — it is a viewer, not a control surface. (Later weeks may add controls.)

**How to evaluate it.** After each sprint, ask: is the information presented **decision-ready**? Does the leaderboard show me the numbers I need to pick a model? Does the route map show constraint violations? If not, prompt Claude Code to improve the panel.

**How to improve it.** _"Add a cost column to the leaderboard using FP=$40, FN=$220."_ _"Overlay violated time windows on the route map in red."_ _"Add a 7-day rolling MAPE to the drift chart."_

### 3.3 The Decision Journal

**What is it.** A simple file-backed log where you record every judgment call you make today. Each entry has: phase, decision, rationale, trade-off, reversal condition, timestamp.

**Why do we need it.** Because the **journal is what you are graded on** (60% of today's grade). It is also your portfolio — by Week 8, it is a 50-page record of your ML decision-making that you can show a CEO or a VC.

**Implications.** If you decide something without journaling it, it did not happen. If your rationale fits in one line, the decision was probably too shallow. If your reversal condition is "I would change my mind if the data changed," you did not think hard enough — name a specific threshold.

**How to use it.** Two ways:

- From the terminal: `metis journal add` opens an editor with a template.
- By asking Claude Code: _"Add a journal entry for my threshold decision: 0.38, because a missed stockout costs 7× a false alarm at peak season; I would change my mind if stockout cost drops below $15."_

**How to evaluate it.** Re-read each entry against these five dimensions (the grading rubric):

1. Harm framing — whose cost, in named units?
2. Metric→cost linkage — did you tie the metric to money?
3. Trade-off honesty — what did you sacrifice?
4. Constraint classification — hard vs. soft?
5. Reversal condition — what specific signal would flip your mind?

**How to improve it.** If an entry scores <3 on any dimension, ask Claude Code: _"Challenge this journal entry as if you were a board member. What would you push back on?"_ Then rewrite.

### 3.4 kailash-nexus (your backend framework)

**What is it.** A Python framework for building multi-channel APIs (HTTP, WebSocket, CLI, MCP) for ML-powered products. Think: an opinionated toolkit that spins up a production-grade backend with authentication, session management, and rate limiting already wired in.

**Why do we need it.** Your product needs a backend so the dashboard, the forecast service, the optimizer, and the drift monitor can all talk to each other. Writing that backend from scratch would eat your whole 3.5 hours. Nexus gives you a template so Claude Code can populate endpoints in minutes.

**Implications.** Because Nexus handles plumbing, your prompts can focus on _what the endpoint should do_ instead of _how to stand up a web server_. It also means every student's backend looks similar, so an instructor can unblock any student quickly.

**How to use it.** You do not interact with Nexus directly. You prompt Claude Code: _"Using kailash-nexus, stand up the forecast endpoints: POST /forecast/train, GET /forecast/compare, POST /forecast/predict. Log requests to the decision journal."_ Claude Code wires it.

**How to evaluate it.**

- Can you `curl` each endpoint and get a sane response? (Claude Code will run the curl for you.)
- Does the Viewer Pane pull data from these endpoints live?
- Does each endpoint log what it did, so you can audit later?

**How to improve it.** _"Add request validation to /forecast/train so it rejects malformed payloads."_ _"Add a /health endpoint that checks the model is loaded and the database is reachable."_

### 3.5 kailash-ml (your ML framework — training, tracking, diagnostics, drift)

**What is it.** The Kailash Python SDK's end-to-end ML framework. It replaces the old stack of sklearn + MLflow + PyCaret with a single, opinionated toolkit where every piece (training, experiment tracking, AutoML, diagnostics, drift monitoring, model registry) is one import away and talks to the others natively.

**Why do we need it.** So you can commission ML work by _saying what you want_, not by stitching together five libraries. Without it, Claude Code would have to write ~300 lines of glue per model. With it, a single prompt trains multiple candidates, tracks them, diagnoses them, and hands you a comparison.

**The components you'll touch today (all from `from kailash_ml import ...`):**

| Component           | What it does                                                                                                                                                                                                                     | Replaces                  |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| `TrainingPipeline`  | Trains any supervised model on a schema + dataset; auto-logs to ExperimentTracker                                                                                                                                                | Hand-written sklearn code |
| `AutoMLEngine`      | Trains and tunes **multiple model families in parallel** with grid / random / Bayesian / successive-halving search; returns a ranked leaderboard                                                                                 | PyCaret                   |
| `ExperimentTracker` | Logs every run (params, metrics, artifacts, timing); queryable via `list_runs`, `get_best_run`, `compare_runs`; MLflow-compatible export                                                                                         | MLflow server             |
| `ModelRegistry`     | Versions models; promotes through lifecycle stages `staging` · `shadow` · `production` · `archived` (see transition table below); SHA256 integrity on load                                                                       | Home-grown registry       |
| `InferenceServer`   | Exposes a registered model behind a Nexus endpoint — the canonical way to serve predictions in production                                                                                                                        | Hand-rolled Flask/FastAPI |
| `DriftMonitor`      | Statistical drift tests (PSI, KS) with 3-value severity ratings ("none"/"moderate"/"severe") + human-readable recommendations — you write the retrain rule from those outputs. See `specs/canonical-values.md §1` for thresholds | Custom drift scripts      |
| `ModelExplainer`    | Feature importance + SHAP global/local/dependence plots                                                                                                                                                                          | Standalone SHAP setup     |
| `DataExplorer`      | Statistical profiling, outlier detection, alerts — before you train                                                                                                                                                              | Pandas boilerplate        |
| `ModelVisualizer`   | Learning curves, confusion matrices, ROC/PR curves, residual plots                                                                                                                                                               | Matplotlib glue           |
| `FeatureEngineer`   | Auto-generates + selects + ranks features                                                                                                                                                                                        | Manual feature work       |

**Implications.**

- You can **compare 5 model families in one prompt** — LinearRegression, Ridge, RandomForestRegressor, GradientBoostingRegressor, XGBoostRegressor (requires `kailash-ml[xgb]` extra) or CatBoost (requires `kailash-ml[catboost]` extra) — without re-engineering.
- Every run is **auto-tracked** by `ExperimentTracker`; you cite run IDs in your journal.
- **Diagnostics are native** — learning curves, SHAP plots, drift reports — not a bolt-on. Your evaluations are grounded in the same artifacts the model shipped with.
- You do **not** need to understand how XGBoost works internally. You need to understand **which model's results imply production risk vs. production fit**.
- **Human approval gates** are built in: `AutoMLEngine` has `auto_approve=False` by default, so LLM-suggested search spaces require your sign-off — a concrete mechanism by which the framework respects your decision authority.

**Model Registry stage transitions** (for Phase 8 deployment gate):

| From         | Legal destinations                  |
| ------------ | ----------------------------------- |
| `staging`    | `shadow`, `production`, `archived`  |
| `shadow`     | `production`, `archived`, `staging` |
| `production` | `archived`, `shadow` (rollback)     |
| `archived`   | `staging`                           |

Note `shadow` is a peer of `staging`/`production`, not a stop on a linear path — it's where you run a new model alongside production to compare before promoting.

**How to use it.** Prompt Claude Code:

> _"First ingest `data/northwind_demand.csv` into a `FeatureStore` using the schema in `specs/schemas/demand.py`. Then build an `AutoMLConfig(task_type='regression', metric_to_optimize='mape', search_strategy='bayesian', search_n_trials=30, auto_approve=False)` and instantiate `AutoMLEngine(feature_store=fs, model_registry=registry, config=config)`. Candidate families: LinearRegression, Ridge, RandomForestRegressor, GradientBoostingRegressor, plus XGBoostRegressor if the `[xgb]` extra is available (fall back to GradientBoostingRegressor variants if not). Use rolling-origin time-series splits. Register the top 3 runs in `ModelRegistry` at stage='staging'. Write `list_runs` output to `leaderboard.json` and render in the dashboard."_

**How to evaluate what it produces.**

- Are all candidates trained on the **same splits** and the **same schema**? (If not, the comparison is invalid.)
- Is the winning model winning by a **meaningful margin** (multiple percent) or by **noise** (0.3%)?
- Does the winning model's **complexity match the problem's complexity**? (A 500-tree XGBoost beating LinReg by 0.3% MAPE is probably overfit — prefer the simpler model.)
- Did `DataExplorer` flag anything before training that should have stopped the pipeline?
- Did `ModelExplainer` surface one feature with disproportionate importance? (Possible leakage.)

**How to improve what it produces.**

- _"Add a naive baseline (predict last-week's demand). Show how much each ML candidate beats that baseline by — if the lift is <5%, recommend the baseline."_
- _"Re-run with a 30-day rolling-origin holdout instead of K-fold — I want forward-looking validation."_
- _"Run `ModelExplainer` on the top model and highlight any feature contributing >40% of importance; that's a leakage smell."_

### 3.6 OR-Tools + PuLP (your optimization solvers)

**What is it.** Two open-source Python libraries that solve optimization problems. **OR-Tools** is Google's toolkit with a powerful Vehicle Routing Problem (VRP) solver; **PuLP** is a simple interface for Linear Programming (LP). Neither is part of kailash-ml — kailash-ml covers ML (predict), these cover optimization (prescribe). Claude Code calls them directly.

**Why do we need it.** Supervised ML predicts "what will happen." Optimization decides "what should we do." The optimizer takes your forecast and turns it into a plan — which truck goes where, in what order, by when — subject to capacity, time windows, and driver hours.

**Implications.** Optimization is where Week 4's new content lives. The solver needs three things from you:

1. An **objective function** (what to minimize or maximize — e.g. total cost, total distance, SLA violations).
2. A set of **constraints** (what must be true — capacity, hours, legal rules).
3. **Weights or priorities** when you have multiple competing goals.

All three are **your decisions**, not the solver's. The solver executes; you design the problem.

**How to use it.** Prompt Claude Code:

> _"Using OR-Tools VRP (`ortools.constraint_solver.pywrapcp`), solve tomorrow's route plan over `forecast_output.json`. Objective: minimize `(fuel_cost × distance) + ($220 × late_deliveries) + ($45 × overtime_hours)`. Hard constraints: vehicle capacity 40 pallets, driver hours ≤ 9/day. Soft constraints: prefer deliveries before 5pm (penalty $15/hour late). Time budget 30 seconds. Log the plan + solver gap to `route_plan.json` and the OR-Tools run to ExperimentTracker (tag `phase=optimize`)."_

**How to evaluate what it produces.**

- Is the solution **feasible** (no hard constraint violated — confirm each)?
- Did the solver **converge** within the time budget, or did it time-out on a heuristic?
- What is the **optimality gap**? (Solver reports this.)
- Are there **pathological edges**? One truck doing 95% of the work; a driver sent on a 12-hour route on paper; a vehicle visiting the same street four times.
- Does the plan match a **human dispatcher's intuition**?

**How to improve what it produces.**

- _"Add a fairness constraint: no driver routes more than 20% longer than the shortest driver's route."_
- _"Raise the late-delivery penalty to $350 and re-solve; tell me which routes changed."_
- _"Current objective ignores carbon — add `$8 × kg_CO₂` and report the new plan's delta on cost, SLA, and carbon."_

### 3.7 ExperimentTracker (inside kailash-ml)

**What is it.** kailash-ml's native experiment tracking component. Replaces MLflow-server workflow. Every training run, AutoML trial, and drift check is auto-logged: parameters, metrics, artifacts, timing, model class, nested parent/child runs for sweeps.

**Why do we need it.** You will trigger dozens of training runs today. Without a log, you cannot answer "which run was my best XGBoost?" or "did Run 47 overfit vs. Run 48?" ExperimentTracker is your audit trail — and your evidence when you defend a model choice in the journal.

**Implications.** Every decision you journal should cite a **specific ExperimentTracker run ID**. "I picked run `xgb_007` (MAPE 6.2%, training 14s, 6 folds stable within ±0.4%)" is defensible. "I picked XGBoost" is not.

**How to use it.** It logs automatically when you invoke `TrainingPipeline` or `AutoMLEngine`. To query: prompt Claude Code:

> _"Using `ExperimentTracker`, list the top 5 runs from Sprint 1 ranked by business-cost-weighted MAPE. Show params, fold variance, and training time. Export the comparison to `sprint1_leaderboard.json`."_

For MLflow-compatible export (if you ever want to open runs in an MLflow UI): _"Export the last 20 ExperimentTracker runs to MLflow format at `mlruns/`."_

**How to evaluate what it produces.**

- Are **all** your runs logged? (`list_runs` count should match runs you triggered.)
- Did Claude Code use **consistent parameter names** across runs so they are directly comparable?
- Are **artifacts** (diagnostic plots, feature importances) attached to each run, or only metrics?

**How to improve what it produces.**

- _"Tag all runs from Sprint 1 with `sprint=forecast` so I can filter by sprint."_
- _"Add a business-cost custom metric to every run: `cost = $40 × under_forecast_units + $12 × over_forecast_units`."_
- _"Promote the top run to `staging` in the ModelRegistry so the deployment gate in phase 8 has a concrete artifact to sign off on."_

---

## 4. The ML Decision Playbook

The Playbook is a **14-phase universal procedure** you apply every time you commission an ML-powered feature. Today you run phases 1–13 (fairness, phase 14, arrives in Week 7). Every week after today, you will run this same Playbook on a new domain.

**Core idea**: every ML product flows through the same decision checkpoints. If you learn the checkpoints, you can commission anything.

The Playbook file lives at `workspaces/metis/PLAYBOOK.md`. Copy it into today's workspace at the start of class.

### How to run a phase

Each phase has three pieces:

1. **The prompt template** — what you type to Claude Code to execute the phase.
2. **The evaluation checklist** — what "good" looks like, so you can judge Claude Code's output.
3. **The journal entry** — what you record when you decide.

### The 14 phases at a glance

| #   | Phase                         | Trust-plane question                                                      | Output                              |
| --- | ----------------------------- | ------------------------------------------------------------------------- | ----------------------------------- |
| 1   | **Frame**                     | What is the target, the population, the horizon, the cost of being wrong? | Problem statement                   |
| 2   | **Data audit**                | Is this data trustworthy? (leakage, bias, imbalance, missingness)         | Data acceptance memo                |
| 3   | **Feature framing**           | Which features are available, leaky, or ethically loaded?                 | Feature list with in/out decisions  |
| 4   | **Model candidates**          | Which 3–5 models are reasonable?                                          | Candidate list                      |
| 5   | **Model implications**        | Given the leaderboard, which model do I stake my career on, and why?      | Model selection memo                |
| 6   | **Metric + threshold**        | Which metric, which threshold, tied to what costs?                        | Threshold memo                      |
| 7   | **Red-team**                  | How does this model fail?                                                 | Vulnerability report + dispositions |
| 8   | **Deployment gate**           | Ship / don't ship, and on what monitoring?                                | Go/no-go memo                       |
| 9   | **Codify**                    | What transfers to the next domain?                                        | Playbook delta                      |
| 10  | **Objective function**        | Single or multi-objective? What are the weights?                          | Objective memo                      |
| 11  | **Constraint classification** | Hard or soft for each rule? Penalties for soft?                           | Constraint table                    |
| 12  | **Solver acceptance**         | Is the solution feasible, optimal, edge-case safe?                        | Acceptance memo                     |
| 13  | **Drift triggers**            | When do we retrain? What's the rule?                                      | Retrain rule memo                   |
| 14  | **Fairness audit**            | _(deferred to Week 7)_                                                    | —                                   |

### Deep dive on the phases you run today

Each phase below gives you the prompt template, the checklist, and the journal schema.

---

#### Phase 1 — Frame

**What**: translate the business brief into a precise ML problem statement.

**Why**: ML teams waste months solving the wrong problem. Framing is the cheapest place to catch that error.

**Implications**: the target variable, the population, the prediction horizon, and the cost-of-error asymmetry are **all your decisions**. Get them wrong and every subsequent phase is working on the wrong problem.

**Prompt template**:

> _"`/analyze` — Read `PRODUCT_BRIEF.md` and produce a one-paragraph ML problem statement for the Forecast module. Include: target variable, unit of prediction, population scope, prediction horizon, and cost asymmetry (cost of over-forecasting vs. under-forecasting in named units)."_

**Evaluation checklist**:

- [ ] Target variable named precisely (not "demand" but "number of orders per depot-day")
- [ ] Population scope explicit (all depots? only active customers? peak-season only?)
- [ ] Horizon named (1 day? 7 days? 30 days?)
- [ ] Cost asymmetry quantified ($40 stockout vs. $12 overstock → 3.3:1 asymmetry)
- [ ] No silent assumptions

**Journal schema**:

```
Phase 1 — Frame
Target: ____
Population: ____
Horizon: ____
Cost asymmetry: ____
What I would change my mind on: ____
```

---

#### Phase 2 — Data Audit

**What**: interrogate the dataset for trustworthiness before any modeling.

**Why**: "garbage in, garbage out" is the #1 cause of ML failure. A leaky feature in training data produces a model that looks perfect but collapses in production.

**Implications**: you must verify six categories of trouble: label quality, temporal leakage, survivorship bias, class imbalance (for classification) / distribution shift (for regression), missingness pattern, and proxy variables. All six are your call.

**Prompt template**:

> _"Audit the dataset at `data/northwind_demand.csv` using `kailash_ml.DataExplorer`. Use the dollar figures in §2 above — stockout $40/unit short of demand, overstock $12/unit of excess capacity, late-delivery SLA $220/violation — as the grounding for cost-of-error reasoning: a label-quality defect or leakage vector in this data translates directly into those dollars when the model ships. For each of these six categories, report findings: label quality, temporal leakage, survivorship bias, distribution across time, missingness pattern, suspected proxy variables. Show me specific rows and numbers, not generalities. Then list every candidate feature and classify each on four axes: (a) available at prediction time, (b) leaky with evidence, (c) ethically loaded, (d) engineered or raw. For any ethically-loaded feature (e.g. customer segment, region), give a defensible rationale — not a drive-by 'OK'. Recommend an initial feature set; I will decide."_

**Evaluation checklist**:

- [ ] All 6 categories addressed with specifics
- [ ] Any flagged issue has a concrete example (row X, column Y)
- [ ] Recommendations offered but not auto-applied (you decide)
- [ ] Findings tied back to the $40 / $12 / $220 cost grounding when cost-of-error is relevant

**Journal schema**:

```
Phase 2 — Data Audit
Accepted? Yes / Conditional / No
Conditions applied: ____
Known risks I am accepting: ____
```

---

#### Phase 3 — Feature Framing

**What**: classify features into _available at prediction time_, _leaky_, _ethically loaded_, _engineered_.

**Why**: features that are "available" in training but not at prediction time cause silent failure in production. Ethically loaded features (demographics, proxies) cause regulatory and reputational failure.

**Implications**: you rule each feature in or out. Claude Code recommends; you decide.

**Prompt template**:

> _"For the Northwind forecast problem (12,000 orders/day · 3 depots · 500 customers · 20 vehicles; stockout $40/unit, overstock $12/unit, late-delivery SLA $220/violation — see §2 above), list every candidate feature. Classify each as: (a) available at prediction time — yes/no, (b) leaky — yes/no with evidence, (c) ethically loaded — yes/no (if yes, give a defensible rationale), (d) engineered or raw (if engineered, explain the derivation). A leaky feature in this dataset translates to silent stockout-cost surprise in production, so be strict about evidence. Recommend an initial feature set. I will make the final call."_

**Evaluation checklist**:

- [ ] Every feature classified
- [ ] Leakage claims backed by specific reasoning (not "might be")
- [ ] Engineered features explained (how they were derived)

**Journal schema**:

```
Phase 3 — Features
Included: ____
Excluded (with reason): ____
```

---

#### Phase 4 — Model Candidates

**What**: pick 3–5 models to train in parallel.

**Why**: single-model bakes carry hidden risk. Comparing 3–5 candidates surfaces which trade-offs actually matter for your problem.

**Implications**: you do NOT need to know how each model works internally. You need to know **why each is a reasonable candidate** (interpretability, capacity, speed, robustness).

**Prompt template**:

> _"Propose 5 candidate regression models for Northwind demand forecasting via `kailash_ml.AutoMLEngine`. For each, give a one-sentence reason it is a reasonable candidate, and a one-sentence risk. Train them all with rolling-origin time-series CV; `ExperimentTracker` auto-logs; `DataExplorer` runs first to flag data issues; `ModelExplainer` attaches feature importances. Write the `compare_runs` output to `leaderboard.json`."_

**Evaluation checklist**:

- [ ] Candidates span a complexity range (don't train 5 variants of XGBoost)
- [ ] Each has a distinct reason for inclusion
- [ ] A simple baseline is included (e.g. "predict last week")

**Journal schema**: (none — just candidates; the decision happens in phase 5)

---

#### Phase 5 — Model Implications

**What**: compare the leaderboard and pick the model you will stake your career on.

**Why**: this is the **core ML decision skill** of this course. Picking well here means knowing what each result _implies_ about fit, generalization, and production risk — not knowing the algorithm's internals.

**Implications**: you are answering five questions:

1. Which model has the best _headline_ metric?
2. Is its advantage _meaningful_ (multiple percent) or _noise_ (fraction of a percent)?
3. Is its _variance across folds_ tight (stable) or loose (fragile)?
4. Does its _complexity_ match the problem, or is it probably overfit?
5. Can you _defend_ it to a non-technical executive in 30 seconds?

**Prompt template**:

> _"Compare the leaderboard. For each candidate, tell me: headline MAPE, fold-to-fold variance, complexity class, and training time. Then recommend one model as the deployment candidate. Frame the trade-offs as if you are briefing a non-technical executive — 90 seconds of speech."_

**Evaluation checklist**:

- [ ] All candidates compared on the same metrics
- [ ] Trade-offs are explicit, not hidden behind "XGBoost wins"
- [ ] Recommendation is defended, not asserted
- [ ] If recommending the most complex model, complexity justified

**Ask-again prompts to sharpen**:

- _"What does the fold-to-fold variance tell me about each model's robustness?"_
- _"If I picked the second-place model instead, what do I gain?"_
- _"Which of these models would fail an internal review, and why?"_

**Journal schema**:

```
Phase 5 — Model Selection
Picked: ____ (ExperimentTracker run ID: ____)
Rejected alternatives: ____
Why not the top of the leaderboard, if applicable: ____
What I would retrain with: ____
```

---

#### Phase 6 — Metric + Threshold

**What**: pick the evaluation metric that matches your business costs; set the decision threshold that turns the model's score into an action.

**Why**: accuracy is usually a lie. The right metric depends on what each kind of error costs you. The threshold is the conversion from "model score" to "do we act?" — it is the single most consequential decision in the whole product.

**Implications**: metric and threshold are **pure business decisions** dressed up as ML. A data scientist should propose options; the manager decides. That manager is you.

**Prompt template**:

> _"For Northwind demand forecasting, propose an evaluation metric linked to business cost (stockout $40, overstock $12). Then for regression: propose a prediction interval (80/90/95%) that balances overstock cost against stockout risk. Show me the cost curve across three interval widths. I will decide."_

**Evaluation checklist**:

- [ ] Metric choice is tied to dollars, not aesthetics (MAPE vs. RMSE debate resolved with cost logic)
- [ ] Interval/threshold trade-off presented as a curve, not a single recommendation
- [ ] Recommendation includes a sensitivity analysis ("at peak season these costs shift; recommend re-tuning weekly")

**Journal schema**:

```
Phase 6 — Metric + Threshold
Metric: ____ (reason: ____)
Threshold/Interval: ____
Expected business impact: $____
Sensitivity: what change flips my decision: ____
```

---

#### Phase 7 — Red-Team

**What**: try to break your own model before production does.

**Why**: every model has failure modes. Finding them here costs hours; finding them in production costs reputation.

**Implications**: you identify (a) subgroups where performance collapses, (b) features the model over-relies on, (c) time regimes where it drifts, (d) adversarial inputs that break it. Then you decide which are blockers and which are acceptable risk.

**Prompt template**:

> _"`/redteam` the chosen forecast model across three AI Verify dimensions, grounded in the business numbers in §2 above (stockout $40/unit, overstock $12/unit, SLA $220/violation). (1) **Transparency**: the single feature the model relies on most, and ablation MAPE delta if removed. (2) **Robustness**: the 3 customer segments with worst MAPE, the 3 worst calendar weeks, and quantified behaviour on the week-78 drift event. (3) **Safety**: cost in dollars of the worst 1% of predictions ($40 × under-forecast-units + $12 × over-forecast-units + $220 × any SLA-violating late deliveries induced); behaviour on zero-demand days and on days missing upstream features; who is harmed if this model silently fails for a week. Rank findings by severity. Fairness (AI Verify's 4th dimension) is deferred to Week 7 per the Playbook — surface this deferral explicitly."_

**Evaluation checklist**:

- [ ] Findings are specific (named segments, named features, named weeks)
- [ ] Severity ranked with reasoning
- [ ] For each finding, a mitigation is proposed

**Journal schema**:

```
Phase 7 — Red-Team
Blockers: ____
Accepted risks: ____
Mitigations to ship with: ____
```

---

#### Phase 8 — Deployment Gate

**What**: go or no-go on shipping.

**Why**: this is the last human checkpoint before the model makes real decisions with real money.

**Implications**: you specify (a) deployment criteria, (b) day-one monitoring, (c) rollback trigger.

**Prompt template**:

> _"Write the go/no-go gate for this model. Include: (1) go criteria (MAPE < X on holdout, no HIGH red-team finding open), (2) monitoring plan (metrics to track, alert thresholds), (3) rollback trigger (what automatically reverts the deploy)."_

**Evaluation checklist**:

- [ ] Gate criteria are measurable, not vibes
- [ ] Monitoring has specific metrics and alert thresholds
- [ ] Rollback trigger is automatable

**Journal schema**:

```
Phase 8 — Deployment Gate
Go / No-Go: ____
If Go, monitoring: ____
If No-Go, what unblocks: ____
```

---

#### Phase 9 — Codify

**What**: capture what transfers to the next domain.

**Why**: the Playbook is an evolving artifact. If you learned something today that applies to retail next week, write it down.

**Prompt template**:

> _"`/codify` — For the Forecast sprint, what 3 lessons transfer to any other ML-powered product? What 2 lessons are specific to demand forecasting? Append to `PLAYBOOK.md` as a 'Week 4 delta' section."_

**Journal schema**:

```
Phase 9 — Codify
Transferable: ____
Domain-specific: ____
```

---

#### Phase 10 — Objective Function

**What**: define what the optimizer minimizes (or maximizes).

**Why**: the optimizer blindly pursues whatever you tell it to. If the objective is wrong, the plan is wrong — regardless of how good the solver is.

**Implications**: single-objective is easier; multi-objective is usually more honest. Weights are your decision.

**Prompt template**:

> _"Propose an objective function for the Northwind route optimizer. Use the business costs: fuel $0.35/km, late delivery $220, overtime $45/hour, carbon $8/kg CO₂. Show me a single-objective version (sum of costs) and a multi-objective version (cost, SLA, carbon with weights). Recommend one."_

**Evaluation checklist**:

- [ ] Every term has a cost in real money or a justified proxy
- [ ] Weights in multi-objective are defended, not assumed
- [ ] Recommendation discusses the trade-off honestly

**Journal schema**:

```
Phase 10 — Objective
Chosen: ____
Weights: ____
Why: ____
```

---

#### Phase 11 — Constraint Classification

**What**: tag each rule as hard (inviolable) or soft (preferential, with a penalty).

**Why**: hard constraints kill infeasible plans; soft constraints let the optimizer trade off. Misclassifying a soft constraint as hard can make the problem infeasible; misclassifying a hard constraint as soft can get you sued.

**Implications**: for every rule (vehicle capacity, driver hours, time windows, carbon targets, service levels) you decide hard/soft and set penalties for soft.

**Prompt template**:

> _"List every constraint the optimizer will face. For each, classify: (a) hard or soft, (b) if soft, the penalty per unit violated. Justify each classification with the business rule it encodes (law, physics, preference, policy)."_

**Evaluation checklist**:

- [ ] Legal/physical rules → hard (driver hours law, vehicle capacity)
- [ ] Preferences → soft with meaningful penalty
- [ ] No constraint left as "probably hard" without a reason

**Journal schema**:

```
Phase 11 — Constraints
Hard: ____ (reason each)
Soft: ____ (penalty each)
```

---

#### Phase 12 — Solver Acceptance

**What**: judge whether the produced plan is good enough to ship.

**Why**: a solver may converge to a locally-optimal-but-operationally-insane plan (one driver does 95% of routes; a truck visits the same street four times). You are the sanity check.

**Implications**: you review the plan against feasibility, optimality, and pathology.

**Prompt template**:

> _"Summarize tomorrow's solver output. Show: (a) all hard constraints satisfied — yes/no per constraint, (b) objective value and how close to the solver's theoretical best, (c) top 3 pathological patterns in the plan (e.g., driver imbalance, geographic zigzags, underutilized vehicles). Recommend accept / re-solve / re-design."_

**Evaluation checklist**:

- [ ] Every hard constraint confirmed satisfied
- [ ] Optimality gap reported (not just "solved")
- [ ] Human-read pathologies flagged

**Journal schema**:

```
Phase 12 — Solver Acceptance
Accepted / Re-solved / Re-designed: ____
Pathologies noted: ____
What would make me re-design: ____
```

---

#### Phase 13 — Drift Triggers

**What**: write the rule that says when to retrain.

**Why**: models decay. Without a retrain rule, a deployed model silently gets worse until customers complain.

**Implications**: you define (a) what drift signals to monitor, (b) thresholds that trigger a retrain, (c) automatic vs. human-approved retraining.

**Prompt template**:

> _"For the Northwind forecast model, first call `DriftMonitor.set_reference_data(model_id, reference_df)` on the training window, then run `check_drift` against the last 30 days. From the severity + per-feature scores + recommendations, propose the signals and thresholds the operator should monitor: 7-day rolling MAPE, feature distribution KL-divergence (from DriftMonitor), and actual-vs-predicted bias. Show the historical variance of each signal so the thresholds are grounded in data, not guesses. Recommend whether the retrain decision should be made by a human reviewer or by a policy the operator pre-approves — and justify with Northwind's operational risk tolerance."_

Notice the prompt does not ask Claude Code to encode `if X > Y trigger retrain` as a piece of agent logic — that's the kind of brittle if-else coupling the SDK discourages in agent reasoning paths. Instead it asks for the _signals and thresholds the human operator monitors_, plus a _recommendation_ on who decides. The retrain decision itself stays in the trust plane.

**Evaluation checklist**:

- [ ] Each signal has a threshold backed by historical variance
- [ ] Duration window prevents retrain-on-spike
- [ ] Human-in-the-loop reasoning defended

**Journal schema**:

```
Phase 13 — Retrain Rule
Signal(s): ____
Threshold(s): ____
Duration: ____
Human-in-the-loop: yes/no, why
```

---

## 5. ML Concepts You Need To Know Today (just-in-time theory)

For each concept: what it is, why we care, how to use it through Claude Code, how to judge the output, how to push back.

### 5.1 Supervised regression

**What**: training a model to predict a continuous number (tomorrow's order count) from past data.

**Why we need it**: the forecast module's core. Without a forecast, the optimizer has no input.

**Implications**: unlike classification (which answers yes/no), regression answers "how much." Evaluation uses _error magnitude_ metrics (MAE, MAPE, RMSE), not precision/recall.

**How to use**: _"Train regression models via kailash-ml for the Northwind daily demand target."_

**How to evaluate**: does the model's _error pattern_ match the business cost pattern? (If overstock is 3× cheaper than stockout, a model that slightly over-predicts is better than one that slightly under-predicts — even if raw MAPE is identical.)

**How to push back**: _"Re-train with an asymmetric loss that penalizes under-prediction 3× more than over-prediction."_

### 5.2 Candidate models (big-picture only)

You do NOT need to know how these work. You need to know _when each is a reasonable candidate_.

| Model                                    | Reasonable because                                            | Risk                                      |
| ---------------------------------------- | ------------------------------------------------------------- | ----------------------------------------- |
| **Linear Regression**                    | Simple, fast, interpretable — the baseline to beat            | Can't capture non-linear patterns         |
| **Ridge / Lasso**                        | Like LinReg but resists overfitting with many features        | Still linear                              |
| **Random Forest**                        | Captures non-linearity without tuning; robust to outliers     | Can over-fit small data; slower           |
| **XGBoost / GBM**                        | Usually best tabular performance; handles interactions        | Easy to overfit; hyperparameter-sensitive |
| **Naive baseline** ("predict last week") | Sanity check — if your ML doesn't beat this, you wasted money | N/A                                       |

**Rule**: always include a naive baseline. If XGBoost beats LinReg by 0.1%, prefer LinReg. If it beats it by 15%, prefer XGBoost and investigate why.

### 5.3 Evaluation metrics for regression

**MAE (mean absolute error)**: average of $|actual - predicted|$. Same unit as the target. Easy to explain.

**MAPE (mean absolute percentage error)**: MAE as a percentage. Use when relative error matters (predicting 100 vs 110 is worse than predicting 10,000 vs 10,010).

**RMSE (root mean squared error)**: penalizes large errors more than small ones. Use when big misses are disproportionately costly (e.g. one huge stockout is much worse than many small ones).

**Rule of thumb for today**: MAPE for headline; RMSE for tail-risk; cost-weighted MAPE for the actual business decision.

**How to ask**: _"Show MAE, MAPE, RMSE, and business-cost-weighted error on the holdout for each candidate."_

### 5.4 Threshold / decision boundary (regression version = prediction interval)

**What**: in regression, instead of a classification threshold, you decide how wide a prediction interval to use — e.g. order enough stock to cover the 80th percentile of predicted demand (safe) vs. the 50th (lean).

**Why**: the model gives you a distribution; _you_ decide how much of that distribution to cover. That decision translates forecast → stocking plan.

**How to ask**: _"For each prediction, give me the 50th, 80th, and 95th percentile forecast. Compute expected stockout cost and overstock cost at each."_

**How to decide**: pick the percentile that minimizes expected total cost. Usually between 60 and 85 for delivery logistics. Defend with numbers.

### 5.5 Objective function

**What**: the math expression the optimizer minimizes.

**Why**: it encodes your priorities. Everything not in the objective is invisible to the solver.

**How to ask** (single-objective): _"Objective = fuel_cost + SLA_penalties + overtime_cost."_

**How to ask** (multi-objective): _"Minimize cost AND carbon AND SLA violations; show me the Pareto frontier, then recommend a point."_

**How to decide**: if there is a single dominant cost, single-objective is fine. If two or three things trade off and no one dominates, multi-objective with explicit weights forces honesty.

### 5.6 Constraints (hard vs soft)

**Hard constraint**: if violated, the plan is invalid. Example: "driver hours ≤ 9" (legal). The solver will NEVER produce a plan that violates this.

**Soft constraint**: if violated, a penalty is added to the objective. Example: "deliver by 5pm preferred" (customer preference). Violating it is sometimes worth doing if the alternative is worse.

**Rule of thumb**: law + physics + contract-breaking = hard. Everything else = soft with a defensible penalty.

### 5.7 Linear programming intuition

You do NOT need to understand simplex or dual theory. You need to understand that LP takes (objective + constraints) and returns the best feasible point. The solver is a black box that is **honest**: it will give you exactly what you asked for — which is why phase 10 and 11 matter.

### 5.8 Drift

**Covariate drift**: the input features change distribution (e.g. customer mix shifts).
**Label drift**: the target variable distribution shifts (e.g. peak-season demand arrives early).
**Concept drift**: the relationship between features and target changes (e.g. a new competitor alters how customers respond to price).

**Why it matters**: a model trained before drift is increasingly wrong after drift.

**How to detect**: statistical tests on feature/target distributions over time (KL-divergence, PSI); rolling error rates.

**How to ask**: _"Run drift detection on the last 30 days vs. the training window. Report which type of drift, by how much, starting when."_

### 5.9 Retraining triggers

**What**: a rule that says _retrain now_.

**Why**: too often and you burn compute and destabilize production. Too rarely and the model decays silently.

**How to write one**:

- Use a sustained signal, not a spike ("7-day rolling MAPE > 15%" not "one-day spike > 20%")
- Combine multiple signals ("KL > 0.2 AND bias > 5% for 5 days")
- Prefer human-in-the-loop on first trigger; automate after confidence

---

## 6. Today's Three Sprints

### Sprint 1 — Forecast (50 min)

**Goal**: ship a deployed forecast service with a chosen model, defensible metric + interval, and signed deployment gate.
**Playbook phases**: 1, 2, 3, 4, 5, 6, 7, 8, 9.
**Deliverable**: `/forecast/*` endpoints live; leaderboard visible in dashboard; 4 journal entries (frame, model pick, metric, deployment gate).

### Sprint 2 — Optimize (50 min)

**Goal**: ship a deployed optimizer that consumes the forecast and produces a route plan.
**Playbook phases**: 10, 11, 12 + re-run 8.
**Scenario injection mid-sprint** (≈ workshop T+02:05): instructor fires `union-cap` — the MOM Employment Act circular tightens driver overtime to 5 h/week. **When it fires, you MUST re-run Phase 11 AND Phase 12, and write a journal entry for each re-run phase**:

1. **Re-run Phase 11** — re-classify the overtime constraint (it was soft with a $45/hr penalty; after the injection it is hard with a 5 h/week ceiling). Write `journal/phase_11_postunion.md`. The prior classification stays as `journal/phase_11_constraints.md`.
2. **Re-run Phase 12** — re-solve `/optimize/solve` with the re-classified constraint set and `scenario_tag: "postunion"`. The new plan is saved to `data/route_plan_postunion.json`; the pre-injection plan is preserved as `data/route_plan_preunion.json`. Write `journal/phase_12_postunion.md`. **Note: `route_plan_postunion.json` is written by Phase 12, not Phase 11** — Phase 11 only re-classifies, Phase 12 re-solves. Submitting only the Phase 11 re-run and skipping Phase 12 is the most common D3 (trade-off honesty) failure in this sprint.

**Deliverable**: `/optimize/*` endpoints live; route map visible in dashboard; 3 base journal entries (Phases 10, 11, 12) + 2 post-injection journal entries (Phase 11 post-union and Phase 12 post-union).

### Sprint 3 — Monitor (35 min)

**Goal**: ship a drift monitor with a retrain rule.
**Playbook phase**: 13 + re-run 5 and 6 on post-drift data.
**Scenario injection**: instructor fires the week-78 drift event.
**Deliverable**: `/drift/*` endpoints live; drift chart visible in dashboard; 1 journal entry (retrain rule).

---

## 7. How You Are Graded

Two layers, weighted 60/40.

### Layer 1 — Decision Journal (60%)

Each journal entry is scored on 5 dimensions, 0 / 2 / 4 each (the 1 and 3 levels are not used — the anchors force binary-plus-evidence judgements):

| Dim                        | 0                            | 2                         | 4                                                           |
| -------------------------- | ---------------------------- | ------------------------- | ----------------------------------------------------------- |
| **D1 Harm framing**        | No stakeholders named        | Names one cost            | Quantifies asymmetry in named dollars ($40 vs $12 = 3.3 :1) |
| **D2 Metric→cost linkage** | Metric chosen without reason | Reason named              | Reason is a dollar figure or dollar-equivalent              |
| **D3 Trade-off honesty**   | Picks winner, ignores loser  | Names what was sacrificed | Quantifies the sacrifice (e.g. "lost 0.8% MAPE")            |
| **D4 Constraint classify** | Unclear hard/soft            | Labelled correctly        | Penalty (in dollars) + reasoning included                   |
| **D5 Reversal condition**  | "If data changed"            | Names a signal            | Names signal + threshold + duration window                  |

Average across all today's entries. Target: ≥ 3.0 on average to pass.

#### Worked examples per dimension (read before writing your first entry)

The side-by-side pairs below come from `journal/_examples.md` (full set lives there). Each pair uses the Phase 6 (Metric + Threshold) entry, because Phase 6 is the one phase that pressures all five dimensions in a single memo.

**D1 — Harm framing.** 4/4 names dollars in both directions and computes the ratio; 1/4 names none.

- **4/4**: _"Stockouts cost $40/unit short of demand (customer goodwill + penalties); overstocks cost $12/unit of excess capacity (wasted driver hours + fuel). Asymmetry is $40 : $12 = 3.3 : 1, so a symmetric metric will systematically under-price stockouts."_
- **1/4**: _"We want to avoid stockouts and overstocks."_

This is the H11 canonical example. "Quantifies asymmetry in named units" means the two dollar figures appear, the ratio is computed, and the direction of the asymmetry is stated — not just "costs more."

**D2 — Metric→cost linkage.** 4/4 ties the metric choice to a dollar figure; 1/4 picks on aesthetics.

- **4/4**: _"Cost-weighted MAPE with under-forecast weight = 40 and over-forecast weight = 12, averaged over depot-days. A symmetric MAPE would over-value over-forecasting because $40 > $12."_
- **1/4**: _"MAPE, because it's a percentage so it's easy to explain."_

**D3 — Trade-off honesty.** 4/4 names what was sacrificed in units; 1/4 only names the winner.

- **4/4**: _"Picked Ridge over RandomForest. Sacrificed 0.8% MAPE (5.9% vs 5.1%) to gain tighter fold-to-fold variance (±0.3% vs ±1.1%) and 6× faster training. In peak Q4, RF's fragility would cost more than the MAPE gain."_
- **1/4**: _"Picked Ridge because it performed well."_

**D4 — Constraint classification.** 4/4 labels, names the dollar penalty, and justifies with the business rule; 1/4 labels only.

- **4/4**: _"Driver overtime cap: HARD after the union-cap injection (MOM Employment Act circular), 5 h/week ceiling. Violation = legal exposure, not a monetised penalty — hence hard, not a $X/hr soft term."_
- **1/4**: _"Overtime: hard."_

**D5 — Reversal condition.** 4/4 names signal + threshold + duration; 1/4 waves at "if data changes."

- **4/4**: _"Retrain when 7-day rolling MAPE exceeds training-window p95 for 3 consecutive days AND `customer_mix` PSI > 0.25. The 3-day window prevents retrain-on-spike."_
- **1/4**: _"If data changed, I'd re-run."_

The Phase 6 4/4 entry that scores the full 16/16 on the 4 applicable dimensions of the $40/$12 reasoning path lives in `journal/_examples.md`; the matching 1/4 first-draft version is on the facing page. Read both before writing Phase 6.

### Layer 2 — Product Shipped (40%)

Binary checks:

- [ ] Dashboard loads at `http://localhost:3000`
- [ ] `/forecast/train`, `/forecast/compare`, `/forecast/predict` return 200
- [ ] `/optimize/solve` returns a feasible plan
- [ ] `/drift/check` returns a drift report
- [ ] `journal.pdf` exports cleanly

Each = 20% of the product grade; partial credit for partial functionality.

---

## 8. When You Get Stuck

Escalation ladder (try each before the next):

1. **Re-prompt Claude Code more precisely.** Nine times out of ten, a stuck moment is a vague prompt. Add the business numbers. Add the file paths. Add the evaluation criteria.
2. **Check this document** (section 3 for tools, section 4 for playbook, section 5 for concepts).
3. **Check the PLAYBOOK.md** in your workspace.
4. **Ask a neighbor** — compare prompts.
5. **Flag the instructor** — wave, don't shout.

### Common pitfalls

- **"Claude Code said it trained the models but I see nothing in the dashboard."** → It probably described the work instead of doing it. Prompt: _"Show me the actual files you wrote and run the training now."_
- **"The leaderboard has one model."** → You asked for "a model" instead of "5 candidates." Re-prompt with the exact list.
- **"The solver says infeasible."** → A hard constraint is too tight. Re-classify one as soft and re-run.
- **"The dashboard doesn't update."** → Ask Claude Code to trigger the Viewer's refresh endpoint.
- **"I don't know which metric to pick."** → Go back to the business numbers. Ask: _"Given cost asymmetry 3.3:1, which metric matches?"_
- **`"/forecast/train` failed with `error_category: xgb_missing` or an `ImportError` on XGBoost."** → The `[xgb]` extra was not installed on your machine. Preflight should have caught this pre-class; the fix is either (a) install the extra with `pip install kailash-ml[xgb]`, or (b) drop XGBoost from the candidate list. Use this fallback prompt: _"`/forecast/train` just failed with `error_category: xgb_missing`. Re-run the AutoML training with `candidate_families` restricted to the four sklearn families only: `sklearn.linear_model.LinearRegression`, `sklearn.linear_model.Ridge`, `sklearn.ensemble.RandomForestRegressor`, `sklearn.ensemble.GradientBoostingRegressor`. Keep `search_strategy='random'`, `search_n_trials=5`, `split_strategy='walk_forward'`. Do not silently substitute a duplicate GradientBoostingRegressor — leave it as a 4-family leaderboard and note the missing `[xgb]` extra in the Phase 4 journal."_ The grader accepts a 4-family leaderboard when `[xgb]` is unavailable; the `n_runs_logged` assertion only requires ≥ 3 runs with distinct `params_hash`.

---

## 9. Your Opening Prompt

Open a terminal at the **project root** (`~/repos/training/metis`). Type `claude` to start. Paste this exactly:

```
The active workspace is workspaces/metis/week-04-supply-chain/.
Read these files from the workspace:
- workspaces/metis/week-04-supply-chain/PRODUCT_BRIEF.md
- workspaces/metis/week-04-supply-chain/PLAYBOOK.md
- workspaces/metis/week-04-supply-chain/START_HERE.md

I am a student running Sprint 1 (Forecast) today. I will drive the
decision phases; you execute.

First, set up the workspace environment:
1. Start the backend (workspaces/metis/week-04-supply-chain/scripts/run_backend.sh)
   in the background. Verify /health returns ok with feature_store: true.
2. Start the viewer (cd workspaces/metis/week-04-supply-chain/apps/web && npm run dev)
   in the background. Verify it serves on localhost:3000.
3. Run the preflight check
   (uv run python workspaces/metis/week-04-supply-chain/scripts/preflight.py)
   and show me the result.

If anything fails, diagnose and fix it before proceeding.

Once the environment is green, summarize:
1. What product we are shipping today
2. The decision phases I will run in Sprint 1
3. What output you will produce vs. what output I will produce
4. What scaffolds are already built so I don't waste time on plumbing

Then stop and wait for my first decision.
```

When Claude Code answers — **evaluate** two things:

1. **Environment**: did it start the backend and viewer? Does preflight show green? If not, tell it to fix the issue.
2. **Summary**: does it accurately name the product? Does it correctly split Trust Plane vs. Execution Plane? Does it know what is scaffolded? If not, correct it before proceeding.

That evaluation is your first decision of the day. You are already in the Trust Plane.

---

## Closing

You have everything you need. The plumbing is built. The Playbook is universal. The product is a real last-mile logistics company in microcosm. Claude Code is your team. The decisions are yours.

By 3:30 pm you will have shipped a product and defended a page of decisions. In Week 5, you do it again on a new domain with the same Playbook. By Week 8, you will be a one-person unicorn — **because you can commission and judge ML products, not because you can code them**.

Let's ship.
