from aiogram.types import InlineKeyboardMarkup, KeyboardButton


participation = KeyboardButton("Участвовать в розыгрыше🔥", callback_data="participation")
Participation_Menu = InlineKeyboardMarkup(row_width=1).add(participation)

subscription1 = KeyboardButton("Да, давай исправим😀", callback_data="lets_fix")
Subscription_Menu1 = InlineKeyboardMarkup(row_width=1).add(subscription1)

check_subscription = KeyboardButton("Проверить подписку🔎", callback_data="check_subscription")
Subscription_Menu = InlineKeyboardMarkup(row_width=1).add(check_subscription)

check_in = KeyboardButton("🔎Проверить подписку", callback_data="check_in")
Subscription_Menu_2 = InlineKeyboardMarkup(row_width=1).add(check_in)