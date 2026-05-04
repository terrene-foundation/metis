<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 4 — Candidates (Vision)

**Sprint:** Sprint 1 · Vision QC · Transfer Learning · See
**Playbook phase:** Phase 4 — Candidates
**Trust-plane decision:** Read the 3-architecture vision leaderboard (`resnet50_lr_head` / `efficientnet_b0_rf_head` / `vit_small_gbm_head`) and decide what _evidence_ would justify each architecture — without yet picking a winner. Picking is Phase 5.
**Paste prompt:** `playbook/phase-04-candidates.md` §1 (Vision branch)
**Evaluation checklist:** `playbook/phase-04-candidates.md` §2
**Endpoints touched:** `GET /inspect/vision/leaderboard` (pre-trained at startup); optional `POST /inspect/vision/train` to re-run the sweep with a new seed.
**Skeleton to copy:** `journal/skeletons/phase_4_candidates.md` → `journal/phase_4_vision.md`
**Acceptance criterion:** `journal/phase_4_vision.md` exists ≥ 500 bytes, all three architectures' macro_f1 + per-class P/R/F1 captured from `/inspect/vision/leaderboard`, each architecture has one paragraph naming when it would be the right pick (cost surface, edge-deployment latency budget at 80 ms/board on Jetson, 800-image data scale, retrain cadence) — but NO winner declared. From-scratch CNN training and AutoML-for-vision BLOCKED by the time budget; the brief's transfer-learning framing owns the architecture choice.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made (journal entry drafted — three rationales, no winner yet)
- [ ] Journal entry quotes per-class numbers from `/inspect/vision/leaderboard` response
- [ ] Moved to `todos/completed/` on human approval
