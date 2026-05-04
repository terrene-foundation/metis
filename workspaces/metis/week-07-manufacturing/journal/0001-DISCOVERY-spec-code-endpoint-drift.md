---
type: DISCOVERY
date: 2026-05-04
created_at: 2026-05-04T13:30:00+08:00
author: agent
session_id: 0b709081-dc57-4817-a9fe-8bae014f9294
project: metis-week-07-manufacturing
topic: spec/code endpoint drift surfaced by /redteam Round 1
phase: redteam
tags: [spec-compliance, predmaint, calibrate, train, scaffold-manifest]
---

# Spec/code endpoint drift surfaced by /redteam Round 1

## Context

`/redteam` Round 1 ran the canonical spec-compliance audit on the Week 7 scaffold: extracted the 33-row endpoint table from `specs/api-surface.md` and the 32 actual `@router.get/post(...)` decorations from `routes/*.py`, sorted both, diffed.

Three spec/code mismatches surfaced — all in `predict_maintenance.py`, none in the other six route files (vision / RL / agent / drift / queue / state were spec-clean).

## Findings

| #   | Spec said                                                                  | Code had                                         | Why it drifted                                                                                                  |
| --- | -------------------------------------------------------------------------- | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| 1   | `POST /predict/maintenance/calibrate` with `{method: "platt"\|"isotonic"}` | `GET /predict/maintenance/calibration` (no body) | I built the spec-authored shape (POST + method) but during code build chose the simpler GET-with-no-body shape. |
| 2   | `POST /predict/maintenance/train` with `{family?, seed}`                   | (missing entirely)                               | Vision had `/train`; predmaint did not — symmetry break.                                                        |
| 3   | (not listed)                                                               | `POST /predict/maintenance/family`               | Code added an explicit family-selection lever; spec was never updated.                                          |

In addition: `SCAFFOLD_MANIFEST.md` endpoint table cited the obsolete `GET /calibration`, and `todos/active/phase_6_predmaint.md` cited `GET /predict/maintenance/calibration` — two downstream artefacts inheriting the same drift.

## What was done

1. Added `POST /predict/maintenance/calibrate` with platt/isotonic body (rejects unknown methods at handler).
2. Added `POST /predict/maintenance/train` (mirrors vision/train, re-fits leaderboard with new seed, preserves chosen family/window/threshold across the retrain).
3. Updated `specs/api-surface.md` to document the existing `POST /predict/maintenance/family` lever instead of removing it from code (it gives students an explicit Phase 5 entry point distinct from `/promote`).
4. Updated SCAFFOLD_MANIFEST endpoint table to list `/calibrate POST`, `/train POST`, `/family POST`, `/registry GET` — filling 4 prior gaps.
5. Updated `todos/active/phase_6_predmaint.md` to reference `POST /calibrate` with method body.
6. Re-ran the spec/code diff: zero drift.
7. Smoke-tested both new endpoints + bogus-method rejection on `/calibrate`.

## Why this matters

The 32-endpoint surface is what students paste into Claude Code via the playbook's paste-ready blocks. A drift between spec and code = a paste that returns 404, breaking workshop flow at exactly the wrong moment (mid-Phase-6 when students are about to commit a threshold).

The drift was invisible to the smoke test in the original build because:

- The smoke test exercised every endpoint that _did_ exist.
- It didn't enumerate from the spec to confirm every spec endpoint was reachable.

The fix at the audit stage is the AST/grep diff. The fix at build time would be the same diff run pre-commit.

## For Discussion

1. Counterfactual: had the spec-compliance audit run only on the spec table (forward direction — every spec row exists in code) and not also on the code (reverse direction — every code endpoint is documented in spec), the orphan `/family` endpoint would never have surfaced. Should `/redteam` mandate the bidirectional check, or accept that orphan code endpoints are lower-severity than missing spec endpoints?

2. Specific data: at default seed 20260504, the `/predict/maintenance/calibrate` endpoint returns `brier_pre=0.000, brier_post=0.000` because the chosen family (LightGBM at 7d window) already fits the 10-machine training set perfectly. The synthetic adjustment delta (-0.02 platt / -0.03 isotonic) clamps to 0.0. Is the calibrate endpoint pedagogically useful when both pre and post are zero, or should the scaffold inject a per-machine holdout split inside `/calibrate` so students see a non-zero Brier and a non-zero delta?

3. The drift surfaced because I built code-first then spec-after, and the two were authored asynchronously across the same session. If next week's scaffold is built spec-first (write `specs/api-surface.md` complete, then code from spec), would the same drift surface, or would the drift simply move from "spec lags code" to "code lags spec"? Which failure mode is cheaper to fix at audit?
