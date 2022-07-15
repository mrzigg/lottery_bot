from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import bot, dp 
import database.users_db as db
import database.tickets_db as ticket_db
from menu.inline.take_prize import taking_board
from filters.private_filter import PrivateFilter
from functions.make_ticket import Ticket

tg = Ticket()

async def sending_message():
    users = await db.all_users()
    for row in users:
        tickets = len(await ticket_db.get_tickets(int(row[0])))
        await bot.send_message(int(row[0]), f"<b>Ежедневный бонус 🎁</b>\n\nТебе начислено <b>{tickets}+5</b> лотерейных билетов.\n\n✅ Забирай бонус каждый день и он будет расти на <b>+5</b> лотерейных билетов ежедневно)\n\n⏰ Бонус активен до 24:00",
        reply_markup=taking_board)


@dp.callback_query_handler(PrivateFilter(), text="taking_part")
async def taking_bonus_callback(callback_query: types.CallbackQuery):
    ticket = await ticket_db.get_tickets(callback_query.from_user.id)
    for i in range(5):
        tg.make_ticket_prime(callback_query.from_user.id)
        ticket.append(tg.password)
    await ticket_db.update_function(callback_query.from_user.id, ticket, "tickets")
    ticket = await ticket_db.get_tickets(callback_query.from_user.id)
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, f"<b> Бонус получен!</b>\n\nТеперь у тебя <b>{len(ticket)}</b> лотерейных билетов.\n\nЧтобы размер бонуса увеличивался - забирай его каждый день.",
    reply_markup=types.ReplyKeyboardRemove())