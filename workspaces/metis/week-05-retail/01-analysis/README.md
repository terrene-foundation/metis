<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# `/analyze` Output — Week 5 Retail

`/analyze` is short tonight (~10 minutes). The product is pre-built. Your only job in this phase is to declare, in writing, the boundary between what the scaffold has already committed to and what remains for the 14 Playbook phases to decide.

## Files produced here

- `failure-points.md` — 5–8 ways the retail product could fail in production. Each one maps to a later Playbook phase. If you cannot name a Playbook phase that catches it, you have discovered a gap in the Playbook (flag to the instructor).
- `assumptions.md` — what the pre-built baseline already assumes. K=3. Content-based recommender (not collaborative, not hybrid). Drift reference drawn from the training window (pre-wellness launch). Every assumption you accept tonight is a decision by omission.
- `decisions-open.md` — the inverse: what remains open for you to decide in Sprints 1–3. K, segment names, per-segment actions, recommender strategy, cold-start disposition, PDPA constraint, drift thresholds.

## Guiding questions

1. **What does the pre-built baseline commit to?** Read `/segment/baseline`, `/recommend/config`, `/drift/status/customer_segmentation`. What numbers are already baked in?
2. **What would a hostile CMO ask about this baseline?** (Hint: she will ask about K=3 first.)
3. **What would a hostile legal counsel ask?** (Hint: postal district, age band, under-18 browse data.)
4. **What would a hostile ops manager ask?** (Hint: how will you know when it breaks?)
5. **Which of the five Trust Plane decision moments from `PLAYBOOK.md §"The five Trust Plane decision moments"` are already resolved, and which are still yours?**

## Gate to `/todos`

Your `failure-points.md` must name at least 5 distinct failure modes, each mapped to the Playbook phase that catches it. Fewer than 5, or any phase left unmapped → `/analyze` re-runs. No `/todos` start until the gate passes.
