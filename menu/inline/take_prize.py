from aiogram.types import InlineKeyboardMarkup, KeyboardButton


button_1 = KeyboardButton("Забрать бонус🎁", callback_data="taking_part")
taking_board = InlineKeyboardMarkup(row_width=1).add(button_1)

button_2 = KeyboardButton("Забрать бонус🎁", callback_data="taking_part_three_days")
taking_board_2 = InlineKeyboardMarkup(row_width=1).add(button_2)

button_3 = KeyboardButton("Забрать бонус🎁", callback_data="taking_part_tomorrow")
taking_board_3 = InlineKeyboardMarkup(row_width=1).add(button_3)

button_4 = KeyboardButton("Забрать бонус🎁", callback_data="taking_part_today")
taking_board_4 = InlineKeyboardMarkup(row_width=1).add(button_4)