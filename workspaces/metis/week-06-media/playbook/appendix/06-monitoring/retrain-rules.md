<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Retrain Rules

> **One-line hook:** The specific signal + threshold + duration window + human decision that determines when to retrain a model — written down before the model goes live.

## The gist

A **retrain rule** is not "retrain when performance drops." That is not a rule; it is a non-commitment. A proper retrain rule has four components:

1. **Signal**: the specific metric you watch (segment-membership churn rate, Brier score, AUC, infeasibility rate, PSI for a named feature).
2. **Threshold**: the value that triggers review, grounded in historical variance — not a round number. "Segment churn > 15% because the rolling monthly variance has its 95th percentile at 12%" is a threshold. "Segment churn > 15% because it feels big" is not.
3. **Duration window**: how long the signal must exceed the threshold before triggering action. One bad week does not trigger a retrain. "Signal exceeds threshold for 3 consecutive monitoring periods" does. Duration windows prevent over-reacting to noise.
4. **Human decision gate**: the retrain trigger produces a notification; a named human decides whether to retrain. "Auto-retrain on trigger" is BLOCKED for production models. The human gate is what catches seasonal anomalies (Black Friday spike ≠ drift) and external shocks (a competitor's store closure causes a temporary uplift — not a reason to retrain).

For Arcadia Phase 13, you write three retrain rules — one per model:

- **Segmentation**: monthly segment-membership churn signal, with Nov–Dec explicitly excluded from the baseline.
- **Churn classifier**: weekly Brier score + AUC signals (dual trigger — both must hold, or either triggers review depending on your decision).
- **Allocator**: daily infeasibility rate + ops override rate signals.

Each rule is a separate journal sub-section in `journal/phase_13_retrain.md`.

## Why it matters for ML orchestrators

The retrain rule is where the Trust Plane has the most leverage after shipping. A poorly written rule (missing duration window, missing seasonal exclusion, missing human gate) produces either over-retraining (chasing noise, creating instability) or under-retraining (missing real drift until a stakeholder notices the model is producing wrong outputs and asks why nobody caught it).

## Common confusions

- **"Thresholds should be round numbers"** — Round numbers signal a guess. Ground the threshold in measured historical variance: "the 95th percentile of monthly segment churn in the training window was 12%, so the trigger is 15%."
- **"Human gate slows down response"** — Human gate prevents auto-retraining during Black Friday, Chinese New Year, or a one-time external shock. The cost of a 24-hour human decision is much lower than the cost of a model retrained on holiday data serving the wrong segments in January.

## When you'll hit it

Used in: Phase 13 (Drift — the entire phase is writing these three rules), Phase 8 (Deployment Gate — monitoring commitment declared here, thresholds set in Phase 13), workflow-06 (Sprint 4 MLOps boot)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Shankar et al., "Operationalizing Machine Learning: An Interview Study" — on retrain decisions in practice
- Ribeiro et al., "Beyond Accuracy: Behavioral Testing of NLP Models with CheckList" — on monitoring production model behaviour
