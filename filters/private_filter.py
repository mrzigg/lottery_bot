from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from menu.inline.check_follow_board import Subscription_Menu_3
from config.load_all import bot

class PrivateFilter(BoundFilter):
    async def check(self, message: types.Message):
        user_channel_status = await bot.get_chat_member(chat_id=-1001576599264, user_id=message.from_user.id)
        if user_channel_status["status"] != 'left':
            return True
        else:
            await bot.send_message(message.from_user.id, '<b>Вы не подписаны на канал❌</b>', reply_markup=Subscription_Menu_3, disable_web_page_preview=True)
            return None