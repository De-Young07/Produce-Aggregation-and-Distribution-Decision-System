import pandas as pd
import numpy as np
from src.config import CROPS, MARKETS, START_DATE, END_DATE

def simulate_demand():

    dates = pd.date_range(START_DATE, END_DATE)

    rows = []

    for crop in CROPS:
        for market in MARKETS:

            base_demand = np.random.randint(300, 1000)

            for date in dates:

                demand = base_demand + np.random.normal(0, 50)

                rows.append({
                    "date": date,
                    "crop": crop,
                    "market": market,
                    "demand": int(abs(demand))
                })

    df = pd.DataFrame(rows)

    df.to_csv("data/raw/demand.csv", index=False)

    return df