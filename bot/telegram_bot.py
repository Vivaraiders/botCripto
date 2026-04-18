from database.users import add_user
from services.cotarMoedas import cotarMoedas
from database.coins import add_coin, find_user_coin




async def process_updates(bot, updates, users, conn, cursor): 
    global last_update_id
    for update in updates:
        last_update_id = update.update_id + 1
        if update.message:
            texto = update.message.text
            nome = update.message.from_user.first_name
            chat_id = update.message.chat.id
            user_coins = find_user_coin(chat_id)

            if chat_id not in users:
                add_user(conn=conn, cursor=cursor, chat_id=chat_id)
                users.append(chat_id)
                print(f'novo usuario adicionado: {nome}')

            texto = texto.upper()
            if not texto.endswith('BRL'):
                texto = f'{texto}BRL'

            if texto in user_coins:
                
                    await bot.send_message(
                        chat_id=chat_id,
                        text=f'Moeda {texto} já está cadastrada'
                    )
                    return
            
            dados = cotarMoedas(texto)

            
            if not dados or 'code' in dados:
                await bot.send_message(
                    chat_id=chat_id,
                    text=f'Moeda inválida: {texto}'
                )

            else:
                add_coin(chat_id, texto)

                await bot.send_message(
                    chat_id=chat_id,
                     text=f'Moeda adicionada: {texto}'
                 )


