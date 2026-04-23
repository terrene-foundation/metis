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

### Paste this

```
I'm entering Playbook Phase 1 — Frame. The scaffold pre-committed to the
product (retail intelligence suite) and the sprint structure (USML →
SML → Opt → MLOps); my decision here is the written frame for Sprint 1
segmentation — target, population, horizon, operational ceiling, and
the cost asymmetry in dollars that every later phase will anchor to.

Copy journal/skeletons/phase_1_frame.md into
workspaces/metis/week-05-retail/journal/phase_1_frame.md and fill in
the blanks as we go. Leave fields I have not decided yet as TODO — do
NOT propose values for me.

Draft the frame for me to edit. Produce these pieces, in order:

1. Target — one sentence naming WHAT is predicted/discovered, the unit
   (per customer, per session), and the window in days or months.
2. Population — inclusions AND explicit exclusions (staff accounts,
   bot accounts, test accounts, customers with <3 transactions).
3. Horizon — named in days or months, not "near-term".
4. Primary cost term AND secondary cost term. The two retail cost
   terms that anchor Sprint 1 are the wrong-segment campaign cost
   and the per-customer touch cost. Quote BOTH lines verbatim from
   PRODUCT_BRIEF.md §2 — the row and the exact dollar value. If you
   cannot find the line, say so; do NOT invent a number.
5. Operational ceiling — how many segments marketing can actually run
   in parallel, and WHO owns that ceiling (a role, not "the team").

Then answer one framing question in plain language: at a plausible
monthly mis-segmentation volume, what is the dollar exposure per
month if we ship the wrong K? Show the arithmetic using only numbers
from PRODUCT_BRIEF.md §2 — no invented counts.

Do NOT use the word "blocker" without naming the specific next step
I cannot take. Fuzzy scope is not a blocker; it's a to-do for me.

When the journal file has the five items drafted and the arithmetic
shown, stop and wait for me to review.
```

### Why this prompt is written this way

- Inheritance-framed opening names what the scaffold committed to (product + sprint order) and what remains my call (the written frame) — protects against agent drift into greenfield framing.
- Show-the-brief is mandatory on the two cost terms ($45 wrong-segment, $3 touch) because the cost anchor carries through every later phase — a Phase 1 without a quoted brief line is a 1/4 on rubric D1.
- Forbidding value proposals on target, K, and ceiling keeps the agent as a drafter, not a decider — the Trust Plane stays with me.
- The "dollar exposure per month" arithmetic is required BEFORE Phase 4 so the ceiling and cost asymmetry graduate from words to a number the CMO would recognize.
- No-fake-blockers guard is one line because Phase 1 has no real blockers — only fuzzy scope, which is a drafting task.

### What to expect back

- `journal/phase_1_frame.md` filled in for items 1–5 with blanks only where I still own the call.
- Two verbatim quoted lines from `PRODUCT_BRIEF.md §2` — one for wrong-segment ($45), one for per-customer touch ($3).
- A plain-language dollar-exposure arithmetic line (count × rate) using only brief-sourced numbers.
- A one-sentence named operational ceiling with a role attached (e.g. "CMO owns the campaign-count ceiling").
- A stop signal pending my review.

### Push back if you see

- A dollar figure with no quoted brief line — "which row of `PRODUCT_BRIEF.md §2` is this from? paste the row."
- A target like "discover patterns" or "understand customers" — "please rewrite in the form 'behavioural segment per active customer over an N-month window'."
- An operational ceiling without a role owner — "who owns the ceiling? the CMO, the CX Lead, the agency? name the role."
- A horizon phrased as "near-term" or "recent" — "please express horizon in days or months."
- A proposed K anywhere in the frame — "please remove the K; that's Phase 6's decision, not Phase 1's."

### Adapt for your next domain

- Change `wrong-segment campaign cost ($45)` to your domain's primary cost term.
- Change `per-customer touch cost ($3)` to the secondary / operational cost.
- Change `marketing ceiling on parallel campaigns` to the ceiling your ops team owns.
- Change `active customers in last 90 days` to your scope — inclusions and exclusions.
- Change `PRODUCT_BRIEF.md §2` to the brief section that holds your cost table.

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

### Paste this

```
I'm entering Playbook Phase 2 — Data Audit. The scaffold pre-committed
to the dataset shape (5,000 customers × 14 features, 400 SKUs, 120,000
transactions under src/retail/data/arcadia_*.csv); my decision here is
the disposition per audit finding — cap, log-transform, exclude, flag,
or leave. I am not validating the data; I am deciding what to do with
what you find.

Copy journal/skeletons/phase_2_data_audit.md into
workspaces/metis/week-05-retail/journal/phase_2_data_audit.md. Fill
the blanks as we go; leave dispositions as TODO — those are my calls.

Run the six-category audit against the three CSVs under
src/retail/data/. For every finding in every category:

1. Duplicates — exact customer_id or transaction_id repeats. Report
   count + the customer_id / transaction_id of the first 3 offenders.
2. Contamination — staff, bot, test, or integration accounts. Cite
   the column and rule that flags them (e.g. "rows where email
   domain ends in @arcadia-internal.sg"). If the column doesn't
   exist, say so.
3. Sparsity — customers with fewer than 3 transactions. Report the
   count and the fraction.
4. Outliers — top-1% on any numeric feature (especially
   total_spend, visits_per_week). Report the threshold and count.
5. Labels-in-disguise — any column that is itself a pre-existing
   segment assignment, tier, or rule output (e.g. a legacy
   loyalty_tier column). Report column name + unique-value count.
6. Missingness — per-column NaN rate; flag any column >5% missing.

For every claim in the audit, cite the exact file and the specific
column or function you used — e.g. "from arcadia_customers.csv
column 'total_spend_sgd', or from customer_features() in
src/retail/backend/ml_context.py". If you cannot cite a file and a
column, delete the claim.

For every dollar figure you mention (if any), quote the line from
PRODUCT_BRIEF.md §2. The audit itself is not priced in dollars, but
the $45 wrong-segment and $3 touch costs come up if you describe the
business impact of skipping the audit.

Propose a disposition per finding — cap, log-transform, exclude,
flag, or leave — with a one-line reason each. I approve or overrule
per finding. Do NOT apply any disposition yet.

Do NOT use the word "blocker" unless you name the specific next phase
I cannot run. A 7% NaN rate on one column is a finding, not a blocker.

When the audit table is complete with cited findings and proposed
dispositions, stop and wait for me to approve per finding.
```

### Why this prompt is written this way

- Inheritance-framed opening names what the scaffold decided (dataset shape, CSV paths) and what's still mine (the disposition per finding) — this prevents the agent from proposing dispositions as facts.
- Cite-or-cut is tightened to "file + column or function" because data audit claims without a column citation are the #1 source of invented findings in Week 4.
- Six categories enumerated, each with a concrete what-to-report shape — prevents vague "everything looks fine" summaries that score 0 on rubric D3.
- Label-in-disguise gets its own numbered slot because in USML it's the difference between discovering structure and re-deriving the 2020 rulebook.
- "Do NOT apply any disposition yet" is load-bearing — the agent applying a log-transform before I approve corrupts the Phase 4 candidate sweep.

### What to expect back

- `journal/phase_2_data_audit.md` with findings filled in for all six categories and disposition blanks held as TODO.
- Per-category findings with counts and first-offender IDs, each cited to `src/retail/data/arcadia_*.csv` or a function in `src/retail/backend/ml_context.py`.
- A proposed disposition (cap / log / exclude / flag / leave) with a one-line reason per finding.
- A list of columns that look like pre-existing segment labels, if any exist.
- A stop signal pending per-finding approval.

### Push back if you see

- A finding without a column or function citation — "which file and which column produced this? please cite or delete."
- "The data looks fine" / "no major issues" without per-category evidence — "please walk through all six categories; each needs a count even if the count is 0."
- A disposition applied before my approval (e.g. "I log-transformed total_spend") — "please revert; dispositions are my call, not yours."
- A contamination rule without the column it runs on — "which column flags staff accounts? if no such column exists, say so."
- A dollar figure not quoted from `PRODUCT_BRIEF.md §2` — "please quote the §2 row."

