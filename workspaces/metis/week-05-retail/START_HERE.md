<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# START HERE — Week 5: Retail Customer Intelligence

**Version:** 2026-04-23 · **License:** CC BY 4.0

> A 3.5-hour workshop where **you commission and defend a customer-intelligence product** — segmentation, a hybrid recommender, and a drift monitor — on a pre-provisioned Arcadia Retail backend, **without writing a single line of code**. Claude Code already has the infrastructure. You run the full COC routine (`/analyze` → `/todos` → `/implement` → `/redteam` → `/codify`) against the 14-phase ML Decision Playbook. You direct, evaluate, decide, and defend.

This document is your manual for today. Read sections 0–3 before class. Keep this open in a tab throughout the session and refer back when stuck.

---

## 0. Five-Minute Orientation

### Tonight is the ML lifecycle, not the build

You inherited this project ten minutes before class. Your predecessor — Arcadia Retail's first ML hire — left last Friday. The CMO is waiting on a segmentation she can run five campaigns against. The CX Lead is waiting on churn and conversion scores she can hand to her retention team on Monday. The E-com Ops Lead is waiting on drift rules so she knows when any of it starts lying. You have until 5:30 pm to ship all three and defend every decision in front of them.

The backend, viewer, data, baseline K=3 segmentation, two pre-trained classifiers, and the drift reference are already running on your laptop — your predecessor's last commit. That is not a shortcut. That is how ML arrives in industry: you walk into a half-done project, you ship it, and you own every judgment call the previous person did not have time to make. This week it is retail. Next week you inherit a media recommender. The week after, a manufacturing anomaly detector. Eight weeks, eight inherited products, one muscle memory: **run the routine, make the calls, defend the work.**

What you still run is the full **COC routine**: `/analyze` first (inventory what your predecessor committed to and name the decisions still open), then `/todos` (lay out the 14 Playbook phases as a tracked plan with a human gate), then `/implement` (each of four sprints executes a block of Playbook phases), then `/redteam` and `/codify` at the close. Every week of this course is the same routine applied to a different inherited product.

### What you will walk away with today

1. **A deployed retail product.** Segmentation assigning every customer to a segment, a hybrid recommender live behind the pre-wired endpoint, and a drift monitor that tells you when either lies. Running at a URL you can share.
2. **A decision journal PDF.** A signed record of every ML judgment call you made today, scored on the 5-dimension rubric.
3. **A reusable ML Decision Playbook** — applied to a second domain (retail, unsupervised ML, recommender strategy) after Week 4's supervised + optimization. This is the point of the course: the Playbook transfers.
4. **A complete COC artefact set** — `01-analysis/failure-points.md`, `todos/active/phase_N_*.md`, `journal/phase_{1..13}_*.md`, `04-validate/redteam.md`, `.claude/skills/project/week-05-lessons.md`. The routine is what institutionalises the learning.

### What you will NOT do today

- Write Python, JavaScript, SQL, or any other code.
- Install libraries, configure environments, debug stack traces.
- Wire endpoints, seed data, or build UI — the product is pre-built at `src/retail/` and `apps/web/retail/`.
- Memorize "what is K-means" or "how does matrix factorisation work".

### What you **will** do

- **Paste one opening prompt** that boots the pre-built Arcadia backend and viewer, and enters `/analyze`.
- **Run the full COC routine** — `/analyze`, `/todos`, `/implement`, `/redteam`, `/codify` — against the 14 Playbook phases.
- **Read the Viewer Pane** as outputs arrive.
- **Evaluate** what Claude Code produced — was it good work? honest work? complete work?
- **Decide** the judgment calls only a human can own (how many segments, which recommender strategy, what counts as drift, what PDPA compliance looks like in practice).
- **Journal every decision** with a short memo justifying it.

### The bargain this course offers

We are not teaching you to build. We are teaching you to **commission, judge, and ship ML products as a one-person team.** Claude Code is your engineer, your data scientist, your DevOps. You are the founder. Your differentiating skill is knowing **what to ask, how to read the answer, and when to say "ship it" or "do it again."**

---

## 1. The Two Planes You Operate Across

Everything today (and every week onward) splits into two planes:

| Plane               | Who does it            | What they produce                                                               | Examples                                                                                                                                                                                                                                                                                                                                   |
| ------------------- | ---------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Trust Plane**     | You — the human        | Judgment, framing, evaluation, approval                                         | "5 segments because marketing can run 5 campaigns, and a 7-segment system is $X of setup cost with no realistic lift." "The hybrid recommender wins on diversity but the cold-start fallback has to be segment-modal-basket, not catalogue popularity." "Retrain the recommender when weekly CTR drops below 14% for 3 consecutive weeks." |
| **Execution Plane** | Claude Code + scaffold | Code, trained models, segment assignments, recommender leaderboards, dashboards | Pre-wired backend endpoints, pre-provisioned clustering sweep path, pre-wired content/collaborative/hybrid recommender variants, pre-registered drift reference data, viewer dashboard                                                                                                                                                     |

### Why this split matters

In the old world, a CMO asked a data-science team for "customer segments", waited three months, got a slide deck, and could not tell if the segments were real. In the AI-native world, **the segments are ten prompts away and the recommender is twenty prompts away** — which means the bottleneck moves to **asking the right questions and evaluating the answers**. That is the Trust Plane. That is your job.

If you cannot frame the problem, commit to metric floors before seeing the results, classify the PDPA constraint correctly, or approve the deployment — the AI is driving, not you. That is the failure mode. Tonight we train you out of it.

### The rule of thumb for today

> If the question is **what** or **how**, let Claude Code answer it.
> If the question is **which**, **whether**, **who wins and who loses**, or **is it good enough to ship** — that is yours.

---

## 2. The Product You Are Shipping: Arcadia Retail Intelligence Suite

### What it is

A customer-intelligence suite for Arcadia Retail. On the books: ~50,000 customers, ~2,000 SKUs, ~500,000 transactions/year across 5 Singapore stores + e-commerce. The workshop scaffold ships a **representative 5,000-customer / 400-SKU / 120,000-transaction sample** — fast enough to re-train live, adversarial enough to force real decisions. Cite the scaffold numbers in your journal entries; the book numbers belong in Phase 1 framing only.

**One product, four layered modules — the traditional ML value chain:**

1. **Customer Segmentation Engine** (Sprint 1 · USML · Discover). Every customer gets a behavioural segment label. Not demographic buckets — patterns in what they actually do.
2. **Response Predictors: Churn + Conversion** (Sprint 2 · SML · Predict). Two supervised classifiers trained on the segment-labelled customers. Churn = "will this customer stop buying in the next 30 days?" Conversion = "will this customer convert on a category-level offer?" Segments are features; the classifiers feed the allocator.
3. **Campaign Allocator** (Sprint 3 · Optimization · Decide). Linear-programming solver that allocates a fixed marketing budget across segments × campaigns to maximise expected revenue under constraints (touch budget, PDPA, inventory). Consumes Sprint 1 + Sprint 2 outputs.
4. **Drift Monitor × 3 models** (Sprint 4 · MLOps · Monitor). One drift signal per artefact: segment-membership churn, classifier calibration decay, allocator constraint-violation rate.

This is the cascade: **segmentation → predicted responses → allocation decisions → monitoring**. Get Sprint 1 wrong and every later sprint inherits the error. Skip Sprint 4 and you'll never know when any of the three silently stops working.

### Who uses it

- **CMO**: approves segmentation (Sprint 1), signs off on campaign map, co-owns allocator objective (Sprint 3)
- **CX Lead**: approves response predictors (Sprint 2), decides what "good" looks like for classifier thresholds
- **E-com Ops Lead**: co-owns Sprint 3 allocator, owns Sprint 4 drift + retrain / rollback

### What "shipped" looks like at 5:30 pm

- The retail viewer running at `http://localhost:3000` with the value-chain banner showing all four sprints completed
- The retail backend running locally (`src/retail/backend/`) with all endpoints live: `/segment/*`, `/predict/{churn,conversion}/*`, `/allocate/*`, `/drift/*`, `/state/*`
- A `journal.pdf` with decision memos spanning Phases 1–9 (USML) + 4–8 replay (SML) + 10–12 (Opt) + 13 (MLOps)
- A complete COC artefact set — `01-analysis/`, `todos/completed/`, `journal/`, `04-validate/`

### The business context (for framing decisions — cite these exact numbers)

- Arcadia runs 5 Singapore stores + `shop.arcadia.sg`; ~50,000 customers on the books, ~18,000 active in last 90 days, ~2,000 SKUs, ~500,000 transactions/year. **Scaffold sample: 5,000 customers / 400 SKUs / 120,000 transactions** (representative).
- Each **converted recommendation** is worth **$18** in basket lift
- Each **wasted impression** (shown, not clicked) costs **$14** in session fatigue + unsubscribe risk
- Each **wrong-segment campaign** costs **$45** per customer sent to the wrong offer
- Each **customer touch** (email/push/SMS) costs **$3** regardless of whether they engage
- Each **PDPA breach** on an under-18 personalised-history record carries **$220** per-record exposure
- Each **cold-start fallback** session (new user, no signal) costs **$8** if it defaults to catalogue popularity
- Peak season is Nov–Dec (Black Friday / Year-End); expect abnormal behaviour — do not auto-retrain on it
- Current rule-based recommender converts at **12%** click-through; the new system must beat that to justify shipping

These numbers drive every decision in Phases 1, 6, 7, 10, 11, and 13. Keep `PRODUCT_BRIEF.md` open in a tab — your journal entries will cite from that file.

---

## 3. Your Toolset — Each Explained

For every tool below, you get six answers: What is it / Why do we need it / Implications / How to use it / How to evaluate it / How to improve it.

### 3.1 Claude Code (your terminal agent)

**What is it.** An AI coding agent running in your terminal. You type natural-language requests; it reads files, writes code, runs commands against the pre-provisioned backend, and reports back.

**Why do we need it.** It is the agent that talks to the scaffold. Without it, you would be curl-ing endpoints by hand. With it, "profile the Sprint 1 segments" becomes a structured comparison rendered in the viewer in 30 seconds.

**Implications.** Because the scaffold is pre-built, your prompts this week focus on **decision-making against a running system**, not on wiring. A vague prompt still produces a plausible-but-shallow answer; a precise prompt with evaluation criteria still produces defensible work. You are still the bottleneck — just in a different place than Week 4.

**How to use it.**

