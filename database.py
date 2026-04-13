import mysql.connector
from datetime import datetime,timedelta
from os import getenv
from dotenv import load_dotenv

load_dotenv()

DB_HOST= getenv('DB_HOST')
DB_USER=getenv('DB_USER')
DB_PASSWORD=getenv('DB_PASSWORD')
DB_DATABASE=getenv('DB_DATABASE')

def get_connection():
    try:
        conn = mysql.connector.connect(
            host= DB_HOST,
            user= DB_USER,
            password= DB_PASSWORD,
            database=DB_DATABASE
        )
    
        print('conexão estabelecida!')
        return conn
    
    except mysql.connector.Error as err:
        print(f'erro na conexão: {err}')
        return None
    
def add_user(conn,cursor, chat_id):
    expires_at = datetime.now() + timedelta(days=30)

    cursor.execute(
    """
        INSERT IGNORE INTO user(chat_id, is_active, plan, expires_at)
        VALUES(%s, %s, %s, %s)
    """, (chat_id, 'yes', 'free', expires_at))

    conn.commit()

def user_chatId(cursor):
    cursor.execute(
    """
        SELECT chat_id
        FROM user;
    """)

    result = cursor.fetchall()
    return [row[0] for row in result]