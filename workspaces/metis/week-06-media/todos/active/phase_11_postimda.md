<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 11 — Constraints (post-IMDA re-run)

**Sprint:** Sprint 3 · Fusion + Queue · Decide (post-injection at ~4:30 pm)
**Playbook phase:** Phase 11 — Constraints (post-IMDA re-classification)
**Trust-plane decision:** Re-classify CSAM-adjacent threshold as HARD (regulator-mandated 0.40) AND flip `imda_priority_must_clear_within_sla` to enabled=True with the 60-second SLA. Enumerate ALL three endpoints the IMDA mandate touches — image threshold, fusion threshold, queue constraints — so nothing slips (`failure-points.md` F3.2). (Decision moment 4 of 5, re-class half.)
**Paste prompt:** `playbook/phase-11-constraints.md` §1 (post-IMDA branch)
**Evaluation checklist:** `playbook/phase-11-constraints.md` §2
**Endpoints touched:** `POST /moderate/image/threshold` (csam_adjacent re-affirm at 0.40 — backend already enforces); `POST /moderate/fusion/threshold` (auto-blur side of the mandate); `POST /queue/constraints` (flip the imda flag enabled=True). Trigger fires via `src/media/scripts/scenario_inject.py imda_csam_mandate` (instructor-launched OR student-launched per workshop staging).
**Skeleton to copy:** `journal/skeletons/phase_11_postimda.md` → `journal/phase_11_postimda.md`
**Acceptance criterion:** `journal/phase_11_postimda.md` enumerates the three endpoints touched by the mandate, each with the new constraint state and rationale citing `PRODUCT_BRIEF.md §2` $1,000,000 IMDA fine; `queue_constraints.json` shows `imda_priority_must_clear_within_sla.enabled = True`.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — three endpoints touched
- [ ] `queue_constraints.json` shows IMDA flag enabled
- [ ] Journal quotes $1,000,000 from `PRODUCT_BRIEF.md §2`
- [ ] Moved to `todos/completed/` on human approval
