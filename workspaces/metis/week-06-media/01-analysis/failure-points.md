<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Failure Points — MosaicHub Content Moderation

**Phase:** `/analyze` · **Author:** agent · **Date:** 2026-04-30
**Source:** read of `src/media/backend/{ml_context,startup,routes/*}.py` and `SCAFFOLD_MANIFEST.md`.

Twelve failure points across the four moderation modules — three per module — each cited to a specific file and function in the scaffold. Each failure maps to the Playbook phase that catches it. Citations name `<file>::<function>`; line numbers are deliberately omitted because they drift across edits.

---

## Module 1 · Image Moderator (Sprint 1 · CNN · See)

### F1.1 — Chosen family wins on macro_f1, hides per-class CSAM-adjacent recall miss

**Where it lives.** `src/media/backend/ml_context.py::build_image_baseline` ranks the 3-family leaderboard by `max(candidates, key=lambda k: candidates[k].macro_f1)`. The `chosen_family` is the macro-F1 winner; per-class recall on `csam_adjacent` is not a tie-breaker.

**What goes wrong.** Macro-F1 averages across all 5 classes equally. The CSAM-adjacent class — the one that costs $1,000,000 per missed incident per `PRODUCT_BRIEF.md §2` — has the smallest weight in the ranking. A family with macro_f1 = 0.88 that achieves 0.55 recall on `csam_adjacent` ranks above a family with macro_f1 = 0.84 and 0.78 recall on `csam_adjacent`. The wrong family ships.

**Caught by.** Phase 5 Implications (re-rank on per-class metrics, not macro) and Phase 6 Metric+Threshold (per-class threshold defense). The `/moderate/image/leaderboard` `note` field already warns against macro-only ranking.

### F1.2 — Embeddings are deterministic per `post_id`; "live training" doesn't see new data

**Where it lives.** `ml_context.py::synthesise_embeddings` derives a per-(`post_id`, `modality`) seed via `_post_seed` and re-uses it on every call. `routes/moderate_image.py::score` re-synthesises the embedding to keep the score stable across requests.

**What goes wrong.** A student who runs `POST /moderate/image/train` with a different seed expects to see a fresh data sweep. They will see the leaderboard re-fit on the same 32-dim embeddings. The pedagogy survives (the leaderboard still ranks differently because the train/test split rotates), but a student who claims "I trained on a new dataset" is wrong — the dataset is fixed at startup.

