# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
#
# Schema authority: specs/canonical-values.md §8.4 (`POST /optimize/solve`
# request/response). Field names here match that spec exactly; solvers/
# vrp_solver.py and routes/optimize.py import from here.
"""Route optimization input/output schemas for `/optimize/solve`.

These dataclasses are the canonical shape of the VRP problem and its plan.
They are imported by `src/backend/routes/optimize.py`,
`src/backend/solvers/vrp_solver.py`, and `scripts/seed_route_plan.py`.

Field names match `specs/canonical-values.md` §8.4 request schema verbatim;
a change here requires a coordinated change in the canonical-values spec
and in every importing module (see `rules/specs-authority.md` MUST Rule 5).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Vehicle:
    """A single delivery vehicle in the Northwind fleet of 20."""

    id: str
    capacity_kg: float
    max_hours_per_day: float


@dataclass(frozen=True)
class DeliveryWindow:
    """Depot-level window during which deliveries may be loaded/dispatched."""

    depot_id: str
    open_hour: int  # 24-hour clock, local depot time
    close_hour: int


@dataclass(frozen=True)
class ConstraintSet:
    """Hard + soft constraints supplied to the solver.

    Shape matches `canonical-values.md` §8.4 — `hard_constraints` is a dict of
    named limits (e.g. {"vehicle_capacity": 40, "driver_hours_max": 9}),
    `soft_constraints` is a dict of named terms each carrying a penalty and a
    unit (e.g. {"delivery_before_5pm": {"penalty": 15, "unit": "per_hour_late"}}).
    """

    hard: dict
    soft: dict


@dataclass(frozen=True)
class RoutePlan:
    """Problem-plus-plan object handed between solver and persistence.

    - `depots`, `vehicles`, `delivery_windows` describe the problem.
    - `stops` is the solver's answer: ordered list of (vehicle_id, customer_id,
      arrival_time_minutes) tuples represented as dicts for JSON portability.
    - `scenario_tag` matches `canonical-values.md` §11 (union-cap, drift-week-78, …).
    """

    depots: list
    vehicles: list
    delivery_windows: list
    stops: list = field(default_factory=list)
    scenario_tag: Optional[str] = None
