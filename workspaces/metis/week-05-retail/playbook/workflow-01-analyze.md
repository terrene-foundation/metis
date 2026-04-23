<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 1 — /analyze (inheritance audit)

> **What this step does:** Produce a written inventory of everything the scaffold committed to before you arrived — what's already fixed, what's still yours to decide — before any code runs or any phase prompt fires.
> **Why it exists:** Every Playbook phase anchors its decisions to this inventory. An analysis that invents claims instead of reading the actual scaffold produces phantom decisions and corrupted phase journals.
> **You're here because:** You just opened the workshop. This is the first paste of the session.
> **Key concepts you'll see:** inheritance audit, cite-or-cut hygiene, fake blocker, cascade structure, decisions-open

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm new to this project. Someone else built the scaffold before me. Before
I decide anything, I need to understand what they committed to on my behalf.

We are in the /analyze phase. The goal here is NOT to design the product —
it may already be pre-built. The goal is an inheritance audit: for every ML
artefact the scaffold ships, separate what is already fixed (baseline model
parameters, pre-selected algorithm families, pre-wired endpoints) from what
remains MY decision (final parameters, model selection, thresholds, weights,
retrain rules).

Produce three files:

1. failure-points.md — for each module in the system, name the 3 most
   likely failure points tonight. For each failure point cite the specific
   file and function in the codebase that the scaffold uses. If you cannot
   cite a file and function for a claim, delete the claim.

2. assumptions.md — list every assumption the scaffold has already baked in.
   Cite each assumption to a file. For any dollar figure you mention, quote
   it verbatim from the project's cost source — do NOT invent numbers.

3. decisions-open.md — the list of decisions still mine to make, organized
   by sprint or module. For each decision name the Playbook phase that owns
   it. Do NOT propose values for any threshold, floor, or parameter — those
   are my calls in the Playbook phases.

Do NOT use the word "blocker" unless you name the specific action I cannot
take until something is resolved. "The backend is slow" is not a blocker.

When all three files are written, stop and wait for me to run /todos.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

```
Output directory: workspaces/metis/week-05-retail/01-analysis/
Files to produce: failure-points.md, assumptions.md, decisions-open.md

Four modules to cover: USML segmentation, SML churn + conversion classifier,
Opt LP allocator, MLOps drift × 3 models.

For each failure point, cite the specific file and function in
src/retail/backend/ (e.g. ml_context.py::train_baseline_segmentation).
If you cannot cite a file and function, delete the claim.

Scaffold assumptions to cover: K=3 baseline, three-family classifier sweep
(LR + RF + GBM), drift reference registered, 5,000 customers / 400 SKUs /
120k transactions. Cite each to a source file.

For every dollar figure, quote the exact line from PRODUCT_BRIEF.md §2.
Do NOT invent numbers.

decisions-open.md format: organize by sprint (Sprint 1 USML / Sprint 2 SML /
Sprint 3 Opt / Sprint 4 MLOps). For each decision name the Playbook phase
that owns it (e.g. "pick final K: Sprint 1, Phase 6 USML"). Do NOT propose
values.

The closing summary should name the four-layer cascade (USML → SML → Opt →
MLOps) and the five Trust Plane decision moments. Then confirm you are
stopping for /todos.
```

