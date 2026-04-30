<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# HITL Patterns

> **One-line hook:** Human-in-the-loop — where in the ML decision chain a human must make a call, rather than the system acting automatically.

## The gist

**HITL (Human-in-the-Loop)** describes the places in an ML system where a human decision is required before the system acts. Arcadia's ML system has several HITL gates by design:

**Phase 8 (Deployment Gate)**: A human — the product owner or sprint lead — must review the deployment gate checklist and approve promotion. The system does not auto-promote a model that passes all floors; it waits for human sign-off. This gate catches cases where the floors passed but something still feels wrong (an unusual segment profile, a PR curve shape that looks suspicious).

**Phase 13 (Retrain trigger)**: When a drift monitoring signal crosses the threshold for the sustained duration window, the system sends an alert. A human (E-com Ops Lead for segmentation, CX Lead for classifiers) decides whether to retrain. "Auto-retrain on trigger" is blocked because:

- The trigger might be seasonal (Black Friday spike — don't retrain)
- The trigger might be a one-time external shock (a competitor closed — wait and see)
- Retraining costs time and compute; the human decides if the cost is justified

**Phase 12 (Solver Acceptance)**: The LP produces a plan. A human reviews it for pathologies (concentration, dead campaigns, sensitivity flip) before the plan executes. Even a mathematically optimal plan can be operationally unacceptable.

HITL is not a limitation — it's a design choice. Fully automated systems are faster but blind to context. HITL gates are the places where context matters enough that automation would be reckless.

For Arcadia, every retrain rule must explicitly state: "signal crosses threshold for N consecutive periods → **alert E-com Ops Lead** → human decides." The word "auto-retrain" in any retrain rule is a red flag in the Phase 13 rubric.

## Why it matters for ML orchestrators

HITL gates are where you, as the orchestrator, are most valuable. The system generates the alert; the human provides the judgment. Understanding which decisions require HITL (retrain, rollback, PDPA classification, deployment gate) vs which are fully automated (drift metric computation, model scoring, plan optimisation) is the Trust Plane / Execution Plane split applied to MLOps.

## Common confusions

- **"HITL slows down the ML system"** — It slows down automatic actions; it doesn't slow down the system's monitoring or computation. The alert fires immediately; the human decision adds hours, not weeks.
- **"HITL means humans do everything"** — HITL means humans decide at specific gates. Between gates, the system runs fully automatically. The goal is the minimum number of HITL gates needed to prevent the most costly automated mistakes.

## When you'll hit it

Used in: Phase 8 (Deployment Gate — HITL approval for promotion), Phase 13 (Drift — retrain trigger requires human decision), Phase 12 (Solver Acceptance — plan review before execution), workflow-06 (Sprint 4 MLOps boot)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Amershi et al., "Software Engineering for Machine Learning: A Case Study" — HITL in production ML
- Monarch, "Human-in-the-Loop Machine Learning" — comprehensive HITL design patterns
