from aiogram import types

gender_board = types.InlineKeyboardMarkup()
button_1 = types.InlineKeyboardButton("Парень🧑", callback_data="gender_male")
button_2 = types.InlineKeyboardButton("Девушка👩‍🦱", callback_data="gender_female")

gender_board.add(button_1, button_2)