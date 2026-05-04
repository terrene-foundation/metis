<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 4 — Candidates (PredMaint)

**Sprint:** Sprint 2 · Predictive Maintenance · Time-Series ML · Predict (replay of Phase 4 against the predmaint module)
**Playbook phase:** Phase 4 — Candidates
**Trust-plane decision:** Read the 3-family × 3-window predmaint leaderboard (`lightgbm_features` / `lstm_sequence` / `survival_forest_tte` × {3, 7, 14} days) and frame the evidence each (family, window) PAIR would need to win — without picking yet (Phase 5 picks). Read the per-window `degenerate` field on the leaderboard rows (F2.3 trap).
**Paste prompt:** `playbook/phase-04-candidates.md` §1 (PredMaint branch)
**Evaluation checklist:** `playbook/phase-04-candidates.md` §2
**Endpoints touched:** `GET /predict/maintenance/leaderboard`.
**Skeleton to copy:** `journal/skeletons/phase_4_candidates.md` → `journal/phase_4_predmaint.md` (re-use skeleton, distinct journal file)
**Acceptance criterion:** `journal/phase_4_predmaint.md` exists ≥ 500 bytes, three families × three windows = 9 cells with f1 + brier + degenerate-flag captured from `/predict/maintenance/leaderboard`, each family has a one-paragraph "when it would win" rationale (cost asymmetry, retrain cadence, sensor-noise robustness, time-to-event interpretability) — no winner declared. Degenerate flag explicitly named on cells where it is True.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made (journal entry drafted — three rationales, no winner yet)
- [ ] Journal entry quotes per-window numbers from `/predict/maintenance/leaderboard` response
- [ ] `degenerate` field cited at least once
- [ ] Moved to `todos/completed/` on human approval
