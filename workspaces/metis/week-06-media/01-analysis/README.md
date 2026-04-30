<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# `/analyze` Output — Week 6 Media

`/analyze` is short tonight (~10 minutes). The product is pre-built. Your only job in this phase is to declare, in writing, the boundary between what the scaffold has already committed to and what remains for the 14 Playbook phases to decide.

## Files produced here

- `failure-points.md` — 5–8 ways the moderation product could fail in production. Each one maps to a later Playbook phase. If you cannot name a Playbook phase that catches it, you have discovered a gap in the Playbook (flag to the instructor).
- `assumptions.md` — what the pre-built baseline already assumes. ResNet-50 frozen backbone (not partial-fine-tune, not full-fine-tune). BERT-base (not RoBERTa-large, not domain-specific). Early-fusion as the fusion default. Drift reference drawn from the training window (pre-election cycle). Every assumption you accept tonight is a decision by omission.
- `decisions-open.md` — the inverse: what remains open for you to decide in Sprints 1–4. Per-class thresholds × 10 (5 image + 5 text), fusion architecture choice, IMDA hard-line stance, queue allocator constraints, three retrain rules at three cadences.

## Guiding questions

1. **What does the pre-built baseline commit to?** Read `/moderate/image/leaderboard`, `/moderate/text/leaderboard`, `/moderate/fusion/score`, `/drift/status/{image,text,fusion}_moderator`. What numbers and architectures are already baked in?
2. **What would a hostile Head of T&S ask about this baseline?** (Hint: she will ask about per-class recall on hate-speech and CSAM-adjacent first.)
3. **What would hostile Legal Counsel ask?** (Hint: IMDA Online Safety Code, audit trail, the 60-second mandatory-review SLA on CSAM-adjacent.)
4. **What would a hostile Reviewer Ops Lead ask?** (Hint: queue depth, $22/min reviewer cost, what happens at peak election-cycle traffic.)
5. **Which of the five Trust Plane decision moments from `PRODUCT_BRIEF.md §"The five Trust Plane decision moments"` are already resolved, and which are still yours?**

## Gate to `/todos`

Your `failure-points.md` must name at least 5 distinct failure modes, each mapped to the Playbook phase that catches it. Fewer than 5, or any phase left unmapped → `/analyze` re-runs. No `/todos` start until the gate passes.
