from aiogram import types

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = types.KeyboardButton("🎫 Мои билеты")
button_2 = types.KeyboardButton("⏰ Когда закончится розыгрыш")
button_3 = types.KeyboardButton("🎁 Бонусные билеты")

keyboard.add(button_1).add(button_2).add(button_3)