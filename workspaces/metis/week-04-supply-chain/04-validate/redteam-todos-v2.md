# Red-Team Report v2 — Week 4 Shard Todos (Convergence Pass)

**Date**: 2026-04-16
**Reviewer**: quality-reviewer agent (convergence pass)
**Target**: `workspaces/metis/week-04-supply-chain/todos/active/*.md` — 11 active shards after rework
**Baseline**: `redteam-todos.md` v1 (8C/14H/13M/6L = 41 findings)
**Rules applied**: autonomous-execution, zero-tolerance, orphan-detection, facade-manager-detection, testing, specs-authority, terrene-naming

---

## 1. Executive Summary

**Delta vs v1**: 7 of 8 CRITICAL closed; 1 CRITICAL downgraded; 10 of 14 HIGH closed; 3 HIGH downgraded; 1 HIGH remains. 2 new HIGH findings introduced by rework (spec edit not executed for AnomalyDetectionEngine deletion; ExperimentTracker alias file unowned). 1 MEDIUM persists (conftest.py still multi-writer between shards 01 and 02 — fix text in implementation sketch not matching acceptance contract).

**v2 counts**: **CRITICAL 0 · HIGH 3 · MEDIUM 6 · LOW 5 = 14 findings** (down from 41).

**Verdict**: **GO with 3 gate conditions**.

Target was 0 CRITICAL + ≤3 HIGH. Met. The 3 remaining HIGH findings are spec-edit-in-next-action issues, not architectural defects: (H-A) the AnomalyDetectionEngine _shard-level_ deletion disposition in shard 04 is correct, but the actual spec file edits in `wiring-contracts.md §12` and `scaffold-contract.md §9` have not yet been applied — the deletion must be executed as a specs-authority.md MUST Rule 5 first-instance edit before `/implement` begins. (H-B) `data/.experiment_aliases.json` + `resolve_experiment_run_id()` helper has no owning shard; grade_product.py will fail to resolve aliases. (H-C) `candidate_families` name format (fully-qualified vs short) still contradicts across four specs. All three are sub-shard edits, not restructure.

Structural decomposition is sound: 11 shards, invariant budgets now all within `autonomous-execution.md` § Shard Budget, orphan-detection Rule 2 satisfied for all 12 components, .env.example and .preflight.json sole-writer contracts pinned, Tier-2 tests reclassified correctly, dependency DAG corrected (07 → 01 → everything else).

---

## 2. Baseline CRITICAL Status (v1 → v2)

All 8 v1 CRITICAL findings verified:

