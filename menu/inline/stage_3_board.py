from aiogram.types import InlineKeyboardMarkup, KeyboardButton

button = KeyboardButton("Да", callback_data="stage_3_yes")
button_2 = KeyboardButton("Нет", callback_data="stage_3_no")
stage_3_board = InlineKeyboardMarkup(row_width=2).add(button, button_2)

button_3 = KeyboardButton("Я в деле", callback_data="stage_3_proof_yes")
stage_3_board_proof = InlineKeyboardMarkup(row_width=2).add(button_3, button_2)