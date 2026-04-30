<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# START HERE — Week 6: Multi-Modal Content Moderation

**Version:** 2026-04-30 · **License:** CC BY 4.0

> A 3.5-hour workshop where **you commission and defend a multi-modal content-moderation product** — image moderator (CNN), text moderator (Transformer), fusion moderator (CLIP-style), and three drift monitors — on a pre-provisioned MosaicHub backend, **without writing a single line of code**. Claude Code already has the infrastructure. You run the full COC routine (`/analyze` → `/todos` → `/implement` → `/redteam` → `/codify`) against the 14-phase ML Decision Playbook. You direct, evaluate, decide, and defend.

Read sections 0–3 before class. Keep this open in a tab throughout the session.

---

## 0. Five-Minute Orientation

### Tonight is the deep-learning value chain, not the build

You inherited this project ten minutes before class. Your predecessor — MosaicHub's first ML T&S hire — left last Friday after a near-miss CSAM incident escalated to the CEO. The Head of T&S is waiting on auto-remove thresholds she can defend to the board. The Head of Engineering is waiting on retrain rules per modality so she can explain to her on-call team when to wake up and when to wait. Legal Counsel is waiting on a hard-constraint table she can hand to IMDA on Monday. You have until 5:30 pm to ship all three and defend every decision in front of them.

The backend, viewer, 80,000 labelled posts, baseline CNN (transfer-learned ResNet head), baseline transformer text classifier (fine-tuned BERT-class), fusion-moderator stub, and drift reference for all three models are already running on your laptop — your predecessor's last commit. That is not a shortcut. That is how ML arrives in industry: you walk into a half-done project, you ship it, and you own every judgment call the previous person did not have time to make. This week it is content moderation. Last week it was retail. The week before, supply chain. Eight weeks, eight inherited products, one muscle memory: **run the routine, make the calls, defend the work.**

What you still run is the full **COC routine**: `/analyze` first (inventory what your predecessor committed to and name the decisions still open), then `/todos` (lay out the 14 Playbook phases as a tracked plan with a human gate), then `/implement` (each of four sprints executes a block of Playbook phases), then `/redteam` and `/codify` at the close. Every week of this course is the same routine applied to a different inherited product.

### What you will walk away with today

1. **A deployed moderation product.** Image moderator returning per-class scores on every uploaded image, text moderator returning per-class scores on every caption, fusion moderator catching cross-modal memes, drift monitors watching all three. Running at a URL you can share.
2. **A decision journal PDF.** A signed record of every ML judgment call you made today, scored on the 5-dimension rubric.
3. **A reusable ML Decision Playbook** — applied to a third domain (content moderation, deep learning, multi-modal AI) after Week 4's supervised + optimization and Week 5's USML + recommender. This is the point of the course: the Playbook transfers.
4. **A complete COC artefact set** — `01-analysis/failure-points.md`, `todos/active/phase_N_*.md`, `journal/phase_{1..13}_*.md`, `04-validate/redteam.md`, `.claude/skills/project/week-06-lessons.md`. The routine is what institutionalises the learning.

### What you will NOT do today

- Write Python, JavaScript, SQL, or any other code.
- Install libraries, configure environments, debug stack traces.
- Wire endpoints, seed data, or build UI — the product is pre-built at `src/media/` and `apps/web/media/`.
- Memorize "what is backpropagation" or "how does CLIP work internally".

### What you **will** do

- **Paste one opening prompt** that boots the pre-built MosaicHub backend and viewer, and enters `/analyze`.
- **Run the full COC routine** — `/analyze`, `/todos`, `/implement`, `/redteam`, `/codify` — against the 14 Playbook phases.
- **Read the Viewer Pane** as outputs arrive.
- **Evaluate** what Claude Code produced — was it good work? honest work? complete work?
- **Decide** the judgment calls only a human can own (what counts as harmful, where the auto-remove line goes, single-modality vs joint, who handles cultural context, when to retrain).
- **Journal every decision** with a short memo justifying it.

### The bargain this course offers

We are not teaching you to build. We are teaching you to **commission, judge, and ship ML products as a one-person team.** Claude Code is your engineer, your data scientist, your DevOps. You are the founder. Your differentiating skill is knowing **what to ask, how to read the answer, and when to say "ship it" or "do it again."**

---

