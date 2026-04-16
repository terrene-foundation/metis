# Scenario Catalog — Singapore-Localized Injections

<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

This file is the authority on which live scenarios the instructor can fire during the Week 4 workshop. It replaces the US-centric `medicare-cut` dry-run with scenarios grounded in the real regulatory and operating environment for a Singapore last-mile logistics operator. `scenario-injection.md` remains the authority on the CLI mechanics (`metis scenario fire <id>`, exit codes, logging); this file enumerates WHICH events exist and what they mean in business terms.

Every event ID is registered in `canonical-values.md` §11. The five scenarios below cover the three sprint surfaces (Forecast / Optimize / Monitor) plus a cross-cutting governance scenario for Week 5+ rehearsal.

---

## 1. Singapore context for Northwind Logistics

The workshop persona ("Northwind Logistics") operates a last-mile delivery network across Singapore: 3 depots, 20 vehicles, 12k orders/day, 500 regular B2B customers. The regulatory surface this creates is small but sharp:

- **Ministry of Manpower (MOM)** sets the Dependency Ratio Ceiling (DRC) for foreign workers and regulates driver working hours under the Employment Act. Changes here land within weeks and reshape crew rosters immediately.
- **Land Transport Authority (LTA)** regulates road use, vehicle emissions, and — as of the national climate plan — piloted carbon-levy schemes on commercial fleets.
- **Housing & Development Board (HDB)** manages the estates where ~80% of B2C deliveries drop. Estate-level noise curfews on loading bays are enforced by Town Councils with escalating fines.
- **Monetary Authority of Singapore (MAS)** sets financial-sector climate-risk disclosure rules (Notice 626 / SS-IFRS S2) that cascade to logistics operators through bank-mandated reporting on financed emissions.

These four agencies produce the kind of mid-workshop rule changes that test whether a student's ML + optimization pipeline can re-reason under new constraints. The scenarios below each target one agency's surface and one sprint's learning objective.

Every scenario is deployable on a student's laptop — no external network, no paid API, no agency calls. Payload files ship as JSON fixtures; the instructor fires with `metis scenario fire <id>`.

---

## 2. `union-cap` — Driver overtime cap tightens (MOM Employment Act framing)

**One-liner (MBA-readable):** The Ministry of Manpower tightens driver overtime rules mid-week (SG Employment Act circular — equivalent in effect to a union-negotiated OT ceiling, hence the legacy event ID). The optimizer's "overtime is cheap" assumption is no longer true, and routes must be re-planned.

- **ID:** `union-cap` (legacy identifier; SG framing = MOM Employment Act tightening. Artifact paths `route_plan_preunion.json` / `_postunion.json` retain this shorthand.)
- **Sprint:** 2 (Optimize)
- **When fired:** minute 30 of Sprint 2 (≈ workshop T+02:05)
- **Deployable tomorrow:** YES
- **Trigger prerequisite:** student has run `POST /optimize/solve` at least once; `data/route_plan.json` exists.
- **What it mutates:**
  - Snapshot — `cp data/route_plan.json data/route_plan_preunion.json` (before-baseline)
  - Write `data/scenarios/active_union_cap.json`:
    - **Before:** scenario not active; `driver_overtime_hours_max` is a soft constraint with $45/hr penalty.
    - **After:** `{"constraint": "driver_overtime_hours_max", "new_cap": 5, "unit": "hours_per_week", "classification_hint": "hard", "reason": "MOM Employment Act circular tightens overtime ceiling for logistics sector"}`
  - Append `.scenario_log.jsonl`
- **Endpoint re-triggered:** `POST /optimize/solve` with `scenario_tag: "postunion"` and the re-classified constraint set (overtime now hard, cap 5 hr/week). Student writes result to `data/route_plan_postunion.json` (NOT overwriting `route_plan.json`).
- **Viewer Pane change:** `RoutePanel.tsx` flips default view to `_postunion`; the `_preunion` view remains selectable for before/after comparison.
- **Rollback:** `metis scenario fire union-cap --undo` deletes the active marker and restores `route_plan.json` from the `_preunion` snapshot.
- **Exit codes:**
  - `0` fired successfully
  - `1` unknown event
  - `2` workspace not detected
  - `3` pre-condition not met (no `route_plan.json`)
  - `4` already fired — pass `--re-fire` to replay (idempotency guard)

