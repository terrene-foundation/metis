<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 5 — Sprint 3 RL Boot (Reflow oven controller + MOM/WSH injection)

> **What this step does:** Boot Sprint 3 by copying skeleton journal files for the reinforcement-learning reflow-oven controller, confirming endpoints, and orienting on the MOM/WSH shadow-mode mandate that fires mid-sprint.
> **Why it exists:** Sprint 3 is two products in one — the RL policy that picks reflow-oven setpoints AND the agent autonomy ladder that constrains it. The MOM/WSH injection at ~4:30pm forces re-classification of WSH-affecting categories AND re-solve of acceptance. Booting cleanly means you don't lose 15 minutes when the injection fires.
> **You're here because:** Sprint 2 PredMaint wrapped (Phase 8 gate signed) and Sprint 3 is RL + the autonomy ladder.
> **Key concepts you'll see:** RL reward function, Goodhart's Law, hard-floor table, MOM/WSH injection, shadow price

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering Sprint 3 — reinforcement learning for the reflow-oven
controller. This sprint is two products in one. The RL policy chooses
zone temperatures + line speed in real time to maximise a four-term
reward (throughput - defect_cost - energy_cost - safety_penalty). The
agent autonomy ladder decides which setpoint changes the agent can act
on autonomously vs which require human confirmation. Phases 10, 11, 12
fire on the reward function AND the autonomy ladder.

Before I start the phase walk, I need you to:

1. Copy the Sprint 3 skeletons from journal/skeletons/ into journal/.
   These cover phase_10_objective.md (the reward function),
   phase_11_constraints.md (autonomy ladder + hard floors),
   phase_12_acceptance.md (RL leaderboard accept/redo + LP solve), plus
   the post-injection variants phase_11_postwsh.md and phase_12_postwsh.md.

2. Confirm the RL + agent + queue endpoints are live by GET requests.

3. State, in writing: which phases drive the REWARD FUNCTION (Phase 10
   sets the four weights; Phase 7 RL defends them against Goodhart) vs
   which phases drive the AGENT AUTONOMY LADDER (Phases 11, 12). Confusing
   the two is the #1 trap of this sprint.

4. State, in writing: when the MOM/WSH injection fires (~4:30pm), what
   re-classification is required (Phase 11 — autonomy ladder shifts to
   shadow on WSH-affecting categories) AND what re-solve is required
   (Phase 12 — quantify the compliance shadow price in $/day of lost RL
   gains). Missing the Phase 12 re-solve is the most common D3 zero of
   the sprint.

5. Do NOT propose reward-function weights or autonomy-mode slots. Those
   are my pre-registration calls in phase_10_objective.md and
   phase_11_constraints.md.

6. Do NOT use the word "blocker" without naming a specific action.

Once skeletons are copied and endpoints confirmed live, summarise: (a) the
four reward terms with their cost units and the two HARD floors named,
(b) the agent autonomy ladder shape (3 modes × 4 task classes), (c) the
MOM/WSH injection mechanics. Then stop.
```

**Tonight-specific additions** (Week 7 LumenCircuit Sprint 3):

```
Sprint: Sprint 3 RL Optimization + agent autonomy ladder.
Phases covered: 10 (RL reward function), 11 (autonomy ladder + hard
floors), 12 (RL leaderboard accept + LP solve) — plus the post-WSH
re-runs of 11 and 12.

Skeleton copy: copy phase_{10,11,12}_*.md skeletons (including the
_postwsh variants) into workspaces/metis/week-07-manufacturing/journal/.

Endpoint checks (GET only):
- /optimize/rl/leaderboard → 3 policies × throughput/defect/energy/safety
- /optimize/rl/reward_function → current reward weights + hard-floor table
- /agent/policy → current autonomy ladder
- /queue/state → inspector queue depth + SLA timer
If any is not live, STOP and raise a hand.

Reward function shape (NAME, do NOT propose weights — Phase 10 owns):
  reward = w_throughput × throughput
        - w_defect × defect_count × $4,200(major) / $180(minor)
        - w_energy × kwh × $0.08
        - w_safety × safety_violations  ← MUST clear hard floor

