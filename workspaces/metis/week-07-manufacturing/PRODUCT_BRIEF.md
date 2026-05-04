<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# LumenCircuit Industrial AI Suite — Product Brief

Workshop product: the **LumenCircuit Industrial AI Suite** — one product assembled as a four-layer industrial value chain (Vision QC → Predictive Maintenance → Process Optimization → Agent + MLOps). By the end of the 210-minute workshop you will have shipped a transfer-learned vision QC inspector (Sprint 1), a predictive-maintenance time-series classifier (Sprint 2), a reinforcement-learning reflow-oven controller (Sprint 3), and an LLM agent that coordinates triage + maintenance + safety with drift monitors across all three (Sprint 4), against a pre-provisioned manufacturing backend, and defended a page of written decisions that explain why you shipped them that way.

Read this before writing your first prompt. Every dollar figure here is cited by the rubric and the contract grader; making them up in a journal entry scores zero.

Like Week 5 and Week 6, tonight **skips the build phase entirely**. The manufacturing backend (at `src/manufacturing/backend/`), viewer (at `apps/web/manufacturing/`), labelled PCB image dataset (at `src/manufacturing/data/`), baseline transfer-learned vision classifier (frozen ResNet/EfficientNet/ViT heads), baseline predictive-maintenance classifier (LightGBM, LSTM, Survival Forest), reinforcement-learning reflow-oven environment with cached PPO/DQN/Random rollouts, and the agent harness with three drift monitors registered are all pre-provisioned and running on your laptop before class starts. You walk in, paste one opening prompt, confirm preflight is green, and spend every minute of your 3.5 hours on the **full COC routine** — `/analyze`, `/todos`, `/implement`, `/redteam`, `/codify` — with the 14-phase ML Decision Playbook as the content of `/implement`. You do not scaffold, wire endpoints, or install libraries; you DO still run the routine you know, because that is the institutional muscle memory the course is building. Your job tonight is pure wielding: apply the Playbook to **transfer learning** (Sprint 1), **time-series predictive maintenance** (Sprint 2), **reinforcement learning** (Sprint 3), and **AI agents + drift across modalities** (Sprint 4).

## 1. Business context

LumenCircuit is a Singapore-headquartered contract manufacturer of high-reliability printed circuit board assemblies (PCBA). Its three Tuas-located SMT lines run 24/6 producing ~40,000 boards per day for medical-device, automotive ADAS, and aerospace customers — markets where IPC-A-610 Class 3 (high-performance / harsh-environment electronics) is the contractual quality standard, not a marketing claim. LumenCircuit is BizSAFE Level 4 certified under Singapore's Workplace Safety and Health Act 2006; the Ministry of Manpower (MOM) can issue stop-work orders within an hour of a notifiable incident, and a single industrial fatality carries personal liability for directors under the WSH Act and reputational fallout that ends the firm. Two years of inspection-decision history, sensor telemetry, and reflow-oven runs sit in `src/manufacturing/data/` (board images + machine sensor stream + reflow-oven episodes).

The Quality team has been inspecting boards with manual visual inspection + AOI (Automated Optical Inspection) rule-based pass/fail for eight years. AOI catches 78% of true defects but raises 12% false positives that flow to manual review, and the operator headcount has tripled since 2024 while throughput has only doubled — the math is breaking. Two near-miss field incidents in Q1 2026 (medical device dispatched with marginal solder joints; one customer caught it before patient harm, the second was an aerospace recall that cost LumenCircuit S$3.2M). The Head of Quality wants ML-assisted triage. The Head of Operations wants RL-assisted reflow control to recover the 2-3% throughput lost to manual oven re-balancing. The Head of EHS wants the agent's autonomy boundaries written down in ink. Legal wants a defensible audit trail for every auto-decision, and a structurally hard floor on any decision that touches WSH-notifiable categories. They are asking whether industrial AI can triage 90% of clear-cut defects automatically, predict pick-and-place failures 7 days before they occur, optimize the reflow-oven setpoints in real time, and coordinate the three with a single agent — without ever putting a human at risk.

Your job during the workshop is to commission Claude Code to train and evaluate this industrial AI stack, make the calls the tool cannot make for you, and write the journal that proves you made them.

