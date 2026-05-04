<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Week 7 Manufacturing — Specs Index

Per `rules/specs-authority.md`, this is the single source of domain truth for Week 7. Every phase reads the relevant spec before acting and updates it when the truth changes.

| File                   | Domain     | Description                                                                |
| ---------------------- | ---------- | -------------------------------------------------------------------------- |
| `business-costs.md`    | Cost model | $4,200 / $85 / $12,000 / $50,000 / $1,000,000 / $35 — cited by every phase |
| `api-surface.md`       | API        | Vision / PredMaint / RL / Agent / Drift / Queue endpoint contracts         |
| `compliance-floors.md` | Compliance | WSH safety floor + MOM shadow mandate + IPC-A-610 Class 3 contract terms   |

Specs update at first instance of domain change. No batched updates. Deviations from spec require explicit acknowledgement (see `rules/specs-authority.md` MUST Rule 6).
