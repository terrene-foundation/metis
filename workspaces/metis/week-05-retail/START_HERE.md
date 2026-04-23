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

A customer-intelligence suite for Arcadia Retail (5 stores + e-commerce, ~50,000 customers, ~2,000 SKUs, ~500,000 transactions per year). **One product, three layered modules that build on each other:**

1. **Customer Segmentation Engine** (Sprint 1, required — the foundation). Every customer gets a behavioural segment label. Not demographic buckets — patterns in what they actually do.
2. **Hybrid Recommender** (Sprint 2, required — uses the segmentation for cold-start). Given a customer and a product page, returns a ranked list of SKUs. For customers with no history, it falls back to the modal basket of that customer's Sprint 1 segment.
3. **Shopping Advisor** (Sprint 3 stretch — grounds retrieval in segment). A RAG-powered assistant that answers customer questions with citations, re-ranking by the customer's segment label so a bargain-hunter and a luxury-buyer see different top results for the same query.

This is the cascade: **segmentation quality → recommender cold-start quality → advisor relevance**. Get the top wrong and every layer below it inherits the error.

### Who uses it

- **CMO**: approves segmentation, signs off on campaign map
- **CX Lead**: approves recommender strategy, decides what "good" looks like on product pages
- **E-com Ops Lead**: tracks live performance, owns retrain / rollback decisions

### What "shipped" looks like at 3:30 pm

- The retail viewer running at `http://localhost:3000` (served from `apps/web/retail/`)
- The retail backend running locally (out of `src/retail/backend/`) with segmentation train/profile, recommender train/predict, and drift check/status endpoints returning real data
- A `journal.pdf` in your workspace with all of today's decision memos
- A complete COC artefact set in `workspaces/metis/week-05-retail/` — `01-analysis/`, `todos/active/` (plus `todos/completed/` as each phase finishes), `journal/`, `04-validate/`

### The business context (for framing decisions — cite these exact numbers)

- Arcadia runs 5 Singapore stores + `shop.arcadia.sg`; ~50,000 customers, ~18,000 active in the last 90 days, ~2,000 SKUs, ~500,000 transactions per year
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

**What is it.** The Arcadia product, living in the monorepo alongside other products. Backend at `src/retail/backend/` (endpoints for segmentation train/profile, recommender train/predict, drift status/check). Data at `src/retail/data/` (~50,000 customers, ~2,000 SKUs, two years of transaction + browsing). Viewer at `apps/web/retail/` (dashboard + leaderboards + drift chart). Baseline K=3 clustering already trained, baseline content-based and collaborative recommender variants already wired, drift monitor already has reference data registered. `SCAFFOLD_MANIFEST.md` in your workspace tells you which paths do what.

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
- Phase 6 (Metric + Threshold) is **replaced**. No label, no "accuracy". The Week 5 shape is three floors — separation, stability, actionability — with dollar lift computed via counterfactual (what do we save / gain vs the current rule-based 12% system).
- Phase 10 (Objective) is **replaced for the recommender**. Four competing signals: click-through, revenue, catalogue diversity, serendipity. Pick a framing and defend the weights.
- Phase 12 (Acceptance) is **replaced**. Offline evaluation: precision@k, coverage, cold-start rate, diversity. Accept / re-tune / fall back / redesign.

All other phases (1, 2, 4, 5, 7, 8, 9, 11, 13) keep their Week 4 shape with retail-specific prompts. Full phase-by-phase detail — trust-plane question, prompt template, evaluation checklist, journal schema, common failure modes — lives in `PLAYBOOK.md`. Do not duplicate it here; jump there when you run a phase.

### The five Trust Plane decision moments (read these twice)

Tonight collapses into five high-pressure decision moments. These are where the rubric has teeth.

1. **Pick K and defend in dollars** (Phase 6). Not "silhouette said 5". Rather: "5 because marketing can run 5 parallel campaigns; 7 costs $X in setup with no realistic lift, and stability drops below 0.80 at K=7 on the hold-out month."
2. **Name each segment and declare a differentiated action per segment** (Phase 5 + 6). If two segments get the same action, they are one segment with noise.
3. **Choose the recommender strategy with an explicit cold-start disposition** (Phase 10 + 12). Collaborative, content-based, or hybrid — and for new customers, say what happens: segment modal basket (uses Sprint 1), catalogue popularity, or editorial curation.
4. **Declare what goes into the RAG corpus and what stays out** (Advisor stretch). PDPA, legal, staleness — every exclusion has a reason.
5. **Set the grounding-failure fallback** (Advisor stretch). Says "I don't know", falls back to popular, or escalates to a human.

If you ship tonight with any of the first three unjudged, the rubric will catch it.

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

### 5.8 Drift (for segments and for the recommender)

**Segment-assignment drift**: fraction of customers who moved segments week-over-week or month-over-month. If it exceeds the training-window variance for a sustained window, re-cluster.

