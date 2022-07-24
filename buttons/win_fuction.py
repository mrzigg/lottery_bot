from aiogram import types
from random import randint

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import dp, bot
import database.lottery_db as lot_db
import database.users_db as user_db
import database.tickets_db as ticket_db


async def find_winner_function():
    winners_amount = len(await lot_db.prizes())
    winners_sp = list()
    upper_bound = await ticket_db.last_ticket()
    winners_tickets = list()
    for i in range(winners_amount):
        winner_ticket = int(str(randint(0, upper_bound)).zfill(4))
        winner = await ticket_db.find_winner(winner_ticket)
        winners_tickets.append(winner_ticket)
        winners_sp.append(winner)
    users_sp = list()
    for i  in range(winners_amount):
        winners = await user_db.all_winners(i*100)
        if winners is None:
            break
        else:
            for row in winners:
                users_sp.append(row[0])
        print(i)
    last_list = users_sp - winners_sp
    for row in winners_sp:
        await bot.send_message(int(row), "Поздравляю Вы победили")


    