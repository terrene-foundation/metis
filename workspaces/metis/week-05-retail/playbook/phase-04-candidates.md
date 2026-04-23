<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

_[← Playbook index (README)](./README.md)_

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

