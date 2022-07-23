from aiogram import types
import asyncio

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config.load_all import bot
import database.tickets_db as db

class MakeTickets:

    async def make_ten_tickets(self, user_id):
        id = await db.ten_tickets(user_id)
        self.id_list = ""
        for row in id:
            self.id_list += f"{str(row[0])}, "