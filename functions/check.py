import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import database.users_db as db

from config.load_all import bot
from menu.inline.check_follow_board import *


class Checking:

    async def thirty_minutes(self, user_id):
        if await db.get_button_status(user_id) is not True:
            return await bot.send_message(user_id, "<b>От участия в розыгрыше, тебя отделяет всего несколько кликов 🙁\n\nДавай это исправим 😀\n\nИсправим? 😀</b>", reply_markup=Subscription_Menu1)

    async def two_hours(self,user_id): 
        if await db.get_button_status(user_id) is not True:
            return await bot.send_message(user_id, "<b>Мега предложение!</b>\n\nПодпишись и получи в 10 раз больше лотерейных билетов, чем все остальные.\n\nСистема выдаст тебе 10 лотерейных билетов, вместо 1.", reply_markup=Participation_Menu)

    async def three_days(self, user_id, prize):
        if await db.get_button_status(user_id) is not True:
            return await bot.send_message(user_id, f"<b>До завершения розыгрыша осталось 3 дня!</b>\n\nТак что сейчас, самое время принять участие и выиграть, ведь главные призы:\n {prize}\n\nПодпишись и получи в <b>10</b> раз больше лотерейных билетов, чем все остальные.\n\nСистема выдаст тебе 10 лотерейных билетов, вместо 1.", reply_markup=Participation_Menu)

    async def today(self, user_id, prize):
        if await db.get_button_status(user_id) is not True:
            return await bot.send_message(user_id, f"<b>Через 24 часа наш робот выберет кто же выиграет:\n{prize} </b>\n\nУспей запрыгнуть в последний вагон и получи шанс на победу)", reply_markup=Participation_Menu)