from random import randint
import logging

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import database.users_db as user_db
import database.lottery_db as lot_db
import database.tickets_db as ticket_db

from filters.channels import CHANNELS
from config.load_all import bot
from database.main_data import customer_id, bot_id, raffle_id
from variables import customer_phone_number, customer_user_name


async def find_winner_function():
    prizes_list = await lot_db.prizes()
    winners_amount = len(prizes_list)
    winners_sp = list()
    upper_bound = await ticket_db.last_ticket()
    winners_tickets = list() 
    while len(winners_sp) >= winners_amount:
        winner_ticket = randint(1, upper_bound)
        winner = await ticket_db.find_winner(winner_ticket) # user_id пользователя, у которого был выбран билет
        for row in CHANNELS:
            user_channel_status = await bot.get_chat_member(chat_id=f"@{row}", user_id=winner)
            main_status = True
            user_state = False
            if user_channel_status['status'] == "left":
                user_state = False
            else:
                user_state = True
            main_status = bool(main_status*user_state)
            if main_status is True:
                winners_tickets.append(winner_ticket)
                winners_sp.append(winner)
            else:
                pass
    i = 0
    while True:
        loosers = await user_db.all_winners(1000*i, winners_sp)
        loosers_sp = list()
        for row in loosers:
            loosers_sp.append(row[0])
            for rows in loosers_sp:
                try:
                    return await bot.send_message(int(rows), f"<b>Розыгрыш завершен!</b>\n\nРезультаты розыгрыша здесь:\n👉 https://go.telegiv.com/results/{customer_id}.{bot_id}.{raffle_id}/\n\nСовсем скоро будет новый розыгрыш и призы будут еще круче 🎁", disable_web_page_preview=True)
                except Exception as e:
                    logging.warning(e)
        if not loosers:
            break
        i += 1
    for row in winners_sp:
        try:
            return await bot.send_message(int(row), f"<b>Розыгрыш завершен!</b>\n\nРезультаты розыгрыша здесь:\n👉 https://go.telegiv.com/results/{customer_id}.{bot_id}.{raffle_id}/\n\nСпойлер: Ты выиграл 🥳\n\nСовсем скоро будет новый розыгрыш!\n\nОбратись сюда, чтобы получить приз:\n<b>@{customer_user_name}\n{customer_phone_number}</b>", disable_web_page_preview=True)
        except Exception as e:
            logging.warning(e)