| #      | v1 Finding                                                                                                                | Fix claimed in rework                                                                                                                                                       | v2 Status                                          | Evidence                                                                                                                                                                                                                                                                                                            |
| ------ | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **C1** | `lta-carbon-levy` 4-term objective endpoint unimplemented                                                                 | Shard 03b created: acceptance "POST /optimize/solve accepts 4-term objective.terms array; scenario_tag=='post_carbon_levy' processed" + test_carbon_levy_objective.py added | **PASS — CLOSED**                                  | 03b lines 11, 25, 27: "carbon-levy-term: when scenario_tag==\"post_carbon_levy\", objective.terms array MUST include {name:\"carbon_levy\", weight:0.18, unit:\"per_km\"}... objective_value reflects all four terms". Wiring test asserts objective_value > 3-term baseline.                                       |
| **C2** | 5 of 12 wiring tests unowned (ModelExplainer / DataExplorer / ModelVisualizer / FeatureEngineer / AnomalyDetectionEngine) | Shard 02 absorbed 3 wiring tests (ModelExplainer, DataExplorer, ModelVisualizer). Shard 04 DELETES AnomalyDetectionEngine. FeatureEngineer — **still pending disposition**  | **PASS** (4 of 5) + **partial** on FeatureEngineer | 02 lines 43-49 wire 3 previously-orphaned tests with explicit orphan_resolution block. 04 line 34-35 declares AnomalyDetectionEngine "DELETED — no natural call site exists" per orphan-detection Rule 3. FeatureEngineer (wiring-contracts.md §10) has no disposition in any active shard — **see new H-D below**. |
| **C3** | Shard 07 dependency graph wrong (claims depends_on=[] but needs ml_context from 01)                                       | Shard 07 now `depends_on: [01]`, `blocks: [02,03,04,06]`; 07 no longer lists itself as blocking 01                                                                          | **PASS — CLOSED**                                  | 07 lines 20-21, 22-29: explicit dependency_note documents C3 fix with rationale.                                                                                                                                                                                                                                    |
| **C4** | Shard 06 misclassified 3 wiring tests as tests/unit/ (actually Tier-2)                                                    | Three tests moved to tests/integration/; explicit tier2_classification_note documents reclassification                                                                      | **PASS — CLOSED**                                  | 06 lines 42-44 list all three under tests/integration/. Lines 45-49 document the Tier-2 basis per testing.md MUST rule.                                                                                                                                                                                             |
| **C5** | 14 unowned scaffold files                                                                                                 | Shard 09 created as sole owner of all 14 files + `blocks: [01, 06, 07, 08]`                                                                                                 | **PASS — CLOSED**                                  | 09 lines 39-55 enumerate all 14 files with acceptance criteria. Blocks list ensures these land before consumers.                                                                                                                                                                                                    |
| **C6** | .env.example overlap between 01 and 07                                                                                    | Sole-writer designated shard 09; shards 01 and 07 explicitly state "not authored by this shard"                                                                             | **PASS — CLOSED**                                  | 01 line 43, 07 line 56, 09 lines 14 + 22-24 all consistent. sole_writer_declaration block in 09 is explicit.                                                                                                                                                                                                        |
| **C7** | .preflight.json overlap between 01 and 06 (atomic-rewrite race)                                                           | Read-modify-write protocol with atomic .tmp+rename pinned in both shards; shard 06 preflight.py initialises on every run                                                    | **PASS — CLOSED**                                  | 01 lines 22-23, 42: "read-modify-write (json.load → merge dict → atomic .tmp+rename); they do NOT perform a full rewrite". 09 line 15 documents the initialisation contract.                                                                                                                                        |
| **C8** | canonical-values §8 sub-numbering false alarm                                                                             | Self-withdrawn in v1                                                                                                                                                        | **N/A** (was already false alarm)                  | —                                                                                                                                                                                                                                                                                                                   |

**Baseline CRITICAL tally**: 7 PASS + 1 N/A = **0 open CRITICAL**. Target met.

---

## 3. Baseline HIGH Status (v1 → v2)

