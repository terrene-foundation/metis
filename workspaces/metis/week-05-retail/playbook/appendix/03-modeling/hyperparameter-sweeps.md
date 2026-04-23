<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Hyperparameter Sweeps

> **One-line hook:** The systematic search over model configuration knobs that determines how well the model fits your data — not a task for manual tuning.

## The gist

Every ML model has **hyperparameters** — settings that govern how the model learns, not what it learns. For a decision tree, max depth is a hyperparameter. For K-means, K is a hyperparameter. For a gradient-boosted model, learning rate, number of trees, and max depth are all hyperparameters.

Hyperparameters are not learned from the data. You set them before training, and the wrong setting produces a model that either underfits (too simple — low training and test performance) or overfits (memorises training data — high training, low test performance).

A **sweep** is a systematic search over hyperparameter combinations. Instead of manually trying K=3, then K=5, then K=7, the sweep tries all three (and more) automatically and reports back a leaderboard of which configuration performs best on a held-out validation set.

For Arcadia Sprint 1 (USML): the sweep tries multiple K values across multiple clustering families. The leaderboard ranks configurations by silhouette score and bootstrap Jaccard stability. You look at the leaderboard in Phase 5 and pick — you don't just take the top-ranked one blindly; you consider the operational ceiling (ceiling = 6 segments means K > 6 is non-starters regardless of score).

For Sprint 2 (SML): the sweep tries multiple configurations of each classifier family. The leaderboard ranks by AUC on the held-out validation set. Again, you pick — not just on AUC, but also on calibration and inference speed.

The Phase 4 prompt boots the sweep; the Phase 5 prompt is where you actually decide.

## Why it matters for ML orchestrators

Your job is to read the leaderboard and pick, not to tune the knobs yourself. But you need to know enough to ask: was the sweep broad enough? Did it include the baseline family? Did it use cross-validation or a single holdout split? A sweep on a single 80/20 split can give misleading rankings.

## Common confusions

- **"The top of the leaderboard is always the right pick"** — Not if the top model has negligible gains over the second-place model but is much slower to retrain. And not if K=7 tops the leaderboard but exceeds your operational ceiling of 6.
- **"More hyperparameter combinations is always better"** — The sweep must complete in your session timeframe. For a 3.5-hour workshop, the scaffold pre-limits sweep breadth to configurations that fit within ~5 minutes per family.

## When you'll hit it

Used in: Phase 4 (Candidates — the sweep runs here), Phase 5 (Implications — you pick from the leaderboard), workflow-03, workflow-04 (Sprint boots kick off the sweeps)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Bergstra & Bengio, "Random Search for Hyper-Parameter Optimization" — random search beats grid search
- Feurer & Hutter, "Hyperparameter Optimization" — survey chapter in AutoML book
