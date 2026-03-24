import pandas as pd
import os
import joblib


def generate_forecasts():

    os.makedirs("data/forecasts", exist_ok=True)

    performance = pd.read_csv("data/forecasts/model_performance.csv")

    best_models = performance.loc[
        performance.groupby("dataset")["mae"].idxmin()
    ]

    for _, row in best_models.iterrows():

        name = row["dataset"]
        model_type = row["model"]

        df = pd.read_csv(f"data/processed/{name}.csv")

        if model_type == "ARIMA":

            model = joblib.load(
                f"models/saved_models/{name}_arima.pkl"
            )

            forecast = model.forecast(steps=30)

            forecast_df = pd.DataFrame({"forecast": forecast})

        else:

            model = joblib.load(
                f"models/saved_models/{name}_prophet.pkl"
            )

            future = model.make_future_dataframe(periods=30)

            forecast = model.predict(future)

            forecast_df = forecast[["ds", "yhat"]].tail(30)

        forecast_df.to_csv(
            f"data/forecasts/{name}_forecast.csv",
            index=False
        )

    print("Forecasts generated")