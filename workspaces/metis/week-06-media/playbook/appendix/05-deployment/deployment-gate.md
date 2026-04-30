<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Deployment Gate

> **One-line hook:** The formal PASS/FAIL decision before a model moves to production — based on pre-registered floors, not gut feel.

## The gist

The **deployment gate** is Phase 8 of the Playbook. It is the moment where you decide, with written criteria, whether a model is ready for production. "It looks good" is not a gate. "It passed all three pre-registered floors from Phase 6 and the Phase 7 red-team found no findings tagged 're-do'" is a gate.

A well-formed deployment gate has four elements:

**1. PASS/FAIL floors** (from Phase 6): Each metric the model must clear to ship. For USML segmentation: silhouette ≥ your pre-registered value, bootstrap Jaccard ≥ your pre-registered value, all segments have distinct named actions. For SML classifiers: AUC > baseline, Brier score within tolerance, confusion matrix cost ≤ your declared maximum.

**2. Red-team clearance** (from Phase 7): Any finding tagged "re-do" blocks shipping. Findings tagged "mitigate" require a documented action before shipping. Findings tagged "accept" are accepted risks — documented, not ignored.

**3. Monitoring commitment** (forward-looking): What monitoring fires after shipping? Segmentation drift signal + cadence, classifier calibration decay + cadence, allocator constraint-violation rate + cadence. These are declared in Phase 8, not Phase 13. Phase 13 sets the thresholds; Phase 8 commits to running the monitoring at all.

**4. Rollback channel**: If the model starts producing bad outputs in production, how do you roll back? For Arcadia: the scaffold's registry system supports reverting to the previous registered model version. The rollback plan names the trigger (what signal causes rollback), the action (which endpoint/command), and the owner (who pulls the lever — E-com Ops Lead).

For Arcadia: each sprint ends with a Phase 8 gate. Sprint 1 gates the segmentation, Sprint 2 gates the two classifiers. The Phase 8 journal entry is the written record that the gate ran.

## Why it matters for ML orchestrators

Skipping the deployment gate means you ship based on "Phase 4 looked good" without checking stability (Phase 6–7) or declaring rollback. In production, when something goes wrong, there's no rollback plan and no pre-committed signal for "this is bad enough to pull". Phase 8 closes both gaps.

## Common confusions

- **"We'll monitor in Phase 13 — that's the real gate"** — Phase 13 sets the drift thresholds for live monitoring. Phase 8 is the gate before you go live at all. Both are required.
- **"The model beat the baseline, so it's ready"** — Beating the baseline is necessary but not sufficient. The gate also requires red-team clearance and a declared rollback channel.

## When you'll hit it

Used in: Phase 8 (Deployment Gate — runs at end of Sprint 1 and Sprint 2), workflow-03 (Sprint 1 boot sets the expectation of a Phase 8 gate at the end)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Sculley et al., "Hidden Technical Debt in Machine Learning Systems" — on the cost of missing deployment infrastructure
- Breck et al., "The ML Test Score: A Rubric for ML Production Readiness" — systematic gate criteria
