<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# START HERE — Week 5: Retail Customer Intelligence

**Version:** 2026-04-23 · **License:** CC BY 4.0

> A 3.5-hour workshop where **you commission and defend a customer-intelligence product** — segmentation, a hybrid recommender, and a drift monitor — on a pre-provisioned Arcadia Retail backend, **without writing a single line of code**. Claude Code already has the infrastructure. You run the full COC routine (`/analyze` → `/todos` → `/implement` → `/redteam` → `/codify`) against the 14-phase ML Decision Playbook. You direct, evaluate, decide, and defend.

Read sections 0–3 before class. Keep this open in a tab throughout the session.

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

## 3. The Orchestrator Hygiene Toolkit

Tonight Claude Code will generate a lot of text very fast. Most of it will be correct. Some of it will not. The four checks below are the discipline that catches the difference — without you needing to know any ML to apply them.

Two quick definitions before the checks, because three of the four use them:

- **Floor** = a pass/fail line. "Silhouette must be at least 0.25" is a floor. A floor is only honest if you wrote it down _before_ you saw the result.
- **Pre-registration** = writing a floor in your journal before running the test. It is the difference between measuring and moving the goalposts.

Use this toolkit reactively. You do not run all four on every response. You watch the output for one of four signals — a technical-sounding claim, a specific number, a threshold, a word like "blocked" or "blocking" — and then you run the matching check.

### The Viewer: Your Live Dashboard

The viewer at `http://localhost:3000` boots automatically at step 3 of the opening prompt (the `bash apps/web/retail/serve.sh` step). It auto-refreshes as Claude Code writes artifacts to the workspace — you do not need to reload it manually. It is read-only: all commanding happens via Claude Code in your terminal, never through the viewer interface.

Dual role: it is both your **live evaluation instrument** (did that phase actually run, or did CC just describe it?) and **the product the CMO, CX Lead, and Ops Lead will look at when they walk over at 5:30 pm**. Treat it seriously.

Glance at it after every phase. If nothing new rendered on the value-chain banner or the module cards, Claude Code described the work instead of running it. Re-prompt: "Show me the files you wrote, run the sweep now, and point me to the output on disk."

### Check 1 — "Show me the line"

**When to run it:** Claude Code names a specific technique, algorithm, library, or method as if it is a fact about the pre-built scaffold.

**The question you ask, verbatim:**

> Show me the exact file, function, and line that proves this. Quote the line. If you have not read it, say so and mark the claim uncertain until we check together.

**Worked example.** When you ran the opening prompt, `/health` returned `customers: 5000, baseline_k: 3`. An hour later Claude Code writes: _"The scaffold holds 10,000 customers and the baseline K is 5, per the startup configuration."_ You ask the verbatim question. Claude Code reads the source files, comes back: _"I was wrong. The scaffold loads 5,000 customers and the baseline K is 3. I confused tonight's scaffold with a larger dataset I have seen elsewhere."_ You move on.

**The analogy.** A journalist fact-checking a source. "You said the contract was signed in March — show me the page of the contract with the date on it."

### Check 2 — "Show me the brief"

**When to run it:** Claude Code cites a specific dollar figure, percentage, or business metric — especially one you did not give it in your prompt.

**The question you ask, verbatim:**

> Which line of `PRODUCT_BRIEF.md` or which document did this number come from? Paste the row. If it is a calculation, show me the calculation step by step using only numbers from the brief.

**The analogy.** A finance director auditing a memo. "You wrote '$594k exposure' — show me the cell in the finance pack. If you built this number from two cells, show me both cells and the formula."

### Check 3 — "Did I write that floor first?"

**When to run it:** Claude Code reports a result, then declares that result "passed" or "failed" against a threshold — and the threshold appears for the first time in the same message as the result.

**The question you ask, verbatim:**

> Where was that threshold written down **before** this run? Point me to the journal entry, the phase brief, or the prompt where I pre-registered it. If it is not there, this is a post-hoc floor and we need to set the real floor before running again.

**The analogy.** A lawyer cross-examining a witness. "When did you decide that 'loud noise' would be your evidence of impact? Before you heard the noise, or after?"

### Check 4 — "What am I blocked from?"

**When to run it:** Claude Code labels something "blocking", "blocker", "incomplete", "defect", "not working", or "gap".

**The question you ask, verbatim:**

> What exact next step can I not take because of this? Name the sprint, the phase, and the endpoint. If I can still run my next phase, this is a future task, not a blocker — relabel it.

**The analogy.** A detective following evidence. "Which specific lead can you not follow because of this? If you can still interview the next witness, this fact is not a blocker."

### The meta-principle

**Make Claude Code show its work.** Every one of the four checks is the same move in a different key — the demand that Claude Code produce the receipt, not just the claim. Technical claim → show me the line of code. Number → show me the row of the brief. Threshold → show me it was written first. Blocker → show me the next step it blocks.

When to apply which: one check per triggering signal, not all four on every response. If Claude Code names a _technique_, run Check 1. If it names a _number_, run Check 2. If it compares a result to a _threshold_, run Check 3. If it uses the word _blocker_, run Check 4.

---

## 4. How to Use This Workshop

Five pointers for the session:

