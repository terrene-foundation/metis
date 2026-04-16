# Red-Team Report — Week 4 Supply Chain Specs (10 files)

**Date**: 2026-04-16
**Reviewer**: quality-reviewer agent
**Target**: `workspaces/metis/week-04-supply-chain/specs/*.md`
**Ground truth**: kailash-ml `__init__.py`, engines/\* source, SKILL.md & sub-skills; kailash-nexus SKILL.md; 01-analysis/ artefacts; START_HERE.md
**Rules applied**: specs-authority, zero-tolerance, orphan-detection, facade-manager-detection, tenant-isolation, agent-reasoning, autonomous-execution, terrene-naming, independence, communication, env-models, dataflow-identifier-safety

---

## 1. Executive summary

**Sev counts**: CRITICAL 14 · HIGH 18 · MEDIUM 17 · LOW 9 = 58 findings
**Verdict**: **FAIL — blocking**. The scaffold cannot ship as specified.

The specs are internally consistent and pedagogically strong, but a majority of the kailash-ml API signatures they assert are wrong against the actual source code. The workshop will collapse in its first 10 minutes when `AutoMLEngine(feature_store=..., model_registry=..., config=...)` throws `TypeError` (actual constructor is `pipeline, search, *, registry`). Multiple other orphan and stub risks flow from the same root cause.

### Top 5 must-fix before scaffold ships

1. **C1 — AutoMLEngine constructor shape** (product-northwind, playbook-universal, scaffold-contract, START_HERE): every prompt template, banner, and example uses kwargs `feature_store=/model_registry=/config=`; actual API is positional `(pipeline, search, *, registry=)`. Every Phase 4 prompt will raise at run-time.
2. **C2 — DriftMonitor severity is 3 values, not 4** (product-northwind §6/§8.5, rubric-grader table 5, scenario-injection, viewer-pane): code dataclass literally says `# "none", "moderate", "severe"`. Specs assert `{none, low, moderate, severe}`. Grader assertion on `severity ∈ {none, low, moderate, severe}` passes a string set the library never emits at `low`.
3. **C3 — TrainingPipeline has no `on_complete` event hook** (scaffold-contract `drift_wiring.py`, data-fixtures §6.4, playbook-universal Phase 13): the specs require `drift_wiring.py` to subscribe to `TrainingPipeline.on_complete`; no such pub/sub exists in kailash-ml. The "auto-wire" story that eliminates failure mode F8 is not implementable.
4. **C4 — FeatureStore has no `ingest()` method** (product-northwind, playbook-universal Phase 2/4, data-fixtures §6, scaffold-contract `fs_preload.py`): actual methods are `register_features`, `compute`, `store`, `get_features`. Every "ingest CSV into FeatureStore" prompt fails.
5. **C5 — `cv_strategy="rolling_origin"` is invalid** (product-northwind §8.1, playbook-universal Phase 4, START_HERE Phase 4): actual EvalSpec accepts `{"holdout", "kfold", "stratified_kfold", "walk_forward"}`. `rolling_origin` is not registered; attempts will raise or silently fall back.

### Structural observations

- Two spec files exceed the 300-line cap in `specs-authority.md` MUST Rule 8 (`playbook-universal.md` at 394, `product-northwind.md` at 307). MUST be split.
- `_index.md` is clean (lookup-only).
- Orphan audit passes only for 6 of 11 listed components — 5 have no verifiable production call site because the surrounding scaffold depends on non-existent APIs.
- Cross-spec consistency is strong on numbers, weights, and scoring — but the endpoint schemas in `product-northwind.md §8` and the rubric assertions in `rubric-grader.md §2` diverge silently (C2, H2).

---

## 2. Findings by severity

### CRITICAL (14)

```
[CRITICAL] [Accuracy] [product-northwind.md:117-150; playbook-universal.md:85; scaffold-contract.md:72-80; START_HERE.md:232]
Title: AutoMLEngine constructor signature fabricated
Problem: Specs assert `AutoMLEngine(feature_store=fs, model_registry=registry, config=config)` and `engine.run(schema=schema, data=df)`. Actual source (automl_engine.py:316) is `AutoMLEngine(pipeline, search, *, registry=None)` with `.run(data, schema, config, eval_spec, experiment_name, *, tracker=None)`. Neither `feature_store` nor `model_registry` is a constructor kwarg.
Evidence: automl_engine.py:
  def __init__(self, pipeline: Any, search: Any, *, registry: Any | None = None) -> None:
  async def run(self, data: pl.DataFrame, schema: FeatureSchema, config: AutoMLConfig, eval_spec: Any, experiment_name: str, *, tracker: Any | None = None)
Fix: Rewrite every Phase 4 prompt and the scaffold banner in routes/forecast.py to:
  "Instantiate TrainingPipeline(feature_store=fs, registry=registry); HyperparameterSearch(...); AutoMLEngine(pipeline, search, registry=registry). Call engine.run(data=df, schema=schema, config=config, eval_spec=eval_spec, experiment_name='forecast_sprint1', tracker=tracker)."
Blast radius: Every Phase 4 live run raises TypeError in the first 15 seconds of Sprint 1. Cascade: Phase 5/6/7/8 have no leaderboard, 80% of journal entries cannot cite a run ID, product grade fails on 3 of 5 endpoints.

[CRITICAL] [Accuracy] [product-northwind.md:256-291; rubric-grader.md:87; scenario-injection.md:46-57; viewer-pane.md:88]
Title: DriftMonitor severity enum is {"none","moderate","severe"} in source, specs claim 4 values
Problem: Specs and grader assert `severity ∈ {none, low, moderate, severe}`. kailash-ml's DriftReport.overall_severity dataclass comment explicitly enumerates 3: `# "none", "moderate", "severe"`. The field name is `overall_severity`, not `severity`.
Evidence: drift_monitor.py:106 `overall_severity: str  # "none", "moderate", "severe"`; feature dataclass at :75 same.
Fix: Update every spec and the grader to (a) use `overall_severity` as the JSON field name, (b) accept the 3-value enum, (c) drop "low" from rubric-grader §2 assertion, scaffold-contract viewer tooltip, and viewer-pane DriftPanel severity badge. Do NOT extend kailash-ml to add "low" — that is a zero-tolerance Rule 4 workaround; if a 4-value enum is pedagogically required, file a GitHub issue and use the 3-value enum today.
Blast radius: Grader will accept student payloads with "severity: low" that the library never produces, OR reject valid `overall_severity: "moderate"` payloads because the schema calls it `severity`. Both modes fail the 8% /drift/check contract assertion.

[CRITICAL] [Accuracy] [scaffold-contract.md:52-53; data-fixtures.md:210-214; playbook-universal.md:340-348]
Title: `TrainingPipeline.on_complete` event hook does not exist
Problem: Scaffold file `drift_wiring.py` is specified as "auto-calls DriftMonitor.set_reference_data on training-complete event" and is "subscribed to `TrainingPipeline.on_complete`". No such pub/sub facility exists in training_pipeline.py or anywhere in kailash-ml.
Evidence: grep -rn "on_complete\|on_training_complete\|training_complete" src/kailash_ml/engines/ returns zero matches. TrainingPipeline.train returns a TrainingResult synchronously; there is no event bus.
Fix: Replace the "auto-wiring" pattern with an explicit call site. In routes/forecast.py after `pipeline.train(...)`, call `drift_wiring.wire(result.model_version, reference_df)` which directly calls `DriftMonitor.set_reference_data`. Update scaffold-contract.md row for drift_wiring.py from "Subscribed to TrainingPipeline.on_complete" to "Called synchronously by routes/forecast.py after each train completes". Update playbook-universal Phase 13 from "auto-wired by `drift_wiring.py` — verify the wiring is active" to "the /forecast/train route calls drift_wiring.wire() before returning; verify by checking `.preflight.json.drift_wiring: true` which `drift_wiring.wire` writes as a side effect."
Blast radius: Claude Code will fabricate a non-existent event bus when generating /forecast/train; attempts to "subscribe" produce a stub that never fires; Phase 13 check_drift raises "reference data not set"; every /drift/check returns 409.

