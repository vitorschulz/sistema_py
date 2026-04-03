import os
import mysql.connector
import time

def get_db_connection():
    for i in range(10):
        try:
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST") or "localhost",
                user=os.getenv("DB_USER") or "root",
                password=os.getenv("DB_PASSWORD") or "",
                database=os.getenv("DB_NAME") or "gestao"
            )
            print("Conectou no MySQL!")
            return conn
        except mysql.connector.Error:
            print("MySQL não disponível ainda, tentando novamente...")
            time.sleep(3)

    raise Exception("Não conseguiu conectar no MySQL")