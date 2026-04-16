# Red-Team — Implementation State, Week 4 Supply Chain

**Auditor**: reviewer agent
**Audit date**: 2026-04-16 (lesson T-1)
**Verdict for "lesson can start tomorrow"**: **NO-GO without the 2 MUST-FIX edits below.** Everything else is repivot-able.

---

## 1. Executive Summary

- **CRITICAL**: 4 (backend does not start; 5 required files missing; 0 of 12 wiring tests; 8 of 9 scripts missing including preflight + grader + scenario_inject)
- **HIGH**: 6 (framework-first violation; `run_backend.sh` env-order bug; spec/code drift on `specs/schemas/routes.py` marked STUDENT-COMMISSIONED vs manifest PRE-BUILT; `data/scenarios/` directory missing; `.github/workflows/` missing; viewer-pane spec path drift)
- **MEDIUM**: 4 (`RuntimeWarning: coroutine 'get_ml_context' was never awaited`; port 8000 occupied by Docker daemon on audit host; `routes/__init__.py` imports `drift` from a module it does not include `drift_status` from; `ml_context` deviation from three-DB spec not reflected in product-northwind §7)
- **LOW**: 3 (pyright version behind; viewer-pane §5 path `apps/web/app/api/state/route.ts` vs actual `apps/web/src/app/api/workspace/state/route.ts`; stock `.env.example` has no `METIS_ML_DB_URL`)

**Bottom line.** Shard 01 (backend core) shipped with a lifespan signature mismatch that makes `uvicorn` abort at startup, so the canonical opening move — "run `scripts/run_backend.sh` and confirm `/health` green" — returns a stack trace at minute zero. This is the single hardest failure: it kills pre-class preflight (T-30), the opening prompt's scaffold-verification (T+3), and every downstream endpoint demo. Fixing it is a 60-second diff in two files. Shards 06 (scripts) and 09 (scaffold support incl. CI) never landed — `scripts/preflight.py`, `scripts/grade_product.py`, `scripts/scenario_inject.py`, and `.github/workflows/*` are absent, meaning the instructor has no preflight, no public grader at 03:20, and no scenario-injection tool at 02:05 / 02:40. Without those, the lesson is still runnable as a "fully manual, COC-out every missing piece" session — but the contract-grading theatre and union-cap / drift-week-78 injections disappear.

---

## 2. Findings

Severity-ranked. Each finding has (a) evidence, (b) blast radius, (c) fix effort, (d) blocks lesson? yes/no.

### C1 — CRITICAL — Backend fails to start: `run_startup()` signature mismatch

**Evidence.**
`src/backend/app.py:39-40`:

```python
ctx = get_ml_context()
await run_startup(ctx)
```

`src/backend/startup.py:124`:

```python
async def run_startup() -> MLContext:
```

Uvicorn smoke run (port 8877, direct `uv run python -m src.backend.app`):

```
File "…/src/backend/app.py", line 40, in _lifespan
    await run_startup(ctx)
TypeError: run_startup() takes 0 positional arguments but 1 was given
RuntimeWarning: coroutine 'get_ml_context' was never awaited
ERROR: Application startup failed. Exiting.
```

Also pyright: `src/backend/app.py:40:23 - error: Expected 0 positional arguments (reportCallIssue)`.

**Blast radius.** Every minute-zero deliverable in `workshop-runofshow.md` §0/§1:

- T-30 preflight: `/health` is unreachable → red banner in Viewer for 100% of students.
- T+3 opening prompt: "Claude Code verifies every file…" — the verify step calls `/health`, gets connection-refused, cohort pivots before a single phase starts.
- Every downstream sprint: `/health`, `/forecast/*`, `/optimize/solve`, `/drift/check` all 503 because uvicorn exited.

**Fix effort.** 60 seconds. Edit `src/backend/app.py:39-40` to:

```python
ctx = await get_ml_context()
await run_startup()
```

(and drop the unused `ctx` local since `run_startup` rebuilds its own reference via the singleton). Alternatively — and safer, because it preserves the read of `ctx` — change `startup.py:124` to `async def run_startup(ctx: MLContext | None = None) -> MLContext:` and accept the already-built context. Both are one-liners.

