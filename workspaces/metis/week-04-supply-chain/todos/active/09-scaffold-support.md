---
shard_id: 09
slug: scaffold-support
title: >
  Author all unowned scaffold support artefacts: PRODUCT_BRIEF.md,
  journal/_template.md, journal/_examples.md, specs/schemas/routes.py,
  specs/business-costs.md, specs/success-criteria.md, specs/api-surface.md,
  specs/rubric.md, specs/ai-verify.md, scripts/run_backend.sh,
  scripts/seed_route_plan.py, scripts/instructor_brief.md,
  .github/workflows/preflight.yml, .github/workflows/grade.yml,
  .env.example (SOLE WRITER), and .preflight.json initial shape.
loc_estimate: 400
invariants:
  - env-example-sole-writer: shard 09 is the ONLY shard that writes .env.example; shards 01 and 07 READ but do not write; the file contains ALL 14 keys from scaffold-contract.md §10 including RANDOM_SEED/AUTOML_SEED/DRIFT_SEED
  - preflight-json-initialised-by-06: .preflight.json is initialised (all 8 fields → false) by scripts/preflight.py (shard 06) on every preflight run; shard 09 ships the documented initial-shape schema only (not a generated file)
  - journal-template-decision-journal-compliant: journal/_template.md implements exactly the 5 heading schema from decision-journal.md §2; no extra headings, no missing headings
  - journal-examples-rubric-grounded: journal/_examples.md contains at least one 4/4 and one 1/4 example per rubric dimension using real $40/$12 numbers from business-costs.md; examples match rubric-grader.md §1.1 and §1.2 anti-pattern list
  - routes-schema-matches-optimize-contract: specs/schemas/routes.py FeatureSchema classes (Vehicle, DeliveryWindow, RoutePlan, ConstraintSet) match the canonical-values.md §8.4 request schema field names exactly; used by solvers/vrp_solver.py
call_graph_hops: 2
depends_on: []
blocks: [01, 06, 07, 08]
sole_writer_declaration:
  .env.example: shard 09
  .preflight.json_initial_schema: shard 09 (documents shape; shard 06 preflight.py initialises at runtime; shards 01 fs_preload/drift_wiring update specific keys via read-modify-write)
specs_consulted:
  - specs/scaffold-contract.md §1 (workspace root PRE-BUILT list: PRODUCT_BRIEF.md, journal/_template.md, journal/_examples.md, .env.example)
  - specs/scaffold-contract.md §3 (specs/ PRE-BUILT list: schemas/routes.py, business-costs.md, success-criteria.md, api-surface.md, rubric.md, ai-verify.md)
  - specs/scaffold-contract.md §6 (scripts/ PRE-BUILT list: run_backend.sh, seed_route_plan.py, instructor_brief.md)
  - specs/scaffold-contract.md §7 (CI PRE-BUILT list: .github/workflows/preflight.yml, .github/workflows/grade.yml)
  - specs/scaffold-contract.md §10 (.env.example key enumeration — 14 keys)
  - specs/decision-journal.md §2 (journal/_template.md: 5 headings schema)
  - specs/decision-journal.md §3 (journal/_examples.md: worked examples)
  - specs/rubric-grader.md §1.1 AND §1.2 (D1-D5 anchors + anti-patterns for examples)
  - specs/canonical-values.md §8.4 (RoutePlan / ConstraintSet field names for specs/schemas/routes.py)
  - specs/canonical-values.md §6 (Northwind business numbers: $40/$12/$220 for business-costs.md)
  - specs/scenario-catalog.md §8 (chat snippets for instructor_brief.md)
  - specs/scenario-injection.md §4 (chat snippets for instructor_brief.md)
  - specs/workshop-runofshow.md §0 (pre-class dry-run steps referenced by instructor_brief.md)
