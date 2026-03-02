from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import dump
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline


TARGET_COLUMN = "Risk_Level"
ID_COLUMN = "Task_ID"
FEATURE_COLUMNS = [
    "Task_Duration_Days",
    "Labor_Required",
    "Equipment_Units",
    "Material_Cost_USD",
    "Start_Constraint",
    "Resource_Constraint_Score",
    "Site_Constraint_Score",
    "Dependency_Count",
]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train ProjectSense risk classifier and save model + metrics metadata."
    )
    parser.add_argument(
        "--dataset",
        default="data/construction_dataset.csv",
        help="Path to the training CSV dataset.",
    )
    parser.add_argument(
        "--model-out",
        default="models/risk_classifier.joblib",
        help="Path to output model artifact.",
    )
    parser.add_argument(
        "--metrics-out",
        default="models/risk_model_metrics.json",
        help="Path to output metrics JSON.",
    )
    parser.add_argument(
        "--model-version",
        default="",
        help="Optional model version override (default: generated timestamp-based version).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible split and model training.",
    )
    return parser.parse_args()


def _sha256_of_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(8192)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _validate_dataset(df: pd.DataFrame) -> None:
    required_columns = [ID_COLUMN, TARGET_COLUMN, *FEATURE_COLUMNS]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Dataset missing required columns: {missing}")
    if df[TARGET_COLUMN].nunique() < 2:
        raise ValueError("Target column must contain at least 2 classes.")


def main() -> None:
    args = _parse_args()

    dataset_path = Path(args.dataset)
    model_out = Path(args.model_out)
    metrics_out = Path(args.metrics_out)

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    model_out.parent.mkdir(parents=True, exist_ok=True)
    metrics_out.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(dataset_path)
    _validate_dataset(df)

    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=args.seed,
        stratify=y,
    )

    baseline = DummyClassifier(strategy="most_frequent")
    baseline.fit(X_train, y_train)
    baseline_pred = baseline.predict(X_test)
    baseline_acc = accuracy_score(y_test, baseline_pred)
    baseline_f1_macro = f1_score(y_test, baseline_pred, average="macro")

    model = Pipeline(
        steps=[
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=400,
                    max_depth=None,
                    min_samples_leaf=2,
                    class_weight="balanced",
                    random_state=args.seed,
                    n_jobs=-1,
                ),
            )
        ]
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    final_acc = accuracy_score(y_test, y_pred)
    final_f1_macro = f1_score(y_test, y_pred, average="macro")

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=args.seed)
    try:
        cv_scores = cross_val_score(model, X, y, cv=cv, scoring="f1_macro", n_jobs=-1)
    except Exception as exc:  # noqa: BLE001
        print(f"Parallel CV failed ({type(exc).__name__}: {exc}). Retrying with n_jobs=1.")
        cv_scores = cross_val_score(model, X, y, cv=cv, scoring="f1_macro", n_jobs=1)

    rf = model.named_steps["classifier"]
    importance_df = pd.DataFrame(
        {
            "feature": FEATURE_COLUMNS,
            "importance": rf.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    dump(model, model_out)

    trained_at = datetime.now(tz=UTC).isoformat()
    default_version = datetime.now(tz=UTC).strftime("v%Y.%m.%d.%H%M")
    model_version = args.model_version or default_version
    dataset_hash = _sha256_of_file(dataset_path)

    payload = {
        "model_version": model_version,
        "trained_at_utc": trained_at,
        "dataset_path": str(dataset_path.resolve()),
        "dataset_sha256": dataset_hash,
        "n_rows": int(df.shape[0]),
        "n_features": int(len(FEATURE_COLUMNS)),
        "feature_columns": FEATURE_COLUMNS,
        "target_column": TARGET_COLUMN,
        "seed": int(args.seed),
        "baseline_accuracy": float(baseline_acc),
        "baseline_macro_f1": float(baseline_f1_macro),
        "final_accuracy": float(final_acc),
        "final_macro_f1": float(final_f1_macro),
        "cv_macro_f1_scores": [float(item) for item in np.round(cv_scores, 6)],
        "cv_macro_f1_mean": float(cv_scores.mean()),
        "cv_macro_f1_std": float(cv_scores.std()),
        "feature_importance": importance_df.to_dict(orient="records"),
        "artifacts": {
            "model_path": str(model_out.resolve()),
            "metrics_path": str(metrics_out.resolve()),
        },
    }

    metrics_out.write_text(json.dumps(payload, indent=2))

    print("Training complete.")
    print(f"model_version={model_version}")
    print(f"dataset_sha256={dataset_hash}")
    print(f"final_accuracy={final_acc:.4f}")
    print(f"final_macro_f1={final_f1_macro:.4f}")
    print(f"cv_macro_f1_mean={cv_scores.mean():.4f}")
    print(f"model_out={model_out.resolve()}")
    print(f"metrics_out={metrics_out.resolve()}")


if __name__ == "__main__":
    main()
