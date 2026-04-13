import asyncio
from cotarMoedas import cotarMoedas
from datetime import datetime
from telegram import Bot
from os import getenv
from dotenv import load_dotenv

moedas = {
    'BTC': ['BTCUSDT', 'BTCBRL'], 
    'ETH': ['ETHUSDT', 'ETHBRL'] 
}

load_dotenv()

TELEGRAM_APIKEY = getenv("TELEGRAM_APIKEY")

bot = Bot(token=TELEGRAM_APIKEY)

last_update_id = None  # 

async def main():
    global last_update_id

    while True:
        # 
        updates = await bot.get_updates(offset=last_update_id)

        for update in updates:
            if update.message:
                texto = update.message.text
                chat_id = update.message.chat.id

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
                            print('Hora de comprar!')

                            await bot.send_message(
                                chat_id=chat_id,
                                text=f"BTC em {price:.2f} — Hora de comprar!"
                            )

                        print(dados)

                    else:
                        print(f'erro: {dados}\n')

        await asyncio.sleep(10)

asyncio.run(main())