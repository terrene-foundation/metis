<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Arcadia Retail Intelligence Suite — Product Brief

Workshop product: a customer-intelligence **Retail Suite** for Arcadia Retail — one product with three layered modules. By the end of the 210-minute workshop you will have shipped a Customer Segmentation Engine and a Hybrid Recommender (and, if Sprint 3 has spare budget, a RAG-powered Shopping Advisor) against a pre-provisioned retail backend, and defended a page of written decisions that explain why you shipped them that way.

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

## 4. The product story — one product, three layered modules

This is a single product with a clear cascade. Each module depends on the one above it. If you get the top wrong, every module below it silently inherits the error.

1. **Segmentation is the foundation.** Every customer gets a segment label — their behavioural class. The segment is the common currency every other module speaks in.
2. **The recommender uses the segment label as its cold-start bootstrap.** A brand-new customer has no purchase history; the recommender falls back on the modal basket of that customer's nearest segment until their own behaviour accumulates. A better segmentation produces a better cold-start; a worse segmentation produces junk recommendations for every new customer.
3. **The Shopping Advisor (if reached) grounds its retrieval in segment-aware ranking.** The same question — "show me jackets under $180" — surfaces different products to a "weekend-bargain-hunter" segment customer than to a "weekday-luxury-buyer" segment customer. The Advisor reads the segment label; it does not re-compute it.

Cascade: segment count and quality drives recommender cold-start quality drives Advisor relevance. One product, three layers, one chain of decisions.

## 4a. The three modules on the table tonight

### 4.1 Customer Segmentation Engine (Sprint 1, required — the foundation)

**What it is.** An unsupervised learning system that groups Arcadia's 50,000 customers into 4–7 behavioural segments — not demographic buckets, but patterns in _what they actually do_ ("high-frequency weekend browser, converts on promo", "premium one-visit-per-quarter", "lapsed e-com, dormant store").

**Why it exists.** The CMO cannot run 50,000 one-to-one campaigns. She can run six. The segmentation engine turns raw customer records into a small, stable set of segments the marketing team can build campaigns around.

**Who signs off.** CMO (segment definitions + campaign map) and CX Lead (segments must be usable on the product pages).

**Success at 3:30 pm.** A segment map exists on disk with a segment ID per customer, every segment has a one-paragraph business profile, the segment count is defended in a journal entry, and the campaign-cost-at-risk has been quantified using the table above.

### 4.2 Hybrid Recommender (Sprint 2, required — uses the segmentation for cold-start)

**What it is.** A system that, given a customer and a product page (or a cart), returns a ranked list of recommended SKUs. It blends three signals: what other similar customers bought (collaborative), what products are similar to the one being viewed (content-based), and — for customers with no purchase history — the modal basket of the segment they were assigned to in Sprint 1 (cold-start bootstrap). This is how the segmentation gets used: it is the answer to "what do we recommend to someone we know nothing about yet?"

**Why it exists.** The current rule-based recommender converts at 12%. Industry benchmarks for a hybrid recommender on a catalogue this size sit at 18–24%. Each converted click is worth $18. Each wasted impression costs $14. The CX Lead wants to know which recommender strategy — collaborative, content-based, or hybrid — wins on Arcadia's specific data, and what the cold-start behaviour should be for new customers.

**Who signs off.** CX Lead (strategy + uplift) and CMO (does the rec respect the segment strategy).

**Success at 3:30 pm.** A chosen recommender strategy is running behind the pre-wired recommender endpoint; the decision (collaborative vs content-based vs hybrid) is defended in a journal entry tied to the $18 / $14 asymmetry; cold-start disposition is an explicit product decision (fall back to segment modal basket, fall back to catalogue popularity, or fall back to editorial curation); the PDPA hard line is documented in the constraint table.

### 4.3 Shopping Advisor (optional stretch — segment-aware retrieval)

**What it is.** A RAG-powered conversational assistant sitting on the catalogue, pricing, stock, and return-policy documents. A customer types "I'm looking for a waterproof jacket under $180 that ships tomorrow" — the assistant retrieves relevant product records, policy snippets, and stock levels, then answers in natural language, grounded in real data. The Advisor reads the customer's segment label (from Sprint 1) and uses it to re-rank retrieval: the same query produces different top results for a bargain-hunter than for a luxury-buyer.

**Why it exists.** The CX Lead thinks 25% of shopping conversations a year from now will be with an AI assistant. She wants a working proof-of-concept that can answer five canonical customer questions honestly, with citations — and that visibly personalises by segment without crossing the PDPA line.

**Who signs off.** CX Lead (useful answers, visible segment-aware personalisation) and E-com Ops Lead (no data leak, no made-up prices).

**Success at 3:30 pm (if reached).** The advisor answers the five canonical questions from `data/arcadia_canonical_questions.md` with cited product IDs and policy snippets; a journal entry names what is in / out of the knowledge base plus why; a journal entry names the grounding-failure fallback (does it say "I don't know", fall back to catalogue popularity, or escalate to a human) — this is a product decision, not a default.

Note for tonight's workshop: Sprint 3 is primarily the **Monitor** sprint (drift on segments + recommender click-through). The Shopping Advisor is a stretch goal. Do not start it until Sprint 3's Phase 13 journal entry is written and accepted.

