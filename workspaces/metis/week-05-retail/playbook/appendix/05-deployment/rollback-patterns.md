<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Rollback Patterns

> **One-line hook:** The pre-planned path from "something's wrong in production" back to the last known-good model — declared before shipping, not improvised after.

## The gist

A **rollback plan** answers three questions before you ship:

1. **What signal triggers rollback?** Not "if the model gets bad" — that's not actionable. A trigger must be specific: "churn classifier AUC on a weekly hold-out drops below 0.72 for two consecutive weeks" or "segmentation bootstrap Jaccard drops below 0.70 on the monthly re-cluster." Without a specific signal, the team debates whether things are "bad enough" while the model continues producing wrong outputs.

2. **What action constitutes rollback?** For Arcadia: the scaffold's registry has a `rollback` endpoint. Calling it reverts the live model to the previous registered version. The previous version must still be in the registry — if you delete it after promotion, rollback is impossible. The action must be documented: which command, which endpoint, who can authorise it.

3. **Who owns the decision to roll back?** Not "the ML team" — a named role. For Arcadia: the E-com Ops Lead owns the segmentation and drift monitoring; the CX Lead owns the classifier rollback. An unowned rollback decision becomes a political football during an incident.

For Arcadia Phase 8: the deployment gate journal entry declares the rollback trigger (from Phase 13's drift thresholds), the rollback action (which registry command), and the rollback owner (which stakeholder role). In Week 5, this is declarative — you're not building a pager — but the declaration is what the rubric checks.

**A common failure**: the team ships the model and archives the previous version to save storage. Three months later, the model drifts and rollback is needed. The previous version is gone. Now you must retrain from scratch — but your training data is also from three months ago, so you have neither a fast path nor a clean one.

## Why it matters for ML orchestrators

Rollback plans are written in Phase 8 when you are calm and the model is passing. They are executed in Phase 13 (or after) when you are under pressure and the model is failing. Writing the plan when calm is the institutional discipline that prevents improvised decisions under stress.

## Common confusions

- **"Rollback is the DevOps team's job"** — The ML team declares the trigger and the previous model version; DevOps automates the action. Saying "DevOps handles rollback" without declaring the trigger and owner is not a rollback plan.
- **"We won't need to roll back if we test thoroughly"** — Production has conditions offline testing doesn't. Rollback is insurance, not an admission of failure.

## When you'll hit it

Used in: Phase 8 (Deployment Gate — rollback plan is one of the four gate elements), Phase 13 (Drift — drift thresholds are the rollback triggers declared here)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Kim et al., "The DevOps Handbook" — rollback and deployment discipline
- Kleppmann, "Designing Data-Intensive Applications" ch. 1 — on maintaining backward compatibility and rollback
