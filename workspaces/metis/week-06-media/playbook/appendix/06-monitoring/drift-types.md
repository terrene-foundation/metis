<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Drift Types

> **One-line hook:** Three ways a model can start lying over time — feature drift, label drift, and concept drift — each requiring a different monitoring signal.

## The gist

A model trained on last year's data is a description of last year's customers. As the world changes, the model's description can become wrong in three distinct ways:

**Feature drift** (also called data drift or covariate shift): The distribution of input features changes. Example: Arcadia's customer base skews younger after a mobile app launch — the age distribution shifts. The model was trained on an older distribution; it now receives inputs that look different from training. PSI (Population Stability Index) measures this.

**Label drift** (also called prior probability shift): The rate at which the target event occurs changes. Example: churn rate rises from 5% to 12% during an economic downturn. The model was calibrated for 5% churn; its probability outputs are now systematically wrong. Calibration decay and Brier score drift detect this.

**Concept drift**: The relationship between features and the target changes. Example: customers who previously had high recency scores were loyal; now high recency means they're browsing competitors before leaving. The feature "high recency" used to predict "loyal"; now it predicts "about to churn". The model's learned weights are wrong. AUC decay is one signal, but concept drift is the hardest to detect early.

For Arcadia Sprint 4 (Phase 13), each of the three models monitors a different drift signal:

- Segmentation: **segment-membership churn** (effectively a structural drift signal — are customers moving between segments at unusual rates?)
- Churn classifier: **calibration decay + AUC decay** (label drift + concept drift combined signal)
- Allocator: **constraint-violation rate** (not feature/label drift per se, but a proxy for upstream drift propagating into the optimization layer)

## Why it matters for ML orchestrators

Knowing the drift type tells you what to do about it. Feature drift → retrain on newer data. Label drift → recalibrate. Concept drift → investigate the causal change (did market conditions shift? did a competitor launch?) before retraining, because retraining on new data that reflects the new relationship is the fix, but you need to understand the change first.

## Common confusions

- **"High PSI means the model is wrong"** — PSI measures feature drift; the model may still perform well if the concept relationship hasn't changed. Always check both feature drift and prediction performance.
- **"One drift signal covers all three models"** — Each model drifts on its own cadence and signal type. Three models = three monitoring rules.

## When you'll hit it

Used in: Phase 13 (Drift — set the three monitoring rules), workflow-06 (Sprint 4 MLOps boot)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Gama et al., "A Survey on Concept Drift Adaptation" — comprehensive concept drift survey
- Klinkenberg & Joachims, "Detecting Concept Drift with Support Vector Machines"
