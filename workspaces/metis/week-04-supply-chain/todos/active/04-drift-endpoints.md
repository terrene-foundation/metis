---
shard_id: 04
slug: drift-endpoints
title: >
  Implement the STUDENT-COMMISSIONED /drift/check route handler wired to
  DriftMonitor.check_drift, enforcing the 3-value severity enum and KS+PSI-only
  test names, plus the Tier-2 DriftMonitor wiring test that proves
  drift_wiring.wire fired and overall_severity is present in both the response
  and data/drift_report.json.
loc_estimate: 180
invariants:
  - severity-3-values: overall_severity field (not "severity") is one of {"none","moderate","severe"}; "low" never appears
  - ks-psi-only: tests[].name is one of {"ks","psi"}; no chi2, no js-divergence
  - reference-guard: /drift/check returns 409 with actionable message when set_reference_data has not been called; never returns bare 500
  - drift-report-file: data/drift_report.json written atomically after every successful check; contains overall_severity field (matching wording)
  - no-re-seed: /drift/check does NOT call set_reference_data; that is drift_wiring.wire's sole responsibility
call_graph_hops: 3
depends_on: [01, 02]
blocks: []
specs_consulted:
  - specs/canonical-values.md §1 (DriftMonitor severity enum — exactly 3 values)
  - specs/canonical-values.md §8.5 (POST /drift/check contract)
  - specs/product-northwind.md §8.5 (full request/response + error taxonomy)
  - specs/scaffold-contract.md §2 (banner text for routes/drift.py, verbatim)
  - specs/wiring-contracts.md §6 (DriftMonitor wiring test contract — overall_severity, drift_report.json, .preflight.json.drift_wiring)
  - specs/data-fixtures.md §2 (week78 drift payload shape)
acceptance_criteria:
  - src/backend/routes/drift.py ships with TODO-STUDENT banner from scaffold-contract.md §2 (verbatim); 501-stub body; route registration stays put
  - POST /drift/check calls ctx.drift_monitor.check_drift(model_name, current_data); returns 409 with message per product-northwind.md §8.5 when reference not set; returns 404 when model not found
  - Response top-level field is overall_severity (not severity); value in {"none","moderate","severe"} per canonical-values.md §1
  - Response tests array contains only entries with name in {"ks","psi"}; each ks entry has p_value field; psi entries do not require p_value
  - data/drift_report.json written atomically after successful check; contains overall_severity field
  - tests/integration/test_drift_monitor_wiring.py passes per wiring-contracts.md §6: (1) overall_severity in {"none","moderate","severe"}; (2) data/drift_report.json written with matching field name; (3) .preflight.json.drift_wiring===true after train call (proves synchronous wire fired)
orphan_resolution:
  AnomalyDetectionEngine: "DELETED (completed) — no natural call site existed in /drift/check or any other endpoint. Per orphan-detection Rule 3, removed from ml_context public surface. wiring-contracts.md §12 section deleted (scope header updated 12→11 components). scaffold-contract.md §9 never listed AnomalyDetectionEngine (verified). START_HERE.md reference noted for removal under separate doc-cleanup track; not blocking /implement."
wiring_tests:
  - tests/integration/test_drift_monitor_wiring.py (wiring-contracts.md §6)
---

# Shard 04 — Drift Endpoints

## What

Implement the /drift/check route with the correct field name (overall_severity), the 3-value enum, KS+PSI-only test names, the file write contract, and the single DriftMonitor Tier-2 wiring test. This is the smallest backend shard by LOC because the heavy lifting (drift_wiring.wire, set_reference_data) was done in shard 01; this shard only implements the check path.

## Why

The most common student failure in Sprint 3 is a 409 "reference data not set" because drift_wiring.wire never fired. The wiring test asserts the .preflight.json.drift_wiring marker was written by the synchronous wire call in /forecast/train — not by an event hook that does not exist. This test is the structural guard for that invariant.

## Implementation sketch

- `routes/drift.py` — TODO-STUDENT banner (verbatim from scaffold-contract.md §2); 501-stub body; route registration stays; inline comment: "DriftMonitor.check_drift returns DriftReport with overall_severity in {'none','moderate','severe'} (3 values, not 4); tests[].name in {'ks','psi'} only; set_reference_data is called by drift_wiring.wire — do NOT re-seed here"
- Route handler resolves model_id via ml_context.parse_model_version_id; calls ctx.drift_monitor.check_drift; maps DriftReport fields to response schema; writes data/drift_report.json atomically; 409 guard checks for reference-not-set error type from library
- Wiring test uses two polars frames (reference slice from training window, post-drift slice from data/scenarios/week78_drift.json shape); calls POST /forecast/train first to trigger drift_wiring.wire as side effect; then POST /drift/check; asserts all three external effects per wiring-contracts.md §6

## Out of scope

- /drift/status route (already in shard 01 as routes/drift_status.py)
- AnomalyDetectionEngine — DELETED from public surface per orphan-detection Rule 3 (decision completed at /todos — spec edits executed in the pre-/implement gate); wiring-contracts.md §12 entry removed and scope header updated to 11 components; no /drift/anomalies endpoint will exist
- scenario_inject.py drift-week-78 firing (shard 06)
- DriftPanel viewer rendering (shard 05)

## Acceptance

- [ ] src/backend/routes/drift.py ships with TODO-STUDENT banner from scaffold-contract.md §2 (verbatim); 501-stub body; route registration stays put
- [ ] POST /drift/check calls ctx.drift_monitor.check_drift(model_name, current_data); returns 409 with message per product-northwind.md §8.5 when reference not set; returns 404 when model not found
- [ ] Response top-level field is overall_severity (not severity); value in {"none","moderate","severe"} per canonical-values.md §1
- [ ] Response tests array contains only entries with name in {"ks","psi"}; each ks entry has p_value field; psi entries do not require p_value
- [ ] data/drift_report.json written atomically after successful check; contains overall_severity field
- [ ] tests/integration/test_drift_monitor_wiring.py passes per wiring-contracts.md §6: (1) overall_severity in {"none","moderate","severe"}; (2) data/drift_report.json written with matching field name; (3) .preflight.json.drift_wiring===true after train call (proves synchronous wire fired)
