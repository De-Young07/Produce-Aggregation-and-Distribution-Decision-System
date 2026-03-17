import pandas as pd
from src.utils.database import get_db_connection

def load_csv_to_mysql(file_path, table_name):

    conn = get_db_connection()
    cursor = conn.cursor()

    df = pd.read_csv(file_path)

    columns = ", ".join(df.columns)

    placeholders = ", ".join(["%s"] * len(df.columns))

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {", ".join([f"{col} VARCHAR(255)" for col in df.columns])}
    )
    """

    cursor.execute(create_table_query)

    insert_query = f"""
    INSERT INTO {table_name} ({columns})
    VALUES ({placeholders})
    """

    for _, row in df.iterrows():
        cursor.execute(insert_query, tuple(row))

    conn.commit()
    conn.close()

    print(f"{table_name} loaded successfully")