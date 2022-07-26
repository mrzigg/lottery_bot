from aiogram.types import InlineKeyboardMarkup, KeyboardButton


button_1 = KeyboardButton("Я в деле ✅", callback_data="i_am_in")
play_board = InlineKeyboardMarkup(row_width=1).add(button_1)