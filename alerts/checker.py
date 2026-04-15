
from services.market_data import get_data
from database.coins import find_user_coin
from datetime import datetime


async def alert_hours(bot, user, coin, opened_formatado, price_formatado, low_formatado, high_formatado, change, alertas_enviados):
    h = datetime.now()
    hora = h.strftime("%H:%M")
    key = f'{user}_{coin}_{hora}_daily'

    if hora in ["09:00", "15:00", "18:00"]:
         if key not in alertas_enviados:
            await bot.send_message(
                chat_id=user,
                text=f'-------- moeda: {coin} --------\npreço de ABERTURA: R${opened_formatado} \npreço de AGORA: R${price_formatado} \npreço mais BAIXO: R${low_formatado} \npreço mais ALTO: R${high_formatado} \nVariação do Dia: {change}%'
            )
            alertas_enviados.add(key)
     
async def check_alert(bot, users, alertas_enviados):
    for user in users:
        coins = find_user_coin(user)

        print("RAW:", coins)

        for coin in coins:
            dados = get_data(coin)
        
            if 'open' in dados:
                opened = float(dados['open'])
                opened_formatado = f'{opened:,.2f}'.replace(",","X").replace(".",",").replace("X",".")

                price= float(dados['last'])
                price_formatado = f'{price:,.2f}'.replace(",","X").replace(".",",").replace("X",".")

                high = float(dados['high'])
                high_formatado = f'{high:,.2f}'.replace(",","X").replace(".",",").replace("X",".")

                low = float(dados['low'])
                low_formatado = f'{low:,.2f}'.replace(",","X").replace(".",",").replace("X",".")

                change = float(dados['change'])

                await alert_hours(bot, user, coin, opened_formatado, price_formatado, low_formatado,high_formatado,change, alertas_enviados)