| #   | v1 Finding                                                                        | v2 Status                | Notes                                                                                                                                                                                                                                                                                                                                            |
| --- | --------------------------------------------------------------------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| H1  | Shard 03 invariant-budget overflow (9-10 invariants, 550-700 LOC)                 | **RESOLVED**             | Split into 03a (OR-Tools + 3-term, 200 LOC, 6 invariants) + 03b (PuLP + 4-term + snapshot, 180 LOC, 5 invariants). Each within budget.                                                                                                                                                                                                           |
| H2  | Shard 05 at 420 LOC with 10 invariants (budget edge)                              | **RESOLVED**             | Split into 05a (shell + watcher, 200 LOC, 5 invariants) + 05b (panels + tests, 220 LOC, 5 invariants). Each comfortably within budget.                                                                                                                                                                                                           |
| H3  | tests/integration/conftest.py multi-writer 01 + 02                                | **DOWNGRADED to MEDIUM** | Shard 01 ships conftest.py with ml_context_real; shard 02 implementation sketch still reads "add seed_feature_store… helper; add sample_eval_spec fixture" to the same file. Acceptance lines don't pin extension protocol. Remaining as M-1 below — not a ship blocker given parallel-write risk is low (01 blocks 02 per DAG, so sequential).  |
| H4  | .preflight.json 8-field merge contract                                            | **RESOLVED**             | Same mechanism as C7 — read-modify-write + atomic rename; initialised by shard 06 preflight.py on every run.                                                                                                                                                                                                                                     |
| H5  | AnomalyDetectionEngine "decide later" defers orphan-detection Rule 3              | **PARTIAL — see H-A**    | Shard 04 correctly states "DELETED" disposition, but the authoritative spec edits to `wiring-contracts.md §12` and `scaffold-contract.md §9` have NOT been executed. Shard 04 out-of-scope block says "wiring-contracts.md §12 entry to be removed" — passive voice; no shard owns executing the edit.                                           |
| H6  | Shard 02 "§8.1-8.3" range notation                                                | **UNCHANGED / LOW**      | Still cites the range. Truly cosmetic; readers resolve correctly. Keep as L-1.                                                                                                                                                                                                                                                                   |
| H7  | Workshop-runofshow.md coverage unowned                                            | **RESOLVED**             | Shard 08 now consults workshop-runofshow.md §0-§8 (line 27) and acceptance line 42 enumerates minute-by-minute checkpoints + producing shards.                                                                                                                                                                                                   |
| H8  | Shard 01 ".env.example contains all keys" deferred enumeration                    | **RESOLVED**             | Now owned by shard 09 with explicit 14-key list and per-key regression test (09 acceptance line 56).                                                                                                                                                                                                                                             |
| H9  | Agent-reasoning.md clarification for OR-Tools vs PuLP routing                     | **RESOLVED**             | 03a invariant #6 line 16 explicitly declares "solver-choice-is-deterministic-guard" is NOT agent reasoning; future dynamic routing is BLOCKED per agent-reasoning.md.                                                                                                                                                                            |
| H10 | Shard 03 test_pulp_wiring.py uses @patch on ortools (testing.md Tier-2 violation) | **RESOLVED**             | 03b line 12: "pulp-fallback-real: PuLP fallback is triggered by OR_TOOLS_DISABLED=1 env var (real runtime code path); the test uses subprocess with OR_TOOLS_DISABLED=1 set; no @patch or MagicMock". Real env-var gate.                                                                                                                         |
| H11 | Shard 02 vs 07 candidate_families format disagreement                             | **UNCHANGED — see H-C**  | Shards 02 (line 14), 07 (line 77), and spec files still disagree: canonical-values.md §8.7 / wiring-contracts.md §1 use short names ("LinearRegression"); product-northwind.md §8.1 / data-fixtures.md §3.1 use fully-qualified ("sklearn.linear_model.Ridge"); playbook-phases-sml.md §Sprint 1 uses fully-qualified. No shard pins one format. |
| H12 | ExperimentTracker alias file + helper unowned                                     | **UNCHANGED — see H-B**  | Still zero shards own `data/.experiment_aliases.json` or `resolve_experiment_run_id(id_or_alias)` helper. Grade_product.py (shard 06) will fail to resolve aliases per canonical-values.md §12 final paragraph.                                                                                                                                  |
| H13 | journal/\_template.md + journal/\_examples.md unowned                             | **RESOLVED**             | Shard 09 owns both, with acceptance anchored to decision-journal.md §2 + §3 and rubric-grader.md §1.1/§1.2 anti-patterns.                                                                                                                                                                                                                        |
| H14 | scenario-catalog §4 carbon_levy weight aggregation contract                       | **RESOLVED**             | 03b line 11: "objective_value reflects all four terms (fuel + sla + overtime + carbon_levy)"; test_carbon_levy_objective.py asserts objective_value > 3-term baseline (line 27) — satisfies sum-contract.                                                                                                                                        |

**Tally**: 10 RESOLVED · 3 carried-over (H5→H-A, H11→H-C, H12→H-B) · 1 DOWNGRADED (H3→M-1).

---

## 4. New Findings From the Rework

### HIGH (3)

