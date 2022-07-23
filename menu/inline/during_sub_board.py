from aiogram.types import InlineKeyboardMarkup, KeyboardButton

during_sub_board = InlineKeyboardMarkup(row_width=1).add(KeyboardButton(text="Проверить подписку🔎", callback_data="during_sub"))

during_sub_board_2 = InlineKeyboardMarkup(row_width=1).add(KeyboardButton(text="Проверить подписку🔎", callback_data="during_sub_2"))