## 1. The Two Planes You Operate Across

Everything today (and every week onward) splits into two planes:

| Plane               | Who does it            | What they produce                                                                  | Examples                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------- | ---------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Trust Plane**     | You — the human        | Judgment, framing, evaluation, approval                                            | "Auto-remove threshold 0.85 on hate-speech because $320 FN cost vs $15 FP cost = 21:1, but CSAM-adjacent threshold is 0.40 because IMDA $1M ceiling, not cost-balanced." "Late-fusion architecture because the cross-modal coverage gain is worth $X but joint-embedding is 3× compute and we cannot afford it tonight." "Retrain text moderator weekly, not daily, because slang volatility is bursty not monotonic." |
| **Execution Plane** | Claude Code + scaffold | Code, trained models, per-class metrics, fusion outputs, drift reports, dashboards | Pre-wired backend endpoints, pre-trained CNN with frozen ResNet head, pre-trained BERT-class text classifier, pre-built fusion stub (early + late variants), pre-registered drift reference, viewer dashboard                                                                                                                                                                                                          |

### Why this split matters

In the old world, a Head of T&S asked an engineering team for "AI moderation", waited six months, got a model that classified at 75% accuracy, and could not tell whether 75% was good enough or where the model failed. In the AI-native world, **the per-class PR curves are ten prompts away and the fusion moderator is twenty prompts away** — which means the bottleneck moves to **asking the right questions and evaluating the answers**. That is the Trust Plane. That is your job.

If you cannot frame what counts as harmful, commit to threshold floors before seeing the results, classify the IMDA constraint correctly, or approve the deployment — the AI is driving, not you. That is the failure mode. Tonight we train you out of it.

### The rule of thumb for today

> If the question is **what** or **how**, let Claude Code answer it.
> If the question is **which**, **whether**, **who wins and who loses**, or **is it good enough to ship** — that is yours.

---

## 2. The Product You Are Shipping: MosaicHub Content Moderation Suite

### What it is

A multi-modal content moderation suite for MosaicHub. On the books: ~5 million MAU, ~2 million text+image posts/day, ~100,000 video uploads/day across SG, MY, ID, PH, TH. The workshop scaffold ships a **representative 80,000-labelled-post sample** (24k image-bearing + 56k text-bearing + 8k multi-modal memes) — fast enough to fine-tune live, adversarial enough to force real decisions. Cite the scaffold numbers in your journal entries; the book numbers belong in Phase 1 framing only.

**One product, four layered modules — the multi-modal value chain:**

1. **Image Moderator** (Sprint 1 · CNN · See). Every uploaded image gets per-class scores (NSFW / violence / weapons / CSAM-adjacent / safe). Frozen ResNet backbone with fine-tuned 5-class head — transfer learning, not training from scratch.
2. **Text Moderator** (Sprint 2 · Transformer · Read). Every caption / comment / DM gets per-class scores (hate-speech / harassment / threats / self-harm-encouragement / safe). Fine-tuned BERT-class encoder. Three-family leaderboard (BERT + RoBERTa + zero-shot LLM baseline).
3. **Fusion Moderator** (Sprint 3 · Multi-Modal · Decide). CLIP-style joint embedding that catches the cross-modal harm Sprint 1 + Sprint 2 individually rate as safe. The cute-puppy + "destroy all humans" meme is the canonical adversarial case.
4. **Drift Monitor × 3 models** (Sprint 4 · MLOps · Monitor). Three rules per artefact, three cadences (image weekly / text daily / fusion per-incident), because the three modalities drift on different signals.

This is the cascade: **image → text → fusion → monitoring**. Get Sprint 1 wrong and the fusion moderator inherits the error. Skip Sprint 4 and you'll never know when any of the three silently stops working.

### Who uses it

- **Head of T&S**: approves moderation policy + auto-remove thresholds (Sprint 1, 2), signs off on fusion architecture (Sprint 3)
- **Head of Engineering**: tracks live model performance, owns retrain / rollback for any of the three (Sprint 4)
- **Legal Counsel**: signs off on IMDA-mandatory hard constraints, owns audit trail
- **Reviewer Ops Lead**: owns the human reviewer queue, sets SLA, co-owns Sprint 3 queue allocator

### What "shipped" looks like at 5:30 pm

