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

## Phase 1 — Frame

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ **USML ◉** ▸ SML ▸ Opt ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 1 · Phase 1 of 8 — Frame
 LEVERS:        scope · horizon · operational ceiling · cost asymmetry
──────────────────────────────────────────────────────────────────
```

### Concept

Declaring — in writing, before any code runs — exactly who is in scope, over what window, how many outputs the business can act on, and what it costs when the answer is wrong. Frame is the single sentence the whole downstream stack gets built on. If Frame is fuzzy, every later phase fails gracefully in your journal and catastrophically in production.

### Why it matters (SML lens)

- Reinforces Week 2 healthcare: "predict readmission" only became useful once scope narrowed to "patients discharged to home within 30 days of an inpatient stay."
- Reinforces Week 3 fraud: cost asymmetry ($40 missed-fraud vs $1 false-alarm) only meant something once volume was attached.
- Reinforces Week 4 forecasting: horizon has to be named in days — "forecast demand" is not a target; "forecast orders per depot per day for the next 14 days" is.
- The dollar cost of being wrong is the anchor every later phase refers back to. No anchor, no grounding.

### Why it matters (USML lens)

- With no label, there is no "accuracy" to fall back on if scope is fuzzy — a bad scope makes every segment unactionable and you won't notice until campaigns ship.
- You must commit to an **operational ceiling** BEFORE the data speaks. _"Marketing can run at most 6 parallel campaigns"_ — declared now, enforced in Phase 6. Waiting until after the elbow plot is how you end up with K=12 and a paralysed marketing team.
- The cost of wrongness has two faces in USML: the wrong-cohort cost AND the cost of touching them at all. SML usually has one cost per direction; USML has two because you're both choosing a cohort AND deciding to contact it.
- Peak seasonality changes the wrong-cohort math — the same 5% misclassification rate costs double when volume doubles.

### Your levers this phase — what to pull, what to ignore

- **Lever 1 (the big one): scope.** Inclusions AND explicit exclusions. "18,000 active customers in last 90 days, excluding staff + bot accounts" is a scope. "All customers" is not. Pulled by telling Claude Code what counts and what doesn't.
- **Lever 2 (usually matters): operational ceiling.** How many outputs can your business _act on_? The answer caps model complexity. A 4-person marketing team cannot run 12 segments.
- **Lever 3 (the anchor): cost asymmetry in dollars.** Two directions, two numbers, with units. "$40 per missed event, $12 per false alarm" lets every later phase do math.
- **Lever 4 (rarely adjusted): horizon.** Days, not "near-term." Forces precision.
- **Skip unless specific:** population segmentation at this phase (that's Sprint 1's output, not its input); peak-season adjustments (Phase 13's problem).

### Trust-plane question

What is the target, the population, the horizon, the cost of being wrong?

### Prompt template — universal

> _"Read the product brief. I need a clear problem statement for [module]. Tell me: what exactly are we [predicting/discovering/deciding], for which population, over what window, and what it costs when we get it wrong in each direction. [Cost asymmetry]. Don't assume anything — if the brief is vague on scope, ask me."_

> **For tonight's product (Arcadia Retail, Sprint 1):** _"I need the segmentation problem statement. Who are we segmenting (18,000 active customers in last 90 days), how many segments can marketing actually run (the ceiling), and what it costs when we place a customer in the wrong segment ($45) vs run redundant campaigns ($3 per touch). Flag anything ambiguous."_

### Evaluation checklist

- [ ] Target / output precise (not "segments" but "behavioural segments over 90-day window, at most 6, distinct marketing action per segment").
- [ ] Population scope explicit — inclusions AND exclusions.
- [ ] Horizon / window named in units (days, months).
- [ ] Cost asymmetry quantified with dollars and units attached.
- [ ] Operational ceiling declared and sourced (who owns it?).

### Journal schema — universal

```
Phase 1 — Frame
Target / output: ____
Population: ____ (inclusions: ____; exclusions: ____)
Horizon / window: ____
Primary cost term: $__ per ____ (the side that loses more)
Secondary cost term: $__ per ____
Operational ceiling: ____ (owned by ____)
What would flip my mind: ____
```

> **Retail instantiation:** Target = "behavioural segment per active customer, max 6 segments"; Population = "18,000 customers active in last 90 days, excl. staff/bots"; Horizon = "6-month rolling"; Primary cost = $45 per wrong-segment campaign; Secondary = $3 per touch; Ceiling = 6 (owned by CMO); Flip = "if marketing restructures to run >6 campaigns".

### Common failure modes

- Target drifts into fuzzy language ("discover patterns") — downstream phases lose grounding.
- Horizon left implicit — the model learns behaviour across seasons that should not be averaged.
- Cost asymmetry stated as "X:Y ratio" without dollars — scores 2/4 on rubric D1.
- Operational ceiling omitted — student ends up with a statistically brilliant K=12 that marketing silently ignores.

### Artefact

`workspaces/.../journal/phase_1_frame.md`

### Instructor pause point

- Write the Sprint 1 frame on the whiteboard. Ask the class: which three numbers would change if Arcadia were a 2,000-customer boutique? Which would change if it were Lazada?
- Ask: what's the smallest operational ceiling that still ships a useful product? Why isn't "premium vs mass" always the right answer?
- Demonstrate: show $45 × 18,000 × 5% = $40,500/month on the board. Ask: does the CMO care at this number? What number flips her from "nice to have" to "must ship"?

### Transfer to your next project

1. Who is explicitly in scope and who is explicitly OUT? (Scope is a list of exclusions, not just inclusions.)
2. What is the operational ceiling on how many outputs your business can act on — and who, not the model, owns that ceiling?
3. What does it cost, in dollars, when a single unit is wrong — and is there a volume that turns that unit cost into a monthly number your executive will care about?

---

## Phase 2 — Data Audit

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ **USML ◉** ▸ SML ▸ Opt ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 1 · Phase 2 of 8 — Data Audit
 LEVERS:        outlier handling · missingness · contamination filters · sampling
──────────────────────────────────────────────────────────────────
```

### Concept

Before you point any algorithm at the data, challenge whether the data is trustworthy enough to carry the decision. Six categories: duplicates, contaminated populations, sparsity that makes rows unusable, outliers that will dominate the result, fields that are labels in disguise, missingness with unknown behaviour.

### Why it matters (SML lens)

- Reinforces Week 2's leakage lesson — a diagnosis code recorded at discharge is a perfect predictor of readmission because it encodes the answer.
- Reinforces Week 3's outlier finding — a single merchant's 0.1% of transactions drove 14% of the fraud score.
- Reinforces Week 4's missingness rule — you don't know what your model does with a NaN until you look.
- Dollar framing: skipping the audit in Week 3 would have cost $22,000/month in false alarms. Same logic here: accepting the top-1% spenders silently means every customer segment becomes "rich vs not rich."

### Why it matters (USML lens)

- Outliers dominate distance-based clustering more than they bias a supervised model — one customer who spends 30× the median can form their own cluster and shift every other boundary. Decide NOW: cap, log-transform, or exclude.
- A **label-in-disguise** in SML is a leakage bug. In USML it's worse: a pre-existing tier column or a 2020 hand-authored segment flag will cause the clustering to rediscover that old rule, and the CMO will correctly ask "why did I pay for this."
- Singleton customers (one transaction ever) cannot be clustered honestly — inventing behaviour from noise. Decide NOW: exclude, or route to a cold-start branch.
- Bots and staff don't just inflate error; they form their own segment. Ship a "4AM high-frequency buyer" segment and you've shipped your own QA team.

### Your levers this phase

- **Lever 1 (the big one): outlier handling.** Cap / log-transform / exclude / own-branch. This decision changes every downstream result. Retail default: log-transform spend variables; cap visits-per-week at 95th percentile.
- **Lever 2 (the sneaky one): contamination filters.** Bots, staff, test accounts, integration partners. Quantify BEFORE you fit.
- **Lever 3 (usually matters): missingness disposition.** Impute / drop / leave-as-NaN / flag with a mask feature. Each choice has different failure modes.
- **Lever 4 (only if large data): sampling.** Keep all / stratified subsample / weight by class. For tabular data <100k rows, usually keep all.
- **Skip unless specific:** schema normalisation (Phase 3's problem); feature derivation (Phase 3's problem).

### Trust-plane question

Is this data trustworthy? Which features are available at prediction time, leaky, or ethically loaded?

### Prompt template — universal

> _"Audit the [dataset] before we train anything. I need to know: is the data trustworthy? Check for duplicates, staff/bot contamination, singleton observations, outliers, label-in-disguise columns, and missingness. For each finding, tell me the row or column affected and the count. Recommend a disposition — cap, log, exclude, flag — for each outlier pattern and each contamination. I'll approve the dispositions."_

> **For tonight's product (Arcadia Retail):** _"Audit the Arcadia customer dataset — 5,000 customers, 14 features. Flag the six audit categories with specifics: row X, column Y, count Z. Pay special attention to (a) customers with <3 transactions who cannot be honestly clustered, (b) the top-1% spenders who will dominate distance-based clustering, (c) any column that is really a pre-existing segment label. Recommend; I decide."_

### Evaluation checklist

- [ ] All 6 audit categories addressed with specifics (row X, col Y, count Z).
- [ ] Outlier dispositions proposed (cap / log / exclude / own-branch) with a reason each.
- [ ] Singleton / low-observation customers flagged with a disposition.
- [ ] Label-in-disguise check run explicitly on every column that looks categorical or "tier"-shaped.
- [ ] Missingness disposition proposed per feature, not blanket.

### Journal schema — universal

```
Phase 2 — Data Audit
Accepted? Yes / Conditional / No
Conditions applied: ____
Known risks I am accepting: ____
Dispositions:
  Outliers: ____
  Singletons: ____
  Missingness: ____
  Contamination: ____
  Label-in-disguise candidates: ____
```

### Common failure modes

- Audit output accepted as-is; no call made on any of the six categories — scores 1/4 on D3.
- "Everything looks fine" without specifics — the phase did not happen.
- Singleton customers left in for clustering — they become a noise cluster that pollutes every segment's boundary.

### Artefact

`workspaces/.../journal/phase_2_data_audit.md`

### Instructor pause point

