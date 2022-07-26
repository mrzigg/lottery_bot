from aiogram.dispatcher.filters import CommandStart
import aiogram.utils.markdown as fmt
from aiogram import types

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import database.users_db as db
import database.raffle_progresses_db as progres_db

from config.load_all import dp
from filters.time_filter import TimeFilter
from menu.reply.user_menu import keyboard
from functions.zero_stage import zero_stage
from functions.first_stage import first_stage
from functions.third_stage import third_stage
from menu.reply.start_board import start_menu
from functions.fourth_stage import fourth_stage
from functions.three_days import invite_message
from functions.tomorrow import invite_message_tomorrow


@dp.message_handler(TimeFilter(), CommandStart())
async def start_command(message: types.Message):
    if not await db.user_exists(message.from_user.id):
        if message.get_args() != "":
            await db.add_user(message.from_user.id, int(message.get_args()))
            await progres_db.add_user(message.from_user.id)
            existing_link = await db.existing_link(int(message.get_args()))
            if existing_link:
                info = await progres_db.get_row_function(existing_link[2], "super_game_stage, invites")
                stage, invites = info[0], (info[1]+1)
                await progres_db.update_function(existing_link[2], "invites", invites)
                if stage == 0:
                    await zero_stage(existing_link[2], invites)
                elif stage == 1:
                    await first_stage(existing_link[2])
                elif stage == 2:
                    invites = await progres_db.get_function(existing_link[2], "super_game_invites") + 1
                    await progres_db.update_function(existing_link[2], "super_game_invites", invites)
                elif stage == 3:
                    await third_stage(existing_link[2])
                elif stage == 4:
                    await fourth_stage(existing_link[2]) 
                elif stage == 5:
                    await invite_message(existing_link[2], invites)
                else:
                    await invite_message_tomorrow(existing_link[2], invites)
        else:
            await db.add_user(message.from_user.id, 0)
            await progres_db.add_user(message.from_user.id)
        return await message.answer(f"<b>Привет, @{fmt.quote_html(message.from_user.username)} 👋</b>\nЯ телеграм-бот для проведения мега-крутых розыгрышей.Здесь каждый может стать победителем, включая тебя самого.\n\nЖми кнопку <b>Начать 🔥</b> и иди к победе!\n\n<b>Желаю удачи и приятного участия в розыгрыше 🍀</b>",
        reply_markup=start_menu)   
    else:
        return await message.answer(f"<b>Привет, @{fmt.quote_html(message.from_user.username)} 👋</b>\nЯ телеграм-бот для проведения мега-крутых розыгрышей.Здесь каждый может стать победителем, включая тебя самого.\n\n<b>Желаю удачи и приятного участия в розыгрыше 🍀</b>",
        reply_markup=keyboard)