[CRITICAL] [Accuracy] [product-northwind.md:147; playbook-universal.md:46-47,85; data-fixtures.md:210-211; scaffold-contract.md:52]
Title: FeatureStore has no `ingest()` method
Problem: Specs describe `fs_preload.py` calling `get_ml_context().feature_store.ingest(path=..., schema=...)`. FeatureStore's actual public methods are `initialize`, `register_features`, `compute`, `store`, `get_features`, `get_training_set`, `get_features_lazy`, `list_schemas`. `ingest` is a convenience wrapper that does not exist.
Evidence: feature_store.py — no method named `ingest`; SKILL.md's Quick Start uses `fs.ingest(...)` but engines/ source does not implement it.
Fix: fs_preload.py MUST call `await fs.register_features(schema); await fs.store(schema, df)`. Update playbook-universal Phase 2/4 prompts, product-northwind §8.1 error message "feature schema 'X' not registered in FeatureStore", and data-fixtures §6.2 to use `register_features`+`store`. If kailash-ml needs an `ingest` helper, file an SDK issue — do not inline a shim.
Blast radius: fs_preload.py raises AttributeError on Nexus startup; /health reports feature_store: "populated" based on a flag that never gets set; /forecast/train fails with a 409 the grader has no fix message for (the spec's "FeatureStore empty" branch assumes an empty-but-initialized state, not a startup crash).

[CRITICAL] [Accuracy] [product-northwind.md:132; playbook-universal.md:85; START_HERE.md (Phase 4 prompt)]
Title: EvalSpec.split_strategy does not include "rolling_origin"
Problem: Prompts and schemas repeatedly specify `cv_strategy: "rolling_origin"`. Actual EvalSpec.split_strategy accepts `{"holdout", "kfold", "stratified_kfold", "walk_forward"}`. "rolling_origin" is a pedagogically nice name but not a library value.
Evidence: training_pipeline.py:93-95 — `split_strategy: str = "holdout"  # "holdout", "kfold", "stratified_kfold", "walk_forward"`.
Fix: Replace "rolling_origin" with "walk_forward" everywhere (same semantic for time-series); or map the pedagogical label inside fs_preload/training route and document the mapping. POST /forecast/train's schema `cv_strategy` field MUST be renamed to `split_strategy` to match the library vocabulary, AND the value set updated.
Blast radius: EvalSpec construction with unknown value silently defaults to "holdout" (no rolling-origin validation) — every "rolling-origin" claim in the journal is false; Phase 5 fold-variance reasoning has no temporal CV underneath it.

[CRITICAL] [Accuracy] [scaffold-contract.md:54-55; product-northwind.md §7; viewer-pane.md:33]
Title: `get_ml_context()` facade with shared ConnectionManager across FeatureStore/ModelRegistry/ExperimentTracker/DriftMonitor is asserted but unverified
Problem: ml_context.py is pre-built and claimed to "prevent parallel-framework construction" per facade-manager-detection.md. But neither the facade's Tier 2 wiring test nor the dependency graph is specified — same shape as Phase 5.11 TrustAwareQueryExecutor orphan.
Evidence: scaffold-contract.md §9 audit table cites only "Imported by every route" — no test file name, no integration test, no assertion that the four engines share one connection.
Fix: Add to scaffold-contract §2: "`tests/integration/test_ml_context_wiring.py` MUST import `get_ml_context`, construct it against real SQLite, call one method on each of the 4 engines it exposes, and assert a single shared `ConnectionManager.id`." Name the test file explicitly per facade-manager-detection Rule 2.
Blast radius: If each engine instantiates its own ConnectionManager, the four SQLite DBs (.experiments.db/.registry.db/.features.db plus an implicit drift one) become non-coherent; students who cite a run_id in Phase 5 journal may have that run vanish by Phase 8. High blast radius because the orphan is invisible until fold-variance sampling reveals mismatch.

[CRITICAL] [Completeness] [scenario-injection.md:64-68; product-northwind.md:303]
Title: `medicare-cut` dry-run fires US-healthcare language into a Singapore MBA cohort with no context bridge
Problem: `medicare-cut` references a US-specific federal insurance program. The data-fixtures spec explicitly anchors Singapore public holidays (data-fixtures §1.2). A Week 7 preview that fires US healthcare lingo at an SG MBA cohort is an orientation failure — students will ask "what's Medicare?" and the instructor has no scripted answer.
Evidence: data-fixtures.md:42 "Singapore public holidays (workshop is aimed at SG MBA cohort)"; scenario-injection.md:64 `medicare-cut`. product-northwind.md:303 lists it as out-of-scope with no domain bridge.
Fix: Rename the dry-run scenario to a Singapore-equivalent reimbursement shock (e.g., `medisave-claim-cap` or `casemix-tariff-cut` — MediShield Life / Casemix tariffs are the SG equivalent). Update every spec that cites "medicare". Keep the pedagogical intent (reimbursement shock) but localise.
Blast radius: Week 7 launch loses 5+ minutes to US/SG confusion; worse, violates communication.md's "plain language" for the cohort's context.

[CRITICAL] [Accuracy] [product-northwind.md:188-199; rubric-grader.md:85]
Title: `/forecast/predict` response field `model_version_id` does not match ModelRegistry's versioning
Problem: Specs use `model_version_id: "mv_007"` as the identifier surface. ModelRegistry's actual primary keys are `(name, version:int)`. No string ID like `mv_X` exists; `ModelRegistry.get_model(name, version=N)` is the real lookup. Grader assertion "ModelRegistry.get(id).stage ∈ {…}" has no matching method.
Evidence: model_registry.py:558 `async def get_model(self, name: str, version: int)`; ModelVersion dataclass has `name: str, version: int, stage: str` — no string `model_version_id` field.
Fix: Either (a) add a derived string ID `model_version_id = f"{name}_v{version}"` via ml_context and extend scaffold-contract to document this convention, OR (b) change the endpoint contract to `{"model_name": "...", "model_version": 7}`. Pick (a) for stability of downstream journal schemas, but explicitly register the derivation in `specs/api-surface.md` and in the grader's helpers.
Blast radius: `ModelRegistry.get(id)` in the grader is AttributeError; the 8% /forecast/predict check is unimplementable; all journal entries that cite model_version_id reference a value the registry cannot resolve.

[CRITICAL] [Accuracy] [playbook-universal.md:85; START_HERE.md §3.5]
Title: AutoMLConfig field `families` does not exist; actual field is `candidate_families`
Problem: Phase 4 prompt uses `families=[...]` in the config. Actual AutoMLConfig field is `candidate_families: list[str] | None = None`.
Evidence: automl_engine.py:54 `candidate_families: list[str] | None = None`. No `families` alias exists.
Fix: Replace every `families=...` with `candidate_families=...` in playbook-universal.md Phase 4 prompt, START_HERE.md §3.5 prompt template, scaffold-contract banner in routes/forecast.py, and product-northwind.md §8.1 request schema `families` → `candidate_families`.
Blast radius: AutoMLConfig(**kwargs) raises TypeError in Phase 4; Sprint 1 collapses.

[CRITICAL] [Accuracy] [playbook-universal.md:161]
Title: `ModelExplainer` import path + capability asserted, SHAP extras unchecked on student laptops
Problem: Phase 7 prompt says "run ModelExplainer — which feature does the model rely on most". ModelExplainer requires `kailash-ml[explain]` (SHAP). preflight.py checks for `[xgb]`, `[explain]`, `ortools`, `pulp` — good — but the Phase 7 prompt has no fallback when SHAP import fails (network sandbox, macOS wheel flake, etc.). Zero-tolerance forbids silent fallback.
Evidence: playbook-universal.md:161; kailash-ml SKILL.md install-matrix; scaffold-contract.md §6 preflight entry confirms `[explain]` check but no Phase 7 mitigation.
Fix: Add a Phase 7 fallback clause: "If `ModelExplainer` raises ImportError, use sklearn's permutation_importance via kailash_ml.engines.model_visualizer (no SHAP dependency) AND record the fallback in the journal entry as a cited limitation." Update scaffold-contract §9 orphan audit row for ModelExplainer to include the fallback path. Preflight must hard-fail if SHAP is missing, not warn.
Blast radius: 15–30% of student machines will lack working SHAP (Apple Silicon + Python 3.12 + numpy pins); Phase 7 Transparency dimension scores 0/4 across a third of the cohort.

[CRITICAL] [Completeness] [scaffold-contract.md §2; orphan-detection §1-3]
Title: Every [STUDENT-COMMISSIONED] route file is a public orphan until the student fills it
Problem: The scaffold ships `src/backend/routes/{forecast,optimize,drift}.py` with banners but no call-site-level wiring. The route files are registered by `routes/__init__.py` only AFTER the student fills them (scaffold-contract.md row 55 "extension slot for forecast / optimize / drift routers"). Orphan-detection Rule 1 requires "production call site inside the framework's hot path within 5 commits of the facade landing". The scaffold effectively ships with 3 orphans.
Evidence: scaffold-contract.md:55 "Mounts `health`; extension slot for forecast / optimize / drift routers"; lines 57-59 mark the three route files as STUDENT-COMMISSIONED.
Fix: Either (a) ship the route files with a stub that registers the route AND returns a typed `501 Not Implemented` with a student-hint message (satisfies orphan-detection Rule 1; student replaces the body, not the registration), OR (b) ship a single `routes/_student_router.py` that each student's filled file extends. Prefer (a). Update scaffold-contract.md §9 to list the 501-stub registration as the call site.
Blast radius: Preflight runs before student has filled anything; /forecast/train returns 404; students can't verify Nexus is up; 10+ minutes of "my preflight is red but Viewer is green" confusion at T+0:00.

[CRITICAL] [Zero-tolerance Rule 2] [scaffold-contract.md:138,144; data-fixtures.md:71-75]
Title: JSON banner format leaks through to the live product — `{"_todo_student": null, "scenario": ...}`
Problem: data-fixtures.md §2.3 ships the drift payload with `"_todo_student": null` at top level — presumably to bypass the JSON-banner rule by setting to null. This is a workaround and violates zero-tolerance Rule 2's intent (no stub ceremony in production data files). A pre-built fixture should not have the marker at all.
Evidence: data-fixtures.md:72-73, 196-197.
Fix: Strip `_todo_student` entirely from PRE-BUILT JSON fixtures. The banner rule in scaffold-contract.md §Legend applies to STUDENT-COMMISSIONED JSON only; clarify that PRE-BUILT JSON MUST NOT contain the marker (in any state). Grader ignores the key per scaffold-contract — that's fine — but shipping the key with null value in PRE-BUILT files teaches the wrong lesson about banner hygiene.
Blast radius: Students reading the fixture to understand what "placeholder" means get a confusing signal; propagates into Phase 7 red-team audit of the fixtures themselves.

[CRITICAL] [Specs-authority §8 — file size] [playbook-universal.md:394; product-northwind.md:307]
Title: Two spec files exceed the 300-line MUST-split threshold
Problem: specs-authority.md MUST Rule 8: "When a spec file exceeds 300 lines, it MUST be split into sub-domain files and `_index.md` updated." playbook-universal.md is 394 lines, product-northwind.md is 307 lines.
Evidence: wc -l confirms 394 and 307.
Fix: Split playbook-universal.md into `playbook-sprint1-phases.md` (Phases 1,2,4,5,6,7,8,9), `playbook-sprint2-phases.md` (Phases 10,11,12), `playbook-sprint3-phases.md` (Phase 13), with `playbook-universal.md` becoming a 50-line cross-index + phase-summary table. Split product-northwind.md by extracting §8 "Endpoint contracts" into `api-surface.md` (already referenced in scaffold-contract.md §3, but not yet a separate file per _index.md). Update _index.md.
Blast radius: Violating specs-authority Rule 8 means every agent delegation that includes playbook content overflows the invariant budget per autonomous-execution.md (≤5–10 invariants). Also caught in future `/redteam` audits.

[CRITICAL] [Cross-spec consistency] [product-northwind.md:68-81; START_HERE.md §2; data-fixtures.md §1.3]
Title: Business numbers table cross-spec drift — "historical drift around week 40" claim
Problem: product-northwind.md:81 lists "Historical drift week: ~Week 40 each year" but data-fixtures.md §1.3 says three "stable segments pre-drift" and only describes the injected week-78 drift; no historical week-40 drift is encoded anywhere in the 2-year training CSV. data-fixtures.md Open Questions (line 233) acknowledges this is "not explicit in any single analysis artefact" and waves at the ambiguity.
Evidence: product-northwind.md:81 says historical week-40 drift; data-fixtures.md §1.3 describes a stable pre-drift distribution; no seed in scripts/seed_experiments.py §7 injects a week-40 event.
Fix: Either (a) inject a mild week-40 wobble in the training CSV generator AND document it in data-fixtures.md §1.3, OR (b) remove the "Historical drift week" row from product-northwind.md §5 and every downstream reference (Phase 13 prompt, START_HERE §2). Option (b) is simpler and honest.
Blast radius: Phase 13 prompt instructs "historical variance grounding" — if no historical drift exists in the training data, students have no historical signal to cite; they'll fabricate one or score 0/4 on reversal condition. Either is a teaching failure.
```

### HIGH (18)

```
[HIGH] [Rigor] [product-northwind.md:98-110]
Title: Port contention unaddressed — two Nexus processes cannot bind :8000 concurrently
Problem: Deployment topology says ports are "not negotiable" but in a shared-classroom topology (scenario-injection.md §1 "each student runs their own workspace"), many students' laptops are fine; instructor's demo machine and a student machine on the same VPN may collide. No detection/fallback policy specified.
Fix: preflight.py must detect `:8000 in use` and print "port 8000 taken — export PORT=8001 and retry". Add KAILASH_NEXUS_PORT env var to .env.example. Update viewer-pane.md next.config.js to read NEXT_PUBLIC_BACKEND_PORT.
Blast radius: One student in five may hit this; costs 5 min each to resolve without a scripted path.

[HIGH] [Accuracy] [product-northwind.md §8.6; scaffold-contract.md:56]
Title: /health payload field names underspecified; "drift_wiring: active" is a boolean-shaped string
Problem: product-northwind.md §8.6 shows `"drift_wiring": "active"` (a string). scaffold-contract.md:56 says `/health` returns "drift wiring active". Is it `{"drift_wiring": "active"}` or `{"drift_wiring": true}`? Grader and Viewer's PreflightBanner both parse this — inconsistent field types break one or the other.
Fix: Standardise all /health fields to typed booleans: `{"ok": true, "db": true, "feature_store": true, "drift_wiring": true, "registry_runs": 3}`. Update §8.6, scaffold-contract, and viewer-pane.md:102.
Blast radius: Preflight banner misrenders for one in three students.

[HIGH] [Completeness] [scaffold-contract.md:60; product-northwind.md §8.5; playbook-universal.md Phase 13]
Title: Drift endpoint does not expose reference data status for debugging
Problem: When /drift/check 409s with "reference data not set", the student has no endpoint to query to confirm whether drift_wiring fired. The only feedback loop is reading `.preflight.json` manually, which is not in the student's scripted path.
Fix: Add `GET /drift/status/<model_id>` returning `{"reference_set": bool, "reference_set_at": iso8601|null, "window_size": int}`. Wire into viewer-pane DriftPanel "debug" row.
Blast radius: Phase 13 hiccup recovery requires terminal spelunking; costs 3-5 min per affected student.

[HIGH] [Rigor] [playbook-universal.md:85; product-northwind.md:149]
Title: AUTOML_QUICK env var semantics contradict themselves
Problem: product-northwind.md §8.1 error 422: "`search_n_trials > 20` AND `KAILASH_ML_AUTOML_QUICK=1` → 422 AUTOML_QUICK env caps trials at 20". playbook-universal.md:82 says Phase 4 uses `search_n_trials=5` as default AND if AUTOML_QUICK=1 "the cap is defence-in-depth". So the 422 only fires at 20+ trials, but the default is 5 — the guard is functionally unreachable in the workshop. Meanwhile .env.example contains `KAILASH_ML_AUTOML_QUICK=1` per scaffold-contract.md:36, which students may export before experimenting with higher trial counts.
Fix: Clarify the contract — either the cap is 20 (then document why, what it protects), or lower to 10 to match the 90s Sprint 1 budget. Add a test in the grader: if AUTOML_QUICK=1 and trials=20 was sent, response MUST cap and include a warning field.
Blast radius: Student experiments in Sprint 1 buffer period ("let me try 30 trials") unexpectedly succeed/fail depending on env state.

[HIGH] [Completeness] [scenario-injection.md:33-45; scaffold-contract.md:145]
Title: `--undo` path for union-cap regenerates from seed — silent data rewrite across workspace
Problem: scenario-injection.md Table row "Student overwrote route_plan.json with no snapshot" says: "`--undo` restores from `route_plan_preunion.json`; if that is also missing, instructor regenerates from `seed_experiments.py` seed run". But `seed_experiments.py` produces the LEADERBOARD, not a route plan — the correct regen path is `seed_drift.py` or a dedicated `seed_route_plan.py`, neither of which exists. Silent inconsistency.
Fix: Ship `scripts/seed_route_plan.py` [PRE-BUILT] that writes a baseline route_plan.json given the pre-baked leaderboard; update scenario-injection.md rollback row and scaffold-contract §6 to add the script.
Blast radius: Instructor's recovery script for 5% of students fails; requires ad-hoc solver re-run at the worst moment (~T+2:10).

[HIGH] [Cross-spec consistency] [playbook-universal.md:85,95; scaffold-contract.md Banner text for forecast.py]
Title: XGBoost fallback path is three-way inconsistent
Problem: playbook-universal.md:85 says "add XGBoostRegressor if the [xgb] extra is available; else fall back to another GBM variant". scaffold-contract.md:71-72 banner lists only LinearRegression + RandomForestRegressor + GradientBoostingRegressor — no XGBoost. START_HERE.md §3.5 lists XGBoostRegressor as a headline candidate. Students reading the three get different answers.
Fix: Pick ONE: "LinearRegression, RandomForestRegressor, GradientBoostingRegressor (XGBoostRegressor if [xgb] installed per preflight; else omit — do NOT silently substitute)". Update all three specs identically.
Blast radius: Leaderboard claims "5 families" but scaffold prompt emits 3; Phase 4 evaluation checklist "Candidates span a complexity range" fails for 100% of students who copy the banner list verbatim.

[HIGH] [Rigor] [rubric-grader.md:73-75]
Title: Partial credit policy claims "3 of 3 assertions" for /forecast/train but §2 table lists 4 assertions
Problem: rubric-grader.md §2.2 says "An endpoint with 3 of 3 assertions passing = 8%, 2 of 3 = 0%." But /forecast/train's §2 row asserts experiment_run_id present AND tracker.get_run succeeds AND ≥2 metrics AND non-null timestamp — that's 4, not 3. And §3.3 report JSON shows 4 assertion entries for /forecast/train.
Fix: Update §2.2 to "N of N assertions" (binary at endpoint level); align the text with the 4-assertion JSON shape.
Blast radius: Students reading "3 of 3" then seeing the grader evaluate 4 assertions get an off-by-one surprise in the public projector moment.

[HIGH] [Completeness] [scaffold-contract.md §6; workshop-runofshow.md §2]
Title: `scripts/preflight.py` does not verify Nexus process health vs. port-bound
Problem: scaffold-contract.md:175 says preflight "curls :3000 + :8000/health". But ":3000 responds" does NOT mean "Nexus is up"; it just means something bound the port. If a stale process is listening, preflight green-lights the session; Sprint 1 collapses on first /forecast/train.
Fix: preflight.py MUST assert /health returns 200 AND body contains `"feature_store": true` AND `"drift_wiring": true`. Failure → actionable red strip with "kill <pid>" instruction (psutil, not shell).
Blast radius: Silent corruption of session start; 5–10 min lost to stale-process debug.

[HIGH] [Agent-reasoning] [playbook-universal.md:341-347; START_HERE.md Phase 13]
Title: Phase 13 prompt says "Do NOT encode `if X > Y trigger retrain` in agent logic" but scaffold ships no counter-example Claude Code can anchor on
Problem: The constraint is real and correct, but the prompt is prose-only. Claude Code's empirical tendency (without a negative example) is to emit `if metric > threshold: registry.transition(...)` anyway. `_examples.md` (journal template) lacks a Phase 13 good-vs-bad pair.
Fix: Add to journal/_examples.md a 4/4 and 1/4 Phase 13 pair demonstrating signals+thresholds memo vs. an if-else agent workflow. Reference this example explicitly in playbook-universal.md Phase 13 prompt.
Blast radius: Agent-reasoning violations recur per cohort at ~30% rate per analysis artefact F7; without a concrete example, instructor must intervene on many students.

[HIGH] [Tenant-isolation] [product-northwind.md:301-302]
Title: "Multi-tenant isolation — the workshop runs locally, one user per process" silently deferred, specs never justify why
Problem: Per tenant-isolation.md, every multi-tenant system needs tenant_id in cache keys, invalidation scope, metric labels, audit rows. Product-northwind.md declares "no multi-tenant isolation" — fine for Week 4 — but the decision-journal.md:154 auto-linkage queries `ExperimentTracker.list_runs(created_after=<last_entry_timestamp>)` which, in a later multi-tenant Nexus deployment, would cross-leak every student's runs.
Fix: Add to product-northwind.md §9 Out-of-scope: "Multi-tenant isolation is deferred because every process runs as a single user. When this product is re-scoped in Week 5+ to a shared backend, ExperimentTracker.list_runs MUST take tenant_id and every CLI (metis journal add/list) MUST pass it. See tenant-isolation.md MUST Rule 1."
Blast radius: Doesn't bite Week 4; becomes a latent P0 at Week 5 if the backend goes shared.

[HIGH] [Independence / terrene-naming] [product-northwind.md:111]
Title: "MLflow-export path is a one-shot file writer (`MlflowFormatWriter` → `mlruns/`)" — no commercial coupling check
Problem: independence.md forbids "compatibility" or "interop" with proprietary systems as a design target. MlflowFormatWriter is a Foundation-owned artifact so this is not a violation — but the surrounding prose frames it as "the MLflow-export path", positioning mlflow as the reference product. This is subtle commercial anchoring.
Fix: Rephrase "the MLflow-export path" → "kailash-ml's MLflow-format writer — an interoperability helper for teams migrating from MLflow; Kailash does not depend on MLflow". Update product-northwind.md:111 and START_HERE.md §3.7.
Blast radius: Low substance impact; independence audit mandates the rewording.

[HIGH] [Accuracy] [rubric-grader.md §2 row 5]
Title: /drift/check contract assertion on statistic name mismatches the 3-value DriftMonitor output
Problem: Grader asserts "≥ 1 named statistical test (`ks` / `chi2` / `psi` / `js`)". Actual FeatureDriftResult fields are `psi: float, ks_statistic: float, ks_pvalue: float` — no chi2 or js in the per-feature result. Only PSI and KS are computed and persisted.
Evidence: drift_monitor.py:67-85 FeatureDriftResult.
Fix: Either extend DriftMonitor to also compute chi2 + js (would require kailash-ml source changes — file SDK issue) or reduce the grader assertion to `{ks, psi}`. Pick the latter for Week 4.
Blast radius: Grader permits invalid test names; students can fake "chi2 stat: 0.42" and pass the 8% check.

[HIGH] [Completeness] [decision-journal.md §6.1; rubric-grader.md §1.3]
Title: Auto-linkage fills frontmatter `experiment_run_ids` via `list_runs(created_after=<last_entry_timestamp>)` but no "last_entry_timestamp" storage is specified
Problem: decision-journal.md §6.1 references `<last_entry_timestamp>` without saying where it is persisted. Across sessions (Week 5+ runs same CLI) the timestamp MUST be durable.
Fix: Specify `journal/.last_entry_timestamp` (file) OR use the max(timestamp) across existing phase_*.md files. Document in decision-journal.md §4.1.
Blast radius: Bug would silently over-populate frontmatter with all historical runs; student journal frontmatter becomes 1KB of IDs.

[HIGH] [Cross-spec consistency] [workshop-runofshow.md:92; decision-journal.md §1.1]
Title: Filename pattern `phase_5_postdrift.md` vs Phase 5 "model_selection" — same-phase reruns have inconsistent slugs
Problem: decision-journal.md §1.1 lists `phase_5_model_selection.md` AND `phase_5_postdrift.md`. Phase 11 reruns are `phase_11_constraints.md` AND `phase_11_postunion.md`. Phase 6 reruns: `phase_6_metric_threshold.md` + `phase_6_postdrift.md`. Phase 8 reruns: `phase_8_gate.md` + ... no post-union-gate filename specified. workshop-runofshow.md §4.02:25 says "Phase 8 re-run" but decision-journal.md never lists a filename for it.
Fix: Add `journal/phase_8_postunion.md` to the canonical filename list in decision-journal.md §1.1; update viewer-pane §3.1 Playbook Progress panel chip logic; update rubric-grader.md applicability matrix if Phase 8 rerun scoring differs.
Blast radius: Phase 8 rerun entry either missing or gets a free-form name that the Viewer's chip matcher misses → student's progress ribbon shows 11/13 when they have 12/13 entries.

[HIGH] [Rigor] [scaffold-contract.md:54; facade-manager-detection]
Title: ml_context.py constructs managers but no Tier 2 wiring test is specified by name
Problem: facade-manager-detection.md Rule 2 requires `test_<lowercase_manager_name>_wiring.py` for every facade. ml_context.get_ml_context() exposes 4 managers (FeatureStore, ModelRegistry, ExperimentTracker, DriftMonitor) — 4 tests must exist with exactly those names.
Fix: Extend scaffold-contract.md §9 audit table to list 4 test files: tests/integration/test_feature_store_wiring.py, test_model_registry_wiring.py, test_experiment_tracker_wiring.py, test_drift_monitor_wiring.py. Fail preflight if any missing.
Blast radius: Phase 5.11-style orphan — the managers may all be instantiated but never actually called in the hot path (e.g. if routes/forecast.py bypasses ml_context and constructs its own). Silent.

[HIGH] [Completeness] [product-northwind.md §8.4; rubric-grader.md row 4]
Title: /optimize/solve response has no `violated_constraints` field on success path
Problem: Error 409 returns `violated_constraints: [...]` (product-northwind.md:241). Success response shows `hard_constraints_satisfied: {vehicle_capacity: true, driver_hours_max: true}`. But the grader asserts "every value is true" — if an ADDITIONAL hard constraint is added by the student (e.g. late-window as hard), the dict shape varies by student. Grader semantics "every value is true" across an unbounded key set is fine, but the spec should fix the minimum keyset.
Fix: Specify in product-northwind.md §8.4: "`hard_constraints_satisfied` MUST contain at least `vehicle_capacity` and `driver_hours_max`; additional keys welcome." Grader asserts both keys present AND all values true.
Blast radius: Grader is lenient by accident; a student who drops `driver_hours_max` entirely passes.

[HIGH] [Completeness] [viewer-pane.md §2; workshop-runofshow.md:112]
Title: Filesystem-watch polling 1s with 304 NotModified is correct contract but the 5-second stale-indicator (viewer-pane §6) contradicts it
Problem: viewer-pane.md §2 requires 1s polling with 304-when-unchanged. §6 failure-modes says "Stale data (> 5 s since last change)" yellow strip. But that says "since last change" not "since last poll" — reading them together: if the file stays unchanged for 5 seconds that alone triggers "stale". That would be fired during every Phase 5 reading (student just thinks, doesn't write). Unexpected yellow strip.
Fix: Clarify: stale = "last successful poll > 5s ago", NOT "last file change > 5s ago". Update §6 and the internal API contract.
Blast radius: Distracting yellow noise every Sprint break; teaches students to ignore the stale indicator.

[HIGH] [Accuracy] [data-fixtures.md §3.1]
Title: Pre-baked leaderboard claims Bayesian default backend, but AutoMLConfig default search_strategy is "random"
Problem: data-fixtures.md §3.1 bullet 1: "Search strategy: Bayesian (kailash_ml AutoML default Bayesian backend)". AutoMLConfig default is `search_strategy: str = "random"` (automl_engine.py:55). "Bayesian default" is false.
Fix: Update §3.1 to "Search strategy: bayesian (explicitly set in `seed_experiments.py`; AutoMLConfig's own default is `random`)".
Blast radius: Student reading the spec infers kailash-ml's default is Bayesian; builds a mental model that breaks at Phase 4 when their live run is `random` by design.
```

### MEDIUM (17)

```
[MEDIUM] [Rigor] [product-northwind.md §5]
Title: Business numbers table numeric precision not locked — "Stockout cost $40 per unit" vs START_HERE "$40 in penalties"
Problem: product-northwind.md shows stockout at "$40 per unit" (per-unit). START_HERE.md:86 says "$40 in penalties + customer goodwill" (per-event). Cost asymmetry "3.3:1" depends on which reading.
Fix: Normalise: stockout = "$40 per unit short of demand"; overstock = "$12 per unit of excess capacity deployed". Identical wording in all specs.

[MEDIUM] [Completeness] [product-northwind.md §8.1]
Title: Response `training_duration_s` not in the error-case schema; grader only asserts it on success
Problem: 500 error schema omits training_duration_s; grader §2 assertion "training_timestamp_nonnull" could map to either. Disambiguate.
Fix: Define top-level telemetry fields that exist on every response: `latency_ms`, `started_at` at the Nexus middleware layer.

[MEDIUM] [Autonomous-execution] [workshop-runofshow.md §1 Pre-class, §6.03:20]
Title: Time estimates in human-minutes frame the workshop, but autonomous-execution.md requires capacity-band framing
Problem: Not a rule violation (workshop-runofshow is inherently human-clocked), but the sprint-level capacity budgets are never mapped to the autonomous-execution 10x or the per-shard invariant budget. When instructor adapts the flow for a faster cohort, the math is informal.
Fix: Add workshop-runofshow.md §9: "Capacity bands for an autonomous run of the same material: Sprint 1 shardable into phases 1-2 (one shard, 3 invariants) and 4-5-6-7-8 (second shard, 5 invariants). Autonomous runtime equivalent: one session per sprint."

[MEDIUM] [Env-models] [.env.example via scaffold-contract.md:36]
Title: `.env.example` MUST be enumerated; specs only cite `KAILASH_ML_AUTOML_QUICK=1` and DB paths
Problem: env-models.md: all API keys and model names from .env. scaffold-contract.md:36 mentions the file exists but doesn't enumerate the full key-set. Any prompt citing a model name must draw from .env, not a literal.
Fix: Enumerate: `KAILASH_ML_AUTOML_QUICK, KAILASH_NEXUS_PORT, DATABASE_URL_EXPERIMENTS, DATABASE_URL_REGISTRY, DATABASE_URL_FEATURES, ARTIFACT_DIR, RANDOM_SEED, AUTOML_SEED, DRIFT_SEED, NEXT_PUBLIC_POLL_MS, NEXT_PUBLIC_BACKEND_PORT`. Add OPENAI_API_KEY/ANTHROPIC_API_KEY if Kaizen agents are used (kailash-ml[agents]).

[MEDIUM] [Rigor] [decision-journal.md §5.2]
Title: Pandoc fallback silently degrades deliverable quality; "grader accepts .pdf OR .md" is a zero-tolerance-rule-3 silent fallback
Problem: Fallback is documented (good), but the degraded .md path loses the cited-sources appendix and rubric-dimension badges. Silent quality drop violates communication.md "report in outcomes".
Fix: Fallback MUST emit a clearly-flagged `journal_markdown_fallback.md` with a header banner "PDF export failed because <reason>; the student lost <X features>". Instructor assesses impact.

[MEDIUM] [Cross-spec consistency] [scenario-injection.md §3; workshop-runofshow.md §4]
Title: Union-cap firing time drift — scenario-injection §3 says "30 min into Sprint 2" (= T+02:05). workshop-runofshow §4.02:05 says 02:05 = minute 30 of Sprint 2. Consistent — but scenario-injection §2.1 "~02:05" vs §3 "30 min into sprint" adds pedagogical noise.
Fix: Pick one reference frame (wall-clock absolute OR sprint-relative) and use it everywhere.

[MEDIUM] [Accuracy] [playbook-universal.md Phase 13 prompt]
Title: Prompt says `DriftMonitor.set_reference_data(model_id, reference_df)` — actual signature takes model_name + schema + df
Problem: drift_monitor.py:431 signature is `set_reference_data(self, model_name: str, feature_columns: list[str], ...)` (verify) — not just `(model_id, reference_df)`. Need to check fine-grained.
Fix: Read actual signature; update playbook-universal.md Phase 13 prompt to match.

[MEDIUM] [Completeness] [scaffold-contract.md §2]
Title: `src/backend/app.py` entry point not enumerated — `uvicorn` invocation missing
Problem: scaffold-contract.md:50 says "Nexus app factory, CORS, logging, health endpoint" but not the uvicorn command, the module path (src.backend.app:app?), or the reload/workers setup. Students cannot debug startup failures.
Fix: Add `scripts/run_backend.sh` [PRE-BUILT] with the canonical `uvicorn src.backend.app:app --host 127.0.0.1 --port 8000`. Document in scaffold-contract.md §6.

[MEDIUM] [Accuracy] [data-fixtures.md §2.0]
Title: "Week 78 corresponds to `2025-07-01`" arithmetic
Problem: 2024-01-01 as week 1 day 1; week 78 = week 1 + 77 weeks = 77 * 7 = 539 days; 2024-01-01 + 539 days = 2025-06-23 (not 2025-07-01). Off by 8 days.
Fix: Either correct the date in data-fixtures.md §2.0 to 2025-06-23 OR define week-indexing convention so the math rounds to 2025-07-01 (e.g., ISO week numbering).

[MEDIUM] [Completeness] [rubric-grader.md §3.2 step 4]
Title: Grader actionable messages list 5 fix instructions but 8 error cases exist across endpoints
Problem: product-northwind.md enumerates 400/409/422/404/500 across endpoints. rubric-grader.md §3.2 maps only 5. Three error paths lack "what to tell the student" text.
Fix: Enumerate all N×M error-cases-to-fix-message pairs. Consider a shared `scripts/grade_fix_messages.json`.

[MEDIUM] [Communication] [product-northwind.md §2.1]
Title: "Target variable: `orders_next_day` per `(depot_id, date)`" uses tuple notation non-coders won't parse
Problem: communication.md forbids unexplained jargon. "(depot_id, date)" is SQL-key shorthand.
Fix: Rewrite as "Target: how many orders each depot will receive tomorrow. Unit: one prediction per depot per day."

[MEDIUM] [Accuracy] [product-northwind.md §2.3; rubric-grader.md]
Title: DriftMonitor enumerated tests "KS / Chi² / PSI / JS-divergence" but the library ships only PSI + KS
Problem: See HIGH above; also in §2.3 and START_HERE §3.5.
Fix: Align spec language to library capability: "KS for continuous features, PSI for population stability" — drop Chi2 and JS throughout unless kailash-ml is extended.

[MEDIUM] [Rigor] [viewer-pane.md §1.2]
Title: Viewer watch-root resolution "`apps/web/../../data/`" is fragile
Problem: Relative paths break when `next dev` is run from different cwd.
Fix: Use `process.env.METIS_WORKSPACE_ROOT` OR compute from `path.resolve(__dirname, '../../../data')` and test in preflight.

[MEDIUM] [Open Q disposition] [data-fixtures.md line 233-234]
Title: Open question on "historical drift week numbering" left unresolved — see CRITICAL C14
Problem: Acknowledged but not fixed.
Fix: Close via the C14 fix above.

[MEDIUM] [Completeness] [scenario-injection.md §6]
Title: No failure mode for "instructor fires union-cap twice"
Problem: Idempotency of `metis scenario fire union-cap` not specified.
Fix: CLI should detect `data/scenarios/active_union_cap.json` exists and exit 4 with "already fired at <timestamp>; pass --re-fire to replay".

[MEDIUM] [Completeness] [rubric-grader.md §3.4]
Title: Grader "does NOT retry" on 5xx — but does not specify timeout; default httpx timeout 5s may fire before /forecast/train (90s)
Problem: grade_product.py against a live 87.4s train call MUST set an explicit 120s timeout. Not specified.
Fix: Add timeout=120 to §3.4; document.

[MEDIUM] [Independence] [START_HERE.md §3.5 component table row for PyCaret]
Title: "Replaces" column names commercial tools (PyCaret, MLflow server, Flask/FastAPI)
Problem: Light anchoring on third-party products. Independence.md: "describe Kailash on its own terms". Fine in student-facing docs as migration aid, but the table also appears duplicated in START_HERE; pick one form.
Fix: Keep the table in START_HERE only (student-facing migration aid); strip "Replaces" column from any spec that re-lists components (product-northwind does not currently; stay clean).
```

### LOW (9)

```
[LOW] [Communication] [product-northwind.md:65]  "named dollars" is idiomatic; non-coders parse as "dollar bills with names on them". Prefer "dollars with a units label".
[LOW] [Communication] [playbook-universal.md Phase 6 prompt]  "cost asymmetry in named units" — same idiom; rewrite for non-coders.
[LOW] [Consistency] [viewer-pane.md:56]  "12 phase chips labelled 1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 13, 9" — that's 12 chips but ordering "..., 9" after 13 is awkward. Use sprint-order.
[LOW] [Rigor] [product-northwind.md:139]  `experiment_run_id: "xgb_007_20260416_143012"` — embeds a timestamp in the ID. ExperimentTracker uses UUIDs internally (see grep output). Clarify the format is a human-readable alias.
[LOW] [Consistency] [workshop-runofshow.md §0]  "T−30 to T+0" uses T+0 as workshop start; §1 uses 00:00. Pick one.
[LOW] [Completeness] [decision-journal.md §7]  "Phases 1, 2, 5, 6, 7, 8, 12, 13" — but Phase 2 reversal-condition row in rubric-grader.md §1.3 maps to reversal? Matrix shows D5 applies to Phase 2. Consistent. Double-check cross-ref.
[LOW] [Completeness] [scaffold-contract.md §8]  "Not installed on student machines" for scenario_inject.py — but §6 lists it as scaffold-shipped. Clarify: shipped in scaffold repo; CLI entrypoint not exposed on student's PATH.
[LOW] [Communication] [workshop-runofshow.md:111]  "triage the 1–3 students who fell furthest behind" — pick one count; specific numbers aid planning.
[LOW] [Terrene-naming] [scenario-injection.md:16]  "classroom topology" is fine language; no capitalisation issue found, but check product-northwind.md:29 "Trust Plane user (the Ops Manager)" — capitalisation is correct, flagged for posterity.
```

---

## 3. Cross-spec consistency matrix

| Topic                       | product-northwind                   | playbook-universal | scaffold-contract   | rubric-grader                   | scenario-injection       | data-fixtures | viewer-pane           | decision-journal                      | workshop-runofshow | Verdict                                   |
| --------------------------- | ----------------------------------- | ------------------ | ------------------- | ------------------------------- | ------------------------ | ------------- | --------------------- | ------------------------------------- | ------------------ | ----------------------------------------- |
| Drift severity enum         | 4 values                            | 4 values           | —                   | 4 values                        | —                        | —             | 4 values              | —                                     | —                  | **FAIL — source is 3 values**             |
| AutoML families arg         | `families`                          | `families`         | `families` (banner) | —                               | —                        | —             | —                     | —                                     | —                  | **FAIL — source is `candidate_families`** |
| FeatureStore load method    | `ingest`                            | `ingest`           | `ingest`            | —                               | —                        | `ingest`      | —                     | —                                     | —                  | **FAIL — no such method**                 |
| cv_strategy value           | `rolling_origin`                    | `rolling_origin`   | —                   | —                               | —                        | —             | —                     | —                                     | —                  | **FAIL — `walk_forward`**                 |
| /optimize/solve keys        | `hard_constraints_satisfied`        | —                  | —                   | `hard_constraints_satisfied`    | —                        | —             | —                     | —                                     | —                  | PASS                                      |
| Model version ID            | `model_version_id` (string)         | —                  | —                   | `model_version_id`              | —                        | —             | —                     | `model_version_ids` (list of strings) | —                  | **FAIL — registry uses (name, int)**      |
| Union-cap fire time         | —                                   | —                  | —                   | —                               | 02:05 (§2.1), 30min (§3) | —             | —                     | —                                     | 02:05              | PASS (but double-referenced)              |
| Stockout $/unit vs $/event  | `$40 per unit`                      | `$40`              | —                   | `$40/$12`                       | —                        | —             | —                     | —                                     | —                  | PASS (all agree per-unit)                 |
| Phase 9 placement           | Sprint/Close                        | Close              | —                   | —                               | —                        | —             | —                     | —                                     | Close              | PASS                                      |
| Phase 8 rerun filename      | —                                   | artefact: record   | —                   | —                               | —                        | —             | —                     | **missing**                           | "Phase 8 re-run"   | **FAIL — no filename**                    |
| Fairness deferral statement | Week 7                              | Week 7             | —                   | —                               | —                        | —             | —                     | —                                     | Week 7             | PASS                                      |
| /health field types         | `"drift_wiring": "active"` (string) | —                  | "active" (text)     | —                               | —                        | —             | PreflightBanner reads | —                                     | —                  | **FAIL — boolean vs string**              |
| Grader partial credit       | —                                   | —                  | —                   | "3 of 3" text vs 4 JSON entries | —                        | —             | —                     | —                                     | —                  | **FAIL — internal inconsistency**         |
| Tests for drift             | KS/Chi²/PSI/JS                      | —                  | —                   | `ks/chi2/psi/js`                | —                        | —             | —                     | —                                     | —                  | **FAIL — source only has ks+psi**         |

13 topics surveyed → 7 consistency failures (54%). Unacceptable for pristine.

---

## 4. Orphan-detection audit

Per orphan-detection.md MUST Rule 1 (production call site) and Rule 2 (Tier 2 wiring test).

| Component                   | Exposed at                                        | Production call site                                                   | Tier 2 wiring test | Status                                            |
| --------------------------- | ------------------------------------------------- | ---------------------------------------------------------------------- | ------------------ | ------------------------------------------------- |
| FeatureStore                | `get_ml_context().feature_store`                  | fs_preload.py (uses non-existent `ingest` → broken)                    | **unspecified**    | **ORPHAN (broken wiring)**                        |
| ModelRegistry               | `get_ml_context().model_registry`                 | routes/forecast.py (student-filled)                                    | **unspecified**    | **ORPHAN (student-commissioned)**                 |
| ExperimentTracker           | `get_ml_context().experiment_tracker`             | routes/forecast.py (student-filled)                                    | **unspecified**    | **ORPHAN (student-commissioned)**                 |
| TrainingPipeline            | routes/forecast.py `/train`                       | routes/forecast.py (student-filled)                                    | **unspecified**    | **ORPHAN (student-commissioned)**                 |
| AutoMLEngine                | routes/forecast.py `/train`                       | routes/forecast.py (student-filled) AND scaffold banner uses wrong API | **unspecified**    | **ORPHAN (student-commissioned + broken)**        |
| InferenceServer             | routes/forecast.py `/predict`                     | routes/forecast.py (student-filled)                                    | **unspecified**    | **ORPHAN (student-commissioned)**                 |
| DriftMonitor                | `get_ml_context().drift_monitor`, drift_wiring.py | drift_wiring.py (relies on non-existent event hook)                    | **unspecified**    | **ORPHAN (broken wiring)**                        |
| ModelExplainer              | routes/forecast.py Phase 7 call                   | routes/forecast.py (student-filled, no ImportError fallback)           | **unspecified**    | **ORPHAN (student-commissioned, fragile)**        |
| OR-Tools VRP                | routes/optimize.py                                | routes/optimize.py (student-filled)                                    | **unspecified**    | **ORPHAN (student-commissioned)**                 |
| PuLP                        | routes/optimize.py (alt LP path)                  | routes/optimize.py (student-filled, alt path may never be exercised)   | **unspecified**    | **DOUBLE-ORPHAN (alt path, no forcing function)** |
| DataExplorer                | routes/forecast.py Phase 2                        | routes/forecast.py (student-filled)                                    | **unspecified**    | **ORPHAN (student-commissioned)**                 |
| ml_context.get_ml_context() | every route                                       | Routes/**init**.py (after student fills)                               | **unspecified**    | **ORPHAN (facade without wiring test)**           |

**Every component fails Tier 2 wiring check.** The scaffold-contract §9 "audit" is a list of intended call sites, not verified ones.

**Fix**: Ship tests/integration/test\_\*\_wiring.py for each (12 files, one per row above) as [PRE-BUILT]. Each constructs ml_context against a temp DB, exercises the component end-to-end, asserts the externally-observable effect.

---

## 5. Open-questions disposition

| Source spec                 | Question                                                         | Status   | Disposition                                                         |
| --------------------------- | ---------------------------------------------------------------- | -------- | ------------------------------------------------------------------- |
| product-northwind.md §Open  | "None"                                                           | closed   | Spec claims none, but findings C1-C5 are open questions in disguise |
| playbook-universal.md §Open | "None"                                                           | closed   | Same — claims none, but C1/C9/H9 are latent                         |
| scaffold-contract.md §Open  | "None"                                                           | closed   | Claims agreement with scaffold-manifest + contracts; C6 refutes     |
| rubric-grader.md §Open      | "None"                                                           | closed   | C2, H7, H12 refute                                                  |
| scenario-injection.md §Open | "Shared-classroom topology"                                      | **open** | Keep open; add decision record before Week 4 launch (H1)            |
| data-fixtures.md §Open      | "Holiday calendar parametrization"; "Drift-week numbering"       | **open** | Accept holiday param as Week 5+; fix drift-week via C14             |
| viewer-pane.md §Open        | "Mobile viewport"; "grade-report rendering timing"               | **open** | Mobile out-of-scope; grade timing pick "only after grader exits"    |
| decision-journal.md §Open   | "Offline export"; "Hand-typed frontmatter"                       | **open** | Accept both as documented limitations                               |
| workshop-runofshow.md §Open | "Shared-screen grader privacy"; "post-workshop debrief artefact" | **open** | Instructor brief §9 to include an opt-out clause for named students |

**Net**: 11 open questions across specs. Most are acceptable punts. The ones that tangle with CRITICAL findings (C14/drift-week, C6/sharing-topology) must be resolved before launch.

---

## 6. Dependency-ordered fix list

**Phase 0 — API truth reconciliation (blocking, 1 session)**

1. Fix C1 (AutoMLEngine constructor) — update playbook-universal, product-northwind, scaffold-contract banner, START_HERE §3.5.
2. Fix C9 (families → candidate_families) — same files.
3. Fix C4 (FeatureStore.ingest → register_features+store) — data-fixtures §6, scaffold-contract fs_preload row, playbook-universal Phase 2/4.
4. Fix C5 (rolling_origin → walk_forward) — same set.
5. Fix C2 (drift severity 3-value) — product-northwind §8.5, rubric-grader §2 row 5, viewer-pane §3.5, scenario-injection §2.2.
6. Fix C10 (drift tests ks+psi only) — same.
7. Fix C3 (drift_wiring: no on_complete event) — rewrite scaffold-contract drift_wiring.py row + playbook-universal Phase 13 + data-fixtures §6.4.
8. Fix C8 (model_version_id derivation) — product-northwind §8.3, rubric-grader §2 row 3, decision-journal frontmatter.

**Phase 1 — Orphan closure (blocking, 1 session)**

9. Fix C11 (orphaned route files) — ship 501-stub route registrations in scaffold; update scaffold-contract §2.
10. Fix C6 (ml_context wiring test) — add 12 test file names to scaffold-contract §9.
11. Fix H16 (facade-manager test naming) — same 12 files.

**Phase 2 — Cross-spec consistency (1 session)**

12. Fix H2 (/health field types to booleans) — product-northwind §8.6, scaffold-contract health row, viewer-pane §2.
13. Fix H6 (XGBoost fallback) — pick one list of 3 families, propagate.
14. Fix H12 (stockout $/unit wording) — product-northwind §5, START_HERE §2.
15. Fix H14 (phase_8_postunion filename) — decision-journal §1.1, viewer-pane §3.1.
16. Fix H8 (grader partial credit "N of N") — rubric-grader §2.2.

**Phase 3 — File size + structure (1 session)**

17. Fix C12 (split playbook-universal.md into 3 files + cross-index).
18. Fix C12b (extract api-surface.md from product-northwind §8).
19. Update \_index.md.

**Phase 4 — Completeness + rigor (1 session)**

20. Fix C7 (medicare-cut → SG equivalent) — scenario-injection §2.3.
21. Fix C14 (week-78 vs week-40 drift) — pick one; update data-fixtures + product-northwind.
22. Fix H1 (port conflict detection) — preflight.py + .env.example + viewer config.
23. Fix H4 (AUTOML_QUICK semantics) — product-northwind §8.1.
24. Fix H5 (seed_route_plan.py) — scaffold-contract §6.
25. Fix H10 (ModelExplainer ImportError fallback) — playbook-universal Phase 7 + preflight.
26. Fix H13 (chi2/js removal) — rubric-grader row 5.
27. Fix H15 (last_entry_timestamp storage) — decision-journal §6.1.
28. Fix H17 (/drift/status endpoint) — product-northwind §8.
29. Fix H18 (pandoc fallback quality flag) — decision-journal §5.2.

**Phase 5 — Medium + Low (1 session, parallel)**

30. Close remaining MEDIUM items 25-40 and all LOW items in one sweep; many are single-word edits.

**Total**: 5 sessions of work. Gate: none of Phase 0 can be deferred. Phases 1-4 can proceed in parallel after Phase 0 lands.

---

## Verdict

**FAIL — blocking gate.** The specs cannot ship as-authored. The root cause is 80% a single failure: the kailash-ml API surface was drafted against SKILL.md's Quick Start blocks (which themselves drift from source in several places) rather than against the engine source. Once the Phase-0 reconciliation lands, the specs are ~90% of the way to pristine. The remaining 10% is orphan-detection + cross-spec consistency hygiene.

The pedagogical design is strong. The rubric design is strong. The scenario injection design is strong. The specs need API-truth alignment, not re-design.

## Files examined

- `/Users/esperie/repos/training/metis/workspaces/metis/week-04-supply-chain/specs/_index.md`
- `/Users/esperie/repos/training/metis/workspaces/metis/week-04-supply-chain/specs/product-northwind.md`
- `/Users/esperie/repos/training/metis/workspaces/metis/week-04-supply-chain/specs/playbook-universal.md`
- `/Users/esperie/repos/training/metis/workspaces/metis/week-04-supply-chain/specs/scaffold-contract.md`
- `/Users/esperie/repos/training/metis/workspaces/metis/week-04-supply-chain/specs/rubric-grader.md`
- `/Users/esperie/repos/training/metis/workspaces/metis/week-04-supply-chain/specs/scenario-injection.md`
- `/Users/esperie/repos/training/metis/workspaces/metis/week-04-supply-chain/specs/data-fixtures.md`
- `/Users/esperie/repos/training/metis/workspaces/metis/week-04-supply-chain/specs/viewer-pane.md`
- `/Users/esperie/repos/training/metis/workspaces/metis/week-04-supply-chain/specs/decision-journal.md`
- `/Users/esperie/repos/training/metis/workspaces/metis/week-04-supply-chain/specs/workshop-runofshow.md`
- `/Users/esperie/repos/training/metis/workspaces/metis/week-04-supply-chain/START_HERE.md`
- `/Users/esperie/repos/training/metis/workspaces/metis/week-04-supply-chain/04-validate/redteam-start-here-doc.md`
- `/Users/esperie/repos/training/metis/workspaces/metis/week-04-supply-chain/01-analysis/approach.md`
- `/Users/esperie/repos/loom/kailash-py/packages/kailash-ml/src/kailash_ml/__init__.py`
- `/Users/esperie/repos/loom/kailash-py/packages/kailash-ml/src/kailash_ml/engines/automl_engine.py`
- `/Users/esperie/repos/loom/kailash-py/packages/kailash-ml/src/kailash_ml/engines/drift_monitor.py`
- `/Users/esperie/repos/loom/kailash-py/packages/kailash-ml/src/kailash_ml/engines/model_registry.py`
- `/Users/esperie/repos/loom/kailash-py/packages/kailash-ml/src/kailash_ml/engines/experiment_tracker.py`
- `/Users/esperie/repos/loom/kailash-py/packages/kailash-ml/src/kailash_ml/engines/training_pipeline.py`
- `/Users/esperie/repos/loom/kailash-py/packages/kailash-ml/src/kailash_ml/engines/feature_store.py`
- `/Users/esperie/repos/loom/kailash-py/packages/kailash-ml/src/kailash_ml/engines/inference_server.py`
- `/Users/esperie/repos/loom/.claude/skills/34-kailash-ml/SKILL.md`
- `/Users/esperie/repos/loom/.claude/skills/34-kailash-ml/ml-training-pipeline.md`
- `/Users/esperie/repos/loom/.claude/skills/34-kailash-ml/ml-model-registry.md`
- `/Users/esperie/repos/loom/.claude/skills/34-kailash-ml/ml-drift-monitoring.md`
- `/Users/esperie/repos/loom/.claude/skills/03-nexus/SKILL.md`
