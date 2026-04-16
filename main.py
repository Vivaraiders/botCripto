import asyncio
from datetime import datetime
from telegram import Bot
from os import getenv
from database.database import get_connection
from database.users import get_user_chatId
from alerts.checker import check_alert
from bot.telegram_bot import process_updates

#CARREGA .ENV E TRÁS A APIKEY

TELEGRAM_APIKEY = getenv("TELEGRAM_APIKEY")

#CONEXÃO COM BANCO DE DADOS
try:
    conn = get_connection()
    cursor = conn.cursor()       

except Exception as e:
    print(f'conexão com banco falhou!\nconexão com banco falhou: {e}')
    conn = None
    cursor = None

if conn is None:
        print('Sem conexão com banco, fechando projeto')
        exit() 

#INSTANCIA O BOT
bot = Bot(token=TELEGRAM_APIKEY)


last_update_id = None  # 

#Onde salva os alertas
alertas_enviados = set()
alertas_down = set()
alertas_high = set()

async def main():
    global last_update_id
    ultimo_reset = None

    while True:
        try:

            h = datetime.now()
            hoje = h.date()

            if ultimo_reset != hoje:
                 alertas_enviados.clear()
                 alertas_down.clear()
                 alertas_high.clear()
                 ultimo_reset = hoje
                 print('Reset Diario feito')

            users = get_user_chatId(cursor=cursor)
            updates = await bot.get_updates(offset=last_update_id)

            if updates:
                last_update_id = updates[-1].update_id + 1

            await process_updates(bot, updates, users, conn, cursor)
            await check_alert(bot, users, alertas_enviados, alertas_down, alertas_high)
        
        except Exception as e:
             print(f"[error loop]: {e}")
        
        await asyncio.sleep(10)

if __name__ == '__main__':
    asyncio.run(main())