- Open **one** terminal at the project root (`~/repos/training/metis`). Type `claude` to start.
- Paste the opening prompt from Section 9. Claude Code will run the preflight, start the backend in the background, start the viewer in the background, and open the viewer in your browser — you do not type any bash commands. When it reports "all four sprints green", the product is up.
- After that, adapt the phase prompts from `PLAYBOOK.md` in your own words.
- **Reference files with the `@` prefix** — typing `@PLAYBOOK.md` in your message pulls that file's contents into the conversation. This is Claude Code syntax, not shell syntax — it works inside the `claude` session only.
- You will NOT open a second terminal tonight. Everything happens inside the one `claude` session plus your browser tab.

**How to evaluate it.** After every response, ask yourself:

1. Did it actually run the work against the scaffold, or did it describe the work?
2. Did it cite specific segments, SKUs, sessions, run IDs — or did it wave at generalities?
3. Did it acknowledge uncertainty (especially around segment stability and recommender cold-start behaviour)?
4. Did it ask for clarification where your brief was ambiguous?

**How to improve it.** When the answer is thin:

- Ask _"show me the numbers, not the summary."_
- Ask _"what are three ways this segmentation could be wrong?"_
- Ask _"what did you assume that I should approve or overrule?"_
- Paste in the cost numbers and ask it to re-reason against them.

### 3.2 The Viewer Pane (your dashboard)

**What is it.** A read-only web dashboard running on your laptop. It renders the current state of the retail product: segment profile cards, recommender leaderboards, drift reports, journal entries.

**Why do we need it.** Terminal text is not how you judge a segmentation. You need to see segment sizes, feature importances, and stability overlays on a screen.

**Implications.** The Viewer is **part of the product you are defending** AND your live evaluation instrument. Dual role.

**How to use it.** Open `http://localhost:3000` in a browser tab next to your terminal. As Claude Code writes files to the workspace, the Viewer auto-refreshes.

**How to evaluate it.** After each sprint: is the information presented **decision-ready**? Does the segment card show a one-paragraph profile in plain language? Does the recommender leaderboard show precision@k, coverage, cold-start rate, diversity? If not, prompt Claude Code to improve the panel.

### 3.3 The Decision Journal

**What is it.** A simple file-backed log where you record every judgment call. Each entry: phase, decision, rationale, trade-off, reversal condition, timestamp.

