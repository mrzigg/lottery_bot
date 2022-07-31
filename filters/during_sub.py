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
from menu.inline.during_sub_board import *
from functions.make_links import Channel_link

func = Channel_link()


class DuringSub(BoundFilter):
    
    async def check(self, call: types.CallbackQuery):
        for row in CHANNELS:
            try:
                user_channel_status = await bot.get_chat_member(chat_id=f"@{row}", user_id=call.from_user.id)
                print(user_channel_status)
                if user_channel_status['status'] == "left":
                    func.make_links()
                    await bot.delete_message(call.from_user.id, call.message.message_id)
                    await bot.send_message(call.from_user.id, f"<b>Оеей... Ошибка 🧐</b>\n\nВозможно ты случайно забыл подписаться.Подпишись на наш канал:\n{func.links}\n\nПосле того как ты подпишешься - нажми кнопку <b>Проверить подписку🔎</b>\nРобот всё проверит и выдаст лотерейный билет.",
                    reply_markup=during_sub_board)
                    return False
            except:
                pass
        return True


class DuringSub2(BoundFilter):

    async def check(self, call: types.CallbackQuery):
        for row in CHANNELS:
            try:
                user_channel_status = await bot.get_chat_member(chat_id=f"@{row}", user_id=call.from_user.id)
                if user_channel_status['status'] == "left":
                    func.make_links()
                    await bot.delete_message(call.from_user.id, call.message.message_id)
                    await bot.send_message(call.from_user.id, f"<b>Снова ошибка...</b>\n\nПожалуйста перепроверь подписку\n{func.links}\n\nПосле того как ты подпишешься - нажми кнопку <b>Проверить подписку🔎</b>\n\nРобот всё проверит и выдаст лотерейный билет.",
                    reply_markup=during_sub_board_2)
                    return False
            except:
                pass
        return True
