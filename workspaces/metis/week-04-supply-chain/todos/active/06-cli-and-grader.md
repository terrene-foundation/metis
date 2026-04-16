---
shard_id: 06
slug: cli-and-grader
title: >
  Implement four scripts under scripts/: preflight.py (env + health check),
  scenario_inject.py (all 5 events from scenario-catalog.md), journal_cli.py
  (metis journal add/list/export + PDF via pandoc), and grade_product.py
  (5 endpoint contract assertions from rubric-grader.md §3), plus a regression
  test per script verifying its exit-code contract.
loc_estimate: 480
invariants:
  - preflight-hard-fail: preflight.py exits non-zero on any false field in /health (db/feature_store/drift_wiring); never continues past a failing check — no "warning, proceeding" path
  - scenario-idempotency: scenario_inject.py exits 4 "already fired" when the active marker exists; requires --re-fire to replay; never overwrites a live marker silently
  - journal-append-only: journal_cli.py add command preserves prior content as "## Previous draft" when the phase+scenario file already exists; destructive overwrite is BLOCKED per decision-journal.md §4.0
  - grader-no-retry: grade_product.py does NOT retry on 5xx; httpx.Client(timeout=120); exit code 0 iff all 5 pass per rubric-grader.md §3.4
  - grade-fix-messages: every grader 4xx/5xx maps to a specific fix instruction from scripts/grade_fix_messages.json; bare stack traces are BLOCKED per rubric-grader.md §3.2 step 4
call_graph_hops: 3
depends_on: [01, 02, 03, 04, 07]
blocks: []
specs_consulted:
  - specs/scaffold-contract.md §6 (scripts/ file list and roles, verbatim role descriptions)
  - specs/scenario-catalog.md §2-7 (all 5 event IDs, exit codes, pre-conditions, file mutations, rollback contract)
  - specs/decision-journal.md §4 (journal lifecycle state machine, add/list/export CLI contract, auto-linkage, append-only rule)
  - specs/decision-journal.md §5 (PDF export: pandoc, LaTeX template, graceful fallback to .md + .html)
  - specs/rubric-grader.md §3 (grade_product.py inputs, execution order, report format, fix messages, no-retry on 5xx, 120s timeout)
  - specs/canonical-values.md §11 (registered scenario IDs)
  - specs/scenario-injection.md (CLI mechanics: firing, logging to .scenario_log.jsonl, rollback, topology)
