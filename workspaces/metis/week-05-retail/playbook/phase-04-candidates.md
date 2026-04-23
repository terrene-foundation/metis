<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 4 — Candidates

> **What this phase does:** Run a fair sweep of this sprint's model families — same features, same stability protocol, naive baseline on every row — so the Phase 5 pick is defensible as a choice among real alternatives.
> **Why it exists:** A single-model run has nothing to compare against; picking without a baseline means you cannot say your choice beats doing nothing sophisticated.
> **You're here because:** Feature decisions are approved (`phase-03-features.md`). This phase is opened TWICE — once during Sprint 1 USML (clustering) and once during Sprint 2 SML (classifiers).
> **Key concepts you'll see:** algorithm family, hyperparameter sweep vs family sweep, naive baseline, multi-family comparison

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering Playbook Phase 4 — Candidates. My decision here is
nothing yet — the pick happens in Phase 5. My job is to commission a
comparable sweep and read the numbers.

Run the sweep with:

1. Three or more families spanning genuinely different assumptions
   (not three variants of the same family).
2. Identical features across all candidates — no silent feature drift
   between rows of the leaderboard.
3. Identical stability protocol across all candidates — same seeds,
   same held-out set, same resample count.
4. A NAIVE BASELINE on the leaderboard. Without the baseline the
   leaderboard winner is not defensible.

For every algorithm or method you name, cite the specific file and
function you read it from. If you cannot cite, say "I did not read
the source for this — marking the claim uncertain."

Produce a leaderboard table with the same columns for every row,
including the naive baseline.

Do NOT pick a winner. Do NOT propose a final K or threshold. Phase 5
picks; Phase 6 sets floors and thresholds. Your job is a comparable
leaderboard, not a decision.

When the leaderboard is in the journal with every row cited, stop and
wait for me to run Phase 5.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