### Adapt for your next domain

- Change `staff, bot, test, integration accounts` to the contamination pattern in your domain (QA testers, partner API calls, demo users).
- Change `legacy loyalty_tier column` to your domain's pre-existing rule output (risk tier, triage tier, severity band).
- Change `customers with <3 transactions` to your sparsity floor (sessions, encounters, orders).
- Change `top-1% on total_spend` to your domain's dominant-outlier signal.
- Change `arcadia_customers.csv` to your source dataset paths.

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

### Paste this

```
I'm entering Playbook Phase 3 — Feature Framing. The scaffold
pre-committed to the raw feature set loaded in
src/retail/backend/ml_context.py (customer-level behavioural and
demographic columns); my decision here is which features go into
Sprint 1 clustering and which stay out — especially the ones that
look behavioural but are really proxies for protected class.

Copy journal/skeletons/phase_3_features.md into
workspaces/metis/week-05-retail/journal/phase_3_features.md.

For each candidate feature, classify on four axes:

1. Available at prediction time? (yes / no — if no, leakage risk)
2. Leaky from the label or from future data? (a transaction_date
   >= decision_date is future-data leakage)
3. Ethically loaded or regulatorily sensitive? Name the regime —
   PDPA §13 for under-18 personalised-history (Singapore), GDPR
   Art. 9 for sensitive categories (EU), HIPAA for health. If the
   feature is age-band-derived, postal-district-derived, or
   category-purchase-derived (implying health or belief), flag it.
4. Raw or engineered? If engineered, one-line derivation.

For every feature you classify, cite the source — either the column
in src/retail/data/arcadia_customers.csv OR the function in
src/retail/backend/ml_context.py that derives it. If you cannot cite,
delete the claim.

Then run the proxy-drop test on the two strongest demographic
candidates (postal_district AND age_band):

A. Fit the clustering with the demographic feature IN.
B. Fit the clustering with the demographic feature OUT.
C. Report the reassignment rate — what fraction of customers
   changed segment between A and B.

Cite the exact function and endpoint you used (likely /segment/fit
per src/retail/backend/routes/segment.py). Report the reassignment
percentage — do NOT compare it to a threshold. My call.

Any dollar figure mentioned (e.g. $220 per under-18 PDPA record from
PRODUCT_BRIEF.md §2) must be quoted verbatim — do NOT invent.

Recommend IN / OUT per feature with a one-line reason. I decide.
Do NOT apply the feature set yet.

Do NOT use "blocker" without naming the specific phase blocked.

When classification, proxy-drop test, and recommendations are in the
journal, stop and wait for my per-feature approval.
```

### Why this prompt is written this way

- Inheritance-framed opening names the scaffold's raw-feature commitment and keeps the in/out decision with me — the agent drafts, doesn't decide.
- Cite-or-cut is required per feature to prevent invented columns — common Week 4 failure where the agent claims `weekend_browse_fraction` exists when it's actually `weekend_sessions` in the source.
- PDPA/GDPR/HIPAA are named explicitly because "ethically loaded" without a regime name scores 1/4 on rubric D4.
- The proxy-drop test is mechanical (A/B/report) to prevent the agent from "interpreting" the result — interpretation is my job, not theirs.
- Show-the-brief on the $220 PDPA figure is mandatory because the feature-out decision has teeth only when the dollar exposure is on the page.

### What to expect back

- `journal/phase_3_features.md` with every candidate feature on the four-axis table.
- The proxy-drop reassignment percentage for `postal_district` and for `age_band`, with the endpoint / function cited.
- A recommended IN / OUT per feature with reason, no thresholds applied.
- A named regime (PDPA §13, GDPR Art. 9, HIPAA, ECOA) for every feature flagged ethically loaded.
- A stop signal pending my per-feature approval.

### Push back if you see

- "Ethically loaded: unclear" or "possibly sensitive" with no named regime — "which regime? PDPA §13, GDPR Art. 9, HIPAA, or ECOA? if none applies, say so."
- A proxy-drop test reported as "passed" or "failed" — "please remove the pass/fail; report the reassignment percentage only. threshold is mine."
- An engineered feature with no one-line derivation — "what's the formula? cite the function or column combination."
- A feature list with no source citation — "which column in `arcadia_customers.csv` or which function in `ml_context.py` produces this?"
- A $220 figure not quoted from `PRODUCT_BRIEF.md §2` — "please paste the §2 row for the under-18 PDPA cost."

### Adapt for your next domain

- Change `postal_district and age_band` to your domain's strongest demographic proxies (zip code, birth year, country of origin).
- Change `PDPA §13 for under-18 personalised-history` to your jurisdiction's minor-protection regime.
- Change `arcadia_customers.csv` to your candidate-feature source.
- Change `category-purchase-derived (health / belief)` to the inferred-sensitive pattern in your data.
- Change the proxy-drop target (clustering) to your downstream model (classifier, recommender).

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

### Paste this

```
I'm entering Playbook Phase 4 — Candidates. The scaffold pre-committed
to the family mix I will sweep — for Sprint 1 USML the clustering
families behind /segment/fit, for Sprint 2 SML the three-family
leaderboard behind /predict/leaderboard/{churn,conversion}. My
decision here is nothing yet; the pick happens in Phase 5. My job is
to commission a comparable sweep and read the numbers.

First, tell me which sprint I'm in:
- Sprint 1 USML → use /segment/fit and /segment/candidates. Write
  to journal/phase_4_usml.md (skeleton in journal/skeletons/).
- Sprint 2 SML → use /predict/leaderboard/churn AND
  /predict/leaderboard/conversion. Write to
  journal/phase_4_sml.md (skeleton in journal/skeletons/).

If Sprint 1: do NOT use AutoMLEngine for clustering. kailash-ml 0.17.0
raises ValueError on task_type='clustering'. Use /segment/fit
directly per src/retail/backend/routes/segment.py. Spending ten
minutes on an AutoML detour is a known trap and costs us the clock.

For whichever sprint I'm in, run the sweep with:

1. Three families spanning different assumptions.
   - USML: K-Means at K=3, 5, 7; DBSCAN at two density settings;
     one spectral approach at K=5.
   - SML: logistic regression, random forest, gradient-boosted
     (the ensemble).
2. Identical features across all candidates (no silent feature
   drift between rows of the leaderboard).
3. Identical stability protocol across all candidates — same
   seeds, same held-out set, same resample count.
4. Include a NAIVE BASELINE — for USML that's the pre-baked K=3
   reference at src/retail/data/segment_baseline.json; for SML
   that's majority-class prediction. Without the baseline the
   leaderboard winner is not defensible.

For every algorithm or method you name (K-means, DBSCAN, GBM,
logistic regression, isotonic calibration), cite the specific file
and function you read it from — e.g. "K-means, per
train_baseline_segmentation in src/retail/backend/ml_context.py". If
you cannot cite, say "I did not read the source for this — marking
the claim uncertain until I check."

Produce a leaderboard table. For USML: silhouette, bootstrap Jaccard
stability, segment-size distribution. For SML: AUC, PR-AUC, Brier
score, precision + recall at a default threshold, top-5 feature
importance. Same columns for every row, including the baseline.

Do NOT pick a winner. Do NOT propose K or threshold. Phase 5 picks;
Phase 6 sets thresholds / floors. Your job is a comparable
leaderboard, not a decision.

Do NOT use "blocker" without naming the blocked next step. A DBSCAN
density that returns 0 clusters is a finding, not a blocker.

When the leaderboard is in the journal with every row cited, stop
and wait for me to run Phase 5.
```

### Why this prompt is written this way

- Inheritance-framed opening distinguishes what the scaffold pre-committed (family mix, endpoint) from what's still open (which family wins — Phase 5) — prevents agent from skipping straight to a recommendation.
- One prompt serves both USML (Sprint 1) and SML (Sprint 2) because the shape is identical — family-diverse sweep + shared protocol + baseline + comparable numbers — and the sprint branch is handled by an explicit choice at the top.
- The AutoML prohibition is called out explicitly with the `ValueError` symptom because this is a documented 10-minute trap.
- Cite-or-cut on every algorithm name prevents the agent from inventing "collaborative filtering" or "NMF" when the code actually does K-means — a documented Week 5 hallucination pattern.
- Forbidding picks at Phase 4 protects the Phase 5 (implications) / Phase 6 (floors) decision structure; a Phase 4 winner becomes post-hoc floor pressure.

