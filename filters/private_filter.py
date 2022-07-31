from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from .channels import CHANNELS

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import bot
from functions.make_links import Channel_link

func = Channel_link()


class PrivateFilter(BoundFilter):

    async def check(self, message: types.Message):
        for row in CHANNELS:
            try:
                user_channel_status = await bot.get_chat_member(chat_id=f"@{row}", user_id=message.from_user.id)
                if user_channel_status['status'] == "left":
                    func.make_links()
                    await bot.send_message(message.from_user.id, f'<b>Убедитесь, что Вы подписаны на эти каналы ❌</b>\n{func.links}')
                    return False
            except:
                pass
        return True