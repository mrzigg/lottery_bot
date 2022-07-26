from aiogram.types import InlineKeyboardMarkup, KeyboardButton

button = KeyboardButton("Я в деле✅", callback_data="stage_1_yes")
button_2 = KeyboardButton("Я не хочу рисковать❌", callback_data="stage_1_no")
stage_board = InlineKeyboardMarkup(row_width=2).add(button, button_2)

button_3 = KeyboardButton("Получить дополнительные билеты", callback_data="stage_1_extra")
extra_tickets_board = InlineKeyboardMarkup(row_width=1).add(button_3)