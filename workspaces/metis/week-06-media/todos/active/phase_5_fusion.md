<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 5 — Implications (Multi-Modal · Fusion architecture pick)

**Sprint:** Sprint 3 · Fusion + Queue · Decide
**Playbook phase:** Phase 5 — Implications (Multi-Modal pass)
**Trust-plane decision:** Pick the fusion architecture — `early_fusion` / `late_fusion` / `joint_embedding` — defended on cross-modal coverage gain × dollar value vs compute cost delta (joint-embedding is metadata-flagged "3× compute" — A6). Set the auto-route threshold for `cross_modal_harm`. (Decision moment 3 of 5.)
**Paste prompt:** `playbook/phase-05-implications.md` §1 (Multi-Modal branch)
**Evaluation checklist:** `playbook/phase-05-implications.md` §2
**Endpoints touched:** `GET /moderate/fusion/leaderboard` (three architectures); `POST /moderate/fusion/architecture` to switch active arch with rationale; `POST /moderate/fusion/threshold` to set the cross-modal-harm threshold.
**Skeleton to copy:** `journal/skeletons/phase_5_implications.md` → `journal/phase_5_fusion.md`
**Acceptance criterion:** `journal/phase_5_fusion.md` names the chosen architecture with quantified coverage gain on the 8k multi-modal subset, compute cost delta cited (call out the "3× compute" claim is scaffold metadata, not a measured number — F3.1), late-fusion coupling to chosen image/text families noted (`failure-points.md` F3.1), threshold value POSTed.

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made — architecture POSTed via `/moderate/fusion/architecture`
- [ ] Threshold POSTed via `/moderate/fusion/threshold`
- [ ] Journal entry quotes coverage gain + compute trade-off in $
- [ ] Moved to `todos/completed/` on human approval
