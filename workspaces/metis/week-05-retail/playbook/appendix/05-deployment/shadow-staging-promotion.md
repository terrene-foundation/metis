<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Shadow, Staging, and Promotion

> **One-line hook:** Three steps from a trained model to a live production model — and why skipping them is how models go wrong quietly.

## The gist

In production ML, models don't jump directly from training to serving all live traffic. A disciplined promotion path has three stages:

**Shadow mode**: The new model runs in parallel with the existing system, receiving the same inputs, but its outputs are not used to make real decisions. You can compare the new model's recommendations against the incumbent's in real time — same customers, same moment — without any risk to live users. Shadow mode is where you catch "the model trained fine but behaves oddly at inference time" bugs.

**Staging (canary / limited release)**: The new model serves a small fraction of real traffic — maybe 5–10% of customers — while the existing model serves the rest. You measure real-world outcomes (click-through, conversion, complaint rate) on the canary group vs the control group. Staging is where you catch "the model's offline metrics looked good but live performance is different" failures.

**Promotion**: The new model takes over all traffic. The previous model is archived (not deleted — you need it for rollback). Promotion is gated on: canary metrics better than incumbent, no error rate spike, no complaint rate spike, rollback ready.

For Arcadia: the scaffold's registry system at `/segment/registry`, `/predict/registry`, and `/recommend/registry` manages this promotion flow. The Phase 8 gate records the registry transition (from shadow to staging to promoted). In a 3.5-hour workshop, the scaffold compresses this to: train → register → promote, without a live canary period. But the Phase 8 journal entry names the stages and declares what would trigger rollback if this were a real production deployment.

## Why it matters for ML orchestrators

Promotion without shadow and staging is the most common path to a public ML incident. The model behaved perfectly in every offline test and produced nonsense in production — because production has edge cases (new SKUs, holiday spikes, data pipeline latency) that offline data doesn't capture.

## Common confusions

- **"Shadow mode doubles compute cost"** — Yes. The cost is justified by catching inference-time bugs before they affect live users.
- **"Staging is optional for internal tools"** — Staging is how you measure real-world delta. Even internal tools have users; a misfiring segmentation silently poisons every downstream campaign.

## When you'll hit it

Used in: Phase 8 (Deployment Gate — records the registry transition), workflow-03, workflow-04 (sprint boots reference the registry as the deployment mechanism)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Kleppmann, "Designing Data-Intensive Applications" ch. 1 — on rolling upgrades and canary deployments
- Sculley et al., "Machine Learning: The High-Interest Credit Card of Technical Debt" — on deployment infrastructure debt
