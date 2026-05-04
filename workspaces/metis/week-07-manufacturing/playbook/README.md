<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# The Week 7 Playbook — Navigation

**Version:** 2026-05-04 · **License:** CC BY 4.0

Everything you paste tonight lives in this folder. Open the files in the chronological run order below. Each file is self-contained: paste prompt → signals to check → concept refresher → handoff to the next file.

---

## 0. Two flows

1. **`../START_HERE.md`** — read once before class for the overview (what Week 7 is, the LumenCircuit industrial AI suite, the two planes, the hygiene toolkit, the grading rubric). Start by pasting the opening prompt in §7 to boot the environment.
2. **This folder, file-by-file** — after the environment is booted, open `workflow-01-analyze.md` and follow the `**Next file:**` pointer at the bottom of each file. Don't skip.

---

## 1. Tonight's run order (open these files in order)

The viewer at `http://localhost:3000` auto-refreshes as each phase writes artifacts. Glance at it after every phase; if nothing new rendered, Claude Code described the work instead of running it.

| #   | File                                       | What happens                                                           |
| --- | ------------------------------------------ | ---------------------------------------------------------------------- |
| 1   | `../START_HERE.md` §7 opening prompt       | Boot the backend, viewer, and preflight                                |
| 2   | `workflow-01-analyze.md`                   | Inheritance audit — what the scaffold committed to                     |
| 3   | `workflow-02-todos.md`                     | Tracked plan, one todo per Playbook phase (human gate)                 |
| 4   | `workflow-03-sprint-1-vision-boot.md`      | Boot Sprint 1 · Transfer Learning · See                                |
| 5   | `phase-01-frame.md`                        | Target, population, horizon, cost asymmetry (49:1)                     |
| 6   | `phase-02-data-audit.md`                   | Six-category audit on labelled boards + sensor stream + RL episodes    |
| 7   | `phase-03-features.md`                     | Feature framing — image features + sensor windows + RL state           |
| 8   | `phase-04-candidates.md` (Vision pass)     | 3-arch sweep (ResNet / EfficientNet / ViT)                             |
| 9   | `phase-05-implications.md` (Vision)        | Pick architecture; defend in $ + edge-latency budget                   |
| 10  | `phase-06-metric-threshold.md` (Vision)    | Per-class thresholds × 4 (safety_critical_defect WSH hard floor 0.40)  |
| 11  | `phase-07-redteam.md` (Vision)             | Adversarial / OOD / demographic-skew (line × shift × supplier)         |
| 12  | `phase-08-gate.md` (Vision gate)           | PASS/FAIL, promote to shadow                                           |
| 13  | `workflow-04-sprint-2-predmaint-boot.md`   | Boot Sprint 2 · Time-series ML · Predict                               |
| 14  | `phase-04-candidates.md` (PredMaint)       | Same file — now for LightGBM / LSTM / Survival Forest                  |
| 15  | `phase-05-implications.md` (PredMaint)     | Pick family + prediction window (3/7/14 days)                          |
| 16  | `phase-06-metric-threshold.md` (PredMaint) | Cost-balanced threshold ($12K unplanned vs $1.8K planned)              |
| 17  | `phase-07-redteam.md` (PredMaint)          | Sensor noise / Q4 ramp / per-machine cohort                            |
| 18  | `phase-08-gate.md` (PredMaint gate)        | PASS/FAIL, promote to shadow                                           |
| 19  | `workflow-05-sprint-3-rl-boot.md`          | Boot Sprint 3 · Reinforcement Learning · Optimize                      |
| 20  | `phase-10-objective.md`                    | RL reward function shape (4 weights)                                   |
| 21  | `phase-11-constraints.md` (first pass)     | Hard vs soft (WSH-affecting categories PENDING)                        |
| 22  | `phase-12-acceptance.md` (first pass)      | Solve LP allocator + RL leaderboard accept/redo                        |
| 23  | **MOM/WSH injection fires** (~4:30pm)      | Instructor-triggered — MOM Inspectorate shadow-mode mandate            |
| 24  | `phase-11-constraints.md` (re-run)         | Re-classify WSH-affecting categories as hard-shadow                    |
| 25  | `phase-12-acceptance.md` (re-run)          | Re-solve — quantify compliance shadow price ($/day lost RL gain)       |
| 26  | `workflow-06-sprint-4-agent-mlops-boot.md` | Boot Sprint 4 · Agent + MLOps · Coordinate                             |
| 27  | `phase-13-drift.md`                        | Three retrain rules (vision weekly / sensor daily / RL per-deployment) |
| 28  | `workflow-07-redteam.md`                   | Cross-sprint cascade red-team                                          |
| 29  | `workflow-08-codify.md`                    | Phase 9 Codify — 3 transferable + 2 domain lessons                     |
| —   | End of workshop                            | `/wrapup` writes `.session-notes`                                      |

