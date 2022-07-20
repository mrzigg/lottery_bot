from aiogram.types import InlineKeyboardMarkup, KeyboardButton


participation = KeyboardButton(text="Участвовать в розыгрыше🔥", callback_data="participation")
Participation_Menu = InlineKeyboardMarkup(row_width=1).add(participation)

subscription1 = KeyboardButton(text="Да, давай исправим😀", callback_data="lets_fix")
Subscription_Menu1 = InlineKeyboardMarkup(row_width=1).add(subscription1)

subscription = KeyboardButton(text="Подписаться✅", url="https://t.me/TELEGIV_TEST") 
check_subscription = KeyboardButton(text="Проверить подписку🔎", callback_data="check_subscription")
Subscription_Menu = InlineKeyboardMarkup(row_width=1).add(subscription, check_subscription)

check_in = KeyboardButton("🔎Проверить подписку", callback_data="check_in")
Subscription_Menu_2 = InlineKeyboardMarkup(row_width=1).add(subscription, check_in)

Subscription_Menu_3 = InlineKeyboardMarkup(row_width=1).add(subscription)