import pandas as pd
import os


def build_time_series():

    df = pd.read_csv("data/features/market_features.csv")

    os.makedirs("data/processed", exist_ok=True)

    grouped = df.groupby(["crop", "market"])

    for (crop, market), group in grouped:

        group = group.sort_values("date")

        filename = f"{crop}_{market}_timeseries.csv"

        group.to_csv(
            f"data/processed/{filename}",
            index=False
        )

        print(f"Created {filename}")