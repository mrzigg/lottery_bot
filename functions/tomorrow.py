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
from menu.inline.take_prize import taking_board_3


async def invite_message_tomorrow(user_id, invites):
    await ticket_db.add_tickets(user_id, invites+2)
    tickets = await ticket_db.get_tickets(user_id)
    super_game_invites = await progres_db.get_function(user_id, "super_game_invites") + 1
    await progres_db.update_function(user_id, "super_game_invites", super_game_invites)
    if super_game_invites < 5:
        return await bot.send_message(user_id, f"<b>Бонус за приглашение!</b>\n\n+1 друг в розыгрыше 🥳\nЗа это ты получаешь <b>{invites+2}</b> 🎫\nТеперь у тебя их <b>{tickets}</b>\n\n<b> До умножения билетов в Х2 осталось всего {5-super_game_invites} приглашения </b>\n\nСсылка для приглашений:\n{link}{user_id}", disable_web_page_preview=True) 
    else:
        await ticket_db.add_tickets(user_id, tickets*2)
        await progres_db.update_super_game(user_id, 0, 0)
        return await bot.send_message(user_id, f"<b>Воу, это же Х2!</b>\n\nУ тебя было <b>{tickets}</b> 🎫\nСейчас у тебя <b>{tickets*2}</b> 🎫\n\nЭто больше чем у 92% участников розыгрыша!\n<b>Хочешь ещё увеличить свои шансы на победу? </b>\n\nСсылка для приглашений:\n{link}{user_id}", disable_web_page_preview=True)
       

async def sending_message_tomorrow():
    users = await db.all_users()
    for row in users:
        days = await progres_db.get_function(int(row[0]), "daily_bonus_duration")
        await bot.send_message(int(row[0]), f"<b>Ежедневный бонус 🎁</b>\n\nТебе начислено <b>{days*5}</b> лотерейных билетов.\n\n✅ Забирай бонус каждый день и он будет расти на <b>+5</b> лотерейных билетов ежедневно)\n\n⏰ Бонус активен до 24:00",
        reply_markup=taking_board_3)


@dp.callback_query_handler(TimeFilter(), text="taking_part_tomorrow")
async def taking_bonus_callback(call: types.CallbackQuery):
    await Routins.edit_callback(call=call)
    info = await progres_db.get_row_function(call.from_user.id, "daily_bonus_duration, super_game_duration")
    days, duration = info[0], (info[1] + 1)
    await ticket_db.add_tickets(call.from_user.id, days*5)
    tickets = await ticket_db.get_tickets(call.from_user.id)
    text = f"<b> Бонус получен!</b>\n\nТеперь у тебя <b>{tickets}</b> лотерейных билетов.\n\nЧтобы размер бонуса увеличивался - забирай его каждый день."
    await Routins.edit_call_text(callback_query=call, text=text)
    await asyncio.sleep(3)
    await bot.send_message(call.from_user.id, f"<b>Завтра станет ясно кто же окажется  победителем.</b>\n\nА сегодня ты сможешь умножить количество своих лотерейных билетов в 2 раза.\nЕсли хочешь умножить свои шансы на победу в 2 раза и получить <b>{tickets}</b> лотерейных билетов\n\nПригласи за сегодня в розыгрыш 5 друзей.\n\nСсылка для приглашений:\n{link}{call.from_user.id}", disable_web_page_preview=True)
    await progres_db.update_function(call.from_user.id, "super_game_stage", 6)
    await progres_db.update_function(call.from_user.id, "super_game_duration", duration)