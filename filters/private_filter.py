from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from .channels import CHANNELS

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import bot

class PrivateFilter(BoundFilter):
    async def check(self, message: types.Message):
        status = bool(True)
        user_status = bool(False)
        for row in CHANNELS:
            user_channel_status = await bot.get_chat_member(chat_id=f"@{row}", user_id=message.from_user.id)
            if user_channel_status['status'] == "left":
                user_status = bool(False)
            else:
                user_status = bool(True)
            status = bool(status*user_status)
        if status is True:
            return True
        else:
            links = ""
            for row in CHANNELS:
                links += f"@{row}\n"
            await bot.send_message(message.from_user.id, f'<b>Вы не подписаны на канал❌</b>\n{links}')
            return None