
from services.market_data import get_data
from database.coins import find_user_coin
from datetime import datetime


async def alert_hours(bot, user, coin, opened_formatado, price_formatado, low_formatado, high_formatado, change, alertas_enviados):
    h = datetime.now()
    hora = h.strftime("%H:%M")
    key = f'{user}_{coin}_{hora}_daily'

  
    if hora in ["12:00", "18:00", "21:00"]:
         if key not in alertas_enviados:
            await bot.send_message(
                chat_id=user,
                text=f'-------- moeda: {coin} --------\npreço de ABERTURA: R${opened_formatado} \npreço de AGORA: R${price_formatado} \npreço mais BAIXO: R${low_formatado} \npreço mais ALTO: R${high_formatado} \nVariação do Dia: {change}%'
            )
            alertas_enviados.add(key)
     
async def check_alert(bot, users, alertas_enviados, alerta_down, alerta_high):
    for user in users:
        coins = find_user_coin(user)

        

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
                await alert_down(bot, user, change, coin, opened_formatado, price_formatado, alerta_down)
                await alert_high(bot, user, change, coin, opened_formatado, price_formatado, alerta_high)


async def alert_down(bot, user, change, coin, opened, price, alerta_down):
    nivel = None

    if change <= -3:
        nivel = -3
    elif change <= -2:
        nivel = -2
    elif change <= -1:
        nivel = -1

    if nivel is not None:
        key = f'{user}_{coin}_{nivel}_daily'

        if key not in alerta_down:
            await bot.send_message(
                chat_id=user,
                text=f'A moeda: {coin} está caindo {change}% \nValor de abertura:{opened}\nValor de agora:{price}'
            )
            alerta_down.add(key)


async def alert_high(bot, user, change, coin, opened, price, alerta_high):
    change = float(change)

    if change >= 1:
        nivel = int(change)

        key = f'{user}_{coin}_{nivel}_daily'

        if key not in alerta_high:
            await bot.send_message(
                chat_id=user,
                text=f'A moeda: {coin} está subindo {change:.2f}% \nValor de abertura:{opened}\nValor de agora:{price}'
            )
            alerta_high.add(key)