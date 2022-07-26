from aiogram.dispatcher.filters import Command
from datetime import datetime
from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import database.lottery_db as lot_db

from config.load_all import dp
from menu.reply.user_menu import keyboard
from filters.time_filter import TimeFilter
from database.main_data import customer_id, bot_id, raffle_id
from functions.lottery_routin import LotRoutin

lotrout = LotRoutin()


@dp.message_handler(TimeFilter(), Command("raffle", ignore_caption=True))
async def raffle_command(message: types.Message):
    lottery = await lot_db.lottery_exists()
    if not lottery:
        return await message.answer("<b>Розыгрыш уже завершен.</b>\n\nНо мы уже готовым к запуску новый розыгрыш с безумно крутыми призами!\n\nНужно чуть-чуть подождать 🎁\n\nСовсем чуть-чуть ☺️",
        reply_markup=types.ReplyKeyboardRemove())
    else:
        lotrout.lottery_message(lottery=lottery)
        try:
            photo = f"https://go.telegiv.com/static/images/draws/{customer_id}.{bot_id}.{raffle_id}.jpeg"
            return await message.answer_photo(photo, f"<b>{lottery[8]} 🔥</b>\n\n<b>Главные призы розыгрыша:\n{lotrout.main_prize}</b>\n\n<b>Описание розыгрыша 📝</b>\n{lottery[4]}\n\n<b>Дата окончания розыгрыша {datetime.strftime(lottery[7], '%d.%m.%Y в %H:%M')}</b>",
            reply_markup=keyboard)
        except:
            return await message.answer(f"<b>{lottery[8]} 🔥</b>\n\n<b>Главные призы розыгрыша:\n{lotrout.main_prize}</b>\n\n<b>Описание розыгрыша 📝</b>\n{lottery[4]}\n\n<b>Дата окончания розыгрыша {datetime.strftime(lottery[7], '%d.%m.%Y в %H:%M')}</b>",
            reply_markup=keyboard)