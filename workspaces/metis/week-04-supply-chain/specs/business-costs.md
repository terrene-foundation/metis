<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

# Business Costs — Workshop Reference

Workshop-local view of the dollar figures used by every prompt template and every rubric-dimension scoring decision. Canonical source is `canonical-values.md` §6; this file exists so prompts and graders can cite a single short reference without scrolling a 240-line spec.

Any change to the numbers here MUST also change `canonical-values.md` §6 in the same commit. See `rules/specs-authority.md` MUST Rule 5.

## Cost terms

| Term                      | Value | Unit                        | Used in (prompt + rubric)                                                               | Canonical reference       |
| ------------------------- | ----- | --------------------------- | --------------------------------------------------------------------------------------- | ------------------------- |
| `stockout_cost_per_unit`  | $40   | per unit short of demand    | Phase 1 framing (D1); Phase 6 metric weight (D2); `journal/_examples.md` D1 anchor      | `canonical-values.md` §6  |
| `overstock_cost_per_unit` | $12   | per unit of excess capacity | Phase 1 framing (D1); Phase 6 metric weight (D2); 3.3:1 ratio vs stockout               | `canonical-values.md` §6  |
| `sla_violation_penalty`   | $220  | per late-delivery violation | Phase 7 Safety red-team (D1, D3); Phase 10 objective term `sla`                         | `canonical-values.md` §6  |
| `driver_overtime_daily`   | $45   | per hour above the base 8-h | Phase 10 objective term `overtime`; `union-cap` scenario (D4 constraint classification) | `canonical-values.md` §6  |
| `fuel_cost_per_km`        | $0.35 | per kilometre               | Phase 10 objective term `fuel`; route-delta calculations in Phase 12                    | `canonical-values.md` §6  |
| `carbon_cost_per_kg_co2`  | $8    | per kg CO2 emitted          | Phase 10 ESG objective; `mas-climate-disclosure` scenario (close block)                 | `canonical-values.md` §6  |
| `lta_carbon_levy_per_km`  | $0.18 | per km (diesel fleet)       | `lta-carbon-levy` scenario injection (Sprint 2 or 3); Phase 10 re-run                   | `canonical-values.md` §11 |

## Ratios and derived numbers

- **Stockout : overstock = $40 : $12 = 3.3 : 1.** Any journal entry scoring 4/4 on D1 cites this ratio in dollar terms; `journal/_examples.md` uses it verbatim.
- **Weekly driver overtime baseline** (~10 drivers × 5 h overtime × $45) = $2,250. The `union-cap` scenario zeros this and shifts the trade-off onto SLA.
- **SLA at fleet scale** ($220 × estimated 10 violations/week on a bad forecast) ≈ $2,200 / week — the hidden-cost number cited in Phase 7 Safety prompts.

## How prompts cite this file

`scripts/grade_product.py` actionable messages reference the table names (`stockout_cost_per_unit`, etc.) directly. Prompt templates under `START_HERE.md` §11 cite the dollar values inline with a "see `specs/business-costs.md`" pointer. Journal rubric rewards any entry that names a cost term from this table AND its value in dollars.

## Non-cost numbers (for reference)

See `canonical-values.md` §6 for the full business-numbers table (daily order volume, depot count, fleet size, historical window, drift event date). Those numbers are NOT cost terms and do not appear above.
