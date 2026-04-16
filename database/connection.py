from database.database import get_connection
conn = None

def get_conn():
    global conn
    if conn is None:
        conn = get_connection()
    return conn