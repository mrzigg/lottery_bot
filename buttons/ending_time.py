from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import dp
from filters.private_filter import PrivateFilter
from functions.get_info import Giving_information
import database.lottery_db as lot_db

gi = Giving_information()

@dp.message_handler(PrivateFilter(), text = '⏰ Когда закончится розыгрыш') 
async def Finish_lottery(message: types.Message):
    if not await lot_db.lottery_exists():
        return await message.answer("<b>Розыгрыш уже завершен.</b>\n\nНо мы уже готовым к запуску новый розыгрыш с безумно крутыми призами!\n\nНужно чуть-чуть подождать🎁\n\nСовсем чуть-чуть☺️")
    else:
        await gi.getting_information(message.from_user.id)
        return await message.answer(f'<b>Розыгрыш завершится:</b>\n\n🗓 {gi.date}\n\n<b>Как будет выбран победитель?</b>\n\nПобедитель будет выбран нашим роботом автоматически и без малейшего вмешательства людей.\n\n👉Робот берёт все выданные лотерейные билеты.\n👉С помощью рандома выбирает выигрышный номерок.\n👉Смотрит, у кого лотерейный билет с выигрышным номерком.\n👉Проверяет, выполнил ли победитель условия розыгрыша.\n👉Если условия не выполнены, то идёт "перерозыгрыш"\n👉А если всё "ОК", то робот отправляет результаты розыгрыша всем участникам.\n\nНа данный момент у тебя <b>{gi.tickets_amount}</b> лотерейных билетов🎫\nЭто <b>{gi.tickets_amount}</b> шансов на победу.\n\nПригласив в розыгрыш своих друзей - ты можешь в десятки раз увеличить свои шансы на победу.\n\n👉 Просто отправь им эту ссылку:\nhttps://t.me/h0riz4nbot?start={message.from_user.id}',
        disable_web_page_preview=True)