### What to expect back

- `journal/phase_4_usml.md` or `journal/phase_4_sml.md` depending on sprint.
- A leaderboard table with identical columns across rows, including the naive baseline (K=3 or majority class).
- Every family name cited to a function in `src/retail/backend/`.
- Numeric observations but NO winner proposed and NO K / threshold named.
- A stop signal pending Phase 5.

### Push back if you see

- `AutoMLEngine` named in a Sprint 1 USML context — "please use `/segment/fit` directly; `AutoMLEngine` doesn't support clustering in kailash-ml 0.17.0."
- A leaderboard without a baseline row — "where is the baseline row? I need the naive baseline (K=3 reference or majority class) on the same table."
- A winner proposed at Phase 4 ("recommend K=5" or "GBM wins") — "Phase 4 has no decision; please remove the pick. Phase 5 is where I choose."
- An algorithm name with no function citation — "which file and function in `src/retail/backend/` produces this?"
- Different feature counts across leaderboard rows — "these candidates aren't on the same features; please re-run with identical features across every row."

### Adapt for your next domain

- Change `K=3, 5, 7` to your K range.
- Change `DBSCAN, spectral` to your domain's alternative clustering families.
- Change `/segment/fit` and `/predict/leaderboard/` to your domain's sweep endpoints.
- Change `segment_baseline.json` to your pre-built naive baseline location.
- Change `majority-class prediction` to your SML naive baseline (mean prediction for regression, last-value for forecasting).

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

### Paste this

```
I'm entering Playbook Phase 5 — Implications. The scaffold
pre-committed to the leaderboard I'm about to read (produced in
Phase 4); my decision here is the pick — which candidate I stake my
name on, named in one paragraph of business language each, with every
rejected alternative given a reason.

Copy the Phase 5 skeleton from journal/skeletons/phase_5_implications.md
into workspaces/metis/week-05-retail/journal/phase_5_implications.md
(Sprint 1 USML). If this is the Sprint 2 SML replay, use
journal/phase_5_sml.md.

Read the Phase 4 leaderboard I just produced. Then:

1. For each candidate on the leaderboard (including the baseline),
   state: how well-separated (USML) or how accurate (SML), how
   stable across seeds / folds, how complex to train, how
   interpretable. One row per candidate, same columns.

2. For the top 2 USML candidates, profile EACH cluster in one
   paragraph of plain business language — no column names, no
   numbers. "Customers who shop on weekends and ignore promos" is
   a profile; "segment with high weekend_browse_fraction and
   low_promo_resp" is a statistical artefact.

   For SML, profile each model family the same way: which
   behaviours does this family predict well? which does it miss?
   What would the CX Lead hear if they asked "why did it pick
   this customer for retention?"

3. Recommend ONE candidate. For USML: weight stability over
   separation — 0.62 silhouette with 88% stability beats 0.71
   silhouette with 62% stability, because the second reshuffles
   every month and the CMO cannot campaign on a moving target.
   For SML: weight interpretability-over-AUC within 1 AUC point
   — the CX Lead will not ship a model she cannot explain to the
   retention team.

4. For every alternative you reject, give a one-sentence reason. A
   rejected alternative with no reason is "Claude Code said so",
   which does not ship.

Do NOT propose floors, thresholds, or K values. The pick is mine —
you write the recommendation and the rationale; I sign or overrule
in my journal. The floors go in Phase 6 and are pre-registered
BEFORE we revisit the leaderboard there.

Do NOT use "blocker" without naming the specific phase blocked. A
leaderboard where two candidates are within 1 point is a decision I
need to make, not a blocker.

When the recommendation and one-paragraph profiles are in the
journal, stop and wait for my pick.
```

### Why this prompt is written this way

- Inheritance-framed opening distinguishes the leaderboard (scaffold-produced via Phase 4) from the pick (my call at Phase 5) — prevents the agent from merging Phase 4 observation and Phase 5 decision.
- Plain-language cluster profiles are load-bearing because Phase 5 failure mode #3 is "cluster names read like column dumps" — CMO cannot act on `high_weekend_browse_fraction`.
- Stability-over-separation (USML) and interpretability-over-AUC (SML) are stated explicitly because the agent will default to the leaderboard top row unless told not to.
- "Rejected alternative with no reason is 'Claude Code said so'" is the anti-outsourcing clause — protects my Trust Plane call.
- Forbidding floors here preserves the Phase 6 pre-registration — any floor named in Phase 5 becomes post-hoc in Phase 6.

### What to expect back

- `journal/phase_5_implications.md` (or `_sml.md`) with a leaderboard-shape table plus a recommendation.
- One-paragraph plain-language profile per cluster (USML) or per model family (SML).
- A rejection reason for every non-recommended alternative.
- An explicit stability-or-interpretability framing for the recommendation.
- A stop signal pending my pick.

### Push back if you see

- Cluster profile that includes column names or numeric feature values — "please rewrite in plain language; no column names, no numbers. would a CMO recognize this segment on the street?"
- Recommendation based only on the top-of-leaderboard metric — "did you weigh stability (USML) or interpretability (SML)? top-of-leaderboard isn't automatic."
- Rejected alternative with no reason — "why was this rejected? one sentence, please."
- A proposed floor or threshold — "please remove; Phase 6 pre-registration is corrupted if I see a floor proposed here."
- "Recommend K=5" without the segment profiles — "profile every segment first; actionability comes before counting."

### Adapt for your next domain

- Change `weekend_browse_fraction / promo_resp` cluster-language examples to your domain's behavioural vocabulary.
- Change `CMO / CX Lead / retention team` stakeholders to the ones on your approval chain.
- Change `stability-over-separation` weighting for USML to your domain's trump dimension.
- Change `interpretability-over-AUC within 1 point` to your SML trade-off band.
- Change `Sprint 1 / Sprint 2` framing to your lifecycle naming.

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

### Paste this

```
I'm entering Playbook Phase 6 — Metric + Threshold. The scaffold
pre-committed to the shape of the commitment (three-floor
pre-registration for USML, PR-curve + calibration for SML); my
decision here is the FLOORS and the THRESHOLD — and I am
pre-registering them in writing BEFORE we re-open the leaderboard.

Which sprint am I in?
- Sprint 1 USML → I pre-register THREE floors (separation,
  stability, actionability). Skeleton:
  journal/skeletons/phase_6_metric_threshold.md → write
  journal/phase_6_usml.md.
- Sprint 2 SML → I pre-register a THRESHOLD-SELECTION RULE on the
  PR curve AND a Brier-score calibration floor. Write
  journal/phase_6_sml.md (same skeleton).

Here is how I want you to help me pre-register — I am the one
writing the values. You:

1. First, CONFIRM that you have not yet reopened the Phase 4
   leaderboard. If you have already seen the winning K or the
   winning family in the last two messages, say so — we must
   record that the floors were set post-hoc and treat the rubric
   accordingly. Honesty first; do not conceal the order.

2. USML path — draft the three floor definitions (NOT values) in
   the journal:
   (a) Separation floor — silhouette (or equivalent) measured how?
   (b) Stability floor — bootstrap Jaccard over how many re-seeds?
   (c) Actionability floor — named as a TEST ("one distinct
       marketing action per segment, tested by writing the action
       in one sentence per segment"), not a number.

3. SML path — draft the threshold-selection RULE (NOT the
   threshold value):
   (a) Curve to read — PR (for rare-positive churn and conversion),
       not ROC. Name the endpoint that produces the curve (per
       src/retail/backend/routes/predict.py).
   (b) Cost asymmetry — quote the $3 per-customer touch cost from
       PRODUCT_BRIEF.md §2 verbatim; the $120 CAC is in
       PLAYBOOK.md Phase 6 SML (not in the brief) — cite the
       Playbook line, not §2.
   (c) Calibration floor — Brier score cutoff; if breached, run
       isotonic calibration BEFORE threshold selection.

4. Compute the counterfactual dollar lift framework — NOT the
   number, the formula. "If K=N moves X customers off the
   $45/wrong-segment path, the monthly lift is $45 × X." I plug
   X when I see the leaderboard.

5. Timestamp the pre-registration — record the wall-clock time in
   the journal header. This is the only evidence that the floors
   preceded the results.

Do NOT propose floor values (0.25 silhouette, 0.80 Jaccard, 0.3
threshold). I write those values myself in the journal, at a
timestamp that precedes my next leaderboard read. If you propose a
value I use, my pre-registration is corrupted.

Any dollar figure you mention must be quoted from PRODUCT_BRIEF.md §2
(or PLAYBOOK.md Phase 6 SML for the $120 CAC). Do NOT invent.

Do NOT use "blocker" without a specific blocked action. An
un-set floor is not a blocker; it is the phase I am currently running.

When the journal has floor DEFINITIONS (USML) or the threshold-rule
FRAME (SML), a timestamp, and the lift-formula skeleton, stop and
wait for me to write the values.
```

