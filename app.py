from aiogram.utils import executor
import logging

from config.load_all import dp 
import config.load_all as cfg 

import commands.start
import buttons.start_play
import buttons.i_am_in
import buttons.my_tickets
import buttons.check_subscription
import buttons.age_country
import buttons.bonus_tickets
import buttons.ending_time
import buttons.any_type

logging.basicConfig(format=u'%(filename)+13s [LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO)

async def on_startup(dp):
    await cfg.db.create_pool()
    logging.warning("Database connection is opened")


async def on_shutdown(dp):
    await cfg.db.close()
    logging.warning("Database connection is closed")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)