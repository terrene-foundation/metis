<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# START HERE — Week 7: Industrial AI

**Version:** 2026-05-04 · **License:** CC BY 4.0

> A 3.5-hour workshop where **you commission and defend an industrial AI product** — a transfer-learned vision QC inspector, a predictive-maintenance classifier, an RL reflow-oven controller, and a coordination agent with three drift monitors — on a pre-provisioned LumenCircuit backend, **without writing a single line of code**. Claude Code already has the infrastructure. You run the full COC routine (`/analyze` → `/todos` → `/implement` → `/redteam` → `/codify`) against the 14-phase ML Decision Playbook. You direct, evaluate, decide, and defend.

Read sections 0–3 before class. Keep this open in a tab throughout the session.

---

## 0. Five-Minute Orientation

### Tonight is the industrial value chain, not the build

You inherited this project ten minutes before class. Your predecessor — LumenCircuit's first ML Quality hire — left last Friday after an aerospace recall cost the firm S$3.2M. The Head of Quality is waiting on per-class auto-pass thresholds she can defend to her IPC-A-610 Class 3 customers. The Head of Operations is waiting on a 7-day predictive-maintenance window so his maintenance team knows when to schedule downtime. The Head of EHS is waiting on the agent autonomy ladder written in ink, with the WSH safety floor below every safety-affecting action. Legal Counsel is waiting on a hard-constraint table she can hand to MOM Inspectorate on Monday. You have until 5:30 pm to ship all four and defend every decision in front of them.

The backend, viewer, 800 labelled PCB images, 30 days × 10-machine sensor stream, baseline transfer-learned vision classifier (3-arch leaderboard), baseline predictive-maintenance classifier (3-family × 3-window leaderboard), reinforcement-learning reflow-oven environment with cached PPO/DQN/Random rollouts, and the agent harness with three drift monitors registered are already running on your laptop — your predecessor's last commit. That is not a shortcut. That is how ML arrives in industry: you walk into a half-done project, you ship it, and you own every judgment call the previous person did not have time to make. This week it is industrial AI. Last week it was content moderation. The week before, retail. Eight weeks, eight inherited products, one muscle memory: **run the routine, make the calls, defend the work.**

What you still run is the full **COC routine**: `/analyze` first (inventory what your predecessor committed to and name the decisions still open), then `/todos` (lay out the 14 Playbook phases as a tracked plan with a human gate), then `/implement` (each of four sprints executes a block of Playbook phases), then `/redteam` and `/codify` at the close. Every week of this course is the same routine applied to a different inherited product.

### What you will walk away with today

1. **A deployed industrial AI product.** Vision QC inspector returning per-class scores on every PCB image, predictive-maintenance classifier scoring every machine each day, RL controller suggesting reflow-oven setpoints, coordination agent routing decisions across all three with the WSH safety floor honoured, drift monitors watching all three. Running at a URL you can share.
2. **A decision journal PDF.** A signed record of every ML judgment call you made today, scored on the 5-dimension rubric.
3. **A reusable ML Decision Playbook** — applied to a fourth domain (manufacturing, transfer learning, RL, agents) after Week 4's supervised + optimization, Week 5's USML + recommender, and Week 6's deep learning + multi-modal. This is the point of the course: the Playbook transfers.
4. **A complete COC artefact set** — `01-analysis/failure-points.md`, `todos/active/phase_N_*.md`, `journal/phase_{1..13}_*.md`, `04-validate/redteam.md`, `.claude/skills/project/week-07-lessons.md`. The routine is what institutionalises the learning.

### What you will NOT do today

- Write Python, JavaScript, SQL, or any other code.
- Install libraries, configure environments, debug stack traces.
- Wire endpoints, seed data, or build UI — the product is pre-built at `src/manufacturing/` and `apps/web/manufacturing/`.
- Memorize "what is backpropagation" or "how does PPO work internally".

### What you **will** do

- **Paste one opening prompt** that boots the pre-built LumenCircuit backend and viewer, and confirms preflight is green.
- **Run the full COC routine** — `/analyze`, `/todos`, `/implement`, `/redteam`, `/codify` — against the 14 Playbook phases.
- **Read the Viewer Pane** as outputs arrive.
- **Evaluate** what Claude Code produced — was it good work? honest work? complete work?
- **Decide** the judgment calls only a human can own (which architecture, what counts as a defect, where the auto-pass line goes per class, what the reward function weights are, where the agent autonomy ladder sits, when to escalate to a human, when an MOM mandate forces shadow mode).
- **Journal every decision** with a short memo justifying it.

