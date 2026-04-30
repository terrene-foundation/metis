<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 5 — Implications (Text)

**Sprint:** Sprint 2 · Text/Transformer · Read (replay)
**Playbook phase:** Phase 5 — Implications
**Trust-plane decision:** Pick the text family for the text moderator and defend the pick — per-class F1 + Brier + held-out reliability check (NOT in-sample; `failure-points.md` F2.2 is the trap).
**Paste prompt:** `playbook/phase-05-implications.md` §1 (Text branch)
**Evaluation checklist:** `playbook/phase-05-implications.md` §2
**Endpoints touched:** `GET /moderate/text/leaderboard`; `GET /moderate/text/calibration` for reliability bins (NB: in-sample — call this out in the journal and request held-out evidence as a Phase 7 sweep input).
**Skeleton to copy:** `journal/skeletons/phase_5_implications.md` → `journal/phase_5_text.md`
**Acceptance criterion:** `journal/phase_5_text.md` names the chosen family, dollar defense via FN/FP cost asymmetry, calibration finding per class with the in-sample caveat documented, retrain-cadence implication for Phase 13 (text is daily — A7).

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made (journal entry drafted)
- [ ] Journal entry cites $320 / $15 from `PRODUCT_BRIEF.md §2`
- [ ] Moved to `todos/completed/` on human approval
