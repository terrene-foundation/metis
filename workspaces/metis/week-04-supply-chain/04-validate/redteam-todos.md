# Red-Team Report — Week 4 Supply Chain Shard Todos (8 files)

**Date**: 2026-04-16
**Reviewer**: quality-reviewer agent
**Target**: `workspaces/metis/week-04-supply-chain/todos/active/{01..08}-*.md`
**Ground truth**: 16 spec files under `specs/` + prior red-team reports under `04-validate/`
**Rules applied**: autonomous-execution, zero-tolerance, orphan-detection, facade-manager-detection, testing, specs-authority, terrene-naming, agent-reasoning, communication, independence, env-models

---

## 1. Executive Summary

**Severity counts**: CRITICAL 8 · HIGH 14 · MEDIUM 13 · LOW 6 = **41 findings**
**Verdict**: **NO-GO — convergence failure**. The shard decomposition covers ~85% of spec surface but drops multiple orphan-detection Rule 2 obligations (wiring tests for 5 of 12 components are unowned), mis-prices the optimize and viewer shards against the invariant budget, leaves the `lta-carbon-levy` 4-term objective endpoint contract un-implemented, misclassifies Tier 2 tests as Tier 1 in shard 06, and does not own `journal/_template.md`, `journal/_examples.md`, `PRODUCT_BRIEF.md`, `.github/workflows/{preflight,grade}.yml`, `specs/schemas/routes.py`, `specs/business-costs.md`, `data/leaderboard_prebaked.json` ExperimentTracker seeding via `scripts/seed_experiments.py` integration step, or `scripts/instructor_brief.md`. Several acceptance criteria reference "canonical-values.md §8.1-8.3" that do not exist (canonical-values §8 is not sub-numbered). The `AnomalyDetectionEngine` orphan flag is acknowledged but unresolved.

**Top 5 must-fix before /implement**:

1. **C1** — `lta-carbon-levy` 4-term objective endpoint: no shard owns implementing the 4-term `carbon_levy` term in `/optimize/solve` (shard 03 only handles 3 terms). D3 cost-quantification learning objective will score 0/4 for the cohort when the levy fires.
2. **C2** — Wiring tests for `ModelExplainer` / `DataExplorer` / `ModelVisualizer` / `FeatureEngineer` / `AnomalyDetectionEngine` are unowned across all 8 shards. `wiring-contracts.md §7-10, §12` and `scaffold-contract.md §9` require 5 additional `test_*_wiring.py` files that no shard authors. This is a direct `facade-manager-detection.md` Rule 2 violation.
3. **C3** — `scripts/seed_experiments.py` in shard 07 requires a LIVE `ExperimentTracker` DB and real `AutoMLEngine` run to produce `leaderboard_prebaked.json` with real run IDs per `data-fixtures.md §3.2`. This is a call-graph-hops-5+ integration task that depends on shard 01 (ml_context), not depends_on=[]. The dependency graph is wrong.
4. **C4** — Shard 06 misclassifies three wiring tests as `tests/unit/` but they require real subprocess, real pandoc, real `ExperimentTracker` + `ModelRegistry` via `ml_context` — they are Tier 2 by `testing.md` definition. Placing them in `tests/unit/` bypasses the real-infra rule and hides integration failures.
5. **C5** — Orphaned scaffold files: `journal/_template.md`, `journal/_examples.md` (PRE-BUILT per `scaffold-contract.md §1`), `PRODUCT_BRIEF.md`, `.env.example` enumeration (shards 01 and 07 both claim partial ownership — overlap with no merge arbiter), `specs/schemas/routes.py`, `specs/business-costs.md`, `.github/workflows/{preflight,grade}.yml` (scaffold-contract §7), `scripts/instructor_brief.md` (scaffold-contract §6 + §8), `scripts/run_backend.sh` explicitly out-of-scope but un-owned, `scripts/seed_route_plan.py` (scaffold-contract §6) — no shard authors any of these.

---

## 2. Coverage Matrix (§A) — Spec Section → Owning Shard

Legend: `01..08` = shard id, `—` = gap, `M` = mentioned but out-of-scope.

