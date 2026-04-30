<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 6 — Metric + Threshold × 5 image classes (Vision)

**Sprint:** Sprint 1 · Vision/CNN · See
**Playbook phase:** Phase 6 — Metric + Threshold (per-class × 5)
**Trust-plane decision:** Set the auto-remove threshold for each of the 5 image classes — `nsfw`, `violence`, `weapons`, `csam_adjacent`, `safe`. Four are cost-balanced under the $320 FN / $15 FP asymmetry; `csam_adjacent` is structurally HARD at the IMDA-mandated 0.40 floor (`ml_context.py::CSAM_ADJACENT_HARD_FLOOR`). (Decision moment 2 of 5, image half.)
**Paste prompt:** `playbook/phase-06-metric-threshold.md` §1 (Sprint 1 / Vision branch)
**Evaluation checklist:** `playbook/phase-06-metric-threshold.md` §2
**Endpoints touched:** `GET /moderate/image/threshold` (read defaults); `POST /moderate/image/threshold` (per class — refuses CSAM < 0.40 with 422); read PR-curve evidence from `GET /moderate/image/leaderboard`.
**Skeleton to copy:** `journal/skeletons/phase_6_metric_threshold.md` → `journal/phase_6_vision.md`
**Acceptance criterion:** `journal/phase_6_vision.md` shows PR curve at K candidate thresholds for each of 5 classes, cost-balanced minimum computed per class with arithmetic shown, `csam_adjacent` capped at 0.40 with regulatory citation (NOT cost-balanced), 5 successful `POST /moderate/image/threshold` calls reflected in `image_thresholds.json` and `image_registry.json`.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — 5 thresholds POSTed
- [ ] Journal entry quotes $320 / $15 / $1,000,000 from `PRODUCT_BRIEF.md §2`
- [ ] Moved to `todos/completed/` on human approval
