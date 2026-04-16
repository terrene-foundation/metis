# Viewer Pane — Read-Only Dashboard

This spec is the authority on the Next.js Viewer Pane shipped as `apps/web/` in the scaffold. It is entirely `[PRE-BUILT]` — students do not edit it. The Viewer is the student's evaluation instrument AND the dashboard the fictional Ops Manager would use; those two roles are deliberate (covered in `product-northwind.md` §3).

The Viewer is **read-only by course contract**. There are no buttons, no form submissions, no control surfaces. It watches files on disk and renders state. Any proposed "add a button" extension violates the course contract.

## 1. Architecture

- **Framework**: Next.js 14 (App Router), React 18, TypeScript 5.
- **Styling**: Tailwind CSS. No custom CSS files; components use Tailwind utility classes.
- **Charts**: Recharts (line, bar, area). No D3 — keeps the dependency tree compact.
- **Data fetching**: React Query (`@tanstack/react-query`) — polls the server-side filesystem watcher endpoint at 1 s intervals.
- **Server runtime**: the Next.js server process runs a filesystem watcher (`chokidar`) over the `data/` directory. It does NOT make cross-origin HTTP calls to Nexus — eliminates F5 (CORS).

### 1.1 Data flow

```
Nexus writes data/*.json  ──┐
                            ├──▶  chokidar FS watcher  ──▶  in-memory state cache
Student writes journal/*.md ┘                                        │
                                                                     ▼
                                                   GET /api/workspace/state
                                                                     │
                                                                     ▼
                                                     React Query (1 s poll)
                                                                     │
                                                                     ▼
                                                        5 panels re-render
```

### 1.2 Ports + paths

- Viewer: `http://localhost:3000` (configurable via `NEXT_PUBLIC_BACKEND_PORT` for the displayed Nexus URL; the Viewer process itself binds whatever port `next dev` uses).
- Watch root: resolved through `process.env.METIS_WORKSPACE_ROOT` if set, otherwise via `path.resolve(__dirname, '../../data')` from the Next app directory. The resolution is tested in `scripts/preflight.py` so `next dev` from a non-canonical cwd fails loudly rather than silently watching the wrong directory.
- Internal API: `GET /api/workspace/state` — server-side only.

## 2. Polling contract

- **Interval**: 1 second (configurable via `NEXT_PUBLIC_POLL_MS=1000`).
- **Latency target**: ≤ 1 s end-to-end from "Nexus writes `data/leaderboard.json`" to "Leaderboard panel renders it".
- **Backpressure**: if the watcher's state cache hasn't changed since the last poll, the endpoint returns `304 Not Modified` + the client skips the re-render.
- **Failure mode**: if the Nexus process is down, the Viewer keeps rendering the last known state with a red strip saying "backend unreachable — last update N seconds ago". This is deliberate — students can still read and evaluate their most recent output even while troubleshooting the backend.

### 2.1 Why filesystem-watch, not HTTP

Risk-assessment Scenario 2 / failure-point F5 flagged CORS as a dominant time-sink with ~50% incidence. Filesystem-watch avoids cross-origin calls entirely. The Viewer process reads the same filesystem the Nexus process writes; there is no network in the loop.

## 3. Panels (5)

The top-level `apps/web/app/page.tsx` renders exactly five panels in a fixed grid. No student prompt adds, removes, or reorders panels.

### 3.1 Playbook Progress panel

- **Component**: not a single `*.tsx` file — implemented as a header strip at the top of `page.tsx` plus a progress ribbon inside each sprint section.
- **Data source**: `journal/*.md` filenames (one per phase). The watcher counts which `phase_N_*.md` files exist.
- **Render**: 12 phase chips in sprint order: **Sprint 1** `[1, 2, 4, 5, 6, 7, 8]`, **Sprint 2** `[10, 11, 12]`, **Sprint 3** `[13]`, **Close** `[9]`. Each chip is green if the corresponding journal entry exists, grey otherwise. Re-runs are sub-chips within the parent phase: Phase 5/6 post-drift, Phase 8 post-union (`journal/phase_8_postunion.md`), Phase 11 post-union, Phase 12 post-union.
- **Update latency**: ≤ 1 s.

