from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import database.users_db as db
import database.tickets_db as ticket_db

from config.load_all import dp, bot
from functions.message_routins import Routins
from menu.inline.contry_board import country_board


@dp.callback_query_handler(text_startswith="age_")
async def age_callback_data(callback_query: types.CallbackQuery):
    if callback_query.data == "age_18":
        await db.update_age(callback_query.from_user.id, "до 18")
    elif callback_query.data == "age_18_24":
        await db.update_age(callback_query.from_user.id, "18-24")
    elif callback_query.data == "age_25_34":
        await db.update_age(callback_query.from_user.id, "25-34")
    elif callback_query.data == "age_35_44":
        await db.update_age(callback_query.from_user.id, "35-44")
    else:
        await db.update_age(callback_query.from_user.id, "45+")
    await Routins.edit_callback(call=callback_query)
    ticket = await ticket_db.add_user(callback_query.from_user.id)
    text=f"<b>Это наверное самый крутой возраст!</b>\n\nДержи <b>+1</b> лотерейный билет\n🎫 Номер билета: <b>{ticket}</b>\n\nВсего лотерейных билетов: <b>3</b>\n\nУ меня остался последний вопрос - и еще <b>1 </b> лотерейный билет 😌"
    await Routins.edit_call_text(callback_query=callback_query, text=text)
    return await bot.send_message(callback_query.from_user.id, "<b>Из какой ты страны?</b>", reply_markup=country_board)
