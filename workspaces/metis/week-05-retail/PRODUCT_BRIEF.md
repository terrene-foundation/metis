<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Arcadia Retail Intelligence Suite — Product Brief

Workshop product: the **Arcadia Retail Intelligence Suite** — one product assembled as the traditional ML value chain (USML → SML → Optimization → MLOps). By the end of the 210-minute workshop you will have shipped a Customer Segmentation engine (USML), churn + conversion classifiers (SML), a campaign allocator (Optimization) and drift monitors for all three (MLOps), against a pre-provisioned retail backend, and defended a page of written decisions that explain why you shipped them that way.

Read this before writing your first prompt. Every dollar figure here is cited by the rubric and the contract grader; making them up in a journal entry scores zero.

Unlike Week 4, tonight **skips the build phase entirely**. The retail backend (at `src/retail/backend/`), viewer (at `apps/web/retail/`), datasets (at `src/retail/data/`), baseline K=3 clustering model, baseline content-based recommender, and the drift monitor with reference data already registered are all pre-provisioned and running on your laptop before class starts. You walk in, paste one opening prompt, confirm preflight is green, and spend every minute of your 3.5 hours on the **full COC routine** — `/analyze`, `/todos`, `/implement`, `/redteam`, `/codify` — with the 14-phase ML Decision Playbook as the content of `/implement`. You do not scaffold, wire endpoints, or install libraries; you DO still run the routine you know, because that is the institutional muscle memory the course is building. Your job tonight is pure wielding: apply the Playbook to **unsupervised** segmentation (Sprint 1), **recommender strategy** (Sprint 2), and **drift monitoring** (Sprint 3).

## 1. Business context

Arcadia Retail is a Singapore omnichannel retailer. Five physical stores (three in the city, one in the east, one in Jurong) plus an e-commerce site live at `shop.arcadia.sg`. Roughly 50,000 customers, 2,000 SKUs across fashion, home, and beauty, and about 500,000 transactions per year. Two years of transaction and behavioural data sit in `src/retail/data/arcadia_customers.csv`, `src/retail/data/arcadia_transactions.csv`, and `src/retail/data/arcadia_products.csv`.

The CMO has been running the same five marketing campaigns for six years — "active members", "lapsed members", "high-value", "e-com only", "store only" — with the same segmentation rules the previous agency handed over in 2020. Conversion has been flat for three quarters. The CX Lead wants a recommender on the product detail pages and in the cart. The E-com Ops lead wants to know when either system starts lying. They are asking whether data-driven customer intelligence can replace hand-authored rules, lift revenue, and tell them when to stop trusting the models.

Your job during the workshop is to commission Claude Code to train and evaluate these systems, make the calls the tool cannot make for you, and write the journal that proves you made them.

Two planes run in parallel: the **Trust Plane** is where you decide (how many segments, which recommender strategy, how much personalisation is too much); the **Execution Plane** is Claude Code, the pre-provisioned backend, and the retail datasets. If a question is _what_ or _how_, route it to the Execution Plane. If it is _which_, _whether_, _who wins_, or _is it good enough to ship_, it stays with you.

## 2. Cost table (ground truth — use these exact numbers)

These numbers come from Arcadia's finance pack. Every journal entry that names dollar impact must cite from this table. The "good recommendation" economics are driven by the **$18 average-basket-lift** and the **$14 wasted-impression** ceiling, and the cross-campaign economics by the **$45 wrong-segment-campaign-cost** vs **$3 per-customer-touch-cost**.

| Cost term                                           | Value                             | Unit                                     | Where it shows up                          |
| --------------------------------------------------- | --------------------------------- | ---------------------------------------- | ------------------------------------------ |
| Average basket lift from a converted recommendation | $18                               | per converted click                      | Phase 6 (rec metric); Phase 10 (objective) |
| Wasted impression (shown, not clicked)              | $14                               | per session of irrelevant recs           | Phase 6; Phase 7 Safety                    |
| Wrong-segment campaign cost                         | $45                               | per customer sent to the wrong offer     | Phase 6 (segment metric); Phase 7 Safety   |
| Per-customer touch cost                             | $3                                | per marketing contact (email/push/SMS)   | Phase 11 (soft cost of touch budget)       |
| PDPA breach exposure                                | $220                              | per under-18 personalised-history record | Phase 7 Safety; Phase 11 (hard constraint) |
| Cold-start fallback cost                            | $8                                | per new-user session with no rec signal  | Phase 11 (soft constraint)                 |
| Peak season                                         | Nov–Dec (Black Friday / Year-End) | seasonal window                          | Phase 1 framing; Phase 13 drift context    |

Supporting business volumes (for Phase 1 framing):

