# Playbook Phases 13–14 — MLOps (Drift + Fairness)

This spec is the detail authority for phases 13 and 14 of the Universal ML Decision Playbook — Sprint 3's Monitor block, plus the deferred fairness audit. Phases 1–9 live in `playbook-phases-sml.md`; phases 10–12 live in `playbook-phases-prescribe.md`. Cross-index is `playbook-universal.md`.

Each phase specifies: (a) sprints that run it, (b) trust-plane question, (c) prompt template, (d) evaluation checklist, (e) journal schema, (f) common failure modes, (g) the artefact that MUST exist on disk to claim the phase complete.

Trust Plane / Execution Plane capitalisation follows `terrene-naming.md`. Library API references follow kailash-ml source — if SKILL.md disagrees with source, source wins.

---

## Phase 13 — Drift Triggers

- **Sprints**: Sprint 3 (~15 min).
- **Trust-plane question**: When do we retrain? What is the rule?
- **Prompt template**:
  > _"For model `<model_name>` (the `{name}_v{version}` form used by /forecast/predict), confirm `DriftMonitor.set_reference_data(model_name, reference_data, feature_columns)` has been called on the training window — the signature is `(model_name: str, reference_data: pl.DataFrame, feature_columns: list[str])`, positional `model_name`, NOT `(model_id, reference_df)`. The `/forecast/train` route calls `drift_wiring.wire(model_name, reference_df, feature_columns)` synchronously before returning; verify by polling `GET /drift/status/<model_id>` or checking `.preflight.json.drift_wiring: true`. Then call `DriftMonitor.check_drift(model_name, current_data)` against `data/scenarios/week78_drift.json`. From `overall_severity` (3-value: `"none" | "moderate" | "severe"` — the library never emits `"low"`) + per-feature `FeatureDriftResult` (psi + ks_statistic + ks_pvalue) + recommendations, propose the signals and thresholds the human operator should monitor: 7-day rolling MAPE, feature-distribution PSI, actual-vs-predicted bias. Show the historical variance of each signal so the thresholds are grounded in data, not guesses. Recommend whether the retrain decision should be made by a human reviewer or by a policy the operator pre-approves — justify with Northwind's operational risk tolerance. Do NOT encode `if X > Y trigger retrain` in agent logic — that violates the Playbook's agent-reasoning rule. See `journal/_examples.md` for a 4/4 vs 1/4 pair on exactly this prompt."_
- **Evaluation checklist**:
  - [ ] `set_reference_data` confirmed active via `GET /drift/status/<model_id>` returning `reference_set: true` (or `.preflight.json.drift_wiring: true`); student must cite the verification in the journal.
  - [ ] `check_drift` output surfaced — per-feature `ks` and `psi` statistics (the two tests kailash-ml emits) + `overall_severity` (3-value enum) + recommendations.
  - [ ] Each proposed signal has a threshold grounded in historical variance, not a guess.
  - [ ] Duration window prevents retrain-on-spike (e.g. "sustained 7 days", not "one spike").
  - [ ] Retrain decision stays in Trust Plane — no `if X > Y` encoded as agent logic (see `agent-reasoning.md`).
- **Journal schema**:
  ```
  Phase 13 — Retrain Rule
  Signal(s): ____
  Threshold(s): ____ (historical variance grounding: ____)
  Duration window: ____
  Human-in-the-loop: yes / no (justification: ____)
  ```
- **Common failure modes**:
  - `set_reference_data` not called (F8) — should be prevented by `drift_wiring.wire()` fired synchronously by `/forecast/train`; `/drift/status` is the debug probe. If status shows `reference_set: false`, re-run `/forecast/train` or call `drift_wiring.wire()` manually.
  - Threshold guessed ("15% feels right") with no variance grounding — 1/4 on reversal condition.
  - Agent-reasoning violation: student asks Claude Code to "auto-retrain when MAPE > 15%". The prompt MUST be reframed as "signals and thresholds for operator monitoring". The 4/4 and 1/4 examples in `journal/_examples.md` make the difference concrete.
- **Artefact**: `data/drift_report.json` + `journal/phase_13_retrain.md`.

### DriftMonitor state machine (reference)

```
(no reference)
   │
   │  set_reference_data(model_name, reference_data, feature_columns)
   ▼
(reference_set, window_size=N)
   │
   ├── check_drift(model_name, current_data) → DriftReport (overall_severity ∈ {none, moderate, severe})
   │
   ├── schedule_monitoring(model_name, data_source_fn, interval_seconds)
   │       → background task running check_drift periodically
   │
   └── cancel_monitoring(model_name)
         → stops the background task

set_reference_data(same model_name, new data) updates the stored reference (UPDATE, not
INSERT); the in-memory cache is bounded to 100 references and evicts oldest.
```

---

## Phase 14 — Fairness Audit (DEFERRED TO WEEK 7)

Not run in Week 4. Phase 7 journal entries include a one-line "Fairness audit deferred to Week 7 per Playbook" so the deferral is explicit, not silent. Week 7 (healthcare + credit) is the natural home — protected classes and disparate-impact testing get a full treatment there.

- **Sprints**: none in Week 4.
- **Artefact**: deferred.