Hard floors (NAME, do NOT pick — these are regulator-mandated):
- safety_penalty weight ≥ floor that yields ZERO hard-floor violations
  across 10,000 cached episodes (specs/compliance-floors.md)
- Equipment-damage envelope: $50,000 per incident, 0/year (insurance policy)
- WSH-notifiable: 0 incidents/year (criminal liability)

Goodhart's Law warning: with safety_penalty=0 the agent runs the line at
90 boards/min, defect rate triples, equipment crashes within 48h. The
Phase 7 RL deliverable IS the demonstration that your chosen weights do
NOT reward-hack — leaderboard MUST show defect rate below ceiling AND
throughput at least 5% above random baseline AND zero hard-floor
violations across 10,000 episodes (PRODUCT_BRIEF.md §5 decision moment 4).

Agent autonomy ladder shape (NAME, do NOT propose slots):
- 4 task classes: vision_triage, maintenance_scheduling,
  setpoint_adjustment, safety_alert
- 3 modes: shadow (recommend-only, human acts), recommend (agent acts on
  low-stakes, escalates safety-critical), act (agent acts within
  hard-floored envelope)
- POST /agent/policy enforces the structural rule: WSH-affecting
  categories CANNOT be set above shadow during the MOM mandate window
  (returns 422)

MOM/WSH injection mechanics (~4:30pm):
- Trigger: instructor fires src/manufacturing/scripts/scenario_inject.py
  mom_wsh_shadow_mandate
- Effect: writes data/scenarios/mom_wsh_shadow_mandate.json marker; opens
  a 90-day mandate window
- Required Phase 11 re-classification: WSH-affecting task classes
  (setpoint_adjustment when line speed > 60 boards/min OR reflow zone >
  250 °C; safety_alert on restricted-zone access pattern) shift to HARD
  shadow mode for 90 days. POST /agent/policy returns 422 if you try to
  set them to recommend or act during the window.
- Required Phase 12 re-solve: re-run the RL leaderboard AND /queue/solve
  with the new envelope; quantify the compliance shadow price (lost RL
  gain in $/day from forcing recommend-only on safety-affecting
  setpoints).
- Files to write: phase_11_postwsh.md (re-classification with rationale)
  AND phase_12_postwsh.md (re-solve with quantified compliance cost in
  $/day). Skipping the Phase 12 re-write is the most common D3 zero in
  this sprint.

After the summary, stop and wait for my Phase 10 prompt.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ Skeleton files copied: `phase_10_objective.md`, `phase_11_constraints.md`, `phase_12_acceptance.md`, `phase_11_postwsh.md`, `phase_12_postwsh.md`
- ✓ All four endpoints (`/optimize/rl/leaderboard`, `/optimize/rl/reward_function`, `/agent/policy`, `/queue/state`) returned 200
- ✓ Summary names the four reward terms with cost units AND the two HARD floors ($50K equipment damage, WSH $1M)
- ✓ Summary names the autonomy ladder shape (3 modes × 4 task classes)
- ✓ MOM/WSH injection mechanics named: trigger script, marker file, required Phase 11 re-classification, required Phase 12 re-solve, the four journal files (NOT two)
- ✓ Stop signal pending Phase 10
- ✓ Viewer Sprint 3 tile activates

**Signals of drift — push back if you see:**

- ✗ A proposed reward weight (e.g. "throughput × 0.5 + defect × 0.3") — ask to remove
- ✗ Goodhart not named anywhere — ask "what stops the agent from setting safety_penalty=0?"
- ✗ The MOM/WSH injection described as "Phase 11 only" — ask "where does the Phase 12 re-solve fit?"
- ✗ Reward function conflated with the autonomy ladder — ask "Phase 10 picks weights; Phase 11 picks the ladder. Which one are we in?"
- ✗ A claim that "PPO obviously wins" without leaderboard reading — ask "what does /optimize/rl/leaderboard actually show across all four reward dimensions?"

---

## 3. Things you might not understand in this step

