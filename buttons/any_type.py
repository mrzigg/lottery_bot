from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import dp
from menu.reply.user_menu import keyboard


@dp.message_handler(content_types=['text', 'photo', 'video', 'document'])
async def any_types(message: types.Message):
        await message.answer_sticker("CAACAgIAAxkBAAEFNL1ixaSNz_r0m1Sd0Mg6dF55Shb3twACAgEAAladvQpO4myBy0Dk_ykE")
        return await message.answer("<b>Я тебя не понимаю❌</b>",reply_markup=keyboard)