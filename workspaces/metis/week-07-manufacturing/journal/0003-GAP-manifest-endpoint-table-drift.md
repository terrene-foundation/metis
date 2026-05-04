---
type: GAP
date: 2026-05-04
created_at: 2026-05-04T13:45:00+08:00
author: agent
session_id: 0b709081-dc57-4817-a9fe-8bae014f9294
project: metis-week-07-manufacturing
topic: SCAFFOLD_MANIFEST endpoint table drifted from code in R1; fully reconciled in R2
phase: redteam
tags: [spec-compliance, scaffold-manifest, endpoint-table, ast-audit]
---

# SCAFFOLD_MANIFEST endpoint table drifted from code; fully reconciled in R2

## Context

`/redteam` Round 2 ran a stronger spec-compliance audit than R1 by re-deriving the assertion tables from scratch via Python `ast.parse()` instead of bash `grep`. Three new drifts surfaced that R1 missed because its grep-based extraction collapsed (METHOD, path) pairs to unique paths only, hiding cases where two methods on the same path diverged.

R1 result (grep-based): spec 32 ≡ code 32 — appeared clean.
R2 result (AST-based): spec 34 = code 34, manifest 33 → drift surfaces.

The 2-tuple difference was: GET and POST on `/inspect/vision/threshold`, `/optimize/rl/reward_function`, `/agent/policy`, `/drift/retrain_rule` were each counted once at path level (R1) but as two distinct rows at (METHOD, path) level (R2).

## Findings

| #   | Drift                                                         | Severity | Resolution                                                                                                       |
| --- | ------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------- |
| F5  | Manifest had `GET /inspect/vision/threshold` row              | HIGH     | Removed (no GET binding in code; current state via `/inspect/vision/leaderboard.promoted_thresholds`)            |
| F6  | Manifest missing `GET /optimize/rl/registry` row              | HIGH     | Added; section header bumped from "33 routes" to "34 routes"                                                     |
| F7  | Manifest had `GET /drift/retrain_rule` (missing `{model_id}`) | MEDIUM   | Renamed to `GET /drift/retrain_rule/{model_id}` (matches code); added missing `GET /drift/status/{model_id}` row |

## What was done

1. Removed orphan `GET /inspect/vision/threshold` row from manifest endpoint table.
2. Added missing `GET /optimize/rl/registry` row (existed in code via `inspect_vision.py` mirror but was never documented).
3. Fixed `/drift/retrain_rule` GET row to include the `{model_id}` path parameter.
4. Added missing `/drift/status/{model_id}` GET row (was in code + spec but not manifest).
5. Bumped manifest section header count from "33 routes" to "34 routes".
6. R3 verification: spec ≡ manifest ≡ code at 34 (METHOD, path) tuples — three-way parity.

## Why R1 missed this

The R1 audit used `grep ... | sort -u` which deduplicates at the URL-path level. A path with both GET and POST handlers (4 such paths in this scaffold) collapsed to a single row in the comparison set. The unique-path counts agreed (32 = 32) so R1 reported clean.

R2 used Python AST: it walks each route file's decorator list, captures `(decorator.func.attr, decorator.args[0].value)` as the unit of comparison, and surfaces every (METHOD, path) tuple separately. This is the canonical "structural enumeration via parser" pattern from `rules/testing.md` § "MUST: `__all__` / Re-export Symbol Counts Use Structural Enumeration, Not Grep" — the same principle applies to API surface enumeration.

## Generalisable lesson

For any `/redteam` audit of API surface, the comparison unit MUST be the (METHOD, path) tuple, not the path alone. Use AST parsing of route decorators (Python: `ast.parse + walk`; Rust: `syn::parse_file`) rather than grep extraction.

Future scaffolds should run this AST-based audit at the end of `/implement`, not at `/redteam` — catching the drift before the manifest ships saves an audit round.

## For Discussion

1. Counterfactual: had R1 used the AST-based audit instead of grep-based, would F1 (the predmaint endpoint drift) and F5/F6 (manifest drifts) have surfaced together as a single round-1 finding cluster, or would F5/F6 have remained hidden behind F1 fixes? Specifically, did fixing F1 (renaming `/calibration` → `/calibrate` etc.) in R1 mask any latent F5/F6 issues?

2. Specific data: code has 34 (METHOD, path) tuples but only 32 unique paths. The ratio of 2 GET+POST paths per `/agent/policy` `/optimize/rl/reward_function` `/inspect/vision/threshold` `/drift/retrain_rule` (well, 4 "doubled" paths × 2 = 8 rows; the rest 26 paths × 1 = 26 rows; 8 + 26 = 34) means the drift surface is concentrated on read/write pairs. Should the spec format itself be (METHOD, path)-keyed (one row per tuple) instead of path-keyed (sometimes two rows for the same path)? It would force authors to write GET and POST contracts explicitly.

3. The new `/drift/status/{model_id}` row was also missing from the manifest. It's a GET endpoint that the playbook's `workflow-03-sprint-1-vision-boot.md` opening prompt relies on (step 4 of the boot prompt: "GET /drift/status/vision returns 'registered: true'"). Had a student copied the manifest's endpoint inventory verbatim into a journal entry as their endpoint reference, they would have been missing the very endpoint the boot prompt asks them to call. This is a leading indicator that workshop materials need a "manifest is the inventory; spec is the contract" rule — when they diverge, the spec wins.
