<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Appendix — ML Concept Reference

**Version:** 2026-04-23 · **License:** CC BY 4.0

Passive reference for Week 5 concepts. Open a file when the phase file's §4 quick-reference isn't enough. Each file is ~200 words: a plain-language gist, why it matters for orchestrators, common confusions, and which phases you'll hit it in.

---

## Themed Contents

### 01 — Framing

Concepts for Phase 1 (Frame) and the `/analyze` inheritance audit.

| File                                                                      | What it covers                                                                  |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| [target-and-population.md](./01-framing/target-and-population.md)         | Who the model predicts for — inclusions AND explicit exclusions                 |
| [horizon-and-ceiling.md](./01-framing/horizon-and-ceiling.md)             | How far ahead the model predicts; how many outputs the team can act on          |
| [cost-asymmetry.md](./01-framing/cost-asymmetry.md)                       | The two error costs in dollars — the only honest anchor for threshold decisions |
| [inheritance-vs-greenfield.md](./01-framing/inheritance-vs-greenfield.md) | Naming what's already fixed vs what's still yours to decide                     |

---

### 02 — Data

Concepts for Phases 2 (Data Audit) and 3 (Feature Framing).

| File                                                                   | What it covers                                                                         |
| ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [data-audit.md](./02-data/data-audit.md)                               | Six-category inspection with written dispositions before any model runs                |
| [feature-framing.md](./02-data/feature-framing.md)                     | Four-axis feature classification: availability, leakage, proxy risk, derivation        |
| [leakage.md](./02-data/leakage.md)                                     | Future information contaminating training — causes great test results, poor production |
| [proxy-for-protected-class.md](./02-data/proxy-for-protected-class.md) | Features that encode race, age, or ethnicity without being labelled as such            |
| [class-imbalance.md](./02-data/class-imbalance.md)                     | Rare events require PR curve evaluation, not accuracy — the churn/conversion case      |

---

### 03 — Modeling

Concepts for Phases 4 (Candidates) and 5 (Implications).

| File                                                                     | What it covers                                                                          |
| ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| [supervised-families.md](./03-modeling/supervised-families.md)           | Linear, tree, ensemble, neural — when each is reasonable for tabular data               |
| [unsupervised-families.md](./03-modeling/unsupervised-families.md)       | K-means, density-based, hierarchical, GMM — shape assumptions and failure modes         |
| [optimization-families.md](./03-modeling/optimization-families.md)       | LP, MIP, constraint satisfaction, greedy — when each fits the allocator problem         |
| [recommender-families.md](./03-modeling/recommender-families.md)         | Content-based, collaborative, hybrid — and why hybrid isn't automatically best          |
| [hyperparameter-sweeps.md](./03-modeling/hyperparameter-sweeps.md)       | Systematic search over model configuration knobs — how the Phase 4 leaderboard is built |
| [stability-protocols.md](./03-modeling/stability-protocols.md)           | Bootstrap Jaccard and re-seed tests — whether the model's structure holds on new data   |
| [naive-baselines.md](./03-modeling/naive-baselines.md)                   | The simplest possible model that every other candidate must beat                        |
| [cold-start.md](./03-modeling/cold-start.md)                             | What happens with no history — a product decision about the fallback, not a bug         |
| [dimensionality-reduction.md](./03-modeling/dimensionality-reduction.md) | PCA/NMF for preprocessing vs t-SNE/UMAP for visualisation — two distinct purposes       |

---

### 04 — Evaluation

Concepts for Phases 6 (Metric + Threshold), 7 (Red-Team), and 8 (Deployment Gate).

| File                                                                   | What it covers                                                                                            |
| ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| [silhouette.md](./04-evaluation/silhouette.md)                         | Per-customer cluster crispness — how far you are from your own cluster vs the nearest other               |
| [bootstrap-jaccard.md](./04-evaluation/bootstrap-jaccard.md)           | Clustering stability across resamples — ≥ 0.80 is the conventional shippable threshold                    |
| [elbow-method.md](./04-evaluation/elbow-method.md)                     | Visual K-selection heuristic — useful for ruling out extreme values, not for picking K alone              |
| [roc-auc.md](./04-evaluation/roc-auc.md)                               | Ranking quality for classifiers — right for comparing models, wrong for setting thresholds on rare events |
| [pr-curve.md](./04-evaluation/pr-curve.md)                             | Precision vs recall across thresholds — the right instrument for cost-based threshold selection           |
| [calibration-and-brier.md](./04-evaluation/calibration-and-brier.md)   | Whether probabilities are honest — critical when they feed a downstream LP objective                      |
| [confusion-matrix.md](./04-evaluation/confusion-matrix.md)             | TP/FP/TN/FN at a chosen threshold — the translation layer between metrics and dollar cost                 |
| [precision-at-k.md](./04-evaluation/precision-at-k.md)                 | Offline recommender metric — fraction of top-k recommendations the customer engaged with                  |
| [coverage-and-diversity.md](./04-evaluation/coverage-and-diversity.md) | Whether the recommender surfaces the full catalogue and varied lists — the long-tail metrics              |
| [pre-registered-floors.md](./04-evaluation/pre-registered-floors.md)   | Writing pass/fail thresholds before seeing results — the discipline that prevents goalpost-moving         |

