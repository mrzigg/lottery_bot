from aiogram.types import InlineKeyboardMarkup, KeyboardButton


button_1 = KeyboardButton("Забрать бонус🎁", callback_data="taking_part")
taking_board = InlineKeyboardMarkup(row_width=1).add(button_1)