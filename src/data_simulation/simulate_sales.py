import pandas as pd
import numpy as np
import yaml
import os

def simulate_sales():

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

            base_price = np.random.uniform(80,200)

            for date in dates:

                quantity = np.random.randint(100,500)

                price = base_price + np.random.normal(0,10)

                revenue = quantity * price

                rows.append({
                    "date": date,
                    "crop": crop,
                    "market": market,
                    "quantity": quantity,
                    "revenue": round(revenue,2)
                })

    df = pd.DataFrame(rows)

    os.makedirs("data/raw", exist_ok=True)

    df.to_csv("data/raw/sales.csv", index=False)

    return df