### The bargain this course offers

We are not teaching you to build. We are teaching you to **commission, judge, and ship ML products as a one-person team.** Claude Code is your engineer, your data scientist, your DevOps. You are the founder. Your differentiating skill is knowing **what to ask, how to read the answer, and when to say "ship it" or "do it again."**

---

## 1. The Two Planes You Operate Across

Everything today (and every week onward) splits into two planes:

| Plane               | Who does it            | What they produce                                                               | Examples                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------- | ---------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Trust Plane**     | You — the human        | Judgment, framing, evaluation, approval                                         | "Auto-pass threshold 0.65 on minor_defect because $4,200 FN cost vs $85 FP cost = 49:1, but safety_critical_defect threshold is 0.40 because WSH $1M ceiling, not cost-balanced." "PPO with safety_penalty=0.50 because cached rollouts at lower weights produce ≥1 hard-floor violation." "Agent setpoint_adjustment=recommend, not act, because operations team owns the line-speed decision under MOM scrutiny." "Retrain vision weekly, sensor daily, RL per-deployment." |
| **Execution Plane** | Claude Code + scaffold | Code, trained models, per-class metrics, RL rollouts, drift reports, dashboards | Pre-wired backend endpoints, pre-trained 3-arch vision leaderboard (ResNet-50 / EfficientNet-B0 / ViT-Small), pre-trained 3-family × 3-window predmaint leaderboard, cached RL transition tables for PPO/DQN/Random, pre-registered drift reference for all three modalities, agent harness with autonomy ladder, viewer dashboard                                                                                                                                            |

### Why this split matters

In the old world, a Head of Quality asked an engineering team for "AI defect inspection", waited six months, got a model that classified at 92% accuracy, and could not tell whether 92% was good enough or whether the 8% it missed was the safety-critical class. In the AI-native world, **the per-class PR curves are ten prompts away and the RL leaderboard is twenty prompts away** — which means the bottleneck moves to **asking the right questions and evaluating the answers**. That is the Trust Plane. That is your job.

If you cannot frame what counts as a safety-critical defect, commit to threshold floors before seeing the results, classify the WSH constraint correctly, defend the RL reward function against Goodhart's Law, or approve the deployment — the AI is driving, not you. That is the failure mode. Tonight we train you out of it.

### The rule of thumb for today

> If the question is **what** or **how**, let Claude Code answer it.
> If the question is **which**, **whether**, **who wins and who loses**, or **is it good enough to ship** — that is yours.

---

## 2. The Product You Are Shipping: LumenCircuit Industrial AI Suite

### What it is

An industrial AI suite for LumenCircuit, a Singapore-headquartered contract manufacturer of high-reliability PCB assemblies. On the books: ~40,000 boards/day across 3 SMT lines, 24/6 operating model, IPC-A-610 Class 3 contract terms, BizSAFE Level 4 certified under WSH Act 2006. The workshop scaffold ships a **representative 800-labelled-board sample** (60% Class 3, 40% Class 2) + **30 days × 10-machine sensor stream** (~432k rows) + **10,000 cached RL episodes per policy** + **200 procedural safety images** — fast enough to fine-tune live, adversarial enough to force real decisions. Cite the scaffold numbers in your journal entries; the book numbers belong in Phase 1 framing only.

**One product, four layered modules — the industrial value chain:**

1. **Vision QC Inspector** (Sprint 1 · Transfer Learning · See). Every PCB image gets per-class scores (good / minor_defect / major_defect / safety_critical_defect). 3-architecture leaderboard: ResNet-50 / EfficientNet-B0 / Vision Transformer-Small. Transfer learning, not training from scratch.
2. **Predictive Maintenance Classifier** (Sprint 2 · Time-series ML · Predict). Every machine each day gets a failure-probability for the next N days from sensor stream. Three-family leaderboard: LightGBM / LSTM / Survival Forest. Three windows: 3 / 7 / 14 days.
3. **Process-Optimization Controller** (Sprint 3 · RL · Optimize). PPO / DQN / Random baseline policies on the 5-zone reflow oven. Reward function = throughput - defect_cost - energy_cost - safety_penalty, with hard floors on equipment damage ($50K) and WSH ($1M) that the agent CANNOT trade off.
4. **Coordination Agent + Drift × 3 models** (Sprint 4 · Agent + MLOps · Coordinate). LLM-style agent harness with four tools, three autonomy modes (shadow / recommend / act), drift monitors at three cadences (vision weekly / predmaint daily / RL per-deployment).