### Why this prompt is written this way

- Inheritance-framed opening separates the SHAPE of commitment (three floors / PR+calibration, pre-committed by the scaffold and rubric) from the VALUES (mine to write) — this is the anti-post-hoc architecture of the phase.
- The "confirm you have not seen the winner" honesty clause is the pre-registration mechanic; without it, a silently-seen leaderboard leaks into the floor values.
- One paste serves both USML (3 floors) and SML (threshold rule + calibration) because Phase 6 is the single phase of the night where both tracks live — branching keeps students from running two different prompts and losing the pre-registration clock.
- Show-the-brief split — $3 from §2, $120 from `PLAYBOOK.md` Phase 6 SML — is called out because the rubric rewards correct citation and 0/4s a $120-from-§2 claim.
- Forbidding value proposals and requiring a timestamp is the D2 (metric→cost linkage) and D5 (reversal) guard together — floors without a timestamp score 0/4 on D2.

### What to expect back

- `journal/phase_6_usml.md` with separation / stability / actionability floor DEFINITIONS and a timestamp (USML), OR `journal/phase_6_sml.md` with the PR-curve + calibration rule and a timestamp (SML).
- An honest note of whether the leaderboard has been seen yet (ideally: "not yet").
- A lift-formula skeleton with brief-sourced unit costs and placeholder customer counts.
- Correct citation split: $3 → brief §2, $120 → `PLAYBOOK.md` Phase 6 SML.
- A stop signal pending my value-writing.

### Push back if you see

- A proposed floor value ("silhouette ≥ 0.25", "threshold 0.3") — "please remove the value; I write those myself. your job is the definition."
- No timestamp on the journal entry — "please add wall-clock time to the header so the order is auditable."
- $120 CAC cited to `PRODUCT_BRIEF.md §2` — "that's in `PLAYBOOK.md` Phase 6 SML, not the brief. please re-cite."
- ROC named as the SML threshold curve — "churn and conversion are rare-positive; please use PR, not ROC."
- Actionability floor expressed as a number (e.g. "0.6 on some actionability index") — "actionability is a test — 'one distinct action per segment', not a number."

### Adapt for your next domain

- Change `separation / stability / actionability` (USML) to your domain's three quality dimensions.
- Change `PR curve + Brier calibration` (SML) to the threshold-selection tool for your target (ROC if balanced; lift chart if ranking matters more than decisions).
- Change `$3 per touch / $120 CAC` cost asymmetry to your domain's FN / FP cost pair.
- Change `counterfactual vs 2020 rulebook` to counterfactual vs your incumbent baseline.
- Keep the timestamp + no-proposed-values mechanic as-is — it's domain-independent.

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

### Paste this

```
I'm entering Playbook Phase 7 — Red-team. The scaffold pre-committed
to the three red-team sweeps for USML (re-seed churn, proxy
leakage, operational collapse) and — in the SML replay — two for
SML (calibration-per-subgroup, feature-ablation). My decision here
is the disposition per finding (accept / mitigate / re-do); your
job is to run the sweeps and report numbers against my
pre-registered floors, not propose new ones.

Copy journal/skeletons/phase_7_red_team.md into
workspaces/metis/week-05-retail/journal/phase_7_red_team.md (Sprint
1) or journal/phase_7_sml.md (Sprint 2 replay).

USML sweeps (Sprint 1):

1. RE-SEED CHURN. Run /segment/fit 3 times with different random
   seeds, hold features and K constant. Report the per-segment
   Jaccard stability distribution — not the mean, the distribution.
   Cite the endpoint and function (src/retail/backend/routes/
   segment.py + the fit function in ml_context.py).

2. PROXY LEAKAGE. Drop postal_district, then drop age_band, then
   drop both. Re-cluster each time. Report the fraction of
   customers who changed segment vs the Phase 5 winning clustering.
   Cite the source columns in src/retail/data/arcadia_customers.csv.

3. OPERATIONAL COLLAPSE. Filter transactions to post-Black-Friday
   shapes (volume spike + mix shift, using src/retail/data/
   scenarios/catalog_drift.json if helpful). Re-cluster. Report
   the size of the smallest segment as a fraction of customers.

SML sweeps (Sprint 2 replay):

A. CALIBRATION-PER-SUBGROUP. Compute Brier score per customer
   segment for both churn and conversion classifiers. Cite the
   endpoint that returns calibration (per routes/predict.py).
   Report the subgroup with the worst calibration.

B. FEATURE-ABLATION. Drop the top-importance feature for each
   classifier, re-train, report the AUC drop. If the drop is >3
   points, that feature was doing more work than the rest
   combined.

For every claim — algorithm name, metric, endpoint, column — cite
the file and function. If you cannot cite, say so explicitly and
mark the finding uncertain.

For every dollar figure, quote the PRODUCT_BRIEF.md §2 line. The
relevant §2 costs for red-team ranking are $45 wrong-segment, $14
wasted impression, $220 under-18 PDPA, $8 cold-start.

CRITICAL: do NOT propose new thresholds or floors. The floors were
pre-registered in Phase 6; this phase MEASURES against them. If
re-seed Jaccard comes back at 0.74 and my Phase 6 floor was 0.80,
the finding is "below my pre-registered floor — Phase 8 gate
failure candidate", not "let me propose 0.70 as the new floor".

Rank findings by severity in dollars using §2 quotes. Tag each
finding as ACCEPT (accepted risk), MITIGATE (action before ship),
or RE-DO (a phase must re-run). My call on dispositions; your
recommendation in writing first.

Do NOT use "blocker" without naming the specific ship-action
blocked. "Segmentation unstable" is not a blocker; "cannot ship
the allocator because its input reshuffles every week" is.

When all five sweeps are in the journal with cited numbers, §2
quotes, and disposition recommendations, stop and wait for my
call per finding.
```

### Why this prompt is written this way

- Inheritance-framed opening names which sweeps are pre-committed (five, split 3+2 across USML and SML) and keeps the disposition call with me — the Trust Plane stays clean.
- Cite-or-cut is enforced because red-team findings without citations become un-auditable "the model failed" claims that score 1/4 on D3.
- "Do NOT propose new thresholds" is the load-bearing anti-cheat — without it the agent lowers floors post-hoc to pass the red team, destroying Phase 6's pre-registration value.
- ACCEPT / MITIGATE / RE-DO triage is explicit so the disposition vocabulary matches what `/redteam` expects at the COC-level close.
- One paste covers both USML (Sprint 1) and SML (Sprint 2 replay) because the disposition discipline is identical and separating them doubles the paste load.

### What to expect back

- `journal/phase_7_red_team.md` (Sprint 1) or `journal/phase_7_sml.md` (Sprint 2) with five cited findings.
- Per-segment Jaccard distribution (not just mean) from the re-seed sweep.
- Proxy-drop reassignment percentages for postal_district, age_band, and both combined.
- Brier-score-per-subgroup for churn and conversion classifiers.
- A ranked finding list with §2-quoted dollar severity and ACCEPT/MITIGATE/RE-DO tags.
- A stop signal pending my disposition call.