**Learning objective:** D4 — re-classify a soft constraint as hard under an explicit regulatory signal. A student who merely raises the overtime penalty to $200/hr scores 1/4 on D4; quantifying the 5 hr/week cap as a hard constraint with penalty reasoning scores 4/4.

---

## 3. `drift-week-78` — Post-Chinese-New-Year demand shift

**One-liner (MBA-readable):** Eight weeks after Chinese New Year, customer ordering patterns have drifted enough that the trained model's error is creeping up; the student must detect it, diagnose which feature moved, and decide whether to retrain.

- **ID:** `drift-week-78`
- **Sprint:** 3 (Monitor)
- **When fired:** minute 5 of Sprint 3 (≈ workshop T+02:40)
- **Deployable tomorrow:** YES
- **Trigger prerequisite:** student has at least one registered model in `ModelRegistry` at stage `shadow` or higher.
- **What it mutates:**
  - Write `data/scenarios/active_drift.json`:
    - **Before:** file absent; `/drift/check` compares against the training reference window only.
    - **After:** `{"scenario": "week78", "window_start": "week_78_day_1", "window_days": 30, "cultural_anchor": "post_CNY_week_8"}`
  - The payload `data/scenarios/week78_drift.json` ships pre-built (30-day window with shifted customer-mix distribution; see `data-fixtures.md` §2.4).
  - Append `.scenario_log.jsonl`
- **Endpoint re-triggered:** `POST /drift/check` with `model_id: <alias>`, `window_days: 30`. Returns severity per `canonical-values.md` §1 enum (`none | moderate | severe`) plus KS + PSI tests per feature.
- **Viewer Pane change:** `DriftPanel.tsx` updates within ≤ 1 s polling window — severity chip flips to `moderate`; `customer_mix` row highlights with KS statistic ≈ 0.34 and p-value ≈ 0.002; `ForecastPanel.tsx` optionally overlays the post-drift window.
- **Rollback:** `metis scenario fire drift-week-78 --undo` removes `active_drift.json`; the fixture `week78_drift.json` is preserved.
- **Exit codes:** `0` success · `1` unknown event · `2` workspace not detected · `3` no shadow-or-higher model in registry · `4` already fired.

**Learning objective:** D5 — reversal condition grounded in historical variance, not bare thresholds. A Phase 13 journal entry that says "retrain when MAPE > 15%" scores 0/4 on D5 (violates `agent-reasoning.md`); one that says "retrain when 7-day rolling MAPE exceeds training-window p95 for 3 consecutive days AND `customer_mix` PSI > 0.25" scores 4/4.

---

## 4. `lta-carbon-levy` — Per-km carbon levy lands mid-sprint

**One-liner (MBA-readable):** The Land Transport Authority pilots a per-km carbon levy on commercial fleets; the optimizer's objective function must gain a new cost term or routes will silently over-pay the levy.

- **ID:** `lta-carbon-levy`
- **Sprint:** 2 or 3 (Optimize re-run OR Monitor re-run) — instructor picks the firing sprint based on cohort pacing.
- **When fired:** minute 35 of Sprint 2 (if chosen) OR minute 15 of Sprint 3 (if Monitor focus)
- **Deployable tomorrow:** YES
- **Trigger prerequisite:** `/optimize/solve` has been run at least once with the baseline objective.
- **What it mutates:**
  - Write `data/scenarios/active_lta_carbon_levy.json`:
    - **Before:** file absent; objective has 3 terms — `fuel` ($0.35/km), `sla` ($220/violation), `overtime` ($45/hr).
    - **After:** `{"new_term": {"name": "carbon_levy", "weight": 0.18, "unit": "per_km", "reason": "LTA commercial fleet carbon pilot (2026 Q2)"}, "applies_to_vehicles": "all_diesel", "revenue_neutral_rebate": false}`
  - The activation marker does NOT mutate the request schema — the student must add the new term when they call `/optimize/solve` with `scenario_tag: "post_carbon_levy"`. This is deliberate: the scenario tests whether the student re-reads the objective contract rather than re-running the old request.
  - Append `.scenario_log.jsonl`
- **Endpoint re-triggered:** `POST /optimize/solve` with the 4-term objective body:
  ```json
  {
    "objective": {
      "terms": [
        { "name": "fuel", "weight": 0.35, "unit": "per_km" },
        { "name": "sla", "weight": 220, "unit": "per_violation" },
        { "name": "overtime", "weight": 45, "unit": "per_hour" },
        { "name": "carbon_levy", "weight": 0.18, "unit": "per_km" }
      ]
    },
    "scenario_tag": "post_carbon_levy"
  }
  ```
