from aiogram import types

country_board = types.InlineKeyboardMarkup(row_width=1)
button_1 = types.InlineKeyboardButton("Беларусь🇧🇾", callback_data="country_belarus")
button_2 = types.InlineKeyboardButton("Украина🇺🇦", callback_data="country_ucrain")
button_3 = types.InlineKeyboardButton("Казахстан🇰🇿", callback_data="country_kazakhstan")
button_4 = types.InlineKeyboardButton("Россия🇷🇺", callback_data="country_russia")
button_5 = types.InlineKeyboardButton("Узбекистан🇺🇿", callback_data="country_uzbekistan")
button_6 = types.InlineKeyboardButton("Другая страна", callback_data="counry_any")
country_board.add(button_1, button_2, button_3, button_4, button_5, button_6)