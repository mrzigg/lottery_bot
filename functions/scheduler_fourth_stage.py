import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import database.tickets_db as ticket_db
import database.raffle_progresses_db as progres_db

from config.load_all import bot
from config.bot_name import link


async def five_minutes(user_id):
    return await bot.send_message(user_id, f"<b>Время уже идёт)</b>\n⏰ До конца пари осталось <b>55</b> минут.\n\nОтправь эту ссылку друзьям:\n{link}{user_id}", disable_web_page_preview=True)


async def thirty_minutes(user_id):
    return await bot.send_message(user_id, f"⏳ <b>Половина времени пройдена!</b>\nКак думаешь, ты справишься?\n\nОтправь эту ссылку друзьям:\n{link}{user_id}", disable_web_page_preview=True) 


async def fifty_minutes(user_id):
    return await bot.send_message(user_id, f"<b>Оёёй! Осталось совсем чуть-чуть!</b>\n⌛ <b>50</b> минут уже прошло.\nОсталось всего <b>10</b> минут 😰\n\nОтправь эту ссылку друзьям:\n{link}{user_id}", disable_web_page_preview=True)


async def sixty_one_minutes(user_id):
    info = await progres_db.get_function(user_id, "super_game_invites, super_game_to_invite")
    invites, to_invite = info[0], info[1]
    tickets = await ticket_db.get_tickets(user_id)
    if invites < to_invite:
        await ticket_db.delete_tickets(user_id, 250)
        return await bot.send_message(user_id, f"<b> К сожалению, в этом пари выиграть не получилось.</b>\n\nКак мы и договорились - ты теряешь 250 лотерейных билетов.\n\nСейчас у тебя: <b>{tickets-250}</b> 🎫\n\nНо не переживай, ты сможешь отыграться чуть позже!")
    else:
        await progres_db.update_super_game(user_id, 0, 0)
        await ticket_db.add_tickets(user_id, 500)
        return await bot.send_message(user_id, f"<b>Да!!!!Это победа 🥳</b>\n\nТы только что выиграл <b>500</b> лотерейных билетов!\n\n🎫 Сейчас у тебя <b>{tickets+500}</b> билетов!\n\nТолько что ты вошёл в топ 10 участников розыгрыша с самым большим количеством лотерейных билетов.\n\nЭто значит шанс на победу... Ооочень большой 😅")