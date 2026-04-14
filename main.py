import asyncio
from services.cotarMoedas import cotarMoedas
from telegram import Bot
from os import getenv
from dotenv import load_dotenv
from database.database import get_connection
from database.users import add_user, get_user_chatId
from services.merket_data import get_data
from alerts.checker import check_alert
from bot.telegram_bot import process_updates


#CONEXÃO COM BANCO DE DADOS
try:
    conn = get_connection()
    cursor = conn.cursor()

    if conn is None:
        print('Sem conexão com banco, fechando projeto')
        exit()    

except Exception as e:
    print(f'conexão com banco falhou!\nconexão com banco falhou: {e}')
    conn = None
    cursor = None




#CARREGA .ENV E TRÁS A APIKEY
load_dotenv()
TELEGRAM_APIKEY = getenv("TELEGRAM_APIKEY")

#INSTANCIA O BOT
bot = Bot(token=TELEGRAM_APIKEY)

#
last_update_id = None  # 

#Onde salva os alertas
alertas_enviados = set()


async def main():
    global last_update_id
    
    while True:
        users = get_user_chatId(cursor=cursor)
        updates = await bot.get_updates(offset=last_update_id)

        if updates:
            last_update_id = updates[-1].update_id + 1

        await process_updates(bot, updates, users, conn, cursor)
        await check_alert(users, bot)
        
        await asyncio.sleep(10)

asyncio.run(main())