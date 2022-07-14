from aiogram import types

keyboard = types.InlineKeyboardMarkup()
button_1 = types.InlineKeyboardButton("Я в деле✅", callback_data="i_am_in")
keyboard.add(button_1)