- **Viewer Pane change:** `OptimizePanel.tsx` shows a new "carbon_levy" row in the objective-terms breakdown; `objective_value` rises by ~$0.53/km × total-km — the delta is visible as a before/after bar overlay.
- **Rollback:** `metis scenario fire lta-carbon-levy --undo` deletes the active marker. The student's 4-term request bodies remain in their journal; they can be replayed if the levy is re-introduced.
- **Exit codes:** `0` success · `1` unknown event · `2` workspace not detected · `3` no baseline `/optimize/solve` run on record · `4` already fired.

**Learning objective:** D3 — quantifying the trade-off. A student who reports "routes are now more expensive" scores 2/4 on D3; one who names "fuel+levy combined unit cost rose from $0.35/km to $0.53/km, total plan cost +$214/day on 612 km of daily routing" scores 4/4.

---

## 5. `hdb-loading-curfew` — Estate-level loading curfew

**One-liner (MBA-readable):** HDB Town Councils enforce a 9pm–7am loading-bay curfew at residential estates; the optimizer must add a hard time-window constraint per depot-estate pair or plans will violate delivery regulations.

- **ID:** `hdb-loading-curfew`
- **Sprint:** 2 (Optimize)
- **When fired:** NOT FIRED in Week 4 — ships as `--dry-run` only for Week 5+ rehearsal. The dry-run path lets instructors validate the time-window handling before a real cohort runs it.
- **Deployable tomorrow:** PARTIAL — payload ships; live firing deferred to Week 5+ because the time-window solver path in `routes/optimize.py` requires OR-Tools VRP-TW extension which is not in the Week 4 preflight guarantee.
- **Trigger prerequisite:** student has a registered vehicle fleet with depot-to-estate assignments.
- **What it would mutate:**
  - Write `data/scenarios/active_hdb_curfew.json`:
    - **Before:** file absent; no time-window constraint per estate.
    - **After:** `{"constraint_type": "hard_time_window", "forbidden_window": {"start": "21:00", "end": "07:00"}, "applies_to_estates": ["ANG_MO_KIO", "BEDOK", "JURONG_WEST"], "reason": "HDB Town Council noise bylaw — repeat violations fineable at $500 per event", "classification_hint": "hard"}`
  - Append `.scenario_log.jsonl`
- **Endpoint re-triggered:** `POST /optimize/solve` with `hard_constraints.loading_time_window` populated per-estate.
- **Viewer Pane change:** `RoutePanel.tsx` flags any Gantt bar crossing the 21:00–07:00 window in red; the solver either shifts the bar to a legal window OR the feasibility flips to `false` with `violated_constraints: ["loading_time_window"]`.
- **Rollback:** `--undo` deletes the marker; fleet assignments are unchanged.
- **Exit codes:** `0` dry-run printed · `5` live-fire blocked in Week 4 (reserved code for "Week 5+ only") · `1` unknown event · `2` workspace not detected.

**Learning objective:** D4 — classifying a time-window constraint as hard with dollar-denominated penalty reasoning ($500/event × expected-violations/week). Also rehearses the feasibility-false code path: a plan that was feasible before the curfew may become infeasible, and the journal entry must name WHICH constraint is now binding.

---

## 6. `mas-climate-disclosure` — Audit row must carry carbon metric

**One-liner (MBA-readable):** MAS climate-risk disclosure requires every audit-row in the logistics operator's pipeline to carry a carbon metric; the Trust Plane's audit schema gains a required field and legacy rows fail validation.

- **ID:** `mas-climate-disclosure`
- **Sprint:** Close (Phase 9 codify) — cross-cutting governance scenario
- **When fired:** NOT FIRED in Week 4 — ships as `--dry-run` only. The live-fire path requires the Trust Plane audit-schema migration machinery which lands in Week 6 (governance sprint).
- **Deployable tomorrow:** NO — Week 5+ ready; dry-run validates the Week 6 rehearsal path.
- **Trigger prerequisite:** student has at least one successful `POST /optimize/solve` AND `POST /forecast/predict` logged with audit rows.
- **What it would mutate:**
  - Write `data/scenarios/active_mas_disclosure.json`:
    - **Before:** audit rows have columns `{run_id, agent_id, operation, clearance, timestamp}`.
    - **After:** `{"new_required_field": "carbon_kg_co2e", "applies_from": "2026-Q3", "legacy_row_policy": "mark_as_non_compliant", "reason": "MAS Notice 626 climate-risk disclosure cascaded via lender covenants"}`
  - Append `.scenario_log.jsonl`
