# Week 4 Supply Chain — Specs Index

<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

Specs are the domain-truth authority for the Week 4 "Northwind Logistics Control Tower" workshop. Each file below is the detailed authority on its subject; `START_HERE.md`, `PLAYBOOK.md`, and `SCAFFOLD_MANIFEST.md` at the workspace root are generated views over these specs.

Read this index first; read only the specs relevant to the current work per `specs-authority.md` MUST Rule 4.

## Authoritative / canonical specs (read first when a value is disputed)

| File                  | Domain                 | Description                                                                                                                                                   |
| --------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `canonical-values.md` | Single Source of Truth | Every enum, number, endpoint schema, severity value, rubric anchor, scenario ID, journal field. All other specs **reference** these; do not duplicate values. |
| `wiring-contracts.md` | Tier-2 Wiring Tests    | Per `facade-manager-detection.md` Rules 1–3: named `test_<component>_wiring.py` for all 12 kailash-ml facade components with real-infra external assertions.  |

## Product + methodology specs

| File                           | Domain      | Description                                                                                                                                         |
| ------------------------------ | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `product-northwind.md`         | Product     | Northwind Control Tower: modules, users, business numbers, endpoints, SLOs, deployment topology (endpoint schemas cite §8 of `canonical-values.md`) |
| `playbook-universal.md`        | Methodology | Cross-index for the 14-phase ML Decision Playbook — routes to the three phase-detail specs below                                                    |
| `playbook-phases-sml.md`       | Methodology | Playbook phases 1–9 (Frame → Codify): supervised ML decision loop for Sprint 1 + close block                                                        |
| `playbook-phases-prescribe.md` | Methodology | Playbook phases 10–12: objective + constraints + solver acceptance for Sprint 2                                                                     |
| `playbook-phases-mlops.md`     | Methodology | Playbook phases 13–14: drift triggers (Sprint 3) and fairness (Week 7)                                                                              |

## Build + grading specs

| File                   | Domain         | Description                                                                                                                                   |
| ---------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `scaffold-contract.md` | Build Contract | Pre-built vs student-commissioned vs student-extended enumeration; TODO-STUDENT banners; orphan-detection audit cross-ref to wiring-contracts |
| `rubric-grader.md`     | Grading        | 60% journal rubric + 40% contract grader; `scripts/grade_product.py` behaviour; anchors cite `canonical-values.md` §9                         |

## Operations specs

| File                    | Domain         | Description                                                                                                                                                            |
| ----------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `scenario-catalog.md`   | Instructor Ops | SG-localized scenario catalog (5 events): `union-cap` (MOM Employment Act framing), `drift-week-78`, `lta-carbon-levy`, `hdb-loading-curfew`, `mas-climate-disclosure` |
| `scenario-injection.md` | Instructor Ops | `metis scenario fire <event>` CLI mechanics: exit codes, rollback, idempotency, chat snippets; event IDs cite `scenario-catalog.md`                                    |
| `data-fixtures.md`      | Data           | Synthetic Northwind dataset shape, week-78 drift payload, pre-baked leaderboard, FeatureStore loading (`register_features` + `store`)                                  |
| `viewer-pane.md`        | Frontend       | Next.js read-only dashboard; 5 panels; filesystem-watch polling contract (≤1 s); UX invariants (no student clicks)                                                     |
| `decision-journal.md`   | Journal        | Entry schema (frontmatter + rubric headings), `metis journal add/list/export` CLI, PDF export, run-ID + model-version-ID auto-linkage                                  |
| `workshop-runofshow.md` | Instructor Run | Minute-by-minute 210-min script (10 + 75 + 10 + 60 + 40 + 15): blocks, injections, checkpoints, mitigations                                                            |

## Known compliance items (documented, not blocking workshop)

- `product-northwind.md` is 374 lines (specs-authority Rule 8 MUST-split threshold is 300). The file's density is dominated by endpoint contracts, most of which now reference `canonical-values.md` §8. Remaining work: extract the operational topology section into `product-northwind-ops.md`, leaving API contract summary in this file. Deferred to next post-workshop pass.
