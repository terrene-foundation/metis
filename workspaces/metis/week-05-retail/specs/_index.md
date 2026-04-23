<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Week 5 Retail — Specs Index

Per `rules/specs-authority.md`, this is the single source of domain truth for Week 5. Every phase reads the relevant spec before acting and updates it when the truth changes.

| File                   | Domain              | Description                                                            |
| ---------------------- | ------------------- | ---------------------------------------------------------------------- |
| `business-costs.md`    | Cost model          | $18 / $14 / $45 / $3 / $220 / $8 / peak Nov–Dec — cited by every phase |
| `api-surface.md`       | API                 | Segment / Recommend / Drift endpoint contracts                         |
| `scaffold-manifest.md` | Layout              | Every file the scaffold ships and its state                            |
| `rubric.md`            | Grading             | 5-dimension scoring anchors (0 / 2 / 4)                                |
| `ai-verify.md`         | Red-team dimensions | Transparency / Robustness / Safety (Fairness deferred to Week 7)       |
| `success-criteria.md`  | Grader              | Binary shipped-product checks (dashboard, endpoints, journal.pdf)      |

Specs update at first instance of domain change. No batched updates. Deviations from spec require explicit acknowledgement (see `rules/specs-authority.md` MUST Rule 6).
