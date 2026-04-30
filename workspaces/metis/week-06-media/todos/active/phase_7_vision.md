<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 7 — Red-team (Vision)

**Sprint:** Sprint 1 · Vision/CNN · See
**Playbook phase:** Phase 7 — Red-team
**Trust-plane decision:** Run three Sprint-1-specific adversarial sweeps — adversarial pixel perturbation / out-of-distribution image robustness / demographic-skew — with pre-registered acceptance criteria, and decide which findings block Sprint 1's Phase 8 gate vs which become Phase 13 monitoring rules.
**Paste prompt:** `playbook/phase-07-redteam.md` §1 (Vision branch)
**Evaluation checklist:** `playbook/phase-07-redteam.md` §2
**Endpoints touched:** `POST /moderate/image/score` against curated holdouts (post_ids drawn from the 24k image-bearing posts).
**Skeleton to copy:** `journal/skeletons/phase_7_red_team.md` → `journal/phase_7_vision.md`
**Acceptance criterion:** `journal/phase_7_vision.md` lists three sweeps, each with: pre-registered acceptance threshold (written before scoring), observed result, severity (block / monitor / accept), and the Phase 13 drift signal that catches it in production. CSAM-near-miss (post crafted to score 0.39 just under the IMDA floor) is one of the cases.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — 3 sweeps run, severity assigned to each finding
- [ ] Journal entry quotes pre-registered acceptance thresholds (timestamps must precede observed results)
- [ ] Moved to `todos/completed/` on human approval