**Recommender CTR decay**: week-over-week click-through rate. If it drifts back toward the old rule-based 12% baseline for a sustained window, investigate — are categories losing conversion, is the cold-start rate creeping up, are segments drifting underneath?

**Retraining trigger**: sustained signal + grounded threshold + duration window + human-in-the-loop on first trigger. Never "auto-retrain on one bad day".

### 5.9 RAG (if you reach Sprint 3 stretch)

Retrieval-Augmented Generation. The LLM searches a knowledge base (catalogue, pricing, stock, return policy) before answering. Your decisions: what goes in the corpus (PDPA boundaries), what stays out (customer reviews, competitor comparisons, stale prices), and what the advisor does when the corpus cannot support the answer ("I don't know", popular fallback, or escalate).

---

## 6. Workshop Shape — COC Routine Over 14 Playbook Phases

Tonight runs the **full COC routine** against the 14-phase Playbook. The COC phases are the outer scaffold; the Playbook phases are the content of `/implement`. Week 4's students felt they skipped the routine because scaffolding ate the clock; this week the scaffold is pre-built so the routine gets its proper time.

### Clock table (wall-clock 2:00 pm → 5:30 pm)

| Clock     | COC phase                 | Playbook phases inside        | Output                                                                |
| --------- | ------------------------- | ----------------------------- | --------------------------------------------------------------------- |
| 2:00–2:10 | `/analyze`                | (pre-phase inventory)         | `01-analysis/failure-points.md`, `01-analysis/assumptions.md`         |
| 2:10–2:15 | `/todos`                  | — (human gate)                | `todos/active/phase_N_*.md` (14 phases as todos; instructor approves) |
| 2:15–3:15 | `/implement` — Sprint 1   | Phases 1, 2, 3, 4, 5, 6, 7, 8 | `journal/phase_{1..8}_*.md`                                           |
| 3:15–3:45 | `/implement` — Sprint 2   | Phases 10, 11, 12             | `journal/phase_{10..12}_*.md`                                         |
| 3:45–4:00 | `/implement` — mid-sprint | scenario inject: PDPA         | `journal/phase_11_postpdpa.md`, `journal/phase_12_postpdpa.md`        |
| 4:00–5:00 | `/implement` — Sprint 3   | Phase 13                      | `journal/phase_13_*.md` + drift report                                |
| 5:00–5:20 | `/redteam`                | Phase 7 final sweep           | `04-validate/redteam.md`                                              |
| 5:20–5:30 | `/codify` + `/wrapup`     | Phase 9                       | `.claude/skills/project/week-05-lessons.md`, `.session-notes`         |

### Sprint 1 — Segment (inside `/implement`, ≈60 min)

**Goal**: ship a segmentation — with K chosen, segments named, and the deployment gate signed.

**Playbook phases**: 1, 2, 3 (unfolded this week), 4, 5, 6, 7, 8.

**Deliverable**: segmentation endpoints returning real segment assignments; segment profiles visible in the dashboard; 7 journal entries (Frame, Data Audit, Features, Segment Selection, K + Floors, Red-team, Deployment gate).

### Sprint 2 — Recommend (inside `/implement`, ≈45 min including mid-sprint re-run)

**Goal**: ship a chosen recommender strategy with an explicit cold-start disposition, all four offline metrics reported, and the PDPA constraint correctly classified.

**Playbook phases**: 10, 11, 12.

**Scenario injection mid-sprint** (≈ workshop T+01:45): instructor fires `pdpa-under-18`. Legal flags that using browsing history of any customer under 18 for personalised recommendations violates PDPA. **When it fires, you MUST re-run Phase 11 AND Phase 12, and write a journal entry for each re-run phase**:

1. **Re-run Phase 11** — re-classify the under-18 browsing-history feature as a hard exclusion (from "soft preference, use with caution" to "hard, $220/record exposure"). Write `journal/phase_11_postpdpa.md`. The prior classification stays as `journal/phase_11_constraints.md`.
2. **Re-run Phase 12** — re-evaluate the recommender variants with the new hard exclusion in force. The new plan is saved to `data/recommender_plan_postpdpa.json`; the pre-injection plan is preserved as `data/recommender_plan_prepdpa.json`. Write `journal/phase_12_postpdpa.md`. **Submitting only the Phase 11 re-run and skipping Phase 12 is the most common D3 (trade-off honesty) failure.**

**Deliverable**: recommender endpoints live; offline metrics table (precision@k, coverage, cold-start rate, diversity) visible in the dashboard; 3 base journal entries (Phases 10, 11, 12) + 2 post-injection journal entries.

### Sprint 3 — Monitor (inside `/implement`, ≈60 min)

**Goal**: ship a drift monitor with a retrain rule (per-module — segmentation and recommender have different cadences).

**Playbook phase**: 13.

**Scenario injection**: instructor fires the `segment-drift` event (or recommender CTR decay, depending on injection choice).

