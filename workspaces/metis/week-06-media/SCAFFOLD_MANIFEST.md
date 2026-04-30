<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Scaffold Manifest — Week 6 Media (MosaicHub)

**Version:** 2026-04-30 · **License:** CC BY 4.0

The moderation product is pre-built at the repo root (`src/media/` + `apps/web/media/`). Workspace artefacts are student-produced during `/analyze` → `/todos` → `/implement` → `/redteam` → `/codify`.

## State legend

- `[PRE-BUILT]` — ships complete; students do not edit.
- `[STUDENT-PRODUCED]` — written during `/analyze` / `/todos` / `/implement` / `/redteam` / `/codify`.
- `[PRE-BUILT + STUDENT-EXTENDED]` — skeleton ships; students extend at a named point.

## Repo-root (pre-built product)

| Path                                                 | State         | Role                                                                                     |
| ---------------------------------------------------- | ------------- | ---------------------------------------------------------------------------------------- |
| `pyproject.toml`                                     | `[PRE-BUILT]` | Shared deps (kailash 2.12.0, kailash-ml 1.6.0, torch, transformers, fastapi, uvicorn)    |
| `MONOREPO.md`                                        | `[PRE-BUILT]` | Monorepo doctrine (src/<domain> + apps/<platform>/<domain>)                              |
| `src/media/backend/app.py`                           | `[PRE-BUILT]` | FastAPI app factory + CORS + lifespan                                                    |
| `src/media/backend/config.py`                        | `[PRE-BUILT]` | Env reader; resolves `media_root` and `workspace_root`                                   |
| `src/media/backend/startup.py`                       | `[PRE-BUILT]` | Loads data, fine-tunes ResNet head, fine-tunes BERT, builds fusion stub, registers drift |
| `src/media/backend/ml_context.py`                    | `[PRE-BUILT]` | Shared state: posts + image_baseline + text_baseline + fusion_stub + drift refs          |
| `src/media/backend/routes/health.py`                 | `[PRE-BUILT]` | `GET /health`                                                                            |
| `src/media/backend/routes/moderate_image.py`         | `[PRE-BUILT]` | per-class scores + leaderboard + threshold + promote + registry                          |
| `src/media/backend/routes/moderate_text.py`          | `[PRE-BUILT]` | BERT + RoBERTa + zero-shot LLM 3-family leaderboard + threshold + calibration            |
| `src/media/backend/routes/moderate_fusion.py`        | `[PRE-BUILT]` | early-fusion + late-fusion + joint-embedding stub + cross-modal-harm score               |
| `src/media/backend/routes/drift.py`                  | `[PRE-BUILT]` | per-modality drift signals + per-class calibration decay + retrain-rule persistence × 3  |
| `src/media/backend/routes/queue.py`                  | `[PRE-BUILT]` | reviewer queue allocator (LP) + queue depth + SLA timer                                  |
| `src/media/data/posts_labelled.csv`                  | `[PRE-BUILT]` | 80,000 labelled posts (image + text + multi-modal) × class label + reviewer decision     |
| `src/media/data/images/`                             | `[PRE-BUILT]` | 24,000 image files referenced by posts_labelled.csv                                      |
| `src/media/data/baseline_image_metrics.json`         | `[PRE-BUILT]` | Per-class P/R/F1 for the frozen-ResNet-50 + 5-class-head baseline                        |
| `src/media/data/baseline_text_metrics.json`          | `[PRE-BUILT]` | 3-family leaderboard (BERT / RoBERTa / zero-shot LLM) per-class                          |
| `src/media/data/fusion_baseline.json`                | `[PRE-BUILT]` | Early-fusion + late-fusion baseline metrics on the 8k multi-modal subset                 |
| `src/media/data/drift_baseline.json`                 | `[PRE-BUILT]` | Reference distributions for image / text / fusion (3 separate baselines)                 |
| `src/media/data/scenarios/imda_csam_mandate.json`    | `[PRE-BUILT]` | Sprint 3 mid-injection — re-classify CSAM-adjacent threshold as hard                     |
| `src/media/data/scenarios/election_cycle_drift.json` | `[PRE-BUILT]` | Sprint 4 mid-injection — adversarial drift on text moderator                             |
| `src/media/scripts/generate_data.py`                 | `[PRE-BUILT]` | Data labeller (seed 20260430) — deterministic re-run                                     |
| `src/media/scripts/preflight.py`                     | `[PRE-BUILT]` | Green-light check; exit 0 = all green                                                    |
| `src/media/scripts/run_backend.sh`                   | `[PRE-BUILT]` | `uvicorn backend.app:app` with `METIS_API_HOST`/`METIS_API_PORT`                         |
| `src/media/scripts/scenario_inject.py`               | `[PRE-BUILT]` | Fire imda_csam_mandate or election_cycle_drift; writes marker in workspace               |
| `apps/web/media/index.html`                          | `[PRE-BUILT]` | Viewer Pane — 6 cards polling backend every 5 s (image / text / fusion / drift / queue)  |
| `apps/web/media/serve.sh`                            | `[PRE-BUILT]` | `python3 -m http.server 3000`                                                            |

## Workspace (student-produced)

