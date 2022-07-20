from aiogram.types import InlineKeyboardMarkup, KeyboardButton


button_1 = KeyboardButton("до 18", callback_data="age_18")
button_2 = KeyboardButton("18-24", callback_data="age_18_24")
button_3 = KeyboardButton("25-34", callback_data="age_25_34")
button_4 = KeyboardButton("35-44", callback_data="age_35_44")
button_5 = KeyboardButton("45+", callback_data="age_45")
age_board = InlineKeyboardMarkup(row_width=1).add(button_1, button_2, button_3, button_4, button_5)