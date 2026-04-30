<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 8 — /codify (Phase 9 transferable lessons)

> **What this step does:** Capture what transfers to next domain (Week 7 manufacturing) vs what is content-moderation-specific. Append to the running lessons file so the Playbook accretes across weeks.
> **Why it exists:** The course's product is a 14-phase Playbook that gets sharper every week. /codify is the mechanism by which sharpening happens. Skip it and the Playbook stagnates.
> **You're here because:** /redteam wrapped; Phase 8 gates signed; Phase 13 retrain rules written; you have ~10 minutes left before /wrapup.
> **Key concepts you'll see:** transferable vs domain-specific, Playbook delta, accretion, anti-platitude

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm running /codify. The goal: extract 3 transferable lessons (apply to any
ML product, any domain) and 2 domain-specific lessons (apply to deep
learning + multi-modal moderation specifically).

Read all 14 of tonight's journal entries. Read the redteam.md findings.
Read appendix-a-lessons.md (the running lessons accretion file).

Produce two outputs:

1. journal/phase_9_codify.md — the per-session codify entry with:
   - 3 transferable lessons (each: a sentence stating the lesson, a
     sentence on why it transfers, a sentence on the cost of ignoring it)
   - 2 domain-specific lessons (deep learning + multi-modal specific)

2. Append to playbook/appendix-a-lessons.md — under "Week 6 — Media
   (MosaicHub)", paste the same 5 lessons.

Do NOT write platitudes. "Data quality matters" is BLOCKED. Lessons must
be actionable in Week 7 (Manufacturing) — name the next-week scenario
where this lesson applies.

Do NOT propose values. Do NOT use "blocker" without specifics.

After both files are written, list the 5 lessons, then stop. /wrapup is next.
```

**Tonight-specific additions** (Week 6 MosaicHub):

```
Anti-platitude check: each lesson must be falsifiable. "Calibration matters"
is a platitude. "Calibration matters when the downstream consumer is an LP
allocator that consumes probabilities directly — miscalibration silently
corrupts the LP's expected-cost calculation by an amount proportional to
Brier-score drift" is a lesson.

Suggested transferable lesson candidates (you decide which 3 are sharpest):
- Pre-registration: per-class threshold floors must be written before the
  Phase 4 leaderboard. Tonight's failure mode: post-hoc threshold setting
  on the IMDA-bound class.
- Cascade reasoning: a robust per-layer model is useless if the cascade
  fails on a coordinated input. /redteam tonight surfaced this in the
  fusion moderator.
- HITL on first trigger: every retrain rule starts HITL even if the cadence
  is fast. Tonight's text moderator has a daily cadence; first trigger is
  still HITL.
- Constraint hardness flips under regulatory pressure: tonight's IMDA fire
  shifted CSAM-adjacent from cost-balanced soft to regulator-mandated hard.
  This pattern recurs in Week 7 (industrial safety regulators).
- Three-cadence drift: when the system spans modalities, drift cadence
  must stratify by modality. Universal cadences fail.

Suggested domain-specific lesson candidates (you decide which 2 are sharpest):
- Joint-embedding fusion catches cross-modal harm but is 3× compute.
  Decide based on cross-modal coverage gain × $ vs compute cost delta.
  Specific to multi-modal AI.
- Transfer learning vs from-scratch: in 50 minutes of Sprint 1 budget,
  frozen ResNet-50 + fine-tuned head is the only viable Phase 4 candidate.
  Specific to vision tonight.
- Calibration matters more for transformers than CNNs — text classifiers
  feed an LP allocator that consumes probabilities; image classifiers
  feed a binary auto-remove decision.
- Adversarial robustness is asymmetric: image adversarial perturbation
  costs money but is rare; text adversarial perturbation (typos, unicode
  confusables) is cheap and frequent.

Files to write:
- workspaces/metis/week-06-media/journal/phase_9_codify.md (5 lessons)
- workspaces/metis/week-06-media/playbook/appendix-a-lessons.md (append
  Week 6 section if file exists; create with header if not)