This is the cascade: **vision → predmaint → RL → agent**. Get Sprint 1 wrong and the agent inherits a noisy classifier. Set the RL safety_penalty too low and the agent's act-mode setpoints crash an oven. Skip Sprint 4 and you'll never know when any of the three silently stops working.

### Who uses it

- **Head of Quality**: approves per-class auto-pass thresholds (Sprint 1), signs off on inspector-queue routing
- **Head of Operations**: owns SMT-line uptime; approves predictive-maintenance prediction window (Sprint 2) + RL reward function weights (Sprint 3)
- **Head of EHS**: owns WSH compliance; signs off on agent autonomy ladder (Sprint 4) + safety-monitor thresholds
- **Legal Counsel**: signs off on WSH hard floors; owns audit trail; reviews any agent-taken action

### What "shipped" looks like at 5:30 pm

- The manufacturing viewer running at `http://localhost:3000` with the value-chain banner showing all four sprints completed
- The manufacturing backend running locally (`src/manufacturing/backend/`) with all 33 endpoints live: `/inspect/vision/*`, `/predict/maintenance/*`, `/optimize/rl/*`, `/agent/*`, `/drift/*`, `/queue/*`, `/state/*`
- A `journal.pdf` with decision memos spanning Phases 1–9 (Vision) + 4–8 replay (PredMaint) + 5–12 (RL + queue) + 12–13 (Agent + MLOps × 3 models)
- A complete COC artefact set — `01-analysis/`, `todos/completed/`, `journal/`, `04-validate/`

### The business context (for framing decisions — cite these exact numbers)

- LumenCircuit: ~40,000 boards/day, 3 SMT lines, 24/6, IPC-A-610 Class 3, BizSAFE Level 4 under WSH Act 2006. **Scaffold sample: 800 labelled boards** + 432k sensor rows + 30,000 RL episodes + 200 safety images.
- Each **major defect shipped** (recall / field return) costs **$4,200** in warranty + replacement + customer-confidence
- Each **good board scrapped** (false-positive auto-fail) costs **$85** in component + labour
- Each **unplanned line stop** (missed predmaint signal) costs **$12,000** at 4 hr × $3,000/hr line revenue
- Each **planned-maintenance window** costs **$1,800** (off-shift)
- Each **equipment-damage incident** from RL action outside safe envelope costs **$50,000** — HARD floor
- Each **WSH-notifiable incident** (worker injury or fatality) costs **$1,000,000+** in MOM fine + criminal liability + reputation — HARD floor
- Each **qualified inspector minute** costs **$35** (IPC-A-610 Class 3 certified)
- Each **cold-start misclassification** on a novel defect mode costs **$620**
- **Edge inference**: $0.001 per board on Jetson-class hardware
- **Cloud RL training**: $0.40/hr A10G class
- Peak throughput windows: Q4 automotive ramp + medical certification cycles (DO NOT auto-retrain on these)
- Current AOI: 78% recall, 12% FP rate — the floor the new system must clear to justify shipping

These numbers drive every decision in Phases 1, 6, 7, 10, 11, 12, and 13. Keep `PRODUCT_BRIEF.md` open in a tab — your journal entries will cite from that file.

---

## 3. The Orchestrator Hygiene Toolkit

Tonight Claude Code will generate a lot of text very fast. Most of it will be correct. Some of it will not. The four checks below are the discipline that catches the difference — without you needing to know any deep learning to apply them.

Two quick definitions before the checks:

- **Floor** = a pass/fail line. "Per-class F1 must be at least 0.70 on safety*critical_defect" is a floor. A floor is only honest if you wrote it down \_before* you saw the result.
- **Pre-registration** = writing a floor in your journal before running the test. It is the difference between measuring and moving the goalposts.

### Check 1 — "Show me the line"

**When:** Claude Code names a specific architecture, technique, library, or method as if it is a fact.

**Ask:** "Show me the exact file, function, and line that proves this. Quote the line. If you have not read it, say so."

