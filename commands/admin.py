from aiogram.dispatcher.filters import Command
from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from filters.channels import CHANNELS
from config.load_all import dp, bot


@dp.message_handler(Command("admin", ignore_caption=False))
async def check_for_admin(message: types.Message):
    channels_not_supported = list()
    for row in CHANNELS:
        try:
            user_channel_status = await bot.get_chat_member(chat_id=f"@{row}", user_id=message.from_user.id)
        except Exception as e:
            channels_not_supported.append(row)

    if len(channels_not_supported) > 0:
        channels_text = ""
        for row in channels_not_supported:
            channels_text += f"@{row}\n"
        return await bot.send_message(message.from_user.id, f"К таким каналам я не имею админки❌\n\n<b>{channels_text}</b>")
    else:
        return await bot.send_message(message.from_user.id, "<b>Всё отлично! Ко всем каналам имею доступ✅</b>")