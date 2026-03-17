import pandas as pd
import numpy as np
import yaml
import os

def simulate_prices():

    with open("config/config.yaml") as f:
        config = yaml.safe_load(f)

    crops = config["entities"]["crops"]
    markets = config["entities"]["markets"]
    start = config["data"]["start_date"]
    end = config["data"]["end_date"]

    dates = pd.date_range(start, end)

    rows = []

    for crop in crops:
        for market in markets:

            base_price = np.random.uniform(90, 200)

            trend = np.linspace(0, 20, len(dates))

            noise = np.random.normal(0, 5, len(dates))

            prices = base_price + trend + noise

            for i, date in enumerate(dates):

                rows.append({
                    "date": date,
                    "crop": crop,
                    "market": market,
                    "price_per_kg": round(prices[i],2)
                })

    df = pd.DataFrame(rows)

    os.makedirs("data/raw", exist_ok=True)

    df.to_csv("data/raw/prices.csv", index=False)

    return df