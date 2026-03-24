import pandas as pd
import os
import joblib
import numpy as np
from sklearn.metrics import mean_absolute_error


def evaluate_models():

    results = []

    files = os.listdir("data/processed")

    for file in files:

        df = pd.read_csv(f"data/processed/{file}")

        series = df["price_per_kg"]

        train = series[:-30]
        test = series[-30:]

        name = file.replace(".csv", "")

        # ARIMA
        arima_model = joblib.load(
            f"models/saved_models/{name}_arima.pkl"
        )

        arima_pred = arima_model.forecast(steps=30)

        arima_mae = mean_absolute_error(test, arima_pred)

        results.append([name, "ARIMA", arima_mae])

        # Prophet
        prophet_model = joblib.load(
            f"models/saved_models/{name}_prophet.pkl"
        )

        future = prophet_model.make_future_dataframe(periods=30)

        forecast = prophet_model.predict(future)

        prophet_pred = forecast["yhat"][-30:]

        prophet_mae = mean_absolute_error(test, prophet_pred)

        results.append([name, "Prophet", prophet_mae])

    result_df = pd.DataFrame(
        results,
        columns=["dataset", "model", "mae"]
    )

    result_df.to_csv("data/forecasts/model_performance.csv", index=False)

    print("Evaluation complete")

    return result_df