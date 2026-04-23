<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Pre-Registered Floors

> **One-line hook:** Writing down your pass/fail thresholds before you see the results — the discipline that separates honest evaluation from moving the goalposts.

## The gist

A **floor** is a pass/fail line: "silhouette must be at least 0.25", "bootstrap Jaccard must be at least 0.80", "conversion classifier AUC must exceed 0.75". A floor is only honest if you wrote it down before you saw the result.

**Pre-registration** is the act of writing the floor in your journal before running the test. It is the difference between measuring and moving the goalposts.

Without pre-registration, the sequence is:

1. Run the model.
2. See the result (e.g., silhouette = 0.31).
3. Decide "0.30 is the floor" because that's slightly below the result.
4. Announce that the model "passed".

That's not evaluation. That's narrative construction after the fact. It scores 1/4 on D2 (metric→cost linkage) in the rubric because there's no pre-committed anchor.

With pre-registration, the sequence is:

1. Write the floor in the journal (e.g., "silhouette ≥ 0.35") before running the model.
2. Run the model.
3. See the result (e.g., silhouette = 0.31).
4. Report that the model failed the floor.
5. Decide: revisit the floor with explicit rationale, or go back to Phase 4.

For Arcadia Phase 6 USML: you pre-register three floors — separation (silhouette), stability (bootstrap Jaccard), and actionability (each segment has a distinct named action) — in `journal/phase_6_usml.md` before you look at the Phase 4 leaderboard. The leaderboard then tells you which K values pass all three floors.

## Why it matters for ML orchestrators

Pre-registration is what makes you an honest evaluator rather than a cheerleader for your own model. The rubric scores this heavily because the course is teaching you a discipline that protects you from your own wishful thinking — and protects the business from shipping a model that was only tested against thresholds invented to justify the result.

## Common confusions

- **"Pre-registration is bureaucratic overhead"** — It takes three minutes per phase. It prevents entire sprints of work building on a model that quietly failed evaluation.
- **"If the model doesn't pass, I've failed"** — No. The model failing its pre-registered floor is correct evaluation. The failure is when you lower the floor to make the model pass.

## When you'll hit it

Used in: Phase 6 (Metric + Threshold — USML three floors pre-registered before seeing leaderboard; SML PR curve operating point pre-committed before seeing test results), Phase 8 (Deployment Gate — floors from Phase 6 are the gate criteria), Phase 7 (Red-Team — floors from Phase 6 are what the re-seed test compares against)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Simmons, Nelson & Simonsohn, "False-Positive Psychology" — the problem of flexible evaluation
- Open Science Collaboration, "Estimating the Reproducibility of Psychological Science" — why pre-registration matters
