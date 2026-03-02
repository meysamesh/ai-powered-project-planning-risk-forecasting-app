from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ai.task_generator import generate_task_plan
from src.analytics.metrics import compute_metrics
from src.config import settings
from src.ml.predictor import load_risk_model
from src.ml.service import build_default_feature_df, score_tasks
from src.modeling.graph_builder import build_project_graph
from src.simulation.monte_carlo import run_monte_carlo


def main() -> None:
    plan = generate_task_plan("Plan a marketing campaign launch", mode="mock")
    tasks = [task.model_dump() for task in plan.tasks]

    graph = build_project_graph(tasks)
    completion = run_monte_carlo(graph, iterations=300, seed=21)
    metrics = compute_metrics(completion, deadline_days=90)

    model, status = load_risk_model(
        enabled=settings.risk_model_enabled,
        model_path=settings.risk_model_path_file,
        model_version=settings.risk_model_version,
    )

    ml_rows = 0
    if model is not None and status.available:
        features = build_default_feature_df(tasks)
        _, predictions, _ = score_tasks(model, features)
        ml_rows = len(predictions)

    print("SMOKE TEST PASSED")
    print(f"tasks={len(tasks)} mean={metrics['mean']:.1f} p80={metrics['p80']:.1f}")
    print(f"ml_enabled={status.enabled} ml_available={status.available} ml_rows={ml_rows}")
    if not status.available:
        print(f"ml_status_message={status.message}")


if __name__ == "__main__":
    main()
