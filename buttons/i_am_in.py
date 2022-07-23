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
from menu.inline.gender_board import gender_board
from menu.inline.check_follow_board import *
import database.users_db as db
import database.lottery_db as lot_db
from filters.during_sub import DuringSub2
from functions.make_tickets import MakeTickets
from functions.make_links import Channel_link
from functions.message_routins import Routins

func = MakeTickets()
check = Checking()
channel_link = Channel_link()

@dp.callback_query_handler(text="i_am_in")
async def in_call_back(callback_query: types.CallbackQuery):
    await db.update_button(callback_query.from_user.id, True)
    channel_link.make_links()
    await bot.send_message(callback_query.from_user.id, f"Для участия в розыгрыше <b>подпишись</b> на наши каналы:\n\n{channel_link.links}\n\nПосле того как ты подпишешься -<b> нажми кнопку</b> “Проверить подписку”\n\n🔎Робот проверит подписку и выдаст лотерейный билет.",
    reply_markup=Subscription_Menu_2)
    await Routins().edit_callback(call=callback_query)
    
    lottery = await lot_db.lottery_exists()
    finish_date = lottery[7]

    if (datetime.now() + timedelta(minutes=30)) < finish_date:
        scheduler.add_job(check.thirty_minutes, "date", run_date=(datetime.now() + timedelta(minutes=30)), args=(callback_query.from_user.id,))
    if (datetime.now() + timedelta(hours=2)) < finish_date:    
        scheduler.add_job(check.two_hours, "date", run_date=(datetime.now() + timedelta(hours=2)), args=(callback_query.from_user.id,))
        
    scheduler.add_job(check.three_days, "date", run_date=(finish_date - timedelta(days=3)), args=(callback_query.from_user.id, str(lottery[3]),))
    scheduler.add_job(check.today, "date", run_date=(finish_date - timedelta(hours=24)), args=(callback_query.from_user.id, str(lottery[3]),))


@dp.callback_query_handler(text="lets_fix")
async def Lets_fix(call: types.CallbackQuery):
    channel_link.make_links()
    await bot.send_message(call.from_user.id, f'Для участия в розыгрыше <b>подпишись</b> на наш канал:\n{channel_link.links}\n\nПосле того как ты подпишешься - <b> нажми кнопку</b> “Проверить подписку”\n\n🔎Робот проверит подписку и выдаст лотерейный билет.', reply_markup=Subscription_Menu_2)
    await Routins().edit_callback(call=call)


@dp.callback_query_handler(text="participation")
async def Participation(call: types.CallbackQuery):
    channel_link.make_links()
    await bot.send_message(call.from_user.id, f'Для участия в розыгрыше <b>подпишись</b> на наш канал:\n{channel_link.links}\n\nПосле того как ты подпишешься - <b> нажми кнопку</b> “Проверить подписку”\n\n🔎Робот проверит подписку и выдаст лотерейный билет.', reply_markup=Subscription_Menu)
    await Routins().edit_callback(call=call)


@dp.callback_query_handler(DuringSub2(), text="check_subscription")
async def Check_subscription(call: types.CallbackQuery):
    await db.update_button_2(call.from_user.id)
    await func.make_ten_tickets(call.from_user.id)
    await bot.send_message(call.message.chat.id, f"<b>Робот всё проверил - всё отлично)</b>\n\nТеперь ты участник розыгрыша!\n\nКак мы и обещали ты получаешь вместо 1 лотерейного билета целых 10 штук)\n\n🎫 Номера твоих лотерейных билетов:{func.id_list}")
    await bot.send_message(call.from_user.id, "Кстати, ты можешь получить <b>+1 лотерейный билет!</b>\n\n<b>Просто ответь на вопрос:</b> Ты парень или девушка?\n\n<i>P.S.Твои ответы позволят нам понять, как в следующий раз сделать розыгрыш еще интереснее)</i>",
    reply_markup=gender_board)
    await Routins().edit_callback(call=call)