from random import randint

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import database.tickets_db as ticket_db


class Ticket:

    async def make_ticket_prime(self, user_id):
        numbers = str(randint(0, 9999)).zfill(4)
        password = str(user_id)
        self.password = int(password+numbers)

    async def updating_db(self, user_id, counter):
        ticket = await ticket_db.get_tickets(user_id)
        self.ticket_sp = list()
        for i in range(counter):
            await self.make_ticket_prime(user_id) 
            ticket.append(self.password)
            self.ticket_sp.append(str(self.password))
        await ticket_db.update_function(user_id, ticket, "tickets")
        self.ticket_sp = ", ".join(self.ticket_sp)