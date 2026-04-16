import os
import mysql.connector

print("HOST:", os.getenv("MYSQLHOST"))
print("USER:", os.getenv("MYSQLUSER"))
print("DB:", os.getenv("MYSQLDATABASE"))
print("PORT:", os.getenv("MYSQLPORT"))

try:
    conn = mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT"))
    )
    print("CONECTOU ✅")
except Exception as e:
    print("ERRO REAL:", e)