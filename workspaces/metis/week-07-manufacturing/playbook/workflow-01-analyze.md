<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 1 — /analyze (inheritance audit)

> **What this step does:** Produce a written inventory of everything the LumenCircuit scaffold committed to before you arrived — what's already fixed, what's still yours to decide — before any code runs or any phase prompt fires.
> **Why it exists:** Every Playbook phase anchors its decisions to this inventory. An analysis that invents claims instead of reading the actual scaffold produces phantom decisions and corrupted phase journals.
> **You're here because:** You just opened the workshop. This is the first paste of the session.
> **Key concepts you'll see:** inheritance audit, cite-or-cut hygiene, fake blocker, four-layer industrial value chain, decisions-open

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm new to this project. Someone else built the scaffold before me. Before
I decide anything, I need to understand what they committed to on my behalf.

We are in the /analyze phase. The goal here is NOT to design the product —
it may already be pre-built. The goal is an inheritance audit: for every ML
artefact the scaffold ships, separate what is already fixed (baseline model
architecture, pre-trained weights, pre-wired endpoints, drift refs) from
what remains MY decision (chosen architecture, per-class thresholds, RL
reward weights, agent autonomy ladder, retrain rules).

Produce three files:

1. failure-points.md — for each module in the system, name the 3 most
   likely failure points tonight. For each failure point cite the specific
   file and function in the codebase. If you cannot cite a file and function
   for a claim, delete the claim.

2. assumptions.md — list every assumption the scaffold has already baked in.
   Cite each assumption to a file. For any dollar figure you mention, quote
   it verbatim from the project's cost source — do NOT invent numbers.

3. decisions-open.md — the list of decisions still mine to make, organized
   by sprint or module. For each decision name the Playbook phase that owns
   it. Do NOT propose values for any threshold, floor, weight, or ladder
   slot — those are my calls in the Playbook phases.

Do NOT use the word "blocker" unless you name the specific action I cannot
take until something is resolved. "The backend is slow" is not a blocker.

When all three files are written, stop and wait for me to run /todos.
```

**Tonight-specific additions** (Week 7 LumenCircuit Industrial AI Suite):

```
Output directory: workspaces/metis/week-07-manufacturing/01-analysis/
Files to produce: failure-points.md, assumptions.md, decisions-open.md

Four modules to cover: Vision QC inspector (transfer learning), Predictive
Maintenance classifier (time-series ML), Process-Optimization controller
(reinforcement learning), Coordination Agent + drift × 3 models (LLM agent
+ MLOps).

For each failure point, cite the specific file and function in
src/manufacturing/backend/ (e.g. ml_context.py::train_vision_leaderboard
or routes/optimize_rl.py::simulate). If you cannot cite a file and function,
delete the claim.

Scaffold assumptions to cover:
- 3-architecture vision leaderboard (resnet50_lr_head /
  efficientnet_b0_rf_head / vit_small_gbm_head) on a frozen-embedding scaffold
- 3-family predmaint leaderboard (lightgbm_features / lstm_sequence /
  survival_forest_tte) on 30 days × 10 SMT machines × 1-min cadence
- 3-policy RL leaderboard (ppo_continuous / dqn_discrete / random_baseline)
  as cached deterministic transition tables (10,000 episodes per policy)
- LLM agent harness with four tools (vision_classify, predict_failure,
  suggest_setpoint, log_safety_incident) and three autonomy modes
- Drift reference registered for all three model_ids (vision / predmaint / rl)
- 800 labelled PCB images (60% IPC-A-610 Class 3 / 40% Class 2)
- 200 procedural safety images (PPE/no-PPE × restricted-zone/clear)
Cite each to a source file in src/manufacturing/backend/ or
src/manufacturing/data/.

For every dollar figure, quote the exact line from PRODUCT_BRIEF.md §2 OR
specs/business-costs.md. Do NOT invent numbers. The five anchors:
$4,200 (major-defect shipped), $85 (false-scrap), $12,000 (unplanned
line-stop), $50,000 (equipment damage from RL), $1,000,000+ (WSH-notifiable
incident).

