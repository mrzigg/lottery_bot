from aiogram import types

button = types.InlineKeyboardButton("Подписать на канал✅", url="https://t.me/TELEGIV_TEST")
keyboard = types.InlineKeyboardMarkup(row_width=1).add(button)