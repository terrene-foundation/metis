<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Cost Asymmetry

> **One-line hook:** The two ways of being wrong rarely cost the same — and the ratio between them determines your threshold before you look at a single result.

## The gist

Every model can be wrong in two directions. A churn classifier can miss a customer who was about to leave (false negative: you lost a customer you could have saved) or it can flag a loyal customer as at-risk and waste retention spend on them (false positive: you spent $3 on someone who would have stayed anyway). These two errors cost different amounts — and the ratio between them is what should drive your threshold decision in Phase 6.

Cost asymmetry is always stated in dollars, per error, from a named source. For Arcadia:

- Wrong-segment campaign: **$45 per customer** (false positive on segment assignment — you send the wrong offer)
- Per-touch cost: **$3 per customer** (false positive on churn prediction — you touch someone who wasn't churning)
- Churn miss: **$120 CAC to reacquire** (false negative on churn prediction — the customer left and now you have to win them back)

The churn ratio is 120:3 = 40:1. That means the model should be very aggressive about flagging churn risk, even at the cost of more false positives, because missing a churner is 40 times more expensive than a wasted touch. Without this ratio, picking a threshold defaults to 0.5 — the silent killer that ignores the asymmetry entirely.

Asymmetry is written down before you see the model's output. Once you know the AUC, the temptation to let the leaderboard winner's natural threshold stand is very strong. Pre-registration closes that door.

## Why it matters for ML orchestrators

The threshold is your call, not the algorithm's. The algorithm outputs a score; you decide what score is "high enough to act". Cost asymmetry is the only honest anchor for that decision. Without it, you are picking a threshold based on what feels right — which is what the rubric scores 0/4.

## Common confusions

- **"The default threshold is 0.5 — isn't that fair?"** — It is fair to neither error type; it treats false positives and false negatives as equally costly, which almost never reflects reality. Use the cost ratio to compute the right threshold.
- **"The dollar figures are estimates anyway, so precision doesn't matter"** — Exact figures from `PRODUCT_BRIEF.md §2` are the citation standard. If you cannot quote the row, you cannot defend the threshold.

## When you'll hit it

Used in: Phase 1 (Frame — declare the asymmetry upfront), Phase 6 (Metric + Threshold — use it to set the threshold), Phase 11 (Constraints — penalty calibration for soft constraints)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Provost & Fawcett, "Data Science for Business" ch. 7 — cost-sensitive classification
- Flach, "Machine Learning" ch. 8 — ROC and cost curves
