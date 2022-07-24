from aiogram.utils.executor import start_webhook
import logging

from variables import end_timestamp
from config.load_all import dp, scheduler
import config.load_all as cfg

import commands.start
import commands.channels
import commands.raffle
import buttons.start_play
import buttons.i_am_in
import buttons.my_tickets
import buttons.check_subscription
import buttons.sub_during
import buttons.age
import buttons.country
import buttons.bonus_tickets
import buttons.ending_time

from functions.sending_message import *
from buttons.win_fuction import find_winner_function

logging.basicConfig(format=u'%(filename)+13s [LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO)

async def on_startup(dp):
    await bot.set_webhook(cfg.WEBHOOK_URL)
    scheduler.start()
    logging.warning("AsyncIOScheduler is active")
    await cfg.db.create_pool()
    logging.warning("Database connection is opened")
    scheduler.add_job(find_winner_function, run_date=end_timestamp)
    scheduler.add_job(sending_message, "interval", days=1)
    logging.warning("Sending tasks is active")


async def on_shutdown(dp):
    logging.warning('Shutting down...')
    await bot.delete_webhook()
    logging.warning('Bye!')
    scheduler.shutdown()
    logging.warning("AsyncIOScheduler is anactive")
    await cfg.db.close()
    logging.warning("Database connection is closed")


if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=cfg.WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=False,
        host=cfg.WEBAPP_HOST,
        port=cfg.WEBAPP_PORT
    )
