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
from menu.inline.gender_board import gender_board
from menu.inline.age_board import age_board

tg = Ticket()

@dp.callback_query_handler(PrivateFilter(), text="check_in")
async def callback_check_in(callback_query: types.CallbackQuery):
    ticket = await ticket_db.get_tickets(callback_query.from_user.id)
    await db.update_button_2(callback_query.from_user.id)
    tg.make_ticket_prime(callback_query.from_user.id)
    ticket.append(tg.password)
    await ticket_db.update_function(callback_query.from_user.id, ticket, "tickets")
    await bot.send_message(callback_query.from_user.id, f"<b>Отлично!</b>\nРобот всё проверил - всё отлично)\n\n<b>Теперь ты участник розыгрыша!</b>\n\n🎫 Номер лотерейного билета: <b>{tg.password}</b>", reply_markup=types.ReplyKeyboardRemove())
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await asyncio.sleep(3)
    await bot.send_message(callback_query.from_user.id, "Кстати, ты можешь получить <b>+1 лотерейный билет!</b>\n\n<b>Просто ответь на вопрос:</b> Ты парень или девушка?\n\n<i>P.S.Твои ответы позволят нам понять, как в следующий раз сделать розыгрыш еще интереснее)</i>",
    reply_markup=gender_board)


@dp.callback_query_handler(PrivateFilter(), text_contains="gender_")
async def gender_message(callback_query: types.CallbackQuery):
    if callback_query.data == "gender_male":
        await db.update_gender(callback_query.from_user.id, True)
    else:
        await db.update_gender(callback_query.from_user.id, False)
    ticket = await ticket_db.get_tickets(callback_query.from_user.id)
    tg.make_ticket_prime(callback_query.from_user.id)
    ticket.append(tg.password)
    await ticket_db.update_function(callback_query.from_user.id, ticket, "tickets")
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, f"<b>Воу, это круто ☺️</b>\n\nДержи +1 лотерейный билет\n🎫 Номер:<u> {tg.password} </u>\n\nТеперь у тебя <b>2</b> лотерейных билета.\n\nОтветь на вопрос - получи еще <b>+1</b>.")
    await asyncio.sleep(3)
    await bot.send_message(callback_query.from_user.id, "<b>Сколько тебе лет?</b>", reply_markup=age_board)