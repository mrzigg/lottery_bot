from aiogram.types import InlineKeyboardMarkup, KeyboardButton


button_1 = KeyboardButton("Беларусь🇧🇾", callback_data="country_belarus")
button_2 = KeyboardButton("Украина🇺🇦", callback_data="country_ukraine")
button_3 = KeyboardButton("Казахстан🇰🇿", callback_data="country_kazakhstan")
button_4 = KeyboardButton("Россия🇷🇺", callback_data="country_russia")
button_5 = KeyboardButton("Узбекистан🇺🇿", callback_data="country_uzbekistan")
button_6 = KeyboardButton("Другая страна", callback_data="country_any")
country_board = InlineKeyboardMarkup(row_width=1).add(button_1, button_2, button_3, button_4, button_5, button_6)