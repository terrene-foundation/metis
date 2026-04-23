<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Horizon and Ceiling

> **One-line hook:** How far ahead the model predicts (horizon) and how many outputs your team can act on (ceiling) — both named in units before any code runs.

## The gist

**Horizon** is the window over which the model's prediction is meaningful, always named in concrete units: days, weeks, months. "Forecast demand" is not a horizon. "Forecast demand per SKU per day for the next 14 days" is. Why does this matter? Because a model trained to predict 14-day demand will be systematically wrong if you use it to plan a quarterly campaign. Horizon sets the shelf life of every prediction the model produces.

Horizon also interacts with seasonality in a way that bites in production. An 18-month training window that includes Black Friday will learn Black Friday patterns as if they apply year-round — and a segmentation model trained on peak-season data will produce peak-season segments that confuse marketing in March. Arcadia's Black Friday / Year-End spike (Nov–Dec) is explicitly excluded from the drift baseline for this reason.

**Operational ceiling** is how many distinct outputs your downstream team can actually act on in parallel. A 4-person marketing team running 5-campaign sprints cannot suddenly run 12-segment campaigns. The ceiling is set by the human role who owns the downstream process — not by what the model can produce. Naming the ceiling with a role owner ("CMO owns the 6-segment ceiling") turns it from a vague aspiration into a real constraint. An unowned ceiling evaporates under quarterly planning pressure.

## Why it matters for ML orchestrators

These two numbers — horizon and ceiling — are the two structural constraints that every later phase anchors to. If Phase 4 produces a K=9 clustering and your ceiling is 6, one of those values is wrong. Settle the ceiling in Phase 1 or it gets settled for you by what the model happens to output.

## Common confusions

- **"Near-term" or "recent" is good enough for now"** — No. Name the units. "Next 30 days" vs "next 90 days" is the difference between a model that re-trains monthly and one that re-trains quarterly; that difference compounds across the entire MLOps Sprint.
- **"The team can handle more segments if the model is good"** — The ceiling is downstream capacity, not model quality. Good segments that nobody can action are waste.

## When you'll hit it

Used in: Phase 1 (Frame), Phase 6 (Metric + Threshold — K selection anchors to ceiling), Phase 8 (Deployment Gate — monitoring cadence anchors to horizon)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Makridakis, Spiliotis, Assimakopoulos, "The M4 Competition" — on forecast horizon choices and their consequences
- Provost & Fawcett, "Data Science for Business" ch. 2 — on operational constraints as model design inputs
