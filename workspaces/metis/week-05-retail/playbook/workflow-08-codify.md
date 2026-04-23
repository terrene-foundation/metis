<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 8 — /codify (Phase 9 — transferable lessons)

> **What this step does:** Separate the lessons from tonight that transfer to any future ML project from the lessons that are specific to retail + USML + SML + Opt + MLOps, then write session notes so the next session inherits the work without re-discovery.
> **Why it exists:** Lessons not written down at close are forgotten. Generic lessons ("be careful with data quality") don't compound across weeks. The codify step forces you to name the near-miss — the specific thing you almost got wrong — which is the form that sticks.
> **You're here because:** `/redteam` is done and dispositions are journaled. This is the final step of the session.
> **Key concepts you'll see:** 3+2 lesson budget, near-miss framing, cite-or-fabricate, transferable vs domain-specific, session inheritance

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering /codify. Red team is done, dispositions are journaled. Before
I close the session I need to separate lessons that transfer to any future ML
project from lessons that only apply to this specific project, domain, and
model type.

Three transferable lessons, two domain-specific. Five total — the Codify
budget. Each lesson names the near-miss it prevents — a specific thing I
almost got wrong tonight, not a platitude.

Produce:

1. .claude/skills/project/<session>-lessons.md — the five lessons with their
   near-misses. Three transferable at the top, two domain-specific below,
   clearly labelled. Each lesson is a paragraph, not a sentence.

2. Append the three transferable lessons to the project Playbook's transferable
   lessons appendix under this week's heading. Leave prior weeks' entries alone.

3. journal/<phase-9-journal-file>.md — the journal entry naming the five
   lessons and the near-miss for each.

Then run /wrapup to write session notes covering: what was shipped, which
journal entries exist, what the next session inherits, any deferred items.

For every lesson, cite the specific journal entry, Playbook phase, or
red-team finding that motivated it. If you cannot cite, the lesson is
fabricated — remove it.

Do NOT invent dollar figures in the lessons. If a lesson quotes a number,
it comes from the project's cost source (quote the line) or from a journal
entry (cite the file).

Do NOT propose lessons I didn't live tonight. Lessons come from near-misses
I actually had, not from a general ML best-practices list.

When all files are written and /wrapup is done, stop. The session is over.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

```
Output files:
1. .claude/skills/project/week-05-lessons.md
2. Append to PLAYBOOK.md "Appendix — Transferable lessons" under "Week 5"
   (leave Week 4 entries alone)
3. journal/phase_9_codify.md (fill per the skeleton)

The 3+2 budget comes from PLAYBOOK.md Phase 9. More than 5 dilutes; fewer
than 5 leaves near-misses unnamed.

Near-miss requirement: "be careful with PDPA" is not a lesson. "When a
regulatory constraint fires mid-sprint, the mandatory re-run is the LP
re-solve, not just the journal re-classification" is a lesson. Name the
specific mechanism of the near-miss.

Each lesson MUST cite a source — a journal entry, a Playbook phase, or a
specific red-team finding from 04-validate/redteam.md. Example: "near-miss
from phase_12_postpdpa.md — I almost skipped the LP re-solve and kept only
the Phase 11 re-classification."

Guard against fabricated lessons: if you propose "always run a fairness
audit" — Phase 14 is deferred to Week 7. That wasn't a lesson I lived
tonight. Remove it.

Guard against generic platitudes: "be careful with data quality" is not a
lesson. Push for the specific mechanism.

For dollar figures in lessons: only from PRODUCT_BRIEF.md §2 (quote the line)
or from a journal entry written tonight (cite the file and entry number).

/wrapup covers: what was shipped, which journal entries exist (list them),
what Week 6 inherits, deferred items (Phase 14 Fairness is the main one).

After all three files are written and /wrapup is done, stop. Session over.
```

