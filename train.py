"""
Smart Travel Planner - Trip Cost Prediction Model
Train a Random Forest Regressor to predict trip costs.
Usage: python train.py
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import os
import json

# ─── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
ENCODERS_PATH = os.path.join(BASE_DIR, "encoders.pkl")
METRICS_PATH = os.path.join(BASE_DIR, "metrics.json")


def load_and_preprocess(csv_path: str):
    """Load CSV and encode categorical columns."""
    df = pd.read_csv(csv_path)
    print(f"[INFO] Loaded {len(df)} records from {csv_path}")
    print(f"[INFO] Columns: {list(df.columns)}")

    categorical_cols = ["destination", "transport_type", "hotel_type"]
    encoders = {}

    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
        print(f"[INFO] Encoded '{col}': {list(le.classes_)}")

    return df, encoders


def train_model(df: pd.DataFrame):
    """Train Random Forest on the dataset."""
    feature_cols = ["destination", "days", "travelers", "transport_type", "hotel_type"]
    target_col = "estimated_trip_cost"

    X = df[feature_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)
    print(f"[INFO] Model trained on {len(X_train)} samples")

    # ── Evaluation ────────────────────────────────────────────────────────
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    cv_scores = cross_val_score(model, X, y, cv=5, scoring="r2")

    metrics = {
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "r2_score": round(r2, 4),
        "cv_r2_mean": round(cv_scores.mean(), 4),
        "cv_r2_std": round(cv_scores.std(), 4),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
    }

    print("\n[METRICS]")
    for k, v in metrics.items():
        print(f"  {k}: {v}")

    # Feature importance
    importances = dict(zip(feature_cols, model.feature_importances_.round(4)))
    print(f"\n[FEATURE IMPORTANCE] {importances}")

    return model, metrics


def save_artifacts(model, encoders, metrics):
    """Persist model, encoders, and metrics to disk."""
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"[INFO] Model saved → {MODEL_PATH}")

    with open(ENCODERS_PATH, "wb") as f:
        pickle.dump(encoders, f)
    print(f"[INFO] Encoders saved → {ENCODERS_PATH}")

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"[INFO] Metrics saved → {METRICS_PATH}")


def main():
    print("=" * 50)
    print("  Smart Travel Planner — Model Training")
    print("=" * 50)

    df, encoders = load_and_preprocess(DATA_PATH)
    model, metrics = train_model(df)
    save_artifacts(model, encoders, metrics)

    print("\n[SUCCESS] Training complete. Model is ready for prediction.")


if __name__ == "__main__":
    main()
