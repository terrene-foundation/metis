<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# The ML Decision Playbook — Universal Edition (Week 5 instantiation: Arcadia Retail)

**Version:** 2026-04-23 · **License:** CC BY 4.0

---

## 0. How to read this Playbook

This is the same 14-phase procedure you run on **every** ML product you commission — tonight, next week, and in your career after this course. The body of each phase reads as **universal**: it names the decisions, the levers, the failure modes, and the vocabulary that apply to any ML paradigm. Retail examples live in `> For tonight's product` sidebars and illustrate how the universal body instantiates for Arcadia.

Read it cold: skim sections 1–8 before class. During class, jump to the phase you are running. After the course, take this file into your next project and swap the sidebars for your domain.

Every phase has the same shape:

- **Orientation frame** — where you are in the value chain, the sprint, the clock
- **Concept** — the ML idea this phase teaches in one sentence
- **Why it matters (SML lens / USML lens / Optimization lens)** — vocabulary you bring back into any future project
- **Your levers this phase** — what to pull, what to ignore; the orchestrator's toolkit
- **Trust-plane question** — the single decision you own
- **Prompt template** — universal first, retail-flavoured sidebar second
- **Evaluation checklist** — how you judge the output
- **Journal schema** — what you record
- **Common failure modes** — the 2–3 ways this phase usually goes wrong
- **Artefact** — the file on disk that proves the phase happened
- **Instructor pause point** — what your instructor stops to discuss live in class
- **Transfer to your next project** — three questions you ask when you open this Playbook on a non-retail product

---

## 1. The ML Value Chain — one product, four paradigms, one Playbook

Tonight is the whole traditional ML value chain in one product. Four paradigms, composed:

```
                    THE ML VALUE CHAIN

  STAKEHOLDER  │ QUESTION                       │ PARADIGM      │ SPRINT  │ PHASES     │ ARTEFACT
  ─────────────┼────────────────────────────────┼───────────────┼─────────┼────────────┼──────────────────────
  CMO          │ Who are my customers, really?  │ USML          │ 1 (45m) │ 1→8        │ Segmentation (K, named)
  CX Lead      │ Which SKU for which customer?  │ SML           │ 2 (45m) │ 4→8 (×2)   │ Churn + Conversion models
  CMO + Ops    │ How to allocate fixed budget?  │ Optimization  │ 3 (40m) │ 10→12      │ Campaign allocator
  Ops Lead     │ When does any of this lie?     │ MLOps         │ 4 (20m) │ 13         │ Drift × 3 models

  Discover ──▶ Predict ──▶ Decide ──▶ Monitor
     │            │           │           │
     └── segments feed cold-start of the recommender;
         recommender feeds response probs into allocator;
         allocator output is what MLOps monitors.

  Skip a link, the chain breaks at your weakest stakeholder.
```

**Why this structure.** In the real world ML is not a model, it is a value chain. Unsupervised learning discovers structure; supervised learning predicts behaviour; optimization decides actions under constraints; MLOps catches drift. Any product you build in your career will touch at least two of these four. Tonight you touch all four, end to end, in one sitting — and the Playbook is what you take to the next project.

---

## 2. How to use this Playbook

You are a **commissioner, not a coder.** Your Playbook fires inside the COC `/implement` phase (see §5). During each Playbook phase, you prompt Claude Code in plain language, evaluate the output against the phase's checklist, make the Trust-plane decision, and write a journal entry.

- **Trust Plane** is you: framing, judging, approving. The decisions.
- **Execution Plane** is Claude Code plus the scaffold: code, trained models, leaderboards, dashboards. The execution.

If a question is _what_ or _how_, route it to Execution. If it is _which_, _whether_, _who wins_, or _is it good enough to ship_, it stays with you.

---

## 3. How to prompt — the delegation skill

This is the single most important skill the course teaches. Every prompt you write contains these 5 elements:

1. **Objective** — business outcome in plain language
2. **Boundaries** — what matters, what doesn't, what costs what
3. **Expected output** — what deliverable you want back
4. **Checks** — what could go wrong, what would flip your decision
5. **Decision authority** — what YOU will decide vs. what Claude Code executes

**What your prompt should NEVER contain:** library names, class names, function signatures, import paths, code snippets, API parameter objects.

