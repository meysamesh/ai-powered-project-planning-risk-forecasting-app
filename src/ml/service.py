from __future__ import annotations

from typing import Any

import pandas as pd
from pydantic import ValidationError

from src.ml.predictor import predict_with_model
from src.ml.schema import FEATURE_EDITOR_COLUMNS, MODEL_FEATURE_COLUMNS, TaskRiskFeatures


def build_default_feature_df(tasks: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for task in tasks:
        risk_factor = float(task.get("risk_factor", 0.4))
        mean_duration = max(1.0, float(task.get("mean_duration", 1.0)))
        dependency_count = len(task.get("dependencies", []))

        rows.append(
            {
                "Task_ID": str(task.get("id", "")).strip(),
                "Task_Duration_Days": round(mean_duration, 2),
                "Labor_Required": max(1, int(round(3 + risk_factor * 10))),
                "Equipment_Units": max(1, int(round(1 + risk_factor * 4))),
                "Material_Cost_USD": round(mean_duration * (900 + risk_factor * 600), 2),
                "Start_Constraint": 0,
                "Resource_Constraint_Score": round(min(max(risk_factor, 0.0), 1.0), 2),
                "Site_Constraint_Score": round(min(max(0.35 + risk_factor * 0.5, 0.0), 1.0), 2),
                "Dependency_Count": dependency_count,
            }
        )

    return pd.DataFrame(rows, columns=FEATURE_EDITOR_COLUMNS)


def validate_and_normalize_features_df(df: pd.DataFrame) -> pd.DataFrame:
    missing_columns = [column for column in FEATURE_EDITOR_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required feature columns: {missing_columns}")

    normalized = df[FEATURE_EDITOR_COLUMNS].copy()
    numeric_cols = [
        "Task_Duration_Days",
        "Labor_Required",
        "Equipment_Units",
        "Material_Cost_USD",
        "Start_Constraint",
        "Resource_Constraint_Score",
        "Site_Constraint_Score",
        "Dependency_Count",
    ]

    for column in numeric_cols:
        normalized[column] = pd.to_numeric(normalized[column], errors="coerce")

    records: list[dict[str, Any]] = []
    errors: list[str] = []
    for idx, row in normalized.iterrows():
        payload = row.to_dict()
        try:
            feature_row = TaskRiskFeatures.model_validate(payload)
            records.append(feature_row.model_dump())
        except ValidationError as exc:
            first_error = exc.errors()[0]
            loc = ".".join(str(part) for part in first_error.get("loc", []))
            msg = first_error.get("msg", "Invalid value")
            errors.append(f"Row {idx + 1} ({loc}): {msg}")

    if errors:
        preview = "; ".join(errors[:5])
        raise ValueError(f"Feature validation failed. {preview}")

    return pd.DataFrame(records, columns=FEATURE_EDITOR_COLUMNS)


def summarize_predictions(predictions_df: pd.DataFrame) -> pd.DataFrame:
    if predictions_df.empty or "Predicted_Risk_Level" not in predictions_df.columns:
        return pd.DataFrame(columns=["Risk_Level", "Count"])

    counts = predictions_df["Predicted_Risk_Level"].value_counts()
    summary_df = counts.rename_axis("Risk_Level").reset_index(name="Count")
    return summary_df


def score_tasks(
    model: Any,
    features_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    validated_df = validate_and_normalize_features_df(features_df)
    model_input = validated_df[MODEL_FEATURE_COLUMNS].copy()
    predictions_df = predict_with_model(model, model_input)
    scored_df = pd.concat([validated_df[["Task_ID"]], predictions_df], axis=1)
    summary_df = summarize_predictions(scored_df)
    return validated_df, scored_df, summary_df
