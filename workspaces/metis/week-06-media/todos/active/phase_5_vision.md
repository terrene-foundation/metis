<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 5 — Implications (Vision)

**Sprint:** Sprint 1 · Vision/CNN · See
**Playbook phase:** Phase 5 — Implications
**Trust-plane decision:** Pick the CNN family for the image moderator and defend the pick in dollars (FN $320 / FP $15 cost-balanced, IMDA $1M ceiling acknowledged separately) AND on per-class evidence — NOT macro-F1 alone (`failure-points.md` F1.1).
**Paste prompt:** `playbook/phase-05-implications.md` §1 (Vision branch)
**Evaluation checklist:** `playbook/phase-05-implications.md` §2
**Endpoints touched:** read-only — `GET /moderate/image/leaderboard`. (No promotion yet — Phase 8 owns promotion.)
**Skeleton to copy:** `journal/skeletons/phase_5_implications.md` → `journal/phase_5_vision.md`
**Acceptance criterion:** `journal/phase_5_vision.md` names the chosen family, dollar defense uses only `PRODUCT_BRIEF.md §2` numbers, per-class CSAM-adjacent recall called out explicitly, calibration finding (Brier-pass / Brier-fail per class) captured for the chosen family.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made (journal entry drafted)
- [ ] Journal entry cites at least one $ figure from `PRODUCT_BRIEF.md §2`
- [ ] Moved to `todos/completed/` on human approval
