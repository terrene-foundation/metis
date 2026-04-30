<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 8 — Deployment Gate (Vision)

**Sprint:** Sprint 1 · Vision/CNN · See
**Playbook phase:** Phase 8 — Deployment Gate
**Trust-plane decision:** Sign the PASS/FAIL gate for the image moderator: per-class evidence + threshold defense + Phase 7 findings + CSAM-floor compliance. On PASS, promote the chosen family to `shadow` stage with rationale; on FAIL, name the specific deficit and the next action.
**Paste prompt:** `playbook/phase-08-gate.md` §1 (Vision branch)
**Evaluation checklist:** `playbook/phase-08-gate.md` §2
**Endpoints touched:** `POST /moderate/image/promote` (refuses if persisted CSAM threshold < 0.40 with 422 — second IMDA gate, defense-in-depth); `GET /moderate/image/registry` for promotion history.
**Skeleton to copy:** `journal/skeletons/phase_8_gate.md` → `journal/phase_8_vision.md`
**Acceptance criterion:** `journal/phase_8_vision.md` records PASS or FAIL with named criteria; if PASS, `image_registry.json` contains a `promote` event with the chosen family + `shadow` stage + rationale ≥ 10 chars + `csam_threshold_at_promote` field present.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — gate signed
- [ ] If PASS, `POST /moderate/image/promote` returned 200 and `image_registry.json` updated
- [ ] Moved to `todos/completed/` on human approval