- The media viewer running at `http://localhost:3000` with the value-chain banner showing all four sprints completed
- The media backend running locally (`src/media/backend/`) with all endpoints live: `/moderate/image/*`, `/moderate/text/*`, `/moderate/fusion/*`, `/drift/*`, `/state/*`
- A `journal.pdf` with decision memos spanning Phases 1–9 (Vision) + 4–8 replay (Text) + 10–12 (Fusion + queue allocator) + 13 (MLOps × 3 models)
- A complete COC artefact set — `01-analysis/`, `todos/completed/`, `journal/`, `04-validate/`

### The business context (for framing decisions — cite these exact numbers)

- MosaicHub: ~5M MAU, ~2M text+image posts/day, ~100K video uploads/day, regulated under SG Online Safety Act 2023. **Scaffold sample: 80,000 labelled posts** (24k image / 56k text / 8k multi-modal memes).
- Each **false negative** (harmful content left up, then user-reported) costs **$320** in regulator complaint risk + lawsuit defense
- Each **false positive** (legitimate content auto-removed) costs **$15** in creator trust + appeal-handling
- Each **human reviewer-minute** costs **$22** (queue cost — drives Phase 11 queue allocator)
- Each **CSAM non-takedown** carries **$1,000,000** IMDA fine + CEO-level reputational cost
- Each **cold-start misclassification** on a novel content type costs **$8** per piece
- **GPU inference**: $0.03 per 1,000 image classifications served
- Peak adversarial periods: election cycles + major news events (DO NOT auto-retrain on these)
- Current rule+keyword system: 31% recall on harmful content, 4% FP rate — the floor the new system must clear to justify shipping

These numbers drive every decision in Phases 1, 6, 7, 10, 11, and 13. Keep `PRODUCT_BRIEF.md` open in a tab — your journal entries will cite from that file.

---

## 3. The Orchestrator Hygiene Toolkit

Tonight Claude Code will generate a lot of text very fast. Most of it will be correct. Some of it will not. The four checks below are the discipline that catches the difference — without you needing to know any deep learning to apply them.

Two quick definitions before the checks, because three of the four use them:

- **Floor** = a pass/fail line. "Per-class F1 must be at least 0.70 on hate-speech" is a floor. A floor is only honest if you wrote it down _before_ you saw the result.
- **Pre-registration** = writing a floor in your journal before running the test. It is the difference between measuring and moving the goalposts.

Use this toolkit reactively. You do not run all four on every response. You watch the output for one of four signals — a technical-sounding claim, a specific number, a threshold, a word like "blocked" or "blocking" — and then you run the matching check.

### The Viewer: Your Live Dashboard

The viewer at `http://localhost:3000` boots automatically at step 3 of the opening prompt (the `bash apps/web/media/serve.sh` step). It auto-refreshes as Claude Code writes artifacts to the workspace — you do not need to reload it manually. It is read-only: all commanding happens via Claude Code in your terminal, never through the viewer interface.

Dual role: it is both your **live evaluation instrument** (did that phase actually run, or did CC just describe it?) and **the product the Head of T&S, Engineering, Legal, and Ops will look at when they walk over at 5:30 pm**. Treat it seriously.

Glance at it after every phase. If nothing new rendered on the value-chain banner or the module cards, Claude Code described the work instead of running it. Re-prompt: "Show me the files you wrote, run the fine-tune now, and point me to the output on disk."

### Check 1 — "Show me the line"

**When to run it:** Claude Code names a specific architecture, technique, library, or method as if it is a fact about the pre-built scaffold.

**The question you ask, verbatim:**

> Show me the exact file, function, and line that proves this. Quote the line. If you have not read it, say so and mark the claim uncertain until we check together.

**Worked example.** When you ran the opening prompt, `/health` returned `image_baseline_arch: "resnet50"` and `text_baseline_arch: "bert-base-uncased"`. An hour later Claude Code writes: _"The image moderator uses EfficientNet-B7 for the backbone, per the startup configuration."_ You ask the verbatim question. Claude Code reads the source files, comes back: _"I was wrong. The image moderator uses ResNet-50 frozen + 5-class head fine-tune; I confused tonight's scaffold with a larger architecture I have seen elsewhere."_ You move on.

**The analogy.** A journalist fact-checking a source. "You said the contract was signed in March — show me the page of the contract with the date on it."