```
If Sprint 1 USML (clustering):
  - KNOWN TRAP: Do NOT use AutoMLEngine. kailash-ml 0.17.0 raises
    ValueError on task_type='clustering'. Use /segment/fit directly
    per src/retail/backend/routes/segment.py. Losing ten minutes on
    an AutoML detour is a documented trap.
  - Families: K-Means at K=3, 5, 7; DBSCAN at two density settings;
    spectral at K=5. Five candidates total.
  - Naive baseline: pre-baked K=3 reference at
    src/retail/data/segment_baseline.json.
  - Leaderboard columns: silhouette, bootstrap Jaccard stability,
    segment-size distribution (min / max / balance ratio).
  - Journal file: journal/skeletons/phase_4_usml.md →
    journal/phase_4_usml.md.

If Sprint 2 SML (classifier):
  - KNOWN TRAP: Default threshold 0.5 is an implicit Phase 6
    decision. Do NOT apply any threshold in this phase — report
    raw scores only and defer the threshold to Phase 6 SML.
  - Families: logistic regression (linear), random forest (tree bag),
    gradient-boosted ensemble (GBM/XGBoost/LightGBM). Three families,
    1–2 hyperparameter settings each.
  - Naive baseline: majority-class prediction for each target.
  - Leaderboard endpoints: /predict/leaderboard/churn AND
    /predict/leaderboard/conversion per
    src/retail/backend/routes/predict.py.
  - Leaderboard columns: AUC, PR-AUC, Brier score, precision +
    recall at a REPORTED (not chosen) threshold, top-5 feature
    importance.
  - Journal file: journal/skeletons/phase_4_sml.md →
    journal/phase_4_sml.md.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success (USML — Sprint 1):**

- ✓ Leaderboard has at least 5 rows including the K=3 baseline from `segment_baseline.json`
- ✓ Silhouette, Jaccard stability, and segment-size distribution present for every row
- ✓ All candidates use the same feature set approved in Phase 3
- ✓ No winner proposed — numbers only
- ✓ Viewer (http://localhost:3000) shows: clustering leaderboard card filled with the K sweep results — one row per candidate, silhouette and stability columns visible, baseline row present

**Signals of success (SML — Sprint 2):**

- ✓ Leaderboard has at least 4 rows including the majority-class baseline
- ✓ AUC, PR-AUC, Brier score present for every row; no threshold applied
- ✓ Top-5 feature importance shown per model
- ✓ No winner proposed, no threshold named
- ✓ Viewer (http://localhost:3000) shows: three-family leaderboard panel filled for churn and conversion targets, baseline row included

**Signals of drift — push back if you see:**

- ✗ `AutoMLEngine` named in Sprint 1 context ("please use `/segment/fit` directly; AutoMLEngine raises ValueError on clustering in kailash-ml 0.17.0")
- ✗ A threshold of 0.5 applied in Sprint 2 ("threshold is a Phase 6 decision — please report raw scores only")
- ✗ Leaderboard without a baseline row ("where is the naive baseline? K=3 reference for USML, majority-class for SML")
- ✗ A winner proposed at Phase 4 ("Phase 4 has no decision; please remove the recommendation")
- ✗ Different feature counts across leaderboard rows ("candidates must be on identical features")
- ✗ Algorithm name with no function citation ("which file and function in `src/retail/backend/` produces this?")
- ✗ Viewer shows nothing new after CC reports the phase complete — CC may have described the work, not run it. Re-prompt: "show me the leaderboard card rendered in the viewer"

---

## 3. Things you might not understand in this phase

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **Algorithm family** — a class of models that share the same mathematical assumptions about what data structure looks like, as opposed to minor variants within one family
- **Hyperparameter sweep vs family sweep** — the difference between tuning settings within one algorithm (hyperparameter sweep) and comparing fundamentally different algorithms (family sweep), and why only the latter makes a leaderboard defensible
- **Naive baseline** — the simplest possible prediction approach, which your model must visibly beat before you can claim the ML is worth the complexity
- **Multi-family comparison** — running algorithms with genuinely different assumptions on the same features and protocol so the comparison is fair

---

## 4. Quick reference (30 sec, generic)

### Algorithm family

A group of algorithms that make the same structural assumptions about data. K-means assumes clusters are spherical blobs around a centre. DBSCAN assumes clusters are dense regions separated by sparse gaps. Logistic regression assumes a linear decision boundary. Gradient-boosted trees assume the signal can be captured by sequential corrections to a weak model. Mixing families (not variants of one family) is what makes a leaderboard meaningful — you're testing different structural bets, not just different settings of the same bet.

> **Deeper treatment:** [appendix/03-modeling/unsupervised-families.md](./appendix/03-modeling/unsupervised-families.md)

### Hyperparameter sweep vs family sweep

A hyperparameter sweep tries K=3, K=5, K=7 all within K-means — useful for tuning but it doesn't tell you whether K-means is the right family at all. A family sweep pits K-means against DBSCAN against spectral — it tests whether the structural assumptions match the data's real shape. Tonight you do a family sweep with a small hyperparameter sample per family (not an exhaustive grid). The goal is a defensible choice, not an optimised one.

> **Deeper treatment:** [appendix/03-modeling/hyperparameter-sweeps.md](./appendix/03-modeling/hyperparameter-sweeps.md)

### Naive baseline

The simplest prediction that requires no ML. For clustering: the pre-existing K=3 hand-authored rulebook. For classification: predict the majority class for every record. The baseline is on every leaderboard row because "my model is better than the baseline" is the minimum bar for shipping. If the winning candidate doesn't clearly beat the baseline, the business case evaporates: save the money, ship the rulebook.

> **Deeper treatment:** [appendix/03-modeling/naive-baselines.md](./appendix/03-modeling/naive-baselines.md)

### Multi-family comparison

Running at least three families with genuinely different assumptions on the same features, same held-out set, and same stability protocol. The comparison is only valid if the protocol is identical — different feature counts, different seeds, or different test sets make the numbers incomparable. If the leaderboard rows don't share a protocol, the winner is an artefact of the protocol difference, not the algorithm quality.

> **Deeper treatment:** [appendix/03-modeling/stability-protocols.md](./appendix/03-modeling/stability-protocols.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in Playbook
Phase 4 — Candidates.

Read `workspaces/metis/week-05-retail/playbook/phase-04-candidates.md`
for what this phase does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. naive baseline >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in Phase 4
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] Leaderboard complete — same columns for every row, naive baseline included
- [ ] All candidates run on the same approved feature set
- [ ] Every family name cited to a function in `src/retail/backend/`
- [ ] No winner proposed, no threshold or K named
- [ ] Journal file written (`phase_4_usml.md` or `phase_4_sml.md`)

**Next file:** [`phase-05-implications.md`](./phase-05-implications.md)

This file is opened twice — once for Sprint 1 USML and once for Sprint 2 SML. When you return here for Sprint 2, re-read the tonight-specific additions for the SML branch before pasting.
