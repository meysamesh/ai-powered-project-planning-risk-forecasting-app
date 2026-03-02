# Architecture Snapshot (MVP -> Demo-Production)

## Objective
Deliver a stakeholder-ready decision-support app that combines:
- AI plan generation,
- probabilistic timeline forecasting,
- advisory ML risk scoring.

## Runtime Flow
1. User enters project text and constraints in Streamlit (`app.py`).
2. `src/ai/task_generator.py` creates task plan (`mock` or `real` Groq mode).
3. `src/ai/schema.py` validates structure and dependency integrity.
4. Workflow graph and critical path are computed (`src/modeling/`).
5. Monte Carlo simulation and metrics run (`src/simulation/`, `src/analytics/`).
6. Advisory classifier scores tasks (`src/ml/`, `models/risk_classifier.joblib`).
7. Scenarios are compared and recommendation is displayed.
8. Session + optional ML payloads persist in SQLite (`src/storage/`).

## Key Modules
- `app.py`: orchestration, tabs, user interactions, export.
- `src/ai/`: prompt, LLM client, task generation.
- `src/modeling/`: graph builder + critical path logic.
- `src/simulation/`: dynamic critical-path Monte Carlo engine.
- `src/analytics/`: metrics, delay drivers, scenario comparison.
- `src/ml/`: feature schema, model loading, advisory scoring.
- `src/storage/`: SQLite schema and repository helpers.

## Reliability Controls
- `APP_MODE=mock` fallback for demo resilience.
- Strict schema checks before simulation.
- Model status reporting and non-blocking fallback when ML artifact is unavailable.
- `scripts/smoke_test.py` for fast end-to-end verification.
- CI: compile check + smoke test + unit tests + Docker build.

## Artifact Lifecycle
- Training script: `scripts/train_risk_model.py`
- Model artifact: `models/risk_classifier.joblib`
- Metrics/version metadata: `models/risk_model_metrics.json`
- Config flags:
  - `RISK_MODEL_ENABLED`
  - `RISK_MODEL_PATH`
  - `RISK_MODEL_METRICS_PATH`
  - `RISK_MODEL_VERSION`