### Check 2 — "Show me the brief"

**When to run it:** Claude Code cites a specific dollar figure, percentage, or business metric — especially one you did not give it in your prompt.

**The question you ask, verbatim:**

> Which line of `PRODUCT_BRIEF.md` or which document did this number come from? Paste the row. If it is a calculation, show me the calculation step by step using only numbers from the brief.

**The analogy.** A finance director auditing a memo. "You wrote '$2.4M annual exposure' — show me the cell in the finance pack. If you built this number from two cells, show me both cells and the formula."

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

When to apply which: one check per triggering signal, not all four on every response. If Claude Code names an _architecture_, run Check 1. If it names a _number_, run Check 2. If it compares a result to a _threshold_, run Check 3. If it uses the word _blocker_, run Check 4.

---

## 4. How to Use This Workshop

Five pointers for the session:

- **Read this file once** — §0–§3 above are your pre-class reading. You do not need to re-read them during the workshop. Keep the tab open for reference.
- **Open `playbook/README.md` for run-order navigation** — that file is your table of contents for the session. Every playbook file has a `**Next file:**` pointer in §6; follow it.
- **Open playbook files in order** — each is self-contained. Paste §1, check §2, look up §3 if confused, read §4 for 30 seconds, use §5 to ask CC for a grounded explanation if needed, check §6 and move on.
- **Use `playbook/appendix/` for deep concept reference** — when the in-file §4 quick-reference is not enough, open `playbook/appendix/README.md`, find the concept in the alphabetical index, and open the file. (Appendix carries forward from Week 5; Week 6 adds CNN / Transformer / Multi-Modal entries.)
- **Ask Claude Code with the in-file §5 template when you need project-grounded explanations** — the §5 prompt tells CC to read our codebase and journal before answering. That grounds the explanation in MosaicHub's actual state, not a generic example.

---

## 5. How You Are Graded

Two layers, weighted 60/40.

### Layer 1 — Decision Journal (60%)

Each journal entry is scored on 5 dimensions, 0 / 2 / 4 each:

| Dim                        | 0                            | 2                         | 4                                                                                                        |
| -------------------------- | ---------------------------- | ------------------------- | -------------------------------------------------------------------------------------------------------- |
| **D1 Harm framing**        | No stakeholders named        | Names one cost            | Quantifies asymmetry in named dollars ($320 FN vs $15 FP = 21:1; $1M IMDA ceiling separately structural) |
| **D2 Metric→cost linkage** | Metric chosen without reason | Reason named              | Reason is a dollar figure or counterfactual-lift vs the current 31%-recall rule baseline                 |
| **D3 Trade-off honesty**   | Picks winner, ignores loser  | Names what was sacrificed | Quantifies the sacrifice (e.g. "lost 0.04 precision on hate-speech to gain 0.11 recall")                 |
| **D4 Constraint classify** | Unclear hard/soft            | Labelled correctly        | Penalty (in dollars) + reasoning (IMDA $1M is hard; $22/min reviewer time is soft)                       |
| **D5 Reversal condition**  | "If data changed"            | Names a signal            | Names signal + threshold + duration window                                                               |

Average across all today's entries. Target: ≥ 3.0 on average to pass.

### Layer 2 — Product Shipped (40%)

Binary checks:

- [ ] Dashboard loads at `http://localhost:3000`
- [ ] Image moderator endpoints return real per-class scores (not `{"status":"ok"}` stubs)
- [ ] Text moderator endpoints return real per-class scores
- [ ] Fusion moderator endpoint returns a cross-modal-harm score
- [ ] Drift endpoints return a meaningful report for all three model IDs
- [ ] `journal.pdf` exports cleanly

Each = 16.7% of the product grade; partial credit for partial functionality.

---

## 6. When You Get Stuck

Escalation ladder (try each before the next):

1. **Re-prompt Claude Code more precisely.** Nine times out of ten, stuck = vague prompt. Add the cost numbers. Add the phase context. Add the evaluation criteria.
2. **Check `playbook/README.md`** for run-order and the current file's §4 quick reference.
3. **Check `playbook/appendix/`** for the deeper concept treatment.
4. **Ask a neighbor** — compare prompts.
5. **Flag the instructor** — wave, don't shout.

### Common traps

