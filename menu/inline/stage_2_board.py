from aiogram.types import InlineKeyboardMarkup, KeyboardButton

button = KeyboardButton("Я в деле", callback_data="stage_2_yes")
button_2 = KeyboardButton("Нет, я пас", callback_data="stage_2_no")
stage_2_board = InlineKeyboardMarkup(row_width=2).add(button, button_2)