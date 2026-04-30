<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Phase 3 — Feature Framing

**Sprint:** Sprint 1 · Vision/CNN · See (shared — covers image, text, and joint-modal feature surfaces)
**Playbook phase:** Phase 3 — Feature Framing
**Trust-plane decision:** Declare the feature surface for each modality (image features + augmentations + post metadata; text token / embedding / lexicon; joint-modal alignment) so Phase 4's candidate sweep is fitting on a known surface, not a black box.
**Paste prompt:** `playbook/phase-03-features.md` §1
**Evaluation checklist:** `playbook/phase-03-features.md` §2
**Endpoints touched:** none — declarative phase. Read `src/media/backend/ml_context.py::synthesise_embeddings` (`EMBED_DIM = 32`, deterministic per-`post_id` seed) for the actual scaffold feature shape — call out the surrogate-vs-real-ResNet/BERT distinction in the journal so Phase 5 implications are honest.
**Skeleton to copy:** `journal/skeletons/phase_3_features.md` → `journal/phase_3_features.md`
**Acceptance criterion:** `journal/phase_3_features.md` exists, image / text / multi-modal feature surfaces each named, augmentations declared (or "none — synthetic embeddings" with citation to `ml_context.py::synthesise_embeddings`), drift signal compatibility noted (PSI is computed on these features in Sprint 4).

## Status

- [ ] Prompt sent
- [ ] Response evaluated against checklist
- [ ] Decision made (journal entry drafted)
- [ ] Journal entry cites `ml_context.py::synthesise_embeddings` or `EMBED_DIM`
- [ ] Moved to `todos/completed/` on human approval
