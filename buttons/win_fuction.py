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
import database.tickets_db as ticket_db


async def find_winner_function():
    upper_bound = await ticket_db.last_ticket()
    ticket = int(str(randint(0, upper_bound)).zfill(4))
    winners = len()