from aiogram import types 


button_1 = types.InlineKeyboardButton("Подписаться✅", url="https://t.me/TELEGIV_TEST")
button_2 = types.InlineKeyboardButton("🔎Проверить подписку", callback_data="check_in")
keyboard = types.InlineKeyboardMarkup(row_width=1).add(button_1, button_2)