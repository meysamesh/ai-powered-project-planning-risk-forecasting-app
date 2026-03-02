from __future__ import annotations

import numpy as np
import pandas as pd

from src.storage.db import get_connection, init_db
from src.storage.repository import get_run_details, save_session_run


def _sample_tasks() -> list[dict]:
    return [
        {
            "id": "T1",
            "name": "Start",
            "mean_duration": 4,
            "std_dev": 1.0,
            "dependencies": [],
            "risk_factor": 0.2,
        },
        {
            "id": "T2",
            "name": "Build",
            "mean_duration": 6,
            "std_dev": 1.5,
            "dependencies": ["T1"],
            "risk_factor": 0.5,
        },
    ]


def test_init_db_is_idempotent_with_ml_table(tmp_path) -> None:
    db_path = tmp_path / "test.db"

    init_db(str(db_path))
    init_db(str(db_path))

    with get_connection(str(db_path)) as conn:
        row = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name='ml_predictions'
            """
        ).fetchone()

    assert row is not None
    assert row["name"] == "ml_predictions"


def test_save_and_load_run_with_ml_predictions(tmp_path) -> None:
    db_path = tmp_path / "test.db"
    init_db(str(db_path))

    tasks = _sample_tasks()
    scenarios_df = pd.DataFrame(
        [
            {
                "Scenario": "Baseline",
                "Delay Prob (%)": 33.3,
                "P80 (days)": 15.0,
                "Mean (days)": 12.1,
                "Notes": "Deadline: 20 days",
            }
        ]
    )
    features_df = pd.DataFrame(
        [
            {
                "Task_ID": "T1",
                "Task_Duration_Days": 4,
                "Labor_Required": 5,
                "Equipment_Units": 2,
                "Material_Cost_USD": 1200.0,
                "Start_Constraint": 0,
                "Resource_Constraint_Score": 0.2,
                "Site_Constraint_Score": 0.3,
                "Dependency_Count": 0,
            },
            {
                "Task_ID": "T2",
                "Task_Duration_Days": 6,
                "Labor_Required": 7,
                "Equipment_Units": 3,
                "Material_Cost_USD": 2200.0,
                "Start_Constraint": 0,
                "Resource_Constraint_Score": 0.4,
                "Site_Constraint_Score": 0.5,
                "Dependency_Count": 1,
            },
        ]
    )
    predictions_df = pd.DataFrame(
        [
            {
                "Task_ID": "T1",
                "Predicted_Risk_Level": "Low",
                "Probability_Low": 0.7,
                "Probability_Medium": 0.2,
                "Probability_High": 0.1,
            },
            {
                "Task_ID": "T2",
                "Predicted_Risk_Level": "Medium",
                "Probability_Low": 0.2,
                "Probability_Medium": 0.6,
                "Probability_High": 0.2,
            },
        ]
    )

    run_id = save_session_run(
        project_text="Sample project",
        mode="mock",
        params={"max_tasks": 12},
        tasks=tasks,
        deadline_days=20,
        iterations=100,
        seed=7,
        metrics={"delay_probability": 0.33, "p80": 15, "mean": 12.1},
        completion_times=np.array([11.0, 12.0, 13.0]),
        scenarios_df=scenarios_df,
        ml_features_df=features_df,
        ml_predictions_df=predictions_df,
        model_version="v-test",
        db_path=str(db_path),
    )

    loaded = get_run_details(run_id, db_path=str(db_path))
    assert loaded is not None
    assert loaded["ml_predictions"] is not None
    assert loaded["ml_predictions"]["model_version"] == "v-test"
    assert len(loaded["ml_predictions"]["features"]) == 2
    assert len(loaded["ml_predictions"]["predictions"]) == 2
