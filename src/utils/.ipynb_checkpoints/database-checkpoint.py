import mysql.connector

def get_db_connection():

    config = {
        "host": "localhost",
        "user": "root",
        "password": "Adebc4real"
    }

    database_name = "agri_pipeline"

    conn = mysql.connector.connect(**config)

    cursor = conn.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")

    conn.database = database_name

    return conn