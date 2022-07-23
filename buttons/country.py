from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import dp, bot
from filters.private_filter import PrivateFilter
import database.users_db as db
import database.tickets_db as ticket_db
from menu.reply.user_menu import keyboard


@dp.callback_query_handler(text_contains="country_")
async def country_callback_data(callback_query: types.CallbackQuery):
    if callback_query.data == "country_belarus":
        await db.update_country(callback_query.from_user.id, "Беларусь")
    elif callback_query.data == "country_ukraine":
        await db.update_country(callback_query.from_user.id, "Украина")
    elif callback_query.data == "country_kazakhstan":
        await db.update_country(callback_query.from_user.id, "Казахстан")
    elif callback_query.data == "country_russia":
        await db.update_country(callback_query.from_user.id, "Россия")
    elif callback_query.data == "country_uzbekistan":
        await db.update_country(callback_query.from_user.id, "Узбекистан")
    elif callback_query.data == "country_any":
        await db.update_country(callback_query.from_user.id, None)
    await callback_query.answer()
    ticket = await ticket_db.add_user(callback_query.from_user.id)
    text = f"<b>Большое спасибо за ответы!</b>\n\nДержи еще <b>+1</b> лотерейный билет\n🎫Номер билета: <b>{ticket}\n</b>Всего лотерейных билетов: <b>4</b>\n\n<i>Этот опрос поможет нам понять, какие призы могут быть максимально интересны в нашем следующем розыгрыше)</i>"
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=text)
    text_2 = f"Кстати, если хочешь <b>увеличить свои шансы на победу</b> в десятки, а то и сотни раз - пригласи своих друзей в этот розыгрыш:\n\nСсылка для приглашений:\nhttps://t.me/h0riz4nbot?start={callback_query.from_user.id}\n\n<b>За каждого друга,</b> принявшего участие в розыгрыше <b>ты получишь</b> бонусные лотерейные билеты 🎫\n\n<i>За первого приглашенного друга ты получишь +3 билета.\nЗа второго +4 билета.\nЗа третьего +5 билетов.\nИ так по нарастающей и до бесконечности</i>\n\nТак что просто отправь эту ссылку своему другу - и твои шансы на победу увеличатся в 2 раза😎"
    await bot.send_message(callback_query.from_user.id, text_2, disable_web_page_preview=True, reply_markup=keyboard)