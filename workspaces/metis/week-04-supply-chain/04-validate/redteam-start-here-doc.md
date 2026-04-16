# Red-Team Report — START_HERE.md (Week 4 entrypoint doc)

**Date**: 2026-04-16
**Target**: `workspaces/metis/week-04-supply-chain/START_HERE.md`
**Reviewer**: `reviewer` agent

**Finding counts**: CRITICAL 7 · HIGH 13 · MEDIUM 12 · LOW 6

## Status of each finding

| ID     | Severity | Finding                                                                                                                               | Status                                                                 |
| ------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| C1     | CRITICAL | ExperimentTracker → MLflow export uses `MlflowFormatWriter`, not a tracker method                                                     | Partially addressed — needs explicit `MlflowFormatWriter` flow in §3.7 |
| C2     | CRITICAL | AutoMLEngine construction uses `AutoMLConfig` dataclass + `feature_store`/`model_registry` dependencies; kwarg-style prompt was wrong | **FIXED** in §3.5 prompt template                                      |
| C3     | CRITICAL | ModelRegistry transitions are a table, not a linear chain                                                                             | **FIXED** — transition table added                                     |
| C4     | CRITICAL | `InferenceServer` missing but `/forecast/predict` endpoint claimed — orphan risk                                                      | **FIXED** — InferenceServer added to component table                   |
| C5     | CRITICAL | `TrainingPipeline`/`AutoMLEngine` require `FeatureStore` ingestion first                                                              | **FIXED** — Sprint 1 prompt now starts with `fs.ingest(...)`           |
| C6     | CRITICAL | Product-grade rubric gameable with stub 200s (auto-40%)                                                                               | **DEFERRED TO /analyze** — needs structural redesign                   |
| C7     | CRITICAL | 50+50+35 min for 13 phases mathematically impossible                                                                                  | **DEFERRED TO /analyze** — needs time rebudget                         |
| H1     | HIGH     | AI Verify framework (Transparency, Fairness, Robustness, Safety) from Week 4 deck is missing                                          | **DEFERRED TO /analyze** — scope decision                              |
| H2     | HIGH     | MLflow experimentation discipline mislabeled                                                                                          | **FIXED** — ExperimentTracker framed as MLflow-compatible              |
| H3     | HIGH     | `auto_approve=False` called "trust-plane/execution-plane split" — misuses CARE terminology                                            | **FIXED** — reworded to "decision authority"                           |
| H4     | HIGH     | Phase 13 prompt embeds `if X > Y trigger retrain` — violates agent-reasoning.md                                                       | **FIXED** — reframed as "signals+thresholds for operator monitoring"   |
| H5     | HIGH     | Phases 2/3/7 prompts lack grounding numbers — produce generic output                                                                  | PENDING — add grounding to prompt templates                            |
| H6     | HIGH     | `compare_runs` method existence unverified                                                                                            | VERIFIED — exists per SKILL.md                                         |
| H7     | HIGH     | DriftMonitor requires `set_reference_data` before `check_drift`                                                                       | **FIXED** — Phase 13 prompt now includes step                          |
| H8     | HIGH     | "auto-retrain trigger rules" was an overclaim                                                                                         | **FIXED** — downgraded to "severity + human-readable recommendations"  |
| H9     | HIGH     | "prompt-typist" language violates communication.md                                                                                    | **FIXED** — reworded to plain language                                 |
| H10    | HIGH     | Rubric 0-2-4 levels lack worked examples                                                                                              | PENDING — needs per-dimension examples                                 |
| H11    | HIGH     | "Quantifies asymmetry" scoring ambiguity                                                                                              | PENDING — needs worked example from §2 numbers                         |
| H12    | HIGH     | Sprint-2 scenario injection — re-run 11 AND 12 not spelled out                                                                        | PENDING                                                                |
| H13    | HIGH     | No escape hatch when `[xgb]` extra missing                                                                                            | PENDING — add to §8 pitfalls                                           |
| M1–M12 | MEDIUM   | Various scoping, orphan mentions, placement issues                                                                                    | **DEFERRED TO /analyze**                                               |
| L1–L6  | LOW      | Tone, capitalization, attribution, timestamps                                                                                         | PENDING                                                                |

## Inputs for `/analyze`

The following issues require structural redesign of the workshop plan, not spot fixes to the doc:

### Structural Issue 1: Time budget

The sprints are budgeted 50+50+35 min for phases distributed:

- Sprint 1: phases 1-9 (9 phases in 50 min = 5.5 min/phase)
- Sprint 2: phases 10-12 + re-run 8 (4 phases in 50 min)
- Sprint 3: phase 13 + re-run 5+6 (3 phases in 35 min)

Each phase requires: student prompts → Claude Code executes → student reads Viewer → student journals → student moves on. A single AutoMLEngine run (Bayesian, 30 trials, 5 families, time-series CV) will exceed 3 minutes wall-clock alone.

**Options**:

- **A**: Cut phases aggressively. Sprint 1 = phases 1, 4, 5, 6, 8 only (drop 2, 3, 7, 9). Drop 9 entirely; move codify to end-of-class block.
- **B**: Pre-bake leaderboard so students critique an existing run instead of waiting on AutoML.
- **C**: Extend total to 4.5 hours.
- **D**: Shrink AutoML scope (10 trials instead of 30; 3 families instead of 5).

### Structural Issue 2: Product grade gaming

Current rubric: 5 endpoint checks × 20% = 100% of product grade (40% of total). Stub 200s pass. A student who ships `{"status": "ok"}` everywhere gets 40% + any journal score.

**Required** (from `zero-tolerance.md` Rule 2): each endpoint must assert non-trivial contracts:

- `/forecast/train` → must have a corresponding ExperimentTracker run ID
- `/forecast/compare` → must return ≥3 runs with distinct params
- `/forecast/predict` → must cite the ModelRegistry version used
- `/optimize/solve` → must return a plan where solver reports feasibility + optimality gap
- `/drift/check` → must return at least one statistical test result + severity

### Structural Issue 3: AI Verify framework

The Week 4 deck covers AI Verify's 4 dimensions (Transparency, Fairness, Robustness, Safety) as a "Gate 3 before deployment" concept. The current doc defers Fairness entirely to Week 7 and does not cover Transparency/Robustness/Safety at all.

**Options**:

- **A**: Expand Phase 7 (red-team) to cover Transparency + Robustness + Safety (defer Fairness to Week 7). These three map naturally onto regression/optimization models.
- **B**: Introduce a new Phase 7.5 "AI Verify screen" between red-team and deployment gate.
- **C**: Keep out entirely; Week 4 becomes pure optimization + MLOps; AI Verify centralized in Week 7 alongside fairness.

### Structural Issue 4: Scaffolded vs. student-build ambiguity

The opening prompt (§9) asks Claude Code to summarize what's scaffolded, but the doc does not specify a canonical list. Claude Code will fabricate one. Students cannot evaluate the summary without a ground-truth scaffold manifest.

**Required**: a `SCAFFOLD_MANIFEST.md` enumerating every pre-built vs. must-build file.

## Remaining tactical fixes (deferrable past /analyze)

- H5, H10, H11, H12, H13 (rubric examples, prompt grounding, pitfalls)
- L1–L6 (tone, metadata, attribution)

These can be folded into the final doc pass after /analyze returns structural recommendations.