Two planes run in parallel: the **Trust Plane** is where you decide (which architecture for transfer learning, what counts as a defect class, where the auto-pass line goes for each defect class, what the reward weights are, where the agent autonomy ladder sits, when to escalate to a human, when an MOM mandate forces shadow mode); the **Execution Plane** is Claude Code, the pre-provisioned backend, and the labelled PCBA dataset + sensor stream + RL environment. If a question is _what_ or _how_, route it to the Execution Plane. If it is _which_, _whether_, _who wins_, or _is it good enough to ship_, it stays with you.

## 2. Cost table (ground truth — use these exact numbers)

These numbers come from LumenCircuit's Quality + Operations finance pack. Every journal entry that names dollar impact must cite from this table. Three asymmetries drive every Phase 6 / 7 / 10 / 11 decision tonight: the **major-defect ($4,200) vs false-scrap ($85) ratio of 49:1** on the vision side, the **$50,000 equipment-damage penalty** that bounds the RL action space, and the **WSH $1,000,000 ceiling** that sits above any cost-balanced policy and forces every safety-affecting decision to a structurally hard floor.

| Cost term                                               | Value                             | Unit                                                       | Where it shows up                                |
| ------------------------------------------------------- | --------------------------------- | ---------------------------------------------------------- | ------------------------------------------------ |
| Major defect shipped (recall / field return)            | $4,200                            | per board (warranty + replacement + customer-confidence)   | Phase 6 metric weighting; Phase 7 Safety         |
| Minor defect shipped (rework downstream)                | $180                              | per board (in-line rework + repackage)                     | Phase 6 (per-class cost differentiation)         |
| Good board scrapped (false-positive auto-fail)          | $85                               | per board (component + labour cost of a scrapped BOM)      | Phase 6 metric weighting; Phase 7 Robustness     |
| Unplanned line-stop from missed maintenance signal      | $12,000                           | per stop (4-hour mean recovery × $3,000/hour line revenue) | Phase 11 (predictive maintenance cost balance)   |
| Equipment damage from RL action outside safe envelope   | $50,000                           | per incident (oven re-line + downtime)                     | Phase 11 (HARD constraint on RL); Phase 7 Safety |
| **WSH-notifiable incident (worker injury or fatality)** | **$1,000,000+**                   | per incident — MOM fine + criminal liability + reputation  | Phase 11 (HARD ceiling); Phase 7 Safety; ★ Floor |
| Qualified inspector time (IPC-A-610 Class 3 certified)  | $35                               | per minute on the manual-review queue                      | Phase 11 (queue cost); Phase 10 objective        |
| Cold-start cost (novel defect type, zero-shot misclass) | $620                              | per misclassified novel defect mode (recall escalation)    | Phase 11 (soft constraint); Phase 13 drift       |
| Edge inference (on-line camera, Jetson-class)           | $0.001                            | per board classification served at the edge                | Phase 10 (cost-of-serving); Phase 6 (peak load)  |
| Cloud RL training (A10G class)                          | $0.40                             | per training hour                                          | Phase 10 (training budget); Phase 13 retrain     |
| Peak season                                             | Q4 automotive ramp + medical reqs | seasonal throughput pressure                               | Phase 1 framing; Phase 13 drift context          |

Asymmetry: **$4,200 / $85 = 49:1** (defect-shipped vs false-scrap). PCB inspection lives in this asymmetry — a symmetric metric (raw accuracy) systematically under-prices missing real defects, and false-positive auto-fail is a real but small cost compared with letting a defective board ship to a medical-device or aerospace customer. The WSH $1M ceiling on safety-affecting decisions is structurally separate from the cost-balanced threshold logic; it is a regulatory floor, not a cost term to optimise. The $50K equipment-damage penalty bounds the RL action space — the reflow oven's max ramp rate and per-zone temperature ceiling are HARD constraints, not reward terms.

Supporting business volumes (for Phase 1 framing):

