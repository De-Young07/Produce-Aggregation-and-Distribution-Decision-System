import pandas as pd
import os
import mlflow
import joblib

from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet


def train_models():

    os.makedirs("models/saved_models", exist_ok=True)

    files = os.listdir("data/processed")

    for file in files:

        df = pd.read_csv(f"data/processed/{file}")

        df["date"] = pd.to_datetime(df["date"])

        df = df.sort_values("date")

        series = df["price_per_kg"]

        name = file.replace(".csv", "")

        with mlflow.start_run(run_name=name):

            # ARIMA
            arima_model = ARIMA(series, order=(2,1,2))
            arima_fit = arima_model.fit()

            joblib.dump(
                arima_fit,
                f"models/saved_models/{name}_arima.pkl"
            )

            mlflow.log_param("model", "ARIMA")

            # Prophet
            prophet_df = df[["date", "price_per_kg"]]
            prophet_df.columns = ["ds", "y"]

            prophet_model = Prophet()
            prophet_model.fit(prophet_df)

            joblib.dump(
                prophet_model,
                f"models/saved_models/{name}_prophet.pkl"
            )

            mlflow.log_param("model", "Prophet")

    print("Models trained")