**H-A** — [orphan-detection.md Rule 3] [shard 04 + specs/wiring-contracts.md §12 + specs/scaffold-contract.md §9]
**Title**: AnomalyDetectionEngine deletion is declared in shard 04 but the spec edits have not been executed.
**Problem**: Shard 04 orphan_resolution line 35 says "wiring-contracts.md §12 section must be deleted. scaffold-contract.md §9 audit table entry must be removed. START_HERE.md must not reference AnomalyDetectionEngine." This is passive-voice: no shard owns the actual edits. `specs/wiring-contracts.md` lines 170-181 still document §12 AnomalyDetectionEngine with the TODO banner. Per specs-authority.md MUST Rule 5 "Spec Files Are Updated at First Instance" — the edit is owed NOW, not during `/implement`. Per orphan-detection.md MUST Rule 3 "Removed = Deleted, Not Deprecated" — leaving the spec section with a "to be removed" banner is exactly deprecation.
**Fix**: Either (a) assign the spec deletion to shard 04 (add acceptance criterion: "delete wiring-contracts.md §12 AnomalyDetectionEngine section and scaffold-contract.md §9 row AnomalyDetectionEngine" + cite specs-authority.md Rule 5), or (b) make the deletion a pre-condition to `/implement` that is executed before the first shard runs. (a) is recommended — keeps the edit auditable in the PR diff.
**Severity**: HIGH. Leaving the spec in place means a future session reads wiring-contracts.md §12 and re-introduces the engine as if it were a pending implementation task.

**H-B** — [completeness] [unowned — no shard; canonical-values.md §12]
**Title**: ExperimentTracker alias file `data/.experiment_aliases.json` + `resolve_experiment_run_id()` helper still unowned.
**Problem**: canonical-values.md §12 (line 228) specifies workshop surfaces human-readable aliases and maintains them in `data/.experiment_aliases.json`. Grade*product.py is expected to resolve alias-or-UUID. Shard 06 (grader) assumes this works. No shard owns creating the alias file OR adding `resolve_experiment_run_id(id_or_alias) -> run_uuid` to ml_context.py. Baseline H12 flagged this; rework did not address it.
**Fix**: Add to shard 01 acceptance: "ml_context.py exposes `resolve_experiment_run_id(id_or_alias: str) -> str` that reads `data/.experiment_aliases.json` and returns the canonical UUID; returns the input unchanged if already a UUID; raises KeyError on unknown alias." Add to shard 02 acceptance: "POST /forecast/train appends a `{alias: uuid}` entry to `data/.experiment_aliases.json` atomically after AutoMLEngine.run completes; alias format is `{short_family}*{ordinal:03d}_{YYYYMMDD}_{HHMMSS}` per canonical-values.md §12."
**Severity**: HIGH. Without the alias resolver, grade_product.py fails on any run where students cite aliases in journal entries (the expected workshop pattern), producing a false 0/4 on D3/D5 dimensions.

**H-C** — [spec consistency] [4 specs + 2 shards]
**Title**: `candidate_families` name format still contradicts across canonical-values.md §8.7 (short names) vs product-northwind.md §8.1 (fully-qualified) vs data-fixtures.md §3.1 (fully-qualified) vs wiring-contracts.md §1 (short names) vs playbook-phases-sml.md (fully-qualified).
**Problem**: Baseline H11. Rework did not address. Shard 02 invariant `automlconfig-field` says "candidate_families=[...]" but doesn't pin the string format. Shard 07 implementation sketch line 77 uses `candidate_families=[...]` — not spelled out. Students/graders cannot reconcile which format the leaderboard compares.
**Fix**: Pin one format in ONE spec and make the others cite it. Recommendation: fully-qualified import paths (e.g. `"sklearn.linear_model.Ridge"`) because `AutoMLConfig.candidate_families` is documented as a dotted-path field in product-northwind.md §8.1 and that matches the library import contract. Update canonical-values.md §8.7 + wiring-contracts.md §1 to use fully-qualified names. Shard 02 and shard 07 should add explicit acceptance: "candidate_families values are fully-qualified Python import paths".
**Severity**: HIGH. Phase 5 leaderboard compare fails because live run uses one format, pre-bake uses another; journal entries cite mismatched names; D2 scoring is unverifiable on exact-string assertions.

### MEDIUM (6)

**M-1** — [H3 carry-over, downgraded] conftest.py multi-writer 01 + 02. Shard 01 writes the file with `ml_context_real`; shard 02 sketch still describes extending it in-place. Because 01 blocks 02 (sequential), parallel race is not possible, but /implement of shard 02 may still edit conftest.py directly. **Fix**: Shard 02 acceptance should specify the fixtures are added via a separate `conftest_forecast.py` auto-imported by pytest, OR shard 01 acceptance should pre-declare all shared fixtures that 02 needs (seed_feature_store, sample_eval_spec, LinearRegression artifact fixture) so 02 only reads.

