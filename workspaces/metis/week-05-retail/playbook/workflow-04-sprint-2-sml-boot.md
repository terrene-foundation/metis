<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 4 — Sprint 2 SML Boot (churn + conversion classifiers)

> **What this step does:** Boot Sprint 2 by copying SML skeleton files, confirming both classifier endpoints live, and orienting Claude Code on the SML paradigm — before re-opening Phase 4 for the SML pass.
> **Why it exists:** Sprint 2 replays Phases 4–8 with a different model type and different evaluation rules. A boot that confuses the SML pass with Sprint 1's USML pass produces journals with crossed wires and PR curves where silhouette scores should be.
> **You're here because:** Phase 8 (Sprint 1 deployment gate) was signed. Sprint 1 USML is complete.
> **Key concepts you'll see:** SML replay, rare-positive problem, PR curve vs ROC, cost asymmetry citation split, downstream calibration

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering a supervised ML sprint. The scaffold pre-trains classifiers at
startup — someone committed to the algorithm families on my behalf. My job
this sprint is to pick one family per classifier and set each classifier's
threshold against the cost asymmetry.

This sprint REPLAYS a set of Playbook phases — once each, covering all
classifiers in scope. The earlier shared phases (Frame, Data Audit, Feature
Classification) are NOT re-run — the outputs from the earlier sprint apply.
The metric phase in this sprint is the SML variant: PR curve + cost-based
threshold + calibration, not the unsupervised multi-floor variant.

Before I start the phase walk:

1. Copy the SML skeletons from journal/skeletons/ into journal/ — one file
   per phase. See journal/skeletons/README.md for the inventory.

2. Confirm the sprint endpoints are live. For each classifier endpoint,
   check that it returns the expected family candidates. If any endpoint is
   not live, STOP and raise a hand.

3. For every algorithm family, loss function, or calibration method you name,
   cite the specific file and function in the codebase. If you cannot cite,
   say so.

4. Do NOT propose a threshold for any classifier. That is my decision in
   the metric+threshold phase journal, set by reading the PR curve against
   the cost asymmetry — NOT by picking the default.

5. Do NOT use the word "blocker" without naming a specific action I cannot take.

Once skeletons are copied and endpoints confirmed, summarise: (a) the phases
of this sprint, (b) each classifier and what it feeds downstream, (c) which
curve to use for threshold selection and why (not ROC).

Then stop and wait for my Phase 4 SML prompt.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

```
Sprint: Sprint 2 SML — churn + conversion classifiers.
Phases covered: Playbook phases 4, 5, 6, 7, 8 — the SML replay.
Phases 1, 2, 3 are SHARED with Sprint 1 and are NOT re-run.
Phase 6 in this sprint is the SML variant (PR curve + cost-based threshold +
calibration), NOT the USML three-floor variant.

Guard: if you think you are running Phase 10 at any point in this sprint,
you are in the wrong sprint — Phase 10 is Sprint 3.

Skeleton copy: copy phase_{4..8}_sml.md from journal/skeletons/ into
workspaces/metis/week-05-retail/journal/. Five files. See
journal/skeletons/README.md.

Endpoint checks (GET only):
- /predict/leaderboard/churn → should return a candidates object with
  exactly three keys: logistic_regression, random_forest, gradient_boosted
- /predict/leaderboard/conversion → same three-key structure
If either is not live, STOP and raise a hand.

For every family, loss function, or calibration method named, cite the
specific file and function in src/retail/backend/. If you cannot cite, say so.

Cost asymmetry — citation split:
- Churn: $120 CAC-to-reacquire vs $3 per-touch (40:1 ratio).
  The $3 touch cost is in PRODUCT_BRIEF.md §2 — quote the line.
  The $120 CAC is in PLAYBOOK.md Phase 6 SML — cite PLAYBOOK.md, NOT §2.
- Conversion: downstream asymmetry covered in Phase 6 SML.

Do NOT propose a threshold for either classifier. The threshold is my call in
phase_6_sml.md, set by reading the PR curve against the cost asymmetry —
NOT by picking 0.5 because it's the default. Proposing a value here corrupts
the pre-registration.

Summary must include:
(a) The five phases of this sprint (no Phase 1/2/3, no Phase 10).
(b) The two classifiers and what each feeds downstream: churn → retention;
    conversion → Sprint 3 allocator (calibration matters because the
    allocator consumes the probability directly).
(c) PR curve (not ROC) as the threshold-selection curve — churn and
    conversion are rare-positive problems.

Then stop and wait for my Phase 4 SML prompt.
```

