from aiogram.dispatcher.filters import Command
from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import dp
from menu.reply.user_menu import keyboard
from filters.time_filter import TimeFilter
from functions.make_links import Channel_link

func = Channel_link()


@dp.message_handler(TimeFilter(), Command("channels", ignore_caption=False))
async def channels_command(message: types.Message):
    func.make_links()
    await message.answer(f"<b>Спонсоры розыгрыша:</b>\n{func.links}\n\nP.S.\nУчастники розыгрыша без подписки на каналы спонсоров теряют возможность участия в розыгрыше.",
    reply_markup=keyboard)