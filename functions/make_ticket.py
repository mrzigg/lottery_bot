import random

class Ticket:

    def make_ticket_prime(self, user_id):
        numbers = str(random.randint(0, 9999)).zfill(4)
        password = str(user_id)
        self.password = password+numbers