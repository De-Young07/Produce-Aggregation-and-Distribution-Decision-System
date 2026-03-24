import pandas as pd
import os
from src.utils.database import get_db_connection


def load_forecasts_to_mysql():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
CREATE TABLE IF NOT EXISTS forecasts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    crop VARCHAR(50),
    market VARCHAR(50),
    model VARCHAR(20),
    forecast_value FLOAT
)
""")

    files = os.listdir("data/forecasts")

    for file in files:

        if "forecast" not in file:
            continue

        path = f"data/forecasts/{file}"

        df = pd.read_csv(path)

        # extract metadata
        name = file.replace("_forecast.csv", "")
        crop, market = name.split("_")

        if "ds" in df.columns:
            df.rename(columns={"ds": "date", "yhat": "forecast_value"}, inplace=True)
        else:
            df["date"] = pd.date_range(start=pd.Timestamp.today(), periods=len(df))
            df.rename(columns={"forecast": "forecast_value"}, inplace=True)

        for _, row in df.iterrows():

            query = """
            INSERT INTO forecasts (date, crop, market, model, forecast_value)
            VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(query, (
                row["date"],
                crop,
                market,
                "auto",
                row["forecast_value"]
            ))

    conn.commit()
    conn.close()

    print("Forecasts loaded into MySQL")