### Push back if you see

- A new threshold proposed ("I suggest lowering the stability floor to 0.70") — "my Phase 6 floor was X; this is a failure against that floor, not a floor adjustment."
- A finding without a file-and-function citation — "which file and function produced this?"
- A dollar severity without a §2 quote — "please quote the §2 row for this cost."
- Mean Jaccard only, without the distribution — "please report the distribution across seeds, not the mean."
- "Blocker: the model is unstable" — "which ship-action is blocked?"

### Adapt for your next domain

- Change `re-seed / proxy / operational collapse` USML sweeps to your domain's unsupervised stress tests.
- Change `calibration-per-subgroup / feature-ablation` SML sweeps to your domain's classifier stress tests.
- Change `postal_district, age_band` to your domain's protected-proxy candidates.
- Change `post-Black-Friday filter` to your domain's known regime-shift scenario.
- Change the `$45 / $14 / $220 / $8` §2 costs to your own cost table's equivalents.

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

### Paste this

```
I'm entering Playbook Phase 8 — Deployment Gate. The scaffold
pre-committed to the registry state machine (staging → shadow →
production) and the /segment/promote endpoint; my decision here is
ship-or-no-ship against my Phase 6 pre-registered floors, plus the
day-one monitoring plan and the rollback trigger. I am not
proposing new criteria; I am checking my pre-registered ones.

Copy journal/skeletons/phase_8_gate.md into
workspaces/metis/week-05-retail/journal/phase_8_gate.md (Sprint 1
USML) or journal/phase_8_sml.md (Sprint 2 SML).

Your job:

1. Read my Phase 6 floors from phase_6_usml.md (or phase_6_sml.md)
   — the three USML floors OR the SML threshold rule + Brier
   calibration floor. Quote the values I wrote, verbatim. Do NOT
   propose or "suggest" values.

2. Read my Phase 7 red-team findings from phase_7_red_team.md (or
   phase_7_sml.md). For every MITIGATE or RE-DO finding, flag it —
   I cannot ship through an unmitigated red-team finding.

3. Measure the current artefact (K=N chosen / classifier family
   chosen) against each floor. Report PASS or FAIL per floor. No
   threshold adjustments. If a floor fails, the gate is NO-GO
   unless I explicitly override in writing.

4. Draft the day-one monitoring plan. For each signal, name:
   (a) the signal,
   (b) the cadence (weekly / monthly / daily),
   (c) the alert threshold — GROUNDED IN VARIANCE, not a round
       number. "15% because the rolling variance's 95th percentile
       is 12%" is D5 = 4/4; "15% because it feels big" is D5 =
       1/4. Compute the variance from the observed Phase 7 sweep
       numbers I just produced, or from the scaffold's drift
       reference at src/retail/data/drift_baseline.json.
   (d) the owner (role — E-com Ops Lead for segmentation, CX Lead
       for classifier).

5. Draft the rollback trigger — one specific signal + threshold
   + duration window. "Any segment drops below 2% of customers in
   one month" is specific; "if things go wrong" is 0/4 on D5.

6. Draft the rollback TARGET — the artefact we fall back to. For
   Sprint 1 USML, the known-working rollback is the 2020
   rule-based 5-segment system (not a previous clustering). For
   Sprint 2 SML, the rollback is the previous threshold or the
   rule-based flag logic — whichever is known to work.

7. Do NOT execute /segment/promote yet. I sign the GO/NO-GO based
   on the PASS/FAIL table, then call /segment/promote myself (or
   authorize you to).

For every technical claim — endpoint, file, function — cite.
For every dollar figure (rare here), quote the §2 line.

Do NOT use "blocker" without naming the specific ship-action.

When the PASS/FAIL table, monitoring plan with variance-grounded
thresholds, rollback trigger, and rollback target are in the
journal, stop and wait for my GO/NO-GO call.
```

### Why this prompt is written this way

- Inheritance-framed opening names the scaffold's registry commitment and keeps the GO/NO-GO with me — the agent does not "pass" the gate on my behalf.
- Reading my Phase 6 values verbatim rather than re-proposing them is the structural defence of pre-registration — floors written in Phase 6 are the floors checked in Phase 8, unchanged.
- Variance-grounded monitoring thresholds are explicitly required with a 4/4-vs-1/4 scoring example, because the #1 D5 failure is "15% because it feels big".
- Forbidding `/segment/promote` until my GO is the structural anti-auto-ship — the agent does not decide to push staging → shadow.
- Rollback TARGET being the 2020 rulebook (USML) or previous threshold (SML) is named explicitly so the agent doesn't invent a "previous model version" that doesn't exist.

### What to expect back

- `journal/phase_8_gate.md` (or `_sml.md`) with a PASS/FAIL table of the Phase 6 floors.
- A day-one monitoring plan with signal / cadence / variance-grounded threshold / owner per line.
- A one-line rollback trigger (specific signal + threshold + duration).
- A named rollback target known to work today (2020 rulebook for USML; previous threshold for SML).
- A stop signal pending my GO/NO-GO — no `/segment/promote` call yet.

### Push back if you see

- A monitoring threshold without variance grounding — "what's the 95th percentile of historical variance? ground the number or remove it."
- A rollback target that's "a previous version of the model" without proof it exists — "is there actually a previous promoted model in the registry, or is this hypothetical?"
- Floors re-proposed ("recommend lowering stability to 0.75") — "my Phase 6 floor was 0.80; the gate checks against that, not a new value."
- `/segment/promote` called before I said GO — "please revert the promotion; GO is my call."
- Monitoring prose without a signal/cadence/threshold/owner — "please rewrite as a table with those four columns."

### Adapt for your next domain

- Change `/segment/promote` to your registry's promotion endpoint.
- Change `staging → shadow → production` to your registry's state machine.
- Change `drift_baseline.json` to your variance reference file.
- Change `2020 rulebook` (USML rollback) to your domain's incumbent / no-ML fallback.
- Change `E-com Ops Lead / CX Lead` to your monitoring owners.

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

### Paste this

> The `/codify` COC workflow phase shares this Playbook Phase 9. **Paste the `/codify` prompt from `START_HERE.md` §6.8** — that prompt drives Phase 9 at both the COC-workflow-entry and Playbook-phase-detail levels, so there is nothing additional to paste here. Return to §6.8 when you reach Close.

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

### Paste this

> The paste-ready prompt for Phase 4 **covers both USML (Sprint 1) and SML (Sprint 2)** via an explicit sprint branch at the top. See **§Phase 4 — Candidates** above. This SML-replay section retains its teaching content (SML lens, family families, evaluation) as reference; the prompt itself is the same one you pasted when you entered Sprint 2 /implement.

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

### Paste this

> The paste-ready prompt for Phase 6 **covers both USML (Sprint 1 three-floor pre-registration) and SML (Sprint 2 PR-curve + Brier calibration)** via an explicit sprint branch at the top. See **§Phase 6 — Metric + Threshold** above. This SML-replay section retains its teaching content (PR vs ROC, cost-based threshold selection, calibration) as reference; the prompt itself is the same one you pasted when you reached Phase 6 in Sprint 2.

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

### Paste this