**Blocks lesson? YES.** This is the hard blocker.

---

### C2 — CRITICAL — `scripts/preflight.py` does not exist

**Evidence.** `ls scripts/` returns only `run_backend.sh`. Scaffold-contract §6 requires: `preflight.py`, `grade_product.py`, `seed_experiments.py`, `seed_drift.py`, `seed_route_plan.py`, `journal_export.py`, `scenario_inject.py`, `instructor_brief.md` — 8 additional files.

**Blast radius.**

- T-30 preflight step (`workshop-runofshow.md §0`) is purely manual.
- T+03:20 PUBLIC GRADER RUN (`workshop-runofshow.md §6`) has no grader to run.
- T+02:05 union-cap injection and T+02:40 drift-week-78 injection have no CLI to fire from (`workshop-runofshow.md §4/§5`).
- `instructor_brief.md` (the minute-by-minute runbook for 00:15, 00:45, 03:20 announcements) does not exist.

**Fix effort.** Cannot be fixed cleanly in <1 hour. Repivot option: instructor announces by voice, the 03:20 grader is skipped or replaced by a visual inspection of each student's Viewer Pane, and the "fire scenario" moment is replaced by the instructor pasting the three-line chat snippet (from `scenario-injection.md`) into class chat manually.

**Blocks lesson? NO — repivot-able**, but every single instructor-side ceremony from `workshop-runofshow.md` loses its automation.

---

### C3 — CRITICAL — `tests/integration/` is empty: 0 of 12 wiring tests

**Evidence.** `ls tests/integration/` returns empty directory. `uv run pytest tests/integration/ --collect-only -q` → "no tests collected in 0.11s".

`specs/wiring-contracts.md` enumerates 11 required `test_<component>_wiring.py` files (+`test_ml_context_wiring.py` for shard 01). Shard 01 acceptance criteria explicitly require `test_ml_context_wiring.py` and `test_feature_store_wiring.py` to pass.

**Blast radius.** `orphan-detection.md` MUST Rule 2 and `facade-manager-detection.md` MUST Rule 2 are in violation for every single kailash-ml engine the scaffold exposes. Empirically, one of them (the `run_startup(ctx)` bug) would have been caught by `test_ml_context_wiring.py` on first run.

**Blocks lesson? NO** for students (they will not run these tests). **YES** for instructor trust in the scaffold — the wiring tests are the only mechanical defense against the 501-stub-never-wired-in-prod pattern that `orphan-detection.md` exists to prevent.

---

### C4 — CRITICAL — 5 required `[PRE-BUILT]` files missing from `src/backend/` and `specs/schemas/`

**Evidence.** Scaffold-contract §2 + §3 mandate:

| Missing file                                                         | Imported by                                                             | Evidence                                                                                             |
| -------------------------------------------------------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `src/backend/fs_preload.py`                                          | Shard-01 acceptance; `workshop-runofshow.md §0` F10 mitigation          | `ls src/backend/` shows only `{__init__,app,config,ml_context,startup}.py` + `routes/`               |
| `src/backend/drift_wiring.py`                                        | `routes/forecast.py` (commented call); `workshop-runofshow.md §5`       | same                                                                                                 |
| `src/backend/routes/drift_status.py`                                 | Viewer DriftPanel debug row; scaffold-contract §2                       | `ls src/backend/routes/` shows only `{__init__,forecast,optimize,drift,health}.py`                   |
| `specs/schemas/demand.py`                                            | `src/backend/startup.py:64` (`from specs.schemas.demand import schema`) | `ls specs/schemas/` shows only `routes.py`                                                           |
| `data/scenarios/union_cap.json` + `data/scenarios/week78_drift.json` | Sprint-2 + Sprint-3 injections                                          | `data/scenarios/` directory does not exist; `week78_drift.json` is at `data/`, not `data/scenarios/` |

**Blast radius.**