acceptance_criteria:
  - .env.example exists with all 14 keys from scaffold-contract.md §10: KAILASH_NEXUS_PORT, KAILASH_ML_AUTOML_QUICK, DATABASE_URL_EXPERIMENTS, DATABASE_URL_REGISTRY, DATABASE_URL_FEATURES, ARTIFACT_DIR, RANDOM_SEED=42, AUTOML_SEED=2026, DRIFT_SEED=78, NEXT_PUBLIC_POLL_MS, NEXT_PUBLIC_BACKEND_PORT, METIS_WORKSPACE_ROOT, OPENAI_API_KEY (commented), ANTHROPIC_API_KEY (commented); no other shard writes this file
  - PRODUCT_BRIEF.md exists at workspace root with: business context summary, cost table ($40/unit stockout, $12/unit overstock, $220/SLA violation from canonical-values.md §6), 5 personas from product-northwind.md §3, and "3:30 pm success definition" section per scaffold-contract.md §1
  - journal/_template.md implements the 5-heading entry schema from decision-journal.md §2: ## What I Decided, ## Why, ## What I Tried, ## What I Learned, ## Next; includes frontmatter stubs (phase, phase_name, sprint, timestamp placeholders)
  - journal/_examples.md contains: at least one 4/4 journal entry per rubric dimension using real domain numbers (D1: $40/$12 asymmetry named; D2: MAPE improvement quantified; D3: $0.53/km delta named; D4: OOD risk framed; D5: deployment gate named); at least one 1/4 entry per dimension showing the anti-pattern from rubric-grader.md §1.2 (e.g. "if data changes" for D5, "costs more" without ratio for D1)
  - specs/schemas/routes.py defines Vehicle, DeliveryWindow, RoutePlan, ConstraintSet dataclasses with field names matching canonical-values.md §8.4 request schema exactly; importable as `from specs.schemas.routes import RoutePlan`
  - specs/schemas/demand.py is NOT authored here — it is shard 07's responsibility
  - specs/business-costs.md lists all dollar figures used in prompts and rubric grading: stockout_cost_per_unit=$40, overstock_cost_per_unit=$12, sla_violation_penalty=$220, driver_overtime_daily=$85, carbon_levy_per_km=$0.18; cited by START_HERE.md prompt templates (shard 08) and grade_product.py grader fix messages (shard 06)
  - specs/success-criteria.md defines the 5 endpoint contract assertions imported by grade_product.py; field names and assertion logic match rubric-grader.md §2 exactly; importable Python dict or dataclass
  - specs/api-surface.md documents all 6 endpoints (/forecast/train, /forecast/compare, /forecast/predict, /optimize/solve, /drift/check, /health) with full request/response schema and error taxonomy; mirrors canonical-values.md §8.1-§8.6 in prose format for student reference
  - specs/rubric.md documents the 5-dimension rubric (D1-D5), 0/2/4 anchors, and applicability matrix from rubric-grader.md §1 in student-readable format; includes the worked 4/4 and 1/4 example pair per dimension
  - specs/ai-verify.md documents the Transparency, Robustness, Safety dimensions for the AI governance review checkpoint (Phase 9 / Phase 13 codify step)
  - scripts/run_backend.sh: single-command backend launcher (`uvicorn src.backend.app:app --reload --port ${KAILASH_NEXUS_PORT:-8000}`); sources .env if present; exits non-zero if .preflight.json ok field is false; per scaffold-contract.md §6
  - scripts/seed_route_plan.py: regenerates data/route_plan.json from the northwind fixture to a known-good baseline state; used by scenario_inject.py --undo for union-cap rollback per scenario-injection.md §2.1; accepts --seed arg defaulting to RANDOM_SEED env
  - scripts/instructor_brief.md: contains the pre-class dry-run checklist (workshop-runofshow.md §0), chat snippets for all 5 scenarios from scenario-catalog.md §8 and scenario-injection.md §4, per-scenario "what to say when" notes, and timing contingency paths from workshop-runofshow.md §7
  - .github/workflows/preflight.yml: runs `python scripts/preflight.py` on push to main; fails build on non-zero exit; per scaffold-contract.md §7
  - .github/workflows/grade.yml: runs `python scripts/grade_product.py --base-url http://localhost:8000 --student-id ci` after spinning up the backend; uploads grade_report.json as artifact; per scaffold-contract.md §7
  - tests/unit/test_env_example_has_all_keys.py passes: reads .env.example and asserts all 14 keys from scaffold-contract.md §10 are present (one test per key); asserts no key appears more than once
  - tests/unit/test_routes_schema_importable.py passes: imports Vehicle, DeliveryWindow, RoutePlan, ConstraintSet from specs.schemas.routes; asserts each has the expected field names from canonical-values.md §8.4