**Worked example.** When you ran the opening prompt, `/health` returned `vision_baseline_arch: "resnet50_lr_head"`. An hour later Claude Code writes: _"The vision QC inspector uses EfficientNet-B7 for the backbone."_ You ask the verbatim question. Claude Code reads the source, comes back: _"I was wrong — `resnet50_lr_head` per `build_vision_baseline` in src/manufacturing/backend/ml_context.py."_ You move on.

### Check 2 — "Show me the brief"

**When:** Claude Code cites a specific dollar figure or business metric you did not give it.

**Ask:** "Which line of `PRODUCT_BRIEF.md` or which document did this number come from? Paste the row."

### Check 3 — "Did I write that floor first?"

**When:** Claude Code reports a result and declares it "passed" or "failed" against a threshold that appears for the first time in the same message as the result.

**Ask:** "Where was that threshold written down **before** this run? Point me to the journal entry where I pre-registered it."

### Check 4 — "What am I blocked from?"

**When:** Claude Code labels something "blocking", "incomplete", "defect", "not working", or "gap".

**Ask:** "What exact next step can I not take because of this? Name the sprint, the phase, and the endpoint. If I can still run my next phase, this is a future task, not a blocker — relabel it."

### The meta-principle

**Make Claude Code show its work.** Architecture claim → line of code. Number → row of brief. Threshold → pre-registered. Blocker → next step it blocks.

---

## 4. How to Use This Workshop

- **Read this file once** — §0–§3 above are pre-class reading. Keep the tab open.
- **Open `playbook/README.md` for run-order navigation** — your table of contents.
- **Open playbook files in order** — each is self-contained.
- **Use `playbook/appendix-a-lessons.md` for transferable lessons** — accreted from Weeks 4-6.

---

## 5. How You Are Graded

Two layers, weighted 60/40.

### Layer 1 — Decision Journal (60%)

Each journal entry is scored on 5 dimensions, 0 / 2 / 4 each:

| Dim                        | 0                            | 2                         | 4                                                                                                          |
| -------------------------- | ---------------------------- | ------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **D1 Harm framing**        | No stakeholders named        | Names one cost            | Quantifies asymmetry in named dollars ($4,200 FN vs $85 FP = 49:1; $1M WSH ceiling separately structural)  |
| **D2 Metric→cost linkage** | Metric chosen without reason | Reason named              | Reason is a dollar figure or counterfactual-lift vs the AOI 78%-recall baseline                            |
| **D3 Trade-off honesty**   | Picks winner, ignores loser  | Names what was sacrificed | Quantifies the sacrifice ("lost 0.04 precision on minor_defect to gain 0.11 recall on safety_critical")    |
| **D4 Constraint classify** | Unclear hard/soft            | Labelled correctly        | Penalty (in dollars) + reasoning (WSH $1M is hard; $35/min inspector time is soft; equipment $50K is hard) |
| **D5 Reversal condition**  | "If data changed"            | Names a signal            | Names signal + threshold + duration window                                                                 |

Average across all today's entries. Target: ≥ 3.0 on average to pass.

### Layer 2 — Product Shipped (40%)

Binary checks:

- [ ] Dashboard loads at `http://localhost:3000`
- [ ] Vision endpoints return real per-class scores (not `{"status":"ok"}` stubs)
- [ ] PredMaint endpoints return per-machine fail-probability per chosen window
- [ ] RL leaderboard shows PPO > DQN > Random with safety_violations counts
- [ ] Agent `/agent/decide` returns real decisions with audit-trail entries
- [ ] Drift endpoints return PSI + severity for all three model IDs
- [ ] `journal.pdf` exports cleanly

Each = 14.3% of the product grade; partial credit for partial functionality.

---

## 6. When You Get Stuck

1. **Re-prompt Claude Code more precisely.** Add cost numbers, phase context, evaluation criteria.
2. **Check `playbook/README.md`** for run-order and the current file's quick reference.
3. **Check `playbook/appendix-a-lessons.md`** for transferable patterns from prior weeks.
4. **Ask a neighbor** — compare prompts.
5. **Flag the instructor** — wave, don't shout.

### Common traps

