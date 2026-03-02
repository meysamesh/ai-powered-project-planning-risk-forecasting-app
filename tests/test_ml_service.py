from __future__ import annotations

import pandas as pd
import pytest

from src.ml.service import build_default_feature_df, score_tasks


class DummyModel:
    classes_ = ["Low", "Medium", "High"]

    def predict(self, features: pd.DataFrame) -> list[str]:
        labels: list[str] = []
        for _, row in features.iterrows():
            if row["Task_Duration_Days"] > 9:
                labels.append("High")
            elif row["Task_Duration_Days"] > 5:
                labels.append("Medium")
            else:
                labels.append("Low")
        return labels

    def predict_proba(self, features: pd.DataFrame) -> list[list[float]]:
        probs: list[list[float]] = []
        for _, row in features.iterrows():
            if row["Task_Duration_Days"] > 9:
                probs.append([0.10, 0.20, 0.70])
            elif row["Task_Duration_Days"] > 5:
                probs.append([0.20, 0.60, 0.20])
            else:
                probs.append([0.75, 0.20, 0.05])
        return probs


def test_build_default_feature_df_derives_duration_and_dependencies() -> None:
    tasks = [
        {
            "id": "T1",
            "name": "Design",
            "mean_duration": 4,
            "std_dev": 1,
            "dependencies": [],
            "risk_factor": 0.2,
        },
        {
            "id": "T2",
            "name": "Build",
            "mean_duration": 10,
            "std_dev": 2,
            "dependencies": ["T1"],
            "risk_factor": 0.7,
        },
    ]

    df = build_default_feature_df(tasks)

    assert list(df["Task_ID"]) == ["T1", "T2"]
    assert list(df["Task_Duration_Days"]) == [4.0, 10.0]
    assert list(df["Dependency_Count"]) == [0, 1]


def test_score_tasks_returns_predictions_and_summary() -> None:
    tasks = [
        {
            "id": "T1",
            "name": "Start",
            "mean_duration": 3,
            "std_dev": 0.5,
            "dependencies": [],
            "risk_factor": 0.1,
        },
        {
            "id": "T2",
            "name": "Integration",
            "mean_duration": 12,
            "std_dev": 2.0,
            "dependencies": ["T1"],
            "risk_factor": 0.8,
        },
    ]
    features = build_default_feature_df(tasks)

    validated, scored, summary = score_tasks(DummyModel(), features)

    assert validated.shape[0] == 2
    assert scored.shape[0] == 2
    assert "Predicted_Risk_Level" in scored.columns
    assert {"Probability_Low", "Probability_Medium", "Probability_High"}.issubset(set(scored.columns))
    assert summary["Count"].sum() == 2


def test_score_tasks_validates_feature_ranges() -> None:
    tasks = [
        {
            "id": "T1",
            "name": "Start",
            "mean_duration": 4,
            "std_dev": 0.5,
            "dependencies": [],
            "risk_factor": 0.3,
        }
    ]
    features = build_default_feature_df(tasks)
    features.loc[0, "Resource_Constraint_Score"] = 1.5

    with pytest.raises(ValueError) as exc_info:
        score_tasks(DummyModel(), features)

    assert "Feature validation failed" in str(exc_info.value)