- ~40,000 boards per day across 3 SMT lines; ~12,000 inspection events per day post-AOI.
- Current AOI: 78% recall on true defects (lots of false negatives on novel modes), 12% false-positive rate (auto-fails legitimate boards), no per-class confidence.
- Manual review queue: average 1,400 boards at start of shift; SLA target = clear queue within 60 minutes.
- Scaffold sample: **800 labelled PCB images** (60% Class 3 — high-rel; 40% Class 2 — general industrial). Each has a class label (good / minor-defect / major-defect / safety-critical-defect) and a defect-mode label (solder-bridge / missing-component / tombstone / cold-joint / scratch / contamination / none).
- Predictive-maintenance scaffold: **30 days × 10 SMT machines × 1-minute cadence ≈ 432,000 sensor rows** (vibration, motor current, head temperature, cycle-count). 4 of the 10 machines fail during the window; 6 do not.
- RL scaffold: **10,000 reflow-oven episodes** per policy (PPO / DQN / Random) cached as deterministic transition tables (state = current zone temps + line speed + board class; action = ±5 °C per zone or hold; reward = throughput - defect_cost - energy_cost - safety_penalty).
- Safety-monitor scaffold: **200 procedural images** of the production floor (PPE/no-PPE; restricted-zone/clear). All 200 hand-labelled.

## 3. Personas (who you are serving)

You play the Student role and commission the Execution Plane on behalf of the four Trust Plane personas below.

| Persona            | Plane           | What they do                                                                           | What they read                                  |
| ------------------ | --------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------- |
| Head of Quality    | Trust Plane     | Approves per-class auto-pass thresholds; signs off on inspection-queue routing         | Per-class P/R/F1 dashboard, threshold register  |
| Head of Operations | Trust Plane     | Owns SMT-line uptime; approves predictive-maintenance prediction window + RL setpoints | Sensor-stream charts, RL leaderboard            |
| Head of EHS        | Trust Plane     | Owns WSH compliance; signs off on agent autonomy ladder + safety-monitor thresholds    | Incident log, safety-monitor decisions          |
| Legal Counsel      | Trust Plane     | Signs off on WSH hard floors; owns audit trail; reviews any agent-taken action         | Decision log, hard-constraint table, audit feed |
| ML Engineer        | Execution Plane | Ships training pipeline, registry, drift monitor (= Claude Code during the workshop)   | Logs, run tracker, model registry               |
| Student (you)      | Trust Plane     | Commissions every piece; graded on journal + contract grader                           | Viewer Pane, terminal, `PLAYBOOK.md`            |

## 4. The product story — one product, four layered modules (the industrial value chain)

This is a single industrial AI product built as the manufacturing value chain: **see → predict → optimize → coordinate**. Each module consumes the one above it. Skip a link and the whole chain misses the failure mode that lives there (vision-only catches today's defects but misses tomorrow's machine drift; sensors-only predict failure but never see the bad board it produced; RL-only optimises throughput but is blind to equipment health; the agent without drift monitoring rots silently as the line ages).

