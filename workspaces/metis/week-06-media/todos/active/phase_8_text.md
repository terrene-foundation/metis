<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 8 — Deployment Gate (Text)

**Sprint:** Sprint 2 · Text/Transformer · Read
**Playbook phase:** Phase 8 — Deployment Gate
**Trust-plane decision:** Sign the PASS/FAIL gate for the text moderator: per-class evidence + threshold defense + dual-action declaration + Phase 7 findings. On PASS, promote the chosen family to `shadow`.
**Paste prompt:** `playbook/phase-08-gate.md` §1 (Text branch)
**Evaluation checklist:** `playbook/phase-08-gate.md` §2
**Endpoints touched:** `POST /moderate/text/promote` (no IMDA gate on text); `GET /moderate/text/registry`.
**Skeleton to copy:** `journal/skeletons/phase_8_gate.md` → `journal/phase_8_text.md`
**Acceptance criterion:** `journal/phase_8_text.md` records PASS/FAIL with named criteria; if PASS, `text_registry.json` contains a `promote` event with chosen family + `shadow` stage + rationale ≥ 10 chars.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — gate signed
- [ ] If PASS, `POST /moderate/text/promote` returned 200
- [ ] Moved to `todos/completed/` on human approval
