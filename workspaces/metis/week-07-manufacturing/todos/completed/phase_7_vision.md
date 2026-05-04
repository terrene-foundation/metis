<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 7 — Red-team (Vision)

**Sprint:** Sprint 1 · Vision QC · Transfer Learning · See
**Playbook phase:** Phase 7 — Red-team
**Trust-plane decision:** Run three Sprint-1-specific adversarial sweeps — adversarial pixel perturbation / OOD novel defect mode (cold-start, $620/misclass per `business-costs.md`) / IPC-A-610 Class-3-vs-Class-2 skew — with pre-registered acceptance criteria, and decide which findings block Sprint 1's Phase 8 gate vs which become Phase 13 monitoring rules.
**Paste prompt:** `playbook/phase-07-redteam.md` §1 (Vision branch)
**Evaluation checklist:** `playbook/phase-07-redteam.md` §2
**Endpoints touched:** `POST /inspect/vision/score` against curated holdouts (image_ids drawn from the 800 labelled boards).
**Skeleton to copy:** `journal/skeletons/phase_7_red_team.md` → `journal/phase_7_vision.md`
**Acceptance criterion:** `journal/phase_7_vision.md` exists ≥ 500 bytes, lists three sweeps, each with: pre-registered acceptance threshold (written before scoring), observed result, severity (block / monitor / accept), and the Phase 13 drift signal that catches it in production. WSH-near-miss case (board crafted to score 0.39 just under the 0.40 hard floor) is one of the cases. Cold-start novel-defect-mode case ($620/misclass per `business-costs.md`) is one of the cases.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — 3 sweeps run, severity assigned to each finding
- [ ] Journal entry quotes pre-registered acceptance thresholds (timestamps must precede observed results)
- [ ] WSH-near-miss case at 0.39 explicitly run
- [ ] Moved to `todos/completed/` on human approval
