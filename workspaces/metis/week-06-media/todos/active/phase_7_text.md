<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 7 — Red-team (Text)

**Sprint:** Sprint 2 · Text/Transformer · Read
**Playbook phase:** Phase 7 — Red-team
**Trust-plane decision:** Run three text-specific adversarial sweeps — typo / unicode-confusable robustness / 5-market OOD (Singlish, Malay, code-mixed) / demographic-skew — with pre-registered acceptance, and decide which findings block Phase 8 vs which become Phase 13 monitoring rules.
**Paste prompt:** `playbook/phase-07-redteam.md` §1 (Text branch)
**Evaluation checklist:** `playbook/phase-07-redteam.md` §2
**Endpoints touched:** `POST /moderate/text/score` against curated holdouts.
**Skeleton to copy:** `journal/skeletons/phase_7_red_team.md` → `journal/phase_7_text.md`
**Acceptance criterion:** `journal/phase_7_text.md` lists three sweeps with pre-registered acceptance + observed result + severity + Phase 13 catch. The OOD sweep MUST exercise at least 3 of the 5 markets (SG/MY/ID/PH/TH), since text drift cadence in Phase 13 is daily and these are where the drift surfaces.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — 3 sweeps run
- [ ] Pre-registered acceptance thresholds timestamped before observed results
- [ ] Moved to `todos/completed/` on human approval
