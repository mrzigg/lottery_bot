from aiogram import types
from aiogram.dispatcher.filters import CommandStart
import aiogram.utils.markdown as fmt

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import dp, bot
import database.users_db as db
import database.tickets_db as ticket_db
from menu.reply.start_board import start_menu
from menu.reply.user_menu import keyboard


@dp.message_handler(CommandStart())
async def start_command(message: types.Message):
    if not await db.user_exists(message.from_user.id):
        if message.get_args() != "":
            await db.add_user(message.from_user.id, int(message.get_args()))
            existing_link = await db.existing_link(int(message.get_args()))
            if existing_link:
                invites = int(existing_link[10])+int(1)
                for i in range(int(invites+2)):
                    await ticket_db.add_user(existing_link[2])
                try:
                    amount_tickets = await ticket_db.get_tickets(existing_link[2])
                    await bot.send_message(existing_link[2], f"<b>Твой друг принял участие в розыгрыше🥳</b>\n\nЗа это ты получаешь <b>{invites+2}</b> билета\n\nПосмотри пополнение билетов в разделе <b>🎫 Мои билеты</b>\n\nТеперь у тебя {amount_tickets} шансов выиграть приз\nПригласим еще 1 друга?\n<b>Увеличим шансы на победу?</b>\n\nСсылка для приглашений:\nhttps://t.me/h0riz4nbot?start={existing_link[2]}",
                    disable_web_page_preview=True, reply_markup=keyboard)
                except:
                    pass
        else:
            await db.add_user(message.from_user.id, 0)
    return await message.answer(f"<b>Привет, @{fmt.quote_html(message.from_user.username)}👋</b>\nЯ телеграм-бот для проведения мега-крутых розыгрышей. Здесь каждый может стать победителем, включая тебя самого.\n\nЖми кнопку <b>Начать🔥</b> и иди к победе!\n\n<b>Желаю удачи и приятного участия в розыгрыше🍀</b>",
    reply_markup=start_menu)