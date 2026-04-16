---
shard_id: 05b
slug: viewer-panels
title: >
  Build the 5 panel components (Leaderboard, ForecastPanel, RoutePanel,
  DriftPanel, JournalPanel) plus PreflightBanner, each rendering from sample
  fixture JSON, and the 3 render-contract tests guarding severity enum,
  preflight field naming, and leaderboard empty/populated toggle.
loc_estimate: 220
invariants:
  - severity-3-values: DriftPanel reads overall_severity; accepts exactly {"none","moderate","severe"}; "low" never appears; colours per viewer-pane.md §3.5
  - preflight-booleans: PreflightBanner parses each .preflight.json field as bool; "true" string and true literal both accepted; shows field name on failure, not a generic error
  - read-only-panels: zero forms, zero state-mutating buttons in any panel; scenario toggle and depot tab are pure React state with no workspace writes
  - empty-state-per-panel: every panel renders its defined empty-state string when its data file is absent from the watcher state; never throws or shows a blank screen
  - failure-modes-implemented: viewer-pane.md §6 failure modes implemented — malformed JSON shows "unable to parse <file>"; watcher lost shows "backend watcher offline; restart next dev"; stale poll >5s shows "last update N seconds ago"
call_graph_hops: 3
depends_on: [05a]
blocks: []
can_build_against: sample fixtures from apps/web/__tests__/fixtures/ (produced by 05a)
specs_consulted:
  - specs/viewer-pane.md §3.2 (Leaderboard: side-by-side, family/MAPE/RMSE/fold_variance/training_time/run_id, delta-MAPE badge)
  - specs/viewer-pane.md §3.3 (ForecastPanel: Recharts line chart, three depot overlays, per-depot tabs D01/D02/D03)
  - specs/viewer-pane.md §3.4 (RoutePanel: scenario toggle pre-union/post-union/current, 2D dot-chart, KPI strip, comparing banner)
  - specs/viewer-pane.md §3.5 (DriftPanel: severity badge, per-feature test table name in {ks,psi}, historical variance chart, debug row GET /drift/status)
  - specs/viewer-pane.md §3.6 (JournalPanel: react-markdown, rubric-dimension headings highlighted, filter by phase)
  - specs/viewer-pane.md §3.7 (PreflightBanner: 8 typed bool fields, green/red strip, field name on failure)
  - specs/viewer-pane.md §6 (failure modes: malformed JSON, watcher lost, stale poll)
  - specs/viewer-pane.md §7 (accessibility: keyboard nav, colour-blind safe)
  - specs/canonical-values.md §1 (severity enum — exactly 3 values)
  - specs/data-fixtures.md §3.2 (leaderboard_prebaked.json schema: run_id, family, params_hash, metrics, training_duration_s, tracker_run_id, best_by_family)
acceptance_criteria:
  - apps/web/app/components/Leaderboard.tsx reads leaderboard.json (left) and leaderboard_prebaked.json (right) side-by-side; columns family/MAPE/RMSE/fold_variance/training_time/run_id per viewer-pane.md §3.2; delta-MAPE badge above live column; empty-state "awaiting /forecast/train" when leaderboard.json absent
  - apps/web/app/components/ForecastPanel.tsx reads forecast_output.json; Recharts line chart with three depot overlays (solid/shaded/dotted); per-depot tab D01/D02/D03; empty-state "awaiting /forecast/predict"
  - apps/web/app/components/RoutePanel.tsx reads route_plan.json (default); scenario toggle pre-union/post-union/current; 2D dot-chart + constraint violation list + KPI strip per viewer-pane.md §3.4; comparing banner when toggle is not current
  - apps/web/app/components/DriftPanel.tsx reads drift_report.json + drift_baseline.json; severity badge from overall_severity in {"none","moderate","severe"}; per-feature test table with name in {"ks","psi"} only; historical variance chart; recommendations list; debug row showing GET /drift/status/<model_id> result per viewer-pane.md §3.5
  - apps/web/app/components/JournalPanel.tsx reads journal/*.md via watcher state; react-markdown rendering; rubric-dimension headings highlighted; filter by phase; empty-state "awaiting metis journal add"
  - apps/web/app/components/PreflightBanner.tsx reads .preflight.json; parses all 8 bool fields (db, feature_store, drift_wiring, ok, xgb_available, explain_available, ortools_available, pulp_available); green strip if all true; red strip naming the specific failing field per viewer-pane.md §3.7
  - Failure modes from viewer-pane.md §6 implemented in all panels: malformed JSON shows "unable to parse <file>" with filename; watcher state stale >5s shows yellow strip "last update N seconds ago"; watcher offline shows red strip "backend watcher offline; restart next dev"
  - No authentication — localhost-only contract from viewer-pane.md §4
  - apps/web/__tests__/DriftPanel.test.tsx passes severity enum guard: renders "none"/"moderate"/"severe" without error; throws/renders error state on "low" or unknown values
  - apps/web/__tests__/PreflightBanner.test.tsx passes per-field false detection: each of the 8 fields set to false independently produces that field's name in the red strip
  - apps/web/__tests__/Leaderboard.test.tsx passes empty-state and delta badge: empty-state renders when leaderboard.json absent from fixture; delta badge present and non-zero when both fixture files present
wiring_tests:
  - apps/web/__tests__/DriftPanel.test.tsx (severity enum guard — renders known values; errors on "low")
  - apps/web/__tests__/PreflightBanner.test.tsx (each false bool field named in red strip)
  - apps/web/__tests__/Leaderboard.test.tsx (empty-state + delta badge checks)
---

# Shard 05b — Viewer Panels

## What

Build all 5 panel components and PreflightBanner, each reading from the watcher state cache delivered by the shell (shard 05a), plus the 3 render-contract tests that guard the highest-risk panel invariants. Every panel has a defined empty-state and renders correctly from the fixture JSON in apps/web/**tests**/fixtures/.

