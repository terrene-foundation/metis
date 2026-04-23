<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# The ML Decision Playbook — Week 5 (Retail, Unsupervised + Recommender)

**Version:** 2026-04-23 · **License:** CC BY 4.0

## How to use this Playbook

This is the student-facing procedure for tonight's retail workshop. It is the same 14-phase universal procedure as Week 4 — same shape, same rubric — applied to a **new domain** (retail customer intelligence) with a **new ML family** (unsupervised segmentation plus a recommender-strategy choice).

**Tonight skips the build, not the routine.** The retail backend, viewer, data generator, baseline K=3 clustering run, baseline content-based recommender, and the drift monitor with reference data already registered are all pre-provisioned before class starts — you do not scaffold or wire anything. What you DO still run is the COC routine you know: `/analyze` (short — inventory what's pre-built and what remains to decide), `/todos` (draft the 14 Playbook phases as todos; instructor gate), `/implement` (the Playbook phases), `/redteam`, `/codify`. The Playbook phases are the CONTENT of `/implement`. See the table in the "The Playbook runs inside `/implement`" section below.

Read this document once end-to-end before class so the shape is familiar. During class, keep it open; jump to the phase you are running.

Every phase follows the same shape:

- **Trust-plane question** — the single decision you own for this phase.
- **Prompt template** — what you type to Claude Code to execute the phase.
- **Evaluation checklist** — how you judge whether the output is good.
- **Journal schema** — what you record when you decide.
- **Common failure modes** — the 2–3 ways this phase usually goes wrong.
- **Artefact** — the file on disk that proves the phase happened.

Two planes are at work. The **Trust Plane** is you: framing, judging, approving. The **Execution Plane** is Claude Code plus the retail datasets and the pre-provisioned backend: code, trained models, segment assignments, recommender leaderboards, dashboards. If the answer is "what" or "how", Execution owns it. If the answer is "which", "whether", "who wins and who loses", or "is it good enough to ship" — Trust owns it, which means you own it.

## How to prompt — the delegation skill

This is the single most important skill the course teaches. You are a **commissioner**, not a coder. Your prompts should sound like a founder briefing a team — not like a developer dictating implementation.

**Every prompt you write should contain these 5 elements:**

1. **Objective** — what business outcome you want, in plain language. _"I need a small set of customer segments my marketing team can build campaigns around."_
2. **Boundaries** — what matters, what doesn't, what costs what. _"A converted recommendation is worth $18; a wasted impression costs $14. Stability across months matters more than squeezing an extra 0.02 silhouette."_
3. **Expected output** — what deliverable you want back. _"Show me a comparison of the clustering approaches. Recommend one. I decide."_
4. **Checks** — what could go wrong, what would make you change your mind. _"Flag any segment that disappears when you re-run on a different month — that means the segment isn't real."_
5. **Decision authority** — make clear what YOU will decide vs. what CC executes. _"You cluster, profile, and compare. I pick the segment count and approve the campaign map."_

**What your prompt should NEVER contain:**

- Library names, class names, function signatures, import paths
- Python code or code snippets
- API parameter names or configuration objects
- File paths to source code (data file paths are fine — that's context, not implementation)

Claude Code has the specs, the skills, and the framework documentation. It knows which libraries to use and how to call them. **If you tell it how, you're doing its job. If you tell it what and why, you're doing yours.**

**Bad prompt** (doing CC's job):

> _"Using sklearn.cluster.KMeans with n_clusters=5, fit on the RFM feature matrix and then UMAP-reduce to 2D for visualization..."_

**Good prompt** (doing YOUR job):

> _"Cluster Arcadia's active customers into behavioural segments. Try three different approaches — one that expects round blobs, one that finds dense pockets, one that builds a nested tree — and compare them on stability and on how interpretable the resulting segments are. Show me the leaderboard in business terms. I'll pick the count and the approach."_

The prompt templates below model this style. Adapt them to your own words — the templates are starting points, not scripts.

## The Playbook runs inside `/implement`

The 14-phase Playbook is not a replacement for the COC phases you already know — it is the **content** of your `/implement` phase. Before you run Playbook Phase 1, you run `/analyze` (inventory what the pre-built Arcadia baseline commits to, and name the ML decisions that are still yours). Before you start Playbook Phase 4, you run `/todos` (draft all 14 Playbook phases as explicit tasks and clear them with the instructor — this is the human gate). During `/implement`, each Playbook phase completes one todo. After Playbook Phase 13, you run `/redteam` (sweep stability / proxy-leakage / operational-collapse) and `/codify` (write the transferable lessons into `.claude/skills/project/`).

Routine is the scaffold; decisions are the content. The ML Decision Playbook is the decision content that lives inside the COC routine you already run for every product.

| Clock     | COC phase                 | Playbook phases inside        | Output                                                            |
| --------- | ------------------------- | ----------------------------- | ----------------------------------------------------------------- |
| 2:00–2:10 | `/analyze`                | (pre-phase inventory)         | `01-analysis/failure-points.md`, `01-analysis/assumptions.md`     |
| 2:10–2:15 | `/todos`                  | —                             | `todos/active/phase_N_*.md` (14 phases as todos; instructor gate) |
| 2:15–3:15 | `/implement` — Sprint 1   | Phases 1, 2, 3, 4, 5, 6, 7, 8 | `journal/phase_{1..8}_*.md`                                       |
| 3:15–3:45 | `/implement` — Sprint 2   | Phases 10, 11, 12             | `journal/phase_{10..12}_*.md`                                     |
| 3:45–4:00 | `/implement` — mid-sprint | scenario inject: PDPA         | `journal/phase_11_postpdpa.md`, `journal/phase_12_postpdpa.md`    |
| 4:00–5:00 | `/implement` — Sprint 3   | Phase 13                      | `journal/phase_13_*.md` + drift report                            |
| 5:00–5:20 | `/redteam`                | Phase 7 final sweep           | `04-validate/redteam.md`                                          |
| 5:20–5:30 | `/codify` + `/wrapup`     | Phase 9                       | `.claude/skills/project/week-05-lessons.md`, `.session-notes`     |

`/analyze` and `/todos` take 15 minutes together and are not busywork: they force you to declare, in writing, what the pre-built baseline already commits to (K=3, content-based recommender, reference data already registered) and what remains open for you to decide (K, strategy, cold-start disposition, PDPA constraint classification, drift thresholds). Week 4's students often felt scaffolding ate their lifecycle; Week 5 fixes the lifecycle without dropping the routine.

## The five Trust Plane decision moments

Tonight collapses into five high-pressure decision moments. These are where the rubric has teeth — the places where a lazy prompt ships a demo that _looks_ identical to a careful student's demo but collapses under any real scrutiny. Know them before you start.

1. **Pick K and defend in dollars** (Phase 6). Not "silhouette said 5". Rather: "5 because marketing can run 5 parallel campaigns; 7 costs $X in setup with no realistic chance of uplift, and segment-stability drops from 88% to 72% at K=7 on the hold-out month." Stability and actionability have floors, not just targets.
2. **Name each segment and declare a differentiated action per segment** (Phase 5 + 6). If two segments get the same action, they are one segment with noise between them. Either collapse them, or defend the difference in dollars.
3. **Choose the recommender strategy with an explicit cold-start disposition** (Phase 10 + 12). Collaborative, content-based, or hybrid — and for new customers with no history, say what happens: segment modal basket (uses Sprint 1's output), catalogue popularity, or editorial curation. "Default fallback" is not an answer.
4. **Declare what goes into the RAG corpus and what stays out** (Advisor stretch, Phase 11 analogue). PDPA, legal exposure, data staleness — every exclusion has a reason.
5. **Set the grounding-failure fallback** (Advisor stretch). When the knowledge base cannot support an answer, does the Advisor say "I don't know", fall back to the popular item, or escalate to a human? This is a product decision.

Decision moments 4 and 5 only apply if you reach the Advisor stretch in Sprint 3. The first three are non-negotiable for every student tonight.

## Phase summary

| #   | Phase                            | Sprint  | Artefact                                                                    | Rubric dimensions pressured       |
| --- | -------------------------------- | ------- | --------------------------------------------------------------------------- | --------------------------------- |
| 1   | Frame                            | S1      | `journal/phase_1_frame.md`                                                  | Harm framing, metric-cost linkage |
| 2   | Data audit                       | S1      | `journal/phase_2_data_audit.md`                                             | Trade-off honesty                 |
| 3   | Feature framing (UNFOLDED)       | S1      | `journal/phase_3_features.md`                                               | Constraint, trade-off honesty     |
| 4   | Candidates (algorithm × K sweep) | S1      | `data/segment_leaderboard.json`                                             | (no journal — decision in 5)      |
| 5   | Implications (named segments)    | S1      | `journal/phase_5_segment_selection.md`                                      | Trade-off honesty, reversal       |
| 6   | Metric + threshold (K + floors)  | S1      | `journal/phase_6_segment_count.md`                                          | Metric-cost linkage, reversal     |
| 7   | Red-team (3 new dimensions)      | S1 + S2 | `journal/phase_7_red_team.md`                                               | All 5 dimensions                  |
| 8   | Deployment gate                  | S1 + S2 | `journal/phase_8_gate.md` + `phase_8_postpdpa.md` + registry record         | Reversal, constraint              |
| 9   | Codify                           | Close   | `journal/phase_9_codify.md` + `PLAYBOOK.md` delta                           | (meta — not scored on rubric)     |
| 10  | Objective (rec four-signal)      | S2      | `journal/phase_10_rec_objective.md`                                         | Metric-cost linkage, trade-off    |
| 11  | Constraints                      | S2 × 2  | `journal/phase_11_constraints.md` + `phase_11_postpdpa.md`                  | Constraint classification         |
| 12  | Recommender offline eval         | S2 × 2  | `data/recommender_plan_*.json` + `journal/phase_12_rec.md` + `_postpdpa.md` | Trade-off honesty, constraint     |
| 13  | Drift triggers (segment churn)   | S3      | `data/drift_report.json` + `journal/phase_13_retrain.md`                    | Reversal condition                |
| 14  | Fairness                         | Week 7  | (deferred)                                                                  | —                                 |

Week 5 runs phases **1, 2, 3, 4, 5, 6, 7, 8** in Sprint 1 (segmentation), **10, 11, 12** in Sprint 2 (recommender), **13** in Sprint 3, and **9** in the Close block. **Phase 3 is unfolded this week** (Week 4 folded it into Phase 2) — pre-cluster feature selection has higher stakes than pre-model feature selection, because an ethically loaded feature does not just bias a model, it _creates a segment_ that is really a proxy for a protected class. Phase 14 (Fairness) is deferred to Week 7.

---

# Sprint 1 — Unsupervised ML: Customer Segmentation (Phases 1–9)

The hardest shift from Week 4 lands in Phase 6. Unsupervised learning has no label — there is no "accuracy" to optimise. The metric conversation changes shape entirely. Read Phase 6 carefully before Sprint 1 begins.

---

## Phase 1 — Frame

- **Sprints**: Sprint 1 (first ~7 min).
- **Trust-plane question**: What are we trying to discover, for which customers, on what time window, and what is the cost of drawing the wrong segments?
- **Prompt template**:
  > _"Read the product brief. I need a clear problem statement for the Customer Segmentation module. Tell me: which customers are in scope, which are out, what behavioural window we look at, how many segments we will commit to using even before we see the data, and what it costs when the segmentation is wrong — both the wasted-campaign cost when a customer is sent the wrong offer ($45 per customer), and the touch-cost of contacting them at all ($3). Don't assume anything — if the brief is vague on scope, ask me."_
- **Evaluation checklist**:
  - [ ] Customer scope precise (not "customers" but e.g. "18,000 customers active in the last 90 days, excluding staff accounts and bot traffic").
  - [ ] Behavioural window named in days or months (not "recent activity").
  - [ ] Commitment stated on the operational segment ceiling ("marketing can run at most 6 parallel campaigns") BEFORE the clustering runs.
  - [ ] Cost framing names both the wrong-segment cost ($45 per customer) and the touch cost ($3 per contact), and ties them to a realistic volume ("if we misclassify 5% of 18,000 active customers, that is $40,500 of wasted campaign spend plus damage to open rates").
  - [ ] No silent assumptions.
- **Journal schema**:
  ```
  Phase 1 — Frame
  Customer scope: ____
  Behavioural window: ____
  Operational segment ceiling: ____ (who set it, why)
  Cost framing: $__ per wrong-segment assignment × __ customers = $__ at risk
  What I would change my mind on: ____
  ```
- **Common failure modes**:
  - Target drifts into fuzzy language ("segment our customers") — downstream phases lose grounding.
  - Operational ceiling set after seeing the elbow plot — the algorithm now dictates the business, not the reverse.
  - Cost framing stated as "segments matter" without dollars — scores 2/4 on Harm framing rubric.
- **Artefact**: `journal/phase_1_frame.md`.

---

## Phase 2 — Data Audit

- **Sprints**: Sprint 1 (~8 min).
- **Trust-plane question**: Is the customer data trustworthy enough to cluster on at all?
- **Prompt template**:
  > _"Audit Arcadia's customer data before we cluster anything. I need to know: is the data trustworthy? Check for duplicate customer records, staff and bot contamination, customers with only one observation (too sparse to segment), missing values across the key behavioural columns, outliers that will dominate the clustering, and any field that is really a derived label in disguise. Recommend conditions under which the data is safe to cluster. I'll make the final call."_
- **Evaluation checklist**:
  - [ ] Duplicate / staff / bot / singleton-observation checks reported with specific counts, not generalities.
  - [ ] Outlier behaviour characterised (the top 1% of spenders will dominate any distance-based clustering — flagged, not hidden).
  - [ ] Missingness pattern per behavioural column named.
  - [ ] Any suspected label-in-disguise field surfaced (e.g. a pre-existing "tier" column that would cause the clustering to rediscover an old rule).
  - [ ] Recommendation offered (accept / accept-with-conditions / reject) — you decide.
- **Journal schema**:
  ```
  Phase 2 — Data Audit
  Accepted? Yes / Conditional / No
  Conditions applied: ____
  Known risks I am accepting: ____
  Label-in-disguise columns found: ____
  ```
- **Common failure modes**:
  - Data accepted as-is; no call made on duplicates or singletons — drives noisy segments later.
  - Top-1% spenders not flagged — they dominate every K-means result and the segmentation reduces to "rich vs not rich".
  - A pre-existing tier column left in the feature set — the clustering "discovers" the 2020 hand-authored segmentation and the CMO sees no value.
- **Artefact**: `journal/phase_2_data_audit.md`.

---

## Phase 3 — Feature Framing (UNFOLDED THIS WEEK)

Week 4 folded this phase into the Data Audit. Week 5 unfolds it. Pre-cluster feature selection has higher stakes than pre-model feature selection: an ethically loaded feature does not merely bias a model, it _creates a segment_ that is really a proxy for a protected class — and the segment then looks like a legitimate behavioural pattern to the marketing team. Phase 3 gets its own pass this week.

- **Sprints**: Sprint 1 (~10 min).
- **Trust-plane question**: Which features do we cluster on, which do we hold out, and for each held-out feature, is it held out because it is unavailable, leaky, or ethically loaded?
- **Prompt template**:
  > _"List every candidate feature for segmentation — transaction frequency, recency, average basket, channel mix, category mix, browsing depth, day-of-week pattern, promo responsiveness, and any demographic fields we hold. For each one, classify it on four axes: (a) available at segmentation time — yes/no, (b) leaky or label-in-disguise — yes/no with evidence (a pre-existing loyalty tier would rediscover the old rule), (c) ethically loaded or PDPA-sensitive — yes/no with rationale (postcode is a proxy for income; under-18 flag is PDPA-sensitive; inferred sensitive attributes like health or religion are red lines), (d) engineered or raw (if engineered, explain the derivation). Also run a proxy-check: for each demographic-like feature, test whether it is highly correlated with a cluster assignment produced without it — if dropping postcode changes 30% of cluster assignments, that means postcode was acting as a proxy. Recommend a feature set. I'll make the final call."_
- **Evaluation checklist**:
  - [ ] Every candidate feature classified on all four axes.
  - [ ] Proxy-for-protected-class check reported — for each demographic-like feature, a paragraph naming whether it is acting as a proxy for a cluster that would form anyway.
  - [ ] Ethically loaded features have a defensible rationale for inclusion or exclusion — not a drive-by "OK".
  - [ ] Engineered features (RFM, tenure decile, channel-mix entropy) have a derivation explanation.
  - [ ] Recommendation offered but not auto-applied.
- **Journal schema**:
  ```
  Phase 3 — Features
  Included: ____
  Excluded (with reason per feature): ____
  PDPA-sensitive features flagged: ____
  Proxy-for-protected-class concerns: ____
  ```
- **Common failure modes**:
  - Postcode or neighbourhood-derived feature included without a proxy check — the resulting segmentation is a PDPA/fairness problem dressed up as behavioural clustering.
  - Under-18 flag left in "because it's just a field" — the mid-Sprint 2 PDPA injection will punish this.
  - Engineered feature added without derivation — becomes a hidden label-leakage vector.
- **Artefact**: `journal/phase_3_features.md`.

---

## Phase 4 — Candidates (Algorithm × K sweep)

- **Sprints**: Sprint 1 (~10 min). Keep the sweep quick — the retail scaffold runs it in under 90 seconds against the preloaded active-customer feature set.
- **Trust-plane question**: Which clustering approaches and which K values are reasonable candidates for this problem?
- **Prompt template**:
  > _"Run a clustering sweep on Arcadia's active customers. Try three different approaches across a range of K values: a K-means-style approach at K = 3, 5, and 7 (different cluster counts), a density-based approach with tuned density (which picks its own cluster count and may leave some customers unassigned), and a hierarchical tree cut at 5. Also apply one pass of dimensionality reduction for preprocessing and one for visualisation. For each approach, use a stability protocol: run it twice on two different months of behaviour and report the percentage of customers who stay in the same cluster across runs. Show me a leaderboard comparing them all on: how well-separated the clusters are, how stable they are month over month, how many customers are unassigned or in tiny segments, and a one-paragraph plain-language profile per resulting segment so I can judge interpretability. I'll pick the count and the approach in the next phase."_
- **Evaluation checklist**:
  - [ ] Candidate sweep spans three algorithmic shapes (blob-expecting at three K values, density-based, hierarchical).
  - [ ] Each candidate has a stated risk ("density-based can leave 20% of customers unassigned — is that acceptable?").
  - [ ] The current rule-based five-segment system is cited as the naive baseline to beat.
  - [ ] Stability protocol executed on two windows — the output names a percentage of customers who stayed in the same cluster, per candidate.
  - [ ] Dimensionality reduction used as a pre-step AND as a visualisation aid — both purposes surfaced separately.
- **Journal schema**: _(no journal entry — decision happens in Phase 5)_
- **Common failure modes**:
  - Student prompts for "AutoML the clustering candidates" in the Week 4 style — the retail scaffold does NOT offer an AutoML path for clustering (clustering is not a supported AutoML task type in the framework we use). The scaffold provides a pre-wired algorithm × K sweep endpoint. If Claude Code returns a ValueError about AutoML, re-prompt in terms of "try three clustering approaches across K values" and let Claude Code hit the scaffold's sweep endpoint.
  - Only one clustering family tried ("I'll do K-means at K=5") — loses the fair comparison, and in particular loses the density-based "some customers are outliers" option.
  - Stability protocol skipped — you ship a segmentation that re-shuffles 30% of customers next month, destroying campaign continuity.
  - Dimensionality reduction treated as optional — on ~40 behavioural features, un-reduced clustering usually finds noise. At least one candidate must run with reduction.
  - Cluster count picked inside Phase 4 ("let me pick K=5") — the decision belongs in Phase 6, not here.
- **Artefact**: `data/segment_leaderboard.json`.

---

## Phase 5 — Model Implications (Segment Selection)

- **Sprints**: Sprint 1 (~10 min).
- **Trust-plane question**: Given the leaderboard, which clustering approach — and at what cluster count — do I stake my career on, and why?
- **Prompt template**:
  > _"Compare the clustering approaches on the leaderboard. For each one, tell me: how well-separated the resulting segments are, how stable they are month-over-month, how many customers are unassigned or in tiny clusters, and whether the segments tell a business story a non-technical CMO can recognise — for each segment, write a one-paragraph profile in plain language ("high-frequency weekend browser who converts on promo"). Then recommend one approach, but explain the trade-offs as if you're briefing the CMO who cares about stability and campaign actionability above statistical purity. I'll make the final pick."_
- **Evaluation checklist**:
  - [ ] All candidates compared on the same diagnostic numbers.
  - [ ] Stability is reported month-over-month as a percentage, and the recommendation factors it in.
  - [ ] Recommendation explicitly mentions how many customers would be left unassigned, and whether that is acceptable (density-based approaches may leave 10–25% unassigned).
  - [ ] Segment profiles are in plain business language, not "Cluster 3: high RFM low entropy".
  - [ ] Recommendation is defensible in 30 seconds to a non-technical CMO.
- **Journal schema**:
  ```
  Phase 5 — Segment Selection
  Picked approach: ____ (run ID: ____)
  Rejected alternatives: ____
  Why not the statistically "best" approach, if applicable: ____
  Unassigned customers tolerated: ____% (rationale: ____)
  What I would re-cluster with: ____
  ```
- **Common failure modes**:
  - Student picks the highest silhouette score without checking stability — ships a segmentation that collapses in two months.
  - Student accepts Claude Code's recommendation verbatim — no Trust Plane decision happened.
  - Segment profiles written in statistical language ("Cluster 3 has high_freq=0.81, low_promo_resp=0.22") — the CMO cannot act on that.
- **Artefact**: `journal/phase_5_segment_selection.md`.

---

## Phase 6 — Metric + Threshold (K + three floors)

**This is the big one for Week 5 — read it twice.** Unsupervised learning has no ground-truth label. There is no "accuracy", no RMSE, no MAPE. The metric conversation changes shape: instead of optimising a single number, you commit to three _floors_ — minimum thresholds any shippable segmentation must clear. Then you pick the K that clears all three floors AND maximises business value.

- **Sprints**: Sprint 1 (~12 min).
- **Trust-plane question**: What are the three floors (separation, stability, actionability) any shippable segmentation must clear — and at what K do we clear all three?
- **Prompt template**:
  > _"I need to decide how many segments to ship. There's no label to score against, so I want to judge this on three floors, not a single number — a shippable segmentation must clear all three or we ship nothing: (1) a **separation floor** — how well-separated the clusters are in plain terms, with a minimum acceptable value I commit to before seeing any results; (2) a **stability floor** — using a re-sampling protocol, what fraction of customers stay in the same segment if we re-cluster on a different month of behaviour, with a minimum acceptable value (conventionally 0.80 or above on the overlap measure); (3) a **business-actionability floor** — for each proposed K (try 3, 4, 5, 6, 7, 8), write me a one-paragraph profile of each segment and tell me whether the marketing team could plausibly build a \_distinct_ campaign for each one. If two segments get the same action, they are one segment with noise; collapse them. Now tie all three floors back to dollars with a counterfactual lift estimate: for each K, estimate the expected lift over the current rule-based five-segment system. Use the $45 wrong-segment campaign cost and the $18 average basket lift from a converted recommendation as the two sides of the ledger — a better segmentation sends fewer customers to the wrong campaign (saving $45 per customer on avoided waste) and surfaces more convertible recommendations (gaining $18 per additional converted click). Show me a table of K vs separation vs stability vs actionability vs dollar-lift-vs-baseline. I will pick the K."\_
- **Evaluation checklist**:
  - [ ] All three floors declared with numeric thresholds BEFORE the student sees the leaderboard (pre-commitment matters — seeing the results first and then reverse-engineering the floor is cheating).
  - [ ] Stability floor uses a re-sampling protocol (bootstrap, two-month split, or similar); the threshold is a specific number (e.g. 0.80 on the overlap measure).
  - [ ] Actionability floor tested by writing a one-line distinct action per segment; if two segments share an action, either one is collapsed or the difference is defended in dollars.
  - [ ] Dollar-lift-vs-baseline computed for each K using a counterfactual — "at this K, the segmentation would send N fewer customers to the wrong campaign ($45 each saved) and surface M more convertible recommendations ($18 each gained) vs the current rule-based system" — rather than a raw cost-of-error calculation.
  - [ ] Sensitivity / reversal condition names a signal, a threshold, and a duration window (e.g. "if stability drops below 0.80 on two consecutive monthly re-clusters, drop to a smaller K").
- **Journal schema**:
  ```
  Phase 6 — Metric + K
  Separation floor: ____ (threshold: ____)
  Stability floor: ____ (protocol: ____; threshold: ____)
  Actionability floor: per-segment distinct action table below
  | Segment | One-line action |
  |---|---|
  | 1 | ____ |
  | ... | ____ |
  Chosen K: ____
  Counterfactual lift vs current rule-based system: $____ per month
    (sources: $45 × __ customers avoided-wrong-campaign + $18 × __ additional converted recs)
  Sensitivity flip point (signal + threshold + duration): ____
  ```
- **Common failure modes**:
  - Student asks for a single "accuracy" number — there isn't one. The prompt must surface three floors.
  - K picked on separation alone — ignores stability (ships a segmentation that reshuffles next month) and actionability (produces two segments that earn the same campaign), scores 1/4 on metric-cost linkage.
  - Floors set _after_ seeing the leaderboard — the pre-commitment principle is the whole point; post-hoc floors are always exactly where the leaderboard winner landed. Grader checks timestamps.
  - Dollar-lift stated as raw cost-of-error with no baseline comparison — scores 2/4 on metric-cost linkage. The counterfactual ("vs current rule-based system") is what turns a number into a business case.
  - Two segments with identical one-line actions shipped without collapsing — scores 1/4 on trade-off honesty. If marketing would treat two segments the same, they are one segment.
- **Artefact**: `journal/phase_6_segment_count.md`.

---

## Phase 7 — Red-Team (AI Verify: Transparency, Robustness, Safety)

Week 5 keeps the AI Verify frame (Transparency, Robustness, Safety) but adds three unsupervised-specific failure modes under Robustness and Safety: **re-seed churn** (does the clustering produce different segments just from a different random seed?), **proxy leakage** (is a segment actually a demographic proxy dressed up as behaviour?), and **operational collapse** (does one segment shrink to fewer than 2% of customers in a single month?).

- **Sprints**: Sprint 1 (~10 min).
- **Trust-plane question**: How does this segmentation fail? Who is harmed when it silently goes wrong?
- **Prompt template**:
  > _"Try to break this segmentation. I want to know three things: (1) **Transparency** — for a given customer, can you explain in one plain sentence which segment they ended up in and why? Name the top 2 behavioural features driving each segment. If we cannot explain it, marketing cannot trust it. (2) **Robustness** — where is this segmentation fragile? Run the clustering three more times with different random seeds and report how much segment membership churns ('re-seed churn' — if 20% of customers change segment just from reseeding, the segmentation is unstable by construction). Check if any segment is really a demographic proxy: for each segment, does dropping a demographic feature (postcode, age band) collapse the segment? That would mean it was a proxy, not a behavioural pattern. What happens to the smallest segment on post-Black-Friday data (operational collapse — does it shrink to less than 2% of customers)? (3) **Safety** — if this segmentation silently mis-grouped 20% of customers for a month, what is the dollar damage ($45 per wrong campaign × expected mis-grouped volume), and are the small segments the ones most likely to represent vulnerable groups (new-to-Singapore, low-income, under-18, first-language-not-English)? Rank every finding by severity. Fairness will be covered in Week 7 — note the deferral explicitly."_
- **Evaluation checklist**:
  - [ ] **Transparency**: top 2 features per segment named; a one-sentence plain explanation exists for a sample customer; if feature importance is unavailable for this clustering approach, the limitation is stated.
  - [ ] **Robustness / re-seed churn**: segment churn across different random seeds reported as a percentage; a finding is raised if it exceeds a stated threshold.
  - [ ] **Robustness / proxy leakage**: for each segment, the effect of dropping a demographic feature is reported; a finding is raised if any segment collapses when postcode / age band / tenure band is removed.
  - [ ] **Robustness / operational collapse**: smallest segment's size on post-Black-Friday data reported; a finding is raised if any segment drops below 2% of the customer base.
  - [ ] **Safety**: worst-case mis-grouping cost in dollars (using the $45 wrong-campaign cost × customer volume); small-segment vulnerable-population check surfaced even if inconclusive.
  - [ ] Fairness row ends with "deferred to Week 7 per Playbook" — explicit, not silent.
  - [ ] Findings ranked by severity with proposed mitigation per finding.
- **Journal schema**:
  ```
  Phase 7 — Red-Team (AI Verify)
  Transparency: top features per segment ____; one-sentence explanation ____
  Robustness — re-seed churn: ____%
  Robustness — proxy leakage: segments that collapse when demographic dropped: ____
  Robustness — operational collapse: smallest segment size on peak data: ____%
  Safety: worst-case mis-grouping cost $____; small-segment vulnerable-population check ____
  Fairness: deferred to Week 7 per Playbook
  Blockers: ____
  Accepted risks: ____
  Mitigations to ship with: ____
  ```
- **Common failure modes**:
  - Re-seed churn skipped — ships a segmentation that is literally a function of the random seed, with no acknowledgement.
  - Proxy leakage check skipped because the result is uncomfortable ("segment 3 really is just 'customers in the east region'") — the whole point of the check is to force that admission.
  - Operational collapse check treated as a "nice to have" — but it IS the Phase 13 drift signal. If a segment can collapse to < 2% in one month, the drift retrain rule must fire on that.
  - Transparency skipped because the clustering approach doesn't have built-in feature importance — the limitation itself is the finding, not a pass.
  - Safety dimension skipped because "segments can't really hurt anyone" — the $45 × 18,000 active customers forces it concrete.
- **Artefact**: `journal/phase_7_red_team.md`.

---

## Phase 8 — Deployment Gate

- **Sprints**: Sprint 1 (~8 min). Re-run in Sprint 2 after the PDPA injection changes the recommender constraint set.
- **Trust-plane question**: Ship or don't ship the segmentation, and on what monitoring?
- **Prompt template**:
  > _"Write the go / no-go gate for deploying this segmentation. Include: (1) what thresholds must hold for it to ship — tie them to the three signals from Phase 6 (separation, stability, actionability), (2) what we monitor on day one — name the specific signals and when they should fire an alert, (3) what triggers a rollback to the old rule-based five-segment system — a specific measurable signal, not 'if things look bad'. Then promote the segmentation from a trial stage to a pre-production stage so it is ready to go live."_
- **Evaluation checklist**:
  - [ ] Go / no-go criteria are measurable (named signal thresholds).
  - [ ] Monitoring plan names specific signals (segment-size stability, monthly reassignment rate, campaign open-rate-by-segment) and alert thresholds.
  - [ ] Rollback trigger is automatable (a specific signal the monitoring system can watch).
  - [ ] Registry stage transition executed in a legal direction (e.g. trial → pre-production), no illegal jumps.
- **Journal schema**:
  ```
  Phase 8 — Deployment Gate
  Go / No-Go: ____
  Monitoring (signal + threshold): ____
  Rollback trigger (signal): ____
  Registry transition: ____ → ____
  ```
- **Common failure modes**:
  - Monitoring plan written as prose, no signal names — grader cannot verify.
  - Rollback trigger tied to a non-existent signal.
  - No rollback path at all — "we'll just retrain if there's a problem" is not a rollback.
- **Artefact**: `journal/phase_8_gate.md`. Post-PDPA Sprint 2 re-run: `journal/phase_8_postpdpa.md`.

---

## Phase 9 — Codify

- **Sprints**: Close block (last ~8 min of class).
- **Trust-plane question**: What transfers from retail + unsupervised ML + recommender-strategy-selection to the next domain?
- **Prompt template**:
  > _"Looking back at tonight's three sprints — what did we learn that applies to ANY ML product we build next week? Give me 3 transferable lessons. And what 2 things were specific to unsupervised segmentation and recommender-strategy selection that won't transfer directly? Add a 'Week 5 lessons' section to the Playbook."_
- **Evaluation checklist**:
  - [ ] 3 transferable lessons (domain-agnostic, e.g. "when there is no label, invent three signals and commit to all three before seeing results").
  - [ ] 2 domain-specific lessons (e.g. PDPA hard-line pattern for any personal-data product; cold-start as product decision, not fallback).
  - [ ] Lessons are actionable in Week 6 (not platitudes).
  - [ ] Playbook delta appended.
- **Journal schema**:
  ```
  Phase 9 — Codify
  Transferable:
  1. ____
  2. ____
  3. ____
  Domain-specific:
  1. ____
  2. ____
  ```
- **Common failure modes**:
  - Codify skipped because time ran out — the knowledge capture is the course's entire point.
  - Lessons written as generic platitudes ("data quality matters").
- **Artefact**: `journal/phase_9_codify.md` + `Week 5 delta` section in `PLAYBOOK.md`.

---

# Sprint 2 — Recommender Strategy (Phases 10–12)

Sprint 2's shape mirrors Week 4's optimization sprint: Phase 10 defines what "good" means in dollars and in competing signals, Phase 11 classifies the rules as hard or soft, Phase 12 accepts or redesigns against offline metrics. The optimisation target is different — it is not a route, it is a recommender strategy — but the decision shape is identical.

**Scaffold note**: the retail backend ships three pre-wired recommender variants — content-based (product-to-product similarity on catalogue embeddings), collaborative (customer-to-customer similarity via a matrix-factorisation pass), and hybrid (a weighted blend plus segment-aware cold-start). There is no framework-level recommender primitive to auto-discover; Claude Code hits the pre-provided recommender endpoints. If your Sprint 2 prompt asks Claude Code to "find a recommender library and use it", the session will stall — re-prompt in terms of "evaluate the three recommender variants against the held-out session data" and let Claude Code call the scaffold's evaluation path.

Mid-sprint injection (fires at roughly T+02:05): a PDPA notice lands. Re-run Phases 11 and 12.

---

## Phase 10 — Objective Function (four competing signals)

- **Sprints**: Sprint 2 (~12 min).
- **Trust-plane question**: What does "good recommendation" mean — CTR, revenue, diversity, serendipity — and with what weighting?
- **Prompt template**:
  > _"Design the objective for the recommender. 'Good' is not one thing; it is four, and they compete. (1) **Click-through** — the operational signal the CX team watches daily. The current rule-based recommender sits at 12%; anything below that and we have regressed. (2) **Revenue** — each converted click is worth $18 in basket lift; each wasted impression costs $14. (3) **Diversity** — does the recommender show the same five hero SKUs to everyone, or does it cover the catalogue? Out of 2,000 SKUs, only ~200 will ever convert well on recommendations, but concentrating on the top 50 means the other 1,950 never sell through. Set a minimum on catalogue coverage. (4) **Serendipity** — does the recommender only surface things the customer would have bought anyway (a content-based approach is prone to this), or does it sometimes surface a relevant item the customer would not have found on their own? Serendipity lifts cross-category conversion but is the hardest to score. Show me two framings: (a) single-objective — lump all four into an 'expected profit per session' with a coverage penalty; (b) multi-objective — keep CTR, revenue-per-session, coverage, and a serendipity proxy as separate scores with weights. Recommend one, defend the weights with business reasoning from the table above, and tell me honestly what each framing sacrifices."_
- **Evaluation checklist**:
  - [ ] All four signals (CTR, revenue, diversity/coverage, serendipity) addressed — not just CTR.
  - [ ] Single-objective AND multi-objective framings both presented.
  - [ ] Weights defended with business reasoning, tied to the $18 / $14 / 12% baseline — not pulled from thin air.
  - [ ] Trade-off discussed honestly ("multi-objective protects the long tail; single-objective is cleaner but may lose $3 per session on diversity-sensitive customer segments").
  - [ ] Coverage explicitly named with a minimum threshold — coverage is the ESG-analogue of Week 4's carbon term; dropping it ships a recommender that kills the long tail.
- **Journal schema**:
  ```
  Phase 10 — Rec Objective
  Chosen: single / multi
  Terms + weights: CTR ____ | revenue ____ | coverage (min ____) | serendipity ____
  Business justification: ____
  Known limitation (which signal am I least confident in): ____
  ```
- **Common failure modes**:
  - Objective written as "maximise click-through rate" alone — ignores the other three signals; scores 2/4 on metric-cost linkage. CTR is a proxy for revenue, not a substitute.
  - Diversity / coverage dropped because "the CMO didn't ask for it this week" — the deck and the brief both call it out, and dropping it ships a recommender that kills the long tail.
  - Serendipity treated as undefinable and quietly removed — use a plain proxy ("percentage of clicks that came from a category the customer had not bought from in the past 90 days"). Something measurable beats nothing.
  - Weights pulled from thin air — 0/4 on trade-off honesty.
- **Artefact**: `journal/phase_10_rec_objective.md`.

---

## Phase 11 — Constraint Classification

- **Sprints**: Sprint 2 (~10 min). Re-run after PDPA injection.
- **Trust-plane question**: Hard or soft for each rule? Penalty for soft?
- **Prompt template (first pass)**:
  > _"List every rule the recommender must respect — inventory availability (can't recommend what's out of stock), product-page relevance (no random SKU on an unrelated page), segment-consistency (recommend within the customer's segment where possible), cold-start behaviour for new users and new SKUs, catalogue-coverage targets, the touch-budget ceiling (we do not spam), and any PDPA surfaces — minor-status, inferred sensitive attributes, cross-session tracking consent. For each one, tell me: is it a hard line that can never be crossed (law, physics, contract), or a preference we'd rather not violate but will if the cost is right? For preferences, propose a penalty in dollars. Justify each classification."_
- **Prompt template (post-PDPA injection re-run)**:
  > _"Legal just flagged a red-line: using the browsing history of any customer under 18 for personalised recommendations violates PDPA. This is law, not a preference. Update the constraint classification — which rules just changed from soft to hard? What is the new exclusion rule? Re-classify the under-18 browsing-history feature as a hard exclusion, state the per-record exposure is $220, and re-justify. Save this as a separate journal entry so we can compare before and after."_
- **Evaluation checklist**:
  - [ ] Every constraint classified with explicit rationale (law / physics / contract / preference).
  - [ ] Soft constraints have defensible penalty values.
  - [ ] No constraint labelled "probably hard" without reason.
  - [ ] Post-injection: under-18 browsing-history feature correctly re-classified as hard exclusion, with the $220-per-record PDPA exposure cited.
  - [ ] Post-injection journal names exactly what changed from the prior pass — not a full re-write.
- **Journal schema** (both passes):
  ```
  Phase 11 — Constraints
  Hard: ____ (reason each)
  Soft: ____ (penalty each)
  What changed from prior pass (post-injection only): ____
  ```
- **Common failure modes**:
  - Under-18 rule mis-classified as soft after injection (the injection exists precisely to test this — scores 1/4 on constraint classification if missed).
  - Hard-constraint set too tight → recommender cannot find any eligible SKU → student panics. Recovery: re-check whether a preference was mis-labelled as hard.
  - Penalty values unspecified ("some penalty") — 1/4 on classification rubric.
  - PDPA re-classification done but the feature itself is not removed from the training pipeline — hard constraints must change behaviour, not just live in a journal.
- **Artefact**: `journal/phase_11_constraints.md` + `journal/phase_11_postpdpa.md`.

---

## Phase 12 — Recommender Offline Evaluation (Accept / Re-tune / Redesign)

- **Sprints**: Sprint 2 (~12 min). Re-run after PDPA injection.
- **Trust-plane question**: On a held-out slice of real Arcadia sessions, does the chosen recommender clear the four offline metrics (precision@k, coverage, cold-start rate, diversity) — and is it free of pathological patterns?
- **Prompt template**:
  > _"Evaluate the recommender in three variants — one that relies on customer-to-customer similarity ('people like you bought'), one that relies on product-to-product similarity ('because you liked this'), and one that blends them. For each variant, run an offline evaluation on the held-out session data and report these four metrics side-by-side: (1) **precision@k** (of the top-k items we recommended, how many did the customer actually engage with; use k=5 and k=10), (2) **catalogue coverage** (what fraction of the 2,000 SKUs ever appeared in a top-10 list across the held-out sessions), (3) **cold-start rate** (what fraction of sessions triggered the cold-start fallback, and — for the hybrid — is the fallback the Sprint 1 segment's modal basket as intended), (4) **diversity** (within a single top-10 list, how many distinct categories are represented on average). Also confirm the hard constraints: no out-of-stock SKU was recommended; no under-18-sourced signal was used. Then look for pathological patterns — does one variant recommend the same top-5 hero SKUs to more than 30% of customers; does any variant's cold-start behaviour default to a generic catalogue popularity list instead of the segment-aware fallback the student declared in Phase 10? Recommend: accept the hybrid, re-tune the weights of one variant, fall back to a simpler variant, or re-design. Save the offline-eval report and the recommender plan for the dashboard."_
- **Evaluation checklist**:
  - [ ] All four offline metrics reported per variant: precision@5, precision@10, catalogue coverage, cold-start rate, diversity within top-10.
  - [ ] Hard constraints confirmed satisfied per variant (inventory availability; PDPA exclusion under-18 signal).
  - [ ] Cold-start behaviour confirmed to match the Phase 10 declaration (segment modal basket, or whatever was chosen) — not a silent default.
  - [ ] Pathologies named (top-5-SKU concentration, long-tail starvation, cold-start default-to-generic, diversity collapse).
  - [ ] Decision — accept / re-tune / fall back / redesign — defended with the numbers.
  - [ ] Post-injection: pre-PDPA and post-PDPA recommender plans both on disk, neither overwritten.
- **Journal schema**:
  ```
  Phase 12 — Recommender Offline Eval
  Variant | precision@5 | precision@10 | coverage | cold-start rate | diversity | PDPA ok
  ---|---|---|---|---|---|---
  collaborative | __ | __ | __ | __ | __ | ___
  content-based | __ | __ | __ | __ | __ | ___
  hybrid | __ | __ | __ | __ | __ | ___
  Pathologies: ____
  Decision: Accept hybrid / Re-tune ____ / Fall back to ____ / Redesign
  What would make me re-design: ____
  ```
- **Common failure modes**:
  - Student accepts the hybrid because "hybrid is always best" — the slide deck warns that hybrid has the highest complexity and is not automatically the winner on a 2,000-SKU catalogue. Numbers decide, not defaults.
  - Catalogue coverage not checked — the recommender ships and kills the long tail.
  - Cold-start behaviour not verified against the Phase 10 declaration — the hybrid silently defaults to catalogue popularity, the Sprint 1 segmentation is unused, and the whole product story breaks.
  - Precision@k reported at one value of k only (usually k=1) — the rank-dependence is the point; use k=5 and k=10 both.
  - Scenario-injection state corruption: the recommender plan file is overwritten without a pre-PDPA snapshot. Recovery: re-run the pre-PDPA variant with a `_prepdpa` suffix from the preserved model registry version.
- **Artefact**: `data/recommender_plan_prepdpa.json` + `data/recommender_plan_postpdpa.json` + `journal/phase_12_rec.md` + `journal/phase_12_postpdpa.md`.

---

# Sprint 3 — MLOps: Drift on Segments and Recommender (Phases 13–14)

Same DriftMonitor shape as Week 4 — but the signal is different. No MAPE to watch (no labels). The signals that matter are **segment-assignment stability** (what fraction of customers stay in the same segment week-over-week) and **recommender click-through decay** (is CTR on the new recommender drifting back down toward the old 12% baseline, and if so, why?).

---

## Phase 13 — Drift Triggers

- **Sprints**: Sprint 3 (~15 min).
- **Trust-plane question**: When do we retrain (or roll back)? What are the signals, and who decides?
- **Prompt template**:
  > _"The retail scaffold has already registered the training-window behavioural data as the baseline for the segmentation model and the first-week live click data as the baseline for the recommender. Confirm both references are active. Then run a drift check on each against the most recent week of live data. Show me: for the segmentation, what fraction of customers have moved segments, which segments are growing or shrinking, and are any segments dissolving (approaching the operational-collapse threshold from Phase 7). For the recommender, what is the week-over-week click-through rate, which product categories are losing CTR fastest, and is the cold-start fallback rate creeping up. Based on the results, propose the signals and thresholds I should monitor going forward — how much drift before we retrain? Should that be an automatic trigger or should a human review first? Ground the thresholds in historical variance of these signals, not round numbers. Treat the segmentation drift signal and the recommender drift signal as separate rules, not one combined alarm."_
- **Evaluation checklist**:
  - [ ] Both reference datasets confirmed active (pre-provisioned by the scaffold — the student confirms, does not re-register).
  - [ ] Drift check output surfaces per-signal numbers (segment-assignment stability %, week-over-week CTR, cold-start fallback rate) plus an overall severity per module.
  - [ ] Each proposed signal has a threshold grounded in historical variance, not a guess.
  - [ ] Duration window prevents retrain-on-spike (e.g. "sustained 3 consecutive weeks", not "one bad week").
  - [ ] Retrain decision stays in the Trust Plane — the journal prescribes _signals and thresholds the operator monitors_, not _if X then retrain_ as automatic agent logic. (Post-Black-Friday behaviour is abnormal by design; auto-retrain on that spike would destabilise the segmentation for no reason.)
  - [ ] Segmentation drift signal and recommender drift signal are written as separate rules with separate thresholds — they are different products with different historical variances.
- **Journal schema**:
  ```
  Phase 13 — Retrain Rule
  Signal(s): ____  (separate rule per module)
  Threshold(s): ____ (historical variance grounding: ____)
  Duration window: ____
  Human-in-the-loop: yes / no (justification: ____)
  Re-cluster cadence (segmentation): ____
  Recommender retrain trigger: ____
  ```
- **Common failure modes**:
  - Student tries to re-register the reference data — it is already registered by the scaffold. If the drift check returns "no reference set", ask Claude Code to read the scaffold's drift status endpoint rather than re-seeding.
  - Threshold guessed ("15% feels right") with no variance grounding — 1/4 on reversal condition.
  - Asks Claude Code to "auto-retrain when segment reassignment rate exceeds 20%". The prompt MUST be reframed as "signals and thresholds for operator monitoring". The retrain decision itself stays in the Trust Plane.
  - One combined alarm for both modules — the segmentation is stable on a monthly cadence; the recommender drifts on a daily-to-weekly cadence. One threshold cannot cover both.
- **Artefact**: `data/drift_report.json` + `journal/phase_13_retrain.md`.

---

## Phase 14 — Fairness Audit (DEFERRED TO WEEK 7)

Not run in Week 5. Phase 7 journal entries include a one-line "Fairness audit deferred to Week 7 per Playbook" so the deferral is explicit, not silent. Week 7 (healthcare + credit) is the natural home — protected classes and disparate-impact testing get a full treatment there.

In retail, the fairness questions that will surface in Week 7 include: are small segments over-populated by vulnerable groups (low-income, new-to-Singapore, under-18, first-language-not-English); does the recommender systematically under-recommend certain SKU categories to certain segments; is any observed segment-by-channel interaction a proxy for a protected attribute. Flag these on the Phase 7 red-team with "deferred to Week 7" — do not silently drop them.

- **Sprints**: none in Week 5.
- **Artefact**: deferred.

---

# Optional: The Shopping Advisor (Sprint 3 stretch — only if drift journal is complete)

If Sprint 3's Phase 13 is done, accepted, and journalled with at least 15 minutes of wall-clock left, consider the RAG-powered Shopping Advisor. It does not have its own Playbook phases tonight — treat it as a mini-version of the same 14-phase shape, compressed:

- **Frame (compressed Phase 1)**: five canonical customer questions from `data/arcadia_canonical_questions.md`; what answered "well" looks like (cited product IDs, cited policy snippets, "I don't know" rather than a fabricated answer).
- **Data audit (compressed Phase 2)**: what is in the knowledge base (catalogue, pricing, stock, return policy, FAQ) and what is explicitly out (customer reviews, competitor comparisons, internal memos). Every exclusion has a reason.
- **Metric (compressed Phase 6)**: grounding-rate (fraction of answers that cite a real document) and refusal-rate (fraction of answers that correctly say "I don't know" when the KB cannot support it). There is no label — the metric shape is again a set of signals, not an accuracy number.
- **Red-team (compressed Phase 7)**: does the advisor leak stale prices, recommend out-of-stock items, answer a question it was not asked, or fabricate a policy that does not exist?

Skip the stretch if Sprint 3 is tight. The segmentation + recommender combination is the full credit path.

---

## Week 5 delta (to be appended by Phase 9 at the close of class)

_Your `/codify` output lands here. Three transferable lessons, two domain-specific, as a section below this line. The next week (Media) will read it._