**How to paste:** Combine both blocks into a single paste into your `claude` session.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ Five skeleton files copied: `journal/phase_{4..8}_sml.md` all exist with blanks intact
- ✓ A live GET against `/predict/leaderboard/churn` returning three-family candidates
- ✓ A live GET against `/predict/leaderboard/conversion` returning three-family candidates
- ✓ Summary names: (a) five phases, (b) two classifiers and their downstream consumers, (c) PR curve (not ROC) as the threshold-selection tool
- ✓ No proposed threshold value for either classifier
- ✓ Stop signal pending the Phase 4 SML prompt
- ✓ Viewer (http://localhost:3000) refreshes and shows: Sprint 2 tile activates; leaderboard panels for churn and conversion are visible as placeholders

**Signals of drift — push back if you see:**

- ✗ A proposed threshold ("I'd use 0.3 for churn") — ask "please remove; I set the threshold in `phase_6_sml.md` against the PR curve."
- ✗ Phase 10 / 11 / 12 mentioned in this sprint's scope — ask "aren't those Sprint 3? Please re-check against `PLAYBOOK.md` §5."
- ✗ ROC named as the primary curve for churn or conversion — ask "aren't churn and conversion rare-positive problems? PR curve, not ROC — please re-check."
- ✗ $120 cited to `PRODUCT_BRIEF.md §2` — ask "is $120 in §2? I think it's in `PLAYBOOK.md` Phase 6 SML."
- ✗ A downstream link for conversion that isn't the Sprint 3 allocator — ask "where does the conversion probability get consumed? I thought the allocator."
- ✗ Viewer Sprint 2 tile does not activate — confirm both leaderboard GETs ran and returned three-family candidates.

---

## 3. Things you might not understand in this step

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **SML replay** — re-running phases 4–8 for a different model family (supervised classifiers vs unsupervised clustering)
- **Rare-positive problem** — a classification task where the positive class (churn, conversion) is uncommon, making precision–recall more meaningful than ROC
- **PR curve vs ROC** — two ways to visualise classifier performance; PR is more informative when the positive class is rare
- **Cost asymmetry citation split** — different numbers come from different sources; citing the wrong source corrupts the brief-grounding rule
- **Downstream calibration** — why the conversion classifier's probability output must be well-calibrated, not just accurate

---

## 4. Quick reference (30 sec, generic)

### SML replay

Running Phases 4–8 a second time, for the supervised classifiers, using the same phase structure as Sprint 1 but with different questions. Phase 6 changes the most: instead of three floors for unsupervised quality, you're reading a PR curve and selecting a threshold against a cost ratio. The replay is not repetition — it's a different decision in the same frame. The confusion to avoid: treating phases 1–3 as needing re-runs (they don't) or importing Phase 10 from Sprint 3 (wrong sprint).

> **Deeper treatment:** [appendix/03-modeling/supervised-families.md](./appendix/03-modeling/supervised-families.md)

### Rare-positive problem

A classification task where the positive outcome (customer churns, customer converts) is much less common than the negative (stays, doesn't convert). For Arcadia, churn is ~8% and conversion is ~12%. When the positive class is rare, the ROC curve is optimistic because it's dominated by the large negative class. The PR curve removes this distortion by measuring precision and recall only on the positive class — the thing you actually care about. Using ROC for a rare-positive problem produces a threshold that looks good on paper and misclassifies many real churners.

> **Deeper treatment:** [appendix/04-evaluation/pr-curve.md](./appendix/04-evaluation/pr-curve.md)

### PR curve vs ROC

The ROC curve plots true-positive rate vs false-positive rate at every threshold. The PR curve plots precision vs recall at every threshold. For balanced classes, both tell a similar story. For rare-positive problems, ROC is misleading — a classifier that calls everything "not churn" can score 0.90 AUC. The PR curve exposes this: that same classifier has near-zero recall on churners. The decision rule: if your positive class is under 20% of data, use PR to pick the threshold.

> **Deeper treatment:** [appendix/04-evaluation/pr-curve.md](./appendix/04-evaluation/pr-curve.md)

### Cost asymmetry citation split

Tonight, the two cost numbers for churn come from different sources: the $3 per-touch is in `PRODUCT_BRIEF.md §2`; the $120 CAC is in `PLAYBOOK.md` Phase 6 SML. Citing both to §2 is a brief-grounding violation — §2 doesn't contain $120. Citing the $120 correctly to the Playbook matters because the rubric checks source citations, and an uncited cost figure weakens the threshold justification.

> **Deeper treatment:** [appendix/01-framing/cost-asymmetry.md](./appendix/01-framing/cost-asymmetry.md)

### Downstream calibration

Calibration means the classifier's output probability matches the actual frequency of the event. A classifier that says "60% chance of conversion" should be right 60% of the time. The conversion classifier's calibration matters because the Sprint 3 LP allocator consumes that probability directly when computing expected revenue. A miscalibrated classifier (e.g. one that always predicts 90%) produces a systematically distorted allocation plan. Calibration is checked in Phase 6 SML alongside the threshold decision.

> **Deeper treatment:** [appendix/04-evaluation/calibration-and-brier.md](./appendix/04-evaluation/calibration-and-brier.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in the Sprint 2
SML boot step.

Read `workspaces/metis/week-05-retail/playbook/workflow-04-sprint-2-sml-boot.md`
for what this step does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. rare-positive problem >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in the Sprint 2 boot
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] Five skeleton files exist in `journal/phase_{4..8}_sml.md`
- [ ] `/predict/leaderboard/churn` returned three-family candidates
- [ ] `/predict/leaderboard/conversion` returned three-family candidates
- [ ] Summary covers five phases, two classifiers with downstream consumers, PR curve selection rationale
- [ ] No proposed threshold for either classifier
- [ ] Claude Code has stopped and is waiting for the Phase 4 SML prompt

**Note on next file:** Phase 4 through Phase 8 are the same files you opened in Sprint 1 — you are re-opening them for the SML pass. This is intentional. The files are written to serve both passes. When you reach Phase 8 (Sprint 2 gate), the next file is `workflow-05-sprint-3-opt-boot.md`.

**Next file:** [`phase-04-candidates.md`](./phase-04-candidates.md)
