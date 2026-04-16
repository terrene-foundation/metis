<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Rubric — Student Reference

Student-readable rubric for the 60% journal-grade layer. Full grader behaviour is in `rubric-grader.md`; this file is the student-facing cheat sheet.

Scores are 0, 2, or 4 per dimension. 1 and 3 do not exist — the rubric forces a binary-plus-evidence choice. Cohort-average target: >= 3.0.

## 1. The five dimensions (anchors from `canonical-values.md` §9)

| #   | Dimension                 | 0 (absent)                   | 2 (partial)               | 4 (complete)                                                  |
| --- | ------------------------- | ---------------------------- | ------------------------- | ------------------------------------------------------------- |
| D1  | Harm framing              | No stakeholders named        | Names one cost            | Quantifies asymmetry in named dollars ($40 vs $12 = 3.3:1)    |
| D2  | Metric -> cost linkage    | Metric chosen without reason | Reason named              | Reason is a dollar figure or dollar-equivalent                |
| D3  | Trade-off honesty         | Picks winner, ignores loser  | Names what was sacrificed | Quantifies the sacrifice ("lost 0.8% MAPE", "$0.53/km delta") |
| D4  | Constraint classification | Unclear hard / soft          | Labelled correctly        | Penalty (in dollars) + reasoning included                     |
| D5  | Reversal condition        | "If data changed"            | Names a signal            | Names signal + threshold + duration window (no bare rules)    |

## 2. Worked 4/4 and 1/4 example per dimension

See `journal/_examples.md` for the full per-dimension pair. Each uses the Northwind numbers from `specs/business-costs.md`:

- **D1**: 4/4 names the $40 / $12 = 3.3:1 ratio and the Ops Manager stakeholder. 1/4 says "forecasting so Northwind can run better".
- **D2**: 4/4 weights MAPE by $40 under / $12 over and translates accuracy to ~$4,200/week. 1/4 says "MAPE because it's standard".
- **D3**: 4/4 cites the chosen run ID and quantifies sacrifice at ~$0.53/km delta. 1/4 says "picked Gradient Boosting because it was top of the leaderboard".
- **D4**: 4/4 re-classifies overtime as hard post `union-cap` with >$10,000 compliance exposure. 1/4 "raised the penalty from $45 to $200/hour".
- **D5**: 4/4 names PSI >= 0.25, training-window p95 threshold, 3 consecutive daily checks, human-in-the-loop. 1/4 "if data changes or MAPE > 15%, retrain automatically".

## 3. Applicability matrix (from `rubric-grader.md` §1.3)

Not every dimension applies to every phase. The grader averages only the applicable dimensions (denominator = applicable-dimension count × 4).

| Phase | D1  | D2  | D3  | D4  | D5  |
| ----- | --- | --- | --- | --- | --- |
| 1     | X   | X   | —   | —   | X   |
| 2     | —   | —   | X   | —   | X   |
| 5     | —   | X   | X   | —   | X   |
| 6     | X   | X   | X   | —   | X   |
| 7     | X   | —   | X   | —   | X   |
| 8     | —   | —   | —   | X   | X   |
| 9     | —   | —   | —   | —   | —   |
| 10    | X   | X   | X   | —   | —   |
| 11    | —   | —   | —   | X   | —   |
| 12    | —   | —   | X   | X   | X   |
| 13    | —   | —   | —   | —   | X   |

## 4. Anti-patterns the rubric catches

From `rubric-grader.md` §5:

- **"If data changed"** — always 0/4 on D5. The canonical anti-pattern.
- **"MAPE because it's standard"** — 0/4 on D2. Metrics must be tied to dollars.
- **"Solver said feasible, accept"** — 1/4 on D3. Name the sacrifice.
- **"Union-cap is still soft"** (post-injection) — 1/4 on D4. Contractual constraints are not price-able.
- **"Auto-retrain when MAPE > 15%"** — blocked by `rules/agent-reasoning.md`. D5 rewards a human-in-the-loop justification.

## 5. Combined score

```
total = 0.60 * journal_score + 0.40 * product_score
```

`journal_score` = mean of per-entry mean-across-applicable-dimensions scores, scaled to [0, 1]. `product_score` is the sum of passed endpoint weights (5 endpoints × 8%), scaled to [0, 1]. Pass threshold: total >= 0.60.

## Related specs

- `canonical-values.md` §9 — single source of truth for the five anchors.
- `rubric-grader.md` §1 — full grader detail, applicability matrix origin.
- `journal/_examples.md` — worked 4/4 and 1/4 pair per dimension.
- `decision-journal.md` §2 — journal entry schema this rubric scores against.
