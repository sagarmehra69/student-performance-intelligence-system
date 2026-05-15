import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


def prepare_features(df):
    grouped = df.groupby("student_id")

    features = grouped["marks"].agg([
        "mean",
        "std",
        "min",
        "max",
        "count"
    ]).reset_index()

    features.columns = [
        "student_id",
        "avg_marks",
        "std_dev",
        "min_marks",
        "max_marks",
        "num_subjects"
    ]

    # Performance Trend
    trends = []

    for sid, group in grouped:
        marks = group["marks"].values

        if len(marks) > 1:
            slope = np.polyfit(range(len(marks)), marks, 1)[0]
        else:
            slope = 0

        trends.append(slope)

    features["trend"] = trends

    # Simulated future score target
    features["future_score"] = (
        features["avg_marks"] * 0.5 +
        features["max_marks"] * 0.2 +
        features["trend"] * 10 +
        np.random.normal(0, 5, len(features))
    )

    features.fillna(0, inplace=True)

    return features

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

def train_model(df):
    features = prepare_features(df)

    X = features.drop(columns=["student_id", "future_score"])
    y = features["future_score"]

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Train Model
    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Metrics
    mae = mean_absolute_error(y_test, y_pred)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    r2 = r2_score(y_test, y_pred)

    metrics = {
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "R2": round(r2, 2)
    }

    return model, features, metrics


def predict_marks(model, features, student_id):
    student = features[features["student_id"] == student_id]

    if student.empty:
        return 0

    X = student.drop(columns=["student_id", "future_score"])
    prediction = model.predict(X)[0]
    return float(model.predict(X)[0])


def risk_level(pred, features):
    """
    Dynamic risk classification using dataset distribution.
    """

    avg_score = features["future_score"].mean()

    high_threshold = avg_score + 10
    low_threshold = avg_score - 10

    if pred >= high_threshold:
        return "🟢 Safe Zone"

    elif pred >= low_threshold:
        return "🟡 Watchlist"

    else:
        return "🔴 Critical"