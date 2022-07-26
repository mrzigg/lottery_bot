from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button = KeyboardButton("Начать🔥")
start_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button)