```
I'm entering Playbook Phase 10 — Objective Function. The scaffold
pre-committed to the LP allocator shape and the endpoints
(/allocate/objective GET + POST, /allocate/campaigns,
/allocate/solve per src/retail/backend/routes/allocate.py); my
decision here is the OBJECTIVE WEIGHTS — single vs multi-objective,
and the specific weight per term — defended in dollars.

Copy journal/skeletons/phase_10_objective.md into
workspaces/metis/week-05-retail/journal/phase_10_objective.md.

Your job:

1. Name the 3–5 competing signals the objective needs to reason
   across. For Arcadia's allocator these are: expected revenue,
   reach (customers touched), diversity (cross-segment coverage),
   touch spend. If you add a fifth (fairness, serendipity), name
   it as a PROXY for long-term revenue, not a direct term.

2. For each term, quote the dollar rate VERBATIM from
   PRODUCT_BRIEF.md §2:
   - Expected revenue per converted click — $18 (row: basket lift)
   - Wasted impression — $14 per session
   - Per-customer touch cost — $3 per contact
   - Cold-start session fallback — $8 per new-user session
   If you cannot find a row, say so; do NOT invent rates.

3. Draft BOTH framings side by side:
   (a) Single-objective: expected revenue maximisation, with
       diversity / reach as constraint floors (those go in Phase
       11). Formula:
       max Σ x × (P(convert) × $18 − $14 × wasted − $3 × touches)
   (b) Multi-objective: separate scores on revenue, reach,
       diversity, each scaled. Pareto frontier sketch.

4. Compute the SHADOW PRICE for the two most important constraints
   (touch budget and the PDPA under-18 exclusion). Shadow price =
   "how much extra revenue per unit of constraint relaxation". Run
   /allocate/solve once and read the solver output. Cite the
   solver function in src/retail/backend/routes/allocate.py.

5. Recommend ONE framing with defensible weights — but do NOT
   set the weight values. Your job is the shape and the rationale
   ("single-objective because stakeholders agree revenue is the
   headline"); my job is the weight numbers I paste into
   /allocate/objective.

6. Name what each framing SACRIFICES. Single-objective sacrifices
   explicit reach / diversity visibility; multi-objective
   sacrifices a single go/no-go number. No free lunch — state it.

Do NOT call /allocate/objective to POST new weights yet. That is
my action. You run /allocate/solve with the current / default
weights to expose the shadow prices, then stop.

Do NOT propose weight VALUES (0.7 revenue, 0.2 reach, 0.1 diversity).
Your job is the framing and the dollar rates; I pick the weights.

Do NOT use "blocker" without naming the specific ship-action.

When framings, shadow prices, and sacrifices are drafted with §2
quotes, stop and wait for my weight decision.
```

### Why this prompt is written this way

- Inheritance-framed opening names the scaffold's LP shape and endpoints and keeps the WEIGHTS with me — the objective is where the CMO's preferences live, so the agent drafts and I number.
- Show-the-brief is mandatory on the four rates because an invented $19 or $15 corrupts the objective and scores 0/4 on D1.
- Single- AND multi-objective framings both required because Phase 10 checklist says both must be presented — skipping multi is a 2/4 on D3 (hidden trade-off).
- Shadow price on touch budget and PDPA is required up front so the "cost of compliance" conversation starts before the injection, not after.
- Forbidding the POST to `/allocate/objective` is the structural guard against auto-picking weights — the agent cannot set the objective by side effect.

### What to expect back

- `journal/phase_10_objective.md` with the 3–5 signals named, each with a §2 quote.
- Both single- and multi-objective framings drafted side by side.
- Shadow prices for touch-budget and PDPA constraints, read from a real `/allocate/solve` run.
- A recommended framing with sacrifice stated, NO weight values.
- A stop signal pending my weight decision.

### Push back if you see

- A weight value proposed ("weight_revenue = 0.7") — "please remove; I own weights, you own framing."
- A dollar rate not quoted from §2 — "please quote the §2 row for this rate."
- Only one framing (single OR multi, not both) — "please draft both; I need to see what each sacrifices."
- Shadow price stated without running the solver — "please run `/allocate/solve` first; shadow prices come from the solver output."
- A POST to `/allocate/objective` already made — "please revert; I set the weights, not you."

### Adapt for your next domain

- Change `expected revenue / reach / diversity / touches` to your domain's objective terms.
- Change the four §2 dollar rates to your domain's cost table rows.
- Change `/allocate/objective`, `/allocate/solve` to your optimization endpoints.
- Change `touch budget + PDPA` shadow-price pair to your domain's binding-constraint pair.
- Keep the "draft both framings, sacrifice named" mechanic — it's domain-independent.

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

### Paste this

```
I'm entering Playbook Phase 11 — Constraint Classification. The
scaffold pre-committed to the constraint list (touch budget,
per-segment fatigue cap, PDPA under-18 browsing, inventory
availability, brand exclusion) exposed at /allocate/constraints
per src/retail/backend/routes/allocate.py; my decision here is
HARD vs SOFT per rule, plus the DOLLAR PENALTY on every soft
constraint. This is also where the PDPA mid-sprint injection
re-fires — I run Phase 11 twice, saving both passes.

First pass (pre-injection):

Copy journal/skeletons/phase_11_constraints.md into
workspaces/metis/week-05-retail/journal/phase_11_constraints.md.

For each constraint, classify:

1. Touch budget cap — hard (contract with marketing) or soft
   (over-spend at $X penalty)?
2. Per-segment fatigue cap — almost always soft; what's the
   dollar penalty per over-touch? Cite the per-customer touch
   cost ($3) from PRODUCT_BRIEF.md §2 verbatim as the floor
   on the penalty.
3. PDPA under-18 browsing — classify as SOFT or HARD (first
   pass; legal has not fired yet). Note the $220 per under-18
   record exposure from PRODUCT_BRIEF.md §2 verbatim.
4. Inventory availability — hard (physical): you cannot sell
   what you don't have.
5. Brand exclusion list — contract hard: you cannot push brand
   X to segment Y.

For every classification, name WHY — the regime (PDPA §13, MAS
circular, contract clause, physical limit) or the stakeholder
(CMO preference, Ops preference).

For every dollar figure, quote PRODUCT_BRIEF.md §2 verbatim. The
two §2 rows that drive Phase 11 are the $3 touch cost and the
$220 PDPA exposure. The $8 cold-start fallback is also a §2 row
and may appear as a penalty.

Do NOT propose penalty VALUES. Your job is the shape
("soft-with-penalty-per-unit-over-cap"); my job is the number.

Post-injection re-run (when instructor fires PDPA at ~4:30):

When I paste the injection payload (src/retail/data/scenarios/
pdpa_redline.json), copy the skeleton AGAIN into
journal/phase_11_postpdpa.md. Do not overwrite the first pass —
the rubric scores BOTH files.

In the re-run:
- Re-classify the PDPA under-18 rule as HARD (PDPA §13).
- Quote the $220 per under-18 record from PRODUCT_BRIEF.md §2
  verbatim as the compliance anchor.
- Save a before / after table showing what changed.
- Note that Phase 12 must now re-run — the LP in
  data/allocator_last_plan.json must be re-solved under the new
  hard constraint. Writing phase_11_postpdpa.md alone is a D3
  zero; Phase 12 re-solve is non-negotiable.

Do NOT POST /allocate/constraints until I approve per rule. The
classifications are my call; you draft, I sign.

Do NOT use "blocker" without naming the specific blocked
ship-action.

When first-pass classifications are drafted with §2 quotes and
cited regimes, stop and wait for me. When PDPA fires, repeat
into phase_11_postpdpa.md and stop again.
```

### Why this prompt is written this way

- Inheritance-framed opening names the scaffold's constraint list and endpoint, keeping the hard-vs-soft call with me — constraint classification is the #1 rubric-teeth moment of Sprint 3.
- Show-the-brief is mandatory on $3 and $220 because these are the two §2 rows where the rubric has 4/4 vs 1/4 scoring on D4.
- Mid-sprint injection is baked into the same paste so I don't lose the clock hunting for a second paste when the instructor fires — the postpdpa flow is a reentrant re-run, not a new prompt.
- "Writing `phase_11_postpdpa.md` alone is a D3 zero" is the load-bearing anti-trap sentence — it names the single most common Sprint 3 failure and attaches it to the rubric directly.
- Forbidding the `/allocate/constraints` POST before my approval prevents the agent from silently locking in a soft PDPA classification.

### What to expect back

- `journal/phase_11_constraints.md` with hard/soft per rule + regime cited + §2 dollar quotes.
- Later (post-injection): `journal/phase_11_postpdpa.md` with PDPA re-classified as HARD, plus a before / after table and a note that Phase 12 must re-run.
- Penalty SHAPES (not values) drafted for every soft constraint.
- A stop signal pending my per-rule approval — no `/allocate/constraints` POST yet.
- After the injection: an explicit cue that Phase 12 re-solve is next.

### Push back if you see

