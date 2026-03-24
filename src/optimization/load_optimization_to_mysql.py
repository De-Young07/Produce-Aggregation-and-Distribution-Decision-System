import pandas as pd
from src.utils.database import get_db_connection


def load_optimization_results():

    df = pd.read_csv("data/optimization/optimal_distribution.csv")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS optimization_results (
        id INT AUTO_INCREMENT PRIMARY KEY,
        crop VARCHAR(50),
        market VARCHAR(50),
        optimal_quantity FLOAT
    )
    """)

    for _, row in df.iterrows():

        cursor.execute("""
        INSERT INTO optimization_results (crop, market, optimal_quantity)
        VALUES (%s, %s, %s)
        """, (row["crop"], row["market"], row["optimal_quantity"]))

    conn.commit()
    conn.close()

    print("Optimization results stored in MySQL")