**Replays are intentional.** Phase-04 through phase-08 are opened TWICE (once Vision in Sprint 1, once PredMaint in Sprint 2). Phase-11 and phase-12 are opened twice (first pass + post-WSH re-run, with the re-run hitting the AGENT autonomy ladder). Each phase file has branched `§1 Tonight-specific` and `§2 Signals` blocks — follow the one that matches your current pass.

**Phase 9 (Codify) is NOT in the run order as `phase-09-codify.md`.** It runs at close via `workflow-08-codify.md`. The `phase-09-codify.md` file is a pointer that explains this.

**Phase 14 (Fairness) is deferred to Week 8 (capstone).** `phase-14-fairness.md` is a deferred stub.

---

## 2. File types

- **`workflow-NN-*.md`** (8 files) — boot one COC-level step (analyze, todos, 4 sprint boots, redteam, codify).
- **`phase-NN-*.md`** (14 files) — run one Playbook ML decision phase. `phase-09` is a pointer, `phase-14` is a deferred stub.

Legacy files `appendix-a-lessons.md` and `appendix-b-dashboard.md` accrete across weeks — they're not part of tonight's run order but `/codify` writes to them at close.

---

## 3. Navigation within every file

Each phase file has 8 self-contained sections:

1. **What this phase decides** — single-sentence framing
2. **The Week 7 lens** — how the phase applies to vision QC / predmaint / RL / agent
3. **Your levers** — the specific decision knobs this phase owns
4. **Paste-ready block for the journal** — fill-in-the-blank text the student copies
5. **Cost anchor** — the dollar number(s) from `specs/business-costs.md`
6. **Hard-floor table** — for safety-affecting phases, the WSH/IPC hard constraint table
7. **Reversal condition** — example signal+threshold+duration triple
8. **Transfer to next project** — how this phase generalises beyond manufacturing

When you're lost, scan §2 (lens) first to re-anchor in Week 7. Section §3 names the levers; §4 is what you paste.

---

## 4. The five Trust Plane decision moments (rubric anchor)

1. **Choose the vision QC base architecture** (Phase 5 Vision) — ResNet-50 / EfficientNet-B0 / ViT-Small, defended against the 80 ms/board edge latency budget
2. **Set the auto-pass confidence threshold per class × 4** (Phase 6 Vision) — defended in $ of (FN $4,200 × FN rate + FP $85 × FP rate); safety_critical_defect HARD-floored at 0.40 per WSH
3. **Choose the predictive-maintenance prediction window** (Phase 5 PredMaint + Phase 11) — 3 / 7 / 14 days, defended in $ of unplanned-stop ($12K) vs planned-maintenance ($1.8K)
4. **Design the RL reward function weights** (Phase 7 RL) — four weights (throughput / defect_cost / energy_cost / safety_penalty); leaderboard MUST show no reward-hacking, zero hard-floor violations across 10,000 episodes
5. **Set the agent autonomy ladder + the WSH safety floor** (Phase 11 + Phase 12) — three modes × four task classes; WSH-affecting categories STRUCTURALLY hard-shadowed when MOM mandate fires; quantify compliance shadow price in $/day

All five are non-negotiable. The rubric (see `../START_HERE.md` §5) scores each phase journal on five dimensions (D1 Harm / D2 Metric→Cost / D3 Trade-off / D4 Constraint / D5 Reversal); the five decision moments are where those dimensions feel teeth.

---

## 5. ML Vocabulary Menu (Week 7 lens)

Use this when CC drops jargon. Each term is grounded in tonight's product.

