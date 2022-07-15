import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import database.lottery_db as lot_db
import database.users_db as user_db
import database.tickets_db as tick_db


class Giving_information:

    def __init__(self):
        pass

    async def getting_information(self, user_id):       
        self.datetime = str(await lot_db.get_date())
        self.date = self.datetime[8:10] + "." + self.datetime[5:7] + "." + self.datetime[:4] + " в " + self.datetime[11:16]
        
        self.tickets_sp = str(await tick_db.get_tickets(user_id)).replace("[", "").replace("]", "")

        if len(self.tickets_sp) != 0:
            self.tickets = str(await tick_db.get_tickets(user_id)).replace("[", "").replace("]", "")
            self.tickets_amount = len(self.tickets_sp)
        else:
            self.tickets, self.tickets_amount = "", 0