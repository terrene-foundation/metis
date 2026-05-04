<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 8 — /codify (Phase 9 transferable lessons)

> **What this step does:** Capture what transfers to next domain (Week 8 capstone) vs what is industrial-AI-specific. Append to the running lessons file so the Playbook accretes across weeks.
> **Why it exists:** The course's product is a 14-phase Playbook that gets sharper every week. /codify is the mechanism by which sharpening happens. Skip it and the Playbook stagnates.
> **You're here because:** /redteam wrapped; Phase 8 gates signed; Phase 13 retrain rules written; you have ~10 minutes left before /wrapup.
> **Key concepts you'll see:** transferable vs domain-specific, Playbook delta, accretion, anti-platitude

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm running /codify. The goal: extract 3 transferable lessons (apply to any
ML product, any domain) and 2 domain-specific lessons (apply to industrial
AI + RL + agent architectures specifically).

Read all of tonight's journal entries. Read the redteam.md findings.
Read appendix-a-lessons.md (the running lessons accretion file).

Produce two outputs:

1. journal/phase_9_codify.md — the per-session codify entry with:
   - 3 transferable lessons (each: a sentence stating the lesson, a
     sentence on why it transfers, a sentence on the cost of ignoring it)
   - 2 domain-specific lessons (industrial AI + RL + agent specific)

2. Append to playbook/appendix-a-lessons.md — under "Week 7 — Manufacturing
   (LumenCircuit)", paste the same 5 lessons.

Do NOT write platitudes. "Data quality matters" is BLOCKED. Lessons must
be actionable in Week 8 (capstone) — name the next-week scenario where
this lesson applies.

Do NOT propose values. Do NOT use "blocker" without specifics.

After both files are written, list the 5 lessons, then stop. /wrapup is next.
```

**Tonight-specific additions** (Week 7 LumenCircuit):

```
Anti-platitude check: each lesson must be falsifiable. "Safety matters" is
a platitude. "WSH-affecting categories must be structurally hard-shadowed
(not cost-balanced) the moment a regulator mandate fires; the agent
autonomy endpoint must enforce 422 server-side; cost in our Phase 12
post-WSH was $X/day of lost RL throughput which IS the compliance cost"
is a lesson.

Suggested transferable lesson candidates (you decide which 3 are sharpest):
- Reward function design IS the load-bearing decision in any RL system —
  pick wrong weights and the agent reward-hacks (Goodhart). The structural
  defense is a four-term reward where each axis is its own term + a
  hard-floor table that lives ABOVE the reward function.
- Hard-floor classification under regulator pressure: tonight's MOM/WSH
  fire shifted setpoint_adjustment + safety_alert from cost-balanced soft
  to regulator-mandated hard shadow. This pattern recurs in any regulated
  domain (any prior-week regulator scenario; Week 8 will hit clinical/medical).
- Three-cadence drift: when the system spans modalities, drift cadence
  must stratify by data-generating process. Universal cadences fail.
  Tonight: vision weekly (equipment + supplier) / sensor daily
  (calibration + ambient) / RL per-deployment.
- Agent autonomy ladder = decision authority structurally enforced.
  The endpoint returns 422 if the autonomy is set above the regulator's
  envelope; the regulator wins by code path, not by policy memo.
- Pre-registration of metric floors: per-class thresholds and reward-
  weight floors must be written before the leaderboard. Tonight's failure
  mode: post-hoc weight setting on the safety_penalty (driven by what
  produces the prettiest leaderboard rather than what produces zero
  hard-floor violations).

Suggested domain-specific lesson candidates (you decide which 2 are sharpest):
- Edge-deployment trade-off: at 80 ms/board on Jetson hardware, EfficientNet
  typically wins on throughput; ViT wins on accuracy but is data-hungry
  at 800 images. The architecture choice is partly an edge-hardware
  trade-off, not a pure accuracy decision. Specific to industrial vision.
- Time-series prediction-window choice: 3 vs 7 vs 14 days for predmaint
  is the trade-off between FP rate (planned-maintenance overhead) and FN
  rate (missed signal → unplanned stop). Specific to predictive
  maintenance + similar time-to-event problems.
- RL Goodhart defense via four-term reward: reward only throughput → agent
  runs unsafe; reward only zero defects → agent stops the line. Four terms
  with explicit weights AND a hard-floor table above the reward bind the
  agent against extremes. Specific to RL.
- LLM agent autonomy ladders need server-side enforcement: a 422 on
  /agent/policy when WSH-affecting categories are set above shadow during
  the mandate window is the structural defense. A policy memo is not.
  Specific to agent architectures.

