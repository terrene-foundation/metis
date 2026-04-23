<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 3 — Sprint 1 USML Boot (segmentation)

> **What this step does:** Boot Sprint 1 by copying skeleton journal files, confirming live endpoints, and getting a written orientation from Claude Code — before any phase prompt fires.
> **Why it exists:** A misconfigured or hallucinated boot wastes 15–20 minutes mid-sprint. Confirming endpoints live and skeleton files in place up front means Phase 1 starts on solid ground.
> **You're here because:** The instructor approved your todo plan (`workflow-02-todos.md`) and Sprint 1 is ready to start.
> **Key concepts you'll see:** sprint boot, skeleton copy, pre-registration, AutoML prohibition, cite-or-confirm

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering /implement for a USML (unsupervised ML) sprint. Someone pre-built
the scaffold before me. My job in this sprint is to decide the final model
parameters, name every discovered group, declare a distinct action per group,
and sign the deployment gate.

Before I start the phase walk, I need you to:

1. Copy the sprint skeletons from journal/skeletons/ into journal/ — one file
   per phase, named consistently. Leave the blanks blank; I fill them phase
   by phase. The skeleton inventory is in journal/skeletons/README.md.

2. Confirm the sprint endpoints are live by making GET requests to each.
   If any endpoint is not live, STOP and raise a hand — do not attempt to
   debug the scaffold.

3. For every algorithm or model family you name in this sprint, cite the
   specific file and function you read it from. If you cannot cite a file
   and function, say "I did not read the source for this — I can confirm
   after I check." Do NOT name algorithm families that are not in the
   scaffold's source.

4. For any dollar figure you state, quote the exact line from the project's
   cost source. Do NOT invent numbers.

5. Do NOT propose the performance floors for the pre-registration phase.
   Those are my pre-registration; I write them in the phase journal BEFORE
   seeing the leaderboard. If you propose values here, you corrupt the
   pre-registration.

6. Do NOT use the word "blocker" without naming a specific action I cannot take.

Once skeletons are copied and endpoints confirmed live, summarise: (a) the
phases of this sprint and the single Trust Plane decision each phase owns,
(b) the performance floors named by SHAPE only — not by value, (c) the
red-team sweeps specific to this sprint's model type.

Then stop and wait for my Phase 1 prompt.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

```
Sprint: Sprint 1 USML — customer segmentation.
Phases covered: Playbook phases 1, 2, 3, 4, 5, 6, 7, 8. Phases 1, 2, 3 are
shared across sprints — framed once here, not re-run in Sprint 2.
Phase 6 in this sprint is the USML variant: three pre-registered floors
(separation, stability, actionability), NOT a single accuracy metric.

Skeleton copy: copy phase_{1..8}_usml.md skeletons from journal/skeletons/
into workspaces/metis/week-05-retail/journal/. Inventory in
journal/skeletons/README.md.

Endpoint checks (GET only):
- /segment/baseline → should return k=3, silhouette ≈ 0.3422
- /segment/registry → should return the registry state
If either is not live, STOP and raise a hand — do not debug.

Cite-or-confirm rule: for every algorithm or family named (K-means, NMF,
etc.), cite the specific file and function in src/retail/backend/. Example
of the correct form: "K-means, per train_baseline_segmentation in
src/retail/backend/ml_context.py."

CRITICAL — AutoML prohibition: do NOT name AutoMLEngine for clustering.
PLAYBOOK.md §Phase 4 notes the scaffold uses /segment/fit directly, not
AutoML. Naming AutoMLEngine here raises a ValueError in kailash-ml 0.17.0
and costs 10 minutes.

Dollar figures for Sprint 1: wrong-segment cost ($45 per customer) and
per-customer touch cost ($3). Both come from PRODUCT_BRIEF.md §2 — quote
the exact line when you reference them.

Floor shapes to name (NOT values): separation, stability, actionability.
Do NOT propose numeric values for any floor here — that is my pre-
registration call in phase_6_usml.md, before I see the Phase 4 leaderboard.

Phase 7 sweeps to name (NOT execute): list the three segmentation-specific
red-team sweeps from PLAYBOOK.md §Phase 7 by name only. Do not run them here.

After the summary, stop and wait for my Phase 1 prompt.
```