| Path                                 | State                | When produced       |
| ------------------------------------ | -------------------- | ------------------- |
| `PRODUCT_BRIEF.md`                   | `[PRE-BUILT]`        | Ships with scaffold |
| `PLAYBOOK.md`                        | `[PRE-BUILT]`        | Ships with scaffold |
| `START_HERE.md`                      | `[PRE-BUILT]`        | Ships with scaffold |
| `specs/_index.md` + supporting specs | `[PRE-BUILT]`        | Ships with scaffold |
| `journal/_template.md`               | `[PRE-BUILT]`        | Schema for entries  |
| `briefs/`                            | `[STUDENT-PRODUCED]` | Student-writable    |
| `01-analysis/failure-points.md`      | `[STUDENT-PRODUCED]` | `/analyze`          |
| `01-analysis/assumptions.md`         | `[STUDENT-PRODUCED]` | `/analyze`          |
| `01-analysis/decisions-open.md`      | `[STUDENT-PRODUCED]` | `/analyze`          |
| `todos/active/phase_N_*.md` (×13)    | `[STUDENT-PRODUCED]` | `/todos`            |
| `todos/completed/phase_N_*.md`       | `[STUDENT-PRODUCED]` | `/implement`        |
| `journal/phase_{1..13}_*.md`         | `[STUDENT-PRODUCED]` | `/implement`        |
| `journal/phase_11_postimda.md`       | `[STUDENT-PRODUCED]` | Sprint 3 injection  |
| `journal/phase_12_postimda.md`       | `[STUDENT-PRODUCED]` | Sprint 3 injection  |
| `04-validate/redteam.md`             | `[STUDENT-PRODUCED]` | `/redteam`          |
| `.session-notes`                     | `[STUDENT-PRODUCED]` | `/wrapup`           |

## Contract violations

- A `[PRE-BUILT]` file with a `TODO-STUDENT` marker is a scaffolding error — instructor fixes.
- A `[STUDENT-PRODUCED]` file with `"placeholder": true` or a `# TODO` marker in the body scores zero on the rubric.
- Missing `journal/phase_N_*.md` for a phase the student claimed to run is a D3 (trade-off honesty) zero.

## Implementation deviations (2026-04-30)

The scaffold ships per the table above. Two implementation choices deviate
from the brief's literal phrasing — both pedagogically conservative.

1. **"Frozen ResNet head" / "fine-tuned BERT" use sklearn surrogates.**
   The backend trains real classifiers on per-class Gaussian-centroid
   embeddings synthesised deterministically per `post_id`. The
   classifiers themselves are real sklearn fits (LogisticRegression,
   RandomForestClassifier, HistGradientBoostingClassifier) producing real
   per-class precision / recall / F1 / Brier. Reason: a literal frozen
   ResNet-50 + BERT fine-tune at startup would take >30 minutes on a
   laptop CPU and break the student iteration loop. The pedagogical
   contract — "students see the leaderboard differ across families and
   defend a per-class threshold under the $320 / $15 asymmetry" — is
   intact. Live `/moderate/*/train` re-runs the sweep so students can
   observe the leaderboard move with seed.

2. **`src/media/data/images/` ships 32×32 procedural PNGs.** The
   manifest specifies "24,000 image files referenced by
   posts_labelled.csv". The scaffold writes 24k 32×32 RGB PNGs whose
   pixel content is deterministic per-class noise (each class has a
   distinct base color + Gaussian noise). Total disk = ~94 MB. The
   backend does NOT read pixels at inference time — it uses synthesised
   embeddings — so the images are a teaching artefact only (students
   who curl `data/images/post_000123.png` see a real PNG, which is what
   the manifest's intent requires).

Endpoint-name mapping (backend-actual ↔ brief-spec):

- `/moderate/image/leaderboard` ✓
- `/moderate/image/threshold` ✓
- `/moderate/text/leaderboard` ✓
- `/moderate/text/threshold` ✓
- `/moderate/text/calibration` ✓ (extra — Phase 5 SML evidence)
- `/moderate/fusion/score` ✓
- `/moderate/fusion/architecture` ✓ (extra — Phase 5 Multi-Modal lever)
- `/drift/check` ✓ (accepts model_id + window)
- `/drift/retrain_rule` ✓ (one rule per model_id)
- `/queue/state`, `/queue/solve`, `/queue/last_plan` ✓ (Phase 11+12)

Family names diverge from "LR / RF / GBM" plain to make the pedagogy
explicit:

- Image: `frozen_resnet_lr_head` / `frozen_resnet_rf_head` /
  `frozen_resnet_gbm_head` (all share the same frozen embedding;
  different head architectures).
- Text: `fine_tuned_bert` / `fine_tuned_roberta` / `zero_shot_llm`
  (the 3-family pattern matches the brief's "BERT + RoBERTa + zero-shot
  LLM" leaderboard).

The CSAM-adjacent IMDA hard floor (0.40) is enforced at the
`POST /moderate/image/threshold` boundary (422 below floor) AND at the
`POST /moderate/image/promote` boundary (422 if the persisted threshold
is below floor at promote time). Both gates are defensive; either one
catches a student who forgets that this class is structurally hard.