wiring_tests:
  - tests/unit/test_env_example_has_all_keys.py (.env.example contains all 14 scaffold-contract.md §10 keys; sole-writer contract verified)
  - tests/unit/test_routes_schema_importable.py (specs/schemas/routes.py importable with correct field names)
---

# Shard 09 — Scaffold Support Artefacts

## What

Author all scaffold support files that no prior shard owned: workspace-root documents (PRODUCT_BRIEF.md, journal templates and examples), workshop-local specs (routes.py schema, business-costs.md, success-criteria.md, api-surface.md, rubric.md, ai-verify.md), operational scripts (run_backend.sh, seed_route_plan.py, instructor_brief.md), CI workflows (preflight.yml, grade.yml), and the single authoritative .env.example. This shard is the sole writer of .env.example and the initial .preflight.json schema document.

## Why

Every other shard either reads .env.example (shards 01, 02, 03, 04, 06, 07) or reads the specs/ support files (shards 06 imports specs/success-criteria.md; shard 08 references specs/business-costs.md). Without a sole writer for .env.example, parallel /implement runs race-write the file and silently drop either backend keys or seed values — a workshop-day blocker. Without journal/\_template.md, `metis journal add` crashes. Without specs/success-criteria.md, grade_product.py cannot import its assertion contract.

The instructor_brief.md is critical for the 210-minute workshop: without it, the instructor has no pre-authored chat snippets for the 5 scenario injections and no pre-class dry-run checklist, producing a recovery scenario instead of a smooth run-of-show.

## Implementation sketch

- `.env.example` — hand-authored with all 14 keys; secrets (OPENAI_API_KEY, ANTHROPIC_API_KEY) commented out with `# optional:`; values for deterministic seeds are pinned (RANDOM_SEED=42, etc.)
- `PRODUCT_BRIEF.md` — 4 sections: Business Context (3-sentence Northwind framing), Cost Table (markdown table, dollar values from canonical-values.md §6), Personas (5 rows from product-northwind.md §3), 3:30pm Success Definition (3 bullet checklist)
- `journal/_template.md` — frontmatter + 5 heading stubs; instructions per decision-journal.md §2
- `journal/_examples.md` — intro note linking to rubric.md; 5 pairs (4/4 then 1/4) for D1-D5; D1 pair uses $40/$12 asymmetry; D3 pair uses $0.53/km delta; anti-patterns sourced verbatim from rubric-grader.md §1.2
- `specs/schemas/routes.py` — Python dataclasses; `@dataclass` Vehicle(id, capacity_kg, max_hours_per_day), DeliveryWindow(depot_id, open_hour, close_hour), RoutePlan(depots, vehicles, delivery_windows, stops), ConstraintSet(hard, soft) matching canonical-values.md §8.4 field names
- `specs/business-costs.md` — markdown table; 5 cost terms with unit, value, canonical spec reference, usage in prompt templates
- `specs/success-criteria.md` — Python module defining `ENDPOINT_CONTRACTS` dict keyed by endpoint path, each entry a list of assertion callables; imported by grade_product.py
- `specs/api-surface.md` — prose documentation of all 6 endpoints, request/response shapes, error taxonomy; cross-references canonical-values.md §8.1-§8.6 explicitly
- `specs/rubric.md` — student-readable rubric; D1-D5 anchors (0/2/4), applicability matrix, 4/4 and 1/4 worked example pair per dimension
- `specs/ai-verify.md` — 3-dimension (Transparency/Robustness/Safety) checklist for the Phase 9 / Phase 13 AI governance review
- `scripts/run_backend.sh` — 5-line shell script; sources .env; runs uvicorn; hard-exits if preflight not green
- `scripts/seed_route_plan.py` — reads northwind_demand.csv, generates a baseline route_plan.json using a deterministic heuristic (nearest-depot assignment); writes data/route_plan.json; used by scenario_inject.py --undo
- `scripts/instructor_brief.md` — 3 sections: Pre-Class Checklist (from workshop-runofshow.md §0), Scenario Chat Snippets (one subsection per scenario from scenario-catalog.md §8), Timing Contingencies (from workshop-runofshow.md §7)
- `.github/workflows/preflight.yml` — on push to main: checkout, pip install -r requirements.txt, python scripts/preflight.py
- `.github/workflows/grade.yml` — on push to main: checkout, start backend, run grade_product.py, upload grade_report.json artifact

