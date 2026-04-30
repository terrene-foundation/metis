<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 3 — Sprint 1 Vision Boot (CNN image moderator)

> **What this step does:** Boot Sprint 1 by copying skeleton journal files, confirming live endpoints, and getting a written orientation from Claude Code — before any phase prompt fires.
> **Why it exists:** A misconfigured or hallucinated boot wastes 15–20 minutes mid-sprint. Confirming endpoints live and skeleton files in place up front means Phase 1 starts on solid ground.
> **You're here because:** The instructor approved your todo plan and Sprint 1 is ready to start.
> **Key concepts you'll see:** sprint boot, skeleton copy, pre-registration, transfer-learning prohibition, cite-or-confirm

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering /implement for a CNN sprint. Someone pre-built the scaffold
before me. My job in this sprint is to decide the per-class auto-remove
thresholds, defend each in dollar terms, and sign the deployment gate.

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
   after I check." Do NOT name architectures that are not in the scaffold.

4. For any dollar figure you state, quote the exact line from the project's
   cost source. Do NOT invent numbers.

5. Do NOT propose the per-class thresholds for the pre-registration phase.
   Those are my pre-registration; I write them in the phase journal BEFORE
   seeing the leaderboard. If you propose values here, you corrupt the
   pre-registration.

6. Do NOT use the word "blocker" without naming a specific action I cannot take.

Once skeletons are copied and endpoints confirmed live, summarise: (a) the
phases of this sprint and the single Trust Plane decision each phase owns,
(b) the per-class threshold decision shape only — not by value, (c) the
red-team sweeps specific to this sprint's CNN model.

Then stop and wait for my Phase 1 prompt.
```

**Tonight-specific additions** (Week 6 MosaicHub):

```
Sprint: Sprint 1 Vision/CNN — image moderator (5 classes: nsfw, violence,
weapons, csam_adjacent, safe).
Phases covered: Playbook phases 1, 2, 3, 4, 5, 6, 7, 8. Phases 1, 2, 3 are
shared across sprints — framed once here, not re-run in Sprint 2.
Phase 6 in this sprint is the per-class variant: 5 thresholds with
different defenses (cost-balanced for 4 classes, hard regulator floor for
csam_adjacent).

Skeleton copy: copy phase_{1..8}_vision.md skeletons from journal/skeletons/
into workspaces/metis/week-06-media/journal/. Inventory in
journal/skeletons/README.md.

Endpoint checks (GET only):
- /moderate/image/leaderboard → should return 5 per-class P/R/F1 entries
- /moderate/image/registry → should return registry state
If either is not live, STOP and raise a hand — do not debug.

Cite-or-confirm rule: for every architecture named (ResNet-50, etc.), cite
the specific file and function in src/media/backend/. Example of the correct
form: "ResNet-50 frozen + 5-class head, per train_baseline_image_moderator
in src/media/backend/ml_context.py."

CRITICAL — Transfer-learning prohibition: do NOT name "training the CNN
from scratch" as a Phase 4 candidate. The scaffold uses frozen ResNet-50 +
fine-tuned head ONLY; full from-scratch training is not in 50 minutes of
budget. Phase 4 candidates are: frozen / partial-unfreeze (last 2 conv
blocks) / full-unfreeze. AutoML for vision architectures raises a
ValueError in kailash-ml 1.6.0 and costs 15 minutes.

Dollar figures for Sprint 1: false-negative cost ($320 per piece) and
false-positive cost ($15 per piece). The IMDA $1M ceiling on csam_adjacent
is structurally separate (HARD constraint, not cost-balanced). All three
come from PRODUCT_BRIEF.md §2 — quote the exact line.

Decision shape to name (NOT values): per-class threshold (5 thresholds,
4 cost-balanced + 1 IMDA-floor-bound). Do NOT propose numeric thresholds
here — that is my pre-registration call in phase_6_vision.md, before I see
the Phase 4 leaderboard.

Phase 7 sweeps to name (NOT execute): list the three CNN-specific red-team
sweeps from the phase-07-redteam.md file: adversarial pixel perturbation,
out-of-distribution image robustness, demographic-skew robustness.

