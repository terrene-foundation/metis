<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# PR Curve

> **One-line hook:** The right instrument for picking a classification threshold on rare-positive problems — shows the precision/recall trade-off across every possible threshold.

## The gist

The **precision-recall curve** plots precision (of customers flagged, what fraction actually churned) against recall (of all customers who actually churned, what fraction did you flag) as the classification threshold moves from 0 to 1.

At a low threshold: you flag almost everyone, so recall is high (you catch nearly all churners) but precision is low (most flagged customers aren't actually churning — you're spending $3 per touch on non-churners).

At a high threshold: you only flag the most obvious churners, so precision is high (nearly every flagged customer is really churning) but recall is low (you miss many churners who weren't quite obvious enough — they leave and you pay $120 CAC to reacquire).

The cost asymmetry tells you where on this curve to land. For churn: missing a churner costs $120 (CAC), flagging a non-churner costs $3 (touch). The 40:1 ratio says you should accept lower precision (more false positives) to gain higher recall (fewer missed churners). Concretely: find the threshold on the PR curve where the expected cost per customer is minimised:

`Expected cost = (1 − recall) × $120 × P(churn) + (1 − precision) × $3 × P(flagged | not churn)`

The minimum of that expression is your operating threshold. That's what "cost-based threshold" means.

For Arcadia Sprint 2 Phase 6: you read the PR curve produced by Claude Code during the Phase 4 sweep, compute expected cost at several threshold candidates, and pick the threshold with the lowest expected cost. You write the threshold and the expected-cost computation in `journal/phase_6_sml.md` before approving the classifier.

## Why it matters for ML orchestrators

The PR curve converts a mathematical question (where do I set the threshold?) into a business decision (how much false-positive cost am I willing to pay for additional recall?). That's your call, not Claude Code's.

## Common confusions

- **"The best threshold is where precision = recall (F1)"** — F1 treats false positives and false negatives as equally costly. They almost never are. Use cost asymmetry, not F1.
- **"PR curve only matters for imbalanced datasets"** — It's most useful for rare-positive problems, but the principle applies whenever the two error types have different costs.

## When you'll hit it

Used in: Phase 6 (Metric + Threshold — SML variant; read the PR curve to set the threshold), Phase 7 (Red-Team — per-subgroup PR curves for bias check)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Saito & Rehmsmeier, "The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets"
- Provost & Fawcett, "Data Science for Business" ch. 7 — cost-sensitive threshold selection
