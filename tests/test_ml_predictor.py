from __future__ import annotations

from pathlib import Path

from joblib import dump

from src.ml.predictor import load_risk_model


class MinimalModel:
    classes_ = ["Low", "Medium", "High"]

    def predict(self, features):  # noqa: ANN001
        return ["Low"] * len(features)

    def predict_proba(self, features):  # noqa: ANN001
        return [[0.8, 0.15, 0.05] for _ in range(len(features))]


def test_load_risk_model_disabled() -> None:
    model, status = load_risk_model(
        enabled=False,
        model_path=Path("models/risk_classifier.joblib"),
        model_version="v-test",
    )
    assert model is None
    assert status.available is False
    assert status.enabled is False


def test_load_risk_model_missing_file(tmp_path) -> None:
    model, status = load_risk_model(
        enabled=True,
        model_path=tmp_path / "missing.joblib",
        model_version="v-test",
    )
    assert model is None
    assert status.available is False
    assert "not found" in status.message.lower()


def test_load_risk_model_success(tmp_path) -> None:
    model_path = tmp_path / "model.joblib"
    dump(MinimalModel(), model_path)

    model, status = load_risk_model(
        enabled=True,
        model_path=model_path,
        model_version="v-test",
    )
    assert model is not None
    assert status.available is True
    assert status.model_version == "v-test"
