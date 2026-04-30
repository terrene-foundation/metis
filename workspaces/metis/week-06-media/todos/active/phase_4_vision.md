<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 4 — Candidates (Vision)

**Sprint:** Sprint 1 · Vision/CNN · See
**Playbook phase:** Phase 4 — Candidates
**Trust-plane decision:** Read the 3-family CNN-head leaderboard (`frozen_resnet_lr_head` / `frozen_resnet_rf_head` / `frozen_resnet_gbm_head`) and decide what _evidence_ would justify each family — without yet picking a winner. Picking is Phase 5.
**Paste prompt:** `playbook/phase-04-candidates.md` §1 (Vision pass — pick the §1.A "Vision" branch)
**Evaluation checklist:** `playbook/phase-04-candidates.md` §2
**Endpoints touched:** `GET /moderate/image/leaderboard` (pre-trained at startup); optional `POST /moderate/image/train` to re-run the sweep with a new seed.
**Skeleton to copy:** `journal/skeletons/phase_4_candidates.md` → `journal/phase_4_vision.md`
**Acceptance criterion:** `journal/phase_4_vision.md` exists, all three families' macro_f1 + per-class P/R/F1 captured from `/leaderboard`, each family has one paragraph naming when it would be the right pick (cost surface, retrain cadence, infra constraints) — but NO winner declared. From-scratch training and AutoML BLOCKED (`workflow-03-sprint-1-vision-boot.md` "Transfer-learning prohibition").

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made (journal entry drafted — three rationales, no winner yet)
- [ ] Journal entry quotes per-class numbers from `/moderate/image/leaderboard` response
- [ ] Moved to `todos/completed/` on human approval
