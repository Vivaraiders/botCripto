
from services.merket_data import get_data
from database.coins import find_user_coin

# alert_open = 



async def check_alert(users, bot):
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

                await bot.send_message(
                chat_id=user,
                text=f'-------- moeda: {coin} --------\npreço de ABERTURA: {opened_formatado} \npreço de AGORA: R${price_formatado} \npreço mais BAIXO: {low_formatado} \npreço mais ALTO: R${high_formatado} \nVariação do Dia: {change}%'
                )
