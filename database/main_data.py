import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from variables import customer_id, bot_id, raffle_id


customer_id = customer_id
bot_id = bot_id
raffle_id = raffle_id