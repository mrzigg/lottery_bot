from aiogram import types
import asyncio

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import dp, bot
import database.lottery_db as lot_db
import database.users_db as db
from menu.inline.play_board import keyboard
import menu.inline.follower_board as follow_board


@dp.message_handler(text="Начать🔥")
async def start_play_message(message: types.Message):
    lottery = await lot_db.lottery_exists()
    if not lottery:
        await bot.send_message(message.from_user.id, "<b>Розыгрыш уже завершен.</b>\n\nНо мы уже готовым к запуску новый розыгрыш с безумно крутыми призами!\n\nНужно чуть-чуть подождать🎁\n\nСовсем чуть-чуть☺️",
        reply_markup=types.ReplyKeyboardRemove())
    else:
        photo = await lot_db.photo_exists()
        if not photo:
            await bot.send_message(message.from_user.id, f"<b>Главный приз розыгрыша: {lottery[3]}🔥</b>\n\n<b>Описание розыгрыша📝</b>\n{lottery[4]}\n\n<b>Правила участия❗️</b>\n{lottery[5]}\n\n<b>Дата окончания розыгрыша {lottery[6]}</b>",
            reply_markup=keyboard)
        else:
            await bot.send_photo(message.from_user.id, lottery[8], f"<b>Главный приз розыгрыша: {lottery[3]}🔥</b>\n\n<b>Описание розыгрыша📝</b>\n{lottery[4]}\n\n<b>Дата окончания розыгрыша {lottery[7]}</b>\n\nНаш робот выберет победителя с помощью рандома. Проверит подписку и сразу же отправит результаты розыгрыша всем участникам.\n\nНажми кнопку <b>Я в деле👇 </b>",
            reply_markup=keyboard)
            await remind_push_button(message.from_user.id)


async def remind_push_button(user_id):
    await asyncio.sleep(300)
    status = await db.button_status(user_id)
    if status is True:
        pass
    else:
        await bot.send_message(user_id, "<b>Для участия в розыгрыше подпишись на наш канал</b>\n\nПосле того как ты подпишешься - нажми кнопку <b>🔎Проверить подписку</b>\n\n🔎Робот проверит подписку и выдаст лотерейный билет.",
        reply_markup=follow_board.keyboard)