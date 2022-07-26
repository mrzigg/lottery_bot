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
from menu.inline.stage_1_board import stage_board


async def first_stage(user_id):
    info = await progres_db.get_row_function(user_id, "super_game_invites, super_game_to_invite, super_game_duration")
    invites, to_invite, duration = (info[0]+1), info[1], info[2]
    await progres_db.update_function(user_id, "super_game_invites", invites)
    if invites >= to_invite:
        await bot.send_message(user_id, f"<b>ВООУ - КРУТО)</b>\n\nТвой друг принял приглашение)\n\nТы получаешь <b>{duration*10}</b> билетов 🎫")
        await ticket_db.add_tickets(user_id, duration*10)
        await progres_db.update_super_game(user_id, 0, 0)
        tickets = await ticket_db.get_tickets(user_id)
        await asyncio.sleep(3)
        return await bot.send_message(user_id, f'Сейчас у тебя <b>{tickets}</b> лотерейных билетов.\n\nДавай устроим пари 🏆\n\nТы можешь заработать <b>{duration*20}</b> лотерейных билетов или потерять <b>{duration*20-10}</b>.\n\n✅ Условия пари:\n\nЕсли ты пригласишь ещё 1 друга в течении 10 минут, то получишь  <b>{duration*20}</b> лотерейных билетов.\n\nЕсли друг не успеет принять приглашение за 10 минут - ты потеряешь <b>{duration*20-10}</b> лотерейных билетов.\n\n<b>Ты хочешь рискнуть?)</b>\n\nP.S.\nОтсчёт времени начнется сразу после того как нажмешь кнопку <b>"Я в деле!"</b>', reply_markup=stage_board)
    else:
        if (to_invite-invites) == 1:
            sentence = f"Отлично!\n\n+1 приглашение есть!"
        elif (to_invite-invites) == 2:
            sentence = f"+1 приглашение в копилке!"
        elif (to_invite-invites) == 3:
            sentence = f"Твой друг принял приглашение!"
        else:
            sentence = f"1 из {to_invite} приглашений есть!"
            
        return await bot.send_message(user_id, f"<b>{sentence}</b>\n\nДо бонуса в <b>{duration*10}</b> билетов - осталось пригласить всего <b>{to_invite-invites}</b> друга!\n\nСсылка для приглашений:\n{link}{user_id}", disable_web_page_preview=True)