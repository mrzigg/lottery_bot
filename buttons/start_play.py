from datetime import datetime, timedelta
from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import database.users_db as db
import database.lottery_db as lot_db

from menu.inline.play_board import play_board
from config.load_all import dp, bot, scheduler
from functions.lottery_routin import LotRoutin
from database.main_data import customer_id, bot_id, raffle_id
from menu.inline.check_follow_board import Subscription_Menu_2

lotrout = LotRoutin()


@dp.message_handler(text="Начать🔥")
async def start_play_message(message: types.Message):
    lottery = await lot_db.lottery_exists()
    if not lottery:
        return await message.answer("<b>Розыгрыш уже завершен.</b>\n\nНо мы уже готовым к запуску новый розыгрыш с безумно крутыми призами!\n\nНужно чуть-чуть подождать 🎁\n\nСовсем чуть-чуть ☺️",
        reply_markup=types.ReplyKeyboardRemove())
    else:
        lotrout.lottery_message(lottery=lottery)
        try:
            photo = f"https://go.telegiv.com/static/images/draws/{customer_id}.{bot_id}.{raffle_id}.jpeg"
            await message.answer_photo(photo, f"<b>{lottery[8]} 🔥</b>\n\n<b>Главные призы розыгрыша:\n{lotrout.main_prize}</b>\n\n<b>Описание розыгрыша 📝</b>\n{lottery[4]}\n\n<b>Дата окончания розыгрыша {datetime.strftime(lottery[7], '%d.%m.%Y в %H:%M')}</b>\n\nНаш робот выберет победителя с помощью рандома. Проверит подписку и сразу же отправит результаты розыгрыша всем участникам.\n\nНажми кнопку <b>Я в деле 👇 </b>",
            reply_markup=play_board)
        except:
            await message.answer(f"<b>{lottery[8]} 🔥</b>\n\n<b>Главные призы розыгрыша:\n{lotrout.main_prize}</b>\n\n<b>Описание розыгрыша 📝</b>\n{lottery[4]}\n\n<b>Дата окончания розыгрыша {datetime.strftime(lottery[7], '%d.%m.%Y в %H:%M')}</b>",
            reply_markup=play_board)
        return scheduler.add_job(remind_push_button, "date", run_date=(datetime.now() + timedelta(minutes=5)), args=(message.from_user.id,))


async def remind_push_button(user_id):
    if await db.button_status(user_id) is not True:
        return await bot.send_message(user_id, "<b>Для участия в розыгрыше подпишись на наш канал</b>\n\nПосле того как ты подпишешься - нажми кнопку <b>🔎 Проверить подписку</b>\n\n🔎 Робот проверит подписку и выдаст лотерейный билет.",
        reply_markup=Subscription_Menu_2)