## Why

The Viewer is the student's live dashboard and the instructor's projector view during the 210-minute workshop. DriftPanel's severity-enum guard prevents a "low" severity value from rendering silently (students would see wrong colours and misunderstand the drift state). PreflightBanner's per-field reporting is the only structural feedback mechanism when a workshop machine has a missing dependency — generic "something failed" is not actionable in a 3-minute troubleshooting window.

## Implementation sketch

- Each panel component reads its slice from the shared React Query cache (`useQuery({ queryKey: ['state'] })`) populated by the watcher route from shard 05a; no direct file reads, no fetch to Nexus
- `DriftPanel.tsx` — severity badge uses a const map `{ none: "green", moderate: "amber", severe: "red" }`; unknown values render an error state with the raw value shown; debug row calls GET /drift/status/<model_id> via the watcher's backend proxy path (still no direct Nexus call)
- `PreflightBanner.tsx` — iterates the 8 known field names in order; coerces string "true"/"false" to bool; collects failing fields into an array; renders the array as `field1, field2 not ready`
- `RoutePanel.tsx` — scenario toggle is pure React state (`useState("current")`); reads the correct snapshot file path based on toggle value from watcher state dict
- `Leaderboard.tsx` — delta-MAPE = `Math.abs(live.mape - prebaked_best.mape)`; badge rendered when both files present; empty-state when live file absent
- All failure modes implemented via a shared `<DataState>` wrapper component that handles loading/error/empty uniformly

## Out of scope

- Shell, watcher, routing, React Query setup (shard 05a)
- Editing journal entries (read-only by contract)
- Mobile viewport
- Authentication

## Acceptance

- [ ] apps/web/app/components/Leaderboard.tsx renders side-by-side with delta-MAPE badge; empty-state when leaderboard.json absent
- [ ] apps/web/app/components/ForecastPanel.tsx renders Recharts line chart with depot tabs; empty-state when forecast_output.json absent
- [ ] apps/web/app/components/RoutePanel.tsx renders scenario toggle + dot-chart + KPI strip; comparing banner on non-current toggle
- [ ] apps/web/app/components/DriftPanel.tsx renders severity badge from overall_severity in {none,moderate,severe}; per-feature table name in {ks,psi} only; debug row
- [ ] apps/web/app/components/JournalPanel.tsx renders react-markdown; rubric headings highlighted; phase filter; empty-state
- [ ] apps/web/app/components/PreflightBanner.tsx parses all 8 bool fields; green strip if all true; red strip names specific failing field
- [ ] Failure modes from viewer-pane.md §6 implemented across all panels
- [ ] apps/web/**tests**/DriftPanel.test.tsx passes severity enum guard
- [ ] apps/web/**tests**/PreflightBanner.test.tsx passes per-field false detection for all 8 fields
- [ ] apps/web/**tests**/Leaderboard.test.tsx passes empty-state and delta badge checks
