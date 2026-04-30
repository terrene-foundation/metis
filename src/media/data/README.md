# MosaicHub Content Moderation — Data Files

Generated 2026-04-30T08:19:19.792377+00:00 by `src/media/scripts/generate_data.py` (seed 20260430).

| File | Role | Consumed by |
| --- | --- | --- |
| `posts_labelled.csv` | 80,000 labelled posts (image+text+multimodal) | startup, all routes |
| `images/` | 24,000 procedural 32×32 PNGs keyed by post_id | teaching reference (backend uses synthesised embeddings) |
| `baseline_image_metrics.json` | descriptive frozen-ResNet baseline | Phase 4 reference |
| `baseline_text_metrics.json` | descriptive 3-family text leaderboard | Phase 5 reference |
| `fusion_baseline.json` | descriptive early/late/joint metrics | Phase 5 Multi-Modal |
| `drift_baseline.json` | per-modality cadence + reference summary | Phase 13 reference |
| `scenarios/imda_csam_mandate.json` | Sprint 3 mid-injection (Phase 11 + 12 re-run) | scenario_inject.py |
| `scenarios/election_cycle_drift.json` | Sprint 4 mid-injection (Phase 13 drift) | scenario_inject.py |

**Ground truth the student must NEVER see directly:**

- `regulator_class` column — the regulator-mandated severity bucket.
- `fusion_class_label` column — the cross-modal harm ground truth.
- The 22% adversarial subset within multi-modal — the meme-attack cohort.

The descriptive baselines are the "reference picture" — students compare
their live `/moderate/*/leaderboard` runs against these numbers in Phase 4-6.
The backend re-trains the live baselines at startup against the same
labelled CSV; the live numbers will track these closely but vary with seed.
