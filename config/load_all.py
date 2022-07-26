from .bot_config import TOKEN
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from database.database_connect import Database


scheduler = AsyncIOScheduler()
db = Database()
bot = Bot(TOKEN, parse_mode="html")
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())