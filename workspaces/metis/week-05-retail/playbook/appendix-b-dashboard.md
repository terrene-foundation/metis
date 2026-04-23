<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

_[← Playbook index (README)](./README.md)_

## Appendix B — Build your own value-chain dashboard at your next job

Tonight's viewer (the `http://localhost:3000` dashboard) is a **teaching instrument**. It exists because a 3.5-hour workshop packs the whole ML value chain into one sitting — students need a "where am I" anchor that would be diffuse across weeks in a real job. Your next ML project will span weeks or months, so the pressure to show "where am I" visually drops. You probably do not need a dashboard at all — you need the Playbook in a file, a journal, and a terminal.

But if your product has multiple stakeholders who need to see progress (CMO, Legal, Ops, Finance), a value-chain dashboard is a useful shared artefact. Build your own. Here is the pattern — not the code — so you can recreate it on any stack.

### The four parts of the pattern

1. **Pipeline banner.** A horizontal strip of N stages showing the flow of your product's lifecycle. For an ML product the stages are typically: `Analyze → Plan → Discover → Predict → Decide → Monitor → Review → Codify`. Label each stage with its paradigm (USML, SML, Optimization, MLOps, MLOps again) and its clock or calendar window. Colour: green for completed, orange for current, grey for upcoming.
2. **Current-phase detail.** A one-paragraph panel under the banner: which phase you're in, the levers you're pulling this phase (3–5, from the lever taxonomy in §4.6), and when the phase ends. This is the "orientation" that a 15-minute hallway chat with a stakeholder should produce.
3. **Decision-moments checklist.** The 5 Trust-Plane decision moments for the product, each rendered as a ticked or un-ticked line. Every decision moment carries a one-line rubric criterion (see §6). When a student journals a decision that clears the criterion, the box ticks. This is the shared visible signal of "we made a judgement call and wrote it down."
4. **Module cards.** One tile per model / system / sub-product, each showing the headline numbers from its current state (baseline metric, chosen threshold, latest drift severity). The cards are read-only — decisions happen in prompts and journals, not on the dashboard. The dashboard just mirrors state.

### The contract that makes it work

The dashboard is a view over a **single state artefact** — one JSON file (or one row in a database) that the backend owns and the dashboard polls. The state artefact has three top-level keys:

- `pipeline`: the ordered list of stages with their metadata (id, label, clock)
- `current`: what stage / phase the product is in right now, plus which levers
- `decision_moments`: the list of 5 rubric-anchored decisions with `completed: true|false`

Two endpoints govern it: `GET /state/current` (the dashboard polls this every 2–5 seconds) and `POST /state/advance` (the engineer calls this at the start of each phase). The polling interval is a taste call — 2s feels alive in a workshop, 30s is enough in real product work.

### When to build it

- **Day 1 of any ML project** if the stakeholders need a shared visible progress signal. A 200-line HTML file and a two-endpoint state contract is a one-afternoon build.
- **Before a major review** if the project has been running long enough that nobody remembers what was decided three months ago. The decision-moments checklist is your receipt trail.
- **Never** if you are the sole stakeholder AND you keep rigorous journal entries. The journal is the source of truth; the dashboard is a viewing convenience.

### When NOT to build it

- Your team uses Linear / Jira / Notion and is disciplined about status. Those tools already render a view like this; adding a custom dashboard competes for attention.
- The product is a one-person research project. A personal journal + the Playbook PDF open in a tab is lighter weight.
- You plan to build it and then stop maintaining it. An outdated dashboard is worse than no dashboard — it tells stakeholders a lie.

### The real portable artefact is the Playbook, not the viewer

You do not need a dashboard to run the 14 phases. You do need the Playbook, a journal file, and the rubric. If the dashboard doesn't happen, the workflow still ships. If the Playbook doesn't happen, no dashboard will save you.

Tonight's viewer is the scaffolding around the Playbook. The Playbook is what you take with you.

---

**END OF PLAYBOOK — v2026-04-23 · Universal Edition · Week 5 (Arcadia Retail) instantiation**
