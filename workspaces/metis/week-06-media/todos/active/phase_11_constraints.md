<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 11 — Constraints (first pass)

**Sprint:** Sprint 3 · Fusion + Queue · Decide
**Playbook phase:** Phase 11 — Constraints (first pass — pre-IMDA)
**Trust-plane decision:** Classify the queue allocator's constraints as hard vs soft, with penalty in $ for each soft constraint. CSAM-adjacent stays SOFT in this first pass — it flips HARD in the post-IMDA re-run.
**Paste prompt:** `playbook/phase-11-constraints.md` §1 (first-pass branch)
**Evaluation checklist:** `playbook/phase-11-constraints.md` §2
**Endpoints touched:** `GET /queue/constraints` (default — `imda_priority_must_clear_within_sla` enabled=False); `POST /queue/constraints` to write the hard/soft classification.
**Skeleton to copy:** `journal/skeletons/phase_11_constraints.md` → `journal/phase_11_constraints.md`
**Acceptance criterion:** `journal/phase_11_constraints.md` lists every constraint as hard or soft with rationale; soft constraints have a $ penalty; reviewer headcount cap (HARD — physics) is named; SLA windows (SOFT — penalty per minute late) are named; `imda_priority_must_clear_within_sla` flag explicitly noted as currently SOFT (cost-balanced) and reserved for the post-IMDA re-run.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — constraints POSTed
- [ ] CSAM-adjacent flagged as SOFT in this pass with explicit reservation for post-IMDA
- [ ] Moved to `todos/completed/` on human approval