## Out of scope

- specs/schemas/demand.py (shard 07 is sole owner)
- Data generation scripts seed_experiments.py, seed_drift.py (shard 07)
- PLAYBOOK.md, SCAFFOLD_MANIFEST.md, START_HERE.md (shard 08)
- Route handler implementations (shards 02, 03a, 03b, 04)

## Acceptance

- [ ] .env.example exists with all 14 keys from scaffold-contract.md §10; sole writer is this shard; RANDOM_SEED=42, AUTOML_SEED=2026, DRIFT_SEED=78 present
- [ ] PRODUCT_BRIEF.md exists with 4 sections: Business Context, Cost Table ($40/$12/$220), Personas, 3:30pm Success Definition
- [ ] journal/\_template.md implements 5-heading schema from decision-journal.md §2; frontmatter stubs present
- [ ] journal/\_examples.md contains 4/4 and 1/4 example pair for each of D1-D5; D1 uses $40/$12; D3 uses $0.53/km delta; anti-patterns from rubric-grader.md §1.2
- [ ] specs/schemas/routes.py defines Vehicle, DeliveryWindow, RoutePlan, ConstraintSet; field names match canonical-values.md §8.4; importable
- [ ] specs/business-costs.md lists all 5 cost terms with values and spec references
- [ ] specs/success-criteria.md defines ENDPOINT_CONTRACTS dict importable by grade_product.py; matches rubric-grader.md §2 assertions
- [ ] specs/api-surface.md documents all 6 endpoints with request/response schemas and error taxonomy
- [ ] specs/rubric.md documents D1-D5 anchors and 4/4 + 1/4 example pairs per dimension
- [ ] specs/ai-verify.md documents Transparency/Robustness/Safety dimensions
- [ ] scripts/run_backend.sh launches uvicorn from .env; exits non-zero if preflight not green
- [ ] scripts/seed_route_plan.py generates baseline data/route_plan.json deterministically; used by scenario_inject.py --undo
- [ ] scripts/instructor_brief.md contains Pre-Class Checklist, Scenario Chat Snippets (all 5), Timing Contingencies
- [ ] .github/workflows/preflight.yml runs preflight.py on push to main
- [ ] .github/workflows/grade.yml runs grade_product.py on push to main; uploads grade_report.json artifact
- [ ] tests/unit/test_env_example_has_all_keys.py passes: all 14 keys present; no duplicates
- [ ] tests/unit/test_routes_schema_importable.py passes: Vehicle/DeliveryWindow/RoutePlan/ConstraintSet importable with correct field names
