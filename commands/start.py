from aiogram import types
from aiogram.dispatcher.filters import CommandStart

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
from functions.make_ticket import Ticket

tc = Ticket()

@dp.message_handler(CommandStart())
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, f"<b>Привет, @{message.from_user.first_name}👋</b>\nЯ телеграм-бот для проведения мега-крутых розыгрышей. Здесь каждый может стать победителем, включая тебя самого.\n\nЖми кнопку <b>Начать🔥</b> и иди к победе!\n\n<b>Желаю удачи и приятного участия в розыгрыше🍀</b>",
    reply_markup=start_menu)
    args = message.get_args()
    user = await db.user_exists(message.from_user.id)
    if not user:
        await db.add_user(message.from_user.id, message.from_user.id)
        await ticket_db.add_user(message.from_user.id, tickets=list())
        if args == "":
            pass
        else:
            existing_link = await db.find_link(int(args))
            print(existing_link)
            if not existing_link:
                pass
            else:
                ticket = await ticket_db.get_tickets(existing_link[2])
                tc.make_ticket_prime(str(existing_link[2]))
                ticket.append(tc.password)
                await ticket_db.update_function(existing_link[2], ticket, "tickets")
    else:
        pass