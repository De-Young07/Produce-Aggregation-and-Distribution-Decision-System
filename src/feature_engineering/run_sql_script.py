import mysql.connector
from src.utils.database import get_db_connection

def run_sql_script():

    conn = get_db_connection()
    cursor = conn.cursor()

    with open("src/sql/feature_queries.sql", "r") as file:
        sql_script = file.read()

    statements = sql_script.split(";")

    for statement in statements:
        if statement.strip():
            cursor.execute(statement)

    conn.commit()
    conn.close()

    print("SQL feature views created successfully")