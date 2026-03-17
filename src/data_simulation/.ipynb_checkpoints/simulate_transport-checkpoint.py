import pandas as pd
import numpy as np
from src.config import MARKETS

def simulate_transport():

    rows = []

    for market in MARKETS:

        rows.append({
            "origin": "central_warehouse",
            "market": market,
            "cost_per_kg": np.random.uniform(5, 15),
            "capacity": np.random.randint(2000, 5000)
        })

    df = pd.DataFrame(rows)

    df.to_csv("data/raw/transport_costs.csv", index=False)

    return df