- **"ResNet always wins so why have three architectures?"** — At 800 images yes; at 50,000 ViT can win. The leaderboard is the demonstration that data scale changes the answer. Phase 5 ★ is defending YOUR pick at YOUR scale.
- **"WSH is just a guideline, right?"** — No. WSH Act 2006 carries criminal liability for directors. The $1M-per-incident ceiling sits structurally above any cost-balanced threshold. The safety_critical_defect threshold floor of 0.40 is HARD. The MOM shadow-mandate is HARD when it fires.
- **"The reward function is just the metric, set it to maximise throughput."** — Goodhart. Cached rollouts under safety_penalty=0 produce 419 hard-floor violations per 10,000 episodes. The four reward weights are a JOINT decision, not four independent metrics. Defend them in Phase 7 against the leaderboard.
- **"My agent autonomy ladder is shadow / shadow / shadow / shadow — that's safest, ship it."** — That's also worthless. The point of the agent is to absorb routine cases at recommend-or-act mode while shadow-ing the WSH-affecting subset. Defend each task class separately.
- **"Claude Code said it ran the simulate but I see nothing in the dashboard."** — It probably described the work. Re-prompt: "Show me the JSON response from /optimize/rl/simulate, the n_episodes argument you passed, and the safety_violations count."
- **"The drift check returned 'no reference set'."** — The reference is pre-registered for all three model IDs. Do NOT re-seed. Ask Claude Code to read /drift/status/{model_id} for vision / predmaint / rl separately.
- **"I'm in Sprint 2 and Phase 10 comes next, right?"** — No. Sprint 2 is the time-series replay — Phases 4, 5, 6, 7, 8 applied to predictive maintenance. Sprint 3 is where Phases 5, 7, 10, 11, 12 fire on the RL controller + queue allocator + agent autonomy ladder.
- **"MOM fired at 4:30 — I only need to re-run Phase 11, right?"** — No. The injection demands BOTH a Phase 11 re-classification AND a Phase 12 re-solve against the agent autonomy ladder. Missing the Phase 12 re-solve scores 0 on D3.
- **"Per-class thresholds, why not one global threshold?"** — Because the cost asymmetry shifts per class. Safety_critical is HARD floor (0.40). Major-defect is cost-balanced (49:1). Minor-defect is cost-balanced (2:1). One threshold per inspector silently averages over all of these. Sprint 1 demands 4 thresholds.

---

## 7. Your Opening Prompt

Open a terminal at the **project root** (`~/repos/training/metis`). Type `claude` to start. Paste this exactly:

