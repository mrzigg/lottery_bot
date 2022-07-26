import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import database.tickets_db as ticket_db

from config.load_all import bot
from config.bot_name import link
from menu.reply.user_menu import keyboard


async def zero_stage(user_id, invites):
    await ticket_db.add_tickets(user_id, invites+2)
    tickets = await ticket_db.get_tickets(user_id)
    return await bot.send_message(user_id, f"<b>Твой друг принял участие в розыгрыше 🥳</b>\n\nЗа это ты получаешь <b>{invites+2}</b> билета\n\nПосмотри пополнение билетов в разделе <b>🎫 Мои билеты</b>\n\nТеперь у тебя {tickets} шансов выиграть приз\nПригласим еще 1 друга?\n<b>Увеличим шансы на победу?</b>\n\nСсылка для приглашений:\n{link}{user_id}",
    disable_web_page_preview=True, reply_markup=keyboard)