- `specs/schemas/demand.py` missing ⇒ `fs_preload` (conceptually) cannot register_features ⇒ `.preflight.json.feature_store_populated` stays `false` ⇒ `/health` returns `feature_store: false` for 100% of students. Currently masked because `fs_preload.py` itself does not exist (the feature-store preload logic is in-line in `startup.py` and swallows the `ImportError` as a WARN — see `startup.py:64-71`).
- `drift_wiring.py` missing ⇒ the Phase 13 mitigation in `workshop-runofshow.md §5` ("`drift_wiring.py` auto-wires `set_reference_data`") does not exist; students hit the exact failure mode the spec claims is auto-mitigated.
- `routes/drift_status.py` missing ⇒ Viewer DriftPanel debug row 404s; students cannot introspect drift reference state without reading `.preflight.json` directly.
- `data/scenarios/*` missing ⇒ instructor's `metis scenario fire union-cap` (itself also missing — C2) has no payload to inject.

**Fix effort.** 20-30 min to stub `fs_preload.py` and `drift_wiring.py` minimally and author `specs/schemas/demand.py` from the 9-feature list in `specs/canonical-values.md §6` + `data/README.md`. `routes/drift_status.py` is ~30 LOC against `ctx.drift_monitor.get_reference_status(...)`.

**Blocks lesson? PARTIAL.** `specs/schemas/demand.py` is the binding one because `startup.py` explicitly imports it at runtime (silently downgrades to WARN currently, but `/health.feature_store=false` is visible to every student). Without `fs_preload.py` and `drift_wiring.py`, Phases 4 and 13 can still run — students just don't get the mitigation the run-of-show promises.

---

### H1 — HIGH — Framework-first violation: raw FastAPI where Nexus is mandated

**Evidence.** `src/backend/app.py:19` `from fastapi import FastAPI`; `app.py:54` `app = FastAPI(…)`. Every docstring and status log says "Nexus backend" but no `kailash-nexus` import anywhere in `src/backend/`:

```
grep -n 'nexus\|Nexus' src/backend/*.py
# All hits are docstring/log strings, zero imports from kailash_nexus.
```

`rules/framework-first.md` § Work-Domain → Framework Binding: "HTTP API, REST, gateway, middleware, login, sessions, websockets → **Nexus**". Raw HTTP frameworks are explicitly listed as requiring `nexus-specialist` consultation before use.

**Blast radius.** Institutional — students watching the scaffold believe the workshop demonstrates Nexus idioms when it demonstrates raw FastAPI idioms; the wiring contracts for `Nexus.register_endpoints` in `wiring-contracts.md` cannot be tested because Nexus is not present.

**Fix effort.** Not fixable pre-lesson — re-architecting from FastAPI to `kailash-nexus` is a multi-session shard. Document as a known deviation in the instructor brief.

**Blocks lesson? NO.** Students will not notice on day one; the 501-stubs serve identically under FastAPI or Nexus.

---

### H2 — HIGH — `scripts/run_backend.sh` env-precedence bug

**Evidence.** `run_backend.sh:20-24`:

```bash
if [[ -f .env ]]; then
    set -o allexport; source .env; set +o allexport
elif [[ -f .env.example ]]; then
    echo "WARN: .env not found; using .env.example defaults…"
    set -o allexport; source .env.example; set +o allexport
fi
```

`.env.example` sets `KAILASH_NEXUS_PORT=8000`. The shell's `source` runs **after** any env vars the user exported, so `KAILASH_NEXUS_PORT=8877 bash scripts/run_backend.sh` is overwritten by the `.env.example` value. Observed:

```
$ KAILASH_NEXUS_PORT=8877 bash scripts/run_backend.sh
ERROR: port 8000 is already in use.
```

**Blast radius.** Audit machine had `com.docker.backend` listening on port 8000 → backend refused to start → diagnosis thought it was a conflict, not the lifespan bug. Students whose machines have anything on 8000 (Docker Desktop, Python dev servers, some VPN clients) will hit the same dead-end.

**Fix effort.** 1 minute. Change `source .env{,.example}` to preserve caller environment:

