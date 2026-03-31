import os
import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST") or "localhost",
        user=os.getenv("DB_USER") or "root",
        password=os.getenv("DB_PASSWORD") or "",
        database=os.getenv("DB_NAME") or "gestao"
    )
    return conn