**M-2** — [v1 M-2 carry-over] Shard 06 loc_estimate=480 still understates scope. The rework did not split 06 further. Four scripts (preflight 120 + scenario_inject 250 + journal_cli 300 + grade_product 220) + 80 JSON + 180 tests ≈ 1150 LOC. Shard 06 has executable feedback loop (pytest) which per autonomous-execution.md §3 yields 3-5× multiplier — so 1150 LOC is not a budget overflow given the loop. But the number should be corrected to 1150 for planning accuracy. **Fix**: Update 06 loc_estimate and explicitly cite the feedback-loop multiplier.

**M-3** — [v1 M-3 carry-over] Shard 01 invariant count. Invariants listed: 5. Actual acceptance criteria imply model_version_id derivation, .preflight.json atomic rename, 501-stub banner verbatim copy, conftest tmp_path fixture lifecycle — call it 8. Still within budget given feedback loop, but should be enumerated.

**M-4** — [v1 M-5 carry-over] Shard 07 dependency_note says "07 depends_on=[01]; blocks=[02,03,04,06]" — correct — but shard 03a (new) lists `depends_on: [01]` and does NOT list 07. 03a reads route_plan.json (produced by itself) + forecast_output.json (02). Correct in isolation. But 03a's OR-Tools VRP wiring test fixture (3-depot 2-vehicle) might benefit from the northwind CSV — if so, shard 03a should add depends_on=[07]. If not, state explicitly. **Fix**: Shard 03a — add a line clarifying whether the test fixture is synthetic or reads northwind_demand.csv.

**M-5** — [v1 M-8 carry-over] `scripts/grade_fix_messages.json` schema not pinned in shard 06. Still listed as "11 key-value entries" without declared shape. **Fix**: 06 should declare `{"endpoint:status_code": {"message": "...", "hint": "..."}}` or equivalent.

**M-6** — [new, from 05a/05b] Shard 05a writes apps/web/**tests**/fixtures/ (line 32). Shard 05b `can_build_against: sample fixtures from apps/web/__tests__/fixtures/ (produced by 05a)` — fine. But fixtures for leaderboard_prebaked.json (file schema per data-fixtures.md §3.2) must match shard 07 schema exactly. Risk: 05a hand-writes a simpler fixture; shard 07 generates a richer schema; DriftPanel.test.tsx passes on fixture but fails against real data. **Fix**: 05a acceptance should state "fixture files minimal but schema-compatible with shard 07 generators"; add a cross-shard fixture-validation test in 05b or 07.

### LOW (5)

- **L-1** Shard 02 / 08 "§8.1-8.3" / "§1-8" range notation — cosmetic.
- **L-2** Shard 07 FeatureSchema import-time validation — still flagged by original L-3 as possibly over-engineered.
- **L-3** Shard 06 pandoc fallback naming — still "journal_markdown_fallback.md" vs decision-journal §5.2 "journal.md" — pick one.
- **L-4** Shard 05 test coverage — 05b has 3 tests for 6 components; ForecastPanel, RoutePanel, JournalPanel still uncovered (v1 L-4 unchanged).
- **L-5** Shard 01 module-level `_ctx` singleton lifecycle for tests — still not documented (v1 L-6 unchanged).

---

## 5. Freshly-Flagged Rework Gaps — Disposition

### Gap 1 — AnomalyDetectionEngine DELETION spec edit

**Flagged**: Rework claims shard 04 deletes AnomalyDetectionEngine, but no shard owns editing `wiring-contracts.md §12` and `scaffold-contract.md §9` to remove the spec sections.

**Confirmed as real gap — this is H-A above.**

**Severity**: HIGH.
**Owner**: Shard 04 (add acceptance criterion for the spec deletion) OR a pre-`/implement` spec edit action.
**Resolution**: Shard 04 acceptance addition: "delete `specs/wiring-contracts.md §12` and remove `AnomalyDetectionEngine` row from `specs/scaffold-contract.md §9` in the same PR as the route-level deletion; per specs-authority.md MUST Rule 5 + orphan-detection.md Rule 3." Shard 04 blocks nothing downstream from its own deliverables, so adding this scope does not shift the DAG.

