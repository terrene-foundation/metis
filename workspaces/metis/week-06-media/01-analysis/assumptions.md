<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Inherited Assumptions — MosaicHub Content Moderation

**Phase:** `/analyze` · **Author:** agent · **Date:** 2026-04-30
**Source:** read of `src/media/backend/{ml_context,startup,config,routes/*}.py` and `PRODUCT_BRIEF.md` §2.

Twelve assumptions the scaffold has already baked in. Each is cited to a source file. Every dollar figure is quoted verbatim from `PRODUCT_BRIEF.md §2` (the cost table). Every assumption you accept tonight is a decision by omission — the rubric will treat it as a decision you made unless you contest it in a journal.

---

## A1. Class taxonomies are frozen at five each per modality

**Cited to.** `src/media/backend/ml_context.py::IMAGE_CLASSES` and `::TEXT_CLASSES`.

```python
IMAGE_CLASSES: tuple[str, ...] = ("nsfw", "violence", "weapons", "csam_adjacent", "safe")
TEXT_CLASSES:  tuple[str, ...] = ("hate_speech", "harassment", "threats", "self_harm", "safe")
```

The 5-class structure is invariant — `startup.py` asserts each baseline ships fits across exactly these 5 classes; routes refuse threshold POSTs for unknown classes (`routes/moderate_image.py::set_threshold` 422s on `req.klass not in IMAGE_CLASSES`). Adding a sixth class (e.g. `terrorism` as its own class rather than folded into `violence`/`csam_adjacent`) is out of scope tonight.

## A2. CSAM-adjacent is structurally HARD; floor is 0.40

**Cited to.** `ml_context.py::CSAM_ADJACENT_HARD_FLOOR = 0.40` and the dual-gate enforcement at `routes/moderate_image.py::set_threshold` (422 if `klass == "csam_adjacent" and threshold < 0.40`) and `::promote` (422 if persisted CSAM threshold below floor at promote time).

The reason is regulatory, not statistical: `PRODUCT_BRIEF.md §2` lists "SG Online Safety Code violation (non-takedown of CSAM) — $1,000,000 per incident — IMDA fine + CEO-level reputational" — quoted verbatim. The cost is high enough that no cost-balanced threshold can compete with the regulatory floor. You inherit the value 0.40 — challenge it only if you have a defensible regulatory reading otherwise.

## A3. Embedding dimensionality is 32; embeddings are deterministic per `post_id`

**Cited to.** `ml_context.py::EMBED_DIM = 32` and `::synthesise_embeddings`. The seed is sha256-derived per `(post_id, modality)` (`_post_seed`); same post → same embedding across reruns.

The framing in `START_HERE.md` says "frozen ResNet head + fine-tuned 5-class head". The scaffold's actual implementation (per `SCAFFOLD_MANIFEST.md` § "Implementation deviations") uses sklearn classifiers on per-class Gaussian-centroid synthetic embeddings — real fits, real per-class metrics, but not real ResNet activations. The pedagogical contract is intact (3-family leaderboard, per-class P/R/F1, $320/$15 cost-balanced threshold). Asking Claude Code to "use real ResNet weights" raises a non-trivial change to startup time and is out of budget tonight.

## A4. Image baseline is a 3-family head sweep, not a from-scratch CNN

**Cited to.** `ml_context.py::build_image_baseline` constructs three families:

- `frozen_resnet_lr_head` — `LogisticRegression(max_iter=300)`
- `frozen_resnet_rf_head` — `RandomForestClassifier(n_estimators=80, max_depth=12)`
- `frozen_resnet_gbm_head` — `HistGradientBoostingClassifier(max_iter=100, max_depth=4, learning_rate=0.10)`

All three share the same frozen embedding; only the head architecture varies. Phase 4 candidates are these three heads. Full from-scratch ResNet training is BLOCKED by the time budget; AutoML for vision architectures is out of scope (per `playbook/workflow-03-sprint-1-vision-boot.md` "Transfer-learning prohibition").

## A5. Text baseline is BERT + RoBERTa + zero-shot LLM 3-family leaderboard

**Cited to.** `ml_context.py::build_text_baseline`:

- `fine_tuned_bert` — `HistGradientBoostingClassifier(max_iter=120)` standing in for fine-tuned BERT-base
- `fine_tuned_roberta` — `RandomForestClassifier(n_estimators=100)` standing in for fine-tuned RoBERTa
- `zero_shot_llm` — `LogisticRegression(max_iter=300)` standing in for prompt-only LLM baseline

Per `SCAFFOLD_MANIFEST.md` § "Family names diverge from 'LR / RF / GBM' plain to make the pedagogy explicit" — the family **labels** preserve the brief's "BERT + RoBERTa + zero-shot LLM" leaderboard pattern even though the underlying classifiers are sklearn surrogates.

## A6. Fusion ships three architectures (early / late / joint-embedding); chosen by macro-F1 at startup

**Cited to.** `ml_context.py::build_fusion_baseline` builds:

- `early_fusion` — concat image+text embeddings → `HistGradientBoostingClassifier`
- `late_fusion` — per-modality `predict_proba` logits → `LogisticRegression`
- `joint_embedding` — L2-normalised image-text element-wise product → `HistGradientBoostingClassifier`

