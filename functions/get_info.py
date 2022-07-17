from datetime import datetime

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import database.lottery_db as lot_db
import database.tickets_db as tick_db

class Giving_information:

    def __init__(self):
        pass

    async def getting_information(self, user_id):       
        self.date = datetime.strftime(await lot_db.get_date(), '%d.%m.%Y в %H:%M')
        
        self.tickets_sp = await tick_db.get_tickets(user_id)

        if len(self.tickets_sp) != 0:
            self.tickets_amount = len(self.tickets_sp)
        else:
            self.tickets, self.tickets_amount = "", 0

    async def my_tickets(self, user_id):
        ticket_sp = await tick_db.get_tickets(user_id)

        self.user_ticket_amount, self.user_tickets = len(ticket_sp), ""
        
        for row in ticket_sp:
            self.user_tickets += f"🎫{str(row)}\n"