After the summary, stop and wait for my Phase 1 prompt.
```

**How to paste:** Combine both blocks into a single paste into your `claude` session.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ Eight skeleton files copied: `journal/phase_{1..8}_vision.md` all exist with blanks intact
- ✓ A live GET against `/moderate/image/leaderboard` returning 5 per-class P/R/F1 entries
- ✓ A live GET against `/moderate/image/registry` returning the registry state
- ✓ Written summary of the eight phases with one Trust Plane decision each
- ✓ Per-class threshold decision shape named (5 thresholds, csam_adjacent flagged as IMDA-bound) with NO numeric values
- ✓ Three Phase 7 sweeps named (not executed)
- ✓ Stop signal pending the Phase 1 walk-prompt
- ✓ Viewer (http://localhost:3000) refreshes and shows: Sprint 1 tile activates; image moderator card region shows "awaiting Phase 4 leaderboard"

**Signals of drift — push back if you see:**

- ✗ A threshold value proposed (e.g. "hate-speech ≥ 0.85") — ask "please remove the proposed value; I pre-register thresholds in `phase_6_vision.md`."
- ✗ "Train CNN from scratch" named for Phase 4 — ask "please re-check — the scaffold uses frozen ResNet-50 + fine-tuned head; full from-scratch is not in budget."
- ✗ A dollar figure not quoted from `PRODUCT_BRIEF.md §2` — ask "please quote the exact line from §2."
- ✗ Skeletons not copied to `journal/` — ask "please copy the skeletons now so every phase has a live journal file."
- ✗ A baseline F1 that is suspicious (e.g. 0.99 across all classes) — ask "is the backend actually live? Please re-run the GET and show me the output."
- ✗ Viewer Sprint 1 tile does not activate — confirm the GET to `/moderate/image/leaderboard` actually ran and returned the expected payload.

---

## 3. Things you might not understand in this step

- **Sprint boot** — the setup ritual that runs once before any phase prompt, confirming infrastructure is ready
- **Pre-registration** — writing the per-class thresholds BEFORE seeing the leaderboard, so the thresholds are honest
- **Transfer-learning prohibition** — frozen ResNet-50 + fine-tuned head is the only Phase 4 architecture family tonight; full from-scratch training is out of budget
- **Cite-or-confirm** — a tighter form of cite-or-cut: either show the file and function, or say "I haven't read the source yet"
- **Threshold shapes vs threshold values** — naming "per-class threshold (5 of them)" without committing to any value

---

## 4. Quick reference (30 sec, generic)

### Sprint boot

The setup ritual that runs before any Playbook phase prompt in a sprint: copy skeletons, confirm endpoints live, get an orientation summary. The boot exists because a hallucinated endpoint or a missing skeleton file creates failure mid-phase when you can least afford to debug it. Ten minutes at boot saves 20 minutes of confusion mid-Phase 4. The boot is NOT a phase — it produces no journal entries of its own; it creates the conditions for the real phase walk to proceed cleanly.

> **Deeper treatment:** [appendix/05-deployment/deployment-gate.md](./appendix/05-deployment/deployment-gate.md)

### Pre-registration

Writing your per-class threshold values — the auto-remove cutoff for each of the 5 image classes — BEFORE you see the Phase 4 leaderboard results. Pre-registration is what makes a threshold honest. If you read the leaderboard first and then write "hate-speech ≥ 0.85" because that's what the best model scored, the threshold is post-hoc and meaningless. Pre-registration is the difference between a standard and a rubber stamp.

> **Deeper treatment:** [appendix/04-evaluation/pre-registered-floors.md](./appendix/04-evaluation/pre-registered-floors.md)

### Transfer-learning prohibition

In tonight's scaffold, the image moderator uses ResNet-50 frozen + fine-tuned 5-class head — that's the only Phase 4 candidate family. Full from-scratch CNN training does not fit in the 50-minute Sprint 1 budget. The Phase 4 sweep varies the unfreeze depth (frozen / partial-unfreeze last-2-blocks / full-unfreeze), not the architecture family. Asking Claude Code to "use AutoML to find the best CNN" raises a ValueError and burns 15 minutes.

> **Deeper treatment:** [appendix/03-modeling/supervised-families.md](./appendix/03-modeling/supervised-families.md)

### Cite-or-confirm

A tighter variant of cite-or-cut: either (a) name the file and function you read it from, or (b) say explicitly "I have not checked the source for this yet." Option b is acceptable at boot; it becomes unacceptable mid-phase. The distinction matters because some scaffold claims (like which augmentations were applied to the training images) are buried in `ml_context.py` and require a real read — Claude Code will confabulate if you don't demand the confirmation.

> **Deeper treatment:** [appendix/01-framing/inheritance-vs-greenfield.md](./appendix/01-framing/inheritance-vs-greenfield.md)

### Threshold shapes vs threshold values

Naming the shape of a constraint means saying "per-class auto-remove threshold (5 of them, 4 cost-balanced + 1 IMDA-bound)." It does NOT mean saying "hate-speech ≥ 0.85." The value is your pre-registration call, written in `phase_6_vision.md` before you see results. If the boot summary names a value, the pre-registration is already corrupted: you've let Claude Code pick the standard rather than setting it yourself, which means you can't push back when the model barely clears it.

> **Deeper treatment:** [appendix/04-evaluation/pre-registered-floors.md](./appendix/04-evaluation/pre-registered-floors.md)

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 6, where I am
building an ML system for MosaicHub content moderation. I'm currently in
the Sprint 1 Vision boot step.

Read `workspaces/metis/week-06-media/playbook/workflow-03-sprint-1-vision-boot.md`
for what this step does, and read `workspaces/metis/week-06-media/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. pre-registration >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current MosaicHub state
3. Implications for the decision I'm about to make (or just made) in the Sprint 1 boot
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] Eight skeleton files exist in `journal/phase_{1..8}_vision.md`
- [ ] `/moderate/image/leaderboard` returned 5 per-class entries
- [ ] `/moderate/image/registry` returned registry state
- [ ] Summary written: eight phases, one Trust Plane decision each, per-class threshold shape (no values), three Phase 7 sweeps named
- [ ] Claude Code has stopped and is waiting for the Phase 1 prompt

**Next file:** [`phase-01-frame.md`](./phase-01-frame.md)
