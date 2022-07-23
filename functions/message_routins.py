from aiogram import types
import asyncio

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import bot 

class Routins:

    def __init__(self):
        pass

    async def routin_callback(self, callback_query: types.CallbackQuery):
        await callback_query.answer()
        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        await bot.send_chat_action(callback_query.from_user.id, types.ChatActions.TYPING)
        await asyncio.sleep(3)

    async def edit_callback(self, call: types.CallbackQuery):
        await call.answer()
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)

    async def edit_call_text(self, callback_query: types.CallbackQuery, text):
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=text)
        await bot.send_chat_action(callback_query.from_user.id, types.ChatActions.TYPING)
        await asyncio.sleep(3)