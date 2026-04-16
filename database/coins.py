from database.database import get_connection

conn = get_connection()

if conn is None:
    print("Sem conexão com banco (arquivo coin)")
    cursor = None
else:
    cursor = conn.cursor()

def add_coin(chat_id, symbol):
    cursor.execute('SELECT id FROM users WHERE chat_id = %s',
    (chat_id,)
    )
    result = cursor.fetchone()

    if result is None:
        return result
    
    user_id = result[0]

    cursor.execute(
        'INSERT IGNORE INTO coins(user_id, symbol) VALUES (%s, %s)'
    , (user_id, symbol)
    )
    conn.commit()
    return user_id
        
def find_user_coin(chat_id):
    cursor.execute('SELECT id FROM users WHERE chat_id = %s',
    (chat_id,)
    )
    result = cursor.fetchone()

    if result is None:
        return result
    
    user_id = result[0]

    cursor.execute(
        'SELECT symbol FROM coins WHERE user_id = %s',
        (user_id,)
    )

    coins = cursor.fetchall()

    return [coin[0] for coin in coins]