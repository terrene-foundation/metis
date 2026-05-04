<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 5 — Implications (Vision) ★

**Sprint:** Sprint 1 · Vision QC · Transfer Learning · See
**Playbook phase:** Phase 5 — Implications
**Trust-plane decision:** ★ Decision moment 1 of 5. Pick the vision architecture (ResNet-50 / EfficientNet-B0 / ViT-Small) and defend the pick in dollars (FN $4,200 / FP $85 cost-balanced, 49:1 asymmetry, WSH $1M ceiling acknowledged separately) AND on per-class evidence — NOT macro-F1 alone (`failure-points.md` F1.1) AND on the 80 ms/board edge-deployment latency budget on Jetson-class hardware.
**Paste prompt:** `playbook/phase-05-implications.md` §1 (Vision branch)
**Evaluation checklist:** `playbook/phase-05-implications.md` §2
**Endpoints touched:** read-only — `GET /inspect/vision/leaderboard`. (No promotion yet — Phase 8 owns promotion.)
**Skeleton to copy:** `journal/skeletons/phase_5_vision.md` → `journal/phase_5_vision.md`
**Acceptance criterion:** `journal/phase_5_vision.md` exists ≥ 500 bytes, names the chosen architecture, dollar defense uses only `PRODUCT_BRIEF.md §2` numbers, per-class `safety_critical_defect` recall called out explicitly (NOT macro-F1), edge-latency budget cited from `PRODUCT_BRIEF.md §7` (80 ms/board on Jetson), Brier-pass / Brier-fail per class captured for the chosen architecture.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made (journal entry drafted)
- [ ] Journal entry cites at least one $ figure from `PRODUCT_BRIEF.md §2` ($4,200 / $85 / $1M)
- [ ] Per-class `safety_critical_defect` recall cited explicitly
- [ ] Moved to `todos/completed/` on human approval