---

### 05 — Deployment

Concepts for Phase 8 (Deployment Gate).

| File                                                                       | What it covers                                                                                      |
| -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [deployment-gate.md](./05-deployment/deployment-gate.md)                   | Formal PASS/FAIL decision before production — four elements: floors, red-team, monitoring, rollback |
| [shadow-staging-promotion.md](./05-deployment/shadow-staging-promotion.md) | Three-step path from trained model to live traffic — why skipping steps causes silent failures      |
| [rollback-patterns.md](./05-deployment/rollback-patterns.md)               | Signal + action + owner, declared before shipping, not improvised after drift                       |

---

### 06 — Monitoring

Concepts for Phase 13 (Drift) and Sprint 4.

| File                                                                         | What it covers                                                                                     |
| ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [drift-types.md](./06-monitoring/drift-types.md)                             | Feature drift, label drift, concept drift — three distinct failure modes, three monitoring signals |
| [psi.md](./06-monitoring/psi.md)                                             | Population Stability Index — single number measuring feature distribution shift from training      |
| [segment-membership-churn.md](./06-monitoring/segment-membership-churn.md)   | Fraction of customers moving between segments — the primary drift signal for USML models           |
| [calibration-decay.md](./06-monitoring/calibration-decay.md)                 | Divergence between stated probability and real-world rate — critical when probabilities feed LP    |
| [constraint-violation-rate.md](./06-monitoring/constraint-violation-rate.md) | Infeasibility and ops override rate — the primary drift signal for the allocator                   |
| [retrain-rules.md](./06-monitoring/retrain-rules.md)                         | Signal + threshold + duration window + human gate — all four components required                   |

---

### 07 — Governance

Concepts for Phases 11 (Constraints), 12 (Solver Acceptance), and 13 (Drift).

| File                                                                       | What it covers                                                                                              |
| -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| [pdpa-basics.md](./07-governance/pdpa-basics.md)                           | Singapore's PDPA §13 and the under-18 hard exclusion in the Arcadia allocator                               |
| [hard-vs-soft-constraints.md](./07-governance/hard-vs-soft-constraints.md) | Hard = infeasible if violated; soft = violate at a dollar penalty — classifying which is a Trust Plane call |
| [shadow-prices.md](./07-governance/shadow-prices.md)                       | Dollar cost of tightening a constraint — makes regulatory and business trade-offs legible                   |
| [hitl-patterns.md](./07-governance/hitl-patterns.md)                       | Where humans must decide rather than the system acting automatically                                        |

---

## Alphabetical Concept Index

