import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def load_data(path):
    df = pd.read_csv(path)

    # Handle missing value
    df["Battery Capacity (kWh)"] = df["Battery Capacity (kWh)"].fillna(
        df["Battery Capacity (kWh)"].median()
    )
    df["Charging Rate (kW)"] = df["Charging Rate (kW)"].fillna(
        df["Charging Rate (kW)"].median()
    )
    df["Temperature (°C)"] = df["Temperature (°C)"].fillna(
        df["Temperature (°C)"].median()
    )

    # Feature Engineering
    df["soc_change"] = (
        df["State of Charge (End %)"] -
        df["State of Charge (Start %)"]
    )

    df["Charging Start Time"] = pd.to_datetime(df["Charging Start Time"])
    df["hour"] = df["Charging Start Time"].dt.hour
    df["month"] = df["Charging Start Time"].dt.month
    df["day_of_week"] = df["Charging Start Time"].dt.dayofweek
    df["is_weekend"] = df["day_of_week"].apply(lambda x: 1 if x >= 5 else 0)

    df = df.drop(columns=[
        "Charging Start Time",
        "State of Charge (Start %)",
        "State of Charge (End %)"
    ])

    return df


def train_model(data_path, model_path):

    df = load_data(data_path)

    target = "Energy Consumed (kWh)"
    X = df.drop(columns=[target])
    y = df[target]

    categorical_cols = X.select_dtypes(include="object").columns

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
        ],
        remainder="passthrough"
    )

    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(
            n_estimators=200,
            random_state=42
        ))
    ])

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("Model Performance:")
    print("MAE:", mean_absolute_error(y_test, y_pred))
    print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
    print("R2:", r2_score(y_test, y_pred))

    # Create models directory if it doesn't exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    joblib.dump(model, model_path)

    print("Model saved successfully!")


if __name__ == "__main__":
    train_model(
        data_path="data/Raw_Dataset.csv",
        model_path="models/ev_demand_model.pkl"
    )