acceptance_criteria:
  - scripts/preflight.py verifies [xgb], [explain], ortools, pulp installed; detects port 8000/3000 collisions via psutil and prints "port 8000 taken — export KAILASH_NEXUS_PORT=8001 and retry"; probes GET :8000/health asserting ok/db/feature_store/drift_wiring all true; hard-fails (non-zero exit) on any false; writes .preflight.json; per scaffold-contract.md §6
  - scripts/scenario_inject.py implements all 5 events from scenario-catalog.md §7: union-cap, drift-week-78, lta-carbon-levy, hdb-loading-curfew (dry-run only in Week 4 — exit code 5 on live-fire), mas-climate-disclosure (dry-run only — exit code 5 on live-fire)
  - scenario_inject.py exit codes match scenario-catalog.md §2-6: 0 fired, 1 unknown event, 2 workspace not detected, 3 pre-condition not met, 4 already fired, 5 Week 5+ only
  - scenario_inject.py --undo deletes the active marker for all 3 live-fire events; for union-cap --undo also restores route_plan.json from the _preunion snapshot; appends .scenario_log.jsonl on fire AND undo
  - scripts/journal_cli.py implements metis journal add [--phase N] [--scenario tag]: copies journal/_template.md → journal/phase_<N>_<slug>.md; fills frontmatter (phase, phase_name, sprint, timestamp, experiment_run_ids via ExperimentTracker.list_runs, model_version_ids via ModelRegistry.list_models + derive_model_version_id, scenario_tag); opens $EDITOR; updates journal/.last_entry_timestamp atomically; per decision-journal.md §4.1
  - journal_cli.py add on existing phase+scenario file appends "## Previous draft" with prior content; never overwrites per decision-journal.md §4.0
  - journal_cli.py list [--phase N] [--scenario tag] prints one-line summary per entry in phase-then-timestamp order per decision-journal.md §4.2
  - journal_cli.py export [--output journal.pdf] invokes pandoc via subprocess; on pandoc/LaTeX absent emits journal_markdown_fallback.md with explicit "PDF export failed because <reason>" banner (NOT silent); per decision-journal.md §5.2
  - scripts/grade_product.py --base-url --student-id --output: preflight check GET /health; 5 endpoint assertions in sequence per rubric-grader.md §3.2; httpx.Client(timeout=120); NO retry on 5xx; exit 0 iff all pass
  - grade_product.py all 5 endpoint contracts per rubric-grader.md §2: /forecast/train (experiment_run_id present + tracker_get_run_succeeds + metrics_count_ge_2 + training_timestamp_nonnull), /forecast/compare (>=3 runs + distinct params_hash + numeric metric), /forecast/predict (model_version_id form {name}_v{version} + registry stage in {staging,shadow,production} + non-empty predictions list), /optimize/solve (feasibility:true + optimality_gap:float>=0 + hard_constraints_satisfied dict with vehicle_capacity+driver_hours_max), /drift/check (name in {ks,psi} + numeric statistic + overall_severity in {none,moderate,severe})
  - grade_product.py treats placeholder:true in response as 0% + prints "this endpoint is still a scaffold placeholder" per rubric-grader.md §3.5
  - grade_product.py emits grade_report.json matching schema in rubric-grader.md §3.3; console output mirrors JSON in colour-coded table
  - scripts/grade_fix_messages.json contains all error → fix-instruction mappings from rubric-grader.md §3.2 step 4 (11 entries enumerated in spec)
  - tests/integration/test_scenario_inject_exit_codes.py passes: asserts exit codes 3 (no pre-condition file), 4 (already fired marker present), 5 (hdb-loading-curfew live-fire blocked) against a real tmp_path fixture workspace; uses real filesystem (no mocks) per testing.md Tier-2 rule
  - tests/integration/test_journal_cli_append_only.py passes: asserts existing phase file gets "## Previous draft" section using real filesystem writes; real tmp_path workspace; no Mock()
  - tests/integration/test_grader_placeholder_detection.py passes: asserts grade_product.py scores 0% when response contains placeholder:true; uses real httpx against a real Nexus TestClient (no MagicMock)
  - scripts/grade_product.py resolves any experiment_run_id in journal frontmatter via ml_context.resolve_experiment_run_id(...) before calling ExperimentTracker.get_run; accepts UUID4 OR alias (per canonical-values.md §12); fails with actionable message when alias is unknown (no silent pass)
  - scripts/grade_product.py leaderboard comparison accepts fully-qualified model_class names ONLY (per canonical-values.md §8.7); short names (e.g. "LinearRegression" without module path) fail with a guidance message pointing to §8.7 regex ^[a-z_]+(\.[a-z_]+)+\.[A-Z][A-Za-z]+$
tier2_classification_note: >
  These three tests were previously misclassified as tests/unit/. They exercise real filesystem
  (.scenario_log.jsonl append, journal/_template.md copy), real subprocess ($EDITOR, pandoc),
  and real httpx against a live endpoint. Per testing.md Tier-2 definition (real infrastructure,
  NO mocking — @patch, MagicMock, unittest.mock BLOCKED), they belong in tests/integration/.
wiring_tests:
  - tests/integration/test_scenario_inject_exit_codes.py (scenario-catalog.md §2-6 exit code contract; real filesystem)
  - tests/integration/test_journal_cli_append_only.py (decision-journal.md §4.0 append-only rule; real filesystem)
  - tests/integration/test_grader_placeholder_detection.py (rubric-grader.md §3.5 stub-detection; real httpx)
---

# Shard 06 — CLI and Grader

## What

