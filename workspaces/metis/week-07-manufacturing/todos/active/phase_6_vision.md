<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 6 — Metric + Threshold × 4 vision classes (Vision) ★

**Sprint:** Sprint 1 · Vision QC · Transfer Learning · See
**Playbook phase:** Phase 6 — Metric + Threshold (per-class × 4)
**Trust-plane decision:** ★ Decision moment 2 of 5. Set the auto-pass confidence threshold for each of the 4 vision classes — `good`, `minor_defect`, `major_defect`, `safety_critical_defect`. Three are cost-balanced under the $4,200 FN / $85 FP asymmetry (49:1); `safety_critical_defect` is structurally HARD at the WSH-mandated 0.40 floor (`ml_context.py::SAFETY_CRITICAL_HARD_FLOOR`). Don't conflate threshold with action — declare `auto_pass` / `human_review` / `hard_block` per class explicitly (D-10 in `decisions-open.md`).
**Paste prompt:** `playbook/phase-06-metric-threshold.md` §1 (Sprint 1 / Vision branch)
**Evaluation checklist:** `playbook/phase-06-metric-threshold.md` §2
**Endpoints touched:** `GET /inspect/vision/threshold` (read defaults); `POST /inspect/vision/threshold` (per class — refuses `safety_critical_defect < 0.40` with 422); read PR-curve evidence from `GET /inspect/vision/leaderboard`.
**Skeleton to copy:** `journal/skeletons/phase_6_metric_threshold.md` → `journal/phase_6_vision.md`
**Acceptance criterion:** `journal/phase_6_vision.md` exists ≥ 500 bytes, shows PR curve at K candidate thresholds for each of 4 classes, cost-balanced minimum computed per class with arithmetic shown using $4,200 / $85, `safety_critical_defect` capped at 0.40 with regulatory citation (NOT cost-balanced — cite WSH Act 2006 + IPC-A-610 Class 3 from `specs/compliance-floors.md`), 4 successful `POST /inspect/vision/threshold` calls reflected in `vision_thresholds.json` and `vision_registry.json`, per-class action declared (`auto_pass` / `human_review` / `hard_block`).

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — 4 thresholds POSTed
- [ ] Journal entry quotes $4,200 / $85 / $1,000,000 from `PRODUCT_BRIEF.md §2`
- [ ] Safety-critical hard-floor justification (NOT cost-balanced) named with regulatory citation
- [ ] Moved to `todos/completed/` on human approval