decisions-open.md format: organize by sprint (Sprint 1 Vision QC /
Sprint 2 Predictive Maintenance / Sprint 3 RL Optimization /
Sprint 4 Agent + MLOps). For each decision name the Playbook phase that
owns it (e.g. "pick per-class auto-pass thresholds × 4 vision classes:
Sprint 1, Phase 6"). Do NOT propose values.

The closing summary should name the four-layer industrial value chain
(See → Predict → Optimize → Coordinate) and the five Trust Plane decision
moments. Then confirm you are stopping for /todos.
```

**How to paste:** Combine both blocks into a single paste into your `claude` session.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ `01-analysis/failure-points.md` exists with 3 failure points per module (12 total), each citing a specific file and function in `src/manufacturing/backend/`
- ✓ `01-analysis/assumptions.md` lists 8–14 inherited assumptions, each cited to a source file; every dollar figure is quoted verbatim from `PRODUCT_BRIEF.md §2` or `specs/business-costs.md`
- ✓ `01-analysis/decisions-open.md` lists 14–18 open decisions organized by sprint, each tagged with the owning Playbook phase, with no proposed values
- ✓ A closing summary naming the four-layer cascade (See → Predict → Optimize → Coordinate) and the five Trust Plane moments
- ✓ A stop signal confirming Claude Code is waiting for `/todos`
- ✓ Viewer (http://localhost:3000) refreshes and shows: the value-chain banner with all four sprint tiles visible in baseline (no sprints green yet)

**Signals of drift — push back if you see:**

- ✗ A failure point with no file-and-function citation — ask "which file and function in `src/manufacturing/backend/` are you referring to?"
- ✗ A dollar figure that doesn't match `specs/business-costs.md` — ask "which row of the cost table does this come from? If it isn't there, remove it."
- ✗ A proposed threshold, floor, weight, or ladder choice anywhere in `decisions-open.md` — ask "please remove the proposed value; I own this decision in the Playbook phase."
- ✗ The word "blocker" without a specific action named — ask "which specific action can I not take until this is resolved?"
- ✗ A summary that collapses all four modules into one description — ask "please separate the four modules; they have different owners and different failure shapes."
- ✗ Viewer shows the banner but sprint tiles are missing or all grey — Claude Code may have described the cascade without reading the scaffold; ask for file citations before continuing.

---

## 3. Things you might not understand in this step

- **Inheritance audit** — a structured read of the scaffold to separate pre-committed choices from open decisions
- **Cite-or-cut hygiene** — every technical claim names a file and function; claims that can't be cited are deleted, not softened
- **Fake blocker** — calling something a blocker when it's actually latency or a warning, not a true stop
- **Four-layer industrial value chain** — See (vision) → Predict (sensors) → Optimize (RL) → Coordinate (agent); failure in one layer corrupts every later layer
- **Decisions-open** — the explicit list of calls that remain yours, framed as decisions not answers

---

## 4. Quick reference (30 sec, generic)

### Inheritance audit

The practice of reading what the scaffold already committed to — model architectures, pre-trained weights, dataset sizes, pre-wired endpoints — and writing it down before any Playbook phase starts. Industry ML almost always starts here, not from a blank slate. The audit separates what is already decided (3 vision archs ranked, 3 predmaint families ranked, 3 RL policies cached) from what is still yours to decide (chosen arch, per-class thresholds, RL reward weights, autonomy ladder, retrain rules). Without the audit, you risk re-deciding things the scaffold already fixed and producing inconsistent journals.

### Cite-or-cut hygiene

Every claim in an analysis document names the file and function it was read from. Claims that cannot be sourced to a specific file are deleted — not hedged, not footnoted, not kept as "likely." Cite-or-cut keeps analysis honest when a scaffold is large: Claude Code will hallucinate plausible-sounding architecture details if you don't demand citations for each one. The positive form: "ResNet-50 frozen + LR head, per `train_vision_leaderboard` in `src/manufacturing/backend/ml_context.py`."

### Fake blocker

A "blocker" is something that stops a specific action — "I cannot run Phase 4 because `/inspect/vision/train` returns 503." "The backend is slow" is not a blocker; it's latency. Distinguishing real blockers from latency or warnings matters tonight because Claude Code will flag the ~30-second LightGBM warm-up as a blocker when it isn't. A real blocker names an action that cannot proceed; a fake blocker just creates anxiety.

### Four-layer industrial value chain

The four models are not independent: vision QC scores feed the inspection queue; predictive-maintenance scores schedule downtime that the RL optimizer must respect; the agent routes signals across all three with autonomy modes that depend on the WSH envelope. A failure in vision (low recall on safety_critical_defect) corrupts the agent's autonomy boundary. Understanding the cascade is why `/redteam` is cross-sprint — a robustness finding in Sprint 1 must be traced through Sprints 2, 3, and 4.

### Decisions-open

The explicit list of calls that remain yours after the inheritance audit. Framed as decisions, not answers — "pick the vision architecture" not "ResNet-50 wins." Each decision names the Playbook phase that owns it so nothing gets silently skipped. The list is also a pre-registration contract: once you start a phase, the decisions-open list says what you were supposed to own.

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 7, where I am
building an industrial AI suite for LumenCircuit (Singapore PCB contract
manufacturer). I'm currently in the /analyze step.

Read `workspaces/metis/week-07-manufacturing/playbook/workflow-01-analyze.md`
for what this step does, and read `workspaces/metis/week-07-manufacturing/01-analysis/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. inheritance audit >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current LumenCircuit state
3. Implications for the decision I'm about to make (or just made) in /analyze
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] `01-analysis/failure-points.md` exists with 12 failure points (3 per module), each citing a specific file and function
- [ ] `01-analysis/assumptions.md` exists with all scaffold assumptions cited; every dollar figure quoted from `specs/business-costs.md`
- [ ] `01-analysis/decisions-open.md` exists with decisions organized by sprint and tagged to Playbook phases; no proposed values
- [ ] Closing summary names the four-layer cascade and five Trust Plane moments
- [ ] Claude Code has stopped and is waiting for `/todos`

**Next file:** [`workflow-02-todos.md`](./workflow-02-todos.md)