- **Endpoint re-triggered:** NO new endpoint — the scenario instead validates that audit rows pass the new schema. Grader runs `scripts/grade_product.py --check-audit-disclosure` (Week 6+ only) which re-reads every audit row and reports non-compliance count.
- **Viewer Pane change:** `AuditPanel.tsx` (Week 6+) gains a `carbon_kg_co2e` column; pre-disclosure rows render with a red badge "non-compliant — re-compute carbon".
- **Rollback:** `--undo` deletes the marker; the audit schema reverts to the 5-column shape.
- **Exit codes:** `0` dry-run printed · `5` live-fire blocked in Week 4 · `1` unknown event · `2` workspace not detected.

**Learning objective:** governance foresight — students see that today's optimisation choices (diesel-heavy routes, carbon-levy avoidance) have audit-trail consequences under tomorrow's disclosure regime. Journal entry scores on D5 by naming the disclosure-timing signal as a reversal condition.

---

## 7. Scenario firing matrix

| ID                       | Sprint | Week 4 live? | File mutated                                 | Endpoint re-run                                      | Exit on success | Exit on pre-cond fail |
| ------------------------ | ------ | ------------ | -------------------------------------------- | ---------------------------------------------------- | --------------- | --------------------- |
| `union-cap`              | 2      | YES          | `data/scenarios/active_union_cap.json`       | `POST /optimize/solve` (`scenario_tag: "postunion"`) | 0               | 3                     |
| `drift-week-78`          | 3      | YES          | `data/scenarios/active_drift.json`           | `POST /drift/check`                                  | 0               | 3                     |
| `lta-carbon-levy`        | 2 or 3 | YES          | `data/scenarios/active_lta_carbon_levy.json` | `POST /optimize/solve` (4-term objective)            | 0               | 3                     |
| `hdb-loading-curfew`     | 2      | dry-run only | `data/scenarios/active_hdb_curfew.json`      | `POST /optimize/solve` (time-window constraint)      | 0 (dry-run)     | 5 (Week 5+ only)      |
| `mas-climate-disclosure` | close  | dry-run only | `data/scenarios/active_mas_disclosure.json`  | audit schema validation (Week 6+ grader flag)        | 0 (dry-run)     | 5 (Week 5+ only)      |

Three scenarios (`union-cap`, `drift-week-78`, `lta-carbon-levy`) fire live tomorrow; two (`hdb-loading-curfew`, `mas-climate-disclosure`) are dry-run-only shells whose payloads validate the Week 5+ rehearsal surface without mutating the Week 4 workspace.

## 8. Instructor three-line chat snippets

The instructor drops one of these into class chat at the moment of firing. Students paste it into Claude Code:

**`union-cap`:**

```
SCENARIO FIRED: union-cap. Save prior plan as route_plan_preunion.json
(if not already). Re-classify driver_overtime_hours_max as HARD with 5 hr/week
cap. Re-run Phase 11 + 12; write result to route_plan_postunion.json. Journal both.
```

**`drift-week-78`:**

```
SCENARIO FIRED: drift-week-78 (post-CNY customer-mix shift). Run POST /drift/check
with the new active window. Re-run Phases 5 and 6 on post-drift data. Journal Phase 13
with signals + thresholds grounded in training-window p95 — NOT "if MAPE > 15% retrain".
```

**`lta-carbon-levy`:**

```
SCENARIO FIRED: lta-carbon-levy ($0.18/km carbon levy on diesel fleet). Add the
carbon_levy term to the objective function; re-run POST /optimize/solve with
scenario_tag: "post_carbon_levy". Quantify the cost delta in your journal Phase 10.
```

All three snippets live in `scripts/instructor_brief.md` (scaffold).

## 9. Relationship to other specs

- `canonical-values.md` §11 — registers every scenario ID.
- `scenario-injection.md` — authoritative on the CLI mechanics (firing, logging, rollback, topology).
- `data-fixtures.md` — owns the payload fixtures referenced above.
- `viewer-pane.md` — owns the panel update contracts referenced as "Viewer Pane change".
- `rubric-grader.md` — owns the D1–D5 anchors a student is graded on after each scenario re-run.