| Concept                          | File                                                                                       |
| -------------------------------- | ------------------------------------------------------------------------------------------ |
| AUC                              | [04-evaluation/roc-auc.md](./04-evaluation/roc-auc.md)                                     |
| Bootstrap Jaccard                | [04-evaluation/bootstrap-jaccard.md](./04-evaluation/bootstrap-jaccard.md)                 |
| Calibration / Brier score        | [04-evaluation/calibration-and-brier.md](./04-evaluation/calibration-and-brier.md)         |
| Calibration decay (monitoring)   | [06-monitoring/calibration-decay.md](./06-monitoring/calibration-decay.md)                 |
| Class imbalance                  | [02-data/class-imbalance.md](./02-data/class-imbalance.md)                                 |
| Cold start                       | [03-modeling/cold-start.md](./03-modeling/cold-start.md)                                   |
| Confusion matrix                 | [04-evaluation/confusion-matrix.md](./04-evaluation/confusion-matrix.md)                   |
| Constraint violation rate        | [06-monitoring/constraint-violation-rate.md](./06-monitoring/constraint-violation-rate.md) |
| Cost asymmetry                   | [01-framing/cost-asymmetry.md](./01-framing/cost-asymmetry.md)                             |
| Coverage and diversity           | [04-evaluation/coverage-and-diversity.md](./04-evaluation/coverage-and-diversity.md)       |
| Data audit                       | [02-data/data-audit.md](./02-data/data-audit.md)                                           |
| Deployment gate                  | [05-deployment/deployment-gate.md](./05-deployment/deployment-gate.md)                     |
| Dimensionality reduction         | [03-modeling/dimensionality-reduction.md](./03-modeling/dimensionality-reduction.md)       |
| Drift types                      | [06-monitoring/drift-types.md](./06-monitoring/drift-types.md)                             |
| Elbow method                     | [04-evaluation/elbow-method.md](./04-evaluation/elbow-method.md)                           |
| Feature framing                  | [02-data/feature-framing.md](./02-data/feature-framing.md)                                 |
| Hard vs soft constraints         | [07-governance/hard-vs-soft-constraints.md](./07-governance/hard-vs-soft-constraints.md)   |
| HITL (human-in-the-loop)         | [07-governance/hitl-patterns.md](./07-governance/hitl-patterns.md)                         |
| Horizon and ceiling              | [01-framing/horizon-and-ceiling.md](./01-framing/horizon-and-ceiling.md)                   |
| Hyperparameter sweeps            | [03-modeling/hyperparameter-sweeps.md](./03-modeling/hyperparameter-sweeps.md)             |
| Inheritance vs greenfield        | [01-framing/inheritance-vs-greenfield.md](./01-framing/inheritance-vs-greenfield.md)       |
| K selection (elbow)              | [04-evaluation/elbow-method.md](./04-evaluation/elbow-method.md)                           |
| Leakage                          | [02-data/leakage.md](./02-data/leakage.md)                                                 |
| Naive baselines                  | [03-modeling/naive-baselines.md](./03-modeling/naive-baselines.md)                         |
| Operational ceiling              | [01-framing/horizon-and-ceiling.md](./01-framing/horizon-and-ceiling.md)                   |
| Optimization families            | [03-modeling/optimization-families.md](./03-modeling/optimization-families.md)             |
| PDPA basics                      | [07-governance/pdpa-basics.md](./07-governance/pdpa-basics.md)                             |
| Population (framing)             | [01-framing/target-and-population.md](./01-framing/target-and-population.md)               |
| PR curve                         | [04-evaluation/pr-curve.md](./04-evaluation/pr-curve.md)                                   |
| Pre-registered floors            | [04-evaluation/pre-registered-floors.md](./04-evaluation/pre-registered-floors.md)         |
| Precision@k                      | [04-evaluation/precision-at-k.md](./04-evaluation/precision-at-k.md)                       |
| Proxy for protected class        | [02-data/proxy-for-protected-class.md](./02-data/proxy-for-protected-class.md)             |
| PSI (Population Stability Index) | [06-monitoring/psi.md](./06-monitoring/psi.md)                                             |
| Recommender families             | [03-modeling/recommender-families.md](./03-modeling/recommender-families.md)               |
| Retrain rules                    | [06-monitoring/retrain-rules.md](./06-monitoring/retrain-rules.md)                         |
| ROC-AUC                          | [04-evaluation/roc-auc.md](./04-evaluation/roc-auc.md)                                     |
| Rollback patterns                | [05-deployment/rollback-patterns.md](./05-deployment/rollback-patterns.md)                 |
| Scope (target and population)    | [01-framing/target-and-population.md](./01-framing/target-and-population.md)               |
| Segment membership churn         | [06-monitoring/segment-membership-churn.md](./06-monitoring/segment-membership-churn.md)   |
| Shadow prices                    | [07-governance/shadow-prices.md](./07-governance/shadow-prices.md)                         |
| Shadow / staging / promotion     | [05-deployment/shadow-staging-promotion.md](./05-deployment/shadow-staging-promotion.md)   |
| Silhouette score                 | [04-evaluation/silhouette.md](./04-evaluation/silhouette.md)                               |
| Stability protocols              | [03-modeling/stability-protocols.md](./03-modeling/stability-protocols.md)                 |
| Supervised families              | [03-modeling/supervised-families.md](./03-modeling/supervised-families.md)                 |
| Target (framing)                 | [01-framing/target-and-population.md](./01-framing/target-and-population.md)               |
| Unsupervised families            | [03-modeling/unsupervised-families.md](./03-modeling/unsupervised-families.md)             |