## 5. The five Trust Plane decision moments

Tonight collapses into five moments where the decision has teeth. Every other phase produces artefacts; these five are where you can silently ship a weak product if you are not paying attention. They are the rubric's highest-pressure points.

1. **Pick K and defend in dollars** (Phase 6). Not "silhouette said 5". Rather: "5 because marketing can run 5 parallel campaigns; 7 would cost $X in setup with no realistic chance of lift." Stability and actionability have floors, not just targets.
2. **Name each segment and declare a differentiated action per segment** (Phase 5 + 6). If two segments get the same action, they are one segment with noise between them. Collapse them, or defend the difference in dollars.
3. **Choose the recommender strategy with an explicit cold-start disposition** (Phase 10 + 12). Collaborative, content-based, or hybrid — and for new customers with no history, say what happens: segment modal basket, catalogue popularity, or editorial curation. "Default fallback" is not an answer.
4. **Declare what goes into the RAG corpus and what stays out** (Advisor stretch, Phase 11 analogue). PDPA, legal exposure, data staleness — every exclusion has a reason.
5. **Set the grounding-failure fallback** (Advisor stretch). When the knowledge base cannot support an answer, does the Advisor say "I don't know", fall back to the popular item, or escalate to a human? This is a product decision.

If you ship tonight with any of the first three unjudged, the rubric will catch it. Decision moments 4 and 5 only apply if you reach the Advisor stretch in Sprint 3.

## 6. 3:30 pm success definition

By the close of the workshop (15:30 wall-clock), a passing run looks like this. Every item is grader-verifiable or rubric-verifiable.

- [ ] All four required product endpoints answer the contract grader with real data (not `{"status":"ok"}` stubs): segmentation train, segmentation profile, recommender train, recommender predict. (Endpoint paths are the scaffold's; you do not wire them.)
- [ ] At least 10 journal entries exist at `journal/phase_<N>_<slug>.md`. Each one names its signal, threshold, and duration window under `## Reversal condition` — never the phrase "if data changes".
- [ ] The `pdpa-under-18` scenario injection at roughly 02:05 produced both `journal/phase_11_constraints.md` and `journal/phase_11_postpdpa.md`; the re-run classifies the under-18 browsing-history feature as a **hard** exclusion with the $220/record exposure cited.
- [ ] The `segment-drift` (or recommender CTR decay) scenario at roughly 02:40 produced a Phase 13 journal entry that names a signal (segment-assignment stability on the top-3 segments, or 7-day click-through-rate decay), a numeric threshold grounded in the training-window variance, and a duration window (e.g. "sustained for 3 consecutive days").
- [ ] `metis journal export --output journal.pdf` renders without silent degradation.

Combined score target: ≥ 0.60 (60% journal rubric mean + 40% contract grader).

## 7. What is different from Week 4 (read this if you took Week 4)

- **No scaffold work, but the COC routine still runs.** The backend, data generator, baseline K=3 clustering run, baseline content-based recommender, and drift monitor with reference data registered are all pre-provisioned at `src/retail/` and `apps/web/retail/`. Your first prompt confirms preflight is green, then you enter `/analyze` — which inventories what the baseline commits to and what decisions are still yours — followed by `/todos` (draft the 14 Playbook phases; instructor gate), then `/implement` (the three Playbook-driven sprints), then `/redteam`, then `/codify`. The Playbook phases are the CONTENT of `/implement`, not a replacement for the routine.
- **No label, no "accuracy".** Sprint 1 is unsupervised. There is no ground-truth segment column. The metric conversation in Phase 6 changes shape — silhouette floor + stability floor + business-actionability floor replace RMSE and MAPE. See the Playbook for the rewrite.
- **Phase 3 is unfolded this week.** Week 4 folded Feature Framing into Data Audit. Week 5 unfolds it: pre-cluster feature selection has higher stakes than pre-model feature selection (an ethically loaded feature does not just bias a model, it _creates_ a segment that is really a proxy for a protected class). Phase 3 gets its own 10-minute pass and its own journal entry.
- **PDPA is the new union cap.** Week 4's mid-sprint legal shock was a MOM overtime circular. This week it is a PDPA notice about under-18 browsing data. Same rubric pressure — hard/soft constraint classification — different regulatory surface.
- **Recommender strategy is the new route-plan decision.** Collaborative vs content-based vs hybrid is the "which solver" call. Phase 12 acceptance applies in the same shape: feasibility (respects PDPA, respects inventory), optimality (precision@k, coverage, cold-start rate beat the 12% rule-based benchmark), pathology (does it keep recommending the same five hero SKUs to everyone?).

## 8. Where to go next

- `START_HERE.md` — student manual with the opening prompt and the Phase 1 entrypoint.
- `PLAYBOOK.md` — the 14-phase procedure, adapted for unsupervised + recommender.
- `src/retail/data/arcadia_*.csv` — the retail datasets (customers, products, transactions).
- `src/retail/data/segment_baseline.json` + `segment_candidates.json` — pre-built K=3 baseline + pre-baked K-sweep reference.
- `src/retail/data/drift_baseline.json` — registered drift reference distribution.
- `src/retail/data/scenarios/` — mid-session injection payloads (`pdpa_redline.json`, `catalog_drift.json`).
