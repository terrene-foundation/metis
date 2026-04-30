<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 2 — Data Audit

> **What this phase does:** Read the labelled moderation dataset before any model trains, surfacing the six categories of trouble that wreck deep-learning supervised pipelines: label quality, leakage, survivorship, distribution shift, missingness, proxy variables.
> **Why it exists:** Models look perfect on holdouts that share the training distribution's flaws. The audit is the only place those flaws become visible before they become production incidents.
> **You're here because:** Phase 1 framed the problem; Phase 2 reads the data.
> **Key concepts you'll see:** label-quality audit, temporal leakage, survivorship bias, demographic skew, multi-modal label-quality

---

## 1. Paste this into Claude Code

**Universal core:**

```
I'm in Playbook Phase 2 — Data Audit. The model trains on labelled
moderation data; the labels were produced by human reviewers under time
pressure. I need a six-category audit BEFORE training:

1. Label quality — what's the inter-reviewer agreement on a sample?
   Where do reviewers disagree most?
2. Temporal leakage — are any features in the training window not yet
   knowable at the time of moderation? (e.g. user_lifetime_reports — if
   the post is what triggers a future report, the feature is leaky)
3. Survivorship bias — what posts are MISSING from the dataset?
   (Posts auto-removed by the rule system never made it to human review,
   so the labels skew toward posts the rule system thought ambiguous.)
4. Distribution shift — does the labelled set look like the live stream?
5. Missingness pattern — what fraction of posts have missing image, text,
   or both? Are missingness patterns correlated with label?
6. Proxy variables — does any feature proxy a protected class
   (account_country → ethnicity proxy; account_age → demographic proxy)?

For each category, name 2–3 specific findings with row counts. Cite the
file. If you cannot cite a file, say "I have not read this — confirming
required."

Do NOT propose remediations beyond "drop", "log", or "investigate".
Remediation is my call.
Do NOT use "blocker" without a named next step.

When the journal file has all six categories with findings, stop.
```

**Tonight-specific additions** (Week 6 MosaicHub):

```
Source dataset: src/media/data/posts_labelled.csv (80k labelled posts).
Image files: src/media/data/images/ (24k image files).

Label-quality specifics:
- Inter-reviewer agreement on the 5k double-labelled subset (column:
  reviewer_2_label). Compute Cohen's kappa per class. Hate-speech and
  CSAM-adjacent classes typically have lowest agreement.
- Worst-agreement class is your highest-risk Phase 6 threshold target.

Temporal leakage specifics:
- user_account_age_days, user_lifetime_reports, user_followers_at_time:
  confirm each is computed at POST TIME, not at LABEL TIME (could differ
  by hours).
- post_engagement_at_label_time: this IS leaky for moderation —
  engagement at label time is influenced by the moderator's decision.

Survivorship specifics:
- Posts auto-removed by rule keywords never reached human review. The
  labelled set is biased toward posts the rule system was UNCERTAIN about.
  Quantify the gap: estimate how many posts/day the rule system removed
  pre-labelling vs how many made the labelled set.

Distribution shift specifics:
- 5 SEA markets — Singlish, Malay, Bahasa Indonesia, Tagalog, Thai
  text mix. What's the language distribution in the labelled set vs the
  scaffold's representation of live traffic?
- Election cycle indicator: are any labelled posts from election-window
  weeks? If so, those weeks should be flagged for the Phase 13 seasonal
  exclusion.

Missingness:
- text-only posts (no image): what fraction? Their label distribution
  must NOT be conflated with image+text posts.
- image-only posts (no caption): what fraction? Same caveat.

Proxy variables:
- account_country: proxy for ethnicity. Do not include in image moderator
  features without explicit Phase 7 demographic-skew check.
- post_time_of_day: proxy for time zone, could correlate with country.

Journal file: copy journal/skeletons/phase_2_data_audit.md into
workspaces/metis/week-06-media/journal/phase_2_data_audit.md.
```

**How to paste:** Combine both blocks.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ `journal/phase_2_data_audit.md` has all 6 categories with 2–3 findings each
- ✓ Each finding has a row count or a specific file/column reference
- ✓ Inter-reviewer kappa computed per class (or marked as "needs run")
- ✓ Survivorship gap quantified (rule-removed pre-label vs labelled count)
- ✓ Language distribution surfaced for the 5 SEA markets
- ✓ Stop signal pending review

