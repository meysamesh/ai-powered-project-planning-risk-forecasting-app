from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class RiskModelStatus:
    enabled: bool
    available: bool
    model_path: str
    model_version: str
    message: str


def load_risk_model(
    enabled: bool,
    model_path: Path,
    model_version: str,
) -> tuple[Any | None, RiskModelStatus]:
    path = Path(model_path)
    if not enabled:
        return None, RiskModelStatus(
            enabled=False,
            available=False,
            model_path=str(path),
            model_version=model_version,
            message="Risk model is disabled by configuration.",
        )

    if not path.exists():
        return None, RiskModelStatus(
            enabled=True,
            available=False,
            model_path=str(path),
            model_version=model_version,
            message="Model file not found. Simulation features remain available.",
        )

    try:
        from joblib import load  # Imported lazily to keep startup resilient.
    except Exception as exc:  # noqa: BLE001
        return None, RiskModelStatus(
            enabled=True,
            available=False,
            model_path=str(path),
            model_version=model_version,
            message=f"joblib import failed: {exc}",
        )

    try:
        model = load(path)
    except Exception as exc:  # noqa: BLE001
        return None, RiskModelStatus(
            enabled=True,
            available=False,
            model_path=str(path),
            model_version=model_version,
            message=f"Failed to load model: {exc}",
        )

    required_attrs = ("predict", "predict_proba", "classes_")
    for attr in required_attrs:
        if not hasattr(model, attr):
            return None, RiskModelStatus(
                enabled=True,
                available=False,
                model_path=str(path),
                model_version=model_version,
                message=f"Loaded object is missing required attribute: {attr}",
            )

    return model, RiskModelStatus(
        enabled=True,
        available=True,
        model_path=str(path),
        model_version=model_version,
        message="Model ready for advisory scoring.",
    )


def predict_with_model(model: Any, features: pd.DataFrame) -> pd.DataFrame:
    predictions = model.predict(features)
    probabilities = model.predict_proba(features)
    classes = [str(item) for item in model.classes_]

    proba_df = pd.DataFrame(
        probabilities,
        columns=[f"Probability_{label}" for label in classes],
    )
    pred_df = pd.DataFrame({"Predicted_Risk_Level": predictions})
    return pd.concat([pred_df, proba_df], axis=1)