```bash
# shellcheck disable=SC2046
set -o allexport
source <(grep -v '^[[:space:]]*#' .env.example | grep -v '^[[:space:]]*$' | awk -F= '!a[$1]++')
set +o allexport
```

Or simpler: only default vars that are currently unset.

**Blocks lesson? YES for 1-5% of students** whose port 8000 is occupied. The `scripts/preflight.py` that was supposed to print the remediation one-liner does not exist (C2), so the student sees `ERROR: port 8000 is already in use` with no fix path.

---

### H3 — HIGH — `specs/schemas/routes.py` ships with `# TODO-STUDENT:` banner but manifest says `[PRE-BUILT]`

**Evidence.**

- `SCAFFOLD_MANIFEST.md` line 57: `specs/schemas/routes.py` → `[PRE-BUILT]`
- `specs/schemas/routes.py:4-7`:
  ```
  # TODO-STUDENT: this is a scaffold placeholder.
  # Your prompt to Claude Code must replace this file with the real
  # implementation described in SCAFFOLD_MANIFEST.md and PLAYBOOK.md.
  ```

The file body below the banner is in fact fully implemented with `Vehicle`, `DeliveryWindow`, `ConstraintSet`, `RoutePlan` dataclasses — the banner is wrong, not the content.

**Blast radius.** Opening prompt's scaffold-verification step ("Claude Code verifies every file in SCAFFOLD_MANIFEST.md exists at the stated path with the stated state") will flag this as a discrepancy. Students will then either (a) delete the working content or (b) commission Claude Code to "replace" a file that doesn't need replacement.

**Fix effort.** 10 seconds. Delete the banner comment block.

**Blocks lesson? NO — repivot-able** (instructor can paper over in their 00:08 transition).

---

### H4 — HIGH — `data/scenarios/` directory does not exist; scenario payloads not at canonical path

**Evidence.** `ls data/scenarios/` → `No such file or directory`. `data/week78_drift.json` exists at the top level instead of `data/scenarios/week78_drift.json`. No `union_cap.json` exists anywhere.

Scaffold-contract §4 mandates:

```
data/scenarios/union_cap.json          [PRE-BUILT]
data/scenarios/week78_drift.json       [PRE-BUILT]
```

**Blast radius.** Sprint 2 (02:05) union-cap injection has no payload. Sprint 3 (02:40) drift-week-78 injection has a payload, just at the wrong path, which a hypothetical `scripts/scenario_inject.py` would miss.

**Fix effort.** 5 minutes: `mkdir data/scenarios && mv data/week78_drift.json data/scenarios/` and author a minimal `union_cap.json` from `scenario-catalog.md` § `union-cap`.

**Blocks lesson? NO** because `scenario_inject.py` itself is missing (C2), so whether the payloads are at the right path is moot for the automated flow. Instructor's manual voice-broadcast of the union-cap scenario does not need the JSON file.

---

### H5 — HIGH — `.github/workflows/` directory missing entirely

**Evidence.** `find workspaces/metis/week-04-supply-chain -name .github -type d` → no result. Scaffold-contract §7 requires `preflight.yml` and `grade.yml`.

**Blast radius.** Nightly preflight that catches SDK-version drift (the one defense against "kailash-ml updated overnight and now AutoMLConfig takes different kwargs") does not run. Gold-standard submission grading against the rubric baseline does not run.

**Fix effort.** Not fixable pre-lesson.

**Blocks lesson? NO.**

---

### H6 — HIGH — Viewer state path drift: `apps/web/src/app/api/workspace/state/route.ts` vs spec `apps/web/app/api/state/route.ts`

**Evidence.** Actual path: `apps/web/src/app/api/workspace/state/route.ts`. Scaffold-contract §5 and SCAFFOLD_MANIFEST line 85 say `apps/web/app/api/state/route.ts`.

**Blast radius.** Opening prompt's scaffold verification will flag this, too. No runtime failure — the Viewer is internally consistent.

**Fix effort.** Update the spec in-place (1 minute) or rename the file (riskier, would break the Viewer).

**Blocks lesson? NO.**

---

### M1 — MEDIUM — `RuntimeWarning: coroutine 'get_ml_context' was never awaited`