Files to write:
- workspaces/metis/week-07-manufacturing/journal/phase_9_codify.md (5 lessons)
- workspaces/metis/week-07-manufacturing/playbook/appendix-a-lessons.md
  (append Week 7 section if file exists; create with header if not)

After both files, list the lessons; stop for /wrapup.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ `journal/phase_9_codify.md` exists with 3 transferable + 2 domain-specific lessons
- ✓ `playbook/appendix-a-lessons.md` has a "Week 7 — Manufacturing (LumenCircuit)" section appended (or created if file is new)
- ✓ Each lesson is falsifiable — names a specific scenario, a specific cost, a specific transfer target
- ✓ At least one transferable lesson points to a Week 8 (capstone) scenario where it applies
- ✓ Stop signal pending `/wrapup`

**Signals of drift — push back if you see:**

- ✗ A lesson stated as a platitude ("safety matters") — ask "what's the falsifiable version? Name the scenario, the cost, the transfer target."
- ✗ A lesson proposing values you didn't pre-register — ask to remove
- ✗ A lesson that doesn't transfer (e.g. "PCB inspection asymmetry is 49:1") in the transferable section — ask "is this transferable to clinical/finance/legal? If not, move to domain-specific."
- ✗ Skipping the appendix append — ask "the Playbook accretes — please append to appendix-a-lessons.md."

---

## 3. Things you might not understand in this step

- **Transferable vs domain-specific** — does the lesson apply to ANY ML product (transferable) or only to industrial AI (domain-specific)?
- **Playbook delta** — the diff between the universal Playbook and tonight's version; what changed
- **Accretion** — the running lessons file gets longer every week; the Playbook gets sharper every week
- **Anti-platitude** — falsifiable lessons name a scenario, a cost, a transfer target

---

## 4. Quick reference (30 sec, generic)

### Transferable vs domain-specific

A transferable lesson applies to any ML product in any domain. "Pre-registration of metric floors" transfers — it works in retail (Week 5), moderation (Week 6), manufacturing (Week 7), and the Week 8 capstone. A domain-specific lesson applies only to a class of products. "Edge-deployment trade-off at 80 ms/board" is specific to industrial vision; "RL four-term reward" is specific to RL. The 3:2 split keeps the Playbook generalising.

### Playbook delta

The diff between the universal 14-phase Playbook and the way Phase N actually fired tonight. Tonight's deltas: Phase 6 expanded to per-class thresholds with the WSH hard floor (4 classes, 1 regulator-bound). Phase 7 became Goodhart defense for RL — defending FOUR weights that interact non-monotonically. Phase 10 became the RL reward function shape, not a route plan. Phase 11 became autonomy ladder + hard floor table. Phase 13 stratified by data-generating process across three model types. The deltas surface where the universal Playbook needs domain-specific guidance.

### Accretion

The running lessons file in `appendix-a-lessons.md` gets longer every week. After 8 weeks, it is the actual product of this course — a 50-page record of generalised lessons grounded in 8 specific projects. Each week's `/codify` is the mechanism. Skipping `/codify` even once causes the appendix to lag, the Playbook to stagnate, and the next week's students to repeat the same mistakes.

### Anti-platitude

A falsifiable lesson names a scenario where it applies, a cost of ignoring it, and a transfer target where it next applies. "Safety matters" is a platitude — it's true but unactionable. "WSH-affecting categories must be structurally hard-shadowed (not cost-balanced) when the regulator mandate fires; agent /policy endpoint MUST return 422 for above-shadow settings; cost of failing to enforce in our Phase 12 post-WSH was $X/day of compliance shadow price; transfer target Week 8 capstone clinical-decision agent" is a lesson.

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 7 /codify, where I
am extracting transferable lessons from the LumenCircuit session.

Read `workspaces/metis/week-07-manufacturing/playbook/workflow-08-codify.md` for
what this step does, and read `workspaces/metis/week-07-manufacturing/journal/`
for the full session record.

Explain "<<< FILL IN: concept name, e.g. transferable vs domain-specific >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current LumenCircuit state
3. Implications for the lessons I'm about to write
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

- [ ] `journal/phase_9_codify.md` exists with 3 + 2 lessons
- [ ] `playbook/appendix-a-lessons.md` has Week 7 section appended/created
- [ ] Each lesson is falsifiable (scenario + cost + transfer target)
- [ ] At least one transferable lesson points to Week 8 (capstone)
- [ ] Claude Code stopped, ready for `/wrapup`

**Next:** Run `/wrapup` to write `.session-notes` and close the workshop.
