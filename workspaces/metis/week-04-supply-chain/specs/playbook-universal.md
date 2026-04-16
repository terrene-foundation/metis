# Universal ML Decision Playbook — 14 Phases (cross-index)

The 14-phase Universal ML Decision Playbook is authored across three sibling specs. This file is a cross-index so `PLAYBOOK.md` (the generated student-facing view) can be assembled from phase-scoped sources without loading any single oversized file.

| Phases | Sprint                 | Detail spec                    | Theme                                      |
| ------ | ---------------------- | ------------------------------ | ------------------------------------------ |
| 1–9    | Sprint 1 + Close block | `playbook-phases-sml.md`       | Supervised ML: Frame → Codify              |
| 10–12  | Sprint 2               | `playbook-phases-prescribe.md` | Prescriptive / Optimization                |
| 13–14  | Sprint 3 + Week 7      | `playbook-phases-mlops.md`     | MLOps: drift monitoring, fairness (Week 7) |

`PLAYBOOK.md` is a generated view that concatenates the three detail files in phase order and injects the summary table below. When a phase's truth changes, update the relevant detail spec; `_index.md` and `PLAYBOOK.md` regenerate automatically.

## Week 4 phase membership

Week 4 runs phases 1, 2, 4, 5, 6, 7, 8 in Sprint 1, phases 10, 11, 12 in Sprint 2, phase 13 in Sprint 3, and phase 9 in the Close block. Phase 3 is folded into Phase 2 for Week 4. Phase 14 is deferred to Week 7. The Playbook itself retains all 14 phases so Weeks 5–8 can re-use any combination.

## Phase summary table

| #   | Phase                | Sprint  | Detail spec                    | Artefact                                                                  | Rubric dimensions pressured       |
| --- | -------------------- | ------- | ------------------------------ | ------------------------------------------------------------------------- | --------------------------------- |
| 1   | Frame                | S1      | `playbook-phases-sml.md`       | `journal/phase_1_frame.md`                                                | Harm framing, metric-cost linkage |
| 2   | Data audit + feat    | S1      | `playbook-phases-sml.md`       | `journal/phase_2_data_audit.md`                                           | Trade-off honesty                 |
| 3   | (folded into 2)      | —       | `playbook-phases-sml.md`       | (in phase 2)                                                              | —                                 |
| 4   | Candidates           | S1      | `playbook-phases-sml.md`       | `data/leaderboard.json` + `data/leaderboard_prebaked.json`                | (no journal — decision in 5)      |
| 5   | Implications         | S1 + S3 | `playbook-phases-sml.md`       | `journal/phase_5_model_selection.md` + `phase_5_postdrift.md`             | Trade-off honesty, reversal       |
| 6   | Metric + threshold   | S1 + S3 | `playbook-phases-sml.md`       | `journal/phase_6_metric_threshold.md` + `phase_6_postdrift.md`            | Metric-cost linkage, reversal     |
| 7   | Red-team (AI Verify) | S1 + S3 | `playbook-phases-sml.md`       | `journal/phase_7_red_team.md`                                             | All 5 dimensions                  |
| 8   | Deployment gate      | S1 + S2 | `playbook-phases-sml.md`       | `journal/phase_8_gate.md` + `phase_8_postunion.md` + ModelRegistry record | Reversal, constraint              |
| 9   | Codify               | Close   | `playbook-phases-sml.md`       | `journal/phase_9_codify.md` + `PLAYBOOK.md` delta                         | (meta — not scored on rubric)     |
| 10  | Objective            | S2      | `playbook-phases-prescribe.md` | `journal/phase_10_objective.md`                                           | Metric-cost linkage, trade-off    |
| 11  | Constraints          | S2 × 2  | `playbook-phases-prescribe.md` | `journal/phase_11_constraints.md` + `phase_11_postunion.md`               | Constraint classification         |
| 12  | Solver acceptance    | S2 × 2  | `playbook-phases-prescribe.md` | `data/route_plan_*.json` + `journal/phase_12_solver.md` + `_postunion.md` | Trade-off honesty, constraint     |
| 13  | Drift triggers       | S3      | `playbook-phases-mlops.md`     | `data/drift_report.json` + `journal/phase_13_retrain.md`                  | Reversal condition                |
| 14  | Fairness             | Week 7  | `playbook-phases-mlops.md`     | (deferred)                                                                | —                                 |

## Open questions

None. Red-team cycle resolved every fabricated API (AutoMLEngine constructor, DriftMonitor severity, FeatureStore.ingest, EvalSpec.cv_strategy, model_version_id derivation) against kailash-ml source. See `wiring-contracts.md` for the consolidated API-truth table; see `canonical-values.md` for the canonical enums.
