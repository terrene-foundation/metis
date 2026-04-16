# Scenario Injection — Instructor CLI

This spec is the authority on the `metis scenario fire <event>` CLI used by the instructor to inject live scenario events during the workshop. The CLI is implemented by `scripts/scenario_inject.py` (scaffold, `[PRE-BUILT]`, instructor-only — not installed on student machines).

The injection CLI is how the workshop tests whether students can re-classify constraints and re-reason over drifted data under time pressure. Each event mutates a specific file in the student workspace and triggers a specific endpoint re-run; the Viewer Pane reflects the change within the filesystem-watch polling window (≤ 1 s per `viewer-pane.md`).

## 1. CLI contract

```
metis scenario fire <event_name> [--target <workspace_path>] [--dry-run]
```

- `<event_name>` ∈ `{union-cap, drift-week-78, casemix-tariff-cut}`.
  - `casemix-tariff-cut` is the SG-localised reimbursement-shock scenario (equivalent of Week 7's US Medicare-cut rehearsal; Casemix tariffs / MediShield Life are the Singapore policy analog). Week 4 fires only the `--dry-run` path; the actual mutation is deferred to Week 7's healthcare workshop. The event was renamed from the US-centric `medicare-cut` during red-team because firing US-healthcare language into an SG MBA cohort is a communication failure (see `communication.md`).
- `--target` defaults to `./workspaces/metis/week-04-supply-chain/` — the instructor's copy that mirrors every student machine via a shared network folder OR a per-machine copy with the same relative paths. Classroom topology is "each student runs their own workspace; instructor fires on the shared screen and students mirror the command locally."
- `--dry-run` prints the mutation plan without writing. The `casemix-tariff-cut` event is `--dry-run`-only in Week 4.

### 1.1 Exit codes

| Code | Meaning                                                                                                                    |
| ---- | -------------------------------------------------------------------------------------------------------------------------- |
| `0`  | Fired successfully (or `--dry-run` plan printed).                                                                          |
| `1`  | Unknown event.                                                                                                             |
| `2`  | Target workspace not detected (missing `SCAFFOLD_MANIFEST.md`).                                                            |
| `3`  | Pre-condition not met (e.g. firing `union-cap` before the first `/optimize/solve` run — no `route_plan.json` to snapshot). |
| `4`  | Already fired (idempotency guard — see §1.3).                                                                              |
| `5`  | Rollback target missing (e.g. `--undo union-cap` without a `route_plan_preunion.json` on disk AND no recoverable seed).    |

### 1.2 Idempotency

Each event writes a marker file at `data/scenarios/active_<event>.json` on first fire. If the marker already exists, the CLI exits with code 4 and prints `"already fired at <fired_at>; pass --re-fire to replay"`. The `--re-fire` flag re-runs the snapshot + mutate + log sequence (useful if the student's workspace drifted after the first fire).

### 1.3 Logging

Every fire writes `data/.scenario_log.jsonl` with `{"event": "...", "fired_at": "...", "files_mutated": [...], "endpoint_to_rerun": "..."}`. The Viewer Pane reads this log and surfaces a toast notification.

## 2. Event catalog

### 2.1 `union-cap`

- **When fired**: Sprint 2, ~02:05 (minute 30 of the 60-minute Sprint 2 block).
- **Trigger prerequisite**: student has run `/optimize/solve` at least once; `data/route_plan.json` exists.
- **What it does**:
  1. **Snapshot** — copies `data/route_plan.json` → `data/route_plan_preunion.json`. This is the before-baseline. If the student has already named their first plan `route_plan_preunion.json` directly, the snapshot is a no-op.
  2. **Mutate** — writes `data/scenarios/active_union_cap.json` = `{"constraint": "driver_overtime_hours_max", "new_cap": 5, "unit": "hours_per_week", "classification_hint": "hard", "reason": "driver union collective bargaining agreement"}`. The scenario payload itself already exists as `data/scenarios/union_cap.json` (pre-built fixture); `active_union_cap.json` is the "this one is firing now" marker.
  3. **Log** to `.scenario_log.jsonl`.
- **Endpoint to re-trigger**: `POST /optimize/solve` with `scenario_tag: "postunion"` and the updated constraint set (driver overtime hours now hard, cap = 5). The student writes the result to `data/route_plan_postunion.json` (NOT overwriting `route_plan.json`, per F6 state-hygiene).
- **Phases to re-run**: 11 (constraint classification — re-classify overtime from soft to hard), 12 (solver acceptance — new plan), 8 (deployment gate — sign off on the new plan).
- **Viewer Pane effect**: `RoutePanel.tsx` swaps the default view to show `_postunion` after the scenario toggle is used; the `_preunion` view remains selectable for before/after comparison.
- **Journal expectation**: student writes `journal/phase_11_postunion.md` naming the constraint that changed from soft to hard AND `journal/phase_12_postunion.md` naming what changed in the plan.
- **Common mis-fires** (instructor guidance):
  - Student overwrites `route_plan.json` instead of writing `route_plan_postunion.json` → before/after comparison is lost. Instructor's three-line chat snippet tells Claude Code to save as `_postunion`.
  - Student leaves overtime as soft and only raises its penalty → technically feasible but misses the learning outcome. The rubric's D4 scores 1/4.
- **Rollback**: `metis scenario fire union-cap --undo` deletes `data/scenarios/active_union_cap.json` and restores `route_plan.json` from `route_plan_preunion.json`. If `route_plan_preunion.json` is ALSO missing, the CLI falls back to `scripts/seed_route_plan.py` (pre-built; writes a baseline plan from the pre-baked leaderboard). If both paths fail, the CLI exits with code 5 and prints `"--undo union-cap: rollback sources missing. Run scripts/seed_route_plan.py manually or re-run /optimize/solve."` Used only if the injection corrupted the workspace beyond recovery.

### 2.2 `drift-week-78`

- **When fired**: Sprint 3, ~02:40 (minute 5 of the 40-minute Sprint 3 block).
- **Trigger prerequisite**: student has a trained model in `ModelRegistry` at stage `shadow` or higher.
- **What it does**:
  1. **Activate** — writes `data/scenarios/active_drift.json` = `{"scenario": "week78", "window_start": "week_78_day_1", "window_days": 30}`.
  2. **Payload** — `data/scenarios/week78_drift.json` is the pre-built 30-day post-drift window with shifted customer mix (documented in `data-fixtures.md`). The activation marker tells `/drift/check` and `/forecast/predict` to use this window as the comparison set.
  3. **Log** to `.scenario_log.jsonl`.
- **Endpoint to re-trigger**: `POST /drift/check` with `model_id: <mv_X>` — the endpoint compares the post-drift window against the training reference and returns severity + per-feature test results.
- **Phases to re-run**: 13 (drift triggers), 5 (model implications — is the chosen model still the right pick post-drift?), 6 (metric + threshold — does the threshold need to shift?).
- **Viewer Pane effect**: `DriftPanel.tsx` updates within the ≤ 1 s polling window to show the new severity and per-feature tests. `ForecastPanel.tsx` optionally overlays the post-drift window.
- **Journal expectation**: student writes `journal/phase_13_retrain.md` with signals + thresholds grounded in historical variance.
- **Common mis-fires**:
  - Student runs `/drift/check` without `set_reference_data` — mitigated by `drift_wiring.py` auto-wiring. If it still fires, grader's actionable message guides the fix.
  - Student writes "retrain when MAPE > 15%" → `agent-reasoning.md` violation; instructor demonstrates the reframing in a 60-second aside.
- **Rollback**: `metis scenario fire drift-week-78 --undo` removes `active_drift.json`. The fixture file `week78_drift.json` is not deleted. DriftMonitor's stored reference (written by `drift_wiring.wire` on train completion) is NOT cleared — a re-fire recomputes against the same reference.

### 2.3 `casemix-tariff-cut` (dry-run only in Week 4)

The SG-localised reimbursement-shock scenario. Casemix tariffs set reimbursement levels for Singapore acute-care hospital procedures; a tariff cut is the SG equivalent of Week 7's US Medicare-cut rehearsal. The event was renamed from `medicare-cut` after red-team — firing US-healthcare language into an SG MBA cohort is a communication failure (see `communication.md`); the SG cohort's context is MediShield Life / Casemix.

- **When fired**: never in Week 4. The dry-run path exists so instructors can rehearse the Week 7 flow without mutating the workshop's workspace.
- **What it does (dry-run)**: prints the mutation plan — "would write `data/scenarios/active_casemix_tariff_cut.json` with Casemix tariff reduced by 18% starting 2027-Q1; would re-trigger `/forecast/predict` on the Week 7 healthcare dataset" — and exits 0.
- **Actual mutation**: deferred to Week 7's healthcare workshop.
- **Rollback**: N/A (no state mutated).

## 3. Timing windows

| Event                | Sprint       | Fire at (min into sprint) | Student re-run budget |
| -------------------- | ------------ | ------------------------- | --------------------- |
| `union-cap`          | Sprint 2     | 30 (wall-clock ~02:05)    | 25 min                |
| `drift-week-78`      | Sprint 3     | 5 (wall-clock ~02:40)     | 30 min                |
| `casemix-tariff-cut` | Week 7 (N/A) | —                         | —                     |

Timing is quoted as sprint-relative (minute-into-sprint) with wall-clock shown parenthetically. Sprint-relative is the primary reference; wall-clock is the secondary/cross-check.

The instructor MUST fire the event AT the minute specified, ± 2 min. Earlier and the student hasn't built the state to inject into; later and the re-run budget is crushed.

## 4. Instructor three-line chat snippet

The instructor drops this into the shared class chat at the moment of injection so students can paste it into Claude Code:

```
SCENARIO FIRED: <event_name>. Save prior state as route_plan_preunion.json
(if not already). Re-run Phase 11 (re-classify the affected constraint) and
Phase 12 (re-solve). Write new plan to route_plan_postunion.json. Journal both.
```

The snippet is tuned for `union-cap`; the `drift-week-78` version reads:

```
SCENARIO FIRED: drift-week-78. Run /drift/check against the new active window.
Re-run Phases 5 and 6 on post-drift data. Journal Phase 13 with signals +
thresholds grounded in historical variance — NOT "if MAPE > 15% retrain".
```

Both snippets live in `scripts/instructor_brief.md`.

## 5. Pre-baked fixture payloads

See `data-fixtures.md` for the shape and content of `data/scenarios/union_cap.json` and `data/scenarios/week78_drift.json`. This spec only governs the CLI's behaviour around them; the data content lives in the fixtures spec.

## 6. Failure modes and mitigations

| Failure                                                 | Mitigation                                                                                                                             |
| ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Student hadn't run `/optimize/solve` before `union-cap` | CLI exits 3 (pre-condition not met); instructor waits 2 min and re-fires                                                               |
| Student overwrote `route_plan.json` with no snapshot    | `--undo` restores from `route_plan_preunion.json`; if that is also missing, instructor regenerates from `seed_experiments.py` seed run |
| Multiple students run mixed-state fires                 | Each student's workspace is independent; the instructor's fire is a signal, not a shared mutation — students run the local equivalent  |
| CLI can't find workspace root                           | Exit 2 with remediation: "pass `--target <path>` pointing at your week-04-supply-chain workspace"                                      |
| Viewer Pane doesn't reflect the scenario within 1 s     | `viewer-pane.md` polling contract violated; fall back to `cat data/.scenario_log.jsonl`                                                |

## Open questions

- **Shared-classroom topology** — the analysis artefacts assume each student runs a local workspace and the instructor fires on the shared screen as a signal. An alternate topology (instructor fires into a shared filesystem all students mount) is not specified; if adopted, the CLI's `--target` resolution semantics need revisiting.
