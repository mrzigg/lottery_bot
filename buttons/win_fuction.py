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

from config.load_all import bot
from database.main_data import customer_id, bot_id, raffle_id


async def find_winner_function():
    prizes_list = await lot_db.prizes()
    winners_amount = len(prizes_list)
    winners_sp = list()
    upper_bound = await ticket_db.last_ticket()
    winners_tickets = list() 
    for i in range(winners_amount):
        winner_ticket = randint(1, upper_bound)
        winner = await ticket_db.find_winner(winner_ticket)
        winners_tickets.append(winner_ticket)
        winners_sp.append(winner)
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
            return await bot.send_message(int(row), f"<b>Розыгрыш завершен!</b>\n\nРезультаты розыгрыша здесь:\n👉 https://go.telegiv.com/results/{customer_id}.{bot_id}.{raffle_id}/\n\nСпойлер: Ты выиграл 🥳\n\nСовсем скоро будет новый розыгрыш!", disable_web_page_preview=True)
        except Exception as e:
            logging.warning(e)