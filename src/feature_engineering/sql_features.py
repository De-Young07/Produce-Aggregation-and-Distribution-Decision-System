import pandas as pd
import os
from src.utils.database import get_db_connection


def extract_feature_table():

    conn = get_db_connection()

    query = """
    SELECT *
    FROM market_features_extended
    """

    df = pd.read_sql(query, conn)

    os.makedirs("data/features", exist_ok=True)

    df.to_csv(
        "data/features/market_features.csv",
        index=False
    )

    conn.close()

    print("Feature dataset created")

    return df