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

**The retail scaffold is pre-built.** The backend (`src/retail/backend/`), viewer (`apps/web/retail/`), datasets (`src/retail/data/`), baseline K=3 clustering run, baseline content-based recommender, and the drift monitor with reference data already registered are all up and running on your laptop before class starts. You do **not** scaffold, wire endpoints, or fix type errors tonight. The instructor did all of that.

What you still run is the full **COC routine**: `/analyze` first (to inventory what's pre-built and name the decisions still open to you), then `/todos` (to lay out the 14 Playbook phases as a tracked plan with a human gate), then `/implement` (where each of the three sprints executes a block of Playbook phases), then `/redteam` and `/codify` at the close. Week 4's students spent most of the clock scaffolding and some never reached the ML lifecycle. Week 5 fixes this by pre-building the product so you can do the lifecycle properly — **with the COC routine, not instead of it.**

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

- Open a terminal at the project root (`~/repos/training/metis`). Type `claude` to start.
- Paste the opening prompt from Section 9.
- After that, adapt the phase prompts from `PLAYBOOK.md` in your own words.
- **Reference files with the `@` prefix** — typing `@PLAYBOOK.md` in your message pulls that file's contents into the conversation. This is Claude Code syntax, not shell syntax — it works inside the `claude` session only.

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

## 6. Workshop Shape — COC Routine Over 14 Playbook Phases

Tonight runs the **full COC routine** against the 14-phase Playbook. The COC phases are the outer scaffold; the Playbook phases are the content of `/implement`. Week 4's students felt they skipped the routine because scaffolding ate the clock; this week the scaffold is pre-built so the routine gets its proper time.

### Clock table (wall-clock 2:00 pm → 5:30 pm)

Four sprints — one per paradigm in the traditional ML value chain:

| Clock     | COC phase             | Sprint / paradigm              | Playbook phases inside           | Output                                                                 |
| --------- | --------------------- | ------------------------------ | -------------------------------- | ---------------------------------------------------------------------- |
| 2:00–2:10 | (opening)             | narrative + preflight          | —                                | green viewer banner                                                    |
| 2:10–2:25 | `/analyze`            | frame the 4-module cascade     | (pre-phase)                      | `01-analysis/failure-points.md`, `assumptions.md`, `decisions-open.md` |
| 2:25–2:30 | `/todos`              | draft phases · instructor gate | —                                | `todos/active/phase_N_*.md` (13 phases; Phase 14 deferred)             |
| 2:30–3:15 | `/implement` Sprint 1 | **USML — Discover**            | Phases 1, 2, 3, 4, 5, 6, 7, 8    | Segmentation · `journal/phase_{1..8}_usml.md`                          |
| 3:15–4:00 | `/implement` Sprint 2 | **SML — Predict**              | Phases 4, 5, 6, 7, 8 (replayed)  | Churn + Conversion classifiers · `journal/phase_{4..8}_sml.md`         |
| 4:00–4:30 | `/implement` Sprint 3 | **Optimization — Decide**      | Phases 10, 11, 12                | Campaign allocator · `journal/phase_{10..12}_*.md`                     |
| 4:30–4:40 | mid-sprint injection  | PDPA red-line                  | Phase 11 + 12 re-run (allocator) | `journal/phase_11_postpdpa.md`, `phase_12_postpdpa.md`                 |
| 4:40–5:00 | `/implement` Sprint 4 | **MLOps — Monitor**            | Phase 13 × 3 models              | Drift rules · `journal/phase_13_*.md`                                  |
| 5:00–5:15 | `/redteam`            | cross-sprint audit             | Phase 7 final sweep              | `04-validate/redteam.md`                                               |
| 5:15–5:30 | `/codify` + `/wrapup` | transferable lessons           | Phase 9                          | `.claude/skills/project/week-05-lessons.md`, `.session-notes`          |

### Sprint 1 — USML · Discover (≈45 min)

**Goal**: ship a segmentation — K chosen, segments named, deployment gate signed. This is the foundation every later sprint inherits.

**Playbook phases**: 1, 2, 3 (unfolded this week), 4, 5, 6, 7, 8.

**Deliverable**: segmentation endpoints returning real assignments; segment profiles in the dashboard; 7 journal entries (Frame, Data Audit, Features, Candidates→Implications, K + 3 Floors, Red-team, Deployment gate).

### Sprint 2 — SML · Predict (≈45 min)

**Goal**: train + gate the two supervised classifiers — **churn** (P(churn_30d | customer)) and **conversion** (P(convert | customer, category)). Same leaderboard of families each time: logistic regression + random forest + gradient-boosted (ensemble-is-the-king). Both classifiers feed Sprint 3's allocator.

**Playbook phases**: 4, 5, 6, 7, 8 **replayed** (same levers as Sprint 1 but applied to an SML product — Phases 1/2/3 are shared with Sprint 1 and not re-run).

**Deliverable**: `/predict/leaderboard/churn` and `/predict/leaderboard/conversion` populated; thresholds set with cost-based justification (CAC vs touch-cost asymmetry); 5 journal entries (Candidates, Implications, Metric+Threshold, Red-team, Gate — each with `_sml` suffix).

### Sprint 3 — Optimization · Decide (≈30 min + 10 min PDPA injection)

**Goal**: ship a campaign allocator. Given segments × predicted responses × touch budget × PDPA/inventory constraints, the LP returns an allocation plan. Phase 12 acceptance asks: feasible? optimal? pathology-free? accept / re-tune / fall back / redesign?

**Playbook phases**: 10 (Objective — single vs multi + shadow prices), 11 (Constraints — hard / soft + penalties), 12 (Acceptance — LP solve + pathology detection).

**Scenario injection at 4:30** (≈workshop T+02:30): instructor fires `pdpa_redline`. Legal classifies under-18 browsing history as a PDPA §13 hard exclusion. **When it fires, you MUST re-run Phase 11 AND Phase 12 against the allocator, not against a recommender**:

1. **Re-run Phase 11** — re-classify the under-18 feature as **hard** with $220/record penalty. Write `journal/phase_11_postpdpa.md`; keep the prior pass at `journal/phase_11_constraints.md`.
2. **Re-run Phase 12** — re-solve the LP with the new hard constraint. Report shadow price (the dollar cost of compliance — expect a significant drop in expected revenue). Write `journal/phase_12_postpdpa.md`. The plan lands at `data/allocator_last_plan.json`. **Writing only the Phase 11 re-run and skipping Phase 12 is the single most common D3 failure.**

**Deliverable**: `/allocate/objective`, `/allocate/constraints`, `/allocate/solve` all live; allocator plan visible in the dashboard; 3 base journal entries (Phases 10, 11, 12) + 2 post-injection entries.

### Sprint 4 — MLOps · Monitor (≈20 min)

**Goal**: ship a drift rule **per model** (three rules, because the three artefacts drift on different signals at different cadences). Segmentation = monthly membership churn. Churn classifier = weekly calibration decay + AUC decay. Allocator = daily constraint-violation rate. One alarm cannot watch all three.

**Playbook phase**: 13 × 3.

**Deliverable**: `/drift/check` run for each of `recent_30d` and `catalog_drift` windows; `/drift/retrain_rule` called three times; 1 journal entry covering all three rules with variance-grounded thresholds, duration windows, human-in-the-loop dispositions.

### Close — `/redteam` + `/codify` + `/wrapup` (≈30 min)

**Goal**: `/redteam` for a cross-sprint audit (stability / proxy-leakage / operational-collapse across all three models), then `/codify` Playbook Phase 9 into `.claude/skills/project/week-05-lessons.md`, then `/wrapup` for `.session-notes`.

**Deliverable**: `04-validate/redteam.md`, codified skill file, session notes. These are what Week 6 inherits.

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

First, confirm the pre-provisioned environment is green:
1. Run .venv/bin/python src/retail/scripts/preflight.py and report
   the exit code plus any non-green rows. All rows should be ✓.
2. If the backend is not already running, start it with
   bash src/retail/scripts/run_backend.sh in a second terminal,
   then curl http://127.0.0.1:8000/health and confirm status=ok
   plus a baseline_silhouette around 0.34.
3. Confirm all four sprint endpoints are live:
   - Sprint 1 USML: /segment/baseline (K=3 sil≈0.34), /segment/candidates (K=2..10 sweep)
   - Sprint 2 SML: /predict/leaderboard/churn AND /predict/leaderboard/conversion
     (each returning a 3-family leaderboard with AUC, precision, recall, Brier)
   - Sprint 3 Opt: /allocate/campaigns (5 campaigns registered) AND
     GET /allocate/objective (default weights visible)
   - Sprint 4 MLOps: /drift/status/customer_segmentation (reference_set=true)
4. Confirm the viewer is up by hitting http://127.0.0.1:3000/ —
   the value-chain banner should render with 9 pipeline stages
   (Open → Analyze → Todos → USML → SML → Opt → MLOps → Redteam → Codify).

If any check fails, STOP and tell me what failed — do not try to
fix the scaffold yourself. The instructor will intervene.

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
