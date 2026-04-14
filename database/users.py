from datetime import datetime, timedelta

def add_user(conn,cursor, chat_id):
    expires_at = datetime.now() + timedelta(days=30)

    cursor.execute(
    """
        INSERT IGNORE INTO users(chat_id, is_active, plan, expires_at)
        VALUES(%s, %s, %s, %s)
    """, (chat_id, 'yes', 'free', expires_at))

    conn.commit()

def get_user_chatId(cursor):
    cursor.execute(
    """
        SELECT chat_id
        FROM users;
    """)

    result = cursor.fetchall()
    return [row[0] for row in result]