**Deliverable**: drift endpoints live; drift chart visible in the dashboard; 1 journal entry (retrain rule, separate per module).

**Stretch (only if Sprint 3 has 15+ minutes left)**: the Shopping Advisor compressed-phases run. See `PLAYBOOK.md` § "Optional: The Shopping Advisor".

### Close — `/redteam`, `/codify`, `/wrapup` (≈30 min)

**Goal**: run `/redteam` for a cross-sprint audit (stability / proxy-leakage / operational-collapse sweep against the full segmentation + recommender surface), then `/codify` Playbook Phase 9 into `.claude/skills/project/week-05-lessons.md`, then `/wrapup` to write `.session-notes`.

**Deliverable**: `04-validate/redteam.md`, codified skill file, session notes. These are what carry the learning into Week 6.

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
- **"Cold-start just happens — there's a default somewhere, right?"** → Cold-start is a product decision, not a fallback accident. You declare in Phase 10 what happens for a new customer with no history (segment modal basket, catalogue popularity, or editorial curation), and Phase 12 verifies the declared behaviour is what actually runs. The cascade is: Sprint 1's segmentation → Sprint 2's cold-start fallback → Sprint 3's (optional) advisor ranking. Skipping the cold-start declaration silently breaks the cascade.
- **"PDPA is a guideline, right?"** → No. PDPA red-lines are **hard** constraints. The under-18 browsing-history rule is $220 per record exposure; misclassifying it as soft scores 1/4 on constraint classification and ships a product that is literally illegal. When the injection fires at T+02:05, re-classify the feature as hard AND re-run Phase 12 — not just the journal entry.
- **"Two of my segments get the same marketing action — should I keep them both?"** → No. If marketing treats them the same, they are one segment with noise. Either collapse to a lower K or defend the difference in dollars. "Statistical separation" without a distinct action is decoration.
- **"Hybrid is always best, so I'll pick hybrid."** → No. On a 2,000-SKU catalogue, hybrid's complexity is not automatically worth it. Let Phase 12's precision@k / coverage / cold-start-rate / diversity numbers decide.
- **"Claude Code said it ran the clustering but I see nothing in the dashboard."** → It probably described the work. Re-prompt: _"Show me the files you wrote, run the sweep against the pre-provisioned scaffold now, and point me to the segment leaderboard on disk."_
- **"The drift check returned 'no reference set'."** → The reference data is pre-registered by the scaffold. Do NOT re-seed. Ask Claude Code to read the drift-status endpoint and confirm the reference is active; if it isn't, that is a scaffold bug and the instructor fixes it, not you.
- **"Claude Code is trying to pip-install a recommender library."** → Stop it. The retail scaffold has three pre-wired recommender variants behind a single evaluation endpoint. Re-prompt in terms of "evaluate the three recommender variants against the held-out session data", not "find and use a recommender library".

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
3. Confirm the baseline K=3 segmentation model and the pre-baked
   K-sweep (K=2..10) are both live by hitting
   /segment/baseline and /segment/candidates.
4. Confirm the drift monitor has reference data registered by
   hitting /drift/status/customer_segmentation.

If any check fails, STOP and tell me what failed — do not try to
fix the scaffold yourself. The instructor will intervene.

Once green, summarise:
1. The three-layer product cascade
   (segmentation → recommender cold-start → optional advisor).
2. What is PRE-BUILT (baseline K=3 at silhouette 0.34, content
   recommender, drift reference, 5k customers, 400 SKUs,
   120k transactions) vs what I will DECIDE tonight
   (K, segment names, per-segment actions, recommender strategy,
   cold-start disposition, PDPA classification, drift thresholds).
3. The five Trust Plane decision moments I must hit.
4. The COC-over-Playbook clock (from PLAYBOOK.md §"The Playbook
   runs inside /implement") — so we both know when /analyze
   ends and /todos starts.

Then stop and wait for me to run /analyze.
```

When Claude Code answers — **evaluate** two things:

1. **Environment**: did the five preflight checks come back green? If not, flag the instructor. Do not try to fix the scaffold.
2. **Summary**: does it correctly describe the three-layer cascade (segmentation → recommender cold-start → optional advisor)? Does it name the five decision moments? Does it correctly split Trust Plane vs. Execution Plane? If not, correct it before proceeding.

That evaluation is your first decision of the day. You are already in the Trust Plane.

---

## Closing

You have everything you need. The scaffold is pre-built. The COC routine is the routine you already know. The Playbook is universal. The product is a real Singapore omnichannel retailer in microcosm. Claude Code is your team. The decisions are yours.

By 5:30 pm you will have shipped a segmentation, a recommender, and a drift monitor — and defended a page of decisions with dollar reasoning — on a product that was pre-built so you could spend your time on the ML lifecycle, not on the wiring. In Week 6, you do it again on a new domain (media + content) with the same Playbook and the same routine. By Week 8, you will be a one-person unicorn — **because you can commission and judge ML products, not because you can code them**.

Let's ship.