**Evidence.** Same uvicorn trace as C1. `app.py:39` calls `get_ml_context()` (async) without `await`.

**Blast radius.** Root cause of C1. Once C1 is fixed, this warning disappears.

---

### M2 — MEDIUM — Docker daemon occupies port 8000 on audit host

**Evidence.** `lsof -iTCP:8000 -sTCP:LISTEN -Pn` → `com.docker.backend (PID 33533)`. Not a codebase issue — a host-environment issue on the audit machine that any student running Docker Desktop will replicate.

**Blast radius.** ~5% of students (Docker Desktop users) will fail to bind port 8000. Combined with H2 (override-blocking), they cannot just set `KAILASH_NEXUS_PORT=8001`.

**Fix effort.** Documented in instructor brief (if it existed — C2).

---

### M3 — MEDIUM — `routes/__init__.py` references `drift_status` in scaffold-contract but does not include it

**Evidence.** Scaffold-contract §2 says `routes/__init__.py` "Mounts `health` + `drift_status`". Actual code (`routes/__init__.py:15-24`) imports only `{drift, forecast, health, optimize}` and does not touch `drift_status`. `routes/drift_status.py` does not exist (C4).

**Blast radius.** Viewer DriftPanel debug row expects `/drift/status/<model_id>` → 404. Phase 13 debug path unavailable.

---

### M4 — MEDIUM — `ml_context` quietly collapses three SQLite URLs to one; not reflected in `product-northwind.md §7`

**Evidence.** `ml_context.py:12-16` docstring:

> The three separate DATABASE*URL*\* env vars from canonical-values.md §7 are retained as informational keys; the shard invariant ("one ConnectionManager instance") overrides, so at runtime we collapse to a single shared URL (`METIS_ML_DB_URL`, default `sqlite:///data/.ml.db`).

`.env.example` does not contain `METIS_ML_DB_URL`; it still lists the three legacy URLs. `canonical-values.md §7` still claims three separate sqlite files (`.experiments.db`, `.registry.db`, `.features.db`).

**Blast radius.** Documentation drift — students reading the spec think there are three DBs; operators `ls data/` and see one `.ml.db`. Not functional.

**Fix effort.** Either restore three DBs (15-30 min, requires three `ConnectionManager` + audit share-invariant test) or update `canonical-values.md §7` to document the collapse (2 min).

---

### L1 — LOW — pyright version behind (1.1.371 vs 1.1.408)

Cosmetic. Does not affect lesson.

---

### L2 — LOW — `.env.example` does not list `METIS_ML_DB_URL`

See M4. The key is read in `ml_context.py:240` but not documented.

---

### L3 — LOW — `.experiment_aliases.json` contains only `{}`

Expected; scaffold-contract calls this "stub only". Noting here so the grader doesn't flag it.

---

## 3. Smoke Test Results (exact output)

### 3.1 Backend imports

```
$ cd week-04-supply-chain && uv run python -c "from src.backend.app import app; print('ok')"
ok
```

PASS — module imports; lifespan has not yet fired.

### 3.2 Pyright scan of `src/backend/`

```
src/backend/app.py
  src/backend/app.py:40:23 - error: Expected 0 positional arguments (reportCallIssue)
1 error, 0 warnings, 0 informations
```

FAIL — one error, the same one that causes C1.

### 3.3 Pytest collection `tests/integration/`

```
no tests collected in 0.11s
```

FAIL — 0 of 12 wiring tests.

### 3.4 Data fixtures load

```
demand rows: 2193
leaderboard runs: 30
```

PASS — CSV and leaderboard JSON parse and have the expected row/run counts.

### 3.5 Uvicorn startup (equivalent of `scripts/run_backend.sh`)

```
$ KAILASH_NEXUS_PORT=8877 uv run python -m src.backend.app
INFO:     Started server process [79617]
INFO:     Waiting for application startup.
2026-04-16 17:47:25,251 INFO metis.app metis.app.starting
ERROR:    Traceback (most recent call last):
  File "…/starlette/routing.py", line 694, in lifespan
  …
  File "…/src/backend/app.py", line 40, in _lifespan
    await run_startup(ctx)
TypeError: run_startup() takes 0 positional arguments but 1 was given
/…/uvicorn/lifespan/on.py:91: RuntimeWarning: coroutine 'get_ml_context' was never awaited
ERROR:    Application startup failed. Exiting.
```