**How to paste:** Combine both blocks into a single paste into your `claude` session.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ `01-analysis/failure-points.md` exists with 3 failure points per module (12 total), each citing a specific file and function in `src/retail/backend/`
- ✓ `01-analysis/assumptions.md` lists 8–12 inherited assumptions, each cited to a source file; every dollar figure is quoted verbatim from `PRODUCT_BRIEF.md §2`
- ✓ `01-analysis/decisions-open.md` lists 10–14 open decisions organized by sprint, each tagged with the owning Playbook phase, with no proposed values
- ✓ A closing summary naming the four-layer cascade and the five Trust Plane moments
- ✓ A stop signal confirming Claude Code is waiting for `/todos`
- ✓ Viewer (http://localhost:3000) refreshes and shows: the value-chain banner with all four sprint tiles visible in baseline (no sprints green yet)

**Signals of drift — push back if you see:**

- ✗ A failure point with no file-and-function citation — ask "which file and function in `src/retail/backend/` are you referring to?"
- ✗ A dollar figure that doesn't match `PRODUCT_BRIEF.md §2` — ask "which line of §2 does this come from? If it isn't in §2, remove it."
- ✗ A proposed threshold, floor, or K value anywhere in `decisions-open.md` — ask "please remove the proposed value; I own this decision in the Playbook phase."
- ✗ The word "blocker" without a specific action named — ask "which specific action can I not take until this is resolved?"
- ✗ A summary that collapses all four modules into one description — ask "please separate the four modules; they have different owners and different failure shapes."
- ✗ Viewer shows the value-chain banner but sprint tiles are missing or all grey — Claude Code may have described the cascade without reading the scaffold; ask for file citations before continuing.

---

## 3. Things you might not understand in this step

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **Inheritance audit** — a structured read of the scaffold to separate pre-committed choices from open decisions
- **Cite-or-cut hygiene** — every technical claim names a file and function; claims that can't be cited are deleted, not softened
- **Fake blocker** — calling something a blocker when it's actually latency or a warning, not a true stop
- **Cascade structure** — how the four-model pipeline (USML → SML → Opt → MLOps) means failure in one layer corrupts every later layer
- **Decisions-open** — the explicit list of calls that remain yours, framed as decisions not answers

---

## 4. Quick reference (30 sec, generic)

### Inheritance audit

The practice of reading what the scaffold already committed to — algorithm families, baseline parameters, dataset sizes, pre-wired endpoints — and writing it down before any Playbook phase starts. Industry ML almost always starts here, not from a blank slate. The audit separates what is already decided (baseline K=3, three-family sweep) from what is still yours to decide (final K, thresholds, weights). Without the audit, you risk re-deciding things the scaffold already fixed, wasting time and producing inconsistent journals.

> **Deeper treatment:** [appendix/01-framing/inheritance-vs-greenfield.md](./appendix/01-framing/inheritance-vs-greenfield.md)

### Cite-or-cut hygiene

Every claim in an analysis document names the file and function it was read from. Claims that cannot be sourced to a specific file are deleted — not hedged, not footnoted, not kept as "likely." The positive form: "K-means, per `train_baseline_segmentation` in `src/retail/backend/ml_context.py`." Cite-or-cut keeps analysis honest when a scaffold is large: Claude Code will hallucinate plausible-sounding architecture details if you don't demand citations for each one.

> **Deeper treatment:** [appendix/01-framing/inheritance-vs-greenfield.md](./appendix/01-framing/inheritance-vs-greenfield.md)

### Fake blocker

A "blocker" is something that stops a specific action — "I cannot run Phase 4 because `/segment/fit` returns 503." "The backend is slow" is not a blocker; it's latency. Distinguishing real blockers from latency or warnings matters tonight because Claude Code will flag the ~17-second NMF warm-up as a blocker when it isn't. A real blocker names an action that cannot proceed; a fake blocker just creates anxiety without directing a fix.

> **Deeper treatment:** [appendix/07-governance/hitl-patterns.md](./appendix/07-governance/hitl-patterns.md)

### Cascade structure

The four models are not independent: segmentation labels feed the classifiers; classifier probabilities feed the LP allocator; all three models generate signals for drift monitoring. A failure in segmentation (wrong K, unstable clusters) corrupts the classifiers' training labels, which corrupts the allocator's inputs, which corrupts the plan. Understanding the cascade is why `/redteam` is cross-sprint — a stability finding in Sprint 1 must be traced through Sprints 2 and 3.

> **Deeper treatment:** [appendix/03-modeling/unsupervised-families.md](./appendix/03-modeling/unsupervised-families.md)

### Decisions-open

The explicit list of calls that remain yours after the inheritance audit. Framed as decisions, not answers — "pick final K" not "K=5." Each decision names the Playbook phase that owns it so nothing gets silently skipped when time pressure hits. The list is also a pre-registration contract: once you start a phase, the decisions-open list says what you were supposed to own. If the journal shows a value you didn't set, the pre-registration is corrupted.

> **Deeper treatment:** [appendix/04-evaluation/pre-registered-floors.md](./appendix/04-evaluation/pre-registered-floors.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in the /analyze step.

Read `workspaces/metis/week-05-retail/playbook/workflow-01-analyze.md` for
what this step does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. inheritance audit >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in /analyze
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] `01-analysis/failure-points.md` exists with 12 failure points (3 per module), each citing a specific file and function
- [ ] `01-analysis/assumptions.md` exists with all scaffold assumptions cited; every dollar figure quoted from `PRODUCT_BRIEF.md §2`
- [ ] `01-analysis/decisions-open.md` exists with decisions organized by sprint and tagged to Playbook phases; no proposed values
- [ ] Closing summary names the four-layer cascade and five Trust Plane moments
- [ ] Claude Code has stopped and is waiting for `/todos`

**Next file:** [`workflow-02-todos.md`](./workflow-02-todos.md)