- **"Deep learning has no closed-form, so what's the 'accuracy'?"** — There is one — per-class precision, recall, F1, and PR-AUC. Fine-tuned classifiers ARE supervised; the labels exist. Sprint 1 + 2 score on per-class PR curves with cost-based thresholds. Sprint 3 fusion scores on a cross-modal-harm holdout (the curated meme subset).
- **"IMDA is just a guideline, right?"** — No. The IMDA CSAM mandate is HARD. The $1M-per-incident ceiling sits structurally above any cost-balanced threshold. When the injection fires at ~4:30, re-classify the CSAM-adjacent class as hard with a regulator-mandated minimum threshold AND re-solve the reviewer queue allocator (Phase 11 + 12) — not just the journal entry.
- **"Two of my classes get the same auto-action — should I keep them both?"** — No. If the moderator workflow treats "violence-depiction" and "violence-encouragement" identically, they are one class with noise. Collapse or defend the split with disparate downstream actions.
- **"Joint-embedding is always best, so I'll pick CLIP-style."** — For multi-modal harm, joint-embedding catches the most. But it is 3× compute, harder to retrain, and requires curated multi-modal training data. You still read the cross-modal coverage gain in dollars, you still check inference-cost feasibility ($0.03/1k × 600k images/day = $18/day for image alone — fusion is 3×). A joint-embedding that wins on coverage by 2% but blows the inference budget is a research model, not a product.
- **"Claude Code said it ran the fine-tune but I see nothing in the dashboard."** — It probably described the work. Re-prompt: "Show me the files you wrote, run the BERT fine-tune against the pre-provisioned scaffold now, and point me to the per-class leaderboard on disk."
- **"The drift check returned 'no reference set'."** — The reference data is pre-registered by the scaffold for all three model IDs. Do NOT re-seed. Ask Claude Code to read the drift-status endpoint and confirm the reference is active for image / text / fusion separately; if any is missing, that is a scaffold bug and the instructor fixes it, not you.
- **"I'm in Sprint 2 and Phase 10 comes next, right?"** — No. Sprint 2 is the Transformer text-moderator replay — Phases 4, 5, 6, 7, 8 applied to text classification. Sprint 3 is where Phases 10, 11, 12 fire on the fusion moderator + queue allocator.
- **"IMDA fired at 4:30 — I only need to re-run Phase 11, right?"** — No. The injection demands BOTH a Phase 11 re-classification AND a Phase 12 re-solve against the reviewer queue allocator. Missing the Phase 12 re-solve scores 0 on D3.
- **"Per-class thresholds, why not one global threshold?"** — Because the cost asymmetry shifts per class. CSAM-adjacent is hard ($1M), hate-speech is cost-balanced ($320 vs $15), self-harm is bounded by clinical-safety floors not just dollars. One threshold per moderator silently averages over all of these. Sprint 1 + 2 each demand 5 thresholds.

---

## 7. Your Opening Prompt

Open a terminal at the **project root** (`~/repos/training/metis`). Type `claude` to start. Paste this exactly:

