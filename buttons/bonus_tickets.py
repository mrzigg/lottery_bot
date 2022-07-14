from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import dp, bot
from filters.private_filter import PrivateFilter
from functions.get_info import Giving_information
import database.lottery_db as lot_db

gi = Giving_information()

@dp.message_handler(PrivateFilter(), text = "🎁 Бонусные билеты")
async def Extra_tickets(message: types.Message):
    lottery = await lot_db.lottery_exists()
    if not lottery:
        await bot.send_message(message.from_user.id, "<b>Розыгрыш уже завершен.</b>\n\nНо мы уже готовым к запуску новый розыгрыш с безумно крутыми призами!\n\nНужно чуть-чуть подождать🎁\n\nСовсем чуть-чуть☺️")
    else:
        link = "https://t.me/h0riz4nbot?start=" + str(message.from_user.id)
        await bot.send_message(message.from_user.id, f"<b>Как получить бонусные лотерейные билеты?</b>\n\nЗа каждого приглашённого друга в розыгрыш - ты получаешь бонусные лотерейные билеты 🎫\n\n<b>Сколько 🎫 я  получу за приглашение друзей?</b>\n\n🎫 За первого друга <b>+3</b> билета.\n🎫 За второго <b>+4</b> билета.\n🎫 За третьего <b>+5 </b> билетов.\nИ так до бесконечности...\n\n<b>Как приглашать друзей в розыгрыш?</b>\n\n👇Это твоя уникальная  ссылка:\n{link}\n\nСкопируй её и отправь друзьям.\nКогда кто-то перейдёт по ней и примет участие в розыгрыше - робот выдаст тебе вознаграждение🎫",
        disable_web_page_preview=True)