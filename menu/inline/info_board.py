from aiogram.types import InlineKeyboardMarkup, KeyboardButton

button_1 = KeyboardButton(text="💰 Как будет выбран победитель", callback_data="info_winner")
button_2 = KeyboardButton(text="Какие у меня шансы на победу 📊", callback_data="info_chances")
info_board = InlineKeyboardMarkup(row_width=1).add(button_1, button_2)