- Show a scatter of two RFM features with top-1% left in vs removed. Ask: which picture is the segmentation going to be _about_?
- Raise-hands: who would exclude the top 1% of spenders from the segmentation? Who would keep them _in_ but in their own segment? Debate 2 minutes.
- Ask: what's a label-in-disguise column in your industry? (Credit: "risk tier." Hospital: "DRG code." Retail: "loyalty tier.") If you can't answer, you haven't audited.

### Transfer to your next project

1. Which populations are contaminating the dataset (bots, staff, test, integration) and have I quantified them BEFORE I fit anything?
2. Is there a field that is a leftover label from an older rule-based system — and if I leave it in, will my model simply re-derive the thing my buyer is paying me to replace?
3. What is my plan for rare-but-real outliers — cap, log, exclude, or own-branch — and have I written the plan down BEFORE I saw the model output?

---

## Phase 3 — Feature Framing (UNFOLDED this week)

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ **USML ◉** ▸ SML ▸ Opt ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 1 · Phase 3 of 8 — Feature Framing
 LEVERS:        availability · leakage · proxy check · engineered derivation
──────────────────────────────────────────────────────────────────
```

### Concept

Every candidate input column classified on four independent axes: (a) available at prediction time? (b) leaky? (c) ethically loaded or regulatorily sensitive? (d) raw or engineered? Week 4 folded this into Data Audit because a supervised regressor with one leaky feature produces a bad prediction you can measure. Week 5 unfolds it because in unsupervised learning, an ethically loaded feature doesn't bias a model — it _creates a segment that is really a protected-class proxy_, and no accuracy metric will flag it.

### Why it matters (SML lens)

- Reinforces Week 2's rule: a feature fails leakage review if it wasn't available at the moment of prediction (discharge date for readmission: no).
- Reinforces Week 3's engineered-feature discipline: RFM, tenure decile, channel-mix entropy — every derived feature has a one-line derivation or it is a hidden bug.
- Reinforces Week 4's feature importance ladder: if one feature dominates 80% of the signal, it's a leakage candidate until proven otherwise.
- Dollar framing: leaving a single leaky feature in Week 4's forecast meant the $40/$12 cost-asymmetry logic was against a self-fulfilling prophecy. The fix prevented a live-production disaster.

### Why it matters (USML lens)

- **Postcode is not a neutral feature.** In Singapore it's a strong proxy for income, ethnicity, and school catchment. Cluster on it → a segmentation that looks behavioural and is actually demographic.
- **Under-18 status is a PDPA red line** (in Singapore; GDPR's under-16 in the EU). Including it is not bad manners; it's $220/record exposure.
- **The proxy check is the new tool:** cluster once with the demographic feature in, cluster once with it out, count how many customers change segments. If 30% move, the demographic was doing the work — the "behavioural" segmentation was demographic all along.
- Inferred sensitive attributes (purchases that imply health conditions, religion, sexual orientation) are equally loaded even when never named.

### Your levers this phase

- **Lever 1 (the big one): proxy-for-protected-class check.** On every demographic or demographic-adjacent feature, run the cluster-with / cluster-without swap and count reassignment. >30% reassignment → the feature was doing the demographic work.
- **Lever 2 (the discipline): availability audit.** Was this feature knowable at the moment the decision gets made? A feature that is only known retrospectively is a leakage bug wearing a pretty dress.
- **Lever 3 (the hygiene): engineered-feature derivation.** Every derived column has a one-line derivation recorded. No exceptions.
- **Lever 4 (the boundary): regulatory classification.** Name the regime (PDPA §13, GDPR Art. 9, HIPAA, ECOA) for each sensitive feature.
- **Skip unless specific:** feature scaling (standardization is universal for distance-based clustering — the scaffold handles it); encoding cardinality (handled by the scaffold's one-hot/frequency logic).

### Trust-plane question

Which features are safe, which are leaky, which are ethically loaded?

### Prompt template — universal

> _"Classify every candidate feature on four axes: (1) available at prediction time? (2) leaky from the label or from future data? (3) ethically loaded, regulatorily sensitive, or a proxy for a protected class — name the regime? (4) raw or engineered, and if engineered, what's the one-line derivation? Run a proxy-drop test on every demographic feature: re-cluster with and without, report the reassignment rate. I'll approve which features go in."_

> **For tonight's product (Arcadia Retail):** _"Classify Arcadia's 14 customer features on the four axes. Pay special attention to: postal_district (proxy for income?), age_band (proxy for under-18 under PDPA?), and any column you wouldn't defend to the CMO if asked. Run the proxy-drop reassignment rate for the two strongest candidates. Recommend in / out; I approve."_

### Evaluation checklist

- [ ] Every candidate feature classified on all four axes — no hand-waving.
- [ ] Ethically-loaded features have a named rationale (which regime) AND a proxy-drop reassignment number.
- [ ] Engineered features have a derivation explanation (one sentence).
- [ ] Recommendation offered per feature, not bulk; you decide per feature.

### Journal schema — universal

```
Phase 3 — Feature Framing
Features IN: ____
Features OUT (with reason): ____
Ethically-loaded features kept IN with rationale: ____ (regime: ____)
Proxy-drop reassignment rate (if demographic feature kept): __%
Engineered feature derivations: ____
```

### Common failure modes

- "Ethically loaded" classified as "OK" with no rationale — scores 1/4 on D4.
- Proxy-drop test skipped because Claude Code "says postcode is fine" — student has outsourced their judgment.
- Engineered feature added without a one-line derivation — becomes a leakage vector six weeks later.

### Artefact

`workspaces/.../journal/phase_3_features.md`

### Instructor pause point

- Whiteboard the 4 axes as a 2×2 table (available × leaky, loaded × engineered). Place 10 Arcadia features into cells. Which cells ship? Which are show-stoppers?
- Ask: if a feature is both engineered AND loaded (e.g., "neighbourhood affluence index"), is it acceptable? Defensible rationale?
- Demonstrate: run the proxy-drop check live on postal_district. Report reassignment rate. Above what % does the segmentation stop being "behavioural"?

### Transfer to your next project

1. For each feature, can I defend its inclusion on all four axes, or am I hoping no one asks about (c)?
2. What are the protected-class features in MY domain (health condition, immigration status, language, age band, neighbourhood) — and have I run the proxy check?
3. Does every engineered feature have a one-line derivation recorded somewhere a future auditor can find — not in my head, on disk?

---

## Phase 4 — Candidates (Sprint 1 = clustering sweep; replayed in Sprint 2 for SML)

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ **USML ◉** ▸ SML ▸ Opt ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 1 · Phase 4 of 8 — Candidates
 LEVERS:        model family mix · sweep breadth · cross-validation · baseline inclusion
──────────────────────────────────────────────────────────────────
```

### Concept

Trying a fair range of approaches before committing — not to find "the best," but to make the eventual choice _defensible as a choice among alternatives_. Every candidate runs on the same features with the same stability protocol. A multi-family sweep against a naive baseline is what makes Phase 5's pick defensible.

### Why it matters (SML lens)

- Reinforces Week 4's AutoML candidate sweep: the leaderboard only means something if every model was trained on the same schema and same folds.
- Reinforces Week 2's "naive baseline" discipline — in Week 5, beat the CMO's hand-authored 5-segment rulebook, or don't ship.
- Reinforces Week 3's "complexity for its own sake is overfit" rule: a hierarchical clustering with 12 branches is usually a 5-segment result in a costume.
- Dollar framing: Week 4's leaderboard turned into a dollar decision because every model was comparable. Same here — incomparable candidates waste the whole phase.

### Why it matters (USML lens)

- **Clustering families make different shape assumptions.** K-means expects round blobs around a centre. DBSCAN expects dense pockets with gaps. Hierarchical builds a nested tree. If your data's real structure doesn't match the family's assumptions, the algorithm still produces clusters — they are just wrong in a way no plot reveals.
- **K-selection methods disagree.** Elbow, silhouette, gap statistic each answer a slightly different question. They frequently point to different K. None of them settles the K decision alone.
- **Dimensionality reduction has two purposes.** PCA as preprocessing (de-noise ~40 features before clustering). UMAP/t-SNE as visualisation (see whether clusters look like clusters on a 2D map). You need both.
- **Density-based approaches leave some customers unassigned** — that is the algorithm admitting "these customers don't fit any clear pattern." Whether 20% unassigned is acceptable is a product call, not an algorithm call.

> **Scaffold reality (tonight):** `AutoMLEngine` in kailash-ml 0.17.0 does NOT support clustering (task_type raises ValueError). The scaffold provides `/segment/fit` which runs the multi-family sweep directly. Your prompt asks for the sweep in business language; don't name AutoML.

### Your levers this phase

