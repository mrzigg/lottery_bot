import logging
from aiogram import types
from random import randint

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import bot
import database.lottery_db as lot_db
import database.users_db as user_db
import database.tickets_db as ticket_db


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
                    tickets_text = ', '.join(winner_ticket)
                    await bot.send_message(int(rows), f"<b>Привет👋</b>\n\nПо окончанию розыгрыша, я считаю важным проинформировать кажодго об этом\n\nПобедителями являются обладателями данных билетов:\n🎫 {tickets_text}\n\n<b>Ждём тебя в следующем розыгрыше☺️</b>")
                except Exception as e:
                    logging.warning(e)
                    pass
        if not loosers:
            break
        i += 1
    for row in winners_sp:
        try:
            prizes_text = ""
            for row in prizes_list:
                prizes_text += f"🎁 {row}\n"
            await bot.send_message(int(row), f"<b>Привет👋</b>\n\n<b>Ты являешься победителем!\nИ это не шутки</b>\n\nОдин из призов уйдёт тебе. Поэтому можешь насладиться этим моментом, а я тебе напоминаю, о призах розыгрыша:\n{prizes_text}")
            await bot.send_sticker(int(row), "CAACAgIAAxkBAAEFXW5i3SDXYQABm931LEF5UPb13Ctdg30AAg0BAAJWnb0KRv1DHQVE15cpBA")
        except Exception as e:
            logging.warning(e)
            pass