**HARD FAIL** — backend does not start.

### 3.6 TestClient `/health` probe (no lifespan)

```
status: 200
body: {'ok': True, 'db': True, 'feature_store': False, 'drift_wiring': False, 'registry_runs': 0, 'nexus_port': 8000}
```

PASS on shape. FAIL on substance — `feature_store: false`, `drift_wiring: false` because fs_preload.py and drift_wiring.py do not exist.

### 3.7 `scripts/run_backend.sh` (as shipped)

```
$ KAILASH_NEXUS_PORT=8877 bash scripts/run_backend.sh
WARN: .env not found; using .env.example defaults. Copy .env.example to .env to customize.
ERROR: port 8000 is already in use. Kill the existing process or set KAILASH_NEXUS_PORT.
```

FAIL — H2 overwrites user-supplied `KAILASH_NEXUS_PORT`.

### 3.8 Viewer TypeScript + build

```
$ cd apps/web && npx tsc --noEmit
(no output — zero errors)
$ npm run build
Route (app)                              Size     First Load JS
┌ ○ /                                    12.4 kB         105 kB
├ ○ /_not-found                          875 B            88 kB
└ ƒ /api/workspace/state                 0 B                0 B
```

PASS — viewer is clean end-to-end.

### 3.9 `uv run pyright apps/web`

```
0 errors, 0 warnings, 0 informations
```

PASS.

---

## 4. MUST-FIX-NOW vs REPIVOT-IN-CLASS

### MUST-FIX-NOW (blocks lesson start, ~15 minutes total)

1. **C1 — backend lifespan signature.** Edit `src/backend/app.py:39-40` to `ctx = await get_ml_context(); await run_startup()`. Verify: `KAILASH_NEXUS_PORT=8877 uv run python -m src.backend.app` → `metis.app.ready` log line + 200 from `/health`. **(~60 seconds.)**
2. **C4a — `specs/schemas/demand.py`.** Author a minimal `FeatureSchema(name="user_demand", features=[…9…], target="orders_next_day")` from the column list in `data/README.md §Columns` and `canonical-values.md §6`. **(~10 minutes.)**
3. **H2 — `run_backend.sh` env precedence.** Change the `source .env*` block to only set values that are not already in the environment (one-line awk as above). **(~60 seconds.)**
4. **H3 — delete the TODO banner from `specs/schemas/routes.py`**. It's a full implementation; the banner is wrong. **(~15 seconds.)**

### REPIVOT-IN-CLASS (students/instructor work around live)

- **C2 — missing scripts.** Instructor announces scenarios by voice at 02:05 and 02:40 using the three-line chat snippet from `scenario-catalog.md`. Instructor runs contract-grading by reading each student's Viewer Pane at 03:20 and scoring by rubric manually instead of running `grade_product.py`. Preflight is replaced by each student running: `curl -sf http://localhost:8000/health` and eyeballing the JSON.
- **C3 — missing wiring tests.** Students are not asked to run these; they would have caught C1 if they existed, but the C1 fix makes them unnecessary for day-one. Codify them in a post-workshop session.
- **C4b/c — missing `fs_preload.py` / `drift_wiring.py` / `routes/drift_status.py`.** `/health` will report `feature_store: false` and `drift_wiring: false` — instructor announces "ignore those two fields; the workshop teaches the pattern, not the preload plumbing" at 00:08 transition.
- **H1 — raw FastAPI vs Nexus.** Acknowledge in the 00:00 welcome: "the scaffold uses raw FastAPI for the Week 4 pilot; Week 5 migrates to kailash-nexus."
- **H4 — missing `data/scenarios/union_cap.json`.** Union-cap injection at 02:05 is announced via voice; no JSON payload needed for the verbal path.
- **H5 — missing `.github/workflows/`.** Not visible to students.
- **H6 — viewer path drift.** Update `SCAFFOLD_MANIFEST.md` line 85 and `scaffold-contract.md §5` to the actual path as a 1-line doc fix when instructor has a minute.
- **M2 — port 8000 occupied.** Instructor brief: any student who sees `ERROR: port ... is already in use` sets `export KAILASH_NEXUS_PORT=8001` (works once H2 is fixed).

