<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 2 — /todos (decision roadmap)

> **What this step does:** Turn the inheritance audit into a tracked plan — one todo per Playbook phase, in sprint order — so nothing gets silently skipped when the clock gets tight.
> **Why it exists:** The todo list is the human gate before implementation starts. You review and approve it; only then does the session enter /implement. Without a tracked plan, phases get dropped under time pressure with no record.
> **You're here because:** You just finished `workflow-01-analyze.md` and have three analysis files written.
> **Key concepts you'll see:** human gate, tracked plan, decision authority, skeleton, phase ordering

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm moving from /analyze into /todos. The goal here is a tracked plan —
every Playbook phase I will run tonight as an explicit todo, so nothing gets
silently skipped when the clock gets tight. This is the human gate before
/implement; you write the plan, I approve it.

Read the three files I just produced in the analysis folder. Read the
Playbook's phase summary and disposition table.

Create one todo file per Playbook phase under todos/active/, named
consistently (e.g. phase_N_<slug>.md). Phase 14 is deferred — do NOT create
a todo for it.

For each todo include:

1. Sprint it belongs to.
2. Playbook phase number and name.
3. The single Trust Plane decision I own this phase — one sentence.
4. The endpoint(s) this phase touches. Name them; do NOT guess — cite from
   the scaffold manifest or leave blank.
5. The skeleton to copy from journal/skeletons/.
6. Acceptance criterion: which file on disk proves the phase happened.

Add a close todo covering /redteam + /codify + /wrapup; this is not a
Playbook phase but it is on the clock.

Do NOT propose floors, thresholds, or parameter values in any todo.
Do NOT estimate effort in developer-days.
Do NOT use the word "blocker" in any todo without naming the specific action.

After writing the todos, list them in the order I will run them tonight
and stop. The instructor will review the plan before I enter /implement.
```

**Tonight-specific additions** (Week 6 MosaicHub Content Moderation):

```
Source files to read: 01-analysis/failure-points.md, 01-analysis/assumptions.md,
01-analysis/decisions-open.md. Also read PRODUCT_BRIEF.md §4 and §5.

Output directory: workspaces/metis/week-06-media/todos/active/
Todo naming: phase_N_<slug>.md (e.g. phase_1_frame.md, phase_6_vision.md).

Phase coverage: Phases 1–13 (Phase 14 deferred to Week 7). Do NOT create a
todo for Phase 14.

