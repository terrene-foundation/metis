<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 7 — /redteam (cross-sprint cascade stress)

> **What this step does:** Stress-test the four-layer industrial value chain end-to-end after all sprints have shipped. Vision → predmaint → RL → agent — the cascade either holds or it doesn't.
> **Why it exists:** A robust vision QC inspector is useless if the agent's autonomy ladder above it allows a setpoint that triggers a defect cascade. `/redteam` finds where the cascade breaks under coordinated stress.
> **You're here because:** All four sprints completed; Phase 8 gates signed; Phase 13 retrain rules written.
> **Key concepts you'll see:** cascade red-team, blast radius, severity ranking, detection cadence, mitigation

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm running /redteam on the entire shipped product. The four-layer cascade
(vision → predmaint → RL → agent + drift) must be stressed end-to-end,
not per-layer.

Read every Phase 7 journal entry I wrote tonight (one per sprint). Read the
Phase 8 deployment gates. Read the post-WSH Phase 12 entry.

Then, for each of the three AI Verify dimensions in scope tonight
(transparency, robustness, safety — fairness deferred to Week 8):

1. Identify cross-sprint findings — places where one sprint's result
   exposes a vulnerability in another sprint's output. Example: if vision
   QC has 0.62 recall on safety_critical_defect (Sprint 1), what is the
   impact on the agent's autonomy ladder (Sprint 3) when a board with
   marginal solder joints is mis-classified as good and the line speed
   is at the upper end of the post-WSH envelope?