- A proposed penalty value ("$5 per over-touch") — "please remove; I set the value, you set the shape."
- $220 or $3 not quoted from `PRODUCT_BRIEF.md §2` — "please quote the §2 row."
- PDPA classified as SOFT in the post-injection pass — "PDPA §13 is a legal hard line; re-classify as HARD."
- Post-injection journal written but no note about Phase 12 re-solve — "the LP plan must re-run; please flag that Phase 12 is next."
- `/allocate/constraints` POSTed before my approval — "please revert; approval is my call per rule."

### Adapt for your next domain

- Change `touch budget / fatigue cap / PDPA / inventory / brand exclusion` to your domain's five constraints.
- Change `PDPA §13` to your jurisdiction's equivalent regulatory anchor.
- Change the `$220 / $3` §2 quotes to your domain's compliance + operational rates.
- Change `pdpa_redline.json` to your domain's mid-sprint injection payload.
- Change the regime hierarchy (contract / law / physics / preference) to match your constraint vocabulary.

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

### Paste this

```
I'm entering Playbook Phase 12 — Solver Acceptance. The scaffold
pre-committed to the LP solver behind /allocate/solve and the
last-plan persistence at data/allocator_last_plan.json per
src/retail/backend/routes/allocate.py; my decision here is
ACCEPT / RE-TUNE / FALL-BACK / REDESIGN on the solved plan,
checked for feasibility AND pathologies. I run this twice — once
with the first-pass constraints, once after the PDPA injection.

Copy journal/skeletons/phase_12_accept.md into
workspaces/metis/week-05-retail/journal/phase_12_accept.md.

Your job, first pass:

1. POST to /allocate/solve with the current Phase 10 objective
   and Phase 11 constraints. Save the response to
   data/allocator_last_plan.json (the endpoint does this
   automatically per allocate.py). Cite the solver function.

2. Report FEASIBILITY per hard constraint — which constraints are
   satisfied (e.g. "touch budget used: X of Y", "inventory: no
   SKU allocated beyond availability"). If any hard constraint
   is violated, the plan is infeasible and my disposition is
   REDESIGN or FALL-BACK.

3. Report the OPTIMALITY GAP — the distance from the LP optimum.
   If >5%, name it as a finding.

4. Check four PATHOLOGIES:
   (a) Concentration — is any segment getting >10% of the
       plan disproportionately? I set the threshold; you report
       the concentration percentage per segment.
   (b) Dead campaigns — any campaign with 0 allocation across
       all segments.
   (c) Boundary — any decision at 100% of a budget when I
       expected 80%.
   (d) Sensitivity — perturb weights by ±10% and re-solve.
       Does the top-concentration segment flip? Does a dead
       campaign come alive? Report the change in allocations.

5. Compute prior-plan comparison — if a prior /allocate/last_plan
   exists, what's the expected-revenue delta in dollars?
   Quote the $18 basket-lift and $14 wasted-impression rates
   from PRODUCT_BRIEF.md §2 verbatim for the calculation.

Do NOT propose pathology THRESHOLDS. The 10% concentration, the
5% optimality gap, the ±10% sensitivity band — I set those. Your
job is to report the measured values; I compare to my floors.
The point is pre-registered pathology floors, not post-hoc ones.

Do NOT decide ACCEPT / RE-TUNE / FALL-BACK / REDESIGN. That is my
call per pass. You recommend with rationale; I sign.

Post-injection re-run (when PDPA fires):

After phase_11_postpdpa.md is written, POST /allocate/solve AGAIN
with the new hard PDPA constraint. Save the new plan — the file
at data/allocator_last_plan.json MUST BE DIFFERENT from the
first-pass plan. If the file is byte-identical, the solver did
not pick up the new constraint and something is wrong.

Copy the skeleton into phase_12_postpdpa.md (do not overwrite
phase_12_accept.md). Report the same four pathologies. Compute
the SHADOW PRICE of the new hard PDPA constraint — "the dollar
revenue lost to compliance". Quote the $220 line from
PRODUCT_BRIEF.md §2 to anchor the shadow price in per-record
terms.

For every claim, cite the file and function. For every dollar
figure, quote §2. Do NOT invent.

Do NOT use "blocker" without the specific blocked ship-action.

When feasibility, gap, pathology report, and sensitivity are in
the journal, stop and wait for my disposition. When PDPA fires,
re-run and stop again.
```

### Why this prompt is written this way

- Inheritance-framed opening names the scaffold's solver and plan-persistence commitments and keeps the disposition with me — "feasible" is not the same as "shippable" and only I say so.
- Four pathologies are enumerated because Phase 12 checklist says all four must be checked; missing one is a 2/4 on D3.
- Forbidding pathology THRESHOLD proposals is the anti-post-hoc guard — the agent reporting "concentration 12% which is below the 15% threshold" post-hoc is exactly the failure Phase 6 pre-registration was supposed to prevent.
- The byte-identical-plan check is the disk-level proof that the PDPA re-solve actually fired — the #1 rubric trap of the night is writing `phase_12_postpdpa.md` while the solver never re-ran.
- Show-the-brief on $18 / $14 / $220 is required so expected-revenue delta and shadow-price claims are audit-traceable.

### What to expect back

- `journal/phase_12_accept.md` with feasibility per hard constraint + optimality gap + four-pathology report + ±10% sensitivity.
- Later: `journal/phase_12_postpdpa.md` after the injection, with a DIFFERENT `data/allocator_last_plan.json` and a quoted shadow price.
- Expected-revenue delta vs prior plan in dollars, sourced from §2 rates.
- A disposition RECOMMENDATION with rationale — not a decision.
- A stop signal pending my ACCEPT / RE-TUNE / FALL-BACK / REDESIGN call.

### Push back if you see

- A proposed pathology threshold ("concentration limit = 10%") — "please remove; I set pathology floors in my journal, not you."
- `phase_12_postpdpa.md` written but `data/allocator_last_plan.json` byte-identical to the first pass — "the solver didn't re-run; please re-POST `/allocate/solve` and confirm the plan file changed."
- A "feasible plan" claim without the four-pathology check — "did you check concentration, dead campaigns, boundary, and sensitivity? feasible alone is 1/4 on D3."
- Shadow price quoted without a $ unit — "shadow price of what, in dollars per what unit?"
- Disposition decided on my behalf ("I recommend accept, accepting the plan") — "please state disposition as a recommendation only; the sign is mine."

### Adapt for your next domain

- Change `/allocate/solve` and `data/allocator_last_plan.json` to your optimization endpoints and plan persistence.
- Change the four pathologies (concentration / dead / boundary / sensitivity) to your domain's pathology taxonomy.
- Change `$18 / $14 / $220` to your domain's §2-equivalent rates.
- Change `PDPA injection` to your domain's mid-sprint regulatory event.
- Keep the byte-identical-plan check as-is — it's domain-independent structural proof.

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

### Paste this

