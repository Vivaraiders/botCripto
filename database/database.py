import mysql.connector
from os import getenv


def get_connection():
    try:
        conn = mysql.connector.connect(
            host=getenv("MYSQLHOST"),
            user=getenv("MYSQLUSER"),
            password=getenv("MYSQLPASSWORD"),
            database=getenv("MYSQLDATABASE"),
            port=int(getenv("MYSQLPORT", 3306))
        )
        return conn
    except Exception as e:
        print("erro na conexão:", e)
        return None
 