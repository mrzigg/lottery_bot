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
from menu.reply.user_menu import keyboard
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
            existing_link = await ticket_db.existing_link(int(args))
            print(existing_link)
            if not existing_link:
                pass
            else:
                invites = int(existing_link[7])+int(1)
                ticket, tickets_sp = existing_link[6], ""
                await ticket_db.update_invites(existing_link[3], invites)
                for i in range(int(invites+2)):
                    tc.make_ticket_prime(str(existing_link[3]))
                    tickets_sp += f"🎫 {str(tc.password)}\n"
                    ticket.append(tc.password)
                await ticket_db.update_function(existing_link[3], ticket, "tickets")
                await bot.send_message(existing_link[3], f"<b>Твой друг принял участие в розыгрыше🥳</b>\n\nЗа это ты получаешь <b>{invites+2}</b> билета\n\nНомера билетов:\n{tickets_sp}\n\nТеперь у тебя {len(ticket)} шансов выиграть приз\nПригласим еще 1 друга?\n<b>Увеличим шансы на победу?</b>\n\nСсылка для приглашений:\nhttps://t.me/h0riz4nbot?start={existing_link[3]}",
                disable_web_page_preview=True, reply_markup=keyboard)
    else:
        pass