- **RL reward function** — the four-term equation that defines what the policy optimises; getting it wrong = Goodhart
- **Goodhart's Law** — "When a measure becomes a target, it ceases to be a good measure." If you reward throughput alone, the agent runs unsafe; if you reward zero defects alone, it stops the line.
- **Hard-floor table** — regulator-mandated floors that override cost-balanced math (safety_penalty floor, $50K equipment, WSH $1M)
- **MOM/WSH injection** — mid-Sprint-3 regulatory event that converts WSH-affecting categories from soft to hard shadow
- **Shadow price** — marginal $ cost of tightening a constraint; tonight, the lost RL gain in $/day from forcing recommend-only on safety-affecting setpoints

---

## 4. Quick reference (30 sec, generic)

### RL reward function

A weighted sum of four terms — throughput, defect cost, energy cost, safety penalty — that defines what the RL policy optimises. The weights are your Phase 10 deliverable; the demonstration that your weights do NOT reward-hack is your Phase 7 RL deliverable. Reward function design is THE load-bearing decision in RL — pick wrong weights and the agent reward-hacks throughput at the cost of defect rate.

### Goodhart's Law

"When a measure becomes a target, it ceases to be a good measure." Reward only throughput, agent runs the line at 90 boards/min, defects triple, equipment crashes. Reward only zero defects, agent stops the line. The four-term reward function is the structural defense — you bind the agent against extremes by making each axis its own term. The Phase 7 RL leaderboard is the audit: prove your weights produce defect rate < ceiling AND throughput > random baseline AND zero hard-floor violations.

### Hard-floor table

Regulator-mandated floors that no cost-balanced reward can negotiate. Tonight: safety_penalty weight must be ≥ the floor that yields zero hard-floor violations on 10,000 cached rollouts (`POST /optimize/rl/reward_function` returns 422 below floor); equipment-damage envelope $50,000/incident with 0/year (insurance policy); WSH-notifiable 0/year (criminal liability). The hard floors are above the reward function, not in it.

### MOM/WSH injection

A scripted event mid-Sprint-3 (~4:30pm) that simulates an MOM Inspectorate directive: any agent action affecting safety-relevant parameters (line speed > 60 boards/min, reflow zone > 250 °C, restricted-zone access during operation) MUST be in shadow mode for 90 days while MOM completes its audit. The injection is the analog to prior-week regulatory mid-injections in this course. The required response is a Phase 11 re-classification (WSH-affecting categories shift to hard shadow) AND a Phase 12 re-solve (quantify the compliance cost in $/day of lost RL gain). Two files must result: `phase_11_postwsh.md` and `phase_12_postwsh.md`.

### Shadow price

The marginal $ cost of tightening a constraint by one unit. Tonight: the post-WSH re-solve produces an RL plan with strictly lower expected throughput (because the agent can no longer auto-act on the safety-relevant setpoint dimensions). The $/day delta between pre- and post-WSH expected throughput IS the compliance shadow price. Quantifying it in `phase_12_postwsh.md` is the rubric D3 deliverable.

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 7 Sprint 3 (RL +
autonomy ladder), where I am building an industrial AI suite for
LumenCircuit.

Read `workspaces/metis/week-07-manufacturing/playbook/workflow-05-sprint-3-rl-boot.md`
for what this step does, and read `workspaces/metis/week-07-manufacturing/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. Goodhart's Law >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current LumenCircuit state
3. Implications for the decision I'm about to make (or just made) in Sprint 3
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

- [ ] Five skeleton files copied (`phase_10`, `phase_11`, `phase_12`, `phase_11_postwsh`, `phase_12_postwsh`)
- [ ] All four RL + agent + queue endpoints returned 200
- [ ] Summary names the four reward terms with cost units AND the two hard floors
- [ ] Summary names the autonomy ladder shape (3 modes × 4 task classes)
- [ ] MOM/WSH injection mechanics named, including the FOUR journal files
- [ ] Claude Code stopped, waiting for Phase 10 prompt

**Next file:** [`phase-10-objective.md`](./phase-10-objective.md)
