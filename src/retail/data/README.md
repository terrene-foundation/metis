# Arcadia Retail — Data Files

Generated 2026-04-23T04:49:03Z by `scripts/generate_data.py` (seed 20260423).

| File | Role | Consumed by |
| --- | --- | --- |
| `arcadia_customers.csv` | 5,000 customers × 14 features | `/segment/*`, `/recommend/*`, `fs_preload` |
| `arcadia_products.csv`  | 400 SKUs × 9 features | `/recommend/*` |
| `arcadia_transactions.csv` | 120,000 txns × 6 features | `/recommend/*`, drift windows |
| `segment_baseline.json` | pre-built K=3 baseline; students critique it | Phase 4 / Phase 5 |
| `segment_candidates.json` | pre-baked k-sweep 2..10 | Phase 4 comparison against live runs |
| `drift_baseline.json` | reference distribution for `DriftMonitor` | Phase 13 |
| `scenarios/pdpa_redline.json` | Sprint 2 injection (Phase 11 re-classification) | scenario_inject.py |
| `scenarios/catalog_drift.json` | Sprint 3 injection (Phase 13 drift) | scenario_inject.py |

**Ground truth the student must NEVER see:**

- `latent_segment` column (7 archetypes) — grader-only.
- `income_tier` column — PDPA proxy leakage surface (Phase 2 / Phase 7 red flag).
- The K-sweep has no dominant silhouette peak: student must defend K in business terms.
