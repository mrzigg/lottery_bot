from datetime import datetime, timedelta
from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.bot_name import link
from filters.time_filter import TimeFilter
from functions.message_routins import Routins
from config.load_all import dp, bot, scheduler
import database.raffle_progresses_db as progres_db
from menu.inline.stage_1_board import extra_tickets_board
from functions.scheduler_third_stage import five_minutes, eight_minutes, eleven_minutes


@dp.callback_query_handler(TimeFilter(), text_contains="stage_2_")
async def taking_bonus_callback(call: types.CallbackQuery):
    await Routins.edit_callback(call=call)
    if call.data == "stage_2_no":
        return await bot.send_message(call.from_user.id, f"<b>Это разумно 😀</b>\nЛотерейные билеты можно заработать и без риска)", reply_markup=extra_tickets_board)
    else:
        await progres_db.update_function(call.from_user.id, "super_game_stage", 3)
        duration = await progres_db.get_function(call.from_user.id, "super_game_duration")
        text = f"<b>Ну что ж... Супер-игре быть!\n</b>⏰ 10 минут пошли.\nНа кону <b>{duration*40}</b> лотерейных билетов за <b>{duration*2}</b> человек.\n\nСсылка для приглашений:\n{link}{call.from_user.id}"
        await Routins.edit_call_text(callback_query=call, text=text)
        scheduler.add_job(five_minutes, "date", run_date=(datetime.now()+timedelta(minutes=5)), args=(call.from_user.id,))
        scheduler.add_job(eight_minutes, "date", run_date=(datetime.now()+timedelta(minutes=8)), args=(call.from_user.id,))
        scheduler.add_job(eleven_minutes, "date", run_date=(datetime.now()+timedelta(minutes=11)), args=(call.from_user.id,))