**How to paste:** Combine both blocks into a single paste into your `claude` session.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ Eight skeleton files copied: `journal/phase_{1..8}_usml.md` all exist with blanks intact
- ✓ A live GET against `/segment/baseline` returning `k=3` and `silhouette ≈ 0.3422`
- ✓ A live GET against `/segment/registry` returning the registry state
- ✓ Written summary of the eight phases with one Trust Plane decision each
- ✓ Three Phase 6 floors named by shape only — `separation`, `stability`, `actionability` — with NO numeric values
- ✓ Three Phase 7 sweeps named (not executed)
- ✓ Stop signal pending the Phase 1 walk-prompt
- ✓ Viewer (http://localhost:3000) refreshes and shows: Sprint 1 tile activates; segment cards region shows "awaiting Phase 4 leaderboard"

**Signals of drift — push back if you see:**

- ✗ A floor value proposed (e.g. "silhouette ≥ 0.25") — ask "please remove the proposed value; I pre-register floors in `phase_6_usml.md`."
- ✗ `AutoMLEngine` named for clustering — ask "please re-check — `PLAYBOOK.md` Phase 4 says the scaffold uses `/segment/fit` directly."
- ✗ A dollar figure not quoted from `PRODUCT_BRIEF.md §2` — ask "please quote the exact line from §2."
- ✗ Skeletons not copied to `journal/` — ask "please copy the skeletons now so every phase has a live journal file."
- ✗ A baseline silhouette that isn't ≈ 0.3422 — ask "is the backend actually live? Please re-run the GET."
- ✗ Viewer Sprint 1 tile does not activate — the sprint boot may not have written state; confirm the GET to `/segment/baseline` actually ran and returned the expected value.

---

## 3. Things you might not understand in this step

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **Sprint boot** — the setup ritual that runs once before any phase prompt, confirming infrastructure is ready
- **Pre-registration** — writing the performance floors BEFORE seeing the results, so the floors are honest
- **AutoML prohibition** — a specific kailash-ml incompatibility that costs 10 minutes if triggered
- **Cite-or-confirm** — a tighter form of cite-or-cut: either show the file and function, or say "I haven't read the source yet"
- **Floor shapes vs floor values** — naming the shape of a constraint (separation) without committing to its value (≥ 0.25)

---

## 4. Quick reference (30 sec, generic)

### Sprint boot

The setup ritual that runs before any Playbook phase prompt in a sprint: copy skeletons, confirm endpoints live, get an orientation summary. The boot exists because a hallucinated endpoint or a missing skeleton file creates failure mid-phase when you can least afford to debug it. Ten minutes at boot saves 20 minutes of confusion mid-Phase 4. The boot is NOT a phase — it produces no journal entries of its own; it creates the conditions for the real phase walk to proceed cleanly.

> **Deeper treatment:** [appendix/05-deployment/deployment-gate.md](./appendix/05-deployment/deployment-gate.md)

### Pre-registration

Writing your performance floors — the minimum acceptable values for separation, stability, and actionability — BEFORE you see the Phase 4 leaderboard results. Pre-registration is what makes a floor honest. If you read the leaderboard first and then write "silhouette ≥ 0.25" because that's what the best model scored, the floor is post-hoc and meaningless. Pre-registration is the difference between a standard and a rubber stamp.

> **Deeper treatment:** [appendix/04-evaluation/pre-registered-floors.md](./appendix/04-evaluation/pre-registered-floors.md)

### AutoML prohibition

In kailash-ml 0.17.0, calling `AutoMLEngine` for clustering raises a `ValueError` because the scaffold's segmentation module uses `/segment/fit` directly. If you ask Claude Code to pick a clustering algorithm and it names `AutoMLEngine`, it will waste 10 minutes on a dead path before discovering the error. The prohibition is explicit in `PLAYBOOK.md` Phase 4. Name it now so you have a reflex: clustering → `/segment/fit`, not `AutoMLEngine`.

> **Deeper treatment:** [appendix/03-modeling/unsupervised-families.md](./appendix/03-modeling/unsupervised-families.md)

### Cite-or-confirm

A tighter variant of cite-or-cut: either (a) name the file and function you read it from, or (b) say explicitly "I have not checked the source for this yet." Option b is acceptable at boot; it becomes unacceptable mid-phase. The distinction matters because some scaffold claims (like which features were selected) are buried in `ml_context.py` and require a real read — Claude Code will confabulate if you don't demand the confirmation.

> **Deeper treatment:** [appendix/01-framing/inheritance-vs-greenfield.md](./appendix/01-framing/inheritance-vs-greenfield.md)

### Floor shapes vs floor values

Naming the shape of a constraint means saying "separation" — a score that measures how distinct the clusters are from each other. It does NOT mean saying "≥ 0.25." The value is your pre-registration call, written in `phase_6_usml.md` before you see results. If the boot summary names a value, the pre-registration is already corrupted: you've let Claude Code pick the standard rather than setting it yourself, which means you can't push back when the model barely clears it.

> **Deeper treatment:** [appendix/04-evaluation/pre-registered-floors.md](./appendix/04-evaluation/pre-registered-floors.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in the Sprint 1
USML boot step.

Read `workspaces/metis/week-05-retail/playbook/workflow-03-sprint-1-usml-boot.md`
for what this step does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. pre-registration >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in the Sprint 1 boot
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] Eight skeleton files exist in `journal/phase_{1..8}_usml.md`
- [ ] `/segment/baseline` returned `k=3`, `silhouette ≈ 0.3422`
- [ ] `/segment/registry` returned registry state
- [ ] Summary written: eight phases, one Trust Plane decision each, three floor shapes (no values), three Phase 7 sweeps named
- [ ] Claude Code has stopped and is waiting for the Phase 1 prompt

**Next file:** [`phase-01-frame.md`](./phase-01-frame.md)