**Caught by.** Phase 4 Candidates (read the actual sweep output rather than trusting the prompt) and Phase 7 Red-team (OOD test surfaces this — adversarial samples don't exist outside the registered embeddings).

### F1.3 — Promote refuses below CSAM hard floor; threshold POST does too — but promote-then-lower bypass

**Where it lives.** `routes/moderate_image.py::promote` checks `csam_tau < CSAM_ADJACENT_HARD_FLOOR` and returns 422. `routes/moderate_image.py::set_threshold` checks the same floor on `POST /moderate/image/threshold`. Both gates exist independently.

**What goes wrong.** The two checks are belt-and-suspenders defense for an honest student. The fail mode is procedural: a student promotes the chosen family at threshold = 0.5 (passes both gates), then later sets `csam_adjacent` threshold = 0.35 (refused — 422) — but if they instead promote at 0.5 and never set the CSAM-class threshold, the workspace `image_thresholds.json` retains the default 0.40 floor; they can claim "I hit the IMDA floor" without having reasoned about it. The floor is met by accident, not by design.

**Caught by.** Phase 6 Metric+Threshold journal (must write the IMDA-floor justification, not just hit it) and Phase 8 Gate (instructor reviews threshold rationale).

---

## Module 2 · Text Moderator (Sprint 2 · Transformer · Read)

### F2.1 — No IMDA-floor analog for `self_harm` — clinical-safety dual action lives only in journal

**Where it lives.** `routes/moderate_text.py::set_threshold` accepts any `[0, 1]` threshold for any class without a hard-floor check. `TEXT_CLASSES` (`ml_context.py`) contains `self_harm` but the route imposes no warn-and-queue gate. The `/threshold` GET `note` says "no IMDA-mandated hard floor" and is silent on clinical-safety floors.

**What goes wrong.** A student sets `self_harm` threshold = 0.85 to hit the cost-balanced minimum, ships, and the platform auto-removes self-harm content above 0.85 with no content-warning, no helpline link, no human-review queue. The clinical-safety guidance from `playbook/phase-06-metric-threshold.md` ("warn-and-queue is non-negotiable") is enforced only by the rubric, not by the backend.

**Caught by.** Phase 6 Metric+Threshold journal must surface dual action explicitly; Phase 7 Red-team on text checks whether high-confidence self-harm flows route to a queue or fall straight to auto-remove.

### F2.2 — Reliability bins computed on training distribution, not held-out

**Where it lives.** `routes/moderate_text.py::calibration` calls `chosen.scaler.transform(ctx.text_embeddings)` and `chosen.model.predict_proba(X_std)` on the **full training set**. The reliability bins reported are in-sample.

**What goes wrong.** A student looks at a near-zero `calibration_gap` across all 10 bins and concludes "BERT is well-calibrated tonight". The model was fit on this exact data; the in-sample calibration is overoptimistic. Out-of-sample Brier — the metric that survives drift — is bigger. The Phase 5 SML calibration check is weaker than the journal will claim.

**Caught by.** Phase 5 Implications calibration check (push back if calibration_gap is suspiciously near zero across all bins; demand held-out evaluation) and Phase 13 Drift (the `per_class_calibration_decay` from `routes/drift.py::check_drift` does compare live Brier to registered baseline — that is the held-out check).

### F2.3 — `/score` decision uses fixed priority list; threshold collisions silently resolved

**Where it lives.** `routes/moderate_text.py::score` computes `harmful = [c for c in TEXT_CLASSES if c != "safe" and per_class[c]["above_threshold"]]`, then dispatches: `if "threats" in harmful or "self_harm" in harmful: decision = "auto_remove_priority_review"`; `elif harmful: decision = "auto_remove"`; `else: decision = "allow"`.

**What goes wrong.** The dispatch is positional (`threats` and `self_harm` win over `hate_speech` and `harassment`). A post above threshold on `hate_speech` AND `threats` gets `auto_remove_priority_review`; a post above on `hate_speech` AND `harassment` gets `auto_remove`. The student never declares this priority anywhere; the model is enforcing a policy the student did not write.

**Caught by.** Phase 1 Frame (define what counts as harmful — and what relative priority each class carries) and Phase 6 Metric+Threshold (per-class action declaration, not a single auto-remove threshold).

---

## Module 3 · Fusion Moderator + Queue Allocator (Sprint 3 · Multi-Modal · Decide)

### F3.1 — `late_fusion` consumes the chosen-family logits at score time; arch switch plus family change silently refits

**Where it lives.** `routes/moderate_fusion.py::score` for `arch == "late_fusion"` calls `ctx.image_baseline.candidates[ctx.image_baseline.chosen_family]` and the same for text, then concatenates the two `predict_proba` outputs. The `late_fusion` model itself was fit at startup against the **then-chosen** image and text families — but it is queried at score time against the **now-chosen** families.

**What goes wrong.** A student promotes a different image family (`POST /moderate/image/promote`) AFTER startup. The `late_fusion` scorer now feeds new image logits into a meta-classifier trained on the old image logits. The meta-classifier sees an input distribution it never trained on; cross-modal-harm probabilities are unreliable.

**Caught by.** Phase 5 Multi-Modal architecture choice (recognise late-fusion has a coupling to chosen image/text families) and Phase 7 Red-team Sprint 3 (the test that lifts a promoted family then re-checks fusion calibration).

### F3.2 — IMDA injection mutates `queue_constraints.json` only — fusion threshold is independent

**Where it lives.** `routes/queue.py::solve` reads `con.get("hard", [])` and looks for `imda_priority_must_clear_within_sla` with `enabled=True`. The injection script (`scripts/scenario_inject.py`) flips that flag in `queue_constraints.json`. Fusion threshold is in a separate `fusion_threshold.json` (`routes/moderate_fusion.py::_threshold_path`); the queue solver never reads it.

**What goes wrong.** A student re-runs `phase_12_postimda.md` after the injection but never touches the fusion threshold (or the image `csam_adjacent` threshold). Compliance cost gets quantified at the queue layer; the auto-block side of the IMDA mandate (any post >0.40 on `csam_adjacent` must auto-blur) gets no journal entry. Student passes Phase 12 by hitting the queue half of the mandate and silently fails the moderation half.

**Caught by.** Phase 11 Constraints re-classification (must enumerate every endpoint the IMDA mandate touches — image threshold, fusion threshold, queue constraints) and Phase 12 Acceptance (must list the mandate's two sides separately and quantify both).

### F3.3 — LP infeasibility returns `feasibility: False` with a hint string; viewer renders no plan

**Where it lives.** `routes/queue.py::solve` returns `{"feasibility": False, ...}` when `result.success` is False. The viewer at `apps/web/media/index.html` reads `/queue/last_plan`; on infeasibility, no plan file is written (the `else` branch ends without `_plan_path().write_text`). The viewer's queue card stays on the previous plan.

**What goes wrong.** The IMDA mandate plus current senior-pool headcount can be infeasible (post-injection demand exceeds 12 senior reviewers × 400 min). The student runs `/queue/solve`, sees `feasibility: False`, and may not realise the viewer is stale-rendering a pre-injection plan. The journal's compliance-cost number ($0 from the prior plan) gets carried into `phase_12_postimda.md` because the field never updated.

**Caught by.** Phase 12 Acceptance pathology check (must inspect `feasibility` field directly, not the rendered card) and Phase 11 Constraints (must verify whether the LP can support the proposed hard set before committing to it).

---

## Module 4 · Drift Monitor × 3 (Sprint 4 · MLOps · Monitor)

### F4.1 — Calibration decay computed against in-sample Brier; drift signal is suppressed

**Where it lives.** `routes/drift.py::check_drift` builds `live_calib` from `ctx.image_baseline.candidates[chosen_family].per_class[c]["brier"]`. The `per_class.brier` was computed at fit time on the held-out test split inside `_train_family` (`ml_context.py`). `ref_calib` (`drift_baselines[model_id].per_class_calibration`) was computed at startup from the same `per_class.brier` (per `startup.py`).

**What goes wrong.** Reference and live Brier are both anchored on the startup-time test-split — so `calibration_decay = live - reference` is identically zero on `recent_30d` and any window that doesn't refit. The signal lights up only on the synthetic `imda_csam_mandate` and `election_cycle_drift` shifts because those re-synthesise the embedding distribution. A real production drift (degraded labels, distribution shift on incoming posts) would not be caught by this signal in tonight's scaffold.

**Caught by.** Phase 13 Drift (recognise the calibration-decay number is informative only when paired with a fresh evaluation pass; a "recent_30d Brier delta = 0" reading is a methodology artefact, not safety).

### F4.2 — `_simulate_recent_30d` is a uniform sub-sample — near-zero PSI by construction

**Where it lives.** `routes/drift.py::_simulate_recent_30d` calls `rng.choice(n, size=min(2000, n), replace=False)` and returns a slice of the reference embeddings.

**What goes wrong.** The "30-day window" never exhibits drift. A student running `/drift/check` with `window=recent_30d` will see PSI < 0.10 across every feature and conclude "no drift in production". The window is by construction a sub-sample of the reference; PSI cannot be high. The defensible interpretation is "the simulator is calm-state" — but the journal won't say that unless Phase 13 surfaces it.

**Caught by.** Phase 13 Drift signal-validity check (every drift signal must include a calm-state reference and an injected-state reference; otherwise the threshold is unfalsifiable).

### F4.3 — Universal "auto-retrain when X" is BLOCKED by route — but only via `set_count == 3` gate, not signal validity

**Where it lives.** `routes/drift.py::set_retrain_rule` accepts any `signals` list of length ≥ 1 with any `thresholds` dict. The `complete: set_count == 3` gate (`get_retrain_rules`) only counts how many `model_id`s have a rule attached, not whether the rule is sensible.

**What goes wrong.** A student sets the same rule (signals=`["psi_max"]`, thresholds=`{"psi_max": 0.25}`, cadence=weekly) for all three model IDs. The route happily accepts; `complete=true` flips green; viewer Sprint 4 lights up. The Phase 13 rubric demand — three cadences, three signals, three durations — is enforced by the rubric but not by the route.

**Caught by.** Phase 13 Drift journal (the rule body must distinguish image weekly / text daily / fusion per-incident with rationale per cadence) and `/redteam` cross-sprint (the test that swaps the text rule onto image and checks whether the system flags it).

---

## Cascade summary

The four-layer cascade — image → text → fusion → drift — propagates errors. F1.1 (image picks wrong family on macro-F1) feeds F3.1 (late-fusion was trained against that family) and F4.1 (calibration baseline anchored on that family). F2.3 (text dispatch silently prioritises `threats`/`self_harm`) corrupts the queue allocator's expected-cost calculation in `routes/queue.py::solve`. F3.2 (IMDA injection touches three independent files) corrupts the Phase 12 compliance-cost number if any one is missed. The `/redteam` cross-sprint sweep (`workflow-07-redteam.md`) is the only place every link is checked end-to-end.

## Five Trust-Plane decision moments — gap status

1. **Define what counts as harmful** (Phase 1) — open. Scaffold supplies the class taxonomy; student writes the auto-remove vs review vs creator-warn mapping.
2. **Per-class auto-remove thresholds × 10** (Phase 6 × Sprint 1 + Sprint 2) — open for 9 of 10 classes; CSAM-adjacent has a structural hard floor at 0.40 already in place.
3. **Fusion architecture** (Phase 5 multi-modal) — three architectures pre-fit; chosen-by-macro-F1 default is `early_fusion`; student picks final on Phase 5.
4. **IMDA re-classification + queue re-solve** (Phase 11 + 12 re-run) — open. Injection script ready; queue constraint flag default `enabled=False`.
5. **Three retrain rules at three cadences** (Phase 13) — open. `drift_retrain_rules.json` defaults to all-`null` rules; student fills three.

Stopping for `/todos`.
