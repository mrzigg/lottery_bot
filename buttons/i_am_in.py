from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import dp, bot 
from menu.inline.follower_board import keyboard
import database.users_db as db

@dp.callback_query_handler(text="i_am_in")
async def in_call_back(callback_query: types.CallbackQuery):
    await db.update_button(callback_query.from_user.id, True)
    await bot.send_message(callback_query.from_user.id, "Для участия в розыгрыше <b>подпишись</b> на наш канал\n\nПосле того как ты подпишешься -<b> нажми кнопку</b> “Проверить подписку”\n\n🔎Робот проверит подписку и выдаст лотерейный билет.",
    reply_markup=keyboard)
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)