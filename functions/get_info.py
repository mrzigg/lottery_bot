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

    async def getting_information(self, user_id):       
        self.date = datetime.strftime(await lot_db.get_date(), '%d.%m.%Y в %H:%M')    
        self.tickets_amount = await tick_db.get_tickets(user_id)

    async def my_tickets(self, user_id):
        tickets = await tick_db.all_tickets(user_id)
        ticket = list()
        for row in tickets: 
            ticket.append(str(row[0]))
        self.ticket_text = ', '.join(ticket)
        self.ticket_count = len(ticket)