---

## 5. Shortest fix path (~15 min sequential, MUST-FIX only)

1. `src/backend/app.py` — change line 39-40 from
   ```python
   ctx = get_ml_context()
   await run_startup(ctx)
   ```
   to
   ```python
   await get_ml_context()
   await run_startup()
   ```
   (C1 + M1; ~60s)
2. `specs/schemas/routes.py` — delete lines 4-7 (the `TODO-STUDENT` banner block). (H3; ~15s)
3. `specs/schemas/demand.py` — new file, ~30-40 LOC:

   ```python
   # Copyright (c) 2026 Terrene Foundation (Singapore CLG)
   # Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
   from kailash_ml.engines.feature_store import FeatureSchema, FeatureField, FieldType

   schema = FeatureSchema(
       name="user_demand",
       entity_id="depot_id",
       timestamp="date",
       target="orders_next_day",
       features=[
           FeatureField("orders_last_day", FieldType.FLOAT),
           FeatureField("orders_7d_rolling_avg", FieldType.FLOAT),
           FeatureField("orders_28d_rolling_avg", FieldType.FLOAT),
           FeatureField("day_of_week", FieldType.INT),
           FeatureField("is_holiday", FieldType.BOOL),
           FeatureField("active_customers", FieldType.INT),
           FeatureField("customer_mix_hash", FieldType.FLOAT),
           FeatureField("avg_order_value", FieldType.FLOAT),
           FeatureField("is_peak_season", FieldType.BOOL),
       ],
   )
   ```

   (verify the exact `FeatureField` / `FieldType` names against the installed `kailash_ml` — may need `FeatureColumn` instead.) (C4a; ~10 min)

4. `scripts/run_backend.sh` — replace the `source .env / .env.example` block with:
   ```bash
   env_file=""
   [[ -f .env ]] && env_file=.env
   [[ -z "$env_file" && -f .env.example ]] && env_file=.env.example && \
       echo "WARN: .env not found; using .env.example defaults." >&2
   if [[ -n "$env_file" ]]; then
       while IFS='=' read -r k v; do
           [[ -z "$k" || "$k" == \#* ]] && continue
           [[ -z "${!k:-}" ]] && export "$k=$v"
       done < "$env_file"
   fi
   ```
   (H2; ~60s)
5. Verify end-to-end:
   ```bash
   KAILASH_NEXUS_PORT=8877 bash scripts/run_backend.sh &
   sleep 5
   curl -sf http://127.0.0.1:8877/health | python -m json.tool
   kill %1
   ```
   Expected: `ok: true, db: true, feature_store: true, drift_wiring: false` (drift_wiring stays false because `drift_wiring.py` still does not exist — that's a REPIVOT, not a MUST-FIX).

---

## 6. Notes for instructor brief (if C2 is repivoted)

- Put up `START_HERE.md` §9 and say out loud: "The opening prompt will flag `specs/schemas/routes.py` as a banner-vs-state mismatch. That's a scaffold bug from the red team; paste this one-line fix in Claude Code and move on: `delete the TODO-STUDENT block at the top of specs/schemas/routes.py`." (Or apply the 15-sec H3 fix above and the opening prompt runs clean.)
- At 02:05 (union-cap) and 02:40 (drift-week-78), the instructor dictates the chat snippets from `scenario-catalog.md` directly into class chat. No CLI tool fires; students paste the snippet into Claude Code manually.
- At 03:20, the instructor runs an eyeball-the-Viewer pass against each student's cockpit instead of `grade_product.py`, and reads the rubric anchors from `rubric-grader.md` aloud. Scoring is verbal; no JSON produced. Session notes capture the scores for the post-workshop audit.
