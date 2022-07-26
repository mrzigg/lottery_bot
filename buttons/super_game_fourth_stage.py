from datetime import datetime, timedelta
from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import database.raffle_progresses_db as progres_db

from filters.time_filter import TimeFilter
from functions.message_routins import Routins
from config.load_all import dp, bot, scheduler
from menu.inline.stage_3_board import stage_3_board_proof
from functions.scheduler_fourth_stage import five_minutes, thirty_minutes, fifty_minutes, sixty_one_minutes


@dp.callback_query_handler(TimeFilter(), text_contains="stage_3_")
async def taking_bonus_callback(call: types.CallbackQuery):
    await Routins.edit_callback(call=call)
    if call.data == "stage_3_no":
        text = f"b>Это правильно 😅</b>\nАзарт это хорошо, но иногда стоит вовремя остановиться))"
        return await Routins.edit_call_text(callback_query=call, text=text)
    elif call.data == "stage_3_yes":
        return await bot.send_message(call.from_user.id, f'<b>Ты точно уверен?)</b>\nНажав на кнопку <b>"Я в деле"</b> ты или выиграешь <b>500</b> лотерейных билетов или проиграешь <b>250</b>.\nТы в себе уверен?\nТы в деле?', reply_markup=stage_3_board_proof)
    else:
        await progres_db.update_function(call.from_user.id, "super_game_stage", 4)
        scheduler.add_job(five_minutes, "date", run_date=(datetime.now()+timedelta(minutes=5)), args=(call.from_user.id,))
        scheduler.add_job(thirty_minutes, "date", run_date=(datetime.now()+timedelta(minutes=30)), args=(call.from_user.id,))
        scheduler.add_job(fifty_minutes, "date", run_date=(datetime.now()+timedelta(minutes=50)), args=(call.from_user.id,))
        scheduler.add_job(sixty_one_minutes, "date", run_date=(datetime.now()+timedelta(minutes=61)), args=(call.from_user.id,))