Extra todos required:
- phase_11_postimda.md and phase_12_postimda.md for the IMDA injection re-runs
  (these are mandatory, not optional — if they're missing, the D3 rubric fails)
- phase_{4..8}_text.md for the Sprint 2 Transformer replay of phases 4–8

A 14th todo: phase_99_close.md covering /redteam + /codify + /wrapup.

Endpoints: name them; cite from SCAFFOLD_MANIFEST.md. If an endpoint isn't in
the manifest, leave blank rather than guessing.

After writing, list all todos in execution order across Sprints 1 → 2 → 3 →
4 → Close, then stop. The instructor reviews before /implement starts.
```

**How to paste:** Combine both blocks into a single paste into your `claude` session.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ Todos exist for Playbook phases 1–13, skipping Phase 14
- ✓ Extra todos present: `phase_11_postimda.md`, `phase_12_postimda.md`, and `phase_{4..8}_text.md` for the Transformer replay
- ✓ A `phase_99_close.md` todo covers `/redteam` + `/codify` + `/wrapup`
- ✓ Each todo names the Trust Plane decision (one sentence), the endpoint(s), the skeleton file, and the acceptance criterion
- ✓ An ordered execution list is shown and Claude Code has stopped for instructor review

**Signals of drift — push back if you see:**

- ✗ A todo that proposes a value (e.g. "set hate-speech threshold to 0.85") — ask "please remove the proposed value; I own the decision, you own framing the todo."
- ✗ A Playbook phase missing from the list, or appearing in the wrong sprint — ask "does this match `PRODUCT_BRIEF.md` §4?"
- ✗ An endpoint path that isn't in `SCAFFOLD_MANIFEST.md` — ask "which manifest line does this endpoint come from?"
- ✗ Effort estimates in developer-days — ask "please remove developer-day estimates; there are no developers tonight."
- ✗ Missing `phase_11_postimda.md` or `phase_12_postimda.md` — ask "where is the IMDA re-run plan? The injection is mandatory, not optional."

---

## 3. Things you might not understand in this step

- **Human gate** — a deliberate stop where you (not Claude Code) decide whether the plan is correct before work begins
- **Tracked plan** — a file-per-phase todo list so nothing is silently skipped under time pressure
- **Decision authority** — the explicit assignment of "who sets this value" — you or the system
- **Skeleton** — the pre-formatted journal template for a phase; copying it before the phase starts prevents "I'll write the journal at the end" failures
- **Phase ordering** — the canonical sprint sequence that determines which phases run when and which share outputs

---

## 4. Quick reference (30 sec, generic)

### Human gate

A deliberate point in the COC workflow where Claude Code stops and waits for you to review and approve before continuing. `/todos` is the main human gate of the workshop: Claude Code writes the plan; you decide whether it is right; then and only then does `/implement` start. Human gates exist because a wrong plan executed fast is worse than a slow plan reviewed carefully. Without the gate, phases get silently reordered or dropped and you discover this at `/redteam`, not at planning time.

> **Deeper treatment:** [appendix/07-governance/hitl-patterns.md](./appendix/07-governance/hitl-patterns.md)

### Tracked plan

A file per Playbook phase under `todos/active/`, written before implementation starts. "Tracked" means each todo names an acceptance criterion — a specific file on disk that proves the phase happened. Untracked plans live in chat history and evaporate. A tracked plan survives a context reset, a session break, or a clock crunch: you re-read the file and know exactly where you are.

> **Deeper treatment:** [appendix/07-governance/hitl-patterns.md](./appendix/07-governance/hitl-patterns.md)

### Decision authority

The explicit assignment of "who sets this value" at plan time. The todo names the decision ("set hate-speech auto-remove threshold"), not the answer. Decision authority is yours: Claude Code frames the decision space; you write the value into the phase journal. If the todo already contains a proposed value, the Playbook pre-registration is corrupted before you even start the phase — the threshold was set by pattern-matching at plan time rather than by reading the PR curve at decision time.

> **Deeper treatment:** [appendix/04-evaluation/pre-registered-floors.md](./appendix/04-evaluation/pre-registered-floors.md)

### Skeleton

A pre-formatted journal template file in `journal/skeletons/`. Copying the skeleton into `journal/` before the phase starts means every phase has a live file with blanks waiting for your inputs. The failure mode it prevents: writing journals at the end of the sprint from memory, which produces post-hoc narratives rather than real-time records. The rubric checks for skeleton-sourced journals; reconstructed-from-memory journals score lower.

> **Deeper treatment:** [appendix/05-deployment/deployment-gate.md](./appendix/05-deployment/deployment-gate.md)

### Phase ordering

The canonical execution order across four sprints (Vision/CNN → Text/Transformer → Fusion+Queue → MLOps), where phases 1–3 are shared across Sprint 1 and Sprint 2, phases 4–8 replay for Sprint 2 (Transformer), and the IMDA injection forces re-runs of phases 11 and 12 mid-Sprint 3. Getting the ordering wrong at `/todos` means implementing phases out of sequence — the IMDA re-run is the highest-risk gap because it looks optional until the rubric says otherwise.

> **Deeper treatment:** [appendix/07-governance/hard-vs-soft-constraints.md](./appendix/07-governance/hard-vs-soft-constraints.md)

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 6, where I am
building an ML system for MosaicHub content moderation. I'm currently in the /todos step.

Read `workspaces/metis/week-06-media/playbook/workflow-02-todos.md` for
what this step does, and read `workspaces/metis/week-06-media/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. human gate >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current MosaicHub state
3. Implications for the decision I'm about to make (or just made) in /todos
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] Todos exist for phases 1–13 (Phase 14 absent — deferred to Week 7)
- [ ] `phase_11_postimda.md`, `phase_12_postimda.md`, and `phase_{4..8}_text.md` all present
- [ ] `phase_99_close.md` covers `/redteam` + `/codify` + `/wrapup`
- [ ] Each todo names one Trust Plane decision, the relevant endpoints (cited or blank), and the acceptance criterion
- [ ] Ordered execution list shown; Claude Code has stopped for instructor review

**Next file:** [`workflow-03-sprint-1-vision-boot.md`](./workflow-03-sprint-1-vision-boot.md)
