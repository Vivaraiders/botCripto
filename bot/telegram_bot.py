from database.users import add_user
from services.cotarMoedas import cotarMoedas

async def process_updates(bot, updates, users, conn, cursor): 
    global last_update_id
    for update in updates:
        last_update_id = update.update_id + 1
        if update.message:
            texto = update.message.text
            nome = update.message.from_user.first_name
            chat_id = update.message.chat.id
                

            if chat_id not in users:
                add_user(conn=conn, cursor=cursor, chat_id=chat_id)
                users.append(chat_id)
                print(f'novo usuario adicionado: {nome}')

            # if texto.isupper() and 'BRL' in texto and texto not in moedas:
            dados = cotarMoedas(texto)
            
            
            if 'code' in dados:
                await bot.send_message(
                    chat_id=chat_id,
                    text=f'Moeda inválida: {texto}'
                )
            else:
                await bot.send_message(
                    chat_id=chat_id,
                    text=f'Moeda adicionada: {texto}'
                )
                    # moedas.append(texto)
                