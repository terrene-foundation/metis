<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# MosaicHub — API Surface

Base URL: `http://127.0.0.1:8000` (override with `METIS_API_PORT`).

All endpoints are wired in `src/media/backend/routes/`. Students call them indirectly through Claude Code; they do not implement them.

## Health

- `GET /health` — `{ status, posts, images, image_baseline_arch, image_baseline_f1, text_baseline_arch, text_baseline_f1, fusion_baseline_strategy, drift_refs_active }`

## Image Moderator (Sprint 1 · CNN)

- `GET  /moderate/image/leaderboard` — per-class P/R/F1 (5 classes: nsfw, violence, weapons, csam_adjacent, safe) on baseline ResNet-50-frozen + pre-baked partial-fine-tune comparison
- `POST /moderate/image/finetune` — `{ unfreeze_layers: int, lr, epochs, seed }` — run a partial-fine-tune sweep
- `POST /moderate/image/threshold` — `{ class_name, threshold, action: "auto_remove"|"human_review"|"allow" }` — Phase 6 deliverable; CSAM-adjacent threshold validated against IMDA hard floor
- `POST /moderate/image/promote` — `{ version, to_stage }` — staging → shadow → production → archived
- `GET  /moderate/image/registry` — all versions + current production + shadow
- `POST /moderate/image/score` — `{ image_id }` — per-class scores for one image (Phase 7 robustness probe)

## Text Moderator (Sprint 2 · Transformer)

- `GET  /moderate/text/leaderboard` — 3-family leaderboard (bert_base / roberta / zero_shot_llm) × 5 classes (hate_speech, harassment, threats, self_harm_encouragement, safe)
- `POST /moderate/text/finetune` — `{ family, lr, epochs, seed }` — run a fine-tune for one family
- `POST /moderate/text/threshold` — `{ class_name, threshold, action }` — Phase 6 deliverable
- `POST /moderate/text/calibrate` — `{ method: "platt"|"isotonic" }` — post-hoc calibration; returns Brier + reliability diagram
- `POST /moderate/text/promote` — `{ version, to_stage }`
- `GET  /moderate/text/registry`
- `POST /moderate/text/score` — `{ caption }` — per-class scores for one caption

## Fusion Moderator (Sprint 3 · Multi-Modal)

- `GET  /moderate/fusion/architecture` — current mode (early / late / joint), encoder configs, alignment-head config
- `POST /moderate/fusion/architecture` — Phase 5 + 10 deliverable; sets mode + per-modality weights
- `POST /moderate/fusion/score` — `{ post_id }` — `{ image_score, text_score, cross_modal_harm_score, disagree_flag }`
- `POST /moderate/fusion/compare` — `{ n_samples }` — offline eval: cross-modal coverage gain, joint AUC, false-positive rate on neutral memes

## Reviewer Queue Allocator (Sprint 3 · LP)

- `GET  /queue/objective` — current LP objective weights (FN cost / FP cost / reviewer-min / SLA)
- `POST /queue/objective` — Phase 10 deliverable; sets weights with dollar justification
- `GET  /queue/constraints` — current hard/soft constraint set (reviewer headcount, SLA, IMDA mandates)
- `POST /queue/constraints` — Phase 11 deliverable; classifies each constraint
- `POST /queue/solve` — solves the LP; returns plan + queue depth + expected SLA + shadow prices
- `GET  /queue/last_plan` — most recent solve result

## Drift (Sprint 4 · MLOps)

- `GET  /drift/status/{model_id}` — is reference registered? `model_id` ∈ {image_moderator, text_moderator, fusion_moderator}
- `POST /drift/check` — `{ model_id, window: "recent_30d"|"election_cycle_drift"|"custom" }` — per-feature PSI + per-class calibration decay + overall severity
- `GET  /drift/retrain_rule/{model_id}` — current rule for that model
- `POST /drift/retrain_rule` — Phase 13 deliverable; `{ model_id, signals, thresholds, duration_window, hitl, seasonal_exclusions }`

## State

- `GET /state/sprints` — per-sprint completion status used by the viewer's value-chain banner
- `GET /state/decisions` — per-decision-moment status used by the viewer

## Error taxonomy

- `404` — unknown version / unknown post_id / unknown model_id
- `409` — illegal stage transition (names the legal set) / IMDA-hard threshold below regulator floor
- `422` — unknown family / unknown fusion mode / unknown calibration method / two classes got the same action / weights don't sum to 1.0 / hard constraint set is infeasible
