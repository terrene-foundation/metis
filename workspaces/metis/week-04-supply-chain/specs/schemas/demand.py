# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
#
# Schema authority: specs/data-fixtures.md §1.2 (the 13-column northwind_demand.csv
# layout) and specs/canonical-values.md §8.7 (candidate_families fully-qualified
# identifiers). Field names match the CSV header verbatim; a change here requires
# a coordinated change to both specs and to data/_generate.py (see
# rules/specs-authority.md MUST Rule 5).
"""FeatureSchema for the Northwind daily-demand forecasting target.

Imported by `src/backend/startup.py::preload_feature_store` and by the student's
Phase 4 AutoMLEngine prompt. Declares:

  - 3 identifier columns (date, depot_id, week_number) used for keys/joins
  - 9 features (autoregressive lags, calendar flags, customer-mix signal,
    average order value, active customer count)
  - 1 target (orders_next_day, 1-day lookahead)

Expected usage:

    from specs.schemas.demand import schema
    await fs.register_features(schema)  # NOT .ingest()
    await fs.store(df, schema)
"""

from __future__ import annotations

# kailash-ml lazy-loads FeatureSchema + FeatureField via the package __init__.
# The `types` submodule is the public import path per the kailash-ml SKILL.md.
from kailash_ml.types import FeatureField, FeatureSchema  # type: ignore[import]

# Feature type constants — strings accepted by kailash-ml's schema validator.
# Mirrors the 13 columns in data/northwind_demand.csv per data-fixtures.md §1.2.
_FLOAT = "float"
_INT = "int"
_BOOL = "bool"


schema: FeatureSchema = FeatureSchema(
    name="northwind_demand",
    version=1,
    # entity_id_column is the FeatureStore primary key; timestamp_column is the
    # walk-forward CV anchor per EvalSpec(split_strategy='walk_forward').
    entity_id_column="depot_id",
    timestamp_column="date",
    features=[
        # NOTE: `date` and `depot_id` are declared as timestamp_column /
        # entity_id_column above — they are auto-added to the feature table by
        # FeatureStore and MUST NOT be duplicated in the features list below.
        FeatureField(
            name="week_number",
            dtype=_INT,
            nullable=False,
            description="1-based week from 2024-01-01 (cyclical indicator)",
        ),
        # === Features (9) ===
        FeatureField(
            name="orders_last_day",
            dtype=_INT,
            nullable=False,
            description="Yesterday's orders (autoregressive lag 1)",
        ),
        FeatureField(
            name="orders_7d_rolling_avg",
            dtype=_FLOAT,
            nullable=False,
            description="Trailing 7-day mean of orders",
        ),
        FeatureField(
            name="orders_28d_rolling_avg",
            dtype=_FLOAT,
            nullable=False,
            description="Trailing 28-day mean of orders",
        ),
        FeatureField(name="day_of_week", dtype=_INT, nullable=False, description="0=Mon, 6=Sun"),
        FeatureField(
            name="is_holiday",
            dtype=_BOOL,
            nullable=False,
            description="SG public holiday flag (2024-2025)",
        ),
        FeatureField(
            name="active_customers",
            dtype=_INT,
            nullable=False,
            description="Count of customers with an order in window",
        ),
        FeatureField(
            name="customer_mix_hash",
            dtype=_FLOAT,
            nullable=False,
            description="Hash of retail/hospitality/industrial ratios",
        ),
        FeatureField(
            name="avg_order_value",
            dtype=_FLOAT,
            nullable=False,
            description="Mean order value in SGD (~40.1 pre-drift)",
        ),
        FeatureField(
            name="is_peak_season", dtype=_BOOL, nullable=False, description="Q4 (Oct-Dec) flag"
        ),
        # === Target ===
        FeatureField(
            name="orders_next_day",
            dtype=_INT,
            nullable=False,
            description="1-day lookahead target (supervised label)",
        ),
    ],
)


__all__ = ["schema"]
