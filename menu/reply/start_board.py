from aiogram import types

start_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button = types.KeyboardButton("Начать🔥")
start_menu.add(button)