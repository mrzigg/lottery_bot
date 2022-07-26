from datetime import datetime, timedelta
from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import database.raffle_progresses_db as progres_db

from config.bot_name import link
from filters.time_filter import TimeFilter
from functions.message_routins import Routins
from config.load_all import dp, bot, scheduler
from menu.inline.stage_1_board import extra_tickets_board
from functions.scheduler_second_stage import five_minutes, eight_minutes, eleven_minutes


@dp.callback_query_handler(TimeFilter(), text_contains="stage_1_")
async def taking_bonus_callback(call: types.CallbackQuery):
    await Routins.edit_callback(call=call)
    if call.data == "stage_1_no":
        return await bot.send_message(call.from_user.id, "<b>Это разумно</b> 😀\nЛотерейные билеты можно заработать и без риска)", reply_markup=extra_tickets_board)
    elif call.data == "stage_1_extra":
        text = f"<b> Чтобы получить дополнительные лотерейные билеты - пригласи своих друзей в розыгрыш!</b>\nСсылка для приглашений:\n{link}{call.from_user.id}"
        await Routins.edit_call_text(callback_query=call, text=text)
    else:
        await progres_db.update_function(call.from_user.id, "super_game_stage", 2)
        text = f"<b>Вот это уже интересно!</b>\nДержи ссылку:\n{link}{call.from_user.id}\nПари закончится ровно через <b>10 минут.</b>"
        await Routins.edit_call_text(callback_query=call, text=text)
        scheduler.add_job(five_minutes, "date", run_date=(datetime.now()+timedelta(minutes=5)), args=(call.from_user.id,))
        scheduler.add_job(eight_minutes, "date", run_date=(datetime.now()+timedelta(minutes=8)), args=(call.from_user.id,))
        scheduler.add_job(eleven_minutes, "date", run_date=(datetime.now()+timedelta(minutes=11)), args=(call.from_user.id,))