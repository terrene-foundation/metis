# TODO-STUDENT: this is a scaffold placeholder.
# Your prompt to Claude Code must replace each handler body (the 501 stubs
# below) with the real implementation described in SCAFFOLD_MANIFEST.md and
# PLAYBOOK.md. The route registrations are PRE-BUILT and stay put.
# Do NOT edit manually — prompt Claude Code.
#
# Required endpoints:
#   POST /forecast/train   — AutoMLEngine run, returns experiment_run_id.
#                            Construct: TrainingPipeline(feature_store=fs, registry=registry);
#                                       HyperparameterSearch(pipeline, registry);
#                                       AutoMLEngine(pipeline, search, registry=registry).
#                            Call:      await engine.run(data=df, schema=schema,
#                                                         config=AutoMLConfig(candidate_families=[...]),
#                                                         eval_spec=EvalSpec(split_strategy='walk_forward'),
#                                                         experiment_name='forecast_sprint1',
#                                                         tracker=tracker).
#                            After pipeline.train() completes, call
#                            drift_wiring.wire(model_name, reference_df, feature_columns)
#                            synchronously before returning the response (writes
#                            .preflight.json.drift_wiring: true as a side effect).
#   GET  /forecast/compare — ExperimentTracker list+compare, returns >=3 runs
#   POST /forecast/predict — InferenceServer.predict. Accept model_version_id as
#                            a derived string `{name}_v{version}`; resolve to
#                            (name, version) via ml_context.parse_model_version_id.
#
# Forbidden constructor shapes (red-team findings):
#   - AutoMLEngine(feature_store=, model_registry=, config=)    # does not exist
#   - AutoMLConfig(families=[...])                              # use candidate_families
#   - EvalSpec(cv_strategy='rolling_origin')                    # use split_strategy='walk_forward'
#   - FeatureStore.ingest(path=, schema=)                       # use register_features + store
#
# Required call sites (for orphan-detection):
#   - TrainingPipeline, AutoMLEngine (from ml_context.get_ml_context())
#   - ExperimentTracker (list runs, compare runs)
#   - ModelRegistry.get_model / .promote_model
#   - InferenceServer.predict / .predict_batch
#   - ModelExplainer (surfaced in Phase 7 red-team; fall back to
#                      kailash_ml.engines.model_visualizer.permutation_importance
#                      on ImportError)
#   - drift_wiring.wire (called at end of /forecast/train)
"""Forecast routes (501 stubs — student-commissioned).

Registrations live from commit 1 so orphan-detection Rule 1 is satisfied
the moment the scaffold lands. Students replace handler bodies, not
registrations.
"""

from __future__ import annotations

import logging
import time
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Request

router = APIRouter()
log = logging.getLogger("metis.routes.forecast")

# Verbatim banner quoted in every 501 body so the operator / grader sees
# the phase-4 prompt template immediately on hitting the stub. Phase 4
# lives in specs/playbook-phases-sml.md — update both together.
_TODO_STUDENT_BANNER = (
    "TODO-STUDENT: POST /forecast/train, GET /forecast/compare, and "
    "POST /forecast/predict are scaffold placeholders. Replace each "
    "handler body by prompting Claude Code with the Phase 4 prompt "
    "template from specs/playbook-phases-sml.md (Phase 4 — Model "
    "Candidates): 'Load data/northwind_demand.csv into a Polars "
    "DataFrame. Build the FeatureSchema imported from "
    "specs/schemas/demand.py. Populate the FeatureStore by awaiting "
    "fs.register_features(schema) then fs.store(schema, df) — NOT "
    "fs.ingest(). Construct TrainingPipeline, HyperparameterSearch, "
    "AutoMLEngine(pipeline, search, registry=registry). Call "
    "await engine.run(data=df, schema=schema, "
    "config=AutoMLConfig(candidate_families=[...], "
    'search_strategy="random", search_n_trials=5), '
    'eval_spec=EvalSpec(split_strategy="walk_forward", '
    'metrics=["mape","rmse"]), '
    'experiment_name="forecast_sprint1", tracker=tracker).\' '
    "See scaffold-contract.md §2 for the full call-site list."
)


def _stub_payload(endpoint: str) -> dict[str, Any]:
    """Shape the 501 body so graders parse the TODO marker."""
    return {
        "error": "not implemented — prompt Claude Code to commission this endpoint",
        "endpoint": endpoint,
        "hint": "see PLAYBOOK.md Phase 4 for /forecast/train",
        "todo_student": _TODO_STUDENT_BANNER,
    }


def _bind_log(request: Request) -> tuple[logging.Logger, str]:
    """Return a logger bound with a correlation ID for this request."""
    request_id = request.headers.get("x-request-id") or f"req-{uuid.uuid4().hex[:12]}"
    # Use a LoggerAdapter-style extra. structlog would be nicer, but keeping
    # the dep surface minimal for the scaffold. Downstream log consumers
    # filter on request_id from extra kwargs.
    return log, request_id


@router.post("/train")
async def forecast_train(request: Request) -> dict[str, Any]:
    logger, request_id = _bind_log(request)
    t0 = time.monotonic()
    logger.info(
        "forecast_train.start",
        extra={"request_id": request_id, "route": "/forecast/train"},
    )
    try:
        body = _stub_payload("POST /forecast/train")
        logger.warning(
            "forecast_train.stub",
            extra={
                "request_id": request_id,
                "latency_ms": (time.monotonic() - t0) * 1000.0,
                "status": 501,
            },
        )
        raise HTTPException(status_code=501, detail=body)
    except HTTPException:
        raise
    except Exception as err:  # noqa: BLE001 — route must surface all errors as 500
        logger.exception(
            "forecast_train.error",
            extra={
                "request_id": request_id,
                "error": str(err),
                "latency_ms": (time.monotonic() - t0) * 1000.0,
            },
        )
        raise


@router.get("/compare")
async def forecast_compare(request: Request) -> dict[str, Any]:
    logger, request_id = _bind_log(request)
    t0 = time.monotonic()
    logger.info(
        "forecast_compare.start",
        extra={"request_id": request_id, "route": "/forecast/compare"},
    )
    body = _stub_payload("GET /forecast/compare")
    logger.warning(
        "forecast_compare.stub",
        extra={
            "request_id": request_id,
            "latency_ms": (time.monotonic() - t0) * 1000.0,
            "status": 501,
        },
    )
    raise HTTPException(status_code=501, detail=body)


@router.post("/predict")
async def forecast_predict(request: Request) -> dict[str, Any]:
    logger, request_id = _bind_log(request)
    t0 = time.monotonic()
    logger.info(
        "forecast_predict.start",
        extra={"request_id": request_id, "route": "/forecast/predict"},
    )
    body = _stub_payload("POST /forecast/predict")
    logger.warning(
        "forecast_predict.stub",
        extra={
            "request_id": request_id,
            "latency_ms": (time.monotonic() - t0) * 1000.0,
            "status": 501,
        },
    )
    raise HTTPException(status_code=501, detail=body)
