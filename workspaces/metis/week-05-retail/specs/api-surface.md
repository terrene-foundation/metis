<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Arcadia Retail — API Surface

Base URL: `http://127.0.0.1:8000` (override with `METIS_API_PORT`).

All endpoints are wired in `src/retail/backend/routes/`. Students call them indirectly through Claude Code; they do not implement them.

## Health

- `GET /health` — `{ status, customers, products, transactions, baseline_silhouette, baseline_k, baseline_stage }`

## Segmentation

- `GET  /segment/baseline` — K=3 baseline already shipped (silhouette, sizes, stage)
- `GET  /segment/candidates` — pre-baked K-sweep K=2..10 for comparison against live runs
- `POST /segment/fit` — `{ algorithm: "kmeans"|"dbscan"|"spectral", k_range, eps, min_samples, seed }` — run a live sweep
- `POST /segment/name` — `{ version, names, actions }` — Phase 5 deliverable; validates one-action-per-segment
- `POST /segment/promote` — `{ version, to_stage }` — staging → shadow → production → archived
- `GET  /segment/registry` — all versions + current production + shadow
- `GET  /segment/stability?seed=N` — Phase 7 red-team probe (Jaccard same-pair on re-seed)

## Recommender

- `GET  /recommend/config` — current mode, hybrid weights, cold-start strategy, constraints
- `POST /recommend/config` — Phase 10 deliverable; sets mode + weights + cold-start disposition
- `POST /recommend/for_customer` — `{ customer_id, n, mode }` — fires cold-start path when < 3 txns
- `POST /recommend/compare` — `{ n, sample_size }` — Phase 12 offline eval: precision@k, coverage, cold-start coverage

## Drift

- `GET  /drift/status/{model_id}` — is reference registered?
- `POST /drift/check` — `{ window: "recent_30d"|"catalog_drift"|"custom" }` — per-feature PSI + segment-membership churn + overall severity
- `GET  /drift/retrain_rule` — current rule
- `POST /drift/retrain_rule` — Phase 13 deliverable; signals + thresholds + duration + human-in-the-loop

## Error taxonomy

- `404` — unknown version / customer_id not on file
- `409` — illegal stage transition (names the legal set)
- `422` — unknown algorithm / unknown cold-start strategy / weights don't sum to 1.0 / two clusters got the same action
