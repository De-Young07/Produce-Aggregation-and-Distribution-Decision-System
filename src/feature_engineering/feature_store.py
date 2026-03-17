import pandas as pd
import os

def register_features():

    df = pd.read_csv("data/features/market_features.csv")

    os.makedirs("data/features/store", exist_ok=True)

    df.to_parquet(
        "data/features/store/market_features.parquet"
    )

    print("Feature store updated")