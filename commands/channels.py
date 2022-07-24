from aiogram import types
from aiogram.dispatcher.filters import Command

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import dp
from functions.make_links import Channel_link
from menu.reply.user_menu import keyboard
from filters.time_filter import TimeFilter

func = Channel_link()

@dp.message_handler(TimeFilter(), Command("channels", ignore_caption=False))
async def channels_command(message: types.Message):
    func.make_links()
    await message.answer(f"Привет, {message.from_user.first_name}👋\n\nВижу тебе интересно на какие каналы надо быть подписаным, чтобы победить в розыгрыше?🧐\n\nНу, раз тебе интересно, то вот😉\n{func.links}",
    reply_markup=keyboard)
    return await message.answer_sticker("CAACAgIAAxkBAAEFXRFi3Jo1GHiP4Eo0n66P0RIEp3P1WwAC1xkAAmIGcEmfFezVajtprSkE")