1. **The vision QC inspector sees defects (Transfer Learning · Sprint 1).** Every board image gets a per-class score (good / minor / major / safety-critical). A pre-trained ImageNet backbone with a fine-tuned classification head — transfer learning is the practical default for industrial vision at 800-image scale, not training from scratch. Three architectures on the leaderboard: ResNet-50, EfficientNet-B0, Vision Transformer (ViT-Small).
2. **The predictive-maintenance classifier predicts failure (Time-series ML · Sprint 2).** Every machine gets a per-day failure-probability for the next N days from its sensor stream (vibration / current / temperature / cycle-count). Three families on the leaderboard: LightGBM (hand-engineered features), LSTM (sequence model), Survival Forest (time-to-event).
3. **The RL controller optimises the reflow oven (Reinforcement Learning · Sprint 3).** A policy that adjusts the 5-zone reflow-oven temperature setpoints + line speed in real time to maximise throughput while keeping defect rate, energy cost, and safety violations bounded. Three policies on the leaderboard: PPO, DQN, Random baseline. The reward function is THE Phase 7 / Phase 10 decision — get the weights wrong and the agent reward-hacks throughput at the cost of defect rate (Goodhart's Law).
4. **The coordination agent + drift monitors close the loop (Agent + MLOps · Sprint 4).** An LLM agent with four tools (`vision_classify`, `predict_failure`, `suggest_setpoint`, `log_safety_incident`), three autonomy modes (shadow / recommend / act), and three drift monitors (vision per-week / sensor per-day / RL per-deployment). The agent is the human-in-the-loop wrapper that turns three independent models into one production line you can defend at a WSH audit.

Cascade: vision quality → predictive-maintenance precision → RL safety envelope → agent autonomy bound. One product, four layers, one chain of decisions.

## 4a. The four modules on the table tonight

### 4.1 Vision QC Inspector (Sprint 1 · Transfer Learning · See)

**What it is.** A transfer-learned image classifier returning per-class probabilities (good / minor-defect / major-defect / safety-critical-defect) for every PCB image. The scaffold ships a 3-architecture leaderboard at `/inspect/vision/leaderboard`: ResNet-50 (frozen backbone + LR head), EfficientNet-B0 (frozen backbone + RF head), Vision Transformer (frozen backbone + GBM head) — three different inductive biases on top of a transfer-learned representation. Per-class P/R/F1 / Brier visible at `/inspect/vision/leaderboard`. Scaffold sample: 800 labelled PCB images.

**Why it exists.** The Head of Quality cannot review 12,000 post-AOI inspection events per day with manual operators alone. The vision inspector triages the obvious 90% (clear good, clear major-defect) and routes the gray zone (minor, ambiguous) to certified IPC-A-610 Class 3 inspectors. The 49:1 asymmetry between major-defect-shipped ($4,200) and false-scrap ($85) means raw accuracy lies — a 96% accurate classifier that's wrong on the 4% safety-critical class is catastrophic.

**Who signs off.** Head of Quality (per-class threshold) and Legal Counsel (safety-critical-defect threshold is hard, not cost-balanced — see decision moment 5).

**Success at 5:30 pm.** A chosen architecture (ResNet / EfficientNet / ViT) is promoted from staging to shadow in the vision-inspector registry. Each of the 4 classes has a defended threshold tied to the $4,200 / $85 asymmetry AND the WSH safety floor for the safety-critical class. K is defended in the Phase 6 journal tied to per-class PR curves AND the counterfactual lift vs the 78%-recall AOI baseline.

### 4.2 Predictive Maintenance Classifier (Sprint 2 · Time-series ML · Predict)

**What it is.** A time-series classifier that scores each machine each day for failure within the next N days, where N is YOUR Phase 6 decision. Same 3-family leaderboard pattern as Week 5 + Week 6 — the scaffold trains LightGBM (hand-engineered features), LSTM (raw-sensor sequence), Survival Forest (time-to-event Cox-style), each at startup; `/predict/maintenance/leaderboard` exposes the comparison. Scaffold sample: 30 days × 10 machines × 1-minute cadence ≈ 432,000 sensor rows. 4 of the 10 machines have a labelled failure event in the window; 6 do not.

**Why it exists.** A pick-and-place machine running with worn bearings produces marginal-solder boards at 3× the rate of a healthy machine — the vision inspector catches them downstream but the line has already lost throughput. The Head of Operations wants 7-day failure prediction so maintenance can be scheduled in low-throughput windows, not as an emergency stop. Unplanned line-stops cost $12,000 each; planned ones cost $1,800.

**Who signs off.** Head of Operations (chosen family + prediction window) and Head of Quality (vision-side coverage during planned downtime).

**Pedagogical leaderboard.** LightGBM consistently wins at 10-machine scale on hand-engineered features (mean / std / max / trend per channel). LSTM-shaped and Survival-Forest-shaped surrogates have high seed-variance at this sample size — depending on the run they may tie, invert, or both score zero. The defendable takeaway is that **tabular ML on hand-engineered features is the right tool for small-data time-series prediction**, not that LSTM is structurally second-best. Students who re-run `/predict/maintenance/train` with a new seed will see the LSTM/Survival ranking move; they should NOT defend a strict ordering between the two.

**Success at 5:30 pm.** All three families on the leaderboard; chosen family + prediction window (3 / 7 / 14 days) defended in Phase 5 SML; cost-based threshold defended in Phase 6 SML against the $12,000 unplanned-stop vs $1,800 planned-stop asymmetry; calibration confirmed (Brier + reliability diagram); promotion to shadow in the predictive-maintenance registry.

### 4.3 Process-Optimization Controller (Sprint 3 · Reinforcement Learning · Optimize)

**What it is.** A reinforcement-learning policy that acts on the 5-zone reflow oven + line-speed setting in real time. State = current zone temps + line speed + board class on the line + minutes since last calibration. Action = ±5 °C per zone or hold + ±10 boards/min line speed. Reward = throughput - defect_cost - energy_cost - safety_penalty, where YOU set the weights in Phase 7 and the safety_penalty is HARD-floored by the $50K equipment-damage and the WSH-notifiable ceilings. The scaffold ships three policies as cached transition tables: PPO (continuous, multi-zone aware), DQN (discretised), Random baseline. `/optimize/rl/leaderboard` exposes the comparison.

**Why it exists.** The reflow oven is the throughput bottleneck. Manual operators re-balance the 5 zones every 30 minutes on average; in between, the oven drifts. Better setpoints would recover 2-3% throughput (~$2.4M/year) without buying new equipment. RL is the right tool because (a) the state-action-reward loop is well-defined, (b) the search space is too big for grid search, (c) the safety constraints are explicit. RL is the WRONG tool if you don't pin the reward function — Goodhart's Law: "Maximize throughput" and the agent runs the line so fast that defect rate triples and the line crashes.

**Who signs off.** Head of Operations (chosen policy + reward function weights) and Head of EHS (safety-penalty weight + hard-floored equipment-damage and WSH constraints).

**Success at 5:30 pm.** All three policies on the leaderboard; chosen policy + reward function weights defended in Phase 5 RL + Phase 7 (the defect-rate-vs-throughput trade-off table is the Phase 7 deliverable); the reward function is on disk at `/optimize/rl/reward_function` with explicit weights AND the two HARD floors named (equipment-damage $50K, WSH $1M); promotion to shadow in the RL registry.

**Mid-sprint injection (~4:30 pm).** **MOM/WSH issues a shadow-mode mandate:** following a near-miss incident at a peer fabricator the week prior, MOM Inspectorate has issued an industry-wide directive — any agent action affecting safety-relevant parameters (line speed above 60 boards/min, reflow zone temps above 250 °C, restricted-zone access during operation) MUST be in shadow mode (recommend-only, human-confirms) for 90 days while MOM completes its audit. This forces re-classification of the agent autonomy ladder for the safety-critical action subset, AND re-solving the Phase 11 + Phase 12 acceptance test for the RL policy under the new hard-shadow envelope. Students re-journal Phase 11 + 12 as `_postwsh.md`.

### 4.4 Coordination Agent + Drift Monitor × 3 models (Sprint 4 · Agent + MLOps · Coordinate)

**What it is.** An LLM agent that coordinates the three models above with four tools (`vision_classify`, `predict_failure`, `suggest_setpoint`, `log_safety_incident`), three autonomy modes (`shadow` — agent recommends, human acts; `recommend` — agent acts on low-stakes, escalates safety-critical; `act` — agent acts within hard-floored envelope), and three drift monitors (vision per-week, sensor per-day, RL per-deployment). The agent is the human-in-the-loop wrapper that turns three models into one production line. The drift monitors are how you keep it from degrading silently. The scaffold's `/agent/decide` accepts a board+machine context and returns the agent's chosen action + the autonomy mode + the audit-trail entry. `/drift/check` accepts a model_id + window and returns per-feature PSI + per-class calibration decay + overall severity per model. `/drift/retrain_rule` persists the retrain rule per model.

**Why it exists.** Without Sprint 4, the three models silently rot to "78% AOI recall" within a quarter, the agent hits novel cases with the wrong autonomy mode, and the WSH audit finds you cannot answer "who decided to ship that board?" The Head of EHS needs the agent autonomy ladder written in ink AND defended; the Head of Quality needs three drift rules — one per model — with variance-grounded thresholds, duration windows, and human-in-the-loop on first trigger. The Phase 13 journal captures all three drift rules in one entry.

**Who signs off.** Head of EHS (autonomy ladder), Head of Quality (re-training approval under HITL first trigger), Head of Operations (queue impact during retrain), Legal Counsel (audit-trail completeness).

**Success at 5:30 pm.** `/agent/decide` returns real decisions on the test contexts; `/drift/retrain_rule` has been called for each of the three model IDs (vision / predmaint / rl) with defensible thresholds. Each rule names: signal, threshold, duration window, HITL disposition, seasonal exclusions (Q4 ramp, scheduled re-calibrations). The Phase 13 journal entry covers all three. The agent autonomy ladder is documented in `/agent/policy` with explicit per-task-class autonomy mode AND the WSH shadow-mode override is honoured.

## 5. The five Trust Plane decision moments

Tonight collapses into five moments where the decision has teeth. Every other phase produces artefacts; these five are where you can silently ship a weak product if you are not paying attention. They are the rubric's highest-pressure points.

1. **Choose the vision QC base architecture** (Phase 5 Vision). _Tonight_: ResNet-50 (robust, well-understood, fast inference; best for general defect detection at 800-image scale), EfficientNet-B0 (best accuracy/efficiency ratio; best for edge deployment on a Jetson), or Vision Transformer (highest accuracy on subtle defects but data-hungry; risky at 800 images). Architecture decision tied to the edge-deployment constraint (the inspection cameras run on Jetson-class hardware; latency budget is 80 ms/board) AND the per-class P/R/F1 leaderboard.
2. **Set the auto-pass confidence threshold per class** (Phase 6 Vision) — defended in $ of (defect-shipped cost × FN rate at threshold) + (false-scrap cost × FP rate at threshold), with the WSH safety floor forcing safety-critical-defect to a structurally hard threshold (not cost-balanced — see decision moment 5).
3. **Choose the predictive-maintenance prediction window** (Phase 5 PredMaint + Phase 11). 3-day (faster recovery, more false positives), 7-day (the operations sweet spot — gives ops time to schedule downtime), or 14-day (lower false positive rate but you've already lost throughput by the time you act). Defended in $ of unplanned-stop avoidance vs planned-maintenance overhead.
4. **Design the RL reward function weights** (Phase 7 RL). Set the four reward weights — throughput, defect_cost, energy_cost, safety_penalty — and prove with the leaderboard that the chosen weights do NOT reward-hack. Goodhart's Law: "Maximize throughput" with safety_penalty=0 → agent runs line at 90 boards/min, defect rate 18%, equipment crash within 48 hours. The leaderboard MUST show your chosen weights produce a defect rate below ceiling AND throughput at least 5% above the random baseline AND zero hard-floor violations across 10,000 episodes.
5. **Set the agent autonomy ladder + the WSH safety floor** (Phase 11 + Phase 12). Three autonomy modes (shadow / recommend / act) per task class (vision triage / maintenance scheduling / setpoint adjustment / safety-monitor alert); the WSH-affecting categories (line speed > 60 / reflow zone > 250 °C / restricted-zone access) are STRUCTURALLY hard-shadowed when the MOM mandate fires (see Sprint 3 mid-injection). Re-solve the agent autonomy table under the post-WSH envelope and quantify the optimization shadow price (compliance cost in $/day of lost RL gains).

All five are non-negotiable tonight.

## 6. 5:30 pm success definition

By the close of the workshop, a passing run looks like this. Every item is grader-verifiable or rubric-verifiable.

- [ ] **All four modules' endpoints return real data** (no `{"status":"ok"}` stubs): `/inspect/vision/leaderboard` + `/inspect/vision/threshold` (per-class), `/predict/maintenance/leaderboard` + `/predict/maintenance/window` + `/predict/maintenance/threshold`, `/optimize/rl/leaderboard` + `/optimize/rl/reward_function`, `/agent/decide` returns real decisions on the test contexts, `/drift/check` ran against the recent_30d window for all three model IDs, `/drift/retrain_rule` called for vision / predmaint / rl.
- [ ] **At least 14 journal entries** at `journal/phase_N_{vision,predmaint,rl,...}.md`. Each one names its signal, threshold, and duration under `## Reversal condition` — never the phrase "if data changes".
- [ ] **MOM/WSH injection produces four files, not two**: `journal/phase_11_constraints.md`, `journal/phase_11_postwsh.md`, `journal/phase_12_acceptance.md`, `journal/phase_12_postwsh.md`. The MOM re-run hits the AGENT autonomy ladder, not just the threshold. The compliance shadow price (lost-RL-gain in $/day) is quantified in `phase_12_postwsh.md`.
- [ ] **Phase 13 journal has three rules**, one per model (vision / predmaint / rl), each with signal + variance-grounded threshold + duration window + HITL disposition + seasonal exclusions (Q4 ramp, planned recalibrations).
- [ ] **The value-chain banner on the viewer shows all four sprints green** at close, and the five decision moments all ticked.

Combined score target: ≥ 0.60 (60% journal rubric mean + 40% endpoint-contract grader).

## 7. What is different from Week 6 (read this if you took Week 6)

- **No scaffold work, but the COC routine still runs.** The backend, data labeller, baseline transfer-learned vision classifier, baseline predictive-maintenance classifier, RL policy cache, agent harness, and drift reference for all three models are pre-provisioned at `src/manufacturing/` and `apps/web/manufacturing/`. Your first prompt confirms preflight is green, then you enter `/analyze` (inventorying baseline commitments and open decisions), `/todos` (Playbook phases as plan; instructor gate), `/implement` (four sprints Vision→PredMaint→RL→Agent), `/redteam`, `/codify`. The Playbook phases are the CONTENT of `/implement`, not a replacement for the routine.
- **Reinforcement learning replaces multi-modal fusion.** Week 6 was CNN + Transformer + Multi-modal fusion. Week 7 is Transfer Learning + Time-series ML + RL + Agent. The Playbook phases stay the same — the model families, metrics, and the Phase 7 / 10 / 11 deliverables swap. RL adds a NEW phase asset: the reward function, defended in Phase 7 in $-weighted units AND with the hard-floor table.
- **AI Agent is the new Multi-modal moderator.** Week 6's fusion moderator was a model that combined two modalities. Week 7's coordination agent is an LLM-driven controller that ROUTES across three models with explicit autonomy modes. The Phase 5 Multi-Modal lens becomes Phase 5 Agent — same place in the routine, different deliverable.
- **MOM/WSH is the new IMDA** — Week 6's IMDA CSAM mandate clarification → Week 7's MOM/WSH shadow-mode mandate. Same rubric pressure (hard/soft constraint classification, Phase 11+12 re-run), different regulatory surface. Fires mid-Sprint-3 at 4:30 against the AGENT autonomy ladder (re-run Phase 11 + 12).
- **The RL reward function is the new threshold** — Week 5's churn threshold + Week 6's per-class moderation threshold → Week 7's reward function weights. Phase 7 (Safety / Robustness) is correspondingly heavier — it's not picking a number on a curve, it's defending FOUR weights that interact non-monotonically.
- **49:1 asymmetry replaces 21:1.** Week 6's content-moderation asymmetry was 21:1 (FN $320 vs FP $15). Week 7's PCB-inspection asymmetry is 49:1 (FN $4,200 vs FP $85). Phase 6 metric weighting tilts even harder toward recall on safety-critical defects.
- **Drift cadences are stratified by data-generating process.** Week 6 had weekly/daily/per-incident on three models. Week 7 has weekly (vision — equipment + supplier drift), daily (sensor — temperature, calibration), per-deployment (RL — every policy update). Phase 13 must defend each cadence separately — universal "weekly retrain" is BLOCKED.
- **Edge deployment is on the table.** Week 6's models ran in the cloud at the platform's API. Week 7's vision QC inspector is targeted for edge deployment on Jetson-class hardware (line cameras). Phase 5 architecture choice MUST cite the 80 ms/board edge latency budget and the device memory ceiling. EfficientNet-B0 ↔ ResNet-50 ↔ ViT trade-off is partly AN EDGE-deployment trade-off.

## 8. Where to go next

- `START_HERE.md` — student manual with the opening prompt, the COC-wrapped clock, and the four-sprint flow.
- `PLAYBOOK.md` — the universal 14-phase procedure with teaching blocks (Vision lens + PredMaint lens + RL lens + Agent lens + Your levers + Transfer to next project) per phase.
- `SCAFFOLD_MANIFEST.md` — every pre-built file, who writes it, who reads it.
- `src/manufacturing/data/boards_labelled.csv` — the labelled PCB inspection dataset (image + AOI flag + manual-decision label + defect-mode label).
- `src/manufacturing/data/sensor_stream.csv` — the 30-day × 10-machine sensor stream.
- `src/manufacturing/data/rl_episodes.json` — the cached PPO/DQN/Random rollouts.
- `src/manufacturing/data/baseline_vision_metrics.json` + `baseline_predmaint_metrics.json` + `baseline_rl_metrics.json` — pre-built baseline per-class metrics.
- `src/manufacturing/data/drift_baseline.json` — registered drift reference distribution (per modality).
- `src/manufacturing/data/scenarios/` — mid-session injection payloads (`mom_wsh_shadow_mandate.json`, `q4_demand_drift.json`).
- `journal/skeletons/` — fill-in-the-blank per-phase templates; copy into `journal/phase_N_*.md` at the start of each phase.