**Why do we need it.** **The journal is what you are graded on** (60% of tonight's grade). By Week 8, it is a 50-page record of your ML decision-making.

**Implications.** If you decide something without journaling it, it did not happen. If your rationale fits in one line, the decision was shallow. If your reversal condition is "if data changes", name a specific signal + threshold + duration.

**How to use it.** Two ways:

- From the terminal: `metis journal add` opens an editor with a template.
- By asking Claude Code: _"Add a journal entry for my segment-count decision: 5 segments, because marketing can run 5 parallel campaigns and K=7 would cost ~$2,500 in setup with segment stability dropping below 0.80; I would drop to 4 segments if stability on next month's re-cluster drops below 0.80 for two consecutive re-clusters."_

**How to evaluate it.** Re-read each entry against the five dimensions (grading rubric):

1. Harm framing — whose cost, in named dollars?
2. Metric→cost linkage — did you tie the metric to money (ideally via a counterfactual vs the current 12% baseline)?
3. Trade-off honesty — what did you sacrifice?
4. Constraint classification — hard vs soft? (PDPA is hard.)
5. Reversal condition — what specific signal flips your mind?

**How to improve it.** If an entry scores <3 on any dimension, ask Claude Code: _"Challenge this journal entry as if you were the CMO. What would you push back on?"_ Then rewrite.

### 3.4 The retail scaffold at `src/retail/` + `apps/web/retail/` (pre-built — you do not wire it)

**What is it.** The Arcadia product, living in the monorepo alongside other products. Backend at `src/retail/backend/` with seven route groups: `/health`, `/state/*` (the progress banner's data source), `/segment/*` (Sprint 1 USML), `/predict/*` (Sprint 2 SML churn + conversion), `/recommend/*` (supporting rec endpoint; consumed by the allocator), `/allocate/*` (Sprint 3 LP), `/drift/*` (Sprint 4 × 3 models). Data at `src/retail/data/` — scaffold ships 5,000 customers / 400 SKUs / 120,000 transactions as a representative sample (full Arcadia book is ~50k/2k/500k). Viewer at `apps/web/retail/` with the value-chain banner at top and 8 module cards below. Baseline K=3 clustering pre-trained, churn + conversion classifiers pre-trained at startup, drift reference registered. `SCAFFOLD_MANIFEST.md` in your workspace tells you which paths do what.

**Why do we need it.** Because you have 3.5 hours and every minute should be on decisions, not on wiring. Everything the Playbook's 14 phases touch is already up by the time you walk in.

**Implications.** You will run `/analyze`, `/todos`, `/implement`, `/redteam`, `/codify` — the full COC routine — but you will NOT scaffold. `/analyze` inventories what is pre-built and flags the decisions still open to you. `/implement` drives each of the 14 Playbook phases through the pre-wired endpoints. If the scaffold is not green on preflight, raise your hand — the instructor will fix it, not you.

**How to use it.** Indirectly, through Claude Code. Your prompts refer to "run a clustering sweep", "evaluate the three recommender variants", "check drift against the last week of live data" — Claude Code hits the pre-wired endpoints at the paths in `SCAFFOLD_MANIFEST.md`.

**How to evaluate it.** Preflight must be green before you complete `/analyze`. If the backend is not responding on its local port, the viewer is not serving, the retail datasets under `src/retail/data/` are missing, or the drift reference is not registered — raise a hand.

**How to improve it.** You do not. If something is broken, it is the instructor's fix tonight.

### 3.5 The 14-Phase Playbook

**What is it.** A universal decision procedure for any ML-powered product. Same shape as Week 4, adapted for retail + unsupervised ML + recommender strategy selection. Full detail in `PLAYBOOK.md`.

**Why do we need it.** Because tonight is exactly that — applying the Playbook to a new domain. If the Playbook transfers, you are learning the course's core skill. If it does not, we have to fix the Playbook.

**Implications.** Keep `PLAYBOOK.md` open alongside this file. The Playbook is the detail authority for each phase; this file is the manual for the day.

### 3.6 The Orchestrator Hygiene Toolkit

Tonight Claude Code will generate a lot of text very fast. Most of it will be correct. Some of it will not. The four checks below are the discipline that catches the difference — without you needing to know any ML to apply them. You are not grading algorithms. You are grading whether Claude Code has **earned** the claim it just made.

Use this toolkit reactively. You do not run all four on every response. You watch the output for one of four signals — a technical-sounding claim, a specific number, a threshold, a word like "blocked" or "blocking" — and then you run the matching check.

#### Check 1 — "Show me the line"

**When to run it:** Claude Code names a specific technique, algorithm, library, or method as if it is a fact about the pre-built scaffold ("the segmentation uses NMF", "the recommender is collaborative filtering", "drift uses KL divergence").

**The question you ask, verbatim:**

> Show me the exact file, function, and line that proves this. Quote the line. If you have not read it, say so and mark the claim uncertain until we check together.

**Worked example.** Claude Code wrote: _"The segmentation module uses NMF clustering with 7 behavioural features, which explains the baseline silhouette of 0.34."_ You reply with the verbatim question above. Claude Code reads `src/retail/backend/ml_context.py`, comes back with: _"I was wrong. The function `train_baseline_segmentation` uses `sklearn.cluster.KMeans(n_clusters=3, random_state=42)`. NMF is used elsewhere (the collaborative recommender's matrix factorisation). I confused two modules. The silhouette of 0.34 is real; the algorithm name was wrong."_ You move on. The check took forty seconds and saved a journal entry that names the wrong algorithm — which the instructor would mark down.

**The analogy.** A journalist fact-checking a source. _"You said the contract was signed in March — show me the page of the contract with the date on it. If you did not see the contract, I am marking this as 'reported, not verified' until we find the PDF."_

#### Check 2 — "Show me the brief"

**When to run it:** Claude Code cites a specific dollar figure, percentage, count, or business metric — especially one you did not give it in your prompt.

**The question you ask, verbatim:**

> Which line of `PRODUCT_BRIEF.md` or which document did this number come from? Paste the row. If it is a calculation, show me the calculation step by step using only numbers from the brief.

**Worked example.** Claude Code wrote: _"A PDPA breach on the under-18 dataset would cost Arcadia approximately $594,000 based on the exposed records in the scaffold sample."_ You reply with the verbatim question. Claude Code responds: _"I combined $220 per under-18 record (PRODUCT_BRIEF.md §2 row 5) with an estimate of 2,700 under-18 records. The $220 is from the brief. The 2,700 is my estimate — I did not count them. I should have said 'the per-record exposure is $220; total exposure depends on how many records are affected, which I have not counted.'"_ You ask Claude Code to rewrite the line as the per-record figure plus a method for counting affected records, with the total marked pending. Your journal now cites the brief verbatim, which is what the rubric rewards.

**The analogy.** A finance director auditing a memo. _"You wrote '$594k exposure' in the summary. Show me the cell in the finance pack. If you built this number from two cells, show me both cells and the formula. I do not accept numbers that do not trace back to the source sheet."_

#### Check 3 — "Did I write that floor first?"

**When to run it:** Claude Code reports a result, then declares that result "passed" or "failed" against a threshold — and the threshold appears for the first time in the same message as the result.

**The question you ask, verbatim:**

> Where was that threshold written down **before** this run? Point me to the journal entry, the phase brief, or the prompt where I pre-registered it. If it is not there, this is a post-hoc floor and we need to set the real floor before running again.

**Worked example.** Claude Code wrote: _"The K=5 segmentation scored 0.41 silhouette, which passes the 0.4 minimum. Recommending K=5 for promotion."_ You reply with the verbatim question. Claude Code: _"I did not find a pre-registered floor. I set 0.4 after seeing the results; K=5 happened to land at 0.41. The Playbook Phase 6 (USML variant) requires three floors pre-registered BEFORE seeing the leaderboard — separation, stability, actionability."_ You stop, write your three floors in a journal stub _before_ you look at the leaderboard again, then ask Claude Code to re-score against **your** floors. If K=5 now fails your stability floor of 0.80, that is the real answer — and your journal shows you committed first and judged second. The rubric rewards this heavily (D2 metric→cost linkage).

**The analogy.** A lawyer cross-examining a witness. _"When did you decide that 'loud noise' would be your evidence of impact? Before you heard the noise, or after? If you decided after, your testimony is working backwards from the conclusion — that is not evidence, that is narration."_

#### Check 4 — "What am I blocked from?"

**When to run it:** Claude Code labels something "blocking", "blocker", "incomplete", "defect", "not working", or "gap" — anything that implies _you cannot proceed_.

**The question you ask, verbatim:**

> What exact next step can I not take because of this? Name the sprint, the phase, and the endpoint. If I can still run my next phase, this is a future task, not a blocker — relabel it.

**Worked example.** Claude Code wrote: _"BLOCKING ISSUE: the campaign allocator has never successfully solved a plan. This must be resolved before Sprint 1 can proceed."_ You reply with the verbatim question. Claude Code: _"You are right — the allocator is a Sprint 3 task (Phases 10–12), and you are currently entering Sprint 1 (segmentation, Phases 1–8). The allocator not having solved yet is the expected starting state. It is not a defect. It is a to-do in my own plan. I will relabel it as 'Sprint 3 open task, expected' instead of 'blocking'."_ You move on to Sprint 1 with full permission. A fake blocker is the most expensive kind of mistake tonight because it steals clock minutes you cannot get back. Catching it in thirty seconds is the highest-ROI check of the four.

**The analogy.** A detective following evidence. _"You said this fact 'blocks the investigation' — which specific lead can you not follow because of it? If you can still interview the next witness and visit the next scene, this fact is not a blocker, it is a note for later. Do not confuse a to-do with a roadblock."_

#### The meta-principle

**Make Claude Code show its work.** Every one of the four checks is the same move in a different key — the demand that Claude Code produce the receipt, not just the claim. Technical claim → show me the line of code. Number → show me the row of the brief. Threshold → show me it was written first. Blocker → show me the next step it blocks.

**When to apply which:** one check per triggering signal, not all four on every response. If Claude Code names a _technique_, run Check 1. If it names a _number_, run Check 2. If it compares a result to a _threshold_, run Check 3. If it uses the word _blocker_, run Check 4. If a single response does all four things, run all four — but the routine is match-the-signal, not screen-every-output. Most responses tonight will be fine. The ones that are not, these four checks will catch in under a minute each.

---

## 4. The ML Decision Playbook (detail in `PLAYBOOK.md`)

The Playbook is the **14-phase universal procedure**. Tonight you run Phases 1–13 (Fairness is Phase 14, deferred to Week 7).

**Tonight's phase unfolding vs Week 4:**

- Phase 3 (Feature Framing) is **unfolded this week**. Week 4 folded it into Phase 2. Week 5 unfolds it because pre-cluster feature selection has higher stakes than pre-model feature selection — an ethically loaded feature creates a segment that is really a proxy for a protected class.
- Phase 6 (Metric + Threshold) has **two replacements tonight**:
  - **USML variant (Sprint 1)**: three floors — separation, stability, actionability — pre-registered BEFORE seeing the leaderboard. Dollar lift via counterfactual vs the 2020 rulebook.
  - **SML variant (Sprint 2)**: read the PR curve, pick the threshold that minimises expected cost against the CAC-vs-touch-cost asymmetry (40:1 for churn), confirm calibration via Brier score.
- Phase 10 (Objective) is **replaced for the allocator** (Sprint 3). Four competing signals: expected revenue, reach, diversity/coverage, touches. Pick single vs multi-objective; defend weights with shadow prices.
- Phase 12 (Acceptance) is **replaced for the LP allocator** (Sprint 3). Check feasibility per hard constraint, optimality gap, pathologies (concentration, dead campaigns). Accept / re-tune / fall back / redesign.

Phases 4, 5, 7, 8 **replay** in Sprint 2 for the SML classifiers (producing `_sml` journal entries alongside Sprint 1's `_usml` entries). Phases 1, 2, 3 are shared across sprints — framed once, not re-run. Phase 13 runs once in Sprint 4 with THREE rules (one per model). Full phase-by-phase detail lives in `PLAYBOOK.md`.

### The five Trust Plane decision moments (read these twice)

Tonight collapses into five high-pressure decision moments. These are where the rubric has teeth.

1. **Pick K and defend in dollars** (Sprint 1, Phase 6 USML). Not "silhouette said 5". Rather: "5 because marketing can run 5 parallel campaigns; 7 costs $X in setup with no realistic lift; stability drops below 0.80 at K=7."
2. **Name each segment and declare a differentiated action per segment** (Sprint 1, Phase 5 + 6). If two segments get the same action, they are one segment with noise.
3. **Pick the SML classifier's family AND threshold with cost-based justification** (Sprint 2, Phase 4→6 replay). Ensemble is the king for tabular, but read the PR curve to set the threshold. Do it for BOTH churn and conversion; the allocator consumes both.
4. **Classify hard-vs-soft constraints when PDPA fires, AND re-run the allocator** (Sprint 3, Phase 11 + 12 post-PDPA). Re-classify under-18 browsing as a hard line with $220/record penalty AND re-solve the LP. Skipping the re-solve is the single most common D3 failure.
5. **Set three retrain rules — one per model** (Sprint 4, Phase 13). Segmentation (monthly membership churn), churn classifier (weekly calibration decay), allocator (daily constraint-violation rate). Three signals, three thresholds, three duration windows, HITL on first trigger for all.

All five are non-negotiable. The rubric scores hardest on #4 and #5 — those are where Week 4 students hit the wall.

---

## 5. ML Concepts You Need Tonight (just-in-time theory)

### 5.0 What You Will Know By 5:30 pm

Five promises the course cashes tonight. By the time the CMO, CX Lead, and Ops Lead sign off on your work, you will walk out of the room with these five capacities — and you will have them for every ML product you commission for the rest of your career.

1. **The levers of the ML lifecycle.** You know, phase by phase across the 14-phase Playbook, which decisions are yours to pull (how many segments, what counts as "good enough", which constraint is hard) and which are Claude Code's to execute (which library, which solver, which hyperparameter). You never again confuse "I don't know how" with "I don't need to know how".

2. **The major model families and when each is reasonable.** For tabular data with labels, ensemble methods (gradient-boosted trees especially) are the default — "ensemble is king". For data with no labels, you reach for K-means when the clusters are round, density-based when you want outliers flagged, hierarchical when you want nested segments. For decisions under constraints, you reach for linear programming when everything is linear, mixed-integer programming when choices are discrete, greedy approximations when the LP is too slow. You also know where each fails — K-means breaks on non-blob shapes; ensembles overfit on tiny data; LPs become infeasible under tight constraints.

3. **The evaluation charts and what they tell you.** You can read a ROC curve (classifier separation — higher area is better), a PR curve (precision against recall — used to pick a threshold), a calibration plot (are the probabilities honest, or does the model say "90% confident" when it is right 60% of the time — Brier score lower is better), a silhouette chart (how crisp the clusters are), and a PSI chart (how far the live data has drifted from training data — above 0.25 is a warning). You do not compute these. You read them, and you know what each one is entitled to tell you and what it is not.

4. **Decisions ON ML.** You can commission a model (Sprint 1 segmentation, Sprint 2 classifiers), pick a classifier threshold defended in dollars (Phase 6 SML), classify a constraint as hard vs soft with a dollar penalty (Phase 11), promote a model from staging to shadow to production (Phase 8), and defend each choice in front of the CMO, CX Lead, and Ops Lead using numbers from the cost table — not silhouette scores.

5. **Decisions WITH ML.** Given the outputs of the three models — segment labels, churn and conversion probabilities, allocator plan — you can make the business decision they feed: which campaigns go to which segments, which customers land on Monday's retention contact list, when to retrain versus when to roll back. The model output is not the answer; it is the input to your decision.

**Tied together:** you **speak ML, you do not write it**. That is the one-person-team superpower the course builds. By Week 8 you will commission, evaluate, and ship ML products across eight domains without typing a line of code — because the Playbook transfers and the four hygiene checks travel with you into every project you inherit.

For each concept: what it is, why we care, how to use it through Claude Code, how to push back.

### 5.1 Unsupervised learning (no label)

**What.** Learning patterns from data without a ground-truth label. The model "finds structure"; you decide whether the structure is real.

**Why we care.** The segmentation is unsupervised. There is no "right answer" column. Your Phase 6 metric shape changes entirely — no RMSE, no MAPE, no accuracy.

**Implications.** You commit to _floors_ on multiple signals (separation, stability, actionability), not to a single optimised number. The pre-commitment matters — post-hoc floors are always conveniently where the leaderboard winner landed.

### 5.2 Clustering families (big picture only)

You do NOT need to know the internals. You need to know when each is reasonable.

| Family            | Reasonable because                                          | Risk                                     |
| ----------------- | ----------------------------------------------------------- | ---------------------------------------- |
| **K-means style** | Fast, simple, works on round blob-shaped clusters           | Forces K; breaks on non-blob-shaped data |
| **Density-based** | Finds dense pockets, flags outliers as unassigned           | Can leave 10–25% of customers unassigned |
| **Hierarchical**  | Lets you cut the tree at different levels (nested segments) | Slow on large data; needs a cut decision |
| **Rule-based**    | Current incumbent — 5 hand-authored segments from 2020      | Does not adapt; the baseline to beat     |

Always compare against the rule-based baseline. If your clustering does not clearly beat "the existing five segments", ship the baseline and save the money.

### 5.3 Dimensionality reduction

On 40+ behavioural features, distance-based clustering finds noise. Reduce first (for preprocessing — collapses correlated features into components) OR reduce for visualisation (a 2D layout you can eyeball). Two purposes, two tools, don't conflate them.

### 5.4 Segmentation-quality signals (no label version of "accuracy")

**Separation** (plain language: "are the clusters crisp, or are they overlapping blurs?"). One common measure is the silhouette score; higher is better but the absolute number matters less than the relative comparison across K.

**Stability** (plain language: "if I re-cluster next month, do customers mostly stay put?"). One common measure is bootstrap Jaccard overlap; ≥ 0.80 is roughly "shippable". Below that, your segmentation reshuffles and the CMO cannot run a campaign on it.

**Actionability** (plain language: "can my marketing team build a different campaign for each segment, and will they recognise the segments in words?"). Not a number — a test. If two segments get the same one-line action, they are one segment with noise.

### 5.5 Recommender families

| Family            | Reasonable because                                    | Risk                                                 |
| ----------------- | ----------------------------------------------------- | ---------------------------------------------------- |
| **Content-based** | Works on product similarity; handles new SKUs; simple | Low serendipity — recommends things you'd have found |
| **Collaborative** | Works on customer similarity; high serendipity        | Cold-start struggles; needs interaction volume       |
| **Hybrid**        | Blends both signals + segment-aware cold-start        | Highest complexity; not automatically the winner     |

On a 2,000-SKU catalogue, "hybrid is always best" is not true. Let the offline evaluation decide.

### 5.6 Offline recommender evaluation (no live traffic yet)

**Precision@k** — of the top-k items we recommended, how many did the customer actually engage with? Report at k=5 and k=10 both.
**Catalogue coverage** — what fraction of SKUs ever appear in a top-10 across the held-out sessions? Low coverage kills the long tail.
**Cold-start rate** — what fraction of sessions triggered the cold-start fallback? Verify the fallback is what you declared (segment modal basket, not catalogue popularity).
**Diversity within a top-10** — how many distinct product categories are in one top-10 list on average? Low diversity = monoculture.

### 5.7 Cold-start (as product decision, not bug)

A new customer with no history is not a bug — it is most of your mobile signups in Singapore. The recommender _must_ have a declared fallback: segment modal basket (uses Sprint 1), catalogue popularity, or editorial curation. The deck says this; the Playbook enforces it; the rubric scores it.

### 5.8 Drift — three signals for three models

- **Segmentation (USML) drift** — **segment-membership churn**: fraction of customers who moved segments month-over-month. If it exceeds the training-window variance for a sustained window, re-cluster. Cadence: monthly.
- **Churn classifier (SML) drift** — **calibration decay + AUC decay**: Brier score drift + AUC drop points. A classifier can have stable AUC and drifted calibration; both matter because the allocator consumes the probability. Cadence: weekly.
- **Allocator (Opt) drift** — **constraint-violation rate + feasibility rate**: fraction of allocator runs that produce infeasibility or are overridden by ops. Cadence: daily.

Each rule: sustained signal + grounded threshold + duration window + human-in-the-loop on first trigger. Never "auto-retrain on one bad day". Seasonal windows (Nov–Dec Black Friday, Chinese New Year) are explicitly excluded from the drift baseline.

### 5.9 Linear programming (just enough to commission the allocator)

The Sprint 3 allocator is a linear program: maximise `Σ x × (P(convert) × revenue − cost)` subject to hard constraints (touch budget, PDPA exclusions, inventory) and soft constraints with dollar penalties (per-segment fatigue cap). You do not solve the LP by hand — scipy does it — but you do pull the levers: the **objective** (Phase 10: weights on revenue vs reach vs diversity), the **constraint classification** (Phase 11: hard vs soft with penalties), the **acceptance decision** (Phase 12: feasibility ✓, optimality gap small, no pathologies like one-segment-90%-concentration). When the solver tells you the shadow price of the PDPA constraint is $50,000/month, that's the dollar cost of compliance made visible.

---

## 6. The Phase Prompts You Will Paste

Every COC phase tonight has exactly one paste-ready opening prompt in this section. Paste the prompt, read the response against the evaluation in the block, then adapt the phase-by-phase Playbook prompts (in `PLAYBOOK.md`) to walk each phase within the sprint. This §6 is the COC-level entry for each phase; `PLAYBOOK.md` is the Playbook-phase-level detail.

Each of the eight blocks below has the same four parts. **Paste this** is the verbatim prompt — copy everything inside the fenced block and paste into your `claude` session. **Why this prompt is written this way** names the three-to-five design choices baked in — read it once so you understand what the prompt is protecting you from. **What to expect back** names the files or artefacts Claude Code should produce; if the response is missing one, your first follow-up is "where is X?" **Push back if you see** is the list of failure shapes — when you see one, ask the question in plain English and do not advance until Claude Code answers it.

The four hygiene guards from §3.6 are baked into every prompt below. (1) **Cite-or-cut** — every technical claim names a specific file and function. (2) **Show-the-brief** — every dollar figure quotes `PRODUCT_BRIEF.md §2`. (3) **No post-hoc thresholds** — floors and pass/fail criteria are set in your journal BEFORE seeing results. (4) **No fake blockers** — the word "blocker" only means a specific action you cannot take.

### Clock at a glance (wall-clock 2:00 pm → 5:30 pm)

| Clock     | COC phase             | Sprint / paradigm              | Playbook phases inside           | Output                                                                 |
| --------- | --------------------- | ------------------------------ | -------------------------------- | ---------------------------------------------------------------------- |
| 2:00–2:10 | (opening)             | narrative + preflight          | —                                | green viewer banner                                                    |
| 2:10–2:25 | `/analyze`            | inheritance audit              | (pre-phase)                      | `01-analysis/failure-points.md`, `assumptions.md`, `decisions-open.md` |
| 2:25–2:30 | `/todos`              | draft phases · instructor gate | —                                | `todos/active/phase_N_*.md` (13 phases + close; Phase 14 deferred)     |
| 2:30–3:15 | `/implement` Sprint 1 | **USML — Discover**            | Phases 1, 2, 3, 4, 5, 6, 7, 8    | Segmentation · `journal/phase_{1..8}_usml.md`                          |
| 3:15–4:00 | `/implement` Sprint 2 | **SML — Predict**              | Phases 4, 5, 6, 7, 8 (replayed)  | Churn + Conversion classifiers · `journal/phase_{4..8}_sml.md`         |
| 4:00–4:30 | `/implement` Sprint 3 | **Optimization — Decide**      | Phases 10, 11, 12                | Campaign allocator · `journal/phase_{10..12}_*.md`                     |
| 4:30–4:40 | mid-sprint injection  | PDPA red-line                  | Phase 11 + 12 re-run (allocator) | `journal/phase_11_postpdpa.md`, `phase_12_postpdpa.md`                 |
| 4:40–5:00 | `/implement` Sprint 4 | **MLOps — Monitor**            | Phase 13 × 3 models              | Drift rules · `journal/phase_13_*.md`                                  |
| 5:00–5:15 | `/redteam`            | cross-sprint audit             | Phase 7 final sweep              | `04-validate/redteam.md`                                               |
| 5:15–5:30 | `/codify` + `/wrapup` | transferable lessons           | Phase 9                          | `.claude/skills/project/week-05-lessons.md`, `.session-notes`          |

---

### 6.1 `/analyze` — the inheritance audit

**Paste this:**

```
I'm new to this project. Someone else built the scaffold before me — the
retail backend, viewer, datasets, baseline K=3 clustering, churn +
conversion classifiers, and drift reference are all already running on
my laptop. Before I decide anything, I need to understand what they
committed to on my behalf.

We are in the /analyze phase. The goal of /analyze tonight is NOT to
design the product — the product is pre-built. The goal is to produce
an inheritance audit: for every ML artefact the scaffold ships,
separate what is already fixed (baseline K, classifier families, drift
reference windows) from what remains MY decision (final K, segment
names, per-segment actions, classifier thresholds × 2, allocator
objective weights, PDPA classification, retrain thresholds × 3).

Produce three files under workspaces/metis/week-05-retail/01-analysis/:

1. failure-points.md — for each of the 4 modules (USML segmentation,
   SML churn + conversion, Opt allocator, MLOps drift × 3), name the
   3 most likely failure points tonight. For each failure point cite
   the specific file and function in src/retail/backend/ that the
   scaffold uses (e.g. `src/retail/backend/ml_context.py::train_baseline_segmentation`).
   If you cannot cite a file and function for a claim, delete the claim.

2. assumptions.md — list every assumption the scaffold has already
   baked in. K=3 baseline. Three-family classifier sweep (LR + RF +
   GBM). Drift reference registered. 5,000 customers / 400 SKUs /
   120k transactions. Cite each assumption to a file. For any dollar
   figure you mention, quote it verbatim from PRODUCT_BRIEF.md §2 —
   do NOT invent numbers.

3. decisions-open.md — the list of decisions still mine to make
   tonight, organized by sprint. For each decision name the Playbook
   phase that owns it (e.g. "pick final K: Sprint 1, Phase 6 USML").
   Do NOT propose values for any threshold, floor, or K — those are
   my calls in the Playbook phases. Listing the decision is your
   job; deciding it is mine.

Do NOT use the word "blocker" unless you name the specific action I
cannot take until something is resolved. "The backend is slow" is not
a blocker. "I cannot list the classifier families because
/predict/leaderboard/churn returns 503" is a blocker.

When all three files are written, stop and wait for me to run /todos.
```

**Why this prompt is written this way:**

- Opening is inheritance-aware — "someone else built the scaffold" puts you in a legacy-inheritance frame, not a greenfield frame, which is what tonight actually is.
- Cite-or-cut is explicit on `failure-points.md` and `assumptions.md` — every claim names a file-and-function, and the "delete if you can't cite" clause removes invented technical claims.
- Show-the-brief fires on dollar figures by forcing verbatim quotes from `PRODUCT_BRIEF.md §2`.
- `decisions-open.md` explicitly forbids proposing values — the scaffold's baseline is NOT your decision, and listing the decisions (not answering them) is what `/analyze` owns. Threshold-proposing leaks into Phase 6 and destroys pre-registration.
- The no-fake-blockers clause is load-bearing tonight because Claude Code will be tempted to call the ~17s NMF warm-up a "blocker" — it isn't, it's latency.

**What to expect back:**

- `01-analysis/failure-points.md` — ~1 page, 12 failure points (3 per module) each with a cited file-and-function.
- `01-analysis/assumptions.md` — ~1 page, 8–12 inherited assumptions with file citations.
- `01-analysis/decisions-open.md` — ~1 page, 10–14 decisions organized by sprint, each tagged with the owning Playbook phase.
- A closing summary naming the four-layer cascade (USML → SML → Opt → MLOps) and the five Trust Plane decision moments.
- A single sentence confirming Claude Code is stopping for `/todos`.

**Push back if you see:**

- A failure point with no file-and-function citation — ask "which file and function in `src/retail/backend/` are you referring to?"
- A dollar figure that doesn't match `PRODUCT_BRIEF.md §2` — ask "which line of PRODUCT_BRIEF.md §2 does this come from?" If it isn't in §2, it goes.
- A proposed threshold, floor, or K value anywhere in `decisions-open.md` — ask "who owns picking this value — you or me? Please remove the value; I'll set it in the Playbook phase."
- The word "blocker" without a specific action — ask "which specific action can I not take until this is resolved?"
- A summary that collapses all four modules into one description — ask "please separate the four modules; they have different owners and different failure shapes."

---

### 6.2 `/todos` — the decision roadmap

**Paste this:**

```
I'm moving from /analyze into /todos. The goal here is a tracked plan
— every Playbook phase I will run tonight as an explicit todo, so
nothing gets silently skipped when the clock gets tight. This is the
human gate before /implement; you write the plan, I approve it.

Read the three files I just produced in 01-analysis/. Read
PLAYBOOK.md §5 (the COC-over-Playbook clock) and §8 (the phase
summary & disposition table).

Create todos under workspaces/metis/week-05-retail/todos/active/. One
file per Playbook phase, named phase_N_<slug>.md. Phase 14 is
deferred to Week 7 — do NOT create a todo for it.

For each todo include:

1. Sprint it belongs to (Sprint 1 USML / Sprint 2 SML / Sprint 3 Opt
   / Sprint 4 MLOps / Close).
2. Playbook phase number and name (Phase 1 Frame, Phase 6 USML
   Metric+Threshold, etc.).
3. The single Trust Plane decision I own this phase — one sentence.
4. The endpoint(s) this phase touches (e.g. Phase 4 USML touches
   /segment/fit; Phase 11 Opt touches /allocate/constraints). Name
   them; do NOT guess — cite from SCAFFOLD_MANIFEST.md or leave
   blank.
5. The skeleton to copy from journal/skeletons/ (e.g.
   phase_6_metric_threshold.md).
6. Acceptance: which file on disk proves the phase happened.

Add a 14th todo at the end called phase_99_close.md covering /redteam
+ /codify + /wrapup; this is not a Playbook phase but it is on the
clock.

Do NOT propose floors, thresholds, or K values in any todo. Those are
my calls in each phase; the todo names the decision, not the answer.
Do NOT estimate effort in developer-days — this is one student with
Claude Code in a 3.5h workshop.

Do NOT use the word "blocker" in any todo without naming the specific
action I cannot take.

After writing the todos, list them in the order I will run them
tonight and stop. The instructor will review the plan before I enter
/implement.
```

**Why this prompt is written this way:**

- The human-gate intent is stated up front so Claude Code knows this is not implementation-ready — it's a draft for instructor review, which is the COC contract at `/todos`.
- Todos are keyed to Playbook phases 1–13, matching `PLAYBOOK.md` §8 one-for-one; this prevents invented phases or re-ordered sprints mid-session.
- Endpoint names come from `SCAFFOLD_MANIFEST.md` (cite-or-blank) — the alternative is Claude Code hallucinating endpoint paths that break at `/implement`.
- "Do NOT propose floors, thresholds, or K values" enforces no-post-hoc-thresholds at plan time; if the plan names `K=5` then the Phase 6 journal is already post-hoc.
- The 14th todo covers the `/redteam` + `/codify` + `/wrapup` block so the close isn't left off the tracked plan when time pressure hits.

**What to expect back:**

- 13 Playbook-phase todos under `todos/active/` named `phase_1_frame.md` through `phase_13_retrain.md` (skipping 14, which is deferred).
- Extra entries: `phase_11_postpdpa.md` and `phase_12_postpdpa.md` for the PDPA injection re-runs, AND `phase_{4..8}_sml.md` for the SML replay.
- A 14th `phase_99_close.md` todo for `/redteam` + `/codify` + `/wrapup`.
- An ordered list showing the execution order across Sprints 1 → 2 → 3 → 4 → Close.
- A stop signal pending instructor review.

**Push back if you see:**

- A todo that proposes a value (e.g. "pick K=5") — ask "please remove the proposed value; I own the decision, you own framing the todo."
- A Playbook phase missing from the list, or a phase appearing in the wrong sprint (e.g. Phase 10 in Sprint 2) — ask "does this match `PLAYBOOK.md` §8?"
- An endpoint path that isn't in `SCAFFOLD_MANIFEST.md` — ask "which manifest line does this endpoint come from?"
- Effort estimates in developer-days — ask "please remove developer-day estimates; there are no developers tonight."
- A missing `phase_11_postpdpa.md` / `phase_12_postpdpa.md` pair — ask "where is the PDPA re-run plan? The injection is mandatory, not optional."

---

### 6.3 `/implement` Sprint 1 — USML · Discover (segmentation)

**Paste this:**

```
I'm entering /implement Sprint 1 — USML · Discover. I'm new to this
project; someone pre-trained a K=3 baseline and committed to seven
behavioural features on my behalf. My job in this sprint is to decide
the final K, name every segment, declare a distinct marketing action
per segment, and sign the deployment gate.

Sprint 1 covers Playbook phases 1, 2, 3, 4, 5, 6, 7, 8 — all eight
phases of the USML pass. Phases 1, 2, 3 are shared across sprints;
they are framed once here and not re-run in Sprint 2. Phase 6 is
REPLACED tonight for USML: three pre-registered floors (separation,
stability, actionability), not a single accuracy metric.

We will walk phase-by-phase. For each Playbook phase in 1→8 I will
paste the phase's prompt (adapted from PLAYBOOK.md). Before I start,
I need you to:

1. Copy the Sprint 1 skeletons from journal/skeletons/ into
   workspaces/metis/week-05-retail/journal/ — one file per phase,
   named phase_{1..8}_usml.md. Leave the blanks blank; I fill them
   phase by phase. The skeleton inventory is in
   journal/skeletons/README.md.

2. Confirm the Sprint 1 endpoints are live by hitting them with a
   GET: /segment/baseline (should return k=3, silhouette≈0.3422),
   /segment/registry (should return the registry state). If either
   is not live, STOP and raise a hand — do not debug.

3. For every algorithm or model family you name in this sprint, cite
   the specific file and function you read it from (e.g. "K-means, per
   train_baseline_segmentation in src/retail/backend/ml_context.py").
   If you cannot cite a file and function, say "I did not read the
   source for this — I can confirm after I check". Do NOT name
   `AutoMLEngine` for clustering — PLAYBOOK.md §Phase 4 notes the
   scaffold uses /segment/fit directly, not AutoML.

4. For any dollar figure you state during this sprint, quote the
   exact line from PRODUCT_BRIEF.md §2 it comes from. The relevant
   retail cost terms for Sprint 1 are wrong-segment cost ($45 per
   customer) and per-customer touch cost ($3). Do NOT invent numbers.

5. Do NOT propose the floors for Phase 6 (separation, stability,
   actionability). Those are my pre-registration; I write them in
   phase_6_usml.md BEFORE seeing the Phase 4 leaderboard. If you
   propose values here, you've corrupted the pre-registration.

6. Do NOT use the word "blocker" without naming a specific action I
   cannot take.

Once skeletons are copied and endpoints confirmed live, summarise:
(a) the eight phases of this sprint and the single Trust Plane
decision each phase owns (one sentence each), (b) the three floors
I will pre-register in Phase 6, (c) the two segmentation-specific
red-team sweeps in Phase 7 (re-seed churn, drop-one-demographic
proxy test).

Then stop and wait for my Phase 1 prompt.
```

**Why this prompt is written this way:**

- Opens inheritance-aware — "someone pre-trained a K=3 baseline" frames the sprint as a judgment task over inherited work, not a build.
- Skeletons are copied up front so every phase's journal file exists before the phase starts — this prevents the "I'll write the journal at the end" failure that cost Week 4 students the rubric.
- Cite-or-cut is tightened with a concrete positive example ("K-means, per `train_baseline_segmentation` in `src/retail/backend/ml_context.py`") so Claude Code knows what good looks like.
- The AutoML prohibition is explicit because `PLAYBOOK.md` Phase 4 flags exactly this failure mode — clustering via `AutoMLEngine` raises a `ValueError` in kailash-ml 0.17.0 and costs 10 minutes.
- The no-post-hoc-thresholds guard is hard-wired: the prompt refuses floor proposals here, forcing you to own pre-registration in `phase_6_usml.md`.

**What to expect back:**

- Eight skeleton files copied to `journal/phase_{1..8}_usml.md` (plus `phase_9_codify.md` if the skeleton inventory copies it).
- A live GET against `/segment/baseline` returning the baseline silhouette ≈ 0.3422, and against `/segment/registry`.
- A written summary of the eight phases, the single decision per phase, the three Phase 6 floors (separation, stability, actionability) named by shape but NOT by value, and the three Phase 7 sweeps.
- A stop signal pending the Phase 1 walk-prompt.

**Push back if you see:**

- A floor value proposed in the summary (e.g. "silhouette ≥ 0.25") — ask "please remove the proposed value; I pre-register floors in `phase_6_usml.md`."
- `AutoMLEngine` named for clustering — ask "please re-check — `PLAYBOOK.md` Phase 4 says the scaffold uses `/segment/fit` directly."
- A dollar figure not quoted from `PRODUCT_BRIEF.md §2` — ask "please quote the exact line from §2."
- Skeletons not copied to `journal/` — ask "please copy the skeletons now so every phase has a live journal file."
- A baseline silhouette that isn't ≈ 0.3422 — ask "is the backend actually live? please re-run the GET."

---

### 6.4 `/implement` Sprint 2 — SML · Predict (churn + conversion)

**Paste this:**

```
I'm entering /implement Sprint 2 — SML · Predict. The scaffold
pre-trains TWO classifiers at startup — churn (P(no visit in next 30
days | customer)) and conversion (P((customer, category) transacts |
features)) — each on a three-family leaderboard (logistic regression,
random forest, gradient-boosted). Someone committed to that family
mix on my behalf. My job this sprint is to pick one family per
classifier and set each classifier's threshold against the cost
asymmetry.

Sprint 2 REPLAYS Playbook phases 4, 5, 6, 7, 8 — once each, covering
BOTH classifiers. Phases 1, 2, 3 are SHARED with Sprint 1 and are
NOT re-run — the frame, data audit, and feature classification from
Sprint 1 apply. Phase 6 in this sprint is the SML variant (PR curve
+ cost-based threshold + calibration), not the USML three-floor
variant from Sprint 1. If you think you are running Phase 10 at any
point in this sprint, you are in the wrong sprint — Phase 10 is
Sprint 3.

Before I start the phase walk:

1. Copy the SML skeletons from journal/skeletons/ into
   workspaces/metis/week-05-retail/journal/ as
   phase_{4..8}_sml.md — five files. See
   journal/skeletons/README.md for the inventory.

2. Confirm Sprint 2 endpoints are live with a GET:
   /predict/leaderboard/churn should return a `candidates` object
   with exactly three keys (logistic_regression, random_forest,
   gradient_boosted). Same for /predict/leaderboard/conversion. If
   either is not live, STOP and raise a hand.

3. For every family, loss function, or calibration method you name,
   cite the specific file and function in src/retail/backend/. If you
   cannot cite, say so.

4. The cost asymmetry for churn is $120 CAC-to-reacquire vs $3
   per-touch (ratio 40:1). Quote the $3 line from PRODUCT_BRIEF.md §2
   verbatim when you reference it. The $120 CAC is in PLAYBOOK.md
   Phase 6 SML — not in the brief — so cite PLAYBOOK.md for that
   number, not §2.

5. Do NOT propose the threshold for either classifier. That is my
   decision in phase_6_sml.md, set by reading the PR curve against
   the cost asymmetry — NOT by picking 0.5 because it's the default.
   If you propose a value here, the pre-registration is corrupted.

6. Do NOT use the word "blocker" without naming a specific action I
   cannot take.

Once skeletons are copied and endpoints confirmed, summarise:
(a) the five phases of this sprint (no Phase 1/2/3, no Phase 10),
(b) the two classifiers and what each feeds downstream (churn →
retention; conversion → Sprint 3 allocator, which is why its
calibration matters), (c) the curve I read to set each threshold
(PR, not ROC — churn and conversion are rare-positive problems).

Then stop and wait for my Phase 4 SML prompt.
```

**Why this prompt is written this way:**

- Opening names the two classifiers by their probability statement — not "train churn" but P(no visit in next 30 days | customer). The precision forces Phase 6 threshold reasoning to be real.
- The "if you think you are running Phase 10, you are in the wrong sprint" guard is a known Week-5 confusion — Phase 10 fires in Sprint 3, not here.
- Cost asymmetry gets a citation split: the $3 touch cost is in `PRODUCT_BRIEF.md §2`; the $120 CAC is in `PLAYBOOK.md` Phase 6 SML. Show-the-brief still fires, but with the correct source.
- The "downstream calibration matters because conversion feeds Sprint 3" line is planted here so you hear it BEFORE Phase 6 SML, not after.
- Threshold-proposal prohibition is explicit — default 0.5 is the single most common Phase 6 SML failure and scores 0/4 on D2.

**What to expect back:**

- Five skeleton files copied to `journal/phase_{4..8}_sml.md`.
- A live GET against both `/predict/leaderboard/churn` and `/predict/leaderboard/conversion` returning three-family candidates each.
- A summary naming (a) the five phases, (b) the two classifiers and their downstream consumers, (c) PR curve (not ROC) as the threshold-selection curve.
- A stop signal pending the Phase 4 SML prompt.

**Push back if you see:**

- A proposed threshold ("I'd use 0.3 for churn") — ask "please remove; I set the threshold in `phase_6_sml.md` against the PR curve."
- Phase 10 / 11 / 12 mentioned in this sprint's scope — ask "aren't those Sprint 3? Please re-check against `PLAYBOOK.md` §5."
- ROC named as the primary curve for churn or conversion — ask "aren't churn and conversion rare-positive problems? PR curve, not ROC — please re-check."
- A downstream link for conversion that ISN'T the Sprint 3 allocator — ask "where does the conversion probability get consumed? I thought the allocator."
- $120 cited to `PRODUCT_BRIEF.md §2` — ask "is $120 in §2? I think it's in `PLAYBOOK.md` Phase 6 SML."

---

### 6.5 `/implement` Sprint 3 — Optimization · Decide (LP allocator + PDPA injection)

**Paste this:**

```
I'm entering /implement Sprint 3 — Optimization · Decide. The
scaffold pre-wires a linear-programming allocator at /allocate/*
that consumes Sprint 1 segments and Sprint 2 conversion
probabilities and returns a campaign plan. Someone committed to the
objective shape (expected-revenue maximisation under constraints) on
my behalf. My job this sprint is to set the objective weights,
classify every constraint as hard or soft, then sign or reject the
solved plan.

Sprint 3 REPLACES three Playbook phases for Optimization: Phase 10
(Objective — single vs multi, shadow prices), Phase 11 (Constraints
— hard / soft + dollar penalties), Phase 12 (Solver Acceptance —
feasibility, optimality gap, pathology detection, accept / re-tune
/ fall back / redesign). Phase 12 is REPLACED for an LP; the
question is not "is accuracy high" but "is the plan feasible and
pathology-free".

CRITICAL: at roughly 4:30 tonight (~workshop T+02:30), the instructor
fires a PDPA injection. Legal classifies under-18 browsing history
as a PDPA §13 hard exclusion. When the injection fires, I MUST
re-run BOTH Phase 11 (re-classify as hard with $220/record penalty
— quote the $220 line from PRODUCT_BRIEF.md §2) AND Phase 12
(re-solve the LP with the new hard constraint; the shadow price is
the dollar cost of compliance). Skipping the Phase 12 re-run is
the single most common D3 rubric failure — do NOT let me ship only
the Phase 11 re-run.

Before I start the phase walk:

1. Copy the Sprint 3 skeletons from journal/skeletons/ into
   journal/ as phase_10_objective.md, phase_11_constraints.md,
   phase_11_postpdpa.md, phase_12_accept.md, phase_12_postpdpa.md —
   FIVE files. The two postpdpa files exist from the start; I fill
   them when the injection fires. Inventory in
   journal/skeletons/README.md.

2. Confirm Sprint 3 endpoints live with a GET: /allocate/campaigns
   (should return 5 campaigns). If not live, STOP and raise a hand.

3. For every objective term, constraint, or solver concept you name
   (shadow price, slack variable, Pareto frontier, feasibility), cite
   the file and function in src/retail/backend/ that implements it.
   If you cannot cite, say so.

4. Every dollar figure I use this sprint comes from PRODUCT_BRIEF.md
   §2. Relevant: $18 basket lift per converted click, $14 per wasted
   impression, $45 per wrong-segment customer, $3 per touch, $220
   per under-18 PDPA exposure, $8 per cold-start session. Quote the
   line. Do NOT invent.

5. Do NOT propose objective weights, penalty values, or the
   hard/soft classification for any constraint. Those are my calls
   in phase_10_objective.md and phase_11_constraints.md. If you
   propose values, the classification is corrupted.

6. When the PDPA injection fires, do NOT let me move on until both
   phase_11_postpdpa.md AND phase_12_postpdpa.md are written and
   /allocate/solve has been re-run under the new hard constraint.
   "Wrote the Phase 11 re-run" alone is the rubric trap — the LP
   plan in data/allocator_last_plan.json must also change.

7. Do NOT use the word "blocker" without naming a specific action.

Once skeletons are copied and endpoints confirmed, summarise:
(a) the three phases of this sprint and the single Trust Plane
decision each phase owns, (b) the four pathologies Phase 12
detects (concentration, dead campaigns, boundary cases, sensitivity
flip), (c) the exact sequence when PDPA fires — re-classify in
Phase 11, re-solve in Phase 12, report the shadow price in dollars.

Then stop and wait for my Phase 10 prompt.
```

**Why this prompt is written this way:**

- PDPA injection is baked in up front — the prompt lists it as CRITICAL and names the exact failure mode (writing Phase 11 but not re-solving Phase 12), which is the highest-scored rubric trap of the night per `PRODUCT_BRIEF.md §4.3` and `PLAYBOOK.md` Phase 12.
- Show-the-brief for the $220 PDPA line is mandatory — the under-18 classification only has rubric teeth if the penalty is sourced from the brief, not from memory.
- "The LP plan in `data/allocator_last_plan.json` must also change" is the concrete disk-level proof that the Phase 12 re-run actually fired, preventing the "journal entry exists but LP wasn't re-solved" failure.
- Objective-weight and constraint-classification proposals are forbidden — these two sets of values are where the Trust Plane lives in Sprint 3, and pre-baked values corrupt the student's calibration conversation with the CMO.
- The four pathologies are enumerated so you have a checklist when Phase 12 returns — "feasible" alone is not enough.

**What to expect back:**

- Five skeleton files copied to `journal/` — including empty `phase_11_postpdpa.md` and `phase_12_postpdpa.md` held ready for the injection.
- A live GET against `/allocate/campaigns` returning five entries.
- A summary of the three phases, the four pathologies Phase 12 checks, and the exact PDPA sequence (re-classify → re-solve → report shadow price).
- A stop signal pending the Phase 10 prompt.
- (Later, mid-sprint at ~4:30) a Phase 11 re-classification AND a Phase 12 re-solve with a different `data/allocator_last_plan.json`.

**Push back if you see:**

- A proposed objective weight or penalty value — ask "please remove; I own these values in `phase_10_objective.md` / `phase_11_constraints.md`."
- $220 not quoted from `PRODUCT_BRIEF.md §2` — ask "please quote the $220 line from §2."
- After the PDPA injection, a written `phase_11_postpdpa.md` but no updated `data/allocator_last_plan.json` — ask "was `/allocate/solve` re-run? The plan file doesn't look different."
- A "feasible plan" claim with no pathology check — ask "did you check concentration, dead campaigns, boundary, and sensitivity? Feasible alone isn't shippable."
- A shadow-price figure stated without a dollar unit — ask "shadow price of what, in dollars?"

---

### 6.6 `/implement` Sprint 4 — MLOps · Monitor (drift × 3 models)

**Paste this:**

```
I'm entering /implement Sprint 4 — MLOps · Monitor. The scaffold
pre-registered drift reference data on my behalf. My job this sprint
is to set THREE retrain rules — one per model — because the three
models I just shipped drift on different signals at different
cadences. Someone cannot watch segmentation, churn classifier, and
allocator with a single alarm; the cadences and signals are different.

Sprint 4 runs Playbook Phase 13 × 3. One journal entry covering all
three rules — phase_13_retrain.md — with three sub-sections, not
three separate files.

The three rules, in shape:

- Segmentation (USML): monthly segment-membership churn. One
  customer who moves segments month-to-month is noise; 10% of
  customers moving is drift.
- Churn classifier (SML): weekly calibration error + AUC decay. A
  classifier can have stable AUC and drifted calibration; both
  matter because Sprint 3's allocator consumes the probability
  directly.
- Allocator (Opt): daily constraint-violation rate + feasibility
  rate. If the LP starts producing infeasible plans or ops starts
  overriding them, something upstream broke.

Before the phase walk:

1. Copy the Sprint 4 skeleton from journal/skeletons/ into
   journal/ as phase_13_retrain.md. See
   journal/skeletons/README.md.

2. Confirm Sprint 4 endpoints live. GET
   /drift/status/customer_segmentation should return
   "reference_set": true. If not, STOP and raise a hand — do NOT
   attempt to re-seed the drift reference; that is the scaffold's
   responsibility.

3. For every drift signal you name (PSI, Jaccard, Brier,
   constraint-violation rate), cite the file and function in
   src/retail/backend/ that computes it. If you cannot cite, say
   so.

4. I will ground every threshold in historical variance, not round
   numbers. "15% because the rolling-weekly variance has its 95th
   percentile at 12%" scores 4/4 on D5. "15% because it feels big"
   scores 1/4. If you propose a threshold without a variance
   grounding, the rule is post-hoc.

5. Do NOT propose the thresholds for any of the three rules. The
   threshold, the duration window, and the HITL vs auto disposition
   are mine. Your job is to run /drift/check against the two windows
   (recent_30d and catalog_drift) and report the observed variance
   so I can ground my thresholds in it.

6. Nov–Dec (Black Friday / Year-End) is explicitly excluded from
   the segmentation baseline per PRODUCT_BRIEF.md §2. Peak-season
   spikes are seasonality, not drift — quote the line.

7. Do NOT use "auto-retrain" phrasing. Retrain is a human decision
   on signal; the monitoring system reports, the human pulls the
   trigger.

8. Do NOT use the word "blocker" without naming a specific action.

Once the skeleton is copied and endpoints confirmed, summarise:
(a) the three rules by model with the signal each uses, (b) the
two /drift/check windows I will run (recent_30d and catalog_drift),
(c) the Phase 13 rubric row — signal + threshold + duration window
+ HITL + seasonal exclusion = 4/4 on D5.

Then stop and wait for my Phase 13 prompt.
```

**Why this prompt is written this way:**

- Up front: three rules, three cadences, one alarm doesn't work — this preempts the single-rule rubric failure flagged in `PLAYBOOK.md` Phase 13 and `PRODUCT_BRIEF.md §4.4`.
- Variance-grounded thresholds are load-bearing for D5 — the prompt names the 4/4-vs-1/4 scoring pattern verbatim so Claude Code cannot claim ignorance.
- "Do NOT attempt to re-seed the drift reference" prevents the known trap where Claude Code tries to re-register reference data and the real issue is scaffold health.
- "No auto-retrain phrasing" enforces the `.claude/rules/agent-reasoning.md` principle that retrain decisions stay with the human — the monitor reports; it doesn't decide.
- The Nov–Dec seasonal exclusion line is explicitly cited from `PRODUCT_BRIEF.md §2` — without it, the first Black Friday trigger silently retrains on known seasonality.

**What to expect back:**

- One skeleton file copied: `journal/phase_13_retrain.md`.
- A live GET against `/drift/status/customer_segmentation` returning `"reference_set": true`.
- Two `/drift/check` runs (one per window — `recent_30d` and `catalog_drift`) returning observed variance that you can use to ground thresholds.
- A summary of three rules × signals, the two check windows, and the D5 rubric row.
- A stop signal pending the Phase 13 prompt.

**Push back if you see:**

- A proposed threshold without variance grounding — ask "what's the 95th-percentile of historical variance for this signal? ground the number or remove it."
- A single combined rule ("retrain when any of the three signals fires") — ask "don't the three models have different cadences? please separate."
- "Auto-retrain" phrasing — ask "who pulls the retrain trigger — the system or me? please re-frame as signal → operator."
- Missing Nov–Dec exclusion — ask "does this rule exclude peak season? please quote the `PRODUCT_BRIEF.md §2` Nov–Dec line."
- An attempt to re-register the drift reference — ask "isn't the reference already registered by the scaffold? please don't re-seed; check `/drift/status/customer_segmentation` again."

---

### 6.7 `/redteam` — cross-sprint stress test

**Paste this:**

```
I'm entering /redteam. All four sprints are done. My job here is to
stress the three shipped models AS A SYSTEM — not each model in
isolation, because the whole point of the cascade (segmentation →
predicted responses → allocation decisions → monitoring) is that
failure in one poisons every later layer.

Produce workspaces/metis/week-05-retail/04-validate/redteam.md with
three sections — one per failure mode, cross-cutting across all
three models:

1. STABILITY. Re-seed the segmentation (Sprint 1) with 3 different
   random seeds. For each seed, trace what changes in Sprint 2
   (does the churn classifier's top-5 feature importance change?
   does the conversion classifier's calibration drift?) and in
   Sprint 3 (does the LP plan in data/allocator_last_plan.json
   change segment-by-segment allocations by more than 10%?). Rank
   findings by dollar severity using PRODUCT_BRIEF.md §2 costs —
   quote the lines.

2. PROXY LEAKAGE. Drop postal_district AND age_band from the
   Sprint 1 feature set and re-cluster. Count how many customers
   change segments. Re-train the churn classifier without these
   features — does its AUC drop? Re-solve the allocator with the
   proxy-dropped segments — does the expected revenue change? If
   the cascade's output changes more than 5% in dollars, the
   original segmentation was demographic in disguise, and every
   later layer inherited that disguise.

3. OPERATIONAL COLLAPSE. Filter the data to post-Black-Friday
   shapes (volume spike + mix shift). Re-cluster: does any segment
   shrink below 2% of customers? Re-run the churn classifier: does
   calibration error blow past the threshold I set in Phase 6 SML?
   Re-solve the allocator: is the plan still feasible? Report
   dollar impact per finding.

For every algorithm, model, or metric you name, cite the file and
function in src/retail/backend/ it lives in. If you cannot cite,
say so — do NOT guess.

For every dollar figure, quote the PRODUCT_BRIEF.md §2 line. Do NOT
invent.

Do NOT propose new thresholds mid-red-team. If you find that
stability = 0.74 under re-seed, the finding is "below my pre-
registered 0.80 floor — this is a Phase 8 deployment gate failure".
The finding is NOT "let me propose 0.70 as the new floor". Floors
were set before results; red-team measures against them, it does
not move them.

Do NOT use the word "blocker" without naming a specific action I
cannot take. "The segmentation is unstable" is not a blocker. "I
cannot ship the allocator because its inputs reshuffle every week"
is a blocker — name the specific ship action that's blocked.

When done, rank every finding by severity in dollars, tag each
finding as (a) accept (accepted risk), (b) mitigate (action needed
before ship), or (c) re-do (a phase must re-run). Then stop — I
decide disposition per finding.
```

**Why this prompt is written this way:**

- Cross-cutting, not per-model — the rubric for `/redteam` is specifically about the cascade, which is where real retail production fails.
- Three named sections match the three USML-specific red-team sweeps from `PLAYBOOK.md` Phase 7 (re-seed, proxy, operational collapse) — plus explicitly traced through Sprints 2 and 3 so the cascade angle is enforced.
- The "floors were set before results" line guards against post-hoc threshold movement — if Claude Code wants to lower the floor to pass red-team, the whole pre-registration collapses.
- "Cannot ship the allocator because its inputs reshuffle every week" is a concrete example of what a real blocker looks like, so you have a template.
- Disposition triage — accept / mitigate / re-do — is structured so you own the call, not Claude Code.

**What to expect back:**

- `04-validate/redteam.md` with three sections (stability, proxy leakage, operational collapse), each with cross-sprint trace.
- A ranked finding list with dollar severity and accept/mitigate/re-do tags.
- Every technical claim cited to a file and function.
- Every dollar figure quoted from `PRODUCT_BRIEF.md §2`.
- A stop signal pending your disposition call.

**Push back if you see:**

- A finding about Sprint 1 with no trace into Sprints 2 or 3 — ask "how does this segmentation finding propagate? the whole point is the cascade."
- A proposed new floor ("stability = 0.74; I suggest lowering to 0.70") — ask "my Phase 6 floor was 0.80 and it's below that. This is a Phase 8 failure, not a floor adjustment."
- An invented dollar figure — ask "please quote from `PRODUCT_BRIEF.md §2`."
- "Blocker: segmentation unstable" with no specific action — ask "which ship action is blocked?"
- A finding with no file-and-function citation — ask "which file computes this metric?"

---

### 6.8 `/codify` — Phase 9 (transferable lessons)

**Paste this:**

```
I'm entering /codify — Playbook Phase 9. /redteam is done, the
dispositions are journaled. Before I close the laptop I need to
separate lessons that transfer to any future ML product from
lessons that only apply to retail + USML + SML + Opt + MLOps. This
is what Week 6, Week 7, Week 8 students inherit; thin or generic
lessons here mean the course doesn't compound across weeks.

Three transferable lessons, two domain-specific. Five total — the
Codify budget. Each lesson names the near-miss it prevents — a
specific thing I almost got wrong tonight, not a platitude.

Produce:

1. .claude/skills/project/week-05-lessons.md — the five lessons
   with their near-misses. Three transferable at the top, two
   domain-specific below, clearly labelled. Each lesson is a
   paragraph, not a sentence; "be careful with PDPA" is not a
   lesson, "when a regulatory constraint fires mid-sprint, the
   re-run is the LP re-solve not just the journal re-classification"
   is a lesson.

2. Append the three transferable lessons to PLAYBOOK.md's "Appendix
   — Transferable lessons accumulating through the term" section
   under Week 5. Leave the Week 4 entries alone.

3. journal/phase_9_codify.md — the journal entry naming the five
   lessons and my near-miss for each.

Then run /wrapup to write workspaces/metis/week-05-retail/.session-notes
covering: what was shipped, which journal entries exist, what Week 6
inherits, any deferred items (Phase 14 Fairness is the big one).

For every lesson, cite the specific journal entry, Playbook phase,
or red-team finding that motivated it (e.g. "near-miss from
phase_12_postpdpa.md — I almost skipped the LP re-solve and kept
only the Phase 11 re-classification"). If you cannot cite, the
lesson is fabricated.

Do NOT invent dollar figures in the lessons. If a lesson quotes a
number, that number comes from PRODUCT_BRIEF.md §2 (quote the
line) or from a concrete journal entry I wrote tonight (cite the
file).

Do NOT propose lessons I didn't live tonight. "Always run a
fairness audit" is not this week's lesson — Phase 14 is deferred.
Lessons come from near-misses I actually had.

Do NOT use "blocker" without a specific action.

When all three files are written and /wrapup is done, stop. The
session is over; the next session reads the notes.
```

**Why this prompt is written this way:**

- 3+2 budget is from `PLAYBOOK.md` Phase 9 — any more and the lessons dilute; any fewer and the near-misses go unnamed.
- Near-miss requirement is the highest-leverage framing — "things that went smoothly" is not a lesson; "things I almost got wrong" is.
- Each lesson MUST cite — a journal entry, a Playbook phase, or a red-team finding. This prevents fabricated lessons from leaking into the appendix and contaminating Week 6.
- The "don't propose lessons I didn't live" clause stops Claude Code from pattern-matching a generic "always run a fairness audit" lesson that you did NOT actually live tonight (Phase 14 is deferred).
- `/wrapup` is chained so session notes are written as part of close, not as a forgotten afterthought — per `.claude/rules/journal.md` and the wrapup command contract.

**What to expect back:**

- `.claude/skills/project/week-05-lessons.md` with 3 transferable + 2 domain-specific lessons, each a paragraph with a cited near-miss.
- `PLAYBOOK.md` Appendix updated under "Week 5" with the three transferable lessons.
- `journal/phase_9_codify.md` written per the skeleton.
- `.session-notes` written covering ship status, journals, Week 6 inheritance, and deferred items.
- A stop signal — session over.

**Push back if you see:**

- A lesson with no cited journal entry or finding — ask "which journal entry or red-team finding motivated this lesson? if you can't cite, please remove."
- A generic platitude ("be careful with data quality") — ask "what's the specific near-miss from tonight? rewrite with the near-miss named."
- A Phase 14 fairness lesson — ask "we deferred Phase 14 to Week 7; this wasn't a lesson I lived tonight. Please remove or replace."
- A dollar figure not tied to `PRODUCT_BRIEF.md §2` or a journal entry — ask "which line of §2, or which journal entry, does this number come from?"
- Transferable lessons written only to the session journal and not appended to `PLAYBOOK.md` — ask "please append to the Playbook appendix; Week 6 students read the Playbook, not my session journal."

---

The eight blocks above are the COC-level entries — one paste per phase. The Playbook-phase-level prompts you use to walk each sprint live in `PLAYBOOK.md`: open the Playbook to the phase you are in, read its "Prompt template" and retail-sidebar, adapt it in your own words, and paste. These §6 prompts boot the phase; `PLAYBOOK.md` runs it.

---

## 7. How You Are Graded

Two layers, weighted 60/40.

### Layer 1 — Decision Journal (60%)

Each journal entry is scored on 5 dimensions, 0 / 2 / 4 each:

| Dim                        | 0                            | 2                         | 4                                                                                                        |
| -------------------------- | ---------------------------- | ------------------------- | -------------------------------------------------------------------------------------------------------- |
| **D1 Harm framing**        | No stakeholders named        | Names one cost            | Quantifies asymmetry in named dollars ($18 vs $14 = 1.3:1 on rec uplift; $45 vs $3 on segment targeting) |
| **D2 Metric→cost linkage** | Metric chosen without reason | Reason named              | Reason is a dollar figure or counterfactual-lift vs the current 12% baseline                             |
| **D3 Trade-off honesty**   | Picks winner, ignores loser  | Names what was sacrificed | Quantifies the sacrifice (e.g. "lost 4% coverage to gain 2% precision@5")                                |
| **D4 Constraint classify** | Unclear hard/soft            | Labelled correctly        | Penalty (in dollars) + reasoning included (PDPA $220/record is hard; $3 touch cost is soft)              |
| **D5 Reversal condition**  | "If data changed"            | Names a signal            | Names signal + threshold + duration window                                                               |

Average across all today's entries. Target: ≥ 3.0 on average to pass.

### Layer 2 — Product Shipped (40%)

Binary checks:

- [ ] Dashboard loads at `http://localhost:3000`
- [ ] Segmentation endpoints return real data (not `{"status":"ok"}` stubs)
- [ ] Recommender endpoints return real data
- [ ] Drift endpoints return a meaningful report
- [ ] `journal.pdf` exports cleanly

Each = 20% of the product grade; partial credit for partial functionality.

---

## 8. When You Get Stuck

Escalation ladder (try each before the next):

1. **Re-prompt Claude Code more precisely.** Nine times out of ten, stuck = vague prompt. Add the cost numbers. Add the phase context. Add the evaluation criteria.
2. **Check this document** (§3 for tools, §4 for playbook shape, §5 for concepts).
3. **Check `PLAYBOOK.md`** for the detailed phase you are running.
4. **Ask a neighbor** — compare prompts.
5. **Flag the instructor** — wave, don't shout.

### Common traps (pre-populated from Week 5 design)

- **"USML has no label, so what's the 'accuracy'?"** → There isn't one, and asking for one is the trap. Sprint 1 scores on three floors (separation, stability, actionability), not on a single optimised number. Commit to the floors BEFORE you see the leaderboard — post-hoc floors score 1/4 on metric-cost linkage.
- **"PDPA is a guideline, right?"** → No. PDPA red-lines are **hard** constraints. The under-18 browsing-history rule is $220 per record exposure; misclassifying it as soft scores 1/4 on D4 and ships a product that is literally illegal. When the injection fires at ~4:30, re-classify the feature as hard AND re-run Phase 12 against the allocator — not just the journal entry.
- **"Two of my segments get the same marketing action — should I keep them both?"** → No. If marketing treats them the same, they are one segment with noise. Either collapse to a lower K or defend the difference in dollars. "Statistical separation" without a distinct action is decoration.
- **"Ensemble is always best, so I'll pick the GBM."** → For tabular data with labels, yes — ensemble is the king. But you still read the PR curve to set the threshold, and you still check calibration (Brier). A GBM that wins on AUC but is miscalibrated produces probabilities the allocator mis-uses. Run calibration per subgroup in Phase 7; recalibrate with Platt/isotonic if needed.
- **"Claude Code said it ran the clustering but I see nothing in the dashboard."** → It probably described the work. Re-prompt: _"Show me the files you wrote, run the sweep against the pre-provisioned scaffold now, and point me to the segment leaderboard on disk."_
- **"The drift check returned 'no reference set'."** → The reference data is pre-registered by the scaffold. Do NOT re-seed. Ask Claude Code to read the drift-status endpoint and confirm the reference is active; if it isn't, that is a scaffold bug and the instructor fixes it, not you.
- **"Claude Code is trying to pip-install a recommender library or an ML framework."** → Stop it. The scaffold has three pre-wired recommender variants behind `/recommend/compare`, three pre-trained SML classifier families on `/predict/leaderboard/{churn,conversion}`, and the LP allocator at `/allocate/solve`. Every capability you need tonight is an endpoint, not a library import. If Claude Code says "let me install X", re-prompt: "use the pre-wired endpoint instead".
- **"I'm in Sprint 2 and Phase 10 comes next, right?"** → No. Sprint 2 is the SML classifier replay — Phases 4, 5, 6, 7, 8 applied to churn + conversion (`_sml` journal entries). Sprint 3 is where Phases 10, 11, 12 fire on the allocator. If you jump to Phase 10 during Sprint 2, you have mis-mapped the clock.
- **"PDPA fired at 4:30 — that's Sprint 3, so I only re-run the Phase 11 classification, right?"** → No. The injection demands BOTH a Phase 11 re-classification (the constraint is now hard) AND a Phase 12 re-solve against the allocator. `journal/phase_11_postpdpa.md` without `journal/phase_12_postpdpa.md` scores 0 on D3 (trade-off honesty).

---

## 9. Your Opening Prompt

Open a terminal at the **project root** (`~/repos/training/metis`). Type `claude` to start. Paste this exactly:

```
The active workspace is workspaces/metis/week-05-retail/.
Read these files from the workspace:
- workspaces/metis/week-05-retail/PRODUCT_BRIEF.md
- workspaces/metis/week-05-retail/PLAYBOOK.md
- workspaces/metis/week-05-retail/START_HERE.md

I am a student running tonight's Week 5 retail workshop.

The product (Arcadia Retail Intelligence Suite) is pre-provisioned under
src/retail/ (backend + data) and apps/web/retail/ (viewer). You will NOT
scaffold, wire endpoints, or install libraries.

We WILL still run the full COC routine — /analyze, /todos, /implement,
/redteam, /codify — because that's the institutional muscle memory we
are building. The 14-phase ML Decision Playbook is the CONTENT of
/implement tonight, not a replacement for it.

Boot the pre-provisioned environment FOR ME (I will not run bash myself).
Execute these steps in order inside this session; start long-running
processes in the background so you can continue. Report progress aloud
so I can see you're alive during the ~17s NMF warm-up.

1. Run the preflight check:
     .venv/bin/python src/retail/scripts/preflight.py
   Expect exit 0, all rows ✓. Report any non-green rows.

2. Start the backend in the background:
     bash src/retail/scripts/run_backend.sh
   Poll curl -sf http://127.0.0.1:8000/health every 2 seconds until it
   responds (it will take ~17s — the collaborative NMF pre-fit is the
   slowest step). Report "backend ready" with the baseline_silhouette
   number (should be ≈0.3422) when /health responds.

3. Start the viewer in the background:
     bash apps/web/retail/serve.sh
   Wait 2s, then curl -sI http://127.0.0.1:3000/ to confirm HTTP 200.

4. Confirm all four sprint endpoints are live (one sample per sprint):
   - Sprint 1 USML: GET /segment/baseline returns a body with "k": 3
     and "silhouette" near 0.3422.
   - Sprint 2 SML: GET /predict/leaderboard/churn returns a body with a
     "candidates" object holding exactly three keys
     (logistic_regression, random_forest, gradient_boosted).
   - Sprint 3 Opt: GET /allocate/campaigns returns a body with 5
     entries under "campaigns".
   - Sprint 4 MLOps: GET /drift/status/customer_segmentation returns
     "reference_set": true.

Describe any algorithm you mention in your summary ONLY if you can
quote the file and function you read it from (e.g. "K-means, per
`train_baseline_segmentation` in src/retail/backend/ml_context.py").
If you are unsure which algorithm backs a module, say "I did not read
the source for this — I can confirm after /analyze" rather than guess.

5. Open the viewer in my browser so I can see the value-chain banner:
     open http://127.0.0.1:3000/
   (If on Linux use xdg-open instead. If neither works, tell me to
   click http://127.0.0.1:3000/ manually.)

If ANY of steps 1–4 fails, STOP and tell me what failed. Do not try to
debug or fix the scaffold — raise your hand for the instructor.

Once green, summarise:
1. The four-layer product cascade: Sprint 1 USML segmentation
   → Sprint 2 SML churn + conversion classifiers → Sprint 3
   Optimization allocator (LP) → Sprint 4 MLOps drift × 3 models.
2. What is PRE-BUILT (baseline K=3 at silhouette 0.34; churn +
   conversion classifiers pre-trained at startup with 3-family
   leaderboards; drift reference registered; 5k customers,
   400 SKUs, 120k transactions) vs what I will DECIDE tonight
   (K, segment names, per-segment actions, classifier family +
   threshold × 2, allocator objective weights, PDPA constraint
   classification, drift thresholds × 3 models).
3. The five Trust Plane decision moments I must hit (pick K,
   name segments, classifier threshold × 2, PDPA re-classify +
   LP re-solve, three retrain rules).
4. The COC-over-Playbook clock (from PLAYBOOK.md §5) — so we
   both know when /analyze ends and /todos starts.

Then stop and wait for me to run /analyze.
```

When Claude Code answers — **evaluate** two things:

1. **Environment**: did the preflight checks come back green? If not, flag the instructor. Do not try to fix the scaffold.
2. **Summary**: does it correctly describe the four-layer cascade (USML → SML → Opt → MLOps)? Does it name the five decision moments? Does it correctly split Trust Plane vs. Execution Plane? If not, correct it before proceeding.

That evaluation is your first decision of the day. You are already in the Trust Plane.

---

## Closing

You have everything you need. The scaffold is pre-built. The COC routine is the routine you already know. The Playbook is universal. The product is a real Singapore omnichannel retailer in microcosm. Claude Code is your team. The decisions are yours.

By 5:30 pm you will have shipped the whole ML value chain — a segmentation (USML), two classifiers (SML), an allocator (Optimization), and three drift rules (MLOps) — and defended a page of decisions with dollar reasoning. In Week 6, you do it again on a new domain (media + content) with the same Playbook and the same routine. By Week 8, you will be a one-person unicorn — **because you can commission and judge ML products, not because you can code them**.

Let's ship.