Claude Code has the frameworks, the skills, the documentation. It knows which library to call and how. **If you tell it how, you're doing its job. If you tell it what and why, you're doing yours.**

> **Bad prompt** (doing CC's job): _"Using sklearn.cluster.KMeans with n_clusters=5, fit on the RFM feature matrix..."_
>
> **Good prompt** (doing yours): _"Cluster Arcadia's active customers into behavioural segments. Try three different approaches — one that expects round blobs, one that finds dense pockets, one that builds a nested tree — and compare them on stability and on how interpretable the resulting segments are. I'll pick the count."_

---

## 4. The ML Vocabulary Menu (one-page orchestrator reference)

You do not write code. You do speak ML. Here is the vocabulary an orchestrator needs — enough for comfort and assurance, not implementation depth.

### 4.1 Supervised families (you have labels)

| Family                              | When to reach for it                                                                                    | Cost                                                         |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| **Linear**                          | Fast, interpretable, strong baseline. Always include one.                                               | Misses non-linear interactions.                              |
| **Tree**                            | Handles non-linear without feature engineering. Single tree = cheap explanation.                        | Single tree overfits; use bags or boosts.                    |
| **Ensemble (the king for tabular)** | Gradient-boosted trees (XGBoost, LightGBM, sklearn GBM) or random forests. Default-winning for tabular. | Slower to train; less interpretable; watch for overfitting.  |
| **Neural**                          | Only for very large data, complex interactions, or heterogeneous inputs (text + image + tabular).       | Opaque, expensive, unnecessary most of the time for tabular. |

> **Default pick for any new tabular classification/regression**: logistic/linear as a baseline + random forest as a tree check + a gradient-boosted model as the serious contender. Unless you have a specific reason, the gradient-boosted family wins.

### 4.2 Unsupervised families (no labels)

| Family               | What it assumes                                       | When it fails                                                |
| -------------------- | ----------------------------------------------------- | ------------------------------------------------------------ |
| **K-means**          | Round blobs of similar size around a centre           | Elongated, nested, or unequal-sized shapes                   |
| **DBSCAN / HDBSCAN** | Dense pockets with gaps; flags outliers as unassigned | Sensitive to density parameters; can leave 10–25% unassigned |
| **Hierarchical**     | A nested tree you can cut at any level                | Slow on large data; cut decision is arbitrary                |
| **Spectral**         | Connectivity / graph-affinity structure               | Expensive (eigendecomp); needs good similarity measure       |
| **GMM**              | Soft membership; probabilistic assignments            | Slow convergence; can find spurious components               |

### 4.3 Optimization families

| Family                      | When to reach for it                                       | Watch out for                                      |
| --------------------------- | ---------------------------------------------------------- | -------------------------------------------------- |
| **Linear programming (LP)** | Linear objective, linear constraints, continuous decisions | Integer decisions need rounding or a harder solver |
| **Integer / Mixed-integer** | Yes/no decisions (which customer to touch)                 | Can be NP-hard; use MIP solver or heuristics       |
| **Constraint satisfaction** | Feasibility first, optimality second                       | Infeasibility requires you to demote a constraint  |
| **Greedy heuristic**        | When LP is overkill; cheap, defensible default             | Can be 10–30% off optimum; good enough often wins  |

### 4.4 Evaluation instruments — read them, don't compute them

- **Confusion matrix** — TP / FP / TN / FN at a chosen threshold. Read precision = TP/(TP+FP) and recall = TP/(TP+FN).
- **ROC curve** — how well does the score rank? AUC = area under the curve, 0.5 = random, 1.0 = perfect. Insensitive to class imbalance.
- **PR curve** — precision vs recall across thresholds. Use this for rare positives (fraud, churn, conversion).
- **Calibration plot** — if the model says 30% probability, do 30% of those cases actually happen? A well-calibrated model lines up along the diagonal.
- **Brier score** — mean squared error of predicted probabilities. Lower = better calibration.
- **Silhouette score** (USML) — how crisp are the clusters? Near 1 is tight/separated, near 0 is overlapping, negative is wrong cluster assignment.
- **Bootstrap Jaccard** (USML) — re-cluster on a different sample; what fraction of customer pairs stay in the same pair? ≥0.80 is shippable.
- **Precision@k** (rec) — of the top-k you recommended, how many did the customer engage with?
- **PSI (Population Stability Index)** (drift) — how far has this feature's distribution moved since training? >0.25 is severe.

### 4.5 Common diagnoses you should recognise

| You see...                                                    | You are looking at...                                                    |
| ------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Train-test gap (train AUC much higher than test)              | **Overfitting**                                                          |
| Good AUC but bad Brier / bad calibration                      | Model **ranks right, probabilities are miscalibrated**                   |
| One feature importance dominates 80%                          | Likely **leakage** — that feature is the label in disguise               |
| High precision, low recall                                    | Threshold set too high; catching few but catching them right             |
| High recall, low precision                                    | Threshold set too low; catching most but also many false positives       |
| Silhouette high but stability (bootstrap Jaccard) low         | Pattern exists in this sample but doesn't hold up on new samples         |
| Clusters explain a demographic variable better than behaviour | **Proxy leakage** — the segmentation is income/age/postcode in disguise  |
| Solver returns feasible but one segment gets 90% of the plan  | **Pathology**: feasible ≠ shippable                                      |
| Drift severity high for one feature but segment-churn low     | Distributional shift without behavioural shift — may not need retraining |

### 4.6 The lever taxonomy — what you pull each phase

| Phase                | Levers (big one first)                                                              |
| -------------------- | ----------------------------------------------------------------------------------- |
| 1 Frame              | scope · horizon · operational ceiling · cost asymmetry                              |
| 2 Data Audit         | outlier handling · missingness · contamination filters · sampling                   |
| 3 Feature Framing    | availability · leakage · proxy-for-protected-class · engineered derivation          |
| 4 Candidates         | model family mix · sweep breadth · cross-validation · baseline inclusion            |
| 5 Implications       | complexity-vs-interpretability · stability-vs-accuracy · speed-vs-performance       |
| 6 Metric + Threshold | primary metric · threshold · class imbalance · calibration                          |
| 7 Red-team           | subgroups · adversarial perturbations · proxy tests · acceptance                    |
| 8 Deployment Gate    | monitoring cadence · rollback channel · alert thresholds · promotion criteria       |
| 10 Objective         | single-vs-multi · weight assignment · proxy metrics · coverage / diversity floors   |
| 11 Constraints       | hard-vs-soft · penalty calibration · demotion rules · regulatory triggers           |
| 12 Solver Acceptance | held-out choice · pathology detection · accept/retune/redesign · rollback readiness |
| 13 Drift             | signal choice · threshold grounding · duration window · HITL-vs-auto                |

---

## 5. The Playbook runs inside `/implement` (COC wrap)

The 14-phase Playbook is not a replacement for the COC phases you already know — it is the **content** of your `/implement` phase. Routine is the scaffold; decisions are the content.

| Clock     | COC phase             | Sprint / paradigm                        | Playbook phases inside          | Output                                                                 |
| --------- | --------------------- | ---------------------------------------- | ------------------------------- | ---------------------------------------------------------------------- |
| 2:00–2:10 | (opening)             | narrative + preflight                    | —                               | green viewer banner                                                    |
| 2:10–2:25 | `/analyze`            | frame the 4-module cascade               | (pre-phase)                     | `01-analysis/failure-points.md`, `assumptions.md`, `decisions-open.md` |
| 2:25–2:30 | `/todos`              | draft phases · instructor gate           | —                               | `todos/active/phase_N_*.md` (13 phases; Phase 14 deferred)             |
| 2:30–3:15 | `/implement` Sprint 1 | **USML — Discover**                      | Phases 1, 2, 3, 4, 5, 6, 7, 8   | Segmentation; `journal/phase_{1..8}_usml.md`                           |
| 3:15–4:00 | `/implement` Sprint 2 | **SML — Predict**                        | Phases 4, 5, 6, 7, 8 (replayed) | Churn + Conversion classifiers; `journal/phase_{4..8}_sml.md`          |
| 4:00–4:30 | `/implement` Sprint 3 | **Optimization — Decide**                | Phases 10, 11, 12               | Campaign allocator; `journal/phase_{10..12}_*.md`                      |
| 4:30–4:40 | mid-sprint injection  | PDPA red-line                            | Phase 11 + 12 re-run            | `journal/phase_11_postpdpa.md`, `phase_12_postpdpa.md`                 |
| 4:40–5:00 | `/implement` Sprint 4 | **MLOps — Monitor**                      | Phase 13                        | Drift × 3 models; `journal/phase_13_*.md`                              |
| 5:00–5:15 | `/redteam`            | stability · proxy · operational collapse | —                               | `04-validate/redteam.md`                                               |
| 5:15–5:30 | `/codify` + `/wrapup` | Phase 9                                  | Phase 9                         | `.claude/skills/project/week-05-lessons.md`, `.session-notes`          |

`/analyze` and `/todos` are short (15 minutes together) and not busywork: they force you to declare what the pre-built baseline commits to (K=3, content recommender, drift reference registered) and what remains open. Week 4's students lost the lifecycle to scaffolding; Week 5 keeps both.

---

## 6. The five Trust-Plane decision moments (universalized)

Tonight collapses into five high-pressure decisions. These are where the rubric has teeth. The universal shape first; the retail instantiation in the sidebar.

1. **Pick the primary operating point and defend it in the declared unit of harm.**

   > _Retail instantiation: pick K for segmentation and defend in $ of wrong-campaign cost + marketing capacity. Not "silhouette said 5"; "5 because marketing runs 5 campaigns; 7 costs $X in setup with no realistic lift; stability drops below 0.80 at K=7."_

2. **Commit to a distinct downstream action per output class; collapse duplicates.**

   > _Retail instantiation: if two segments get the same marketing campaign, they are one segment with noise. Collapse to lower K or defend the difference in dollars._

3. **Choose the model strategy with an explicit fallback for the cold / low-confidence / no-signal regime.**

   > _Retail instantiation: collaborative / content-based / hybrid for the recommender — AND for new customers with no history, say what happens: segment modal basket, catalogue popularity, or editorial curation._

4. **Classify hard-vs-soft constraints under regulatory pressure and justify the penalty.**

   > _Retail instantiation: mid-Sprint-2, Legal flags PDPA exposure on under-18 browsing history. Re-run Phase 11 (re-classify as hard) AND Phase 12 (re-solve with the new constraint). Not just the journal entry._

5. **Set the retrain rule: signal + threshold grounded in historical variance + duration window + human-in-the-loop on first trigger.**
   > _Retail instantiation: three separate rules, one per model (segmentation churn, churn predictor calibration decay, allocator constraint-violation rate)._

Decision moments 4 and 5 are where Week 4 students hit the wall. They are the parts the rubric scores hardest.

---

## 7. Workshop clock (4 sprints, 3.5 hours)

```
2:00  opening narrative + preflight green
2:10  /analyze  (10m)
2:25  /todos    (5m)   ── instructor gate ──
2:30  ┌───────────────────────────────────────────────────┐
      │ SPRINT 1 · USML · Discover · Phases 1→8           │ 45m
3:15  ├───────────────────────────────────────────────────┤
      │ SPRINT 2 · SML · Predict · Phases 4→8 (×2)        │ 45m
4:00  ├───────────────────────────────────────────────────┤
      │ SPRINT 3 · Opt · Decide · Phases 10→12            │ 30m
4:30  │    PDPA injection fires (re-run Phase 11 + 12)    │ 10m
4:40  ├───────────────────────────────────────────────────┤
      │ SPRINT 4 · MLOps · Monitor · Phase 13             │ 20m
5:00  ├───────────────────────────────────────────────────┤
      │ /redteam                                           │ 15m
5:15  │ /codify + /wrapup                                  │ 15m
5:30  └───────────────────────────────────────────────────┘
```

---

## 8. Phase summary & disposition

Which phases **keep** as-is across ML problems, which **adapt** to the paradigm, which are **replaced** for USML/recommender vs SML, which **defer**:

| #   | Phase                      | Disposition                     | Sprint | Artefact                                                   |
| --- | -------------------------- | ------------------------------- | ------ | ---------------------------------------------------------- |
| 1   | Frame                      | KEEP                            | 1      | `journal/phase_1_frame.md`                                 |
| 2   | Data audit                 | KEEP (+ proxy chk)              | 1      | `journal/phase_2_data_audit.md`                            |
| 3   | Feature framing (UNFOLDED) | KEEP (live this wk)             | 1      | `journal/phase_3_features.md`                              |
| 4   | Candidates                 | ADAPT (USML/SML)                | 1, 2   | `data/segment_leaderboard.json`, `predict/leaderboard/*`   |
| 5   | Implications               | ADAPT                           | 1, 2   | `journal/phase_5_*.md`                                     |
| 6   | Metric + Threshold         | **REPLACE** (USML three floors) | 1, 2   | `journal/phase_6_usml.md`, `phase_6_sml.md`                |
| 7   | Red-team                   | ADAPT                           | 1, 2   | `journal/phase_7_*.md`                                     |
| 8   | Deployment Gate            | KEEP                            | 1, 2   | `journal/phase_8_*.md` + registry transition               |
| 9   | Codify                     | KEEP                            | close  | `.claude/skills/project/week-05-lessons.md`                |
| 10  | Objective                  | **REPLACE** (optimization)      | 3      | `journal/phase_10_objective.md`                            |
| 11  | Constraints                | ADAPT                           | 3      | `journal/phase_11_constraints.md` + `phase_11_postpdpa.md` |
| 12  | Solver Acceptance          | **REPLACE** (LP)                | 3      | `data/allocator_last_plan.json` + `journal/phase_12_*.md`  |
| 13  | Drift                      | ADAPT (× 3 models)              | 4      | `data/drift_report_*.json` + `journal/phase_13_*.md`       |
| 14  | Fairness                   | DEFER to Week 7                 | —      | (deferred)                                                 |

**Phases 10–12 are deferrable** when your product has no secondary optimization or ranking layer (e.g., a pure clustering or pure classification product). Tonight Arcadia has both — USML segments feed SML predictors feed the optimization allocator — so all three phases run. On your next project, ask: is there a decision to optimize given the model's output? If no, skip 10–12.

---

# SPRINT 1 — USML · Discover · Phases 1–9

---


---

## Playbook file inventory

| File | Contents |
| --- | --- |
| [phase-01-frame.md](./phase-01-frame.md) | Frame — target, population, horizon, operational ceiling, cost asymmetry |
| [phase-02-data-audit.md](./phase-02-data-audit.md) | Data Audit — six-category audit with dispositions |
| [phase-03-features.md](./phase-03-features.md) | Feature Framing — four-axis classification + proxy-drop test (unfolded this week) |
| [phase-04-candidates.md](./phase-04-candidates.md) | Candidates — multi-family sweep (USML + SML replay) |
| [phase-05-implications.md](./phase-05-implications.md) | Implications — pick the candidate; name the segments / families |
| [phase-06-metric-threshold.md](./phase-06-metric-threshold.md) | Metric + Threshold — USML three floors + SML PR-curve + calibration |
| [phase-07-redteam.md](./phase-07-redteam.md) | Red-Team — stability / proxy leakage / operational collapse |
| [phase-08-gate.md](./phase-08-gate.md) | Deployment Gate — PASS/FAIL floors + monitoring + rollback |
| [phase-09-codify.md](./phase-09-codify.md) | Codify — transferable lessons + Week 5 appendix update (also /codify workflow phase) |
| [phase-10-objective.md](./phase-10-objective.md) | Objective Function — LP weights + shadow prices |
| [phase-11-constraints.md](./phase-11-constraints.md) | Constraint Classification — hard/soft + PDPA injection re-run |
| [phase-12-acceptance.md](./phase-12-acceptance.md) | Solver Acceptance — feasibility + pathologies + PDPA re-solve |
| [phase-13-drift.md](./phase-13-drift.md) | Drift — three retrain rules, one per model |
| [phase-14-fairness.md](./phase-14-fairness.md) | Fairness — deferred to Week 7 |
| [appendix-a-lessons.md](./appendix-a-lessons.md) | Transferable lessons accumulating across weeks (accretive) |
| [appendix-b-dashboard.md](./appendix-b-dashboard.md) | Build your own value-chain dashboard at your next job |

**How to navigate during class:** when you enter a Playbook phase (after `/implement` boots the sprint from `START_HERE.md` §6), open the matching `phase-NN-*.md` file in the folder above. Each phase file is self-contained — spine (Concept / lens / levers / Trust-plane question) on top, paste-ready prompt in the middle, evaluation / journal schema / failure modes / Transfer at the bottom.
