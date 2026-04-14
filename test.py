from database.coins import add_coin, find_user_coin

chat_id = 6084699453

# add_coin(chat_id, "BTCBRL")
# add_coin(chat_id, 'ETHBRL')

user = find_user_coin(6084699453)

print(user)