After both files, list the lessons; stop for /wrapup.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ `journal/phase_9_codify.md` exists with 3 transferable + 2 domain-specific lessons
- ✓ `playbook/appendix-a-lessons.md` has a "Week 6 — Media (MosaicHub)" section appended (or created if file is new)
- ✓ Each lesson is falsifiable — names a specific scenario, a specific cost, a specific transfer target
- ✓ At least one transferable lesson points to a Week 7 (manufacturing) scenario where it applies
- ✓ Stop signal pending `/wrapup`

**Signals of drift — push back if you see:**

- ✗ A lesson stated as a platitude ("data quality matters") — ask "what's the falsifiable version? Name the scenario, the cost, the transfer target."
- ✗ A lesson proposing values you didn't pre-register — ask to remove
- ✗ A lesson that doesn't transfer (e.g. "moderation policy varies by jurisdiction") in the transferable section — ask "is this transferable to manufacturing? If not, move to domain-specific."
- ✗ Skipping the appendix append — ask "the Playbook accretes — please append to appendix-a-lessons.md."

---

## 3. Things you might not understand in this step

- **Transferable vs domain-specific** — does the lesson apply to ANY ML product (transferable) or only to multi-modal moderation (domain-specific)?
- **Playbook delta** — the diff between the universal Playbook and tonight's version; what changed
- **Accretion** — the running lessons file gets longer every week; the Playbook gets sharper every week
- **Anti-platitude** — falsifiable lessons name a scenario, a cost, a transfer target. Vague lessons are filtered out.

---

## 4. Quick reference (30 sec, generic)

### Transferable vs domain-specific

A transferable lesson applies to any ML product in any domain. "Pre-registration of metric floors" transfers — it works in retail (Week 5), moderation (Week 6), manufacturing (Week 7). A domain-specific lesson applies only to a class of products. "Joint-embedding fusion catches cross-modal harm" is specific to multi-modal AI; "the IMDA $1M ceiling makes CSAM threshold hard" is specific to content moderation. The 3:2 split (3 transferable, 2 domain) keeps the Playbook generalising.

> **Deeper treatment:** [appendix-a-lessons.md](./appendix-a-lessons.md)

### Playbook delta

The diff between the universal 14-phase Playbook and the way Phase N actually fired tonight. Tonight's deltas: Phase 6 expanded to per-class thresholds (5+5+1 = 11 thresholds, not 1). Phase 10 became a queue allocator instead of a route plan. Phase 13 stratified by modality. The deltas surface where the universal Playbook needs domain-specific guidance and feed back into appendix files.

> **Deeper treatment:** [appendix-a-lessons.md](./appendix-a-lessons.md)

### Accretion

The running lessons file in `appendix-a-lessons.md` gets longer every week. After 8 weeks, it is the actual product of this course — a 50-page record of generalised lessons grounded in 8 specific projects. Each week's `/codify` is the mechanism. Skipping `/codify` even once causes the appendix to lag, the Playbook to stagnate, and the next week's students to repeat the same mistakes.

> **Deeper treatment:** [appendix-a-lessons.md](./appendix-a-lessons.md)

### Anti-platitude

A falsifiable lesson names a scenario where it applies, a cost of ignoring it, and a transfer target where it next applies. "Data quality matters" is a platitude — it's true but unactionable. "Tier 2 integration tests must run against real infrastructure because mocks pass while production migrations fail; cost in our 2026-01 incident was 4 hours of downtime; transfer target Week 7 manufacturing process-control DBs" is a lesson.

> **Deeper treatment:** [appendix-a-lessons.md](./appendix-a-lessons.md)

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 6 /codify, where I
am extracting transferable lessons from the MosaicHub session.

Read `workspaces/metis/week-06-media/playbook/workflow-08-codify.md` for
what this step does, and read `workspaces/metis/week-06-media/journal/` for
the full session record.

Explain "<<< FILL IN: concept name, e.g. transferable vs domain-specific >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current MosaicHub state
3. Implications for the lessons I'm about to write
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

- [ ] `journal/phase_9_codify.md` exists with 3 + 2 lessons
- [ ] `playbook/appendix-a-lessons.md` has Week 6 section appended/created
- [ ] Each lesson is falsifiable (scenario + cost + transfer target)
- [ ] At least one transferable lesson points to Week 7 (manufacturing)
- [ ] Claude Code stopped, ready for `/wrapup`

**Next:** Run `/wrapup` to write `.session-notes` and close the workshop.