- **Lever 1 (the big one): model family mix.** USML: K-means + DBSCAN + spectral + hierarchical spans the assumption space. SML: linear + random forest + gradient-boosted ensemble. Always include ≥3 families spanning the bias-variance range.
- **Lever 2 (usually matters): sweep breadth.** How many K values? How many hyperparameters? For tonight's clock: K ∈ {3, 5, 7} for K-means + DBSCAN with 2 densities + spectral at 5. Five candidates, not twenty.
- **Lever 3 (the protocol): stability.** Same features, same test-set, same stability probe (seed, time, resample) across all candidates. Without this the leaderboard is uninterpretable.
- **Lever 4 (the floor): naive baseline.** Current rule-based segmentation (the 5-segment 2020 rulebook) is the baseline. If your best candidate doesn't clearly beat it, ship the baseline and save the money.
- **Skip unless specific:** extensive hyperparameter grids within a family (save for Phase 5 if a winner emerges); neural-net exotica (tabular data doesn't need it).

### Trust-plane question

Which 3–5 approaches are reasonable for this problem, and does the sweep produce comparable numbers?

### Prompt template — universal

> _"Run a candidate sweep for the [module]. Three families spanning different assumptions — one [linear/blob-expecting], one [tree-based/density-based], one [ensemble/hierarchical]. Use the same features, same stability protocol, same held-out set across all candidates. Include a naive baseline. Produce a leaderboard comparing them on the 3–5 signals I care about. Don't optimise hyperparameters yet — that's Phase 5 if one wins."_

> **For tonight's product (Sprint 1 USML):** _"Run a clustering sweep on Arcadia's active-customer behavioural features. Three algorithm shapes: K-Means at K=3, 5, 7; DBSCAN with two densities; one spectral approach. Same 7 features across all. Compare on silhouette, stability (re-seed Jaccard), and segment-size distribution. Also compare against the pre-baked K-sweep reference on disk. I'll pick the count and algorithm in Phase 5."_

### Evaluation checklist

- [ ] Candidates span an assumption range (not three variants of K-means).
- [ ] Each candidate has a stated reason for inclusion and a stated risk.
- [ ] A naive baseline is present on the leaderboard.
- [ ] All candidates on identical features + identical stability protocol.
- [ ] Comparison table uses the same signals for every row.

### Journal schema — universal

```
Phase 4 — Candidates
Candidates ran: ____
Shared protocol: features = ____, stability = ____, baseline = ____
Observations (numeric): ____
(Decision happens in Phase 5 — no journal decision here)
```

### Common failure modes

- AutoML-style prompt for clustering — the scaffold returns an error; student loses 10 minutes.
- Candidates on different features / different hold-outs — leaderboard is meaningless.
- Baseline omitted; student can't defend "beating the incumbent."

### Artefact

`data/segment_leaderboard.json` (live) + `data/segment_candidates.json` (pre-baked reference).

### Instructor pause point

- Show the leaderboard side by side. Ask: which candidate has the highest silhouette? Highest stability? Are they the same candidate? If not, what does that tell you about Phase 6?
- Draw three blob patterns on the whiteboard (concentric rings, two moons, four ellipses). Which family can find each? Why does K-means fail on concentric rings?
- Ask: if the density-based candidate leaves 22% of customers unassigned, is that better or worse than K-means putting 22% into a "misfit" cluster? Defend in business terms.

### Transfer to your next project

1. Have I tried at least three approaches that make genuinely different assumptions — or three variants of the same family?
2. Is my stability protocol comparable across candidates (same hold-out, same perturbation, same measurement)?
3. Is there a naive baseline on the leaderboard so the winner is defensibly better than doing nothing sophisticated?

---

## Phase 5 — Implications (Segment Selection)

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ **USML ◉** ▸ SML ▸ Opt ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 1 · Phase 5 of 8 — Implications
 LEVERS:        complexity-vs-interpretability · stability-vs-accuracy · speed-vs-performance
──────────────────────────────────────────────────────────────────
```

### Concept

Look at the Phase 4 leaderboard and make the human call: which approach, at which setting, do you stake your name on, and can you explain the trade-off in 30 seconds to someone who has never heard of silhouette. Every alternative gets rejected with a reason. "Claude Code recommended it" with no paragraph underneath is not a Phase 5.

### Why it matters (SML lens)

- Reinforces Week 4's model-selection discipline: top of the leaderboard is NOT automatically the pick. A Ridge that's 0.3% worse than XGBoost but trains in 2 seconds and is interpretable is often the right call for production.
- Reinforces Week 2's "defend in non-technical language" rule — if you can't explain it to the clinician/CMO/buyer, you can't ship it.
- Reinforces Week 3's fold-variance check: 82% mean precision with 15% fold-variance is more dangerous than 78% mean with 3% variance.

### Why it matters (USML lens)

- The "most statistically separated" clustering is often the **least actionable** — the algorithm finds a genuine pattern that marketing cannot build a campaign around ("customers who browse between 2–4 AM on Tuesdays").
- Each segment needs a **plain-language profile** — a paragraph a non-technical CMO can read. "Cluster 3: high_freq=0.81, low_promo_resp=0.22" is a statistical artefact; "customers who shop weekly on weekends and ignore promos" is a segment.
- **Stability trumps separation** in USML almost always. 0.62 silhouette with 88% stability beats 0.71 silhouette with 62% stability — the second one reshuffles 38% of customers each month, destroying every campaign plan.
- If a density-based approach leaves customers unassigned, the question isn't "is that OK" but "what is the cold-start fallback for those unassigned customers?" This cascades straight into Sprint 2.

### Your levers this phase

- **Lever 1 (the big one): complexity-vs-interpretability.** Complex model that wins by 0.02 silhouette but nobody can name the segments = lose. Simple model with slightly worse stats but named segments = win.
- **Lever 2 (usually matters): stability-vs-accuracy trade.** Always weight stability heavily; a "best" model that reshuffles monthly is unusable.
- **Lever 3 (only if scaling): speed-vs-performance.** If one candidate takes 10× to train for 2% gain, that only matters if you retrain often.
- **Skip unless specific:** hyperparameter micro-tuning (if you need to, do it here; don't leave it for Phase 8).

### Trust-plane question

Given the leaderboard, which approach do I stake my name on and why?

### Prompt template — universal

> _"Compare the candidates on the leaderboard. For each, tell me: how [accurate / well-separated], how stable across [time / seed / resample], how complex, and how long to train. Profile each cluster/class in plain business language — one paragraph each. Then recommend one — explain the trade-offs as if briefing someone who doesn't know what [silhouette / AUC / gini] is. I make the final pick."_

> **For tonight's product (Sprint 1):** _"Compare the five candidates on silhouette + stability + segment-size balance. For the winning candidate at each K value, profile each cluster in one paragraph of plain English ('these customers shop...') — no column names. Then recommend K and algorithm. Rank K=3 (the baseline) against K=5 and K=7 on all three signals. I'll pick."_

### Evaluation checklist

- [ ] Every candidate compared on the same metrics.
- [ ] Headline advantage classified as meaningful (multiple %) vs noise (<1%).
- [ ] Stability examined explicitly (not assumed).
- [ ] Each cluster / class has a one-paragraph plain-language profile.
- [ ] Recommendation defensible in 30 seconds to a non-technical executive.

### Journal schema — universal

```
Phase 5 — Implications (Chosen)
Picked: ____ (family × hyperparameters)
Named outputs (one line each): ____
Rejected alternatives + why: ____
Why not the top of the leaderboard, if applicable: ____
```

### Common failure modes

- Student picks top of leaderboard without checking stability — scores 2/4 on D3.
- Student accepts Claude Code's recommendation verbatim — no Trust-plane decision happened.
- Cluster names read like column dumps ("segment with high RFM_R, low RFM_F") — CMO can't act on them.

### Artefact

`workspaces/.../journal/phase_5_segment_selection.md`

### Instructor pause point

- Pick the winning candidate. Read one segment's profile aloud. Ask the class: would you build a campaign for this? What would it be called? If nobody has a name within 30 seconds, the segment is weak.
- Show two candidates — one with higher silhouette, one with higher stability. Ask: which do you ship? Whose career is on the line?
- Ask: if 18% of customers are unassigned in the winning candidate, what do you tell the CMO? Is "they get the default campaign" acceptable?

### Transfer to your next project

1. For every output class, can I write a one-paragraph plain-language profile a non-technical executive could act on tomorrow?
2. Am I picking on the single most impressive metric, or have I weighted stability and actionability at least as heavily as separation/accuracy?
3. What is my explicit rejection reason for every alternative on the leaderboard — and does it hold up to "you're just lazy" pushback?

---

## Phase 6 — Metric + Threshold (REPLACED for USML)

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ **USML ◉** ▸ SML ▸ Opt ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 1 · Phase 6 of 8 — Metric + Threshold (USML)
 LEVERS:        primary metric · threshold · class imbalance · calibration
──────────────────────────────────────────────────────────────────
```

### Concept

When there is no label, there is no single accuracy number to optimise. This phase replaces Week 4's "pick the metric, pick the threshold, tie to dollars" with a **three-floor commitment**: separation floor, stability floor, business-actionability floor. All three declared BEFORE you see the leaderboard. You pick the K that clears all three and maximises dollar lift versus the incumbent rule-based system.

**What's different from Week 4.** Week 4 asked "which accuracy metric, which threshold, tied to what costs?" and the answer was MAPE plus a conservative/moderate/aggressive interval with dollar cost per bucket. Week 5 has no MAPE. The conversation becomes **commit to floors** (pre-registration), not **optimise one number**. Dollar linkage is a **counterfactual vs the current rule-based system**, not raw cost-of-error.

### Why it matters (SML lens)

- Reinforces Week 4's metric-cost linkage: the leaderboard number only earns its keep when translated to dollars per month.
- Reinforces Week 3's cost-asymmetry logic — $45 wrong-segment and $18 converted-recommendation are the two sides of retail's ledger, mirroring $40/$1 fraud asymmetry.
- Reinforces Week 2/3's pre-registration rule: thresholds set AFTER seeing results are always conveniently where the leader landed. Cheating yourself.

### Why it matters (USML lens)

- **Separation** (silhouette or Davies-Bouldin) = how crisp are the clusters. Ship-by-separation-alone → segmentations that dissolve in two months.
- **Stability** (bootstrap Jaccard) = what fraction of customers stay in the same pair when you re-cluster on a different month or a different seed. Convention: 0.80 floor.
- **Actionability** = can marketing build a DISTINCT campaign for each segment? Not a number, a test. If two segments get the same one-line action, they are one segment with noise — collapse them.
- **Dollar lift via counterfactual** — not "how much does each error cost" but "how many fewer customers does this K send to the wrong campaign ($45 saved each) and how many more convertible clicks ($18 gained each) vs the 2020 rulebook." That's what turns a floor into a business case.

### Your levers this phase

- **Lever 1 (the big one): the three floors, pre-registered.** Separation floor (silhouette ≥ 0.25 is a typical minimum for real data), stability floor (Jaccard ≥ 0.80), actionability floor (one distinct campaign per segment — tested by naming). Declare BEFORE you see Phase 4 leaderboard.
- **Lever 2 (the business anchor): dollar counterfactual.** How many customers does this K re-route to a better campaign vs the rulebook? Multiply by $45.
- **Lever 3 (the reversal condition): what drops you back to the baseline?** "If stability drops below 0.80 on next month's re-cluster for two consecutive re-clusters, drop back to K-1."
- **Lever 4 (only for SML replay): class imbalance + calibration.** Not applicable to USML (no class).

### Trust-plane question

Which floors, at what values, tied to what dollar lift versus the incumbent?

### Prompt template — universal

> _"Given [cost asymmetry], which [metric / floors] should we commit to BEFORE seeing the leaderboard? Propose [three / one] pre-registration floor(s) with defensible values. Then compute the dollar lift counterfactual against the incumbent system. If peak season changes the economics, flag that. I pre-register the floors, then you compare against the leaderboard. I pick."_

> **For tonight's product (Sprint 1 USML):** _"Given $45 wrong-segment × 18,000 customers, propose the three USML floors (separation, stability, actionability) pre-registration. Set silhouette at 0.25, Jaccard at 0.80, actionability at 'one distinct marketing action per segment, tested by naming each'. Compute dollar lift of each K candidate vs the 2020 rulebook assuming a 5% mis-segmentation rate in the rulebook. I'll pick the K that clears all three floors AND maximises lift."_

### Evaluation checklist

- [ ] Three floors declared AT VALUES (not "high silhouette").
- [ ] Floors committed BEFORE seeing the leaderboard (timestamp in journal).
- [ ] Dollar lift computed as counterfactual vs incumbent.
- [ ] Reversal condition named (specific signal + threshold + duration).
- [ ] Chosen K passes all three floors, not just the best one.

### Journal schema — universal

```
Phase 6 — Metric + Threshold
Primary metric: ____ (reason: ____)
Floor 1: ____ at ____ (committed at timestamp ____)
Floor 2: ____ at ____
Floor 3: ____ at ____  (USML only)
Chosen operating point: K = ____  /  threshold = ____
Counterfactual lift vs incumbent (in declared unit): ____
Reversal condition: signal ____ + threshold ____ + duration ____
```

> **Retail instantiation:** Separation floor = silhouette ≥ 0.25; Stability floor = bootstrap Jaccard ≥ 0.80; Actionability floor = one distinct campaign per segment. Chosen K = 5; lift = $14,800/month vs 2020 rulebook. Reversal: stability < 0.80 for 2 consecutive monthly re-clusters → drop to K=4.

### Common failure modes

- Floors set AFTER seeing the leaderboard — 0/4 on D2.
- Dollar lift stated as "higher is better" without counterfactual — 1/4 on D2.
- Reversal condition stated as "if data changes" — 0/4 on D5.
- "Actionability" floor skipped because it's not a number — scores 1/4 on D3; this is the single biggest Sprint 1 rubric trap.

### Artefact

`workspaces/.../journal/phase_6_usml.md` (and `phase_6_sml.md` when replayed in Sprint 2).

### Instructor pause point

- Sketch a silhouette curve that peaks at K=2 and drops off. Ask: why isn't K=2 the answer? (Because the actionability floor rejects it.)
- Ask every student to write separation and stability floors silently, then compare. Spread is usually 0.55–0.75 for separation, 0.70–0.85 for stability. Ask: how did you pick?
- Demonstrate: take two segments from K=7 that got nearly identical one-line actions. Collapse, keep, or defend the difference in dollars?

### Transfer to your next project

1. What are my three analogues of separation / stability / actionability — whatever "signal quality," "time-robustness," and "business-action-distinctness" mean in my domain?
2. Did I commit to numeric floors BEFORE seeing the leaderboard, and can I prove it (timestamps, journal order)?
3. Is my dollar-lift a counterfactual against the _current_ system being replaced, or a raw cost-of-error floating in a vacuum?

---

## Phase 7 — Red-Team

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ **USML ◉** ▸ SML ▸ Opt ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 1 · Phase 7 of 8 — Red-team
 LEVERS:        subgroups · adversarial perturbations · proxy tests · acceptance
──────────────────────────────────────────────────────────────────
```

### Concept

Actively try to break the model before deployment does it for you. AI Verify frame — Transparency, Robustness, Safety — stays across weeks. Week 5 adds three USML-specific failure modes: **re-seed churn** (did the random seed, not the data, produce the segments?), **proxy leakage** (is a segment actually a demographic shadow?), **operational collapse** (does any segment shrink below 2% in one month, breaking the campaign it was built for?).

### Why it matters (SML lens)

- Reinforces Week 4's adversarial-drift dimension — "what does the model do on data it wasn't trained on" is universal.
- Reinforces Week 3's Safety dimension: the $220 PDPA breach and $45 wrong-segment are the concrete dollar handles for "who gets hurt when this silently fails."
- Reinforces Week 2's blast-radius rule — name the population that gets harmed, not "users."
- Reinforces the rule that Transparency failing is a finding, not a pass: if the algorithm doesn't expose feature importance, the limitation goes in the journal.

### Why it matters (USML lens)

- **Re-seed churn** has no SML analogue. If you re-run K-means with a different seed and 20% of customers move, the segmentation is a function of the seed, not a discovery.
- **Proxy leakage in USML is worse than SML.** In SML, the label forces you to notice when a protected attribute is doing the work. In USML, with no label, a demographic proxy masquerades indefinitely. Drop-one-demographic test: if the segment collapses, it was a proxy.
- **Operational collapse** — a small segment shrinks below your ability to run a campaign (e.g., below 2% of customers). This is also the Phase 13 drift signal; Phases 7 and 13 must use consistent thresholds.
- Small segments disproportionately contain vulnerable groups (new-to-market, under-18, low-income).

### Your levers this phase

- **Lever 1 (the big one): proxy-leakage audit.** For every apparent behavioural segment, run the drop-one-demographic test. If the segment dissolves when postcode/age is removed, the segment WAS demographics.
- **Lever 2 (the stability probe): re-seed / re-sample Jaccard.** Multiple seeds, multiple resamples. Report the distribution, not the mean.
- **Lever 3 (the operational stress): worst-subgroup severity.** Where does the model fail WORST — which customer segment, which month, which condition?
- **Lever 4 (the Safety frame): blast radius in dollars.** If this model silently went wrong for a week, what's the dollar damage AND who gets hurt?
- **Skip unless specific:** Fairness dimension (deferred to Week 7 — named in the journal explicitly so the deferral is not silent).

### Trust-plane question

How does this fail? What breaks it?

### Prompt template — universal

> _"Try to break this [model]. Three dimensions: (1) Transparency — what is it relying on most? Can you explain one prediction / one segment to a non-technical manager? (2) Robustness — where does it fail worst? Which subgroups, which months, which conditions? (3) Safety — if this silently went wrong for a week, what's the dollar damage and who gets hurt? Name every finding with severity. Fairness is deferred to Week 7 — flag any concerns and move on."_

> **For tonight's product (Sprint 1 USML):** _"Red-team the segmentation on three unsupervised-specific sweeps: (a) re-seed with 3 different random seeds and report the distribution of per-segment Jaccard stability, (b) drop-one-demographic proxy test on postal_district and age_band, (c) operational-collapse simulation: on Black-Friday-shaped data, does any segment shrink below 2%? Rank findings by severity in $."_

### Evaluation checklist

- [ ] **Transparency:** top 3 features per segment / class named; one-sentence plain-language explanation of one output.
- [ ] **Robustness:** 3 worst subgroups with metrics; 3 worst months / conditions; adversarial perturbation behaviour.
- [ ] **Safety:** tail-risk in dollars; degenerate-input behaviour; blast-radius memo naming who is harmed.
- [ ] Fairness row ends with "deferred to Week 7 per Playbook" — explicit, not silent.

### Journal schema — universal

```
Phase 7 — Red-Team
Transparency: top features ____; one-sentence explanation ____
Robustness: worst subgroups ____; worst conditions ____
Safety: worst-1% cost $____; degenerate-input behaviour ____; blast radius ____
USML-specific: re-seed Jaccard distribution ____; proxy collapse test ____; operational collapse ____
Fairness: deferred to Week 7 per Playbook
Blockers: ____
Accepted risks: ____
Mitigations to ship with: ____
```

### Common failure modes

- Red-team stops at "the model sometimes gets confused" — no specifics.
- Explainability output produced (feature importance) but not surfaced as a Transparency finding (orphaned call).
- Safety dimension skipped because it "feels abstract" — grounding in $220 and $45 forces it concrete.

### Artefact

`workspaces/.../journal/phase_7_red_team.md`

### Instructor pause point

- Re-run the winning clustering with three seeds. Students compute churn by hand. Above what threshold is the segmentation unshippable?
- Ask: if segment 3 collapses when postcode is dropped, what do you tell the CMO — "ship anyway" or "re-cluster"? Make the dollar trade-off explicit.
- Demonstrate: filter to post-Black-Friday data and re-cluster. Smallest segment? If below 2%, which campaign is now uneconomical?

### Transfer to your next project

1. What is my domain's analogue of re-seed churn (any source of randomness that could be driving the output rather than the data)?
2. What is my domain's analogue of proxy leakage (any protected-class feature that could be silently doing the work of an apparently-neutral output)?
3. What is the smallest population my product can act on economically, and what signal tells me when a population dropped below it?

---

## Phase 8 — Deployment Gate

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ **USML ◉** ▸ SML ▸ Opt ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 1 · Phase 8 of 8 — Deployment Gate
 LEVERS:        monitoring cadence · rollback channel · alert thresholds · promotion criteria
──────────────────────────────────────────────────────────────────
```

### Concept

The go/no-go. Write the criteria that must hold for this artefact to ship, the signals you monitor on day one, the specific measurable condition that triggers rollback. Then move the artefact from trial to shadow (or staging to production) in the registry. Every criterion is a signal and a threshold — no vibes.

### Why it matters (SML lens)

- Reinforces Week 4's ModelRegistry state-machine: illegal transitions blocked by the framework so you don't jump staging → production by accident.
- Reinforces Week 3's monitoring rule: "monitor production" means nothing; "monitor precision@50 weekly and alert when it drops below 0.62 for 2 consecutive weeks" is the point.
- Reinforces Week 2's "rollback is a path, not a wish" — you cannot roll back to a state that was never preserved.

### Why it matters (USML lens)

- The go signals are the **three floors from Phase 6**, not a single accuracy cutoff — the pre-commitment follows through.
- Monitoring signals include **segment-size stability**, **monthly reassignment rate**, and (where the segmentation feeds a recommender) **campaign open-rate-by-segment**. None of these exist in SML.
- **Rollback target is the previous rule-based system**, not a previous version of the same model — in USML "previous version" is a different random seed and isn't necessarily better. Rolling back to the 2020 rulebook is the honest fallback.

### Your levers this phase

- **Lever 1 (the big one): monitoring cadence.** Segmentation re-scores monthly; recommender drifts weekly; allocator daily. One alarm cannot watch all three.
- **Lever 2 (the rollback channel): shadow deployment.** Always promote to shadow before production. Production is the rollback channel's rollback channel.
- **Lever 3 (the alert thresholds): variance-grounded, not round numbers.** "15% drift" because it feels right is 1/4 on D5. "15% drift because the historical rolling variance has 95th percentile at 12%" is 4/4.
- **Lever 4 (the promotion criteria): the three floors re-tested, not re-declared.** The floors from Phase 6 must still hold on the deployment hold-out.

### Trust-plane question

Ship or don't ship, and on what monitoring?

### Prompt template — universal

> _"Write the go/no-go gate for deploying this [model]. Include: (1) what [metric thresholds / three floors] must hold, tied to the numbers from Phase 6, (2) what we monitor on day one — specific signals + alert thresholds + cadence, (3) what triggers automatic rollback — specific measurable signal, not 'if things look bad'. Then promote the model from trial to shadow via the registry."_

> **For tonight's product (Sprint 1):** _"Write the deployment gate for the chosen K=5 segmentation. Go/no-go on the three Phase-6 floors (0.25 / 0.80 / actionability). Monitoring: segment-size distribution weekly + per-segment reassignment monthly. Rollback trigger: any segment drops below 2% in one month. Promote K=5 from staging to shadow via /segment/promote."_

### Evaluation checklist

- [ ] Go/no-go criteria are measurable (named metric thresholds, not "it looks good").
- [ ] Monitoring plan names specific signals + alert thresholds + cadence.
- [ ] Rollback trigger is automatable (specific signal, not "if things go bad").
- [ ] Registry stage transition executed (shadow minimum).
- [ ] Rollback target is known to work today (not "a prior version we'd roll back to").

### Journal schema — universal

```
Phase 8 — Deployment Gate
Go / No-Go: ____
Monitoring (signal + threshold + cadence + owner): ____
Rollback trigger (specific signal): ____
Rollback target (known-working): ____
Registry transition: staging → ____
```

### Common failure modes

- Monitoring written as prose, no signals — grader cannot verify.
- Rollback trigger tied to non-existent signal.
- Rollback target is "a previous model" that doesn't exist / is worse than the baseline.
- Illegal registry transition attempted (production → staging directly).

### Artefact

`workspaces/.../journal/phase_8_gate.md` + registry record at shadow or higher.

### Instructor pause point

- Ask: what signal fires the rollback this week? Can the monitoring system actually watch it? If "someone would notice" — it is not a signal.
- Walk through registry states on the board. Why can trial → pre-production but not trial → production directly?
- Demonstrate: show a monitoring plan as prose. Ask the class to rewrite as signal + threshold + cadence + owner. Count missing fields.

### Transfer to your next project

1. What specific signal — nameable by a monitoring system — fires my rollback, and have I verified the signal is actually collectable in my pipeline?
2. What is my rollback _target_ — a prior model version, a rule-based system, or a no-op default — and is it known to work today?
3. Have I executed the registry/artefact transition so the deployment is a recorded event, not an implicit understanding?

---

## Phase 9 — Codify (Close block)

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ USML ✓ ▸ SML ✓ ▸ Opt ✓ ▸ MLOps ✓ ▸ **Codify ◉**
 THIS PHASE:    Close · Phase 9 of 14 — Codify
 LEVERS:        transferable lessons · domain-specific lessons
──────────────────────────────────────────────────────────────────
```

### Concept

Before you close the laptop, separate the lessons that transfer to any future ML product from the lessons that only apply to this domain. Three transferable, two domain-specific. Domain goes in the domain folder; transferable lessons append to the Playbook so future students inherit them.

### Why it matters (SML + USML + Opt + MLOps lenses)

- "Data quality matters" is not a lesson. "AutoML trials above 10 blow the Sprint-1 budget and add no discovery value" IS a lesson.
- Transfer test: would this apply if the product were a forecaster, classifier, recommender, or allocator next week?
- The best lessons are _things you almost got wrong tonight_ — not things that went smoothly.

### Your levers this phase

- **Lever 1 (the big one): separate transferable from domain-specific.** Five lessons total, three transferable + two domain-specific is the Codify budget.
- **Lever 2 (the discipline): name the near-miss.** Every transferable lesson pairs with a sentence that starts "the failure mode this prevents is \_\_\_\_".
- **Lever 3 (the persistence): append to the right place.** Transferable → update the Playbook's appendix OR write to `.claude/skills/project/`. Domain-specific → domain folder only.

### Trust-plane question

What transfers to the next domain?

### Prompt template — universal

> _"Looking back at all four sprints — what did we learn that applies to ANY ML product we build next week? Give me 3 transferable lessons. And 2 things that are specific to [this paradigm / domain] that won't transfer. Each lesson names the near-miss that motivated it. Append transferables to the Playbook appendix; write domain-specific to the domain's skill file."_

### Evaluation checklist

- [ ] 3 transferable lessons (domain-agnostic, paradigm-agnostic).
- [ ] 2 domain-specific lessons (retail + USML + recommender + allocator).
- [ ] Each lesson includes the near-miss it prevents.
- [ ] Transferable lessons appended to the Playbook appendix (not just the session journal).

### Journal schema — universal

```
Phase 9 — Codify
Transferable:
1. ____ (near-miss prevented: ____)
2. ____ (near-miss prevented: ____)
3. ____ (near-miss prevented: ____)
Domain-specific:
1. ____
2. ____
```

### Common failure modes

- Codify skipped because time ran out — systemic knowledge capture lost.
- Lessons written as platitudes ("be careful") — no near-miss, no transfer.
- Transferable lessons saved only to the session journal — Week 6 students never see them.

### Artefact

`workspaces/.../journal/phase_9_codify.md` + `.claude/skills/project/week-05-lessons.md` + Playbook appendix update.

### Instructor pause point

- Ask: of the five decision moments tonight, which one felt least confident? That is the transferable lesson.
- Ask: which piece was hard _because retail_, and which was hard _because USML+SML+Opt_? Second transfers; first doesn't.
- Demonstrate: read two students' lesson lists. Interchangeable = both too generic. Sharpen with the class.

### Transfer to your next project

1. What did I almost get wrong tonight, and what signal would tell me I'm about to repeat it on a different product?
2. Of my lessons, which would still be true if the product were a classifier / forecaster / recommender / allocator instead of this week's shape?
3. Have I written the domain-specific ones somewhere a future me or a teammate picking up this domain can find, not buried in a chat log?

---

# SPRINT 2 — SML · Predict · Phases 4–8 (replayed)

**What changes in the replay.** Phases 1–3 are shared — the frame, the data audit, the feature classification all apply across Sprints 1 and 2. You RE-RUN Phases 4–8 for the SML classifiers (churn + conversion), producing `journal/phase_{4..8}_sml.md` alongside Sprint 1's `phase_{4..8}_usml.md`. Two artefacts this sprint: churn classifier + conversion classifier. Same family sweep (LR + RF + GBM) and same levers.

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ USML ✓ ▸ **SML ◉** ▸ Opt ▸ MLOps ▸ Close
 THIS SPRINT:   Predict · Phases 4→8 on churn + conversion
 LEVERS:        ensemble-is-the-king · class imbalance · PR curve · calibration
──────────────────────────────────────────────────────────────────
```

## Phase 4 (SML replay) — SML Candidates

### Concept

Same structure as Phase 4 USML — multi-family sweep — but now with labels. Three families spanning the bias-variance range: linear (logistic regression), tree bag (random forest), ensemble (gradient-boosted — **the king for tabular**).

### Why it matters (SML lens — the DEPTH Week 4 skipped)

- **Logistic regression** is your floor and your sanity check. Interpretable, fast, small variance. Not including it is a tell that you don't know what a baseline is.
- **Random forest** is the cheap tree-based default. Handles non-linearity without feature engineering. Variance comes from the bagging, bias from the tree depth.
- **Gradient-boosted trees (XGBoost / LightGBM / sklearn GBM) is the ensemble that usually wins.** It builds trees sequentially, each correcting the previous one's residual errors. The loss function can be mean-squared error (for regression) or log-loss (for classification). Regularization via learning rate + tree depth + number of estimators. **For tabular data this is the default-winning family unless you have a specific reason.**
- **Neural nets** are almost always overkill for tabular data <1M rows. Reach for them only when you have heterogeneous inputs (text + image + tabular) or very large data. If you find yourself reaching for neural, first check that your GBM is properly regularized.

### Your levers this phase

- **Lever 1 (the big one): include an ensemble.** If your sweep doesn't have GBM / XGBoost / LightGBM, your leaderboard is incomplete.
- **Lever 2 (the cross-validation protocol):** for time-series-like data use temporal CV (train on past, test on future). For i.i.d. data use stratified k-fold. For imbalanced classes use stratified sampling (preserves base rate in each fold).
- **Lever 3 (the sweep breadth):** three families; each with 1–2 hyperparameter settings. Not twenty candidates with random hyperparameters.
- **Lever 4 (the naive baseline):** majority class prediction. Beat it or don't ship.

### Trust-plane question

Which 3 model families give me a fair leaderboard for this SML task?

### Prompt template — universal

> _"Run an SML candidate sweep for [target]. Three family-diverse candidates: linear (e.g., logistic regression), tree bag (e.g., random forest), ensemble gradient-boosted (the usual winner for tabular). Same features, same stratified CV, same held-out test set. Report AUC, precision and recall at a default threshold, Brier score (calibration), and feature importance. Include a majority-class baseline. I'll pick."_

> **For tonight's product (Sprint 2 SML):** _"Run the sweep for CHURN (label = days_since_last_visit > 90) on the 7 non-leakage behavioural features. Then re-run for CONVERSION (label = customer-category interaction in last 90 days). Same three families each time: logistic regression + random forest + gradient-boosted. I'll compare Sprint 2's ensembles vs linear baseline."_

### Evaluation checklist

- [ ] At least one ensemble family on the leaderboard.
- [ ] Linear baseline present.
- [ ] Identical features, identical CV split, identical test set across candidates.
- [ ] AUC + precision + recall + Brier score reported for each.
- [ ] Feature importance exposed (top 5 features per model).

### Journal schema — universal

```
Phase 4 SML — Candidates
Target: ____ (label definition: ____)
Candidates: linear ____ | tree bag ____ | ensemble ____ | baseline ____
Protocol: CV = ____, stratification = ____, test size = ____
Observations: AUC range ____; Brier range ____; top features ____
```

### Common failure modes

- No ensemble in the sweep — the "the king" is absent and you can't justify your pick.
- Features that include the label (data leakage) — AUC will be suspiciously close to 1.0.
- Test-set bleed into the CV (same rows in both) — leaderboard overstated.

### Artefact

`GET /predict/leaderboard/churn` and `GET /predict/leaderboard/conversion` responses + `journal/phase_4_sml.md`.

### Instructor pause point

- Show the churn leaderboard. Ask: which family wins? By how much? Is the advantage "worth the complexity"?
- Ask: if the linear model is within 1% AUC of the GBM, which do you ship and why?
- Demonstrate: look at feature importance — is one feature doing 80%? Leakage suspect?

### Transfer to your next project

1. Does my sweep include at least one ensemble (GBM / XGBoost / LightGBM)? If no, why not?
2. Is my CV protocol appropriate for the data's temporal / hierarchical structure?
3. Have I run a naive baseline so my winner is defensibly better than no ML?

---

## Phase 6 (SML replay) — SML Metric + Threshold

### Concept

The SML variant that Week 4 couldn't go deep on. This is the classifier's threshold-selection phase. Read the PR curve, pick the operating point, tie it to dollars.

### Why it matters (SML lens — the DEPTH Week 4 skipped)

- **ROC curve** shows the classifier's ranking ability across all thresholds. AUC summarises it. **Use AUC when classes are balanced OR you care about ranking, not decisions.**
- **PR curve** shows precision vs recall across thresholds. **Use PR when positives are rare (churn, fraud, conversion) — ROC is overly optimistic on imbalanced data.**
- **Cost-based threshold selection.** For each threshold, compute expected cost = (P(FP) × cost_FP) + (P(FN) × cost_FN). Pick the threshold that minimises expected cost. This is what turns your leaderboard into a dollar decision.
- **Calibration** (Brier score, reliability diagram) — if the model says 30% probability, do 30% of those cases actually happen? A well-calibrated model's probabilities are trustworthy; a miscalibrated model's rankings are fine but its probabilities are not. If you use probabilities directly (e.g., expected-revenue allocator), calibration matters. Platt scaling and isotonic regression are the two standard fixes.
- **Class imbalance handling.** When positives are <10%: stratified sampling in CV, class weights in the loss, or SMOTE-style resampling. The threshold selection needs to happen AFTER rebalancing.

### Your levers this phase

- **Lever 1 (the big one): threshold on the PR curve.** For rare positives, find the threshold that maximises F1 or meets a precision target (e.g., "precision ≥ 0.6 at minimum recall 0.5").
- **Lever 2 (the cost-asymmetry):** if FN cost is 5× FP cost, push threshold LOWER (more alarms, catch more positives). If FP cost is 5× FN cost, push threshold HIGHER (fewer alarms, only confident positives).
- **Lever 3 (the calibration):** if you use the probability directly (not just rank), run calibration (Platt / isotonic). Raw GBM probabilities are usually miscalibrated.
- **Lever 4 (the imbalance):** stratified sampling, class weights, or resampling.

### Trust-plane question

At what threshold does this classifier earn its dollars?

### Prompt template — universal

> _"Given [cost_FN] per false negative and [cost_FP] per false positive, pick the decision threshold for [target]. Show me the PR curve. Compute expected cost across threshold values from 0.1 to 0.9 in 0.05 steps. Recommend the cost-minimising threshold. If the model is miscalibrated (Brier > [floor]), run calibration and redo. I set the threshold; you set the operating point."_

> **For tonight's product (Sprint 2 SML churn):** _"Churn cost structure: $120 CAC to reacquire a churned customer vs $3 to send them a retention touch. Pick the threshold on the PR curve that minimises expected cost. If Brier score is > 0.04, run isotonic calibration. Default to 0.30 if calibration is already good."_

### Evaluation checklist

- [ ] PR curve read + operating point named (not "I chose 0.5 because default").
- [ ] Threshold tied to cost asymmetry (dollar math shown).
- [ ] Calibration checked (Brier); re-calibrated if needed.
- [ ] Class imbalance addressed (stratification / weights / resampling noted).
- [ ] Reversal condition named (what signal flips this threshold decision).

### Journal schema — universal

```
Phase 6 SML — Metric + Threshold
Primary metric: ____ (ROC-AUC / PR-AUC / F1 / precision@recall-X / calibrated-Brier)
Cost asymmetry: FN = $____, FP = $____, ratio = ____
Chosen threshold: ____ (expected cost = $____ per 1,000 predictions)
Calibration: Brier = ____ (adjusted? ____)
Class imbalance handling: ____
Reversal condition: signal ____ + threshold ____ + duration ____
```

> **Retail instantiation (churn):** CAC = $120, touch cost = $3 → ratio 40:1. Pick threshold at 0.22 (per PR curve); expected cost ≈ $1,800 per 1,000 predictions. Brier = 0.03 — no recalibration needed. Reversal: if 7-day calibration error > 0.05 for 2 weeks, re-train.

### Common failure modes

- Threshold at 0.5 because "that's the default" — 0/4 on D2.
- ROC used for rare-positive problem — threshold looks good but product is miscalibrated for imbalanced reality.
- Calibration skipped when probabilities feed downstream (allocator) — the downstream allocator optimizes against bad numbers.
- Reversal condition = "if model does poorly" — 0/4 on D5.

### Artefact

`POST /predict/threshold` with justification + `journal/phase_6_sml.md`.

### Instructor pause point

- Draw the PR curve on the whiteboard. Ask: why do we care about PR, not ROC, for churn?
- Ask: if touching everyone costs $3 and re-acquiring a churned customer costs $120, at what threshold do you send a retention offer? Compute live.
- Show a miscalibrated output (30% predicted → 50% actual). Ask: if the allocator uses this probability, what goes wrong?

### Transfer to your next project

1. Which curve applies to MY problem — ROC (balanced) or PR (rare positives)?
2. What is my cost asymmetry in dollars, and did my chosen threshold actually minimise expected cost (not just "feel right")?
3. Are my probabilities calibrated? If a downstream system uses them, calibration is not optional.

---

## Phase 5, 7, 8 (SML replay)

Same shape as Sprint 1 phases, applied to the classifiers. The levers and failure modes transfer. Key differences:

**Phase 5 SML — Implications.** Pick between logistic regression, random forest, GBM. Ensemble usually wins but not by enough to justify complexity over LR + domain features. Profile each model: "LR picks up weekend_browse_fraction and visits_per_week most; GBM picks up interactions between them." Name the winning family in one paragraph a non-technical executive could act on.

**Phase 7 SML — Red-team.** Re-seed the split, report variance. Drop-one-feature proxy tests: does any classifier rely on age_band (PDPA)? Worst-subgroup severity: which customer segment does the classifier most mispredict? Calibration per subgroup — are probabilities equally reliable across segments?

**Phase 8 SML — Gate.** Promote churn classifier + conversion classifier to shadow. Monitoring: calibration drift weekly, AUC decay monthly, per-subgroup performance gaps. Rollback: calibration error > 0.08 for 2 weeks OR AUC drop > 3 points.

All three journal entries (`phase_5_sml.md`, `phase_7_sml.md`, `phase_8_sml.md`) follow the same schema as Sprint 1.

---

# SPRINT 3 — OPTIMIZATION · Decide · Phases 10–12

**Why these are separate phases.** Phases 10–12 apply when your product has a **secondary optimization layer** on top of the models (allocator, scheduler, solver). Arcadia has one: given segments × predicted responses × budget × constraints, allocate campaigns optimally. Week 4's route planner was the Sprint 3 equivalent. **Deferrable** if your next project has no secondary layer (pure classification, pure clustering).

---

## Phase 10 — Objective Function

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ USML ✓ ▸ SML ✓ ▸ **Opt ◉** ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 3 · Phase 10 of 12 — Objective
 LEVERS:        single-vs-multi · weight assignment · proxy metrics · coverage floors
──────────────────────────────────────────────────────────────────
```

### Concept

Defining "good" for a product that has a secondary optimization layer. "Good" is almost never one number — it's 3–5 competing signals (revenue, reach, diversity, touches, cost, fairness). You present both a single-objective framing (weighted sum) and a multi-objective framing (separate scores with a Pareto frontier). Recommend one; defend weights; name honestly what each framing sacrifices.

### Why it matters (SML + Optimization lens — the DEPTH Week 4 skipped)

- **Loss functions in SML ARE objective functions.** Cross-entropy (classification), MSE (regression), hinge (SVM). The choice shapes what the model optimizes.
- **Linear programming objective.** `minimise c^T x` where `c` is the cost vector, `x` is the decision. Every LP has an objective; choosing it IS the job.
- **Dual variables and shadow prices.** When an LP solves, each constraint has a **shadow price** = the marginal improvement in the objective if the constraint were relaxed by one unit. "What's it worth to add one more touch to the budget?" = shadow price of the touch-budget constraint.
- **Pareto frontier.** For multi-objective problems, a Pareto-optimal point is one where you can't improve one objective without worsening another. The frontier is the set of all Pareto-optimal points. You pick on it by declaring weights.
- **Coverage / fairness floors as constraints, not as objectives.** If you optimize revenue and _hope_ for diverse coverage, you'll get a monoculture. Coverage belongs in the constraint set (Phase 11), not in the objective (Phase 10). The objective is what you _maximise_; the constraint is what you _respect_.

### Your levers this phase

- **Lever 1 (the big one): single vs multi-objective.** Single-objective = everything in one weighted sum → simpler, may hide trade-offs. Multi-objective = separate scores → honest, harder to action. Default to single WITH coverage/fairness in constraints; go multi when stakeholders explicitly disagree on trade-offs.
- **Lever 2 (the weight-assignment): defend in dollars.** Each term in the objective has a dollar interpretation: revenue is $, reach is $/customer, diversity is $/category-covered (via long-tail protection). Weights come from stakeholder conversation + dollar math.
- **Lever 3 (the proxy-metrics rule):** some signals (serendipity, customer-happiness) are proxies for long-term revenue. Name them as proxies; don't pretend they're direct.
- **Lever 4 (the skip):** coverage/fairness/diversity BELONGS in Phase 11 constraints, not Phase 10 objective.

### Trust-plane question

Single-objective (revenue only, with coverage as constraint) or multi-objective (revenue AND reach AND diversity with weights)? What are the weights, and what does each framing sacrifice?

### Prompt template — universal

> _"Design the objective for [secondary layer]. Name the competing signals (expect 3–5). Show me two framings: single-objective (weighted sum, with secondary signals as constraint floors) and multi-objective (separate scores, Pareto frontier). For each, state what it sacrifices. Recommend one with defensible weights; I approve."_

> **For tonight's product (Sprint 3):** _"Objective for campaign allocator: expected revenue ($18 per converted click, $14 per wasted impression) + reach (customers touched) + diversity (cross-segment coverage). Single-objective with diversity as a coverage floor (Phase 11) is the default; propose multi-objective framings only if single loses more than 10% revenue. Show me shadow prices on the touch budget + PDPA constraint."_

### Evaluation checklist

- [ ] Every term has a dollar value or a named proxy.
- [ ] Single-objective AND multi-objective both presented.
- [ ] Weights defended with stakeholder reasoning (not "they feel right").
- [ ] Shadow prices shown for main constraints (touch budget, PDPA).
- [ ] Trade-off discussed honestly ("X weighting sacrifices Y").

### Journal schema — universal

```
Phase 10 — Objective
Mode: single | multi
Terms + weights: ____
Business justification: ____
Shadow price of key constraint: ____
Known limitation (what this framing sacrifices): ____
Reversal: if ____ changes, switch to ____
```

### Common failure modes

- Objective written in math-y language with no business grounding.
- Coverage / diversity in objective, not constraints → monoculture output.
- Weights pulled from thin air — 0/4 on D3.
- Shadow prices not surfaced — student doesn't learn what relaxing each constraint is worth.

### Artefact

`POST /allocate/objective` with justification + `journal/phase_10_objective.md`.

### Instructor pause point

- Whiteboard a 2×2: revenue high/low × reach high/low. Where does "hero SKU to everyone" land? Where's "long-tail showcase"? Where's Arcadia's target?
- Have students write weights silently on sticky notes. Compare. 2× differences = class disagrees on "good."
- Ask: the allocator's shadow price on the touch budget is $12 per extra touch. Do we raise the budget? How much?

### Transfer to your next project

1. What are the 3–5 competing signals "good" actually means in MY domain — and am I pretending one doesn't exist because it's hard to measure?
2. Does each signal have a dollar value or a named proxy? Am I willing to defend the weights in front of a sceptical executive?
3. Is coverage / fairness / diversity in my objective (where it will get sacrificed) or in my constraints (where it will be enforced)?

---

## Phase 11 — Constraint Classification

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ USML ✓ ▸ SML ✓ ▸ **Opt ◉** ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 3 · Phase 11 of 12 — Constraints
 LEVERS:        hard-vs-soft · penalty calibration · demotion rules · regulatory triggers
──────────────────────────────────────────────────────────────────
```

### Concept

For each rule the system must respect, classify **hard** (law, physics, contract — never crossable) or **soft** (preference — we'd rather not, at what price). Soft constraints get dollar penalties. Hard constraints get a regulatory/physical reason. When the world changes mid-sprint (the PDPA injection), re-classify and save both passes — before and after.

### Why it matters (SML + Optimization lens)

- **LP constraints are linear inequalities.** `A x ≤ b`. A hard constraint forbids `A x > b`; a soft constraint allows `A x > b` at a cost (`+ λ (A x − b)` in the objective with penalty coefficient λ).
- **Dual / shadow prices on hard constraints** tell you the cost of the regulation. If the PDPA hard constraint has shadow price $50k, that's the dollar cost of compliance.
- **Slack variables** make soft constraints workable: `A x − s ≤ b` where `s ≥ 0` is the violation, and `c^T x + λ · s` is the penalized objective.
- **Infeasibility diagnosis.** When no `x` satisfies all hard constraints, the LP is infeasible. Fix: demote a hard constraint to soft with a big penalty, or widen the budget. Infeasibility is a product problem, not a solver problem.

### Your levers this phase

- **Lever 1 (the big one): hard-vs-soft classification.** Law / contract / physics → hard. Preference / convenience → soft.
- **Lever 2 (the soft-constraint penalty):** in dollars per unit of violation. "$2 per touch over the per-segment cap" — defensible? The penalty should make the solver trade off soft constraint violation against objective gain.
- **Lever 3 (the demotion rule):** if all-hard produces infeasibility, demote to soft with a reasoned penalty. Document which one demoted and why.
- **Lever 4 (the regulatory trigger):** when a law changes mid-sprint (the PDPA injection), re-classify + re-solve. Save both passes as separate journal entries.

### Trust-plane question

Hard or soft for each rule? Penalty for each soft?

### Prompt template — universal (first pass)

> _"List every rule the [system] must respect. For each: hard (law/physics/contract) or soft (preference with penalty)? For soft, propose a dollar penalty per unit of violation. Justify each classification. Show me which pairs (objective × constraint) would change if I demoted a hard to soft or vice versa."_

> **Universal (post-injection re-run):** _"[Regulatory event] changes [rule] — re-classify. Document the change in a separate journal entry. Show the old pass and the new pass side by side. Explain the cost of the new hard classification in $ (shadow price)."_

> **For tonight's product (first pass):** _"Classify Arcadia allocator rules — touch budget, per-segment fatigue cap, PDPA under-18 browsing, inventory availability, brand exclusion list. Hard or soft with penalty. Defend each."_

> **For tonight's product (PDPA injection):** _"Legal has classified under-18 browsing history as a PDPA §13 hard exclusion (was soft before). Re-classify. Re-solve the allocator with the new hard constraint. Report the dollar cost of compliance (shadow price). Save `phase_11_postpdpa.md`."_

### Evaluation checklist

- [ ] Every constraint classified with explicit rationale (law / contract / physics / preference).
- [ ] Soft constraints have defensible penalty values.
- [ ] No constraint labelled "probably hard" without a reason.
- [ ] Post-injection: PDPA correctly re-classified as hard (PDPA §13).
- [ ] Post-injection re-solve produces a different plan than pre-injection.

### Journal schema — universal

```
Phase 11 — Constraints
Hard: ____ (regime + reason each)
Soft: ____ (penalty $ each)
What changed post-injection (if applicable): ____ (from ___ to ___)
Shadow price of key hard: $ ____ (cost of compliance)
```

### Common failure modes

- Constraint mis-classified as soft when law says hard (PDPA!) — 1/4 on D4.
- All-hard produces infeasibility → student panics instead of demoting one.
- Penalty values unspecified ("some penalty") — LP solver can't use them.
- Student writes `phase_11_postpdpa.md` but doesn't re-solve the LP — Phase 12 still has the old plan.

### Artefact

`POST /allocate/constraints` + `journal/phase_11_constraints.md` + `journal/phase_11_postpdpa.md`.

### Instructor pause point

- Inject PDPA live. Ask every student to re-classify the under-18 browsing feature in 90 seconds. Collect. Anyone still at "soft" loses D4 — discuss why.
- Draw the constraint ladder: law → contract → preference → convenience. Place 5 rules.
- Ask: if 3 constraints are hard and the allocator is infeasible, what went wrong? Walk the recovery (demote one + justify).

### Transfer to your next project

1. For each constraint, can I name the exact law / contract clause / physical limit that makes it hard — or is "probably hard" doing the work?
2. For each soft constraint, is the penalty a real dollar or hand-wave — and does it actually change the system's behaviour (traced to the objective function, not just the journal)?
3. When the regulator changes the rules mid-project, do I have a process to re-classify in writing, save the before/after, and re-run — or will I just patch and hope?

---

## Phase 12 — Solver Acceptance (REPLACED for Optimization)

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ USML ✓ ▸ SML ✓ ▸ **Opt ◉** ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 3 · Phase 12 of 12 — Solver Acceptance
 LEVERS:        held-out choice · pathology detection · accept/retune/redesign · rollback readiness
──────────────────────────────────────────────────────────────────
```

### Concept

The solver runs. It returns a plan. You check: feasibility (every hard constraint satisfied), optimality (how close to the LP optimum), pathologies (one segment getting 90% of the plan, dead campaigns with zero allocation). Decide: accept, re-tune (change weights or penalties), fall back (demote a hard constraint), or redesign (the problem is ill-posed).

### Why it matters (Optimization lens — the DEPTH Week 4 skipped)

- **Feasibility first, optimality second.** An infeasible LP returns no plan. A feasible-but-pathological plan returns an unusable one. Both are failures; the diagnosis differs.
- **Optimality gap.** Distance from the LP optimum (or the LP relaxation upper bound for MIP). Gap > 5% → either tighten the solver or accept the sub-optimality with a reason.
- **Pathology detection.** Feasible plans can still be wrong: concentration (one output gets the whole plan), dead variables (unused campaigns / SKUs / routes), boundary cases (the solver chose an extreme corner of the polytope).
- **Sensitivity analysis.** How robust is the plan to small changes in the objective weights or constraint values? If weight_revenue = 0.95 gives plan A but weight_revenue = 0.93 gives plan B, your plan is fragile.

### Your levers this phase

- **Lever 1 (the big one): pathology detection.** Concentration (one segment > 60%), dead campaigns (0 allocation), boundary solutions (activity at 100% of budget when you expected 80%).
- **Lever 2 (the decision):** accept, re-tune, fall back, redesign. Don't default to accept; the solver being feasible is not the same as the plan being shippable.
- **Lever 3 (the rollback readiness):** the prior plan. Is the current plan better than the prior plan by the dollar lift you expected? If not, stay with the prior.
- **Lever 4 (the sensitivity):** perturb the weights by ±10% and re-solve. If the plan is stable, ship. If it flips, your decision is on a knife edge.

### Trust-plane question

Is the solution feasible, optimal, edge-case safe, and pathology-free?

### Prompt template — universal

> _"Run the [solver] with the Phase 10 objective and Phase 11 constraints. Report: (a) feasibility per hard constraint, (b) optimality gap, (c) pathologies — concentration, dead variables, boundary solutions, (d) sensitivity: perturb weights by 10% and re-solve. Recommend accept / re-tune / fall back / redesign; I decide. Save the plan."_

> **For tonight's product (Sprint 3):** _"Run the allocator with the current objective + constraints. Report: PDPA active yes/no, touch budget used / remaining, per-segment concentration, dead campaigns. Run sensitivity: weight_revenue ± 0.05. Pathology list. Decide: accept the plan, re-tune weights, demote PDPA (don't!), or redesign."_

### Evaluation checklist

- [ ] Every hard constraint confirmed satisfied.
- [ ] Optimality gap reported numerically.
- [ ] Pathologies named (concentration, dead variables, boundary cases).
- [ ] Sensitivity checked (perturb ± 10%).
- [ ] Accept / re-tune / fall back / redesign decision defended.
- [ ] Post-injection re-run: `phase_12_postpdpa.md` on disk alongside `phase_12_accept.md`.

### Journal schema — universal

```
Phase 12 — Solver Acceptance
Feasibility per hard constraint: ____
Optimality gap: ____
Pathologies: ____
Sensitivity (± 10%): plan stable? ____
Decision: Accept / Re-tune / Fall back / Redesign
Reason: ____
Prior-plan comparison: expected lift = ____; actual lift = ____
What would make me re-design: ____
```

### Common failure modes

- Solver returns feasible but pathological plan (one segment 90%). Student accepts because "feasible" — 1/4 on D3.
- Optimality gap not surfaced (solver reports it; student doesn't read it).
- Sensitivity skipped — plan ships on a knife edge.
- Post-injection plan overwrites pre-injection (state corruption).

### Artefact

`POST /allocate/solve` response saved to `data/allocator_last_plan.json` + `journal/phase_12_accept.md` + `journal/phase_12_postpdpa.md`.

### Instructor pause point

- Show the 3-segment concentration plot. Ask: 70% of the plan in one segment — is this shippable?
- Demonstrate: perturb weight_revenue by 10%. Plan changes? By how much?
- Ask: PDPA re-solve shows $50K of shadow-price cost. Do we accept? What's the business defence?

### Transfer to your next project

1. Does my solver return **feasible** AND **pathology-free**? Did I check for concentration, dead variables, boundary solutions?
2. What is the optimality gap, and is it tight enough for the decision's dollar stakes?
3. Is my plan stable under ± 10% perturbation of the weights, or is it on a knife edge?

---

# SPRINT 4 — MLOPS · Monitor · Phase 13

---

## Phase 13 — Drift (× 3 models tonight)

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ USML ✓ ▸ SML ✓ ▸ Opt ✓ ▸ **MLOps ◉** ▸ Close
 THIS PHASE:    Sprint 4 · Phase 13 of 14 — Drift Monitoring
 LEVERS:        signal choice · threshold grounding · duration window · HITL-vs-auto
──────────────────────────────────────────────────────────────────
```

### Concept

Setting up monitoring for the day after launch. Reference data registered; current-week data checked. You propose signals and thresholds grounded in historical variance, classify each rule as human-in-the-loop or automatic. The retrain decision stays in the Trust Plane; the monitoring system reports signals, it does not pull the trigger.

**Three models tonight, three drift rules.** Segmentation (USML) drifts on **membership churn** — fraction of customers who move segments monthly. Churn classifier (SML) drifts on **calibration decay + feature PSI**. Allocator (Opt) drifts on **constraint-violation rate + feasibility rate**. Not one alarm — three, with separate cadences.

### Why it matters (SML + USML + Opt lenses — the DEPTH Week 4 skipped)

- **Feature drift (PSI)** measures distributional shift in input features. PSI < 0.1 stable, 0.1–0.25 moderate, > 0.25 severe.
- **Performance decay** measures target-related drift. For SML: AUC decay, precision decay, recall decay. For USML: cluster-stability decay (re-cluster + compare).
- **Calibration drift** measures whether predicted probabilities still match actual rates. A classifier can have stable AUC and drifted calibration.
- **Concept drift** (label definition changes over time) is the subtlest. If "churn" means "90 days of inactivity" today and will mean "60 days" next year, your label is moving. Monitor your definitions.
- **Virtuous drift** (the model got better!) is also drift. If your customer base is maturing and the old threshold is too sensitive, the model needs retraining to benefit from the shift — not just when it degrades.
- **Don't retrain on seasonal spikes.** Black Friday, Chinese New Year, payday. These look like drift but are known seasonality. Duration window + HITL on first trigger.

### Your levers this phase

- **Lever 1 (the big one): signal choice per model.** Segmentation = membership churn %. Classifier = calibration error + AUC decay + feature PSI. Allocator = constraint-violation rate.
- **Lever 2 (threshold grounding):** historical rolling variance, not round numbers. "0.15 because it's the 95th percentile of weekly drift variance in the past year" = 4/4. "0.15 because that's sort of big" = 1/4.
- **Lever 3 (duration window):** 1 day of drift = usually seasonality or single-day anomaly. 7 days = real. 30 days = definitely. Pick based on the cost of a false-positive retrain.
- **Lever 4 (HITL vs auto):** first trigger always HITL (human approves). Repeat triggers may auto-retrain if the process has been stable for multiple cycles.

### Trust-plane question

When do we retrain? What is the rule?

### Prompt template — universal

> _"Set up drift monitoring for [model(s)]. First confirm reference data is registered. For each model, name: (1) primary drift signals (at least one distributional, one performance), (2) thresholds grounded in historical variance, (3) duration window that distinguishes drift from seasonality, (4) human-in-the-loop-vs-automatic for first trigger. If multiple models, separate rules per model. Flag any seasonal dates in the reference window that should be excluded."_

> **For tonight's product (Sprint 4):** _"Three drift rules: (a) segmentation = monthly segment-membership churn, threshold = 12% grounded in the training window's weekly variance; (b) churn classifier = weekly calibration error + AUC decay > 3 points; (c) allocator = daily constraint-violation rate, threshold = 5%. Duration: 2 consecutive triggers for segmentation, 1 for classifier, 3 for allocator. HITL on first trigger for all three. Exclude Nov–Dec from the segmentation baseline."_

### Evaluation checklist

- [ ] Reference data confirmed registered for every model.
- [ ] Primary + secondary signals named per model.
- [ ] Thresholds grounded in historical variance, not round numbers.
- [ ] Duration window prevents retrain-on-spike.
- [ ] HITL-vs-auto classified with reason.
- [ ] Retrain decision stays in Trust Plane (no "auto-retrain on X" without HITL first).

### Journal schema — universal

```
Phase 13 — Retrain Rule (per model)
Model: ____
Signal(s): ____
Threshold(s): ____ (variance grounding: ____)
Duration window: ____
Human-in-the-loop: yes / no (justification: ____)
Seasonal exclusions: ____
Reversal: what makes me change this rule? ____
```

### Common failure modes

- `set_reference_data` not called — drift check returns "no reference".
- Threshold = "15% feels right" without variance grounding — 1/4 on D5.
- Duration window = "immediately" — model retrains on Black Friday → produces worse model.
- Agent-reasoning violation: "auto-retrain when X > Y". Must be reframed as "signal + threshold for operator" — the human owns retraining.
- Single rule for all three models — the cadences are different, the signals are different, the rule must be different.

### Artefact

`POST /drift/retrain_rule` × 3 + `journal/phase_13_retrain.md`.

### Instructor pause point

- Ask: if segment-reassignment rate was 8% last month and 14% this month, is that drift? What's the fourth data point that turns "two spikes" into "a trend"?
- Draw two cadences (segmentation monthly, recommender daily). What would a single combined alarm miss on each side?
- Show a Black-Friday-shaped data spike. Ask: retrain or hold? Why?

### Transfer to your next project

1. What is the signal my product leaks when it starts going wrong — and is there a measurable historical baseline for what "normal" looks like?
2. What duration distinguishes genuine drift from known seasonality or one-off spikes?
3. Who decides to retrain — human with signal as input, or automatic? If automatic, what's my safeguard against retraining on a Black-Friday-style event?

---

## Phase 14 — Fairness Audit (DEFERRED to Week 7)

```
──────────────────────────────────────────────────────────────────
 THIS PHASE:    Week 7 · Phase 14 of 14 — Fairness
 STATUS:        DEFERRED (see narrative below)
──────────────────────────────────────────────────────────────────
```

This phase is intentionally **not executed in Week 5** — and the deferral is an instructional choice, not a gap. Running a fairness audit well requires two literacies students haven't built yet: (a) naming the protected classes that actually apply in the jurisdiction (Singapore PDPA, EU GDPR Article 22, US ECOA, HIPAA — not just "protected groups"), and (b) disparate-impact testing with baselines and significance, which needs the credit + healthcare case material Weeks 6 and 7 are built on. A half-done fairness audit in Week 5 ("no segment is more than 60% one demographic, so we're fine") is worse than no audit — it produces a defensive document the student then references as if real, exactly the fairness-washing failure we want to prevent.

In the interim, the student does three things. First, during Phase 3 they run the proxy-check for every demographic-like feature and document proxy concerns explicitly. Second, during Phase 7 the Safety dimension flags "small-segment vulnerable-population overlap" as a finding with the explicit note "deferred to Week 7 per Playbook." Third, when the student commissions a similar product in the real world six months after the course, the presence of a deferred Phase 14 in their journal is the reminder to either run it properly (after Week 7 material) or commission a qualified fairness auditor; it is not permission to skip the step.

---

## Appendix — Transferable lessons accumulating through the term

_(Populated by Phase 9 Codify at the end of each week.)_

### Week 4 (supply chain / SML + optimization)

- AutoML trials above 10 blow the Sprint 1 budget and add no discovery value.
- "Monitor production" means nothing; "monitor [signal] weekly, alert at [threshold]" is the contract.
- Cost asymmetry in $ anchors every later phase; without it, floors float.

### Week 5 (retail / USML + SML + Opt + MLOps) — _to be populated tonight_

- (Student groups add 3 transferable lessons here during /codify.)

---

**END OF PLAYBOOK — v2026-04-23 · Universal Edition · Week 5 (Arcadia Retail) instantiation**