```
The active workspace is workspaces/metis/week-07-manufacturing/.
Read these files from the workspace:
- workspaces/metis/week-07-manufacturing/PRODUCT_BRIEF.md
- workspaces/metis/week-07-manufacturing/START_HERE.md
- workspaces/metis/week-07-manufacturing/playbook/README.md
- workspaces/metis/week-07-manufacturing/specs/_index.md

I am a student running tonight's Week 7 industrial AI workshop.

The product (LumenCircuit Industrial AI Suite) is pre-provisioned under
src/manufacturing/ (backend + data + pre-trained models + cached RL
rollouts) and apps/web/manufacturing/ (viewer). You will NOT scaffold,
wire endpoints, or install libraries.

NOTE: The /analyze and /todos files are PRE-PRODUCED at
01-analysis/{failure-points,assumptions,decisions-open}.md and
todos/active/phase_*.md. Copy them as the basis for our /analyze and
/todos rounds — do NOT regenerate from scratch. Then proceed straight
to /implement Sprint 1 Vision QC boot.

We WILL still run the full COC routine — /analyze, /todos, /implement,
/redteam, /codify — because that's the institutional muscle memory we
are building. The 14-phase ML Decision Playbook is the CONTENT of
/implement tonight, not a replacement for it.

Boot the pre-provisioned environment FOR ME (I will not run bash myself).
Execute these steps in order inside this session; start long-running
processes in the background so you can continue. Report progress aloud
so I can see you're alive during the ~10s startup.

1. Run the preflight check:
     .venv/bin/python src/manufacturing/scripts/preflight.py
   Expect exit 0, all rows ✓. Report any non-green rows.

2. Start the backend in the background:
     bash src/manufacturing/scripts/run_backend.sh
   Poll curl -sf http://127.0.0.1:8000/health every 2 seconds until it
   responds (it will take ~10s — sklearn fits at startup are the slowest
   step). Report "backend ready" with the vision_baseline_arch +
   vision_baseline_f1 + predmaint_baseline_family + rl_baseline_policy
   numbers when /health responds.

3. Start the viewer in the background:
     bash apps/web/manufacturing/serve.sh
   Wait 2s, then curl -sI http://127.0.0.1:3000/ to confirm HTTP 200.

4. Confirm all four sprint endpoints are live (one sample per sprint):
   - Sprint 1 Vision QC: GET /inspect/vision/leaderboard returns 3 archs
     (resnet50_lr_head, efficientnet_b0_rf_head, vit_small_gbm_head) each
     with per-class P/R/F1 across 4 classes (good, minor_defect,
     major_defect, safety_critical_defect).
   - Sprint 2 PredMaint: GET /predict/maintenance/leaderboard returns 3
     families (lightgbm_features, lstm_sequence, survival_forest_tte)
     across 3 windows (3, 7, 14 days).
   - Sprint 3 RL: GET /optimize/rl/leaderboard returns 3 policies
     (ppo_continuous, dqn_discrete, random_baseline) with throughput,
     defect_rate, safety_violations per policy. PPO MUST show 0 safety
     violations; Random MUST show >100.
   - Sprint 4 Agent + Drift: GET /agent/policy returns the per-task-class
     autonomy ladder; GET /drift/status/vision returns "registered: true"
     (and likewise for predmaint and rl).

Describe any algorithm you mention in your summary ONLY if you can quote
the file and function you read it from (e.g. "ResNet-50 frozen, per
`build_vision_baseline` in src/manufacturing/backend/ml_context.py").
If you are unsure which architecture backs a module, say "I did not read
the source for this — I can confirm after /analyze" rather than guess.

5. Open the viewer in my browser so I can see the value-chain banner:
     open http://127.0.0.1:3000/
   (If on Linux use xdg-open instead. If neither works, tell me to click
   http://127.0.0.1:3000/ manually.)

If ANY of steps 1–4 fails, STOP and tell me what failed. Do not try to
debug or fix the scaffold — raise your hand for the instructor.

Once green, summarise:
1. The four-layer industrial cascade: Sprint 1 Transfer-Learning vision
   QC → Sprint 2 Time-series predictive maintenance → Sprint 3 RL reflow
   oven → Sprint 4 Coordination Agent + Drift × 3 models.
2. What is PRE-BUILT (3-arch transfer-learned vision leaderboard;
   3-family × 3-window predmaint leaderboard; cached PPO/DQN/Random
   rollouts on the reflow-oven environment; agent harness with four
   tools and three autonomy modes; drift reference for all three modules;
   800 labelled boards + 432k sensor rows + 30k RL episodes + 200 safety
   images) vs what I will DECIDE tonight (vision arch choice, per-class
   thresholds × 4 classes with WSH floor on safety_critical, predmaint
   family + window, RL reward function weights × 4, agent autonomy ladder
   × 4 task classes, three retrain rules at three cadences).
3. The five Trust Plane decision moments I must hit (vision arch, per-
   class threshold incl. WSH floor, predmaint window, RL reward function,
   agent autonomy ladder + WSH safety floor).

Then stop and wait for me to open playbook/workflow-01-analyze.md and
paste the /analyze prompt from that file (which will copy the pre-
produced 01-analysis/ files as the basis).
```

When Claude Code answers — **evaluate** two things:

1. **Environment**: did the preflight checks come back green? If not, flag the instructor. Do not try to fix the scaffold.
2. **Summary**: does it correctly describe the four-layer cascade (Vision QC → PredMaint → RL → Agent+Drift)? Does it name the five decision moments? Does it correctly split Trust Plane vs. Execution Plane? If not, correct it before proceeding.

That evaluation is your first decision of the day. You are already in the Trust Plane.

**Then open `playbook/workflow-01-analyze.md`** and paste the prompt from its §1. Every other paste tonight comes from a `playbook/*.md` file — follow the `**Next file:**` pointer at the bottom of each file through all 22 files in the order laid out in `playbook/README.md`.

---

## Closing

You have everything you need. The scaffold is pre-built. The COC routine is the routine you already know. The Playbook is universal. The product is a real Singapore high-reliability electronics manufacturer in microcosm. Claude Code is your team. The decisions are yours.

By 5:30 pm you will have shipped the industrial AI chain — a transfer-learned vision QC inspector, a predictive-maintenance classifier, an RL reflow-oven controller, and a coordination agent with three drift rules — and defended a page of decisions with dollar reasoning. In Week 8 (Capstone), you do it again on YOUR own product idea (with the same Playbook and the same routine), and pitch it. By then, you will be a one-person unicorn — **because you can commission and judge ML products, not because you can code them**.

Let's ship.