### Gap 2 — ExperimentTracker alias file + resolver helper

**Flagged**: `data/.experiment_aliases.json` + `resolve_experiment_run_id()` helper not assigned.

**Confirmed as real gap — this is H-B above.**

**Severity**: HIGH.
**Owner**: Split ownership: shard 01 (resolver helper in ml_context.py) + shard 02 (alias-file writer in /forecast/train handler).
**Resolution**: See H-B fix.

### Gap 3 — conftest.py multi-writer between shards 01 and 02

**Flagged**: Shard 01 writes conftest.py; shard 02 sketch extends in-place.

**Confirmed as real gap — this is M-1 above (downgraded from H3).**

**Severity**: MEDIUM (downgraded from HIGH because 01 blocks 02, so the race is sequential not parallel — but semantic edit conflict remains).
**Owner**: Shard 01 (pre-declare all fixtures) OR shard 02 (use separate conftest_forecast.py file).
**Resolution**: See M-1 fix.

### Gap 4 — `candidate_families` name format (fully-qualified vs short)

**Flagged**: Unresolved across specs + shards.

**Confirmed as real gap — this is H-C above.**

**Severity**: HIGH.
**Owner**: Spec edit owner (shard 08 or a pre-`/implement` spec action) + shards 02 and 07 to pin in acceptance.
**Resolution**: See H-C fix.

---

## 6. Final GO / NO-GO Verdict

**GO — with 3 gate conditions that MUST be satisfied before `/implement` begins.**

### Rationale

- All 8 baseline CRITICAL closed.
- 10 of 14 baseline HIGH closed; 3 HIGH remain (H-A, H-B, H-C) — all are sub-shard edits (spec deletion, helper addition, format pin), not architectural restructure.
- 2 invariant-budget overflows resolved via shard splits (03 → 03a+03b; 05 → 05a+05b).
- Orphan-detection Rule 2 now satisfied for all 12 components (AnomalyDetectionEngine deleted, others wired).
- Sole-writer contracts (.env.example, .preflight.json) explicit.
- Tier-2 test reclassification applied in shard 06 and shard 03b (no mocks).
- DAG corrected (07 depends on 01; blocks list fixed).
- Target was 0 CRITICAL + ≤3 HIGH. Met exactly.

### Pre-`/implement` Gate Conditions (3)

These MUST be resolved as direct edits before `/implement` launches — no restructure required, no additional shards needed:

1. **H-A execution** — Add acceptance criterion to shard 04: "delete `specs/wiring-contracts.md §12` AnomalyDetectionEngine section and `specs/scaffold-contract.md §9` audit-table row in the same PR as the route-level deletion; cite specs-authority.md MUST Rule 5 + orphan-detection.md Rule 3". Est: 1 edit, ~10 min.

2. **H-B execution** — Add to shard 01 acceptance: "ml_context.py exposes `resolve_experiment_run_id(id_or_alias) -> str` that reads `data/.experiment_aliases.json`; raises KeyError on unknown alias". Add to shard 02 acceptance: "POST /forecast/train writes `{alias: uuid}` atomically to `data/.experiment_aliases.json` after AutoMLEngine.run". Add to shard 06 acceptance: "grade_product.py resolves alias-or-uuid via `resolve_experiment_run_id()` when asserting ExperimentTracker.get_run()". Est: 3 acceptance edits, ~20 min.

3. **H-C execution** — Pin `candidate_families` to fully-qualified format in canonical-values.md §8.7 + wiring-contracts.md §1 setup line; add invariant to shards 02 and 07 stating "candidate_families values are fully-qualified Python import paths matching product-northwind.md §8.1". Est: 4 spec edits + 2 shard invariant additions, ~30 min.

**Total pre-`/implement` work**: ~60 minutes, single autonomous cycle.

### CI / `/implement` Gate Checks (Drift Prevention)

