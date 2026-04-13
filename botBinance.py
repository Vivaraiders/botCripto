import asyncio
from cotarMoedas import cotarMoedas
from datetime import datetime
from telegram import Bot
from os import getenv
from dotenv import load_dotenv
from database import get_connection, add_user, user_chatId

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

users = user_chatId(cursor)
print(users)

#CARREGA .ENV E TRÁS A APIKEY
load_dotenv()

TELEGRAM_APIKEY = getenv("TELEGRAM_APIKEY")

#INSTANCIA O BOT
bot = Bot(token=TELEGRAM_APIKEY)

last_update_id = None  # 

#CRIPTOMOEDAS SELECIONADAS
moedas = {
    'BTC': ['BTCUSDT', 'BTCBRL'], 
    'ETH': ['ETHUSDT', 'ETHBRL'] 
}



async def main():
    global last_update_id
    users = user_chatId(cursor=cursor)

    while True:
        # 
        updates = await bot.get_updates(offset=last_update_id)

        for update in updates:
            if update.message:
                texto = update.message.text
                nome = update.message.from_user.first_name
                chat_id = update.message.chat.id
                

                if chat_id not in users:
                    add_user(conn=conn, cursor=cursor, chat_id=chat_id)
                    users.append(chat_id)
                    print(f'novo usuario adicionado: {nome}: chat_id: {chat_id}')
                

                print(f"Mensagem recebida: {texto}")

                last_update_id = update.update_id + 1  # 

        # 
        agora = datetime.now()
        data_formatada = agora.strftime('%d/%m/%Y %H:%M:%S')

        with open('dadosBinance.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{data_formatada}\n")

            for nome, pares in moedas.items():
                f.write(f"=== {nome} ===\n")

                for par in pares:
                    dados = cotarMoedas(par)

                    if 'price' in dados:
                        price = float(dados['price'])

                        f.write(f"Moeda: {dados['symbol']} valor: R${price:.2f}\n")

                        if par == 'BTCBRL' and price <= 377181:
                            f.write('Hora de comprar BTC!\n')
                            print('Hora de comprar BTC!')

                            for id_chat in users:
                                await bot.send_message(
                                    chat_id=id_chat,
                                    text=f"BTC em {price:.2f} — Hora de comprar!"
                                )

                        if par == 'ETHBRL' and price <= 10975:
                            f.write('Hora de comprar ETH!\n')
                            print('Hora de comprar ETH!')

                            for id_chat in users:
                                await bot.send_message(
                                    chat_id=id_chat,
                                    text=f"ETH em {price:.2f} — Hora de comprar!"
                                )

                        print(dados)

                    else:
                        print(f'erro: {dados}\n')

        await asyncio.sleep(10)

asyncio.run(main())