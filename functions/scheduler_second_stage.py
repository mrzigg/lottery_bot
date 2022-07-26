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
from menu.reply.user_menu import keyboard
from menu.inline.stage_2_board import stage_2_board


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
        await ticket_db.delete_tickets(user_id, (duration*20-10)) 
        return await bot.send_message(user_id, f"<b>К сожалению, в этом пари ты не смог выиграть.</b>\n\nКак мы и договорились - ты теряешь <b>{duration*20-10}</b> лотерейных билетов.\n\nСейчас их у тебя <b>{tickets-(duration*20-10)}</b> 🎫\nНо не переживай, отыграться ты сможешь чуть позже 😎")
    else:
        await ticket_db.add_tickets(user_id, duration*20)
        await bot.send_message(user_id, f'<b>Воу воу воу!!!</b>\n\nТвой друг принял приглашение, а это значит... ЧТО?\n\n<b>Ты выиграл в этом пари!</b>\n\nКак и договаривались: ты получаешь <b>{duration*20}</b> лотерейных билетов.\n\nСейчас у тебя: <b>{tickets+duration*20}</b> билетов 🎫\n\nКстати, все номера лотерейных билетов ты сможешь посмотреть, перейдя в раздел меню <u>"Мои билеты" </u>', reply_markup=keyboard)
        await asyncio.sleep(3)
        return await bot.send_message(user_id, f"<b>Предлагаю поднять ставки 😎</b>\n\nНо это последняя игра на сегодня)\n\nТы можешь выиграть или проиграть <b>{duration*40}</b> лотерейных билетов.\n\n✅ Условия:\n\nЗа 10 минут нужно пригласить <b>{duration*2}</b> человек.\n\n<b>Ты в деле или всё же пас?</b>", reply_markup=stage_2_board)