| Spec                             | Section                             | Content                                                                                    | Owner                                                                                                                                                                                                                                                                                |
| -------------------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **\_index.md**                   | all                                 | manifest-only                                                                              | — (not actionable)                                                                                                                                                                                                                                                                   |
| **canonical-values.md**          | §1 severity enum                    | 3-value enum                                                                               | 04 (invariant), 05 (invariant)                                                                                                                                                                                                                                                       |
|                                  | §2 AutoML search strategies         | values + default                                                                           | 02 (invariant), 07 (Bayesian pre-bake)                                                                                                                                                                                                                                               |
|                                  | §3 EvalSpec split strategies        | walk_forward                                                                               | 02 (invariant), 07 (pre-bake config)                                                                                                                                                                                                                                                 |
|                                  | §4 ModelRegistry lifecycle          | 4 states + transitions                                                                     | 02 (implicit)                                                                                                                                                                                                                                                                        |
|                                  | §5 ModelVersion (name, version)     | derive/parse helpers                                                                       | 01 (implementer), 02 (consumer)                                                                                                                                                                                                                                                      |
|                                  | §6 Northwind business numbers       | $40/$12/$220 etc.                                                                          | 08 (H5 fix, via business-costs.md) **but business-costs.md is orphaned — see F5 below**                                                                                                                                                                                              |
|                                  | §7 Port topology                    | ports + env vars                                                                           | 01 (consumer), 06 (preflight)                                                                                                                                                                                                                                                        |
|                                  | §8 Endpoint contracts               | 5 endpoints + /health                                                                      | — **sub-numbering referenced but wrong**                                                                                                                                                                                                                                             |
|                                  | §8.1 /forecast/train                | request/response                                                                           | 02                                                                                                                                                                                                                                                                                   |
|                                  | §8.2 /forecast/compare              |                                                                                            | 02                                                                                                                                                                                                                                                                                   |
|                                  | §8.3 /forecast/predict              |                                                                                            | 02                                                                                                                                                                                                                                                                                   |
|                                  | §8.4 /optimize/solve                |                                                                                            | 03                                                                                                                                                                                                                                                                                   |
|                                  | §8.5 /drift/check                   |                                                                                            | 04                                                                                                                                                                                                                                                                                   |
|                                  | §8.5.1 /drift/status                |                                                                                            | 01 (routes/drift_status.py)                                                                                                                                                                                                                                                          |
|                                  | §8.6 /health                        |                                                                                            | 01                                                                                                                                                                                                                                                                                   |
|                                  | §8.7 Candidate family list          | 3 families default                                                                         | 02 (partial), 08 (H13 fix)                                                                                                                                                                                                                                                           |
|                                  | §9 Rubric 5 dims × 3 anchors        | 0/2/4 scoring                                                                              | 06 (grader implementer), 08 (H10/H11 worked examples)                                                                                                                                                                                                                                |
|                                  | §10 Journal entry schema            | frontmatter + headings                                                                     | 06 (CLI implementer)                                                                                                                                                                                                                                                                 |
|                                  | §11 Scenario event IDs              | 5 scenarios                                                                                | 06                                                                                                                                                                                                                                                                                   |
|                                  | §12 ExperimentTracker UUID format   | run_id contract                                                                            | 02 (consumer), 06 (grader check), 07 (pre-bake seed)                                                                                                                                                                                                                                 |
| **wiring-contracts.md**          | §1 TrainingPipeline                 | test + call site                                                                           | 02 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §2 AutoMLEngine                     |                                                                                            | 02 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §3 ExperimentTracker                |                                                                                            | 02 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §4 ModelRegistry                    |                                                                                            | 02 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §5 InferenceServer                  |                                                                                            | 02 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §6 DriftMonitor                     |                                                                                            | 04 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §7 ModelExplainer                   |                                                                                            | — **GAP** (02 lists as "out of scope")                                                                                                                                                                                                                                               |
|                                  | §8 DataExplorer                     |                                                                                            | — **GAP**                                                                                                                                                                                                                                                                            |
|                                  | §9 ModelVisualizer                  |                                                                                            | — **GAP**                                                                                                                                                                                                                                                                            |
|                                  | §10 FeatureEngineer                 |                                                                                            | — **GAP** (decision "wire or delete" deferred to implement)                                                                                                                                                                                                                          |
|                                  | §11 FeatureStore                    |                                                                                            | 01 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §12 AnomalyDetectionEngine          |                                                                                            | — **GAP** (04 punts to /implement)                                                                                                                                                                                                                                                   |
|                                  | "Audit hook" (grader runs 12 tests) |                                                                                            | — **GAP** (06 grader does not run the 12 wiring tests per §Audit hook)                                                                                                                                                                                                               |
| **product-northwind.md**         | §1 what it is                       | framing                                                                                    | 08 (PLAYBOOK preamble)                                                                                                                                                                                                                                                               |
|                                  | §2 Modules                          | 3 modules                                                                                  | 08 (PLAYBOOK)                                                                                                                                                                                                                                                                        |
|                                  | §3 Users & personas                 | 5 personas                                                                                 | — (docs-only; 08 covers via PLAYBOOK)                                                                                                                                                                                                                                                |
|                                  | §4 User flows                       | timing                                                                                     | 08 (PLAYBOOK)                                                                                                                                                                                                                                                                        |
|                                  | §5 Business numbers                 | costs                                                                                      | 08 (H5) + orphan business-costs.md — see F5                                                                                                                                                                                                                                          |
|                                  | §6 SLOs                             | p95 latency                                                                                | 02/03/04 (invariants)                                                                                                                                                                                                                                                                |
|                                  | §7 Deployment topology              | ports + artifact dir                                                                       | 01                                                                                                                                                                                                                                                                                   |
|                                  | §8.1–8.6 endpoint contracts         | see canonical §8                                                                           | 01/02/03/04                                                                                                                                                                                                                                                                          |
|                                  | §9 out-of-scope                     | fairness/tenant/auth                                                                       | — (acknowledgment only)                                                                                                                                                                                                                                                              |
| **playbook-universal.md**        | cross-index                         | phase→sprint map                                                                           | 08 ✓                                                                                                                                                                                                                                                                                 |
| **playbook-phases-sml.md**       | Phase 1 Frame                       | prompt + rubric                                                                            | 08 (PLAYBOOK generation)                                                                                                                                                                                                                                                             |
|                                  | Phase 2 Data Audit                  | DataExplorer call                                                                          | 08 (PLAYBOOK) + **GAP** for wiring test                                                                                                                                                                                                                                              |
|                                  | Phase 4 Candidates                  | AutoML prompt                                                                              | 08 (PLAYBOOK) + 02 (endpoint)                                                                                                                                                                                                                                                        |
|                                  | Phase 5 Implications                | leaderboard compare                                                                        | 08 (PLAYBOOK) + 02                                                                                                                                                                                                                                                                   |
|                                  | Phase 6 Metric+Threshold            | cost curve                                                                                 | 08 (PLAYBOOK)                                                                                                                                                                                                                                                                        |
|                                  | Phase 7 Red-Team                    | ModelExplainer fallback                                                                    | 08 (PLAYBOOK) + **GAP** for wiring test                                                                                                                                                                                                                                              |
|                                  | Phase 8 Deployment Gate             | promote_model transition                                                                   | 08 (PLAYBOOK) + 02 (registry call)                                                                                                                                                                                                                                                   |
|                                  | Phase 9 Codify                      | end-of-class                                                                               | 08 (PLAYBOOK)                                                                                                                                                                                                                                                                        |
|                                  | ModelRegistry state machine         | transition table                                                                           | 02 (invariant)                                                                                                                                                                                                                                                                       |
| **playbook-phases-prescribe.md** | Phase 10 Objective                  | multi-term                                                                                 | 08 (PLAYBOOK) + **partial gap** (4-term levy — see C1)                                                                                                                                                                                                                               |
|                                  | Phase 11 Constraints                | hard/soft                                                                                  | 08 (PLAYBOOK) + 03 (invariant hard_constraints_satisfied)                                                                                                                                                                                                                            |
|                                  | Phase 12 Solver                     | OR-Tools + snapshots                                                                       | 08 (PLAYBOOK) + 03 ✓                                                                                                                                                                                                                                                                 |
| **playbook-phases-mlops.md**     | Phase 13 Drift                      | severity + signals                                                                         | 08 (PLAYBOOK) + 04 ✓                                                                                                                                                                                                                                                                 |
|                                  | Phase 14 Fairness                   | deferred                                                                                   | — (deferred)                                                                                                                                                                                                                                                                         |
|                                  | DriftMonitor state machine          |                                                                                            | 01 + 04                                                                                                                                                                                                                                                                              |
| **scaffold-contract.md**         | §1 Workspace root                   | START_HERE, PLAYBOOK, PRODUCT_BRIEF, journal templates/examples, `.env.example`            | 08 (partial) + **GAPS: journal/\_template.md, journal/\_examples.md, PRODUCT_BRIEF.md are unowned**                                                                                                                                                                                  |
|                                  | §2 Backend source                   | app/config/ml_context/fs_preload/drift_wiring/routes                                       | 01 ✓ + 02/03/04 (route bodies)                                                                                                                                                                                                                                                       |
|                                  | §3 Specs                            | specs/schemas/, business-costs, success-criteria, api-surface, rubric, ai-verify           | — **GAP: specs/schemas/routes.py, specs/business-costs.md, specs/success-criteria.md, specs/api-surface.md, specs/rubric.md, specs/ai-verify.md all unowned**                                                                                                                        |
|                                  | §4 Data                             | fixtures + README                                                                          | 07 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §5 Frontend Viewer                  | Next.js app                                                                                | 05 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §6 Scripts                          | preflight, grade, seeds, scenario, journal, run_backend, instructor_brief, seed_route_plan | 06 (4 scripts) + 07 (2 seeds) + **GAP: scripts/run_backend.sh, scripts/seed_route_plan.py, scripts/instructor_brief.md**                                                                                                                                                             |
|                                  | §7 CI                               | preflight.yml, grade.yml                                                                   | — **GAP**                                                                                                                                                                                                                                                                            |
|                                  | §8 Instructor-only                  | scenario_inject, instructor_brief                                                          | 06 (partial) + **GAP: instructor_brief.md**                                                                                                                                                                                                                                          |
|                                  | §9 Orphan audit                     | 12 components                                                                              | 01/02/04 (7 of 12) + **GAPS: 5 of 12 unowned — see C2**                                                                                                                                                                                                                              |
|                                  | §10 .env.example enumeration        | keys list                                                                                  | 01 (claim) + 07 (claim seeds only) — **OVERLAP**                                                                                                                                                                                                                                     |
| **rubric-grader.md**             | §1 Journal rubric                   | 5 dims × 3 anchors                                                                         | 06 (grader), 08 (H10/H11 worked examples)                                                                                                                                                                                                                                            |
|                                  | §1.3 Applicability matrix           | per-phase                                                                                  | 06 (implementer)                                                                                                                                                                                                                                                                     |
|                                  | §2 Product grade (5 endpoints)      | contract assertions                                                                        | 06 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §3 grade_product.py contract        | execution order                                                                            | 06 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §3.2 step 4 fix messages            | 11 mappings                                                                                | 06 (grade_fix_messages.json) + 08 (H13 grader tolerance)                                                                                                                                                                                                                             |
|                                  | §3.5 placeholder detection          | stub guard                                                                                 | 06 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §4 Combined score                   | 60/40 weights                                                                              | 06 (implicit)                                                                                                                                                                                                                                                                        |
|                                  | §5 Anti-patterns                    | "if data changed" etc.                                                                     | 08 (H10 worked examples)                                                                                                                                                                                                                                                             |
| **scenario-catalog.md**          | §1 Singapore context                | MOM/LTA/HDB/MAS                                                                            | 06 (CLI) + 08 (PLAYBOOK)                                                                                                                                                                                                                                                             |
|                                  | §2 union-cap                        | full event                                                                                 | 06 ✓ + 03 (snapshot hygiene)                                                                                                                                                                                                                                                         |
|                                  | §3 drift-week-78                    |                                                                                            | 06 ✓ + 04 (endpoint) + 07 (payload)                                                                                                                                                                                                                                                  |
|                                  | §4 lta-carbon-levy                  | 4-term objective                                                                           | 06 (CLI) + **GAP in 03: endpoint does not accept 4-term objective** — see C1                                                                                                                                                                                                         |
|                                  | §5 hdb-loading-curfew               | dry-run only                                                                               | 06 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §6 mas-climate-disclosure           | dry-run only                                                                               | 06 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §7 Scenario firing matrix           | summary                                                                                    | 06 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §8 chat snippets                    | instructor brief                                                                           | — **GAP: scripts/instructor_brief.md unowned**                                                                                                                                                                                                                                       |
| **scenario-injection.md**        | §1 CLI contract                     | entry point                                                                                | 06 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §1.1 Exit codes                     | 0-5                                                                                        | 06 ✓ (but 06 conflates catalog's 5-code with injection's 5-code — they agree but the documentation bridge is missing)                                                                                                                                                                |
|                                  | §1.2 Idempotency                    | --re-fire flag                                                                             | 06 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §1.3 Logging                        | .scenario_log.jsonl                                                                        | 06 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §2.1 union-cap                      |                                                                                            | 06 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §2.2 drift-week-78                  |                                                                                            | 06 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §2.3 casemix-tariff-cut             | dry-run only                                                                               | **INCONSISTENCY — see F3** (06 lists the 3 live + 2 dry-run scenarios from catalog.md but injection.md §2.3 spec asserts casemix-tariff-cut is the dry-run event; shard 06's catalog-version wins — but the spec-authority inconsistency is not resolved)                            |
|                                  | §3 Timing windows                   | minute offsets                                                                             | 06 (implicit)                                                                                                                                                                                                                                                                        |
|                                  | §4 chat snippets                    |                                                                                            | — **GAP: scripts/instructor_brief.md unowned**                                                                                                                                                                                                                                       |
|                                  | §5 pre-baked payloads               | cross-ref to fixtures                                                                      | 07 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §6 failure modes                    |                                                                                            | 06 (implicit)                                                                                                                                                                                                                                                                        |
| **data-fixtures.md**             | §1 primary CSV                      | shape + columns                                                                            | 07 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §1.3 distribution anchors           | D01/D02/D03                                                                                | 07 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §1.4 holdout CSV                    |                                                                                            | 07 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §2 week 78 drift                    |                                                                                            | 07 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §3 leaderboard_prebaked             |                                                                                            | 07 ✓ — **BUT see C3: requires ml_context DB integration, shard ordering wrong**                                                                                                                                                                                                      |
|                                  | §4 drift_baseline                   |                                                                                            | 07 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §5 union_cap scenario               |                                                                                            | 07 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §6 FeatureStore loading             | register_features + store                                                                  | 01 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §7 Determinism                      | 3 seeds                                                                                    | 07 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §8 Data hygiene                     | no PII                                                                                     | — (implicit — LOW finding)                                                                                                                                                                                                                                                           |
| **viewer-pane.md**               | §1 Architecture                     | Next 14 + chokidar                                                                         | 05 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §2 Polling contract                 | 1s + 304                                                                                   | 05 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §3.1 Playbook Progress              | inline                                                                                     | 05 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §3.2 Leaderboard                    | side-by-side                                                                               | 05 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §3.3 Forecast                       | line chart                                                                                 | 05 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §3.4 Route                          | scenario toggle                                                                            | 05 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §3.5 Drift                          | severity badge                                                                             | 05 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §3.6 Journal                        | react-markdown                                                                             | 05 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §3.7 Preflight banner               | 8 booleans                                                                                 | 05 ✓ (8 fields) — **but shard 01 writes only `feature_store_populated` + `drift_wiring`; the other 6 booleans (ok, xgb_available, explain_available, ortools_available, pulp_available, db) are preflight.py's job (shard 06). Viewer expects all 8; overlap unarbitrated — see H4** |
|                                  | §4 UX invariants                    | read-only                                                                                  | 05 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §5 Component ownership              | import table                                                                               | 05 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §6 Failure modes                    |                                                                                            | 05 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §7 Accessibility                    | keyboard + colour-blind                                                                    | 05 ✓                                                                                                                                                                                                                                                                                 |
| **decision-journal.md**          | §1 entry schema                     | filename + frontmatter                                                                     | 06 ✓ (add command fills frontmatter)                                                                                                                                                                                                                                                 |
|                                  | §1.1 filename patterns              | 15 patterns                                                                                | 06 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §1.2 frontmatter                    | YAML                                                                                       | 06 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §1.3 body schema                    | 5 headings                                                                                 | 06 ✓ (via `_template.md`) — **BUT `journal/_template.md` is unowned across shards (see C5)**                                                                                                                                                                                         |
|                                  | §2 template                         |                                                                                            | — **GAP**                                                                                                                                                                                                                                                                            |
|                                  | §3 worked examples                  |                                                                                            | — **GAP** (`journal/_examples.md` unowned)                                                                                                                                                                                                                                           |
|                                  | §4 CLI subcommands                  | add/list/export                                                                            | 06 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §4.0 lifecycle state machine        |                                                                                            | 06 ✓ (append-only invariant)                                                                                                                                                                                                                                                         |
|                                  | §5 PDF export                       | pandoc + fallback                                                                          | 06 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §6 auto-linkage                     |                                                                                            | 06 ✓                                                                                                                                                                                                                                                                                 |
|                                  | §7 reversal condition               |                                                                                            | 06 (implicit) + 08 (PLAYBOOK)                                                                                                                                                                                                                                                        |
|                                  | §8 hygiene                          |                                                                                            | — (implicit)                                                                                                                                                                                                                                                                         |
| **workshop-runofshow.md**        | §0 pre-class                        | scenario dry-run                                                                           | — **GAP: scripts/instructor_brief.md + scripts/dry_run staging**                                                                                                                                                                                                                     |
|                                  | §1-6 minute-by-minute               | 210-min script                                                                             | — **GAP: unowned; 08 owns PLAYBOOK but not the run-of-show**                                                                                                                                                                                                                         |
|                                  | §7 timing contingencies             | recovery paths                                                                             | — **GAP**                                                                                                                                                                                                                                                                            |
|                                  | §8 post-workshop                    | archive + audit                                                                            | — **GAP**                                                                                                                                                                                                                                                                            |

---

## 3. Findings by Severity

### CRITICAL (8)

```
[CRITICAL] [Completeness] [03-optimize-endpoints.md:acceptance_criteria]
Title: No shard implements the 4-term objective for lta-carbon-levy
Problem: scenario-catalog.md §4 requires /optimize/solve to accept a 4-term objective
  ({fuel, sla, overtime, carbon_levy}) when the lta-carbon-levy scenario fires. Shard 03
  specifies the 3-term objective from canonical-values.md §8.4 and product-northwind.md §8.4;
  it does not list the carbon_levy term in any acceptance criterion. The scenario-catalog
  learning objective D3 "cost-quantification" depends on the $0.53/km total cost delta being
  produced by the endpoint.
Evidence: 03-optimize-endpoints.md mentions scenario_tag "preunion"/"postunion" only;
  scenario-catalog.md §4 specifies scenario_tag "post_carbon_levy" with a 4-term body;
  specs_consulted in shard 03 does NOT include scenario-catalog.md §4.
Fix: Add acceptance criterion to shard 03: "accepts variable-length objective.terms array;
  when scenario_tag=='post_carbon_levy', accepts a 4-term body {fuel, sla, overtime, carbon_levy}
  and returns objective_value reflecting all four terms". Add wiring assertion in
  test_ortools_vrp_wiring.py or a new test_carbon_levy_objective.py that POSTs a 4-term body
  and asserts objective_value > baseline.
Blast radius: When instructor fires lta-carbon-levy at minute 35 of Sprint 2 (scenario-catalog §4),
  students POST the 4-term body per spec; route rejects with schema error OR silently ignores
  the carbon_levy term; journal Phase 10 entries cite a cost delta that never happened.
  D3 learning objective scores 0/4 for every student who fires the scenario. The scenario is
  live per §4 "Deployable tomorrow: YES".

[CRITICAL] [Orphan-detection Rule 2] [02, 04; wiring-contracts.md §7-10, §12]
Title: 5 of 12 wiring tests are unowned across all 8 shards
Problem: wiring-contracts.md §7 (ModelExplainer), §8 (DataExplorer), §9 (ModelVisualizer),
  §10 (FeatureEngineer), §12 (AnomalyDetectionEngine) each require a Tier-2 wiring test file
  with a specific name. No shard lists any of these test files under wiring_tests.
  Shard 02's "out of scope" section explicitly punts ModelExplainer/DataExplorer/ModelVisualizer
  ("wiring tests 7/8/9 belong to this shard's test files per wiring-contracts.md but the route
  bodies are student-commissioned"), but does NOT include them in acceptance criteria.
  Shard 04 punts AnomalyDetectionEngine ("confirm call site or delete before /implement; not in
  scope for this shard"). wiring-contracts.md §10 FeatureEngineer acceptance is entirely unowned.
Evidence: Grep across todos/active/*.md: 0 matches for test_model_explainer_wiring,
  test_data_explorer_wiring, test_model_visualizer_wiring, test_feature_engineer_wiring,
  test_anomaly_detection_engine_wiring. scaffold-contract.md §9 lists 12 components requiring
  wiring tests; only 7 are owned (FeatureStore, ModelRegistry, ExperimentTracker, TrainingPipeline,
  AutoMLEngine, InferenceServer, DriftMonitor + ml_context facade = 8 actually). OR-Tools VRP
  and PuLP are owned by 03.
Fix: Either (a) extend shard 02 acceptance to include 3 additional wiring tests
  (test_model_explainer_wiring, test_data_explorer_wiring, test_model_visualizer_wiring)
  against the Phase 2/5/7 student-commissioned call sites, OR (b) add a new shard 02b explicitly
  owning these tests. For FeatureEngineer, make the "wire or delete" decision at /todos NOT at
  /implement (per orphan-detection Rule 3). For AnomalyDetectionEngine, same: either pin a
  call site in shard 04's /drift/anomalies endpoint OR delete from public surface. The "decide
  at implement" deferrals violate autonomous-execution.md "Defer sharding decisions to /implement
  — BLOCKED".
Blast radius: Per facade-manager-detection Rule 2, these components become Phase 5.11-style
  orphans. ModelExplainer is specifically called in Phase 7 red-team; DataExplorer in Phase 2;
  ModelVisualizer in Phase 5 fold-variance plot. Without wiring tests, the scaffold can ship
  with any of these components instantiated in ml_context but never actually called on a hot
  path — exact Phase 5.11 shape.

[CRITICAL] [Dependency-graph correctness] [07-data-and-leaderboard.md:depends_on, blocks]
Title: seed_experiments.py generation of leaderboard_prebaked.json requires live ml_context
Problem: Shard 07 declares depends_on: [] and blocks: [01, 02, 03, 04, 06]. But its acceptance
  criterion "generates data/leaderboard_prebaked.json: 30 real ExperimentTracker runs, Bayesian
  search" requires a functioning AutoMLEngine, ExperimentTracker, FeatureStore — i.e. the
  ml_context facade. That facade lives in shard 01. Shard 07 cannot produce real ExperimentTracker
  UUIDs without shard 01's ConnectionManager + get_ml_context.
Evidence: 07-data-and-leaderboard.md line 39: "generates data/leaderboard_prebaked.json: 30
  real ExperimentTracker runs". data-fixtures.md §3.1 confirms this requires AutoMLConfig with
  candidate_families, EvalSpec(split_strategy='walk_forward'), ExperimentTracker writes.
  canonical-values.md §12 confirms run_id is `str(uuid.uuid4())` from ExperimentTracker.
Fix: Either (a) split shard 07 into 07a (synthetic CSV + static JSON fixtures — true depends_on=[])
  and 07b (leaderboard_prebaked.json via live ml_context — depends_on=[01]), OR (b) make 07
  depends_on=[01] and adjust the critical path. The claimed DAG is acyclic on paper but the
  true dependency 07→01 is missing. This also adjusts the "07 blocks 01" edge — 01 does not
  actually require 07's leaderboard_prebaked.json to construct ml_context; it requires the CSV
  and union_cap.json + specs/schemas/demand.py.
Blast radius: /implement launches 07 in parallel with 01 per the claimed DAG; 07 crashes because
  kailash_ml.AutoMLEngine cannot be imported against a null ConnectionManager; shard is stuck
  mid-implementation; session stalls. When unblocked, 07 re-runs against shard 01's output
  but its "deterministic seeds" guarantee is violated because the first attempt produced partial
  state files the rerun cannot match byte-for-byte.

[CRITICAL] [testing.md Tier 2 classification] [06-cli-and-grader.md:wiring_tests]
Title: Three wiring tests placed in tests/unit/ instead of tests/integration/
Problem: Shard 06 lists test_scenario_inject_exit_codes.py, test_journal_cli_append_only.py,
  and test_grader_placeholder_detection.py under tests/unit/. But each exercises real filesystem
  (.scenario_log.jsonl append, $EDITOR subprocess, journal/_template.md copy), real network
  (grade_product.py hits live /health endpoint), real pandoc subprocess. Per testing.md §3-tier,
  real infrastructure = Tier 2; mocking allowed = Tier 1. These tests MUST be tests/integration/.
Evidence: 06-cli-and-grader.md:46-48 lists three tests under tests/unit/; implementation sketch
  line 64 confirms real subprocess + real httpx.
Fix: Move all three test files to tests/integration/. Update scaffold-contract.md §9 audit
  table if it cross-references. Ensure conftest.py Tier 2 fixtures (real tmp_path workspace)
  are used, not Mock().
Blast radius: Tier 1 placement signals "mocking allowed"; the /implement agent will mock the
  filesystem + subprocess + httpx, which defeats the purpose of the tests (the real failure
  modes are file-atomic-rename races, $EDITOR command resolution, pandoc absence). A test suite
  that passes on mocks will ship a scenario_inject.py that fires but never writes the marker,
  a journal_cli.py that appends but loses atomicity, a grade_product.py that returns fake 0%
  scores on real backends. testing.md MUST: "NO mocking (@patch, MagicMock, unittest.mock —
  BLOCKED)" in Tier 2.

[CRITICAL] [Completeness] [scaffold-contract.md §1, §3, §6, §7, §8; all shards]
Title: Major scaffold files have no owning shard
Problem: scaffold-contract.md enumerates these [PRE-BUILT] files as shipped by scaffold; no
  shard owns authoring them:
  - PRODUCT_BRIEF.md (§1) — "Business context; cost table; personas; 3:30 pm success definition"
  - journal/_template.md (§1) — "Skeleton entry with 5 rubric-dimension headings"
  - journal/_examples.md (§1) — "3 entries at 4/4 and 3 at 1/4, side-by-side per phase"
  - specs/schemas/routes.py (§3) — "Vehicle, DeliveryWindow, RoutePlan, ConstraintSet"
  - specs/business-costs.md (§3) — "Dollar values for every cost term — read by every prompt"
  - specs/success-criteria.md (§3) — "Endpoint contract assertions; imported by grade_product.py"
  - specs/api-surface.md (§3) — "Endpoint signatures, request/response schemas, error taxonomy"
  - specs/rubric.md (§3) — "5-dimension scoring, 0/2/4 anchors, worked examples"
  - specs/ai-verify.md (§3) — "Transparency / Robustness / Safety dimensions"
  - scripts/run_backend.sh (§6) — canonical backend entrypoint (03 out-of-scope comment acknowledges, but no owner)
  - scripts/seed_route_plan.py (§6) — used by scenario_inject.py --undo (shard 06 calls it but shard 07 does not generate it)
  - scripts/instructor_brief.md (§6, §8) — chat snippets per scenario-catalog §8
  - .github/workflows/preflight.yml (§7)
  - .github/workflows/grade.yml (§7)
Evidence: Grep across todos/active/*.md: 0 matches for PRODUCT_BRIEF, journal/_template,
  journal/_examples, specs/schemas/routes.py, specs/business-costs, specs/success-criteria,
  specs/api-surface, specs/rubric.md, specs/ai-verify, instructor_brief, preflight.yml, grade.yml,
  seed_route_plan.
Fix: Add a new shard 09 "Scaffold Support Artefacts" owning these 14 files, OR fold PRODUCT_BRIEF
  + specs/ files + journal templates into shard 08 (docs), CI into a separate shard or 06,
  seed_route_plan + run_backend.sh into shard 06 or 07, and instructor_brief into 06. Whichever
  path, every file in scaffold-contract.md §1-8 MUST have exactly one owner.
Blast radius: (a) grade_product.py (shard 06) imports specs/success-criteria.md per rubric-grader
  §3.1 — if the file is not produced, shard 06 cannot complete. (b) All PLAYBOOK prompts cite
  specs/business-costs.md — if absent, H5 fix in shard 08 is a dangling reference. (c) Students
  running `metis journal add` cannot proceed without journal/_template.md. (d) scenario_inject.py
  --undo falls back to scripts/seed_route_plan.py per scenario-injection.md §2.1 — if absent,
  undo exit code 5 becomes unavoidable. (e) Nightly CI per scaffold-contract.md §7 never runs.
  Every one of these is a scaffold-ship blocker.

[CRITICAL] [Overlap — .env.example ownership] [01, 07]
Title: Both shards 01 and 07 claim to author .env.example; no merge contract
Problem: 01-backend-core.md acceptance #11: ".env.example contains all keys enumerated in
  scaffold-contract.md §10". 07-data-and-leaderboard.md acceptance #9: ".env.example contains
  RANDOM_SEED=42, AUTOML_SEED=2026, DRIFT_SEED=78". Both shards WRITE the same file. Neither
  says "extends" or "merges". Two /implement runs in parallel will race-write and the last
  writer wins; seeds OR backend keys will be silently dropped.
Evidence: 01-backend-core.md:37 and 87; 07-data-and-leaderboard.md:44 and 86.
Fix: Designate shard 01 as the SOLE author of .env.example with all keys from scaffold-contract.md §10
  (which ALREADY includes RANDOM_SEED/AUTOML_SEED/DRIFT_SEED — line 276 of scaffold-contract.md).
  Shard 07 SHOULD NOT write .env.example; remove the acceptance criterion from shard 07 and
  move the seed documentation into shard 07's generator script comments.
Blast radius: Parallel /implement causes non-deterministic .env.example contents; grader fails
  because KAILASH_NEXUS_PORT missing OR seeds missing; preflight.py reports a field as false
  and refuses to proceed.

[CRITICAL] [Preflight output overlap] [01, 06; viewer-pane.md §3.7]
Title: Viewer expects 8-boolean .preflight.json; shard 01 writes 2 fields, shard 06 writes the others — no contract
Problem: viewer-pane.md §3.7 PreflightBanner parses 8 boolean fields: db, feature_store, drift_wiring,
  ok, xgb_available, explain_available, ortools_available, pulp_available. Shard 01's
  fs_preload.py + drift_wiring.py write feature_store_populated and drift_wiring only (the
  acceptance criteria at 01:31 confirms). Shard 06's preflight.py writes the remaining 6
  (xgb/explain/ortools/pulp/db/ok) per implementation sketch line 63. Neither shard specifies
  the merge strategy: atomic rewrite (overwrites other writer's fields) vs read-modify-write
  (needs locking). This is a silent orphan waiting to fire.
Evidence: Shard 01:31 writes ".preflight.json.drift_wiring:true as side effect" and 01:33
  "writes .preflight.json feature_store_populated:true". Shard 06:63 "json.dump to .preflight.json".
  Neither acknowledges the other writer.
Fix: Specify the protocol explicitly in both shards: "both writers use read-modify-write with
  json.load → merge dict → atomic .tmp+rename; the file is initialized by shard 06 preflight.py
  FIRST (on every preflight run), then shards 01's fs_preload.py and drift_wiring.py UPDATE
  specific keys during Nexus startup". Add a fixture in conftest.py that zeros .preflight.json
  at test start, and a regression test asserting both fields survive a fs_preload + preflight
  sequence.
Blast radius: During workshop, one writer clobbers another's fields; Viewer banner shows red
  "feature_store: false" even when FeatureStore is populated (because preflight.py overwrote
  the flag), OR shows green when XGB is missing (because fs_preload.py overwrote the xgb flag
  with null). Students troubleshoot a false signal for 3-5 minutes.

[CRITICAL] [Broken reference] [02, 04, 05, 07; canonical-values.md §8.1-8.6]
Title: canonical-values.md §8 is sub-numbered (8.1..8.7) but cited as "§8.1-8.3" / "§8.4" / "§8.5"
  — the actual structure is correct but §8 top-level does not exist; sub-numbers are the only
  valid references, and 02's spec_consulted line "§8.1-8.3" is correct. However, shard 04 cites
  §8.5 and shard 03 cites §8.4; these resolve. BUT: scaffold-contract.md §1-8 cited by shard 08
  is valid (scaffold has sections 1-8). FALSE ALARM on cross-reference integrity; withdrawing
  this as CRITICAL. Downgrade to LOW (noted in §6 below).
Fix: N/A (self-resolved).
Blast radius: N/A.
```

### HIGH (14)

```
[HIGH] [Invariant budget] [03-optimize-endpoints.md:loc_estimate=310, invariants]
Title: Shard 03 underestimates LOC + invariants when OR-Tools VRP + PuLP + snapshot hygiene + scenario multipaths are summed
Problem: Shard 03 claims 310 LOC with 5 invariants. But scope includes: (a) OR-Tools VRP wrapper
  (routes/optimize.py + solvers/vrp_solver.py), (b) PuLP LP wrapper (solvers/lp_solver.py), (c)
  objective-DSL parser (3-term AND 4-term per C1), (d) hard/soft constraint classifier, (e)
  snapshot state machine (route_plan / _preunion / _postunion with idempotency), (f) ExperimentTracker
  tagging, (g) OR-Tools import-guard → PuLP fallback, (h) time_budget enforcement, (i) two
  Tier-2 wiring tests with real OR-Tools + real PuLP. Realistic LOC: 550-700. Invariants by
  count: solver-primary-vs-fallback, objective-term-variable-arity, hard_constraints_satisfied
  required keys, feasibility+optimality_gap always present, snapshot idempotency, scenario-tag
  state transitions, ExperimentTracker tagging, time-budget enforcement, 500-with-error_category
  = 9 invariants. Exceeds autonomous-execution.md §Shard Budget MUST rule ("≤5-10 simultaneous
  invariants the implementation must hold").
Evidence: 03 acceptance criteria lines 27-36 enumerate 10 distinct contracts. Missing from
  invariants list: 4-term objective (C1), solver-primary-vs-fallback, time-budget enforcement.
Fix: Split shard 03 into 03a (OR-Tools VRP primary path + wiring test) and 03b (PuLP fallback
  + snapshot hygiene + scenario-tag state machine + wiring test). OR compress scope by moving
  PuLP fallback to shard 04-adjacent or a Phase 2 follow-up. Explicitly name all 9+ invariants
  in the frontmatter.
Blast radius: Autonomous-execution MUST Rule: "Beyond the budget the model stops tracking
  cross-file invariants and pattern-matches instead." Shard 03 as-written is the Phase 5.11
  shape at 310 LOC + 9-10 hidden invariants.

[HIGH] [Invariant budget] [05-viewer-pane.md:loc_estimate=420, invariants]
Title: Shard 05 at 420 LOC with 7 panel components + watcher + polling is at-or-over budget
Problem: Scope includes (a) chokidar watcher with ETag 304, (b) 6 panel components, (c) inline
  PlaybookProgress, (d) PreflightBanner with 8 typed bools, (e) React Query provider + polling,
  (f) 3 render-contract tests, (g) empty-state logic per panel, (h) scenario-toggle state, (i)
  Recharts + Tailwind wiring, (j) failure-mode messages per §6 of viewer-pane.md. LOC estimate
  420 is low; 600-750 is realistic. Invariant count: no-cross-origin, poll-interval, read-only,
  severity-3-values, preflight-booleans, 304-on-nochange, scenario-toggle-purity, per-depot-tab,
  journal-markdown-rendering, empty-state-per-panel = 10. At the upper limit of autonomous-execution
  rule. With the frontend feedback loop (jest + chokidar in test env), this may just fit — but
  shard MUST cite "3-5x budget due to executable feedback loop" explicitly per autonomous-execution
  §3 to justify.
Evidence: 05:9 loc_estimate:420; invariants lists 5; but 10 distinct render-contracts in
  acceptance.
Fix: Either (a) split into 05a (watcher + layout + 3 panels: Leaderboard, Forecast, Drift)
  and 05b (3 panels: Route, Journal, PreflightBanner + 3 render tests), OR (b) justify the
  10-invariant budget via the frontend feedback loop (jest test-per-save) and cite it in the
  shard's "describable in 3 sentences" check.
Blast radius: Same Phase 5.11 risk — at the budget limit, cross-component invariants
  (severity-enum consistency, preflight-field naming) can drift between panels.

[HIGH] [Overlap — wiring test co-location] [01, 02; testing.md]
Title: tests/integration/conftest.py is written by shard 01 AND augmented by shard 02; no contract
Problem: Shard 01 acceptance includes "tests/integration/conftest.py — ml_context_real fixture".
  Shard 02 implementation sketch line 65: "tests/integration/conftest.py — add seed_feature_store(ctx, sample_df)
  helper; add sample_eval_spec fixture". Both shards modify the same file. No merge contract.
Evidence: 01:63 and 02:65.
Fix: Explicitly: "shard 01 ships conftest.py with ml_context_real. Shard 02 EXTENDS via new
  fixture file tests/integration/conftest_forecast.py imported by the forecast wiring tests."
  Either that, OR shard 01 ships all shared fixtures including seed_feature_store + sample_eval_spec
  and shard 02 consumes them only.
Blast radius: Parallel /implement: shard 02 reads conftest.py written by shard 01, adds
  fixtures, saves. Simultaneously shard 01's wrap-up edits conftest.py for a minor fix and
  overwrites shard 02's edits. Tests in shard 02 fail with "fixture not found".

[HIGH] [Agent-reasoning.md] [03-optimize-endpoints.md]
Title: "primary OR-Tools, fallback to PuLP on import error" — deterministic routing, not LLM-decision
Problem: Invariants and acceptance state the solver choice is made by an if-else guard: import
  ortools; on ImportError use pulp. This is acceptable for a library choice (not an LLM-reasoning
  path), BUT the framing is ambiguous. If this routing ever extends to "choose solver based on
  problem shape", it becomes an agent-reasoning.md violation.
Fix: Clarify in shard 03 invariants: "solver-choice is a deterministic installer-guard check,
  NOT an agent decision; if a future shard proposes 'choose solver by problem shape', that
  introduces LLM-reasoning-in-agent-path and is BLOCKED per rules/agent-reasoning.md."
Blast radius: Low today; but without clarification, a future Phase 12 prompt ("decide which
  solver to use") could be interpreted as "add if-else routing" instead of letting Claude Code
  reason.

[HIGH] [Missing endpoint — /drift/anomalies] [04, wiring-contracts.md §12]
Title: AnomalyDetectionEngine proposed endpoint /drift/anomalies has no implementing shard
Problem: wiring-contracts.md §12 proposes POST /drift/anomalies as the call site for
  AnomalyDetectionEngine. Shard 04 explicitly punts this decision ("AnomalyDetectionEngine
  flagged by wiring-contracts.md §12 as TODO — confirm call site or delete before /implement").
  Per orphan-detection.md Rule 3 "Removed = Deleted, Not Deprecated", the decision MUST be made
  at /todos time, not deferred. autonomous-execution.md MUST NOT "Defer sharding decisions to
  /implement".
Fix: At /todos gate, either (a) add /drift/anomalies endpoint to shard 04's scope AND add a
  test_anomaly_detection_engine_wiring.py, extending shard 04's scope from 180 LOC to ~230 LOC
  — still under budget, OR (b) delete AnomalyDetectionEngine from the scaffold public surface
  AND delete wiring-contracts.md §12 section AND update START_HERE.md and scaffold-contract.md
  §9 to remove it. Do not enter /implement with the decision pending.
Blast radius: Phase 5.11 orphan. If the component is exposed in ml_context public API and no
  production call site exists, downstream consumers build against it and ship code that
  silently bypasses it.

[HIGH] [Broken reference] [02-forecast-endpoints.md:specs_consulted]
Title: "canonical-values.md §8.1-8.3" is a valid range but grouping is misleading
Problem: Shard 02 cites "canonical-values.md §8.1-8.3 (endpoint contracts)". These are three
  distinct sections, not a range. On inspection they exist, so this is not a fabrication — but
  the "§8.1-8.3" shorthand is brittle (a future rename breaks 3 references). Shard 08 similarly
  cites "specs/scaffold-contract.md §1-8" as a range.
Fix: Cite explicitly: §8.1 AND §8.2 AND §8.3. Same for shard 08's §1-8.
Blast radius: Low. Audit trail ambiguity only.

[HIGH] [Workshop-runofshow.md coverage] [all shards]
Title: No shard owns ensuring minute-by-minute checkpoints from workshop-runofshow.md are honoured
Problem: workshop-runofshow.md is the authority on the 210-min script. It asserts that certain
  endpoints/panels/files MUST be live at specific minutes (e.g. 00:27 — AutoML running ≤90s;
  02:05 — union-cap fires and /optimize/solve with scenario_tag is called; 03:20 — grade_product.py
  runs publicly). No shard acceptance criterion cross-references runofshow checkpoints.
Evidence: Grep across todos/active/*.md: 0 matches for "workshop-runofshow" or "run-of-show".
Fix: Either (a) add workshop-runofshow.md to the specs_consulted list in shards 06 and 08,
  with explicit acceptance "shard N delivers artefact X by minute M per runofshow §K", OR (b)
  acknowledge that runofshow is an operational doc not an implementation spec, and move it to
  a dedicated "Operations" shard.
Blast radius: Medium. The scaffold can ship and all wiring tests pass, yet when the instructor
  runs the 210-min script, a specific artefact is missing (e.g. scripts/instructor_brief.md
  with the chat snippets) because no shard asserted its presence.

[HIGH] [Scaffold-contract §10 vs shard 01 — key enumeration incomplete] [01, scaffold-contract §10]
Title: Shard 01 ".env.example contains all keys" defers enumeration without listing them
Problem: Shard 01 acceptance "contains all keys enumerated in scaffold-contract.md §10" — a
  reference, not a listing. scaffold-contract.md §10 lists 13 keys (KAILASH_NEXUS_PORT,
  KAILASH_ML_AUTOML_QUICK, DATABASE_URL_EXPERIMENTS, DATABASE_URL_REGISTRY, DATABASE_URL_FEATURES,
  ARTIFACT_DIR, RANDOM_SEED, AUTOML_SEED, DRIFT_SEED, NEXT_PUBLIC_POLL_MS, NEXT_PUBLIC_BACKEND_PORT,
  METIS_WORKSPACE_ROOT, OPENAI_API_KEY, ANTHROPIC_API_KEY — 14 with commented). Shard 01 does
  not verify the count or names.
Fix: Expand shard 01 acceptance to list the 13 keys explicitly OR add a unit test
  tests/unit/test_env_example_has_all_keys.py that imports scaffold-contract.md §10 list and
  asserts every key appears in .env.example.
Blast radius: If one key is missing, downstream fails silently (e.g. missing NEXT_PUBLIC_POLL_MS
  → viewer polls at 0ms → CPU melt). A test catches this at commit time.

[HIGH] [Tier-2 test "mocks ortools ImportError"] [03-optimize-endpoints.md:test_pulp_wiring.py]
Title: Shard 03 explicitly proposes patching ortools import in a Tier-2 test — violates testing.md MUST Rule
Problem: 03:58 "test_pulp uses real PuLP; test_pulp_wiring.py patches import ortools to raise
  ImportError then asserts the PuLP fallback fires". testing.md § Tier 2: "NO mocking (@patch,
  MagicMock, unittest.mock — BLOCKED)".
Evidence: Shard 03 acceptance #10: "tests/integration/test_pulp_wiring.py passes: mocks ortools
  ImportError".
Fix: Use a real uninstalled ortools environment (a test venv without ortools), OR use a
  package-level import guard that accepts an env var (OR_TOOLS_DISABLED=1) and let the real
  runtime path trigger the fallback. Patching imports in a Tier-2 test is a testing.md
  violation.
Blast radius: The test passes on mocks but ships a PuLP fallback code path that never actually
  fires on real machines — pattern "test passes with mock, prod fails silently".

[HIGH] [canonical-values §8.1 candidate_families values] [02, 07]
Title: Shard 02 vs 07 disagree on default candidate_families list
Problem: canonical-values.md §8.7 specifies default candidate_families as ["LinearRegression",
  "RandomForestRegressor", "GradientBoostingRegressor"] (unqualified names). product-northwind.md
  §8.1 example uses fully qualified names ["sklearn.linear_model.Ridge",
  "sklearn.ensemble.RandomForestRegressor", "sklearn.ensemble.GradientBoostingRegressor"].
  Shard 02 does not pin the name format. Shard 07 uses ["Ridge", "RandomForestRegressor",
  "GradientBoostingRegressor", "LinearRegression", "XGBoostRegressor"] (unqualified). A student
  who uses canonical-values §8.7 format differs from data-fixtures §3.1 pre-bake format.
Fix: Pin exactly one format. Recommended: fully-qualified (per product-northwind §8.1
  `"sklearn.linear_model.Ridge"`) because `AutoMLConfig.candidate_families` is a dotted-path
  import spec. Update canonical-values.md §8.7 table + shard 07 acceptance.
Blast radius: Phase 5 leaderboard compare mismatches because live-run families don't share
  exact same names as pre-bake families; journal entries cite mismatched names.

[HIGH] [Completeness — canonical-values §12 alias generator] [02, 06, 07]
Title: ExperimentTracker alias "{short_family}_{ordinal:03d}_{YYYYMMDD}_{HHMMSS}" is workshop convention — no shard implements the alias file
Problem: canonical-values.md §12 Open TODOs: "alias format is workshop convention, not library
  contract. Flagged for scaffold implementation; no library citation possible." The file is
  `data/.experiment_aliases.json` per §12. No shard owns writing/reading this file.
Evidence: Grep: 0 matches for "experiment_aliases" in todos/active.
Fix: Add to shard 01's ml_context responsibility a helper `resolve_experiment_run_id(id_or_alias) -> run_uuid`
  that reads `data/.experiment_aliases.json`. Add to shard 02's /forecast/train a write to the
  alias file after AutoMLEngine.run completes.
Blast radius: grade_product.py (shard 06) asserts "the response experiment_run_id MUST resolve
  via ExperimentTracker.get_run(id) whether it was passed as UUID or alias" (canonical-values
  §12 last paragraph). Without the alias file, grade_product.py cannot honour its own contract.

[HIGH] [Completeness — decision-journal §2 template + §3 examples] [scaffold-contract §1; shard 08 + 06]
Title: journal/_template.md and journal/_examples.md are PRE-BUILT but unowned
Problem: scaffold-contract.md §1 lists journal/_template.md (PRE-BUILT) and journal/_examples.md
  (PRE-BUILT). decision-journal.md §2 + §3 specify their content. No shard authors either file.
  Shard 06 uses the template (06:33 "copies journal/_template.md → journal/phase_<N>_<slug>.md")
  but does not create it.
Evidence: Grep: 0 matches for "journal/_template" or "journal/_examples" as acceptance criterion.
Fix: Add to shard 08 or a new shard 09: author journal/_template.md per decision-journal.md §2
  and journal/_examples.md per decision-journal.md §3 (+ rubric-grader.md §1.1/§1.2 worked
  examples).
Blast radius: scenario-catalog §3 drift-week-78 Phase 13 mitigation depends on students reading
  journal/_examples.md for the 4/4 vs 1/4 contrast (scenario-catalog §3: "See journal/_examples.md
  for a 4/4 vs 1/4 pair on exactly this prompt"). Without the file, the anti-pattern ("auto-retrain
  MAPE > 15%") has no counterexample; students fall into it and score 0/4 on D5. This is
  pedagogically critical.

[HIGH] [Scenario-catalog §4 carbon_levy weight field units] [03]
Title: lta-carbon-levy weight 0.18 per_km vs baseline fuel weight 0.35 per_km — unit mismatch in acceptance
Problem: scenario-catalog §4 ships carbon_levy with weight 0.18 unit per_km. This pair already
  exists as a distinct 4th term alongside fuel (weight 0.35 per_km). Shard 03 acceptance does
  not specify how the solver aggregates two per_km weights. The learning objective D3 depends
  on the student seeing a specific $0.53/km combined cost (0.35 + 0.18 = 0.53).
Fix: Shard 03 acceptance MUST assert: objective_value scales linearly with total_km for any
  per_km-weighted term; the solver aggregates per_km weights via simple sum. Add a wiring test
  that POSTs a 4-term objective and asserts objective_value ≈ sum(weights × units).
Blast radius: Without a sum-contract, the solver could (a) pick max instead of sum, (b) apply
  weights only to the fuel term, (c) double-count. Journal Phase 10 entries cite cost deltas
  that don't match the solver output; D3 score is unverifiable.
```

### MEDIUM (13)

```
[MEDIUM] [Test-naming convention] [06-cli-and-grader.md]
Title: test_grader_placeholder_detection.py uses "detection" instead of testing.md naming scheme test_[feature]_[scenario]_[expected_result].py
Fix: Rename test_grader_detects_placeholder_and_scores_zero.py.
Blast radius: Low.

[MEDIUM] [LOC estimate vs content] [06-cli-and-grader.md:loc_estimate=480]
Title: 480 LOC for 4 scripts (preflight + scenario_inject + journal_cli + grade_product) with 11 fix messages and 3 tests is underestimated
Problem: Realistic: preflight.py 120, scenario_inject.py 250 (5 events × 50 LOC each with rollback),
  journal_cli.py 300 (add with frontmatter auto-linkage + list + export + pandoc + fallback),
  grade_product.py 220 (5 assertions × 40 LOC + fix-message lookup + report JSON + colour
  output), fix_messages.json 80, 3 tests × 60 = 180. Total ~1150 LOC.
Fix: Split shard 06 into 06a (preflight + scenario_inject) and 06b (journal_cli + grade_product
  + fix_messages).
Blast radius: Shard 06 depends_on=[01,02,03,04,07] — at the end of the dependency chain. Critical
  path pressure + underestimated LOC = schedule slip risk.

[MEDIUM] [Invariant-budget description count] [01-backend-core.md]
Title: Shard 01 lists 5 invariants but the acceptance criteria imply ≥8
Problem: Hidden invariants: model_version_id derivation (canonical-values §5), drift_status endpoint
  reference-set semantics, 501-stub banner verbatim copy, .preflight.json atomic rename, conftest
  tmp_path fixture lifecycle. 8-9 invariants overall.
Fix: Enumerate all invariants in frontmatter.
Blast radius: Same Phase 5.11 risk.

[MEDIUM] [Terrene-naming compliance] [05-viewer-pane.md]
Title: Viewer/scaffold doc uses "Trust Plane" / "Execution Plane" correctly but inside panels the terminology is absent
Problem: viewer-pane.md §3 panels do not surface Trust/Execution Plane labels in the UI. The
  workshop persona (Ops Manager = Trust Plane) is a learning outcome; surfacing on the dashboard
  would reinforce it.
Fix: Add PlaybookProgress strip label: "Trust Plane decisions" — orients the student.
Blast radius: Learning objective alignment; not a ship-blocker.

[MEDIUM] [Dependency arithmetic] [07-data-and-leaderboard.md:blocks]
Title: Shard 07 claims to block shards 01/02/03/04/06, but 03 does not consume any 07 output
Problem: Shard 03 (optimize endpoints) depends on OR-Tools + PuLP + route plan data. It does
  NOT read northwind_demand.csv, leaderboard_prebaked.json, drift_baseline.json, or union_cap.json
  from shard 07. It DOES read data/forecast_output.json (written by /forecast/predict in shard
  02) and data/route_plan.json (written by itself). Shard 07's "blocks 03" declaration
  overstates the dependency.
Fix: Change shard 07 blocks to [01, 02, 04, 06]. Shard 03 can start once 01 is done.
Blast radius: Lost parallelism — shard 03 could start one slot earlier than the claimed graph
  allows.

[MEDIUM] [Missing invariant] [02-forecast-endpoints.md]
Title: Shard 02 does not assert the experiment_name "forecast_sprint1" is the literal string
Problem: product-northwind §8.1 uses experiment_name='forecast_sprint1'. Shard 02 acceptance
  mentions it but does not assert literal match.
Fix: Add invariant: "experiment_name='forecast_sprint1' is the literal string; downstream
  grader relies on it for list_runs filter (rubric-grader §3.2)."
Blast radius: If experiment_name drifts, grader's list_runs(experiment_name=...) returns empty;
  /forecast/compare can't find ≥3 runs.

[MEDIUM] [tenant-isolation.md acknowledgment only] [01, 02, 06]
Title: Shards don't explicitly adopt the tenant-isolation.md MUST Rule 1 stance
Problem: product-northwind §9 acknowledges tenant-isolation deferred to Week 5+. Shards 01 and
  02 do not assert "multi_tenant=False on every model" OR document the single-tenant assumption
  explicitly. Journal entries could claim "multi-tenant safe" without evidence.
Fix: Add to shard 01 invariants: "single-tenant assumption — no tenant_id in any cache key,
  audit row, or metric label; any future multi-tenant extension MUST follow tenant-isolation.md
  Rule 1-5." Document in app.py as a comment.
Blast radius: Low for Week 4; foundational for Week 5+.

[MEDIUM] [Missing: scripts/grade_fix_messages.json format] [06]
Title: Shard 06 specifies 11 fix-message entries but does not pin the JSON schema
Problem: grade_fix_messages.json format is not declared. Fields? key=error name, value=string
  message? key=(endpoint, status), value=dict of {message, hint}? Implementation sketch says
  "11 key-value entries".
Fix: Pin schema: `{"endpoint:status": {"message": "...", "hint": "..."}}` OR similar.
Blast radius: Test test_grader_placeholder_detection uses this file; undefined schema = brittle
  test.

[MEDIUM] [Scaffold-contract.md §10 openai/anthropic keys] [01]
Title: OPENAI_API_KEY and ANTHROPIC_API_KEY are commented-out but shard 01 may include them as active
Problem: scaffold-contract §10: "# OPENAI_API_KEY=  # ANTHROPIC_API_KEY=". These are commented
  because Week 4 does NOT exercise kailash-ml[agents]. Shard 01 "contains all keys" may include
  them as active keys, violating env-models.md (no hard-coded keys) and creating a confusing
  scaffold.
Fix: Shard 01 acceptance MUST say: "keys OPENAI_API_KEY and ANTHROPIC_API_KEY appear as
  commented-out placeholders per scaffold-contract §10 — never as active keys with values."
Blast radius: Students commit .env.example with uncommented LLM keys → secrets land in git
  on copy.

[MEDIUM] [Scaffold-contract §2 routes/__init__.py banner] [01]
Title: Shard 01 ships 501-stub registrations; banner text for routes/__init__.py is not pinned
Problem: Scaffold-contract §2 lists three banner texts verbatim (routes/forecast.py, optimize.py,
  drift.py). routes/__init__.py's 501-stub payload is described ("returns {'error': 'not
  implemented — prompt Claude Code to commission this endpoint', 'hint': 'see PLAYBOOK.md Phase
  4 for /forecast/train'}") but not banner. Shard 01 acceptance says "ships 501-stub registrations
  for forecast/optimize/drift per scaffold-contract.md §2 banner text (verbatim)".
Fix: Shard 01 MUST cite the exact 501 response body, not "banner text". The banner applies to
  routes/forecast.py, optimize.py, drift.py (shards 02, 03, 04), not __init__.py.
Blast radius: Scaffold ships 501 with mismatched payload; grader fails contract.

[MEDIUM] [Shard 08 redeclares PLAYBOOK build target location] [08]
Title: PLAYBOOK.md built into workspace root; shard 08 does not specify absolute path
Problem: 08:30 "writes PLAYBOOK.md"; workspace root path or workspace-relative?
Fix: "writes to workspaces/metis/week-04-supply-chain/PLAYBOOK.md".
Blast radius: Low.

[MEDIUM] [Missing: AI-Verify dimension spec] [scaffold-contract §3; playbook-phases-sml Phase 7]
Title: specs/ai-verify.md referenced but unowned; Phase 7 prompt cites Transparency/Robustness/Safety
Problem: scaffold-contract §3 lists specs/ai-verify.md as PRE-BUILT. Playbook Phase 7 prompt
  cites 3 dimensions + deferred Fairness. No shard authors this file.
Fix: Add to shard 08 (docs) or new shard 09.
Blast radius: Phase 7 prompt references an un-authored spec. Students clicking through read a
  404. Ungradeable.

[MEDIUM] [Shard 07 unit test placement] [07:wiring_tests]
Title: test_data_fixtures_determinism.py placed in tests/unit/ but requires real numpy + real CSV I/O
Problem: Byte-identical output check requires real filesystem + real numpy RNG. This is a
  Tier-2 test by testing.md; Tier 1 allows mocks.
Fix: Move to tests/integration/ OR acknowledge the Tier-1/Tier-2 boundary is soft for
  determinism tests and justify.
Blast radius: Minor; numpy/polars RNG on real inputs is deterministic and safe in Tier-1.
```

### LOW (6)

```
[LOW] [Shard 02 specs_consulted format] — cites "canonical-values.md §8.1-8.3" as a range; expand to explicit list.
[LOW] [Shard 08 specs_consulted format] — cites "scaffold-contract.md §1-8" as range.
[LOW] [Shard 07 FeatureSchema import-time validation] — 07:64 says "validates column presence at import time (raises on mismatch)". This is defensive but possibly over-engineered; a unit test is sufficient.
[LOW] [Shard 05 test coverage] — 3 render-contract tests for 7 components. Add tests for ForecastPanel, RoutePanel, JournalPanel (minimum 1 test per panel).
[LOW] [Shard 06 pandoc fallback naming] — 06 calls it "journal_markdown_fallback.md"; decision-journal §5.2 also says "journal.md" via pure-Python. Pin one name.
[LOW] [Shard 01 ml_context.py module-level _ctx cache] — 01:56 caches in "module-level _ctx". Document if get_ml_context() is meant to be a singleton vs per-request; matters for test isolation.
```

---

## 4. Wiring-Test Ownership Table (§C)

Per `wiring-contracts.md §1-12` + `scaffold-contract.md §9`, 12 components need Tier-2 wiring tests. One owner = compliant; zero or multiple = violation.

| #     | Component              | Test file                               | Shard Owner | Status                                                          |
| ----- | ---------------------- | --------------------------------------- | ----------- | --------------------------------------------------------------- |
| 1     | TrainingPipeline       | test_training_pipeline_wiring.py        | **02**      | OWNED                                                           |
| 2     | AutoMLEngine           | test_automl_engine_wiring.py            | **02**      | OWNED                                                           |
| 3     | ExperimentTracker      | test_experiment_tracker_wiring.py       | **02**      | OWNED                                                           |
| 4     | ModelRegistry          | test_model_registry_wiring.py           | **02**      | OWNED                                                           |
| 5     | InferenceServer        | test_inference_server_wiring.py         | **02**      | OWNED                                                           |
| 6     | DriftMonitor           | test_drift_monitor_wiring.py            | **04**      | OWNED                                                           |
| 7     | ModelExplainer         | test_model_explainer_wiring.py          | **—**       | **GAP**                                                         |
| 8     | DataExplorer           | test_data_explorer_wiring.py            | **—**       | **GAP**                                                         |
| 9     | ModelVisualizer        | test_model_visualizer_wiring.py         | **—**       | **GAP**                                                         |
| 10    | FeatureEngineer        | test_feature_engineer_wiring.py         | **—**       | **GAP** (decision pending)                                      |
| 11    | FeatureStore           | test_feature_store_wiring.py            | **01**      | OWNED                                                           |
| 12    | AnomalyDetectionEngine | test_anomaly_detection_engine_wiring.py | **—**       | **GAP** (decision pending)                                      |
| extra | get_ml_context()       | test_ml_context_wiring.py               | **01**      | OWNED                                                           |
| extra | OR-Tools VRP           | test_ortools_vrp_wiring.py              | **03**      | OWNED                                                           |
| extra | PuLP                   | test_pulp_wiring.py                     | **03**      | OWNED (but uses @patch — testing.md violation — see HIGH above) |

**Compliance**: 8 of 12 required + 3 extras = 8/12 (67%) wiring-contracts.md compliance.
**Action**: C2 (CRITICAL) above must be resolved at /todos gate.

---

## 5. Endpoint Contract Alignment Table (§D)

For each endpoint: producing shard ▸ grader shard ▸ viewer shard ▸ scenario-inject shard.

| Endpoint               | Producer         | Grader Assertion                                                          | Viewer Consumer                                            | Scenario Re-trigger                                                    | Status                        |
| ---------------------- | ---------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------- | ----------------------------- |
| POST /forecast/train   | **02** ✓         | **06** ✓ (4 sub-assertions)                                               | 05 Leaderboard (leaderboard.json)                          | —                                                                      | CLEAN                         |
| GET /forecast/compare  | **02** ✓         | **06** ✓ (≥3 runs, distinct params_hash)                                  | 05 Leaderboard                                             | drift-week-78 re-run Phase 5 (ambiguous cascade)                       | CLEAN                         |
| POST /forecast/predict | **02** ✓         | **06** ✓ (stage ∈ staging/shadow/production + numeric predictions)        | 05 ForecastPanel (forecast_output.json)                    | drift-week-78 overlay                                                  | CLEAN                         |
| POST /optimize/solve   | **03** ✓         | **06** ✓ (feasibility + optimality_gap + hard_constraints_satisfied keys) | 05 RoutePanel (route_plan.json + \_preunion + \_postunion) | union-cap re-trigger (06 ✓) + **lta-carbon-levy 4-term body (C1 GAP)** | BROKEN — see C1               |
| POST /drift/check      | **04** ✓         | **06** ✓ (name ∈ ks/psi + overall_severity enum)                          | 05 DriftPanel (drift_report.json)                          | drift-week-78 re-trigger (06 ✓)                                        | CLEAN                         |
| GET /health            | **01** ✓         | **06** ✓ (preflight check)                                                | 05 PreflightBanner (.preflight.json)                       | —                                                                      | CLEAN (with H4 overlap noted) |
| GET /drift/status/<id> | **01** ✓         | — (not in grader)                                                         | 05 DriftPanel debug row                                    | —                                                                      | CLEAN                         |
| POST /drift/anomalies  | **—** (proposed) | **—**                                                                     | **—**                                                      | **—**                                                                  | **GAP** (see HIGH above)      |

**Action**: C1 and H5 (AnomalyDetectionEngine) must resolve before /implement.

---

## 6. Scenario End-to-End Traces (§E)

For each live scenario, trace: trigger → mutation → endpoint re-trigger → Viewer → rollback.

### `union-cap` (Sprint 2, minute 30; LIVE Week 4)

| Step                                                                                  | Owner                                             | Status |
| ------------------------------------------------------------------------------------- | ------------------------------------------------- | ------ |
| Trigger: `metis scenario fire union-cap`                                              | 06 ✓                                              | CLEAN  |
| Precondition: `data/route_plan.json` exists                                           | 03 (producer) ✓                                   | CLEAN  |
| File mutation: snapshot to `_preunion.json` + write `active_union_cap.json`           | 06 ✓                                              | CLEAN  |
| Endpoint re-trigger: POST /optimize/solve with `scenario_tag: "postunion"`            | 03 ✓                                              | CLEAN  |
| Snapshot hygiene: route_plan.json not overwritten; postunion.json written             | 03 ✓ (invariant)                                  | CLEAN  |
| Viewer: RoutePanel toggle default → postunion; pre-union selectable                   | 05 ✓                                              | CLEAN  |
| Rollback: `--undo` restores from \_preunion OR scripts/seed_route_plan.py             | 06 ✓ + **06/07 GAP** on seed_route_plan.py author | BROKEN |
| Journal re-runs: phase_11_postunion.md + phase_12_postunion.md + phase_8_postunion.md | 06 (add command supports) ✓                       | CLEAN  |

### `drift-week-78` (Sprint 3, minute 5; LIVE Week 4)

| Step                                                                          | Owner                                                       | Status |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------- | ------ |
| Trigger: `metis scenario fire drift-week-78`                                  | 06 ✓                                                        | CLEAN  |
| Precondition: shadow-or-higher model in registry                              | 02 (register+promote in /forecast/train + Phase 8 prompt) ✓ | CLEAN  |
| File mutation: `active_drift.json` marker                                     | 06 ✓                                                        | CLEAN  |
| Payload: `data/scenarios/week78_drift.json`                                   | 07 ✓                                                        | CLEAN  |
| Endpoint re-trigger: POST /drift/check with `model_id`                        | 04 ✓                                                        | CLEAN  |
| Viewer: DriftPanel severity + customer_mix KS row + post-drift window overlay | 05 ✓                                                        | CLEAN  |
| Rollback: `--undo` removes active_drift.json                                  | 06 ✓                                                        | CLEAN  |
| Journal re-runs: phase_13_retrain + phase_5_postdrift + phase_6_postdrift     | 06 ✓                                                        | CLEAN  |

### `lta-carbon-levy` (Sprint 2 or 3; LIVE Week 4)

| Step                                                                     | Owner                                                                                        | Status     |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- | ---------- |
| Trigger: `metis scenario fire lta-carbon-levy`                           | 06 ✓                                                                                         | CLEAN      |
| Precondition: one `/optimize/solve` run logged                           | 03 ✓                                                                                         | CLEAN      |
| File mutation: `active_lta_carbon_levy.json` marker                      | 06 ✓                                                                                         | CLEAN      |
| **Endpoint re-trigger: POST /optimize/solve with 4-term objective body** | **03 — GAP C1**                                                                              | **BROKEN** |
| Viewer: OptimizePanel carbon_levy row + before/after overlay             | 05 — **GAP** (viewer-pane.md does not specify OptimizePanel; scenario-catalog §4 invents it) | BROKEN     |
| Rollback: `--undo` removes marker                                        | 06 ✓                                                                                         | CLEAN      |
| Journal: Phase 10 objective entry with cost delta                        | — (student-written per playbook)                                                             | CLEAN      |

### `hdb-loading-curfew` (dry-run only; Week 5+)

CLEAN — dry-run path produces exit 0; live-fire exits 5 (06 ✓).

### `mas-climate-disclosure` (dry-run only; Week 5+)

CLEAN — dry-run path; audit-schema migration deferred (06 ✓).

### **Findings from traces**

- `lta-carbon-levy`: 2 broken steps (endpoint + viewer).
- `union-cap`: 1 broken step (seed_route_plan.py unowned — CRITICAL C5).

---

## 7. Recommended Fix Order (dependency-aware)

Apply in this order to avoid re-shuffling.

1. **C5** — Create shard 09 "Scaffold Support Artefacts" owning the 14 unowned files. Depends_on=[]. Blocks every other shard that imports them. Adjust DAG.
2. **C1 + H14** — Extend shard 03 scope: accept variable-length objective.terms (3 or 4); add wiring test for 4-term objective; update scenario-catalog §4 references. Reconcile with shard 05 viewer-pane.md §3.4 (RoutePanel consumes route_plan.json; no OptimizePanel exists — decide whether to add).
3. **C3 + M5** — Fix shard 07 dependency: either split into 07a (static) + 07b (leaderboard via live ml_context, depends_on=[01]) OR make 07 depends_on=[01]. Update blocks list to [01_partial, 02, 04, 06].
4. **C6 + H4** — Pin .env.example and .preflight.json merge protocols. Shard 01 owns .env.example with all 13 keys; shards 01 and 06 both write .preflight.json via read-modify-write with atomic rename.
5. **C2** — Resolve 5 orphan wiring tests. Add to shard 02: ModelExplainer, DataExplorer, ModelVisualizer (3 tests). Decide at /todos: wire-or-delete FeatureEngineer, AnomalyDetectionEngine (2 components).
6. **C4 + H10** — Move 06's three wiring tests to tests/integration/; remove @patch on ortools in 03's test_pulp_wiring (use real uninstalled env or env var guard).
7. **H1 + H2** — Split shard 03 (OR-Tools + PuLP + snapshot + 4-term) into 03a + 03b; split shard 05 (panels + watcher) into 05a + 05b OR justify with feedback-loop multiplier.
8. **H3** — Specify conftest.py ownership + extension protocol (01 owns; 02 extends via separate file).
9. **H7** — Add workshop-runofshow.md to shard 06 + 08 specs_consulted; cross-reference minute-by-minute deliverables.
10. **H11 + H12** — Add alias-file `data/.experiment_aliases.json` helper to shard 01; pin candidate_families format (fully qualified sklearn.\* names).
11. **H13** — Add journal/\_template.md + journal/\_examples.md to shard 08 (or new shard 09 per C5).
12. All MEDIUM findings — address after CRITICAL/HIGH resolved.
13. LOW findings — defer post-workshop.

---

## 8. GO / NO-GO Verdict

**VERDICT: NO-GO.**

The shard decomposition is architecturally sound and covers ~85% of spec surface, but has:

- **8 CRITICAL findings** — any single one of C1 (4-term objective), C2 (5 orphaned wiring tests), C3 (dependency graph wrong), C4 (Tier-1/Tier-2 mis-placement), C5 (14 unowned files), C6 (.env.example overlap), C7 (.preflight.json overlap) — ships the scaffold with demonstrable Phase 5.11 orphan-shaped code OR a non-running workshop.
- **14 HIGH findings** — including 3 that violate testing.md (Tier-2 mocks) + 2 that violate autonomous-execution.md (invariant-budget overflows at shards 03 and 05) + 1 orphan-detection Rule 3 violation (AnomalyDetectionEngine "decide later").

**Proceeding to /implement without resolving C1-C7 and H1-H4 will produce a scaffold that:**

- Crashes at minute 30 of Sprint 2 when lta-carbon-levy fires (C1).
- Ships with 5 orphaned engines that downstream consumers build against (C2).
- Cannot generate leaderboard_prebaked.json because shards 01 and 07 race (C3).
- Passes wiring tests on mocks but fails on real infrastructure (C4, H10).
- Has 14 unowned scaffold files that block workshop start (C5).
- Races on .env.example and .preflight.json writes (C6, C7).
- Shards 03 and 05 overflow invariant budget and produce Phase 5.11-style orphaned code (H1, H2).

**Action before /implement**: Return to /todos; rebuild the DAG per "Recommended Fix Order" above; resolve C1-C7 as hard pre-conditions; H1-H4 as strong shoulds. Estimated rework: 1 autonomous session (sharding + DAG update, no code).

**Re-review gate**: After rework, re-run this red-team against the updated shards. Expected outcome post-fix: CRITICAL ≤ 0, HIGH ≤ 3 (residual: invariant-budget splits require justification, not zero).
