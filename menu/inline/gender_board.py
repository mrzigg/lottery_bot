from aiogram.types import InlineKeyboardMarkup, KeyboardButton


button_1 = KeyboardButton("Парень🧑", callback_data="gender_male")
button_2 = KeyboardButton("Девушка👩‍🦱", callback_data="gender_female")
gender_board = InlineKeyboardMarkup(row_width=1).add(button_1, button_2)