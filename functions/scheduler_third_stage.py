import asyncio

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
from menu.inline.stage_3_board import stage_3_board


async def five_minutes(user_id):
    return await bot.send_message(user_id, "<b>⏳Половина времени пройдена!</b>\nА это значит, что сейчас становится всё ещё интереснее 😅")


async def eight_minutes(user_id):
    return await bot.send_message(user_id, "<b>Оёёй!</b>\n⌛Осталось совсем чуть-чуть 😯")


async def eleven_minutes(user_id):
    info = await progres_db.get_row_function(user_id, "super_game_invites, super_game_to_invite, super_game_duration")
    invites, to_invite, duration = info[0], info[1], info[2]
    tickets = await ticket_db.get_tickets(user_id)
    await progres_db.update_super_game(user_id, 0, 0)
    if invites < to_invite:
        await ticket_db.delete_tickets(user_id, (duration*40-10))
        return await bot.send_message(user_id, f"<b>К сожалению, в этом пари ты не смог выиграть.</b>\nКак мы и договорились - ты теряешь {duration*40-10} лотерейных билетов.\nСейчас их у тебя <b>{tickets-(duration*40-10)}</b> 🎫\nНо не переживай, отыграться ты сможешь чуть позже 😎")
    else:
        percents = (74, 76, 81, 82, 84, 86, 83, 86, 88, 87, 89, 90, 92, 93)
        await ticket_db.add_tickets(user_id, duration*40)
        await bot.send_message(user_id, f"<b>Мы снимаем шляпу)</b> 🥳\n\nТы сделал <b>{duration*2}</b> из <b>{duration*2}</b> приглашений меньше чем за 10 минут. Это очень круто!\n\nМы тебе проиграли кучу билетов ... Но уговор есть уговор 😁\n\nДержи <b>{duration*40}</b> лотерейных билетов 🎫")
        await asyncio.sleep(3)
        await bot.send_message(user_id, f"<b>Сейчас у тебя {tickets+duration*40} лотерейных билетов </b> 🎫\n\nЭто больше, чем у <b>{percents[duration-1]}%</b> участников данного розыгрыша - очень круто.\n\nХочешь получить больше шансов для победы?\nПригласи <b>+1</b> друга и получи дополнительные билеты🎫\n\nСсылка для приглашений:\n{link}{user_id}", disable_web_page_preview=True)
        if duration >=5:
            await asyncio.sleep(3)
            return await bot.send_message(user_id, f"<b>ФИНАЛЬНАЯ СУПЕР ИГРА</b> 🎰\n\nТы можешь выиграть <b>500</b> лотерейных билетов, пригласив всего +5 человек за 60 минут.\nИли потеряешь 250 билетов.\n\n{link}{user_id}\n\nХочешь сыграть?", disable_web_page_preview=True, reply_markup=stage_3_board)