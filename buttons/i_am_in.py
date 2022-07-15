from aiogram import types
from datetime import datetime, timedelta

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from functions.check import Checking
from config.load_all import dp, bot, scheduler
from menu.inline.follower_board import keyboard
from menu.inline.gender_board import gender_board
from menu.inline.check_follow_board import *
import database.users_db as db
import database.lottery_db as lot_db
import database.tickets_db as ticket_db
from functions.make_ticket import Ticket
from filters.private_filter import PrivateFilter


check = Checking()
tg = Ticket()


@dp.callback_query_handler(text="i_am_in")
async def in_call_back(callback_query: types.CallbackQuery):
    await db.update_button(callback_query.from_user.id, True)
    await bot.send_message(callback_query.from_user.id, "Для участия в розыгрыше <b>подпишись</b> на наш канал\n\nПосле того как ты подпишешься -<b> нажми кнопку</b> “Проверить подписку”\n\n🔎Робот проверит подписку и выдаст лотерейный билет.",
    reply_markup=keyboard)
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    
    lottery = await lot_db.lottery_exists()
    finish_date = lottery[7]
    prize = str(lottery[3])

    if (datetime.now() + timedelta(minutes=30)) < finish_date:
        scheduler.add_job(check.thirty_minutes, "date", run_date=(datetime.now() + timedelta(minutes=30)), args=(callback_query.from_user.id,))
    if (datetime.now() + timedelta(hours=2)) < finish_date:    
        scheduler.add_job(check.two_hours, "date", run_date=(datetime.now() + timedelta(hours=2)), args=(callback_query.from_user.id,))
        
    scheduler.add_job(check.three_days, "date", run_date=(finish_date - timedelta(days=3)), args=(callback_query.from_user.id, prize,))
    scheduler.add_job(check.today, "date", run_date=(finish_date - timedelta(hours=24)), args=(callback_query.from_user.id, prize,))


@dp.callback_query_handler(text="lets_fix")
async def Lets_fix(call: types.CallbackQuery):    
    await bot.send_message(call.from_user.id, 'Для участия в розыгрыше <b>подпишись</b> на наш канал:\n👉 https://t.me/testtelegiv\n\nПосле того как ты подпишешься - <b> нажми кнопку</b> “Проверить подписку”\n\n🔎Робот проверит подписку и выдаст лотерейный билет.', reply_markup=keyboard,
    disable_web_page_preview=True)
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text="participation")
async def Participation(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Для участия в розыгрыше <b>подпишись</b> на наш канал:\n👉 https://t.me/testtelegiv\n\nПосле того как ты подпишешься - <b> нажми кнопку</b> “Проверить подписку”\n\n🔎Робот проверит подписку и выдаст лотерейный билет.', reply_markup=Subscription_Menu,
    disable_web_page_preview=True)
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(PrivateFilter(), text="check_subscription")
async def Check_subscription(call: types.CallbackQuery):
    await db.update_button_2(call.from_user.id)
    ticket = await ticket_db.get_tickets(call.from_user.id)
    ticket_sp = list()
    for i in range(10):
        tg.make_ticket_prime(call.from_user.id)
        ticket.append(tg.password)
        ticket_sp.append(str(tg.password))
    await ticket_db.update_function(call.from_user.id, ticket, "tickets")
    ticket_sp = ", ".join(ticket_sp)
    await bot.send_message(call.message.chat.id, f"<b>Робот всё проверил - всё отлично)</b>\n\nТеперь ты участник розыгрыша!\n\nКак мы и обещали ты получаешь вместо 1 лотерейного билета целых 10 штук)\n\n🎫 Номера твоих лотерейных билетов:{ticket_sp}")
    await bot.send_message(call.from_user.id, "Кстати, ты можешь получить <b>+1 лотерейный билет!</b>\n\n<b>Просто ответь на вопрос:</b> Ты парень или девушка?\n\n<i>P.S.Твои ответы позволят нам понять, как в следующий раз сделать розыгрыш еще интереснее)</i>",
    reply_markup=gender_board)
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)