```
The active workspace is workspaces/metis/week-06-media/.
Read these files from the workspace:
- workspaces/metis/week-06-media/PRODUCT_BRIEF.md
- workspaces/metis/week-06-media/START_HERE.md
- workspaces/metis/week-06-media/playbook/README.md

I am a student running tonight's Week 6 content-moderation workshop.

The product (MosaicHub Content Moderation Suite) is pre-provisioned under
src/media/ (backend + data + pre-trained models) and apps/web/media/
(viewer). You will NOT scaffold, wire endpoints, or install libraries.

We WILL still run the full COC routine — /analyze, /todos, /implement,
/redteam, /codify — because that's the institutional muscle memory we
are building. The 14-phase ML Decision Playbook is the CONTENT of
/implement tonight, not a replacement for it.

Boot the pre-provisioned environment FOR ME (I will not run bash myself).
Execute these steps in order inside this session; start long-running
processes in the background so you can continue. Report progress aloud
so I can see you're alive during the ~30s transformer warm-up.

1. Run the preflight check:
     .venv/bin/python src/media/scripts/preflight.py
   Expect exit 0, all rows ✓. Report any non-green rows.

2. Start the backend in the background:
     bash src/media/scripts/run_backend.sh
   Poll curl -sf http://127.0.0.1:8000/health every 2 seconds until it
   responds (it will take ~30s — the BERT fine-tune warm-up is the
   slowest step). Report "backend ready" with the image_baseline_f1
   number AND text_baseline_f1 number when /health responds.

3. Start the viewer in the background:
     bash apps/web/media/serve.sh
   Wait 2s, then curl -sI http://127.0.0.1:3000/ to confirm HTTP 200.

4. Confirm all four sprint endpoints are live (one sample per sprint):
   - Sprint 1 CNN: GET /moderate/image/leaderboard returns a body with
     5 per-class entries (nsfw, violence, weapons, csam_adjacent, safe)
     each with precision/recall/f1.
   - Sprint 2 Transformer: GET /moderate/text/leaderboard returns a body
     with a "candidates" object holding three keys (bert_base, roberta,
     zero_shot_llm).
   - Sprint 3 Fusion: GET /moderate/fusion/score returns a body with a
     "cross_modal_harm_score" field on a sample meme.
   - Sprint 4 MLOps: GET /drift/status/image_moderator returns
     "reference_set": true (and likewise for text_moderator and
     fusion_moderator).

Describe any algorithm you mention in your summary ONLY if you can
quote the file and function you read it from (e.g. "ResNet-50 frozen,
per `train_baseline_image_moderator` in src/media/backend/ml_context.py").
If you are unsure which architecture backs a module, say "I did not read
the source for this — I can confirm after /analyze" rather than guess.

5. Open the viewer in my browser so I can see the value-chain banner:
     open http://127.0.0.1:3000/
   (If on Linux use xdg-open instead. If neither works, tell me to
   click http://127.0.0.1:3000/ manually.)

If ANY of steps 1–4 fails, STOP and tell me what failed. Do not try to
debug or fix the scaffold — raise your hand for the instructor.

Once green, summarise:
1. The four-layer multi-modal cascade: Sprint 1 CNN image moderator
   → Sprint 2 Transformer text moderator → Sprint 3 Fusion (CLIP-style
   joint embedding) → Sprint 4 MLOps drift × 3 models.
2. What is PRE-BUILT (frozen ResNet-50 + 5-class head fine-tuned on
   image baseline; BERT-base + RoBERTa fine-tuned at startup with
   3-family text leaderboard; fusion early/late stub; drift reference
   for all three; 80k labelled posts split 24k image / 56k text /
   8k multi-modal memes) vs what I will DECIDE tonight (per-class
   thresholds × 5 image classes + 5 text classes, fusion architecture
   choice, IMDA hard-line + queue allocator re-solve, three retrain
   rules at three cadences).
3. The five Trust Plane decision moments I must hit (define harmful,
   set per-class auto-remove thresholds × 10, choose fusion arch,
   IMDA re-classify + queue re-solve, three retrain rules).

Then stop and wait for me to open playbook/workflow-01-analyze.md
and paste the /analyze prompt from that file.
```

When Claude Code answers — **evaluate** two things:

1. **Environment**: did the preflight checks come back green? If not, flag the instructor. Do not try to fix the scaffold.
2. **Summary**: does it correctly describe the four-layer cascade (CNN → Transformer → Fusion → MLOps)? Does it name the five decision moments? Does it correctly split Trust Plane vs. Execution Plane? If not, correct it before proceeding.

That evaluation is your first decision of the day. You are already in the Trust Plane.

**Then open `playbook/workflow-01-analyze.md`** and paste the prompt from its §1. Every other paste tonight comes from a `playbook/*.md` file — follow the `**Next file:**` pointer at the bottom of each file through all 22 files in the order laid out in `playbook/README.md`.

---

## Closing

You have everything you need. The scaffold is pre-built. The COC routine is the routine you already know. The Playbook is universal. The product is a real Singapore omnichannel social platform in microcosm. Claude Code is your team. The decisions are yours.

By 5:30 pm you will have shipped the multi-modal moderation chain — an image moderator (CNN), a text moderator (Transformer), a fusion moderator (CLIP-style), and three drift rules (MLOps × 3 cadences) — and defended a page of decisions with dollar reasoning. In Week 7, you do it again on a new domain (manufacturing + industrial — transfer learning, RL, AI agents) with the same Playbook and the same routine. By Week 8, you will be a one-person unicorn — **because you can commission and judge ML products, not because you can code them**.

Let's ship.