### 3.2 Leaderboard panel — `Leaderboard.tsx`

- **Data source**: reads BOTH `data/leaderboard.json` (student's live run) AND `data/leaderboard_prebaked.json` (pre-baked 30-trial).
- **Render**: two-column view, side-by-side. Columns: family, MAPE, RMSE, fold variance, training time, `ExperimentTracker` run ID.
- **Student's run** on the left, **pre-baked** on the right. A "Δ MAPE vs pre-bake best" badge is shown above the live-run column.
- **Interactive sort**: click a column header sorts within that column only. No side effects on the workspace — sort is pure view state.
- **Empty-state**: if `data/leaderboard.json` is missing (student hasn't run AutoML yet) the left column shows "awaiting `/forecast/train`."

### 3.3 Forecast Panel — `ForecastPanel.tsx`

- **Data source**: `data/forecast_output.json`. Rendered only when the file exists.
- **Render**: Recharts line chart with three overlays per depot — point forecast (solid line), 80% prediction interval (shaded band), actual value from holdout (dotted line when present).
- **Per-depot tab**: click D01 / D02 / D03 to switch depot.
- **Empty-state**: "awaiting `/forecast/predict`."

### 3.4 Route Panel — `RoutePanel.tsx`

- **Data source**: `data/route_plan.json` (default). Scenario toggle switches between `data/route_plan_preunion.json` and `data/route_plan_postunion.json` when both exist.
- **Render**:
  - **Route map**: a 2D dot-chart plotting customer locations (latitude/longitude normalised to depot-relative coordinates); lines connecting deliveries in route order; colour-coded by driver.
  - **Constraint violation list**: time-window violations highlighted in red.
  - **KPI strip**: total distance, total overtime hours, SLA violations, total cost from the solver's objective.
- **Scenario toggle**: segmented control with three states — `pre-union` / `post-union` / `current`. Default is `current` → reads `route_plan.json`. When the scenario toggle is set to `pre-union` / `post-union`, a "comparing" banner appears with the delta on distance / SLA / overtime.
- **Empty-state**: "awaiting `/optimize/solve`."

### 3.5 Drift Panel — `DriftPanel.tsx`

- **Data source**: `data/drift_report.json` + `data/drift_baseline.json`.
- **Render**:
  - **Severity badge**: reads `overall_severity` (the library's JSON field name; NOT `severity`). One of `"none"` / `"moderate"` / `"severe"` (3-value enum — kailash-ml never emits `"low"`). Colour-coded green / orange / red. Icons `✓` / `⚠` / `✕` for colour-blind safety.
  - **Per-feature test table**: feature, test name (`ks` / `psi` — the two tests kailash-ml emits; no `chi2`, no `js`), statistic, p-value (KS only; PSI has no p-value), alert bool.
  - **Historical variance chart**: line chart of rolling 7-day MAPE across the training window with the post-drift window shaded.
  - **Recommendations bullet list**: the `recommendations` array from the response verbatim.
  - **Debug row**: small status pill reading `GET /drift/status/<model_id>` — shows `reference_set: true/false` + `reference_set_at` so Phase 13 students can confirm `drift_wiring.wire` fired without terminal spelunking.
- **Empty-state**: "awaiting `/drift/check`."

### 3.6 Journal Panel — `JournalPanel.tsx`

- **Data source**: `journal/*.md` — rendered through `react-markdown` with the rubric-dimension headings highlighted.
- **Render**: vertical scroll of every entry in phase order. Each entry has a rubric-dimension score preview (if the grader has scored it) shown as five dots (0 / 2 / 4) colour-coded.
- **Filter**: top-of-panel dropdown to filter by phase.
- **Empty-state**: "awaiting `metis journal add` — template at `journal/_template.md`."

### 3.7 Preflight banner — `PreflightBanner.tsx`

Not a full panel — a 24 px strip at the top of the viewport. Reads `.preflight.json`. Parses each status field as a boolean (`db`, `feature_store`, `drift_wiring`, `ok`, `xgb_available`, `explain_available`, `ortools_available`, `pulp_available`); green if all are `true`, red with the specific failing-check name (e.g. `"drift_wiring not active — restart Nexus"`) if any are `false`. Also reads `GET :8000/health` (same boolean schema) for live status. Visible throughout the workshop.

## 4. UX invariants (MUST NOT violate)

- **Read-only**: no forms, no buttons that mutate workspace state. The segmented controls (scenario toggle, per-depot tab, panel filter) are pure view state.
- **No authentication**: the workshop is localhost-only. `app.py` binds only to `127.0.0.1`.
- **No telemetry**: the Viewer does not emit any outbound HTTP. Everything is local-loopback filesystem.
- **No blocking spinners**: panels render the last-known state immediately on load. Stale-indicator strip replaces spinners.
- **Deterministic rendering**: same input files → same pixels. No animated easing that hides state transitions; students need to perceive updates as they happen.
- **No AI-driven UI**: the panels do not run any LLM calls. All reasoning is in the terminal (Claude Code) or in the student's head.
- **Plain language labels**: no "MAPE" without a tooltip; no "PSI" without a tooltip. Tooltips are one sentence, per `communication.md`.

## 5. Component ownership and imports

| Panel             | Component path                                | Consumes files                                                                            |
| ----------------- | --------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Playbook Progress | `apps/web/app/page.tsx` (inline)              | `journal/phase_*.md` (filenames only)                                                     |
| Leaderboard       | `apps/web/app/components/Leaderboard.tsx`     | `data/leaderboard.json`, `data/leaderboard_prebaked.json`                                 |
| Forecast          | `apps/web/app/components/ForecastPanel.tsx`   | `data/forecast_output.json`                                                               |
| Route             | `apps/web/app/components/RoutePanel.tsx`      | `data/route_plan.json`, `data/route_plan_preunion.json`, `data/route_plan_postunion.json` |
| Drift             | `apps/web/app/components/DriftPanel.tsx`      | `data/drift_report.json`, `data/drift_baseline.json`                                      |
| Journal           | `apps/web/app/components/JournalPanel.tsx`    | `journal/*.md`, `grade_report.json` (if present)                                          |
| Preflight banner  | `apps/web/app/components/PreflightBanner.tsx` | `.preflight.json`                                                                         |
| FS watcher / API  | `apps/web/app/api/state/route.ts`             | (scans `data/` + `journal/` + `.preflight.json`)                                          |

No panel reads from any other panel's file. No panel writes. No cross-panel state sharing beyond the common React Query cache of `/api/workspace/state`.

## 6. Failure modes

| Failure                                                         | Behaviour                                                                                                                                                                                 |
| --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data/leaderboard.json` malformed JSON                          | Panel shows "unable to parse leaderboard.json — check the file for syntax errors"                                                                                                         |
| `data/route_plan.json` missing when scenario toggle = `current` | Panel shows "awaiting /optimize/solve"                                                                                                                                                    |
| FS watcher lost (process died)                                  | Red strip "backend watcher offline; restart `next dev`"                                                                                                                                   |
| Stale poll (> 5 s since last successful poll of the watcher)    | Yellow strip "last update N seconds ago" (NOT "since last file change" — the watcher's state cache is considered fresh as long as the poll is reaching it, even when no file has changed) |
| Journal markdown too long (> 10 KB per entry)                   | Panel truncates with "… expand" affordance (pure view state)                                                                                                                              |

## 7. Accessibility

- Keyboard-only navigation: scenario toggle + panel filters respond to arrow keys and Enter.
- Tailwind's default focus rings enabled; no `outline: none`.
- Colour-blind-safe palette for severity (green / yellow / orange / red → also icons `✓` / `⚠` / `⚠!` / `✕`).
- Tooltip text passes to screen readers via `aria-describedby`.

## Open questions

- **Mobile viewport** — the Viewer is designed for a laptop screen split with the terminal. Mobile rendering is not a goal and not tested. Flag for future weeks if a demo ever runs on a projector-only setup.
- **Grade-report rendering timing** — `grade_report.json` is written by `scripts/grade_product.py` at 03:20. The Viewer's Journal Panel can read it, but approach.md doesn't specify whether the rubric dots are shown live-as-the-grader-runs or only once the grader completes. Conservative default: only after the grader exits.