**Signals of drift — push back if you see:**

- ✗ A finding with no row count or file citation — ask "which file? how many rows?"
- ✗ Recommendations beyond drop/log/investigate — ask "remediation is my call"
- ✗ Survivorship described as "minor" without quantification
- ✗ Proxy variables waved away as "OK" — ask for specific Phase 7 sweep
- ✗ Missing language/market split — ask "we span 5 SEA markets, what's the distribution?"

---

## 3. Things you might not understand in this phase

- **Inter-reviewer agreement (Cohen's kappa)** — does the label even mean the same thing across reviewers?
- **Temporal leakage** — features that aren't yet knowable at decision time
- **Survivorship bias** — labels you have are biased toward posts the rule system couldn't decide
- **Demographic skew in moderation labels** — reviewers' implicit biases bake into the labels
- **Multi-modal label-quality** — is the label about the image, the text, or the joint? They differ for memes.

---

## 4. Quick reference (30 sec, generic)

### Inter-reviewer agreement (Cohen's kappa)

A measure of how often two human reviewers agree on a label, corrected for chance. κ < 0.4 = poor agreement; κ > 0.7 = strong. Hate-speech and CSAM-adjacent classes typically have lower kappa than NSFW or weapons. The class with the worst kappa is your highest Phase 6 threshold risk — labels are noisier, so the model's PR curve is less reliable.

> **Deeper treatment:** [appendix/02-data/data-audit.md](./appendix/02-data/data-audit.md)

### Temporal leakage

A feature available at training time but NOT at decision time. Tonight: `post_engagement_at_label_time` is leaky because engagement-at-label is influenced by the moderator's prior action. `user_lifetime_reports` may or may not be leaky depending on whether reports are pre-post or post-post. The check: would this feature value be available the millisecond the post is uploaded? If no, leaky.

> **Deeper treatment:** [appendix/02-data/leakage.md](./appendix/02-data/leakage.md)

### Survivorship bias

The labels you have describe posts that survived the rule-system filter. Posts the rules auto-removed never reached human reviewers, so they don't appear in the training set. The labelled distribution is biased toward "posts the rule system was uncertain about." Models trained on this bias will struggle on posts the rule system would have caught.

> **Deeper treatment:** [appendix/02-data/data-audit.md](./appendix/02-data/data-audit.md)

### Demographic skew in moderation labels

Reviewers carry implicit biases. The same hate-speech post may be labelled differently by reviewers from different cultures. Tonight's data spans 5 SEA markets; reviewer pool composition matters. Skew shows up as: per-class kappa varies by reviewer-demographic, certain language-mixes get over-flagged, etc. Phase 7 demographic-skew sweep checks this.

> **Deeper treatment:** [appendix/02-data/proxy-for-protected-class.md](./appendix/02-data/proxy-for-protected-class.md)

### Multi-modal label-quality

For memes (image + text), the label is about the joint meaning. Reviewers may disagree on which modality drove the label. The 8k multi-modal subset has its own kappa, often lower than per-modality. Phase 5 multi-modal must defend the architecture against this disagreement floor.

> **Deeper treatment:** [appendix/02-data/data-audit.md](./appendix/02-data/data-audit.md)

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 6 Phase 2.

Read `workspaces/metis/week-06-media/playbook/phase-02-data-audit.md` and
`workspaces/metis/week-06-media/journal/phase_2_data_audit.md`.

Explain "<<< FILL IN: concept name >>>" — plain language, MosaicHub-grounded,
implications for my Phase 2 decision, what to push back on. Under 400 words.
```

---

## 6. Gate / next

- [ ] All 6 audit categories covered with 2–3 findings each
- [ ] Each finding has a row count + file/column reference
- [ ] Cohen's kappa computed per class
- [ ] Survivorship gap quantified
- [ ] Language distribution across 5 SEA markets surfaced
- [ ] Proxy variables flagged with Phase 7 follow-ups

**Next file:** [`phase-03-features.md`](./phase-03-features.md)
