<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 6 — Metric + Threshold

> **What this phase does:** Pre-register your quality floors (USML) or your threshold-selection rule (SML) IN WRITING, with a timestamp, BEFORE you re-open the leaderboard — then pick the operating point that clears the floors.
> **Why it exists:** Floors set after seeing the results are always conveniently where the leader landed. Pre-registration is the only structural proof that you didn't cheat yourself.
> **You're here because:** A candidate has been selected in Phase 5 (`phase-05-implications.md`). This phase is opened TWICE — Sprint 1 USML (three floors) and Sprint 2 SML (PR curve + calibration).
> **Key concepts you'll see:** pre-registered floors, separation / stability / actionability (USML); PR curve, ROC vs PR, calibration / Brier score, cost-based threshold (SML)

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering Playbook Phase 6 — Metric + Threshold. My decision here
is the FLOORS and the THRESHOLD RULE — and I am pre-registering them
in writing BEFORE we re-open the leaderboard.

Here is how I want you to help me pre-register:

1. CONFIRM that you have not yet reopened the Phase 4 leaderboard. If
   you have already seen the winning result in the last two messages,
   say so — we must record that the floors were set post-hoc. Honesty
   first; do not conceal the order.

2. For unsupervised models — draft the floor DEFINITIONS (not values)
   in the journal:
   (a) Separation floor — metric name and how it is measured.
   (b) Stability floor — protocol and re-seed count.
   (c) Actionability floor — named as a TEST, not a number.

3. For supervised models — draft the threshold-selection RULE (not the
   value):
   (a) Which curve to read (PR or ROC) and why.
   (b) Cost asymmetry — two cost terms, both sourced from the project
       brief verbatim.
   (c) Calibration floor — Brier score cutoff; if breached, calibrate
       before threshold selection.

4. Compute the dollar-lift framework — the formula, not the number.
   I plug in the counts when I see the leaderboard.

5. Timestamp the pre-registration. Record wall-clock time in the
   journal header. This is the only evidence that the floors preceded
   the results.

Do NOT propose floor values. I write those myself in the journal, at a
timestamp that precedes my next leaderboard read.

Do NOT use "blocker" without a specific blocked action. An un-set
floor is not a blocker; it is the phase I am currently running.

When the journal has floor DEFINITIONS (unsupervised) or the
threshold-rule FRAME (supervised), a timestamp, and the lift-formula
skeleton, stop and wait for me to write the values.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

