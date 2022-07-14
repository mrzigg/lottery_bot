from aiogram import types
import asyncio

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import dp, bot
from filters.private_filter import PrivateFilter
from functions.make_ticket import Ticket
import database.tickets_db as ticket_db
import database.users_db as db
from menu.inline.contry_board import country_board

tg = Ticket()

@dp.callback_query_handler(PrivateFilter(), text_contains="age_")
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
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    ticket = await ticket_db.get_tickets(callback_query.from_user.id)
    tg.make_ticket_prime(callback_query.from_user.id)
    ticket.append(tg.password)
    await ticket_db.update_function(callback_query.from_user.id, ticket, "tickets")
    await bot.send_message(callback_query.from_user.id, f"<b>Это наверное самый крутой возраст!</b>\n\nДержи <b>+1</b> лотерейный билет\n🎫 Номера билетов: <b>{tg.password}</b>\n\nВсего лотерейных билетов: <b>3</b>\n\nУ меня остался последний вопрос - и еще <b>1 </b> лотерейный билет😌")
    await asyncio.sleep(3)
    await bot.send_message(callback_query.from_user.id, "<b>Из какой ты страны?</b>", reply_markup=country_board)