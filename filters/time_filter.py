from aiogram.dispatcher.filters import BoundFilter
from datetime import datetime
from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import bot
from variables import end_timestamp
from menu.inline.during_sub_board import *
from functions.make_links import Channel_link

func = Channel_link()


class TimeFilter(BoundFilter):
    async def check(self, message: types.Message):
        if datetime.now() >= end_timestamp:
            await bot.send_message(message.from_user.id, "<b>Розыгрыш уже завершен.</b>\n\nНо мы уже готовым к запуску новый розыгрыш с безумно крутыми призами!\n\nНужно чуть-чуть подождать 🎁\n\nСовсем чуть-чуть☺️",
        reply_markup=types.ReplyKeyboardRemove())
            return False
        else:
            return True