- 50,000 customers on record; ~18,000 active in the last 90 days.
- 2,000 SKUs; roughly 1,200 are in stock at any time; 40 SKUs rotate weekly.
- 500,000 transactions per year; 60% e-com, 40% in-store with loyalty-card match.
- 8,000 product-page views per day on the e-com site; 12% click-through on recommender slots in the current (rule-based) system — the target the new system must beat to justify shipping.

## 3. Personas (who you are serving)

You play the Student role and commission the Execution Plane on behalf of the three Trust Plane personas below.

| Persona        | Plane           | What they do                                                                         | What they read                           |
| -------------- | --------------- | ------------------------------------------------------------------------------------ | ---------------------------------------- |
| CMO            | Trust Plane     | Approves the segmentation; signs off on the campaign map; owns the segment strategy  | Segment dashboard, segment profile cards |
| CX Lead        | Trust Plane     | Approves the recommender strategy; decides what "good" looks like on product pages   | Recommender leaderboard, uplift charts   |
| E-com Ops Lead | Trust Plane     | Tracks live performance; owns the decision to retrain or roll back                   | Drift chart, segment-stability chart     |
| ML Engineer    | Execution Plane | Ships training pipeline, registry, drift monitor (= Claude Code during the workshop) | Logs, run tracker, model registry        |
| Student (you)  | Trust Plane     | Commissions every piece; graded on journal + contract grader                         | Viewer Pane, terminal, `PLAYBOOK.md`     |

## 4. The product story — one product, four layered modules (the ML value chain)

This is a single product built as the traditional ML value chain: **discover → predict → decide → monitor**. Each module consumes the one above it. Skip a link and the chain breaks at your weakest stakeholder.

1. **Segmentation is the foundation (USML · Sprint 1).** Every customer gets a segment label — their behavioural class. The segment is the common currency every later module speaks in.
2. **The classifiers predict behaviour (SML · Sprint 2).** Two supervised models use the segment label as a feature. _Churn_ answers "will this customer stop buying in the next 30 days?"; _Conversion_ answers "will this customer convert on a category-level offer?". The churn model drives retention; the conversion model feeds the allocator.
3. **The allocator decides where money goes (Optimization · Sprint 3).** A linear-programming solver takes segments × predicted conversion probabilities × touch budget × PDPA/inventory constraints and returns a campaign plan that maximises expected revenue under the constraints. This is where ML becomes a business decision.
4. **The drift monitor watches for lies (MLOps · Sprint 4).** Three rules, one per artefact, because the three models drift on different signals at different cadences. Without Sprint 4 you never learn that Sprint 1/2/3 have silently rotted.

Cascade: segment quality → predicted-response quality → allocator decisions → monitoring coverage. One product, four layers, one chain of decisions.

## 4a. The four modules on the table tonight

### 4.1 Customer Segmentation Engine (Sprint 1 · USML · Discover)

**What it is.** An unsupervised learning system that groups Arcadia's customers into 3–7 behavioural segments — not demographic buckets, but patterns in _what they actually do_ ("high-frequency weekend browser, converts on promo", "premium one-visit-per-quarter", "lapsed e-com, dormant store"). Scaffold sample: 5,000 customers clustered on 7 behavioural features.

**Why it exists.** The CMO cannot run 50,000 one-to-one campaigns. She can run six. The segmentation engine turns raw customer records into a small, stable set of segments the marketing team can build campaigns around.

**Who signs off.** CMO (segment definitions + campaign map) and CX Lead (segments must be usable on product pages).

**Success at 5:30 pm.** A chosen K is promoted from staging to shadow in the segment registry. Every segment has a one-paragraph business profile and a differentiated marketing action. K is defended in the Phase 6 journal tied to the three floors (separation, stability, actionability) AND the counterfactual dollar lift vs the 2020 rulebook.

### 4.2 Response Predictors: Churn + Conversion (Sprint 2 · SML · Predict)

**What it is.** Two supervised classifiers trained on the segment-labelled customers. Same 3-family leaderboard each time (logistic regression + random forest + gradient-boosted ensemble — the king for tabular data). _Churn_: P(customer has not visited in 30+ days | features). _Conversion_: P((customer, category) produces a transaction | features + category one-hot). The scaffold trains them at startup; `/predict/leaderboard/{churn,conversion}` exposes the numbers.

**Why it exists.** The CX Lead wants to know who to reach out to (churn) and what to recommend (conversion). Both are binary SML problems with clean cost asymmetries. Churn CAC is $120 to reacquire vs $3 touch cost (40:1). Conversion feeds Sprint 3: you can't allocate campaign budget without knowing per-segment-per-category response probabilities.

