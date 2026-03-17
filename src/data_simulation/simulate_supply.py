import pandas as pd
import numpy as np
from src.config import CROPS, FARMERS, START_DATE, END_DATE

def simulate_supply():

    dates = pd.date_range(START_DATE, END_DATE)

    rows = []

    for farmer in range(1, FARMERS+1):
        crop = np.random.choice(CROPS)

        for date in dates:

            quantity = np.random.randint(50, 500)

            rows.append({
                "date": date,
                "farmer_id": farmer,
                "crop": crop,
                "quantity_supplied": quantity
            })

    df = pd.DataFrame(rows)

    df.to_csv("data/raw/supply.csv", index=False)

    return df