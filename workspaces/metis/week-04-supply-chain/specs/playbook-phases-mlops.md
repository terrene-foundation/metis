# Playbook Phases 13–14 — MLOps (Drift + Fairness)

This spec is the detail authority for phases 13 and 14 of the Universal ML Decision Playbook — Sprint 3's Monitor block, plus the deferred fairness audit. Phases 1–9 live in `playbook-phases-sml.md`; phases 10–12 live in `playbook-phases-prescribe.md`. Cross-index is `playbook-universal.md`.

Each phase specifies: (a) sprints that run it, (b) trust-plane question, (c) prompt template, (d) evaluation checklist, (e) journal schema, (f) common failure modes, (g) the artefact that MUST exist on disk to claim the phase complete.

Trust Plane / Execution Plane capitalisation follows `terrene-naming.md`. Library API references follow kailash-ml source — if SKILL.md disagrees with source, source wins.

---

## Phase 13 — Drift Triggers

- **Sprints**: Sprint 3 (~15 min).
- **Trust-plane question**: When do we retrain? What is the rule?
- **Prompt template**:
  > _"Set up drift monitoring for the forecast model. First make sure the training data is registered as the baseline. Then run a drift check against the post-CNY data that just landed and show me: overall severity, which features shifted most, and what the system recommends. Based on the results, propose the signals and thresholds I should monitor going forward — how much drift before we retrain? Should that be an automatic trigger or should a human review first? Ground the thresholds in the data's actual historical variance, not round numbers."_
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
