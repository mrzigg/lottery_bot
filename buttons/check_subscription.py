from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import database.users_db as db
import database.tickets_db as ticket_db

from config.load_all import dp, bot
from filters.during_sub import DuringSub
from menu.inline.age_board import age_board
from functions.message_routins import Routins
from menu.inline.gender_board import gender_board


@dp.callback_query_handler(DuringSub(), text="check_in")
async def callback_check_in(callback_query: types.CallbackQuery):
    await db.update_button_2(callback_query.from_user.id)
    ticket = await ticket_db.add_user(callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, f"<b>Отлично!</b>\nРобот всё проверил - всё отлично)\n\n<b>Теперь ты участник розыгрыша!</b>\n\n🎫 Номер лотерейного билета: <b>{ticket}</b>", reply_markup=types.ReplyKeyboardRemove())
    await Routins.routin_callback(callback_query=callback_query) 
    return await bot.send_message(callback_query.from_user.id, "Кстати, ты можешь получить <b>+1 лотерейный билет!</b>\n\n<b>Просто ответь на вопрос:</b> Ты парень или девушка?\n\n<i>P.S.Твои ответы позволят нам понять, как в следующий раз сделать розыгрыш еще интереснее)</i>",
    reply_markup=gender_board)


@dp.callback_query_handler(text_contains="gender_")
async def gender_message(callback_query: types.CallbackQuery):
    if callback_query.data == "gender_male":
        await db.update_gender(callback_query.from_user.id, True)
    else:
        await db.update_gender(callback_query.from_user.id, False)
    ticket = await ticket_db.add_user(callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, f"<b>Воу, это круто ☺️</b>\n\nДержи +1 лотерейный билет\n🎫 Номер: {ticket}\n\nТеперь у тебя <b>2</b> лотерейных билета.\n\nОтветь на вопрос - получи еще <b>+1</b>.", reply_markup=types.ReplyKeyboardRemove())
    await Routins.routin_callback(callback_query=callback_query)
    return await bot.send_message(callback_query.from_user.id, "<b>Сколько тебе лет?</b>", reply_markup=age_board)