import pandas as pd
from src.utils.database import get_db_connection
import os


def build_optimization_dataset():

    conn = get_db_connection()

    query = """
    SELECT 
        f.crop,
        f.market,
        AVG(f.forecast_value) AS forecast_price,
        COALESCE(SUM(s.quantity_supplied), 1000) AS supply,
        COALESCE(AVG(t.cost_per_kg), 10) AS transport_cost

    FROM forecasts f

    LEFT JOIN supply s
    ON f.crop = s.crop

    LEFT JOIN transport_costs t
    ON f.market = t.market

    GROUP BY f.crop, f.market
    """

    df = pd.read_sql(query, conn)

    conn.close()

    os.makedirs("data/optimization", exist_ok=True)

    df.to_csv("data/optimization/optimization_input.csv", index=False)

    print("Optimization dataset created")

    return df