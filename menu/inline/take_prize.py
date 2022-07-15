from aiogram import types

taking_board = types.InlineKeyboardMarkup(row_width=1)
button_1 = types.InlineKeyboardButton("Забрать бонус🎁", callback_data="taking_part")

taking_board.add(button_1)