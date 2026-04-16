from database.database import get_connection


def add_coin(chat_id, symbol):
    conn = get_connection()
    if conn is None:
        print("Sem conexão com banco (add_coin)")
        return None

    cursor = conn.cursor()

    cursor.execute(
        'SELECT id FROM users WHERE chat_id = %s',
        (chat_id,)
    )
    result = cursor.fetchone()

    if result is None:
        return None

    user_id = result[0]

    cursor.execute(
        'INSERT IGNORE INTO coins(user_id, symbol) VALUES (%s, %s)',
        (user_id, symbol)
    )

    conn.commit()
    conn.close()

    return user_id


def find_user_coin(chat_id):
    conn = get_connection()
    if conn is None:
        print("Sem conexão com banco (find_user_coin)")
        return []

    cursor = conn.cursor()

    cursor.execute(
        'SELECT id FROM users WHERE chat_id = %s',
        (chat_id,)
    )
    result = cursor.fetchone()

    if result is None:
        conn.close()
        return []

    user_id = result[0]

    cursor.execute(
        'SELECT symbol FROM coins WHERE user_id = %s',
        (user_id,)
    )

    coins = cursor.fetchall()

    conn.close()

    return [coin[0] for coin in coins]