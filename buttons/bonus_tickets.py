from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import database.lottery_db as lot_db

from config.load_all import dp
from config.bot_name import link
from filters.private_filter import PrivateFilter


@dp.message_handler(PrivateFilter(), text = "🎁 Бонусные билеты")
async def Extra_tickets(message: types.Message):
    if not await lot_db.lottery_exists():
        return await message.answer("<b>Розыгрыш уже завершен.</b>\n\nНо мы уже готовым к запуску новый розыгрыш с безумно крутыми призами!\n\nНужно чуть-чуть подождать 🎁\n\nСовсем чуть-чуть ☺️")
    else:
        return await message.answer(f"<b>Как получить бонусные лотерейные билеты?</b>\n\nЗа каждого приглашённого друга в розыгрыш - ты получаешь бонусные лотерейные билеты 🎫\n\n<b>Сколько 🎫 я  получу за приглашение друзей?</b>\n\n🎫 За первого друга <b>+3</b> билета.\n🎫 За второго <b>+4</b> билета.\n🎫 За третьего <b>+5 </b> билетов.\nИ так до бесконечности...\n\n<b>Как приглашать друзей в розыгрыш?</b>\n👇 Это твоя уникальная ссылка:\n{link}{message.from_user.id}\n\nСкопируй её и отправь друзьям.\nКогда кто-то перейдёт по ней и примет участие в розыгрыше - робот выдаст тебе вознаграждение🎫",
        disable_web_page_preview=True)