**Who signs off.** CX Lead (chosen family + threshold per classifier) and CMO (threshold must respect marketing's capacity ceiling).

**Success at 5:30 pm.** Both classifiers have a chosen family on the leaderboard, a cost-based threshold on the PR curve with dollar justification (Phase 6 SML lens), calibration confirmed (Brier score), promotion to shadow in the predictor registry (Phase 8). 5 SML journal entries per classifier (Candidates → Implications → Metric+Threshold → Red-team → Gate, each with `_sml` suffix).

### 4.3 Campaign Allocator (Sprint 3 · Optimization · Decide)

**What it is.** A linear-programming solver that decides, for each (segment, campaign) pair, how many customers to touch. Maximises expected revenue = Σ x × (P(convert) × revenue_per_convert − cost_per_touch). Respects hard constraints (touch budget cap, PDPA exclusions, inventory) and soft constraints with dollar penalties (per-segment fatigue cap). The scaffold exposes `/allocate/objective`, `/allocate/constraints`, `/allocate/solve`, `/allocate/last_plan`.

**Why it exists.** The CMO has a fixed quarterly budget. The CX Lead knows which classifier says who will convert. Neither knows how to allocate optimally across five campaigns × three+ segments under a touch budget and PDPA hard-lines. Optimization is where ML becomes a business decision under constraints.

**Who signs off.** CMO + E-com Ops Lead (co-ownership: CMO owns the objective weights, Ops owns the constraint set).

**Mid-sprint injection (~4:30pm).** Legal flags under-18 browsing-history use as a PDPA §13 hard exclusion. The allocator re-runs with the new hard constraint, the expected revenue drops (the shadow price of compliance becomes visible in dollars), and students re-journal Phase 11 + 12 as `_postpdpa.md`.

**Success at 5:30 pm.** `/allocate/solve` produces a feasible, non-pathological plan; objective weights + constraint classifications are defended in Phase 10–12 journals; post-PDPA re-run saved as `phase_11_postpdpa.md` AND `phase_12_postpdpa.md` (skipping the Phase 12 re-run is the single most common D3 failure).

### 4.4 Drift Monitor × 3 models (Sprint 4 · MLOps · Monitor)

**What it is.** Three separate drift rules, one per artefact, because the three models drift on different signals at different cadences. Segmentation drifts on **membership churn** (monthly). Churn/conversion classifiers drift on **calibration decay + feature PSI** (weekly). Allocator drifts on **constraint-violation rate + feasibility rate** (daily). The scaffold's `/drift/check` accepts a window name and returns per-feature PSI + segment-membership churn + overall severity.

**Why it exists.** Without Sprint 4, a student ships a "working" product that silently rots over the next quarter. The Ops Lead needs three drift rules — one per model — with variance-grounded thresholds, duration windows, and human-in-the-loop on first trigger. The Phase 13 journal captures all three in one entry.

**Who signs off.** E-com Ops Lead (monitoring + retrain rules), CMO (re-training approval under HITL first trigger).

**Success at 5:30 pm.** `/drift/retrain_rule` has been called for each of the three models with defensible thresholds. Each rule names: signal, threshold, duration window, HITL disposition, seasonal exclusions. The Phase 13 journal entry covers all three.

## 5. The five Trust Plane decision moments

Tonight collapses into five moments where the decision has teeth. Every other phase produces artefacts; these five are where you can silently ship a weak product if you are not paying attention. They are the rubric's highest-pressure points.

1. **Pick the primary operating point and defend it in the declared unit of harm** (Phase 6). _Retail tonight_: pick K for segmentation and defend in $ of wrong-campaign cost + marketing capacity. Not "silhouette said 5" — "5 because marketing can run 5 campaigns; 7 costs $X in setup; stability drops below 0.80 at K=7".
2. **Commit to a distinct downstream action per output class** (Phase 5 + 6). _Retail tonight_: if two segments get the same marketing campaign, they are one segment with noise. Collapse or defend in dollars.
3. **Choose the SML classifier's family and threshold with cost-based justification** (Phase 4→6 SML replay). Ensemble is the king for tabular data, but you still read the PR curve and pick the threshold that minimises expected cost against the CAC vs touch asymmetry (churn 40:1). For both classifiers, not just one.
4. **Classify hard-vs-soft constraints under regulatory pressure** (Phase 11 + re-run). _Retail tonight_: when PDPA fires at 4:30, re-classify under-18 browsing as a hard line AND re-solve the LP. Not just the journal entry.
5. **Set retrain rules × 3 models, grounded in historical variance** (Phase 13). Three rules, three cadences, three signals. No universal "auto-retrain when X" — signal + threshold + duration window + HITL.

All five are non-negotiable tonight.

## 6. 5:30 pm success definition

By the close of the workshop, a passing run looks like this. Every item is grader-verifiable or rubric-verifiable.

- [ ] **All four modules' endpoints return real data** (no `{"status":"ok"}` stubs): `/segment/baseline` + `/segment/registry` (shadow/production set), `/predict/leaderboard/{churn,conversion}` with chosen thresholds via `/predict/threshold`, `/allocate/solve` produces a feasible plan at `/allocate/last_plan`, `/drift/check` ran against both `recent_30d` and `catalog_drift` windows, `/drift/retrain_rule` called for all three model IDs.
- [ ] **At least 14 journal entries** at `journal/phase_N_{usml,sml,...}.md`. Each one names its signal, threshold, and duration under `## Reversal condition` — never the phrase "if data changes".
- [ ] **PDPA injection produces four files, not two**: `journal/phase_11_constraints.md`, `journal/phase_11_postpdpa.md`, `journal/phase_12_accept.md`, `journal/phase_12_postpdpa.md`. The PDPA re-run hits the ALLOCATOR, not a recommender. The compliance cost (expected revenue delta) is quantified in `phase_12_postpdpa.md`.
- [ ] **Phase 13 journal has three rules**, one per model (segmentation / churn / allocator), each with signal + variance-grounded threshold + duration window + HITL disposition + seasonal exclusions.
- [ ] **The value-chain banner on the viewer shows all four sprints green** at close, and the five decision moments all ticked.

Combined score target: ≥ 0.60 (60% journal rubric mean + 40% endpoint-contract grader).

## 7. What is different from Week 4 (read this if you took Week 4)

- **No scaffold work, but the COC routine still runs.** The backend, data generator, baseline K=3 clustering, churn + conversion classifiers pre-trained at startup, and drift reference registered are all pre-provisioned at `src/retail/` and `apps/web/retail/`. Your first prompt confirms preflight is green, then you enter `/analyze` — inventorying what the baseline commits to and what decisions are still yours — followed by `/todos` (draft the Playbook phases; instructor gate), then `/implement` (four paradigm sprints USML→SML→Opt→MLOps), `/redteam`, `/codify`. The Playbook phases are the CONTENT of `/implement`, not a replacement for the routine.
- **Four paradigms, one night.** Week 4 was SML (forecasting) + Optimization (routing). Week 5 is the whole value chain in one product: USML (segmentation) + SML (churn + conversion classifiers) + Optimization (campaign allocator) + MLOps (drift on all three). Students take the Playbook into their next project with all four paradigms practised.
- **No label in Sprint 1.** Segmentation is unsupervised — no ground-truth segment column, no MAPE, no AUC. Phase 6 USML changes shape: silhouette floor + stability floor + business-actionability floor, all pre-registered BEFORE seeing the Phase 4 leaderboard.
- **Phase 3 is unfolded this week.** Week 4 folded Feature Framing into Data Audit. Week 5 unfolds it because pre-cluster feature selection has higher stakes — an ethically loaded feature does not just bias a model, it _creates_ a segment that is really a proxy for a protected class.
- **PDPA is the new union cap** — Week 4's MOM overtime circular → Week 5's PDPA under-18 browsing. Same rubric pressure (hard/soft constraint classification), different regulatory surface. Fires mid-Sprint-3 at 4:30 against the ALLOCATOR (re-run Phase 11 + 12).
- **The campaign allocator is the new route plan** — Week 4 optimised delivery routes under vehicle/driver constraints. Week 5 optimises campaign allocation under touch budget + PDPA + inventory constraints. Phase 12 asks the same questions: feasibility, optimality gap, pathologies (concentration? dead campaigns?), accept / re-tune / fall back / redesign.

## 8. Where to go next

- `START_HERE.md` — student manual with the opening prompt, the COC-wrapped clock, and the four-sprint flow.
- `PLAYBOOK.md` — the universal 14-phase procedure with teaching blocks (SML lens + USML lens + Optimization lens + Your levers + Transfer to next project) per phase.
- `SCAFFOLD_MANIFEST.md` — every pre-built file, who writes it, who reads it.
- `src/retail/data/arcadia_*.csv` — the retail datasets (customers, products, transactions).
- `src/retail/data/segment_baseline.json` + `segment_candidates.json` — pre-built K=3 baseline + pre-baked K-sweep reference.
- `src/retail/data/drift_baseline.json` — registered drift reference distribution.
- `src/retail/data/scenarios/` — mid-session injection payloads (`pdpa_redline.json`, `catalog_drift.json`).
- `journal/skeletons/` — fill-in-the-blank per-phase templates; copy into `journal/phase_N_*.md` at the start of each phase.
