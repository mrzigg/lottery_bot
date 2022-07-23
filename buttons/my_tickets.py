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

@dp.message_handler(PrivateFilter(), text = '🎫 Мои билеты') 
async def Finish_lottery(message: types.Message):
    if not await lot_db.lottery_exists():
        return await message.answer("<b>Розыгрыш уже завершен.</b>\n\nНо мы уже готовым к запуску новый розыгрыш с безумно крутыми призами!\n\nНужно чуть-чуть подождать🎁\n\nСовсем чуть-чуть☺️")
    else:
        await gi.my_tickets(message.from_user.id)
        return await message.answer(f"<b>У тебя {gi.ticket_count} лотерейных билетов:</b>\n\n🎫 {gi.ticket_text}\n\n👉Каждый номерок - это номер твоего лотерейного билета.\nКаждый лотерейный билет - это +1 шанс выиграть приз.\n\n👉 Ты можешь увеличить  количество билетов, пригласив в розыгрыш своих друзей.\n\n👉Просто отправь им эту ссылку:\nhttps://t.me/h0riz4nbot?start={message.from_user.id}",
        disable_web_page_preview=True)