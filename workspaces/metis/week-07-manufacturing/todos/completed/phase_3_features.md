<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 3 — Feature Framing

**Sprint:** Sprint 1 · Vision QC · Transfer Learning · See (shared — covers vision, sensor, RL state, and safety-monitor surfaces)
**Playbook phase:** Phase 3 — Feature Framing
**Trust-plane decision:** Declare the feature surface for each modality (vision: per-architecture frozen-backbone embeddings + augmentations; sensor: sliding window stats per machine; RL state: zone temps + line speed + board class on the line + minutes since last calibration; safety: PPE/no-PPE × restricted-zone/clear) so Phase 4's candidate sweep is fitting on a known surface, not a black box.
**Paste prompt:** `playbook/phase-03-features.md` §1
**Evaluation checklist:** `playbook/phase-03-features.md` §2
**Endpoints touched:** none — declarative phase. Read `src/manufacturing/backend/ml_context.py::synthesise_image_embeddings` (per-architecture embedding dimensionalities, deterministic per-`image_id` seed) and `::synthesise_sensor_window_features` (per-machine sliding window stats) for the actual scaffold feature shapes — call out the surrogate-vs-real-ResNet/EfficientNet/ViT distinction in the journal so Phase 5 implications are honest.
**Skeleton to copy:** `journal/skeletons/phase_3_features.md` → `journal/phase_3_features.md`
**Acceptance criterion:** `journal/phase_3_features.md` exists ≥ 500 bytes, vision / sensor / RL-state / safety feature surfaces each named, augmentations declared (or "none — synthetic embeddings" with citation to `ml_context.py::synthesise_image_embeddings`), drift signal compatibility noted (PSI is computed on these features in Sprint 4 per `routes/drift.py::_compute_psi`; the brier-N/A caveat for the RL drift signal cited per `assumptions.md` A9).

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made (journal entry drafted)
- [ ] Journal entry cites `ml_context.py::synthesise_image_embeddings` AND `::synthesise_sensor_window_features`
- [ ] Moved to `todos/completed/` on human approval