**How to paste:** Combine both blocks into a single paste into your `claude` session.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ `.claude/skills/project/week-05-lessons.md` exists with 3 transferable + 2 domain-specific lessons, each a paragraph, each citing a near-miss source
- ✓ `PLAYBOOK.md` Appendix updated under "Week 5" with the three transferable lessons; Week 4 entries untouched
- ✓ `journal/phase_9_codify.md` written per the skeleton
- ✓ `.session-notes` written covering ship status, journal inventory, Week 6 inheritance, and deferred items
- ✓ Every lesson cites a journal entry, Playbook phase, or red-team finding
- ✓ Stop signal — session is over
- ✓ Viewer (http://localhost:3000) journal panel shows all phase journal entries accumulated across the session

**Signals of drift — push back if you see:**

- ✗ A lesson with no cited journal entry or finding — ask "which journal entry or red-team finding motivated this? If you can't cite, please remove."
- ✗ A generic platitude ("be careful with data quality") — ask "what is the specific near-miss from tonight? Rewrite with the near-miss named."
- ✗ A Phase 14 fairness lesson — ask "we deferred Phase 14 to Week 7; this wasn't a lesson I lived tonight. Please remove or replace."
- ✗ A dollar figure not tied to `PRODUCT_BRIEF.md §2` or a journal entry — ask "which line of §2, or which journal entry, does this number come from?"
- ✗ Transferable lessons written only to the session journal and not appended to `PLAYBOOK.md` — ask "please append to the Playbook appendix; Week 6 students read the Playbook, not my session journal."
- ✗ Session notes missing the deferred-items list — ask "where is the Phase 14 deferral noted? Week 6 students need to know what was skipped."

---

## 3. Things you might not understand in this step

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **3+2 lesson budget** — exactly five lessons (three transferable, two domain-specific) to force prioritisation
- **Near-miss framing** — lessons written as "specific thing I almost got wrong" rather than as generic advice
- **Cite-or-fabricate** — each lesson must name a source; uncited lessons are fabricated and must be removed
- **Transferable vs domain-specific** — what crosses project/domain boundaries vs what only applies to retail ML tonight
- **Session inheritance** — the contract between tonight's session and the next one, written into session notes

---

## 4. Quick reference (30 sec, generic)

### 3+2 lesson budget

Exactly five lessons: three that transfer to any ML project (e.g. "pre-registration is not optional"), two that are specific to tonight's domain (e.g. "LP re-solve is the proof, not the journal re-classification"). The budget forces triage: you cannot put everything in, so you name only the things that actually changed how you work. More than five dilutes — weak lessons crowd out strong ones. Fewer than five means real near-misses went unnamed and will recur.

> **Deeper treatment:** [appendix/07-governance/hitl-patterns.md](./appendix/07-governance/hitl-patterns.md)

### Near-miss framing

A lesson written as "the specific thing I almost got wrong, and the mechanism by which I would have gotten it wrong." The positive form: "When a regulatory constraint fires mid-sprint, the mandatory re-run is the LP re-solve in Phase 12, not just the journal re-classification in Phase 11 — because the plan file on disk is the evidence the rubric checks, not the journal." The negative form: "be careful with regulatory constraints" is not a lesson; it's advice that doesn't change behaviour because it doesn't specify the mechanism.

> **Deeper treatment:** [appendix/07-governance/pdpa-basics.md](./appendix/07-governance/pdpa-basics.md)

### Cite-or-fabricate

Every lesson must name the journal entry, Playbook phase, or red-team finding that motivated it. A lesson without a citation is plausible-sounding advice pulled from a general ML best-practices mental model — it may or may not be grounded in what actually happened tonight. Fabricated lessons contaminate the Playbook appendix that Week 6, 7, and 8 students inherit. The citation is the proof that the lesson was earned, not confabulated.

> **Deeper treatment:** [appendix/01-framing/inheritance-vs-greenfield.md](./appendix/01-framing/inheritance-vs-greenfield.md)

### Transferable vs domain-specific

A transferable lesson applies to any ML project, regardless of whether it's retail, healthcare, or logistics; regardless of whether the model is a classifier, a clustering algorithm, or an LP. Example: "Pre-register performance floors before seeing leaderboard results." A domain-specific lesson only applies to tonight's specific setup — LP re-solve mechanics, PDPA injection sequence, Arcadia's cost ratios. Distinguishing them is the work of /codify: it forces you to decide which insights escape the context and which don't.

> **Deeper treatment:** [appendix/05-deployment/deployment-gate.md](./appendix/05-deployment/deployment-gate.md)

### Session inheritance

The contract between tonight's session and the next one, written into `.session-notes`. A good session notes file lets the next session — even if run by a different student or weeks later — resume without re-discovery: it lists what was shipped, which journals exist, what was deferred, and what the open questions are. The failure mode: /wrapup treated as a formality produces notes that say "completed all phases" with no specifics, and the next session spends 30 minutes re-deriving what was actually done.

> **Deeper treatment:** [appendix/05-deployment/deployment-gate.md](./appendix/05-deployment/deployment-gate.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in the /codify step.

Read `workspaces/metis/week-05-retail/playbook/workflow-08-codify.md` for
what this step does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. near-miss framing >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in /codify
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before closing:

- [ ] `.claude/skills/project/week-05-lessons.md` exists with 3 transferable + 2 domain-specific lessons, each citing a near-miss source
- [ ] `PLAYBOOK.md` Appendix updated under "Week 5" with the three transferable lessons
- [ ] `journal/phase_9_codify.md` exists and names five lessons with sources
- [ ] `.session-notes` written: ship status, journal inventory, Week 6 inheritance, deferred items (including Phase 14)
- [ ] All five lessons cite a source; no generic platitudes; no fabricated lessons

**End of workshop.** See the closing paragraph of `START_HERE.md` for what happens next.