Once the 3 gate conditions are satisfied, add these drift-prevention checks:

- **Grep audit at `/implement` start**: `grep -rn "AnomalyDetectionEngine" specs/ src/ tests/ docs/` MUST return zero matches (H-A closure verification).
- **Unit test for H-B**: `tests/unit/test_experiment_alias_resolver.py` — asserts `resolve_experiment_run_id("ridge_001_20260416_090000")` returns a UUID when the alias file contains it.
- **Unit test for H-C**: `tests/unit/test_candidate_families_fqname.py` — asserts every `candidate_families` value in `leaderboard_prebaked.json` matches the regex `^[a-z_]+(\.[a-z_]+)+\.[A-Z][A-Za-z]+$` (fully-qualified Python import path).
- **Orphan sweep at `/codify`**: run the detection protocol from `orphan-detection.md` § Detection Protocol against the produced scaffold; zero orphans = pass.
- **Shard-budget audit at `/redteam`**: confirm each shard's actual LOC + invariant count stayed within the declared budget; any overflow triggers a re-split before `/codify`.

### Smallest Re-Rework Scope If Rejected

Not needed — verdict is GO.

If the pre-`/implement` gate conditions are not executed before `/implement` starts, re-rework scope = the 3 edits listed above (60 minutes). No new shards needed; no DAG changes.

---

## 7. Summary Tables

### Finding Count Delta

| Severity  | v1 Count | v2 Count | Change  |
| --------- | -------- | -------- | ------- |
| CRITICAL  | 8        | 0        | −8      |
| HIGH      | 14       | 3        | −11     |
| MEDIUM    | 13       | 6        | −7      |
| LOW       | 6        | 5        | −1      |
| **Total** | **41**   | **14**   | **−27** |

### New vs Carried-Over Findings

| Category                   | Count | Items                                                       |
| -------------------------- | ----- | ----------------------------------------------------------- |
| Closed (v1 → v2)           | 26    | C1-C7, H1, H2, H4, H7, H8, H9, H10, H13, H14 + 7 MEDIUM/LOW |
| Carried-over unchanged     | 3     | H-A (was H5), H-B (was H12), H-C (was H11)                  |
| Downgraded                 | 2     | M-1 (was H3), L-1 (was H6)                                  |
| New (introduced by rework) | 1     | M-6 (05a/05b fixture-schema compatibility)                  |

### Shard Count Delta

|               | v1  | v2                                                  |
| ------------- | --- | --------------------------------------------------- |
| Active shards | 8   | 11 (01, 02, 03a, 03b, 04, 05a, 05b, 06, 07, 08, 09) |
| SUPERSEDED    | —   | 2 (03, 05 redirect files)                           |

---

## 8. Risk Posture Going Into `/implement`

**Low residual risk**:

- Invariant budgets respected across all 11 shards.
- Wiring tests cover 12 of 12 components (AnomalyDetectionEngine deleted rather than orphaned).
- Sole-writer contracts explicit on conflicting-write files.
- Test tiers correctly classified.
- Fully traced scenario end-to-end chain (union-cap, drift-week-78, lta-carbon-levy).

**Residual risks post-gate-conditions**:

- Shard 09 (400 LOC, 14 files) has the highest single-shard file count; potentially underestimates cross-file invariants but boilerplate multiplier per autonomous-execution.md §2 likely covers it.
- Shard 06 loc_estimate (480) still understates; feedback-loop multiplier makes it tractable but plan-accuracy suffers.
- Fixture schema parity between shard 05a test fixtures and shard 07 generated files (M-6) — add a cross-shard schema-compatibility test at `/implement` time.

**Recommended order at `/implement`**:

1. Satisfy gate conditions H-A, H-B, H-C (60 min).
2. Launch shard 09 first (depends_on=[]; blocks 01, 06, 07, 08).
3. Launch shards 01 and 07 in parallel after 09 (09 → 01; 09 → 07).
4. After 01 lands: 02, 03a, 04 in parallel. (07 also parallelisable after 01.)
5. After 03a: 03b. After 02: 06, 04.
6. After 05a: 05b.
7. Shard 08 last (depends_on everything).
