<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

_[← Playbook index (README)](./README.md)_

## Appendix B — Build your own industrial AI dashboard at your next plant

Tonight's viewer (the `http://localhost:3000` dashboard) is a **teaching instrument**. It exists because a 3.5-hour workshop packs the whole industrial AI value chain (See → Predict → Optimize → Coordinate) into one sitting — students need a "where am I" anchor that would be diffuse across weeks in a real job. Your next industrial AI project will span months, so the pressure to show "where am I" visually drops. You probably do not need a dashboard at all — you need the Playbook in a file, a journal, and a terminal.

But if your plant has multiple stakeholders who need to see progress (Head of Quality, Head of Operations, Head of EHS, Legal Counsel), a value-chain dashboard is a useful shared artefact. Build your own. Here is the pattern — not the code — so you can recreate it on any stack.

### The four parts of the pattern

1. **Pipeline banner.** A horizontal strip of N stages showing the flow of your product's lifecycle. For an industrial AI suite the stages are typically: `Analyze → Plan → See → Predict → Optimize → Coordinate → Monitor → Audit → Codify`. Label each stage with its paradigm (Transfer Learning, Time-series, RL, Agent, MLOps) and its clock or calendar window. Colour: green for completed, orange for current, grey for upcoming.
2. **Current-phase detail.** A one-paragraph panel under the banner: which phase you're in, the levers you're pulling this phase (3–5, from the lever taxonomy), and when the phase ends. This is the "orientation" that a 15-minute hallway chat with the Head of Quality should produce.
3. **Decision-moments checklist.** The 5 Trust-Plane decision moments for the product, each rendered as a ticked or un-ticked line. Every decision moment carries a one-line rubric criterion. When a journal entry clears the criterion, the box ticks. This is the shared visible signal of "we made a judgement call and wrote it down" — invaluable at an MOM Inspectorate audit.
4. **Module cards.** One tile per model / system / sub-product, each showing the headline numbers from its current state (baseline metric, chosen threshold or weight, latest drift severity). Tonight's six cards: vision QC / predmaint / RL / agent / drift / inspector queue. The cards are read-only — decisions happen in prompts and journals, not on the dashboard.

### The contract that makes it work

The dashboard is a view over a **single state artefact** — one JSON file (or one row in a database) that the backend owns and the dashboard polls. Tonight the artefact is `GET /state/current` — the aggregator at `src/manufacturing/backend/routes/state.py` returns `{ phases, decisions, sprints, mom_mandate_active }`.

Two endpoints govern it: `GET /state/current` (the dashboard polls this every 2–5 seconds) and the per-action POSTs at `/inspect/vision/promote`, `/optimize/rl/reward_function`, `/agent/policy`, `/drift/retrain_rule` (the engineer fires these to change state). The polling interval is a taste call — 2s feels alive in a workshop, 30s is enough in real plant work.

### When to build it

- **Day 1 of any industrial AI project** if the plant managers + EHS + Legal need a shared visible progress signal. A 200-line HTML file and a one-endpoint state contract is a one-afternoon build.
- **Before an MOM Inspectorate audit** if the project has been running long enough that nobody remembers what was decided three months ago. The decision-moments checklist is your receipt trail.
- **Never** if you are the sole stakeholder AND you keep rigorous journal entries. The journal is the source of truth; the dashboard is a viewing convenience.

### When NOT to build it

- Your team uses an existing MES (Manufacturing Execution System) cockpit and is disciplined about status. Those tools already render a view like this; adding a custom dashboard competes for attention.
- The product is a one-engineer research project. A personal journal + the Playbook PDF open in a tab is lighter weight.
- You are building it because "every plant has an MES dashboard." That's a vibes-driven build; come back when there's a stakeholder who'll use it.

### The week-over-week reuse pattern

The Week 5 retail dashboard (Arcadia Retail Intelligence Suite), the Week 6 content-platform dashboard, and the Week 7 manufacturing dashboard (LumenCircuit Industrial AI Suite) share the same four-part pattern: pipeline banner across the top, current-phase detail, decision-moments checklist, module cards. Only the LABELS differ — Week 5's modules are segmentation/recommender/allocator/drift; Week 6's modules are image/text/fusion/drift × 3; Week 7's modules are vision/predmaint/RL/agent/drift × 3 + queue. The pattern transfers because the meta-shape (cascade of ML stages with stakeholder visibility) transfers.

The transfer is the lesson: at your next plant, reach for this pattern when you need a multi-stakeholder cockpit — Quality + Operations + EHS + Legal in one view, audit-ready by construction.
