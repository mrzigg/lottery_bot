from aiogram.types import InlineKeyboardMarkup, KeyboardButton

#--------КНОПКА ДЛЯ УЧАСТИЯ В РОЗЫГРЫШЕ--------
participation = KeyboardButton(text="Участвовать в розыгрыше🔥", callback_data="participation")
Participation_Menu = InlineKeyboardMarkup(row_width=1).add(participation)

#--------МЕНЮ ДЛЯ ПОДПИСКИ НА КАНАЛ И ПРОВЕРКИ ПОДПИСКИ--------
subscription = KeyboardButton(text="Подписаться✅", url="https://t.me/testtelegiv")
check_subscription = KeyboardButton(text="Проверить подписку🔎", callback_data="check_subscription")
Subscription_Menu = InlineKeyboardMarkup(row_width=1).add(subscription, check_subscription)

#--------ЕСЛИ ЧЕЛОВЕК НЕ НАЖИМАЕТ НА КНОПКУ "ПРОВЕРИТЬ ПОДПИСКУ"--------
subscription1 = KeyboardButton(text="Да, давай исправим😀", callback_data="lets_fix")
Subscription_Menu1 = InlineKeyboardMarkup(row_width=1).add(subscription1)