- **Read this file once** — §0–§3 above are your pre-class reading. You do not need to re-read them during the workshop. Keep the tab open for reference.
- **Open `playbook/README.md` for run-order navigation** — that file is your table of contents for the session. Every playbook file has a `**Next file:**` pointer in §6; follow it.
- **Open playbook files in order** — each is self-contained. Paste §1, check §2, look up §3 if confused, read §4 for 30 seconds, use §5 to ask CC for a grounded explanation if needed, check §6 and move on.
- **Use `playbook/appendix/` for deep concept reference** — when the in-file §4 quick-reference is not enough, open `playbook/appendix/README.md`, find the concept in the alphabetical index, and open the file.
- **Ask Claude Code with the in-file §5 template when you need project-grounded explanations** — the §5 prompt tells CC to read our codebase and journal before answering. That grounds the explanation in Arcadia's actual state, not a generic example.

---

## 5. How You Are Graded

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

## 6. When You Get Stuck

Escalation ladder (try each before the next):

1. **Re-prompt Claude Code more precisely.** Nine times out of ten, stuck = vague prompt. Add the cost numbers. Add the phase context. Add the evaluation criteria.
2. **Check `playbook/README.md`** for run-order and the current file's §4 quick reference.
3. **Check `playbook/appendix/`** for the deeper concept treatment.
4. **Ask a neighbor** — compare prompts.
5. **Flag the instructor** — wave, don't shout.

### Common traps

- **"USML has no label, so what's the 'accuracy'?"** — There isn't one. Sprint 1 scores on three pre-registered floors (separation, stability, actionability). Commit to the floors BEFORE you see the leaderboard.
- **"PDPA is a guideline, right?"** — No. PDPA red-lines are **hard** constraints. The under-18 browsing-history rule is $220 per record exposure. When the injection fires at ~4:30, re-classify the feature as hard AND re-run Phase 12 against the allocator — not just the journal entry.
- **"Two of my segments get the same marketing action — should I keep them both?"** — No. If marketing treats them the same, they are one segment with noise.
- **"Ensemble is always best, so I'll pick the GBM."** — For tabular data with labels, yes — ensemble is the king. But you still read the PR curve to set the threshold, and you still check calibration (Brier). A GBM that wins on AUC but is miscalibrated produces probabilities the allocator mis-uses.
- **"Claude Code said it ran the clustering but I see nothing in the dashboard."** — It probably described the work. Re-prompt: "Show me the files you wrote, run the sweep against the pre-provisioned scaffold now, and point me to the segment leaderboard on disk."
- **"The drift check returned 'no reference set'."** — The reference data is pre-registered by the scaffold. Do NOT re-seed. Ask Claude Code to read the drift-status endpoint and confirm the reference is active; if it isn't, that is a scaffold bug and the instructor fixes it, not you.
- **"I'm in Sprint 2 and Phase 10 comes next, right?"** — No. Sprint 2 is the SML classifier replay — Phases 4, 5, 6, 7, 8 applied to churn + conversion. Sprint 3 is where Phases 10, 11, 12 fire on the allocator.
- **"PDPA fired at 4:30 — I only need to re-run Phase 11, right?"** — No. The injection demands BOTH a Phase 11 re-classification AND a Phase 12 re-solve against the allocator. Missing the Phase 12 re-solve scores 0 on D3.

---

## 7. Your Opening Prompt

Open a terminal at the **project root** (`~/repos/training/metis`). Type `claude` to start. Paste this exactly:

```
The active workspace is workspaces/metis/week-05-retail/.
Read these files from the workspace:
- workspaces/metis/week-05-retail/PRODUCT_BRIEF.md
- workspaces/metis/week-05-retail/START_HERE.md
- workspaces/metis/week-05-retail/playbook/README.md

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

Then stop and wait for me to open playbook/workflow-01-analyze.md
and paste the /analyze prompt from that file.
```

When Claude Code answers — **evaluate** two things:

1. **Environment**: did the preflight checks come back green? If not, flag the instructor. Do not try to fix the scaffold.
2. **Summary**: does it correctly describe the four-layer cascade (USML → SML → Opt → MLOps)? Does it name the five decision moments? Does it correctly split Trust Plane vs. Execution Plane? If not, correct it before proceeding.

That evaluation is your first decision of the day. You are already in the Trust Plane.

**Then open `playbook/workflow-01-analyze.md`** and paste the prompt from its §1. Every other paste tonight comes from a `playbook/*.md` file — follow the `**Next file:**` pointer at the bottom of each file through all 22 files in the order laid out in `playbook/README.md`.

---

## Closing

You have everything you need. The scaffold is pre-built. The COC routine is the routine you already know. The Playbook is universal. The product is a real Singapore omnichannel retailer in microcosm. Claude Code is your team. The decisions are yours.

By 5:30 pm you will have shipped the whole ML value chain — a segmentation (USML), two classifiers (SML), an allocator (Optimization), and three drift rules (MLOps) — and defended a page of decisions with dollar reasoning. In Week 6, you do it again on a new domain (media + content) with the same Playbook and the same routine. By Week 8, you will be a one-person unicorn — **because you can commission and judge ML products, not because you can code them**.

Let's ship.