Implement all four `scripts/` executables: `preflight.py` (env health gate), `scenario_inject.py` (all 5 scenario events with idempotency and rollback), `journal_cli.py` (`metis journal add/list/export` with PDF via pandoc), and `grade_product.py` (5 non-trivial endpoint contract assertions). Three unit tests guard the most failure-prone invariants: exit-code contract for scenario injection, append-only rule for journal, and stub-detection for the grader.

## Why

`grade_product.py` is the 40%-of-grade instrument run publicly at 03:20 — any regression in its assertion logic produces wrong grades in front of the cohort. `scenario_inject.py`'s idempotency guard (`already fired` exit 4) is the primary safeguard against a student accidentally double-firing `union-cap` and clobbering their `route_plan_preunion.json` baseline. `journal_cli.py`'s append-only invariant prevents a `metis journal add --phase 5` call from destroying the student's prior Phase 5 entry mid-workshop.

## Implementation sketch

- `preflight.py` — `importlib.util.find_spec` checks for each extra; `psutil.net_connections` for port collision; `httpx.get("/health")` with response-field validation; `json.dump` to `.preflight.json`; `sys.exit(1)` on any failure
- `scenario_inject.py` — subcommand dispatch on first arg; per-event handler reads precondition file (raises exit 3 if absent), checks active marker (raises exit 4 if present unless `--re-fire`), writes active marker + appends `.scenario_log.jsonl`; `--undo` deletes marker; `hdb-loading-curfew` and `mas-climate-disclosure` always exit 5 on live-fire path (dry-run printed then exit 0)
- `journal_cli.py` — `add`: read template, fill frontmatter via `ml_context` API calls, check for existing file (append `## Previous draft` section if present), write, open `$EDITOR`, update `.last_entry_timestamp` atomically; `list`: walk `journal/*.md`, parse frontmatter, print one-liner; `export`: invoke `pandoc` via subprocess with LaTeX template; fallback to `journal_markdown_fallback.md` on `FileNotFoundError` with explicit banner
- `grade_product.py` — ordered 5-step loop: preflight → each endpoint POST/GET → assert contract fields → map failures to `grade_fix_messages.json` entries → write `grade_report.json` + print colour table; `httpx.Client(timeout=120)` — no retry
- `grade_fix_messages.json` — 11 key-value entries from `rubric-grader.md §3.2 step 4`

## Out of scope

- `seed_experiments.py` and `seed_drift.py` (shard 07 — data generation)
- `run_backend.sh` (trivial shell wrapper, pre-built separately)
- Grader Week 6+ flag `--check-audit-disclosure` (scenario `mas-climate-disclosure` audit path)

## Acceptance

- [ ] scripts/preflight.py verifies extras, ports, /health fields; hard-fails on any false; writes .preflight.json
- [ ] scripts/scenario_inject.py implements all 5 events; exit codes per scenario-catalog.md §2-6; idempotency guard; --undo contract; appends .scenario_log.jsonl
- [ ] scripts/journal_cli.py add fills frontmatter via ml_context APIs; opens $EDITOR; updates .last_entry_timestamp atomically
- [ ] journal_cli.py add on existing file appends "## Previous draft"; never overwrites
- [ ] journal_cli.py list prints one-line summary in phase-then-timestamp order
- [ ] journal_cli.py export invokes pandoc; fallback to journal_markdown_fallback.md with explicit banner on pandoc absent
- [ ] scripts/grade_product.py runs 5 endpoint assertions; httpx.Client(timeout=120); no retry; exit 0 iff all pass
- [ ] grade_product.py all 5 endpoint contracts per rubric-grader.md §2
- [ ] grade_product.py treats placeholder:true as 0%
- [ ] grade_product.py emits grade_report.json per rubric-grader.md §3.3 schema
- [ ] scripts/grade_fix_messages.json contains all 11 error→fix mappings from rubric-grader.md §3.2 step 4
- [ ] tests/integration/test_scenario_inject_exit_codes.py passes (real filesystem, no mocks)
- [ ] tests/integration/test_journal_cli_append_only.py passes (real filesystem, no mocks)
- [ ] tests/integration/test_grader_placeholder_detection.py passes (real httpx, no MagicMock)