```
I'm entering Playbook Phase 13 — Drift. The scaffold pre-committed
to drift reference data registered at startup and the endpoints
/drift/status/{model_id}, /drift/check, /drift/retrain_rule per
src/retail/backend/routes/drift.py; my decision here is THREE
RETRAIN RULES — one per model, grounded in historical variance,
with human-in-the-loop disposition. Not one rule for three models;
three rules, three cadences.

Copy journal/skeletons/phase_13_retrain.md into
workspaces/metis/week-05-retail/journal/phase_13_retrain.md.

Your job:

1. Confirm the drift reference is registered for each of the
   three models:
   - Segmentation (customer_segmentation)
   - Churn classifier (churn)
   - Conversion classifier (conversion)
   Run GET /drift/status/customer_segmentation and confirm
   "reference_set": true. If not, STOP — do NOT attempt to
   re-seed; that is the scaffold's responsibility.

2. Run /drift/check against two windows — recent_30d AND
   catalog_drift (per src/retail/data/scenarios/
   catalog_drift.json). Report the OBSERVED VARIANCE per signal.
   I need the 50th, 95th, 99th percentile of the historical
   variance to ground my thresholds in.

3. Draft the SHAPE of three rules — one per model — each with:
   - Signal(s): segmentation = membership churn; churn
     classifier = calibration error + AUC decay + feature
     PSI; conversion classifier = same; allocator (if
     applicable) = constraint-violation rate.
   - Cadence: segmentation monthly; classifiers weekly;
     allocator daily.
   - Threshold grounding: "to be set by the student at the
     95th percentile of observed variance from step 2".
   - Duration window: 1 day is seasonality, 7 days is real,
     30 days is definitive. Segmentation needs 2 consecutive
     triggers; classifier needs 1; allocator needs 3. Name
     the rationale.
   - HITL disposition: first trigger is ALWAYS human-in-the-
     loop. After 3 consecutive clean re-trains, the operator
     may opt into auto-retrain — but the default is HITL.
   - Seasonal exclusions: quote PRODUCT_BRIEF.md §2 Nov–Dec
     (Black Friday / Year-End) row verbatim. Peak season is
     seasonality, not drift.

4. Cite the drift signal functions in src/retail/backend/
   routes/drift.py. For every signal (PSI, Jaccard, Brier,
   constraint-violation rate), name the function. If you cannot
   cite, say so.

Do NOT propose THRESHOLD VALUES. I write the numbers grounded in
the observed variance you reported in step 2. A threshold you
proposed that happens to match the 95th percentile is still
post-hoc — the discipline is that I set the number.

Do NOT use "auto-retrain when X" phrasing. Retrain is a human
decision. The monitor reports; the operator pulls. Reframe any
"auto-retrain" as "signal fires → operator decides".

Do NOT POST /drift/retrain_rule until I approve per rule. The
classifications are my call.

Any dollar figure cited — including any §2 cost (e.g. $45 for
wrong-segment, driving the segmentation drift urgency) — must be
quoted verbatim from §2. Drift thresholds themselves are
variance-grounded (not $-grounded), but any downstream dollar
claim ("below this threshold, the wrong-segment cost climbs
above $X/month") must be §2-sourced.

Do NOT use "blocker" without naming the specific ship-action.

When the reference is confirmed registered, the observed-variance
table is populated from both windows, and the three rule shapes
are drafted with cadence / HITL / seasonal exclusion, stop and
wait for me to write the threshold values.
```

### Why this prompt is written this way

- Inheritance-framed opening names the scaffold's drift reference and endpoints and keeps the three threshold values with me — three rules, three cadences is the load-bearing structural insight.
- Variance-grounded thresholds are required with explicit percentile language so the agent reports variance rather than picking a round number.
- "Do NOT attempt to re-seed" is the load-bearing anti-trap from Phase 13 common failure #1 — re-seeding masks a scaffold issue as a drift problem.
- No-auto-retrain phrasing enforces the `.claude/rules/agent-reasoning.md` principle that retrain stays with the human — monitor reports, operator pulls.
- Show-the-brief on Nov–Dec seasonal exclusion is mandatory because without it the first Black Friday spike triggers a retrain on known seasonality.

### What to expect back

- `journal/phase_13_retrain.md` with three rule skeletons (segmentation / churn / conversion).
- An observed-variance table with 50th / 95th / 99th percentile per signal from the two `/drift/check` windows.
- `"reference_set": true` confirmations for each model.
- Every signal cited to a function in `src/retail/backend/routes/drift.py`.
- A quoted Nov–Dec seasonal exclusion line from `PRODUCT_BRIEF.md §2`.
- A stop signal pending my threshold values.

### Push back if you see

- A proposed threshold value ("15% membership churn") — "please remove; I write the values from the observed variance you reported."
- "Auto-retrain when X > Y" phrasing — "please reframe as 'signal fires → operator decides'. retrain is a human call."
- One combined rule for three models — "the three models have different cadences; please split into three rules."
- An attempt to re-register drift reference data — "please don't re-seed; if `reference_set` is false, that's a scaffold issue — hand up instead."
- Missing Nov–Dec exclusion — "please quote the §2 Nov–Dec row; peak-season spikes are seasonality, not drift."

### Adapt for your next domain

- Change the three models (segmentation / churn / conversion) to your domain's deployed artefacts.
- Change `PSI / Jaccard / Brier / constraint-violation rate` signals to your domain's drift signals.
- Change `Nov–Dec Black Friday` to your domain's known seasonality window.
- Change `monthly / weekly / daily` cadences to match your models' observable drift timescales.
- Change `/drift/status/{model_id}` etc. to your domain's drift endpoints.

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

## Appendix B — Build your own value-chain dashboard at your next job

Tonight's viewer (the `http://localhost:3000` dashboard) is a **teaching instrument**. It exists because a 3.5-hour workshop packs the whole ML value chain into one sitting — students need a "where am I" anchor that would be diffuse across weeks in a real job. Your next ML project will span weeks or months, so the pressure to show "where am I" visually drops. You probably do not need a dashboard at all — you need the Playbook in a file, a journal, and a terminal.

But if your product has multiple stakeholders who need to see progress (CMO, Legal, Ops, Finance), a value-chain dashboard is a useful shared artefact. Build your own. Here is the pattern — not the code — so you can recreate it on any stack.

### The four parts of the pattern

1. **Pipeline banner.** A horizontal strip of N stages showing the flow of your product's lifecycle. For an ML product the stages are typically: `Analyze → Plan → Discover → Predict → Decide → Monitor → Review → Codify`. Label each stage with its paradigm (USML, SML, Optimization, MLOps, MLOps again) and its clock or calendar window. Colour: green for completed, orange for current, grey for upcoming.
2. **Current-phase detail.** A one-paragraph panel under the banner: which phase you're in, the levers you're pulling this phase (3–5, from the lever taxonomy in §4.6), and when the phase ends. This is the "orientation" that a 15-minute hallway chat with a stakeholder should produce.
3. **Decision-moments checklist.** The 5 Trust-Plane decision moments for the product, each rendered as a ticked or un-ticked line. Every decision moment carries a one-line rubric criterion (see §6). When a student journals a decision that clears the criterion, the box ticks. This is the shared visible signal of "we made a judgement call and wrote it down."
4. **Module cards.** One tile per model / system / sub-product, each showing the headline numbers from its current state (baseline metric, chosen threshold, latest drift severity). The cards are read-only — decisions happen in prompts and journals, not on the dashboard. The dashboard just mirrors state.

### The contract that makes it work

The dashboard is a view over a **single state artefact** — one JSON file (or one row in a database) that the backend owns and the dashboard polls. The state artefact has three top-level keys:

- `pipeline`: the ordered list of stages with their metadata (id, label, clock)
- `current`: what stage / phase the product is in right now, plus which levers
- `decision_moments`: the list of 5 rubric-anchored decisions with `completed: true|false`

Two endpoints govern it: `GET /state/current` (the dashboard polls this every 2–5 seconds) and `POST /state/advance` (the engineer calls this at the start of each phase). The polling interval is a taste call — 2s feels alive in a workshop, 30s is enough in real product work.

### When to build it

- **Day 1 of any ML project** if the stakeholders need a shared visible progress signal. A 200-line HTML file and a two-endpoint state contract is a one-afternoon build.
- **Before a major review** if the project has been running long enough that nobody remembers what was decided three months ago. The decision-moments checklist is your receipt trail.
- **Never** if you are the sole stakeholder AND you keep rigorous journal entries. The journal is the source of truth; the dashboard is a viewing convenience.

### When NOT to build it

- Your team uses Linear / Jira / Notion and is disciplined about status. Those tools already render a view like this; adding a custom dashboard competes for attention.
- The product is a one-person research project. A personal journal + the Playbook PDF open in a tab is lighter weight.
- You plan to build it and then stop maintaining it. An outdated dashboard is worse than no dashboard — it tells stakeholders a lie.

### The real portable artefact is the Playbook, not the viewer

You do not need a dashboard to run the 14 phases. You do need the Playbook, a journal file, and the rubric. If the dashboard doesn't happen, the workflow still ships. If the Playbook doesn't happen, no dashboard will save you.

Tonight's viewer is the scaffolding around the Playbook. The Playbook is what you take with you.

---

**END OF PLAYBOOK — v2026-04-23 · Universal Edition · Week 5 (Arcadia Retail) instantiation**
