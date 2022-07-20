from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_1 = KeyboardButton("🎫 Мои билеты")
button_2 = KeyboardButton("⏰ Когда закончится розыгрыш")
button_3 = KeyboardButton("🎁 Бонусные билеты")
keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1).add(button_2).add(button_3)