- **Transfer learning** — frozen ImageNet backbone (ResNet/EfficientNet/ViT) + task-specific head trained on 800 labelled PCBs. Practical default at small-data scale.
- **Time-series ML** — features built from sliding sensor windows (vibration / motor current / head temp / cycle-count). LSTM treats raw sequence; LightGBM uses hand-engineered window features; Survival Forest models time-to-event.
- **Reinforcement learning (RL)** — a policy that chooses an action (±5 °C per zone, ±10 boards/min) given a state (current temps, line speed, board class) to maximise a reward (throughput − defect cost − energy − safety penalty). Tonight's policies are cached deterministic rollouts; the choice is the reward weights.
- **Reward function** — the four-term equation that defines what RL optimises. Get it wrong and the agent reward-hacks (Goodhart's Law).
- **Goodhart's Law** — "When a measure becomes a target, it ceases to be a good measure." If `safety_penalty=0`, the agent runs the line at 90 boards/min, defects triple, equipment crashes.
- **Edge inference** — running the vision classifier on the line camera (Jetson-class) instead of the cloud. 80 ms/board latency budget, $0.001/inference.
- **LLM agent** — an LLM-driven controller with tools (`vision_classify`, `predict_failure`, `suggest_setpoint`, `log_safety_incident`) and an autonomy ladder (shadow / recommend / act).
- **Autonomy ladder** — three modes per task class (vision triage, maintenance scheduling, setpoint adjustment, safety alert). Shadow = recommend-only, human acts. Recommend = agent acts on low-stakes, escalates safety-critical. Act = agent acts within hard-floored envelope.
- **Drift cadence stratification** — three models drift at three speeds. Vision: weekly (equipment + supplier drift). Sensor: daily (calibration + temperature). RL: per-deployment (every policy update).
- **PSI** — Population Stability Index; how much a distribution moved from a registered baseline. Used per-feature in vision and per-token in sensor windows.
- **Hard floor** — regulator-mandated minimum that overrides cost-balanced math. WSH safety-critical class auto-pass minimum 0.40; RL safety_penalty floor; line-speed/temp ceilings under MOM mandate.
- **Shadow price** — marginal $ cost of tightening a constraint by one unit. Used to quantify the MOM/WSH compliance cost in $/day.

---

## 6. Playbook file inventory

| File                                       | Type      | Runs at step | What it contains                                      |
| ------------------------------------------ | --------- | ------------ | ----------------------------------------------------- |
| `workflow-01-analyze.md`                   | Workflow  | 2            | `/analyze` — inheritance audit                        |
| `workflow-02-todos.md`                     | Workflow  | 3            | `/todos` — tracked plan + human gate                  |
| `workflow-03-sprint-1-vision-boot.md`      | Workflow  | 4            | Sprint 1 boot (transfer-learned vision QC)            |
| `workflow-04-sprint-2-predmaint-boot.md`   | Workflow  | 13           | Sprint 2 boot (time-series predictive maintenance)    |
| `workflow-05-sprint-3-rl-boot.md`          | Workflow  | 19           | Sprint 3 boot (RL reflow controller + MOM/WSH inject) |
| `workflow-06-sprint-4-agent-mlops-boot.md` | Workflow  | 26           | Sprint 4 boot (agent + drift × 3)                     |
| `workflow-07-redteam.md`                   | Workflow  | 28           | `/redteam` — cross-sprint cascade stress              |
| `workflow-08-codify.md`                    | Workflow  | 29           | `/codify` — Phase 9 transferable lessons              |
| `phase-01-frame.md`                        | Phase     | 5            | Target / population / horizon / 49:1 asymmetry        |
| `phase-02-data-audit.md`                   | Phase     | 6            | Six-category audit (labels, leakage, etc.)            |
| `phase-03-features.md`                     | Phase     | 7            | Feature framing for vision (Sprint 1)                 |
| `phase-04-candidates.md`                   | Phase     | 8, 14        | Multi-family sweep (Vision in S1, PredMaint in S2)    |
| `phase-05-implications.md`                 | Phase     | 9, 15        | Pick architecture / family + window, defend in $      |
| `phase-06-metric-threshold.md`             | Phase     | 10, 16       | Per-class thresholds + WSH floor 0.40                 |
| `phase-07-redteam.md`                      | Phase     | 11, 17       | Per-sprint adversarial / OOD / cohort sweeps          |
| `phase-08-gate.md`                         | Phase     | 12, 18       | Deployment gate (PASS/FAIL, promote, rollback signal) |
| `phase-09-codify.md`                       | Pointer   | —            | Explains Phase 9 runs via `workflow-08-codify.md`     |
| `phase-10-objective.md`                    | Phase     | 20           | RL reward function shape (4 weights)                  |
| `phase-11-constraints.md`                  | Phase     | 21, 24       | Hard vs soft + post-MOM re-classification             |
| `phase-12-acceptance.md`                   | Phase     | 22, 25       | RL accept + post-MOM re-solve + compliance cost       |
| `phase-13-drift.md`                        | Phase     | 27           | Three retrain rules (one per model_id)                |
| `phase-14-fairness.md`                     | Stub      | —            | Deferred to Week 8                                    |
| `appendix-a-lessons.md`                    | Accretion | —            | Transferable lessons running across weeks             |
| `appendix-b-dashboard.md`                  | Reference | —            | How to build a value-chain dashboard at your next job |