```
If Sprint 1 USML (clustering):
  - Three floors: (a) Separation = silhouette (measured how? cite
    the function in src/retail/backend/routes/segment.py); (b)
    Stability = bootstrap Jaccard over how many re-seeds?; (c)
    Actionability = one distinct marketing action per segment, tested
    by writing the action in one sentence per segment — not a number.
  - Dollar counterfactual formula: "if K=N moves X customers off the
    $45/wrong-segment path, monthly lift = $45 × X." I plug in X
    when I see the leaderboard.
  - Journal file: journal/skeletons/phase_6_metric_threshold.md →
    journal/phase_6_usml.md.

If Sprint 2 SML (classifier):
  - Curve: PR not ROC. Churn and conversion are rare-positive
    problems — ROC is overly optimistic on imbalanced data.
    Endpoint: per src/retail/backend/routes/predict.py.
  - Cost asymmetry: $3 per-customer touch from PRODUCT_BRIEF.md §2
    (quote verbatim); $120 CAC from PLAYBOOK.md Phase 6 SML (cite
    the Playbook line, not §2 — rubric penalises §2 citation for
    the $120 figure).
  - Calibration floor: Brier score cutoff; if breached, run isotonic
    calibration before threshold selection (raw GBM probabilities
    are usually miscalibrated).
  - Journal file: journal/phase_6_sml.md.
  - Actionability floor: named as "precision ≥ X at minimum recall Y"
    — the X and Y are mine to set.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success (USML — Sprint 1):**

- ✓ Three floor DEFINITIONS in the journal (separation, stability, actionability) — no values yet
- ✓ Actionability floor expressed as a TEST ("one distinct marketing action per segment"), not a number
- ✓ Dollar counterfactual formula skeleton present with $45 from PRODUCT_BRIEF.md §2 quoted verbatim
- ✓ Wall-clock timestamp in the journal header
- ✓ An honest note of whether the leaderboard has been seen yet (ideally: "not yet")
- ✓ Viewer (http://localhost:3000) shows three-floor panel with separation / stability / actionability bars awaiting values

**Signals of success (SML — Sprint 2):**

- ✓ PR curve named (not ROC), endpoint cited from `routes/predict.py`
- ✓ $3 touch cost quoted verbatim from `PRODUCT_BRIEF.md §2`; $120 CAC cited to `PLAYBOOK.md Phase 6 SML`
- ✓ Calibration floor defined (Brier score, recalibration trigger)
- ✓ Threshold-selection rule framed (precision-at-recall target or cost-minimisation rule) — value is blank
- ✓ Wall-clock timestamp in the journal header
- ✓ Viewer (http://localhost:3000) shows PR curve with threshold marker and calibration plot — threshold marker pending your value entry

**Signals of drift — push back if you see:**

- ✗ A proposed floor value ("silhouette ≥ 0.25", "Jaccard ≥ 0.80", "threshold 0.3") — "please remove the value; I write those myself. Your job is the definition."
- ✗ No timestamp on the journal entry ("please add wall-clock time to the header so the order is auditable")
- ✗ $120 CAC cited to `PRODUCT_BRIEF.md §2` ("that's in `PLAYBOOK.md` Phase 6 SML, not the brief — please re-cite")
- ✗ ROC named as the SML threshold curve ("churn and conversion are rare-positive; please use PR, not ROC")
- ✗ Actionability expressed as a number ("actionability is a test — 'one distinct action per segment' — not a number")
- ✗ Viewer shows nothing new after CC reports the phase complete — re-prompt: "show me the floor panel or PR curve rendered in the viewer"

---

## 3. Things you might not understand in this phase

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **Pre-registered floors** — writing down your quality thresholds BEFORE you see the results, so the thresholds can't be conveniently set where the winner already landed
- **Separation / stability / actionability** (USML) — the three independent dimensions a clustering must pass: how crisp the clusters are, how stable they are across re-runs, and whether each one warrants a distinct business action
- **PR curve** (SML) — the precision-vs-recall curve used to choose an operating threshold for rare-positive problems; different from ROC, which is optimistic on imbalanced data
- **ROC vs PR** — why these two curves tell different stories and when each is appropriate
- **Calibration / Brier score** (SML) — whether a model's predicted probabilities are trustworthy as probabilities (not just rankings), and how to measure and fix miscalibration
- **Cost-based threshold** (SML) — picking the threshold that minimises expected dollar cost given your false-positive and false-negative cost terms, rather than defaulting to 0.5

---

## 4. Quick reference (30 sec, generic)

### Pre-registered floors

A quality threshold written down BEFORE you see the results. The key word is "before." A floor set after seeing the leaderboard is always conveniently where the winner landed — you have quietly guaranteed the winner passes. A timestamped floor in the journal, set before the leaderboard is opened, is the structural proof that you made a real decision rather than rationalising the outcome. Tonight, you write the values yourself; CC writes the definitions.

> **Deeper treatment:** [appendix/04-evaluation/pre-registered-floors.md](./appendix/04-evaluation/pre-registered-floors.md)

### Separation / stability / actionability

The three floors a USML model must clear independently. **Separation** (silhouette, Davies-Bouldin) measures how crisp the clusters are — high overlap = low separation. **Stability** (bootstrap Jaccard) measures what fraction of customers stay in the same segment when you re-cluster on a different month or seed — instability means campaigns are built on a moving target. **Actionability** is a TEST, not a number: can you write a distinct one-sentence marketing action for each segment? If two segments get the same sentence, collapse them. All three must pass; clearing two doesn't count.

> **Deeper treatment:** [appendix/04-evaluation/silhouette.md](./appendix/04-evaluation/silhouette.md)

### PR curve

The precision-vs-recall curve sweeps through every possible threshold for a classifier and plots what fraction of its positives were correct (precision) against what fraction of the true positives it caught (recall). For rare-positive problems — churn is typically 5–15% of customers, fraud is <1% — the PR curve is more informative than the ROC curve. The PR curve shows degradation on imbalanced data that the ROC curve hides. Use PR when positives are rare and every missed positive is expensive.

> **Deeper treatment:** [appendix/04-evaluation/pr-curve.md](./appendix/04-evaluation/pr-curve.md)

### ROC vs PR

ROC (Receiver Operating Characteristic) plots true positive rate vs false positive rate at every threshold. It is appropriate when classes are roughly balanced OR when you care about ranking (not decisions). PR (Precision-Recall) plots precision vs recall. It is appropriate when positives are rare and a false negative is costly. The difference matters: a classifier on 5% positive rate can show AUC-ROC = 0.95 while performing poorly in practice. The PR curve will show this degradation; the ROC curve will not.

> **Deeper treatment:** [appendix/04-evaluation/roc-auc.md](./appendix/04-evaluation/roc-auc.md)

### Calibration / Brier score

Calibration means that when a model says "30% probability," roughly 30% of those cases actually happen. A model can rank customers perfectly (AUC = 0.9) but be badly miscalibrated (the model says 70% probability for things that happen 20% of the time). Calibration matters whenever you use the probability directly — for example, in an allocator that weights campaign spend by predicted conversion probability. The Brier score is the mean squared error of predicted probability vs actual outcome: lower is better, 0.25 is the uninformative baseline.

> **Deeper treatment:** [appendix/04-evaluation/calibration-and-brier.md](./appendix/04-evaluation/calibration-and-brier.md)

### Cost-based threshold

Choosing the classifier's decision threshold by minimising the expected dollar cost of predictions. For each possible threshold, compute: (false positive rate × cost of a false alarm) + (false negative rate × cost of a miss). Pick the threshold that gives the lowest expected cost. This replaces "0.5 because default" with math. Tonight: touch cost $3 (false alarm) vs CAC $120 (missed churn) — a 40:1 ratio that pushes the threshold well below 0.5.

> **Deeper treatment:** [appendix/04-evaluation/pr-curve.md](./appendix/04-evaluation/pr-curve.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in Playbook
Phase 6 — Metric + Threshold.

Read `workspaces/metis/week-05-retail/playbook/phase-06-metric-threshold.md`
for what this phase does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. pre-registered floors >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in Phase 6
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] Floor definitions (USML) or threshold-rule frame (SML) in the journal
- [ ] Wall-clock timestamp in the journal header
- [ ] Dollar-lift formula skeleton present with sourced cost terms
- [ ] $3 → quoted from `PRODUCT_BRIEF.md §2`; $120 → cited to `PLAYBOOK.md Phase 6 SML`
- [ ] No floor values proposed by CC — you wrote them yourself
- [ ] CC confirmed it has not re-opened the leaderboard

**Next file:** [`phase-07-redteam.md`](./phase-07-redteam.md)

This file is opened twice — once for Sprint 1 USML and once for Sprint 2 SML. When you return here for Sprint 2, re-read the tonight-specific additions for the SML branch before pasting.
