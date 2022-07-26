from aiogram import types
import asyncio

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import database.users_db as db
import database.tickets_db as ticket_db
import database.raffle_progresses_db as progres_db

from config.bot_name import link
from config.load_all import bot, dp
from filters.time_filter import TimeFilter
from functions.message_routins import Routins 
from menu.inline.take_prize import taking_board_2


async def invite_message(user_id, invites):
    await ticket_db.add_tickets(user_id, ((invites+2)*3))
    tickets = await ticket_db.get_tickets(user_id)
    await progres_db.update_function(user_id, "super_game_stage", 0)
    return await bot.send_message(user_id, f"<b>Бонус за приглашение!</b>\n\n+1 друг в розыгрыше🥳\nЗа это ты получаешь <b>{(invites+2)*3}</b> 🎫\n\nТеперь у тебя {tickets} 🎫\n<b>За следующего друга ты получишь +{invites+4} 🎫</b>\n\nСсылка для приглашений:\n{link}{user_id}") 
    

async def sending_message_three_days():
    users = await db.all_users()
    for row in users:
        days = await progres_db.get_function(int(row[0]), "daily_bonus_duration")
        await bot.send_message(int(row[0]), f"<b>Ежедневный бонус 🎁</b>\n\nТебе начислено <b>{days*5}</b> лотерейных билетов.\n\n✅ Забирай бонус каждый день и он будет расти на <b>+5</b> лотерейных билетов ежедневно)\n\n⏰ Бонус активен до 24:00",
        reply_markup=taking_board_2)


@dp.callback_query_handler(TimeFilter(), text="taking_part_three_days")
async def taking_bonus_callback(call: types.CallbackQuery):
    await Routins.edit_callback(call=call)
    info = await progres_db.get_row_function(call.from_user.id, "daily_bonus_duration, super_game_duration, invites")
    days, duration, invites = info[0], (info[1] + 1), info[2]
    await ticket_db.add_tickets(call.from_user.id, days*5)
    tickets = await ticket_db.get_tickets(call.from_user.id)
    text = f"<b> Бонус получен!</b>\n\nТеперь у тебя <b>{tickets}</b> лотерейных билетов.\n\nЧтобы размер бонуса увеличивался - забирай его каждый день."
    await Routins.edit_call_text(callback_query=call, text=text)
    await asyncio.sleep(3)
    await bot.send_message(call.from_user.id, f"<b>До окончания розыгрыша осталось 3 дня.</b>\n\nПо этому поводу, сегодня за каждое приглашение - <u>ты получишь в 3 раза больше</u> лотерейных билетов, чем обычно!\n\n<b>Давай увеличим шансы на победу:</b>\n\n<b>+{(invites+2)*3}</b> лотерейных билетов ждет тебя за <b>1</b> приглашение!\n\nСсылка для приглашений:\n{link}{call.from_user.id}", disable_web_page_preview=True)
    await progres_db.update_function(call.from_user.id, "super_game_stage", 5)
    await progres_db.update_function(call.from_user.id, "super_game_duration", duration)