`fusion_baseline.chosen_architecture = max(candidates, key=lambda k: candidates[k].macro_f1)`. The `joint_embedding` variant carries `family_why="...best on cross-modal harm, 3× compute"` — the 3× compute factor is a **claim in the metadata string**, not a measured number; treat it as the pedagogical framing the brief uses, not a literal benchmark of tonight's stub.

## A7. Drift baselines are registered for exactly three model IDs; cadence is hardcoded per modality

**Cited to.** `startup.py` builds `drift_baselines = {"image": ..., "text": ..., "fusion": ...}` with `cadence="weekly"` for image, `cadence="daily"` for text, `cadence="per_incident"` for fusion. The hard invariant at the bottom of `startup.py` raises `RuntimeError` if `drift_baselines_registered != 3`.

The cadence labels are metadata only — they live on the `DriftReference` dataclass. The scaffold does not enforce that the student's Phase 13 `retrain_rule` matches the registered cadence; that match is a rubric concern.

## A8. Reviewer queue allocator: 5 tiers × 3 reviewer pools; capacity = 100 reviewers × 400 working min/day

**Cited to.** `routes/queue.py::TIERS` (5 tiers — `imda_priority`, `self_harm_review`, `threats_review`, `hate_speech_review`, `general_review`), `::REVIEWER_POOLS` (3 pools — `senior` headcount 12, `standard` headcount 50, `surge` headcount 38), and `::WORKING_MINUTES_PER_REVIEWER = 400`.

Total working minutes/day = (12+50+38) × 400 = 40,000. The `imda_priority` SLA is 60 seconds (hardcoded `sla_seconds: 60`); the `senior` pool is the only pool qualified for `imda_priority` (`qualified_tiers` lists imda_priority only on senior). When the IMDA hard constraint fires, demand on `imda_priority` × `minutes_per_post: 4.0` × backlog must fit inside `senior.headcount × 400 = 4,800` minutes/day.

The $22/min reviewer-time cost from `PRODUCT_BRIEF.md §2` is reflected as `cost_per_min: 22.0` on the `standard` pool; the `senior` pool is set to `cost_per_min: 32.0` and the `surge` pool to `18.0`. The brief lists only the standard rate; the senior and surge rates are scaffold-set assumptions.

## A9. Default expected backlog: 8,080 posts/day across the 5 tiers

**Cited to.** `routes/queue.py::DEFAULT_BACKLOG`:

```python
DEFAULT_BACKLOG = {
    "imda_priority": 80,
    "self_harm_review": 240,
    "threats_review": 460,
    "hate_speech_review": 1800,
    "general_review": 5500,
}
```

These are scaffold-set; the brief mentions "Reviewer queue depth: average 8,000 items at start of workshop" (matches within rounding). `routes/queue.py::SolveRequest` allows `backlog` override per call — students can reframe the LP for a specific day's expected volume.

## A10. Cost asymmetry $320 FN / $15 FP / $1M IMDA / $22 reviewer min — verbatim from brief

**Cited to.** `PRODUCT_BRIEF.md §2`. Quoted verbatim:

- "False negative (harmful content left up, then reported) — $320 per piece (regulator complaint risk + lawsuit defense)"
- "False positive (legitimate content auto-removed) — $15 per piece (creator trust + appeal-handling cost)"
- "Human reviewer time — $22 per minute on the queue"
- "SG Online Safety Code violation (non-takedown of CSAM) — $1,000,000 per incident — IMDA fine + CEO-level reputational"
- "Cold-start cost (novel content type, zero-shot misclass) — $8 per misclassified novel meme format"
- "GPU inference cost — $0.03 per 1,000 image classifications served"

The 21:1 ratio (320/15) is stated in the brief. These are the only numbers tonight's journal entries may cite without separate justification.

## A11. CORS is permissive; backend binds 127.0.0.1 by default

**Cited to.** `src/media/backend/app.py` registers `CORSMiddleware(allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])`. `src/media/backend/config.py::load_settings` defaults `api_host` to `"127.0.0.1"`.

The scaffold's own comment in `app.py` says "the wildcard is acceptable HERE because the backend binds to 127.0.0.1 by default and the dataset contains no real PII" — explicit teaching-scaffold concession. Do not copy this CORS configuration into a production journal entry. Flagging this in `phase_7_red_team` is the rubric-recognised disposition.

## A12. Workspace JSON files are the persistence layer; auto-detection treats journal files >500 bytes as authored

**Cited to.** `routes/state.py::_PHASE_FILE_RE` and `_SKELETON_BYTES_THRESHOLD = 500`. State auto-detection scans `workspace_root/journal/phase_*.md`; any file matching `phase_(\d+)_<slug>.md` larger than 500 bytes is treated as an authored phase entry.

`routes/queue.py`, `routes/moderate_image.py`, `routes/moderate_text.py`, `routes/moderate_fusion.py`, and `routes/drift.py` all persist state via JSON files in `workspace_root` (`queue_constraints.json`, `image_thresholds.json`, etc.). The state survives backend restart. Files written via the IMDA injection script (`scripts/scenario_inject.py`) directly mutate `queue_constraints.json` — that's the mechanism behind the `~4:30 pm` Sprint 3 trigger.

---

## Closing note

The dollar table (A10), the 5-class taxonomies (A1), the IMDA hard floor (A2), and the three drift cadences (A7) are the load-bearing assumptions tonight. Everything else is a scaffold-set default that you can override or contest in a journal — and if you don't contest it, the rubric scores you as having accepted it.

Stopping for `/todos`.
