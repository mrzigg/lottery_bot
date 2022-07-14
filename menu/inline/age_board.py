from aiogram import types

age_board = types.InlineKeyboardMarkup(row_width=1)
button_1 = types.InlineKeyboardButton("до 18", callback_data="age_18")
button_2 = types.InlineKeyboardButton("18-24", callback_data="age_18_24")
button_3 = types.InlineKeyboardButton("25-34", callback_data="age_25_34")
button_4 = types.InlineKeyboardButton("35-44", callback_data="age_35_44")
button_5 = types.InlineKeyboardButton("45+", callback_data="age_45")

age_board.add(button_1, button_2, button_3, button_4, button_5)