2. Rank by severity, naming for each finding:
   - The blast radius in dollars (use the cost table)
   - The detection cadence (which Phase 13 drift signal would catch it)
   - The mitigation (within tonight's product, not "rebuild from scratch")

3. Write the findings to 04-validate/redteam.md.

Do NOT invent findings. Do NOT use the word "blocker" without specifics.
Do NOT propose values for thresholds I have already pre-registered.

After the file is written, stop. The instructor reviews before /codify.
```

**Tonight-specific additions** (Week 7 LumenCircuit):

```
Output file: workspaces/metis/week-07-manufacturing/04-validate/redteam.md

Cross-sprint findings to specifically check:

A. Sprint 1 → Sprint 4 (vision → agent):
   - If vision recall on safety_critical_defect is below 0.85, what
     fraction of true safety-critical boards reach /agent/decide and get
     auto-passed? Quantify against $4,200 FN cost and the WSH $1M ceiling.
   - If vision FP rate on good is high (false-scrap rate), what queue
     load impact at $35/min inspector time × 1,400 queue start?

B. Sprint 2 → Sprint 3 (predmaint → RL):
   - If predmaint over-fires on Line 3 (one of the four failing machines
     in the training window), the RL policy gets a planned-maintenance
     downtime signal that constrains the action space. Quantify the
     $/day throughput gap.
   - If predmaint under-fires (misses a real failure precursor), an
     unplanned line-stop ($12,000) collides with an active RL policy.
     What's the agent's expected disposition under the post-WSH ladder?

C. Sprint 1 + 2 → Sprint 3 RL safety-envelope blind spots:
   - The canonical case: vision says "good" (0.91), predmaint says
     "healthy" (0.08 fail-prob), RL pushes line speed to 60 boards/min
     (right at the post-WSH ceiling). A real safety_critical_defect on
     that board passes through and a worker on the line picks it up.
     What's the WSH-notifiable exposure × probability across the year?

D. MOM/WSH hard-line robustness:
   - With WSH-affecting categories at hard shadow, what is the FP load
     on the manual-review queue? At $35/min × N false-routes, is the
     60-min SLA achievable?
   - Adversarial sensor noise designed to push a healthy machine's
     score to 0.39 (just under the predmaint alarm floor): how vulnerable
     are we?

E. Sprint 4 → cross-cascade detection:
   - For each Phase 7 robustness finding above, name the Phase 13 drift
     signal that would detect it in production. If no signal catches
     it, that's an MLOps gap — flag it.

Severity-rank all findings; for each, name blast-radius in $, detection
cadence (vision weekly / sensor daily / RL per-deployment), and mitigation.

After /redteam.md is written, stop and wait for /codify.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ `04-validate/redteam.md` exists with at least 8 findings, severity-ranked
- ✓ Each finding names blast-radius in $, detection cadence, mitigation
- ✓ At least one cross-sprint finding (vision → agent or predmaint → RL or RL → agent autonomy ladder)
- ✓ MOM/WSH hard-line robustness checked (FP load on queue + adversarial-just-under-floor)
- ✓ Each robustness finding mapped to a Phase 13 detection signal (or flagged as MLOps gap)
- ✓ Stop signal pending `/codify`

**Signals of drift — push back if you see:**

- ✗ Findings that don't cite blast-radius in $ — ask "which row of `specs/business-costs.md` grounds the dollar amount?"
- ✗ Per-sprint findings only (no cross-sprint) — ask "what's the cascade impact? A robust vision alone is useless if the agent above it allows a setpoint that triggers a defect cascade."
- ✗ A finding without a detection signal — ask "if this fires in production, which Phase 13 signal catches it? If none, that's an MLOps gap to flag."
- ✗ "Rebuild from scratch" as a mitigation — ask "what's a mitigation we can ship tonight, within the existing scaffold?"
- ✗ Inventing findings (no source data) — ask "which holdout, which board_id, which machine_id, which file proves this?"

---

## 3. Things you might not understand in this step

- **Cascade red-team** — stressing the chain end-to-end, not per-layer
- **Blast radius** — how many users / boards / $ exposure / regulator visibility a failure produces
- **Severity ranking** — ordering findings by (probability × blast radius), not by how scary they sound
- **Detection cadence** — how fast a Phase 13 drift signal would catch the failure in production
- **Mitigation** — a fix shippable tonight, within the scaffold, not a future research project

---

## 4. Quick reference (30 sec, generic)

### Cascade red-team

Stress-testing the chain end-to-end rather than per-layer. Each individual model can be robust on its own holdout while the joint cascade fails on a coordinated input. The canonical case tonight: vision QC says "good" (0.91 confidence), predmaint says "healthy" (0.08 fail-prob), RL pushes line speed to 60 boards/min. A real safety_critical_defect on that board passes through and a worker downstream picks it up — the cascade fails despite all three upstream models scoring high. Cascade red-team finds these joint failures.

### Blast radius

The size and visibility of a failure. Three components: how many boards / workers see it; how much $ it costs (FN × $4,200 major-defect, FP × $85 false-scrap, equipment × $50,000, WSH × $1M+); how visible it is to regulators (private customer complaint vs MOM Inspectorate audit vs CEO-level escalation under WSH Act personal liability for directors). A finding with a large blast radius and a clear detection signal warrants immediate attention; a finding with a small blast radius and no detection is a future-task.

### Severity ranking

Ordering findings by (probability × blast radius), not by how scary they sound or how much effort they took to discover. A finding that costs $50/year in expected FN cost is lower severity than one that costs $5M/year, even if the second is rarer. Severity ranking forces you to allocate mitigation effort against actual risk, not against how loudly the finding presents.

### Detection cadence

How fast a Phase 13 drift signal would surface the failure in production. Vision weekly, sensor daily, RL per-deployment. A finding with no detection cadence is silent — it can run for months before anyone notices. A finding with detection at the right cadence is bounded — a regression can run for at most one window before alerting.

### Mitigation

A fix shippable tonight, within the scaffold. "Retrain with more data" is a mitigation if the data is on hand. "Add a new architecture" is a research project, not a mitigation. The Phase 8 deployment gates committed to specific monitoring; mitigations that fall within those monitors are shippable, those that don't are research.

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 7 /redteam, where I
am stress-testing the LumenCircuit industrial AI cascade end-to-end.

Read `workspaces/metis/week-07-manufacturing/playbook/workflow-07-redteam.md` for
what this step does, and read `workspaces/metis/week-07-manufacturing/journal/`
and `workspaces/metis/week-07-manufacturing/04-validate/redteam.md` for the
current state.

Explain "<<< FILL IN: concept name, e.g. cascade red-team >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current LumenCircuit state
3. Implications for the finding I'm about to write (or just wrote) in /redteam
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

- [ ] `04-validate/redteam.md` exists with ≥8 findings, severity-ranked
- [ ] Each finding has blast-radius $, detection cadence, mitigation
- [ ] At least one cross-sprint finding documented
- [ ] MOM/WSH hard-line robustness checked
- [ ] Each finding mapped to a Phase 13 signal or flagged as MLOps gap
- [ ] Claude Code stopped, waiting for `/codify`

**Next file:** [`workflow-08-codify.md`](./workflow-08-codify.md)
